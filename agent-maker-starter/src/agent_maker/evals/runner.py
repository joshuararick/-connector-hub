from __future__ import annotations

import yaml
from pathlib import Path
from agent_maker.core.orchestrator import Orchestrator


def run_eval_file(path: str) -> list[dict]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    tasks = data.get("tasks", [])
    orchestrator = Orchestrator(memory_path=".agent_runs/eval_memory.jsonl")
    results = []
    for task in tasks:
        run = orchestrator.run_goal(task["goal"], auto_approve=False)
        results.append({
            "id": task.get("id"),
            "goal": task["goal"],
            "status": run.status,
            "steps": len(run.plan),
        })
    return results
