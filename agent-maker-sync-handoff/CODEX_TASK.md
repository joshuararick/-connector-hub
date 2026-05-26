# Codex Task: Sync Agent Maker into Ai Army

Please run this task in `workspace-write` mode.

## Goal

Import the Agent Maker project source into:

`C:\Users\joshu\OneDrive\Documents\Ai Army`

## Steps

1. Verify the target path exists and is writable.
2. Verify whether it is a Git repo.
3. If it has no commits, initialize the first commit after importing files.
4. Use files in `source_drop_here/` as the source project export.
5. Copy source files into the repo without copying `.git` directories.
6. Preserve existing files unless there is a clear replacement from the source.
7. Add/refresh `docs/agent-maker-sync-status.md`.
8. Run `git status` and summarize changed files.
9. Commit changes with message: `Sync Agent Maker handoff`.
10. If no real source files are present, do not invent app files; report that the source export is still missing.

## Important

Do not rely on a ChatGPT project URL that requires a logged-in browser session. Use attached/exported files or a Git remote only.
