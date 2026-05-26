from __future__ import annotations

from agent_maker.core.state import AgentRun, TaskStatus
from agent_maker.memory.local_store import LocalMemoryStore
from agent_maker.safety.policy import PolicyEngine
from agent_maker.tools.registry import ToolRegistry


class Executor:
    def __init__(self, registry: ToolRegistry, policy: PolicyEngine, memory: LocalMemoryStore) -> None:
        self.registry = registry
        self.policy = policy
        self.memory = memory

    def run(self, agent_run: AgentRun, auto_approve: bool = False) -> AgentRun:
        agent_run.status = TaskStatus.RUNNING
        for step in agent_run.plan:
            decision = self.policy.evaluate(step)
            agent_run.add_note(f"Policy for {step.id}: {decision.reason}")
            if not decision.allowed:
                step.status = TaskStatus.BLOCKED
                step.result = decision.reason
                agent_run.status = TaskStatus.BLOCKED
                break
            if decision.requires_approval and not auto_approve:
                step.status = TaskStatus.BLOCKED
                step.result = "Approval required. Re-run with --auto-approve only after reviewing risk."
                agent_run.status = TaskStatus.BLOCKED
                break
            if step.tool is None:
                step.status = TaskStatus.DONE
                step.result = "No tool needed."
                continue
            step.status = TaskStatus.RUNNING
            tool = self.registry.get(step.tool)
            step.result = tool.fn(step.args)
            step.status = TaskStatus.DONE
            self.memory.append({"step_id": step.id, "goal": step.goal, "tool": step.tool, "result": step.result})
        else:
            agent_run.status = TaskStatus.DONE
        self.memory.append(agent_run.model_dump())
        return agent_run
