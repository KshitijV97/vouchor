# Adopt CraftRail in an existing project

CraftRail is designed for gradual adoption. An existing project does not need to rename its folders, move all documentation, adopt every identifier prefix, or replace its issue tracker. The goal is one durable source for each important engineering fact, with links that make the ownership clear.

## Step 1: inventory existing sources

Identify where the project currently keeps product intent, requirements, architecture, technical decisions, API/data contracts, feature plans, tests, and release notes. For each area, ask who maintains it and whether engineers trust it. A stale wiki may not be authoritative merely because it has a page title; a test suite may describe actual behavior while not explaining desired policy.

Record the current canonical path and owner in `docs/project/README.md`. If a source is outside the repository, link to it and record access/retention assumptions. Do not copy content until you have an owner for resolving differences.

## Step 2: add the shared instruction boundary

Create or adapt one concise root `AGENTS.md` for common working rules. Preserve any valuable existing instruction content and consolidate duplicated policy. Keep provider-specific syntax out of this file. If Claude Code compatibility is needed, add `CLAUDE.md` with only `@AGENTS.md`; OpenCode users rely on root `AGENTS.md` directly. Avoid nested instructions until a directory has a genuinely different rule.

## Step 3: choose one small pilot

Pick an upcoming change with a real requirement or architecture question. Do not start by rewriting years of historical documents. Use one feature spec to discover missing context, stable IDs, and verification evidence. If the pilot exposes a template problem, change the template and explain the change.

## Step 4: migrate by ownership, not by file extension

Move or adapt an artifact only when its current owner agrees and the destination adds value. Preserve links from old locations where history matters. Mark superseded records and identify replacements. Keep existing ADR conventions if they already work; map their status and fields rather than creating parallel decisions.

For contracts, choose one source file and generate other representations when possible. For diagrams, commit editable source. For tasks, the team's project tracker can remain canonical; include stable issue links and the requirement/verification relationship in the feature docs as needed.

## Step 5: scope validation to the real project

The supplied validator expects CraftRail's starter baseline. Before copying it into a repository with a different structure, decide whether to adapt `REQUIRED_PATHS`, add a config interface, or run it only on a dedicated subtree. Do not make the validator green by adding empty placeholder files. A passing structural check is useful only when its scope matches project reality.

## Step 6: retain what works and remove what does not

After a feature or two, review whether IDs improve discussions, whether docs are updated during review, and whether checks catch real mistakes. Remove ceremony with no reviewer value. Expand checks only when the desired rule is stable and can be checked accurately. Do not make the optional docs-site package a runtime dependency for a project that only wants the Markdown framework.

## Typical adoption patterns

| Pattern | When it fits | How to avoid drift |
|---|---|---|
| Copy `AGENTS.md` and add feature specs | The project needs durable intent but already has good architecture docs. | Link to the existing architecture and assign ownership. |
| Add ADR and requirements conventions | Decisions and policy currently disappear into chat or PR descriptions. | Choose one folder/ID scope; avoid parallel decision logs. |
| Use templates but keep issue tracker as task source | Work execution already lives in GitHub/Jira/another tracker. | Reference issue IDs in tasks instead of copying statuses manually. |
| Add the validator | Structural consistency is worth catching in CI. | Tune required paths and understand semantic limits before gating merges. |
| Add the docs website | Readers need browsable navigation and search. | Render canonical Markdown; never edit generated site output. |

Start with the [quickstart](quickstart.md) or review [repository structure](repository-structure.md) before copying files.
