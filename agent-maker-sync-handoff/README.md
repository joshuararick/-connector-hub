# Agent Maker to Ai Army Sync Handoff

This package is a concrete sync handoff bundle for the Codex workspace/local repo at:

`C:\Users\joshu\OneDrive\Documents\Ai Army`

## What This Bundle Does

It gives Codex a repeatable sync workflow:

1. Verify the local repo state.
2. Import real source files from `source_drop_here/`.
3. Preserve existing repo metadata.
4. Create or refresh project documentation.
5. Stage and commit when real source files are present.

## Current Limitation

The updated handoff archive is not the Agent Maker project source. It contains setup notes and scripts only.

To complete a true source sync, put the exported Agent Maker project files into `source_drop_here/` before running the script, or provide a Git remote URL for the source project.

## Run On Windows PowerShell

From inside this extracted bundle:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\sync-agent-maker.ps1 -TargetRepo "C:\Users\joshu\OneDrive\Documents\Ai Army"
```

Optional dry run:

```powershell
.\scripts\sync-agent-maker.ps1 -TargetRepo "C:\Users\joshu\OneDrive\Documents\Ai Army" -DryRun
```

## Expected Output

- A verified Git repo at the target path.
- `docs/agent-maker-sync-status.md` refreshed in the repo.
- Real files placed in `source_drop_here/` copied into the repo.
- Setup notes ignored as placeholders.
- A Git commit named `Sync Agent Maker handoff` when real source files are imported and changes exist.
