# #305 wrap seat - mint the store rows for the wrap's own documents and R1's report; close the rows whose
# conditions this session met, each with its receipt. Modelled on #304's mint_304.py.
import sys, os
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/305/W/_work')
import _state as st
from names_305 import *
doc = st.load()
have = {i['id']: i for i in doc['items']}
rows = [
 dict(id='W-305v', home=BRIEF, links=[EXPORT1, EXPORT2, R['C4']], title="#305 wrap brief - Dave's 16 messages verbatim (Sun 13:25 to Mon 10:08 BST) and the session's facts; the sitting, the cut, CI green, the loose ends, the pictures; rulings 638 -> 699",
      closes_when="#306 has answered or carried every item of the brief's 'Open, Dave's' list, starting with the 102 parked questions", owner='dave'),
 dict(id='W-305h', home=HO, links=['GOOD-MORNING.md', '_CARRIES.md', '_CHAIN.md', HO_PREV], title="#305 handoff - he took the sitting, v1.0.14 was cut, and CI went green",
      closes_when="#306's opener has read it and put the 102 parked questions to Dave; its OWED list is then carried or struck by the #306 wrap", owner='dave'),
 dict(id='W-305wk', home=HOOK, links=[HO], title="#305 wrap memory hook - payloads prepared by the #305 wrap seat (files only, no memory tool) for the conductor to place after Dave's 'wrap'",
      closes_when="the placement receipt (index line, wrap-305 file, the oldest index line moved verbatim, the four area additions) is appended to this file", owner='claude'),
 dict(id='W-305w', home=REPW, links=['GOOD-MORNING.md', '_LIVE-STATE.md', '_CARRIES.md', HO, BRIEF], title="#305 W - the wrap: 14 commits and 7 CI reads recorded, rulings 638 -> 699, 13 carries struck with receipts, the pictures lesson carried; wrap commit on the declared not-a-wrap path by the brief",
      body="s218-D7 filed report, delegated wrap seat (Opus 5.5).",
      closes_when="Dave has ruled or carried the report's ruling-shaped questions - the 102, s212-D1/s256-D1, the ring and the threads, the s279-D1/W-305n6 collision, whether --wrap is the wrap path again", owner='dave'),
 dict(id='W-305dh', home=DOS, links=['_LIVE-STATE.md', BRIEF, EXPORT1, EXPORT2], title="#305 dossier - the why and how: set in ink, the sitting by lanes of kind, the cut and V2's collision, the public repo, why CI took three runs, the loose ends and the pictures",
      closes_when="the 102 parked questions have his ticks and the s279-D1 / W-305n6 collision is ruled", owner='dave'),
]
for r in rows:
    assert os.path.exists(r['home']), r['home']
    for l in r['links']:
        assert l.startswith('W-') or os.path.exists(l), l
    assert st.ID_RE.match(r['id']), r['id']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=305, state='open', condition='stated', **r)
    print('added', r['id'])
if 'W-305r1' not in have:
    st.add(doc, project='apollo', opened=305, state='done', condition='stated', id='W-305r1', home=R['R1'], links=[R['B5'], LOOSE],
           title="#305 R1 - the hub's other ten pages reconciled against the Tuesday sitting; what was left open became the loose-ends page",
           closes_when="the report is committed and the loose ends it listed are put to Dave",
           closed_by="#305 wrap seat: B5 built the loose-ends page from its 'What is left open' items 1-5 (" + R['B5'] + ", committed at f6aeb264), Dave answered it Mon 2026-09-28 08:05 BST (" + EXPORT2 + "), and this report rides the #305 wrap commit",
           owner='claude')
    print('added W-305r1 (done)')
