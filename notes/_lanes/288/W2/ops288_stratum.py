#!/usr/bin/env python3
"""#288 wrap — insert the #288 session stratum under `### ⏱ SESSION STRATA`.

The stratum is written with `{{SIZES}}`, `{{CHAIN}}` and `{{BANNER}}` placeholders: all three
measure regions that CONTAIN them, so they are filled at the ritual's close (declare-last),
each iterated to a fixed point, through the mover like everything else.
"""
import json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read()
assert gm.count("### ⏱ SESSION STRATA") == 1
assert "#### 2026-09-19 #288" not in gm, "a #288 stratum already exists"
assert "#### 2026-09-19 #287" not in gm, "the #287 stratum has NOT been rolled — run 2f first"

body = open(os.path.join(HERE, "stratum288.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert body[0] == "#### 2026-09-19 #288"
assert sum(1 for l in body if l.startswith("> **COMMIT STATE")) == 1
assert sum(1 for l in body if l.startswith("> **subs ")) == 1
assert not any(" job " in l or l.startswith("> **subs") and "job" in l for l in body if l.startswith("> **subs"))

ops = [{"op": "insert", "file": "GOOD-MORNING.md", "at": "### ⏱ SESSION STRATA",
        "where": "after", "lines": [""] + body + [""]}]
OPSF = os.path.join(HERE, f"ops-288-stratum-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 5000
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops  ({len(body)} stratum lines)")
