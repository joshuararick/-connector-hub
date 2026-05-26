param(
    [string]$TargetRepo = "C:\Users\joshu\OneDrive\Documents\Ai Army"
)

$ErrorActionPreference = "Stop"

Write-Host "Repo path: $TargetRepo"
if (-not (Test-Path $TargetRepo)) {
    Write-Host "Target path does not exist."
    exit 1
}

Write-Host "\nFiles:"
Get-ChildItem -Path $TargetRepo -Force | Select-Object Mode,Length,LastWriteTime,Name | Format-Table -AutoSize

Write-Host "\nGit status:"
if (Test-Path (Join-Path $TargetRepo ".git")) {
    git -C $TargetRepo status
    Write-Host "\nRemotes:"
    git -C $TargetRepo remote -v
    Write-Host "\nRecent commits:"
    git -C $TargetRepo log --oneline -5 2>$null
} else {
    Write-Host "Not a Git repo."
}
