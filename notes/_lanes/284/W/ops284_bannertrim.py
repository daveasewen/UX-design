#!/usr/bin/env python3
"""#284 wrap — a FOURTH compression pass on the ★ LATEST banner, run AFTER the GENERATED
residual line landed: the real `_roll_state.py` line is longer than the placeholder it
replaced and took the banner to 1,207 of the `s241-D2` cap of 1,200. Girth only — no item,
carry, declared skip or receipt is dropped. Measured before and after."""
import sys
from run_ops import run
OPS = [
 {"op": "replace", "file": "GOOD-MORNING.md",
  "find": ["> - ⛔ ① **NO RULING INSCRIBED — `_rulings.json` STAYS 620**, `json.load` here. **④ and ⑤ are the two ruling-shaped things, written as QUESTIONS PUT and NOT inscribed: that is his.**"],
  "replace": ["> - ⛔ ① **NO RULING INSCRIBED — `_rulings.json` STAYS 620**, `json.load` here. **④ and ⑤ are the two ruling-shaped things, QUESTIONS PUT and NOT inscribed: his.**"]},
]
if __name__ == "__main__":
    sys.exit(run("bannertrim", OPS, write="--write" in sys.argv, min_bytes=100))
