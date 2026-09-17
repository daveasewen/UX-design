#!/usr/bin/env python3
"""#280 wrap — ONE textual span into knowledge/_state.json, proven by reconstruction in THIS
process before anything is written. Never json.load + json.dump: that is the #179 defect (a
serializer reformatting thousands of lines nobody edited), and an insertions-only numstat is what
a span looks like from the outside.

ADD: this wrap's own filed report row, W-280wr (`s218-D7` doc-row gate).
⚠ Nothing is REPAIRED here: `knowledge/_state.py --check` read clean at this ritual's open
(exit 0, zero ⛔), unlike #279's, so there is no inherited row defect to fix and none is invented.
"""
import json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
P = os.path.join(ROOT, "knowledge", "_state.json")
orig = open(P, encoding="utf-8").read()

row = {
 "links": [
   "notes/_lanes/280/W/WRAP-REPORT.md",
   "notes/_lanes/280/WRAP-MEMORY-HOOK.md",
   "notes/_lanes/280/DAVE-RULINGS-2026-09-17.md",
   "_DECISION-HISTORY/2026-09-17-280-the-matrix-and-the-front-door.md",
   "_HANDOFF-131-the-matrix-and-the-front-door.md",
   "knowledge/_rulings.json",
 ],
 "home": "notes/_subreports/2026-09-17-280-W-wrap.md",
 "id": "W-280wr",
 "title": "#280 W filed report - the delegated capture ritual for #280 -> #281",
 "state": "open",
 "owner": "dave",
 "opened": 280,
 "project": "apollo",
 "closes_when": "Dave has ruled or explicitly parked the report's ruling-shaped questions - chiefly the orphan census export (ten radios, his, not received), the eye-check of the six matrix cells, jade-lifestyle, and the wrap-sub memory seat limit now measured false twice",
 "why": "The #280 wrap verified both of the session's rulings by span against git rather than restating them (605 -> 607, 19/0 and 18/0), re-measured every figure the brief declared and published the two that disagreed as two readings (six inherited gate fails declared, seven measured), wrote the cloud memory store from the wrap sub's own seat for the second consecutive wrap against a runbook line that calls that impossible, and minted three carries that had been living only in wrap reports.",
 "condition": "stated",
}
body = json.dumps(row, indent=2, ensure_ascii=False)
body = "\n".join("    " + l if l.strip() else l for l in body.split("\n"))
TAIL = "\n  ]\n}"
assert orig.endswith(TAIL) or orig.endswith(TAIL + "\n"), repr(orig[-12:])
j = orig.rfind(TAIL)
INSERT = ",\n" + body
text = orig[:j] + INSERT + orig[j:]
span = len(INSERT)

# ---- reconstruction proof, before any write --------------------------------------------------
back = text[:j] + text[j + span:]
assert back == orig, "REFUSED — reconstruction failed"
parsed = json.loads(text)
before = json.loads(orig)
assert len(parsed["items"]) == len(before["items"]) + 1
assert parsed["items"][-1]["id"] == "W-280wr"
assert not any(r.get("id") == "W-280wr" for r in before["items"]), "row already present"

if "--write" not in sys.argv:
    print(f"DRY: new row span +{span} B · items {len(before['items'])} → {len(parsed['items'])}; "
          f"reconstruction PASSED")
    sys.exit(0)
open(P, "w", encoding="utf-8").write(text)
print(f"WROTE: W-280wr added (+{span} B); reconstruction PASSED before the write")
