from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from agent_maker.tools.registry import Tool, ToolRegistry


def note_tool(args: dict[str, Any]) -> str:
    return args.get("text", "No note provided.")


def write_file_tool(args: dict[str, Any]) -> str:
    path = Path(args["path"]).expanduser().resolve()
    content = args.get("content", "")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"Wrote {path}"


def inspect_json_tool(args: dict[str, Any]) -> str:
    return json.dumps(args, indent=2, sort_keys=True)


def default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(Tool("note", "Record a note or intermediate result.", note_tool))
    registry.register(Tool("write_file", "Write a local file. Treat as medium risk in real systems.", write_file_tool))
    registry.register(Tool("inspect_json", "Pretty-print structured data for debugging.", inspect_json_tool))
    return registry
