#!/usr/bin/env python3
"""Build notes/_KG-EXPLORER.html — the component knowledge graph as an interactive explorer.

Reads (never writes) knowledge/components/*.meta.json, _nodes-pattern.json, _nodes-context.json
and knowledge/_rulings.json; lays the graph out deterministically (Fruchterman-Reingold in 2D
and 3D, seeded, numpy) and bakes data + positions into knowledge/_kg_explorer.template.html.

  python3 knowledge/_build_kg_explorer.py            # → notes/_KG-EXPLORER.html
  python3 knowledge/_build_kg_explorer.py OUT.html

Born #266 (2026-09-10). Zero runtime dependencies in the page; numpy at build time.
Islands (disconnected components) are laid on a ring around the giant component; isolated
registered nodes (degree 0) are listed in the page as orphans, not hidden.
"""
import json, glob, os, sys, datetime, subprocess
VERSION = "1.1"  # 1.0 #266 sector dig + 3D · 1.1 #266 scrub line (history)
from collections import defaultdict
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'knowledge')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'notes', '_KG-EXPLORER.html')

def extract(K=K):
    nodes, edges = {}, []
    def add(id, label=None, **kw):
        n = nodes.setdefault(id, {'id': id, 'type': id.split(':')[0], 'label': label or id.split(':', 1)[1]})
        n.update({k: v for k, v in kw.items() if v})
    for f in ['_nodes-pattern.json', '_nodes-context.json']:
        fp = os.path.join(K, 'components', f)
        if not os.path.exists(fp): continue
        for n in json.load(open(fp)):
            add(n['id'], n.get('label'), sources=n.get('sources'), registered=True)
    rp = os.path.join(K, '_rulings.json')
    rul = {x['id']: x for x in json.load(open(rp)).get('rulings', []) if isinstance(x, dict)} if os.path.exists(rp) else {}
    for f in sorted(glob.glob(os.path.join(K, 'components', '*.meta.json'))):
        slug = os.path.basename(f)[:-10]
        if slug.startswith('EXAMPLE-'): continue  # the schema's worked example, not a component
        try: m = json.load(open(f))
        except Exception: continue
        if not isinstance(m, dict): continue
        cid = 'component:' + slug
        add(cid, m.get('name'), purpose=(m.get('purpose') or '')[:260], category=m.get('category'), interactive=m.get('interactive'))
        for et, lst in (m.get('edges') or {}).items():
            if et.startswith('$') or not isinstance(lst, list): continue
            for e in lst:
                if not isinstance(e, dict): continue
                ref = e.get('ref'); note = (e.get('$note') or e.get('note') or '')[:320]
                if not ref:
                    edges.append({'s': cid, 't': None, 'type': et, 'note': note}); continue
                if ref.startswith('ruling:'):
                    r = rul.get(ref.split(':', 1)[1], {})
                    ruled = r.get('ruled') if isinstance(r.get('ruled'), str) and len(r.get('ruled')) < 8 else None
                    add(ref, ref.split(':', 1)[1], text=(r.get('says') or '')[:280], date=r.get('date'), ruled=ruled)
                else:
                    add(ref)
                edges.append({'s': cid, 't': ref, 'type': et, 'note': note})
    for n in nodes.values():
        if n['type'] == 'snippet': n['label'] = n['label'].replace('.reference.html', '')
    return list(nodes.values()), edges

def fr(n, Es, dim, k, IT, R0, seed):
    rng = np.random.default_rng(seed)
    pos = rng.normal(size=(n, dim)); pos /= np.linalg.norm(pos, axis=1, keepdims=True); pos *= rng.uniform(0.2, 1, (n, 1)) * R0
    for it in range(IT):
        dd = pos[:, None, :] - pos[None, :, :]; dist = np.sqrt((dd ** 2).sum(-1)) + 1e-6
        fo = np.minimum(k * k / dist, k * 6); np.fill_diagonal(fo, 0)
        disp = ((fo / dist)[..., None] * dd).sum(1)
        if len(Es):
            ed = pos[Es[:, 0]] - pos[Es[:, 1]]; el = np.sqrt((ed ** 2).sum(-1)) + 1e-6
            att = (el * el / k)[:, None] * ed / el[:, None]
            np.add.at(disp, Es[:, 0], -att); np.add.at(disp, Es[:, 1], att)
        disp -= pos * 0.012
        t = max(1.0, k * 1.2 * (1 - it / IT)); l = np.sqrt((disp ** 2).sum(-1))[:, None] + 1e-6
        pos += disp / l * np.minimum(l, t)
    return pos - pos.mean(0)

