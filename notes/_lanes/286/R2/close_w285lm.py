#!/usr/bin/env python3
"""#286 lane R2 — close `W-285lm` THROUGH THE STORE'S OWN WRITER.

Same shape as notes/_lanes/286/S/close_w285sc.py: `knowledge/_state.py` has no `--close`
CLI (its `__main__` is a reporter), so the sanctioned close is the module API —
`load()` / mutate / `check()` / `save()`. `_state.json` is never hand-edited.

`closes_when` is UNCHANGED and is not rewritten: "Dave has looked at the 4x before/after
contact sheet and either accepted the regenerated masters by eye or named what still looks
wrong". Its literal condition was met at #285 (he accepted by eye). #285 and #286 lane R
both held the row OPEN because the registration the row is about was still owed. It is no
longer owed: this lane registered the 40 masters and MEASURED the result.

DRY RUN by default; pass `--write` to save.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state  # noqa: E402

RECEIPT = (
    '#286 2026-09-18 lane R2 — BOTH HALVES NOW MET. (1) THE EYE: Dave accepted the '
    'regenerated masters at #285 on the 4x before/after contact sheet — the literal '
    '`closes_when`. (2) THE REGISTRATION the row was held open for is DONE. Dave ruled the '
    'shape on 2026-09-18, verbatim: "okay size-on-the-existing-node" — a master is a SIZE '
    'FIELD on its lockup\'s existing node, not a node of its own (receipt: '
    'notes/_lanes/286/DAVE-RULINGS-2026-09-18.md). `gen_kg_icons.py` was taught '
    '`assets/logos/masters/` and run ONCE with --land --ratified s277-D4. MEASURED, not '
    'asserted: knowledge/_logo_nodes.json nodes 8 -> 8 (0 added, 0 removed), edges 33 -> 33 '
    'with the multiset identical, and the only changes are a new `sizes` map on each of the 8 '
    'logo nodes (40 entries, heights 24/28/32/36/40, each carrying the relative path, the '
    'SVG\'s own width/height and its sha256 — all 40 re-verified against the bytes on disk) '
    'plus `$description` and `$s282-D5.generatorVerdict`. HAND-AUTHORED STATE SURVIVED: the 12 '
    '`governedBy` edges of s282-D5 are byte-identical after the run, 0 t:null stubs came back, '
    '`ratified` and `$s282-D5` are intact, and no field was lost anywhere in either output '
    '(loss test parsed). `--land` now MERGES on write instead of clobbering, so re-applying '
    'notes/_lanes/282/logo-land/bind.py after a regenerate is no longer needed. Receipt: '
    'notes/_subreports/2026-09-18-286-R2-masters-registered-as-sizes.md.')

doc = _state.load()

ok0, fails0, notes0 = _state.check(doc)
print(f"PRE  check ok={ok0} fails={len(fails0)} notes={len(notes0)}")
for f in fails0:
    print("  pre-existing ⛔", f)

row = next(i for i in doc["items"] if i["id"] == "W-285lm")
print("BEFORE state:", row["state"])
print("BEFORE closes_when:", row["closes_when"])

before_order = [i["id"] for i in doc["items"]]
before_closes = row["closes_when"]

row["state"] = "done"
row["closed_by"] = RECEIPT
links = row.setdefault("links", [])
for p in ("notes/_lanes/286/DAVE-RULINGS-2026-09-18.md",
          "notes/_subreports/2026-09-18-286-R2-masters-registered-as-sizes.md",
          "notes/_subreports/2026-09-18-286-R-masters-registered.md",
          "notes/_lanes/277/icons-propose/gen_kg_icons.py",
          "knowledge/_logo_nodes.json"):
    if p not in links:
        links.append(p)

ok1, fails1, notes1 = _state.check(doc)
print(f"POST check ok={ok1} fails={len(fails1)}")
for n in notes1:
    print("  NOTE:", n)
mine = [f for f in fails1 if f.startswith("W-285lm")]
for f in mine:
    print("  MINE ⛔", f)
if mine:
    sys.exit("REFUSED by the gate — not saving.")

after_order = sorted(doc["items"], key=_state._sort_key)
print("save() would reorder items:", [i["id"] for i in after_order] != before_order)
print("closes_when unchanged:", row["closes_when"] == before_closes)

if "--write" in sys.argv:
    _state.save(doc)
    print("SAVED")
    fresh = next(i for i in _state.load()["items"] if i["id"] == "W-285lm")
    print("AFTER state:", fresh["state"], "| closes_when unchanged:",
          fresh["closes_when"] == before_closes,
          "| closed_by len:", len(fresh.get("closed_by") or ""))
    print("counts:", json.dumps(_state.counts(_state.load())))
else:
    print("DRY RUN — nothing written")
