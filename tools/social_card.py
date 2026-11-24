"""Generate the 1200x630 link-preview image for the documentation site.

Maintainer tool, not part of the site build or any runtime. It needs Pillow
(HPND licence) and the Roboto font (Apache-2.0, the site's own typeface):

    python3 -m venv .venv-tools
    .venv-tools/bin/pip install -r tools/requirements-social-card.txt
    .venv-tools/bin/python tools/social_card.py --font-dir /path/to/roboto

The output is committed at docs/images/social-card.png and referenced by
overrides/main.html. Colours match docs/stylesheets/extra.css and the favicon.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630
BACKGROUND = "#132a3a"  # --md-primary-fg-color
PANEL = "#0b1b26"  # --md-primary-fg-color--dark
RAIL = "#68d6b0"  # favicon rail colour
TEXT = "#ffffff"
MUTED = "#b7cbd6"

NAME = "Vouchor"
TAGLINE = "An AI assistant that does real work for you, and proves it."  # README.md
FOOTER = "Self-hosted  ·  Open source  ·  AGPL-3.0"
DOMAIN = "vouchor.vercel.app"

DEFAULT_FONT_DIRS = [
    Path("/Library/Fonts"),
    Path.home() / "Library/Fonts",
    Path("/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF"),
    Path("/usr/share/fonts/truetype/roboto"),
]
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "docs/images/social-card.png"


def find_font(font_dirs: list[Path], filename: str) -> Path:
    for directory in font_dirs:
        candidate = directory / filename
        if candidate.is_file():
            return candidate
    searched = ", ".join(str(d) for d in font_dirs)
    raise SystemExit(f"{filename} not found in: {searched}. Pass --font-dir.")


def wrap(
    draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int
) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_rail_mark(draw: ImageDraw.ImageDraw, x: int, y: int, size: int) -> None:
    """Scaled copy of docs/images/favicon.svg (64x64 viewBox)."""
    s = size / 64
    draw.rounded_rectangle((x, y, x + size, y + size), radius=int(14 * s), fill=PANEL)
    stroke = max(1, round(5 * s))
    for x1, y1, x2, y2 in [
        (20, 13, 20, 51),
        (44, 13, 44, 51),
        (20, 22, 44, 22),
        (20, 32, 44, 32),
        (20, 42, 44, 42),
    ]:
        draw.line((x + x1 * s, y + y1 * s, x + x2 * s, y + y2 * s), fill=RAIL, width=stroke)
    for cx, cy in [(20, 13), (20, 51), (44, 13), (44, 51)]:
        r = stroke / 2
        draw.ellipse((x + cx * s - r, y + cy * s - r, x + cx * s + r, y + cy * s + r), fill=RAIL)


def render(font_dirs: list[Path], output: Path) -> None:
    bold = find_font(font_dirs, "Roboto-Bold.ttf")
    regular = find_font(font_dirs, "Roboto-Regular.ttf")
    medium = find_font(font_dirs, "Roboto-Medium.ttf")

    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    margin = 88

    # Accent bar along the left edge, echoing the site's teal accent.
    draw.rectangle((0, 0, 12, HEIGHT), fill=RAIL)

    mark = 112
    draw_rail_mark(draw, margin, 96, mark)
    name_font = ImageFont.truetype(str(bold), 104)
    draw.text((margin + mark + 36, 96 + mark // 2), NAME, font=name_font, fill=TEXT, anchor="lm")

    tagline_font = ImageFont.truetype(str(medium), 54)
    y = 280
    for line in wrap(draw, TAGLINE, tagline_font, WIDTH - 2 * margin):
        draw.text((margin, y), line, font=tagline_font, fill=TEXT)
        y += 68

    small = ImageFont.truetype(str(regular), 28)
    draw.line((margin, HEIGHT - 120, WIDTH - margin, HEIGHT - 120), fill="#294b5f", width=2)
    draw.text((margin, HEIGHT - 72), FOOTER, font=small, fill=MUTED, anchor="ls")
    draw.text((WIDTH - margin, HEIGHT - 72), DOMAIN, font=small, fill=RAIL, anchor="rs")

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, "PNG", optimize=True)
    print(f"wrote {output} ({output.stat().st_size // 1024} KB)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--font-dir", type=Path, action="append", help="directory with Roboto TTFs")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    render(args.font_dir or DEFAULT_FONT_DIRS, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
