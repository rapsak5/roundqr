#!/bin/bash
mkdir -p /home/claude/gaver/test
# build.sh slug...  bygger, kopierer og tester
rm -rf /tmp/ud && SITE=1 python3 tools/build_brand.py tools/gaver/kommuner/brands.json /tmp/ud "$@" | tail -n +1
for s in "$@"; do mkdir -p $s; f=/tmp/ud/roundqr-$s.html; cp "$f" $s/index.html; done
python3 tools/gaver/check.py $(for s in "$@"; do echo $PWD/$s/index.html; done)
grep -c noindex $(for s in "$@"; do echo $s/index.html; done)
