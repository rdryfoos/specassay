#!/usr/bin/env bash
# Build distributable zips for SpecAssay preset, check extension, and bundle.
#
# Each component carries its own version and is named from its own manifest,
# the same way .github/workflows/release.yml does it. They drift on purpose:
# the preset can sit at 0.2.1 while the bundle is at 0.3.2. A single shared
# version for all three is what produced specassay-preset-0.3.2.zip, a file
# no catalog points at.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"

if [[ $# -gt 0 ]]; then
  echo "error: this script takes no arguments." >&2
  echo "Versions come from bundle.yml, extension.yml, and preset.yml." >&2
  exit 2
fi

# Read a manifest's own version: the first two-space-indented version key.
manifest_version() {
  awk '/^  version:/{gsub(/"/,""); print $2; exit}' "$1"
}

BUNDLE_V="$(manifest_version "$ROOT/bundle.yml")"
EXT_V="$(manifest_version "$ROOT/extensions/specassay-check/extension.yml")"
PRE_V="$(manifest_version "$ROOT/presets/specassay/preset.yml")"

for pair in "bundle:$BUNDLE_V" "extension:$EXT_V" "preset:$PRE_V"; do
  [[ -n "${pair#*:}" ]] || { echo "error: no version found for ${pair%%:*}" >&2; exit 1; }
done
echo "Versions: bundle $BUNDLE_V · extension $EXT_V · preset $PRE_V"

rm -rf "$DIST"
mkdir -p "$DIST"

# Preset zip: preset.yml at archive root (or single top-level dir)
(
  cd "$ROOT/presets/specassay"
  zip -qr "$DIST/specassay-preset-${PRE_V}.zip" . -x '*.DS_Store' -x '*__pycache__*'
)

# Extension zip: extension.yml at archive root
(
  cd "$ROOT/extensions/specassay-check"
  zip -qr "$DIST/specassay-check-${EXT_V}.zip" . -x '*.DS_Store' -x '*__pycache__*'
)

# Bundle artifact via Spec Kit, which names it from bundle.yml itself
specify bundle build --path "$ROOT" --output "$DIST"

# The catalogs are what an adopter actually resolves, so a zip whose name no
# catalog references is a release that 404s on install. Check before publishing.
status=0
for expected in \
  "specassay-preset-${PRE_V}.zip" \
  "specassay-check-${EXT_V}.zip" \
  "specassay-${BUNDLE_V}.zip"; do
  if [[ ! -f "$DIST/$expected" ]]; then
    echo "MISSING: $expected was not built" >&2
    status=1
  elif ! grep -qr "$expected" "$ROOT/catalogs/"; then
    echo "UNREFERENCED: $expected is built but no catalog download_url names it" >&2
    status=1
  fi
done

echo "Built:"
ls -la "$DIST"
if [[ $status -ne 0 ]]; then
  echo >&2
  echo "Refusing to call this a good release: fix catalogs/*.json or the" >&2
  echo "manifest versions so the artifacts and the catalog entries agree." >&2
  exit $status
fi
echo "Artifacts and catalog download URLs agree."
