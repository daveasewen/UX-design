#!/bin/bash
S=$1; set --; cd "$HOME/mnt/Projects--UX-design"; export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
if [ "$S" = before ]; then TREE=$HOME/w5b4; G=$HOME/w5a/knowledge/_vgeo_head_w5a.py; else TREE=$HOME/w5a; G=$HOME/w5a/knowledge/_validate_geometry.py; fi
cd $TREE; mkdir -p $HOME/w5w/geo2-$S; python3 $G knowledge/_fitness-test/*.html --widths 1440 --json $HOME/w5w/geo2-$S/ft.json > $HOME/w5w/geo2-$S/ft.txt 2>&1; echo "$S rc=$?"
