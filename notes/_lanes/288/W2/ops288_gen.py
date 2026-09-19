#!/usr/bin/env python3
"""#288 wrap — substitute the GENERATED residual line into the ★ LATEST banner, BYTE-IDENTICAL.

The banner was built BEFORE 2c/2d/2f ran, so its generated line still reads `#287`. `_roll_state.py`
is the ONE measurer of that line (`roll_claim_check` re-derives it through the same function and
FAILS on a mismatch), so the current line is COPIED IN rather than predicted.

⛔ ANCHORED ON A PAIR OF LINES, not on the generated line alone: `> **residual (GENERATED #287):**`
   now matches TWICE — once in this banner (pre-substitution) and once on the ★ PRIOR (#287) banner,
   whose record must not move while the live line does. The #287 lesson, re-applied.
"""
import json, os, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")
lines = open(GM, encoding="utf-8").read().split("\n")

res = [l for l in lines if l.startswith("> **residual → #289:**")]
assert len(res) == 1, f"expected one residual → #289 line, got {len(res)}"
i = lines.index(res[0])
old_gen = lines[i + 1]
assert old_gen.startswith("> **residual (GENERATED"), old_gen[:80]

new_gen = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_roll_state.py")],
                         capture_output=True, text=True, cwd=ROOT).stdout.strip()
assert new_gen.startswith("> **residual (GENERATED #288):**"), new_gen[:120]
assert new_gen != old_gen, "the generated line is already current — nothing to do"

ops = [{"op": "replace", "file": "GOOD-MORNING.md",
        "find": [res[0], old_gen], "replace": [res[0], new_gen]}]
OPSF = os.path.join(HERE, f"ops-288-gen-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 1000
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops")
print("  old:", old_gen[:100])
print("  new:", new_gen[:100])
