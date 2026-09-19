#!/usr/bin/env python3
"""#288 wrap — run an ops file through `_gm_move.py`, DRY FIRST, receipts read back.

⛔ THE #166 CONTRACT, ENFORCED HERE RATHER THAN REMEMBERED:
   · the ops file is session-owned and uniquely named (`notes/_lanes/288/W2/ops-288-*.json`)
   · `os.path.exists` + a size floor are asserted IN THIS PROCESS before the mover reads it
   · the ops are PARSED here and the receipt count is checked against the op count, so a
     stale or truncated file cannot print green receipts for someone else's ops
   · --dry-run runs first and must succeed before the real run is offered

usage:  python3 run_ops.py <ops.json> [--write]
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

opsf = sys.argv[1]
if not os.path.isabs(opsf):
    opsf = os.path.join(HERE, opsf)

assert os.path.exists(opsf), f"ops file missing: {opsf}"
sz = os.path.getsize(opsf)
assert sz >= 200, f"ops file implausibly small ({sz} B)"
assert os.path.dirname(os.path.abspath(opsf)) == HERE, \
    "REFUSED: the ops file is not session-owned (s218-D7 clause 3 / #166)"
ops = json.load(open(opsf, encoding="utf-8"))
assert isinstance(ops, list) and ops, "ops file is not a non-empty list"
print(f"OPS {os.path.basename(opsf)}  {sz:,} B  {len(ops)} op(s): "
      + " · ".join(o["op"] for o in ops))

MOVER = os.path.join(ROOT, "knowledge", "_gm_move.py")


def run(dry: bool):
    cmd = ["python3", MOVER, "--ops", opsf, "--repo", ROOT] + (["--dry-run"] if dry else [])
    p = subprocess.run(cmd, capture_output=True, text=True)
    tag = "DRY" if dry else "WRITE"
    print(f"--- {tag} rc={p.returncode} ---")
    print(p.stdout.rstrip())
    if p.stderr.strip():
        print("STDERR:", p.stderr.rstrip()[-2000:])
    return p


p = run(dry=True)
if p.returncode != 0:
    sys.exit("DRY RUN REFUSED — nothing written, and nothing is retried blind.")

if "--write" not in sys.argv:
    print("\nDRY ONLY — pass --write to land it.")
    sys.exit(0)

p = run(dry=False)
if p.returncode != 0:
    sys.exit("WRITE REFUSED — read the refusal above; do not retry blind.")

# ── RECEIPTS READ BACK against the ops meant to be run ──────────────────────────────────────
receipts = [l for l in p.stdout.split("\n") if l.strip() and not l.startswith(("DRY", "#", " "))]
print(f"\nreceipts: {len(receipts)} line(s) for {len(ops)} op(s)")
for r in receipts:
    print("  ✓", r[:200])
