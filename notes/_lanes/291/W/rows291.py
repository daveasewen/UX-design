#!/usr/bin/env python3
"""rows290.py — the #291 doc rows, added through `_state.add` (never hand-edited JSON).

One row per document that `_gate_doc_rows.py`'s glob covers and that this wrap stages:
this wrap's own filed report — the ONLY document #291 stages that the gate's glob covers,
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
    ("W-291ww", "notes/_subreports/2026-09-21-291-W-wrap.md",
     "#291 W - the delegated capture ritual for #291 -> #292",
     "Every runbook step 1..5b, measured. No ruling inscribed (622 unchanged). NINE Opus lanes, none in seat: the two workers drawn six times by Dave's eye in one day, v6 onto deck v12 slide 4 with the robots kept on 5, and slide 10 recut to three cells with bigger drawings. The seam check fired at 220,302, was overridden once by another note from Dave, then obeyed - the third firing on record and the first human override. FILL measured 264,714 / 76 turns against 245,652 / 66 declared, delta 19,062, boots agreeing to the token at 74,155. DATE SPLIT: session and both commits 2026-09-20, push and ritual 2026-09-21, nothing re-dated.",
     "Dave rules on the five questions put - the six acceptances by eye and what the 'almost' is, Parts on slide 10 being the gearbox or the catalogue, the arm drawing's home, advisory versus blocking on the tolerance arm, and slide 4's copy - plus his slide-by-slide read of v12 and the rest of _HANDOFF-130..141"),
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
                   owner="dave", opened=291, project="apollo", closes_when=closes,
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
