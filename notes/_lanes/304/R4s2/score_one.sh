#!/bin/bash
# score_one.sh <cand2-rN> — one resumable seat call of the W4b harness on a candidate-2 cold run.
# Writes only under notes/_lanes/304/R4s2/runs (R4C_RUNS); stage lives at $HOME/r4c/stage/cold-<run>.
R=$1; shift
cd "$HOME/mnt/Projects--UX-design"
export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh
export R4C_RUNS="$PWD/notes/_lanes/304/R4s2/runs"
python3 notes/_lanes/304/R4c/harness/score.py all --run-id cold-$R --kind "cold run" --label "$R" \
  --pack notes/_lanes/304/R4a/cand/Apollo-Spider-v1.0.14-candidate-2.zip \
  --copy-out notes/_lanes/304/R4c/cold/$R/out --page notes/_lanes/304/R4c/cold/$R/out/index.html --budget 150 2>&1 | tail -25
