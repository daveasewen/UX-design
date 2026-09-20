#!/usr/bin/env python3
"""#289 wrap — build the `GOOD-MORNING.md` ops file (ritual steps 2c and 2f).

FIVE ops, one transaction, all-or-nothing:
  (1) a new `## Batch 2026-09-20 #289` heading at the TOP of `_GM-ARCHIVE.md` (newest-first);
  (2) the ★ PRIOR (#287) banner MOVES verbatim under it — 2c keeps ★ LATEST + 1 PRIOR;
  (3) the #288 banner is DEMOTED ★ LATEST → ★ PRIOR;
  (4) the #289 ★ LATEST banner + its two residual lines are inserted above it;
  (5) `roll_2f` for session 288 — post-mortem half to `notes/_GAUGE-LOG.md` (EOF append, no
      anchor by construction), commit-state half to `_GM-ARCHIVE.md` under the new batch key.
The #289 stratum is inserted by a SIXTH op under `### ⏱ SESSION STRATA`.

⚠ `roll_2f` is driven with the SESSION-QUALIFIED `> **COMMIT STATE #288:**` anchor — the bare
form matches four lines in this file (the rolling stratum plus the three EXEMPT #40/#41/#42
blocks) and the mover refuses it, correctly.
"""
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")

gm = open(GM, encoding="utf-8").read().split("\n")
latest = [l for l in gm if l.startswith("> ## ★ LATEST — 2026-09-19 (Sat **#288**")]
assert len(latest) == 1, latest
prior = [l for l in gm if l.startswith("> ## ★ PRIOR — 2026-09-19 (Sat **#287**")]
assert len(prior) == 1, prior

banner = open(os.path.join(HERE, "banner289.md"), encoding="utf-8").read().rstrip("\n").split("\n")
pointer = open(os.path.join(HERE, "pointer289.md"), encoding="utf-8").read().rstrip("\n").split("\n")
gen = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_roll_state.py")],
                     capture_output=True, text=True, cwd=ROOT)
assert gen.returncode == 0, gen.stdout + gen.stderr
genline = gen.stdout.strip().split("\n")[-1]
# ⚠ PLACEHOLDER BY CONSTRUCTION: this line is re-read from `_roll_state.py` AFTER every roll has
# landed and substituted BYTE-IDENTICAL, never predicted (the #287/#288 lesson).
stratum = open(os.path.join(HERE, "stratum289.md"), encoding="utf-8").read().rstrip("\n").split("\n")

BATCH = "## Batch 2026-09-20 #289"

ops = [
    {"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-19 #288",
     "where": "before", "lines": [BATCH, ""]},
    {"op": "move", "src": "GOOD-MORNING.md",
     "start": "> ## ★ PRIOR — 2026-09-19 (Sat **#287**",
     "end": "## ⬛ DO THIS FIRST",
     "dst": "_GM-ARCHIVE.md", "at": BATCH, "where": "after"},
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [latest[0]],
     "replace": [latest[0].replace("> ## ★ LATEST —", "> ## ★ PRIOR —", 1)]},
    {"op": "insert", "file": "GOOD-MORNING.md",
     "at": "> ## ★ PRIOR — 2026-09-19 (Sat **#288**", "where": "before",
     "lines": banner + pointer + [genline, ""]},
    {"op": "roll_2f", "session": 288,
     "pm_start": "#### 2026-09-19 #288", "pm_end": "> **COMMIT STATE #288:**",
     "cs_start": "> **COMMIT STATE #288:**", "cs_end": "#### 2026-08-05 #96",
     "archive_at": BATCH},
    {"op": "insert", "file": "GOOD-MORNING.md", "at": "### ⏱ SESSION STRATA",
     "where": "after", "lines": [""] + stratum},
]

out = os.path.join(HERE, f"ops-289-gm-{int(time.time())}.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(ops, f, ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 200
print(f"WROTE {out}  {os.path.getsize(out):,} B  {len(ops)} ops")
print(f"  banner {len(banner)} ln + pointer {len(pointer)} ln + generated 1 ln · stratum {len(stratum)} ln")
