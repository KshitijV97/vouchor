# Quickstart

This guide gets a team from an empty or existing repository to one reviewable feature. It assumes Python 3 for the helper scripts. The framework itself is plain files; no agent account, package install, or web service is required.

## Path A: start a new project from the template

1. Create a repository from the [published CraftRail GitHub template](https://github.com/kshitijv97/craft-rail), or clone/copy it locally. GitHub template creation is explained in [template usage](github-template-usage.md).
2. Read `AGENTS.md` and `docs/framework/overview.md`. Keep `AGENTS.md` as the shared instructions file; adapt it only to actual project rules.
3. Rewrite `docs/project/product-brief.md` with evidence, users, outcomes, boundaries, constraints, assumptions, and open questions. This is project intent, not a landing page.
4. Review `docs/project/engineering-principles.md`. Adopt or edit principles through the project decision process rather than accepting the starter verbatim.
5. Replace stakeholder and glossary entries with verified terms. Remove example rows that are not true of the new project.
6. Decide where authoritative requirements, architecture, ADRs, and contracts live. Fill in `docs/project/README.md` or link to external in-repository paths; avoid two canonical copies.
7. Delete illustrative content when it could confuse readers, or leave it clearly labeled as an example. Do not treat `000-example-feature` as a real feature.
8. Run baseline checks and commit the customized starting point after review.

## Path B: add one feature

Create a folder:

```bash
python3 scripts/new_feature.py "User authentication"
```

The tool normalizes the title into a safe slug, picks the next available feature number, copies the feature templates, and fills feature ID/title/date metadata. It never overwrites a path. It does not decide requirements or approve the draft.

Then:

1. Inspect relevant source, tests, and project docs; record facts and unknowns.
2. Draft `spec.md`: problem, outcomes, scope, actors, requirements, acceptance criteria, risks, and open questions.
3. Resolve material ambiguities and get approval from the project's human decision owner.
4. Write `plan.md` and diagrams for the technical approach. Link to accepted ADRs and contracts.
5. Break work into dependency-ordered, verifiable tasks in `tasks.md`.
6. Cross-check the artifacts, implement within approved scope, and add tests.
7. Record evidence in `verification.md`; update docs after behavior is reviewed.

See the [detailed lifecycle](workflow.md), [feature-spec guide](feature-specification-guide.md), and [worked example](../examples/sample-feature-walkthrough.md).

## Validate the repository

```bash
python3 scripts/validate_docs.py
python3 -m unittest discover -s tests -v
```

The validator checks selected structure and syntax offline. It cannot decide whether product intent is correct or whether a test proves its requirement. `--strict` also fails on warnings; OpenAPI YAML currently produces a documented warning because the core tool intentionally has no YAML parser. See [validator checks and limits](validation.md).

## Use a coding agent

Open the repository root in Codex, Claude Code, or OpenCode and describe your task normally. The project instructions make CraftRail the default, so no separate setup prompt is needed. Each agent should read the relevant project brief, requirements, accepted ADRs, and feature records as directed by `AGENTS.md`; avoid loading the whole docs tree. Claude Code's root `CLAUDE.md` imports the shared file; OpenCode reads `AGENTS.md` itself. Compatibility is documented, while direct interactive testing remains pending.

Use the prompts in [workflow prompts](workflow-prompts.md) as ordinary chat instructions. Read their output as a proposal until the appropriate human approves it.

## Preview and deploy documentation

For a local docs-site preview or Vercel build, follow the [documentation website guide](documentation-site.md). The site generator is isolated from the core Python scripts and reads canonical Markdown directly.
