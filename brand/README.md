# Kubemoot brand

The single source for the mark, colors, type, and tagline. Every repository, the
documentation site, slides, and social cards copy from here; nothing redraws its own.

## The mark

A round table seen from above, with seven water drops gathered around it, every
drop's point aimed at the center. Seven, like the seven sides of the Kubernetes
wheel. The table is the moot; the drops are the agents: many,
small, alike in form, each turned toward the shared decision. The image comes from
the round table of the Arthurian legend: no head of the table, so no seat outranks
another.

The full-color mark carries a thin light keyline (Keyline `#e5e7eb`) just outside the
table. On white it is a faint rim; on dark backgrounds it outlines the table, so one file
serves light and dark. The one-color forms cut the inner ring out of the table, so the
background shows through it.

## Files

The SVGs are hand-written and are the sources. Every PNG and the `.ico` are generated
from them by `render.sh` (needs `rsvg-convert`); after changing an SVG, run it and
commit the outputs together.

| File | Use |
|---|---|
| `icon/color/kubemoot-icon-color.svg` | Canonical. Full color with keyline: white, light, mid-tone, and dark backgrounds. |
| `icon/black/kubemoot-icon-black.svg` | One color, Table navy: single-ink print, light backgrounds where color is not wanted. |
| `icon/white/kubemoot-icon-white.svg` | One color, white: brand blue and other colored backgrounds, photos, dark one-ink uses. |
| `icon/<form>/kubemoot-icon-<form>.png`, `kubemoot-icon-<form>-512.png` | Transparent 1024 and 512 px renders for places that cannot take SVG (social cards, slide tools). |
| `horizontal/<form>/kubemoot-horizontal-<form>.svg` | The mark left of the name: headers, slides, README banners. Forms `color`, `black`, `white`, `white-text`. |
| `stacked/<form>/kubemoot-stacked-<form>.svg` | The mark above the name: square-ish spaces, title slides, stickers. Same forms. |
| `horizontal/<form>/*.png`, `stacked/<form>/*.png` | Transparent renders, 512 px high (horizontal) and 1024 px high (stacked). |
| `avatar/kubemoot-avatar-1024.png`, `kubemoot-avatar-512.png` | Profile pictures (the GitHub org avatar): the full-color icon on solid Paper, filling about 78% of the square. |
| `favicon/kubemoot-favicon.svg` | Adaptive SVG favicon: full color in light browser chrome, the white form under `prefers-color-scheme: dark`. Cropped tighter than the icon. |
| `favicon/kubemoot-favicon-small.svg` | The small form: the table as a solid disc, no ring. Source of the 16 px favicon. |
| `favicon/favicon-32.png`, `favicon-16.png`, `favicon.ico` | Fallbacks for browsers without SVG favicons. The `.ico` holds both PNGs. |
| `render.sh` | Regenerates every PNG and the `.ico`. With `WORDMARK_FONT_DIR` set, first rebuilds the lockup SVGs with `wordmark.py`. |
| `wordmark.py` | Builds the lockup SVGs from the icon SVGs and the Plex Sans OTF (needs fontTools and uharfbuzz). The committed SVGs are authoritative. |
| `test_wordmark.py` | Checks the lockups against the icon drawing and the `.ico` against the PNGs: `python3 -m unittest test_wordmark` from `brand/` (needs fontTools and uharfbuzz). |
| `mark-review.md`, `review/`, `render-review.sh` | The decision record for this mark set and its comparison images. |

The lockup forms: `color` is the full-color mark with the name in Table navy, for light
backgrounds; `white-text` is the full-color mark with the name in white, for dark
backgrounds; `black` and `white` are the one-color forms, mark and name in one color.

