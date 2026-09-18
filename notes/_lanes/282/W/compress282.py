#!/usr/bin/env python3
"""#282 wrap — a SECOND compression pass on the ★ LATEST banner, driven by the GATE'S OWN
measurement of the banner region rather than by `banner282.py`'s (the two differ because the
GENERATED line's final text is longer than the PENDING placeholder measured at draft time —
declared here rather than left as a mystery). SHORTER, never quieter: no item, carry, declared
skip or receipt name is dropped."""
import os, sys
from run_ops import run
sys.path.insert(0, "/sessions/tender-hopeful-allen/mnt/UX-design/knowledge")
import _capture_gate as cg

GM = "/sessions/tender-hopeful-allen/mnt/UX-design/GOOD-MORNING.md"

PAIRS = [
 ("SAME fail as #281** · resolver **FAIL(6)** · ownership **2/3** · showroom **138 vs 108** HIS",
  "SAME fail as #281** · resolver **FAIL(6)** · ownership **2/3** · showroom **138 v 108** HIS"),
 ("· ONE logo guideline · clear space ¼ height + ¼ LOGOMARK width, up to 4px.",
  "· ONE logo guideline · clear space ¼ height + ¼ LOGOMARK width, to 4px."),
 ("(ceiling breach + 5 boot double-counts, another seat's testimony — **a wrap may not repair them**)",
  "(ceiling breach + 5 boot double-counts, another seat's — **a wrap may not repair them**)"),
]

def measure():
    return cg.measure_tokens(cg._latest_banner_region(open(GM, encoding="utf-8").read()))[0]

if __name__ == "__main__":
    text = open(GM, encoding="utf-8").read()
    lines = text.split("\n")
    edits = {}
    for old, new in PAIRS:
        if old == new:
            continue
        idx = [i for i, ln in enumerate(lines) if old in edits.get(i, ln)]
        assert len(idx) == 1, ("anchor not unique", old[:50], len(idx))
        i = idx[0]
        edits[i] = edits.get(i, lines[i]).replace(old, new, 1)
    ops = [{"op": "replace", "file": "GOOD-MORNING.md",
            "find": [lines[i]], "replace": [edits[i]]} for i in sorted(edits)]
    print("banner BEFORE (gate's own measure):", measure())
    rc = run("compress", ops, write="--write" in sys.argv, min_bytes=500)
    if "--write" in sys.argv:
        print("banner AFTER (gate's own measure):", measure(), "· cap", cg.BANNER_LATEST_CAP_TK)
    sys.exit(rc)
