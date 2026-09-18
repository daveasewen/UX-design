#!/usr/bin/env python3
"""#284 wrap — 2c + 2d archive rolls, every move through `knowledge/_gm_move.py`.

2c: the #282 ★ PRIOR banner leaves GOOD-MORNING.md for `_GM-ARCHIVE.md` § Batch 2026-09-18 #284.
2d: the #281 ⏱ PRIOR DELTA leaves `_LIVE-STATE.md` for `_LIVE-STATE-ARCHIVE.md` § Rolled
    2026-09-18 #284. (#280's `Previous:` chain segment follows in lastrefreshed284.py — one
    behind the delta roll, the #281…#283 boundary unchanged.)

⛔ Batch key is `<date> <session#>` (GM-D5(a)), never a serial.
⚠ EXIT CHECK ran BEFORE these ops — recorded at `notes/_lanes/284/W/WRAP-REPORT.md`.
"""
import sys
from run_ops import run

OPS = [
    {"op": "insert", "file": "_GM-ARCHIVE.md",
     "at": "# GOOD-MORNING — banner archive", "where": "after",
     "lines": ["", "## Batch 2026-09-18 #284", ""]},
    {"op": "move", "src": "GOOD-MORNING.md",
     "start": "> ## ★ PRIOR — 2026-09-18 (Fri **#282**",
     "end": "## ⬛ DO THIS FIRST",
     "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-18 #284", "where": "after"},
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
     "at": "# _LIVE-STATE archive — rolled PRIOR DELTAs (verbatim, newest-first)",
     "where": "after",
     "lines": ["", "## Rolled 2026-09-18 #284 (2d, at the #284 wrap) — via the mover", ""]},
    {"op": "move", "src": "_LIVE-STATE.md",
     "start": "## ⏱ PRIOR DELTA — 2026-09-17 (Thu from `date`) (**#281**",
     "end": "## 🕓 OPEN — Latin Univers **WEBFONT**",
     "dst": "_LIVE-STATE-ARCHIVE.md",
     "at": "## Rolled 2026-09-18 #284 (2d, at the #284 wrap) — via the mover", "where": "after"},
]

if __name__ == "__main__":
    sys.exit(run("rolls", OPS, write="--write" in sys.argv, min_bytes=600))
