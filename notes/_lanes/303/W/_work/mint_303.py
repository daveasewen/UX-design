# #303 wrap seat - mint the store rows for every new #303 document (including lane P's report, which
# went out at 6c881313 under a declared DOC_ROW_ACK, and G1/G2), and add by-addition notes to two #302 rows.
# Modelled on #302's mint_302.py.
import sys, os
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/303/W/_work')
import _state as st
from names_303 import *
doc = st.load()
have = {i['id'] for i in doc['items']}
rows = [
 dict(id='W-303p', home=REPP, links=[BRIEF, DECK_SRC, PRESS], title="#303 P filed report - the press loop on slide 16: a page composed, checked by a red scan and laid on the stack, in the line-drawing style, three phases",
      body="s218-D7 filed report, lane P (#303). Committed at 6c881313 under a declared DOC_ROW_ACK; row minted by the #303 wrap seat.",
      closes_when="Dave has watched slide 16's loop on his own screen and said keep or change", owner='dave'),
 dict(id='W-303g1', home=REPG1, links=[BRIEF, VISION, REPG2], title="#303 G1 filed report - GenUI archaeology: the repo's earlier run-time and GenUI work and the run-time reuse inventory, for the Apollo-MCP proposal",
      body="s218-D7 filed report, lane G1 (#303), read-only. Source for #304's first beat.",
      closes_when="the Apollo-MCP proposal page is written from it and put to Dave", owner='claude'),
 dict(id='W-303g2', home=REPG2, links=[BRIEF, REPG1], title="#303 G2 filed report - the agent-UI landscape: A2UI, MCP Apps, AG-UI, Adaptive Cards and design-system MCP servers, 40 dated sources",
      body="s218-D7 filed report, lane G2 (#303), web research; the lane returned its research and the conductor filed it. Source for #304's first beat.",
      closes_when="the Apollo-MCP proposal page is written from it and put to Dave", owner='claude'),
 dict(id='W-303v', home=BRIEF, links=[REPP, REPG1, REPG2, PROMPT], title="#303 wrap brief - Dave's 31 messages verbatim (Thu 13:48 to Sat 13:47 BST) and the session's facts; the deck finished, the Apollo-MCP ask; nothing inscribed, store 638",
      closes_when="#304 has answered or carried every item of the brief's owed list, starting with the Apollo-MCP page", owner='dave'),
 dict(id='W-303h', home=HO, links=['GOOD-MORNING.md', '_CARRIES.md', '_CHAIN.md', HO_PREV], title="#303 handoff - the deck was finished for Friday, and Apollo-MCP was asked for",
      closes_when="#304's opener has read it and the Apollo-MCP proposal page is written; its OWED list is then carried or struck by the #304 wrap", owner='dave'),
 dict(id='W-303k', home=HOOK, links=[HO], title="#303 wrap memory hook - placed by the #303 wrap seat after Dave's 'wrap up :)', under his Project instructions",
      closes_when="the placement receipt (index line, wrap-303 file, the #300 line moved verbatim, the two area files) is appended to this file", owner='claude'),
 dict(id='W-303w', home=REPW, links=['GOOD-MORNING.md', '_LIVE-STATE.md', '_CARRIES.md', HO, REPP, REPG1, REPG2], title="#303 W - the wrap: his deck and prompt changes recorded as his acts, not inscribed; six carries struck by his acts; the wrap gate red on the boot ceiling again",
      body="s218-D7 filed report, delegated wrap seat (Opus 5.5).",
      closes_when="Dave has ruled or carried the report's 5 ruling-shaped questions - the Apollo-MCP headline, his three observations into the graph, the HSBC face in the font stack, the callipers' corner overrun, the boot ceiling", owner='dave'),
 dict(id='W-303dh', home=DOS, links=['_LIVE-STATE.md', BRIEF, REPP, REPG1, REPG2], title="#303 dossier - the why and how: the tested prompt restructured, the deck finished on his words, the press loop, the value grid, the ask replaced by his copy, the Apollo-MCP ask",
      closes_when="the Apollo-MCP proposal page is his and his three observations are in the graph", owner='dave'),
]
for r in rows:
    assert os.path.exists(r['home']), r['home']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=303, state='open', **r)
    print('added', r['id'])
notes = {
 'W-302h': " · #303 (by addition, the #303 wrap seat): read at #303's opener; the demo prompt was put to Dave first and he answered it (15:37 BST 2026-09-24, 'I've tested this already'); OWED items 1, 2, 4 and 5 are STRUCK by his acts with receipts at the #303 wrap (addendum at its foot) and the rest carried in _CARRIES.md residual -> #304.",
 'W-302k': " · #303 (by addition, the #303 wrap seat): the condition is MET - the #302 wrap seat appended its placement receipt to notes/_lanes/302/WRAP-MEMORY-HOOK.md (index.md 8,305 B, #302 · #301 · #300).",
}
for it in doc['items']:
    if it['id'] in notes and '#303 (by addition' not in (it.get('body') or ''):
        it['body'] = (it.get('body') or '').rstrip() + notes[it['id']]
        print('noted', it['id'])
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '303' in f or '302' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
