#!/usr/bin/env python3
"""#316 lane PR - add the two born-closed report rows the doc-row gate asks for: W-316ct (lane CT's own
prepared row, notes/_lanes/316/CT/_state-row.json, which did not land in f0d66dfd) and W-316pr (this lane).
Goes through knowledge/_state.py's load / add / check / save; no count is hand-edited."""
import json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state as S  # noqa: E402
doc = S.load()
ids = {i["id"] for i in doc["items"]}
ct = json.load(open(os.path.join(ROOT, "notes/_lanes/316/CT/_state-row.json"), encoding="utf-8"))
if ct["id"] not in ids:
    S.add(doc, **ct)
if "W-316pr" not in ids:
    S.add(doc, **{"id": "W-316pr",
        "title": "#316 lane PR report - the pending roundel amber in both modes with the clock hands only (s315-D7/D33) and the footer dark in dark on a minted surface/dark-band (s315-D40)",
        "project": "apollo", "opened": 316, "owner": "claude", "condition": "stated",
        "home": "notes/_subreports/2026-10-03-316-PR.md", "links": [], "state": "done",
        "closes_when": "the report is committed", "body": "s218-D7 filed report.",
        "closed_by": "born closed (s305-D40): notes/_subreports/2026-10-03-316-PR.md filed at #316 - the file is the record."})
ok, fails, _ = S.check(doc)
if not ok:
    raise SystemExit("REFUSED by the store gate:\n  " + "\n  ".join(fails[:12]))
S.save(doc); print("rows added; store check OK")
