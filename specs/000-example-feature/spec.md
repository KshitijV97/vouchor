# Feature 000: Account recovery request (illustrative)

- **Status:** verified (illustrative only; not production guidance)
- **Owner:** Example product team
- **Created:** 2026-11-08
- **Updated:** 2026-11-08
- **Related issues/PRs:** none

## Context and problem

A user who cannot sign in needs a safe way to request account recovery. This fictional example records a minimal user-visible outcome, not a complete security design.

## Goals and outcomes

- Give the user a clear confirmation that a request was received without disclosing whether an account exists.

## Actors and scenarios

- `US-001`: As a locked-out user, I want to request a recovery message so I can regain access.

## Scope and non-goals

- In scope: submit an email address and show a neutral confirmation.
- Non-goals: token design, identity proofing, delivery provider, account recovery completion.

## Requirements

- `FR-001`: The system MUST return the same confirmation for syntactically valid submissions whether or not an account matches.
- `NFR-001`: The response SHOULD avoid exposing account existence through response text; timing and abuse controls require separate security review.

## Business rules

- `BR-001`: A recovery request does not itself grant account access.

## Acceptance criteria

- `AC-001`: Given a syntactically valid address, when a request is submitted, then a neutral confirmation is shown regardless of account match.
- `AC-002`: Given a malformed address, when submitted, then validation feedback is shown without creating a request.

## Edge cases and failures

- Temporary service failure produces a retryable generic error.
- Repeated submissions and rate limits require a security design before production use.

## Data, dependencies, and interfaces

No real delivery integration is defined. See the illustrative sequence diagram.

## Security, privacy, accessibility, observability

This sample is intentionally incomplete and must not be copied as a production recovery design. A real design needs threat modeling, rate limits, token expiry, abuse monitoring, privacy review, accessible feedback, and operational controls.

## Assumptions, questions, risks

- Risk: response timing could still reveal account existence; not addressed in this illustrative feature.
- Open: verification and recovery policy must be specified by the adopting project.

## Traceability

`FR-001` → `AC-001` → `TEST-001`; `FR-001` → `AC-002` → `TEST-002`.
