# Python quality checks

CraftRail's core scripts and tests keep their runtime dependency footprint small, while the repository applies a stronger development-only quality toolchain. Contributors install these checks in an isolated environment; projects that copy CraftRail's templates do not inherit them as application dependencies.

## What is checked

| Check | Tool | Purpose | Limit |
|---|---|---|---|
| Types | Mypy strict mode | Check all functions and test code have consistent static types | Python remains dynamically typed; external/runtime behavior can still violate annotations |
| Lint and format | Ruff | Catch common code errors, import issues, selected bug patterns, and formatting drift | Style/lint rules are not a proof of correctness |
| Workflow lint | actionlint | Check GitHub Actions workflow syntax, expressions, action inputs, and selected security hazards | It does not execute a workflow or prove the hosted environment behaves as expected |
| Tests | pytest running `unittest` tests | Run focused tests with readable diagnostics | Tests only cover behavior we wrote assertions for |
| Coverage | pytest-cov + coverage.py | Enforce at least 90% combined statement/branch coverage of `scripts/` | Coverage shows executed lines and branches; it does not measure test quality |
| Commit hooks | pre-commit | Run format, lint, type, structure, and test checks before a local commit | Hooks can be skipped with Git flags and are not the security boundary |
| CI | GitHub Actions | Re-run checks on pushes and pull requests on hosted runners | It does not decide whether a change is acceptable or deploy the docs site |

The 90% threshold is deliberately scoped to the two small, maintained scripts, not Markdown files, generated HTML, or Python's standard library. Current tests exercise the initializer and validator across success/failure behavior, path handling, malformed inputs, Markdown/YAML-independent syntax checks, and CLI exit outcomes. Coverage is a floor, not a claim that every possible input or integration has been tested.

## Install the developer toolchain

The core scripts run on Python 3.10 or newer using only its standard library. Use Python 3.12 or newer for the full developer environment; the pinned current `pre-commit` release requires Python 3.11 or newer.

```bash
python3 -m venv .venv-dev
source .venv-dev/bin/activate
python -m pip install -r requirements-dev.txt
pre-commit install
```

`requirements-dev.txt` pins tool versions to keep local results aligned with CI. Upgrade those pins intentionally and run the full suite before committing the upgrade. The documentation site has its own dependency in `requirements-docs.txt`, installed separately in an isolated environment.

## Run the checks directly

```bash
ruff check scripts tests
ruff format --check scripts tests
mypy --strict scripts tests
pytest
python scripts/validate_docs.py
pre-commit run --all-files
```

`pytest` runs the `unittest.TestCase` suite and applies branch coverage settings from `pyproject.toml`. The repository continues to use the standard-library `unittest` runner in its Python-version compatibility matrix, so the core tests can also run without installing pytest:

```bash
python -m unittest discover -s tests -v
```

`pre-commit run --all-files` is the single command for the complete local hook set. It creates pinned isolated environments for Ruff, YAML/JSON hooks, and actionlint; the mypy, validator, and pytest hooks use your installed developer environment. `pre-commit install` wires those checks into future local commits; it does not install tools itself, so install `requirements-dev.txt` first.

## What “type safe” means here

Both scripts and tests are checked by Mypy with strict mode enabled, and every project function is annotated. This catches many incompatible calls, missing annotations, and incorrect assumptions before runtime. Type hints are not runtime validation: JSON, Markdown, filesystem state, user input, and operating-system errors still need validation and tests. Do not use `Any`, broad ignores, or casts to silence a real uncertainty without explaining why.

## Continuous integration and delivery

GitHub Actions runs standard-library tests on Python 3.10, 3.12, and 3.14; runs the Ruff, Mypy, pytest/coverage, pre-commit, and documentation validator checks; and builds the static documentation site with Zensical in strict mode. A failing job blocks a green CI result. Repository branch protection must be configured separately if merges should require those checks.

There is no continuous deployment workflow. CraftRail is a repository template, not a runtime service, so deploying an application is out of scope. The docs site currently deploys to Vercel by a maintainer using the CLI; GitHub is not connected to the Vercel project. CI is useful for every change; CD is only needed when the team wants site publication automated. A future Vercel deploy workflow needs an authorized deployment credential or a working Vercel/GitHub integration and should run only after CI succeeds.

## Release tags and notes

CraftRail uses semantic version tags with a `v` prefix: `v0.1.0`, `v0.2.0`, `v1.0.0`; prereleases may use `v1.0.0-rc.1`. The maintainer updates `CHANGELOG.md` for the release and creates an annotated tag on the reviewed commit:

```bash
git tag -a v0.1.0 -m "CraftRail v0.1.0"
git push origin v0.1.0
```

Pushing a valid `v*` tag runs `.github/workflows/release.yml`. That workflow validates the semantic version, reruns the quality and documentation-site checks, and only after they pass uses GitHub CLI to create a GitHub Release with notes generated from the preceding release and merged pull requests. `.github/release.yml` groups those notes by pull-request labels. Add labels such as `feature`, `bug`, `documentation`, `breaking-change`, and `skip-changelog` to pull requests so generated notes remain useful. Review the generated release before sharing it.

Creating the annotated tag is a maintainer decision; GitHub Actions creates the Release page after the tag is pushed. The repository currently has no release tag. Do not create the first public release until the owner has reviewed the provisional license and recorded brand risk.
