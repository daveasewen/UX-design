#!/bin/bash
# os.sh <tag> <dir-with-out> <name> — W6: own-size @1440 on a staged cand2 run (the stage pack's canon/engine)
T=$1; D=$2; N=$3; set --; cd "$HOME/mnt/Projects--UX-design"; export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
mkdir -p $HOME/w6w/os-$T
python3 $HOME/w6/knowledge/_validate_own_size.py $(ls $D/out/*.html | grep -v USED) --widths 1440 --json $HOME/w6w/os-$T/$N.json > $HOME/w6w/os-$T/$N.txt 2>&1; echo "$T $N rc=$? $(grep -E '^(ADVISORY|PASS|FAIL|own-size)' $HOME/w6w/os-$T/$N.txt | tail -1)"
