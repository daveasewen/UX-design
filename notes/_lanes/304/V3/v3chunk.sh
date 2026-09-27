#!/bin/bash
# usage: v3chunk.sh A B [clonedir]
cd ${3:-$HOME/clone304v3} || exit 9
export TMPDIR=/dev/shm
M=$HOME/mnt/Projects--UX-design
source knowledge/_render/seat_env.sh $M/outputs/_render-env >/dev/null 2>&1 || { echo SEAT_ENV FAIL; exit 8; }
echo "RENDER_SHELL=${RENDER_SHELL:+set}"
st=$(date +%s)
python3 knowledge/_build_survey.py --include-mutating --resume --timeout 60 --range $1:$2 > $HOME/v3logs/v3_after_$1_$2.log 2>&1
echo "rc=$? t=$(( $(date +%s)-st ))"
grep -E "^  [^ ]" $HOME/v3logs/v3_after_$1_$2.log | grep -v "✅" | head -20
grep -E "^SURVEY:" $HOME/v3logs/v3_after_$1_$2.log
