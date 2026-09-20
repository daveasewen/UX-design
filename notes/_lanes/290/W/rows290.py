#!/usr/bin/env python3
"""rows290.py — the #290 doc rows, added through `_state.add` (never hand-edited JSON).

One row per document that `_gate_doc_rows.py`'s glob covers and that this wrap stages:
this wrap's own filed report — the ONLY document #290 stages that the gate's glob covers,
because ZERO lanes ran and there are no lane reports. Ids obey the store's own regex
`^(?:W-[0-9]{1,3}[a-z]{0,2}|G[0-9]{1,2}[a-z]?)$` — the #287/#288 lesson: navigate the
pattern the refusal quoted, never re-attempt a shape already refused on the record.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "knowledge"))
import _state  # noqa: E402

STORE = os.path.join(REPO, "knowledge", "_state.json")

ROWS = [
    ("W-290ww", "notes/_subreports/2026-09-20-290-W-wrap.md",
     "#290 W - the delegated capture ritual for #290 -> #291",
     "Every runbook step 1..5b, measured. No ruling inscribed (622 unchanged). ZERO lanes: the catalogue edits were made in seat, a declared departure from s204-D1. The seam check fired at 228,094 and Dave answered 'okay, wrap' - the second session on record to stop on its own instrument. FILL measured 241,485 / 53 turns against 228,094 / 48 declared, delta 13,391, boots agreeing to the token at 74,165.",
     "Dave rules on the six questions put - the acceptance by eye, the in-seat exception, whether s283-D1 becomes blocking, the workers lane, his slide-by-slide read of v11, and the rest of _HANDOFF-130..140"),
]


def main():
    doc = json.load(open(STORE, encoding="utf-8"))
    have = {i["id"] for i in doc["items"]}
    added = []
    for rid, home, title, body, closes in ROWS:
        if rid in have:
            print(f"SKIP {rid} — already present")
            continue
        if not os.path.exists(os.path.join(REPO, home)):
            raise SystemExit(f"REFUSED: {home} does not exist — a row may not name a missing home")
        _state.add(doc, id=rid, home=home, title=title, body=body, state="open",
                   owner="dave", opened=290, project="apollo", closes_when=closes,
                   links=[home])
        added.append(rid)
    ok, fails, notes = _state.check(doc)
    if not ok:
        raise SystemExit("REFUSED: " + "; ".join(fails[:5]))
    tmp = STORE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, STORE)
    print(f"ADDED {len(added)}: {', '.join(added)}")
    print(f"store now {len(doc['items'])} items")


if __name__ == "__main__":
    main()
