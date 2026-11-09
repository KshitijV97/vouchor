# Requirements writing guide

A requirement is a durable statement of an outcome or boundary that a team needs to build, review, or verify. Writing requirements is valuable when it removes ambiguity or preserves intent across time and contributors. It is counterproductive when a project creates many records that no one uses. Start with the smallest set that makes a change reviewable.

## Write from evidence to outcome

For each proposed requirement, record where it came from: user research, an incident, a policy, an external contract, a product decision, or an explicit assumption. Separate three things that are often confused:

1. **Evidence:** what was observed or requested.
2. **Requirement:** what outcome or constraint the project decides must hold.
3. **Implementation:** one way the system could satisfy that requirement.

For example, “users currently wait up to a minute for an export” is evidence. “The export MUST be available within 10 seconds for the agreed dataset size at the 95th percentile” is a measurable requirement if the team has approved that target. “Use Redis” is an implementation choice unless there is an approved constraint that specifically requires Redis.

## Make a requirement atomic and observable

One requirement should express one obligation when practical. A reviewer should be able to say whether the behavior or quality is satisfied without inferring what the writer intended. Include the actor, condition, trigger, outcome, and boundary that matter. Avoid combining unrelated requirements with “and”, “or”, or a long list of behaviors.

Weak:

> The system should be fast, reliable, and easy to use.

Better, once product and operational owners set actual targets:

> `NFR-031`: The report endpoint MUST return a response within **[approved latency target]** at the **[approved percentile]** for **[workload and dataset]**, measured by **[test method]**.

The bracketed values must be resolved before approval. This example does not invent a service target. “Easy to use” may be assessed by user research rather than a single threshold; identify the research method, participant group, and decision owner rather than pretending it is a unit-test assertion.

## Distinguish requirements from preferences

If the statement changes what users or systems can observe, it may be functional. If it states a quality level or operating limit, it may be non-functional. If it is an organizational rule, it may be a business requirement. If it rules out otherwise viable approaches, it may be a constraint. If it is uncertain, keep it as an assumption or open question.

These categories help find the right reviewers and evidence. They do not determine implementation. Avoid turning a common technical preference into a mandatory system property without recording why it constrains the solution.

## Identify a source and rationale

An ID alone does not explain why a requirement exists. Keep a short rationale or source link for requirements that could be challenged or interpreted in more than one way. Cite stable paths, issue identifiers, policy sections, or a dated decision. If a requirement is based on an assumption, name the owner who can validate it and when it should be revisited.

## Write acceptance criteria as examples of behavior

Acceptance criteria make a requirement concrete in a scenario. Given/When/Then is a useful structure when the starting state, action, and result need to be separated:

```text
AC-012: Given a syntactically valid recovery address,
        when the request is submitted,
        then the user sees a neutral confirmation.
```

Add scenarios for materially different outcomes: permissions, invalid input, unavailable dependencies, retries, duplicate requests, empty data, boundaries, and accessibility. Do not restate the same condition in many criteria; link criteria to the requirement they clarify. Avoid writing criteria in terms of an internal method name unless the method itself is part of a supported contract.

## Include non-functional constraints in measurable form

Quality words are useful categories, not sufficient requirements. For each relevant quality, decide whether it applies, how it will be evaluated, and what level is acceptable. Examples:

- **Performance:** name operation, workload, dataset, percentile/threshold, and environment.
- **Reliability:** identify service objective, failure mode, recovery expectation, and observation window.
- **Security:** name asset, threat or control objective, scope, and verification method; link to the threat model.
- **Privacy:** identify data, purpose, retention or deletion behavior, and responsible policy owner.
- **Accessibility:** name the applicable standard or user task and the test/review evidence expected.
- **Maintainability:** describe the architectural property, boundary, or review practice that can be observed.

Do not add every quality category to every feature. A feature spec should explain why an area is out of scope when omission would otherwise be surprising or risky.

## Avoid these traps

| Trap | Why it causes trouble | Better approach |
|---|---|---|
| “The system is intuitive” | No user, task, or evaluation method is defined. | Define the target task and an agreed usability evaluation or describe the design goal as non-normative context. |
| “Use PostgreSQL” in a functional requirement | Couples a desired behavior to an implementation. | State the data behavior in FR/NFR; put a justified technology choice in the plan or ADR. |
| “Support all users” | An unbounded scope hides tradeoffs. | Identify user groups, accessibility needs, platforms, and explicit exclusions. |
| Requirements split into many vague statements | More IDs do not create more clarity. | Combine tightly related conditions into a precise requirement with separate acceptance scenarios. |
| Passing test equals requirement correctness | A test can encode the wrong behavior. | Review the requirement's source and acceptance criteria as well as test results. |

## Maintain IDs without turning the register into a database

Use IDs for stable references in specs, ADRs, code review, tests, or verification matrices. Keep them stable after approval. Retire an ID with an explicit status instead of recycling it. The validator catches selected formatting and duplicate declarations but does not check semantic uniqueness across every file. If global traceability is essential, establish a canonical register and expand automation in a documented way.

## Review checklist

Before approving a requirement, ask:

- Can two engineers interpret it differently in a way that changes the result?
- Is the obligation about an outcome rather than an unapproved implementation preference?
- Is its source or rationale clear enough for future reviewers?
- Can the team decide what evidence would demonstrate it?
- Are affected actors, failure paths, data lifecycle, permissions, and constraints considered?
- Is the requirement genuinely needed as a stable record, or is it explanatory prose?
- Does it conflict with another requirement, business rule, contract, or accepted ADR?

Use the [feature specification guide](feature-specification-guide.md) to place these records in context and the [traceability guide](traceability-and-verification.md) to connect them to evidence.
