# Autonomous Tiered Execution Platform (ATEP)

**Functional Architecture, Technical Specification & Claude Code Implementation Blueprint**

## Part 1: Executive & Functional Specification

### 1.1 Architectural Philosophy

Most agentic frameworks fail in production because they treat LLM tool-calling as a stateless, best-effort `while` loop. They trust stale search engine snippets, acsk for human permission either too late or too frequently, treat HTTP `200 OK` or DOM click events as proof of completion, and pollute vector databases with noisy execution logs.

The **Autonomous Tiered Execution Platform (ATEP)** is a self-hosted, open-source, durable execution engine built around **six operational invariants**:

1. **Cascading Deterministic Routing (Rule 3):** Tasks are routed through a strict Chain of Responsibility ordered by determinism and verifiability:

   * **Tier 1 (Direct Connectors):** Typed REST/GraphQL/SMTP/IMAP integrations.

   * **Tier 2 (Deterministic Skills):** Multi-step domain playbooks (pre-defined DAGs).

   * **Tier 3 (Live Browser Automation):** Stateful Playwright DOM interaction using accessibility trees.

   * **Tier 4 (Local Sandbox):** Isolated container execution for file generation, data processing, and custom scripting.

   * *Invariant:* A failure at Tier $N$ logs the structured error and automatically falls back to Tier $N+1$ before surfacing an inability to execute.

2. **Ground-Truth Verification Before Action (Rule 4):** Search results (SearXNG) are treated strictly as **untrusted discovery pointers**. Every critical entity attribute (e.g., store email address, stock status, part number, account existence) must be verified by fetching the live source (via API or headless DOM inspection) and capturing a freshness timestamp and raw source proof before moving to preparation.

3. **Upfront Batch Preparation (Rule 5):** Read-only discovery, verification, and artifact drafting run to completion autonomously across all targets in a batch (e.g., drafting inquiries for 7 vendors) before requesting human intervention.

4. **Consequence-Gated Human-in-the-Loop (Rule 6):** Tools are strictly classified as `READ_ONLY` or `CONSEQUENTIAL`. Any action that mutates external state, acts in the user's name, or incurs financial/reputational cost triggers a hard state checkpoint (`INTERRUPT`), presenting the complete batch of prepared drafts and verified target metadata for a single human approval decision.

5. **Idempotent Execution & Read-Back Verification (Rule 7):** Execution is decoupled from completion. Every consequential action is assigned a deterministic idempotency key and requires an out-of-band **Read-Back Verification Hook** (e.g., querying the IMAP `Sent` folder or re-scraping the target page state). If an action fails or times out mid-flight, the retry handler **executes the Read-Back Hook first** to reconcile partial successes and guarantee zero duplicate side effects.

6. **Plain Reporting & Selective Memory Distillation (Rule 8):** Upon workflow termination, the system emits a concise execution report derived from an immutable relational audit ledger. A background distillation pipeline extracts *only* durable facts (user preferences, permanent decisions, verified entity attributes) into long-term vector/relational storage, discarding transient DOM states, drafts, and retry logs.

### 1.2 Self-Hosted Open-Source Stack

All components run locally or on self-hosted infrastructure via Docker Compose with zero paid SaaS dependencies:

| Subsystem | Technology | Role in Architecture |
| ----- | ----- | ----- |
| **Core Orchestrator** | **Python 3.12 + FastAPI + LangGraph** | Durable cyclic state machine with native `PostgresSaver` checkpointing and `interrupt` support. |
| **Tool Protocol** | **FastMCP (Model Context Protocol)** | Decouples Tier 1–4 execution capabilities into standardized, hot-swappable tool servers. |
| **Primary Persistence** | **PostgreSQL 16 + `pgvector`** | Stores LangGraph state checkpoints, the `execution_ledger` idempotency table, relational audit logs, and semantic memory embeddings. |
| **Coordination & Pub/Sub** | **Redis 7** | Distributed idempotency locks, rate-limit counters, and real-time Server-Sent Events (SSE) / WebSocket streaming to the client. |
| **Discovery & Browser** | **SearXNG + Playwright + Crawl4AI** | SearXNG provides zero-cost metasearch discovery; Playwright/Crawl4AI performs live DOM verification (Rule 4) and Tier 3 GUI automation. |
| **Local Sandbox (Tier 4)** | **Docker-in-Docker / Rootless Worker** | Ephemeral Python/Bash workspace with a mounted `/workspace/artifacts` volume for local file generation. |
| **LLM Inference Router** | **LiteLLM / Ollama** | Unified local gateway supporting self-hosted models (Qwen-2.5-Coder, Llama-3.3) or pluggable API endpoints. |
| **Local Email Test Sink** | **Mailpit** | Local SMTP/IMAP server included in the dev stack to deterministically test email sending, network faults, and `Sent` folder read-back verification. |

