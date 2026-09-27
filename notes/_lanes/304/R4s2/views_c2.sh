#!/bin/bash
# views_c2.sh <run-id>... — W4b views phase on the six earlier runs restaged on candidate-2 canon (R4s2 comparison c)
cd "$HOME/mnt/Projects--UX-design"; IDS="$@"; set --
export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
export R4C_RUNS="$PWD/notes/_lanes/304/R4s2/runs-c2canon"
for r in $IDS; do python3 notes/_lanes/304/R4c/harness/score.py views --run-id $r --budget 80 2>&1 | tail -2; done
