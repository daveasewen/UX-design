"""#287 wrap — the store row for THIS seat's filed report, written through _state.py's module API
(never by hand-editing _state.json). `_gate_doc_rows.py` refuses a commit that stages a sub-report
with no row (s218-D7), and this wrap's own report is the last one owed."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'knowledge'))
import _state

doc = _state.load()
ok, fails, notes = _state.check(doc)
print('PRE  check ok=%s fails=%d items=%d' % (ok, len(fails), len(doc['items'])))
if any(i['id'] == 'W-287ww' for i in doc['items']):
    print('W-287ww already present — nothing written'); sys.exit(0)
_state.add(doc,
    id='W-287ww',
    title='#287 wrap — the delegated capture ritual for #287 → #288',
    state='open', owner='dave', opened=287, project='apollo',
    closes_when=("Dave has read _HANDOFF-138 and either ordered #288's first moves as it states them "
                 "(1 the strand map and the Friday-25th path, 2 the bento spacing review with the "
                 "s219-D3 arm built, 3 the template quality review, 4 the two carried decisions) or "
                 "re-ranked them"),
    home='notes/_subreports/2026-09-19-287-W2-wrap.md',
    links=['_HANDOFF-138-the-rulings-land-and-the-strand-map-is-ordered.md',
           '_DECISION-HISTORY/2026-09-19-287-the-rulings-land-and-the-strand-map-is-ordered.md',
           'notes/_lanes/287/W2/', 'notes/_lanes/287/WRAP-MEMORY-HOOK.md',
           'notes/_lanes/287/DAVE-RULINGS-2026-09-19.md', '_CARRIES.md'],
    body=("Every ritual step ran in order 1 - 1b - 2 - 2c - 2c(i) - 2d - 2e - 2f - 2g - 3 - 4 - 4b - 4c "
          "- 4d - 5 - 5b. knowledge/_rulings.json moved 620 to 622 on his 'inscribe', the first movement "
          "in seven sessions; four carries STRUCK with receipts and a fifth deliberately not struck "
          "because its headline stays true; _CARRIES.md residual to #288 probes 560. FILL 181,277 real "
          "across 24 turns against 180,375 declared, delta 902; boot 74,120 agreeing to the token, the "
          "second reading on #286's setup, so the -7,031 connector lever is a measured effect at n=2. "
          "subs 573,531 (n=5) by the log's convention and 568,179 by _checkin.read_fill - two "
          "definitions, both published, neither rewritten. Six inherited gate fails carried in the #243 "
          "declared not-a-wrap form, the thirteenth wrap; a seventh was born mid-session by a lane and "
          "healed by the remedy the gate named."))
ok, fails, notes = _state.check(doc)
print('POST check ok=%s fails=%d items=%d' % (ok, len(fails), len(doc['items'])))
for f in fails: print('  FAIL:', f[:200])
assert ok, 'store check FAILED — nothing saved'
_state.save(doc)
print('SAVED W-287ww')
