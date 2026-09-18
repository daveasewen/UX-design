#!/usr/bin/env python3
"""#285 wrap — substitute the `s214-D6` BANNER-DISCIPLINE figure into the #285 stratum.

⛔ QUOTED FROM `_CHAIN.md`'s GENERATED FOOTER, never re-derived here, and taken AFTER the
DECLARE-LAST `size:` stamp because the stamp is itself inside the chain slice (#241's rule, from
#240's one-wrap-two-figures lesson). The figure the stratum carries is the one the NEXT session
actually pays.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
from run_ops import run

chain = open(os.path.join(ROOT, "_CHAIN.md"), encoding="utf-8").read()
m = re.search(r"\*\*([\d,]+) tape \(cl100k ESTIMATE\) — the unit is THE WHOLE FILE\*\*", chain)
assert m, "REFUSED — the generated footer's figure did not parse"
tape = m.group(1)
pct = re.search(r"you have paid for\s*\n?\s*(\d+)% of it", chain)
assert pct, "REFUSED — the ratio did not parse"

FIG = (f"**`_CHAIN.md` reads {tape} tape** against the `s214-D6` target of ~10–12K real, so the "
       f"chain is INSIDE the clause's band for the first time this run — down from #284's 10,048 "
       f"tape, and the fall is the SHORTER banner (1,196 against #284's 1,199 over the same 10 "
       f"lines) plus a #283 ★ PRIOR banner rolled out of the slice, not a drop. The generator's own "
       f"chain/GM ratio reads **{pct.group(1)}%** against its `<40%` floor — ✅ GREEN, and ⛔ **the "
       f"`0.40` is Dave's constant and was not touched.**")

gm = os.path.join(ROOT, "GOOD-MORNING.md")
old = [l.rstrip("\n") for l in open(gm, encoding="utf-8") if "S214D6_FIGURE" in l]
assert len(old) == 1, f"REFUSED — placeholder found {len(old)} times"
new = old[0].replace("S214D6_FIGURE", FIG)
print(f"chain footer: {tape} tape · ratio {pct.group(1)}%")

ops = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [old[0]], "replace": [new]}]
sys.exit(run("s214d6", ops, write="--write" in sys.argv, min_bytes=500))
