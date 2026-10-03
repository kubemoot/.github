"""Tests for social_card.py and the committed social preview cards.

Run from brand/: python3 -m unittest test_social_card (needs fontTools and uharfbuzz).
"""
import os
import re
import struct
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import social_card
import wordmark

BRAND = Path(__file__).resolve().parent
SOCIAL = BRAND / "social"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
GITHUB_LIMIT = 1_000_000  # GitHub refuses social preview images of 1 MB or more.
FONT_DIR = os.environ.get("WORDMARK_FONT_DIR")
SVG_NS = "{http://www.w3.org/2000/svg}"


def chars(text):
    """A stand-in measure: every character is 1 unit wide."""
    return len(text)


class WrapTest(unittest.TestCase):
    def test_short_text_stays_on_one_line(self):
        self.assertEqual(social_card.wrap("one two", chars, 10), ["one two"])

    def test_two_lines_are_balanced_not_greedy(self):
        # Greedy would leave "dd" alone on the second line.
        self.assertEqual(social_card.wrap("aa bb cc dd", chars, 10), ["aa bb", "cc dd"])

    def test_text_that_fits_exactly_is_not_broken(self):
        self.assertEqual(social_card.wrap("abcde fghi", chars, 10), ["abcde fghi"])

    def test_rejects_text_needing_too_many_lines(self):
        with self.assertRaises(ValueError):
            social_card.wrap("aaaa bbbb cccc", chars, 5, max_lines=2)

    def test_rejects_a_word_wider_than_the_line(self):
        with self.assertRaises(ValueError):
            social_card.wrap("abcdefghijk", chars, 10)

    def test_rejects_empty_text(self):
        with self.assertRaises(ValueError):
            social_card.wrap("   ", chars, 10)


class FakeFace:
    """A Typesetter stand-in: records what it sets, 1 unit per character."""

    def __init__(self):
        self.set = []

    def width(self, text, size):
        return len(text) * size / 2

    def path(self, text, size, left, baseline, color):
        self.set.append((text, size, left, baseline, color))
        return f'  <path fill="{color}" d="M{left} {baseline}"/>'


class NumTest(unittest.TestCase):
    def test_drops_trailing_zeros_and_point(self):
        self.assertEqual(wordmark.num(2.0), "2")
        self.assertEqual(wordmark.num(2.50), "2.5")
        self.assertEqual(wordmark.num(-0.125, 1), "-0.1")

    def test_keeps_requested_precision(self):
        self.assertEqual(wordmark.num(0.496738, 5), "0.49674")


class TitleBlockTest(unittest.TestCase):
    BOX = (1.8, 0.0, 685.5, 192.9)

    def test_kubemoot_card_uses_the_lockup_as_title(self):
        face = FakeFace()
        parts, baseline = social_card.title_block(None, "<g/>", self.BOX, face)
        self.assertEqual(len(parts), 1)
        self.assertEqual(face.set, [])
        self.assertEqual(baseline, social_card.MAIN_LINE_BASELINE)

    def test_other_cards_set_the_title_below_the_parent_lockup(self):
        face = FakeFace()
        parts, baseline = social_card.title_block("kmctl", "<g/>", self.BOX, face)
        self.assertEqual(len(parts), 2)
        self.assertEqual(face.set, [("kmctl", social_card.TITLE_SIZE, social_card.LEFT,
                                     social_card.TITLE_BASELINE, social_card.WHITE)])
        self.assertGreater(baseline, social_card.TITLE_BASELINE)


class CardTest(unittest.TestCase):
    def test_escapes_markup_in_text(self):
        face = FakeFace()
        svg = social_card.card('a&b', "A & B", 'Fish & "chips" <here>.', BRAND, face, face)
        root = ET.fromstring(svg)  # raises on invalid XML
        self.assertEqual(root.find(f"{SVG_NS}title").text, "a&b")
        self.assertIn('Fish & "chips" <here>.', root.get("aria-label"))

    def test_wraps_a_long_line_onto_two_rows(self):
        face = FakeFace()
        social_card.card("kubemoot", None, social_card.CARDS[0][2], BRAND, face, face)
        rows = [t for t, size, *_ in face.set if size == social_card.LINE_SIZE]
        self.assertEqual(len(rows), 2)
        self.assertEqual(" ".join(rows), social_card.CARDS[0][2])

    def test_rejects_a_line_that_does_not_fit(self):
        with self.assertRaises(ValueError):
            social_card.card("x", "x", "word " * 80, BRAND, FakeFace(), FakeFace())


