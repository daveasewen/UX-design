"""#287 lane C — store rows for the I, W and C reports, through _state.py's module API only."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'knowledge'))
import _state

doc = _state.load()
ok, fails, notes = _state.check(doc)
print('PRE  check ok=%s fails=%d' % (ok, len(fails)))

ROWS = [
  dict(id='W-287i',
       title='#287 lane I — the two #286 sentences INSCRIBED (s287-D1, s287-D2); 620 -> 622',
       state='open', owner='dave', opened=287, project='apollo',
       closes_when=("Dave has read s287-D1 and s287-D2 as inscribed and either accepts both texts as "
                    "his, or names what either says wrongly"),
       home='notes/_subreports/2026-09-19-287-I-rulings-inscribed.md',
       links=['knowledge/_rulings.json', 'notes/_RULINGS.html', 'knowledge/_seam.py',
              'knowledge/_standing.md', 'notes/_lanes/287/DAVE-RULINGS-2026-09-19.md'],
       body=('Dave 2026-09-19: "inscribe" and "keep `sizes` and rebuild." Both #286 sentences are '
             'inscribed through _inscribe_ruling.py (--dry-run then --write), notes/_RULINGS.html '
             're-rendered in the same change, the stale DRAFT clause in _seam.py:44 amended and '
             '_standing.md\'s header brought onto the ruling. 620 -> 622 rulings, re-derived at the '
             'commit seam by json.load.')),
  dict(id='W-287w',
       title='#287 lane W — the 256,000 "wall" wording swept from ten live files; NO number moved',
       state='open', owner='dave', opened=287, project='apollo',
       closes_when=("Dave has read the amended wording in at least the runbook and the ruling text "
                    "and either accepts 'quality line / tolerance line' as the standing vocabulary "
                    "or names the words he wants instead"),
       home='notes/_subreports/2026-09-19-287-W-wall-wording-swept.md',
       links=['GOOD-MORNING.md', '_LIVE-STATE.md', '_CHAIN.md',
              'knowledge/_RUNBOOK-context-gauge.md', 'notes/_MEMENTO-DECISIONS.md',
              'dashboard/index.html', 'notes/_lanes/287/DAVE-RULINGS-2026-09-19.md'],
       body=('On Dave\'s "3. do it". BUDGET_HARD is still 256_000 and STOP_LINE_TK still 180_000 — '
             'only the word next to each figure changed. dashboard/index.html is GENERATED and was '
             'regenerated rather than hand-edited; lane W measured that a regen from the UNCHANGED '
             'HEAD _state.json alone moves 11,617 lines, so the committed dashboard was already '
             'stale against its own source before #287 touched it.')),
  dict(id='W-287c',
       title='#287 lane C — the three lanes committed and pushed, CI read back',
       state='open', owner='claude', opened=287, project='apollo',
       closes_when=("the conductor has read the sha, the script's literal push verdict line and the "
                    "CI read in the filed report, and the two inherited `gates` step failures are "
                    "either still inherited or owned by someone"),
       home='notes/_subreports/2026-09-19-287-C-commit-and-push.md',
       links=['notes/_lanes/287/C/', 'knowledge/_git_commit.sh',
              'notes/_subreports/2026-09-18-286-C2-commit-and-push.md'],
       body=('One commit through knowledge/_git_commit.sh with every path named (P5), --quiet, '
             'SESSION_N=287. The 4.3 MB notes/_lanes/287/K/before-_KG-EXPLORER.html was mv\'d to the '
             'gitignored _to_delete/287-K-before/ (the #284/#286 precedent — the sandbox delete-guard '
             'forbids rm); its 807 KB .gz IS committed as K\'s evidence. .gitignore was not edited. '
             'The dashboard regeneration is declared on the face of the commit message.')),
]

for r in ROWS:
    if any(i['id'] == r['id'] for i in doc['items']):
        print('%s already present — skipped' % r['id']); continue
    _state.add(doc, **r)
    print('ADDED %s' % r['id'])

ok, fails, notes = _state.check(doc)
print('POST check ok=%s fails=%d' % (ok, len(fails)))
for n in notes: print('  NOTE:', n[:160])
for f in fails: print('  FAIL:', str(f)[:200])
_state.save(doc)
print('SAVED')
