# #306 lane V - the ruling entry s306-D10: Dave adopted lane U's eleven proposed limits into the wrap redesign.
# The eleven limits are READ from lane U's report section 3 (never retyped); the phase for each is U's own
# parenthesis, read from the same line. His question and answer are the conductor's verbatim relay (chat #306,
# 16:58 BST), held once here as constants and written to DAVE-WORDS-2026-09-28-1658.md beside this script.
import json, re, os
UREP = 'notes/_subreports/2026-09-28-306-U-rulings-and-bloat.md'
PAGE = 'notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html'
OUT = 'notes/_lanes/306/V/entries/'; os.makedirs(OUT, exist_ok=True)
Q = ("1. Adopt the proposed limits into the design? I recommend yes. They go into phases 3 and 6, where they're "
     "needed.\n2. Build phases 1 and 2 now: turn the wrap's throwaway scripts into permanent tools, and send your "
     "summary as soon as the wrap is pushed. Tonight's wrap would then be their first real proof. I recommend yes.")
A = "go on both"
words = ("# Dave's words, #306, Mon 2026-09-28 16:58 BST — verbatim, as relayed by the conductor to lane V\n\n"
         "provenance: 306 · 2026-09-28\nstatus: observed\n\n## The question (the conductor, verbatim)\n\n"
         + Q + "\n\n## His answer, 16:58 BST, verbatim\n\n" + A + "\n\n"
         "Item 1 is inscribed as `s306-D10` (ruled). Item 2 is scheduling, not a ruling: it is recorded by addition on "
         "store row `W-305wr`.\n")
open('notes/_lanes/306/V/DAVE-WORDS-2026-09-28-1658.md', 'w', encoding='utf-8').write(words)
txt = open(UREP, encoding='utf-8').read()
sec = re.search(r'^## 3\. Proposed guards[^\n]*\n(.*?)^## 4\.', txt, re.S | re.M).group(1)
items = re.findall(r'^(\d+)\. (.+)$', sec, re.M)
assert [int(n) for n, _ in items] == list(range(1, 12)), items
PH = []
for n, line in items:
    ph = re.findall(r'\(phase (\d)[;)]', line)
    assert len(ph) == 1, (n, ph, line)
    PH.append((int(n), line.strip(), int(ph[0])))
by_phase = {}
for n, _, p in PH:
    by_phase.setdefault(p, []).append(n)
assert by_phase == {6: [1, 3, 4, 5], 3: [2, 6, 7, 11], 2: [8], 4: [9], 5: [10]}, by_phase
plain = lambda s: s.replace('**', '')
lst = ' '.join(f'({n}) {plain(line)} ENACTED BY PHASE {p}.' for n, line, p in PH)
ruled = ("THE ELEVEN LIMITS LANE U PROPOSED FOR THE WRAP REDESIGN ARE ADOPTED INTO THE DESIGN, ALL ELEVEN, EXACTLY AS "
         f"{UREP} § 3 'Proposed guards' LISTS THEM; EACH IS BUILT, AS A GATE ARM OR A RULE, BY THE PHASE THAT NEEDS IT. "
         "Dave's answer, verbatim: \"go on both\", to the conductor's question 1 of 2, verbatim: 'Adopt the proposed "
         "limits into the design? I recommend yes. They go into phases 3 and 6, where they're needed.' The phases, by "
         "the report's own parentheses: phase 3 takes limits 2, 6, 7 and 11; phase 6 takes 1, 3, 4 and 5; phase 2 "
         "takes 8 (the opener reads the CI run summary only); phase 4 takes 9; phase 5 takes 10 (the full carried "
         "list generated on read, never committed per wrap, and `_CARRIES.md` grows at most 20,000 B a wrap, a number "
         "picked, not measured). So the question's 'phases 3 and 6' holds for eight of the eleven; the other three "
         "ride phases 2, 4 and 5. The limits, as the report writes them: " + lst +
         " Each limit is enacted with its phase and proven on the same real wrap; this ruling amends the design "
         "(`s306-D4`..`s306-D9`), it edits none of them. Status stays `ruled` until the last of phases 2 to 6 that "
         "carries a limit is proven; store row W-305wr (the wrap redesign) closes only then. Question 2 of the same "
         "message ('Build phases 1 and 2 now') is scheduling, not a ruling, and is recorded by addition on W-305wr.")
says = ("chat #306, Mon 2026-09-28 16:58 BST, Dave's answer to the conductor's two-part question, both quoted verbatim "
        "(notes/_lanes/306/V/DAVE-WORDS-2026-09-28-1658.md). The question, verbatim: '" + Q.replace('\n', ' ') +
        "' — his answer, verbatim: \"" + A + "\"")
e = {"id": "s306-D10", "date": "2026-09-28", "by": "Dave", "status": "ruled", "ruled": ruled, "says": says,
     "governs": ["knowledge/_RUNBOOK-capture-ritual.md", "knowledge/_capture_gate.py", "knowledge/_gen_chain.py",
                 "knowledge/_seam.py", "knowledge/_gauge_tokens.py", "_CARRIES.md"],
     "evidence": ["chat #306 2026-09-28 (live) - 16:58 BST, the conductor's two-part question and his \"go on both\", quoted verbatim in `says`",
                  "notes/_lanes/306/V/DAVE-WORDS-2026-09-28-1658.md",
                  UREP + "#3. Proposed guards (PROPOSED, NOT RULED; each a gate arm)",
                  UREP, PAGE]}
json.dump(e, open(OUT + 's306-D10.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('s306-D10', len(json.dumps(e, ensure_ascii=False)), 'bytes;', by_phase)
