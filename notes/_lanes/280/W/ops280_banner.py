#!/usr/bin/env python3
"""#280 wrap — the ★ LATEST banner swap in `GOOD-MORNING.md`, through `_gm_move.py`:
  (1) #279's ★ LATEST heading is demoted to ★ PRIOR — a FULL-LINE replace, the only edit to it;
  (2) #280's banner (`banner280.py`, held in ONE place and MEASURED first) is inserted BEFORE it.
The banner's own measurement is printed here before the mover is called, so the `s241-D2` cap is
read rather than hoped for.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_ops import run, ROOT
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg
import banner280

ROLLSTATE = sys.argv[sys.argv.index("--rollstate") + 1] if "--rollstate" in sys.argv else None
kw = {"rollstate": ROLLSTATE} if ROLLSTATE else {}
block = banner280.lines(**kw)
sub = [l for l in block if l.strip() and l.strip() != ">"]
tape = cg.measure_tokens("\n".join(block))[0]
print(f"BANNER: {tape:,} tape / {len(sub)} substantive lines "
      f"(cap {cg.BANNER_LATEST_CAP_TK:,} / {cg.BANNER_LATEST_CAP_LINES})")
assert tape <= cg.BANNER_LATEST_CAP_TK and len(sub) <= cg.BANNER_LATEST_CAP_LINES, "REFUSED — over cap"

GM = os.path.join(ROOT, "GOOD-MORNING.md")
old = [l for l in open(GM, encoding="utf-8").read().split("\n")
       if l.startswith("> ## ★ LATEST — 2026-09-16 (Wed **#279**")]
assert len(old) == 1, ("LATEST heading", len(old))
old = old[0]
new = old.replace("> ## ★ LATEST", "> ## ★ PRIOR", 1)
assert new != old

OPS = [
 {"op": "replace", "file": "GOOD-MORNING.md", "find": [old], "replace": [new]},
 {"op": "insert", "file": "GOOD-MORNING.md",
  "at": "> ## ★ PRIOR — 2026-09-16 (Wed **#279**", "where": "before", "lines": block},
]
sys.exit(run("banner", OPS, write="--write" in sys.argv))
