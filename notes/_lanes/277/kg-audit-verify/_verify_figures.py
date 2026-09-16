#!/usr/bin/env python3
"""_verify_figures.py — lane A2V: re-derive every figure on the A2 decisions page, independently.
Imports _build_kg_explorer.extract()/extract_extra() only. Never main(). Never gen_kg_edges.py. Never _build_all.py.
    python3 notes/_lanes/277/kg-audit-verify/_verify_figures.py
"""
import sys, os, json, glob, re, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
K = os.path.join(ROOT, 'knowledge')
sys.path.insert(0, K)
import _build_kg_explorer as X

bn, be = X.extract()
xn, xe, rep = X.extract_extra(bn, be)
nodes = bn + xn
edges = be + xe
live = [e for e in edges if e.get('t')]
null = [e for e in edges if not e.get('t')]
out = {}
out['totals'] = dict(nodes=len(nodes), edges_live=len(live), edges_null=len(null),
                     types=len({e['type'] for e in live}), kinds=len({n['type'] for n in nodes}))
kind = {n['id']: n['type'] for n in nodes}

# ---- 432/593 ruling scope, from the LIVE governs edges (target kind), not from re-parsing governs[]
gov = collections.defaultdict(set)
for e in live:
    if e['type'] == 'governs':
        gov[e['s']].add(kind.get(e['t'], '?'))
rul_ids = [n['id'] for n in nodes if n['type'] == 'ruling']
sc = collections.Counter()
for r in rul_ids:
    ks = gov.get(r, set())
    design = {'component', 'snippet'} & ks
    system = ks - {'component', 'snippet'}
    sc['none' if not ks else 'design' if design and not system else 'system' if system and not design else 'both'] += 1
out['ruling_scope_by_governs_target'] = dict(sc, total=len(rul_ids))
# alt: what counts as "design" if snippet targets are system? (gov_target maps .reference.html to component when possible)
out['governs_target_kinds'] = dict(collections.Counter(kind.get(e['t']) for e in live if e['type'] == 'governs'))

# ---- ruledIn / session-in-id
ri = {e['s'] for e in live if e['type'] == 'ruledIn'}
out['ruledIn'] = dict(with_edge=len(ri), without=len(rul_ids) - len(ri),
                      session_in_id=sum(1 for r in rul_ids if r not in ri and re.match(r'^ruling:s\d+-D\d+', r)))

# ---- rules: 470, 34 files, 59 BLOCKING, obeys reach
idx = json.load(open(os.path.join(K, 'guidelines', '_rules-index.json')))['rules']
rn = json.load(open(os.path.join(K, '_rule_nodes.json')))
rfile = {n['id']: n.get('file') for n in rn['nodes']}
by_file = collections.Counter(r['file'] for r in idx)
obeys = [e for e in live if e['type'] == 'obeys']
obeys_rule = [e for e in obeys if e['t'].startswith('rule:')]
obeys_ux = [e for e in obeys if e['t'].startswith('ux:')]
obeyed = {e['t'] for e in obeys_rule}
blocking = {'rule:' + r['id'] for r in idx if r['destiny'] == 'BLOCKING'}
# other in-edges to a rule from a component: appliesTo? no, that is sc->component. Any component->rule edge type?
comp_to_rule_types = collections.Counter(e['type'] for e in live if e['s'].startswith('component:') and e['t'].startswith('rule:'))
rule_in_types = collections.Counter(e['type'] for e in live if e['t'].startswith('rule:'))
rule_out_types = collections.Counter(e['type'] for e in live if e['s'].startswith('rule:'))
files_reached = sorted({rfile.get(t) for t in obeyed} - {None})
out['rules'] = dict(total=len(idx), files=len(by_file), blocking=len(blocking),
                    blocking_obeyed=len(blocking & obeyed), blocking_unbound=len(blocking - obeyed),
                    obeys_edges_total=len(obeys), obeys_to_rule=len(obeys_rule), obeys_to_ux=len(obeys_ux),
                    distinct_rules_obeyed=len(obeyed), rules_no_component=len(idx) - len(obeyed),
                    metas_with_obeys=len({e['s'] for e in obeys_rule}),
                    files_reached=files_reached, files_reached_n=len(files_reached), files_unreached_n=len(by_file) - len(files_reached),
                    rules_in_unreached=sum(n for f, n in by_file.items() if f not in files_reached),
                    comp_to_rule_types=dict(comp_to_rule_types), rule_in_types=dict(rule_in_types), rule_out_types=dict(rule_out_types),
                    facet_sums=dict(copy=by_file['copywriting.md'], tone=by_file['tone-of-voice.md'],
                                    colour=by_file['colour-standards-2026.md'] + by_file['colour-usage.md'],
                                    type=by_file['typography-standards-2026.md'] + by_file['typography-usage.md'],
                                    icons=by_file['icons.md'] + by_file['pictograms.md'], neuro=by_file['neurodiversity.md']))
