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

v1.2 adds TWO ADDITIVE FAMILIES on top of the component graph, each behind its own chip:
  governance — every ruling in knowledge/_rulings.json (not only the 14 a meta points at),
               plus the sessions they were ruled in, the artefacts they govern and the
               evidence they cite. `mentions` edges are DERIVED (regex over `says`) and are
               drawn dashed; a verb near the mention is recorded as `proposedType` only —
               the edge type stays `mentions` until Dave ratifies it.
  guidelines  — the WCAG success criteria in knowledge/compliance/rules/*.json, the
               guidelines/principles above them, EN 301 549, the HSBC policy and the
               axe-core rules that can check them.
The base component graph is laid out FIRST and UNTOUCHED (same seed, same node set, same
edges as v1.1), so with both new chips off the page is v1.1 to the pixel; the two new
families are laid out separately and parked either side of it.
"""
import json, glob, os, re, sys, datetime, subprocess
VERSION = "1.2"  # 1.0 #266 sector dig + 3D · 1.1 #266 scrub line (history) · 1.2 #266 governance + guidelines families
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

# ---------------------------------------------------------------- v1.2: governance + guidelines
MENTION_RX = re.compile(r's\d{2,3}-D\d+|ds-\d{3}|DV-D\d+|ADR-\d{4}(?:-A\d)?|T-D\d+|B-D\d+|GM-D\d+(?:-am)?')
VERB_STEMS = {'supersedes': 'supersed', 'retires': 'retir', 'narrows': 'narrow', 'refines': 'refin',
              'corrects': 'correct', 'enacts': 'enact', 'extends': 'extend', 'bounds': 'bound',
              'confirms': 'confirm', 'overrides': 'overrid'}
VERB_RX = {k: re.compile(r'\b' + v, re.I) for k, v in VERB_STEMS.items()}
PRINCIPLE = {'1': 'perceivable', '2': 'operable', '3': 'understandable', '4': 'robust'}
POLICY_ID = 'policy:hsbc-digital-accessibility-framework'
STANDARD_ID = 'standard:en-301-549'
SESSION_RX = re.compile(r'^#(\d+)')  # "#81-D1" → session #81; anything with no leading #N has no session


def rulings(K=K):
    fp = os.path.join(K, '_rulings.json')
    if not os.path.exists(fp): return []
    try: d = json.load(open(fp))
    except Exception: return []
    return [x for x in d.get('rulings', []) if isinstance(x, dict) and x.get('id')]


def ruling_ids(K=K):
    return sorted({r['id'] for r in rulings(K)})


def sc_rules(K=K):
    out = []
    for f in sorted(glob.glob(os.path.join(K, 'compliance', 'rules', '*.json'))):
        try: r = json.load(open(f))
        except Exception: continue
        if isinstance(r, dict) and r.get('sc'): out.append(r)
    return out


def sc_ids(K=K):
    return sorted({r['sc'] for r in sc_rules(K)})


def extract_extra(base_nodes, base_edges, K=K):
    """The two new families. Returns (nodes, edges, report). Never touches the base graph."""
    base = {n['id'] for n in base_nodes}
    comp_slugs = {n['id'].split(':', 1)[1] for n in base_nodes if n['type'] == 'component'}
    snip_ids = {n['id'] for n in base_nodes if n['type'] == 'snippet'}
    # applies_to names are matched against the meta's OWN `name` field, read from the meta files —
    # NOT against the node label (a node first created by another component's ref keeps the slug as
    # its label, so labels are not a reliable index) and NOT fuzzily. A miss is reported, not guessed.
    comp_by_name = {}
    for f in sorted(glob.glob(os.path.join(K, 'components', '*.meta.json'))):
        slug = os.path.basename(f)[:-10]
        if slug.startswith('EXAMPLE-') or ('component:' + slug) not in base: continue
        try: m = json.load(open(f))
        except Exception: continue
        if isinstance(m, dict) and m.get('name'): comp_by_name.setdefault(m['name'], 'component:' + slug)
    snip_to_comp = {}
    for e in base_edges:
        if e.get('t') and e['t'].startswith('snippet:') and e['s'].startswith('component:'):
            snip_to_comp.setdefault(e['t'], e['s'])

    nodes, edges = {}, []
    rep = defaultdict(int); rep['unmatched_applies_to'] = []; rep['proposed'] = defaultdict(int)

    def add(id, label, fam, **kw):
        n = nodes.setdefault(id, {'id': id, 'type': id.split(':')[0], 'label': label, 'fam': fam})
        n.update({k: v for k, v in kw.items() if v not in (None, '', [], {})})
        return id

    def link(s, t, ty, fam, **kw):
        e = {'s': s, 't': t, 'type': ty, 'note': kw.pop('note', ''), 'fam': fam, 'authored': kw.pop('authored', True)}
        e.update({k: v for k, v in kw.items() if v not in (None, '', [], {})})
        edges.append(e); return e

    def gov_target(entry):
        m = re.match(r'^knowledge/components/(.+)\.meta\.json$', entry.strip())
        if m and m.group(1) in comp_slugs:
            rep['governs_to_component'] += 1; return 'component:' + m.group(1)
        m = re.search(r'([^/\s]+\.reference\.html)$', entry.strip())
        if m:
            sid = 'snippet:' + m.group(1)
            if sid in snip_to_comp:
                rep['governs_to_component'] += 1; return snip_to_comp[sid]
            if sid in snip_ids:
                rep['governs_to_component'] += 1; return sid
        rep['governs_to_artefact'] += 1
        return add('artefact:' + entry.strip(), entry.strip(), 'governance')

    # ---- A. governance
    R = rulings(K)
    rid_set = {r['id'] for r in R}
    for r in R:
        rid = 'ruling:' + r['id']
        if rid in base:  # already a base node (a meta points at it) — leave it in the base family
            nodes.pop(rid, None)
        else:
            add(rid, r['id'], 'governance', text=(r.get('says') or '')[:280], date=r.get('date'),
                ruled=r.get('ruled'), by=r.get('by'), status=(r.get('status') or '')[:180])
        for g in (r.get('governs') or []):
            if isinstance(g, str) and g.strip(): link(rid, gov_target(g), 'governs', 'governance', note=g.strip()[:200])
        for ev in (r.get('evidence') or []):
            if not (isinstance(ev, str) and ev.strip()): continue
            eid = add('evidence:' + ev.strip(), ev.strip()[:110], 'governance', full=ev.strip()[:300])
            link(rid, eid, 'evidencedBy', 'governance')
        m = SESSION_RX.match(str(r.get('ruled') or ''))
        if m:
            sid = add('session:' + m.group(1), '#' + m.group(1), 'governance')
            link(rid, sid, 'ruledIn', 'governance', note=str(r['ruled'])[:60])
    # mentions — DERIVED, dashed, unratified
    seen = set()
    for r in R:
        says = r.get('says') or ''
        for m in MENTION_RX.finditer(says):
            t = m.group(0)
            if t not in rid_set or t == r['id'] or (r['id'], t) in seen: continue
            seen.add((r['id'], t))
            win = says[max(0, m.start() - 80):m.end() + 80]
            proposed = next((k for k, rx in VERB_RX.items() if rx.search(win)), None)
            if proposed: rep['proposed'][proposed] += 1
            link('ruling:' + r['id'], 'ruling:' + t, 'mentions', 'governance', authored=False,
                 derived=True, proposedType=proposed, at=m.start(),
                 note=(('proposed ' + proposed + ' · ') if proposed else '') + win.strip()[:200])
            rep['mentions'] += 1

    # ---- B. guidelines
    gi = {}
    gip = os.path.join(K, 'compliance', 'graph-index.json')
    if os.path.exists(gip):
        try: gi = json.load(open(gip))
        except Exception: gi = {}
    verif = ((gi.get('verification') or {}).get('by_sc') or {})
    for r in sc_rules(K):
        sc = r['sc']; g = '.'.join(sc.split('.')[:2]); p = PRINCIPLE.get(sc.split('.')[0], 'perceivable')
        src = r.get('sources') or {}; chk = r.get('check') or {}
        axe = [a for a in (r.get('external_automatable_refs') or []) if isinstance(a, dict) and a.get('rule_id')]
        v = verif.get(sc)
        scid = add('sc:' + sc, f"{sc} {r.get('title', '')}".strip(), 'guidelines',
                   level=r.get('level'), severity=r.get('severity'), checkType=chk.get('type'),
                   checkDesc=(chk.get('description') or '')[:260], threshold=chk.get('threshold'),
                   verified=bool(v), axeCount=len(axe), enClause=src.get('en301549_clause'),
                   policy=(src.get('internal_policy_ref') or '')[:300], wcagUrl=src.get('wcag_url'),
                   versions=r.get('wcag_versions'))
        gid = add('guideline:' + g, g, 'guidelines')
        pid = add('principle:' + p, p, 'guidelines')
        link(scid, gid, 'under', 'guidelines'); link(gid, pid, 'under', 'guidelines')
        for name in (r.get('applies_to') or []):
            cid = comp_by_name.get(name)
            if cid: link(scid, cid, 'appliesTo', 'guidelines'); rep['applies_to_matched'] += 1
            else:
                rep['applies_to_unmatched'] += 1
                if name not in rep['unmatched_applies_to']: rep['unmatched_applies_to'].append(name)
        if src.get('en301549_clause'):
            add(STANDARD_ID, 'EN 301 549', 'guidelines')
            link(scid, STANDARD_ID, 'enClause', 'guidelines', note=src['en301549_clause'])
        if src.get('internal_policy_ref'):
            add(POLICY_ID, 'HSBC digital accessibility framework', 'guidelines')
            link(scid, POLICY_ID, 'boundBy', 'guidelines', note=src['internal_policy_ref'][:200])
        for a in axe:
            aid = add('axe:' + a['rule_id'], a['rule_id'], 'guidelines', url=a.get('url'),
                      version=a.get('source_version'), text=(a.get('description') or '')[:220])
            link(scid, aid, 'checkedBy', 'guidelines', note=(a.get('description') or '')[:200])
        if v and v.get('script'):
            for part in [x.strip() for x in str(v['script']).split('+') if x.strip()]:
                aid = 'artefact:' + part
                if aid not in nodes: add(aid, part, 'guidelines')
                link(scid, aid, 'verifiedBy', 'guidelines',
                     note=f"{v.get('mechanism', '')[:180]}".strip() or v.get('artifact', ''))
                rep['verifiedBy'] += 1

    # keep only edges whose two ends exist somewhere (base or new)
    known = base | set(nodes)
    edges = [e for e in edges if e['s'] in known and e['t'] in known]
    rep['nodes'] = len(nodes); rep['edges'] = len(edges)
    rep['unmatched_applies_to'] = sorted(rep['unmatched_applies_to'])
    rep['proposed'] = dict(rep['proposed'])
    return list(nodes.values()), edges, dict(rep)


def date_extra(xnodes, xedges, hist, ndays):
    """born/died for the new families. Rulings and SCs get REAL born dates from the history
    snapshots; every other new node (session/artefact/evidence/guideline/principle/policy/
    standard/axe) inherits the earliest born of the ruling or SC that introduced it, and every
    new EDGE takes born = the later of its two endpoints. That is an APPROXIMATION: the day a
    ruling first names an artefact is not separately recorded, so the edge is dated by its ends."""
    days = sorted(hist)
    born, died = {}, {}
    for key, pref in (('rulings', 'ruling:'), ('scs', 'sc:')):
        for i, d in enumerate(days):
            present = set(hist[d].get(key) or [])
            for x in present:
                born.setdefault(pref + x, i); died[pref + x] = None
            for k in list(born):
                if not k.startswith(pref): continue
                if k.split(':', 1)[1] not in present and died.get(k) is None and born[k] < i: died[k] = i
    byid = {n['id']: n for n in xnodes}
    for n in xnodes:
        if n['id'] in born: n['born'] = born[n['id']]; n['died'] = died.get(n['id'])
    # inherit: seed from ruling/sc ends of each edge
    for _ in range(2):
        for e in xedges:
            for a, b in ((e['s'], e['t']), (e['t'], e['s'])):
                na, nb = byid.get(a), byid.get(b)
                if nb is None or 'born' not in (na or {}): continue
                if 'born' not in nb or nb['born'] > na['born']: nb['born'] = na['born']; nb.setdefault('died', None)
    for n in xnodes:
        n.setdefault('born', max(0, ndays - 1)); n.setdefault('died', None)
    def bo(i):
        n = byid.get(i)
        return (n['born'], n.get('died')) if n else (0, None)
    for e in xedges:
        bs, ds = bo(e['s']); bt, dt = bo(e['t'])
        e['born'] = max(bs, bt)
        dd = [x for x in (ds, dt) if x is not None]
        e['died'] = min(dd) if dd else None


def place_extra(xnodes, xedges, base_extent):
    """Lay the two new families out on their own and park them either side of the base graph,
    so no base position moves. Governance left, guidelines right."""
    if not xnodes: return
    idx = {n['id']: i for i, n in enumerate(xnodes)}
    for fam, cx in (('governance', -1.0), ('guidelines', 1.0)):
        grp = [n for n in xnodes if n['fam'] == fam]
        if not grp: continue
        loc = {n['id']: i for i, n in enumerate(grp)}
        E = np.array([[loc[e['s']], loc[e['t']]] for e in xedges if e['s'] in loc and e['t'] in loc] or [[0, 0]])
        for dim in (2, 3):
            P = fr(len(grp), E, dim, 34.0 if dim == 2 else 46.0, 240 if dim == 2 else 160, 400, 1266 + dim)
            mx = np.abs(P).max() or 1
            P = P / mx * (base_extent * 0.82)
            for n, i in zip(grp, range(len(grp))):
                v = [round(float(P[i, j]), 1) for j in range(dim)]
                if dim == 2:
                    n['x'] = v[0] + cx * base_extent * 2.05; n['y'] = v[1]
                else:
                    n['x3'] = v[0] + cx * base_extent * 2.05; n['y3'] = v[1]; n['z3'] = v[2]
    del idx


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
    base_nodes, base_edges = list(nodes), list(edges)
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
    # ---- v1.2: the two additive families, laid out AFTER (and beside) the untouched base graph
    xnodes, xedges, rep = extract_extra(base_nodes, base_edges)
    hp = os.path.join(K, '_kg_history.json')
    hist = json.load(open(hp)) if os.path.exists(hp) else {}
    date_extra(xnodes, xedges, hist, len(snaps) or 1)
    place_extra(xnodes, xedges, 1000.0)
    xdeg = defaultdict(int)
    for e in xedges: xdeg[e['s']] += 1; xdeg[e['t']] += 1
    for n in xnodes: n['deg'] = xdeg[n['id']]
    nodes = nodes + xnodes; edges = edges + xedges
    sha = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    data = {'generated': datetime.date.today().isoformat(), 'version': VERSION, 'commit': sha, 'nodes': nodes, 'edges': edges,
            'islands': islands, 'orphans': orphans, 'snaps': snaps,
            'extra': {'nodes': len(xnodes), 'edges': len(xedges),
                      'rulings': sum(1 for n in nodes if n['type'] == 'ruling'),
                      'sc': sum(1 for n in nodes if n['type'] == 'sc'),
                      'derived': sum(1 for e in xedges if e.get('derived')),
                      'proposed': rep.get('proposed', {})}}
    tpl = open(os.path.join(K, '_kg_explorer.template.html')).read()
    html = tpl.replace('__KG__', json.dumps(data, separators=(',', ':')).replace('</script', '<\\/script')).replace('__DATE__', f"v{VERSION} · {data['generated']} · {sha}")
    open(OUT, 'w').write(html)
    print(f"wrote {OUT} · v{VERSION} · snaps {len(snaps)} · nodes {len(nodes)} · edges {len(edges)} · islands {len(islands)} · orphans {len(orphans)} · {os.path.getsize(OUT):,} B")
    lb = [n for n in base_nodes if not n.get('dead') and n.get('died') is None]
    print(f"  base (live): {len(lb)} nodes / {len([e for e in base_edges if e['t'] and not e.get('dead') and e.get('died') is None])} relations"
          f" / {sum(1 for n in lb if n['type'] == 'component')} components")
    print(f"  extra: {rep['nodes']} nodes / {rep['edges']} edges · mentions {rep.get('mentions', 0)} derived"
          f" · governs→component {rep.get('governs_to_component', 0)} / →artefact {rep.get('governs_to_artefact', 0)}"
          f" · appliesTo matched {rep.get('applies_to_matched', 0)} unmatched {rep.get('applies_to_unmatched', 0)}"
          f" · verifiedBy {rep.get('verifiedBy', 0)}")
    print(f"  proposedType: {rep.get('proposed', {})}")
    if rep.get('unmatched_applies_to'): print(f"  UNMATCHED applies_to names: {rep['unmatched_applies_to']}")

if __name__ == '__main__':
    main()
