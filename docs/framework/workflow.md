# Feature lifecycle

CraftRail uses nine named phases: **Discover → Specify → Clarify → Plan → Tasks → Analyze → Implement → Verify → Converge**. They describe the reasoning needed for a change, not nine separate meetings or a waterfall schedule. A small, reversible copy edit can combine several phases. A change that affects identity, money, permissions, persistent data, external contracts, or service reliability usually benefits from more explicit gates.

The lifecycle exists to prevent a common failure: implementation begins while the team still has different ideas about the problem. That failure is expensive because code makes one interpretation concrete and later reviews then debate the implementation instead of clarifying intent. The artifacts provide handoffs between phases. They are intentionally small enough to revise as evidence changes.

## At a glance

| Phase | Input | Work | Output and exit condition |
|---|---|---|---|
| Discover | User report, outcome, or change request | Inspect relevant code and documentation; identify actors, current behavior, evidence, constraints, and unknowns. | A problem statement grounded in sources; material unknowns are visible. |
| Specify | Discovery notes | Define goals, non-goals, requirements, rules, scenarios, and observable acceptance criteria. | A draft feature spec with stable IDs and scope boundaries. |
| Clarify | Draft spec | Find ambiguous language, conflicting requirements, edge cases, assumptions, and missing decisions. | Material issues are resolved, explicitly accepted, or assigned an owner; the decision owner approves intent. |
| Plan | Approved spec, architecture, accepted ADRs | Choose an implementation approach and examine interfaces, data, security, operations, rollout, and tests. | A reviewable plan within approved scope, with alternatives and open decisions. |
| Tasks | Reviewed plan | Break work into ordered slices with outputs and verification. | Each task can be implemented and reviewed without hiding dependencies. |
| Analyze | Spec, plan, tasks, contracts, architecture | Cross-check consistency and traceability before code changes. | Conflicts are repaired at their source; remaining risks are visible to reviewers. |
| Implement | Approved work and relevant tasks | Make incremental code and test changes; stop at requirement or scope conflicts. | Changes and tests correspond to approved tasks. |
| Verify | Acceptance criteria and changed implementation | Run automated, manual, review, and operational checks as appropriate. | Evidence is recorded per criterion; unverified work is not described as complete. |
| Converge | Reviewed implementation and verification evidence | Compare code with approved artifacts; document approved changes, deviations, and deferred work. | Canonical docs describe the current approved system and unresolved work remains explicit. |

## Phase details

### 1. Discover: learn what is true before writing what should change

Start with the user problem or desired outcome, then inspect only the relevant repository paths. Record current behavior separately from desired behavior. Use issue reports, support cases, logs, existing requirements, tests, API contracts, and code as evidence where available. Code is evidence about current implementation; it is not automatically authority for intended behavior.

Identify affected actors, systems, constraints, and stakeholders. Mark inference as inference. Do not fill gaps with product assumptions just because a coding agent can produce a plausible answer. Discovery is complete when another engineer can state the observed problem and distinguish known facts from open questions.

### 2. Specify: make intent testable

Create a feature spec from `templates/feature/spec.md`. State why the change matters, what outcome is expected, and what will remain out of scope. Add atomic requirements only when a stable reference will help review or traceability. Give each requirement a durable ID. Write acceptance criteria as observable outcomes; use Given/When/Then when it clarifies context, trigger, and result.

Specify failure paths and constraints when they affect outcomes. A requirement like “the system should be fast” does not tell an implementer or reviewer what to build. A useful performance requirement identifies the operation, workload, percentile or measurement, threshold, and evaluation environment. If a qualitative review is the appropriate method, say who reviews what and against which standard.

### 3. Clarify: resolve the questions that change implementation

Review the spec for ambiguous nouns, undefined states, conflicts, missing negative paths, data lifecycle, abuse cases, authorization, compatibility, accessibility, and operational expectations. Not every theoretical edge case deserves a question. Ask when different plausible answers would lead to meaningfully different code, risk, or user experience.

For each open question, record the question, the decision owner, and the resolution. If it cannot be resolved before planning, write an explicit assumption with its owner and impact. A human decision owner marks the feature approved according to the adopting team's governance. A file's status field communicates state; it does not grant an agent authority to approve it.

