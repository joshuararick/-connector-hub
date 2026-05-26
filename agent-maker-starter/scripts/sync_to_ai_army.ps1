param(
  [string]$Target = "C:\Users\joshu\OneDrive\Documents\Ai Army"
)

$Source = Resolve-Path "$PSScriptRoot\.."
Write-Host "Syncing Agent Maker starter from $Source to $Target"

if (!(Test-Path $Target)) {
  New-Item -ItemType Directory -Force -Path $Target | Out-Null
}

robocopy $Source $Target /E /XD .git .venv __pycache__ /XF .env .agent_memory.jsonl

Write-Host "Done. Next: cd '$Target'; python -m venv .venv; .\.venv\Scripts\activate; pip install -e ."
