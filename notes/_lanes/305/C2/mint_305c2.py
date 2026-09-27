# #305 C2 commit seat - mint doc rows for wave two's reports (H1, H2, V2, C2). Modelled on notes/_lanes/305/C1/mint_305c1.py.
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/2026-09-27-305-'
rows = [
 dict(id='W-305hr', home=S + 'H1-records.md', owner='claude', condition='stated',
      links=['knowledge/_state.json', 'knowledge/_rulings.json', 'knowledge/_parked.json', '_CARRIES.md', 'notes/_lanes/305/H1/'],
      title="#305 H1 the records lane - sitting calls 13 and 31-39 applied through the sanctioned writers: live 741 -> 485, carry residual 715 -> 391",
      body=("s218-D7 filed report. Call 31 95/95 closed; 32 102/102 parked with B4's tripwires; 33 20 closed + 2 kept parked (W-222, W-272, also on the call-32 scan); "
            "34 17/17 closed; 35 14/14 dispositioned (W-305h1..h4 split out); 36 324 of 342 dropped from the #305 residual, 18 held on purpose; 37 26 parked; "
            "38 kinds 1-4 and 36 of kind 6 stamped, kind 5 and 28 of kind 6 left; 39 all three halves (P-305-1, P-305-2, s135-D3 superseded); W-304r3 closed."),
      closes_when="the wave carrying these store, ruling, parked and carry writes is committed, and Dave has said which way W-222 and W-272 go and re-sorted the 28 kind-6 rulings or left them"),
 dict(id='W-305hc', home=S + 'H2-code.md', owner='claude', condition='stated',
      links=['knowledge/_gauge_tokens.py', 'knowledge/_state.py', 'knowledge/_git_commit.sh', 'knowledge/_TOKEN-FORK-LEDGER.json', '_retired/deck-v7-slide-checkers-268/README.md'],
      title="#305 H2 the code lane - window lines 236,000/276,000, boot ceiling 130,000, the regrowth arming switch and doc birth, the helper-aware push check, the three CI calls",
      body=("s218-D7 filed report. Calls 28, 29, 40, 41 in the code, and call 30's consequence in _git_commit.sh --push. Fork ban [92]/[93], delta-audit [133]/[134] and the boot-ceiling arm "
            "green at the seat; _build_all.py unchanged at 154 steps; seven deck checkers retired by move. Regrowth arming: armed when the 75 pinned rows are closed or parked."),
      closes_when="the wave carrying these paths is committed, CI has read [92], [133] and [134] green, and knowledge/_standing.md's 180,000 line is put to Dave"),
 dict(id='W-305v2', home=S + 'V2-verifier-cut.md', owner='claude', condition='stated',
      links=['notes/_lanes/305/V2/shoot.py', 'notes/_lanes/305/V2/hits-surprise.txt', 'notes/_lanes/305/V2/renders/', 'W-305n6'],
      title="#305 V2 cold verifier of the v1.0.14 zip - the zip is sound, but it ships s305-D45..D55 (the Launchpad PoC): DO NOT SHIP to the audience until Dave rules",
      body=("s218-D7 filed report, cold verifier. sha256 matches, manifest matches, frozen-release PASS, demo page 7/7; the shipped _rulings.json carries the PoC rulings, "
            "colliding s279-D1 with W-305n6; showroom/_foundations/logos.html has four broken images (identifier files scrapped at s282-D4)."),
      closes_when="Dave has ruled the s279-D1 / W-305n6 collision (hand nothing over, or cut v1.0.15 without the reader group, or let the name travel), and the logos foundation page is regenerated or carried as a named defect"),
 dict(id='W-305c2', home=S + 'C2-commit.md', owner='claude', condition='stated',
      links=['notes/_lanes/305/C2/'],
      title="#305 C2 commit seat, wave two - H1, H2, K's post-Y2 tail and V2 committed locally, the discharged s305 rulings stamped enacted; no push",
      body=("s218-D7 filed report, commit seat (interim-report pattern). The interim copy rides the wave-two commit; the final copy with both shas, "
            "the stamps done and left, and the held list rides the stamps commit. Nothing is pushed by this seat."),
      closes_when="the final copy of this report, carrying both shas and the stamps done and left, is committed"),
]
doc = st.load()
have = {i['id'] for i in doc['items']}
for r in rows:
    assert os.path.exists(r['home']), r['home']
    for l in r['links']:
        assert l.startswith('W-') or os.path.exists(l), l
    assert st.ID_RE.match(r['id']), r['id']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=305, state='open', **r)
    print('added', r['id'])
ok, fails, _ = st.check(doc)
print('check ok', ok)
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
