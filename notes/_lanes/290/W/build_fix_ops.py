#!/usr/bin/env python3
"""#290 wrap — the post-roll corrections, every one a MOVER op, one transaction.

(1) The GENERATED residual line inside the NEW ★ LATEST block is substituted BYTE-IDENTICAL from
    `_roll_state.py`, re-read AFTER every roll landed and never predicted (the #287/#288/#289
    lesson). ⛔ It is anchored on a PAIR — the `residual → #291` pointer line plus the generated
    line — because `> **residual (GENERATED #289):**` matches TWICE once #289's banner became
    ★ PRIOR and the mover refuses an ambiguous anchor, correctly.

(2) ONE claim in the ⏱ LATEST DELTA #290 is CORRECTED BEFORE IT IS PUBLISHED, not after: the
    draft said #290's boot figure would join the CEILING BREACH list "as its eighth reading".
    MEASURED after the 2f roll landed, the list is a SLIDING WINDOW and stayed at SEVEN — #279
    fell out of it as #289 came in. The corrected sentence says what was measured.
"""
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")
LS = os.path.join(ROOT, "_LIVE-STATE.md")

gm = open(GM, encoding="utf-8").read().split("\n")
pointer = open(os.path.join(HERE, "pointer290.md"), encoding="utf-8").read().rstrip("\n")
assert gm.count(pointer) == 1, "pointer line is not unique"
i = gm.index(pointer)
stale = gm[i + 1]
assert stale.startswith("> **residual (GENERATED #289):**"), stale[:60]

gen = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_roll_state.py")],
                     capture_output=True, text=True, cwd=ROOT)
assert gen.returncode == 0, gen.stdout + gen.stderr
fresh = gen.stdout.strip().split("\n")[-1]
assert fresh.startswith("> **residual (GENERATED #290):**"), fresh[:60]

ls = open(LS, encoding="utf-8").read().split("\n")
OLD = ("⚠ **#290's own boot figure joins the CEILING BREACH list as its eighth reading — that is "
       "the SAME fail growing by one row, not a new one**")
NEW = ("⚠ **AND THE CEILING BREACH LIST DID NOT GROW, WHICH IS ITSELF A MEASUREMENT: it reads "
       "SEVEN both before and after the roll, because the window SLID — #279 fell out of it as "
       "#289 came in**")
hit = [k for k, l in enumerate(ls) if OLD in l]
assert len(hit) == 1, f"delta correction anchor not unique ({len(hit)})"
line = ls[hit[0]]

ops = [
    {"op": "replace", "file": "GOOD-MORNING.md",
     "find": [pointer, stale], "replace": [pointer, fresh]},
    {"op": "replace", "file": "_LIVE-STATE.md",
     "find": [line], "replace": [line.replace(OLD, NEW, 1)]},
]

out = os.path.join(HERE, f"ops-290-fix-{int(time.time())}.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(ops, f, ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 200
print(f"WROTE {out}  {os.path.getsize(out):,} B  {len(ops)} ops")
print(f"  generated line: {fresh[:96]}…")
