#!/usr/bin/env python3
"""#282 wrap, step 4b — write the GENERATED forward title into GOOD-MORNING.md through the mover.
The line is `_gen_titles.py`'s stdout, not a fresh prose recall (#119/#120)."""
import sys
from run_ops import run
OLD = "> **TITLE THE NEXT CHAT →** `Apollo - #282: the rule notes and the eye-check`"
NEW = "> **TITLE THE NEXT CHAT →** `Apollo - #283: the logo masters and the third dial`"
OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [OLD], "replace": [NEW]}]
if __name__ == "__main__":
    sys.exit(run("title", OPS, write="--write" in sys.argv, min_bytes=100))
