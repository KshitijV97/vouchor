# Documentation validation

Run from any working directory:

```bash
python3 scripts/validate_docs.py
python3 scripts/validate_docs.py --strict
```

The script resolves its repository root from its own file path. It uses only the Python standard library and makes no network requests.

## Checks

- Required root files and baseline directories exist.
- Markdown fences balance; recognized Mermaid fences and `.mmd` files are non-empty and begin with a known diagram declaration.
- Common double-brace tokens, angle-bracket placeholder markers, and explicit TODO labels do not appear in non-template/non-example Markdown.
- Declared requirement/task/verification IDs with supported prefixes have at least three digits and are not duplicated within the same Markdown document's declarations.
- Numbered feature directories contain `spec.md`, `plan.md`, `tasks.md`, and `verification.md`; the spec has a supported status.
- Inline relative Markdown links resolve to an existing local path.
- `.json` files parse as JSON.

The validator reports errors and warnings separately. It does not assess whether requirements are correct, complete, secure, or semantically consistent. It checks that Mermaid source starts with a recognized diagram declaration, but does not render diagrams or verify their architecture against code. Markdown links using reference definitions and fragment anchor existence are not checked. JSON Schema files are checked for JSON syntax, not against the JSON Schema meta-schema. The dependency-free core validator does not parse OpenAPI YAML or validate OpenAPI semantics, so it reports a warning. The separate pre-commit `check-yaml` hook checks YAML syntax in local hooks and CI.

`--strict` returns a failing exit status if either an error or warning is reported. Therefore, with the current OpenAPI semantics warning, ordinary validation passes and strict validation returns status 1 until semantic OpenAPI validation is added or the warning is otherwise resolved. The Zensical site build itself uses strict mode for website navigation and configuration errors.

For Python formatting, lint, strict type checks, branch coverage, pre-commit hooks, CI, and release tags, see the [Python quality guide](python-quality.md).
