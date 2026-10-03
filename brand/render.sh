#!/usr/bin/env bash
# Regenerates every PNG (and the .ico) in brand/ from the hand-written SVG sources.
# Needs only rsvg-convert. The output is deterministic: run it after changing an SVG
# and commit the results together.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p avatar favicon

RSVG="${RSVG:-rsvg-convert}"
PAPER='#ffffff'

# render SRC SIZE OUT [BACKGROUND]: a square render, transparent unless a background is given.
render() {
  local src="$1" size="$2" out="$3" bg="${4:-}"
  local args=(-w "$size" -h "$size")
  if [[ -n "$bg" ]]; then
    args+=(--page-width "$size" --page-height "$size" --background-color "$bg")
  fi
  "$RSVG" "${args[@]}" "$src" -o "$out"
}

# Icons: transparent renders of each form at 1024 (the plain .png) and 512.
for form in color black white; do
  src="icon/$form/kubemoot-icon-$form.svg"
  render "$src" 1024 "icon/$form/kubemoot-icon-$form.png"
  render "$src" 512 "icon/$form/kubemoot-icon-$form-512.png"
done

# Lockups: the committed SVGs are authoritative. With WORDMARK_FONT_DIR pointing at the
# IBM Plex Sans OTFs (and fontTools and uharfbuzz installed), wordmark.py rebuilds them first.
if [[ -n "${WORDMARK_FONT_DIR:-}" ]]; then
  "${PYTHON:-python3}" wordmark.py "$WORDMARK_FONT_DIR"
fi
# Transparent renders by height: horizontal 512 px, stacked 1024 px.
for variant in color black white white-text; do
  "$RSVG" -h 512 "horizontal/$variant/kubemoot-horizontal-$variant.svg" \
    -o "horizontal/$variant/kubemoot-horizontal-$variant.png"
  "$RSVG" -h 1024 "stacked/$variant/kubemoot-stacked-$variant.svg" \
    -o "stacked/$variant/kubemoot-stacked-$variant.png"
done

# Avatar: the full-color icon on solid Paper, so it reads on light and dark profile themes.
for size in 1024 512; do
  render icon/color/kubemoot-icon-color.svg "$size" "avatar/kubemoot-avatar-$size.png" "$PAPER"
done

# Favicon PNGs: 32 px keeps the ring; 16 px uses the small form (solid table, no ring).
render favicon/kubemoot-favicon.svg 32 favicon/favicon-32.png
render favicon/kubemoot-favicon-small.svg 16 favicon/favicon-16.png

# favicon.ico: an ICO directory wrapping the two PNGs unchanged (PNG-in-ICO).
le16() { printf "\\x$(printf %02x $(($1 & 255)))\\x$(printf %02x $(($1 >> 8 & 255)))"; }
le32() { le16 $(($1 & 65535)); le16 $(($1 >> 16)); }
pngs=(favicon/favicon-16.png favicon/favicon-32.png)
sizes=(16 32)
{
  le16 0; le16 1; le16 ${#pngs[@]}
  offset=$((6 + 16 * ${#pngs[@]}))
  for i in "${!pngs[@]}"; do
    bytes=$(wc -c < "${pngs[$i]}")
    printf "\\x$(printf %02x "${sizes[$i]}")\\x$(printf %02x "${sizes[$i]}")\\x00\\x00"
    le16 1; le16 32; le32 "$bytes"; le32 "$offset"
    offset=$((offset + bytes))
  done
  for png in "${pngs[@]}"; do cat "$png"; done
} > favicon/favicon.ico
