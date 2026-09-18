#!/usr/bin/env python3
"""#285 wrap — repair the `section-usage #285` line, which the gate refused as MALFORMED.

⛔ NAMED, NOT SMOOTHED. The first line testified nine GM sections and only five LS ones; the
gate's refusal is exact — *"every section is testified exactly once, U is a statement too"*, and
a malformed line is *"worse than missing — a false inscription"*. The ids are FORM (from
`_gm_usage.py --usage-template`, whose vocabulary is the only copy); the CODES are testimony and
are written by hand, here, by the seat that did the reading.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
from run_ops import run

NEW = ("> **section-usage #285 (self-report, delegated OPUS 5 wrap sub):** "
       "GM HDR:C LATEST:C PRIOR:R DOFIRST:U A:U C1:U C2:U C4:U STRATA:C · "
       "LS HDR:C LANES:U SPIN:U DELTAS:C WEBFONT:U LIVE:U LIFECYCLE:U DEAD:U OPEN:U TARGETS:U SPINOFFS:U")

gm = os.path.join(ROOT, "GOOD-MORNING.md")
old = [l.rstrip("\n") for l in open(gm, encoding="utf-8") if l.startswith("> **section-usage #285")]
assert len(old) == 1, len(old)
assert old[0] != NEW
ops = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [old[0]], "replace": [NEW]}]
sys.exit(run("usagefix", ops, write="--write" in sys.argv, min_bytes=200))
