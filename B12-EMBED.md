# B12 Embed Instructions

Use this when updating the production B12 website at:

https://agent-command-center.b12sites.com/#overview

## Recommended option: button link

Add a button on the B12 page that opens the working GitHub-backed command center:

```html
<a href="https://joshuararick.github.io/-connector-hub/" target="_blank" rel="noopener noreferrer">Open Agent Maker Command Center</a>
```

## Embed option: iframe

If B12 allows custom HTML embeds, paste this into an embed/custom-code block:

```html
<iframe
  src="https://joshuararick.github.io/-connector-hub/"
  title="Agent Maker Command Center"
  style="width:100%; min-height:900px; border:0; border-radius:24px; overflow:hidden; background:#07111f;"
  loading="lazy"
></iframe>
```

## What the embedded app does

- Loads GitHub-backed AI agent repositories from `agents.json` and public GitHub repo metadata.
- Lets you search/filter agent repos by name, framework, status, and risk.
- Imports GitHub repos into the local AI Agents dashboard.
- Adds apps, agents, and connectors in browser-local storage.
- Exports/imports a JSON backup.
- Locks the browser dashboard with a local PIN.
- Blocks obvious API keys/tokens from being saved into the static browser app.
- Performs basic public reachability checks for connector URLs.

## Security note

Do not store production API keys, tokens, refresh tokens, private keys, customer secrets, or private backend credentials in this browser app or in B12 custom code. Private actions need a server-side API, secure worker, or backend with environment variables.
