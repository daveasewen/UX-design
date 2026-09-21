#!/usr/bin/env python3
"""#292 wrap seat — doc rows for the B3 lane report and this wrap's own filed report.

Continues `knowledge/_tmp/wrap292/rows292b.py`'s pattern (seat 2's W-515/W-516): rows are
added through `_state.add()`, never by hand-editing `_state.json`, and `_state.check()` must
pass before the store is written. Ids obey the store's own regex
`^(?:W-[0-9]{1,3}[a-z]{0,2}|G[0-9]{1,2}[a-z]?)$`.

usage:  python3 rows292w.py W-517 [W-518]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "knowledge"))
import _state  # noqa: E402

S = "notes/_subreports/2026-09-21-292-"

ROWS = {
    "W-517": dict(
        project="apollo", owner="claude", opened=292, state="open",
        home=S + "B3-brain-inline-with-tray.md",
        links=["notes/_lanes/289/illustration/brain.html",
               "notes/_lanes/289/illustration/brain-v8.html",
               "notes/_lanes/289/illustration/brain-rest.png",
               "notes/_lanes/292/B3/two-up.png",
               "notes/_lanes/292/B3/top-check.png",
               "notes/_lanes/292/B3/alt-body-23-tray-35.png",
               "notes/_lanes/292/B3/axis-overlay.png"],
        title="#292 LANE B3 FILED - the brain turned back inline with its tray at the alternate's "
              "angle, on Dave's word ('two up alt is better but we need to orientate the brain so "
              "its inline with the tray as it was before, but this is the right angle'): ONE "
              "CONSTANT MOVED, YAW0 -35 -> -50, and nothing else - PIT0, YAW_R, PIT_R, TAU, AOV, "
              "setView, the projection, the fit, the trace and the ink all untouched; pass eight "
              "preserved byte-for-byte as brain-v8.html; screen residual back to 6.10 degrees and "
              "the plan split back to 0 from B2's alternate's 14.81 / 15.0",
        body="Filed report. ONE CAMERA IS THE WHOLE DIAGNOSIS - `a` is BOTH the brain's "
             "front-back axis AND the tray's long axis (the tray is box(u, a, b) over the same "
             "`a` the trace runs along), so under one camera the two long axes are parallel by "
             "construction at every yaw. B2's alternate was not one camera: body -50 with the "
             "tray held at -35 is a 15-degree rotation of the body about `b` relative to the "
             "tray, and that relative rotation is the entire defect. The fix puts it back to "
             "zero while LEAVING THE BODY WHERE THE ALTERNATE HAD IT - the tray follows the body "
             "to -50 rather than the body being dragged back to -35 (which is pass eight, the "
             "frame Dave did not pick); the brain in two-up.png is pixel-identical to "
             "two-up-alt.png's brain. Computed, not eyeballed: 51 candidate poses rendered and "
             "measured (a 36-frame body-yaw sweep at 10 degrees with the tray split off, plus 15 "
             "full frames), the plate edge and body pole line taken in closed form off the "
             "orthographic projection, and a pitch-88 plan render as the check. Blob PCA of the "
             "body silhouette was TRIED AND DISCARDED - elongation runs 1.0-1.3 at every useful "
             "yaw so the principal axis is noise. COSTS, NAMED: eye.a = +0.72 (the back turned "
             "further towards us than pass eight's +0.54, which is what the alternate bought and "
             "what Dave kept) and body foreshortening 0.842 -> 0.694, i.e. the brain is 18% "
             "shorter on screen than at -35. Plate plan proportion UNCHANGED at 2.34:1 against "
             "the gearbox's 2.35:1; plate screen angle moved +13.47 -> +22.18 while the "
             "gearbox's stays at +13.47. BOOKS AND GEARBOX: 0 edits. THE DECK WAS NOT TOUCHED "
             "and is now THREE passes out of step - it inlines the brain at L3012 YAW0 10 / PIT0 "
             "8 and L2976 AOV 12. Git not touched, _build_all.py not run.",
        closes_when="Dave has ruled Q1 - the plate follows the body to -50 (shipped) or the plate "
                    "holds the cogs' -35 and the brain turns 11.6 degrees in its own axes "
                    "(alt-body-23-tray-35.png, screen residual 0.01 degrees, costs an 11.6-degree "
                    "plan split and a second view matrix) - and has ruled Q2, whether AOV widens "
                    "past 33 so the plate reads as catching the body at the shorter on-screen "
                    "length; and the deck's own brain IIFE has either been moved to the ruled "
                    "constants or explicitly left at pass six"),
    "W-518": dict(
        project="apollo", owner="dave", opened=292, state="open",
        home=S + "W-wrap.md",
        links=[S + "W-wrap.md"],
        title="#292 W - the delegated capture ritual for #292 -> #293",
        body="Every runbook step 1..5b, measured. NO RULING INSCRIBED and knowledge/_rulings.json "
             "stays at 622 - he did not say 'inscribe', so every ruling-shaped thing carries as a "
             "QUESTION PUT (s271-D4). Eight Opus lanes plus two commit seats, none in seat: the "
             "overview dashboard defined and cold one-shot, the chart engine re-driven to the "
             "FIRST GREEN RELEASE IN FIVE SESSIONS, a Swiss design-system map (10 have / 2 coming "
             "soon) slotted into deck v13 after slide 10, and the brain ruled by his eye three "
             "more times in one day - rest angle REJECTED, the tray/back alternate ACCEPTED, then "
             "turned back inline with its tray. The seam check fired at the stop line, was "
             "overridden once by one more note and then obeyed - the SAME shape as #291, now n=2.",
        closes_when="Dave gives his v12/v13 notes (the four D2 layout flags and the dark robots "
                    "slide are gated on them), rules lane B3's plate question, and answers the "
                    "ruling-shaped questions put by lanes C, D and H - plus the dashboard review "
                    "and the next one-shot on the DEMO'S COLD BRIEF, and the workers' finessing, "
                    "together"),
}


def main():
    want = sys.argv[1:]
    if not want:
        raise SystemExit("name the row ids to mint")
    doc = _state.load()
    have = {i["id"] for i in doc["items"]}
    added = []
    for rid in want:
        if rid in have:
            print(f"SKIP {rid} — already present")
            continue
        home = ROWS[rid]["home"]
        if not os.path.exists(os.path.join(REPO, home)):
            raise SystemExit(f"REFUSED: {home} does not exist — a row may not name a missing home")
        _state.add(doc, id=rid, **ROWS[rid])
        added.append(rid)
    ok, fails, _ = _state.check(doc)
    if not ok:
        raise SystemExit("REFUSED: " + "; ".join(fails[:5]))
    _state.save(doc)
    doc2 = _state.load()
    ok2, fails2, _ = _state.check(doc2)
    print(f"ADDED {len(added)}: {', '.join(added) or '(none)'}")
    print(f"store now {len(doc2['items'])} items · check ok {ok2} · {len(fails2)} fails")


if __name__ == "__main__":
    main()
