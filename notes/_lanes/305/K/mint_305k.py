# #305 K (cut seat, acting commit seat for the cut) - mint the doc row for K's report. Modelled on notes/_lanes/305/C1/mint_305c1.py.
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
r = dict(id='W-305k', home='notes/_subreports/2026-09-27-305-K-cut.md', owner='claude', condition='stated',
         links=['notes/_lanes/305/K/build_cut.sh', 'apollo-spider/build-designer-pack.sh', 'knowledge/_release/_gen_pack_manifest.py', 'notes/_lanes/305/K/renders/'],
         title="#305 K the cut seat - v1.0.14 rebuilt from wave one, the Gumdrop stamp stops rewriting three historical rulings, keyed to s305-D2, the real chain X -> Y1 -> Y2",
         body=("s218-D7 filed report. Rehearsal in a scratch clone: probe 57/57, manifest RATIFIED (s305-D2), --check GREEN (first since the Constitution ships), "
               "--release byte-identical to the dry run, frozen-release PASS after literal + seed, demo page 7/7 in 4 themes, pack's own gates 37 pass / 6 fail (v1.0.13 34 / 7). "
               "Then, as the conductor's commit seat for the cut: X (sweep + key + stamp fix), Y1 (manifest, probe, review page, the v1.0.14 zip), Y2 (frozen literal + ledger seed). No push: a cold verifier opens the real zip first."),
         closes_when="a cold verifier that built none of it has opened the real v1.0.14 zip and filed under notes/_subreports/, the three commits are pushed with CI read back, and s305-D2 is stamped enacted")
doc = st.load()
if r['id'] in {i['id'] for i in doc['items']}:
    print('exists', r['id'])
else:
    assert os.path.exists(r['home'])
    for l in r['links']: assert os.path.exists(l), l
    assert st.ID_RE.match(r['id'])
    st.add(doc, project='apollo', opened=305, state='open', **r); print('added', r['id'])
ok, fails, _ = st.check(doc); print('check ok', ok); assert ok, fails[:5]
st.save(doc); print('saved items', len(doc['items']))
