#!/bin/bash
# drive.sh <page> ... — W6: re-drive chart-engine receipts in the clone via R3's shim
A=("$@"); set --
cd "$HOME/mnt/Projects--UX-design"; export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh >/dev/null 2>&1; source knowledge/_render/seat_env.sh >/dev/null
cd $HOME/w6; ARGS=(); for p in "${A[@]}"; do ARGS+=(--page "$p"); done
python3 notes/_lanes/304/R3/drive_shim.py "${ARGS[@]}" 2>&1 | tail -4
