#!/bin/sh
# Bygger, kopierer og tester LinkedIn-brandsider (ja tak).
# Brug: sh tools/gaver/linkedin/ny.sh slug [slug ...]
# Kræver: brandet i tools/gaver/linkedin/brands.json, logo i linkedin/logos/<slug>.png, mærke i marks/<slug>.png (eller "none").
# Skrifter: FONTSOURCE peger på node_modules/@fontsource (npm i @fontsource/<navn>).
set -e
cd "$(dirname "$0")/../../.."
[ -n "$FONTSOURCE" ] || FONTSOURCE=/tmp/fs/node_modules/@fontsource
export FONTSOURCE
python3 tools/build.py >/dev/null
git checkout -q sitemap.xml 2>/dev/null || true
rm -rf /tmp/ud
SITE=1 python3 tools/build_brand.py tools/gaver/linkedin/brands.json /tmp/ud "$@"
mkdir -p /home/claude/gaver/test
for s in "$@"; do
  mkdir -p "$s"; cp "/tmp/ud/roundqr-$s.html" "$s/index.html"
  grep -q noindex "$s/index.html" && echo "$s: noindex ok" || echo "$s: MANGLER noindex"
done
python3 tools/gaver/check.py $(for s in "$@"; do echo "$PWD/$s/index.html"; done)