## Part 2: Technical Architecture & Data Contracts

### 2.1 System Topology & State Machine Flow

```
                      ┌────────────────────────────────────┐
                      │   FastAPI Gateway (REST / SSE)     │
                      └─────────────────┬──────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                     LangGraph Durable State Machine                        │
│                                                                            │
│  ┌──────────────────────┐     Untrusted URLs    ┌───────────────────────┐  │
│  │ 1. Discovery &       │ ────────────────────► │ 2. Ground-Truth       │  │
│  │    Capability Router │                       │    Verifier (Rule 4)  │  │
│  └──────────▲───────────┘                       └───────────┬───────────┘  │
│             │                                               │              │
│     Tier N+1 Fallback                               Verified Entities      │
│             │                                               ▼              │
│  ┌──────────┴───────────┐                       ┌───────────────────────┐  │
│  │ 5. Idempotent        │                       │ 3. Batch Preparation  │  │
│  │    Executor (Rule 7) │                       │    & Staging (Rule 5) │  │
│  └──────────▲───────────┘                       └───────────┬───────────┘  │
│             │                                               │              │
│       Approved Batch                                  Staged Payloads      │
│             │                                               ▼              │
│  ┌──────────┴───────────┐                       ┌───────────────────────┐  │
│  │ 4. Consequence Gate  │ ◄──────────────────── │   Check Consequence   │  │
│  │    (HITL Interrupt)  │    If CONSEQUENTIAL   │       Metadata        │  │
│  └──────────────────────┘                       └───────────────────────┘  │
│             │                                                              │
│             ▼ (Post-Verification)                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ 6. Plain Reporter & Selective Memory Distiller (Rule 8)              │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
         │                          │                           │
         ▼                          ▼                           ▼
┌─────────────────┐      ┌─────────────────────┐     ┌─────────────────────┐
│  PostgreSQL 16  │      │   FastMCP Servers   │     │   Redis 7 Event     │
│ + pgvector      │      │ Tiers 1, 2, 3, & 4  │     │   Bus & Locks       │
└─────────────────┘      └─────────────────────┘     └─────────────────────┘

```

### 2.2 PostgreSQL Schema Definitions (`init.sql`)

Beyond LangGraph's internal checkpoint tables (`checkpoints`, `checkpoint_blobs`, `checkpoint_writes`), the platform enforces state integrity through three dedicated tables:

