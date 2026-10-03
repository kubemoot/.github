#!/usr/bin/env bash
# Renders the account avatar (GitHub org and similar profile pictures) from the
# canonical mark: a solid Paper background, because avatars show on light and dark
# themes and a transparent mark's dark table would vanish on dark. Needs rsvg-convert.
set -euo pipefail
cd "$(dirname "$0")"
rsvg-convert --page-width 1024 --page-height 1024 -w 1024 -h 1024 \
  --background-color '#ffffff' kubemoot-mark.svg -o kubemoot-avatar-1024.png
