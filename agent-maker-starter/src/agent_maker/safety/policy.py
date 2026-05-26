from __future__ import annotations

from dataclasses import dataclass
from agent_maker.core.state import PlanStep, RiskLevel


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    requires_approval: bool
    reason: str


class PolicyEngine:
    """Simple policy layer. Expand this before connecting powerful tools."""

    risky_tools = {"shell", "browser_purchase", "send_email", "delete_file", "write_repo"}

    def evaluate(self, step: PlanStep) -> PolicyDecision:
        if step.tool in self.risky_tools or step.risk == RiskLevel.HIGH:
            return PolicyDecision(
                allowed=True,
                requires_approval=True,
                reason="High-impact tool or high-risk step requires human approval.",
            )
        if step.risk == RiskLevel.MEDIUM:
            return PolicyDecision(
                allowed=True,
                requires_approval=True,
                reason="Medium-risk step requires approval in starter mode.",
            )
        return PolicyDecision(allowed=True, requires_approval=False, reason="Low-risk step allowed.")
