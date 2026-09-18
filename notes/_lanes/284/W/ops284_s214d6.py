#!/usr/bin/env python3
"""#284 wrap — substitute the `{{S214D6}}` placeholder in the #284 stratum with the
BANNER-DISCIPLINE MEASUREMENT, QUOTED from `_CHAIN.md`'s generated footer and read AFTER the
declare-last `size:` stamp landed (the #241 clause). The stratum is in §C, OUTSIDE the chain
slice, so this substitution cannot make `_CHAIN.md` stale."""
import sys
from run_ops import run
NEW = ("**`_CHAIN.md` regenerates at 9,224 tape** (slice 8,377 + generated wrapper 847), against "
 "#283's **9,324** — **100 SMALLER**, ✅ **UNDER the `s214-D6` 10–12K target rather than merely "
 "inside it**, and at **26.7% of GM's 34,533** against the generator's own `<40%` floor, ✅ not red. "
 "⚠ **The wrapper is 847 of those 9,224 — a FIXED cost in the numerator only, which no edit to GM or "
 "`_LIVE-STATE.md` can move**, and it is the remaining lever inside the machinery "
 "(`notes/_subreports/2026-08-30-225-carries-home.md` § RULING-SHAPED QUESTIONS, priced and open). "
 "⛔ **AND THE #240 DISCREPANCY IS RE-MEASURED AND STILL NOT REPAIRED: "
 "`grep -c 'BANNER-DISCIPLINE MEASUREMENT' notes/_GAUGE-LOG.md` reads 72 while the newest ORDINAL "
 "NAMED in that file disagrees with it — the count is re-derivable and the naming is not, so both are "
 "reported and NO THIRD FIGURE IS INVENTED.**")
OPS = [{"op": "replace", "file": "GOOD-MORNING.md",
        "find": None, "replace": None}]
if __name__ == "__main__":
    import os
    ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
    gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read().split("\n")
    old = [l for l in gm if "{{S214D6}}" in l]
    assert len(old) == 1, len(old)
    OPS[0]["find"] = [old[0]]
    OPS[0]["replace"] = [old[0].replace("{{S214D6}}", NEW)]
    sys.exit(run("s214d6", OPS, write="--write" in sys.argv, min_bytes=500))
