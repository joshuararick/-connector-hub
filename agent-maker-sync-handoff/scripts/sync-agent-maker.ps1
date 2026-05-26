param(
    [Parameter(Mandatory=$true)]
    [string]$TargetRepo,

    [string]$SourceDir = "$(Split-Path -Parent $PSScriptRoot)\source_drop_here",

    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Write-Step($Message) {
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Assert-Command($Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

Assert-Command git

$TargetRepo = [System.IO.Path]::GetFullPath($TargetRepo)
$SourceDir = [System.IO.Path]::GetFullPath($SourceDir)

Write-Step "Checking target repo: $TargetRepo"
if (-not (Test-Path $TargetRepo)) {
    if ($DryRun) {
        Write-Host "DRY RUN: Would create target directory $TargetRepo"
    } else {
        New-Item -ItemType Directory -Path $TargetRepo | Out-Null
    }
}

if (-not (Test-Path (Join-Path $TargetRepo ".git"))) {
    Write-Step "Initializing Git repo"
    if (-not $DryRun) {
        git -C $TargetRepo init
    }
}

Write-Step "Checking source drop: $SourceDir"
if (-not (Test-Path $SourceDir)) {
    throw "Source directory does not exist: $SourceDir"
}

$sourceFiles = Get-ChildItem -Path $SourceDir -Recurse -File -Force | Where-Object {
    $_.FullName -notmatch "\\.git(\\|$)" `
        -and $_.Name -ne ".gitkeep" `
        -and $_.Name -ne "Sync Setup Assistance.txt"
}

if ($sourceFiles.Count -eq 0) {
    Write-Host "No Agent Maker source project files found in source_drop_here/. Nothing to import yet." -ForegroundColor Yellow
} else {
    Write-Step "Copying source files into target repo"
    foreach ($file in $sourceFiles) {
        $sourceRoot = New-Object System.Uri(($SourceDir.TrimEnd('\') + '\'))
        $fileUri = New-Object System.Uri($file.FullName)
        $relative = [System.Uri]::UnescapeDataString($sourceRoot.MakeRelativeUri($fileUri).ToString()).Replace('/', '\')
        if ($relative.StartsWith("..") -or [System.IO.Path]::IsPathRooted($relative)) {
            throw "Refusing to copy a file outside the source directory: $($file.FullName)"
        }
        $dest = Join-Path $TargetRepo $relative
        $destDir = Split-Path -Parent $dest
        if ($DryRun) {
            Write-Host "DRY RUN: Would copy $($file.FullName) -> $dest"
        } else {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            Copy-Item -Path $file.FullName -Destination $dest -Force
        }
    }
}

Write-Step "Writing sync status docs"
$docsDir = Join-Path $TargetRepo "docs"
$statusPath = Join-Path $docsDir "agent-maker-sync-status.md"
$status = @"
# Agent Maker Sync Status

Last sync run: $(Get-Date -Format o)

## Target

$TargetRepo

## Source

$SourceDir

## Source files copied

$($sourceFiles.Count)

## Next checks

- Confirm the Agent Maker project files are present, not just setup notes.
- Add a remote with `git remote add origin <url>` if one is available.
- Run tests/build commands once the project type is known.
"@

if ($DryRun) {
    Write-Host "DRY RUN: Would write $statusPath"
} else {
    New-Item -ItemType Directory -Path $docsDir -Force | Out-Null
    Set-Content -Path $statusPath -Value $status -Encoding UTF8
}

Write-Step "Git status"
git -C $TargetRepo status --short

if (-not $DryRun) {
    $changes = git -C $TargetRepo status --porcelain
    if ($changes -and $sourceFiles.Count -gt 0) {
        git -C $TargetRepo add .
        git -C $TargetRepo commit -m "Sync Agent Maker handoff" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Commit skipped. Git user.name/user.email may not be configured, or there was nothing committable." -ForegroundColor Yellow
            Write-Host "Run: git config --global user.name 'Your Name'"
            Write-Host "Run: git config --global user.email 'you@example.com'"
        } else {
            Write-Host "Created commit: Sync Agent Maker handoff" -ForegroundColor Green
        }
    } else {
        if ($sourceFiles.Count -eq 0) {
            Write-Host "Commit skipped because no Agent Maker source files were imported." -ForegroundColor Yellow
        } else {
            Write-Host "No changes to commit." -ForegroundColor Green
        }
    }
}

Write-Step "Done"
