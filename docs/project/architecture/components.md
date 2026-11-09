# Component view

**Status:** proposed
**Last reviewed:** 2026-11-09

Python package layout (`src/vouchor/`, see [ADR-002](../decisions/ADR-002-python-toolchain-and-quality-gates.md)):

| Module | Responsibility | Depends on |
|---|---|---|
| `core/contracts.py` | Pydantic v2 models and enums (original blueprint §2.3 at commit `ac5b91d`, amended per ADRs) | — |
| `core/config.py` | `pydantic-settings` configuration | — |
| `core/ledger.py` | Ledger repository, state-transition guard, row locking | `asyncpg` |
| `core/llm.py` | LLM client protocol + LiteLLM implementation + deterministic fake | `httpx` |
| `orchestrator/registry.py` | Capability and tier-handler registry, validation at load | contracts |
| `orchestrator/state.py` | LangGraph `AgentState` | contracts |
| `orchestrator/graph.py` | Graph wiring, `AsyncPostgresSaver`, gate interrupt | nodes |
| `nodes/discovery.py` | Intent parsing, memory recall, SearXNG pointers | llm, memory |
| `nodes/verifier.py` | Live verification, discrepancy log, freshness | MCP client |
| `nodes/staging.py` | Draft batch, reject unverified dependencies | contracts |
| `nodes/gate.py` | Consequence evaluation, single `interrupt()` | registry |
| `nodes/executor.py` | 5-step idempotent state machine + tier fallback | ledger, MCP client |
| `nodes/reporter_memory.py` | Ledger-derived report, distiller, noise filter, dedupe | ledger, llm |
| `tools/client.py` | Typed MCP client wrapper with error taxonomy (`RetriableTierError`, `TerminalToolError`) | `fastmcp` |
| `mcp_servers/*` | Tier 1–4 FastMCP servers, each runnable as its own process | provider SDKs |
| `api/` | FastAPI routers, auth, SSE | orchestrator |

Dependency rule: `core` imports nothing from other packages; `nodes` never import provider SDKs directly — only the MCP client. This keeps every node testable with in-memory fakes. Enforced with `import-linter` contracts.
