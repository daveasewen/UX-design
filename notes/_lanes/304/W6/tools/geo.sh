#!/bin/bash
# geo.sh <side> <from> <to> — W6: geometry gate @1440 on pages [from,to) of (showroom/*.html + chart test pages + 14 chart snippets + bento + _fitness-test/*.html), in $HOME/w6 as it stands
S=$1; F=$2; T=$3; set --; cd "$HOME/mnt/Projects--UX-design"; export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
cd $HOME/w6; L=$( (ls showroom/*.html; ls knowledge/_tests/chart-engine/*.html; ls knowledge/snippets/Chart-*.reference.html knowledge/snippets/Template-dashboard-bento.reference.html; ls knowledge/_fitness-test/*.html) | sed -n "$((F+1)),${T}p")
mkdir -p $HOME/w6w/geo-$S; python3 knowledge/_validate_geometry.py $L --widths 1440 --json $HOME/w6w/geo-$S/c$F.json > $HOME/w6w/geo-$S/c$F.txt 2>&1; echo "$S $F-$T rc=$? $(echo $L | wc -w) pages"
