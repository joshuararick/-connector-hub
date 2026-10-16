from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from agent_maker.core.state import AgentRun, PlanStep, RiskLevel


def _load_openai_key() -> str:
    """Read OPENAI_API_KEY from the environment or the git-ignored .env file."""
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    env_file = Path(__file__).resolve().parents[3] / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            name, _, value = line.partition("=")
            if name.strip() == "OPENAI_API_KEY":
                return value.strip()
    return ""


OPENAI_KEY = _load_openai_key()

SYSTEM_PROMPT = """You are an autonomous AI agent planner for Josh Rarick — Father, Husband, Creator.

You receive a goal and return a JSON list of steps. Each step must have:
- id: "step-N"
- goal: what this step accomplishes
- tool: one of [note, write_file, inspect_json, brain_read, web_search, think]
- args: dict of arguments for the tool
- risk: "low", "medium", or "high"

Rules:
- Low risk: reading, thinking, noting
- Medium risk: writing files, web searches  
- High risk: sending messages, payments, deleting things

Return ONLY valid JSON array. No explanation. No markdown.
Example:
[
  {"id": "step-1", "goal": "Analyze the request", "tool": "think", "args": {"prompt": "..."}, "risk": "low"},
  {"id": "step-2", "goal": "Write the output", "tool": "write_file", "args": {"path": "output.txt", "content": "..."}, "risk": "medium"}
]"""

class LLMPlanner:
    def plan(self, goal: str) -> AgentRun:
        run = AgentRun(goal=goal)
        try:
            steps_json = self._call_openai(goal)
            steps_data = json.loads(steps_json)
            run.plan = [
                PlanStep(
                    id=s.get("id", f"step-{i+1}"),
                    goal=s.get("goal", ""),
                    tool=s.get("tool"),
                    args=s.get("args", {}),
                    risk=RiskLevel(s.get("risk", "low"))
                )
                for i, s in enumerate(steps_data)
            ]
        except Exception as e:
            run.plan = [PlanStep(
                id="step-1",
                goal=f"Fallback: {goal}",
                tool="note",
                args={"text": f"LLM planning failed: {e}. Goal: {goal}"},
                risk=RiskLevel.LOW
            )]
        return run

    def _call_openai(self, goal: str) -> str:
        payload = json.dumps({
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Goal: {goal}"}
            ],
            "max_tokens": 1000,
            "temperature": 0.3
        }).encode()
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        return data["choices"][0]["message"]["content"].strip()
