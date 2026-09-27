# #305 D1 - mint the doc row for D1's report. Modelled on notes/_lanes/305/C3/mint_305c3.py.
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
r = dict(id='W-305d1', home='notes/_subreports/2026-09-27-305-D1-ci-release-divergence.md', owner='claude', condition='stated',
      links=['knowledge/_release/_gen_pack_manifest.py', 'notes/_lanes/305/D1/'],
      title="#305 D1 the CI-only ship-list red named - git 2.55 prints %cI's zero offset as Z, so commit_date differed; the generator now formats the date itself; s305-D25 and D24 statuses corrected",
      body=("s218-D7 filed report. Reproduced with git 2.55.0 in a full clone (fresh d1c0a018 = CI's); one-line diff, commit_date. "
            "commit_date() reads --date=raw and formats with isoformat(): identical to the old %cI on all 1,650 commits, so the RATIFIED v1.0.14 manifest does not move."),
      closes_when="the fix is pushed and CI's release job and [145]/[146] read green")
doc = st.load()
if r['id'] in {i['id'] for i in doc['items']}:
    print('exists'); sys.exit(0)
assert os.path.exists(r['home'])
st.add(doc, project='apollo', opened=305, state='open', **r)
ok, fails, _ = st.check(doc); print('check ok', ok); assert ok, fails[:5]
st.save(doc); print('saved items', len(doc['items']))