```
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Ground-Truth Verification Cache (Rule 4)
CREATE TABLE verified_sources (
    verification_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    thread_id TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    attribute_key TEXT NOT NULL,          -- e.g., 'contact_email', 'battery_stock_status'
    attribute_value TEXT NOT NULL,        -- e.g., 'parts@canadacomputers.com'
    source_uri TEXT NOT NULL,             -- Live URL or API endpoint
    verification_method TEXT NOT NULL,    -- 'LIVE_DOM_SCRAPE' | 'DIRECT_API'
    raw_evidence_snippet TEXT NOT NULL,   -- Exact DOM text or JSON fragment proving the fact
    verified_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Idempotent Execution Ledger (Rules 6, 7, 8)
CREATE TYPE execution_status AS ENUM (
    'STAGED',                 -- Drafted and awaiting human approval
    'APPROVED',               -- Approved by user, queued for execution
    'ATTEMPTED_UNVERIFIED',   -- Mutation fired, awaiting read-back confirmation
    'VERIFIED_SUCCESS',       -- Read-back hook confirmed external state change
    'PARTIAL_RECOVERED',      -- Failed mid-flight, but pre-retry read-back confirmed success
    'FAILED_TERMINAL',        -- All tiers and retries exhausted
    'REJECTED_BY_USER'        -- User declined action at HITL gate
);

CREATE TABLE execution_ledger (
    idempotency_key TEXT PRIMARY KEY,     -- sha256(thread_id + capability + target + payload_hash)
    thread_id TEXT NOT NULL,
    capability_name TEXT NOT NULL,        -- e.g., 'vendor_outreach'
    selected_tier SMALLINT NOT NULL,      -- 1: Connector, 2: Skill, 3: Browser, 4: Sandbox
    target_identifier TEXT NOT NULL,      -- e.g., 'parts@canadacomputers.com'
    staged_payload JSONB NOT NULL,        -- Exact parameters approved by the user
    status execution_status NOT NULL DEFAULT 'STAGED',
    attempt_count INT NOT NULL DEFAULT 0,
    route_history JSONB NOT NULL DEFAULT '[]'::jsonb, -- Array of failed tier attempts & reasons
    readback_proof JSONB,                 -- e.g., {"imap_message_id": "<...>", "folder": "Sent"}
    last_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ledger_thread ON execution_ledger(thread_id);

-- 3. Selective Durable Memory Store (Rule 8)
CREATE TYPE memory_category AS ENUM (
    'USER_PREFERENCE',
    'DECISION_RULE',
    'VERIFIED_ENTITY_FACT'
);

CREATE TABLE durable_memories (
    memory_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category memory_category NOT NULL,
    subject_entity TEXT NOT NULL,         -- e.g., 'Canada Computers', 'User'
    fact_statement TEXT NOT NULL,         -- Concise, self-contained factual statement
    structured_metadata JSONB DEFAULT '{}'::jsonb,
    embedding vector(768),                -- Sized for nomic-embed-text (Ollama)
    source_thread_id TEXT NOT NULL,
    confidence_score FLOAT NOT NULL DEFAULT 1.0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(category, subject_entity, fact_statement)
);

CREATE INDEX idx_memory_embedding ON durable_memories USING hnsw (embedding vector_cosine_ops);

```

### 2.3 Core Python Data Contracts (`src/core/contracts.py`)

All state transitions inside LangGraph must validate against strict Pydantic v2 models:

```
from datetime import datetime
from enum import Enum, IntEnum
from typing import Any, Annotated
import operator
from pydantic import BaseModel, Field, HttpUrl, computed_field
import hashlib
import json

class ExecutionTier(IntEnum):
    TIER_1_CONNECTOR = 1
    TIER_2_SKILL = 2
    TIER_3_BROWSER = 3
    TIER_4_SANDBOX = 4

class ConsequenceLevel(str, Enum):
    READ_ONLY = "READ_ONLY"
    CONSEQUENTIAL = "CONSEQUENTIAL"

class ExecutionStatus(str, Enum):
    STAGED = "STAGED"
    APPROVED = "APPROVED"
    ATTEMPTED_UNVERIFIED = "ATTEMPTED_UNVERIFIED"
    VERIFIED_SUCCESS = "VERIFIED_SUCCESS"
    PARTIAL_RECOVERED = "PARTIAL_RECOVERED"
    FAILED_TERMINAL = "FAILED_TERMINAL"
    REJECTED_BY_USER = "REJECTED_BY_USER"

class VerifiedAttribute(BaseModel):
    """Enforces Rule 4: Cannot be instantiated from a search snippet alone."""
    entity_name: str
    attribute_key: str
    attribute_value: str
    source_uri: str
    verification_method: str = Field(pattern="^(LIVE_DOM_SCRAPE|DIRECT_API)$")
    raw_evidence_snippet: str = Field(min_length=5)
    verified_at: datetime

class RouteAttempt(BaseModel):
    tier: ExecutionTier
    tool_name: str
    timestamp: datetime
    error_type: str
    error_message: str

class StagedAction(BaseModel):
    """Enforces Rules 5, 6, and 7."""
    thread_id: str
    capability_name: str
    consequence: ConsequenceLevel
    current_tier: ExecutionTier
    target_identifier: str
    summary_for_user: str
    payload: dict[str, Any]
    verified_dependencies: list[VerifiedAttribute] = Field(min_length=1)
    status: ExecutionStatus = ExecutionStatus.STAGED
    route_history: list[RouteAttempt] = Field(default_factory=list)
    readback_proof: dict[str, Any] | None = None
    last_error: str | None = None

    @computed_field
    @property
    def idempotency_key(self) -> str:
        canonical_payload = json.dumps(self.payload, sort_keys=True)
        raw = f"{self.thread_id}:{self.capability_name}:{self.target_identifier}:{canonical_payload}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

class DurableFactCandidate(BaseModel):
    """Enforces Rule 8: Output contract for the Memory Distiller."""
    category: str = Field(pattern="^(USER_PREFERENCE|DECISION_RULE|VERIFIED_ENTITY_FACT)$")
    subject_entity: str
    fact_statement: str
    confidence_score: float = Field(ge=0.8, le=1.0)

```

