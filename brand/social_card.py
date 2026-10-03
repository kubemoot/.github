#!/usr/bin/env python3
"""Builds the social preview cards (the image GitHub shows when a repository link is
shared): one 1280 x 640 SVG per public repository, in brand/social/.

Every card is the Table navy background, the white-text horizontal lockup, the
repository's name and one line about it, and the tagline with the site address. All
text is IBM Plex Sans converted to outlines, the same way wordmark.py sets the name, so
the SVGs need no font to display. The committed SVGs are authoritative; render.sh
turns them into PNGs. Needs fontTools and uharfbuzz.

    social_card.py FONT_DIR [OUT_DIR]

FONT_DIR holds IBMPlexSans-SemiBold.otf and IBMPlexSans-Regular.otf from
https://github.com/IBM/plex. OUT_DIR defaults to brand/social/.
"""
import re
import sys
from xml.sax.saxutils import escape, quoteattr
from pathlib import Path

import wordmark

WIDTH, HEIGHT = 1280, 640
TABLE = "#1f2a37"
RING = "#5b8def"
KEYLINE = "#e5e7eb"
WHITE = "#ffffff"
TAGLINE = "Every voice, one answer."
SITE = "kubemoot.org"
LOCKUP = Path("horizontal") / "white-text" / "kubemoot-horizontal-white-text.svg"

# Layout in card pixels. Content stays inside x 96..1184 and y 64..576, well within
# the 1200 x 630 crop some platforms apply.
LEFT, RIGHT = 96.0, 1184.0
TEXT_WIDTH = RIGHT - LEFT
TITLE_WEIGHT, BODY_WEIGHT = "SemiBold", "Regular"
TITLE_SIZE = 132.0
LINE_SIZE = 46.0
LINE_LEADING = 62.0
MAX_LINES = 2
# The kubemoot card: the lockup is the title, its drawn height and top.
MAIN_LOCKUP = (150.0, 110.0)
MAIN_LINE_BASELINE = 360.0
# Other cards: the lockup as parent brand above the name. 76 px keeps the mark at
# 24 px, its minimum size, in a 400 px wide link preview.
PARENT_LOCKUP = (76.0, 64.0)
TITLE_BASELINE = 312.0
TITLE_TO_LINE = 92.0
FOOTER_SIZE = 32.0
FOOTER_BASELINE = 568.0

# Each card: (repository, the name shown large or None for the lockup itself, one line).
CARDS = [
    ("kubemoot", None,
     "A Kubernetes operator for crews of LLM agents that deliberate to consensus."),
    ("crews", "crews", "Example Kubemoot crews as Helm charts."),
    ("kmctl", "kmctl", "The command-line tool for Kubemoot crews and discussions."),
    ("kubemoot-docs", "kubemoot-docs", "The Kubemoot landing page and reference documentation."),
    ("vscode-crewforge", "CrewForge", "Build, deploy, and talk to crews from VS Code."),
    ("release-actions", "release-actions", "Shared GitHub Actions for Kubemoot releases."),
]


class Typesetter:
    """Sets text in one IBM Plex Sans weight as SVG path outlines."""

    def __init__(self, font_path):
        self.font_path = font_path
        self._shaped = {}

    def _shape(self, text):
        if not text.strip():
            raise ValueError("nothing to set")
        if text not in self._shaped:
            self._shaped[text] = wordmark.shape(self.font_path, text)
        return self._shaped[text]

    def bounds(self, text, size):
        """Ink bounds (xmin, ymin, xmax, ymax) of text set at left 0 on baseline 0."""
        ttf, placed = self._shape(text)
        return wordmark.text_metrics(ttf, placed, size)

    def width(self, text, size):
        x0, _, x1, _ = self.bounds(text, size)
        return x1 - x0

    def path(self, text, size, left, baseline, color):
        """A path element whose ink starts exactly at left."""
        ttf, placed = self._shape(text)
        ink_left = self.bounds(text, size)[0]
        d, _ = wordmark.outline(ttf, placed, size, left - ink_left, baseline)
        return f'  <path fill="{color}" d="{d}"/>'


