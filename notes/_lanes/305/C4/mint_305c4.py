# #305 C4 commit seat - mint doc rows for day two's reports (A2, B6, B5, C4). Modelled on notes/_lanes/305/C3/mint_305c3.py.
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/'
rows = [
 dict(id='W-305a2', home=S + '2026-09-28-305-A2-loose-ends.md', owner='claude', condition='stated',
      links=['notes/_lanes/305/DAVE-RULINGS-2026-09-28-loose-ends.md', 'notes/_DECIDE-305-loose-ends-2026-09-27-v1.html', 'notes/_lanes/305/A2/'],
      title="#305 A2 the inscription seat, loose ends - Dave's 2026-09-28 answers inscribed as s305-D58..D61, thirteen status and evidence writes, five threads W-305e1..e5, Friday's 13 recorded",
      body=("s218-D7 filed report. _rulings.json 695 -> 699 and _state.json 925 -> 930 through the sanctioned writers only; "
            "s305-D61 enacted at e4ff4284; s305-D60 left for the commit that carries B6's four meta edits; D58 and D59 ruled, need build."),
      closes_when="this report, its lane dir and the four files its evidence points at (the export, the loose-ends page, B5's report, rings.json) are committed"),
 dict(id='W-305b6', home=S + '2026-09-28-305-B6-names-and-rules.md', owner='claude', condition='stated',
      links=['knowledge/when-fields.json', 'knowledge/components/button.meta.json', 'notes/_lanes/305/B6/'],
      title="#305 B6 the four names held, the accepted when-rules built (4 moved, 11 already in the tree), the ring and the two wordings confirmed",
      body=("s218-D7 filed report. Four when lines (filter bar, footer, the dashboard bento template, button AND actions <= 1) and layout.grammar in when-fields.json by addition; "
            "list and top-nav metas untouched (his Change on both); chooser output byte-identical before and after. The four setting-or-slot names held for the PoC."),
      closes_when="the four meta edits and when-fields.json are committed and s305-D60 is stamped enacted at that sha"),
 dict(id='W-305b5', home=S + '2026-09-27-305-B5-loose-ends.md', owner='claude', condition='stated',
      links=['notes/_DECIDE-305-loose-ends-2026-09-27-v1.html', 'notes/_lanes/305/B5/rings.json', 'notes/_lanes/305/B5/'],
      title="#305 B5 the loose ends - one decision page for what the sitting did not answer (candidate 2's six blanks, four names, the two greens, three wordings, the 13)",
      body=("s218-D7 filed report. Page rendered at 1440 and 390, light and dark, 0 overflow, 0 page errors; ring widths re-measured 90.5 / 95.2 / 47.8 percent (rings.json); "
            "the decision bar driven and its copied text read back. Dave answered it on 2026-09-28 (the export A2 inscribed)."),
      closes_when="the page, this report and the lane dir are committed"),
 dict(id='W-305c4', home=S + '2026-09-28-305-C4-commit.md', owner='claude', condition='stated',
      links=['notes/_lanes/305/C4/'],
      title="#305 C4 commit, push and CI seat, day two - A2, B6, B5, the call-27 page, Dave's loose-ends export and D1's tail committed, s305-D60 stamped enacted, pushed, CI read back",
      body=("s218-D7 filed report, commit seat (interim-report pattern). The interim copy rides the first commit; the final copy with both shas, "
            "the push range, the CI run and the red set by name rides the stamp commit."),
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
