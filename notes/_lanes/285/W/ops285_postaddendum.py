#!/usr/bin/env python3
"""#285 wrap — the two figures the 5b addendum MOVED, corrected BY ADDITION and each naming the cause.

⛔ THE #240 LESSON, MET A THIRD TIME IN ONE WRAP: a figure written before the step that moves it is
a PREDICTION, not a measurement. The `s214-D6` chain figure and the `size:` stamp were both taken
DECLARE-LAST — and then step 5b appended a post-wrap addendum to the ⏱ LATEST delta, which is
inside the chain slice. Neither figure is erased and neither is silently swapped; both readings
stand, with the cause named.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
from run_ops import run
import _gauge_tokens as G

chain = open(os.path.join(ROOT, "_CHAIN.md"), encoding="utf-8").read()
m = re.search(r"\*\*([\d,]+) tape \(cl100k ESTIMATE\) — the unit is THE WHOLE FILE\*\*", chain)
assert m, "REFUSED — the generated footer's figure did not parse"
tape = m.group(1)
pct = re.search(r"you have paid for\s*\n?\s*(\d+)% of it", chain)
assert pct, "REFUSED — the ratio did not parse"
ls_now, _ = G.count(open(os.path.join(ROOT, "_LIVE-STATE.md"), encoding="utf-8").read())

gm = os.path.join(ROOT, "GOOD-MORNING.md")
lines = [l.rstrip("\n") for l in open(gm, encoding="utf-8")]

s214 = [l for l in lines if l.startswith("> **⚠ `s214-D6` BANNER-DISCIPLINE MEASUREMENT")]
assert len(s214) == 1, len(s214)
s214_new = s214[0] + (
    f" ⛔ **AND THIS FIGURE WAS ITSELF MOVED BY STEP 5b, WHICH RAN AFTER IT — SO BOTH READINGS "
    f"STAND AND NEITHER IS ERASED.** The post-wrap addendum (the shipped sha, the push verdict and "
    f"the CI read) was appended to the ⏱ LATEST delta, which is INSIDE the chain slice, taking "
    f"`_CHAIN.md` from **9,307 tape to {tape}** and the chain/GM ratio from 27% to "
    f"**{pct.group(1)}%** — ✅ still GREEN against the generator's `<40%` floor, and ⛔ **the `0.40` "
    f"is Dave's constant and was not touched.** ★ **This is the #240 lesson met for the THIRD time "
    f"in one wrap** (the banner cap, the GENERATED residual line, and now this): a figure written "
    f"before the step that moves it is a PREDICTION. **{tape} is the figure the next session "
    f"actually pays.**")

stamp = [l for l in lines if l.startswith("> **size:**")]
assert len(stamp) == 1, len(stamp)
stamp_new = stamp[0] + (
    f" ⛔ **AND ONE MORE DRIFT IS DECLARED RATHER THAN DISCOVERED: STEP 5b RAN AFTER THIS STAMP.** "
    f"The post-wrap addendum appended to the ⏱ LATEST delta takes `_LIVE-STATE.md` from the "
    f"**66,940** measured above to **{ls_now:,}** — **{ls_now-66940:+,} tape**, well inside the "
    f"stamp's 10% grading tolerance, and GM is unmoved by it. **The stamp is NOT re-taken**, for "
    f"the same reason the `s214-D6` note gives: saying so is cheaper and truer than a second "
    f"reading nobody can reconcile.")

print(f"chain after 5b: {tape} tape · ratio {pct.group(1)}% · LS {ls_now:,} (was 66,940)")
ops = [
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [s214[0]], "replace": [s214_new]},
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [stamp[0]], "replace": [stamp_new]},
]
sys.exit(run("postaddendum", ops, write="--write" in sys.argv, min_bytes=1_000))
