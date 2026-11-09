from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path
from unittest.mock import patch

from scripts.new_feature import (
    ROOT as FEATURE_ROOT,
)
from scripts.new_feature import (
    create_feature,
    next_feature_number,
    slugify,
)
from scripts.new_feature import (
    main as new_feature_main,
)
from scripts.validate_docs import Report, validate
from scripts.validate_docs import main as validator_main


class NewFeatureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "specs").mkdir()
        template = self.root / "templates" / "feature"
        (template / "diagrams").mkdir(parents=True)
        for name in ("spec.md", "plan.md", "tasks.md", "verification.md"):
            (template / name).write_text(
                "# Feature NNN: [Feature title]\nCreated YYYY-MM-DD\nFR-NNN\n"
            )
        (template / "diagrams" / "sequence.mmd").write_text("sequenceDiagram\n    title NNN\n")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_slug_normalization(self) -> None:
        self.assertEqual(slugify("Café & User Authentication!"), "cafe-user-authentication")
        self.assertEqual(slugify("!!!"), "")
        self.assertLessEqual(len(slugify("feature " * 30)), 64)

    def test_next_id_selection(self) -> None:
        (self.root / "specs" / "003-old").mkdir()
        (self.root / "specs" / "010-later").mkdir()
        self.assertEqual(next_feature_number(self.root / "specs"), 11)
        self.assertEqual(next_feature_number(self.root / "not-created"), 1)

    def test_creates_from_templates_with_metadata(self) -> None:
        target = create_feature("User Authentication", self.root, date(2026, 1, 2))
        self.assertEqual(target.name, "001-user-authentication")
        spec = (target / "spec.md").read_text()
        self.assertIn("Feature 001: User Authentication", spec)
        self.assertIn("2026-01-02", spec)
        self.assertIn("FR-001", spec)
        self.assertTrue((target / "diagrams" / "sequence.mmd").exists())

    def test_refuses_duplicate_directory(self) -> None:
        target = self.root / "specs" / "001-user-authentication"
        target.mkdir()
        sentinel = target / "keep.txt"
        sentinel.write_text("preserve")
        with (
            patch("scripts.new_feature.next_feature_number", return_value=1),
            self.assertRaises(FileExistsError),
        ):
            create_feature("User Authentication", self.root)
        self.assertEqual(sentinel.read_text(), "preserve")

    def test_rejects_title_without_ascii_letters_or_digits(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one ASCII"):
            create_feature("!!!", self.root)

    def test_reports_missing_template(self) -> None:
        (self.root / "templates" / "feature" / "plan.md").unlink()
        with self.assertRaisesRegex(FileNotFoundError, "plan.md"):
            create_feature("Missing template", self.root)

    def test_cli_success_and_failure(self) -> None:
        output = io.StringIO()
        target = FEATURE_ROOT / "specs" / "001-test"
        with (
            patch("scripts.new_feature.create_feature", return_value=target),
            redirect_stdout(output),
        ):
            self.assertEqual(new_feature_main(["A feature"]), 0)
        self.assertIn("Created", output.getvalue())

        errors = io.StringIO()
        with (
            patch("scripts.new_feature.create_feature", side_effect=ValueError("bad title")),
            redirect_stderr(errors),
        ):
            self.assertEqual(new_feature_main(["!!!"]), 2)
        self.assertIn("bad title", errors.getvalue())


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for required in (
            "README.md",
            "AGENTS.md",
            "CLAUDE.md",
            "LICENSE",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "SUPPORT.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "docs/framework",
            "docs/framework/python-quality.md",
            "docs/project",
            "specs",
            "templates",
            "scripts",
            "tests",
            ".github/workflows",
            ".pre-commit-config.yaml",
            "pyproject.toml",
            "requirements-dev.txt",
            "requirements-docs.txt",
            "zensical.toml",
            "vercel.json",
        ):
            path = self.root / required
            if "." in path.name and not path.suffix or path.suffix:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}" if path.suffix == ".json" else "stub")
            else:
                path.mkdir(parents=True, exist_ok=True)
        for required in (
            "scripts/new_feature.py",
            "scripts/validate_docs.py",
            "scripts/__init__.py",
            ".github/workflows/quality.yml",
            ".github/workflows/release.yml",
            ".github/release.yml",
            ".github/PULL_REQUEST_TEMPLATE.md",
        ):
            path = self.root / required
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("stub")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_detects_unbalanced_markdown_fence(self) -> None:
        (self.root / "README.md").write_text("# Test\n```python\nprint('x')\n")
        self.assertTrue(any("unclosed fenced" in item for item in validate(self.root).errors))

    def test_detects_mismatched_fence_markers(self) -> None:
        (self.root / "README.md").write_text("```python\ncode\n~~~\n")
        self.assertTrue(any("unclosed fenced" in item for item in validate(self.root).errors))

    def test_accepts_tilde_fences_and_ignores_links_inside_fences(self) -> None:
        (self.root / "README.md").write_text("~~~md\n[ignored](missing.md)\n~~~\n")
        self.assertFalse(validate(self.root).errors)

    def test_detects_duplicate_requirement_declarations(self) -> None:
        (self.root / "README.md").write_text("| FR-001 | first |\n| FR-001 | duplicate |\n")
        self.assertTrue(
            any("duplicate declared ID FR-001" in item for item in validate(self.root).errors)
        )

    def test_ignores_duplicate_ids_in_exempt_template_files(self) -> None:
        template = self.root / "templates" / "requirements.md"
        template.parent.mkdir(parents=True, exist_ok=True)
        template.write_text("| FR-001 | one |\n| FR-001 | two |\n")
        self.assertFalse(validate(self.root).errors)

    def test_detects_short_requirement_id(self) -> None:
        (self.root / "README.md").write_text("A requirement is FR-01.\n")
        self.assertTrue(any("at least three digits" in item for item in validate(self.root).errors))

    def test_detects_unresolved_placeholder(self) -> None:
        (self.root / "README.md").write_text("Value is {{TODO}}.\n")
        self.assertTrue(
            any("unresolved placeholder" in item for item in validate(self.root).errors)
        )

    def test_ignores_placeholders_inside_code_fences(self) -> None:
        (self.root / "README.md").write_text("```text\n{{example}}\n```\n")
        self.assertFalse(validate(self.root).errors)

    def test_detects_empty_and_invalid_mermaid(self) -> None:
        (self.root / "README.md").write_text("```mermaid\n```\n\n```mermaid\nnotADiagram\n```\n")
        errors = validate(self.root).errors
        self.assertTrue(any("empty Mermaid" in item for item in errors))
        self.assertTrue(any("unrecognized Mermaid" in item for item in errors))

    def test_checks_standalone_mermaid_files(self) -> None:
        (self.root / "diagram.mmd").write_text("not a diagram\n")
        self.assertTrue(
            any("unrecognized Mermaid declaration" in item for item in validate(self.root).errors)
        )

    def test_accepts_standalone_mermaid_diagram(self) -> None:
        (self.root / "diagram.mmd").write_text("flowchart LR\n  A --> B\n")
        self.assertFalse(validate(self.root).errors)

    def test_detects_broken_internal_markdown_link(self) -> None:
        (self.root / "README.md").write_text("[missing](no-such-file.md)\n")
        self.assertTrue(
            any("broken local Markdown link" in item for item in validate(self.root).errors)
        )

    def test_valid_and_invalid_json(self) -> None:
        (self.root / "valid.json").write_text('{"ok": true}')
        (self.root / "invalid.json").write_text('{"broken": }')
        errors = validate(self.root).errors
        self.assertTrue(any("invalid JSON" in item and "invalid.json" in item for item in errors))
        self.assertFalse(any(item.split(":", 1)[0].endswith("/valid.json") for item in errors))

    def test_accepts_external_and_fragment_links(self) -> None:
        (self.root / "README.md").write_text(
            "[web](https://example.com) [email](mailto:team@example.com) [section](#details)\n"
        )
        self.assertFalse(validate(self.root).errors)

    def test_checks_feature_files_and_status(self) -> None:
        feature = self.root / "specs" / "001-example"
        feature.mkdir()
        (feature / "spec.md").write_text("# Example\n- **Status:** unknown\n")
        errors = validate(self.root).errors
        self.assertTrue(any("missing plan.md" in item for item in errors))
        self.assertTrue(any("unsupported feature status" in item for item in errors))

    def test_detects_missing_path_and_spec_status(self) -> None:
        (self.root / "README.md").unlink()
        feature = self.root / "specs" / "003-no-status"
        feature.mkdir()
        (feature / "spec.md").write_text("# Example\n")
        errors = validate(self.root).errors
        self.assertTrue(
            any("README.md: error: required baseline path is missing" in item for item in errors)
        )
        self.assertTrue(any("must include a supported Status" in item for item in errors))

    def test_accepts_complete_feature_with_supported_status(self) -> None:
        feature = self.root / "specs" / "002-example"
        feature.mkdir()
        (feature / "spec.md").write_text("# Example\n- **Status:** approved\n")
        for filename in ("plan.md", "tasks.md", "verification.md"):
            (feature / filename).write_text("# Complete\n")
        self.assertFalse(validate(self.root).errors)

    def test_validator_cli_warning_and_strict_exit(self) -> None:
        report = Report()
        report.warning("sample.md", "warning")
        output = io.StringIO()
        errors = io.StringIO()
        with (
            patch("scripts.validate_docs.validate", return_value=report),
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            self.assertEqual(validator_main([]), 0)
            self.assertEqual(validator_main(["--strict"]), 1)
        self.assertIn("1 warning(s)", output.getvalue())
        self.assertIn("warning", errors.getvalue())

    def test_validator_cli_error_exit(self) -> None:
        report = Report()
        report.error("sample.md", "bad")
        with (
            patch("scripts.validate_docs.validate", return_value=report),
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()),
        ):
            self.assertEqual(validator_main([]), 1)


if __name__ == "__main__":
    unittest.main()
