#!/usr/bin/env python3
"""#280 wrap — the ⏱ LATEST DELTA swap in `_LIVE-STATE.md`, through `_gm_move.py`:
  (1) #279's LATEST heading is demoted to PRIOR — a FULL-LINE replace, the only edit to it;
  (2) #280's delta block (`delta280.md`, held in ONE place and read from disk) is inserted
      BEFORE it, so newest-first ordering is by construction and not by an anchor guess.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_ops import run, ROOT

LS = os.path.join(ROOT, "_LIVE-STATE.md")
lines = open(LS, encoding="utf-8").read().split("\n")
old = [l for l in lines if l.startswith("## ⏱ LATEST DELTA — 2026-09-16 (Wed from `date`) (**#279**")]
assert len(old) == 1, ("LATEST heading", len(old))
old = old[0]
new = old.replace("## ⏱ LATEST DELTA", "## ⏱ PRIOR DELTA", 1)
assert new != old

block = open(os.path.join(HERE, "delta280.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert len(block) >= 10 and block[0].startswith("## ⏱ LATEST DELTA — 2026-09-17"), block[0][:60]
block = block + [""]

OPS = [
 {"op": "replace", "file": "_LIVE-STATE.md", "find": [old], "replace": [new]},
 {"op": "insert", "file": "_LIVE-STATE.md",
  "at": "## ⏱ PRIOR DELTA — 2026-09-16 (Wed from `date`) (**#279**", "where": "before",
  "lines": block},
]
print(f"delta280.md: {len(block)} lines, {sum(len(l) for l in block):,} chars")
sys.exit(run("lsdelta", OPS, write="--write" in sys.argv))
