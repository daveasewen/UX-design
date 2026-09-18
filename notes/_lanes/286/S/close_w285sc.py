#!/usr/bin/env python3
"""#286 lane S — close `W-285sc` THROUGH THE STORE'S OWN WRITER.

`knowledge/_state.py` exposes no `--close` CLI: its `__main__` is a REPORTER (`check()` +
`counts()`), and its writer surface is the module API — `load()` / mutate / `check()` / `save()`.
`add()` is the only convenience wrapper and it only ADDS. So the sanctioned close is this shape,
the same one every prior lane used (`notes/_lanes/276/W/carry277.py`, `knowledge/_tmp/wrap241/
mk_rows.py`): import the module, mutate the loaded doc, re-run the BLOCKING gate, and only then
`save()`. `_state.json` is never hand-edited.

The gate at `_state.py:478` is the one that matters here: a row in state `done` with no
non-empty `closed_by` FAILS. The receipt is Dave's words and the rulings file path.

DRY RUN by default; pass `--write` to save.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state  # noqa: E402

RECEIPT = ('#286 2026-09-18 — close condition met: Dave ruled the wording at #286. His words, '
           'verbatim: "okay go on everything", answered to a three-item opener whose item 1 was '
           'the eight standing lines. knowledge/_standing.md is out of DRAFT — header replaced, '
           'the eight lines byte-identical (git diff touches header only); the seam still prints '
           'STANDING 8 lines · 246 cl100k, unchanged. Receipt: '
           'notes/_lanes/286/DAVE-RULINGS-2026-09-18.md, which records that reading his six words '
           'as ratification-as-written is the CONDUCTOR\'S reading, not Dave\'s sentence. '
           'No s286- ruling was inscribed in _rulings.json by this lane — inscribing is a '
           'separate act (s271-D4).')

doc = _state.load()

ok0, fails0, notes0 = _state.check(doc)
print(f"PRE  check ok={ok0} fails={len(fails0)} notes={len(notes0)}")
for f in fails0:
    print("  pre-existing ⛔", f)

row = next(i for i in doc["items"] if i["id"] == "W-285sc")
print("BEFORE:", json.dumps(row, ensure_ascii=False, indent=2))

before_order = [i["id"] for i in doc["items"]]

row["state"] = "done"
row["closed_by"] = RECEIPT
links = row.setdefault("links", [])
for p in ("notes/_lanes/286/DAVE-RULINGS-2026-09-18.md",
          "notes/_subreports/2026-09-18-286-S-standing-ratified.md",
          "knowledge/_standing.md"):
    if p not in links:
        links.append(p)

ok1, fails1, notes1 = _state.check(doc)
print(f"POST check ok={ok1} fails={len(fails1)}")
mine = [f for f in fails1 if f.startswith("W-285sc")]
for f in mine:
    print("  MINE ⛔", f)
if mine:
    sys.exit("REFUSED by the gate — not saving.")

after_order = sorted(doc["items"], key=_state._sort_key)
print("save() would reorder items:", [i["id"] for i in after_order] != before_order)

if "--write" in sys.argv:
    _state.save(doc)
    print("SAVED")
else:
    print("DRY RUN — nothing written")
