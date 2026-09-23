# #301 wrap seat - mint the store rows for every new #301 document, and add by-addition notes
# to two #300 rows whose conditions this session met. Modelled on #300's mint_300.py.
import sys, os
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/301/W/_work')
import _state as st
from names_301 import *
doc = st.load()
have = {i['id'] for i in doc['items']}
rows = [
 dict(id='W-301g', home=REPG, links=[BRIEF], title="#301 G filed report - the window's hard line 256,000 -> 300,000 and working 200,000 -> 256,000, PICKED Dave #301; boot ceiling 72,768 and amber unmoved",
      body="s218-D7 filed report, lane G (#301), resumed once. Row owed by the conductor, minted by the #301 wrap seat. The report carries no COUNTS line, no REPLAY-THESE line and no RULING-SHAPED QUESTIONS heading (advisory warns, reported in the #301 wrap report). His words enacted as his acts, not inscribed.",
      closes_when="Dave has said whether his three window messages are inscribed, and whether the stop (180,000) and tolerance (220,000) lines move under the new 256,000 working line", owner='dave'),
 dict(id='W-301v', home=BRIEF, links=[REPG], title="#301 wrap brief - Dave's words verbatim (19:11 to 20:58 BST) and the session's facts; the new opener measured; nothing inscribed, store 638",
      closes_when="#302 has answered or carried every item of the brief's open list, starting with the ask on slide 15", owner='dave'),
 dict(id='W-301h', home=HO, links=['GOOD-MORNING.md', '_CARRIES.md', '_CHAIN.md', HO_PREV], title="#301 handoff - the window was raised, and the ask is still open",
      closes_when="#302's opener has read it and put the ask on slide 15 to Dave; its OWED list is then carried or struck by the #302 wrap", owner='dave'),
 dict(id='W-301k', home=HOOK, links=[HO], title="#301 wrap memory hook - placed by the #301 wrap seat after Dave's wrap, under his pasted instructions",
      closes_when="the placement receipt (index line, wrap-301 file, the #298 line moved verbatim) is appended to this file", owner='claude'),
 dict(id='W-301w', home=REPW, links=['GOOD-MORNING.md', '_LIVE-STATE.md', '_CARRIES.md', HO, REPG], title="#301 W - the wrap: his window words recorded as his acts, not inscribed; four carries and two headlines struck; the wrap gate red on the boot ceiling again",
      body="s218-D7 filed report, delegated wrap seat (Opus 5.5).",
      closes_when="Dave has ruled or carried the report's 5 ruling-shaped questions - inscribing the window messages, the stop and tolerance lines, the _standing.md:19 wording, the boot ceiling, and the hand sum as the wrap's measurement", owner='dave'),
 dict(id='W-301dh', home=DOS, links=['_LIVE-STATE.md', BRIEF, REPG], title="#301 dossier - the why and how: the first chat under his pasted instructions, the conductor's reasoning in the window, his polish answers, and the window lines he moved",
      closes_when="the ask for slide 15 is written and Friday's deck is final", owner='dave'),
]
for r in rows:
    assert os.path.exists(r['home']), r['home']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=301, state='open', **r)
    print('added', r['id'])
notes = {
 'W-300h': " · #301 (by addition, the #301 wrap seat): read at #301's opener under his pasted instructions, and the ask on slide 15 was put to Dave (unanswered, twice); its OWED items 2, 3, 4 and 8, item 6's second half and item 10's 256K headline are STRUCK with receipts at the #301 wrap (addendum at its foot) and the rest carried in _CARRIES.md residual -> #302.",
 'W-300k': " · #301 (by addition, the #301 wrap seat): the condition is MET - the #300 wrap seat appended its placement receipt to notes/_lanes/300/WRAP-MEMORY-HOOK.md (index.md 6,825 B, #300 · #299 · #298).",
}
for it in doc['items']:
    if it['id'] in notes and '#301 (by addition' not in (it.get('body') or ''):
        it['body'] = (it.get('body') or '').rstrip() + notes[it['id']]
        print('noted', it['id'])
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '301' in f or '300' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
