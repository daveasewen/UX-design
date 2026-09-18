#!/usr/bin/env python3
"""#282 wrap, 2f — roll the #281 stratum out of GOOD-MORNING.md (post-mortem → notes/_GAUGE-LOG.md,
COMMIT STATE → _GM-ARCHIVE.md) through the mover's `roll_2f`. GM keeps LATEST only.
⛔ The COMMIT STATE anchor is the SESSION-QUALIFIED form — the bare `> **COMMIT STATE` matches
FOUR blocks in this file (the #40/#41/#42 exempt ones) and the mover refuses it, correctly."""
import sys
from run_ops import run
OPS = [{"op": "roll_2f", "session": 281,
        "pm_start": "#### 2026-09-17 #281",
        "pm_end": "> **COMMIT STATE #281:**",
        "cs_start": "> **COMMIT STATE #281:**",
        "cs_end": "#### 2026-08-05 #96"}]
if __name__ == "__main__":
    sys.exit(run("roll2f", OPS, write="--write" in sys.argv, min_bytes=100))
