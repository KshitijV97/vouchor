# ADR-001: CraftRail Studio is a Git-native, static, optional view-and-editor over repository artifacts

- **Status:** proposed
- **Date:** 2026-11-09
- **Decision owner:** CraftRail maintainer
- **Related:** [spec](spec.md), [plan](plan.md), [graph contract](contracts/craftrail-graph.schema.json), [front-matter contract](contracts/craftrail-frontmatter.schema.json); CraftRail guides `docs/framework/concepts.md`, `docs/framework/traceability-and-verification.md`, `docs/framework/agent-compatibility.md`

> Numbering note: renumber this ADR to the next free ADR number in the target repository when it is moved there.

## Context and forces

CraftRail records intent, decisions, work and evidence as Markdown in Git. People want what tools like Jira and Trello offer: boards, filters, item detail, history, burn-up, cycle time and WIP. They also want what those tools can't do: requirement → acceptance → task → test → evidence traceability. The relevant forces:

1. **Single source of truth.** CraftRail says generated views must never become a second source of policy (`concepts.md` → "Canonical versus generated information"). A tracker with its own database would drift away from `spec.md`, `tasks.md` and `verification.md`.
2. **Agent neutrality.** The core must not depend on any AI provider, and adapters stay optional (`AGENTS.md`).
3. **Dependency-free core.** CraftRail's Python tools use only the standard library.
4. **Cost.** Hosting should be free or nearly free, and token spend should be zero unless a person explicitly runs an AI action.
5. **Honest metrics.** A dashboard percentage can create false confidence (`traceability-and-verification.md`). Metrics must say what they measure.
6. **Parseability.** The current conventions mix bullet metadata (`- **Status:** draft`), Markdown tables and prose. Parsing is fragile, and the same IDs (for example `TASK-001`) appear in many feature folders.

## Decision

Build **CraftRail Studio** as an **optional** component with five parts:

1. **Machine-readable conventions (core).** A restricted YAML front-matter profile carries per-file metadata. Per-item data stays in Markdown tables and declaration bullets with **canonical column headers**. Both are documented as contracts and checked by the standard-library validator. Files without front-matter still parse through the legacy bullet metadata for one minor version, and a migration command converts them.
2. **Identity model (core).** Project-wide kinds (`BR`, `FR`, `NFR`, `CON`, `US`, `ADR`) are unique across the repository. Feature-local kinds (`AC`, `TASK`, `TEST`) are qualified by feature number, giving canonical keys like `003:TASK-002`. This formalises what `concepts.md` already permits.
3. **Exporter (core, standard library only).** `scripts/export_graph.py` parses the working tree and Git history (through the `git` CLI) into one versioned JSON document, `craftrail.json`. The document holds items, typed links, status-change events, computed metrics and diagnostics. The exporter uses no AI.
4. **Studio web app (optional, `studio/`).** A static single-page app (Vite + React + TypeScript) reads `craftrail.json` and renders an overview, boards, a traceability graph and matrix, item detail, history, metrics and decisions. It has no server and no database. It can be hosted anywhere static: GitHub Pages, Cloudflare Pages, or any web server.
5. **Editing through Git only.** Every edit is a typed patch that a single TypeScript patch engine turns into a minimal text diff of the source file. Edits are saved through a pluggable **Git backend**:
   - `local`: a standard-library HTTP server bound to `127.0.0.1` reads and writes files in the working tree.
   - `github`: the GitHub REST API, through commits on a branch or pull requests. Changes to approval statuses always go through a pull request.
   - Other forges, such as GitLab and Gitea, can be added later behind the same interface.

**AI policy:** Studio makes **no model calls** in v1. It builds **scoped prompts and context packs** from the graph, using CraftRail's neutral workflow prompts. The user copies them into any agent. The same algorithm is available as a CLI (`scripts/context_pack.py`) for terminal agents. Token cost to the platform is therefore zero, and prompts stay small because they contain only the linked items.

## Alternatives considered

| Alternative | Why not chosen |
|---|---|
| Jira, Linear or another SaaS tracker | Paid, proprietary, and a second source of truth that drifts from specs |
| GitHub Projects or Issues as the tracker | Free, but duplicates status and is tied to one forge. Acceptable later as a **one-way mirror** adapter only. |
| Git-based CMS (Decap, TinaCMS, Keystatic) | Good for editing prose, but no traceability graph, boards, metrics or ID model. Would need forking or heavy customisation. |
| Obsidian with plugins | Not open source and not shareable as a hosted view; plugin data formats are not CraftRail contracts |
| Server app with a database (for example FastAPI + Postgres) | Hosting cost, sync problems, backups, and a second source of truth |
| One file per requirement or task | Machine-friendly, but too much file churn for people. Tables remain readable on GitHub. |
| TOML front-matter (`+++`) with stdlib `tomllib` | GitHub and Zensical render YAML front-matter natively but not TOML. `tomllib` would also force Python 3.11+ on the core. |
| Patch engine written in both Python and TypeScript | Two implementations to keep in sync. Only reads are duplicated (exporter in Python), and a shared fixture corpus checks them against each other. |
| AI calls built into Studio | Adds provider coupling, keys and cost. Copyable prompts give most of the value for free. |

## Consequences

- **Positive:**
  - Git stays the only source of truth, so history, review, permissions and audit come free from the forge.
  - Hosting costs $0. The tool works offline in local mode.
  - Traceability gaps become visible. Agents and people edit the same files.
  - The JSON export is useful to any tool, including agents, CI gates and external dashboards.
- **Negative / risks:**
  - Parsing Markdown tables is less robust than a database. Mitigation: strict canonical headers, validator diagnostics, and fixture-based round-trip tests.
  - Minimal-diff editing can collide with concurrent edits. Mitigation: optimistic concurrency (file content hash locally, blob SHA on GitHub) and a conflict UI.
  - Mining Git history needs full history (`fetch-depth: 0`) and slows down on large repositories. Mitigation: an incremental cache, and metrics marked `partial` on shallow clones.
  - The repository gains a Node toolchain for `studio/`. It stays outside the core: the validator and exporter remain standard-library Python.
  - Metrics can still be misread. Mitigation: every metric shows its definition, and "linked coverage" is labelled as links, not proof of correctness.
- **Follow-ups:** a GitHub Projects one-way mirror adapter, GitLab/Gitea backends, an optional AI-action adapter, and live multi-user collaboration are all out of scope for v1.

## Supersedes / superseded by

None.
