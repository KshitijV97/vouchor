# ADR-004: Postgres is the single source of truth; Valkey only for ephemeral coordination

- **Status:** proposed
- **Date:** 2026-11-09
- **Decision owner:** Maintainer (STK-001)
- **Related:** `FR-013`, `FR-017`, `NFR-004`, [ADR-001](ADR-001-adopt-craftrail-and-atep-blueprint-with-amendments.md) A4–A5

## Context and forces

Exactly-once effects require that "who may execute this key" and "what happened" are decided in the same transactional store. A Redis lock with TTL can expire mid-call and allow a second executor.

## Decision

- The executor claims an action with `SELECT … FROM execution_ledger WHERE idempotency_key = $1 FOR UPDATE SKIP LOCKED` inside a short transaction, writes `ATTEMPTED_UNVERIFIED` with an attempt fencing token (`attempt_count`), commits, then calls the tool. Status updates are conditional on the fencing token (`WHERE attempt_count = $n`).
- A stale `ATTEMPTED_UNVERIFIED` row (worker died) is reclaimed after a lease timeout, always starting with read-back (`FR-015`).
- **Valkey 8** (BSD-3) replaces Redis for SSE pub/sub and rate-limit counters. Losing Valkey data never affects correctness.

## Alternatives considered

- Redis Redlock: rejected (correctness depends on clocks and TTLs). Postgres advisory locks: viable but row locks keep the claim tied to the data.

## Consequences

- Positive: one store to back up and reason about; correctness testable with plain Postgres.
- Negative / risks: Postgres load from locking is negligible at expected volumes.

## Supersedes / superseded by

None.
