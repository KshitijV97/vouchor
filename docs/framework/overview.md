# CraftRail overview and architecture

CraftRail is a repository-native framework for keeping engineering intent connected to architecture, implementation, and verification. It provides conventions, templates, examples, agent instructions, and small offline checks. A project adopts it by committing ordinary files in the same Git history as its code.

> **The framework owns the engineering process. The coding agent is replaceable.**

This principle is structural. A provider can change its instruction discovery, available models, and product features without changing the project's requirements, decisions, contracts, or verification records.

## The three layers

### Core: define the project that must be built

Core consists of project brief, business and system requirements, architecture, contracts, ADRs, feature specs, acceptance criteria, and verification evidence. These artifacts state intent and system properties. The formats are Markdown for explanatory prose and tables, Mermaid for diagram source, YAML for OpenAPI and GitHub forms, and JSON for machine-readable structured examples. These formats are readable in a code editor and reviewable as normal diffs; no account or proprietary service is required to understand them.

The Core does not depend on a model provider. `scripts/validate_docs.py` uses Python's standard library to check selected structure and syntax. It intentionally cannot decide whether requirements are correct, whether an architecture is sound, or whether an agent obeyed the specification.

### Workflow: define how intent becomes verified change

The lifecycle is Discover → Specify → Clarify → Plan → Tasks → Analyze → Implement → Verify → Converge. The workflow is separate from the agent because the quality gates matter regardless of who performs them. A human, an agent, or a mixed team can produce and review the same artifacts.

Workflow prompts are copyable natural-language instructions. They are not slash commands and do not require skills, hooks, subagents, MCP integrations, or an orchestration runtime. Their separation lets a team change its process without migrating requirements, and lets agents change without rewriting process instructions.

### Adapters: map a tool to shared context

The root `AGENTS.md` is the sole canonical shared instruction file. `CLAUDE.md` contains a minimal `@AGENTS.md` import, so Claude Code loads the same guidance without a second copy. OpenCode reads `AGENTS.md` directly; it does not treat `CLAUDE.md` as a fallback. Codex also reads `AGENTS.md` as project guidance. These adapter facts are documented against current official product docs, but direct interactive verification of all three products remains pending.

Future provider-specific skills, commands, hooks, or configuration may be useful for convenience. They belong in optional adapters and must not own canonical intent or make the framework unusable when removed. A provider's command vocabulary should never be required to run a CraftRail workflow.

## Why repository-native

Keeping the artifacts in Git makes review, history, branching, and change ownership use tools the engineering team already has. It also places requirements close to code and tests that implement them. The tradeoff is that teams must maintain readable records and resolve diffs; CraftRail does not provide a central database, workflow dashboard, or automated approval system.

## Why Markdown-first, not Markdown-only

Markdown handles prose and tables well and is supported by common code review and editor tools. Mermaid provides editable diagrams without storing only binary screenshots. YAML and JSON provide machine-readable structures for contracts and forms. No one format is appropriate for every project: use a native binary/editor format when it clearly serves a need, but commit its editable source and link to it. The framework's core examples use text formats because they make the simplest portable baseline.

## Why stable IDs and traceability

Stable IDs help link requirements to acceptance criteria, tasks, tests, ADRs, and reviews. They reduce ambiguity when prose moves or titles change. The cost is careful ID retirement and scope discipline. IDs should be used only for records that need stable references; numbering every sentence creates maintenance without meaningful traceability.

## Why small scripts instead of a platform

The initializer creates one feature folder from templates. The validator checks a selected set of structural and syntax errors. Python's standard library avoids a runtime dependency tree and makes both tools work offline. This means semantic consistency, YAML/OpenAPI validation, visual diagram rendering, and automatic artifact generation remain outside the core tool. The project can add optional tooling later if the need is demonstrated.

## What CraftRail does not do

- It does not guarantee generated code or decisions are correct.
- It does not replace tests, review, security analysis, product judgment, or architecture ownership.
- It does not automatically approve requirements or architecture.
- It does not generate or enforce all code from specifications.
- It does not mandate a coding agent, programming language, architecture, issue tracker, or delivery method.
- It does not replace Spec Kit, OpenSpec, or a requirements-management platform.

## Use the site without coupling source content

The documentation website is a presentation layer over repository Markdown. The generator and Vercel config are replaceable; the Core remains in `docs/`, `specs/`, and `templates/`. A reader can clone the repo and use the framework without visiting the website.

Continue with the [repository structure](repository-structure.md), [workflow](workflow.md), or [quickstart](quickstart.md).

For the reasons behind the format, workflow, Python tooling, and website choices—including their tradeoffs—see the [design rationale](design-rationale.md).
