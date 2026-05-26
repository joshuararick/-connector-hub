# Agent Maker Profile

Status: awaiting ChatGPT agent instructions

## Purpose

Describe what this agent is supposed to do.

## ChatGPT Instructions

Paste the full instructions from the ChatGPT agent/GPT Configure screen here.

## Expected Behavior

- Primary jobs:
- Things it should avoid:
- Tone or style:
- Escalation rules:

## Tools And Integrations

List any tools, actions, APIs, webhooks, or external services the agent needs.

| Name | Type | Purpose | Required Env Vars |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

## Knowledge Files

List files uploaded to the ChatGPT agent, then add exported copies to this repo when available.

| File | Purpose | Local Path |
| --- | --- | --- |
| TBD | TBD | TBD |

## Codex Usage Notes

When asked to act as this agent, Codex should:

1. Read this profile.
2. Load any referenced local knowledge files.
3. Confirm missing integrations before attempting external actions.
4. Keep implementation files in normal project folders, not inside this profile.

## Open Items

- [ ] Paste the ChatGPT agent instructions.
- [ ] Add any exported knowledge files.
- [ ] Document needed APIs/actions.
- [ ] Add source export to `agent-maker-sync-handoff/source_drop_here/`, if there is app code to sync.
