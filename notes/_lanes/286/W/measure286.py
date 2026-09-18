#!/usr/bin/env python3
"""#286 lane W — first-hand gauge measurement, by IMPORTING _checkin.read_fill.

⛔ ONE implementation of the FILL rule exists and it is `_checkin.read_fill`.
This script does NOT re-implement it — it points it at named transcripts, so the
figures it publishes are the gauge's own, not a second opinion.
"""
import glob
import json
import os
import sys

REPO = "/sessions/nifty-eager-euler/mnt/UX-design"
sys.path.insert(0, os.path.join(REPO, "knowledge"))
import _checkin  # noqa: E402

CONDUCTOR = ("/sessions/nifty-eager-euler/mnt/.claude/projects/session/"
             "f00a81c6-812c-4fb9-b2e1-90eec24a3c47.jsonl")
SUBDIR = ("/sessions/nifty-eager-euler/mnt/.claude/projects/session/"
          "f00a81c6-812c-4fb9-b2e1-90eec24a3c47/subagents")

assert os.path.exists(CONDUCTOR), f"conductor transcript missing: {CONDUCTOR}"
assert os.path.getsize(CONDUCTOR) > 10_000, "conductor transcript implausibly small"

out = {}

f = _checkin.read_fill(CONDUCTOR)
out["conductor"] = {"boot": f["boot"], "now": f["now"], "peak": f["peak"],
                    "turns": f["turns"], "drops": f.get("drops"),
                    "compaction_records": f.get("compaction_records"),
                    "skipped_synthetic": f.get("skipped_synthetic")}

subs = []
for p in sorted(glob.glob(os.path.join(SUBDIR, "agent-*.jsonl"))):
    try:
        s = _checkin.read_fill(p)
    except Exception as e:                     # noqa: BLE001 — named, never swallowed
        subs.append({"path": os.path.basename(p), "error": repr(e)})
        continue
    if not s.get("available"):
        subs.append({"path": os.path.basename(p), "unavailable": s.get("reason", "")[:80]})
        continue
    subs.append({"path": os.path.basename(p), "boot": s["boot"], "last": s["now"],
                 "peak": s["peak"], "turns": s["turns"], "bytes": os.path.getsize(p)})
out["subs"] = subs
avail = [s for s in subs if "last" in s]
out["subs_n"] = len(avail)
out["subs_sum_last"] = sum(s["last"] for s in avail)
out["subs_sum_peak"] = sum(s["peak"] for s in avail)

print(json.dumps(out, indent=1))
