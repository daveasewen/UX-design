# build -> mint -> receipt + screen gates for every page (records to our own TMPDIR)
W=$HOME/cold/cand2-r3; cd $W && python3 tools/build.py x >/dev/null || exit 1
cd $W/pack
for p in index accounts liquidity payments fx risk trade reports messages settings; do
  python3 knowledge/gen_provenance_receipt.py --mint ../out/$p.html >/dev/null 2>&1 || echo "MINT FAIL $p"
  TMPDIR=$W/tmp SCREEN_GATE_REBIND=1 python3 knowledge/_validate_screen.py ../out/$p.html > $W/tmp/screen-$p.txt 2>&1; rc=$?
  echo "$p screen_exit=$rc :: $(grep -E '^- (receipt|compose|composition|icon-source|a11y):' $W/tmp/screen-$p.txt | sed 's/ — .*//' | tr '\n' '|')"
done
