from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    BLOCKED = "blocked"
    FAILED = "failed"


class PlanStep(BaseModel):
    id: str
    goal: str
    tool: str | None = None
    args: dict[str, Any] = Field(default_factory=dict)
    risk: RiskLevel = RiskLevel.LOW
    status: TaskStatus = TaskStatus.PENDING
    result: str | None = None


class AgentRun(BaseModel):
    goal: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: TaskStatus = TaskStatus.PENDING
    plan: list[PlanStep] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    def add_note(self, message: str) -> None:
        self.notes.append(f"{datetime.now(timezone.utc).isoformat()} | {message}")
