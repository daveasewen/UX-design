#!/usr/bin/env python3
"""#283 wrap — write the GENERATED residual line onto the banner, from `_roll_state.py`'s own
output, through the mover. It is GENERATED: never typed, never adjusted."""
import subprocess, sys, os
from run_ops import run
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
GEN = subprocess.run([sys.executable, "knowledge/_roll_state.py"], cwd=ROOT,
                     capture_output=True, text=True).stdout.strip()
assert GEN.startswith("> **residual (GENERATED #283):**"), GEN[:80]
OLD = "> **residual (GENERATED #283):** PENDING — written after 2c/2d/2f and the stratum"
OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [OLD], "replace": [GEN]}]
if __name__ == "__main__":
    sys.exit(run("genline", OPS, write="--write" in sys.argv, min_bytes=100))
