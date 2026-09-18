#!/usr/bin/env python3
"""#282 wrap — 2c + 2d archive rolls, every move through `knowledge/_gm_move.py`.

2c: the #280 ★ PRIOR banner leaves GOOD-MORNING.md for `_GM-ARCHIVE.md` § Batch 2026-09-18 #282.
2d: the #279 ⏱ PRIOR DELTA leaves `_LIVE-STATE.md` for `_LIVE-STATE-ARCHIVE.md` § Rolled
    2026-09-18 #282. (#278's `Previous:` chain segment follows in lastrefreshed282.py — one
    behind the delta roll, the #278…#281 boundary unchanged.)

⛔ Batch key is `<date> <session#>` (GM-D5(a)), never a serial.
"""
import sys
from run_ops import run

OPS = [
    {"op": "insert", "file": "_GM-ARCHIVE.md",
     "at": "# GOOD-MORNING — banner archive", "where": "after",
     "lines": ["", "## Batch 2026-09-18 #282", ""]},
    {"op": "move", "src": "GOOD-MORNING.md",
     "start": "> ## ★ PRIOR — 2026-09-17 (Thu **#280**",
     "end": "## ⬛ DO THIS FIRST",
     "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-18 #282", "where": "after"},
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
     "at": "# _LIVE-STATE archive — rolled PRIOR DELTAs (verbatim, newest-first)",
     "where": "after",
     "lines": ["", "## Rolled 2026-09-18 #282 (2d, at the #282 wrap) — via the mover", ""]},
    {"op": "move", "src": "_LIVE-STATE.md",
     "start": "## ⏱ PRIOR DELTA — 2026-09-16 (Wed from `date`) (**#279**",
     "end": "## 🕓 OPEN — Latin Univers **WEBFONT**",
     "dst": "_LIVE-STATE-ARCHIVE.md",
     "at": "## Rolled 2026-09-18 #282 (2d, at the #282 wrap) — via the mover", "where": "after"},
]

if __name__ == "__main__":
    sys.exit(run("rolls", OPS, write="--write" in sys.argv, min_bytes=600))
