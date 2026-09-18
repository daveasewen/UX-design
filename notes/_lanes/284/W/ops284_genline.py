#!/usr/bin/env python3
"""#284 wrap — substitute the GENERATED residual line on the ★ LATEST banner with
`knowledge/_roll_state.py`'s own output, AFTER 2c/2d/2f have run. The figure is GENERATED,
never typed: a roll-state claim written by hand is a claim nobody can probe."""
import subprocess, sys, os
from run_ops import run
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
OLD = "> **residual (GENERATED #284):** PENDING — substituted after 2f by ops284_genline.py"
NEW = subprocess.run([sys.executable, "knowledge/_roll_state.py"], cwd=ROOT,
                     capture_output=True, text=True).stdout.strip().split("\n")[-1]
assert NEW.startswith("> **residual (GENERATED #284):** 2c OK"), NEW
OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [OLD], "replace": [NEW]}]
if __name__ == "__main__":
    print("GENERATED:", NEW)
    sys.exit(run("genline", OPS, write="--write" in sys.argv, min_bytes=100))
