from agent_maker.core.orchestrator import Orchestrator
from agent_maker.core.state import TaskStatus


def test_demo_agent_runs(tmp_path):
    memory = tmp_path / "memory.jsonl"
    result = Orchestrator(memory_path=str(memory)).run_goal("make an agent")
    assert result.status == TaskStatus.DONE
    assert len(result.plan) == 3
    assert memory.exists()
