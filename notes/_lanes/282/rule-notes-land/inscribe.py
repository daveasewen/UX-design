#!/usr/bin/env python3
"""#282 lane RN — inscribe s282-D1 at the END of knowledge/_rulings.json BY TEXTUAL SPAN.

Additive only: the closing ` }`, ` ]` and `}` lines are left untouched and the separating
comma is written on its own line, so the numstat is `N  0`. Idempotent: refuses if the id
is already present.
"""
import json, sys, pathlib

R = pathlib.Path(__file__).resolve().parents[4] / 'knowledge' / '_rulings.json'

RULED = (
 "A RULE NOTE BECOMES A RULE EDIT WHEN HE SAYS SO. s281-D6 filed thirteen of his notes as arguments with "
 "the RULE rather than with the link and refused to touch a single guideline file: they were HIS to rule, in #282. "
 "This is that ruling, landed on his own export of the fifteen-row rule-notes page "
 "(notes/_lanes/282/rule-notes/DAVE-EXPORT-2026-09-17.json, 2026-09-17T19:10:24.887Z): 14 of 15 on the "
 "recommendation, one overruled. ELEVEN OF HIS NOTES BECOME GUIDELINE EDITS, IN HIS OWN WORDS. Each is a CLAUSE "
 "ADDED to the rule's existing bullet - the stored sentence is never rewritten, no {#id} is added, moved or removed "
 "- and each ends `(s282-D1, Dave 2026-09-17)`, so every edit cites this ruling in its own line: "
 "`aca-003` (c) the title stays an obligation and a heuristic joins it - the first heading need not repeat the page "
 "title, an active navigation state or a salutation may lead, and the title, not the H1, is what orientation rests on; "
 "`aid-009` (a) SPLIT - the obligation keeps 44 default / 24 floor and now states they are measured on the HIT AREA, "
 "and a graded heuristic sits beside it: the visible target, the clear space around it (spacing is also emphasis) and "
 "compact views (a user choice) are context the designer weighs; `col26-009` (a) the second reason - brand "
 "consistency, 'if designers were allowed to use the supporting palette we would get dramatically varied designs'; "
 "`dv-bar-007` (a) scoped to positive-scale bar charts, negatives use the vertical below-zero form; "
 "`icon-006` (a) the two reasons - floor = legibility, ceiling = the icon/illustration boundary, and consistency; "
 "`logo26-001` (a) the native-app clause - the journey's logon or splash screen satisfies the rule, 'the user "
 "summoned an HSBC app, they know where the destination is'; `photo26-002` (a) a REVIEW DATE on the gen-AI clause, "
 "review by 2027-03, and NO edit to the ban; `pict-001` (a) the definition - a pictogram supports a concept, an icon "
 "signals an action; `pict-010` (a) the reason - consistency and enforcement against misuse by designers, not a "
 "perceptual threshold; `col26-016` (a) THE EXCEPTION, AND IT IS SYMMETRIC - RAG red text for downward AND RAG green "
 "text for upward position movement, stat-card style, on his own note 'the same is true for green for possitive BTW' "
 "- and it CROSS-REFERENCES the delta clause already scoped under `data-visualisation.md` {#dv-017} ({#dv-019} (a), "
 "ruled 2026-07-16 and split 2026-07-19) instead of restating it; `neuro-026` (a) the carve-out BY REFERENCE - "
 "unpaired icons only for the universal set named in `icons.md`, pictograms stay no-exception (pict-001). "
 "TWO OF HIS NOTES BECOME EDGES, not edits: `mot-005` gains a SECOND `restsOn` to `ux:pr-wcag-operable` (his 'it is "
 "also a Ally rule we adhere to so the grade is probably wrong' - the rule is SC 2.2.2 Pause, Stop, Hide restated at "
 "brand level, so the statutory obligation lands beside the control principle it already rests on, the s281-D6 "
 "many-to-many shape), and `type26-003` gains a SECOND `restsOn` to `ux:pr-tog-readability` on his 'linked to 2 as "
 "you stated'. Both carry `why`, `grade` at the time of writing and his note verbatim. `type26-002` STANDS AS LANDED "
 "- the declared null and the consistency principle both, exactly as s281-D6 put them. "
 "`col26-012` IS NOT EDITED. He overruled the recommendation to (c) 'Discuss first', so the flat ban stands as "
 "written, the colour-standards chart-red line is untouched, and it REMAINS AN OPEN ASK - the reservation he "
 "described (primary red for logo, CTAs, tabs and the brand bar; RAG red in charts only as status) is recorded here "
 "and inscribed nowhere. `aid-009`'s 'maybe we need to discuss' is answered by the split, not deferred. "
 "THE INDEX IS REGENERATED, THE EDGE BLOCK SURVIVES: `knowledge/guidelines/_rules-index.json` is rebuilt by "
 "`knowledge/guidelines/gen_rules_index.py`, which reads the markdown and touches no edge; `gen_kg_rules.py` - which "
 "WOULD delete the hand-authored `restsOn` block - is NOT run and is NOT fixed by this lane, so the footgun lane RL "
 "named at #281 stays open and named."
)

