# ADR-005: Versioned schema migrations with Alembic running plain SQL

- **Status:** proposed
- **Date:** 2026-11-09
- **Decision owner:** Maintainer (STK-001)
- **Related:** [ADR-001](ADR-001-adopt-craftrail-and-atep-blueprint-with-amendments.md) A6, `NFR-006`

## Context and forces

The blueprint ships `001_init_schema.sql` via Postgres init scripts, which only run on an empty data directory. Cloud upgrades need ordered, repeatable migrations.

## Decision

- Alembic manages revision order; each revision executes reviewed SQL files from `migrations/sql/` (keeps DDL readable and lintable by sqlfluff). No ORM.
- Migrations run as a one-shot container: `migrate` service in Compose (other services `depends_on: condition: service_completed_successfully`), Helm `pre-install,pre-upgrade` hook Job in Kubernetes.
- Every migration has a tested downgrade or is explicitly marked irreversible; CI runs upgrade → downgrade → upgrade against a pgvector testcontainer.
- LangGraph checkpoint tables are created by `AsyncPostgresSaver.setup()` invoked from the same migrate job.

## Alternatives considered

- dbmate / sqitch: plain SQL and language-agnostic but add a non-Python binary. Raw init scripts: rejected (see context).

## Consequences

- Positive: identical schema path locally and in cloud.
- Negative / risks: two migration owners (Alembic + LangGraph setup) — sequenced in one job and covered by a schema snapshot test.

## Supersedes / superseded by

None.
