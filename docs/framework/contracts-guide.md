# API and data contracts

A contract defines what one system or component can rely on at a boundary. It is more precise than explanatory prose and can be validated or consumed by tools. Keep the contract machine-readable where that benefits implementers and consumers, and document policy and rationale around it.

## Pick a format that fits the boundary

| Boundary | Useful format | Why / limits |
|---|---|---|
| HTTP API | OpenAPI | Describes operations, parameters, payloads, responses, and reusable schemas. It is not a requirement to use REST or HTTP. |
| JSON object or event payload | JSON Schema | Captures shape and validation rules for JSON. Syntax-valid JSON is not automatically a valid schema. |
| Asynchronous event or message | Schema plus a short event-contract document | State producer, consumer, ordering, delivery, idempotency, compatibility, and error behavior. Format depends on the messaging system. |
| Binary, database, or non-JSON protocol | Native schema and versioned docs | Use the ecosystem's authoritative format; avoid translating into JSON solely to satisfy this starter. |

Keep one canonical contract per boundary. If a generated client or documentation page is checked in, identify it as generated and define how it is refreshed. Do not manually edit generated output as the source of truth.

## What a useful contract records

Include ownership, versioning/compatibility policy, examples, errors, authentication and authorization expectations, data classification, deprecation approach, and consumer responsibilities where they matter. Specify optional versus required fields, nullability, defaults, ordering, units, timestamps/time zones, limits, and unknown-field behavior. These small choices cause substantial consumer breakage if left implicit.

For an API change, identify additive and breaking effects, old-client behavior, rollout order, migration/rollback options, and the versioning policy. Do not assume that a new optional field is harmless: strict clients may reject it. Do not assume a renamed optional field is additive: consumers may rely on its existing value.

## Examples and errors

Examples should be valid against the contract and should reflect realistic values without including secrets or personal data. Document error shapes, stable error identifiers, retryability, and whether an operation is idempotent. State which layer owns input validation and what happens when the downstream dependency times out.

## Validation limits in this repository

The starter contains an illustrative OpenAPI 3.1 document and JSON Schema example. The standard validator parses `.json` files but does not validate them against a JSON Schema meta-schema. The core `validate_docs.py` script does not parse YAML, so it reports that limitation. The repository's pinned pre-commit `check-yaml` hook parses YAML syntax, including the OpenAPI file, in local hooks and CI; it does not validate the OpenAPI schema, referenced operations, or contract behavior. Teams that need semantic contract validation should add an OpenAPI-aware checker, pin its version, and keep the canonical contract readable and portable.
