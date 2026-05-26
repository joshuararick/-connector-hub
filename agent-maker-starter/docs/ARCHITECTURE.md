# Architecture

```mermaid
flowchart LR
    U[User / Scheduler] --> O[Orchestrator]
    O --> P[Planner]
    P --> S[State / Plan]
    S --> G[Policy Gate]
    G --> E[Executor]
    E --> T[Tool Registry]
    T --> F[Files]
    T --> R[Repos]
    T --> B[Browser]
    T --> A[APIs]
    E --> M[Memory]
    E --> L[Logs / Traces]
    G --> H[Human Approval]
```

## Core contracts

- Planner produces `PlanStep` objects.
- Policy engine decides whether a step is allowed, blocked, or approval-gated.
- Executor runs only registered tools.
- Memory store records outcomes.
- Eval runner checks whether changes improve real task completion.

## Production additions

- LangGraph or equivalent durable orchestration
- Postgres + pgvector for memory
- OpenTelemetry/OpenInference tracing
- Browser worker sandbox
- Code execution sandbox
- Per-tool scoped secrets
- CI eval suite
