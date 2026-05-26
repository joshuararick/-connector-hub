param(
  [Parameter(Mandatory=$false)] [string] $RemoteUrl = ""
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$secretPatterns = @(".env", ".env.*", "secrets/*", "*.pem", "*.key", "id_rsa*", "id_ed25519*")
Write-Host "Checking for staged secrets..."
$staged = git diff --cached --name-only
foreach ($pattern in $secretPatterns) {
  if ($staged -like $pattern) { throw "Refusing to push: staged secret-like file matched $pattern" }
}

if (-not (Test-Path ".git")) { git init }
git config core.hooksPath .githooks

git add .
git reset -- .env .env.* secrets/* *.pem *.key id_rsa* id_ed25519* 2>$null

$commitOutput = git commit -m "Initial Agent Maker autonomous agent scaffold" 2>&1
if ($LASTEXITCODE -ne 0) { Write-Host "Nothing new to commit, or commit skipped: $commitOutput" }

if ($RemoteUrl -ne "") {
  if (-not (git remote | Select-String -SimpleMatch "origin")) {
    git remote add origin $RemoteUrl
  }
}

git branch -M main
if (git remote | Select-String -SimpleMatch "origin") {
  git push -u origin main
} else {
  Write-Host "No origin remote configured. Add one with: git remote add origin <repo-url>"
}
