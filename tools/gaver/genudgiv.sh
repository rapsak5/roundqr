#!/bin/sh
# Lægger gavesider tilbage på roundqr.dk præcis som de var 13. november 2026.
# Brug:  sh tools/gaver/genudgiv.sh            (alle 342 sider)
#        sh tools/gaver/genudgiv.sh dm glasgow (kun de nævnte)
# Kør fra roden af repo'et. Scriptet committer, men pusher ikke. Push selv bagefter.
set -e
TAG=gavesider-online-2026-11-13
git fetch --depth=1 origin "refs/tags/$TAG:refs/tags/$TAG"
if [ $# -eq 0 ]; then set -- $(cat tools/gaver/nedtagne-sider.txt); fi
for s in "$@"; do
  grep -qx "$s" tools/gaver/nedtagne-sider.txt || { echo "Ukendt side: $s"; exit 1; }
  git checkout "$TAG" -- "$s"
done
git commit -qm "Genudgiv gavesider: $*" -- "$@"
echo "Klar. Kør: git push origin main"
