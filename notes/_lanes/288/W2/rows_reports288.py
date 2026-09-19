"""#288 wrap — the three MISSING filed-report rows, through _state.py's module API.

⛔ `_gate_doc_rows.py` counts a document ROWED only when some item's `home` NAMES it — `home`
ONLY, never `links`. Lanes A, M and T each minted a row whose `home` is their DELIVERABLE
(the generator, the strand-map page, the review page) and put the filed report in `links`, so
all three reports were UNROWED and the doc-row gate refused the commit, correctly.

⛔ NOT repaired by editing the lanes' rows: a close condition is the lane's and the conductor's,
and re-homing someone else's row would silently move what that row is about. Three NEW rows are
minted instead, each homed on the report itself and pointing back at the lane's work row.
⛔ NOT DOC_ROW_ACK: that would ship three invisible documents to pass a gate (#287's lane C
made the same call and named it).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'knowledge'))
import _state

ROWS = [
 dict(id='W-288ar', work='W-288a', lane='A',
      title='#288 lane A filed report — the s219-D3 generation arm',
      home='notes/_subreports/2026-09-19-288-A-s219-d3-arm.md',
      closes_when=("Dave has read the lane A report and ruled on the outer gutter it leaves open "
                   "(token 0/24/24/0 versus role default 40/24/40/24) - the arm is built either way"),
      body=("Filed report for the s219-D3 generation arm build: knowledge/canon/gen_bento_role_vars.py, "
            "289 lines, first consumer of _bento_edit_rails.json. Gates green and a four-theme rendered "
            "proof. The arm does NOT settle Mono's 0 and the lane picked no winner.")),
 dict(id='W-288mr', work='W-288m', lane='M',
      title='#288 lane M filed report — the strand map and the path to Friday the 25th',
      home='notes/_subreports/2026-09-19-288-M-strand-map.md',
      closes_when=("Dave has read the strand map and said which event Friday 2026-09-25 is - the page "
                   "declares it NOT ESTABLISHED rather than guessing"),
      body=("Filed report for notes/_STRAND-MAP-2026-09-19.html: 13 sections, all 13 anchors resolving, "
            "41 cited paths all existing, self-contained, and the Friday date on a band of its own.")),
 dict(id='W-288tr', work='W-288t', lane='T',
      title='#288 lane T filed report — the bento template quality review',
      home='notes/_subreports/2026-09-19-288-T-template-quality.md',
      closes_when=("Dave has answered the six-question decision pack the review puts to him - the "
                   "inline-style rule, the template's status, the three $awaitingDave and a max-width ruling"),
      body=("Filed report for the template quality review: the drawn page is sound and the paperwork is "
            "not - zero invented markup and zero dangling vars, against four of the meta's five $status "
            "claims measured FALSE and the inline-style census re-run at 87 against #287's 88.")),
]

doc = _state.load()
ok, fails, _ = _state.check(doc)
print('PRE  check ok=%s fails=%d items=%d' % (ok, len(fails), len(doc['items'])))
written = 0
for r in ROWS:
    if any(i['id'] == r['id'] for i in doc['items']):
        print('  %s already present — skipped' % r['id']); continue
    _state.add(doc, id=r['id'], title=r['title'], state='open', owner='dave', opened=288,
               project='apollo', closes_when=r['closes_when'], home=r['home'],
               links=[r['work'], '_HANDOFF-139-apollo-composes-and-the-sloppiness-class-is-named.md',
                      'notes/_lanes/288/DAVE-RULINGS-2026-09-19.md'],
               body=r['body'])
    written += 1
    print('  minted %s -> %s' % (r['id'], r['home']))
ok, fails, _ = _state.check(doc)
print('POST check ok=%s fails=%d items=%d' % (ok, len(fails), len(doc['items'])))
for f in fails: print('  FAIL:', f[:200])
assert ok, 'store check FAILED — nothing saved'
if written:
    _state.save(doc); print('SAVED %d row(s)' % written)
