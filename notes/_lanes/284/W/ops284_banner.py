#!/usr/bin/env python3
"""#284 wrap — step 2c(ii): DEMOTE #283's ★ LATEST banner heading to ★ PRIOR and INSERT the
new ★ LATEST #284 banner above it, through `knowledge/_gm_move.py`.

The banner text is built and MEASURED by `banner284.py` against the gate's own `s241-D2`
cap (10 substantive lines / 1,200 tape). The `residual (GENERATED #284)` line carries a
placeholder here and is substituted by `ops284_genline.py` AFTER 2f, exactly as #283 did —
`_roll_state.py` cannot report the roll state until the roll has happened.
"""
import sys
from run_ops import run
from banner284 import banner

OLD = ("> ## ★ LATEST — 2026-09-18 (Fri **#283**, Fable 5.1, NO lanes cut, DELEGATED wrap — "
       "★★ **THE SEAM CHECK IS BORN AND STOPS ITS OWN SESSION; THE DISK IS DIAGNOSED**)")
NEW = OLD.replace("> ## ★ LATEST —", "> ## ★ PRIOR —", 1)

TEXT = banner("PENDING — substituted after 2f by ops284_genline.py")
LINES = TEXT.split("\n")
assert LINES[0].startswith("> ## ★ LATEST — 2026-09-18 (Fri **#284**")
assert len([l for l in LINES if l.strip() not in ("", ">")]) == 10

OPS = [
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [OLD], "replace": [NEW]},
    {"op": "insert", "file": "GOOD-MORNING.md", "at": NEW, "where": "before",
     "lines": LINES + [""]},
]

if __name__ == "__main__":
    sys.exit(run("banner", OPS, write="--write" in sys.argv, min_bytes=1500))
