#!/usr/bin/env python3
"""#284 wrap — step 1 / 2d second half on `_LIVE-STATE.md`, through `_gm_move.py`:

  1. DEMOTE #283's `## ⏱ LATEST DELTA` heading to `## ⏱ PRIOR DELTA` (one full-line replace).
  2. INSERT the new ⏱ LATEST DELTA #284 block (read VERBATIM from `lsdelta284.md`) above it.

The `Last refreshed:` line is a separate transaction — `lastrefreshed284.py` — because the
#280 chain segment it trims must be extracted and asserted in the writing process first.
"""
import os, sys
from run_ops import run

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = ("## ⏱ LATEST DELTA — 2026-09-18 (Fri from `date`) (**#283**, ✅ **ONE DAY, NO DATE SPLIT**, "
       "conductor **FABLE 5.1**, **NO LANE SEATS — none were cut**, with this **OPUS 5** wrap sub, "
       "DELEGATED — ★★ **THE SEAM CHECK IS BORN AND STOPS ITS OWN SESSION; THE DISK IS DIAGNOSED**)")
NEW = OLD.replace("## ⏱ LATEST DELTA", "## ⏱ PRIOR DELTA", 1)

block = open(os.path.join(HERE, "lsdelta284.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert block[0].startswith("## ⏱ LATEST DELTA — 2026-09-18"), block[0][:60]
assert len(block) >= 10, len(block)

OPS = [
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [OLD], "replace": [NEW]},
    {"op": "insert", "file": "_LIVE-STATE.md", "at": NEW, "where": "before",
     "lines": block + [""]},
]

if __name__ == "__main__":
    sys.exit(run("lsdelta", OPS, write="--write" in sys.argv, min_bytes=600))
