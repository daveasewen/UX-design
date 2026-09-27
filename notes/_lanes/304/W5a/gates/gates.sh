#!/bin/bash
# gates.sh <tag> — receipt + screen gate (no --render) on the three cand2 page sets, pack-local
T=$1; export TMPDIR=/dev/shm/w5a-gates-$T; mkdir -p $TMPDIR; O=$HOME/w5w/g-$T; mkdir -p $O
for r in 1 2 3; do
  cd $HOME/w5w/st/c2r$r/pack; export TMPDIR=/dev/shm/w5a-gates-$T-$r; mkdir -p $TMPDIR
  for f in ../out/*.html; do python3 knowledge/_validate_receipt.py "$f" > $O/receipt-c2r$r-$(basename $f .html).txt 2>&1; done
  python3 knowledge/_validate_screen.py ../out/*.html > $O/screen-c2r$r.txt 2>&1; echo "c2r$r screen rc=$?"
done
