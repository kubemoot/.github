"""Tests for wordmark.py and for the committed files it and render.sh produce.

Run from brand/: python3 -m unittest test_wordmark (needs fontTools and uharfbuzz).
"""
import struct
import unittest
from pathlib import Path

import wordmark

BRAND = Path(__file__).resolve().parent
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class IconBodyTest(unittest.TestCase):
    def test_strips_svg_title_and_background_comment(self):
        src = (
            '<svg xmlns="http://www.w3.org/2000/svg">\n  <title>Kubemoot</title>\n'
            "  <!-- No background: the mark sits on whatever is behind it. -->\n"
            '  <circle r="40"/>\n</svg>\n'
        )
        body = wordmark.icon_body(src)
        self.assertEqual(body.strip(), '<circle r="40"/>')

    def test_keeps_every_drawing_element_of_the_shipped_icon(self):
        src = wordmark.icon_source(BRAND, "color")
        body = wordmark.icon_body(src)
        self.assertEqual(body.count('<path d="M0 0'), 7)
        self.assertNotIn("<svg", body)
        self.assertNotIn("<title>", body)


class MarkBoundsTest(unittest.TestCase):
    def test_bounds_of_the_shipped_icon(self):
        x0, y0, x1, y1 = wordmark.mark_bounds(wordmark.icon_source(BRAND, "color"))
        self.assertAlmostEqual(y0, 20.0, places=3)  # the top drop's round end
        self.assertAlmostEqual(x0 + x1, 200.0, places=3)  # symmetric about the center
        self.assertTrue(170 < y1 < 175)

    def test_all_forms_share_the_same_bounds(self):
        bounds = {f: wordmark.mark_bounds(wordmark.icon_source(BRAND, f)) for f in ("color", "black", "white")}
        self.assertEqual(len(set(bounds.values())), 1)

    def test_rejects_an_svg_without_drops(self):
        with self.assertRaises(ValueError):
            wordmark.mark_bounds('<svg><circle r="40"/></svg>')


class CommittedLockupsTest(unittest.TestCase):
    def test_every_layout_and_variant_exists_with_its_png(self):
        for layout in wordmark.LAYOUTS:
            for variant, _, _ in wordmark.VARIANTS:
                base = BRAND / layout / variant / f"kubemoot-{layout}-{variant}"
                self.assertTrue(base.with_suffix(".svg").is_file(), base)
                self.assertTrue(base.with_suffix(".png").is_file(), base)

    def test_lockups_embed_the_current_icon_drawing(self):
        for layout in wordmark.LAYOUTS:
            for variant, form, name_color in wordmark.VARIANTS:
                svg = (BRAND / layout / variant / f"kubemoot-{layout}-{variant}.svg").read_text(encoding="utf-8")
                body = wordmark.icon_body(wordmark.icon_source(BRAND, form))
                self.assertIn(body, svg, f"{layout}/{variant} drifted from icon/{form}")
                self.assertIn(f'<path fill="{name_color}" d="', svg)


class FaviconIcoTest(unittest.TestCase):
    def test_ico_wraps_the_two_png_favicons(self):
        data = (BRAND / "favicon" / "favicon.ico").read_bytes()
        reserved, kind, count = struct.unpack_from("<HHH", data, 0)
        self.assertEqual((reserved, kind, count), (0, 1, 2))
        for i, size in enumerate((16, 32)):
            w, h, colors, res, planes, bpp, length, offset = struct.unpack_from("<BBBBHHII", data, 6 + 16 * i)
            self.assertEqual((w, h, colors, res, planes, bpp), (size, size, 0, 0, 1, 32))
            png = (BRAND / "favicon" / f"favicon-{size}.png").read_bytes()
            self.assertEqual(length, len(png))
            self.assertEqual(data[offset:offset + length], png)
            self.assertTrue(png.startswith(PNG_SIGNATURE))


if __name__ == "__main__":
    unittest.main()
