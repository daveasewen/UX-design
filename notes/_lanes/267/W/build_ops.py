#!/usr/bin/env python3
"""#267 wrap — build the session-owned mover ops files, uniquely named, asserted before use.

⛔ THE OPS FILE IS A MSGFILE (runbook 2c): unique name under notes/_lanes/267/W/, written from
THIS process, `os.path.exists` + a size floor asserted here, receipts read back against the ops.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


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
W("ops-267-rolls.json", [
    {"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-10 #266",
     "where": "before", "lines": ["## Batch 2026-09-10 #267", ""]},
    {"op": "move", "src": "GOOD-MORNING.md",
     "start": "> ## ★ PRIOR — 2026-09-09 (Wed from `date` **#265**",
     "end": "## ⬛ DO THIS FIRST",
     "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-10 #267", "where": "after"},
    {"op": "roll_2f", "session": 266,
     "pm_start": "#### 2026-09-10 #266", "pm_end": "> **COMMIT STATE #266:**",
     "cs_start": "> **COMMIT STATE #266:**", "cs_end": "#### 2026-08-05 #96",
     "archive_at": "## Batch 2026-09-10 #267"},
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-10 #266",
     "where": "before",
     "lines": ["## Rolled 2026-09-10 #267 (2d, at the #267 wrap) — via the mover", ""]},
    {"op": "move", "src": "_LIVE-STATE.md",
     "start": "## ⏱ PRIOR DELTA — 2026-09-09 (Wed from `date`) (**#264**",
     "end": "## 🕓 OPEN — Latin Univers",
     "dst": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-10 #267", "where": "after"},
])
