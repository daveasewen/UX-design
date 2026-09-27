# #305 lane A follow-up — close W-305n4 through the store's own writer (state done + closed_by receipt; check() gates it).
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
before = os.path.getmtime(st.STORE)
doc = st.load()
it = [i for i in doc['items'] if i['id'] == 'W-305n4']
assert len(it) == 1 and it[0]['state'] == 'open', it
it = it[0]
it['state'] = 'done'
it['closed_by'] = ("#305 lane A: its close condition is met — the visuals page for sitting call 27 is filed at "
                   "notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html (lane B4) and Dave ruled call 27 from it: half A "
                   "\"yes\" saved 16:04 BST, half B \"yes\" saved 16:05 BST (export notes/_lanes/305/DAVE-RULINGS-2026-09-27-call-27.md), "
                   "inscribed as s305-D57.")
it['links'] = it['links'] + ['notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html', 'notes/_lanes/305/DAVE-RULINGS-2026-09-27-call-27.md']
for l in it['links']:
    assert os.path.exists(l), l
ok, fails, _ = st.check(doc)
assert ok, fails
if '--write' in sys.argv:
    assert os.path.getmtime(st.STORE) == before, 'store changed under us'
    st.save(doc); print('CLOSED W-305n4')
else:
    print('DRY ok')
