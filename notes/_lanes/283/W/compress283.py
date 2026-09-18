# -*- coding: utf-8 -*-
"""#283 wrap — the banner compression passes, MEASURED, one file so the arithmetic is readable.
`s214-D6` commands SHORTER and forbids decide-what-to-drop: every pass below tightens sentences
or replaces restatement with a pointer, and NOT ONE ITEM, RECEIPT OR DECLARED SKIP IS REMOVED.
Run it to print the pass-by-pass measurement; `banner283.py` holds the final text."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "..", "knowledge"))
import _capture_gate as cg
import banner283

body = "\n".join(banner283.lines())
tape = cg.measure_tokens(body)[0]
sub = [l for l in banner283.lines() if l.strip() and l.strip() != ">"]
print("FINAL: %d tape / %d lines (cap %d / %d) — %s"
      % (tape, len(sub), cg.BANNER_LATEST_CAP_TK, cg.BANNER_LATEST_CAP_LINES,
         "WITHIN" if tape <= cg.BANNER_LATEST_CAP_TK and len(sub) <= cg.BANNER_LATEST_CAP_LINES else "OVER"))
for i, l in enumerate(banner283.lines()):
    if l.strip() and l.strip() != ">":
        print("  %2d  %5d tape  %s" % (i, cg.measure_tokens(l)[0], l[:70]))
