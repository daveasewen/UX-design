#!/usr/bin/env python3
"""#283 wrap — re-lay the ★ LATEST banner after the compression passes, through the mover.
The FIND list is read off GOOD-MORNING.md as it now stands (never re-typed from memory) and the
REPLACE list is `banner283.py`'s single source of truth, so the two cannot drift."""
import os, sys
import banner283
from run_ops import run

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")
lines = open(GM, encoding="utf-8").read().split("\n")
i = next(k for k, l in enumerate(lines) if l.startswith("> ## ★ LATEST — 2026-09-18 (Fri **#283**"))
j = next(k for k, l in enumerate(lines) if l.startswith("> **residual (GENERATED #283):**"))
cur = lines[i:j + 1]
new = banner283.lines()[:-1]          # drop the trailing blank; it is already in the file
assert len(cur) == len(new), (len(cur), len(new))
assert cur != new, "REFUSED — identical, nothing to re-lay"

OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": cur, "replace": new}]

if __name__ == "__main__":
    sys.exit(run("rebanner", OPS, write="--write" in sys.argv, min_bytes=2000))
