# Feature NNN: CraftRail Studio

- **Status:** proposed
- **Owner:** CraftRail maintainer
- **Created:** 2026-11-09
- **Updated:** 2026-11-09
- **Related issues/PRs:** none yet
- **Decision:** [ADR-001](ADR-001-craftrail-studio-git-native-static-studio.md)

> Numbering note: `NNN` becomes the next free feature number when this folder is copied into the target repository's `specs/`. IDs below (`FR-001` …) are local to this proposal; renumber them if they collide with the target repository's registers.

## Context and problem

CraftRail keeps requirements, decisions, tasks and verification evidence as Markdown in Git. That is reviewable and agent-friendly, but people cannot easily see the state of a project: what is in progress, what is blocked, which requirements have no tests, how long work takes, or what changed this week. Teams then reach for Jira or Trello and create a second source of truth that drifts from the specs.

Current repository facts (evidence):

- Feature metadata is a bullet block (`- **Status:** draft`) parsed by `scripts/validate_docs.py`. Registers, tasks and verification are Markdown tables with mostly consistent headers.
- `scripts/new_feature.py` copies `templates/feature/`. Every feature therefore contains `TASK-001` and `TEST-001`, so these IDs are only unique inside one feature, which `docs/framework/concepts.md` allows.
- The validator detects duplicate IDs only within one file.
- `docs/framework/traceability-and-verification.md` warns that dashboard percentages can create false confidence.

## Goals and measurable outcomes