### 2.4 Detailed Component Mechanics

#### 1. The Tiered Capability Registry (`src/orchestrator/registry.py`)

Every high-level intent (e.g., `send_message`, `check_inventory`, `publish_post`) maps to a `CapabilityDefinition`. Each capability registers handlers for Tiers 1 through 4, alongside a paired **Read-Back Verifier**:

```
class TierHandler(BaseModel):
    tier: ExecutionTier
    mcp_server: str
    tool_name: str
    readback_tool_name: str | None = None  # Required if capability is CONSEQUENTIAL

```

When executing a capability:

1. The router queries the registry for the lowest numerical `ExecutionTier` configured and healthy for that user/service.

2. If execution raises a `RetriableTierError` (e.g., missing OAuth token, HTTP 403/404, DOM selector change), the router appends a `RouteAttempt` to `action.route_history`, increments `action.current_tier` to the next available tier, and retries immediately.

3. If `ExecutionTier.TIER_4_SANDBOX` is reached, the system falls back to generating a local artifact (e.g., a CSV, script, or pre-formatted file) so the user still receives actionable output.

#### 2. Ground-Truth Verification Engine (`src/nodes/verifier.py`)

To satisfy Rule 4:

* Search tools (`searxng_search`) return objects tagged with `untrusted_snippet=True`.

* The `StagingNode` is programmed to reject any `StagedAction` whose `verified_dependencies` list is empty or contains unverified snippets.

* The `VerifierNode` takes candidate URLs or entities from discovery and dispatches **Crawl4AI / Playwright** (or a Tier 1 read API) to inspect the live page. It extracts the target attribute (such as an email address matching a regex or a specific battery SKU on the page) and records the exact surrounding DOM text into `raw_evidence_snippet`.

#### 3. Idempotent Executor & Pre-Retry Read-Back (`src/nodes/executor.py`)

The execution loop for each approved `StagedAction` follows a strict 5-step state machine:

```
┌───────────────────────────────────────────────────────────────────┐
│ 1. Query `execution_ledger` by `action.idempotency_key`           │
└───────────────┬───────────────────────────────────────────────────┘
                │
                ├──► Status == VERIFIED_SUCCESS or PARTIAL_RECOVERED?
                │         └──► Return cached proof immediately (No-Op).
                │
                ├──► Status == ATTEMPTED_UNVERIFIED? (Previous crash/timeout)
                │         └──► Run `readback_tool` FIRST!
                │               ├──► Proof found? -> Mark PARTIAL_RECOVERED & Return.
                │               └──► Proof absent? -> Proceed to Step 2 (Safe to retry).
                │
                ▼
┌───────────────────────────────────────────────────────────────────┐
│ 2. Set Ledger Status = ATTEMPTED_UNVERIFIED (Commit to Postgres)  │
└───────────────┬───────────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────────────┐
│ 3. Invoke Primary Tool via FastMCP (`action.current_tier`)        │
└───────────────┬───────────────────────────────────────────────────┘
                │
                ├──► Tool threw exception?
                │         └──► Run `readback_tool` (Check if side-effect occurred anyway)
                │               ├──► Proof found? -> Mark PARTIAL_RECOVERED.
                │               └──► Proof absent? -> Fallback to next Tier or Retry.
                │
                ▼
┌───────────────────────────────────────────────────────────────────┐
│ 4. Poll `readback_tool` with Exponential Backoff ($2^0, 2^1, 2^2$s) │
└───────────────┬───────────────────────────────────────────────────┘
                │
                ├──► Proof verified -> Set Status = VERIFIED_SUCCESS + Save Proof.
                └──► Poll exhausted -> Raise VerificationTimeoutError.

```

