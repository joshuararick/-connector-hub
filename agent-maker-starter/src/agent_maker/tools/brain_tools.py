from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from agent_maker.tools.registry import Tool

BRAIN_FILE = Path("C:/Users/joshu/Brain of Ai/brain-server/data.json")

def brain_read_tool(args: dict[str, Any]) -> str:
    try:
        if BRAIN_FILE.exists():
            data = json.loads(BRAIN_FILE.read_text())
            key = args.get("key", "all")
            if key == "all":
                return json.dumps({
                    "identity": data.get("identity", {}),
                    "weekly_theme": data.get("weekly_theme", ""),
                    "focus": data.get("focus", {}),
                    "life_areas": {k: v.get("goal","") for k, v in data.get("life_areas", {}).items()},
                    "priorities": [p["text"] for p in data.get("priorities", [])[:5]],
                    "recent_wins": [w["text"] for w in data.get("wins", [])[-3:]]
                }, indent=2)
            return str(data.get(key, f"Key {key} not found"))
    except Exception as e:
        return f"Brain read error: {e}"
    return "Brain file not found"

def think_tool(args: dict[str, Any]) -> str:
    return f"[Thinking about: {args.get('prompt', '')}] - This step requires LLM reasoning to execute fully."

def web_search_tool(args: dict[str, Any]) -> str:
    query = args.get("query", "")
    return f"[Web search: '{query}'] - Connect Perplexity bridge on port 3338 to enable real searches."

def get_brain_tools() -> list[Tool]:
    return [
        Tool("brain_read", "Read Josh's brain context - goals, priorities, focus", brain_read_tool),
        Tool("think", "Think through a problem step by step", think_tool),
        Tool("web_search", "Search the web for information", web_search_tool),
    ]
