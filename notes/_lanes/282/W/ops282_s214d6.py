#!/usr/bin/env python3
"""#282 wrap — substitute the `s214-D6` BANNER-DISCIPLINE MEASUREMENT into the #282 stratum,
QUOTED from `_CHAIN.md`'s generated footer and read AFTER the declare-last `size:` stamp
(the #241 clause: the stamp is itself inside the chain slice)."""
import sys
from run_ops import run

FILL = ("**`_CHAIN.md` reads 9,801 tape (cl100k ESTIMATE) — the WHOLE FILE, this generator's own wrapper "
 "included: slice 8,954 + wrapper 847, at a fixed point in 2 passes.** ✅ **THAT IS INSIDE THE ~10–12K REAL "
 "TARGET `s214-D6` SETS, and DOWN from #281's reading** — the capped banner and the rolled #280 banner both "
 "paid for it. The generator's own ratio line reads **28% of `GOOD-MORNING.md` (34,581 tape) paid for at "
 "boot**, against its `<40%` floor — ✅ **not red, and it was red at #225.** ⚠ **GM reads 34,581 here against "
 "the `size:` stamp's 34,681 taken minutes earlier** — the generator rewrites its own verdict placeholder in "
 "GM as it runs, so the two readings describe the file before and after that substitution; **0.29%, against a "
 "10% tolerance, and both are published rather than one being quietly replaced.** ⛔ **THE #240 DEFECT IS "
 "RE-DECLARED AND IS STILL NOT REPAIRED:** `grep -c 'BANNER-DISCIPLINE MEASUREMENT' notes/_GAUGE-LOG.md` and "
 "the newest ORDINAL NAMED in that file disagree — the count is re-derivable, the naming is not. Both are "
 "reported; no third figure is invented.")


def old_line():
    for ln in open("/sessions/tender-hopeful-allen/mnt/UX-design/GOOD-MORNING.md", encoding="utf-8"):
        if "{S214D6}" in ln:
            return ln.rstrip("\n")
    raise SystemExit("REFUSED — no {S214D6} placeholder found")


if __name__ == "__main__":
    o = old_line()
    OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [o],
            "replace": [o.replace("{S214D6}", FILL)]}]
    sys.exit(run("s214d6", OPS, write="--write" in sys.argv, min_bytes=800))
