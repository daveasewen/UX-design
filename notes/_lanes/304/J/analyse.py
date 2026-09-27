#!/usr/bin/env python3
"""304-J: score Jev's edge answers against the frozen hand labels. Writes results.json."""
import json, os, hashlib, statistics as st
from collections import defaultdict
here = os.path.dirname(os.path.abspath(__file__))
Ld = json.load(open(os.path.join(here, 'labels.json')))
blob = json.dumps(Ld['labels'], sort_keys=True, ensure_ascii=False).encode()
assert hashlib.sha256(blob).hexdigest() == Ld['frozen_sha256'], 'labels changed after freeze'
L = {x['eid']: x for x in Ld['labels']}
R = {}
for l in open(os.path.join(here, 'results-edges.jsonl')):
    r = json.loads(l); R[r['eid']] = r
C = {c['eid']: c for c in json.load(open(os.path.join(here, 'candidates.json')))}
rows = []
for eid in sorted(L):
    r = R[eid]; rows.append({'eid': eid, 'type': r['edge_type'], 'origin': r['origin'], 's': C[eid]['s'], 't': C[eid]['t'],
        'label': L[eid]['label'], 'firm': L[eid]['firmness'], 'p': r['p_true'], 'ms': r['latency_ms'], 'reason': L[eid]['reason']})
def conf(rs, th=0.5):
    tp = sum(1 for x in rs if x['p'] >= th and x['label']); fp = sum(1 for x in rs if x['p'] >= th and not x['label'])
    fn = sum(1 for x in rs if x['p'] < th and x['label']); tn = sum(1 for x in rs if x['p'] < th and not x['label'])
    # "flag" direction: Jev says FALSE (p<th) = a flag for Dave. precision/recall of flags against label FALSE.
    fprec = tn / (tn + fn) if tn + fn else None; frec = tn / (tn + fp) if tn + fp else None
    prec = tp / (tp + fp) if tp + fp else None; rec = tp / (tp + fn) if tp + fn else None
    acc = (tp + tn) / len(rs) if rs else None
    brier = st.mean((x['p'] - (1 if x['label'] else 0)) ** 2 for x in rs) if rs else None
    return dict(n=len(rs), tp=tp, fp=fp, fn=fn, tn=tn, accept_precision=prec, accept_recall=rec,
                flag_precision=fprec, flag_recall=frec, accuracy=acc, brier=brier)
def rnd(d): return {k: (round(v, 3) if isinstance(v, float) else v) for k, v in d.items()}
out = {'labels_sha256': Ld['frozen_sha256'], 'threshold': 0.5, 'overall': rnd(conf(rows)),
       'firm_only': rnd(conf([x for x in rows if x['firm'] == 'firm'])),
       'overall_th_0.35': rnd(conf(rows, 0.35)), 'overall_th_0.65': rnd(conf(rows, 0.65))}
by = defaultdict(list)
for x in rows: by[x['type']].append(x)
out['by_type'] = {t: dict(rnd(conf(v)), mean_p_true_edges=round(st.mean([x['p'] for x in v if x['label']]), 3) if any(x['label'] for x in v) else None,
                        mean_p_false_edges=round(st.mean([x['p'] for x in v if not x['label']]), 3) if any(not x['label'] for x in v) else None) for t, v in by.items()}
# calibration: bins of p
bins = [(0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.01)]
out['calibration'] = [{'bin': '%.1f-%.1f' % (a, min(b, 1)), 'n': len(v), 'mean_p': round(st.mean([x['p'] for x in v]), 3) if v else None,
                       'frac_true': round(sum(x['label'] for x in v) / len(v), 3) if v else None}
                      for a, b in bins for v in [[x for x in rows if a <= x['p'] < b]]]
ms = [x['ms'] for x in rows]
out['latency_ms'] = {'median': round(st.median(ms), 1), 'min': min(ms), 'max': max(ms), 'mean': round(st.mean(ms), 1)}
ut = [R[e].get('usage') or {} for e in R]
out['tokens'] = {'input': sum(u.get('input_tokens', 0) for u in ut), 'output': sum(u.get('output_tokens', 0) for u in ut)}
# auc (rank) — label-free of threshold
pos = [x['p'] for x in rows if x['label']]; neg = [x['p'] for x in rows if not x['label']]
out['auc'] = round(sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg)), 3)
out['disagreements'] = [x for x in rows if (x['p'] >= 0.5) != x['label']]
out['rows'] = rows
json.dump(out, open(os.path.join(here, 'results.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: out[k] for k in ['overall', 'firm_only', 'overall_th_0.35', 'overall_th_0.65', 'auc', 'latency_ms', 'tokens', 'calibration']}, indent=0))
for t, v in out['by_type'].items(): print(t, v)
for x in out['disagreements']: print('DIS', x['eid'], x['type'], x['origin'], x['label'], x['firm'], x['p'], x['s'], '->', x['t'])
