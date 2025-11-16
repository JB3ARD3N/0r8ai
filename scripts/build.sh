#!/usr/bin/env bash
set -euo pipefail

OUTDIR=dist
mkdir -p "$OUTDIR"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
ZIPFILE="$OUTDIR/orb-dist-$TIMESTAMP.zip"

# Include app, spells, README if they exist
FILES=()
[ -d app ] && FILES+=(app)
[ -d spells ] && FILES+=(spells)
[ -f README.md ] && FILES+=(README.md)

if [ ${#FILES[@]} -eq 0 ]; then
  echo "No content to package" >&2
  exit 1
fi

zip -r "$ZIPFILE" "${FILES[@]}"

echo "Created $ZIPFILE"
