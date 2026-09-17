#!/usr/bin/env python3
"""#280 wrap — 2c + 2d + 2f rolls, all through `_gm_move.py`, one all-or-nothing ops file.

  (1) the `_GM-ARCHIVE.md` batch key for this wrap — `<date> <session#>`, never a serial;
  (2) 2c: the #278 ★ PRIOR banner moves VERBATIM into it (GM keeps ★ LATEST + 1 PRIOR);
  (3) the `_LIVE-STATE-ARCHIVE.md` section header for this wrap;
  (4) 2d: the #277 ⏱ PRIOR DELTA moves VERBATIM into it (LS keeps ⏱ LATEST + 2 PRIOR);
  (5) 2f: #279's stratum SPLITS — post-mortem to `notes/_GAUGE-LOG.md` (append at true EOF),
      commit-state to `_GM-ARCHIVE.md` under the same batch key. Neither half can happen
      without the other.

EXIT CHECK, run BEFORE this and recorded in the wrap report: every ⚠/⬛/AWAITING item inside the
three rolling regions already stands in a standing section — `_CARRIES.md` § residual → #281
(the `#243` not-a-wrap form, the hard-wall question, `s277-D12`, showroom, the four #130 items)
or this wrap's own ★ LATEST banner. Nothing was orphaned by these moves.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_ops import run

OPS = [
 {"op": "insert", "file": "_GM-ARCHIVE.md",
  "at": "# GOOD-MORNING — banner archive", "where": "after",
  "lines": ["", "## Batch 2026-09-17 #280", ""]},
 {"op": "move", "src": "GOOD-MORNING.md",
  "start": "> ## ★ PRIOR — 2026-09-16 (Wed **#278**", "end": "## ⬛ DO THIS FIRST",
  "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-17 #280", "where": "after"},
 {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
  "at": "# _LIVE-STATE archive — rolled PRIOR DELTAs (verbatim, newest-first)", "where": "after",
  "lines": ["", "## Rolled 2026-09-17 #280 (2d, at the #280 wrap) — via the mover", ""]},
 {"op": "move", "src": "_LIVE-STATE.md",
  "start": "## ⏱ PRIOR DELTA — 2026-09-16 (Wed from `date`) (**#277**",
  "end": "## 🕓 OPEN — Latin Univers",
  "dst": "_LIVE-STATE-ARCHIVE.md",
  "at": "## Rolled 2026-09-17 #280 (2d, at the #280 wrap) — via the mover", "where": "after"},
 {"op": "roll_2f", "session": 279,
  "pm_start": "#### 2026-09-16 #279", "pm_end": "> **COMMIT STATE #279:**",
  "cs_start": "> **COMMIT STATE #279:**", "cs_end": "#### 2026-08-05 #96",
  "archive_at": "## Batch 2026-09-17 #280"},
]

sys.exit(run("rolls", OPS, write="--write" in sys.argv))