# does a rule reach a component by ANY path of length<=2 other than obeys? rule -cites-> sc -appliesTo-> component
cites = collections.defaultdict(set)
for e in live:
    if e['type'] == 'cites' and e['s'].startswith('rule:'): cites[e['s']].add(e['t'])
app = collections.defaultdict(set)
for e in live:
    if e['type'] == 'appliesTo': app[e['s']].add(e['t'])
reach2 = {r for r in rfile if any(app.get(s) for s in cites.get(r, ()))}
out['rules']['rules_reaching_component_via_cites_appliesTo'] = len(reach2)
out['rules']['blocking_reaching_via_cites_appliesTo'] = len(blocking & reach2)
out['rules']['blocking_unbound_even_counting_cites_path'] = len(blocking - obeyed - reach2)

# ---- accessibility holdings 55 / 52 / 20 / 0 cross links
sc_nodes = [n for n in nodes if n['type'] == 'sc']
acc_rules = [i for i, f in rfile.items() if f and f.startswith('accessibility-')]
un = json.load(open(os.path.join(K, '_ux_principle_nodes.json')))
std = ('fam-wcag22', 'fam-coga', 'fam-en301549', 'fam-eaa', 'fam-aria-apg')
ux_std = [n['id'] for n in un['nodes'] if n['type'] == 'ux' and n.get('family') in std]
ux_std_set = set(ux_std)
cross = [e for e in live if (e['s'] in ux_std_set and kind.get(e['t']) in ('sc', 'guideline', 'principle', 'rule')) or
         (e['t'] in ux_std_set and kind.get(e['s']) in ('sc', 'guideline', 'principle', 'rule'))]
cross_rule_sc = sum(1 for e in live if e['s'] in acc_rules and kind.get(e['t']) == 'sc')
out['a11y'] = dict(sc=len(sc_nodes), acc_rules=len(acc_rules), ux_std=len(ux_std), ux_std_to_sc_or_rule=len(cross),
                   acc_rule_to_sc_cites=cross_rule_sc, families=dict(collections.Counter(n.get('family') for n in un['nodes'] if n['id'] in ux_std_set)))

# ---- consumer census: 12 types / 3125 edges / 47%
tc = collections.Counter(e['type'] for e in live)
nc12 = ['evidencedBy', 'appliesTo', 'definedIn', 'ruledIn', 'checkedBy', 'hasParty', 'enforcedBy', 'boundBy', 'enClause', 'flaggedBy', 'tensionWith', 'verifiedBy']
out['consumers'] = dict(nc12_edges=sum(tc[t] for t in nc12), pct=round(100 * sum(tc[t] for t in nc12) / len(live), 1),
                        per_type={t: tc[t] for t in nc12}, governs=tc['governs'], governedBy=tc['governedBy'], mentions=tc['mentions'], cites=tc['cites'])

# ---- ux orphans 99 / A-grade
deg = collections.Counter()
for e in live: deg[e['s']] += 1; deg[e['t']] += 1
ux = [n for n in nodes if n['type'] == 'ux']
out['ux'] = dict(total=len(ux), orphans=sum(1 for n in ux if deg[n['id']] == 0), polarities=sum(1 for n in nodes if n['type'] == 'polarity'),
                 a_grade_deg={n['id']: deg[n['id']] for n in un['nodes'] if n.get('grade') == 'A'})
