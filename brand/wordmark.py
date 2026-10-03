#!/usr/bin/env python3
"""Builds the horizontal and stacked lockup SVGs: the icon plus the name "kubemoot"
set in IBM Plex Sans and converted to outlines, so no font is needed to show them.

The committed SVGs are authoritative; this script only regenerates them when the
font is at hand. Needs fontTools and uharfbuzz (for the font's own kerning).

    wordmark.py FONT_DIR [OUT_DIR [WEIGHT]]

FONT_DIR holds IBMPlexSans-<Weight>.otf from https://github.com/IBM/plex. OUT_DIR
defaults to this script's directory (brand/); WEIGHT defaults to the brand weight.
"""
import math
import re
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

NAME = "kubemoot"
WEIGHT = "SemiBold"
NAVY = "#1f2a37"
WHITE = "#ffffff"
LABEL = "Kubemoot: a round table with seven water drops gathered around it, and the name kubemoot"

# Geometry, in the icon's 200-unit artwork.
TABLE_CENTER = 100.0
MARGIN = 20.0
LAYOUTS = {
    # Name size in units per em, and the gap between the mark's drawn edge and the name.
    "horizontal": {"size": 100.0, "gap": 32.0},
    "stacked": {"size": 64.0, "gap": 24.0},
}
# Each variant: (folder and file suffix, icon form for the mark, name color).
VARIANTS = [
    ("color", "color", NAVY),
    ("black", "black", NAVY),
    ("white", "white", WHITE),
    ("white-text", "color", WHITE),
]


def num(v, places=2):
    """A number for SVG output: rounded to places, trailing zeros dropped."""
    return f"{v:.{places}f}".rstrip("0").rstrip(".")


def shape(font_path, text=NAME):
    """Glyph names and kerned pen positions for text (default NAME), in font units."""
    blob = hb.Blob.from_file_path(str(font_path))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb_font = hb.Font(hb.Face(blob))
    hb.shape(hb_font, buf, {"kern": True})
    ttf = TTFont(str(font_path))
    order = ttf.getGlyphOrder()
    x = 0
    placed = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        placed.append((order[info.codepoint], x + pos.x_offset))
        x += pos.x_advance
    return ttf, placed


def outline(ttf, placed, size, left, baseline):
    """One SVG path for the whole name, with coordinates baked in, plus its ink bounds."""
    glyphs = ttf.getGlyphSet()
    scale = size / ttf["head"].unitsPerEm
    pen = SVGPathPen(glyphs, ntos=num)
    bounds = BoundsPen(glyphs)
    for name, x in placed:
        matrix = (scale, 0, 0, -scale, left + x * scale, baseline)
        glyphs[name].draw(TransformPen(pen, matrix))
        glyphs[name].draw(TransformPen(bounds, matrix))
    return pen.getCommands(), bounds.bounds


def text_metrics(ttf, placed, size):
    """The name's ink bounds when set at left 0 on baseline 0."""
    return outline(ttf, placed, size, 0.0, 0.0)[1]


def icon_source(brand, form):
    return (brand / "icon" / form / f"kubemoot-icon-{form}.svg").read_text(encoding="utf-8")


def icon_body(src):
    """The drawing inside an icon SVG, without its svg, title, and background comment."""
    body = src.split("</title>\n", 1)[1].rsplit("</svg>", 1)[0]
    lines = [line for line in body.splitlines() if "No background" not in line]
    return "\n".join(lines)


DROP = re.compile(
    r'<path d="(M0 0 [^"]+)" transform="rotate\(([\d.]+) 100 100\) translate\(100 (\d+)\)"/>'
)


def mark_bounds(src):
    """The drawn extent (xmin, ymin, xmax, ymax) of the drops, read from an icon SVG."""
    pen = BoundsPen(None)
    drops = DROP.findall(src)
    if not drops:
        raise ValueError("no drop paths found in the icon SVG")
    for d, angle, dy in drops:
        a = math.radians(float(angle))
        cos, sin = math.cos(a), math.sin(a)
        # rotate(angle, 100, 100) then translate(100, dy), as one affine matrix.
        tx, ty = 100.0, float(dy)
        matrix = (cos, sin, -sin, cos,
                  100 + cos * (tx - 100) - sin * (ty - 100),
                  100 + sin * (tx - 100) + cos * (ty - 100))
        parse_path(d, TransformPen(pen, matrix))
    return pen.bounds


def horizontal_place(ttf, placed, mark):
    size, gap = LAYOUTS["horizontal"]["size"], LAYOUTS["horizontal"]["gap"]
    ink_left = text_metrics(ttf, placed, size)[0]
    x_height = ttf["OS/2"].sxHeight * size / ttf["head"].unitsPerEm
    baseline = TABLE_CENTER + x_height / 2
    left = mark[2] + gap - ink_left
    return size, left, baseline


def stacked_place(ttf, placed, mark):
    size, gap = LAYOUTS["stacked"]["size"], LAYOUTS["stacked"]["gap"]
    ink_left, ink_top, ink_right, _ = text_metrics(ttf, placed, size)
    left = TABLE_CENTER - (ink_left + ink_right) / 2
    baseline = mark[3] + gap - ink_top
    return size, left, baseline


PLACE = {"horizontal": horizontal_place, "stacked": stacked_place}


def svg(layout, ttf, placed, src, name_color, weight):
    mark = mark_bounds(src)
    size, left, baseline = PLACE[layout](ttf, placed, mark)
    path, (tx0, ty0, tx1, ty1) = outline(ttf, placed, size, left, baseline)
    vx0 = min(mark[0], tx0) - MARGIN
    vy0 = min(mark[1], ty0) - MARGIN
    vw = max(mark[2], tx1) + MARGIN - vx0
    vh = max(mark[3], ty1) + MARGIN - vy0
    box = " ".join(num(v, 1) for v in (vx0, vy0, vw, vh))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" '
        f'width="{vw:.0f}" height="{vh:.0f}" role="img" aria-label="{LABEL}">\n'
        "  <title>Kubemoot</title>\n"
        "  <!-- No background: the lockup sits on whatever is behind it. -->\n"
        f"{icon_body(src)}\n"
        f"  <!-- The name: IBM Plex Sans {weight}, lowercase, kerned, as outlines. -->\n"
        f'  <path fill="{name_color}" d="{path}"/>\n'
        "</svg>\n"
    )


def main():
    font_dir = Path(sys.argv[1])
    brand = Path(__file__).resolve().parent
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else brand
    weight = sys.argv[3] if len(sys.argv) > 3 else WEIGHT
    ttf, placed = shape(font_dir / f"IBMPlexSans-{weight}.otf")
    for layout in LAYOUTS:
        for variant, form, name_color in VARIANTS:
            out = out_dir / layout / variant / f"kubemoot-{layout}-{variant}.svg"
            out.parent.mkdir(parents=True, exist_ok=True)
            text = svg(layout, ttf, placed, icon_source(brand, form), name_color, weight)
            out.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
