from __future__ import annotations

from agent_maker.core.executor import Executor
from agent_maker.core.planner import DemoPlanner
from agent_maker.core.state import AgentRun
from agent_maker.memory.local_store import LocalMemoryStore
from agent_maker.safety.policy import PolicyEngine
from agent_maker.tools.basic import default_registry


class Orchestrator:
    def __init__(self, memory_path: str = ".agent_memory.jsonl") -> None:
        self.planner = DemoPlanner()
        self.memory = LocalMemoryStore(memory_path)
        self.executor = Executor(default_registry(), PolicyEngine(), self.memory)

    def run_goal(self, goal: str, auto_approve: bool = False) -> AgentRun:
        run = self.planner.plan(goal)
        return self.executor.run(run, auto_approve=auto_approve)
