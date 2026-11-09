# Non-functional requirements

| ID | Quality attribute / constraint | Measure or evaluation method | Scope | Status |
|---|---|---|---|---|
| NFR-001 | Offline testability: the unit suite MUST run with no network and no LLM; integration suites MUST need only local containers. | CI job with network disabled for unit tests; deterministic fake LLM fixture | Whole repo | proposed |
| NFR-002 | Static typing: `mypy --strict` MUST pass on `src/` and `tests/`. | Pre-commit + CI | Python code | proposed |
| NFR-003 | Coverage: ≥ 90% combined line+branch overall; 100% branch coverage on `contracts`, `ledger` and `executor` modules. | `pytest --cov` thresholds in CI | Python code | proposed |
| NFR-004 | Exactly-once effect: across the fault-injection matrix (crash before send, timeout after accept, crash after send before ledger write, concurrent retries), duplicate side effects MUST be 0. | Fault-injection integration suite | Executor + connectors | proposed |
| NFR-005 | Unit suite runtime < 30 s; full local integration suite < 10 min on a 4-core laptop. | CI timing report | Tests | proposed |
| NFR-006 | Durability: a suspended thread MUST resume correctly after API/worker restart and after a Postgres failover. | Integration test (restart); CNPG failover drill (Phase 7) | Runtime | proposed |
| NFR-007 | Security: containers run as non-root with read-only root filesystem; images scanned with zero unwaived critical CVEs; secrets never in images, logs or Git. | Trivy + gitleaks in CI; Helm policy tests | Images, chart | proposed |
| NFR-008 | Observability: every node transition and tool call emits structured logs and OpenTelemetry traces carrying `thread_id` and `idempotency_key`. | Integration test asserts spans | Runtime | proposed |
| NFR-009 | Portability: the same OCI images and Helm chart MUST deploy to a local kind cluster and to any CNCF-conformant Kubernetes; no cloud-proprietary managed service is required. | CI deploy to kind; manual cloud deploy per release | Deployment | proposed |
| NFR-010 | Local developer experience: a fresh clone reaches a running stack with one documented command after installing Docker and uv. | Fresh-clone check in CI | Repo | proposed |
| NFR-011 | Documentation: each phase MUST update Tier 1, Tier 2 and Tier 3 docs as defined in the [documentation strategy](../documentation-strategy.md); the docs site MUST build in strict mode. | Phase exit gate; CI site build | Docs | proposed |
| NFR-012 | Reproducibility: all dependencies and container images pinned (lockfile, image digests or exact tags); no `latest` tags. | Lint rule + review | Repo | proposed |
