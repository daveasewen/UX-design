# #305 D1 - close W-305k (brief: close when CI's release job goes green) and D1's own row W-305d1.
import sys
sys.path.insert(0, 'knowledge')
import _state as st
doc = st.load()
by = {i['id']: i for i in doc['items']}
closes = {
 'W-305k': ("#305 D1 (2026-09-27): every limb of closes_when, receipted. (1) the cold verifier V2, which built none of it, opened the real "
            "apollo-spider/dist/Apollo-Spider-v1.0.14.zip and filed notes/_subreports/2026-09-27-305-V2-verifier-cut.md (its verdict, DO NOT SHIP to the "
            "audience because the shipped store carries the PoC rulings, s279-D1 against W-305n6, is Dave's and is NOT closed by this row); (2) the three "
            "commits X 0ef30746, Y1 02d679b3, Y2 d3b809a7 are on origin/master, and CI is read back GREEN at last: run 36347602064 (9c3f4663) and run "
            "36347858414 (fd607c74), release job SUCCESS with step 7 PASS a5b00c14 on git 2.55.0, gates SUCCESS (survey 69 pass 0 FAIL, step 6 all 154 "
            "asked, 0 gate red), render SUCCESS - after D1 fixed the git-2.55 commit_date divergence (9c3f4663); (3) s305-D2 reads enacted."),
 'W-305d1': ("#305 D1 (2026-09-27): the fix is pushed (e4ff4284..9c3f4663, then ..fd607c74) and CI reads green: run 36347602064 release SUCCESS "
             "(step 7 PASS a5b00c14), survey [145]/[146] pass, step 6 0 gate red of 154; run 36347858414 the same. Report "
             "notes/_subreports/2026-09-27-305-D1-ci-release-divergence.md."),
}
for k, why in closes.items():
    it = by[k]
    if it['state'] == 'done':
        print('already done', k); continue
    it['state'] = 'done'; it['closed_by'] = why
    print('closed', k)
ok, fails, _ = st.check(doc); print('check ok', ok); assert ok, fails[:5]
st.save(doc); print('saved items', len(doc['items']))
