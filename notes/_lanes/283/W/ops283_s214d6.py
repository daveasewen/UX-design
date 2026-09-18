#!/usr/bin/env python3
"""#283 wrap — substitute the `s214-D6` banner-discipline measurement into the stratum, QUOTED
from `_CHAIN.md`'s generated footer and read AFTER the declare-last `size:` stamp (#241 clause)."""
import sys
from run_ops import run
OLD = "> **⚠ `s214-D6` BANNER-DISCIPLINE MEASUREMENT — QUOTED FROM `_CHAIN.md`'s GENERATED FOOTER, NEVER RE-DERIVED, AND READ AFTER THE DECLARE-LAST `size:` STAMP** (the #241 clause: the stamp is itself inside the chain slice, so a wrap that shortens its banner can still hand the next session a BIGGER chain through its header). {S214D6}"
NEW = (OLD.replace("{S214D6}",
  "**`_CHAIN.md` regenerates at 9,324 tape — slice 8,478 + the generator's own 846-tape wrapper — "
  "against #282's 9,801, so the chain this wrap hands #284 is 477 tape SMALLER even though GM grew.** "
  "✅ **INSIDE the `s214-D6` 10–12K target and BELOW it**, and at **26.7% of GM against `_gen_chain.py`'s "
  "`<40%` floor** — not red. ⛔ **AND THE #240 DISCREPANCY IS RE-REPORTED, NOT RESOLVED: "
  "`grep -c 'BANNER-DISCIPLINE MEASUREMENT' notes/_GAUGE-LOG.md` and the newest ORDINAL NAMED in that file "
  "still disagree by two — the count is re-derivable and the naming is not, so both are reported and no "
  "third figure is invented.**"))
OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [OLD], "replace": [NEW]}]
if __name__ == "__main__":
    sys.exit(run("s214d6", OPS, write="--write" in sys.argv, min_bytes=500))
