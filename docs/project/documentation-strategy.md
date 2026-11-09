# Documentation strategy

- **Status:** proposed
- **Last reviewed:** 2026-11-09
- **Related:** `NFR-011`, [implementation plan](implementation-plan.md)

Vouchor documentation has three tiers for three different readers. All tiers are Markdown in this repository and render on the documentation site (Zensical); the site never holds content that is not in Git.

| Tier | Reader | Question it answers | Location | Site section |
|---|---|---|---|---|
| **Tier 1 — Product** | Anyone: users, decision makers, curious visitors | What is Vouchor and why should I care? | `README.md`, `docs/index.md` | Home |
| **Tier 2 — Use it** | People who want to run Vouchor and get things done | How do I set it up and use it for real tasks? | `docs/guide/` | Guide |
| **Tier 3 — How it was built** | Software engineers learning to build such a system | How was this built from zero to completion, and why this way? | `docs/build/` (journal) + `docs/project/` (reference) + `specs/` | Build journal, Engineering reference |

## Tier 1 — Product

Plain language, no jargon without explanation, no code beyond a three-line quickstart. Must stay honest about project status. Content: problem, promise (the six guarantees in plain words), how it works (one diagram), use-case highlights, local-first and self-hosted story, status and roadmap, links to Tier 2 and Tier 3.

## Tier 2 — Use it (guide with demonstrations)

Task-oriented walkthroughs. Every walkthrough shows the request, what Vouchor verifies, the approval screen, the result, and the read-back proof. Each walkthrough is backed by an e2e test so it cannot silently rot.

| Page | Content | Delivered in |
|---|---|---|
| `guide/index.md` | What you can do; how a request flows | P0 (outline) |
| `guide/install-local.md` | Docker + uv, `make setup up`, choosing an LLM | P0 |
| `guide/first-request.md` | Create a thread, review, approve, read the report | P1 |
| `guide/connect-google.md` | Create your own Google OAuth client, scopes, `vouchor connect google` | P5 |
| `guide/use-cases/send-email-gmail.md` | Send email through Gmail, see `Message-ID` read-back | P5 |
| `guide/use-cases/read-email.md` | Search and summarise your inbox (read-only, no approval needed) | P5 |
| `guide/use-cases/schedule-calendar-event.md` | Create a Google Calendar event; idempotent event IDs | P5 |
| `guide/use-cases/add-note-keep.md` | Add a note to Keep; API vs browser fallback | P5 |
| `guide/use-cases/vendor-outreach.md` | The seven-vendor batch scenario end to end | P5 |
| `guide/approvals.md` | Approve, reject, edit; what happens on failure | P1, P5 |
| `guide/deploy-cloud.md` | Deploy with OpenTofu + Helm to kind or a cloud | P7 |
| `guide/troubleshooting.md` | Common errors, reading the ledger | P5–P7 |

## Tier 3 — How it was built

Two complementary parts:

1. **Build journal** (`docs/build/`) — a narrative, chronological, reproducible account. One chapter per phase, written at the phase's converge step, covering: goal, design decisions and the alternatives rejected (linking ADRs), the code walk-through of key modules, the tests that prove it (with their commands), what went wrong and how it was fixed, and the exact commit/tag where the chapter ends so a reader can check out and follow along.

   | Chapter | Phase |
   |---|---|
   | `00-the-idea-and-the-blueprint.md` | Before P0 |
   | `01-foundation-and-walking-skeleton.md` | P0 |
   | `02-contracts-ledger-and-durable-hitl.md` | P1 |
   | `03-exactly-once-execution.md` | P2 |
   | `04-ground-truth-verification-and-browser.md` | P3 |
   | `05-reports-and-memory.md` | P4 |
   | `06-real-integrations-gmail-calendar-keep.md` | P5 |
   | `07-production-hardening.md` | P6 |
   | `08-cloud-deployment-and-release.md` | P7 |

2. **Engineering reference** (`docs/project/`, `specs/`) — the canonical CraftRail records: requirements, architecture views, ADRs, contracts, feature specs and verification evidence. The journal links into these rather than duplicating them.

## Rules

- Tier 1 claims must be true for the current release; planned features are labelled "planned".
- A Tier 2 page ships only with its backing e2e test.
- A journal chapter is written when its phase closes and is not rewritten later; corrections are added as dated notes.
- The CraftRail framework guides in `docs/framework/` remain available as the "Engineering workflow" section.
