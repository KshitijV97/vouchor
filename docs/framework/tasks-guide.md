# Planning and task breakdown

A technical plan explains the implementation approach and the important tradeoffs. A task list makes that plan executable and reviewable. They answer different questions: the plan says **how the solution should fit together**; tasks say **what can be completed and verified in sequence**.

## What belongs in a plan

Use the plan template as a coverage prompt. Describe the selected approach and alternatives, affected components, interfaces, data and migration, diagrams, security boundaries, error/retry/idempotency behavior, operations and observability, rollout/rollback, compatibility, tests, and open decisions. Cover the areas that matter to this change. If an area has no impact, a short reason is more useful than copying boilerplate.

The plan should explain consequential choices, not restate the spec. Link to requirement IDs and accepted ADRs. Do not quietly change approved scope. If a new design requires a changed outcome, return to the spec owner. If it creates a lasting architecture choice, use an ADR.

## Make tasks reviewable

Each task should answer:

1. What artifact or behavior will exist when it is done?
2. Which requirement or acceptance criterion does it serve?
3. What must happen first?
4. How will a reviewer verify it?

Prefer vertical slices where practical: a thin end-to-end behavior, tests, and necessary docs can often be reviewed together. Split work where a task has multiple unrelated outcomes, crosses risky boundaries, or cannot be safely reviewed as one change. Avoid file-by-file task plans unless the work is genuinely mechanical.

| Weak task | Why it is weak | Better task |
|---|---|---|
| “Do the API” | No result, contract, scope, or evidence is named. | “Add the recovery request endpoint for AC-012 and test valid/invalid input paths.” |
| “Update files 1–8” | Organizes work by file rather than behavior; review intent is hidden. | Group files by a coherent behavior and name the test or review evidence. |
| “Add lots of tests” | Quantity does not define coverage. | Name the scenarios and requirement IDs that the tests must demonstrate. |
| “Make it secure” | No threat or control is identifiable. | Reference the approved security requirement and the threat-model checks. |

## Dependency ordering and parallel work

Place enabling decisions and contract changes before consumers. Avoid parallel tasks that edit the same artifact or depend on unresolved interfaces. If a team uses parallel contributors, define ownership and an integration point rather than assuming the coding tool will resolve conflicting edits. CraftRail does not prescribe subagents or any specific orchestration feature.

## Track progress honestly

Use `planned` for work not started, `in-progress` when work is under way, `blocked` when a named dependency prevents progress, and the project's chosen terminal status after review. If the project uses a separate issue tracker as its task system, keep only a stable link and the traceability information needed in the spec; do not duplicate a complete task database.

## Analyze the task set

Before implementation, check that every in-scope requirement has work and verification, no task introduces unapproved behavior, dependencies are ordered, and the plan's rollout and migration needs are represented. Update the task breakdown when the plan changes; preserve evidence about why the plan changed.

The [workflow](workflow.md) describes when planning and task creation can be combined. Use the [verification guide](traceability-and-verification.md) to decide what evidence each task should produce.
