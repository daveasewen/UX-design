#!/usr/bin/env python3
"""#282 wrap — repair the `section-usage #282` line: the LS half must testify EVERY section, and
the first draft omitted WEBFONT, LIFECYCLE, DEAD and SPINOFFS. The gate is right to call a
partial line WORSE than a missing one — it reads as complete testimony and is not."""
import sys
from run_ops import run
OLD = ("> **section-usage #282 (self-report, delegated OPUS 5 wrap sub):** GM HDR:C LATEST:C PRIOR:R "
       "DOFIRST:R A:U C1:U C2:U C4:U STRATA:C · LS HDR:C LANES:U SPIN:U DELTAS:C LIVE:U OPEN:U TARGETS:U")
NEW = ("> **section-usage #282 (self-report, delegated OPUS 5 wrap sub):** GM HDR:C LATEST:C PRIOR:R "
       "DOFIRST:R A:U C1:U C2:U C4:U STRATA:C · LS HDR:C LANES:U SPIN:U DELTAS:C WEBFONT:U LIVE:U "
       "LIFECYCLE:U DEAD:U OPEN:U TARGETS:U SPINOFFS:U")
OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [OLD], "replace": [NEW]}]
if __name__ == "__main__":
    sys.exit(run("usagefix", OPS, write="--write" in sys.argv, min_bytes=100))
