# ADR-001: Adopt CraftRail and the ATEP blueprint, with recorded amendments

- **Status:** proposed
- **Date:** 2026-11-09
- **Decision owner:** Maintainer (STK-001)
- **Related:** [blueprint](../vision/atep-blueprint.md), [implementation plan](../implementation-plan.md)

## Context and forces

The repository was created from the [CraftRail template](https://github.com/KshitijV97/craft-rail). The ATEP blueprint defines vision, schema and phases, but a close review found gaps that would break its own invariants in production.

## Decision

Use CraftRail's workflow (spec → plan → tasks → verify → converge) for every phase. Treat the blueprint as the source vision, amended as follows:

| # | Blueprint text | Problem | Amendment |
|---|---|---|---|
| A1 | `interrupt_before=["executor"]` conditional on consequence | `interrupt_before` is static per node and cannot depend on state | Gate node calls LangGraph's dynamic `interrupt()` only when the batch contains consequential actions ([ADR-003](ADR-003-durable-orchestration-langgraph-dynamic-interrupt.md)) |
| A2 | Read-back by recipient + subject; "IMAP Sent folder" | Not unique; plain SMTP does not write to Sent | Stamp a `Message-ID` derived from the idempotency key and search by it ([ADR-007](ADR-007-provider-native-idempotency-markers.md)) |
| A3 | "Proof absent → safe to retry" | Mail/APIs are eventually consistent; immediate absence may be a false negative | Read-back polls for a per-capability grace window before declaring absence |
| A4 | Redis for idempotency locks | Two sources of truth; lock expiry can allow double execution | Postgres row lock on the ledger row; Valkey for pub/sub only ([ADR-004](ADR-004-postgres-source-of-truth-valkey-for-coordination.md)) |
| A5 | Redis 7 | Redis 7.4+ is not OSI-licensed | Valkey (BSD-3), wire-compatible |
| A6 | Migrations mounted into `docker-entrypoint-initdb.d` | Runs only on empty volumes; unusable for upgrades in cloud | Versioned migrations run as a one-shot job ([ADR-005](ADR-005-versioned-migrations-alembic-sql.md)) |
| A7 | `verified_dependencies` `min_length=1` for every `StagedAction` | Some actions (e.g. "add a note to Keep", Tier 4 artifacts) have no external entity to verify | Required only when the capability declares `requires_verification=True` (default for outreach); validated by registry |
| A8 | Idempotency key includes `thread_id` | Same request in a new thread could re-send | Keep thread scoping (intentional: a new request is a new intent) but staging warns when an identical action succeeded in the last 24 h for the same target |
| A9 | Docker-in-Docker sandbox | Privileged containers are a cluster-wide escape risk | Pluggable sandbox backends ([ADR-008](ADR-008-tier4-sandbox-isolation-backends.md)) |
| A10 | `src/` as the import package; `:latest` image tags | Ambiguous imports; non-reproducible | `src/vouchor/` src-layout; pinned versions (`NFR-012`) |
| A11 | Embedding dimension fixed at 768 | Ties schema to one model | Dimension is a migration-time setting; default 768 (`nomic-embed-text`) |

## Alternatives considered

- Implement the blueprint verbatim: rejected; A1–A4 violate invariants 4–5.
- Rewrite the blueprint file: rejected; it is the historical vision input. Amendments live here.

## Consequences

- Positive: invariants hold under crash, retry and concurrency.
- Negative / risks: more moving parts than the blueprint (grace windows, markers); mitigated by fault-injection tests.

## Supersedes / superseded by

None.
