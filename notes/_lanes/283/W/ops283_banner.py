#!/usr/bin/env python3
"""#283 wrap, step 2 — demote the #282 ★ LATEST banner heading to ★ PRIOR and insert the new
#283 ★ LATEST banner above it. Both moves through `knowledge/_gm_move.py`. The banner text is
held in ONE place (`banner283.py`) and was MEASURED against the `s241-D2` cap before this ran."""
import sys
import banner283
from run_ops import run

OLD282 = ("> ## ★ LATEST — 2026-09-18 (Fri **#282**, Fable 5.1, 3 Opus lanes, DELEGATED wrap "
          "— ★★ **THE RULE NOTES LAND, THE LOGO IS RULED, THE GRAPH'S PHILOSOPHY IS PUT**)")
NEW282 = OLD282.replace("> ## ★ LATEST", "> ## ★ PRIOR", 1)

OPS = [
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [OLD282], "replace": [NEW282]},
    {"op": "insert", "file": "GOOD-MORNING.md", "at": NEW282, "where": "before",
     "lines": banner283.lines()},
]

if __name__ == "__main__":
    sys.exit(run("banner", OPS, write="--write" in sys.argv, min_bytes=2000))
