#!/usr/bin/env python3
"""#304 Run 2b — apply the CLOSE verdicts of close_plan.json through the store's own API
(`_state.load` → mutate → `_state.check` → `_state.save`; save() is byte-identical on a round-trip, proven
at the start of this run). Close = state open→done + a `closed_by` receipt: BY ADDITION, nothing removed.
  python3 close.py --dry-run | --write      (idempotent: a row already done is skipped)"""
import json, sys, datetime
sys.path.insert(0, 'knowledge')
import _state
write = '--write' in sys.argv
P = [p for p in json.load(open('notes/_lanes/304/R2/close_plan.json')) if p['verdict'] == 'CLOSE']
doc = _state.load(); by = {i['id']: i for i in doc['items']}
before = _state.counts(doc)
done = skip = 0; log = []
for p in P:
    it = by[p['id']]
    if it['state'] != 'open':
        skip += 1; continue
    assert it['owner'] == 'claude', p['id']
    rec = ' · '.join(f"{l['limb']}: {l['receipt']}" for l in p['limbs'] if l['state'] == 'RECEIPTED')
    dec = ' · '.join(f"{l['limb']} ({l['receipt']})" for l in p['limbs'] if l['state'] == 'DECLARED')
    alt = ' · '.join(l['limb'] for l in p['limbs'] if l['state'] == 'DAVE-ALT')
    it['state'] = 'done'
    it['closed_by'] = (f"#304 Run 2 (2026-09-26) — receipted close, BY ADDITION; each limb of closes_when checked at HEAD 571d458c. "
                       f"RECEIPTS: {rec}."
                       + (f" DECLARED, NOT PROVABLE FROM THE REPO: {dec}." if dec else '')
                       + (f" The Dave branch of this OR-condition was not used; the carry branch closes it ({alt})." if alt else '')
                       + " Record: notes/_lanes/304/R2/close_plan.json")
    done += 1; log.append({'id': p['id'], 'closed_by_chars': len(it['closed_by'])})
ok, fails, notes = _state.check(doc)
after = _state.counts(doc)
print(f"{'WRITE' if write else 'DRY-RUN'}: closed {done} · skipped (already closed) {skip} · check ok={ok} fails={len(fails)}")
print(' before', before['live'], before['by_state'], before['by_owner']); print(' after ', after['live'], after['by_state'], after['by_owner'])
for f in fails[:5]: print('  ⛔', f)
if write and ok and done:
    _state.save(doc)
    with open('notes/_lanes/304/R2/WRITES.log', 'a') as fh:
        for l in log: fh.write(json.dumps({'at': datetime.datetime.utcnow().isoformat() + 'Z', 'op': 'close', 'file': 'knowledge/_state.json', **l}) + '\n')
    print(' saved')
