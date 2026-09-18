#!/usr/bin/env python3
"""#282 wrap — replace the PENDING `residual (GENERATED #282)` line with `_roll_state.py`'s own
output. A generated line, quoted, never retyped."""
import sys
from run_ops import run
OLD = "> **residual (GENERATED #282):** PENDING — written after 2c/2d/2f and the stratum"
NEW = ("> **residual (GENERATED #282):** 2c OK (banners 2/2) · 2d OK (deltas 3/3) · "
       "2f OK (strata 1, log #281) — _roll_state.py · 2026-09-18")
OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [OLD], "replace": [NEW]}]
if __name__ == "__main__":
    sys.exit(run("genline", OPS, write="--write" in sys.argv, min_bytes=100))
