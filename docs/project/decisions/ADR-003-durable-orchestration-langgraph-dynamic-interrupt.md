# ADR-003: Durable orchestration with LangGraph and a dynamic gate interrupt

- **Status:** proposed
- **Date:** 2026-11-09
- **Decision owner:** Maintainer (STK-001)
- **Related:** `FR-009`–`FR-012`, [ADR-001](ADR-001-adopt-craftrail-and-atep-blueprint-with-amendments.md) A1

## Context and forces

Threads must pause for human approval for minutes or days and survive restarts. The blueprint selects LangGraph with `AsyncPostgresSaver`.

## Decision

- Use LangGraph `StateGraph` with `AsyncPostgresSaver` (psycopg 3 pool) as the checkpointer.
- The `gate` node calls `interrupt(payload)` with the full staged batch **only** if any action is `CONSEQUENTIAL`; resume via `Command(resume=decision)` where `decision` maps idempotency key → approve / reject / edited payload.
- Edited payloads are re-validated and receive a new idempotency key; the old row becomes `REJECTED_BY_USER` with a link to the replacement.
- Nodes are pure async functions over `AgentState`; all I/O goes through injected ports (ledger, MCP client, LLM) so graph tests run with fakes and an in-memory checkpointer, and integration tests with Postgres.
- Phase 6 moves graph execution into a `worker` pulling jobs from a Postgres queue (**Procrastinate**, MIT) so the API stays stateless.

## Alternatives considered

- Temporal: excellent durability but adds a heavy server and a second programming model. Prefect / Celery: no native HITL interrupt semantics. Hand-rolled state machine: re-implements checkpointing.

## Consequences

- Positive: native HITL, resumability, time-travel debugging.
- Negative / risks: LangGraph API churn — pin version and isolate graph wiring in `orchestrator/graph.py`.

## Supersedes / superseded by

None.
