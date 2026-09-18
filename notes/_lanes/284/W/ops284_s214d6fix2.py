#!/usr/bin/env python3
"""#284 wrap — the `s214-D6` figure RE-READ a third time, after the 5b addendum landed in the
⏱ LATEST DELTA. This is the #241 clause biting exactly as it says it will: a wrap that wrote a
1,199-tape banner still hands the next session a BIGGER chain, because 5b's home is inside the
chain slice. The final reading is the one the stratum carries."""
import os, sys
from run_ops import run
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
PAIRS = [("**`_CHAIN.md` regenerates at 9,255 tape** (slice 8,408 + generated wrapper 847), against "
          "#283's **9,324** — **69 SMALLER**",
          "**`_CHAIN.md` regenerates at 10,048 tape** (slice 9,200 + generated wrapper 848), against "
          "#283's **9,324** — **724 BIGGER**. ⚠ **IT READ 9,255 — 69 SMALLER — BEFORE THE 5b ADDENDUM, "
          "AND THE ADDENDUM'S HOME IS INSIDE THE CHAIN SLICE: this is the #241 clause biting exactly "
          "as it says it will, and the FINAL reading is the one this stratum carries.** A wrap that "
          "wrote a 1,199-tape banner still hands the next session a bigger chain"),
         ("at **26.6% of GM's 34,845**", "at **28.8% of GM's 34,845**"),
         ("⚠ **The wrapper is 847 of those 9,255", "⚠ **The wrapper is 848 of those 10,048")]
lines = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read().split("\n")
hits = [l for l in lines if PAIRS[0][0] in l]
assert len(hits) == 1, len(hits)
new = hits[0]
for a, b in PAIRS:
    assert a in new, a[:40]
    new = new.replace(a, b)
OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [hits[0]], "replace": [new]}]
if __name__ == "__main__":
    sys.exit(run("s214d6fix2", OPS, write="--write" in sys.argv, min_bytes=500))
