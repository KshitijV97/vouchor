# Traceability and verification

Traceability links intent to evidence so a reviewer can answer two questions: “What approved outcome does this code implement?” and “What evidence shows that outcome works?” CraftRail uses the path **Requirement → Acceptance criterion → Verification ID/method → evidence/location → status**. Use the path when it adds confidence; do not turn it into line-by-line paperwork.

## Define verification before implementation

While specifying, identify what would demonstrate each criterion. This can shape a better requirement: if no one can imagine how to evaluate it, the requirement may be too vague or may need a qualitative review method. The implementation plan should carry those checks into tests, review, accessibility evaluation, or operations.

| Requirement | Acceptance criterion | Verification ID and method | Evidence or location | Status |
|---|---|---|---|---|
| FR-022 | AC-012 | TEST-041: integration test compares matching and non-matching account responses | `tests/recovery/test_response.py`, command `pytest tests/recovery -q`, commit/build reference | verified |
| NFR-009 | AC-013 | TEST-042: performance run at defined workload | Benchmark report path, run date, environment | planned |
| CON-003 | AC-014 | TEST-043: release review confirms approved delivery service | Review record and contract reference | implemented |

This table is illustrative; the exact commands and evidence above do not assert tests exist in this repository. Put the actual project evidence in the feature's `verification.md`.

## Pick evidence that answers the criterion

- **Unit tests** show a local transformation or rule under controlled inputs.
- **Integration tests** show interactions across a defined boundary.
- **End-to-end tests** show a user journey through running components, with higher setup cost and more environmental variability.
- **Manual checks** are appropriate for exploratory behavior or a human-visible quality that automation does not measure well. Record steps and observations so the check can be repeated.
- **Review evidence** can establish architectural, accessibility, security, privacy, or content properties when the review method and accountable reviewer are stated.
- **Operational evidence** can establish rollout, monitoring, recovery, or service-level behavior that cannot be proven in a unit test.

The chosen method should be proportionate to risk. A screenshot can support evidence for layout, but should not be the only evidence for a state transition. A passing test can show implementation behavior but cannot prove the requirement itself is correct or complete.

## Status definitions

| Status | Meaning | Do not use it to mean |
|---|---|---|
| `planned` | The check is defined but not yet run. | The implementation is likely correct. |
| `implemented` | Code or a verification procedure exists but the result has not been confirmed. | The criterion passed. |
| `verified` | Evidence was reviewed and the criterion passed for the recorded context. | All nearby requirements or untested environments passed. |
| `blocked` | A named dependency prevents the check. Record what and who can unblock it. | The criterion is waived. |
| `waived` | An accountable human accepted the uncovered risk with rationale and scope. | The requirement was satisfied. |
| `deprecated` | The criterion no longer applies because approved intent changed. Link the replacement or decision. | It can be silently deleted. |

Record owner, environment, build/commit, date, and evidence path where those details affect repeatability. If a check only covers one platform or dataset, make the limit explicit.

## Measure coverage without inventing precision

A useful feature review asks whether each in-scope requirement has an acceptance criterion, planned implementation, and appropriate verification. The validator cannot calculate semantic coverage. A dashboard percentage can create false confidence if the linked test does not actually prove the behavior. Start with a readable matrix and automate only stable relationships that the project can validate accurately.

Some requirements need several criteria and checks; several requirements may share one system-level test. Use links and explicit notes rather than forcing one-to-one relationships. Criteria should remain observable, and test names should explain behavior rather than mirror requirement text mechanically.

## Waivers and deferred requirements

For a waiver, record the accountable human, rationale, accepted risk, affected users/systems, compensating control, and review or expiration date when appropriate. For a deferral, keep the requirement ID, status, owner, reason, and trigger/date for revisiting. These states preserve honesty about what the release does and does not demonstrate.

The illustrative [worked example](../examples/sample-feature-walkthrough.md) connects its requirements and acceptance criteria to tests while making clear that the listed evidence was not generated by a running application.
