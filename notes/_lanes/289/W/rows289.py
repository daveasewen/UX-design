#!/usr/bin/env python3
"""rows289.py — the #289 doc rows, added through `_state.add` (never hand-edited JSON).

One row per document that `_gate_doc_rows.py`'s glob covers and that this wrap stages:
the fourteen filed lane reports, this wrap's own filed report, and the #288 test brief
that stood untracked in the tree at the open. Ids obey the store's own regex
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
    ("W-289ga", "notes/_subreports/2026-09-19-289-G1-deck-v8.md",
     "#289 G1 - deck v8 slides 1-5, the first draft on Dave's arc board",
     "Five sections s1-s5 plus one scoped style block; s1 copied from v7 byte for byte on his word 'keep the opening slide as it is'. Superseded as a deck by v9/v10 but kept as the fragment record.",
     "Dave has read the v10 deck slide by slide and said what stays; until then the v8 fragments are history, not a queue item"),
    ("W-289gb", "notes/_subreports/2026-09-19-289-G2-deck-v8.md",
     "#289 G2 - deck v8 slides 6-9, the library, the explorer, the build, what she is made of",
     "Four slide sections, no new style block - every class already in v7's CSS. Superseded by v9/v10.",
     "same as W-289ga: his slide-by-slide read of v10"),
    ("W-289gc", "notes/_subreports/2026-09-19-289-G3-deck-v8.md",
     "#289 G3 - deck v8 slides 10-13, and the three slides Dave dropped",
     "s10-s13 with a scoped style block. His word dropped 10-11-12 (KPIs, scorecard, ask) - the fragments are KEPT for a later deck for a future audience, by his own framing.",
     "Dave asks for the KPI/scorecard/ask deck, or rules those slides dead"),
    ("W-289ha", "notes/_subreports/2026-09-19-289-H1-library-buildout-numbers.md",
     "#289 H1 - the library build-out, measured, every figure with its source line",
     "REPO says 32 real component metas at 87a71e4f (2026-06-18); ~38 at the build-out proposal; 137 today. Dave's own figure for the story is 36 (the Figma count, his word). Both readings published; neither rewritten.",
     "the deck and the proposal both state the figure Dave ruled (36 -> 137 = 125 components + 12 templates on 8 foundations) and the repo's 32 is recorded beside it, which is done in the v2 proposal and carries to v3"),
    ("W-289hb", "notes/_subreports/2026-09-19-289-H2-library-buildout-story.md",
     "#289 H2 - the library build-out as a story the record can back",
     "Legend-marked narrative: HIS WORD / RULED / READING, each with file+line. Feeds beats 02-03 of the proposal.",
     "proposal v3 lands with the premise as beat zero and this narrative behind beats 02-03"),
    ("W-289hc", "notes/_subreports/2026-09-20-289-H3-agentic-loops-experiment.md",
     "#289 H3 - the pair of agentic loops, and what they showed",
     "Dave: 'this is the story about the experiments with a pair of agentic loops, its in the archive i think'. The record holds TWO A/B pairs three weeks apart - component grain (Tabs, 2026-06-19) and screen grain (30 June / 7 July) - and the lane names which one he probably means rather than choosing silently.",
     "the robots slide carries the experiment Dave recognises as his, or he names the other one"),
    ("W-289da", "notes/_subreports/2026-09-20-289-D1-deck-v9.md",
     "#289 D1 - deck v9, the recut on Dave's seven beats with the first three drawings",
     "12 slides at notes/_DEMO-SLIDES-apollo-2026-09-20-v9.html. Superseded by v10 the same day.",
     "v11 lands, or Dave rules v10 final"),
    ("W-289db", "notes/_subreports/2026-09-20-289-D2-deck-v10.md",
     "#289 D2 - deck v10, three more drawings in and the five-up anatomy",
     "12 slides at notes/_DEMO-SLIDES-apollo-2026-09-20-v10.html - the WORKING deck. Lane flags NOT acted on: s4-s8 are five white cards in a row, callipers fill half their card, the gearbox scale bar rides into the s10 Parts cell, brain frame a hair heavier than the gearbox's.",
     "deck v11 lands with the D2 flags answered and Dave has read v10 slide by slide"),
    ("W-289ia", "notes/_subreports/2026-09-20-289-I1-brain-illustration.md",
     "#289 I1 - the brain in the gearbox's line-drawn 3D hand, six passes",
     "notes/_lanes/289/illustration/brain.html; passes v1-v5 preserved beside it. v6 traces Dave's own side-view reference and mirrors the hemispheres on his word. His verdict: 'okay this is good for now'. CAVEAT carried: top and front views still read narrower than a real brain.",
     "Dave rules the brain finished, or names what to change in the top/front views"),
    ("W-289ib", "notes/_subreports/2026-09-20-289-I2-books-illustration.md",
     "#289 I2 - a stack of books, the knowledge metaphor",
     "notes/_lanes/289/illustration/books.html; v1 with the curved spine kept as books-v1.html after his correction 'these edges should be straight :)'.",
     "the catalogue page replaces books on v10 s6, or Dave keeps the books there"),
    ("W-289ic", "notes/_subreports/2026-09-20-289-I3-arm-illustration.md",
     "#289 I3 - industrial robot arm, a six-axis kinematic chain",
     "notes/_lanes/289/illustration/arm.html. Built from his engineering-drawing references (stock, watermarked, NOT filed - the idea only, by his word).",
     "the arm is placed on a slide Dave has read, or retired"),
    ("W-289id", "notes/_subreports/2026-09-20-289-I4-line-scene.md",
     "#289 I4 - the line scene, two arms either side of a conveyor",
     "notes/_lanes/289/illustration/line.html, on his word 'I wonder if the robots slide could have two robots spaced apart on either side of a conveyor belt'. CAVEAT: the far arm can read as floating at yaw extremes.",
     "Dave rules the s5 line scene right, or names the yaw fix"),
    ("W-289ie", "notes/_subreports/2026-09-20-289-I5-callipers-illustration.md",
     "#289 I5 - callipers, the inspector's instrument",
     "notes/_lanes/289/illustration/callipers.html. His word: 'callipers are good'. CAVEATS: the jaws read wedge-like and the drawing fills half its card on s8.",
     "the s8 callipers are re-scaled in v11 or Dave rules the card right as drawn"),
    ("W-289if", "notes/_subreports/2026-09-20-289-I6-catalogue-illustration.md",
     "#289 I6 - the open catalogue, the inventory metaphor",
     "notes/_lanes/289/illustration/catalogue.html, built on 'The inventory slide (06) I think this should be an open book, like a catalogue'. His follow-up while the lane ran asks for a variant: 'or maybe just a page from a catalogue with a grid of the parts, image description etc' - the PAGE variant is OWED and is #290's first job.",
     "the catalogue PAGE variant is drawn and replaces books on v10 s6"),
    ("W-289ww", "notes/_subreports/2026-09-20-289-W-wrap.md",
     "#289 W - the delegated capture ritual for #289 -> #290, every step, every figure with its source",
     "s218-D7 filed report for the wrap seat itself: the ritual's steps, the gauge re-measured first-hand against the conductor's transcript, the carry set, the date split declared in the #241 shape, the commit, the push and the CI read-back.",
     "the #290 opener has read it, or its REPLAY-THESE items are replayed"),
    ("W-289tb", "notes/_briefs/2026-09-19-288-test-brief-ceo-international-banking.md",
     "#288 test brief - the CEO International Banking page, Dave's own test brief for the one-shot probes",
     "Written by Dave at #288 on his word 'I'll create a test brief for these tests' and left UNTRACKED in the tree through #289; committed by this wrap with its GRILL-SOURCE sibling. It closes #288's finding that the frozen demo prompt is not recoverable and that two probe pages answered different briefs.",
     "a cold one-shot has been run against this brief and its result put to Dave"),
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
                   owner="dave", opened=289, project="apollo", closes_when=closes,
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
