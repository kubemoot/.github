#!/usr/bin/env bash
# Regenerates the comparison images of the mark review (mark-review.md) into review/.
# Each image is one SVG of tiles, rendered with rsvg-convert, so the output is
# deterministic. The Kubernetes icon precedent is fetched at render time and its
# render stays out of git (review/.gitignore); the review links its source instead.
set -euo pipefail
cd "$(dirname "$0")"

RSVG="${RSVG:-rsvg-convert}"
OUT=review
K8S_ICON_URL='https://raw.githubusercontent.com/cncf/artwork/40e2e8948509b40e4bad479446aaec18d6273bf2/projects/kubernetes/icon/color/kubernetes-icon-color.svg'
mkdir -p "$OUT"

drops() { # drops FILL
  local a
  printf '<g fill="%s">' "$1"
  for a in 0.000 51.429 102.857 154.286 205.714 257.143 308.571; do
    printf '<path d="M0 0 C 11 -14, 11 -34, 0 -34 C -11 -34, -11 -14, 0 0 Z" transform="rotate(%s 100 100) translate(100 54)"/>' "$a"
  done
  printf '</g>'
}

# shipped FORM: the drawing of a shipped icon SVG, so the decided forms are the real files.
shipped() {
  sed -e '/<svg /d' -e '/<\/svg>/d' -e '/<title>/d' -e '/<!--/d' "icon/$1/kubemoot-icon-$1.svg" | tr -d '\n'
}

# The generators below draw only the rejected options and the old ring width.
# full TABLE RING RING_WIDTH KEYLINE_RADIUS (0 = none): a full-color variant, 200 units.
full() {
  if [[ "$4" != 0 ]]; then printf '<circle cx="100" cy="100" r="%s" fill="#e5e7eb"/>' "$4"; fi
  printf '<circle cx="100" cy="100" r="40" fill="%s"/>' "$1"
  printf '<circle cx="100" cy="100" r="32" fill="none" stroke="%s" stroke-width="%s"/>' "$2" "$3"
  drops '#3b82f6'
}

# mono COLOR RING_WIDTH: a one-color variant, the ring cut out of the table.
mono() {
  local o i
  o=$(awk "BEGIN{print 32 + $2 / 2}")
  i=$(awk "BEGIN{print 32 - $2 / 2}")
  printf '<path fill="%s" fill-rule="evenodd" d="M60 100a40 40 0 1 0 80 0a40 40 0 1 0 -80 0Z M%s 100a%s %s 0 1 0 %s 0a%s %s 0 1 0 -%s 0Z M%s 100a%s %s 0 1 0 %s 0a%s %s 0 1 0 -%s 0Z"/>' \
    "$1" "$(awk "BEGIN{print 100 - $o}")" "$o" "$o" "$(awk "BEGIN{print 2 * $o}")" "$o" "$o" "$(awk "BEGIN{print 2 * $o}")" \
    "$(awk "BEGIN{print 100 - $i}")" "$i" "$i" "$(awk "BEGIN{print 2 * $i}")" "$i" "$i" "$(awk "BEGIN{print 2 * $i}")"
  drops "$1"
}

# tile X Y BG BODY: a 200x160 tile with the mark at 128 px and at 32 px.
tile() {
  printf '<rect x="%s" y="%s" width="200" height="160" fill="%s"/>' "$1" "$2" "$3"
  printf '<g transform="translate(%s %s) scale(0.64)">%s</g>' "$(($1 + 8))" "$(($2 + 16))" "$4"
  printf '<g transform="translate(%s %s) scale(0.16)">%s</g>' "$(($1 + 152))" "$(($2 + 64))" "$4"
}

# sheet NAME COLUMNS ROWS: renders tiles read from stdin, laid out by the caller.
sheet() {
  local w=$((8 + $2 * 208)) h=$((8 + $3 * 168))
  { printf '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" viewBox="0 0 %s %s">' "$w" "$h" "$w" "$h"
    printf '<rect width="%s" height="%s" fill="#888888"/>' "$w" "$h"
    cat
    printf '</svg>\n'
  } | "$RSVG" -o "$OUT/$1.png"
}

# grid NAME BGS... -- BODIES...: one row per background, one column per body.
grid() {
  local name="$1"; shift
  local bgs=() bodies=() r c
  while [[ "$1" != -- ]]; do bgs+=("$1"); shift; done; shift
  bodies=("$@")
  for r in "${!bgs[@]}"; do
    for c in "${!bodies[@]}"; do
      tile $((8 + c * 208)) $((8 + r * 168)) "${bgs[$r]}" "${bodies[$c]}"
    done
  done | sheet "$name" "${#bodies[@]}" "${#bgs[@]}"
}

A=$(full '#1f2a37' '#5b8def' 2.5 0)   # the mark before the review
B=$(full '#1f2a37' '#5b8def' 2.5 43)  # A with the light keyline
C=$(full '#64748b' '#e5e7eb' 2.5 0)   # a slate table
NEW=$(shipped color)                  # the decided forms, from the shipped files
WHITE=$(shipped white)
NAVY=$(shipped black)

# Columns A, B, C; rows white and GitHub dark.
grid options-light-dark '#ffffff' '#0d1117' -- "$A" "$B" "$C"
# Columns A, B, C; rows mid gray, brand blue, GitHub canvas, GitHub dark surface.
grid options-midtones '#6e7681' '#3b82f6' '#f6f8fa' '#161b22' -- "$A" "$B" "$C"
# White form on brand blue, dark, gray; navy form on white, brand blue, light gray.
{
  tile 8 8 '#3b82f6' "$WHITE"; tile 216 8 '#0d1117' "$WHITE"; tile 424 8 '#6e7681' "$WHITE"
  tile 8 176 '#ffffff' "$NAVY"; tile 216 176 '#3b82f6' "$NAVY"; tile 424 176 '#f6f8fa' "$NAVY"
} | sheet one-color 3 2
# Ring width, 2.5 units (before) against 5 units (decided): full color, then one color;
# top row on white with the navy form, bottom row on GitHub dark with the white form.
{
  tile 8 8 '#ffffff' "$A"; tile 216 8 '#ffffff' "$NEW"
  tile 424 8 '#ffffff' "$(mono '#1f2a37' 2.5)"; tile 632 8 '#ffffff' "$NAVY"
  tile 8 176 '#0d1117' "$B"; tile 216 176 '#0d1117' "$NEW"
  tile 424 176 '#0d1117' "$(mono '#ffffff' 2.5)"; tile 632 176 '#0d1117' "$WHITE"
} | sheet ring-width 4 2

# Kubernetes icon precedent, on white and on GitHub dark. Fetched, never committed.
k8s=$(mktemp)
trap 'rm -f "$k8s"' EXIT
if curl -sfL "$K8S_ICON_URL" -o "$k8s"; then
  icon=$(sed -e 's/<?xml[^>]*?>//' -e 's/<svg /<svg x="24" y="24" width="152" height="152" /' "$k8s")
  { printf '<rect x="8" y="8" width="200" height="200" fill="#ffffff"/><g transform="translate(8 8)">%s</g>' "$icon"
    printf '<rect x="216" y="8" width="200" height="200" fill="#0d1117"/><g transform="translate(216 8)">%s</g>' "$icon"
  } | { printf '<svg xmlns="http://www.w3.org/2000/svg" width="424" height="216" viewBox="0 0 424 216"><rect width="424" height="216" fill="#888888"/>'
        cat; printf '</svg>\n'; } | "$RSVG" -o "$OUT/kubernetes-precedent.png"
else
  echo "render-review.sh: could not fetch the Kubernetes icon; skipped its render" >&2
fi
