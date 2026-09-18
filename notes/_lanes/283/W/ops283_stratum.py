#!/usr/bin/env python3
"""#283 wrap, 2f — insert THIS session's stratum block under `### ⏱ SESSION STRATA`, at the top
of the stack (GM keeps LATEST only; #281's rolled out through `roll_2f` first).
⛔ Testimony and key are ONE act (ds-022 (d)): the `#### <date> #<N>` key is written above the
entry as the entry is written, never afterwards."""
import os, sys
from run_ops import run
HERE = os.path.dirname(os.path.abspath(__file__))
BODY = open(os.path.join(HERE, "stratum283.md"), encoding="utf-8").read().rstrip("\n").split("\n")
OPS = [{"op": "insert", "file": "GOOD-MORNING.md", "at": "### ⏱ SESSION STRATA",
        "where": "after", "lines": [""] + BODY + [""]}]
if __name__ == "__main__":
    sys.exit(run("stratum", OPS, write="--write" in sys.argv, min_bytes=2000))
