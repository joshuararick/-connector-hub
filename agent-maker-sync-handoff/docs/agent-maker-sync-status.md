# Agent Maker Sync Status

Last checked: 2026-05-26

## Target

`C:\Users\joshu\OneDrive\Documents\Ai Army`

## Current State

- The target repo exists and is writable from Codex.
- The repo contains the Connector Hub static app and local agent guidance.
- `agent-maker-sync-handoff-updated.zip` has been received.
- The updated zip is still a handoff package, not the actual Agent Maker source export.
- `source_drop_here/` contains setup assistance notes only.

## Fixed In This Handoff

- `scripts/sync-agent-maker.ps1` now preserves source-relative paths.
- `.gitkeep` and setup notes are ignored when counting and copying source files.
- Files outside `source_drop_here/` are rejected before copy.
- Commits are skipped when the source folder only contains placeholders.
- Sync status docs now describe the real writable workspace state.

## Still Needed

Add the actual Agent Maker project files to `source_drop_here/`, or provide a Git remote URL. Then run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\sync-agent-maker.ps1 -TargetRepo "C:\Users\joshu\OneDrive\Documents\Ai Army"
```
