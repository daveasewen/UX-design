#!/bin/bash
# views1.sh <variant> <r> — harness views + card on one cand2 run, clone harness + gate, R4C_RUNS redirected
V=$1; r=$2; set --; cd "$HOME/mnt/Projects--UX-design"; export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
cd $HOME/w5a; export R4C_RUNS=$HOME/w5w/runs-$V
python3 notes/_lanes/304/R4c/harness/score.py views --run-id cold-cand2-r$r --budget 165 2>&1 | tail -2
