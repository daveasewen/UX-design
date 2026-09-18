#!/usr/bin/env python3
"""#284 wrap, 2f — insert the NEW `#### 2026-09-18 #284` stratum under `### ⏱ SESSION STRATA`
in GOOD-MORNING.md. GM keeps LATEST only; the #283 block has already been split out by
`ops284_2f.py`, so this insert leaves exactly one un-exempt block.

The `s214-D6` chain figure is a `{{S214D6}}` placeholder here and is substituted by
`ops284_s214d6.py` AFTER the declare-last `size:` stamp — the #241 clause: the stamp is
itself inside the chain slice, so the chain must be re-read after it lands.
"""
import os, sys
from run_ops import run

HERE = os.path.dirname(os.path.abspath(__file__))
block = open(os.path.join(HERE, "stratum284.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert block[0] == "#### 2026-09-18 #284", block[0]
assert any(l.startswith("> **COMMIT STATE #284:**") for l in block)
assert any(l.startswith("> **subs 159,965 tokens (n=1)**") for l in block)
assert not any(" job " in l for l in block), "the `job` containment rule on the subs line"

OPS = [
    {"op": "insert", "file": "GOOD-MORNING.md", "at": "### ⏱ SESSION STRATA", "where": "after",
     "lines": [""] + block + [""]},
]

if __name__ == "__main__":
    sys.exit(run("stratum", OPS, write="--write" in sys.argv, min_bytes=2000))
