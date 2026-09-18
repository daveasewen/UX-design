#!/usr/bin/env python3
"""#286 wrap — step 2f: the ds-022 stratum split, through the mover's `roll_2f`.

⛔ ONE op, and it is the only supported way. The post-mortem half APPENDS at true EOF of
   `notes/_GAUGE-LOG.md` (no anchor argument — #27's prepend must not be expressible); the
   commit-state half goes into `_GM-ARCHIVE.md`'s newest-first batch, which REQUIRES an anchor.
⛔ THE COMMIT-STATE ANCHOR IS THE SESSION-QUALIFIED FORM `> **COMMIT STATE #285:**` — the bare
   `> **COMMIT STATE` matches four lines in this file (the rolling one plus the three EXEMPT
   #40/#41/#42 blocks) and the mover refuses it, correctly (#241's homed note).
"""
import json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read()
assert gm.count("#### 2026-09-18 #285") == 1
assert gm.count("> **COMMIT STATE #285:**") == 1
assert gm.count("#### 2026-08-05 #96") == 1
assert "#### 2026-09-18 #286" not in gm, "a #286 stratum already exists"
assert "## Batch 2026-09-18 #286" in open(os.path.join(ROOT, "_GM-ARCHIVE.md"), encoding="utf-8").read()

ops = [{"op": "roll_2f", "session": 285,
        "pm_start": "#### 2026-09-18 #285", "pm_end": "> **COMMIT STATE #285:**",
        "cs_start": "> **COMMIT STATE #285:**", "cs_end": "#### 2026-08-05 #96",
        "archive_at": "## Batch 2026-09-18 #286"}]
OPSF = os.path.join(HERE, f"ops-286-roll2f-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 200
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops")
