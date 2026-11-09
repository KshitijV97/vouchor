# Repository structure

CraftRail separates reusable framework guidance from the adopting project's own intent and from feature-specific change records. This prevents a template from being mistaken for a requirement and keeps each record close to its owner.

```text
AGENTS.md                         Canonical shared agent instructions
CLAUDE.md                         Minimal Claude Code import adapter
docs/
├── framework/                    How to use and maintain CraftRail
├── project/                      Adopter-owned project context and registers
└── examples/                     Clearly illustrative walkthroughs
specs/
├── README.md                     Feature folder conventions
└── NNN-feature-name/              One feature's spec, plan, tasks, verification
templates/                         Blank starting points used by humans/tools
scripts/                           Standard-library helper tools
tests/                             Tests for the helper tools
zensical.toml                      Documentation navigation and presentation
vercel.json                        Static docs build/output configuration
```

## What belongs where

| Path | Owner and purpose | Should not become |
|---|---|---|
| `AGENTS.md` | Compact project navigation and shared working rules that apply to any agent. | A copy of the full handbook or a provider's business logic. |
| `CLAUDE.md` | One-line import adapter so Claude Code reads shared instructions. | A separately maintained Claude policy. |
| `docs/framework/` | Framework concepts, methods, limits, and tool operation. | Project-specific business requirements. |
| `docs/project/` | Product brief, principles, stakeholder notes, requirements, architecture, decisions, and contracts for an adopter. | A parallel copy of existing authoritative docs. |
| `specs/` | Feature-sized scope, implementation plan, work items, and verification. | A permanent architecture encyclopedia. |
| `templates/` | Blank reusable content patterns. | An authoritative statement of project policy. |
| `docs/examples/` and `specs/000-example-feature/` | Illustrations explaining the framework. | Verified product behavior or a production-ready design. |
| `site/` | Generated website output. | Hand-edited canonical content. |

## Why keep framework docs apart from project docs

The framework needs stable explanations of how to write an ADR or verify a requirement. A consuming project needs to decide its own retention policy or latency objective. Keeping those in separate directories makes ownership explicit. A project can copy or customize `docs/project/` without rewriting the framework explanation, and can adopt the framework incrementally without accepting every starter example as policy.

## Why each feature has four core files

- `spec.md` records intent and the accepted outcome.
- `plan.md` records the proposed technical approach and its tradeoffs.
- `tasks.md` turns the approach into reviewable implementation work.
- `verification.md` records which criteria were checked and what evidence exists.

These files mirror distinct review questions. Small projects may combine or shorten them, but preserving the separation becomes useful when a decision changes after approval or when verification is delegated to someone other than the implementer. Diagrams live in a feature subdirectory when they help explain that feature.

## Adapting the layout

Paths are recommendations, not a repository migration requirement. Existing teams may use `requirements/`, `architecture/`, or an issue tracker already. Record canonical locations in `docs/project/README.md`, then link to existing sources rather than creating duplicates. If a project has a generator that owns docs, identify source versus generated files and avoid editing generated output.

## Naming and numbering

Feature folders use a zero-padded sequence and a human-readable slug, such as `001-user-authentication/`. The number makes paths stable and sortable; the slug helps humans navigate. The initializer selects the next number it finds and refuses a conflicting target. Do not renumber folders after links exist. The special `000-example-feature/` directory is illustrative and not part of the sequence.