out['orphans_all'] = dict(collections.Counter(n['type'] for n in nodes if deg[n['id']] == 0))
out['pattern_deg1'] = sum(1 for n in nodes if n['type'] == 'pattern' and deg[n['id']] == 1)
out['context_deg1'] = sum(1 for n in nodes if n['type'] == 'context' and deg[n['id']] == 1)

# ---- tokens: 135/137 metas, 316 refs, 10 files, top groups
metas = {}
for f in sorted(glob.glob(os.path.join(K, 'components', '*.meta.json'))):
    s = os.path.basename(f)[:-10]
    if s.startswith('EXAMPLE'): continue
    metas[s] = json.load(open(f))
tokmetas = [s for s, m in metas.items() if m.get('tokens')]
refs, groups = set(), collections.Counter()
shape = collections.Counter(type(m.get('tokens')).__name__ for m in metas.values())
for s in tokmetas:
    t = metas[s]['tokens']
    for ref in set(re.findall(r"\b([a-z][a-z0-9-]*(?:/[a-z0-9-]+)+)\b", json.dumps(t))):
        refs.add(ref); groups[ref.split('/')[0]] += 1
# alt: tokens as the explorer would see them — the first path-shaped token in each string value
first_tok = collections.Counter()
for s in tokmetas:
    t = metas[s]['tokens']
    vals = t.values() if isinstance(t, dict) else t
    for v in vals:
        if isinstance(v, str):
            m = re.match(r'\s*([a-z][a-z0-9-]*(?:/[a-z0-9-]+)+)', v)
            if m: first_tok[m.group(1).split('/')[0]] += 1
allfiles = sorted(os.path.basename(f) for f in glob.glob(os.path.join(K, 'tokens', '*.json')))
tf = [f for f in allfiles if not f.startswith(('_', 'EXAMPLE')) and '-pre-s141' not in f]
out['tokens'] = dict(metas=len(metas), with_tokens=len(tokmetas), tokens_shape=dict(shape), distinct_refs=len(refs), groups=len(groups),
                     top12=dict(groups.most_common(12)), first_tok_top12=dict(first_tok.most_common(12)),
                     token_files_all=allfiles, token_files_live=tf, token_files_live_n=len(tf))
# leaf count (s269-D3 said 932?)
leaf = 0
def walk(o):
    global leaf
    if isinstance(o, dict):
        if '$value' in o or 'value' in o: leaf += 1
        else:
            for v in o.values(): walk(v)
for f in tf: walk(json.load(open(os.path.join(K, 'tokens', f))))
out['tokens']['leaf_count_live_files'] = leaf

# ---- components: 29 without provides, 21 with governedBy, 127 without obeys
out['components'] = dict(metas=len(metas), without_provides=sum(1 for m in metas.values() if not m.get('provides')),
                         with_governedBy=sum(1 for m in metas.values() if (m.get('edges') or {}).get('governedBy')),
                         without_obeys=len(metas) - len({e['s'] for e in obeys}),
                         governs_reach_components=len({e['t'] for e in live if e['type'] == 'governs' and kind.get(e['t']) == 'component'}),
                         appliesTo_reach_components=len({e['t'] for e in live if e['type'] == 'appliesTo' and kind.get(e['t']) == 'component'}))

# ---- dangling by type
out['null_by_type'] = dict(collections.Counter(e['type'] for e in null))

# ---- explorer: 5 meta edge types in no chip
tpl = open(os.path.join(K, '_kg_explorer.template.html')).read()
fam_map = re.search(r"const FAMILY=\{(.*?)\};", tpl, re.S).group(1)
in_chip = set(re.findall(r"\b([A-Za-z]+):'", fam_map))
schema = json.load(open(os.path.join(K, 'components', 'meta.schema.json')))
met = [k for k in schema['properties']['edges']['properties'] if not k.startswith('$')]
out['explorer'] = dict(meta_edge_types=len(met), not_in_chip=sorted(t for t in met if t not in in_chip),
                       live_types_not_in_chip=sorted(t for t in tc if t not in in_chip))

json.dump(out, open(os.path.join(os.path.dirname(__file__), 'verify-figures.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
