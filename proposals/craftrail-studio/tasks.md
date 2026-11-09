# Tasks: NNN CraftRail Studio

Dependency-ordered vertical slices. Each task is one reviewable pull request. Implement only after the spec is `approved`.

| ID | Task / expected output | Requirement / AC | Depends on | Verification | Status |
|---|---|---|---|---|---|
| TASK-001 | Resolve open questions (ADR location, contracts path, release packaging); move ADR and contracts into place; add `.gitignore` entries for generated outputs | BR-004 | — | TEST-031 review | planned |
| TASK-002 | `craftrail_core/frontmatter.py`: restricted YAML profile parser with line-accurate errors; unit tests covering every grammar rule and invalid case | FR-001, AC-001 | TASK-001 | TEST-001 | planned |
| TASK-003 | `legacy_meta.py` + precedence/conflict rules; deprecation diagnostic | FR-002, AC-002 | TASK-002 | TEST-002 | planned |
| TASK-004 | `md_tables.py` (escaped pipes, inline code, alignment rows) and canonical header matching; `declarations.py` | FR-004, AC-004 | TASK-001 | TEST-004 | planned |
| TASK-005 | `items.py`, `resolve.py`, `statuses.py`: canonical keys, feature-local scoping, status vocabularies with notes | FR-005, FR-006, AC-005, AC-006 | TASK-003, TASK-004 | TEST-005, TEST-006 | planned |
| TASK-006 | `validate_docs.py --graph`: global uniqueness, statuses, front-matter, dangling references; existing tests stay green | FR-005, FR-006, AC-005, AC-006 | TASK-005 | TEST-005, TEST-006 | planned |
| TASK-007 | `migrate_frontmatter.py` with `--check`; migrate the CraftRail repo and templates; golden diffs | FR-003, AC-003 | TASK-003 | TEST-003 | planned |
| TASK-008 | `new_feature.py`: front-matter output, global requirement ID allocation, `--local-requirement-ids` | FR-007, AC-007 | TASK-005, TASK-007 | TEST-007 | planned |
| TASK-009 | Write `contracts/craftrail-graph.schema.json` final version; `links.py`; `graph.py` deterministic serializer; `export_graph.py --no-history`; golden export of fixture repo | FR-008, FR-009, FR-013, FR-014, AC-008, AC-009, AC-013, AC-014 | TASK-006 | TEST-008, TEST-009, TEST-013, TEST-014 | planned |
| TASK-010 | `tests/fixtures/make_fixture_repo.py`: deterministic Git histories (status transitions, renames, deletions, re-adds, rebase scenario, 2,000-item perf repo) | FR-010, FR-011 | TASK-009 | TEST-010 | planned |
| TASK-011 | `history.py`: event mining via `git log --name-status -M` + `git show`, author names only, cache in `.craftrail/cache/`, ancestry check | FR-010, FR-011, AC-010, AC-011 | TASK-010 | TEST-010, TEST-011 | planned |
| TASK-012 | `metrics.py`: all metrics in the spec table, partial flags; `expected-metrics.json` hand-calculated fixture | FR-012, AC-012 | TASK-011 | TEST-012 | planned |
| TASK-013 | `config.py` + `.craftrail/studio.json` defaults and validation | FR-031, AC-030 | TASK-009 | TEST-030 | planned |
| TASK-014 | `context.py` + `context_pack.py`; golden packs; shared fixtures for TS parity | FR-028, AC-027 | TASK-009 | TEST-027 | planned |
| TASK-015 | Export benchmark job against the perf fixture; meet `NFR-002` | NFR-002, AC-031 | TASK-012 | TEST-031 | planned |
| TASK-016 | Scaffold `studio/` (Vite, React, TS strict, Biome, Vitest, Playwright, pnpm lock), generated types from schema with staleness check, CI job | CON-003, NFR-007 | TASK-009 | TEST-031 | planned |
| TASK-017 | `studio_server.py` read-only endpoints (`/`, `/api/health`, `/api/graph`, `/api/file` GET) with token, Host/Origin checks | FR-023, AC-022 | TASK-009 | TEST-022 | planned |
| TASK-018 | App shell: data loading (static file or `/api/graph`), freshness banner, diagnostics panel, hash routing, URL state, global search | FR-021, AC-017 | TASK-016, TASK-017 | TEST-017 | planned |
| TASK-019 | Overview view | FR-015, AC-015 | TASK-018 | TEST-015 | planned |
| TASK-020 | Boards view with column mapping, filters, swimlanes, keyboard "Move to…" (read-only until TASK-025) | FR-017, AC-017, AC-030 | TASK-018, TASK-013 | TEST-017, TEST-030 | planned |
| TASK-021 | Traceability graph (React Flow + dagre, clustering above 5,000 nodes) and matrix with gap highlighting | FR-016, AC-016 | TASK-018 | TEST-016 | planned |
| TASK-022 | Item detail drawer: metadata, sanitised excerpt, links, source link, history timeline | FR-018, AC-018 | TASK-018 | TEST-018 | planned |
| TASK-023 | Metrics view (uPlot) with definitions, partial notices and data-table fallbacks | FR-019, BR-002, AC-019 | TASK-018, TASK-012 | TEST-019 | planned |
| TASK-024 | Decisions view with supersession chains | FR-020, AC-020 | TASK-018 | TEST-020 | planned |
| TASK-025 | TS patch engine (front-matter, tables, declarations, all ops in `FR-022`), 100% branch coverage, cross-language contract tests | FR-022, AC-021 | TASK-016, TASK-014 | TEST-021 | planned |
| TASK-026 | Client-side validation (Ajv + graph rules) and change queue with diff preview | FR-025, FR-027, AC-025 | TASK-025 | TEST-025 | planned |
| TASK-027 | `studio_server.py` `PUT /api/file` (atomic, newline-preserving, globs, symlinks, size); local backend; conflict view | FR-023, FR-026, BR-003, AC-022, AC-024 | TASK-026, TASK-017 | TEST-022, TEST-024 | planned |
| TASK-028 | Approval guard (typed confirmation, `approved_by`/`approved_on`, no bulk approve, PR-only in GitHub mode) | BR-001, AC-026 | TASK-027 | TEST-026 | planned |
| TASK-029 | Enable editing in Boards, Item detail, create feature/ADR/item flows | FR-022, AC-021 | TASK-027 | TEST-021 | planned |
| TASK-030 | GitHub backend (PAT entry, Git Data API single commit, branch naming, PR body, error handling) with MSW tests | FR-024, FR-026, AC-023, AC-024 | TASK-026, TASK-028 | TEST-023, TEST-024 | planned |
| TASK-031 | TS context pack parity + Copy prompt menu with workflow prompts; network assertion in e2e | FR-029, NFR-005, AC-027, AC-028 | TASK-022, TASK-014 | TEST-027, TEST-028 | planned |
| TASK-032 | Accessibility pass: axe on every view, keyboard-only journey, chart tables | NFR-004, AC-031 | TASK-019, TASK-020, TASK-021, TASK-022, TASK-023, TASK-024 | TEST-031 | planned |
| TASK-033 | `studio.yml` workflow template, base-path build, CSP meta, bundle budget check; scratch-repo run | FR-030, NFR-003, NFR-006, CON-002, AC-029 | TASK-029 | TEST-029, TEST-031 | planned |
| TASK-034 | Docs: `docs/framework/studio.md`, updates to concepts/validation/spec guide, nav, CHANGELOG; release asset packaging | FR-030 | TASK-033 | TEST-031 review | planned |
| TASK-035 | Converge: update spec/plan/verification with evidence and deviations; set feature status per owner decision | — | TASK-034 | TEST-031 | planned |
