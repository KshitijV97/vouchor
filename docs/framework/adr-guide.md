# Architecture decision records

An architecture decision record (ADR) captures why a consequential technical choice was made. It helps a later developer understand the forces, rejected options, and costs without reconstructing a decision from chat history or code archaeology.

## When to write an ADR

Write one when a choice has material effects on boundaries, data ownership, security posture, extensibility, operational cost, compatibility, or the ability to change course. Do not create an ADR for every library or local implementation detail. A useful test is: “Would a future engineer reasonably need to know why this path was chosen, or what alternative was deliberately rejected?” If the answer is no, a plan note or code comment may be sufficient.

## Keep the ADR about one decision

Use one record for one coherent decision. Record an ID/title, status, date, decision owner, context and forces, decision, alternatives, positive and negative consequences, and links to related requirements, diagrams, code, or ADRs. State the decision at a level future changes can use. Avoid describing a sequence of coding steps.

### Context and forces

Describe the problem, constraints, quality attributes, existing architecture, and relevant requirements. Separate fixed constraints from preferences. Include the evidence or assumptions that shaped the choice.

### Decision

State what is chosen and the principal reason. Be specific about the boundary of the decision: an ADR about event delivery should make clear whether it chooses a broker, an event contract, a delivery guarantee, or all three.

### Alternatives

Include plausible options that were seriously considered. Explain why they were not selected in this context. Do not pad the record with implausible alternatives or imply no tradeoff exists.

### Consequences

Name both benefits and costs. Include migration, reliability, security, maintenance, staffing, observability, and exit costs where relevant. Consequences make it possible to revisit the decision when conditions change.

## Status lifecycle

Use `proposed` while review is open, `accepted` when the authorized owner approves it, `rejected` when it will not be adopted, `deprecated` when it no longer applies, and `superseded` when a later ADR replaces the choice. The project's approval process determines who can change a status. A coding agent can prepare a proposal; it cannot make the organization's decision simply by writing `accepted`.

Accepted ADRs are historical. Correct errors transparently, but do not silently rewrite the decision or its alternatives. When the decision materially changes, create a new ADR, link the previous record, and state what changed in the context.

## Example decision framing

Weak title: “Implement cache”. This describes work but not the choice.

Better title: “Cache catalog reads at the application boundary”. The record can explain expected read load, freshness tolerance, invalidation approach, alternatives such as database tuning or CDN caching, and the consequences of stale data. The implementation details still belong in the plan and code.

Use the repository-root `templates/adr.md` as the starting file. Keep ADRs under `docs/project/decisions/` unless the adopting repository has an established architecture-record location.
