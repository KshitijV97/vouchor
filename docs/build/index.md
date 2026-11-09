# Build journal: how Vouchor was made

> **Tier 3 documentation.** A chronological engineering account of building Vouchor from an empty folder to a released, cloud-deployable system. It's written for software engineers who want to learn by following along. Each chapter ends at a Git tag, so you can check out the code exactly as it was.

## How to read this journal

Each chapter covers:

- **Goal:** what the phase had to prove.
- **Decisions:** what was chosen, what was rejected, and why (linked to [ADRs](../project/decisions/README.md)).
- **Walk-through:** the important modules, explained.
- **Proof:** the tests that show it works, with the exact commands.
- **What went wrong:** problems found and how they were fixed.
- **Checkpoint:** the Git tag to check out.

## Chapters

| # | Chapter | Phase | Status |
|---|---|---|---|
| 0 | The idea and the blueprint: why most agents fail in production, CraftRail, and the amended plan | Before P0 | to be written after owner approval |
| 1 | Foundation and walking skeleton | P0 | planned |
| 2 | Contracts, ledger and durable human approval | P1 | planned |
| 3 | Exactly-once execution | P2 | planned |
| 4 | Ground-truth verification and the browser tier | P3 | planned |
| 5 | Reports and memory | P4 | planned |
| 6 | Real integrations: Gmail, Calendar, Keep | P5 | planned |
| 7 | Production hardening | P6 | planned |
| 8 | Cloud deployment and release | P7 | planned |

## Engineering reference

The journal tells the story. The canonical records live here:

- [Product brief](../project/product-brief.md) and [requirements](../project/requirements/functional-requirements.md)
- [Architecture](../project/architecture/overview.md) and [decisions](../project/decisions/README.md)
- [Implementation plan](../project/implementation-plan.md)
- [Documentation strategy](../project/documentation-strategy.md)
- Original vision: [ATEP blueprint](../project/vision/atep-blueprint.md)