closes = {
 'W-305c4': "#305 wrap seat: the FINAL copy of " + R['C4'] + " (commit f6aeb264, stamp commit cd16f7ec, push 01fb005a..cd16f7ec, CI run 36393419907 green on release, gates and render) and its post-push tail under notes/_lanes/305/C4/ ride the #305 wrap commit, as the row's close condition says",
 'W-305c1': "#305 wrap seat: the FINAL copy of " + R['C1'] + " (27efb7b6, 568e2534, push 7cae0189..568e2534, CI run 36330780485 by job) was committed at 0ef30746 and reads clean against HEAD",
 'W-305c2': "#305 wrap seat: the FINAL copy of " + R['C2'] + " (1e107eea and the stamps commit 21c9b7f4) was committed at 21c9b7f4 and reads clean against HEAD",
 'W-305c3': "#305 wrap seat: the FINAL copy of " + R['C3'] + " (e4ff4284, stamps 7b544593, push 21c9b7f4..e4ff4284, CI run 36345615782 by job) was committed at 7b544593 and reads clean against HEAD",
 'W-305p1': "#305 wrap seat: " + R['P1'] + " and its lane dir were committed at e4ff4284 (git log of the path)",
 'W-305a': "#305 wrap seat: the s305-D1..D57 inscriptions and their evidence files were committed at 27efb7b6 and the builds' rulings stamped enacted by the commit seats at 568e2534 (18), 21c9b7f4 (11) and 7b544593 (3)",
 'W-305a2': "#305 wrap seat: " + R['A2'] + ", its lane dir (minus backup/) and the four evidence files (the loose-ends export, the page, B5's report, rings.json) were committed at f6aeb264 (C4)",
 'W-305b5': "#305 wrap seat: " + LOOSE + ", " + R['B5'] + " and notes/_lanes/305/B5/ (minus shots/) were committed at f6aeb264 (C4)",
 'W-305b6': "#305 wrap seat: the four meta edits and when-fields.json were committed at f6aeb264 and s305-D60 was stamped enacted at that sha in cd16f7ec (C4)",
 'W-305f1': "#305 wrap seat: both fixes pushed (e4ff4284), then D1's git-2.55 fix; CI runs 36349147952 and 36393419907 read [133], [134], [145], [146] and the release job's step 7 green (" + R['D1'] + ", " + R['C4'] + ")",
 'W-303h': "#305 wrap seat: the condition was met at the #304 wrap - #304's opener read it, the Apollo-MCP page was written (6af293df) and its OWED list was carried or struck by the #304 wrap (9f9ff879, _HANDOFF-155 § THE STRIKES and _HANDOFF-154's #304 addendum); closed now, before the regrowth arm names it",
 'W-304h': "#305 wrap seat: #305's opener read it and put the Tuesday sitting to Dave (Sun 13:26 BST); its OWED list is carried or struck by the #305 wrap (" + HO + " § THE STRIKES and the addendum at _HANDOFF-155's foot)",
 'W-304v': "#305 wrap seat: every item of the #304 brief's owed list is answered or carried - the sitting answered (" + EXPORT1 + "), the rest struck or carried in _CARRIES.md residual -> #306",
 'W-304fb': "#305 wrap seat: Dave sat with the page on Sun 2026-09-27 and exported his rulings - to notes/_lanes/305/ rather than notes/_lanes/304/ (" + EXPORT1 + ") - and lane A inscribed each of the 53 by his words as s305-D2..D56 (" + R['A'] + ", 27efb7b6)",
 'W-304rs': "#305 wrap seat: Dave ruled the v1.0.14 cut question - sitting call 1, 'yes', s305-D2 - and K cut it at 0ef30746 / 02d679b3 / d3b809a7",
 'W-304m': "#305 wrap seat: Dave answered the seven decisions at the sitting (calls 42-51), inscribed as s305-D45..D54",

 'W-304w': "#305 wrap seat: the report's ruling-shaped questions are ruled or carried - the three behaviours (s305-D7, s305-D14), the two held back (s305-D6, s305-D43), the hub's links (they open), the boot ceiling (s305-D29); the dream pass's runbook is carried in _CARRIES.md residual -> #306",
 'W-304dh': "#305 wrap seat: the Tuesday sitting was held (Sun 2026-09-27, " + EXPORT1 + ") and the three behaviours shipped without a ruling are his - s305-D7 and s305-D14",
}
for iid, why in closes.items():
    it = have[iid]
    if it['state'] != 'done':
        it['state'] = 'done'; it['closed_by'] = why
        print('closed', iid)
ok, fails, _ = st.check(doc)
print('check ok', ok, fails[:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
