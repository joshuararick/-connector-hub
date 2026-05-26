# Agent Maker Sync Status

Last sync run: 2026-05-26

## Current Source

- Source site: https://joshuararick.github.io/-connector-hub/
- Source repository: https://github.com/joshuararick/-connector-hub
- Source branch: main
- Source commit: 838d65cb8469280cc2f895efc337a1cfd06bd8c5

## Current Repo State

- Ai Army is synced from Connector Hub as a static HTML/CSS/JS app.
- Imported app files: `index.html`, `styles.css`, `app.js`, `README.md`, and `.github/workflows/pages.yml`.
- Local agent guidance is preserved in `AGENTS.md` and `agents/agent-maker.profile.md`.
- The original and updated Agent Maker handoff archives/folder are preserved for audit history.
- The local Git remote is configured as `origin` pointing at `https://github.com/joshuararick/-connector-hub.git`.

## Behavior And Storage

- The app remains frontend-only with no backend.
- Browser storage keys remain `ch_apps`, `ch_agents`, and `ch_connectors`.
- Backup export remains `connector-hub-backup.json`.

## Security Notes

- Do not store real API keys in browser-local storage.
- Use placeholders until a private backend and authentication are added.
- Keep exported backups in a safe location.

## Handoff Note

- The private ChatGPT project URL is no longer the source for this sync.
- `agent-maker-sync-handoff/source_drop_here/` still does not contain a full private Agent Maker project export; it is retained only as handoff history.
- The handoff sync script ignores placeholder notes and skips commits unless real Agent Maker source files are imported.
