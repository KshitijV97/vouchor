# Contributing to Vouchor

Thanks for your interest. Vouchor follows the [CraftRail](docs/framework/workflow.md) workflow: changes that affect behaviour start from an approved feature spec under `specs/`. Read the [implementation plan](docs/project/implementation-plan.md) to see which phase is active.

## Licence and sign-off

Vouchor is licensed under [AGPL-3.0-or-later](LICENSE) ([ADR-009](docs/project/decisions/ADR-009-license-agpl-3-0-or-later.md)). Contributions are accepted under the same licence (inbound = outbound). Every commit must carry a [Developer Certificate of Origin](https://developercertificate.org/) sign-off:

```bash
git commit -s -m "feat(executor): reclaim stale leases with read-back first"
```

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/).

## Development

Until Phase 0 lands, the only code is CraftRail's documentation tooling:

```bash
python3 -m venv .venv-dev
source .venv-dev/bin/activate
python -m pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
```

From Phase 0 onward the toolchain moves to `uv` and `make` ([ADR-002](docs/project/decisions/ADR-002-python-toolchain-and-quality-gates.md)): `make setup`, `make check`, `make test-integration`, `make e2e`, `make k8s-test`, `make docs`.

## Pull requests

Include the problem, the linked spec/requirement IDs, exact validation commands and results, and documentation impact across all three tiers ([documentation strategy](docs/project/documentation-strategy.md)). Do not claim a check passed unless you ran it.

By participating, contributors agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md). See [support](SUPPORT.md) for questions and [security](SECURITY.md) for vulnerability reports.
