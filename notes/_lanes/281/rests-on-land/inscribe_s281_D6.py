#!/usr/bin/env python3
"""#281 lane RL — inscribe s281-D6 into knowledge/_rulings.json by TEXTUAL SPAN.

Pure APPEND, lane RO's shape kept: the file is re-read at run time, the span is inserted
immediately before the array's closing bracket with the separating comma on its own line, and
nothing already in the file is rewritten. `git diff --numstat` must read `N  0`.

Idempotent: refuses if s281-D6 is already present.
Run:  python3 notes/_lanes/281/rests-on-land/inscribe_s281_D6.py
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
F = REPO / "knowledge" / "_rulings.json"

RULING = {
 "id": "s281-D6",
 "ruled": (
  "A RULE MAY REST ON MORE THAN ONE PRINCIPLE: `restsOn` IS MANY-TO-MANY. s281-D3 authorised "
  "the type and the first wave; this ruling lands it on Dave's own export of the 59-card page "
  "and fixes the shape the card could not hold. THE RADIO TOOK ONE ANSWER AND HIS SENTENCE "
  "SAID TWO - on thirteen of the fifty-nine rows his note reads 'both 1 and 2' / '1 and 2' / "
  "'and 2' - so ON THOSE ROWS BOTH OPTIONS LAND, each as its own edge carrying ITS OWN `$why`, "
  "which is the sentence the proposal page printed for THAT option and never a merged one. The "
  "radio is the instrument, not the answer: where the instrument could not take what he said, "
  "THE SENTENCE WINS. A RULE THAT RESTS ON CONVENTION ALONE IS `restsOn -> ref:null` WITH HIS "
  "NOTE VERBATIM (the declared-null shape of s275-D2, unchanged), and A NULL AND A PRINCIPLE "
  "MAY STAND TOGETHER on one rule: `type26-002` is convention AND he wrote 'I think 1 is also "
  "applicable', so the null lands with his note and option 1 lands beside it. EVERY EDGE "
  "CARRIES `$why` AND, WHERE HE WROTE ONE, `daveNote` - his words verbatim, never summarised, "
  "never edited. The grade rides the edge as s281-D3 said, and it is THE GRADE AT THE TIME OF "
  "WRITING: the `ux:` node's own `grade` field stays authoritative on a re-grade, and a stale "
  "grade on an edge is a reading of the record, not a claim about the principle today. HIS "
  "NOTES ABOUT THE RULE ITSELF ARE NOT RULE EDITS. Thirteen of his notes argue with the RULE - "
  "its scope, its grade, its caveat - not with the link. NO GUIDELINE FILE IS CHANGED BY THIS "
  "LANE. They are filed, unedited and one per row with the rule's own text beside them, in "
  "notes/_lanes/281/rests-on-land/RULE-NOTES-2026-09-17.md, and they are HIS TO RULE, in #282. "
  "THREE ROWS ARE ASKS, not decisions: `col26-012` ('I'm actually not sure'), `aid-009` ('maybe "
  "we need to discuss') and `type26-002` (the null he named an option beside) land exactly what "
  "he chose, carry the note, and are named as open questions in the report. THE PICTURE: "
  "`restsOn` gets its reading in knowledge/_kg_verbs.json under `rests-on` at force `should`, "
  "and a chip labelled 'rests on' in the THEORY box, OFF by default, draws rule -> principle. "
  "It is the s281-D4 shape one type along: the chip gates the line INSTEAD OF the edge's "
  "storage family, the storage family is untouched and still named in INSPECT, and INSPECT "
  "reads the `$why` and the `daveNote` in the edge's own door. NO node id and NO existing edge "
  "type moves; the default canvas changes only by this inscription's own Constitution dots."
 ),
 "date": "2026-09-17",
 "by": "Dave",
 "says": (
  "His export of the 59-card page, 2026-09-17T14:49:41.532Z, "
  "notes/_lanes/281/rests-on/DAVE-EXPORT-2026-09-17.json - 59 answers, 8 convention, 8 "
  "overruled. The thirteen rows whose note says the rule rests on BOTH options, his words "
  "verbatim: appf-002 \"This is actually both 1 and 2 in this list\"; col26-008 \"...so its a "
  "bit of of 1 in the list and 2\"; col26-015 \"This is both 1 and 2\"; col26-016 \"This is "
  "both 1 and 2, there is one caveat, red text is allowed, but only the RAG red when used for "
  "position movement downward, as in a stat card\"; dv-016 \"1 and 2\"; dv-line-011 \"It's both "
  "1 and 2\"; dv-pie-009 \"This is both 1 and 2\"; dv-pie-010 \"both 1 and 2\"; neuro-026 "
  "\"This 1 and 2. we also allow unpaired icons for the most commonly understood icons\"; "
  "tov-038 \"1 and 2\"; type25-003 \"and 2\"; type25-008 \"1 and 2\"; webf-027 \"1 and 2\". And "
  "on type26-002, where he chose convention: \"I think 1 is also applicable, think of different "
  "H1s on every page\". The ruling s281-D3 this one lands is his q4 = (a) of the decisions "
  "export 11:58:34Z, read back after the chat as \"Okay these all look good to me, thanks for "
  "the explanation\" (notes/_lanes/281/DAVE-RULINGS-2026-09-17.md)."
 ),
 "governs": [
  "knowledge/_rule_nodes.json",
  "knowledge/_kg_verbs.json",
  "knowledge/_build_kg_explorer.py",
  "knowledge/_kg_explorer.template.html",
  "notes/_KG-EXPLORER.html",
  "notes/_lanes/281/rests-on-land/RULE-NOTES-2026-09-17.md",
  "notes/_lanes/281/rests-on-land/land_rests_on.py",
  "notes/_lanes/281/rests-on/DAVE-EXPORT-2026-09-17.json"
 ],
 "evidence": [
  "notes/_lanes/281/rests-on/DAVE-EXPORT-2026-09-17.json - his own export, 14:49:41Z, 59 answers",
  "notes/_lanes/281/rests-on/RESTS-ON-2026-09-17.html - the page he answered; 59 cards, 222 radios",
  "notes/_lanes/281/rests-on/proposals.json - the options a/b and their $why sentences, and the null sentence",
  "notes/_lanes/281/rests-on-land/RULE-NOTES-2026-09-17.md - the 13 notes about the RULE, filed for #282",
  "notes/_lanes/281/rests-on-land/land_rests_on.py - the lander; idempotent, asserts the 'both' set",
  "notes/_subreports/2026-09-17-281-RO-rests-on.md - lane RO's report, which proposed the verb",
  "notes/_subreports/2026-09-17-281-RL-rests-on-land.md - this lane's report"
 ],
 "status": "ruled",
}


def main():
    src = F.read_text()
    if '"s281-D6"' in src:
        print("REFUSED: s281-D6 already present", file=sys.stderr)
        return 1
    tail = "\n ]\n}"
    if not src.endswith(tail):
        print("REFUSED: tail is not %r - file shape changed, re-read and adjust" % tail,
              file=sys.stderr)
        return 1
    body = json.dumps(RULING, indent=1, ensure_ascii=True)
    block = "\n".join(" " + ln for ln in body.split("\n"))
    span = "\n ,\n" + block
    new = src[: -len(tail)] + span + tail
    json.loads(new)  # must still parse
    F.write_text(new)
    print("inserted s281-D6: %d lines, 0 removed" % (span.count("\n")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
