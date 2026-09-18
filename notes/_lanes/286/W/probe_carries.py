#!/usr/bin/env python3
"""#286 lane W — locate the carry items this wrap may strike, BY PROBE, never by memory.

⛔ A strike needs its item's EXACT current text. This prints candidate headlines so the
strike list is built from the file rather than from the brief's description of it.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # noqa: E402 — the ONE definition of "a carry"

src = [l for l in open(os.path.join(ROOT, "_CARRIES.md"), encoding="utf-8")
       if l.startswith("> **residual → #286:**")]
assert len(src) == 1, len(src)
items = cg._carry_items(src[0].rstrip("\n"))
print("items:", len(items))

NEEDLES = [w.strip() for w in sys.argv[1:]] or [
    "standing.md", "REGISTRATION", "256,000", "INSEAT", "in-seat", "--quiet", "quiet",
    "MOVE 2", "MOVE 3", "seam", "archive",
]
for n in NEEDLES:
    hits = [i for i, t in enumerate(items) if n.lower() in str(t).lower()]
    print(f"\n### {n!r} -> {len(hits)} hit(s)")
    for i in hits[:6]:
        head = str(items[i])[:260].replace("\n", " ")
        print(f"  [{i}] {head}")
