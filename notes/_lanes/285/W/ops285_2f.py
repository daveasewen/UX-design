#!/usr/bin/env python3
"""#285 wrap — step 2f: split the #284 stratum through the mover's own `roll_2f`.

post-mortem half → `notes/_GAUGE-LOG.md` (APPENDED at true EOF, no anchor — #27's prepend must
not be expressible); commit-state half → `_GM-ARCHIVE.md` NEWEST-FIRST under the same
`<date> <session#>` batch key 2c used. Neither half can happen without the other.

⛔ `cs_start` uses the SESSION-QUALIFIED form `> **COMMIT STATE #284:**` — the bare
`> **COMMIT STATE` anchor matches FOUR lines in this file (the rolling stratum plus the EXEMPT
#40/#41/#42 blocks, Dave's #58 ruling) and the mover refuses it, correctly and loudly.

EXIT CHECK, run before this and recorded in `WRAP-REPORT.md`: the stratum's Dave-owed items —
the declared-skips block, and `COMMIT STATE #284`'s `#243` not-a-wrap form, its declared hash
gap and the instrumentation-append policy — all stand in `_CARRIES.md` § `residual → #286` and
are re-declared on this wrap's own `COMMIT STATE #285`.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_ops import run

ops = [{"op": "roll_2f", "session": 284,
        "pm_start": "#### 2026-09-18 #284",
        "pm_end": "> **COMMIT STATE #284:**",
        "cs_start": "> **COMMIT STATE #284:**",
        "cs_end": "#### 2026-08-05 #96",
        "archive_at": "## Batch 2026-09-18 #285"}]
sys.exit(run("roll2f", ops, write="--write" in sys.argv, min_bytes=200))