## Part 3: Claude Code Scaffolding & Iteration Blueprint

> **Usage Instructions:** Save this file as `CLAUDE.md` (or `AGENTIC_PLATFORM_SPEC.md`) in the root of an empty repository. Open `claude` in your terminal and instruct it:
> *"Read `AGENTIC_PLATFORM_SPEC.md` and execute Phase 1. Do not proceed to Phase 2 until all Phase 1 verification gates pass."*

### 3.1 Target Repository Structure

Claude Code must scaffold and maintain this exact directory layout:

```
atep-platform/
├── CLAUDE.md                        # This architectural specification
├── docker-compose.yml               # Postgres (pgvector), Redis, SearXNG, Mailpit
├── pyproject.toml                   # Poetry / uv dependency management (Python 3.12+)
├── .env.example                     # Environment variables template
├── migrations/
│   └── 001_init_schema.sql          # DDL for verified_sources, execution_ledger, durable_memories
├── src/
│   ├── __init__.py
│   ├── config.py                    # Pydantic Settings
│   ├── main.py                      # FastAPI application entrypoint & SSE endpoints
│   ├── core/
│   │   ├── contracts.py             # Pydantic v2 models & enums
│   │   ├── db.py                    # AsyncPG pool & ledger repository methods
│   │   └── llm.py                   # LiteLLM / Ollama client wrapper
│   ├── orchestrator/
│   │   ├── state.py                 # LangGraph AgentState TypedDict
│   │   ├── registry.py              # Tiered Capability Registry (Tiers 1-4)
│   │   └── graph.py                 # StateGraph definition, edges, PostgresSaver, interrupts
│   ├── nodes/
│   │   ├── discovery.py             # Node 1: Intent parsing & untrusted discovery
│   │   ├── verifier.py              # Node 2: Rule 4 live DOM/API ground-truth verifier
│   │   ├── staging.py               # Node 3: Rule 5 upfront batch preparation
│   │   ├── gate.py                  # Node 4: Rule 6 consequence evaluation & HITL interrupt
│   │   ├── executor.py              # Node 5: Rule 7 idempotent execution + read-back + tier fallback
│   │   └── reporter_memory.py       # Node 6: Rule 8 plain reporting & durable memory distillation
│   └── mcp_servers/
│       ├── tier1_connectors.py      # FastMCP: Direct SMTP/IMAP (Mailpit/Gmail) & REST connectors
│       ├── tier2_skills.py          # FastMCP: Deterministic multi-step playbooks
│       ├── tier3_browser.py         # FastMCP: Playwright live DOM scraper & form automation
│       └── tier4_sandbox.py         # FastMCP: Local workspace file/spreadsheet generator
└── tests/
    ├── conftest.py
    ├── test_phase1_hitl_graph.py
    ├── test_phase2_idempotency_readback.py
    ├── test_phase3_verifier_fallback.py
    └── test_phase4_memory_distillation.py

```

### 3.2 Strict Engineering Rules for Claude Code

1. **Tooling & Environment:** Use `uv` (or `poetry`) for Python dependency management. Target Python 3.12+.

2. **Strict Typing:** All functions and methods must have full type annotations. Run `mypy --strict src/` at the end of every phase.

3. **Async Native:** Use `asyncio`, `httpx.AsyncClient`, `psycopg` (v3 async) for `langgraph-checkpoint-postgres`, and `asyncpg` for ledger queries. Never use blocking `requests` or `time.sleep` inside async nodes.

