# #300 wrap seat - mint the store rows for every new #300 document (the new-doc-needs-a-store-row
# gate covers notes/_subreports/*.md; the rest follow #299's practice), and add by-addition notes
# to two #299 rows whose conditions this session met.
import sys, os
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/300/W/_work')
import _state as st
from names_300 import *
doc = st.load()
have = {i['id'] for i in doc['items']}
R = "s218-D7 filed report, lane %s (#300). Row owed by the conductor, minted by the #300 wrap seat. The lane brief (notes/_lanes/300/BRIEF-300-boot-diet.md) asked for plain words and a stub, so the report carries no COUNTS line (advisory warn, reported in the #300 wrap report)."
rows = [
 dict(id='W-300a', home=REPA, links=[LANE_BRIEF], title="#300 A filed report - the cloud boot attributed: 126,185 = tools ~65K + Anthropic's prompt ~31.5K + the memory list ~19K; the cloud adds ~51K over the desktop seat",
      body=R % 'A', closes_when="Dave has ruled or carried the plan page's post-Friday steps that rest on this attribution (the Mac seat, the memory cut)", owner='dave'),
 dict(id='W-300b', home=REPB, links=[LANE_BRIEF], title="#300 B filed report - levers and seats: settings reach little; pausing memory is account-wide; the Mac seat (~30K boot) is the big lever",
      body=R % 'B', closes_when="Dave has said whether the Mac seat is trialled after Friday and whether any account switch is used", owner='dave'),
 dict(id='W-300c', home=REPC, links=[LANE_BRIEF, ROLLBACK], title="#300 C filed report - the opener costs 81,049 (61,678 + a 19,371 re-send); v2 instructions save ~50.6K; the boot card is after Friday",
      body=R % 'C', closes_when="#301 has measured the fill under the v2 instructions Dave pasted, and Dave has ruled the card-versus-chain question", owner='dave'),
 dict(id='W-300d', home=REPD, links=[LANE_BRIEF], title="#300 D filed report - the memory store: 250 files, the boot list shows 150 of 234 Apollo files, ~200 imported notes never committed; export before any cut",
      body=R % 'D', closes_when="Dave has decided whether the store is exported into the repo and then cut, left, or retired for Apollo", owner='dave'),
 dict(id='W-300x', home=REPX, links=[REPA, REPB, REPC, REPD], title="#300 X filed report - the adversary: card alone 4/18 FALSE, card + chain 12/18, handoff + chain 18/18; BM25 look-up 11/18 vs 2/18; the stop threw away two lanes",
      body=R % 'X', closes_when="Dave has ruled the plan page's seven questions, each read beside X's verdict", owner='dave'),
 dict(id='W-300p', home=REPP, links=[PLAN, REPX], title="#300 P filed report - the plan page: four before-Friday moves, thirteen levers ranked, six after-Friday steps, seven questions",
      body=R % 'P', closes_when="Dave has answered the page's before-Friday moves 3 and 4 and ruled or carried its after-Friday steps", owner='dave'),
 dict(id='W-300g', home=PLAN, links=[REPP, REPX], title="#300 plan page - the boot diet: four moves before Friday, the levers ranked with the adversary's verdicts, the Memento balance, look-up",
      closes_when="Dave has acted on or declined each before-Friday move and ruled the seven after-Friday questions", owner='dave'),
 dict(id='W-300i', home=LIVE, links=[LIVE_TXT, ROLLBACK, PLAN], title="#300 - the Project instructions Dave pasted before wrap, byte-exact, and their diff against the page, lane C's draft and the rollback",
      body="His act, not an inscribed ruling. The text is identical to the plan page's paste-ready block and differs from lane C's draft at step 4 only.",
      closes_when="Dave has said whether the pasted text becomes a ruling (it changes ritual step 3), and #301 has measured the opener it produces", owner='dave'),
 dict(id='W-300v', home=BRIEF, links=[LANE_BRIEF], title="#300 wrap brief - Dave's words verbatim (15:46 to 17:56 BST, incl. the 16:16 queued note) and the session's facts; nothing inscribed, store 638",
      closes_when="#301 has answered or carried every item of the brief's OPEN list, starting with the ask on slide 15", owner='dave'),
 dict(id='W-300h', home=HO, links=['GOOD-MORNING.md', '_CARRIES.md', '_CHAIN.md'], title="#300 handoff - the boot was measured, and the reading stays",
      closes_when="#301's opener has read it under the new instructions and put the ask on slide 15 to Dave; its OWED list is then carried or struck by the #301 wrap", owner='dave'),
 dict(id='W-300k', home=HOOK, links=[HO], title="#300 wrap memory hook - placed by the #300 wrap seat after Dave's wrap, under his pasted instructions",
      closes_when="the placement receipt (index line, wrap-300 file, the #297 line moved verbatim) is appended to this file", owner='claude'),
 dict(id='W-300w', home=REPW, links=['GOOD-MORNING.md', '_LIVE-STATE.md', '_CARRIES.md', HO], title="#300 W - the wrap: the boot was measured, the reading stays, his pasted instructions saved byte-exact, one headline struck, the wrap gate red on the boot ceiling again",
      body="s218-D7 filed report, delegated wrap seat (Opus 5.5).",
      closes_when="Dave has ruled or carried the report's 5 ruling-shaped questions - the boot ceiling, whether his pasted instructions become a ruling, headline strikes, the s218-D7 skeleton in lane briefs, and the hand sum as the wrap's measurement", owner='dave'),
 dict(id='W-300dh', home=DOS, links=['_LIVE-STATE.md', BRIEF], title="#300 dossier - the why and how: four lanes and an adversary on the boot, the quiz that kept the reading, the look-up test, the stop, and his paste",
      closes_when="the ask for slide 15 is written and Friday's deck is final", owner='dave'),
]
for r in rows:
    assert os.path.exists(r['home']), r['home']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=300, state='open', **r)
    print('added', r['id'])
notes = {
 'W-299k': " · #300 (by addition, the #300 wrap seat): the condition is MET as DECLARED by the conductor — the #300 opener placed the index line and the wrap-299 file from the conductor's own seat; the store is read and the receipt appended to notes/_lanes/299/WRAP-MEMORY-HOOK.md at the #300 wrap's 5b.",
 'W-299h': " · #300 (by addition, the #300 wrap seat): read at #300's opener, and the ask on slide 15 was put to Dave in the first reply (unanswered); its OWED item 8's first headline is STRUCK with receipts at the #300 wrap and the rest carried in _CARRIES.md residual -> #301.",
}
for it in doc['items']:
    if it['id'] in notes and notes[it['id']].strip(' ·')[:12] not in it.get('body', ''):
        it['body'] = (it.get('body') or '').rstrip() + notes[it['id']]
        print('noted', it['id'])
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '300' in f or '299' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