@unittest.skipUnless(FONT_DIR, "set WORDMARK_FONT_DIR to the IBM Plex Sans OTFs")
class GeneratedCardsTest(unittest.TestCase):
    def test_committed_svgs_match_the_generator(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as out:
            subprocess.run([sys.executable, str(BRAND / "social_card.py"), FONT_DIR, out], check=True)
            for repo, _, _ in social_card.CARDS:
                fresh = (Path(out) / f"{repo}.svg").read_bytes()
                self.assertEqual(fresh, (SOCIAL / f"{repo}.svg").read_bytes(),
                                 f"social/{repo}.svg is stale: run render.sh with WORDMARK_FONT_DIR")


class PlaceLockupTest(unittest.TestCase):
    def test_drawn_mark_lands_at_the_left_margin_and_top(self):
        box = (1.8, 0.0, 685.5, 192.9)
        group = social_card.place_lockup("<g/>", box, 76.0, 64.0)
        tx, ty, scale = map(float, re.search(
            r"translate\(([-\d.]+) ([-\d.]+)\) scale\(([\d.]+)\)", group).groups())
        self.assertAlmostEqual(scale * (box[3] - 2 * wordmark.MARGIN), 76.0, places=1)
        self.assertAlmostEqual(tx + (box[0] + wordmark.MARGIN) * scale, social_card.LEFT, places=1)
        self.assertAlmostEqual(ty + (box[1] + wordmark.MARGIN) * scale, 64.0, places=1)


class CardListTest(unittest.TestCase):
    def test_one_card_for_every_repository(self):
        repos = [repo for repo, _, _ in social_card.CARDS]
        self.assertEqual(repos, ["kubemoot"])

    def test_text_is_plain_ascii(self):
        for repo, title, line in social_card.CARDS:
            for text in (title or "", line):
                self.assertTrue(text.isascii(), f"{repo}: {text!r}")


class CommittedCardsTest(unittest.TestCase):
    def test_every_card_has_an_outlined_svg_and_its_png(self):
        lockup_body, _ = social_card.lockup(BRAND)
        for repo, _, _ in social_card.CARDS:
            svg = (SOCIAL / f"{repo}.svg").read_text(encoding="utf-8")
            self.assertNotIn("<text", svg, repo)
            self.assertNotIn("font-family", svg, repo)
            self.assertIn(lockup_body, svg, f"{repo} drifted from the white-text lockup")
            self.assertIn(f'fill="{social_card.TABLE}"', svg)

    def test_every_card_states_its_current_line(self):
        for repo, title, line in social_card.CARDS:
            root = ET.parse(SOCIAL / f"{repo}.svg").getroot()
            self.assertIn(line, root.get("aria-label"), f"social/{repo}.svg is stale")
            self.assertEqual(root.find(f"{SVG_NS}title").text, repo)

    def test_pngs_are_1280_by_640_and_under_the_github_limit(self):
        for repo, _, _ in social_card.CARDS:
            data = (SOCIAL / f"{repo}.png").read_bytes()
            self.assertTrue(data.startswith(PNG_SIGNATURE), repo)
            width, height = struct.unpack(">II", data[16:24])
            self.assertEqual((width, height), (1280, 640), repo)
            self.assertLess(len(data), GITHUB_LIMIT, repo)

    def test_no_stray_cards(self):
        expected = {repo for repo, _, _ in social_card.CARDS}
        for path in SOCIAL.iterdir():
            self.assertIn(path.stem, expected, path.name)


if __name__ == "__main__":
    unittest.main()
