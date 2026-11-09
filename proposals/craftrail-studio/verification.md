# Verification: NNN CraftRail Studio

Statuses: `planned`, `implemented`, `verified`, `blocked`, `waived`, `deprecated`.

Record exact command, environment (OS, Python/Node versions, browser), commit SHA, result and date in the evidence column when a check runs. Code generation alone is not evidence.

| Requirement | Acceptance criterion | Verification ID / method | Evidence or location | Status |
|---|---|---|---|---|
| FR-001 | AC-001 | TEST-001 automated: `python -m unittest tests.test_frontmatter -v` | not yet run | planned |
| FR-002 | AC-002 | TEST-002 automated: `python -m unittest tests.test_legacy_meta -v` | not yet run | planned |
| FR-003 | AC-003 | TEST-003 automated: `python -m unittest tests.test_migrate -v` + golden diff review | not yet run | planned |
| FR-004 | AC-004 | TEST-004 automated: `python -m unittest tests.test_tables -v` | not yet run | planned |
| FR-005 | AC-005 | TEST-005 automated: `python -m unittest tests.test_identity -v`; `python3 scripts/validate_docs.py --graph` on duplicate fixture exits 1 | not yet run | planned |
| FR-006 | AC-006 | TEST-006 automated: `python -m unittest tests.test_statuses -v` | not yet run | planned |
| FR-007 | AC-007 | TEST-007 automated: `python -m unittest tests.test_new_feature_ids -v` | not yet run | planned |
| FR-008 | AC-008 | TEST-008 automated: export fixture, validate against schema (jsonschema in dev env), compare golden | not yet run | planned |
| FR-009 | AC-009 | TEST-009 automated: `python -m unittest tests.test_links -v` | not yet run | planned |
| FR-010 | AC-010 | TEST-010 integration: `python -m unittest tests.test_history -v` (real git, fixed dates); grep output for `@` in author fields | not yet run | planned |
| FR-011 | AC-011 | TEST-011 integration: incremental parse-count and rebase rebuild tests | not yet run | planned |
| FR-012 | AC-012 | TEST-012 automated: `python -m unittest tests.test_metrics -v` vs `expected-metrics.json`; shallow-clone case | not yet run | planned |
| FR-013 | AC-013 | TEST-013 automated: malformed-file fixture, exit codes with and without `--strict` | not yet run | planned |
| FR-014 | AC-014 | TEST-014 automated: double export byte comparison; dirty flag | not yet run | planned |
| FR-015 | AC-015 | TEST-015 e2e: `pnpm -C studio test:e2e -- overview` | not yet run | planned |
| FR-016 | AC-016 | TEST-016 e2e: traceability graph and matrix gap fixtures | not yet run | planned |
| FR-017 | AC-017 | TEST-017 e2e: board filters, swimlanes, URL reload | not yet run | planned |
| FR-021 | AC-017 | TEST-017 e2e: shareable URL state and search | not yet run | planned |
| FR-018 | AC-018 | TEST-018 e2e: item detail links, source, timeline | not yet run | planned |
| FR-019 | AC-019 | TEST-019 e2e: metric values and definitions; partial notice | not yet run | planned |
| BR-002 | AC-019 | TEST-019 review: every coverage figure labelled "linked coverage" | not yet run | planned |
| FR-020 | AC-020 | TEST-020 e2e: supersession chain | not yet run | planned |
| FR-022 | AC-021 | TEST-021 automated: Vitest patch engine + cross-language contract suite | not yet run | planned |
| FR-023 | AC-022 | TEST-022 integration: `python -m unittest tests.test_server -v` (loopback, token, Origin, traversal, symlink, size) | not yet run | planned |
| BR-003 | AC-022 | TEST-022 integration: writes outside globs rejected | not yet run | planned |
| FR-024 | AC-023 | TEST-023 automated: Vitest + MSW GitHub backend; token storage assertions | not yet run | planned |
| FR-025 | AC-023 | TEST-023 automated: change queue batches edits into one commit | not yet run | planned |
| FR-026 | AC-024 | TEST-024 e2e: local and GitHub conflict flows | not yet run | planned |
| FR-027 | AC-025 | TEST-025 automated: validation blocks invalid saves | not yet run | planned |
| BR-001 | AC-026 | TEST-026 e2e: approval confirmation, recorded approver, PR-only, no bulk approve | not yet run | planned |
| FR-028 | AC-027 | TEST-027 automated: `python3 scripts/context_pack.py 003:TASK-002 --budget 4000` vs golden; Vitest parity | not yet run | planned |
| FR-029 | AC-028 | TEST-028 e2e: clipboard content; network log shows only app origin | not yet run | planned |
| NFR-005 | AC-028 | TEST-028 e2e: offline run with network blocked | not yet run | planned |
| FR-030 | AC-029 | TEST-029 manual+automated: run `studio.yml` in scratch repo; sub-path load with zero 404s | not yet run | planned |
| CON-002 | AC-029 | TEST-029 review: artifact contains only static files | not yet run | planned |
| FR-031 | AC-030 | TEST-030 e2e + unit: column remap; invalid config falls back with diagnostic | not yet run | planned |
| NFR-001 | AC-031 | TEST-031 CI: stdlib-only test matrix on all supported Python versions | not yet run | planned |
| NFR-002 | AC-031 | TEST-031 CI benchmark: cold < 15 s, incremental < 2 s on `ubuntu-latest` | not yet run | planned |
| NFR-003 | AC-031 | TEST-031 CI bundle check ≤ 350 KB gzip; manual 1,000-node fps recording | not yet run | planned |
| NFR-004 | AC-031 | TEST-031 CI axe (zero serious/critical) + keyboard-only e2e journey | not yet run | planned |
| NFR-006 | AC-029 | TEST-029 review: CSP meta present and restrictive in built `index.html` | not yet run | planned |
| NFR-007 | AC-031 | TEST-031 CI coverage thresholds (Python ≥ 90%, TS ≥ 85%, parsers/patch 100% branch) | not yet run | planned |
| NFR-008 | AC-031 | TEST-031 Playwright projects for Chromium, Firefox, WebKit; manual Edge smoke test | not yet run | planned |
| BR-004 | AC-031 | TEST-031 review: generated outputs ignored by Git | not yet run | planned |

Waivers require an accountable owner, rationale, and accepted risk. Code generation alone is not evidence.