4. **Zero Paid API Lock-in:** Default all LLM calls to a local Ollama endpoint (`http://localhost:11434`) or configurable OpenAI-compatible base URL via `pydantic-settings`. Provide deterministic mock LLM responses in `pytest` fixtures so all architectural tests run offline in milliseconds.

5. **No Silent Exceptions:** Every tier failure must be caught, structured into a `RouteAttempt` model, and persisted to `execution_ledger.route_history`.

### 3.3 Phased Implementation Runbook (Prompts for Claude Code)

#### Phase 1: Infrastructure, Database & Durable HITL State Graph

**Objective:** Stand up the Docker infrastructure, apply database migrations, implement the Pydantic contracts, and prove that the LangGraph state machine can stage a batch of actions, suspend execution to PostgreSQL on a consequential action, and resume upon user approval.

* **Tasks for Claude Code:**

  1. Create `docker-compose.yml` with:

     * `pgvector/pgvector:pg16` (Port 5432, auto-mounting `./migrations/001_init_schema.sql` into `/docker-entrypoint-initdb.d/`).

     * `redis:7-alpine` (Port 6379).

     * `axllent/mailpit:latest` (SMTP on 1025, HTTP UI/API on 8025, IMAP enabled) for local email testing.

     * `searxng/searxng:latest` (Port 8080, configured with JSON format enabled).

  2. Create `pyproject.toml` with dependencies: `fastapi`, `uvicorn`, `langgraph`, `langgraph-checkpoint-postgres`, `psycopg[binary,pool]`, `asyncpg`, `pydantic>=2.7`, `pydantic-settings`, `httpx`, `redis`, `fastmcp`, `playwright`, `pytest`, `pytest-asyncio`, `mypy`.

  3. Implement `src/core/contracts.py` and `src/orchestrator/state.py`.

  4. Implement `src/orchestrator/graph.py` with `AsyncPostgresSaver` and `interrupt_before=["executor"]` when `StagedAction.consequence == ConsequenceLevel.CONSEQUENTIAL`.

  5. Expose FastAPI endpoints in `src/main.py`:

     * `POST /threads` (starts a task, runs Discovery -> Verifier -> Staging, and returns the staged batch if interrupted at the Consequence Gate).

     * `POST /threads/{thread_id}/approve` (accepts approved/modified `StagedAction` payloads and resumes graph execution).

* **Phase 1 Verification Gate:**

  * Run `docker compose up -d` and verify Postgres, Redis, and Mailpit are healthy.

  * Run `pytest tests/test_phase1_hitl_graph.py` which creates a thread with 7 staged vendor outreach tasks, asserts the graph pauses at the `gate` node, inspects Postgres to confirm `execution_ledger` shows 7 rows in `STAGED` status, invokes the resume command, and asserts completion.

#### Phase 2: Idempotent Executor, Pre-Retry Read-Back & Cascading Fallbacks

**Objective:** Implement Rules 3 and 7. Build the Tier 1 Email Connector against Mailpit, implement the Read-Back Verification Hook, and prove that a simulated mid-flight network timeout does not result in duplicate emails on retry.

* **Tasks for Claude Code:**

  1. Implement `src/mcp_servers/tier1_connectors.py` with two tools:

     * `send_smtp_email(recipient, subject, body)`: Sends email via `aiosmtplib` to Mailpit (Port 1025).

     * `verify_email_sent(recipient, subject)`: Queries Mailpit's REST/IMAP inspection API (`http://localhost:8025/api/v1/messages`) to verify the exact recipient and subject exist in the sent messages store, returning the message ID and timestamp as `readback_proof`.

  2. Implement `src/nodes/executor.py` with the 5-step idempotency state machine:

     * Check `execution_ledger` by `idempotency_key`.

     * If `ATTEMPTED_UNVERIFIED`, run `verify_email_sent` **before** re-sending. If found, transition to `PARTIAL_RECOVERED`.

     * Implement the Tier fallback loop: if Tier 1 raises `ConnectionRefusedError` or `TierUnavailableError`, log the `RouteAttempt` and automatically fall back to Tier 2, Tier 3, or Tier 4 (`src/mcp_servers/tier4_sandbox.py` which writes ready-to-send `.eml` draft files to `/workspace/artifacts`).

