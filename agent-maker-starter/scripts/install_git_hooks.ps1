Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

git config core.hooksPath .githooks
Write-Host "Installed Agent Maker git hooks. Secret files will be blocked from commits."
