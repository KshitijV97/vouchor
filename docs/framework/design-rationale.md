# Design rationale for developers

This page explains why CraftRail is built the way it is, what the design enables, and where its limits are. It is intended to make the repository reviewable as an engineering system rather than just a collection of templates. The brief is the historical input; the canonical working conventions are the root `AGENTS.md` plus the Markdown, Mermaid, YAML, and JSON files linked from this documentation.

## The governing principle

> **The framework owns the engineering process. The coding agent is replaceable.**

This is both product philosophy and an architectural boundary. Product requirements, architecture, decisions, contracts, workflow, and verification evidence live in provider-neutral formats under version control. An agent adapter tells a particular tool where to find the shared policy; it does not become the authority for product behavior. This makes the repository usable in Codex, Claude Code, OpenCode, a future agent, and ordinary human-only development.

The practical test is straightforward: if an agent-specific configuration disappears, can a developer still understand the requirements, make a change, and verify it? If not, too much project knowledge has been placed in the adapter.

## Three layers and why they are separated

| Layer | Owns | Examples | Change when |
|---|---|---|---|
| Core | Durable engineering intent and evidence | `docs/project/`, `specs/`, `templates/`, contracts, ADRs | The project or feature intent changes |
| Workflow | The human-governed path from intent to verified change | Lifecycle guide and copyable prompts | The team changes its engineering process |
| Adapters | Tool-specific discovery of shared context | `AGENTS.md`, minimal `CLAUDE.md` import | An agent changes how it reads instructions |

This separation prevents tooling churn from forcing a migration of specifications. It also keeps any future adapter optional. There is no provider SDK, model API, prompt execution engine, plugin system, or proprietary command in the Core.

## Why repository-native and Git-backed

Engineering intent changes with the software. Storing it beside the code lets the same review, branch, history, and access-control practices govern both. A requirement change can be reviewed with its implementation; a decision can be linked to the code and tests it explains; a new contributor can inspect the history rather than rely on a private chat.

The cost is deliberate: teams must curate records, resolve text conflicts, choose what should be committed, and keep documents current. Git does not provide a requirements dashboard, workflow engine, approval policy, notification system, or semantic merge. CraftRail uses repository conventions because they are widely available and auditable, not because files are always the best interface for every organization.

## Why Markdown is the prose format

Markdown is readable without a special editor, renders in source hosts and code review, produces useful diffs, and can include tables, links, and fenced examples. It is plain text, so it remains understandable if CraftRail's site generator or current coding agents disappear. It also supports gradual adoption: teams can start with only `AGENTS.md` and one feature specification.

Markdown is not a database. It cannot reliably enforce relationships or semantics on its own, and large tables can be awkward to maintain. CraftRail adds stable identifiers and small structural checks where those solve a concrete problem. It does not attempt to parse every sentence into a schema or make prose machine-authoritative.

## Why Mermaid, YAML, and JSON sit alongside Markdown

- **Mermaid** stores diagrams as editable text next to explanatory prose. It is useful for context, container, component, sequence, state, and data-flow views. Text diffs show changes to relationships. Rendering still depends on a compatible viewer, and CraftRail's validator checks only that a diagram is non-empty and begins with a recognized declaration; it does not prove the diagram compiles or matches the implementation.
- **YAML** is used where an existing ecosystem already expects it, especially OpenAPI and GitHub issue forms. YAML is concise for hand-authored structures, but indentation and implicit typing can surprise readers. The core validator does not parse YAML, so the OpenAPI starter currently emits a visible warning rather than claiming validation.
- **JSON** is used for machine-readable structured examples such as JSON Schema. The standard library can verify JSON syntax, but the current validator does not verify a schema against its meta-schema or validate instance data against that schema.

No format is mandated for every artifact. A team can use another format when it has a clear reason, but should keep the source editable, reviewable, and linked from the canonical project documentation.

## Why a lifecycle with explicit quality gates

The Discover → Specify → Clarify → Plan → Tasks → Analyze → Implement → Verify → Converge lifecycle names the kinds of thinking that are often skipped when an agent begins editing code immediately. Separating them makes ambiguity, assumptions, constraints, and verification observable. The gates are proportional: a small typo need not create a full specification, while a security boundary or data migration deserves deeper discovery and review.

