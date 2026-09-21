#!/usr/bin/env python3
"""293-J3 — one question set, three artefacts, three live requests.

Falsifies lane J2's rubric. Written to the skill's rules: one narrow judgment per
question; two INDEPENDENT Noul premises; Score levels that describe concrete
situations, stand on their own, and include a no-match outcome at level 0; all
three asked together over the same state (one request per artefact).
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../knowledge"))
import _jev

QUESTIONS = {
    # Noul A — J2's premise, restated so a high value means yes.
    "marks_every_gap": _jev.noul(
        "Every capability this page lists that it does not yet have is explicitly marked "
        "as not yet available, at the capability itself.",
        true="Each listed capability that the page does not have carries its own marker "
             "of unavailability — a 'Coming soon' badge, a faded treatment, or wording on "
             "that entry saying it is not yet held.",
        false="At least one listed capability that the page does not have carries no "
              "marker of its own and is presented the same way as the ones it has.",
    ),
    # Noul B — INDEPENDENT premise. Not the negation of A: a page can fail A without
    # claiming anything it does not have, and can pass A while still over-claiming.
    "claims_unbuilt_as_available": _jev.noul(
        "At least one capability is presented on this page as available or held, while "
        "the page's own text elsewhere says that same capability is not built or not held.",
        true="A listed capability reads as available or in place, and another part of the "
             "page states that this capability is absent, not held or not built.",
        false="Nothing on the page is presented as available while the page's own text "
              "says it is absent.",
    ),
    "absence_honesty": _jev.score(
        "How honestly does this page report the capabilities it does not have?",
        [
            # level 0 — the NO-MATCH outcome
            "The page does not present a list, grid or inventory of capabilities, "
            "features or components at all, so there is nothing whose absence could be "
            "reported. A dashboard of figures, a single article or a component demo.",
            "The page lists capabilities and some of the listed items are not actually "
            "held, but no listed item carries any marker of unavailability: every entry "
            "is presented the same way whether it is held or not.",
            "The page lists capabilities and marks at least one unheld item at the item "
            "itself — badged, faded or labelled 'not yet' — while at least one other "
            "unheld item carries no such marker and reads as available.",
            "The page lists capabilities and every item it does not hold carries an "
            "explicit marker of unavailability at the item itself, so a reader can tell "
            "held from unheld from the list alone.",
        ],
    ),
}

ARTEFACTS = [
    ("P", "notes/_lanes/292/H/design-system-map.html"),
    ("N", "notes/_lanes/293/J3/fixture-unbadged.html"),
    ("M", "notes/_lanes/293/J3/fixture-one-unbadged.html"),
]

if __name__ == "__main__":
    if "--dump" in sys.argv:
        print(json.dumps(QUESTIONS, indent=2, ensure_ascii=False))
        sys.exit(0)
    _jev.validate_questions(QUESTIONS)
    out = []
    for label, path in ARTEFACTS:
        st = _jev.html_to_state(os.path.join(_jev.REPO, path), cap=6000)
        state = {"artefact_path": st["source"], "page_text": st["text"]}
        r = _jev.ask(state, QUESTIONS, note="293-J3 rubric falsification probe, artefact %s" % label)
        print("===== %s  %s  (text_chars=%d truncated=%s)"
              % (label, path, st["text_chars"], st["truncated"]))
        print(json.dumps(r, indent=2, sort_keys=True, ensure_ascii=False))
        out.append((label, r))
