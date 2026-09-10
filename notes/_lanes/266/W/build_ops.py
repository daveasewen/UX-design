#!/usr/bin/env python3
"""#266 wrap — build the session-owned mover ops files, uniquely named, asserted before use.

⛔ THE OPS FILE IS A MSGFILE (runbook 2c): unique name under notes/_lanes/266/W/, written from
THIS process, `os.path.exists` + a size floor asserted here, receipts read back against the ops.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def W(name, ops, floor=200):
    p = os.path.join(HERE, name)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(ops, fh, ensure_ascii=False, indent=1)
    assert os.path.exists(p), p
    sz = os.path.getsize(p)
    assert sz >= floor, (p, sz)
    print("wrote %s (%d B)" % (name, sz))
    return p


# ---- ops 1: 2c/2d/2f rolls ---------------------------------------------------------------------
W("ops-266-rolls.json", [
    {"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-09 #265",
     "where": "before", "lines": ["## Batch 2026-09-10 #266", ""]},
    {"op": "move", "src": "GOOD-MORNING.md",
     "start": "> ## ★ PRIOR — 2026-09-09 (Wed from `date` **#264**",
     "end": "## ⬛ DO THIS FIRST",
     "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-10 #266", "where": "after"},
    {"op": "roll_2f", "session": 265,
     "pm_start": "#### 2026-09-09 #265", "pm_end": "> **COMMIT STATE #265:**",
     "cs_start": "> **COMMIT STATE #265:**", "cs_end": "#### 2026-08-05 #96",
     "archive_at": "## Batch 2026-09-10 #266"},
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-09 #265",
     "where": "before",
     "lines": ["## Rolled 2026-09-10 #266 (2d, at the #266 wrap) — via the mover", ""]},
    {"op": "move", "src": "_LIVE-STATE.md",
     "start": "## ⏱ PRIOR DELTA — 2026-09-09 (Wed from `date`) (**#263**",
     "end": "## 🕓 OPEN — Latin Univers",
     "dst": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-10 #266", "where": "after"},
])
