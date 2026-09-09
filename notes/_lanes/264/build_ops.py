#!/usr/bin/env python3
"""#264 wrap — build the mover ops files. Session-owned, uniquely named, asserted before use."""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
LS = os.path.join(ROOT, "_LIVE-STATE.md")


def read(p):
    return open(p, encoding="utf-8").read().split("\n")


def write_ops(name, ops):
    p = os.path.join(HERE, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(ops, f, ensure_ascii=False, indent=1)
    assert os.path.exists(p) and os.path.getsize(p) > 200, (p, os.path.getsize(p))
    print("wrote %s (%d bytes, %d ops)" % (name, os.path.getsize(p), len(ops)))
    return p


ls = read(LS)
lr = [l for l in ls if l.startswith("*Last refreshed: ")]
assert len(lr) == 1
lr = lr[0]

M261 = "  Previous: 2026-09-09 (Wed from `date` — **#261 wrap**."
M260 = "  *Last refreshed (#260, trimmed at the #263 wrap)"
i261, i260 = lr.find(M261), lr.find(M260)
assert i261 > 0 and i260 > i261, (i261, i260)
seg261 = lr[i261:i260]                       # the VERBATIM chain segment that rolls out
assert lr.count(M261) == 1 and lr.count(M260) == 1
TRIM = ("  *Last refreshed (#261, trimmed at the #264 wrap): #261's `Previous:` chain segment was "
        "moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-09 #264, in the same section "
        "as its ⏱ delta block. Nothing was deleted — moved.*")
lr_trimmed = lr[:i261] + TRIM + lr[i260:]
open(os.path.join(HERE, "seg261.txt"), "w", encoding="utf-8").write(seg261.strip())

# ---------------------------------------------------------------- ops 1: the rolls (2c / 2d / 2f)
rolls = [
    {"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-09 #263",
     "where": "before", "lines": ["## Batch 2026-09-09 #264", ""]},
    {"op": "move", "src": "GOOD-MORNING.md",
     "start": "> ## ★ PRIOR — 2026-09-09 (Wed from `date` **#262**",
     "end": "## ⬛ DO THIS FIRST",
     "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-09 #264", "where": "after"},
    {"op": "roll_2f", "session": 263,
     "pm_start": "#### 2026-09-09 #263", "pm_end": "> **COMMIT STATE #263:**",
     "cs_start": "> **COMMIT STATE #263:**", "cs_end": "#### 2026-08-05 #96",
     "archive_at": "## Batch 2026-09-09 #264"},
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-09 #263",
     "where": "before",
     "lines": ["## Rolled 2026-09-09 #264 (2d, at the #264 wrap) — via the mover", ""]},
    {"op": "move", "src": "_LIVE-STATE.md",
     "start": "## ⏱ PRIOR DELTA — 2026-09-09 (Wed from `date`) (**#261**",
     "end": "## 🕓 OPEN — Latin Univers",
     "dst": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-09 #264", "where": "after"},
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-09 #264",
     "where": "after",
     "lines": ["",
               "*Chain segment trimmed from `_LIVE-STATE.md`'s `Last refreshed` line at the same "
               "2d boundary, VERBATIM:*",
               "",
               seg261.strip()]},
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [lr], "replace": [lr_trimmed]},
]
write_ops("ops-264-rolls.json", rolls)

# ---------------------------------------------------------------- ops 2: banner + delta + titles
banner = open(os.path.join(HERE, "banner264.txt"), encoding="utf-8").read().rstrip("\n").split("\n")
delta = open(os.path.join(HERE, "delta264.txt"), encoding="utf-8").read().rstrip("\n").split("\n")
new_lr_body = open(os.path.join(HERE, "lastrefreshed264.txt"), encoding="utf-8").read().strip()

gm = read(os.path.join(ROOT, "GOOD-MORNING.md"))
gm_latest = [l for l in gm if l.startswith("> ## ★ LATEST — ")]
assert len(gm_latest) == 1
gm_latest = gm_latest[0]
gm_prior263 = gm_latest.replace("> ## ★ LATEST — ", "> ## ★ PRIOR — ", 1)

ls_latest = [l for l in ls if l.startswith("## ⏱ LATEST DELTA — ")]
assert len(ls_latest) == 1
ls_latest = ls_latest[0]
ls_prior263 = ls_latest.replace("## ⏱ LATEST DELTA — ", "## ⏱ PRIOR DELTA — ", 1)

title_old = [l for l in gm if l.startswith("> **TITLE THE NEXT CHAT →**")]
assert len(title_old) == 1
title_new = ("> **TITLE THE NEXT CHAT →** `Apollo - #265: the /goal bite-test, and the four "
             "ungraded glyphs`")

lr2 = lr_trimmed[len("*Last refreshed: "):]
new_lr = "*Last refreshed: " + new_lr_body + "  Previous: " + lr2

main = [
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [gm_latest], "replace": [gm_prior263]},
    {"op": "insert", "file": "GOOD-MORNING.md",
     "at": "> ## ★ PRIOR — 2026-09-09 (Wed from `date` **#263**",
     "where": "before", "lines": banner + [">", ""]},
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [ls_latest], "replace": [ls_prior263]},
    {"op": "insert", "file": "_LIVE-STATE.md",
     "at": "## ⏱ PRIOR DELTA — 2026-09-09 (Wed from `date`) (**#263**",
     "where": "before", "lines": delta + [""]},
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [lr_trimmed], "replace": [new_lr]},
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [title_old[0]], "replace": [title_new]},
]
write_ops("ops-264-main.json", main)

# ---------------------------------------------------------------- ops 3: the #264 stratum (2f)
stratum = open(os.path.join(HERE, "stratum264.txt"), encoding="utf-8").read().rstrip("\n").split("\n")
strat = [
    {"op": "insert", "file": "GOOD-MORNING.md", "at": "### ⏱ SESSION STRATA", "where": "after",
     "lines": ["", "#### 2026-09-09 #264", ""] + stratum},
]
write_ops("ops-264-stratum.json", strat)
print("seg261 %d chars · new Last refreshed %d chars" % (len(seg261.strip()), len(new_lr)))
