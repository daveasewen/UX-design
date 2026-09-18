#!/usr/bin/env python3
"""#285 wrap — step 2f's other half: GM keeps the LATEST stratum only, and this is it.

The #284 block was split out by `roll_2f` first (post-mortem → `notes/_GAUGE-LOG.md` at true
EOF, commit-state → `_GM-ARCHIVE.md` § Batch 2026-09-18 #285), so inserting this one leaves
exactly ONE block under `### ⏱ SESSION STRATA` — "LATEST only" is the entire contract, and the
gate counts BLOCKS, not lines.

⚠ `s241-D2`: ONE first-turn figure per stratum. 80,863 is stated ONCE, in the `POST-MORTEM #285`
line, and nowhere else in this block — asserted here before the mover is called.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_ops import run

block = open(os.path.join(HERE, "stratum285.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert block[0] == "#### 2026-09-18 #285", block[0]
joined = "\n".join(block)
assert joined.count("80,863") == 1, f"REFUSED — first-turn figure appears {joined.count('80,863')} times (`s241-D2`: ONCE)"
assert "job " not in joined.lower(), "REFUSED — the word `job` must not appear near the subs line"
subs = [l for l in block if l.startswith("> **subs ")]
assert len(subs) == 1 and re.fullmatch(r"> \*\*subs [\d,]+ tokens \(n=\d+\)\*\*", subs[0]), subs

ops = [{"op": "insert", "file": "GOOD-MORNING.md",
        "at": "### ⏱ SESSION STRATA", "where": "after",
        "lines": [""] + block + [""]}]
sys.exit(run("stratum", ops, write="--write" in sys.argv, min_bytes=1_000))
