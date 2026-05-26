from __future__ import annotations

from agent_maker.core.state import AgentRun, PlanStep, RiskLevel


class DemoPlanner:
    """Deterministic starter planner.

    Replace this with an LLM-backed planner once your eval suite exists.
    """

    def plan(self, goal: str) -> AgentRun:
        run = AgentRun(goal=goal)
        run.plan = [
            PlanStep(
                id="step-1",
                goal="Clarify the requested outcome and restate it as an executable objective.",
                tool="note",
                args={"text": f"Objective: {goal}"},
                risk=RiskLevel.LOW,
            ),
            PlanStep(
                id="step-2",
                goal="Create an implementation checklist for the objective.",
                tool="note",
                args={
                    "text": "Checklist: define scope, choose tools, execute safe steps, request approval for risky actions, log results, evaluate output."
                },
                risk=RiskLevel.LOW,
            ),
            PlanStep(
                id="step-3",
                goal="Persist a run summary for later review.",
                tool="inspect_json",
                args={"goal": goal, "mode": "safe_demo", "next": "replace DemoPlanner with LLM planner after evals"},
                risk=RiskLevel.LOW,
            ),
        ]
        return run
