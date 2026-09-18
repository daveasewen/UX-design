#!/usr/bin/env python3
"""#285 wrap — step 1 + 2d on `_LIVE-STATE.md`, every move through `_gm_move.py`.

FOUR ops, one transaction (all-or-nothing):
  1. insert the new `## Rolled 2026-09-18 #285` heading at the TOP of `_LIVE-STATE-ARCHIVE.md`
     (newest-first; the archive already exists, so the mover's NEVER-creates-a-file rule holds);
  2. MOVE the ⏱ PRIOR DELTA **#282** block out of `_LIVE-STATE.md` into that section —
     VERBATIM, by construction, receipts carry the line count so a wrong extent is visible;
  3. demote the `## ⏱ LATEST DELTA … #284` heading to `## ⏱ PRIOR DELTA …`;
  4. insert the new ⏱ LATEST DELTA #285 block above it.

2d keeps LATEST + 2 PRIOR: after this, LATEST #285 · PRIOR #284 · PRIOR #283.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_ops import run

LS = "_LIVE-STATE.md"
ARCH = "_LIVE-STATE-ARCHIVE.md"

d284 = open(os.path.join(HERE, "lsdelta285.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert d284[0].startswith("## ⏱ LATEST DELTA — 2026-09-18"), d284[0][:60]

old_latest = [l for l in open(os.path.join(HERE, "..", "..", "..", "..", LS), encoding="utf-8")
              if l.startswith("## ⏱ LATEST DELTA")]
assert len(old_latest) == 1, len(old_latest)
old_latest = old_latest[0].rstrip("\n")
new_prior = old_latest.replace("## ⏱ LATEST DELTA", "## ⏱ PRIOR DELTA", 1)
assert new_prior != old_latest

ops = [
    {"op": "insert", "file": ARCH,
     "at": "## Rolled 2026-09-18 #284", "where": "before",
     "lines": ["## Rolled 2026-09-18 #285 (2d, at the #285 wrap) — via the mover", ""]},
    {"op": "move", "src": LS,
     "start": "## ⏱ PRIOR DELTA — 2026-09-18 (Fri from `date`) (**#282**",
     "end": "## 🕓 OPEN — Latin Univers",
     "dst": ARCH, "at": "## Rolled 2026-09-18 #285 (2d, at the #285 wrap) — via the mover",
     "where": "after"},
    {"op": "replace", "file": LS, "find": [old_latest], "replace": [new_prior]},
    {"op": "insert", "file": LS, "at": new_prior, "where": "before",
     "lines": d284 + [""]},
]

sys.exit(run("lsdelta", ops, write="--write" in sys.argv, min_bytes=500))
