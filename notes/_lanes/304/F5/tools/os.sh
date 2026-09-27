#!/bin/bash
# os.sh <side> <r> — own-size @1440 on one staged cand2 run
S=$1; r=$2; set --; cd "$HOME/mnt/Projects--UX-design"; export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
mkdir -p $HOME/f5m/os-$S; st=$(date +%s)
python3 $HOME/f5w/knowledge/_validate_own_size.py $HOME/f5st/$S/c2r$r/out/*.html --widths 1440 --json $HOME/f5m/os-$S/c2r$r.json > $HOME/f5m/os-$S/c2r$r.txt 2>&1; echo "$S c2r$r rc=$? t=$(( $(date +%s)-st )) $(grep -E '^(ADVISORY|OWN-SIZE|RESULT)' $HOME/f5m/os-$S/c2r$r.txt | head -3)"
