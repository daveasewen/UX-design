#!/usr/bin/env python3
"""#283 wrap — repair the `section-usage` line to the vocabulary's own FORM (all 11 LS ids),
caught by `_capture_gate` at the wrap run. ⛔ The IDS come from `--usage-template`; the CODES are
testimony and are written by this seat, not by the tool."""
import sys
from run_ops import run
OLD = "> **section-usage #283 (self-report, delegated OPUS 5 wrap sub):** GM HDR:C LATEST:C PRIOR:R DOFIRST:R A:U C1:U C2:U C4:U STRATA:C · LS HDR:C LANES:U SPIN:U DELTAS:C LIVE:U OPEN:U TARGETS:U"
NEW = "> **section-usage #283 (self-report, delegated OPUS 5 wrap sub):** GM HDR:C LATEST:C PRIOR:R DOFIRST:R A:U C1:U C2:U C4:U STRATA:C · LS HDR:C LANES:U SPIN:U DELTAS:C WEBFONT:U LIVE:U LIFECYCLE:U DEAD:U OPEN:U TARGETS:U SPINOFFS:U"
OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [OLD], "replace": [NEW]}]
if __name__ == "__main__":
    sys.exit(run("usagefix", OPS, write="--write" in sys.argv, min_bytes=100))