### 4. Plan: choose a design within the approved contract

Use `templates/feature/plan.md`. Explain the selected approach and why it fits the requirements and existing architecture. Identify impacted components, interfaces, data, migrations, security boundaries, errors, retries, idempotency, consistency, observability, rollout, compatibility, rollback, and test strategy where relevant. Link accepted ADRs rather than copying their reasoning.

Consider alternatives in proportion to the decision's impact. The plan is not an excuse to silently add scope. If implementation requires a different product outcome, return to the spec and obtain approval. If the plan discovers a material technical choice that should persist beyond this feature, draft an ADR instead of burying the reasoning in a task list.

### 5. Tasks: make execution reviewable

Use `templates/feature/tasks.md`. Order tasks by dependency and describe the result a reviewer should see. Prefer a vertical slice that exercises a behavior over a checklist of files to edit. Each task references requirement or acceptance IDs and a verification method. Split tasks when they mix unrelated behavior, cannot be reviewed safely, or leave too much unverified work at once.

Tasks are a work queue, not a second feature specification. If a task changes desired behavior, update the spec. If a task depends on an unresolved choice, keep it blocked or add a decision task rather than choosing silently during implementation.

### 6. Analyze: catch mismatches before implementation compounds them

Compare the spec, plan, tasks, contracts, architecture, and relevant ADRs. Ask whether every in-scope requirement has an acceptance criterion, planned work, and a verification path. Ask whether tasks implement only approved scope. Check that contract changes and migration plans match the behavior described. The validator can catch some structure and ID mistakes; this analysis is a human review of meaning.

### 7. Implement: keep code inside the reviewed boundary

Implement a small task or coherent slice at a time. Read the local code and existing tests before editing. Add tests while the behavior is in focus. If code reveals a contradiction, an unsafe assumption, or an unplanned external dependency, pause the affected work and return the question to the spec or plan owner. Do not alter a requirement or accepted ADR just to make the current code look compliant.

### 8. Verify: attach evidence to outcomes

Run the checks that speak to each acceptance criterion. A unit test can establish a local rule; integration tests can establish cross-component behavior; manual and accessibility review can establish interaction quality; operational checks can establish rollout readiness. Record command, environment/build, result, and evidence path where they matter. If verification is blocked or waived, state who accepted the risk and why.

### 9. Converge: make the repository describe the shipped system

Review the diff against the approved spec, plan, tasks, contract, diagrams, and ADRs. Update canonical documents to reflect approved behavior and design. Record implementation deviations, deferred criteria, follow-up tasks, and decision changes. Do not rewrite history to imply the shipped outcome was the original intent. Mark obsolete requirements as deprecated or superseded rather than reusing their IDs.

## Scaling the workflow to the change

| Change profile | Suggested path | Reason |
|---|---|---|
| Typo, comment, or internal refactor with no behavior change | Inspect → implement → relevant checks → converge | A feature spec would add overhead without clarifying intent. Record that behavior is unchanged in review context. |
| Small user-visible behavior with clear existing requirements | Discover → concise spec update → clarify → plan/tasks together → implement → verify → converge | Existing intent reduces discovery; explicit acceptance still protects behavior. |
| New feature, data migration, contract change, auth/security behavior, or uncertain product rule | Full nine-phase path | Scope, compatibility, and failure handling need independent review before implementation. |
| Emergency fix | Reproduce → define minimal safe outcome → implement/test → review → document rationale and follow-up | Speed may justify compressed gates; the record and post-fix verification still matter. |

This is guidance, not a complexity score. Teams should use their own risk and approval policy. When in doubt, make the question visible and take the smallest step that can safely resolve it.

## Approval boundaries

Agents may gather evidence, draft documents, recommend alternatives, implement approved tasks, and report results. Humans retain authority over business intent, material scope changes, exceptions to security/privacy policy, accepted risk, and architecture decisions that the team requires approval for. A label such as `approved` in Markdown records the team's decision; it does not replace the decision process or identify an approver unless the project records that information.

For post-approval change handling, see [change control](change-control.md). For copyable neutral prompts, see [workflow prompts](workflow-prompts.md).
