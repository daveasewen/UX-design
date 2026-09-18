#!/usr/bin/env python3
"""#282 wrap, step 2 — demote the #281 ★ LATEST banner heading to ★ PRIOR and insert the new
#282 ★ LATEST banner above it. Both moves through `knowledge/_gm_move.py`. The banner text is
held in ONE place (`banner282.py`) and was MEASURED against the `s241-D2` cap before this ran."""
import sys
import banner282
from run_ops import run

OLD281 = ("> ## ★ LATEST — 2026-09-17 (Thu **#281**, Fable 5.1, 6 Opus lanes, DELEGATED wrap "
          "— ★★ **THE ORPHAN PLAN, SIX RULINGS, AND THE BRAIN LEARNS WHY**)")
NEW281 = OLD281.replace("> ## ★ LATEST", "> ## ★ PRIOR", 1)

OPS = [
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [OLD281], "replace": [NEW281]},
    {"op": "insert", "file": "GOOD-MORNING.md", "at": NEW281, "where": "before",
     "lines": banner282.lines()},
]

if __name__ == "__main__":
    sys.exit(run("banner", OPS, write="--write" in sys.argv, min_bytes=2000))
