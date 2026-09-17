#!/usr/bin/env python3
"""#280 wrap — 2f: insert THIS session's stratum block under `### ⏱ SESSION STRATA`, newest
first. `roll_2f` has already taken #279's block out (post-mortem → `notes/_GAUGE-LOG.md`,
commit-state → `_GM-ARCHIVE.md`), so GM keeps LATEST only, which is D5's whole contract."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_ops import run

block = open(os.path.join(HERE, "stratum280.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert block[0] == "#### 2026-09-17 #280", block[0]
assert sum(1 for l in block if l.startswith("> **COMMIT STATE")) == 1
block = block + [""]

OPS = [{"op": "insert", "file": "GOOD-MORNING.md", "at": "### ⏱ SESSION STRATA",
        "where": "after", "lines": [""] + block}]
print(f"stratum280.md: {len(block)} lines, {sum(len(l) for l in block):,} chars")
sys.exit(run("stratum", OPS, write="--write" in sys.argv))
