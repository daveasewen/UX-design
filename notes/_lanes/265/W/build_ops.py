#!/usr/bin/env python3
"""#265 wrap — build the session-owned mover ops files, uniquely named, asserted before use.

⛔ THE OPS FILE IS A MSGFILE (runbook 2c): unique name under notes/_lanes/265/W/, written from
THIS process, `os.path.exists` + a size floor asserted here, receipts read back against the ops.
"""
import json
import os
import sys

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


LATEST264 = ("> ## ★ LATEST — 2026-09-09 (Wed from `date` **#264**, **Fable**, no subs but this "
             "OPUS 5 wrap sub, DELEGATED — ★★★ **TWO GLYPH TWINS RULED, A MIS-TWINNING GATE ARM, "
             "AND EIGHT DERIVED `-active` GLYPHS**)")
PRIOR264 = LATEST264.replace("★ LATEST —", "★ PRIOR —")
banner = open(os.path.join(HERE, "banner265.txt"), encoding="utf-8").read().rstrip("\n").split("\n")

# ---- ops 1: 2c/2d/2f rolls ---------------------------------------------------------------------
W("ops-265-rolls.json", [
    {"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-09 #264",
     "where": "before", "lines": ["## Batch 2026-09-09 #265", ""]},
    {"op": "move", "src": "GOOD-MORNING.md",
     "start": "> ## ★ PRIOR — 2026-09-09 (Wed from `date` **#263**",
     "end": "## ⬛ DO THIS FIRST",
     "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-09 #265", "where": "after"},
    {"op": "roll_2f", "session": 264,
     "pm_start": "#### 2026-09-09 #264", "pm_end": "> **COMMIT STATE #264:**",
     "cs_start": "> **COMMIT STATE #264:**", "cs_end": "#### 2026-08-05 #96",
     "archive_at": "## Batch 2026-09-09 #265"},
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-09 #264",
     "where": "before",
     "lines": ["## Rolled 2026-09-09 #265 (2d, at the #265 wrap) — via the mover", ""]},
    {"op": "move", "src": "_LIVE-STATE.md",
     "start": "## ⏱ PRIOR DELTA — 2026-09-09 (Wed from `date`) (**#262**",
     "end": "## 🕓 OPEN — Latin Univers",
     "dst": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-09 #265", "where": "after"},
])

# ---- ops 2: the new banner (2c insert) + LATEST→PRIOR rename ------------------------------------
W("ops-265-banner.json", [
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [LATEST264], "replace": [PRIOR264]},
    {"op": "insert", "file": "GOOD-MORNING.md",
     "at": "> ## ★ PRIOR — 2026-09-09 (Wed from `date` **#264**", "where": "before",
     "lines": banner + [""]},
])
print("banner lines:", len(banner))
