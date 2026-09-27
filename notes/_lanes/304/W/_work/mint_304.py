# #304 wrap seat - mint the store rows for the wrap's own documents, close W-304c6 (its final copy rides this
# commit), W-304c1 (its final copy rode 4be130e5) and W-303g1/g2 (the page was written from them and put to Dave),
# and add by-addition notes to W-303h and W-303k. Modelled on #303's mint_303.py and C6's mint_304c6.py.
import sys, os
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/304/W/_work')
import _state as st
from names_304 import *
doc = st.load()
have = {i['id']: i for i in doc['items']}
rows = [
 dict(id='W-304v', home=BRIEF, links=[REPW5B, SITTING, REPC6, ARTIFACT_COPY], title="#304 wrap brief - Dave's 13 messages verbatim (Sat 14:40 to Sun 12:16 BST, seven sent mid-turn) and the session's facts; the weekend runs, the links, the artifact; nothing inscribed, store 638",
      closes_when="#305 has answered or carried every item of the brief's owed list, starting with the Tuesday sitting", owner='dave'),
 dict(id='W-304h', home=HO, links=['GOOD-MORNING.md', '_CARRIES.md', '_CHAIN.md', HO_PREV], title="#304 handoff - the weekend runs landed, and the review moved to an artifact",
      closes_when="#305's opener has read it and put the Tuesday sitting to Dave; its OWED list is then carried or struck by the #305 wrap", owner='dave'),
 dict(id='W-304k', home=HOOK, links=[HO], title="#304 wrap memory hook - payloads prepared by the #304 wrap seat for the conductor to place after Dave's 'no worries lets wrap up'",
      closes_when="the placement receipt (index line, wrap-304 file, the #301 line moved verbatim, the two area additions and the two new area files) is appended to this file", owner='claude'),
 dict(id='W-304w', home=REPW, links=['GOOD-MORNING.md', '_LIVE-STATE.md', '_CARRIES.md', HO, BRIEF, SITTING], title="#304 W - the wrap: seven pushed commits and six CI reads recorded, nothing inscribed; four carries struck by acts and receipts; the artifact hub's links measured without their notes/ prefix; the wrap gate red on the boot ceiling again",
      body="s218-D7 filed report, delegated wrap seat (Opus 5.5).",
      closes_when="Dave has ruled or carried the report's ruling-shaped questions - the three behaviours shipped without a ruling, the two held back, the dream pass's runbook, the hub's links, the boot ceiling", owner='dave'),
 dict(id='W-304dh', home=DOS, links=['_LIVE-STATE.md', BRIEF, REPM, REPF, REPW5B], title="#304 dossier - the why and how: the proposal page and the Jev correction, the plan and six runs, the four waves after them, the dream pass on a live tree, the links and the artifact",
      closes_when="the Tuesday sitting has been held and the three behaviours shipped without a ruling are his", owner='dave'),
]
for r in rows:
    assert os.path.exists(r['home']), r['home']
    for l in r['links']:
        assert l.startswith('W-') or os.path.exists(l), l
    assert st.ID_RE.match(r['id']), r['id']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=304, state='open', condition='stated', **r)
    print('added', r['id'])
closes = {
 'W-304c6': "#304 wrap seat: the FINAL copy of notes/_subreports/2026-09-27-304-C6-verify-and-commit-wave-six.md (sha 8a5fa863, push 52049781..8a5fa863, CI run 36311157795 by job) and its transcripts in notes/_lanes/304/C6/ ride the #304 wrap commit, as the row's close condition says",
 'W-304c1': "#304 wrap seat: the FINAL copy of notes/_subreports/2026-09-26-304-C1-commit-seat-wave-one.md (sha 6af293df, push 571d458c..6af293df, CI run 36257551837 by job) rode 4be130e5 (git log of the path: 6af293df interim, 4be130e5 final), as the row's close condition says",
 'W-303g1': "#304 wrap seat: the Apollo-MCP proposal page was written from it - v1 by lane M (notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html, report notes/_subreports/2026-09-26-304-M-apollo-mcp-proposal.md) and v2 on Dave's 14:51/14:52 words, both at 6af293df - and put to Dave (15:02 BST 2026-09-26 in chat, and item 11 of the artifact 'Apollo 304 review')",
 'W-303g2': "#304 wrap seat: the Apollo-MCP proposal page was written from it (G2's sources 1-40 parsed from the filed report by notes/_lanes/304/M/build.py) - v1 and v2 at 6af293df - and put to Dave (15:02 BST 2026-09-26 in chat, and item 11 of the artifact 'Apollo 304 review')",
}
for iid, why in closes.items():
    it = have[iid]
    if it['state'] != 'done':
        it['state'] = 'done'; it['closed_by'] = why
        print('closed', iid)
notes = {
 'W-303h': " · #304 (by addition, the #304 wrap seat): read at #304's opener; the Apollo-MCP page was written (v1, v2 at 6af293df); OWED item 1 STRUCK by the act at the #304 wrap (addendum at its foot), items 2-8 carried in _CARRIES.md residual -> #305.",
 'W-303k': " · #304 (by addition, the #304 wrap seat): the #303 note WAS placed, by the conductor after efe3bb47 and 571d458c - the store's index.md carries the receipt line 'THE CUT WAS PAID AT #303's WRAP (2026-09-26)' and the #303 line at the top (read at the #304 wrap, index.md 34877d8ae0fe); the receipt was not appended to the hook file itself, so the condition as written is not met.",
}
for it in doc['items']:
    if it['id'] in notes and '#304 (by addition' not in (it.get('body') or ''):
        it['body'] = (it.get('body') or '').rstrip() + notes[it['id']]
        print('noted', it['id'])
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '304' in f or '303' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
