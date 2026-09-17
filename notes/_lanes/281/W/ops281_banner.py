#!/usr/bin/env python3
"""#281 wrap — the ★ LATEST banner swap in `GOOD-MORNING.md`, through `_gm_move.py`:
  (1) #280's ★ LATEST heading is demoted to ★ PRIOR — a FULL-LINE replace, its only edit;
  (2) #281's banner (`banner281.py`, held in ONE place and MEASURED first) is inserted BEFORE it;
  (3) the NEXT-CHAT title line is re-pointed at #282.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_ops import run, ROOT
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg
import banner281

ROLLSTATE = sys.argv[sys.argv.index("--rollstate") + 1] if "--rollstate" in sys.argv else None
kw = {"rollstate": ROLLSTATE} if ROLLSTATE else {}
block = banner281.lines(**kw)
sub = [l for l in block if l.strip() and l.strip() != ">"]
tape = cg.measure_tokens("\n".join(block))[0]
print(f"BANNER: {tape:,} tape / {len(sub)} substantive lines "
      f"(cap {cg.BANNER_LATEST_CAP_TK:,} / {cg.BANNER_LATEST_CAP_LINES})")
assert tape <= cg.BANNER_LATEST_CAP_TK and len(sub) <= cg.BANNER_LATEST_CAP_LINES, "REFUSED — over cap"

GM = os.path.join(ROOT, "GOOD-MORNING.md")
txt = open(GM, encoding="utf-8").read().split("\n")
old = [l for l in txt if l.startswith("> ## ★ LATEST — 2026-09-17 (Thu **#280**")]
assert len(old) == 1, ("LATEST heading", len(old))
old = old[0]
new = old.replace("> ## ★ LATEST", "> ## ★ PRIOR", 1)
assert new != old

oldt = [l for l in txt if l.startswith("> **TITLE THE NEXT CHAT →**")]
assert len(oldt) == 1, ("title line", len(oldt))
oldt = oldt[0]
newt = "> **TITLE THE NEXT CHAT →** `Apollo - #282: the rule notes and the eye-check`"
assert newt != oldt

OPS = [
 {"op": "replace", "file": "GOOD-MORNING.md", "find": [old], "replace": [new]},
 {"op": "replace", "file": "GOOD-MORNING.md", "find": [oldt], "replace": [newt]},
 {"op": "insert", "file": "GOOD-MORNING.md",
  "at": "> ## ★ PRIOR — 2026-09-17 (Thu **#280**", "where": "before", "lines": block},
]
sys.exit(run("banner", OPS, write="--write" in sys.argv))