The lifecycle is guidance, not a mandatory meeting sequence or state machine. Teams decide which artifacts are proportionate and who approves them. CraftRail deliberately has no automatic approval feature: an agent can propose a requirement or decision, but an accountable human owns material product and architecture choices.

## Why stable IDs and traceability

Stable IDs are useful when the title or wording of a requirement changes but downstream discussions still need to point to the same obligation. CraftRail's examples connect requirement IDs to acceptance criteria, tasks, and verification evidence. This makes gaps easier to spot during review and helps a change explain what it intended to satisfy.

IDs have a maintenance cost. Avoid numbering every sentence; reserve identifiers for requirements and records that need durable cross-references. Do not recycle retired IDs, and document supersession where references matter. Current tooling catches short IDs and duplicate declarations within a document, but it does not build a repository-wide graph, detect every dangling reference, or prove a test truly verifies a criterion.

## Why Python for the repository tooling

The two core scripts solve small repository tasks: copy and number a feature folder, and identify selected documentation structure errors. Python was chosen because it is commonly available on developer and CI machines, has a readable standard library, handles filesystem and text processing well, and can run without installing dependencies. The scripts use `argparse`, `pathlib`, `re`, and `json`; the core validator and initializer make no network calls. Python is also familiar to maintainers who may want to extend a small tool without introducing a compiled binary or runtime service.

This choice optimizes for a low-friction baseline, not maximum language neutrality or exhaustive parsing. Python is an extra interpreter requirement for the scripts and tests; users of other ecosystems may prefer a native tool. The scripts are not a stable public API, package, or general-purpose specification engine. The standard library has no YAML or OpenAPI parser and no Mermaid renderer. That is why unsupported checks are disclosed rather than silently approximated.

The website is a separate concern: its build dependency is pinned in `requirements-docs.txt` and installed into an isolated environment. That does not add a Python dependency to the software project that adopts the framework unless the adopter chooses to use the scripts or build the site.

### What the Python tooling enables

- Create a numbered feature directory from the same reviewed templates every time.
- Refuse to overwrite an existing feature folder and normalize titles to portable slugs.
- Catch common structural mistakes, malformed JSON, broken simple relative links, and duplicate or undersized declared IDs.
- Run locally and in GitHub Actions with the same standard-library code.
- Run tests written with the standard-library `unittest` module on Python 3.10, 3.12, and 3.14 without installing a test runner.
- Use optional, pinned development tools (Ruff, Mypy, pytest/coverage, and pre-commit) for stricter checks on the framework repository itself.

### What it does not enable

- Judge whether prose is correct, complete, unambiguous, secure, or valuable.
- Understand all Markdown link forms, resolve heading fragments, or validate links on the public internet.
- Validate OpenAPI semantics, render Mermaid, validate JSON Schema semantics, or prove that tests trace to actual behavior. The optional development hook checks YAML syntax only.
- Enforce code architecture, block an agent from editing files, or replace code review and test suites.
- Operate as a hosted service, accept team approvals, or produce a report database.

Adding a dependency should require a specific, recurring validation need, a clear owner, and a documented failure mode. The cost includes installation, supply-chain review, version compatibility, and maintenance. The current warning about OpenAPI YAML is an explicit boundary that can be revisited rather than a claim that the file has been checked.

## Why these tools and workflows

| Choice | Why it fits this version | What it enables | What it does not do |
|---|---|---|---|
| Git and ordinary files | Existing developer workflow; portable and inspectable | Version history, code review, branches, offline authoring | Semantic merges, dashboards, approvals, synchronization to external systems |
| Markdown | Broad editor and hosting support | Human-readable specifications and guides | Typed data validation or relationship enforcement |
| Mermaid | Diagrams remain source text | Reviewable architecture and behavior diagrams | Guaranteed rendering in every host or source-code conformance |
| Python standard library | Low setup and no third-party runtime dependencies | Small cross-platform file/text tooling and unit tests | Deep language parsing, YAML support, diagrams rendering |
| `unittest` + pytest-cov | Tests use standard-library `unittest`; pytest-cov adds local branch coverage | Cross-version core test execution and a 90% scripts coverage gate in the dev environment | Formal proof, exhaustive input testing, or zero untested behavior |
| Ruff + Mypy | One fast lint/formatter and a strict static type checker | Catch common errors, formatting drift, and many type inconsistencies before runtime | Runtime type enforcement or correctness guarantees |
| actionlint | Static checker designed for GitHub Actions | Catch workflow schema/expression errors and selected script-injection hazards | Run workflows or verify deployed infrastructure |
| pre-commit | Manages local commit-time checks | Run formatter, lint, typing, docs validation, YAML/JSON checks, and tests before committing | Enforceable security; a contributor can bypass local hooks, so CI repeats the checks |
| GitHub Actions | Runs cross-version tests, quality hooks, and site build on pushes and pull requests; creates releases on tags | Automated CI and repeatable GitHub release notes | Docs-site CD, local verification, or review judgment |
| Zensical | Reuses Markdown, provides navigation/search/Mermaid, emits static files | A navigable developer manual and static output | Canonical storage, engineering semantics, or a stable mature generator API; it is pinned at beta 0.1.0 |
| Vercel static deployment | Serves generated files without a CraftRail server | CDN delivery of the docs site | Automatic Git deploy unless repo integration is connected; documentation is currently behind deployment protection |

