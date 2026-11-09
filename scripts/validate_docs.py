#!/usr/bin/env python3
"""Validate CraftRail document structure and selected syntax (not semantics)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
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
    "scripts/new_feature.py",
    "scripts/validate_docs.py",
    "scripts/__init__.py",
    "tests",
    "pyproject.toml",
    "requirements-dev.txt",
    "requirements-docs.txt",
    "zensical.toml",
    "vercel.json",
    ".pre-commit-config.yaml",
    ".github/workflows/quality.yml",
    ".github/workflows/release.yml",
    ".github/release.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
)
ID_RE = re.compile(r"\b(?:BR|FR|NFR|CON|US|AC|ADR|TASK|TEST)-\d{3,}\b")
SHORT_ID_RE = re.compile(r"\b(?:BR|FR|NFR|CON|US|AC|ADR|TASK|TEST)-(\d{1,2})\b")
MERMAID_DECLARATIONS = (
    "flowchart",
    "graph",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram",
    "stateDiagram-v2",
    "erDiagram",
    "journey",
    "mindmap",
    "timeline",
    "C4Context",
    "C4Container",
    "C4Component",
)
PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}|<PLACEHOLDER(?:\s+[^>]*)?>|\[TODO:[^\]]*\]", re.I)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: Path | str, message: str, line: int | None = None) -> None:
        self.errors.append(f"{path}{':' + str(line) if line else ''}: error: {message}")

    def warning(self, path: Path | str, message: str, line: int | None = None) -> None:
        self.warnings.append(f"{path}{':' + str(line) if line else ''}: warning: {message}")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def markdown_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)


def mermaid_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.mmd") if ".git" not in p.parts)


def without_fences(text: str) -> str:
    return re.sub(r"(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$", "", text)


def check_fences(path: Path, text: str, report: Report, root: Path) -> None:
    opener: tuple[str, int] | None = None
    for line_no, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if not match:
            continue
        marker = match.group(1)[0]
        size = len(match.group(1))
        if opener is None:
            opener = (marker, line_no)
        elif opener[0] == marker and size >= 3:
            opener = None
    if opener:
        report.error(
            rel(path, root), f"unclosed fenced code block opened with {opener[0] * 3}", opener[1]
        )


def check_mermaid(path: Path, text: str, report: Report, root: Path) -> None:
    if path.suffix == ".mmd":
        body = text.strip()
        if not body:
            report.error(rel(path, root), "empty Mermaid source")
        else:
            first = body.splitlines()[0].strip()
            if not any(first.startswith(decl) for decl in MERMAID_DECLARATIONS):
                report.error(rel(path, root), f"unrecognized Mermaid declaration: {first!r}", 1)
    for match in re.finditer(r"(?ms)^\s*```mermaid\s*\n(.*?)^\s*```\s*$", text, re.I):
        body = match.group(1).strip()
        line = text.count("\n", 0, match.start()) + 1
        if not body:
            report.error(rel(path, root), "empty Mermaid block", line)
            continue
        first = body.splitlines()[0].strip()
        if not any(first.startswith(decl) for decl in MERMAID_DECLARATIONS):
            report.error(rel(path, root), f"unrecognized Mermaid declaration: {first!r}", line)


def check_links(path: Path, text: str, report: Report, root: Path) -> None:
    clean = without_fences(text)
    for match in re.finditer(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", clean):
        target = match.group(1).strip().split()[0].strip("<>")
        if not target or target.startswith(("https://", "http://", "mailto:", "data:")):
            continue
        if target.startswith("#"):
            continue
        target_path = target.split("#", 1)[0]
        if not target_path:
            continue
        resolved = (path.parent / target_path).resolve()
        line = clean.count("\n", 0, match.start()) + 1
        if not resolved.exists():
            report.error(rel(path, root), f"broken local Markdown link: {target}", line)


def is_exempt(path: Path, root: Path) -> bool:
    relative = path.relative_to(root).as_posix()
    return relative.startswith(
        ("templates/", "docs/project/", "docs/examples/", "specs/000-example-feature/")
    )


def check_ids(root: Path, report: Report) -> None:
    # Count only requirement bullets or table rows with the ID in the first cell.
    declaration = re.compile(
        r"^\s*(?:[-*]\s+`?(BR|FR|NFR|CON|US|AC|ADR|TASK|TEST)-\d{3,}`?\s*:|\|\s*`?(BR|FR|NFR|CON|US|AC|ADR|TASK|TEST)-\d{3,}`?\s*\|)"
    )
    for path in markdown_files(root):
        if is_exempt(path, root):
            continue
        seen: dict[str, int] = {}
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = declaration.match(line)
            if not match:
                continue
            found = ID_RE.search(line)
            if not found:
                continue
            item = found.group(0)
            if item in seen:
                report.error(
                    rel(path, root),
                    f"duplicate declared ID {item} (first declared on line {seen[item]})",
                    line_no,
                )
            else:
                seen[item] = line_no


def validate(root: Path = ROOT) -> Report:
    report = Report()
    for item in REQUIRED_PATHS:
        if not (root / item).exists():
            report.error(item, "required baseline path is missing")

    for path in sorted([*markdown_files(root), *mermaid_files(root)]):
        text = path.read_text(encoding="utf-8")
        check_fences(path, text, report, root)
        check_mermaid(path, text, report, root)
        check_links(path, text, report, root)
        if not is_exempt(path, root):
            for match in PLACEHOLDER_RE.finditer(without_fences(text)):
                line = text.count("\n", 0, match.start()) + 1
                report.error(rel(path, root), f"unresolved placeholder {match.group(0)}", line)
            for match in SHORT_ID_RE.finditer(without_fences(text)):
                line = text.count("\n", 0, match.start()) + 1
                report.error(
                    rel(path, root),
                    f"ID does not use at least three digits: {match.group(0)}",
                    line,
                )

    check_ids(root, report)

    for path in (
        sorted((root / "specs").glob("[0-9][0-9][0-9]-*")) if (root / "specs").exists() else []
    ):
        if not path.is_dir() or path.name.startswith("000-example-"):
            continue
        for filename in ("spec.md", "plan.md", "tasks.md", "verification.md"):
            if not (path / filename).is_file():
                report.error(rel(path, root), f"feature is missing {filename}")
        spec_path = path / "spec.md"
        if spec_path.exists():
            spec = spec_path.read_text(encoding="utf-8")
            status = re.search(r"(?m)^-\s*\*\*Status:\*\*\s*([a-z-]+)\s*$", spec)
            if not status:
                report.error(
                    rel(spec_path, root), "feature metadata must include a supported Status"
                )
            elif status.group(1) not in {
                "draft",
                "proposed",
                "approved",
                "in-progress",
                "verified",
                "deferred",
                "deprecated",
            }:
                report.error(
                    rel(spec_path, root), f"unsupported feature status {status.group(1)!r}"
                )

    json_files = sorted(root.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            report.error(rel(path, root), f"invalid JSON: {exc}", getattr(exc, "lineno", None))

    # OpenAPI semantics are outside this standard-library validator's scope.
    report.warning(
        "docs/project/contracts/openapi.yaml",
        "OpenAPI semantics are not validated by the dependency-free core tool",
    )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict", action="store_true", help="also return failure when warnings are present"
    )
    args = parser.parse_args(argv)
    report = validate()
    for item in report.errors:
        print(item, file=sys.stderr)
    for item in report.warnings:
        print(item, file=sys.stderr)
    if not report.errors:
        print("Documentation validation passed (structural checks only).")
    print(f"{len(report.errors)} error(s), {len(report.warnings)} warning(s).")
    return 1 if report.errors or (args.strict and report.warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
