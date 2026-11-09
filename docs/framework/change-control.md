# Change control

Approved artifacts are a record of intent. When implementation or new evidence changes that intent, preserve the history and make the new decision explicit. Change control prevents code from becoming the accidental authority simply because it already exists.

## Change after approval

1. Pause work that depends on the affected requirement or decision.
2. Describe what new evidence or constraint requires a change.
3. Propose exact spec/plan/contract edits and explain scope, user, compatibility, risk, test, and rollout impact.
4. Obtain approval from the role defined by the project.
5. Update the canonical artifacts and linked tasks before continuing.

Small clarifications that do not alter behavior may be recorded directly with a review note. If the meaning or outcome changes, treat it as a requirement change. An agent may draft the change but must not approve its own interpretation.

## Requirement supersession

Do not recycle IDs or rewrite an accepted requirement to erase a previous commitment. Mark the old record as deprecated or superseded, explain the reason, identify the replacement if one exists, and create new IDs for new obligations. Keep consumers and tests that still depend on the old behavior in the impact analysis.

## Architecture changes

If the implementation approach changes but approved behavior does not, update the plan and tasks and record the review. If an accepted architectural decision materially changes, create a new ADR that supersedes the old one. Do not edit the old ADR's decision section as though the original choice never happened.

## Implementation deviations

Sometimes a release cannot satisfy an approved criterion. Record the deviation, unmet criterion, reason, impact, mitigations, owner who accepted the risk, and a follow-up task/date. Mark verification `blocked` or `waived` as appropriate. Do not call an unchecked or waived criterion verified.

## Deferred or deprecated behavior

When a requirement is deferred, preserve its ID and state who will decide when to revisit it. When behavior is deprecated, explain the replacement path, compatibility period, and removal criteria. This avoids making users infer whether an absent feature was omitted deliberately or forgotten.

## Emergency fixes

An urgent repair can use a short path to reduce immediate harm: reproduce the failure, state the smallest safe correction, implement with a focused regression check, and obtain the review your incident policy requires. Afterward, converge the specification, rationale, and verification evidence. Record remaining risks and a follow-up owner. An emergency is a reason to compress process, not to discard the record.