* **Phase 2 Verification Gate:**

  * Run `pytest tests/test_phase2_idempotency_readback.py` covering three scenarios:

    1. **Batch Execution:** 7 vendor emails sent and verified via read-back hook (`VERIFIED_SUCCESS`).

    2. **Partial Failure Recovery (The "Canada Computers Retry" Test):** Inject a fault that raises a `TimeoutError` *after* the SMTP message is accepted by Mailpit on vendor #4, leaving the ledger in `ATTEMPTED_UNVERIFIED`. Trigger a retry run and assert that `executor.py` detects the message in Mailpit via the read-back hook, updates status to `PARTIAL_RECOVERED`, and confirms Mailpit contains **1 copy** of the email (not 2).

    3. **Cascading Fallback:** Disable Tier 1 connector for vendor #5 and assert the executor automatically falls back to the next configured tier and records the failure reason in `route_history`.

#### Phase 3: Ground-Truth Verifier & Live Browser Automation

**Objective:** Implement Rule 4 (Anti-Snippet Verification) and Tier 3 (Playwright Headless Browser execution).

* **Tasks for Claude Code:**

  1. Implement `src/mcp_servers/tier3_browser.py` using `playwright.async_api`:

     * `verify_live_page_fact(url, target_attribute, regex_or_selector)`: Navigates to the live URL, waits for DOM settle, extracts the accessibility tree / visible text, verifies the fact exists on the live page, and returns a populated `VerifiedAttribute` object.

     * `execute_browser_form(url, form_actions)`: Serializes interactive DOM elements (`button`, `input`, `textarea`) with numerical indices, executes form fills/clicks, and captures post-submission DOM state for read-back verification.

  2. Implement `src/nodes/verifier.py`:

     * Takes candidate URLs from `discovery.py` (SearXNG).

     * Rejects stale snippets if live page verification fails (e.g., if a search snippet claims a store email is `sales@example.com`, but the live contact page shows `parts@example.com`, the verifier overwrites the attribute with the live DOM value and logs the discrepancy).

* **Phase 3 Verification Gate:**

  * Run `pytest tests/test_phase3_verifier_fallback.py` which spins up a lightweight local FastAPI mock vendor storefront with a live DOM contact page and web contact form, verifies live attribute extraction overrides stale search snippet data, and executes a Tier 3 Playwright form submission with DOM read-back confirmation.

#### Phase 4: Plain Reporter & Selective Memory Distiller

**Objective:** Implement Rule 8. Generate clean human-readable execution summaries and distill *only* durable facts into `pgvector`, keeping routine execution chatter out of memory.

* **Tasks for Claude Code:**

  1. Implement `src/nodes/reporter_memory.py`:

     * **Reporter:** Reads all rows for `thread_id` from `execution_ledger` and formats a structured plain-English report (e.g., *"6/7 emails sent and verified via Tier 1. 1/7 (Canada Computers) recovered after timeout via Sent-folder read-back check. 0 duplicates."*).

     * **Selective Memory Distiller:** Passes the initial user request, verified attributes, and user approval modifications through a strict distillation prompt returning `list[DurableFactCandidate]`.

     * **Noise Filter Guardrail:** Explicitly reject any candidate fact containing transient execution verbs (`"clicked"`, `"retried"`, `"timed out"`, `"drafted"`, `"status"`).

     * **Upsert & Deduplicate:** Compute embeddings via Ollama (`nomic-embed-text`) or a deterministic local embedding model, check cosine similarity in `durable_memories` (threshold $> 0.92$), and upsert into PostgreSQL.

  2. Update `src/nodes/discovery.py` to query top-$K$ ($K=5$) relevant `durable_memories` at the start of every new thread so previously verified vendor emails and user preferences are loaded immediately without re-asking the user.

* **Phase 4 Verification Gate:**

  * Run `pytest tests/test_phase4_memory_distillation.py` to confirm that after a 7-store outreach run, `durable_memories` stores the verified store contact emails and user formatting preferences, stores **zero** routine execution steps, and automatically pre-populates those verified facts on a subsequent thread.
