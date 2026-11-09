# CraftRail Studio: handoff package

A complete CraftRail feature package for **CraftRail Studio**: a Git-native, static, optional dashboard and editor for CraftRail repositories. It gives Jira/Trello-style boards and metrics plus traceability, with $0 hosting and no AI calls.

This package was drafted in the Vouchor repository. It is meant to be implemented in the **CraftRail repository** (`https://github.com/KshitijV97/craft-rail`), not in Vouchor.

| File | Purpose |
|---|---|
| [ADR-001-craftrail-studio-git-native-static-studio.md](ADR-001-craftrail-studio-git-native-static-studio.md) | The architecture decision and rejected alternatives |
| [spec.md](spec.md) | Requirements (`FR`/`NFR`/`BR`/`CON`), acceptance criteria, conventions, metrics definitions, algorithms |
| [plan.md](plan.md) | Components, file layout, stack, APIs, security, rollout milestones, test strategy |
| [tasks.md](tasks.md) | 35 dependency-ordered tasks, each one pull request |
| [verification.md](verification.md) | Requirement → AC → TEST matrix (all `planned`) |
| [contracts/craftrail-graph.schema.json](contracts/craftrail-graph.schema.json) | JSON Schema for `craftrail.json` (exporter output, Studio input) |
| [contracts/craftrail-frontmatter.schema.json](contracts/craftrail-frontmatter.schema.json) | JSON Schema for per-file front-matter |

Status: **proposed**. Both JSON Schemas were checked as valid Draft 2020-12 schemas, with one valid and one invalid sample document each. Nothing else has been implemented or tested.

## Before handing to Codex

1. Read the ADR and spec. Answer the three open questions in `spec.md` → "Assumptions, questions, and risks":
   - where CraftRail keeps its own ADRs;
   - where `contracts/` lives;
   - whether the prebuilt Studio app ships as a release asset.
2. In the CraftRail repository, run `python3 scripts/new_feature.py "CraftRail Studio"` to get the next feature folder. Then replace its four files with `spec.md`, `plan.md`, `tasks.md` and `verification.md` from here, replacing `NNN` with the new number.
3. Copy the ADR to the agreed decisions folder (renumber it) and the schemas to the agreed contracts folder. Fix relative links.
4. Set the spec's `Status` to `approved` yourself. Codex must not approve it.

## Prompt for Codex

Codex reads `AGENTS.md` automatically. Paste this as your first message, replacing `NNN`:

```text
Implement CraftRail Studio from specs/NNN-craftrail-studio/ following AGENTS.md and the CraftRail workflow.

Read first, in order: specs/NNN-craftrail-studio/spec.md, plan.md, tasks.md, verification.md,
the Studio ADR, both JSON Schemas, then docs/framework/concepts.md,
docs/framework/traceability-and-verification.md and docs/framework/workflow-prompts.md.
Do not load other docs unless a task needs them.

Rules:
- The spec status must be "approved" before you write code. If it is not, stop and tell me.
- Work through tasks.md in order, one task per pull request (or one commit if I say so).
  Start with TASK-001 and stop after each milestone (M1..M6 in plan.md) for my review.
- Core Python tools (scripts/, scripts/craftrail_core/) must use only the standard library and
  run on every Python version the repo supports. Node tooling stays inside studio/.
- Never change an approved requirement, acceptance criterion or ADR to fit the code. If something
  is ambiguous, contradictory or infeasible, stop and ask, quoting the spec section.
- For every task: write tests first from the linked acceptance criteria, implement, then run
  `pre-commit run --all-files`, the relevant unittest/Vitest/Playwright commands, and
  `python3 scripts/validate_docs.py`. Report exact commands and results. Do not claim unrun checks passed.
- Update verification.md rows for the task's ACs with command, environment, commit and result.
  Mark a row "verified" only when the evidence shows it passed.
- Keep diffs minimal. No new dependencies beyond plan.md without asking. Pin everything.
- Never mark a feature "approved" or an ADR "accepted"; that is my decision.

Begin with TASK-001: list the open questions you need me to answer, then propose the exact file moves.
```

## What "done" looks like

All 31 acceptance criteria have `verified` rows in `verification.md` with evidence. The CI jobs `core-graph`, `studio`, `studio-e2e` and `benchmark` are green. `docs/framework/studio.md` is published on the CraftRail docs site. A release attaches `craftrail-studio-<version>.zip`.