def layout(nodes, edges, dim):
    ids = [n['id'] for n in nodes]; idx = {k: i for i, k in enumerate(ids)}; N = len(ids)
    E = np.array([[idx[e['s']], idx[e['t']]] for e in edges if e['t']])
    par = list(range(N))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in E: par[f(a)] = f(b)
    comp = defaultdict(list)
    for i in range(N): comp[f(i)].append(i)
    cs = sorted(comp.values(), key=len, reverse=True)
    def sub_edges(c):
        loc = {g: i for i, g in enumerate(c)}
        return np.array([[loc[a], loc[b]] for a, b in E if a in loc and b in loc]) if len(c) > 1 else np.zeros((0, 2), int)
    giant = cs[0]; P = fr(len(giant), sub_edges(giant), dim, 42.0 if dim == 2 else 60.0, 600 if dim == 2 else 350, 600, 266)
    R = np.sqrt((P ** 2).sum(-1)); Rmax = np.percentile(R, 99) * 1.05; P = np.clip(P, -Rmax, Rmax)
    pos = np.zeros((N, dim))
    for g, i in zip(giant, range(len(giant))): pos[g] = P[i]
    isl = [c for c in cs[1:] if len(c) > 1]; ring = Rmax + 140; a0 = 0; tot = sum(len(c) + 2 for c in isl) or 1
    for c in isl:
        span = 2 * np.pi * (len(c) + 2) / tot; a = a0 + span / 2; a0 += span
        sub = fr(len(c), sub_edges(c), dim, 30.0, 200, 30, len(c))
        centre = np.zeros(dim); centre[0] = np.cos(a) * ring; centre[1] = np.sin(a) * ring
        for g, i in zip(c, range(len(c))): pos[g] = sub[i] + centre
    orphans = [c[0] for c in cs[1:] if len(c) == 1]
    for j, g in enumerate(orphans):  # orphans: a short arc at the top, so they are seen
        a = -np.pi / 2 + (j - (len(orphans) - 1) / 2) * 0.12
        pos[g] = 0; pos[g][0] = np.cos(a) * (ring + 90); pos[g][1] = np.sin(a) * (ring + 90)
    pos /= np.abs(pos).max(); pos *= 1000
    return pos, cs, orphans

def with_history(nodes, edges):
    hp = os.path.join(K, '_kg_history.json')
    if not os.path.exists(hp): return nodes, edges, []
    hist = json.load(open(hp)); days = sorted(hist)
    byid = {n['id']: n for n in nodes}; ekey = lambda e: f"{e['s']}|{e['t']}|{e['type']}"
    ekeys = {ekey(e) for e in edges if e['t']}
    born_n, died_n, born_e, died_e = {}, {}, {}, {}
    for i, d in enumerate(days):
        for nid in hist[d]['nodes']: born_n.setdefault(nid, i); died_n[nid] = None
        for k in hist[d]['edges']: born_e.setdefault(k, i); died_e[k] = None
        # anything born earlier and absent today died today (first absence after presence)
        pn, pe = set(hist[d]['nodes']), set(hist[d]['edges'])
        for nid in list(born_n):
            if nid not in pn and died_n.get(nid) is None and born_n[nid] < i: died_n[nid] = i
        for k in list(born_e):
            if k not in pe and died_e.get(k) is None and born_e[k] < i: died_e[k] = i
    # dead nodes/edges join the graph so the scrub can show them
    for nid, b in born_n.items():
        if nid not in byid:
            n = {'id': nid, 'type': nid.split(':')[0], 'label': nid.split(':', 1)[1].replace('.reference.html', ''), 'dead': True}
            nodes.append(n); byid[nid] = n
    for k, b in born_e.items():
        if k not in ekeys:
            s_, t_, ty = k.split('|'); edges.append({'s': s_, 't': t_, 'type': ty, 'note': '', 'dead': True})
    for n in nodes:
        n['born'] = born_n.get(n['id'], len(days) - 1); n['died'] = died_n.get(n['id'])
    for e in edges:
        if e['t']: e['born'] = born_e.get(ekey(e), len(days) - 1); e['died'] = died_e.get(ekey(e))
    snaps = [{'date': d, 'commit': hist[d]['commit'], 'nodes': len(hist[d]['nodes']), 'edges': len(hist[d]['edges']), 'unresolved': hist[d]['unresolved']} for d in days]
    return nodes, edges, snaps

def main():
    nodes, edges = extract()
    nodes, edges, snaps = with_history(nodes, edges)
    p2, cs, orphans = layout(nodes, edges, 2)
    p3, _, _ = layout(nodes, edges, 3)
    deg = defaultdict(int)
    for e in edges:
        if e['t']: deg[e['s']] += 1; deg[e['t']] += 1
    for i, n in enumerate(nodes):
        n['x'], n['y'] = round(float(p2[i, 0]), 1), round(float(p2[i, 1]), 1)
        n['x3'], n['y3'], n['z3'] = (round(float(v), 1) for v in p3[i])
        n['deg'] = deg[n['id']]
    # islands + orphans are a LIVE finding: recompute on today's graph, dead edges excluded
    live_nodes = [n for n in nodes if not n.get('dead')]
    live_edges = [e for e in edges if e['t'] and not e.get('dead') and e.get('died') is None]
    _, cs_live, orph_live = layout(live_nodes, live_edges, 2) if live_nodes else (None, [], [])
    islands = [[live_nodes[i]['id'] for i in c] for c in cs_live[1:] if len(c) > 1]
    orphans = [live_nodes[i]['id'] for i in orph_live]
    sha = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    data = {'generated': datetime.date.today().isoformat(), 'version': VERSION, 'commit': sha, 'nodes': nodes, 'edges': edges,
            'islands': islands, 'orphans': orphans, 'snaps': snaps}
    tpl = open(os.path.join(K, '_kg_explorer.template.html')).read()
    html = tpl.replace('__KG__', json.dumps(data, separators=(',', ':')).replace('</script', '<\\/script')).replace('__DATE__', f"v{VERSION} · {data['generated']} · {sha}")
    open(OUT, 'w').write(html)
    print(f"wrote {OUT} · v{VERSION} · snaps {len(snaps)} · nodes {len(nodes)} · edges {len(edges)} · islands {len(islands)} · orphans {len(orphans)} · {os.path.getsize(OUT):,} B")

if __name__ == '__main__':
    main()
