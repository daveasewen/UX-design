# #306 lane U - the six ruling entries s306-D4..D9 from Dave's wrap-redesign decision page export (16:01).
# Every quoted word of his is READ from the export (the six calls from its markdown, the free text from its
# machine copy), never retyped. Writes entry files only; the writes go through knowledge/_inscribe_ruling.py.
# Status `ruled`: the build is six phases, each proven on a real wrap (the page's build order), none enacted today.
import json, re, os
EX = 'notes/_lanes/306/DAVE-RULINGS-2026-09-28-wrap-redesign.md'
PAGE = 'notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html'
RREP = 'notes/_subreports/2026-09-28-306-R-wrap-redesign.md'
PLAN = 'notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md'
UREP = 'notes/_subreports/2026-09-28-306-U-rulings-and-bloat.md'
OUT = 'notes/_lanes/306/U/entries/'; os.makedirs(OUT, exist_ok=True)
txt = open(EX, encoding='utf-8').read()
A = json.loads(re.search(r'```json\n(.*?)\n```', txt, re.S).group(1))['answers']
CALLS = re.findall(r'^(\d)\. (.+?)\n   → \*\*(.+?)\*\* \(recommended: (.+?)\)$', txt, re.M)
assert len(CALLS) == 6 and [c[0] for c in CALLS] == list('123456'), CALLS
WORDS = A['notes']['page']
assert WORDS in txt and WORDS.startswith('lets go with all the recommendations')
page = open(PAGE, encoding='utf-8').read()
for _, q, _, _ in CALLS:
    assert q.replace("'", '&#39;').replace("'", "’") in page or q in page or q.replace("'", "’") in page, q
q = lambda s: '"' + s + '"'
SAYS0 = (f"chat #306, Mon 2026-09-28 16:01 BST, decision page export ({PAGE}, exported 2026-09-28 16:01, received "
         f"in chat as {EX})")
BUILD = ("The build is the page's six phases, in order, each proven on one real wrap with the page's figures measured "
         "again before and after: 1 the mechanics become permanent tools; 2 his summary at the push, no second CI "
         "wait; 3 one story, every view generated; 4 three seats; 5 carried items written as changes; 6 wrap as you go.")
PH = {
 '1': ("THE WRAP WRITES THE SESSION'S STORY ONCE, AS STORY PLUS MEASURED FIGURES, AND EVERY OTHER VIEW IS GENERATED "
       "FROM IT, THE HANDOFF INCLUDED.", 3,
       "Two source files, one writer each: notes/_lanes/<n>/W/STORY.md (the story seat) and FACTS.json (the mechanics "
       "seat, measured values only); one generator makes the handoff, dossier, wrap report, banner, delta, summary, "
       "memory note, commit message and state-row titles; the gate gains a blocking views-are-fresh arm. Enacted by "
       "PHASE 3 (one story, every view generated), built on PHASE 1 (the mechanics become permanent tools). "),
 '2': ("A GENERATED WRAP REPORT COUNTS AS THE FILED REPORT EVERY SEAT OWES (`s218-D7`).", 3,
       "The generated report still carries the three machine-read lines, gets a state row and is cited by path; the "
       "generator is its one writer and the freshness arm stops hand edits. `s218-D7` is not edited. Enacted by "
       "PHASE 3 (one story, every view generated). "),
 '3': ("THE WRAP RUNS AS THREE SEATS AT ONCE — STORY, MECHANICS, COMMIT — JOINED ONLY AT THE COMMIT.", 4,
       "The story seat writes STORY.md, the mechanics seat measures FACTS.json and runs the moves, carries and rows, "
       "the commit seat waits for both done markers, generates the views, rebuilds the index once, commits and "
       "pushes. Enacted by PHASE 4 (three seats: the seat brief templates and the runbook's step order), which "
       "needs phases 1 and 3. "),
 '4': ("HIS SUMMARY GOES TO HIM AS SOON AS THE WRAP IS PUSHED, AND THE WRAP STOPS WAITING ON CI FOR THE SMALL "
       "FOLLOW-UP COMMIT: THE NEXT OPENER READS THE FOLLOW-UP'S CI.", 2,
       "A runbook change and one opener line, no new code. Enacted by PHASE 2 (his summary at the push; no second "
       "CI wait). "),
 '5': ("THE WRAP STOPS COPYING THE WHOLE CARRIED-ITEMS LIST FORWARD: IT WRITES ONLY WHAT CHANGED (NEW, STRUCK, "
       "AGING), AND THE FULL LIST IS GENERATED WHEN IT IS READ.", 5,
       "The gate's carried count reads the generated list; the count must reproduce (401 at the page). Enacted by "
       "PHASE 5 (carried items written as changes). "),
 '6': ("IN A LATER PHASE, THE SEAM CHECK ADDS HIS WORDS AND THE RUNNING TALLY TO THE STORY DRAFT DURING THE "
       "SESSION, SO THE WRAP EDITS A DRAFT INSTEAD OF READING THE WHOLE TRANSCRIPT.", 6,
       "Enacted by PHASE 6 (wrap as you go), which needs phase 3's story file. His question on the same page, "
       "whether this bloats anything else, is answered on measurement in " + UREP + "; its proposed guards are "
       "not ruled. "),
}
GOV = {'1': ["knowledge/_RUNBOOK-capture-ritual.md"], '2': ["knowledge/_RUNBOOK-capture-ritual.md"],
       '3': ["knowledge/_RUNBOOK-capture-ritual.md"], '4': ["knowledge/_RUNBOOK-capture-ritual.md"],
       '5': ["knowledge/_RUNBOOK-capture-ritual.md", "_CARRIES.md"],
       '6': ["knowledge/_RUNBOOK-capture-ritual.md", "knowledge/_seam.py"]}
for n, qu, ans, rec in CALLS:
    head, phase, body = PH[n]
    rid = f's306-D{int(n) + 3}'
    ruled = (f"{head} Dave's answer, verbatim: {q(ans)} (the page's recommendation: {rec}), to the decision page's "
             f"call {n} of 6, verbatim: '{qu}'. {body}{BUILD} Status stays `ruled` until phase {phase} is proven on "
             f"a real wrap; store row W-305wr (the wrap redesign) closes only then.")
    says = f"{SAYS0} · call {n}, verbatim: '{qu}' — his answer, verbatim: {q(ans)}"
    ev = [f"chat #306 2026-09-28 (live) - the 16:01 BST decision page export, quoted verbatim in `says`",
          EX + "#The six calls", PAGE, RREP]
    if n == '1':
        says += (f" · his words on the page, verbatim: {q(WORDS)} · store row W-305wr (the wrap redesign, "
                 f"scheduled by his \"yes both\" at 12:21 BST)")
        ev = [ev[0].replace('quoted verbatim in `says`', 'his six answers and his free-text words, quoted verbatim in `says`'),
              EX + "#His words, verbatim", EX + "#The six calls", PAGE, RREP, PLAN]
    if n in ('2', '6'):
        ev.append(PLAN)
    e = {"id": rid, "date": "2026-09-28", "by": "Dave", "status": "ruled", "ruled": ruled, "says": says,
         "governs": GOV[n], "evidence": ev}
    json.dump(e, open(OUT + rid + '.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(rid, len(json.dumps(e, ensure_ascii=False)), '|', ans, '| phase', phase)
