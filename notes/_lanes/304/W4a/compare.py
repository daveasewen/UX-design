import json, os, sys
H = os.path.expanduser
SETS = [('pack', H('~/mnt/Projects--UX-design/notes/_lanes/304/W4b/runs')), ('head', H('~/w4a/runs-head')), ('after', H('~/w4a/runs-after'))]
runs = ['cold-v1013-r1','cold-v1013-r2','cold-v1013-r3','cold-cand-r1','cold-cand-r2','cold-cand-r3']
CL = ['dead','cut','collision','size','markers']; GC = ['G6','G7','G8','G11','G12']
out = {}; tot = {s: {c: 0 for c in CL + GC + ['views']} for s, _ in SETS}
print('%-14s %-5s %5s | %s | %s' % ('run','set','views',' '.join('%9s'%c for c in CL),' '.join('%4s'%g for g in GC)))
for r in runs:
    V = {}
    for s, d in SETS:
        j = json.load(open(os.path.join(d, r, 'views.json')))
        V[s] = {v['key']: v for v in j['views'] if v.get('kept')}
    common = sorted(set.intersection(*[set(V[s]) for s, _ in SETS]), key=lambda k: (k != 'entry', int(k[3:]) if k.startswith('nav') else -1))
    out[r] = {'views': common}
    for s, _ in SETS:
        a = {c: sum(V[s][k]['ink']['affected'][c] for k in common) for c in CL}
        g = {c: sum(V[s][k]['geometry_counts'].get(c, 0) for k in common) for c in GC}
        out[r][s] = {'affected': a, 'geometry': g}
        for c in CL: tot[s][c] += a[c]
        for c in GC: tot[s][c] += g[c]
        tot[s]['views'] += len(common)
        print('%-14s %-5s %5d | %s | %s' % (r, s, len(common), ' '.join('%9d'%a[c] for c in CL), ' '.join('%4d'%g[c] for c in GC)))
print()
for s, _ in SETS:
    t = tot[s]; n = t['views']
    print('%-5s views %d  ink/view %.2f  | %s | %s' % (s, n, sum(t[c] for c in CL)/n, ' '.join('%s %d'%(c,t[c]) for c in CL), ' '.join('%s %d'%(c,t[c]) for c in GC)))
out['_totals'] = tot
json.dump(out, open(H('~/w4a/compare.json'), 'w'), indent=1)