- A person can open one page and see project state (boards, gaps, metrics) without reading every file. Signal: every view in [Views](#views) renders from a fixture repository in the e2e suite.
- A person can change status, owner or text fields through a form, and the result is a minimal Git diff. Signal: round-trip fixture tests show only the intended lines change.
- Running Studio costs nothing: read-only hosting is static, local mode needs no network, and no AI calls are made. Signal: the deployed build has no server-side code, and a network-blocked e2e test passes in local mode.
- Studio shows traceability that trackers cannot: requirement → acceptance criterion → task → test → evidence. Signal: matrix and graph views flag every gap category defined in `FR-016`.

## Actors and scenarios

- **Maintainer / tech lead:** reviews the board weekly, spots blocked tasks and uncovered requirements, and approves a spec through a pull request opened from Studio.
- **Contributor:** drags a task to `in-progress`, fills in verification evidence after running tests, and saves. Studio writes the files, and the contributor commits.
- **Coding agent (any provider):** runs `python3 scripts/context_pack.py 003:TASK-002` to get a small, linked context bundle before implementing. Alternatively, a person copies a Studio prompt into the agent.
- **Stakeholder / reader:** opens the hosted read-only Studio to check progress and metrics.

## Scope and non-goals

- In scope:
  - the front-matter profile and canonical table conventions;
  - the identity model;
  - validator extensions;
  - the `craftrail.json` exporter with Git-history events and metrics;
  - the static Studio app (overview, boards, traceability, item detail, metrics, decisions, search);
  - editing through `local` and `github` backends;
  - context packs and copyable prompts;
  - a CI workflow template for hosting;
  - migration of existing files;
  - an update to `new_feature.py`.
- Non-goals (v1):
  - a database or application server;
  - live multi-user co-editing;
  - comment threads (use pull request reviews);
  - time tracking;
  - notifications;
  - direct AI model calls;
  - GitLab/Gitea backends;
  - a GitHub Projects mirror;
  - mobile-specific layouts beyond responsive behaviour;
  - authentication for the hosted read-only view (use the host's access control).

## Requirements

### Conventions and identity

- `FR-001`: The system MUST define and validate a **front-matter profile**: a restricted YAML subset between `---` lines at the top of a Markdown file. The profile allows these keys:
  - `craftrail` (profile version, integer, required when front-matter is present);
  - `type`;
  - `id`;
  - `title`;
  - `status`;
  - `owner`;
  - `created`;
  - `updated`;
  - `approved_by`;
  - `approved_on`;
  - `related`;
  - `tags`;
  - `feature` (owning feature number in plan, tasks and verification files);
  - `supersedes` and `superseded_by` (ADRs);
  - extension keys prefixed `x_`.

  The grammar is defined in [Front-matter profile](#front-matter-profile). The canonical contract is [craftrail-frontmatter.schema.json](contracts/craftrail-frontmatter.schema.json).
- `FR-002`: The parser MUST also read the legacy bullet metadata block (`- **Key:** value` lines directly under the H1). It MUST emit a `deprecated-metadata` warning diagnostic for files using only the legacy form. When both forms are present, front-matter wins, and conflicting values produce an error.
- `FR-003`: The system MUST provide `python3 scripts/migrate_frontmatter.py [--check] [paths…]`. The command converts legacy metadata to front-matter, idempotently and without changing any other line. `--check` changes nothing and exits non-zero if a migration is needed.
- `FR-004`: The parser MUST recognise item tables by **canonical headers**, matched case-insensitively after trimming and collapsing whitespace, as listed in [Canonical tables](#canonical-tables). It MUST ignore other tables.
- `FR-005`: The system MUST assign every item a **canonical key**:
  - Features use `F<number>` (`F003`).
  - Project-wide kinds (`BR`, `FR`, `NFR`, `CON`, `US`, `ADR`) use the bare ID (`FR-012`).
  - Feature-local kinds (`AC`, `TASK`, `TEST`) use `<feature-number>:<ID>` (`003:TASK-002`).

  In graph mode (`validate_docs.py --graph`), duplicate declarations of a project-wide ID anywhere outside exempt paths MUST be an error.
- `FR-006`: The validator MUST check item statuses against per-type vocabularies ([Status vocabularies](#status-vocabularies)). Unknown statuses are errors in graph mode. Statuses with a trailing parenthetical note, such as `verified (illustrative)`, MUST be read as the base status plus a note.
- `FR-007`: `scripts/new_feature.py` MUST write front-matter into new feature files. It MUST replace requirement placeholders (`FR-NNN`, `NFR-NNN`, `BR-NNN`, `CON-NNN`) with the next free project-wide number per kind instead of the feature number. It MUST keep `AC`, `TASK` and `TEST` numbering local, starting at `001`.

### Exporter

- `FR-008`: `python3 scripts/export_graph.py [--out PATH] [--no-history] [--since REF]` MUST write a JSON document conforming to [craftrail-graph.schema.json](contracts/craftrail-graph.schema.json). The document contains `schema_version`, `repo`, `items`, `links`, `events`, `metrics`, `diagnostics` and `config`. The default output path is `craftrail.json` at the repository root, which is ignored by Git.
- `FR-009`: The exporter MUST extract typed links using the rules in [Link extraction](#link-extraction). Each link records its source location (`file`, `line`).
- `FR-010`: Unless `--no-history` is given, the exporter MUST mine Git history through the `git` CLI into `events` (`item_created`, `status_changed`, `owner_changed`, `item_removed`). Each event records the commit SHA, ISO-8601 timestamp and author **name** (never email). Renames MUST be followed.
- `FR-011`: The exporter MUST keep an incremental cache in `.craftrail/cache/` keyed by the last processed commit. It MUST rebuild fully when that commit is no longer an ancestor of `HEAD`.
- `FR-012`: The exporter MUST compute the metrics defined in [Metrics](#metrics) and include each metric's definition text. If history is shallow or missing, history-based metrics MUST be marked `partial: true` with a reason.
- `FR-013`: The exporter MUST report problems as structured `diagnostics` (`severity`, `code`, `message`, `file`, `line`). It MUST exit non-zero only for errors when `--strict` is given. A parse problem in one file MUST NOT stop the export of other files.
- `FR-014`: For the same commit and a clean working tree, export output MUST be byte-identical across runs. Keys are sorted, collections are ordered by canonical key, and `generated_at` is the `HEAD` commit time. A dirty working tree MUST set `repo.dirty: true`.

### Views

- `FR-015`: **Overview** MUST show:
  - item counts by type and status;
  - linked-coverage figures;
  - gap counts by category;
  - items blocked longer than the configured threshold;
  - the 20 most recent events;
  - data freshness (commit, time, dirty flag).
- `FR-016`: **Traceability** MUST provide a graph view and a matrix view of requirement → acceptance criterion → task → test → evidence. Both MUST highlight these gap categories:
  - `requirement-without-ac`;
  - `ac-without-task`;
  - `ac-without-verification`;
  - `task-without-requirement`;
  - `verification-without-evidence`;
  - `verified-without-evidence`;
  - `adr-proposed-stale`;
  - `dangling-reference`.
- `FR-017`: **Boards** MUST show Kanban columns per item type (tasks by default; also features, requirements, verification, ADRs). Columns come from the configured status mapping. Boards MUST filter by feature, owner, tag, type and text, and MUST support swimlanes by feature or owner.
- `FR-018`: **Item detail** MUST show:
  - metadata;
  - the rendered Markdown excerpt;
  - incoming and outgoing links;
  - the source location as a link to the file in the forge, or a local path;
  - a history timeline built from events.
- `FR-019`: **Metrics** MUST show burn-up, cumulative flow, cycle-time distribution, lead time, throughput per week, WIP over time, and the work-item ageing chart. Each chart MUST display its definition and the `partial` state.
- `FR-020`: **Decisions** MUST list ADRs with status, date and owner, and MUST draw supersession chains.
- `FR-021`: Global search MUST match keys, titles and excerpts. All filters, the selected view and the selected item MUST be encoded in the URL so a view can be shared by link.

### Editing

- `FR-022`: Studio MUST support these typed edit operations, each producing a minimal text diff:
  - `set_status`;
  - `set_field`, for `owner`, `title` and table cells under known headers;
  - `set_frontmatter`;
  - `create_item` (a new row or declaration with the next free key);
  - `create_feature` (equivalent to `new_feature.py`);
  - `create_adr` (from `templates/adr.md`);
  - `add_link`, which appends an ID to the relevant cell, such as tasks' `Requirement / AC` or `Depends on`.

  Lines not targeted by the operation MUST remain byte-identical, including line endings and trailing newline.
- `FR-023`: The **local backend** MUST be served by `python3 scripts/studio_server.py [--port N] [--app-dir PATH] [--open]`. The server uses the standard library only, binds to `127.0.0.1`, and provides:
  - `GET /api/graph`;
  - `GET /api/file?path=`;
  - `PUT /api/file` with `{path, base_sha256, content}`;
  - the static app.

  It MUST NOT run Git commands that change repository state.
- `FR-024`: The **GitHub backend** MUST authenticate with a user-supplied fine-grained personal access token. The token is held in memory by default, and in `sessionStorage` only if the user opts in. It needs `contents:write` and `pull_requests:write` on a single repository. The backend MUST write all queued changes as **one commit** on a new branch through the Git Data API, then open a pull request. The branch is named `studio/<YYYYMMDD>-<slug>`.
- `FR-025`: Studio MUST keep a **change queue** listing pending edits with a unified diff preview. The user can remove individual edits and save them together.
- `FR-026`: Saving MUST use optimistic concurrency: a content hash in local mode, the blob SHA in GitHub mode. On mismatch, Studio MUST show a conflict view with the current file, the user's edit and the option to re-apply the edit to the new version. It MUST never overwrite silently.
- `FR-027`: Before saving, Studio MUST validate edits against the JSON Schemas and against the graph rules it can check locally (status vocabulary, link targets exist, unique keys). It MUST block saving on errors and show warnings.

### Agent support (no model calls)

- `FR-028`: `python3 scripts/context_pack.py <key> [--budget CHARS] [--prompt NAME]` MUST output a Markdown context pack for an item using the [Context pack algorithm](#context-pack-algorithm).
- `FR-029`: Item detail MUST offer **Copy prompt** for these prompts from `docs/framework/workflow-prompts.md`:
  - review a specification;
  - produce a technical plan;
  - decompose into tasks;
  - implement approved work;
  - verify against acceptance criteria.

  Each prompt combines the pack with the selected prompt. Studio MUST NOT call any AI service.

### Hosting and configuration

- `FR-030`: The repository MUST include an optional workflow template, `.github/workflows/studio.yml`, that:
  1. checks out full history;
  2. runs the exporter;
  3. builds `studio/`;
  4. publishes a static artifact with the app plus `craftrail.json`.

  GitHub Pages deployment is the default step and can be replaced with any static host. The app MUST work from any base path.
- `FR-031`: Studio MUST read optional configuration from `.craftrail/studio.json` (schema in the graph contract under `config`). The configuration covers board column mappings, the blocked-age threshold, the stale-ADR threshold, artifact path globs, the forge URL template, and the default context budget. Every setting has a documented default.

## Non-functional requirements

- `NFR-001`: The validator, exporter, migration tool, context-pack CLI and local server MUST use only the Python standard library and support every Python version the core supports.
- `NFR-002`: On GitHub's `ubuntu-latest` runner, export of the reference fixture (2,000 items, 1,500 commits) MUST finish in under 15 s cold and under 2 s incremental with one new commit.
- `NFR-003`: The Studio initial JavaScript + CSS payload MUST be at most 350 KB gzip. The traceability graph MUST stay interactive with 1,000 nodes, measured as at least 30 fps while panning on the reference laptop in a recorded manual check.
- `NFR-004`: Studio MUST meet WCAG 2.2 AA: automated axe checks report zero serious or critical violations on every view, every drag action has a keyboard equivalent, and colour is never the only signal.
- `NFR-005`: Studio MUST work fully offline in local mode. It loads no CDN assets or remote fonts and sends no telemetry.
- `NFR-006`: The hosted build MUST ship a Content-Security-Policy meta tag restricting scripts to self and network access to self plus `api.github.com`.
- `NFR-007`: Test coverage MUST be at least 90% line+branch for the new Python modules (unit tests) and at least 85% for `studio/src` (Vitest). The patch engine and parsers MUST have 100% branch coverage.
- `NFR-008`: Studio MUST support the latest two versions of Chrome, Firefox, Safari and Edge.

## Business rules

- `BR-001`: Changing a feature to `approved` or an ADR to `accepted` MUST require an explicit confirmation step in which the user types the target key. The change MUST record `approved_by` and `approved_on` in front-matter. In GitHub mode it MUST go through a pull request, never a direct commit to the default branch. Studio MUST NOT offer bulk approval.
- `BR-002`: Studio and its prompts MUST NOT present a linked-coverage figure as proof of correctness. Every coverage figure MUST be labelled "linked coverage" with its definition.
- `BR-003`: Edits MUST only touch files matching the configured artifact globs. The defaults are `docs/project/**/*.md`, `specs/**/*.md` and `docs/**/decisions/*.md`. Templates, generated output and source code MUST be out of reach.
- `BR-004`: Generated outputs (`craftrail.json`, `.craftrail/cache/`, `studio/dist/`) MUST NOT be committed. The template `.gitignore` MUST list them.

## Constraints

- `CON-001`: No AI-provider or forge SDK may be a dependency of core Python tools. Forge access exists only in the optional Studio app's backend modules.
- `CON-002`: Read-only hosting MUST need only static file serving.
- `CON-003`: `studio/` dependencies MUST use OSI-approved licences compatible with the repository licence and MUST be pinned through a lockfile.
- `CON-004`: Canonical artifacts MUST stay readable and reviewable as plain Markdown on GitHub. No convention may require Studio to understand a file.

## Acceptance criteria

Conventions and identity

- `AC-001`: Given a file with valid front-matter, when the validator runs, then it reports no front-matter errors. Given each invalid case in the fixture corpus (bad key, nested map, multi-line string, wrong type, missing `craftrail`), then it reports one error with file and line. (`FR-001`)
- `AC-002`: Given a spec with only legacy bullet metadata, when exported, then its status is read correctly and a `deprecated-metadata` warning is emitted. Given conflicting front-matter and bullets, then an error is emitted. (`FR-002`)
- `AC-003`: Given the CraftRail repository, when `migrate_frontmatter.py` runs twice, then the second run changes nothing. A diff of the first run shows only metadata lines changed. `--check` exits 1 before migration and 0 after. (`FR-003`)
- `AC-004`: Given tables whose headers differ only in case or spacing from the canonical ones, when exported, then their rows become items. Given an unrelated table, then no items are created from it. (`FR-004`)
- `AC-005`: Given two features that each declare `TASK-001`, when exported, then keys `001:TASK-001` and `002:TASK-001` both exist. Given `FR-004` declared in two files, when `validate_docs.py --graph` runs, then it exits non-zero naming both locations. (`FR-005`)
- `AC-006`: Given `verified (illustrative)` in a verification row, when exported, then status is `verified` and note is `illustrative`. Given `donee`, then graph mode reports an unknown-status error. (`FR-006`)
- `AC-007`: Given a repository whose registers already declare `FR-001` to `FR-007`, when `new_feature.py "X"` runs, then the new spec declares `FR-008`, its tasks start at `TASK-001`, and the files contain valid front-matter. (`FR-007`)

Exporter

- `AC-008`: Given the fixture repository, when exported, then the output validates against `craftrail-graph.schema.json` and matches the committed golden file. (`FR-008`, `FR-014`)
- `AC-009`: Given a tasks row `| TASK-002 | … | FR-003, AC-002 | TASK-001 | TEST-002 … | planned |` in feature `004`, when exported, then the links include `004:TASK-002 implements FR-003`, `004:TASK-002 implements 004:AC-002`, `004:TASK-002 depends_on 004:TASK-001` and `004:TASK-002 verified_by 004:TEST-002`. (`FR-009`)
- `AC-010`: Given a fixture Git history where `003:TASK-001` moves `planned → in-progress → done` across three commits and its file is renamed in between, when exported, then three events exist with correct timestamps and author names, and no email appears anywhere in the output. (`FR-010`)
- `AC-011`: Given an exported repository, when one commit is added and export runs again, then only that commit is parsed (verified by a parse-count hook in tests). Given a rebase that removes the cached commit, then a full rebuild happens and the output equals a cold export. (`FR-011`)
- `AC-012`: Given the metrics fixture with known event timestamps, when exported, then every metric equals the hand-calculated value in the fixture's `expected-metrics.json`. Given a shallow clone, then history metrics have `partial: true` with reason `shallow-clone`. (`FR-012`)
- `AC-013`: Given a fixture with one malformed file among valid ones, when exported, then the valid files' items are present, one error diagnostic points at the malformed file, and the exit code is 0 without `--strict` and 1 with it. (`FR-013`)
- `AC-014`: Given a clean checkout, when exported twice, then the outputs are byte-identical. Given an uncommitted change, then `repo.dirty` is `true`. (`FR-014`)

Views (Playwright e2e against the fixture repository through the local server)

- `AC-015`: Given the fixture, when Overview opens, then counts, gap totals, blocked items and recent events equal those in the golden export. (`FR-015`)
- `AC-016`: Given the fixture with one example of every gap category, when Traceability opens in graph and matrix mode, then each gap is highlighted and listed with its category name. (`FR-016`)
- `AC-017`: Given the tasks board, when filtered by feature `002` and owner `qa`, then only matching cards show, and the URL reproduces the same view when reloaded. (`FR-017`, `FR-021`)
- `AC-018`: Given an item with links and history, when its detail opens, then incoming/outgoing links, source location and the event timeline are shown. (`FR-018`)
- `AC-019`: Given the metrics fixture, when Metrics opens, then each chart shows its definition text and values equal to `expected-metrics.json`. In shallow mode, a visible "partial data" notice appears. (`FR-019`, `BR-002`)
- `AC-020`: Given ADR-003 superseded by ADR-007, when Decisions opens, then the chain ADR-003 → ADR-007 is drawn and statuses are shown. (`FR-020`)

Editing

- `AC-021`: For every operation in `FR-022`, given its fixture file, when the patch is applied, then the result equals the expected file byte for byte. Re-exporting the result shows exactly the intended change. CRLF fixtures keep CRLF. (`FR-022`)
- `AC-022`: Given the local server is running, when a request comes from a non-loopback address, without the session token, with a foreign `Origin`, or for a path outside the artifact globs (including `../` traversal and symlinks), then it is rejected with 403. A valid `PUT` writes the file, and Git shows the change as unstaged. (`FR-023`, `BR-003`)
- `AC-023`: Given a mocked GitHub API (recorded fixtures via MSW), when three edits in two files are saved, then exactly one commit containing both files is created on a `studio/` branch and one pull request is opened. The token never appears in the URL, logs or `localStorage`. (`FR-024`, `FR-025`)
- `AC-024`: Given a file changed on disk (local) or on the branch (GitHub) after Studio loaded it, when the user saves, then a conflict view appears and no write happens until the user re-applies or discards. (`FR-026`)
- `AC-025`: Given an edit setting an unknown status or linking a non-existent key, when the user tries to save, then saving is blocked with an explanation. (`FR-027`)
- `AC-026`: Given a draft feature, when the user sets it to `approved`, then a confirmation dialog requires typing the feature key and records `approved_by`/`approved_on`. In GitHub mode the change can only be saved as a pull request. No multi-select approval control exists. (`BR-001`)

Agent support, hosting, quality

- `AC-027`: Given `003:TASK-002` in the fixture, when `context_pack.py 003:TASK-002 --budget 4000` runs, then the output is at most 4,000 characters, contains the task, its linked requirement and ACs with file paths, and matches the golden file. The TypeScript pack builder produces identical text for the same input. (`FR-028`, `FR-029`)
- `AC-028`: Given item detail, when **Copy prompt → Implement approved work** is clicked, then the clipboard contains the context pack followed by the prompt text, and the network log shows no request other than to the app origin. (`FR-029`, `NFR-005`)
- `AC-029`: Given the workflow template in a test repository, when it runs, then the artifact contains `index.html`, assets and `craftrail.json`. Served from a sub-path (`/repo-name/`), the app loads with no 404s. (`FR-030`, `CON-002`)
- `AC-030`: Given a `.craftrail/studio.json` that remaps task columns, when the board opens, then the columns follow the config. Given an invalid config, then a diagnostic is shown and defaults are used. (`FR-031`)
- `AC-031`: Given CI, when the quality job runs, then:
  - core-tool tests run on every supported Python version with only the standard library;
  - Python coverage is at least 90%, `studio/src` coverage is at least 85%, and parsers/patch engine have 100% branches;
  - axe reports no serious/critical violations;
  - the bundle-size check is at most 350 KB gzip;
  - the export benchmark meets `NFR-002`.

  (`NFR-001`–`NFR-004`, `NFR-007`)

## Edge cases and failure paths

- A table cell containing an escaped pipe (`\|`) or inline code with pipes MUST parse correctly and be preserved on edit.
- An item ID that appears only in prose (not declared) becomes a `mentions` link, not an item.
- A feature folder without a number (`specs/notes/`) is ignored, with an info diagnostic.
- Two features with the same number produce an error. Studio shows both but disables editing for them.
- Files over 1 MB are skipped with a warning.
- Non-UTF-8 files are skipped with an error diagnostic.
- Merge-conflict markers in a file produce an error, and that file's items are frozen (read-only) in Studio.
- Item deleted in history, then re-added with the same ID: emit `item_removed` then `item_created`. Metrics treat it as reopened, and cycle time uses the latest start.
- A GitHub token lacking scopes produces a clear permission error that lists the required scopes. Nothing is retried in a loop.
- The local server is started outside a Git repository: the server still serves files, history is disabled, and metrics are partial.
- Very large graphs (over 5,000 nodes): the graph view switches to feature-level clustering by default.
- A migrated feature or ADR that is already `approved`/`accepted` but has no recorded approver: migration leaves `approved_by` out, and graph mode reports `approval-unrecorded` (error) so the owner fills it in. Studio never guesses an approver.

## Data, dependencies, and interfaces

### Front-matter profile

```text
frontmatter := "---" NEWLINE { line } "---" NEWLINE
line        := key ":" SP value [SP "#" comment] NEWLINE
             | key ":" NEWLINE { "  - " scalar NEWLINE }      ; block list of scalars
             | "#" comment NEWLINE | NEWLINE
key         := [a-z][a-z0-9_]*
value       := scalar | "[" [ scalar { "," SP scalar } ] "]"   ; inline list
scalar      := integer | "true" | "false" | date | quoted | plain
date        := YYYY-MM-DD
quoted      := '"' { char | '\"' } '"'
plain       := text without leading [ "[", "{", "&", "*", "!", "|", ">", "'", '"', "%", "@", "`" ] and without ": " or " #"
```

No anchors, aliases, tags, nested mappings, flow mappings or multi-line scalars. Allowed keys and types per `type` are defined in [craftrail-frontmatter.schema.json](contracts/craftrail-frontmatter.schema.json).

Example (feature spec):

```yaml
---
craftrail: 1
type: feature
id: "003"
title: Account recovery
status: approved
owner: Identity lead
created: 2026-11-09
updated: 2026-11-12
approved_by: Identity lead
approved_on: 2026-11-12
related: [FR-012, ADR-004]
tags: [auth, security]
---
```

### Canonical tables

| Table (file) | Required headers (in order of first two; rest any order) | Item key from | Optional headers |
|---|---|---|---|
| Requirement register (`docs/project/requirements/*.md`) | `ID`, then any title header, `Status` | `ID` cell (project-wide kind) | `Owner`, `Rationale/source`, `Acceptance / verification`, `Scope`, `Type (BR or CON)`, `Measure or evaluation method` |
| Tasks (`specs/NNN-*/tasks.md`) | `ID`, `Task / expected output` (alias `Expected output`), `Requirement / AC`, `Depends on`, `Verification`, `Status` | `ID` cell (feature-local) | `Owner`, `Estimate`, `Notes` |
| Verification (`specs/NNN-*/verification.md`) | `Requirement`, `Acceptance criterion`, `Verification ID / method` (alias `Verification`), `Evidence or location` (alias `Evidence / location`), `Status` | first `TEST-` ID in the verification cell (feature-local) | `Owner`, `Date`, `Environment` |
| ADR index (`docs/**/decisions/README.md`) | `ADR`, `Decision`, `Status` | not items (ADR files are canonical); used only for consistency diagnostics | — |

Declaration bullets in `spec.md`: `` - `FR-001`: text `` (colon optional for legacy). A bullet declares an item. Its status is `proposed` unless a register row or front-matter of that requirement says otherwise.

### Status vocabularies

| Item type | Statuses (board column order) |
|---|---|
| feature | `draft`, `proposed`, `approved`, `in-progress`, `verified`, `deferred`, `deprecated` |
| requirement (`BR`/`FR`/`NFR`/`CON`/`US`) | `proposed`, `approved`, `implemented`, `verified`, `deferred`, `deprecated`, `superseded` |
| acceptance criterion | derived: `uncovered`, `planned`, `implemented`, `verified`, `blocked`, `waived` (from linked verification rows; worst state wins) |
| task | `planned`, `in-progress`, `blocked`, `in-review`, `done`, `dropped` |
| verification (`TEST`) | `planned`, `implemented`, `verified`, `blocked`, `waived`, `deprecated` |
| ADR | `proposed`, `accepted`, `rejected`, `deprecated`, `superseded` |

"Done" states for metrics: task `done`; feature `verified`; verification `verified`; requirement `verified`. "Started" states: task `in-progress`; feature `in-progress`.

### Link extraction

| Source | Rule | Link type |
|---|---|---|
| Tasks `Requirement / AC` cell | each ID | `implements` |
| Tasks `Depends on` cell | each `TASK-` ID | `depends_on` |
| Tasks `Verification` cell | each `TEST-` ID | `verified_by` |
| Verification row | `Requirement` cell IDs → item | `verifies` (TEST → requirement) |
| Verification row | `Acceptance criterion` cell IDs → item | `verifies` (TEST → AC) |
| Verification row | `Evidence` cell non-empty and not a placeholder | sets `evidence` attribute |
| Spec | AC bullet text containing requirement IDs, or AC listed under a requirement's sub-bullets | `refines` (AC → requirement) |
| Spec | every declared item | `belongs_to` (item → feature) |
| Front-matter `related` | each ID | `related` |
| ADR "Supersedes / superseded by" section | ADR IDs | `supersedes` |
| Any other ID mention in prose | — | `mentions` (weak; not used for coverage) |

Feature-local IDs in a feature's own files resolve to that feature. Cross-feature references use `NNN:ID`. Unresolvable references produce `dangling-reference` diagnostics.

### Metrics

All time metrics use event timestamps (commit author time, UTC). Weeks are ISO weeks. Values are computed for tasks unless stated otherwise.

| Metric | Definition |
|---|---|
| Linked coverage (requirements) | approved-or-later requirements with at least one `verifies` link from a `verified` TEST ÷ approved-or-later requirements. Label: "linked coverage, not proof". |
| Linked coverage (ACs) | ACs whose derived status is `verified` or `waived` ÷ all ACs in approved-or-later features |
| Cycle time | first transition into a started state → first subsequent transition into a done state. Reported as median, 85th percentile and per item. |
| Lead time | `item_created` → first done transition |
| Throughput | count of items entering a done state per ISO week |
| WIP | count of items in a started state at the end of each day |
| Cumulative flow | per day, count of items per status |
| Burn-up | per day, cumulative done count and total scope (created minus removed/dropped) |
| Ageing | for items currently in a started state: now (HEAD time) − latest start |
| Blocked age | for items currently `blocked`: HEAD time − entry into `blocked`. Items over the threshold (default 5 days) are flagged. |
| ADR staleness | `proposed` ADRs older than the threshold (default 14 days) since `item_created` |

Estimates: if a tasks table has an `Estimate` column with numbers, burn-up and throughput are also computed by estimate sum. Otherwise only counts are shown. No velocity is computed without estimates.

### Context pack algorithm

1. Start from the root item. Collect neighbours by link type in priority order:
   1. `implements` / `refines` targets;
   2. `verified_by` / `verifies`;
   3. `depends_on`;
   4. `belongs_to` feature;
   5. `related` ADRs.

   Use depth 1. For a feature root, use depth 2.
2. For each item, emit `### <key> — <title> (<status>)`, `Source: <path>:<line>`, then its excerpt (at most 600 characters, whole sentences).
3. If over budget (default 8,000 characters), drop excerpts in reverse priority order, then whole items, but never the root or its direct requirements.
4. Append `Read the source files listed above before acting.`, then the selected workflow prompt with `[spec path]`/`[IDs]` filled in.
5. Output is deterministic. Python (`context_pack.py`) and TypeScript (`studio/src/context/pack.ts`) MUST produce identical text on the shared fixtures.

### Interfaces

- Graph JSON: [contracts/craftrail-graph.schema.json](contracts/craftrail-graph.schema.json) (`schema_version` `1.0`; additive changes bump minor; breaking changes bump major).
- Front-matter: [contracts/craftrail-frontmatter.schema.json](contracts/craftrail-frontmatter.schema.json).
- Local server HTTP API: defined in [plan](plan.md#local-server-api).

## Security, privacy, accessibility, observability

- **Security:**
  - The local server binds to loopback only and uses a random 32-byte session token. The token is printed to the terminal and passed to the app in the URL fragment, never the query string, and is sent in the `X-CraftRail-Token` header.
  - The server checks `Origin` and `Host`, rejects symlinks and paths outside the globs, and limits request size to 2 MB.
  - The GitHub token is never persisted by default and never logged. A CSP is applied (`NFR-006`).
  - All Markdown is rendered with a sanitiser (no raw HTML execution).
- **Privacy:** no author emails, no telemetry, no external requests except the chosen forge API.
- **Accessibility:** `NFR-004`. Boards offer a "Move to…" menu as the keyboard alternative to drag. Charts have data-table fallbacks.
- **Observability:** the exporter prints timings per phase with `--verbose`. Studio shows the data freshness banner and a diagnostics panel.

## Assumptions, questions, and risks

| Type | Item | Owner / resolution |
|---|---|---|
| Question | Where should CraftRail keep its own ADRs (the `docs/project/` starter is illustrative)? Proposal: `docs/decisions/`. | Maintainer, before T1 |
| Question | Should Studio be released as part of the template repository or as a separate repository consumed by templates? Proposal: same repository, `studio/` optional, prebuilt app attached to releases. | Maintainer, before T9 |
| Assumption | GitHub is the first forge. Others follow through the backend interface. | Maintainer |
| Assumption | Python 3.10 remains the core minimum (3.10 reached end of life in October 2026; raising to 3.11 would not change this design). | Maintainer |
| Risk | Changing `new_feature.py` ID allocation affects existing users. Mitigation: documented in CHANGELOG, with old behaviour behind `--local-requirement-ids`. | Maintainer |
| Risk | Teams may treat metrics as performance targets. Mitigation: definitions shown everywhere, and guidance text in docs. | Maintainer |

## Traceability

- Decision: [ADR-001](ADR-001-craftrail-studio-git-native-static-studio.md)
- Plan: [plan.md](plan.md) · Tasks: [tasks.md](tasks.md) · Verification: [verification.md](verification.md)
- Framework guidance relied on: `docs/framework/concepts.md` (ID scope, canonical vs generated), `docs/framework/traceability-and-verification.md` (coverage honesty), `docs/framework/workflow-prompts.md` (prompt texts), `AGENTS.md` (agent neutrality).
