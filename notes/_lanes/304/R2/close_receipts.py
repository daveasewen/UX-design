#!/usr/bin/env python3
"""#304 Run 2b — gather receipts for A2's 93 close candidates (READ-ONLY). For each row:
  docs     : the row's own document(s) (home + notes/ links), existence at HEAD;
  events   : every '#N' session named in closes_when → the commits of that session (first/last) and any
             commit whose subject says it is the #N wrap;
  cites    : commits AFTER the row's opening session whose message names a doc by basename or the row id;
  filecites: tracked files at HEAD (not the doc itself, not the stores) that name the doc basename.
Writes notes/_lanes/304/R2/close_receipts.json."""
import json, re, os, subprocess, collections
S = {i['id']: i for i in json.load(open('knowledge/_state.json'))['items']}
cands = json.load(open('notes/_lanes/304/A2/autonomous_close_candidates.json'))
C = json.load(open('/tmp/r2/commits.json'))
def sess(subj):
    m = re.search(r'#(\d{2,3})\b', subj[:60]); return int(m.group(1)) if m else None
for c in C: c['sess'] = sess(c['subject'])
# one git-grep pass for every basename at once (a per-name pass took >2 min)
ALLB = set()
for r in cands:
    it = S[r['id']]
    for d in [it['home']] + [l for l in it['links'] if isinstance(l, str) and l.startswith('notes/')]:
        if d: ALLB.add(os.path.basename(d.split('#')[0].split(':')[0]))
open('/tmp/r2/bases.txt', 'w').write('\n'.join(sorted(b for b in ALLB if b)) + '\n')
g = subprocess.run(['git', '--no-optional-locks', 'grep', '-o', '-F', '-f', '/tmp/r2/bases.txt', '571d458c', '--', '.',
                    ':(exclude)knowledge/_state.json', ':(exclude)knowledge/_memento-index.json'], capture_output=True, text=True).stdout
FILEHITS = collections.defaultdict(set)
for ln in g.splitlines():
    p = ln.split(':')
    if len(p) >= 3: FILEHITS[p[-1]].add(p[1])
out = []
for r in cands:
    it = S[r['id']]; cw = it['closes_when']
    docs = [it['home']] + [l for l in it['links'] if isinstance(l, str) and l.startswith('notes/')]
    docs = [d.split('#')[0].split(':')[0] for d in docs if d]
    docs = list(dict.fromkeys(d for d in docs if d.endswith(('.md', '.html', '.json'))))
    exist = {d: os.path.exists(d) for d in docs}
    sessions = sorted({int(x) for x in re.findall(r'#(\d{3})\b', cw)})
    ev = {}
    for n in sessions:
        cs = [c for c in C if c['sess'] == n]
        wraps = [c for c in cs if re.search(r'\bwrap\b', c['subject'], re.I)]
        ev[n] = {'n_commits': len(cs), 'first': (cs[0]['sha'][:8], cs[0]['date'][:10], cs[0]['subject'][:120]) if cs else None,
                 'wrap_commits': [(c['sha'][:8], c['date'][:10], c['subject'][:140]) for c in wraps][:4]}
    bases = [os.path.basename(d) for d in docs]
    cites = []
    for c in C:
        if c['sess'] is None or c['sess'] < it['opened']: continue
        t = c['subject'] + '\n' + c['body']
        hit = [b for b in bases if b in t] + ([r['id']] if re.search(r'(?<![\w-])' + re.escape(r['id']) + r'(?![\w])', t) else [])
        if hit: cites.append((c['sha'][:8], c['date'][:10], c['sess'], hit[0], c['subject'][:100]))
    fc = sorted({f for b in bases for f in FILEHITS.get(b, ()) if not f.endswith(b)})
    out.append({'id': r['id'], 'opened': it['opened'], 'closes_when': cw, 'a2_receipts': r['receipts'], 'a2_verdict': r['verdict'],
                'docs': exist, 'sessions': ev, 'cites': cites[:12], 'n_cites': len(cites), 'filecites': fc[:15]})
json.dump(out, open('notes/_lanes/304/R2/close_receipts.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), 'rows;', sum(1 for o in out if o['n_cites']), 'with a later commit citation;', sum(1 for o in out if o['filecites']), 'with a file citation;',
      sum(1 for o in out if all(o['docs'].values())), 'with every doc on disk')
