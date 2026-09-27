#!/bin/bash
# usage: chunk.sh A B tree tag
cd $3 || exit 9
export TMPDIR=/dev/shm
M=$HOME/mnt/Projects--UX-design
source knowledge/_render/seat_env.sh $M/outputs/_render-env >/dev/null 2>&1 || { echo SEAT_ENV FAIL; exit 8; }
st=$(date +%s)
python3 knowledge/_build_survey.py --include-mutating --resume --timeout 60 --range $1:$2 > $HOME/w4a/logs/$4_$1_$2.log 2>&1
echo "rc=$? t=$(( $(date +%s)-st ))"
grep -E "^  [^ ]" $HOME/w4a/logs/$4_$1_$2.log | grep -v "✅" | head -20
grep -E "^SURVEY:" $HOME/w4a/logs/$4_$1_$2.log
