#!/bin/bash
# usage: chunk.sh A B — W6 survey chunk in the fresh clone $HOME/w6s (F5's chunk.sh, paths changed)
cd $HOME/w6s || exit 9
export TMPDIR=/dev/shm
M=$HOME/mnt/Projects--UX-design
source knowledge/_render/seat_env.sh $M/outputs/_render-env >/dev/null 2>&1 || { echo SEAT_ENV FAIL; exit 8; }
st=$(date +%s)
python3 knowledge/_build_survey.py --include-mutating --resume --timeout 60 --range $1:$2 > $HOME/w6m/survey/after_$1_$2.log 2>&1
echo "rc=$? t=$(( $(date +%s)-st ))"
grep -E "^  [^ ]" $HOME/w6m/survey/after_$1_$2.log | grep -v "✅" | head -20
grep -E "^SURVEY:" $HOME/w6m/survey/after_$1_$2.log
