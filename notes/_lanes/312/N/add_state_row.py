#!/usr/bin/env python3
"""Adds lane N1's born-closed store row (s305-D40 form) to knowledge/_state.json.

knowledge/_state.json is job A's single-writer file this wave, so lane N1 (cloud, never
commits) did not touch it. AC runs this once at the 15:00 wave, from the repo root:

    python3 notes/_lanes/312/N/add_state_row.py            # dry: prints the row
    python3 notes/_lanes/312/N/add_state_row.py --write    # adds it, byte-exact round-trip

Refuses to add the row twice.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state  # noqa: E402

HOME = "notes/_subreports/2026-10-01-312-N1-adapter-schema.md"
ROW = dict(
    id="W-312n1",
    title="#312 lane N1 report - s311-D7 adapter schema + gate + first manifest (adapters/schema.json, _validate_adapter.py in test_gates, adapters/sutherland-react.json 4 unverified / 134 unmapped) and the Copilot kit for Dave's work machine (adapters/kits/sutherland-react/)",
    project="apollo",
    opened=312,
    owner="claude",
    state="done",
    closes_when="the report is committed",
    closed_by="born closed (s305-D40): %s filed at #312 - the file is the record." % HOME,
    body="s218-D7 filed report.",
    home=HOME,
)


def main(argv):
    doc = _state.load()
    if any(i.get("id") == ROW["id"] for i in doc["items"]):
        print("row %s already present - nothing to do" % ROW["id"])
        return 0
    if "--write" not in argv:
        print(json.dumps(ROW, indent=2, ensure_ascii=False))
        print("dry run - pass --write to add it")
        return 0
    _state.add(doc, **ROW)
    _state.save(doc)
    print("added %s to knowledge/_state.json" % ROW["id"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
