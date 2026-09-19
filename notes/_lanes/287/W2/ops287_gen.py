#!/usr/bin/env python3
"""#287 wrap — substitute the GENERATED residual line on the ★ LATEST banner.

The line was written at 2c time, when the tree still measured #286's rolls. `roll_claim_check`
re-derives it through `_roll_state.py` — ONE measurer, no second slicer — and FAILS on any
disagreement, correctly. This op copies the generator's CURRENT line in BYTE-IDENTICAL rather
than predicting it.
"""
import json, os, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
gen = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_roll_state.py")],
                     capture_output=True, text=True, cwd=ROOT).stdout.strip()
assert gen.startswith("> **residual (GENERATED #287):**"), gen[:90]
gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read().split("\n")
# ⛔ `> **residual (GENERATED #286):**` matches TWICE — the ★ LATEST banner (written at 2c time,
#   before 2f rolled) and the ★ PRIOR (#286) banner, which is the RECORD and must not move.
#   The pair [this wrap's own pointer line, the generated line] is unique by construction.
ptr = [l for l in gm if l.startswith("> **residual → #288:**")]
assert len(ptr) == 1, len(ptr)
i = gm.index(ptr[0])
assert gm[i + 1].startswith("> **residual (GENERATED #286):**"), gm[i + 1][:60]
ops = [{"op": "replace", "file": "GOOD-MORNING.md",
        "find": [ptr[0], gm[i + 1]], "replace": [ptr[0], gen]}]
OPSF = os.path.join(HERE, f"ops-287-gen-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 200
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops")
print("  generated line, copied not predicted:", gen[:120])
