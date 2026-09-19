#!/usr/bin/env python3
"""#288 wrap — step 2f: the ds-022 stratum split, through the mover's `roll_2f`.

⛔ ONE op, and it is the only supported way. The post-mortem half APPENDS at true EOF of
   `notes/_GAUGE-LOG.md` (no anchor argument — #27's prepend must not be expressible); the
   commit-state half goes into `_GM-ARCHIVE.md`'s newest-first batch, which REQUIRES an anchor.
⛔ THE COMMIT-STATE ANCHOR IS THE SESSION-QUALIFIED FORM `> **COMMIT STATE #287:**` — the bare
   `> **COMMIT STATE` matches four lines in this file (the rolling one plus the three EXEMPT
   #40/#41/#42 blocks, Dave's #58 ruling) and the mover refuses it, correctly (#241's homed note).

2f EXIT CHECK, run before this op: the #287 stratum's lessons must ALREADY live in
`knowledge/_RUNBOOK-capture-ritual.md`, not only in the stratum, because a dated home does not
count. Verified by grep, not by memory: the `delta`-is-only-legal-on-one-named-window clause
(homed #272), the take-the-chain-figure-AFTER-the-stamp clause (homed #241), and the
session-owned uniquely-named ops-file contract (homed #166) are each asserted present.
"""
import json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read()
assert gm.count("#### 2026-09-19 #287") == 1
assert gm.count("> **COMMIT STATE #287:**") == 1
assert gm.count("#### 2026-08-05 #96") == 1
assert "#### 2026-09-19 #288" not in gm, "a #288 stratum already exists"
assert "## Batch 2026-09-19 #288" in open(os.path.join(ROOT, "_GM-ARCHIVE.md"), encoding="utf-8").read()

rb = open(os.path.join(ROOT, "knowledge", "_RUNBOOK-capture-ritual.md"), encoding="utf-8").read()
for lesson in ("`unobservable`, NOT A SUBTRACTION",
               "QUOTE IT AFTER THE DECLARE-LAST",
               "GIVE IT A UNIQUE NAME AND ASSERT IT EXISTS"):
    assert lesson in rb, f"EXIT CHECK FAILED — lesson not inscribed in the runbook: {lesson[:44]!r}"
print("2f EXIT CHECK: the #287 stratum's lessons are inscribed in the runbook — safe to roll.")

ops = [{"op": "roll_2f", "session": 287,
        "pm_start": "#### 2026-09-19 #287", "pm_end": "> **COMMIT STATE #287:**",
        "cs_start": "> **COMMIT STATE #287:**", "cs_end": "#### 2026-08-05 #96",
        "archive_at": "## Batch 2026-09-19 #288"}]
OPSF = os.path.join(HERE, f"ops-288-roll2f-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 200
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops")
