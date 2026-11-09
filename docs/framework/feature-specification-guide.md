# Feature specification guide

The feature specification is the approved description of the problem, scope, required outcomes, and acceptance criteria for one coherent change. It should let a developer understand what success means before selecting how to implement it. The specification is deliberately independent of the coding agent and the implementation language.

## When to create a feature spec

Create one when a change introduces or alters user-visible behavior, business rules, data lifecycle, authorization, external contracts, system quality, or a decision that needs durable traceability. For a no-behavior refactor or a typo fix, a feature spec is usually unnecessary; reference the existing requirement and explain how behavior is preserved.

One folder should represent one reviewable outcome. Split independent outcomes if they can be prioritized, rolled out, or verified separately. Keep tightly coupled changes together when splitting would obscure a shared contract or make tests misleading.

## Metadata and status

Use the numbered directory created by `scripts/new_feature.py`. Preserve the ID when a title changes. Record owner, created/updated dates, and issue/PR links when known. A status describes the document's lifecycle; the responsible project process determines who can approve it. In particular, `draft` and `proposed` do not authorize implementation.

## Section-by-section guidance

| Section | Include | Why it matters | Omit or shorten when |
|---|---|---|---|
| Context/problem | Current behavior, affected user, evidence, impact | Prevents a feature title from standing in for a problem statement. | The context is already explicit in a linked canonical issue; still summarize the key fact. |
| Goals/outcomes | User/business outcome and measurable signal | Lets review assess whether the proposed scope is useful. | The change is a maintenance task with no product outcome. |
| Actors/scenarios | Roles, systems, and relevant use cases | Exposes permissions, handoffs, and alternate paths. | There is only one simple actor and the requirements already make it clear. |
| Scope/non-goals | Included behavior and explicit exclusions | Protects against accidental scope growth. | A trivial change has an unambiguous one-line boundary. |
| Requirements | Stable, atomic obligations and applicable constraints | Creates durable language for plan, code review, and verification. | Existing requirements fully cover the change; link and state that coverage. |
| Business rules | Policies, eligibility, limits, and ownership | Keeps business decisions out of code and agent inference. | None apply; say “none identified” only if it helps reviewers. |
| Acceptance criteria | Observable results for important scenarios | Provides the feature-level completion contract. | A pure refactor can instead cite existing tests and requirements. |
| Edge/failure cases | Invalid input, dependency errors, retries, duplicate actions, abuse | Makes negative behavior intentional instead of accidental. | The case is not plausible or is covered by a linked platform contract. |
| Data/dependencies/interfaces | Data fields, sources, retention, external systems, contract changes | Exposes migration, compatibility, privacy, and delivery work. | No data/interface change; a concise statement is enough. |
| Security/privacy/accessibility/observability | Impact and expected review or evidence | Ensures non-functional concerns are considered early. | Not applicable with a short reason if the feature could reasonably raise the concern. |
| Assumptions/questions/risks | Unverified facts, unresolved decisions, failure impact | Prevents an agent from silently choosing a product policy. | None remain; remove the empty section rather than keeping filler. |
| Traceability | Related requirements, ADRs, architecture, and tests | Helps someone follow intent in both directions. | References are already unambiguous in a small local spec. |

The template is a menu, not a form that must be filled mechanically. Delete irrelevant sections when they create noise; retain a reason where reviewers might otherwise infer that an important risk was overlooked.

## Example of scope boundaries

For an account recovery request, “send a recovery link” may conceal multiple policies: how the user is identified, whether account existence is disclosed, how tokens expire, how abuse is limited, and what happens after delivery failure. A useful spec can define the user-facing behavior while explicitly excluding token creation if that policy is owned by a separate identity design. It should then link that design and make the dependency visible. It should not present a neutral confirmation alone as a complete or safe recovery feature.

The repository's `000-example-feature` demonstrates this bounded approach and calls out what it does not define. It is illustrative, not production security advice.

## Review before approval

Review for a clear problem, bounded outcome, observable acceptance, requirement sources, error paths, permissions, data, compatibility, and cross-document conflicts. Resolve questions that change implementation or risk. A reviewer should be able to explain what is deliberately excluded. Then record approval using the adopting project's own decision method and update the spec's status and owner metadata.

After approval, a code implementation may reveal that the spec is wrong. That is a reason to change control the spec, not a reason to quietly adapt the spec to the code. See [change control](change-control.md) and the [feature lifecycle](workflow.md).
