#!/usr/bin/env python3
"""#287 wrap — step 2f: the ds-022 stratum split, through the mover's `roll_2f`.

⛔ ONE op, and it is the only supported way. The post-mortem half APPENDS at true EOF of
   `notes/_GAUGE-LOG.md` (no anchor argument — #27's prepend must not be expressible); the
   commit-state half goes into `_GM-ARCHIVE.md`'s newest-first batch, which REQUIRES an anchor.
⛔ THE COMMIT-STATE ANCHOR IS THE SESSION-QUALIFIED FORM `> **COMMIT STATE #286:**` — the bare
   `> **COMMIT STATE` matches four lines in this file (the rolling one plus the three EXEMPT
   #40/#41/#42 blocks, Dave's #58 ruling) and the mover refuses it, correctly (#241's homed note).

2f EXIT CHECK, run before this op: the #286 stratum's two lessons — that `delta` is only a legal
subtraction when both terms read the SAME named window, and that the `s214-D6` chain figure is
taken AFTER the declare-last `size:` stamp — are ALREADY inscribed in
`knowledge/_RUNBOOK-capture-ritual.md` (homed at the #272 and #241 wraps respectively), so no
lesson is rolling into a dated home. Verified by grep, not by memory.
"""
import json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read()
assert gm.count("#### 2026-09-18 #286") == 1
assert gm.count("> **COMMIT STATE #286:**") == 1
assert gm.count("#### 2026-08-05 #96") == 1
assert "#### 2026-09-19 #287" not in gm, "a #287 stratum already exists"
assert "## Batch 2026-09-19 #287" in open(os.path.join(ROOT, "_GM-ARCHIVE.md"), encoding="utf-8").read()

# EXIT CHECK — the two lessons must already live in the runbook, not only in the stratum.
rb = open(os.path.join(ROOT, "knowledge", "_RUNBOOK-capture-ritual.md"), encoding="utf-8").read()
for lesson in ("`unobservable`, NOT A SUBTRACTION",
               "QUOTE IT AFTER THE DECLARE-LAST"):
    assert lesson in rb, f"EXIT CHECK FAILED — lesson not inscribed in the runbook: {lesson[:40]!r}"
print("2f EXIT CHECK: both #286 stratum lessons are inscribed in the runbook — safe to roll.")

ops = [{"op": "roll_2f", "session": 286,
        "pm_start": "#### 2026-09-18 #286", "pm_end": "> **COMMIT STATE #286:**",
        "cs_start": "> **COMMIT STATE #286:**", "cs_end": "#### 2026-08-05 #96",
        "archive_at": "## Batch 2026-09-19 #287"}]
OPSF = os.path.join(HERE, f"ops-287-roll2f-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 200
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops")