def wrap(text, measure, max_width, max_lines=MAX_LINES):
    """The fewest lines that keep text within max_width, broken between words so the
    widest line is as narrow as possible (no single word left alone on a last line).

    Raises ValueError when the text is empty or does not fit in max_lines lines.
    """
    words = text.split()
    if not words:
        raise ValueError("nothing to wrap")
    for count in range(1, min(max_lines, len(words)) + 1):
        lines = _balanced(words, count, measure)
        if max(measure(line) for line in lines) <= max_width:
            return lines
    raise ValueError(f"{text!r} does not fit in {max_lines} lines of {max_width}")


def _balanced(words, count, measure):
    """words split into count lines with the narrowest widest line. Tries every split,
    which is fine for one-line descriptions and MAX_LINES of 2 or 3."""
    if count == 1:
        return [" ".join(words)]
    splits = (
        [" ".join(words[:i])] + _balanced(words[i:], count - 1, measure)
        for i in range(1, len(words) - count + 2)
    )
    return min(splits, key=lambda lines: max(measure(line) for line in lines))


def lockup(brand):
    """The white-text lockup's drawing and its viewBox (x, y, w, h)."""
    src = (brand / LOCKUP).read_text(encoding="utf-8")
    box = re.search(r'viewBox="([^"]+)"', src).group(1)
    return wordmark.icon_body(src), tuple(float(v) for v in box.split())


def place_lockup(body, box, ink_height, top):
    """The lockup scaled so its drawn mark is ink_height tall, its left edge at LEFT.

    The lockup files carry wordmark.MARGIN of clear space on every side; that space is
    left out of the size and the alignment.
    """
    x, y, _, h = box
    scale = ink_height / (h - 2 * wordmark.MARGIN)
    tx = LEFT - (x + wordmark.MARGIN) * scale
    ty = top - (y + wordmark.MARGIN) * scale
    return (f'  <g transform="translate({wordmark.num(tx)} {wordmark.num(ty)}) scale({wordmark.num(scale, 5)})">\n'
            f"{body}\n  </g>")


def title_block(title, body, box, title_face):
    """The top of the card, and the baseline of the one line's first row."""
    if title is None:
        return [place_lockup(body, box, *MAIN_LOCKUP)], MAIN_LINE_BASELINE
    return [
        place_lockup(body, box, *PARENT_LOCKUP),
        title_face.path(title, TITLE_SIZE, LEFT, TITLE_BASELINE, WHITE),
    ], TITLE_BASELINE + TITLE_TO_LINE


def card(repo, title, line, brand, title_face, body_face):
    body, box = lockup(brand)
    parts, baseline = title_block(title, body, box, title_face)
    for row in wrap(line, lambda t: body_face.width(t, LINE_SIZE), TEXT_WIDTH):
        parts.append(body_face.path(row, LINE_SIZE, LEFT, baseline, KEYLINE))
        baseline += LINE_LEADING
    parts.append(title_face.path(TAGLINE, FOOTER_SIZE, LEFT, FOOTER_BASELINE, RING))
    site_left = RIGHT - body_face.width(SITE, FOOTER_SIZE)
    parts.append(body_face.path(SITE, FOOTER_SIZE, site_left, FOOTER_BASELINE, KEYLINE))
    label = f"{title or 'Kubemoot'}: {line} {TAGLINE} {SITE}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}" role="img" aria-label={quoteattr(label)}>\n'
        f"  <title>{escape(repo)}</title>\n"
        "  <!-- Generated by brand/social_card.py; all text is IBM Plex Sans as outlines. -->\n"
        f'  <rect width="{WIDTH}" height="{HEIGHT}" fill="{TABLE}"/>\n'
        + "\n".join(parts) + "\n</svg>\n"
    )


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    font_dir = Path(sys.argv[1])
    brand = Path(__file__).resolve().parent
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else brand / "social"
    out_dir.mkdir(parents=True, exist_ok=True)
    fonts = [font_dir / f"IBMPlexSans-{weight}.otf" for weight in (TITLE_WEIGHT, BODY_WEIGHT)]
    missing = [str(font) for font in fonts if not font.is_file()]
    if missing:
        sys.exit(f"missing font: {', '.join(missing)}")
    title_face, body_face = (Typesetter(font) for font in fonts)
    for repo, title, line in CARDS:
        text = card(repo, title, line, brand, title_face, body_face)
        (out_dir / f"{repo}.svg").write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
