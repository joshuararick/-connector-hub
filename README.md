# Agent Maker Command Center

Owned website for Agent Maker / AI Army: apps, AI agents, connectors, sync workflows, and deployment tracking.

## Live production site

https://agent-command-center.b12sites.com/#overview

## Backup / repo-hosted static version

GitHub Pages backup target:

https://joshuararick.github.io/-connector-hub/

## What is included in this repo

- `index.html` - repo-hosted static backup / prototype
- `styles.css` - responsive dashboard styling
- `app.js` - browser-local app/agent/connector registry
- `.github/workflows/pages.yml` - GitHub Pages deployment workflow

## Important security note

This static repo version is browser-only. Do not store real API keys, tokens, refresh tokens, passwords, private keys, or customer secrets in localStorage or page code. Use placeholders here until a private backend, Cloudflare Worker, or secure server-side environment is connected.

## Deployment

The B12 site above is the canonical live website. Pushes to `main` can still trigger the GitHub Pages backup workflow. If the backup site does not appear, open GitHub repo settings and set Pages source to **GitHub Actions**.
