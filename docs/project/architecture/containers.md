# Container view

**Abstraction:** deployable/runtime units and data stores
**Scope:** Vouchor
**Last reviewed:** 2026-11-09

```mermaid
C4Container
    title Vouchor containers
    Person(user, "User")
    System_Boundary(v, "Vouchor") {
        Container(api, "api", "FastAPI", "REST + SSE gateway, auth, enqueues graph runs")
        Container(worker, "worker", "Python, LangGraph", "Runs durable graph threads and the executor")
        Container(mcp1, "mcp-connectors", "FastMCP", "Tier 1: SMTP/IMAP, Gmail, Calendar, Keep APIs")
        Container(mcp2, "mcp-skills", "FastMCP", "Tier 2: deterministic playbooks")
        Container(mcp3, "mcp-browser", "FastMCP + Playwright", "Tier 3: live DOM verification and forms")
        Container(mcp4, "mcp-sandbox", "FastMCP", "Tier 4: launches isolated sandbox jobs")
        Container(llm, "llm-gateway", "LiteLLM proxy", "Routes to Ollama or OpenAI-compatible endpoints")
        Container(searx, "searxng", "SearXNG", "Self-hosted metasearch (untrusted discovery)")
        ContainerDb(pg, "postgres", "PostgreSQL 16 + pgvector", "Checkpoints, ledger, verified sources, memories, job queue")
        ContainerDb(kv, "valkey", "Valkey 8", "SSE pub/sub, rate-limit counters")
    }
    Rel(user, api, "HTTPS")
    Rel(api, pg, "Reads state, enqueues jobs")
    Rel(api, kv, "Subscribes to thread events")
    Rel(worker, pg, "Checkpoints, ledger rows, row locks")
    Rel(worker, kv, "Publishes events")
    Rel(worker, mcp1, "MCP streamable HTTP")
    Rel(worker, mcp2, "MCP")
    Rel(worker, mcp3, "MCP")
    Rel(worker, mcp4, "MCP")
    Rel(worker, llm, "OpenAI-compatible HTTP")
    Rel(worker, searx, "JSON search")
```

## Runtime responsibilities

| Container | Owns | Scales by | Local (Compose) | Cloud (Helm) |
|---|---|---|---|---|
| api | HTTP contract, authn/z, SSE fan-out | Replicas (stateless) | `api` service | Deployment + Gateway API route |
| worker | Graph execution, executor state machine | Replicas; per-key Postgres row locks prevent double execution | `worker` service | Deployment |
| mcp-* | One tier each; isolate credentials and heavy deps (Chromium) | Replicas per tier | one service each | one Deployment each |
| sandbox jobs | Untrusted code execution | One short-lived job per task | Docker container via rootless socket proxy | Kubernetes Job (optionally gVisor RuntimeClass) |
| postgres | All durable state | CloudNativePG replicas | `pgvector/pgvector:pg16` | CloudNativePG `Cluster` |
| valkey | Ephemeral coordination only | Single instance acceptable | `valkey/valkey` | StatefulSet |
| llm-gateway / Ollama | Model routing | GPU nodes optional | `litellm` + `ollama` (profile `llm`) | Deployment; Ollama optional |
| searxng | Discovery | Replicas | `searxng` | Deployment |
| mailpit | Dev/test SMTP+IMAP sink | — | `mailpit` | not deployed |

Phase 1–4 may run the graph inside the `api` process for simplicity; the split into `worker` with a Postgres-backed queue happens in Phase 6 ([implementation plan](../implementation-plan.md)).
