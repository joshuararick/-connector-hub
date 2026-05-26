"""Generate local development secrets for Agent Maker.

This creates a .env file with strong random local secrets. It does NOT create
provider API keys like OPENAI_API_KEY or GITHUB_TOKEN; those must come from the
provider account/dashboard.
"""
from __future__ import annotations

import argparse
import base64
import os
import secrets
from pathlib import Path


def fernet_key() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("ascii")


def random_urlsafe(nbytes: int = 48) -> str:
    return secrets.token_urlsafe(nbytes)


def build_env() -> str:
    return "\n".join(
        [
            "# Agent Maker local secrets",
            "# Generated locally. DO NOT COMMIT.",
            "AGENT_MAKER_ENV=development",
            f"AGENT_MAKER_APP_SECRET={random_urlsafe(48)}",
            f"AGENT_MAKER_ENCRYPTION_KEY={fernet_key()}",
            f"AGENT_MAKER_SIGNING_KEY={random_urlsafe(64)}",
            "AGENT_MAKER_STATE_DIR=.data",
            "AGENT_MAKER_REQUIRE_APPROVAL=true",
            "",
            "# Fill these from official provider dashboards when ready.",
            "OPENAI_API_KEY=",
            "ANTHROPIC_API_KEY=",
            "GITHUB_TOKEN=",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a safe local .env file.")
    parser.add_argument("--out", default=".env", help="Output path. Default: .env")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file.")
    args = parser.parse_args()

    out = Path(args.out)
    if out.exists() and not args.force:
        print(f"Refusing to overwrite {out}. Re-run with --force if you really mean it.")
        return 2

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_env(), encoding="utf-8")

    try:
        os.chmod(out, 0o600)
    except OSError:
        # Windows may ignore POSIX perms; .gitignore and git hooks still protect it.
        pass

    print(f"Generated {out}")
    print("Keep it local. Do not commit it. Provider API keys still need to be pasted in manually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
