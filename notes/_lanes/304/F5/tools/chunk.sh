#!/bin/bash
# usage: chunk.sh A B — F5 survey chunk in the fresh clone (V5's v5chunk.sh, paths changed)
cd $HOME/f5s || exit 9
export TMPDIR=/dev/shm
M=$HOME/mnt/Projects--UX-design
source knowledge/_render/seat_env.sh $M/outputs/_render-env >/dev/null 2>&1 || { echo SEAT_ENV FAIL; exit 8; }
st=$(date +%s)
python3 knowledge/_build_survey.py --include-mutating --resume --timeout 60 --range $1:$2 > $HOME/f5m/survey/after_$1_$2.log 2>&1
echo "rc=$? t=$(( $(date +%s)-st ))"
grep -E "^  [^ ]" $HOME/f5m/survey/after_$1_$2.log | grep -v "✅" | head -20
grep -E "^SURVEY:" $HOME/f5m/survey/after_$1_$2.log
