#!/usr/bin/env python3
"""#306 V — store writes, through _state.load -> mutate -> _state.check -> _state.save, BY ADDITION (U's method):
W-305wr gains the 16:58 BST paragraph (s306-D10 ruled; phases 1 and 2 scheduled; phase 2 built by lane V);
W-306v (this lane's report) is born closed under s305-D40.  python3 notes/_lanes/306/V/store_batch.py --dry-run | --write"""
import json, sys
sys.path.insert(0, 'knowledge')
import _state
WRITE = '--write' in sys.argv
VREP = 'notes/_subreports/2026-09-28-306-V-limits-and-phase2.md'
WORDS = 'notes/_lanes/306/V/DAVE-WORDS-2026-09-28-1658.md'
UREP = 'notes/_subreports/2026-09-28-306-U-rulings-and-bloat.md'
doc = _state.load(); by = {i['id']: i for i in doc['items']}
before = _state.counts(doc); ops = []
wr = by['W-305wr']
if '#306 V' not in (wr.get('body') or ''):
    wr['body'] = (wr.get('body') or '').rstrip() + '\n\n' + (
        '✎ #306 V (2026-09-28) — BY ADDITION: at 16:58 BST Dave answered the conductor\'s two-part question '
        '"go on both" (verbatim, both parts quoted at `' + WORDS + '`). Part 1 is a ruling: `s306-D10`, the eleven '
        'limits of `' + UREP + '` § 3 adopted into the design, each enacted by its phase (2: limit 8; 3: 2, 6, 7, 11; '
        '4: 9; 5: 10; 6: 1, 3, 4, 5). Part 2 is SCHEDULING, recorded here and nowhere in the store of rulings: '
        'phases 1 and 2 are built NOW, and tonight\'s #306 wrap is their first real proof. Phase 2 was built by '
        'lane V (`knowledge/_ci_readback.py`, the runbook\'s ★ THE ORDER AFTER THE COMMIT block, '
        '`_capture_gate.py::ci_owed_check`; report `' + VREP + '`); phase 1 goes to lane W after it. `s306-D7` '
        'stays `ruled` until the wrap runs in the new order. This row stays OPEN; `closes_when` is unchanged.')
    ops.append(('W-305wr', 'body+'))
NEW = [dict(id='W-306v',
    title="#306 V - s306-D10 inscribed (the eleven limits adopted, each by its phase) and phase 2 built: _ci_readback.py, one CI wait, the CI-owed arm",
    project='apollo', state='done', opened=306, owner='claude', condition='stated', home=VREP,
    links=['knowledge/_rulings.json', 'knowledge/_ci_readback.py', 'knowledge/_RUNBOOK-capture-ritual.md',
           'knowledge/_capture_gate.py', WORDS, 'notes/_lanes/306/V/', 'W-305wr', 'W-306u'],
    closes_when='the report is committed',
    closed_by=f'born closed (s305-D40): {VREP} filed at #306 — the file is the record.',
    body=("s218-D7 filed report. s306-D10 ruled (711 -> 712). Phase 2 of the wrap redesign built and wired, not yet "
          "proven: the permanent CI read-back (step 155 runs its selftest), the runbook's new order (one CI wait, "
          "his summary at the push, the 5b pushed without waiting, CI owed to the next opener), and a blocking "
          "wrap-gate arm for the handoff's CI owed line from _HANDOFF-157 on."))]
for n in NEW:
    if n['id'] in by: ops.append((n['id'], 'SKIP-exists')); continue
    doc['items'].append(n); by[n['id']] = n; ops.append((n['id'], 'added'))
ok, fails, notes = _state.check(doc)
after = _state.counts(doc)
print(('WRITE' if WRITE else 'DRY-RUN'), ops, 'check ok', ok, 'fails', len(fails))
for f in fails[:10]: print('  FAIL', f[:300])
print(' before', before['live'], before['by_state']); print(' after ', after['live'], after['by_state'])
json.dump({'ops': ops, 'before': before, 'after': after, 'check_ok': ok, 'fails': fails},
          open(f'notes/_lanes/306/V/store_batch.{"write" if WRITE else "dry"}.json', 'w'), indent=1, ensure_ascii=False)
if WRITE and ok:
    _state.save(doc); print(' saved')
