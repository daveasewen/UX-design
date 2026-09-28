# #305 lane L - mint the doc row for L's filed report (modelled on notes/_lanes/305/C4/mint_305c4.py).
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/'
rows = [
 dict(id='W-305l', home=S + '2026-09-28-305-L-window-and-summary.md', owner='claude', condition='stated',
      links=['notes/_lanes/305/L/', 'notes/_lanes/305/L/DAVE-WORDS-2026-09-28-1141.md', 'notes/_lanes/305/W/SUMMARY-BULLETS.md',
             'knowledge/_gauge_tokens.py', 'knowledge/_RUNBOOK-capture-ritual.md'],
      title="#305 L post-wrap - s305-D62 (window 320,000 incl. the wrap, amber 320,000, hard 350,000, stop 300,000) and s305-D63 (the wrap summary as bullets: decisions, outputs, problems) inscribed and built; his boot line added to W-305w",
      body=("s218-D7 filed report, lane L (also the commit seat). Rulings 699 -> 701 through _inscribe_ruling.py; four constants moved in lockstep with both pins "
            "driven to a named refusal; step 5c in the capture ritual by addition; SUMMARY-BULLETS.md for #305; knowledge/_standing.md:19 left alone (Dave's ratified text)."),
      closes_when="the final copy of this report, carrying both shas, the push range and the CI verdict by job, is committed"),
]
doc = st.load()
have = {i['id'] for i in doc['items']}
for r in rows:
    assert os.path.exists(r['home']), r['home']
    for l in r['links']:
        assert os.path.exists(l), l
    assert st.ID_RE.match(r['id']), r['id']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=305, state='open', **r)
    print('added', r['id'])
ok, fails, _ = st.check(doc)
print('check ok', ok); assert ok, fails[:5]
st.save(doc); print('saved items', len(doc['items']))
