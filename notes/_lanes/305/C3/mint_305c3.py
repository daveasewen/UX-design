# #305 C3 commit seat - mint doc rows for wave three's reports (F1, W2, P1, C3). Modelled on notes/_lanes/305/C2/mint_305c2.py.
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/2026-09-27-305-'
rows = [
 dict(id='W-305f1', home=S + 'F1-ci-reds.md', owner='claude', condition='stated',
      links=['knowledge/_release/_gen_pack_manifest.py', 'knowledge/_validate_package_delta.py', 'notes/_lanes/305/F1/'],
      title="#305 F1 the two CI reds of run 36341948728 - an enacted release ruling read as not ratified ([145], [146], release step 7), and a quote typed from Python 3.10's ast.unparse ([133], [134])",
      body=("s218-D7 filed report. ratification_status() now counts a status whose first word is ruled or enacted (case-insensitive, declared); "
            "_validate_package_delta.py renders the tuple-unpack quote with the running interpreter's ast.unparse. Proved in a clean clone of 21c9b7f4 under Python 3.12.14 and 3.10.12; "
            "the committed _pack_manifest.json is byte-unchanged and a fresh generation matches it. [147]-[154] were not proved by the lane."),
      closes_when="the wave carrying both fixes is pushed and CI reads [133], [134], [145], [146] and the release job's step 7 green"),
 dict(id='W-305w2', home=S + 'W2-remaining.md', owner='claude', condition='stated',
      links=['knowledge/guidelines/web-foundations.md', 'knowledge/_validate_a11y.py', 'notes/_jev-link-check/jev_link_check.py', 'notes/_lanes/305/W2/'],
      title="#305 W2 the four rulings recorded but not built - own size in the graph (webf-036), the motion check per part, Jev as a hand-run link checker built; the rails half of s305-D10 held with its drift named",
      body=("s218-D7 filed report. s305-D24: rule webf-036 with enforcedBy/definedIn edges added by addition (never gen_kg_rules.py --land, which drops 75 restsOn edges); "
            "s305-D54: _validate_a11y 2.3.3 per part, zero verdict changes over 282 files; s305-D55: 330 of 330 links asked, 13 look wrong, for Dave. "
            "s305-D10's rails half held: a first-match resolver bug, the nav family as a tile group, and no ramp word for surface/section."),
      closes_when="the wave carrying these paths is committed, and Dave has seen the 13 looks-wrong links and ruled the rails half's two questions (the ramp word and its scope, the nav family) or parked them"),
 dict(id='W-305p1', home=S + 'P1-push-ci.md', owner='claude', condition='stated',
      links=['notes/_lanes/305/P1/'],
      title="#305 P1 the push and CI seat - pushed 568e2534..21c9b7f4, CI run 36341948728 read to completion: release red on the ship-list audit, gates red on [133], [134], [145], [146]",
      body=("s218-D7 filed report. Cause of the release red found and not repaired (ratification_status read s305-D2's enacted stamp as not ratified); "
            "step 6 aborted at [146], so [147]-[154] were not asked. W-305k left open."),
      closes_when="this report and its lane dir are committed"),
 dict(id='W-305c3', home=S + 'C3-commit.md', owner='claude', condition='stated',
      links=['notes/_lanes/305/C3/'],
      title="#305 C3 commit, push and CI seat, wave three - F1's fixes, W2's builds and P1's report committed, s305-D24/D54/D55 stamped enacted, pushed, CI read back",
      body=("s218-D7 filed report, commit seat (interim-report pattern). The interim copy rides the wave-three commit; the final copy with both shas, "
            "the push range, the CI run and the red set by name rides the stamps commit."),
      closes_when="the final copy of this report, carrying both shas, the push range and the CI verdict by job, is committed"),
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
