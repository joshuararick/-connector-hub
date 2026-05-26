from __future__ import annotations

import argparse
import json
from rich.console import Console
from rich.table import Table
from agent_maker.core.orchestrator import Orchestrator

console = Console()


def render_run(run) -> None:
    console.print(f"\n[bold]Goal:[/bold] {run.goal}")
    console.print(f"[bold]Status:[/bold] {run.status}\n")
    table = Table(title="Agent Plan")
    table.add_column("Step")
    table.add_column("Tool")
    table.add_column("Risk")
    table.add_column("Status")
    table.add_column("Result")
    for step in run.plan:
        table.add_row(step.id, step.tool or "-", step.risk, step.status, step.result or "")
    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(prog="agent-maker")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run a goal through the safe demo agent")
    run_cmd.add_argument("goal")
    run_cmd.add_argument("--auto-approve", action="store_true")
    run_cmd.add_argument("--json", action="store_true")
    run_cmd.add_argument("--memory-path", default=".agent_memory.jsonl")

    args = parser.parse_args()

    if args.command == "run":
        orchestrator = Orchestrator(memory_path=args.memory_path)
        result = orchestrator.run_goal(args.goal, auto_approve=args.auto_approve)
        if args.json:
            print(json.dumps(result.model_dump(), indent=2))
        else:
            render_run(result)


if __name__ == "__main__":
    main()
