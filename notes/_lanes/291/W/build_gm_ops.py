#!/usr/bin/env python3
"""#291 wrap — build the `GOOD-MORNING.md` ops file (ritual steps 2c and 2f).

SEVEN ops, one transaction, all-or-nothing:
  (1) a new `## Batch 2026-09-21 #291` heading at the TOP of `_GM-ARCHIVE.md` (newest-first);
  (2) the ★ PRIOR (#289) banner MOVES verbatim under it — 2c keeps ★ LATEST + 1 PRIOR;
  (3) the #290 banner is DEMOTED ★ LATEST → ★ PRIOR;
  (4) the #291 ★ LATEST banner + its two residual lines are inserted above it;
  (5) `roll_2f` for session 290 — post-mortem half to `notes/_GAUGE-LOG.md` (EOF append, no
      anchor by construction), commit-state half to `_GM-ARCHIVE.md` under the new batch key;
  (6) the #291 stratum is inserted under `### ⏱ SESSION STRATA`;
  (7) the FIFTH DATE-SPLIT line is added to the header BY ADDITION, after the fourth.

⚠ `roll_2f` is driven with the SESSION-QUALIFIED `> **COMMIT STATE #290:**` anchor — the bare
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
latest = [l for l in gm if l.startswith("> ## ★ LATEST — 2026-09-20 (Sun **#290**")]
assert len(latest) == 1, latest
prior = [l for l in gm if l.startswith("> ## ★ PRIOR — 2026-09-20 (Sun **#289**")]
assert len(prior) == 1, prior
ds4 = [l for l in gm if l.startswith("> ⚠ **WRAP DATE SPLIT, FOURTH OCCURRENCE ON THIS RUN")]
assert len(ds4) == 1, ds4

DS5 = ("> ⚠ **WRAP DATE SPLIT, FIFTH OCCURRENCE ON THIS RUN — SESSION AND BOTH COMMITS "
       "2026-09-20, PUSH + RITUAL + COMMIT 2026-09-21.** #291 opened on the morning of Sunday "
       "09-20 and ran nine Opus lanes; both of its commits carry that date (`b9ab75b0` · "
       "`b721144a`). The push, this ritual and its own commit are Monday 09-21. ⛔ **No key, "
       "filename, report stem or stamp was re-dated to match the ritual** — the nine lane "
       "reports keep their `2026-09-20-291-*` stems, `notes/_lanes/291/DAVE-RULINGS-2026-09-20.md`"
       " keeps its day and the deck keeps `-2026-09-20-v12` — and this line carries the ritual's "
       "date so the gate's `is not today` check grades a true statement. The #241 shape by "
       "ADDITION: the four lines above stand verbatim, and #241's ruling-shaped question — what a "
       "midnight-spanning wrap should stamp — is still Dave's, now at age 50. Detail in "
       "`_LIVE-STATE.md`'s ⏱ LATEST DELTA.")

banner = open(os.path.join(HERE, "banner291.md"), encoding="utf-8").read().rstrip("\n").split("\n")
pointer = open(os.path.join(HERE, "pointer291.md"), encoding="utf-8").read().rstrip("\n").split("\n")
gen = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_roll_state.py")],
                     capture_output=True, text=True, cwd=ROOT)
assert gen.returncode == 0, gen.stdout + gen.stderr
genline = gen.stdout.strip().split("\n")[-1]
# ⚠ PLACEHOLDER BY CONSTRUCTION: this line is re-read from `_roll_state.py` AFTER every roll has
# landed and substituted BYTE-IDENTICAL, never predicted (the #287/#288 lesson).
stratum = open(os.path.join(HERE, "stratum291.md"), encoding="utf-8").read().rstrip("\n").split("\n")

BATCH = "## Batch 2026-09-21 #291"

ops = [
    {"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-20 #290",
     "where": "before", "lines": [BATCH, ""]},
    {"op": "move", "src": "GOOD-MORNING.md",
     "start": "> ## ★ PRIOR — 2026-09-20 (Sun **#289**",
     "end": "## ⬛ DO THIS FIRST",
     "dst": "_GM-ARCHIVE.md", "at": BATCH, "where": "after"},
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [latest[0]],
     "replace": [latest[0].replace("> ## ★ LATEST —", "> ## ★ PRIOR —", 1)]},
    {"op": "insert", "file": "GOOD-MORNING.md",
     "at": "> ## ★ PRIOR — 2026-09-20 (Sun **#290**", "where": "before",
     "lines": banner + pointer + [genline, ""]},
    {"op": "roll_2f", "session": 290,
     "pm_start": "#### 2026-09-20 #290", "pm_end": "> **COMMIT STATE #290:**",
     "cs_start": "> **COMMIT STATE #290:**", "cs_end": "#### 2026-08-05 #96",
     "archive_at": BATCH},
    {"op": "insert", "file": "GOOD-MORNING.md", "at": "### ⏱ SESSION STRATA",
     "where": "after", "lines": [""] + stratum},
    {"op": "insert", "file": "GOOD-MORNING.md", "at": ds4[0], "where": "after",
     "lines": [DS5]},
]

out = os.path.join(HERE, f"ops-291-gm-{int(time.time())}.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(ops, f, ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 200
print(f"WROTE {out}  {os.path.getsize(out):,} B  {len(ops)} ops")
print(f"  banner {len(banner)} ln + pointer {len(pointer)} ln + generated 1 ln · "
      f"stratum {len(stratum)} ln · date-split line 1")
