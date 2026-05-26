from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

ToolFn = Callable[[dict[str, Any]], str]


@dataclass
class Tool:
    name: str
    description: str
    fn: ToolFn


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Tool not registered: {name}")
        return self._tools[name]

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())
