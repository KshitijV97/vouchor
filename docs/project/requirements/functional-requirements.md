# Functional requirements

> Derived from the [ATEP blueprint](../vision/atep-blueprint.md). Status `proposed` until the owner approves. "Phase" refers to the [implementation plan](../implementation-plan.md).

| ID | Requirement | Rationale/source | Acceptance / verification | Status |
|---|---|---|---|---|
| FR-001 | The system MUST resolve every capability through a registry that lists handlers per tier (1 Connector, 2 Skill, 3 Browser, 4 Sandbox) and select the lowest healthy, configured tier first. | Invariant 1 | Unit tests on registry selection; Phase 2 | proposed |
| FR-002 | Each capability MUST declare a consequence level (`READ_ONLY` or `CONSEQUENTIAL`); a `CONSEQUENTIAL` capability MUST declare a read-back verifier for every tier it can execute on. | Invariants 4, 5 | Registry load fails on violation; Phase 1 | proposed |
| FR-003 | On a retriable tier failure the system MUST record a `RouteAttempt` (tier, tool, time, error type, message) in the ledger and retry on the next configured tier. | Invariant 1 | Integration test "cascading fallback"; Phase 2 | proposed |
| FR-004 | When all executable tiers fail, the system MUST fall back to Tier 4 and produce a ready-to-use local artifact (e.g. `.eml`, `.ics`, `.csv`) unless the capability forbids it, and MUST report the inability clearly. | Invariant 1 | Integration test; Phase 2 | proposed |
| FR-005 | Search results (SearXNG) MUST be typed as untrusted pointers and MUST NOT be accepted as a verified dependency of a staged action. | Invariant 2 | Type-level + unit tests; Phase 3 | proposed |
| FR-006 | Every critical entity attribute used by a staged action MUST be verified from a live source (direct API or live DOM) and stored with source URI, method, raw evidence snippet and timestamp. | Invariant 2 | Integration test against mock storefront; Phase 3 | proposed |
| FR-007 | When a live source contradicts a search snippet, the verifier MUST use the live value and record the discrepancy. | Invariant 2 | Integration test "stale snippet"; Phase 3 | proposed |
| FR-008 | Verified attributes MUST carry a freshness window per attribute type; expired attributes MUST be re-verified before staging. | Invariant 2 (freshness) | Unit test with frozen clock; Phase 3 | proposed |
| FR-009 | Discovery, verification and drafting for all targets in a batch MUST complete before any human approval is requested. | Invariant 3 | Graph test: no interrupt before staging finishes; Phase 1 | proposed |
| FR-010 | A batch containing one or more consequential actions MUST suspend at exactly one consequence-gate checkpoint presenting all drafts and their verified metadata. | Invariant 4 | Graph test "7 vendors, 1 interrupt"; Phase 1 | proposed |
| FR-011 | At the gate the user MUST be able to approve, reject, or edit each staged action individually; edits MUST be re-validated before execution. | Invariant 4 | API + graph tests; Phase 1 | proposed |
| FR-012 | Suspended threads MUST survive process restarts and resume from the persisted checkpoint. | Durability | Integration test: kill and resume; Phase 1 | proposed |
| FR-013 | Every consequential action MUST have a deterministic idempotency key and a ledger row whose status follows the allowed state machine (`STAGED → APPROVED → ATTEMPTED_UNVERIFIED → VERIFIED_SUCCESS / PARTIAL_RECOVERED / FAILED_TERMINAL`, or `REJECTED_BY_USER`). | Invariant 5 | Property tests on transitions; Phase 1–2 | proposed |
| FR-014 | An action MUST be marked successful only after an out-of-band read-back confirms the side effect; a tool's own success response is not sufficient. | Invariant 5 | Integration tests per connector; Phase 2 | proposed |
| FR-015 | Before retrying an `ATTEMPTED_UNVERIFIED` action, the executor MUST run read-back first and mark `PARTIAL_RECOVERED` if the side effect exists. | Invariant 5 | Fault-injection test "timeout after accept"; Phase 2 | proposed |
| FR-016 | The executor MUST stamp each side effect with an identifier derived from its idempotency key wherever the target system allows (email `Message-ID`, calendar event ID, note label) so read-back can match it exactly. | Invariant 5; [ADR-007](../decisions/ADR-007-provider-native-idempotency-markers.md) | Integration tests; Phase 2, 5 | proposed |
| FR-017 | Only one executor MAY run a given idempotency key at a time, across processes and replicas. | Invariant 5 | Concurrency test with parallel workers; Phase 2 | proposed |
| FR-018 | The gateway MUST expose REST endpoints to create a thread, read its state, list staged actions, and approve/reject/edit them. | Blueprint Phase 1 | OpenAPI contract tests; Phase 1 | proposed |
| FR-019 | The gateway MUST stream thread progress events to clients via Server-Sent Events. | Blueprint stack | Integration test; Phase 5 | proposed |
| FR-020 | On termination the system MUST emit a plain-language report derived only from ledger rows (counts per outcome, tier used, recoveries, duplicates = 0). | Invariant 6 | Unit + golden-file tests; Phase 4 | proposed |
| FR-021 | A distiller MUST extract only durable facts (user preference, decision rule, verified entity fact) with confidence ≥ 0.8 and MUST reject candidates describing transient execution. | Invariant 6 | Unit tests on noise filter; Phase 4 | proposed |
| FR-022 | Durable facts MUST be deduplicated by embedding similarity (default threshold 0.92) before upsert. | Invariant 6 | Integration test with pgvector; Phase 4 | proposed |
| FR-023 | A new thread MUST load the top-K (default 5) relevant durable memories during discovery. | Invariant 6 | Integration test; Phase 4 | proposed |
| FR-024 | The system MUST provide capabilities for: sending email, reading/searching email, creating/updating calendar events, and creating notes, each usable through at least one tier. | Tier 2 docs use cases | Use-case scenario tests; Phase 5 | proposed |
| FR-025 | Tier 4 MUST execute generated code only inside an isolated sandbox with no network by default, resource limits, and a writable artifacts directory only. | Invariant 1; security | Sandbox escape-attempt tests; Phase 5 | proposed |
| FR-026 | The gateway MUST authenticate API clients; the approval endpoint MUST only accept the thread owner's credentials. | Security | API tests; Phase 6 | proposed |
