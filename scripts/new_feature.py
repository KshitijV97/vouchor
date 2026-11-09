#!/usr/bin/env python3
"""Create a numbered feature folder from the CraftRail templates."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "specs"
TEMPLATE = ROOT / "templates" / "feature"
CORE_FILES = ("spec.md", "plan.md", "tasks.md", "verification.md")


def slugify(title: str) -> str:
    """Convert a title to a conservative, filesystem-safe ASCII slug."""
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return slug[:64].rstrip("-")


def next_feature_number(specs_dir: Path = SPECS) -> int:
    numbers = []
    if specs_dir.exists():
        for child in specs_dir.iterdir():
            match = re.match(r"^(\d{3,})-", child.name)
            if child.is_dir() and match:
                numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def create_feature(title: str, root: Path = ROOT, today: date | None = None) -> Path:
    slug = slugify(title)
    if not slug:
        raise ValueError("title must contain at least one ASCII letter or digit")
    specs = root / "specs"
    template = root / "templates" / "feature"
    missing = [str(template / name) for name in CORE_FILES if not (template / name).is_file()]
    if missing:
        raise FileNotFoundError("missing feature template(s): " + ", ".join(missing))
    number = next_feature_number(specs)
    feature_id = f"{number:03d}"
    target = specs / f"{feature_id}-{slug}"
    if target.exists():
        raise FileExistsError(f"refusing to overwrite existing feature directory: {target}")
    specs.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, target)
    date_text = (today or date.today()).isoformat()
    for path in target.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".mmd"}:
            content = path.read_text(encoding="utf-8")
            content = content.replace("NNN", feature_id).replace("[Feature title]", title)
            content = content.replace("YYYY-MM-DD", date_text)
            path.write_text(content, encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="human-readable feature title")
    args = parser.parse_args(argv)
    try:
        target = create_feature(args.title)
    except (ValueError, FileExistsError, FileNotFoundError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Created {target.relative_to(ROOT)}")
    print("Next: edit the spec, resolve questions, get approval, then plan and task the work.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
