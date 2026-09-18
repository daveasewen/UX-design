#!/usr/bin/env python3
"""#286 wrap — step 2c: roll the banner stack and write the new ★ LATEST.

FOUR ops, in order:
  1. insert the `## Batch 2026-09-18 #286` header at the TOP of `_GM-ARCHIVE.md`
     (newest-first — the archive REFUSES an EOF append for exactly this reason)
  2. move the #284 ★ PRIOR banner out of `GOOD-MORNING.md` into that batch, VERBATIM
  3. rename #285's ★ LATEST heading to ★ PRIOR
  4. insert the measured #286 ★ LATEST banner above it

⚠ 2c's EXIT CHECK is PROSE and runs BEFORE this script — see `WRAP-REPORT.md`. This file
  performs the move; it does not certify the check.
"""
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")
GMA = os.path.join(ROOT, "_GM-ARCHIVE.md")

banner = open(os.path.join(HERE, "banner286.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert banner[0].startswith("> ## ★ LATEST — 2026-09-18 (Fri **#286**"), banner[0][:70]
assert len(banner) == 11, f"banner is {len(banner)} lines — expected 11 (10 substantive + 1 `>` spacer, the #285 shape)"

gm = open(GM, encoding="utf-8").read().split("\n")
lat = [l for l in gm if l.startswith("> ## ★ LATEST —")]
pri = [l for l in gm if l.startswith("> ## ★ PRIOR —")]
assert len(lat) == 1 and len(pri) == 1, f"expected 1 LATEST + 1 PRIOR, found {len(lat)}/{len(pri)}"
LATEST285, PRIOR284 = lat[0], pri[0]
assert "(Fri **#285**" in LATEST285 and "(Fri **#284**" in PRIOR284
assert "**#286**" not in "\n".join(gm), "a #286 banner already exists — refusing to run twice"

PRIOR285 = LATEST285.replace("> ## ★ LATEST —", "> ## ★ PRIOR —", 1)
BATCH = "## Batch 2026-09-18 #286"
assert BATCH not in open(GMA, encoding="utf-8").read(), "the #286 batch already exists"

ops = [
 {"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-18 #285", "where": "before",
  "lines": [BATCH, ""]},
 {"op": "move", "src": "GOOD-MORNING.md", "start": PRIOR284,
  "end": {"regex": r"^## ⬛ DO THIS FIRST"},
  "dst": "_GM-ARCHIVE.md", "at": BATCH, "where": "after"},
 {"op": "replace", "file": "GOOD-MORNING.md", "find": [LATEST285], "replace": [PRIOR285]},
 {"op": "insert", "file": "GOOD-MORNING.md", "at": PRIOR285, "where": "before",
  "lines": banner + [""]},
]

OPSF = os.path.join(HERE, f"ops-286-banner-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF)
sz = os.path.getsize(OPSF)
assert sz > 4_000, f"ops file implausibly small ({sz} B)"
print(f"OPS {OPSF}  {sz:,} B  {len(ops)} ops  · banner {len(banner)} ln")
