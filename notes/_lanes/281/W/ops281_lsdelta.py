#!/usr/bin/env python3
"""#281 wrap, step 1 — `_LIVE-STATE.md`: demote #280's ⏱ LATEST DELTA heading to ⏱ PRIOR DELTA
and insert #281's delta block (`delta281.md`) before it. Through `_gm_move.py`, never by hand."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_ops import run, ROOT

block = open(os.path.join(HERE, "delta281.md"), encoding="utf-8").read().split("\n")
LS = os.path.join(ROOT, "_LIVE-STATE.md")
txt = open(LS, encoding="utf-8").read().split("\n")
old = [l for l in txt if l.startswith("## ⏱ LATEST DELTA — 2026-09-17 (Thu from `date`) (**#280**")]
assert len(old) == 1, ("LATEST DELTA heading", len(old))
old = old[0]
new = old.replace("## ⏱ LATEST DELTA", "## ⏱ PRIOR DELTA", 1)
assert new != old

OPS = [
 {"op": "replace", "file": "_LIVE-STATE.md", "find": [old], "replace": [new]},
 {"op": "insert", "file": "_LIVE-STATE.md",
  "at": "## ⏱ PRIOR DELTA — 2026-09-17 (Thu from `date`) (**#280**", "where": "before",
  "lines": block},
]
sys.exit(run("lsdelta", OPS, write="--write" in sys.argv))
