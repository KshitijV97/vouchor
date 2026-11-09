# ADR-002: Python toolchain and quality gates

- **Status:** proposed
- **Date:** 2026-11-09
- **Decision owner:** Maintainer (STK-001)
- **Related:** `NFR-001`–`NFR-003`, `NFR-007`, `NFR-012`, [CraftRail Python quality guide](../../framework/python-quality.md)

## Context and forces

The owner wants everything linted, pre-commit hooks, and unit plus integration tests. The blueprint mandates Python 3.12, `uv`, `mypy --strict`, async-native code, and offline tests. CraftRail already ships Ruff, Mypy, pytest-cov, pre-commit and actionlint for its scripts.

## Decision

| Concern | Tool | Notes |
|---|---|---|
| Python / deps | **uv** (lockfile `uv.lock`), Python 3.12 | Workspace members not needed; single package `vouchor` in `src/vouchor/` |
| Task runner | **Makefile** | Zero-install on macOS/Linux; each target wraps a `uv run` command |
| Lint + format | **Ruff** (rules `E,F,I,B,UP,SIM,S,ASYNC,PT,RUF,N,ANN,TID`) | `S` replaces Bandit; `ASYNC` enforces `CON-002` |
| Types | **mypy --strict** + Pydantic plugin | `src/` and `tests/` |
| Architecture rules | **import-linter** | Enforces dependency rule in [components](../architecture/components.md) |
| Unit tests | **pytest**, pytest-asyncio, **Hypothesis**, respx, time-machine | Network disabled with `pytest-socket` for the unit marker |
| Integration tests | **testcontainers-python** (pgvector, Valkey, Mailpit), FastMCP in-memory transport, Playwright | Hermetic per session; same containers in CI |
| API contract tests | **Schemathesis** against generated OpenAPI; OpenAPI snapshot diff | Contract committed in `docs/project/contracts/openapi.yaml` |
| E2E / acceptance | pytest marker `e2e` against `docker compose` stack | Blueprint scenario tests (7 vendors) |
| Mutation testing | **mutmut** on `core/` and `nodes/executor.py` | Nightly CI, not pre-commit |
| Coverage | pytest-cov, thresholds per `NFR-003` | |
| SQL | **sqlfluff** (postgres dialect) | Lints migrations |
| Containers | **hadolint**, **Trivy** (image + config), **Syft** SBOM | |
| IaC / K8s | `tofu fmt/validate`, **TFLint**, `helm lint`, **kubeconform**, chart-testing (`ct`) | |
| Shell / YAML / Markdown | shellcheck, yamllint, CraftRail `validate_docs.py` | |
| Secrets | **gitleaks** | pre-commit + CI |
| Commits | Conventional Commits via **commitizen** (commit-msg hook) | Feeds CHANGELOG |
| Dependency updates | **Renovate** (self-hostable, FOSS) | Pins image digests too |
| Licence check | **pip-licenses** allow-list in CI | `CON-001` |

Pre-commit runs fast checks only (Ruff, mypy, unit tests, linters, gitleaks, validator). Integration, e2e, Helm-on-kind and mutation suites run in CI and via `make` locally.

## Alternatives considered

- Poetry: slower, no Python version management. `just`: nicer but another install. Bandit standalone: redundant with Ruff `S`. Compose-based integration tests: less hermetic than testcontainers; kept for e2e only.

## Consequences

- Positive: one command per gate (`make check`, `make test-integration`, `make e2e`); identical locally and in CI.
- Negative / risks: large hook set slows commits — mitigated by keeping slow suites out of pre-commit.

## Supersedes / superseded by

None.
