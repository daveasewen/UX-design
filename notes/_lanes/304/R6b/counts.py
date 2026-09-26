"""R6b: every count on the three decision pages, computed from the record (read-only). Writes counts.json.
Run from the repo root. Class assignment of Run 2's 109 UNCERTAIN rulings is EXPLICIT (hand-read from each
row's nearest_receipt, reasons below); the script asserts every one of the 109 lands in exactly one class."""
import json, os, collections
ROOT = os.getcwd(); L = lambda p: json.load(open(os.path.join(ROOT, p)))
out = {}
# ---------- the uncertain stamps ----------
U = L('notes/_lanes/304/R2/for_tuesday_uncertain.json')
unc = {u['id']: u for u in U['uncertain_rulings']}
CLASSES = [
 ('carried', 'Done, through a later ruling',
  ['s130-D4','s130-D5','s135-D2','s151-D1','s151-D2','s173-D1'],
  'Run 2 names the later ruling or commit that carried each; none has one enacting commit of its own.'),
 ('overtaken', 'Overtaken, or its window lapsed',
  ['s130-D6','s219-D6','s219-D7','s219-D9','s228-D5','s190-D2','s218-D3','s203-D2','s251-D13','s251-D15'],
  'A later ruling replaced each (named in the receipt), or it set a window that closed on 21 September.'),
 ('standing', 'A rule in force, with nothing to build',
  ['s186-D2','s203-D1','s212-D5','s212-D8','s214-D1','s214-D2','s224-D2','s244-D2','s251-D8','s254-D1','s265-D1','s265-D2','s267-D4','s294-D10'],
  'Run 2 reads each as a policy, posture, deferral, order of work, schedule or keep-as-is: no code was ever owed.'),
 ('part', 'Half built, by its own record',
  ['s131-D2','s136-D1','s143-D1','s172-D1','s174-D1','s177-D1','s273-D2'],
  'The ruling\'s own status or receipt says part is done and part is not.'),
 ('untraced', 'No trace of the build, or the record disagrees',
  ['s155-D1','s234-D4','s212-D1','s216-D1','s244-D1','s229-D3','s256-D1','s262-D5'],
  'Run 2 found no build receipt, a receipt that says "not built", or two reports that disagree.'),
]
assigned = collections.Counter(i for c in CLASSES for i in c[2])
dup = [i for i, n in assigned.items() if n > 1]; missing = [i for i in assigned if i not in unc]
assert not dup and not missing, (dup, missing)
rest = [i for i in unc if i not in assigned]
CLASSES.append(('intree', 'In the tree, but no commit names it', rest,
  'The tree carries the ruling (its id beside working code, in a governed file, or in its own record of being done), but no commit message claims the enactment, so the stamp rule (a named commit) cannot fire.'))
assert sum(len(c[2]) for c in CLASSES) == len(unc) == 109
out['stamps'] = {'total_uncertain': len(unc), 'classes': [{'key': k, 'name': n, 'n': len(ids), 'ids': ids, 'basis': b} for k, n, ids, b in CLASSES]}
nf = U['not_found_rulings']
out['stamps']['not_found'] = {'probe_verified': len(nf['probe_verified_not_enacted']), 'when_harvest': len(nf['s272_when_harvest_bloc']['ids']),
                              'no_id_receipt': len(nf['no_id_receipt'])}
out['stamps']['closes_left_open'] = len(U['closes_left_open'])
P = L('notes/_lanes/304/R2/ruled_not_built_probe.json')
out['stamps']['ruled_not_built'] = [{'id': r['id'], 'verdict': r['verdict'], 'probe': r['probe']} for r in P['rows']]
out['stamps']['overlap_uncertain_and_rnb'] = sorted(set(unc) & {r['id'] for r in P['rows']})
C = L('notes/_lanes/304/R2/counts.json'); out['stamps']['r2_counts'] = C
# ---------- rulings store now ----------
R = L('knowledge/_rulings.json')['rulings']
out['rulings'] = {'count': len(R), 'bare_ruled': sum(1 for r in R if r.get('status', '').strip() == 'ruled'),
                  'status_leads_enacted': sum(1 for r in R if r.get('status', '').strip().upper().startswith('ENACTED'))}
# ---------- the work store now + A2's eight ----------
S = L('knowledge/_state.json'); items = {i['id']: i for i in S['items']}
st = collections.Counter(i['state'] for i in S['items'])
out['store'] = {'items': len(items), 'states': dict(st), 'live_by_owner': dict(collections.Counter(i['owner'] for i in S['items'] if i['state'] == 'open'))}
D = L('notes/_lanes/304/A2/decision_unblocks.json')
dec = {}; u0 = set(); u1 = set()
for k, v in D.items():
    ids = [x if isinstance(x, str) else x.get('id') for x in v]
    live = [i for i in ids if items.get(i, {}).get('state') == 'open']
    dec[k] = {'a2': len(ids), 'live_now': len(live), 'closed_since': len(ids) - len(live)}
    u0 |= set(ids); u1 |= set(live)
out['a2'] = {'decisions': dec, 'union_a2': len(u0), 'union_live_now': len(u1)}
# carries
K = L('notes/_lanes/304/A2/carries_classified.json')
kc = collections.Counter(x['cls'] for x in K)
out['carries'] = {'total': len(K), 'by_class': dict(kc), 'substantive': kc.get('substantive', None)}
# boot ceiling as coded
g = open(os.path.join(ROOT, 'knowledge/_gauge_tokens.py')).read()
line = [l for l in g.splitlines() if l.startswith('BOOT_CEILING_TK')][0]
out['boot_ceiling_line'] = line.strip()
# ---------- CI ----------
V = L('notes/_lanes/304/R1/verdicts-before-after.json')
def fails(run): return sorted([int(k) for k, (v, n) in V[run].items() if v == 'FAIL'])
out['ci'] = {'before_fail': fails('before'), 'final_fail': fails('final_mutating_231c7ed0'),
             'final_counts': dict(collections.Counter(v for v, n in V['final_mutating_231c7ed0'].values())),
             'before_counts': dict(collections.Counter(v for v, n in V['before'].values())),
             'names': {k: n for k, (v, n) in V['final_mutating_231c7ed0'].items() if v == 'FAIL'}}
out['badge'] = L('notes/_lanes/304/R6b/badge_measure.json')
def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    c = [x/12.92 if x <= .03928 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0] + .7152*c[1] + .0722*c[2]
def cr(a, b='#ffffff'):
    la, lb = lum(a), lum(b); return round((max(la, lb)+.05)/(min(la, lb)+.05), 2)
FORKS = [('--status-positive', '#57a369', '#137f3c'), ('--status-negative', '#f3543e', '#da1a00'), ('--status-neutral', '#6893d3', '#1a1a1a')]
out['forks'] = [{'token': t, 'bar': b, 'bar_cr': cr(b), 'spark': s, 'spark_cr': cr(s)} for t, b, s in FORKS]
json.dump(out, open(os.path.join(ROOT, 'notes/_lanes/304/R6b/counts.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('badge',)}, indent=1)[:6000])
