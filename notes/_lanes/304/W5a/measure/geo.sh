#!/bin/bash
# geo.sh <side> <from> <to> — geometry gate @1440 on pages [from,to) of the list (showroom/*.html + 13 test pages + 14 chart snippets)
S=$1; F=$2; T=$3; set --; cd "$HOME/mnt/Projects--UX-design"; export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
if [ "$S" = before ]; then TREE=$HOME/w5b4; G=$HOME/w5a/knowledge/_vgeo_head_w5a.py; else TREE=$HOME/w5a; G=$HOME/w5a/knowledge/_validate_geometry.py; fi
cd $TREE; L=$( (ls showroom/*.html; ls knowledge/_tests/chart-engine/*.html; ls knowledge/snippets/Chart-*.reference.html knowledge/snippets/Template-dashboard-bento.reference.html) | sed -n "$((F+1)),${T}p")
mkdir -p $HOME/w5w/geo-$S; python3 $G $L --widths 1440 --json $HOME/w5w/geo-$S/c$F.json > $HOME/w5w/geo-$S/c$F.txt 2>&1; echo "$S $F-$T rc=$? $(echo $L | wc -w) pages"
