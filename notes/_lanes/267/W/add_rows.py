#!/usr/bin/env python3
"""#267 wrap — row the session's unrowed documents (`_gate_doc_rows.py`, `s218-D7`).

Six documents were flagged UNROWED by the gate at this wrap's opener, plus one untracked brief
that this wrap's own commit will make tracked (and therefore part of the gate's population), plus
this wrap's own filed report. Every row goes through the store's own writer — this script never
edits `_state.json` text.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state  # noqa: E402

doc = _state.load()

ROWS = [
    ("W-267a", "notes/_briefs/2026-09-10-267-cold-run-6-brief.md",
     "#267 brief - the sixth cold run of the frozen prompt against the v1.0.9 zip, blind, light-led",
     "the C6 findings are answered - canon.css regenerated (done, #267 lane N), the packaging hole "
     "closed (done, v1.0.10), and the two dropdown menus reachable with a mouse",
     ["notes/_subreports/2026-09-10-267-C6-cold-run-6.md"]),
    ("W-267b", "notes/_briefs/2026-09-10-267-kg-sphere-brief.md",
     "#267 brief - restore the KG explorer dig to a world-space sphere after Dave's flat-plane screenshot",
     "the SC dig with default families showing 0 neighbours is repaired or ruled acceptable",
     ["notes/_lanes/2026-09-10-267-K-sphere.md"]),
    ("W-267c", "notes/_briefs/2026-09-10-267-v1010-cut-brief.md",
     "#267 brief - cut v1.0.10 with the packaging hole closed",
     "v1.0.10 is released and pushed (done at de8ed57) and the dataviz cut rule holds at the next cut",
     ["notes/_lanes/2026-09-10-267-P-v1010-cut.md"]),
    ("W-267d", "notes/_briefs/2026-09-10-267-v1010-recut-brief.md",
     "#267 brief - re-cut v1.0.10 with the chart pages shipped by measurement (s267-D1)",
     "the receipt_named_chart_pages rule survives the next release cut without a typed page list",
     ["notes/_lanes/2026-09-10-267-P2-v1010-recut.md"]),
    ("W-267e", "notes/_briefs/2026-09-10-267-edge-judgement-brief.md",
     "#267 brief - judge the 78 proposed ruling edges before any of them is applied",
     "the DECLARED_EDGE_TYPES seam is ruled and gen_kg_edges.py is unfenced",
     ["notes/_lanes/2026-09-10-267-E-edge-judgement.md",
      "notes/_lanes/2026-09-10-267-G-edge-enactment.md"]),
    ("W-267f", "notes/_subreports/2026-09-10-267-C6-cold-run-6.md",
     "#267 C6 filed report - the sixth cold run, 2/3/3/2, and the packaging hole three releases deep",
     "the three top findings are closed - canon.css divergence (closed #267 lane N, ships at v1.0.11), "
     "the missing mint helper (closed at v1.0.10), and rule 18 arguing with the engine",
     ["notes/_briefs/2026-09-10-267-cold-run-6-brief.md",
      "notes/_lanes/2026-09-10-267-N-canon-divergence.md"]),
    ("W-267g", "notes/_subreports/2026-09-10-267-R-release-v1010.md",
     "#267 R filed report - the v1.0.10 release, ten gates green, twice-baked byte-equal",
     "v1.0.11 carries the canon regen the v1.0.10 zip could not",
     ["notes/_lanes/2026-09-10-267-P2-v1010-recut.md"]),
    ("W-267w", "notes/_subreports/2026-09-10-267-W-wrap.md",
     "#267 W filed report - the #267 capture ritual, delegated; steps 1-5 with step 3 DONE at the conductor's seat",
     "the carried items are answered - the run-of-show v1 is reviewed, v1.0.11 carries the canon regen, "
     "the DECLARED_EDGE_TYPES seam is ruled, the eight islands are wired and Dave's N is filled",
     ["knowledge/_RUNBOOK-capture-ritual.md", "_CARRIES.md", "notes/_GAUGE-LOG.md"]),
]

added = []
for _id, home, title, closes, links in ROWS:
    _state.add(doc, id=_id, title=title, state="open", opened=267, owner="dave",
               condition="stated", closes_when=closes, links=links, home=home,
               project="apollo",
               body="s218-D7 / W-20 store row, written at the #267 wrap so the document is visible "
                    "to every carry. Rowed through _state.add(), never by hand-editing the store.")
    added.append(_id)

ok, fails, _ = _state.check(doc)
assert ok, fails
_state.save(doc)
print("added %d rows: %s" % (len(added), " ".join(added)))