SAYS = (
 "His export of the fifteen-row rule-notes page, 2026-09-17T19:10:24.887Z, "
 "notes/_lanes/282/rule-notes/DAVE-EXPORT-2026-09-17.json - 15 answers, 14 on the recommendation, 1 overruled. "
 "THE FOURTEEN PICKS, each the option sentence printed for that row in "
 "notes/_lanes/282/rule-notes/gen_rule_notes.py: aca-003 = (c) 'Split it: the title stays an obligation; add a "
 "heuristic that the first heading need not repeat the title'; aid-009 = (a) 'Split it: the hit area stays boolean "
 "(44 default, 24 floor); the visible target, clear space and compact views become a graded heuristic beside it'; "
 "col26-009 = (a) 'Add the second reason to the rule text'; dv-bar-007 = (a) 'Scope it: applies to positive-scale "
 "bar charts; negatives use the vertical below-zero form'; icon-006 = (a) 'Add the two reasons to the rule text: "
 "floor = legibility, ceiling = the icon/illustration boundary'; logo26-001 = (a) 'Add the native-app clause: in a "
 "native app the journey's logon or splash screen satisfies the rule'; mot-005 = (a) 'Both land: the control "
 "principle and the WCAG obligation (SC 2.2.2) as two edges; rule text unchanged'; photo26-002 = (a) 'Put a review "
 "date on the gen-AI clause - March 2027 - no edit to the ban'; pict-001 = (a) 'Write the definition into the rule: "
 "a pictogram supports a concept; an icon signals an action'; pict-010 = (a) 'Add the reason line; the null stands'; "
 "type26-002 = (a) 'Both stand - the null and the consistency principle'; type26-003 = (a) 'Yes - land readability "
 "as a second edge'; col26-016 = (a) 'Inscribe the exception: RAG red text is allowed for downward movement, "
 "stat-card style'; neuro-026 = (a) 'Inscribe the carve-out by reference: unpaired icons allowed only for the "
 "universal set named in icons.md; pictograms stay no-exception'. "
 "HIS ONE NOTE ON THE EXPORT, VERBATIM - col26-016: \"the same is true for green for possitive BTW\". "
 "THE ONE OVERRULE, VERBATIM - col26-012 = (c) \"Discuss first\" (recommended was (a), the reservation rewrite); "
 "his note on that row at #281, verbatim: \"I'm actually not sure about this, the rule is partly a brand concern the "
 "primary red is only for the logo and for CTAs, tabs and the 'brand-bar' tilting. We allow the use of RAG in charts "
 "as long as it's used appropriately.\" "
 "His original notes, verbatim, and the rule text as stored: notes/_lanes/281/rests-on-land/RULE-NOTES-2026-09-17.md."
)

GOVERNS = [
 "knowledge/guidelines/accessibility-content-authoring.md",
 "knowledge/guidelines/accessibility-interaction-design.md",
 "knowledge/guidelines/brand-refresh-assets.md",
 "knowledge/guidelines/colour-standards-2026.md",
 "knowledge/guidelines/data-visualisation-bar-charts.md",
 "knowledge/guidelines/icons.md",
 "knowledge/guidelines/neurodiversity.md",
 "knowledge/guidelines/pictograms.md",
 "knowledge/_rule_nodes.json",
 "knowledge/guidelines/_rules-index.json",
 "notes/_lanes/282/rule-notes/DAVE-EXPORT-2026-09-17.json",
 "notes/_lanes/282/rule-notes-land/edit_guidelines.py",
 "notes/_lanes/282/rule-notes-land/land_rule_notes.py",
]

EVIDENCE = [
 "notes/_lanes/282/rule-notes/DAVE-EXPORT-2026-09-17.json - his own export, 19:10:24Z, 15 answers, 1 note, 1 overrule",
 "notes/_lanes/282/rule-notes/RULE-NOTES-2026-09-17.html - the page he answered; 15 rows",
 "notes/_lanes/282/rule-notes/gen_rule_notes.py - the option sentences he picked, the `opts` tuples",
 "notes/_lanes/281/rests-on-land/RULE-NOTES-2026-09-17.md - his notes verbatim and the rule text as stored",
 "notes/_lanes/282/rule-notes-land/edit_guidelines.py - the eleven edits; idempotent; refuses a non-unique anchor",
 "notes/_lanes/282/rule-notes-land/land_rule_notes.py - the two edges + the eleven refreshed node texts; idempotent",
 "notes/_lanes/282/rule-notes-land/index-diff.json - the json.load diff: 11 changed, 0 lost, 0 added, 470 both sides",
 "notes/_subreports/2026-09-17-282-RN-rule-notes-land.md - this lane's report",
]

OBJ = {"id": "s282-D1", "ruled": RULED, "date": "2026-09-17", "by": "Dave", "says": SAYS,
       "governs": GOVERNS, "evidence": EVIDENCE, "status": "ruled"}


def main():
    txt = R.read_text(encoding='utf-8')
    if '"s282-D1"' in txt:
        print('s282-D1 already inscribed - no-op')
        return 0
    tail = '\n }\n ]\n}'
    assert txt.endswith(tail), 'unexpected tail'
    body = json.dumps(OBJ, indent=1, ensure_ascii=False)
    body = '\n'.join(' ' + ln for ln in body.split('\n'))
    new = txt[:-len(tail)] + '\n }\n ,\n' + body + '\n ]\n}'
    d = json.loads(new)
    assert d['rulings'][-1]['id'] == 's282-D1' and len(d['rulings']) == 614, 'parse/shape'
    R.write_text(new, encoding='utf-8')
    print(f"inscribed s282-D1 - rulings {len(d['rulings'])-1} -> {len(d['rulings'])}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
