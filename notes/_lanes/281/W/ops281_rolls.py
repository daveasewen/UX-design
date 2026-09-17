#!/usr/bin/env python3
"""#281 wrap — 2c + 2d + 2f rolls, all through `_gm_move.py`, one all-or-nothing ops file.
EXIT CHECK ran BEFORE this and is recorded in `notes/_lanes/281/W/WRAP-REPORT.md`."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_ops import run

OPS = [
 {"op": "insert", "file": "_GM-ARCHIVE.md",
  "at": "# GOOD-MORNING — banner archive", "where": "after",
  "lines": ["", "## Batch 2026-09-17 #281", ""]},
 {"op": "move", "src": "GOOD-MORNING.md",
  "start": "> ## ★ PRIOR — 2026-09-16 (Wed **#279**", "end": "## ⬛ DO THIS FIRST",
  "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-17 #281", "where": "after"},
 {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
  "at": "# _LIVE-STATE archive — rolled PRIOR DELTAs (verbatim, newest-first)", "where": "after",
  "lines": ["", "## Rolled 2026-09-17 #281 (2d, at the #281 wrap) — via the mover", ""]},
 {"op": "move", "src": "_LIVE-STATE.md",
  "start": "## ⏱ PRIOR DELTA — 2026-09-16 (Wed from `date`) (**#278**",
  "end": "## 🕓 OPEN — Latin Univers",
  "dst": "_LIVE-STATE-ARCHIVE.md",
  "at": "## Rolled 2026-09-17 #281 (2d, at the #281 wrap) — via the mover", "where": "after"},
 {"op": "roll_2f", "session": 280,
  "pm_start": "#### 2026-09-17 #280", "pm_end": "> **COMMIT STATE #280:**",
  "cs_start": "> **COMMIT STATE #280:**", "cs_end": "#### 2026-08-05 #96",
  "archive_at": "## Batch 2026-09-17 #281"},
]
sys.exit(run("rolls", OPS, write="--write" in sys.argv))
