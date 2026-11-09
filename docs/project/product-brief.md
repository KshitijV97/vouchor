# Project brief — Vouchor

- **Status:** proposed (awaiting owner review)
- **Source vision:** [ATEP blueprint](vision/atep-blueprint.md)
- **Last reviewed:** 2026-11-09

## Problem and context

Agent frameworks that let an LLM call tools in a best-effort loop fail in predictable ways once they act in the real world:

- they trust stale search snippets as facts;
- they ask for permission per click (annoying) or not at all (dangerous);
- they treat an HTTP `200 OK` or a DOM click as proof that something happened;
- a retry after a timeout sends the same email twice;
- their "memory" fills up with execution noise.

Vouchor is a self-hosted, open-source durable execution engine that implements the Autonomous Tiered Execution Platform (ATEP) blueprint. Its name reflects the core promise: **every action it takes is vouched for** — verified before it is prepared, approved before it is executed, and proven after it is executed.

## Users and stakeholders

See [stakeholders](stakeholders.md). Primary users are technically capable individuals and small teams who want an assistant that acts on their behalf (email, calendar, notes, vendor outreach, web forms) without giving up control or running on a paid SaaS.

## Outcomes and success signals

| Outcome | Signal / baseline / target | Review period |
|---|---|---|
| Zero duplicate side effects | Fault-injection suite: 0 duplicate emails/events across retry scenarios (`NFR-004`) | Every CI run |
| One approval per batch | A batch of N consequential actions produces exactly one human approval request (`FR-010`) | Every CI run |
| Fully local operation | Whole stack and full test suite run on one laptop with no paid API (`NFR-001`, `CON-001`) | Every release |
| Portable deployment | Same Helm chart deploys to a local kind cluster and to at least one cloud provider via OpenTofu (`NFR-009`) | Every release |
| Trustworthy reports | Report numbers match ledger rows exactly (`FR-020`) | Every CI run |

## Boundaries and non-goals

- In scope: the six ATEP invariants; Tier 1–4 execution; Gmail/SMTP/IMAP, Google Calendar, Google Keep (API or browser) and generic web-form capabilities; local Compose stack; Kubernetes deployment through Helm and OpenTofu; three tiers of documentation.
- Out of scope for v1: multi-tenant SaaS hosting, a graphical workflow builder, mobile apps, paid-API-only features, financial transactions of any kind (`BR-005`).

## Environment and constraints

Python 3.12+, FOSS-only dependencies (`CON-001`), offline-capable test suite (`NFR-001`), container images that run unchanged on a laptop and on any conformant Kubernetes cluster (`CON-003`).

## Assumptions, risks, and open questions

| Item | Type | Owner | Review date / resolution |
|---|---|---|---|
| Product name "Vouchor" (from the repository folder) is final | Assumption | Owner | Before first public release |
| Google Keep has no public API for consumer accounts; Keep is reached through Tier 3 browser automation unless a Workspace API is available | Assumption | Owner | Phase 5 |
| Real Gmail/Calendar demos need the user's own Google Cloud OAuth client; CI uses fakes and Mailpit only | Constraint | Owner | Phase 5 |
| Local LLMs may be too weak for reliable intent parsing; mitigated by deterministic playbooks and an OpenAI-compatible endpoint option | Risk | Owner | Phase 3 |
| Browser automation of third-party sites can break or violate terms of service | Risk | Owner | Phase 3; Tier 3 is opt-in per capability |
| Licence: AGPL-3.0-or-later proposed in [ADR-009](decisions/ADR-009-license-agpl-3-0-or-later.md) | Decision | Owner | Before first public release |

## Related artifacts

- Requirements: [requirements/](requirements/functional-requirements.md)
- Architecture: [architecture/overview.md](architecture/overview.md)
- Decisions: [decisions/](decisions/README.md)
- Implementation plan: [implementation-plan.md](implementation-plan.md)
- Documentation strategy: [documentation-strategy.md](documentation-strategy.md)