Serve the favicon set with:

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/kubemoot-favicon.svg" type="image/svg+xml">
```

## Using the mark

**Minimum size: 24 px.** The inner ring is drawn 5 units wide in the 200-unit artwork,
the thinnest ring that still reads at 32 px in both the full-color and one-color forms,
and it holds at 24 px. Below 24 px the ring smears into the table: use the small form
(`favicon/kubemoot-favicon-small.svg`, the table as a solid disc with the seven drops).

**Clear space:** keep at least one drop's length (34 units of the 200-unit artwork) free
around the outermost drops. The artwork already carries about 20 units of it on every
side; do not crop it tighter, except in the favicon.

**Which form on which background:**

| Background | Form |
|---|---|
| White or light gray (Paper `#ffffff`, `#f6f8fa`) | Full color. One-color black when color is not available. |
| Mid-tone gray | Full color; the keyline separates the table from the gray. Lockups: `white-text`, since the navy name is too weak on gray. |
| Brand blue or any saturated color | One-color white. The blue drops vanish on brand blue. |
| Dark (`#161b22`, `#0d1117`) | Full color; the keyline outlines the table. Lockups: `white-text`. One-color white for one-ink uses. |
| Photo | One-color white on a calm, dark area; never on a busy photo. |

The one-color "black" is Table navy `#1f2a37`, not pure black: at 32 and 24 px it reads
as black on white and keeps the palette to one dark.

**Do not:** rotate the mark or change the number of drops; recolor it outside the three
forms; add a second outline, a shadow, a glow, or a gradient; stretch or skew it; fill the
ring with another color in the one-color forms (it is cut out); put the full-color mark on
brand blue; retype the name in live text or another face, or change the lockup's spacing:
use the lockup files.

## Colors

| Name | Hex | Used for |
|---|---|---|
| Table | `#1f2a37` | The table, the one-color black form, headings on light backgrounds, dark surfaces |
| Drop | `#3b82f6` | The drops, links, primary actions |
| Ring | `#5b8def` | The table's ring, accents, focus states |
| Keyline | `#e5e7eb` | The light rim behind the table in the full-color mark |
| Paper | `#ffffff` | Page background, the avatar background, the one-color white form |

Drop on Table and Table on Paper both pass WCAG AA for text.

## Type

**Wordmark:** IBM Plex Sans SemiBold, all lowercase: "kubemoot". Kerned with the font's
own kerning and converted to outlines, so the lockups need no font to display. SemiBold
matches the weight of the solid table and the drops; Medium looks light beside them and
thins out at small sizes.

Lockup geometry, in the units of the 200-unit icon drawing:

- Horizontal: the name at 100 units per em (x-height 52), its x-height centered on the
  table; 32 units between the rightmost drop and the name, a little under one drop's length.
- Stacked: the name at 64 units per em, centered under the table; 24 units between the
  lowest drop and the top of the name.
- Clear space around either lockup: one drop's length (34 units) on every side; the
  files carry 20 units of it.

The font is not committed. IBM Plex Sans is Copyright 2017 IBM Corp., with Reserved Font
Name "Plex", and is licensed under the SIL Open Font License, Version 1.1
(https://github.com/IBM/plex, https://openfontlicense.org). The outlined name is a
rendering of the font, not a copy of it.

**Text:** the documentation site uses the Docsy default sans-serif stack (system fonts);
nothing is embedded or licensed. Headings are set in the same face, heavier.

## Voice

Tagline: **Every voice, one answer.**

Prose names: Kubemoot, Homelab Pilot, CrewForge, kmctl. Identifiers: `kubemoot`,
`homelab-pilot`, `crewforge` (extension id `kubemoot.crewforge`, repository
`vscode-crewforge`), `kmctl`. Never "KubeMoot", "Crew Forge", or "production-grade".
Plain hyphens, never em dashes.

## Where the mark is used

Every use is a copy, refreshed from here when the mark changes.

- GitHub organization avatar: `avatar/kubemoot-avatar-1024.png`, uploaded in the org settings.
- Organization profile: `profile/README.md` in this repository links the full-color icon.
- Documentation site: `kubemoot-docs/assets/icons/logo.svg` (navbar),
  `assets/img/kubemoot-mark.svg` (landing page, served under a content hash),
  `static/favicons/*` (the favicon set).
- Kubemoot dashboard: the favicon set, in `kubemoot/dashboard/static/`.
- Homelab Pilot: the favicon set, in `homelab-pilot`'s SvelteKit static assets.
- CrewForge: `vscode-crewforge/media/` (the activity bar icon and the webview logo in
  light and dark forms).
