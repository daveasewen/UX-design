#!/usr/bin/env python3
"""#281 lane TV — inscribe s281-D4 and s281-D5 into knowledge/_rulings.json by TEXTUAL SPAN.

Lane RO inserted s281-D3 into the same file in this session, so this is a pure APPEND on the
shape lane RO left: the file is re-read at run time, each span is inserted immediately before the
array's closing bracket with the separating comma on its own line, and nothing already in the file
is rewritten. `git diff --numstat` must read `N  0`.

Idempotent: refuses if either id is already present, and refuses if the tail is not the shape it
expects (which is what a parallel lane's own insert would change).

Run:  python3 notes/_lanes/281/theory-view/inscribe_s281_D4_D5.py
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
F = REPO / "knowledge" / "_rulings.json"

D4 = {
 "id": "s281-D4",
 "ruled": (
  "A DESIGN'S CITATION OF A PRINCIPLE IS EXPLANATION, AND IT IS DRAWN IN THE THIRD VIEW. The 14 "
  "authored `obeys` lines that run from a component meta to a `ux:` principle - HELD since #281 "
  "lane CM, carried in the data and drawn by no chip at any setting - are DRAWN, in the THEORY "
  "view (the third view, s277-D8; renamed by s281-D5), under their own chip labelled `cited by a "
  "design`, beside the UX principles and their polarities. They are EXPLANATION, NOT OBLIGATION: a "
  "component naming a principle is the designer citing a reason, and a reason is read in the view "
  "where the principle lives. DESIGN GOVERNANCE THEREFORE STAYS AT THREE PROVENANCES - WCAG `sc:`, "
  "HSBC `rule:`, and the rulings a design cites - and s277-D8 is NOT reopened: no fourth provenance "
  "sub-chip is added to the obligation box, now or by this ruling. THE DESIGNER'S OWN `$why` "
  "SENTENCE RIDES THE EDGE and is read in INSPECT: it is authored in the meta beside the ref, the "
  "builder carries it in the edge's own field, and the page prints it in the edge's door under the "
  "designer's own words. STORAGE IS UNTOUCHED: no node id, no edge type and no fam KEY moves, the "
  "`obeys` type keeps the `guidelinerules` family it was given at 1.21 and INSPECT still names it, "
  "and no edge is invented - the builder's `held` flag becomes a `cited` flag on the same 14 lines, "
  "chosen by the same predicate. The chip loads OFF, like every other chip in that view, so the "
  "default canvas does not gain a line. FORCE BY GRADE IS NOT RULED HERE: these 14 are the "
  "hand-authored SEED of applicability, and whether a highly graded principle carries force on a "
  "design that has not cited it is a LATER ruling, to be taken once the rule->principle lines "
  "s281-D3 authorises exist. Nothing in this ruling derives a scope, infers an obligation from a "
  "grade, or promotes a principle to a rule."
 ),
 "date": "2026-09-17",
 "by": "Dave",
 "says": (
  "Decisions export 2026-09-17T11:58:34.925Z, "
  "notes/_lanes/281/orphan-plan/DAVE-EXPORT-DECISIONS-2026-09-17.json, q3 = (a), recommended (a), "
  "overruled false. The question, verbatim: \"Where is an obligation on a UX principle drawn?\" The "
  "option he chose, verbatim: \"The Explanation view - a 'cited by a design' chip beside the "
  "polarities\". His note on the export, verbatim: \"This seems more complicated to me, maybe I "
  "just need a longer explanation, I feels right if it is the rational behind a rule, but it is "
  "also really good contextif the principles are graded then ones that are graded high could "
  "arguably be rules. these nodes have to be used somehow, let's think like a designer, I would "
  "endevour to adhere to all the ones I think are applicable and work out the comprimises of ones "
  "that clash or result in undesirable outcomes. lets have a chat about this.\" The chat that note "
  "asked for put two things to him: the 14 lines are the hand-authored SEED of applicability, and "
  "whether force follows grade is a LATER ruling, once rule->principle lines exist. After it, "
  "verbatim: \"Okay these all look good to me, thanks for the explanation\" "
  "(notes/_lanes/281/DAVE-RULINGS-2026-09-17.md) - so q3 (a) stands as ruled, on those terms."
 ),
 "governs": [
  "knowledge/_build_kg_explorer.py",
  "knowledge/_kg_explorer.template.html",
  "notes/_KG-EXPLORER.html"
 ],
 "evidence": [
  "notes/_lanes/281/orphan-plan/DAVE-EXPORT-DECISIONS-2026-09-17.json - Dave's own export, 11:58:34Z, q3",
  "notes/_lanes/281/orphan-plan/DECISIONS-2026-09-17.html - the page he ruled on; question 3 and its three options",
  "notes/_lanes/281/DAVE-RULINGS-2026-09-17.md - the read-back after the chat: q3 (a) stands as ruled, seed-not-force",
  "notes/_subreports/2026-09-17-281-CM-chip-map.md - lane CM's report: the 14 lines held, and the ruling-shaped question this answers",
  "notes/_lanes/280/orphan-census/REPORT.md - lane OC's census, set 08 `obeys-ux`: 4 principles a design cites, 0 of the lines drawn",
  "notes/_lanes/281/theory-view/facts-before.json - the census re-run against HEAD's explorer 1.23: set 08 is 4 at every chip setting",
  "notes/_lanes/281/theory-view/facts-after.json - explorer 1.24: set 08 is 0 at every-chip-on, 14 lines drawn, 0 held",
  "notes/_lanes/281/theory-view/shots/shots-after.json - the driven INSPECT pass: the $why sentence read out of the edge's own door",
  "notes/_subreports/2026-09-17-281-TV-theory-view.md - lane TV's report"
 ],
 "status": "ruled",
}

D5 = {
 "id": "s281-D5",
 "ruled": (
  "THE TRIAD IS SYSTEM . GOVERNANCE . THEORY - three one-word nouns, each with a verb line under "
  "it. SYSTEM: what exists - the agent chooses here. GOVERNANCE: what a design must or should do - "
  "the agent obeys here. THEORY: why - the agent consults here. `Explanation` and `Design "
  "governance` are retired as labels wherever the page says them: the chip bar's view boxes, the "
  "legend's prose, the strata band tints' left-edge labels, the 3D plates, the 2D rings, the 3D "
  "shells and the phone sheet. THE CONSTITUTION KEEPS ITS NAME and is still NOT one of the three "
  "views - it is the ruling record, named on the page as its own thing (s277-D8, unchanged). THIS "
  "IS LABELS ONLY, which is s277-D8's own clause: no fam KEY, no node id and no edge type moves; "
  "the view ids `system`, `design`, `explain` and `constitution` are untouched in the builder and "
  "in the page, as are `RULE_FAM`, `UX_FAM`, `guidelines` and `governance`; nothing in storage is "
  "renamed, rewritten or re-filed, and no baked coordinate moves. One `BAND_NAME` map in the "
  "builder feeds all four furniture sets, so the rename is made in one place and cannot drift "
  "between the four layouts."
 ),
 "date": "2026-09-17",
 "by": "Dave",
 "says": (
  "Decisions export 2026-09-17T11:58:34.925Z, "
  "notes/_lanes/281/orphan-plan/DAVE-EXPORT-DECISIONS-2026-09-17.json, q5 = (a), recommended (a), "
  "overruled false. The question, verbatim: \"Is 'Explanation' the right name for the third view?\" "
  "The option he chose, verbatim: \"Rename it 'UX Theory'...\". His note on the export, verbatim: "
  "\"What is the triad of verbs, i like neatness so maybe we can think of something else\". The "
  "chat that note asked for put three triads to him; he took OPTION 1, verbatim from the chat: "
  "\"System . Governance . Theory - three one-word nouns, verb line under each (choose . obey . "
  "consult)\". After it, verbatim: \"Okay these all look good to me, thanks for the explanation\" "
  "(notes/_lanes/281/DAVE-RULINGS-2026-09-17.md). Earlier the same day, on the orphan plan export "
  "of 11:02Z, his note on polarity-reach, verbatim: \"Explanation ist a great label maybe "
  "something like 'UX Theory' \" - read as \"isn't\", and NOT inscribed then, which is why it was "
  "put as a question here."
 ),
 "governs": [
  "knowledge/_build_kg_explorer.py",
  "knowledge/_kg_explorer.template.html",
  "notes/_KG-EXPLORER.html"
 ],
 "evidence": [
  "notes/_lanes/281/orphan-plan/DAVE-EXPORT-DECISIONS-2026-09-17.json - Dave's own export, 11:58:34Z, q5",
  "notes/_lanes/281/orphan-plan/DECISIONS-2026-09-17.html - the page he ruled on; question 5 and its options",
  "notes/_lanes/281/orphan-plan/DAVE-EXPORT-2026-09-17.json - the 11:02Z export whose polarity-reach note first raised the name",
  "notes/_lanes/281/DAVE-RULINGS-2026-09-17.md - the read-back after the chat: the triad he took, in the chat's own words",
  "notes/_lanes/281/theory-view/shots/shots-after.json - the four view-box headings and the four band names, scraped off the rendered page",
  "notes/_subreports/2026-09-17-281-TV-theory-view.md - lane TV's report, with every 'Explanation' / 'Design governance' occurrence listed"
 ],
 "status": "ruled",
}


def main():
    src = F.read_text()
    todo = [r for r in (D4, D5) if '"%s"' % r["id"] not in src]
    if not todo:
        print("REFUSED: s281-D4 and s281-D5 are both already present", file=sys.stderr)
        return 1
    tail = "\n ]\n}"
    if not src.endswith(tail):
        print("REFUSED: tail is not %r - file shape changed, re-read and adjust" % tail,
              file=sys.stderr)
        return 1
    span = ""
    for r in todo:
        body = json.dumps(r, indent=1, ensure_ascii=True)
        # one-space base indent, matching the entries already in the array
        span += "\n ,\n" + "\n".join(" " + ln for ln in body.split("\n"))
    new = src[: -len(tail)] + span + tail
    parsed = json.loads(new)  # must still parse
    ids = [x["id"] for x in parsed["rulings"]]
    assert len(ids) == len(set(ids)), "duplicate ruling id after the insert"
    F.write_text(new)
    print("inserted %s: %d lines, 0 removed · %d rulings in the file"
          % (", ".join(r["id"] for r in todo), span.count("\n"), len(ids)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
