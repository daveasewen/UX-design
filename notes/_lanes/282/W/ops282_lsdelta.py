#!/usr/bin/env python3
"""#282 wrap, 2d — demote the #281 ⏱ LATEST DELTA heading to ⏱ PRIOR and insert the new
#282 ⏱ LATEST DELTA above it. Both moves through `knowledge/_gm_move.py`; the delta body is
authored in `delta282.md` and read from disk so exactly one copy of the text exists."""
import os, sys
from run_ops import run

HERE = os.path.dirname(os.path.abspath(__file__))
BODY = open(os.path.join(HERE, "delta282.md"), encoding="utf-8").read().rstrip("\n").split("\n")

OLD281 = ("## ⏱ LATEST DELTA — 2026-09-17 (Thu from `date`) (**#281**, ONE DAY, conductor "
          "**FABLE 5.1**, **6 OPUS LANE SEATS**, with this **OPUS 5** wrap sub, DELEGATED — ★★ "
          "**THE ORPHAN PLAN, SIX RULINGS, AND THE BRAIN LEARNS WHY**)")
NEW281 = OLD281.replace("## ⏱ LATEST DELTA", "## ⏱ PRIOR DELTA", 1)

OPS = [
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [OLD281], "replace": [NEW281]},
    {"op": "insert", "file": "_LIVE-STATE.md", "at": NEW281, "where": "before",
     "lines": BODY + [""]},
]

if __name__ == "__main__":
    sys.exit(run("lsdelta", OPS, write="--write" in sys.argv, min_bytes=2000))
