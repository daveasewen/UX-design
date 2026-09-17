#!/usr/bin/env python3
"""#281 lane RO — inscribe s281-D3 into knowledge/_rulings.json by TEXTUAL SPAN.

Lanes FO and TV may be committing to the same file in parallel, so this is a
pure APPEND: the file is re-read at run time, the span is inserted immediately
before the array's closing bracket with the separating comma on its own line, and
nothing already in the file is rewritten. `git diff --numstat` must read `N 0`.

Idempotent: refuses if s281-D3 is already present.
Run:  python3 notes/_lanes/281/rests-on/inscribe_s281_D3.py
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
F = REPO / "knowledge" / "_rulings.json"

RULING = {
 "id": "s281-D3",
 "ruled": (
  "A RULE'S REASON IS AUTHORED, NEVER PARSED. `restsOn` (rule -> ux, carrying a `$why` "
  "sentence and the principle's grade) ENTERS THE CLOSED VOCABULARY as an AUTHORED edge "
  "type: a person writes each line and no generator ever infers one from prose. FIRST WAVE "
  "= THE 59 BLOCKING RULES, one line each, in the shape agreed in the chat - one rule, one "
  "proposed principle, ONE SENTENCE of why, the grade. ANY GRADE IS ALLOWED, not only the "
  "six A-grade laws the audit's proposal named (A2 Q3, G6): an honest C or L beats a forced "
  "A, and the grade is what the reader is being told, not a bar the link has to clear. A "
  "RULE THAT RESTS ON CONVENTION ALONE SAYS SO - `restsOn -> ref:null` with a note giving "
  "the reason no principle fits - which is the declared-null shape of s275-D2 (RP-2 option "
  "a): a legal answer, never a dropped row. THE LINES LAND ONLY ON DAVE'S EXPORT of the "
  "proposal page notes/_lanes/281/rests-on/RESTS-ON-2026-09-17.html. Until that export comes "
  "back, `restsOn` is NOT a verb in knowledge/_kg_verbs.json, NOT in the builder, NOT in the "
  "explorer and NOT an edge anywhere - #281 lane RO proposed and inscribed and landed "
  "nothing. The twelve-verb reading map (s277-D11) files it under `rests-on`, whose "
  "$definition today says 'the future restsOn ... is NOT a type today and is not listed'; "
  "the landing lane is what moves it out of that sentence and gives it a force."
 ),
 "date": "2026-09-17",
 "by": "Dave",
 "says": (
  "Decisions export 2026-09-17T11:58:34.925Z, "
  "notes/_lanes/281/orphan-plan/DAVE-EXPORT-DECISIONS-2026-09-17.json, q4 = (a), "
  "recommended (a), overruled false. The question, verbatim: \"Do we author a line from each "
  "rule to the principle it rests on?\" The option he chose, verbatim: \"Yes - start with the "
  "fifty-nine blocking rules; bring a page for my export\". His note on the export, verbatim: "
  "\"I think this feels right, but maybe we need to talk it through\". After the chat that "
  "note asked for, verbatim: \"Okay these all look good to me, thanks for the explanation\" "
  "(notes/_lanes/281/DAVE-RULINGS-2026-09-17.md) - and the chat's terms he agreed to are the "
  "card shape above, declared nulls included."
 ),
 "governs": [
  "knowledge/_kg_verbs.json",
  "knowledge/gen_kg_rules.py",
  "knowledge/_rule_nodes.json",
  "knowledge/_ux_principle_nodes.json",
  "knowledge/_validate_kg.py",
  "knowledge/_build_kg_explorer.py",
  "knowledge/_kg_explorer.template.html",
  "notes/_KG-EXPLORER.html",
  "knowledge/_compose_slice.py",
  "notes/_lanes/281/rests-on/proposals.json"
 ],
 "evidence": [
  "notes/_lanes/281/orphan-plan/DAVE-EXPORT-DECISIONS-2026-09-17.json - Dave's own export, 11:58:34Z, q4",
  "notes/_lanes/281/orphan-plan/DECISIONS-2026-09-17.html - the page he ruled on; question 4 and its three options",
  "notes/_lanes/281/DAVE-RULINGS-2026-09-17.md - the read-back after the chat: q4 (a) stands as ruled",
  "notes/_lanes/277/kg-audit/A2-AUDIT.md - Q3 / G6: rule->ux is 0 of 470, no edge type in either direction; restsOn is the proposal",
  "notes/_lanes/281/rests-on/RESTS-ON-2026-09-17.html - the 59-card proposal page this ruling authorises and nothing else",
  "notes/_lanes/281/rests-on/proposals.json - the 59 proposals, 52 with a principle, 7 declared convention",
  "notes/_subreports/2026-09-17-281-RO-rests-on.md - lane RO's report"
 ],
 "status": "ruled",
}


def main():
    src = F.read_text()
    if '"s281-D3"' in src:
        print("REFUSED: s281-D3 already present", file=sys.stderr)
        return 1
    tail = "\n ]\n}"
    if not src.endswith(tail):
        print("REFUSED: tail is not %r - file shape changed, re-read and adjust" % tail,
              file=sys.stderr)
        return 1
    body = json.dumps(RULING, indent=1, ensure_ascii=True)
    # one-space base indent, matching the entries already in the array
    block = "\n".join(" " + ln for ln in body.split("\n"))
    span = "\n ,\n" + block
    new = src[: -len(tail)] + span + tail
    json.loads(new)  # must still parse
    F.write_text(new)
    print("inserted s281-D3: %d lines, 0 removed" % (span.count("\n")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
