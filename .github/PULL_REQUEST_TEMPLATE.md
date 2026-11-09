## Summary

[What changed and why?]

## Validation

- [ ] `pre-commit run --all-files`
- [ ] `python -m unittest discover -s tests -v` on supported Python versions (when available)
- [ ] `python3 -m venv .venv-docs && .venv-docs/bin/pip install -r requirements-docs.txt && .venv-docs/bin/zensical build --clean --strict` (for documentation changes)
- [ ] Other checks (list exact commands and outcomes):

## Documentation impact

- [ ] Tier 1 (README / site home), Tier 2 (guide), Tier 3 (build journal / reference) updated where affected.

- [ ] Specs, templates, diagrams, contracts, and traceability are updated where needed.
- [ ] No documentation change is needed (explain why):

## Compatibility impact

- [ ] Core remains agent-neutral; provider integrations are optional.
- [ ] Shared instructions and adapters are consistent.
- [ ] Directly tested behavior is distinguished from documented compatibility.

## Licence

- [ ] All commits are signed off (DCO) and new dependencies are AGPL-3.0-compatible.

## Review notes

[Limitations, risks, owner decisions, or follow-up work]
