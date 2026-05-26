# Agent Maker Starter

A practical starter repo for building an autonomous AI agent system without jumping straight into unsafe “let it do everything” chaos.

This project is intentionally shaped as a **hybrid autonomous agent**:

- explicit planner/supervisor
- tool registry with policy checks
- persistent run logs and memory hooks
- human approval gates for risky actions
- evaluation harness before production use
- sync scripts for moving into a local `Ai Army` workspace

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
cp .env.example .env
python -m agent_maker.cli run "Research LangGraph and summarize what to build first"
```

By default, the project runs in safe demo mode. It does not need API keys to prove the flow works.

## Repo layout

```text
src/agent_maker/
  cli.py                 Command line entrypoint
  core/                  Planner, executor, orchestrator, state
  tools/                 Tool registry and example tools
  memory/                Local memory store
  safety/                Policy checks and approval gates
  evals/                 Scenario evaluation harness
docs/
  BUILD_PLAN.md          What we are building and why
  ARCHITECTURE.md        Component map
  ROADMAP.md             Prototype milestones
scripts/
  sync_to_ai_army.ps1    Windows sync helper
  sync_to_ai_army.sh     Unix sync helper
examples/
  tasks.yaml             Example tasks for agent runs
```

## The first target

Build a useful, controlled autonomous assistant that can:

1. decompose a goal into steps,
2. choose tools,
3. execute low-risk actions automatically,
4. pause for approval on high-risk actions,
5. log every action,
6. evaluate itself against real tasks.

That gives us autonomy without letting the raccoon drive the forklift.

## Next step

Copy or unzip this repo into:

```text
C:\Users\joshu\OneDrive\Documents\Ai Army
```

Then run the PowerShell sync script or initialize Git there.
