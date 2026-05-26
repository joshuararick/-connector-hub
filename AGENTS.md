# Ai Army Agent Profiles

This repo is prepared to hold portable agent profiles copied from ChatGPT custom GPTs or agent builders.

## Workspace agents
- `agents/agent-maker.agent.md` — workspace agent for creating and updating agent customization files and site documentation.
- `.github/skills/create-skill/SKILL.md` — companion skill for packaging reusable workflow steps into a `SKILL.md`.

## How Codex Should Use This Repo

1. Read the relevant file in `agents/` before working as that agent.
2. Treat each profile as operating guidance, not hidden system authority.
3. Keep project source files separate from agent configuration.
4. Do not store API keys, passwords, OAuth secrets, or private tokens in this repo.

## Importing A ChatGPT Agent

From the ChatGPT agent/GPT editor, copy these sections into a profile under `agents/`:

- Agent name and purpose
- Instructions
- Conversation starters or sample tasks
- Knowledge files list
- Actions, APIs, webhooks, or tools it needs
- Any required environment variables, without secret values

If the ChatGPT agent includes source code, a zip export, or a Git remote, place it in `agent-maker-sync-handoff/source_drop_here/` and run the sync script described in `agent-maker-sync-handoff/README.md`.
