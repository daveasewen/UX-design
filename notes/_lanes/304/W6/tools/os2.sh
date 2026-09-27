#!/bin/bash
# os2.sh <side> — W6: own-size @1440 on the chart test pages + _fitness-test screens, $HOME/w6 as it stands
S=$1; set --; cd "$HOME/mnt/Projects--UX-design"; export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
cd $HOME/w6; mkdir -p $HOME/w6w/os2-$S
python3 knowledge/_validate_own_size.py knowledge/_tests/chart-engine/*.html knowledge/_fitness-test/*.html --widths 1440 --json $HOME/w6w/os2-$S/os.json > $HOME/w6w/os2-$S/os.txt 2>&1; echo "own-size $S rc=$? $(grep ^ADVISORY $HOME/w6w/os2-$S/os.txt)"
