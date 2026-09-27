#!/bin/bash
# os2.sh <side> — own-size + geometry @1440 on the 13 chart test pages and the _fitness-test canon screens
S=$1; set --; cd "$HOME/mnt/Projects--UX-design"; export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
if [ "$S" = before ]; then TREE=$HOME/w5b4; else TREE=$HOME/w5a; fi
cd $TREE; mkdir -p $HOME/w5w/os2-$S
python3 $HOME/w5a/knowledge/_validate_own_size.py knowledge/_tests/chart-engine/*.html knowledge/_fitness-test/*.html --widths 1440 --json $HOME/w5w/os2-$S/os.json > $HOME/w5w/os2-$S/os.txt 2>&1; echo "own-size $S rc=$? $(grep ^ADVISORY $HOME/w5w/os2-$S/os.txt)"
