# Concepts and identifiers

CraftRail gives common engineering records names and stable references. The names are a shared vocabulary, not a mandatory enterprise requirements taxonomy. Projects should use the parts that improve review and traceability and omit items that add no value.

## Requirement categories

| Type | Prefix | Question it answers | Example |
|---|---|---|---|
| Business requirement | `BR-` | What business outcome or policy must hold? | `BR-014`: An account recovery request MUST NOT grant access without the established identity check. |
| Functional requirement | `FR-` | What observable behavior must the system provide? | `FR-022`: The system MUST show a neutral confirmation after a valid recovery request. |
| Non-functional requirement | `NFR-` | How well, safely, or under what operating quality must it behave? | `NFR-009`: The recovery endpoint MUST sustain the agreed request rate at the target latency under the recorded test workload. |
| Constraint | `CON-` | What boundary must the solution respect? | `CON-003`: Recovery messages MUST use the approved delivery service. |
| Assumption | Usually prose/table key, not a global prefix | What is being treated as true until someone verifies it? | `ASM-002`: The account email is verified; owner: Identity team; revisit before rollout. |
| User story | `US-` | Which user need is this scenario organized around? | `US-004`: As a locked-out user, I want a recovery path so I can regain access. |
| Acceptance criterion | `AC-` | What outcome lets a reviewer decide the requirement is met? | `AC-012`: Given a valid address, when submitted, then a neutral confirmation appears. |

An assumption is not a requirement. If it later becomes a mandatory rule, promote it into the appropriate requirement category with a new stable ID and source. A constraint differs from a requirement because it restricts the solution space (for example, an approved platform or legal boundary), while a requirement describes a required outcome. Projects may model constraints differently if their governance already defines a consistent taxonomy.

## Normative language

Use **MUST** for mandatory behavior, **SHOULD** for a strong recommendation with an understood exception path, and **MAY** for an optional capability. Use these terms consistently within an adopting project. Avoid mixing casual “should” with normative **SHOULD** in the same requirement register unless the meaning is made explicit.

Normative words are useful when a requirement is reviewed as a contract. They are unnecessary in ordinary explanatory prose. A requirement should say what must be true, not use capital letters to make a vague sentence look testable.

## Acceptance criteria and verification identifiers

Acceptance criteria identify observable feature outcomes. `TEST-` is a verification reference, not a promise that the check is automated; the record may refer to a manual test, a review, or an operational check. `TASK-` is optional because some teams use issue trackers as their task authority. `ADR-` identifies architecture decision records.

Example:

```text
FR-022: The system MUST show a neutral confirmation after a valid recovery request.
AC-012: Given a syntactically valid address, when submitted, then a neutral confirmation appears regardless of account match.
TEST-041: Integration test compares the response for matching and non-matching accounts.
```

The relationship between those records is more useful than adding an ID to every paragraph. Use a stable ID when people need to cite, test, change, or audit the item. Leave explanatory prose unnumbered.

## IDs: stability, scope, and retirement

Use prefixes from this set where applicable: `BR`, `FR`, `NFR`, `CON`, `US`, `AC`, `ADR`, `TASK`, and `TEST`. Follow each with at least three digits, such as `FR-001`. The exact width is a convention, not a numeric limit; numbering beyond 999 should continue naturally.

IDs are anchors, not semantic codes. Do not encode a component name, priority, team, year, or current status into the ID; those properties change and make references brittle. Do not recycle a deleted identifier. Mark an item `deprecated` or `superseded`, explain why, and create a new ID when new intent replaces it.

Choose the smallest useful scope for uniqueness:

- Project requirements are usually unique within the project's requirement register.
- Feature-local acceptance criteria may be unique within one feature folder if every reference includes the feature path or ID.
- ADRs are normally unique across the project because they are cited from many features.
- Task and test IDs can be local to a feature if their scope is consistently apparent.

The current validator catches duplicate declarations within a Markdown document; it is not a project-wide registry and cannot detect every cross-file collision. Teams requiring global uniqueness should define one canonical register or extend validation deliberately.

## Statuses describe state, not authority

Feature statuses used by the validator are `draft`, `proposed`, `approved`, `in-progress`, `verified`, `deferred`, and `deprecated`. Verification statuses are `planned`, `implemented`, `verified`, `blocked`, `waived`, and `deprecated`. ADR statuses are `proposed`, `accepted`, `rejected`, `deprecated`, and `superseded`.

Use status to answer “what state is this record in?” Add owner and date metadata where they answer “who is responsible?” and “when was the decision made?” Neither a status nor a checkbox proves review occurred. The project's process defines authorized approvers. Record an accountable person or role when that matters.

## Canonical versus generated information

The project's reviewed Markdown requirements, Mermaid source, ADRs, contracts, and verification evidence are canonical in their chosen repository location. A generated site, rendered diagram, search index, or agent command file is a view or adapter. When a generated page disagrees with its Markdown source, correct the source and rebuild the view; do not edit generated HTML as project policy.

The same principle applies to chat: a conversation can help draft an artifact but is not itself the durable approval record. Move an approved decision into its canonical file and link to evidence that should be retained.
