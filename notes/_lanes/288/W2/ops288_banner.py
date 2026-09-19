#!/usr/bin/env python3
"""#288 wrap — step 2c ops: roll the ★ PRIOR (#286) banner, demote #287, insert #288's.

FOUR ops, all-or-nothing:
  1. `insert`  a new `## Batch 2026-09-19 #288` heading at the TOP of `_GM-ARCHIVE.md`
               (newest-first, mirroring `_CARRIES.md`).
  2. `move`    the whole ★ PRIOR (#286) banner block out of `GOOD-MORNING.md` into that batch,
               VERBATIM — a move, never a rewrite.
  3. `replace` the #287 heading `★ LATEST` → `★ PRIOR`.
  4. `insert`  the new ★ LATEST #288 banner above it.

⛔ The banner text is MEASURED with the gate's own instrument in `banner288.py` before this
   runs, with the GENERATED residual line substituted, because that line is inside the block
   `s241-D2` charges.

2c EXIT CHECK: every ⚠/⬛/AWAITING item on the rolling #286 banner must already stand in a
standing section before it rolls. Asserted below against `_CARRIES.md` — the standing home
`s225-D2` gives the carry set — by grep, not by memory.
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
import banner288 as B

gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read()
arch = open(os.path.join(ROOT, "_GM-ARCHIVE.md"), encoding="utf-8").read()

PRIOR286 = "> ## ★ PRIOR — 2026-09-18 (Fri **#286**"
LATEST287 = "> ## ★ LATEST — 2026-09-19 (Sat **#287**"
assert gm.count(PRIOR286) == 1 and gm.count(LATEST287) == 1
assert "## Batch 2026-09-19 #288" not in arch, "the #288 batch already exists"
assert arch.count("# GOOD-MORNING — banner archive") == 1

# ── 2c EXIT CHECK ────────────────────────────────────────────────────────────────────────────
carries = open(os.path.join(ROOT, "_CARRIES.md"), encoding="utf-8").read()
for token in ("CONNECTOR LEVER", "INSEAT_WARN_TK", "DELEGATION RULE", "BOOT_CEILING_TK", "#243"):
    assert token in carries, \
        f"2c EXIT CHECK FAILED — a #286 banner item has no standing home: {token!r}"
print("2c EXIT CHECK: #286's carried items stand in `_CARRIES.md` — safe to roll.")

old_head = [l for l in gm.split("\n") if l.startswith(LATEST287)][0]
demoted = old_head.replace("> ## ★ LATEST —", "> ## ★ PRIOR —", 1)

# the GENERATED line is re-read HERE, after 2c/2d/2f's own state has settled as far as it can,
# and is substituted BYTE-IDENTICAL rather than predicted.
gen = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_roll_state.py")],
                     capture_output=True, text=True, cwd=ROOT).stdout.strip()
assert gen.startswith("> **residual (GENERATED"), gen[:120]

n = int(sys.argv[1])
text = B.build(n, gen)
tk, ln = B.measure(text)
assert tk <= B.cg.BANNER_LATEST_CAP_TK, f"banner OVER the s241-D2 tape cap: {tk}"
assert ln <= B.cg.BANNER_LATEST_CAP_LINES, f"banner OVER the s241-D2 line cap: {ln}"
print(f"banner pre-check (gate's own instrument): {tk:,} tape / {ln} lines — INSIDE "
      f"{B.cg.BANNER_LATEST_CAP_TK:,} / {B.cg.BANNER_LATEST_CAP_LINES}")
open(os.path.join(HERE, "banner288.md"), "w", encoding="utf-8").write(text + "\n")

ops = [
 {"op": "insert", "file": "_GM-ARCHIVE.md", "at": "# GOOD-MORNING — banner archive",
  "where": "after", "lines": ["", "## Batch 2026-09-19 #288", ""]},
 {"op": "move", "src": "GOOD-MORNING.md", "start": PRIOR286,
  "end": "## ⬛ DO THIS FIRST", "dst": "_GM-ARCHIVE.md",
  "at": "## Batch 2026-09-19 #288", "where": "after"},
 {"op": "replace", "file": "GOOD-MORNING.md", "find": [old_head], "replace": [demoted]},
 {"op": "insert", "file": "GOOD-MORNING.md", "at": demoted[:70], "where": "before",
  "lines": text.split("\n") + [""]},
]

OPSF = os.path.join(HERE, f"ops-288-banner-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 2000
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops")
