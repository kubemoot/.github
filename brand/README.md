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

| File | Use |
|---|---|
| `kubemoot-mark.svg` | Canonical. Light or mid backgrounds. Scales to any size; the favicons are cut from it. |
| `kubemoot-mark-on-dark.svg` | Dark backgrounds: the table turns light so it stays visible. |
| `kubemoot-mark-512.png`, `kubemoot-mark-1024.png`, `kubemoot-mark-on-dark-512.png` | Renders for places that cannot take SVG (social cards, slide tools, avatars). |

Rules: keep clear space of at least one drop's length around the mark; never rotate,
recolor, outline, or add a gradient; below 24 px use the mark alone, no wordmark; do
not put the mark on a busy photo.

## Colors

| Name | Hex | Used for |
|---|---|---|
| Table | `#1f2a37` | The table, headings on light backgrounds, dark surfaces |
| Drop | `#3b82f6` | The drops, links, primary actions |
| Ring | `#5b8def` | The table's ring, accents, focus states |
| Table on dark | `#e5e7eb` | The table when the mark sits on a dark background |
| Paper | `#ffffff` | Page background |

Drop on Table and Table on Paper both pass WCAG AA for text.

## Type

The documentation site uses the Docsy default sans-serif stack (system fonts); nothing
is embedded or licensed. Headings are set in the same face, heavier. If a display face
is adopted later, it is added here first and the site follows.

## Voice

Tagline: **Every voice, one answer.**

Prose names: Kubemoot, Homelab Pilot, CrewForge, kmctl. Identifiers: `kubemoot`,
`homelab-pilot`, `crew-forge`, `kmctl`. Never "KubeMoot", "Crew Forge", or
"production-grade". Plain hyphens, never em dashes.

## Where the mark is used

- Organization profile: `profile/README.md` in this repository.
- Documentation site: `kubemoot-docs/assets/icons/logo.svg` (navbar),
  `assets/img/kubemoot-mark.svg` (landing page, served under a content hash), `static/favicons/*` (cut from the
  1024 px render). Copies, refreshed from here when the mark changes.
