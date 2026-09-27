#!/bin/bash
# os.sh <tag> <r> — own-size @1440 on one cand2 stage run, with whatever canon.css the stage pack holds
T=$1; r=$2; set --; cd "$HOME/mnt/Projects--UX-design"; export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
mkdir -p $HOME/w5w/os-$T
python3 $HOME/w5a/knowledge/_validate_own_size.py $HOME/w5w/st/c2r$r/out/*.html --widths 1440 --json $HOME/w5w/os-$T/c2r$r.json > $HOME/w5w/os-$T/c2r$r.txt 2>&1; echo "c2r$r rc=$? $(grep -c . $HOME/w5w/os-$T/c2r$r.txt)"
