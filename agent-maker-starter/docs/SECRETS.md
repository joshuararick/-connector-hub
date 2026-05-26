# Secrets and Keys

Agent Maker uses two classes of secrets:

1. **Local app secrets** generated on your machine.
2. **Provider API keys** created in provider dashboards such as OpenAI, Anthropic, GitHub, etc.

Do not commit secrets. The repo includes `.gitignore` and a pre-commit hook to block common secret files.

## Generate local secrets

From the repo root:

```powershell
python scripts/generate_secrets.py
```

This creates `.env` with:

- `AGENT_MAKER_APP_SECRET`
- `AGENT_MAKER_ENCRYPTION_KEY`
- `AGENT_MAKER_SIGNING_KEY`

The script intentionally leaves provider keys blank. Paste provider keys into `.env` only on your machine.

## Install commit protection

```powershell
.\scripts\install_git_hooks.ps1
```

## Safer Windows storage options

For production or serious workflows, keep provider keys in one of these instead of plain `.env`:

- 1Password / Bitwarden / KeePassXC
- Windows Credential Manager
- GitHub Actions Secrets for CI
- cloud secret managers when deployed

`.env` is fine for local development, but it should never be pushed.

## Emergency rotation

If a secret is ever pasted publicly or committed:

1. Revoke it at the provider.
2. Generate a replacement.
3. Remove it from git history before sharing the repo.
4. Re-test with the new key.
