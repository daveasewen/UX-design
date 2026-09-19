"""#288 wrap — the store row for THIS seat's filed report, written through _state.py's module API
(never by hand-editing _state.json). `_gate_doc_rows.py` refuses a commit that stages a sub-report
with no row (s218-D7), and this wrap's own report is the last one owed.

⚠ THE ID IS `W-288ww`, NOT `W-288w2`: `_state.add`'s pattern
`^(?:W-[0-9]{1,3}[a-z]{0,2}|G[0-9]{1,2}[a-z]?)$` allows at most two trailing lowercase letters and
NO digit after them. #287 met that refusal at this same seat and PUBLISHED the pattern, so this wrap
paid nothing for it [[gate-must-quote-what-it-forbids]]."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'knowledge'))
import _state

doc = _state.load()
ok, fails, notes = _state.check(doc)
print('PRE  check ok=%s fails=%d items=%d' % (ok, len(fails), len(doc['items'])))
if any(i['id'] == 'W-288ww' for i in doc['items']):
    print('W-288ww already present — nothing written'); sys.exit(0)
_state.add(doc,
    id='W-288ww',
    title='#288 wrap — the delegated capture ritual for #288 to #289',
    state='open', owner='dave', opened=288, project='apollo',
    closes_when=("Dave has read _HANDOFF-139 and either ordered #289's first moves as it states them "
                 "(what the one-shot generates FROM and the #230 pass condition, the sloppiness class "
                 "and the test brief he writes himself, the deck structure that unblocks wave 2, and "
                 "which event Friday 2026-09-25 is) or re-ranked them"),
    home='notes/_subreports/2026-09-19-288-W2-wrap.md',
    links=['_HANDOFF-139-apollo-composes-and-the-sloppiness-class-is-named.md',
           '_DECISION-HISTORY/2026-09-19-288-apollo-composes-and-the-sloppiness-class-is-named.md',
           'notes/_lanes/288/W2/', 'notes/_lanes/288/WRAP-MEMORY-HOOK.md',
           'notes/_lanes/288/DAVE-RULINGS-2026-09-19.md', '_CARRIES.md'],
    body=("Every ritual step ran in order 1 - 1b - 2 - 2c - 2c(i) - 2d - 2e - 2f - 2g - 3 - 4 - 4b - 4c "
          "- 4d - 5 - 5b. NO ruling was inscribed and knowledge/_rulings.json stays at 622, verified by "
          "json.load with no s288- id, because he did not say inscribe today; all ten ruling-shaped "
          "things are carried as questions put. ZERO carries struck and the zero is a judgment: the "
          "s219-D3 arm being BUILT discharges half of a carry headline whose other half, Mono's 0 is "
          "doubted, stays true, so it is said in a new item instead. _CARRIES.md residual to #289 "
          "probes 572 with seventeen new. FILL 197,234 real across 33 turns against 180,585 declared, "
          "delta 16,649; boot 74,174 agreeing to the token, the third reading on the Browser-blocked "
          "setup. subs 1,004,095 (n=5) by the log's convention and 998,602 by _checkin.read_fill - two "
          "definitions, both published, the gap reconciling per lane. Six inherited gate fails carried "
          "in the #243 declared not-a-wrap form, the fourteenth wrap; #288 has no lane commit at all, "
          "so this wrap is the session's only commit."))
ok, fails, notes = _state.check(doc)
print('POST check ok=%s fails=%d items=%d' % (ok, len(fails), len(doc['items'])))
for f in fails: print('  FAIL:', f[:200])
assert ok, 'store check FAILED — nothing saved'
_state.save(doc)
print('SAVED W-288ww')
