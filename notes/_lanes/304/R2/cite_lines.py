#!/usr/bin/env python3
"""#304 Run 2b — file:line citations of each candidate row's documents (home + every notes/ path named in
closes_when/links), at HEAD 571d458c, with the session the citing line belongs to:
  - filename-dated artefacts (…/2026-09-02-239-…): the NNN in the name;
  - archive/ledger files (_GM-ARCHIVE.md, _LIVE-STATE-ARCHIVE.md, _CARRIES.md, GOOD-MORNING.md): the nearest
    '#NNN' at or above the line (the banner/heading the line sits under) — an approximation, stated as such.
READ-ONLY. Output notes/_lanes/304/R2/cite_lines.json."""
import json, re, os, subprocess, collections
S = {i['id']: i for i in json.load(open('knowledge/_state.json'))['items']}
cands = json.load(open('notes/_lanes/304/A2/autonomous_close_candidates.json'))
PATH_RE = re.compile(r'(?:notes|reviews|_DECISION-HISTORY)/[\w./-]+\.(?:md|html|json)')
rowdocs = {}
for r in cands:
    it = S[r['id']]
    ds = [it['home']] + [l for l in it['links'] if isinstance(l, str)] + PATH_RE.findall(it['closes_when'])
    ds = [d.split('#')[0].split(':')[0].rstrip('.,;)') for d in ds if d]
    rowdocs[r['id']] = list(dict.fromkeys(d for d in ds if re.search(r'\.(md|html|json)$', d) and '/' in d))
bases = sorted({os.path.basename(d) for v in rowdocs.values() for d in v})
open('/tmp/r2/bases2.txt', 'w').write('\n'.join(bases) + '\n')
g = subprocess.run(['git', '--no-optional-locks', 'grep', '-n', '-o', '-F', '-f', '/tmp/r2/bases2.txt', '571d458c', '--', '.',
                    ':(exclude)knowledge/_state.json', ':(exclude)knowledge/_memento-index.json', ':(exclude)notes/_lanes/300',
                    ':(exclude)notes/_lanes/286', ':(exclude)notes/_lanes/304', ':(exclude)dashboard'], capture_output=True, text=True).stdout
hits = collections.defaultdict(list)
for ln in g.splitlines():
    p = ln.split(':')
    if len(p) >= 4: hits[p[-1]].append((p[1], int(p[2])))
_cache = {}
def ctx_session(f, n):
    m = re.search(r'\d{4}-\d{2}-\d{2}-(\d{3})-', os.path.basename(f))
    if m: return int(m.group(1)), 'filename'
    m = re.search(r'_HANDOFF-(\d+)', f)
    if f not in _cache:
        try: _cache[f] = open(f, encoding='utf-8', errors='replace').read().splitlines()   # working tree == HEAD for these ledgers
        except Exception: _cache[f] = []
    L = _cache[f]
    for i in range(min(n - 1, len(L) - 1), max(-1, n - 400), -1):
        mm = re.findall(r'#(\d{3})\b', L[i][:200])
        if mm: return int(mm[0]), 'nearest-heading'
    return None, 'unknown'
out = {}
for rid, ds in rowdocs.items():
    rows = []
    for d in ds:
        b = os.path.basename(d)
        for f, n in hits.get(b, []):
            if f == d: continue
            s, how = ctx_session(f, n)
            rows.append({'doc': d, 'file': f, 'line': n, 'session': s, 'how': how})
    out[rid] = {'docs': {d: os.path.exists(d) for d in ds}, 'cites': rows}
json.dump(out, open('notes/_lanes/304/R2/cite_lines.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), 'rows;', sum(1 for v in out.values() if v['cites']), 'with ≥1 file:line citation')
