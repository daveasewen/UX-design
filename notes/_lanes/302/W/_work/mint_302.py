# #302 wrap seat - mint the store rows for every new #302 document (including lane A's two reports,
# which went out at 7f10b5b8 under a declared DOC_ROW_ACK), and add by-addition notes to two #301 rows.
# Modelled on #301's mint_301.py.
import sys, os
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/302/W/_work')
import _state as st
from names_302 import *
doc = st.load()
have = {i['id'] for i in doc['items']}
rows = [
 dict(id='W-302a', home=REPA, links=[BRIEF, DECK_SRC], title="#302 A filed report - the callipers on 09 and 12 stood upright, then turned over, floating, jaw end raised 10 deg; ray-cast 0 bad samples in 18 views",
      body="s218-D7 filed report, lane A (#302), resumed three times. Committed at 7f10b5b8 under a declared DOC_ROW_ACK; row minted by the #302 wrap seat. No COUNTS, REPLAY-THESE or RULING-SHAPED lines (advisory, reported in the #302 wrap report).",
      closes_when="Dave has said whether the ~50px orbit-corner overrun stays or the view is reframed", owner='dave'),
 dict(id='W-302b', home=REPB, links=[BRIEF, DECK_SRC], title="#302 B filed report - the new slide 15, Benefits beyond speed, quality and consistency: Customisation / Convergence / Cost-effectiveness, Light, $3.2m bold red",
      body="s218-D7 filed report, lane A (#302). Committed at 7f10b5b8 under a declared DOC_ROW_ACK; row minted by the #302 wrap seat. No COUNTS, REPLAY-THESE or RULING-SHAPED lines (advisory).",
      closes_when="Dave has seen slide 15's Light headwords on his own screen (the seat cannot show Univers Next)", owner='dave'),
 dict(id='W-302v', home=BRIEF, links=[REPA, REPB], title="#302 wrap brief - Dave's words verbatim (07:22 to 12:42 BST) and the session's facts; the ask to his colleagues; nothing inscribed, store 638",
      closes_when="#303 has answered or carried every item of the brief's owed list, starting with the demo prompt", owner='dave'),
 dict(id='W-302h', home=HO, links=['GOOD-MORNING.md', '_CARRIES.md', '_CHAIN.md', HO_PREV], title="#302 handoff - the deck grew a slide, and the ask went to his colleagues",
      closes_when="#303's opener has read it and put the demo prompt to Dave; its OWED list is then carried or struck by the #303 wrap", owner='dave'),
 dict(id='W-302k', home=HOOK, links=[HO], title="#302 wrap memory hook - placed by the #302 wrap seat after Dave's wrap, under his pasted instructions",
      closes_when="the placement receipt (index line, wrap-302 file, the #299 line moved verbatim) is appended to this file", owner='claude'),
 dict(id='W-302w', home=REPW, links=['GOOD-MORNING.md', '_LIVE-STATE.md', '_CARRIES.md', HO, REPA, REPB], title="#302 W - the wrap: his deck changes recorded as his acts, not inscribed; the ask struck in part; 7f10b5b8's CI read back; the wrap gate red on the boot ceiling again",
      body="s218-D7 filed report, delegated wrap seat (Opus 5.5).",
      closes_when="Dave has ruled or carried the report's 4 ruling-shaped questions - the demo prompt, the HSBC face in the font stack, judgement layer on 13, the callipers' corner overrun", owner='dave'),
 dict(id='W-302dh', home=DOS, links=['_LIVE-STATE.md', BRIEF, REPA, REPB], title="#302 dossier - the why and how: the ask to his colleagues, slides 11-13, the Scrutiny plate, the callipers twice, the benefits slide and its four words, the fallback face",
      closes_when="Friday's deck is final and the demo prompt is his", owner='dave'),
]
for r in rows:
    assert os.path.exists(r['home']), r['home']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=302, state='open', **r)
    print('added', r['id'])
notes = {
 'W-301h': " · #302 (by addition, the #302 wrap seat): read at #302's opener; the ask and the demo brief were put to Dave and he answered both at 07:43 BST ('1. this will come from my colleagues' / '2. we'll do this after some more changes'); OWED item 1 is STRUCK IN PART with its receipt at the #302 wrap (addendum at its foot) and the rest carried in _CARRIES.md residual -> #303.",
 'W-301k': " · #302 (by addition, the #302 wrap seat): the condition is MET - the #301 wrap seat appended its placement receipt to notes/_lanes/301/WRAP-MEMORY-HOOK.md (index.md 7,538 B, #301 · #300 · #299).",
}
for it in doc['items']:
    if it['id'] in notes and '#302 (by addition' not in (it.get('body') or ''):
        it['body'] = (it.get('body') or '').rstrip() + notes[it['id']]
        print('noted', it['id'])
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '302' in f or '301' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
