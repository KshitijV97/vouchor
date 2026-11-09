# Agent-neutral workflow prompts

Paste these as ordinary instructions in any coding-agent chat. Replace bracketed context. Review proposed artifacts before approval. No slash command, skill, hook, subagent, MCP server, or vendor API is required.

## Establish project context

Read the relevant existing repository docs. Draft or revise the project brief, engineering principles, stakeholder notes, glossary, requirements, and architecture pointers from verified facts. Separate known facts from assumptions and questions. Do not invent policy. Propose the smallest useful set of files and identify human decisions needed.

## Discover and clarify a feature

Inspect relevant code and docs, then summarize current behavior, users, problem, constraints, risks, and unknowns for [feature]. Cite repository paths. Ask only material questions that cannot be resolved from evidence. Do not change code.

## Draft or revise a specification

Using the feature template, write scope, goals, non-goals, atomic requirements with stable IDs, business rules, scenarios, acceptance criteria, edge/failure cases, data/security/accessibility concerns, assumptions, and risks. Distinguish evidence from inference. Leave unresolved questions visible and mark status `draft`.

## Review a specification

Review [spec path] for ambiguity, contradictions, missing actors/edge cases, testability, scope creep, and traceability gaps. Report findings with section references and proposed wording. Do not silently rewrite the spec or approve it.

## Produce a technical plan

Read the approved spec and relevant architecture/ADRs. Propose components, interfaces, data changes, diagrams, trust boundaries, errors/retries/idempotency, operations, rollout/rollback, compatibility, tests, alternatives, and open decisions as applicable. Identify scope changes instead of assuming approval.

## Decompose into tasks

Turn the reviewed plan into dependency-ordered, reviewable slices. Each task must reference requirements or criteria and state expected output and verification. Prefer vertical slices; do not create arbitrary task counts.

## Implement approved work

Implement only approved tasks [IDs] within [spec path]. Read relevant code and instructions first. Make small changes, add/update tests, and stop to surface any requirement conflict or scope change. Do not change accepted requirements or ADRs to fit code.

## Verify against acceptance criteria

For every criterion in [spec path], run the relevant checks and record exact commands, outcomes, evidence locations, and status in the verification matrix. Include manual/review checks where needed. Mark gaps blocked or unverified; do not infer success from generated code.

## Converge documentation

Compare shipped behavior with approved spec, plan, tasks, contracts, diagrams, and ADRs. Update documents only to reflect approved changes. Record deviations, deferred work, evidence, and decisions needing review. Preserve historical reasoning.

## Assess a bug or change

Reproduce or inspect [issue] and trace affected requirements, contracts, architecture, and tests. Describe impact, whether existing approved intent covers it, and a minimal proposed change. Do not bypass a requirement; propose a spec/decision update if intent must change.
