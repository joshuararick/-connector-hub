# Build Plan

## Mission

Create a controlled autonomous AI agent platform that can eventually operate across research, files, repositories, browser workflows, and project management without becoming a mystery goblin.

## Build order

1. **Safe demo loop** — deterministic planner, policy engine, tool registry, memory log.
2. **Private task corpus** — convert real work into repeatable eval scenarios.
3. **LLM planner** — add model-backed planning only after scoring exists.
4. **Tool expansion** — add repo, browser, file, database, and API tools behind policy gates.
5. **Observability** — trace every prompt, decision, tool call, approval, retry, and cost.
6. **Human approval** — require review for writes, spending, messages, deletion, secrets, external actions.
7. **Autonomy tiers** — graduate tasks from manual to suggested to supervised to autonomous.

## Autonomy levels

| Level | Meaning | Examples |
|---|---|---|
| L0 | Chat only | Advice, plans, summaries |
| L1 | Drafts actions | Creates files or commands for review |
| L2 | Executes safe local actions | Read-only repo scans, summaries, local notes |
| L3 | Supervised external actions | PR creation, emails, browser workflows with approval |
| L4 | Bounded autonomy | Recurring tasks with budgets, rollback, alerts |
| L5 | Not a near-term target | Fully open-ended self-directed action |

Start at L1/L2. Earn L3 with tests. Treat L4 like production infrastructure.
