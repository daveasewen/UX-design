#!/usr/bin/env python3
"""#286 wrap — insert the #286 stratum under `### ⏱ SESSION STRATA`, GM keeping LATEST only."""
import json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
body = open(os.path.join(HERE, "stratum286.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert body[0] == "#### 2026-09-18 #286", body[0]
gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read()
assert "#### 2026-09-18 #286" not in gm, "already inserted"
assert "#### 2026-09-18 #285" not in gm, "2f has not run — the #285 stratum is still in GM"
assert gm.count("### ⏱ SESSION STRATA") == 1
ops = [{"op": "insert", "file": "GOOD-MORNING.md", "at": "### ⏱ SESSION STRATA",
        "where": "after", "lines": [""] + body}]
OPSF = os.path.join(HERE, f"ops-286-stratum-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 8_000
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops · stratum {len(body)} ln")
