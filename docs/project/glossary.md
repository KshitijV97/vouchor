# Glossary

| Term | Definition | Preferred use / source |
|---|---|---|
| ATEP | Autonomous Tiered Execution Platform — the architecture blueprint Vouchor implements | [blueprint](vision/atep-blueprint.md) |
| Capability | A high-level intent (e.g. `send_email`, `create_calendar_event`) with handlers for one or more tiers and a read-back verifier | Registry |
| Tier | Execution route ordered by determinism: 1 Connector, 2 Skill, 3 Browser, 4 Sandbox | Invariant 1 |
| Tier fallback | Automatic move to the next tier after a retriable failure, recorded as a `RouteAttempt` | `FR-003` |
| Untrusted pointer | A search result or snippet; may only guide where to look, never be used as a fact | `FR-005` |
| Verified attribute | A fact fetched from a live source with evidence snippet and timestamp | `FR-006` |
| Staged action | A fully prepared, not-yet-executed action awaiting approval | `FR-009` |
| Consequential | A tool that mutates external state, acts in the user's name, or costs money/reputation | `BR-001` |
| Consequence gate | The single human-approval checkpoint for a batch of consequential actions | `FR-010` |
| Idempotency key | Deterministic hash identifying one logical side effect | `FR-013` |
| Read-back | Independent, out-of-band check that a side effect really happened | `FR-014` |
| Execution ledger | Append-oriented Postgres table recording every action's lifecycle | `FR-013` |
| Durable memory | Distilled long-lived facts: preferences, decision rules, verified entity facts | `FR-021` |
| Thread | One user request and its durable graph run | LangGraph |
