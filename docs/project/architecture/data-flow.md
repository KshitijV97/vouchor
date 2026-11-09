# Data flow

**Status:** proposed
**Last reviewed:** 2026-11-09

## Executor state machine (per staged action)

```mermaid
stateDiagram-v2
    [*] --> STAGED
    STAGED --> APPROVED: user approves
    STAGED --> REJECTED_BY_USER: user rejects
    APPROVED --> ATTEMPTED_UNVERIFIED: lock row, commit, then call tool
    ATTEMPTED_UNVERIFIED --> VERIFIED_SUCCESS: read-back finds marker
    ATTEMPTED_UNVERIFIED --> PARTIAL_RECOVERED: tool errored or crashed, read-back finds marker
    ATTEMPTED_UNVERIFIED --> APPROVED: read-back absent after grace window, next tier
    ATTEMPTED_UNVERIFIED --> FAILED_TERMINAL: all tiers exhausted
    VERIFIED_SUCCESS --> [*]
    PARTIAL_RECOVERED --> [*]
    FAILED_TERMINAL --> [*]
    REJECTED_BY_USER --> [*]
```

Transitions not shown are rejected by the ledger repository (`FR-013`).

## Data ownership

| Data | Store | Written by | Retention |
|---|---|---|---|
| Graph checkpoints | Postgres (`checkpoints*`) | LangGraph saver | Until thread archived |
| `verified_sources` | Postgres | Verifier | Per freshness window; audit kept |
| `execution_ledger` | Postgres | Staging, gate, executor | Immutable audit (no deletes) |
| `durable_memories` | Postgres + pgvector | Distiller | Until user deletes |
| Thread events | Valkey pub/sub | Worker | Ephemeral |
| Sandbox artifacts | Volume / object storage (S3-compatible, e.g. MinIO or Garage) | Tier 4 | Configurable |
| OAuth tokens | Encrypted at rest (Postgres, envelope key from secret) | Connector setup | Until revoked |
