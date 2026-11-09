# Architecture documentation guide

Architecture documentation explains the parts of a system, their responsibilities, and the boundaries that shape change. Its purpose is to help a developer make a change without accidentally violating an important dependency, security boundary, data ownership rule, or operational assumption. It should not reproduce every class or line of code.

## Start with the change question

Before drawing, state what a reader should learn. Examples: “Which external systems can access this data?”, “Which service owns this record?”, or “What happens if the payment provider times out?” Choose a view that answers that question. A diagram with no question tends to collect components without clarifying a decision.

Every view should record:

- **Scope:** the system or feature being described.
- **Abstraction:** context, container, component, sequence, data flow, state, or deployment.
- **Last reviewed:** a date or revision that signals when someone checked the diagram against reality.
- **Explanation:** the important relationship, boundary, or omission that the picture alone may not show.

## Use layered views, not one all-purpose map

| View | Contents | Use it when | Keep it focused by |
|---|---|---|---|
| System context | Users, external systems, and the system boundary | Explaining product boundary and external dependencies | Show only actors and systems relevant to the audience. |
| Container | Independently running/deployable units and data stores | Discussing runtime topology, ownership, deployment, or integration | Label responsibilities and communication, not every technology detail. |
| Component | Important modules inside a container | Changes cross internal boundaries or responsibilities are unclear | Show only components relevant to a change or architectural constraint. |
| Sequence | Time-ordered messages in one scenario | Reviewing protocol behavior, failures, retries, or ordering | Include the failure path if it changes system behavior. |
| Data flow | Where data originates, transforms, crosses trust boundaries, and is stored | Reviewing privacy, retention, access, or pipeline behavior | Name sensitive data and identify its owner and destination. |
| State | States and allowed transitions | Lifecycle rules, workflows, status machines, or edge cases matter | Define event/guard conditions and invalid transitions. |
| Deployment | Infrastructure, regions, networks, and runtime placement | Availability, compliance, latency, or operations depend on location | Keep ephemeral deployment detail elsewhere if it changes frequently. |

C4 names are useful for context, container, and component levels, but are not a mandatory notation. The useful property is the explicit abstraction level. Do not draw all seven views just because they exist in this guide.

## Keep the diagram aligned with the architecture

Use the same names for services, actors, and stores across the overview, contracts, code, and other diagrams. When a name changes, update links and views together. An accepted ADR explains why a boundary exists; the view explains where it is. The code still defines what currently runs, so diagrams should be reviewed during substantial changes and marked with their last-reviewed date.

Avoid detail that changes more frequently than the diagram can be maintained. A component view is not a substitute for source navigation. Generated diagrams may help for large systems, but retain the generator input and explain what is authoritative. Reviewers should be able to edit the source, not only view a screenshot.

## Document security and trust boundaries

Mark where untrusted input enters, where identity/authorization is enforced, where sensitive data crosses a component or network boundary, and which component owns retention/deletion. A boundary line by itself is not a security control. Pair it with a control statement, owner, threat or risk, and verification evidence. Keep threat-model detail in the project's selected security record and link to it.

## Keep docs proportional and useful

New projects can start with a context view and one feature-specific sequence or data-flow diagram. Add more views only when a design review, operational need, or recurring source of confusion justifies them. In an existing project, link to a current architecture source rather than importing stale diagrams. The repository's starter Mermaid views are in `docs/project/architecture/` for adopters to copy or replace.