GitHub Actions validates the framework repository and builds the site in CI. It is intentionally separate from Vercel's manual CLI deployment. The existing Vercel project did not connect to the GitHub repository, so a push alone does not update the deployed site today. The release workflow creates GitHub Release pages after a maintainer pushes an annotated semantic-version tag; it does not create tags or choose versions on the maintainer's behalf.

## Why the documentation site is only a presentation layer

The site improves navigation and discovery for a long developer guide, while every page remains ordinary Markdown under `docs/`. Zensical reads that source and builds static HTML into the ignored `site/` directory. Static files avoid a server, database, account-backed authoring system, or application runtime. The site generator is an adapter over documentation, not a new canonical repository.

Zensical was selected as the successor project announced by the Material for MkDocs maintainers. At the time of adoption, Zensical 0.1.0 is a beta, so pinning it provides repeatable builds but also requires periodic upgrade review. If it becomes unsuitable, the source pages can move to another static generator without rewriting their content. See [how the site is built and updated](documentation-site.md).

The explicit navigation order adds a small maintenance step when adding a page. It prevents internal starter project files, the build brief, and example registers from becoming primary public navigation. `exclude_docs` also excludes the starter `docs/project/` content from the generated site; the repository itself still contains those editable files for template adopters.

## Why not a full platform, database, or code generator

The problem to solve first is durable intent and consistent practice. A platform would introduce hosting, accounts, data migration, service availability, security boundaries, and a required product runtime before proving that teams want those capabilities. Full code generation can also turn an incomplete or incorrect specification into confidently structured but still wrong output. CraftRail starts with human-readable records, reviewable templates, and bounded checks; later automation can be optional and validated against real adoption needs.

This makes CraftRail less automated than a workflow product. That is a deliberate scope tradeoff for an initial repository template, not a claim that manual process is always better.

## Why adapters stay small

`AGENTS.md` is the shared instruction source because it is supported directly by Codex and OpenCode and provides the common policy. `CLAUDE.md` is only an import adapter, so the Claude-specific discovery filename does not become a second policy source. Workflow prompts are ordinary language that can be pasted into supported tools or followed by a person.

Compatibility is documented separately from direct product testing. Instruction discovery is a published product behavior, but CraftRail has not claimed that the exact acceptance procedure was manually run in all three agent applications. See the [compatibility matrix](agent-compatibility.md).

## Security and trust boundaries

CraftRail's Markdown is advisory context for an agent, not an access-control boundary. A repository agent can still misread instructions, make an unsafe edit, or produce insecure code. Review permissions, secrets, CI tokens, and tool access using the underlying platform controls. The templates call attention to sensitive data and trust boundaries, but do not provide a security scanner or certify architecture.

The documentation deployment is configured as static output. Vercel deployment protection is currently enabled on the deployed project, and the GitHub repository is not connected for automatic deployment. Both facts matter operationally: the URL exists, but public readers may be asked to authenticate, and updates need a manual CLI deployment until the owner changes those settings.

## Revisit these choices when evidence changes

Reconsider tooling when teams repeatedly need checks the standard library cannot provide; revisit the site generator when its beta status or maintenance changes; revisit artifact formats if review becomes unreadable; and revisit the workflow if teams find its gates too heavy or too weak. Record material changes as an ADR rather than silently rewriting history. The current known owner decisions are listed in [assumptions and decisions](assumptions-and-decisions.md).
