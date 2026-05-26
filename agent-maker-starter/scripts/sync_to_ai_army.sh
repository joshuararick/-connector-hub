#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-$HOME/Ai Army}"
SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$TARGET"
rsync -av --exclude .git --exclude .venv --exclude __pycache__ --exclude .env --exclude .agent_memory.jsonl "$SOURCE/" "$TARGET/"
echo "Done. Next: cd '$TARGET' && python -m venv .venv && source .venv/bin/activate && pip install -e ."
