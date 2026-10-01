#!/usr/bin/env python3
"""#311 overnight lane D3 — s308-D28 (item 9 v2, taken whole; extends s308-D24): the five edges and the theme node
kind written into knowledge/_edge_register.json. Adds four rows (aliasOf, providesCapability, ariaRole, replacedBy)
and points defaultFor at theme. Measured counts are read from knowledge/_standard_nodes.json and the logo store.
Idempotent: a second run rewrites the same rows."""
import json, collections, datetime

REG = 'knowledge/_edge_register.json'
reg = json.load(open(REG, encoding='utf-8'))
std = json.load(open('knowledge/_standard_nodes.json', encoding='utf-8'))
AT = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ')
D28 = ("s308-D28 (Dave 2026-09-29 12:13 BST, '9. Five edges the outside world has and Apollo lacks Changed in v2 — "
       "Take it', taken whole)")
D21B = ("s308-D21 (Dave 2026-09-29 09:26 BST, '6. One maker field on every edge — Take it') — one rule per type, "
        "stamped on every edge by knowledge/_build_kg_explorer.py; a stored line that carries its own `maker` keeps it")
D27N = ("s308-D27 (Dave 2026-09-29 12:13 BST, 'Lets do what is neatest, and if changes my answer thats fine, I don't "
        "like patches more than my preference for ango-saxon')")
OB = ("s308-D22 + s308-D27 (#311 lane D3): graded on the outside definition the research page names for the edge "
      "(notes/_RESEARCH-308-design-system-ontologies-2026-09-29-v2.html item 9)")


def measured(ty):
    es = [e for e in std['edges'] if e['type'] == ty]
    k = lambda x: str(x).split(':')[0]
    return {'edges': len(es), 'nulls': 0, 'from': dict(collections.Counter(k(e['s']) for e in es)),
            'to': dict(collections.Counter(k(e['t']) for e in es)), 'at': AT}


GEN = lambda: {'made': 'generated', 'by': 'gen_kg_standards.py', 'value': 'generated:gen_kg_standards.py',
               'note': 'knowledge/gen_kg_standards.py --land', 'store': ['knowledge/_standard_nodes.json'], 'basis': D21B}
NOWHY = {'field': 'why', 'required': False, 'floor': None, 'basis': 'not required: generated structure (s308-D20)',
         'today': {'spelled': None, 'carried': '0', 'note': 'the line carries its source sentence or leaf pairs in `note`'}}
NONULL = {'allowed': False, 'basis': 'gen_kg_standards.py lands no declared null for this type'}
NOOPP = {'type': None, 'stored': True, 'basis': 'no opposite type; the backward reading is `reads.back`, derived by walking the graph, never stored'}
UNREAD = lambda s: {'reads': [], 'unread': s + ' Read by no verb: a verb for it is a ruling, not a default.', 'source': 'this register (#311 lane D3)'}


def outside(term, vocab, grade, word, also=(), note=None):
    o = {'term': term, 'vocabulary': vocab, 'grade': grade, 'also': list(also)}
    if note: o['note'] = note
    basis = ("kept: an exact match, and Apollo's word is the plainer label" if grade == 'exact' else
             f"kept: the outside term is {grade}, not the same relation, so adopting it as the name would say something the edge does not; the term is written beside it")
    if word == 'aliasOf':
        basis = "adopted: dt:aliasOf is the neatest name and is Apollo's word too (s308-D28 a names it)"
    if word == 'replacedBy':
        basis = "adopted: Spectrum's replacedBy is the neatest name and is Apollo's word too (s308-D28 e names it)"
    o.update({'candidates': [], 'name': {'word': word, 'adopted': word in ('aliasOf', 'replacedBy'), 'basis': basis + ' (' + D27N + ').'},
              'basis': OB})
    return o


ROWS = [
    {'word': 'aliasOf', 'plain': 'is an alias of',
     'verb': UNREAD("token:<group> → token:<group> — a token's `$alias` (per mode) at the graph's group grain, s308-D28 (a)."),
     'from': ['token'], 'to': ['token'], 'nulls': NONULL, 'opposite': NOOPP,
     'reads': {'forward': 'takes its value from', 'back': 'gives its value to'},
     'shape': {'self': False, 'loops': False, 'bothWays': False, 'chains': True,
               'basis': "the design-token format: circular references must be detected — gen_kg_standards.py refuses a cycle at LEAF grain before landing, and the shape check refuses one between groups; an alias inside one group is not drawn",
               'measured': {'selfLoops': 0, 'twoCycles': 0, 'repeatedPairs': 0}},
     'count': {'perStart': None, 'basis': "one target per leaf per mode is checked by the generator (dt:aliasOf, 'only one allowed'); a group carries many leaves, so no group count"},
     'maker': GEN(), 'outside': outside('dt:aliasOf', 'Canonical dt:', 'exact', 'aliasOf', ['DTCG alias (curly-brace reference)']),
     'family': 'tokens', 'note': 's308-D28 (a), #311 lane D3', 'why': NOWHY},
    {'word': 'providesCapability', 'plain': 'provides the capability',
     'verb': UNREAD('component → capability: the other half of acceptsCapability, s308-D28 (b); by name match only.'),
     'from': ['component'], 'to': ['capability'], 'nulls': NONULL, 'opposite': NOOPP,
     'reads': {'forward': 'provides', 'back': 'is provided by'},
     'shape': {'self': False, 'loops': False, 'bothWays': False, 'chains': False, 'basis': 'its two ends are different kinds, so it cannot point at itself or loop',
               'measured': {'selfLoops': 0, 'twoCycles': 0, 'repeatedPairs': 0}},
     'count': {'perStart': None, 'basis': 'no count is declared for this type today'},
     'maker': GEN(), 'outside': outside('providesApi', 'Backstage', 'close', 'providesCapability', [],
                                        'other (none of the design-system vocabularies, SKOS, Dublin Core or PROV covers it)'),
     'family': 'sources', 'note': "s308-D28 (b), #311 lane D3: a capability is provided by the component that carries its own name; the rest are listed `unprovided` in the store until a meta declares what it provides", 'why': NOWHY},
    {'word': 'ariaRole', 'plain': 'takes the ARIA role',
     'verb': UNREAD("component → aria:<role> — the WAI-ARIA roles the meta's own accessibility.role field names with role=<x>, s308-D28 (d)."),
     'from': ['component'], 'to': ['aria'], 'nulls': NONULL, 'opposite': NOOPP,
     'reads': {'forward': 'takes the role', 'back': 'is the role of'},
     'shape': {'self': False, 'loops': False, 'bothWays': False, 'chains': False, 'basis': 'its two ends are different kinds, so it cannot point at itself or loop',
               'measured': {'selfLoops': 0, 'twoCycles': 0, 'repeatedPairs': 0}},
     'count': {'perStart': None, 'basis': 'a component may use several roles in its markup (a chart: group and img)'},
     'maker': GEN(), 'outside': outside('role (the WAI-ARIA role attribute)', 'WAI-ARIA 1.2', 'exact', 'ariaRole', [],
                                        'other (WAI-ARIA is the standard the edge points into)'),
     'family': 'guidelines', 'note': "s308-D28 (d), #311 lane D3. ARIA's required-context and required-owned checks against containedBy are not built here.", 'why': NOWHY},
    {'word': 'replacedBy', 'plain': 'is replaced by',
     'verb': UNREAD('component → component, token → token, with the version it happened in, s308-D28 (e).'),
     'from': ['component', 'token'], 'to': ['component', 'token'], 'pairs': [['component', 'component'], ['token', 'token']],
     'nulls': NONULL, 'opposite': NOOPP,
     'reads': {'forward': 'is replaced by', 'back': 'replaces'},
     'shape': {'self': False, 'loops': False, 'bothWays': False, 'chains': True, 'basis': 'an order (a part, a partial, a variant, a replacement): never a loop',
               'measured': {'selfLoops': 0, 'twoCycles': 0, 'repeatedPairs': 0}},
     'count': {'perStart': {'max': 1}, 'basis': 'a thing is replaced by one thing (Spectrum replacedBy names one)'},
     'maker': {'made': 'ratified', 'by': 's308-D42', 'value': 'ratified:s308-D42',
               'note': 'the ratified lines in knowledge/_replaced_by.json, each naming its ruling and version; the two lines today are s308-D42 (stat card and KPI tile replaced by Metric)',
               'store': ['knowledge/_replaced_by.json', 'knowledge/_standard_nodes.json'], 'basis': D21B},
     'outside': outside('replacedBy', 'Spectrum', 'exact', 'replacedBy', ['DTCG $deprecated', 'Dublin Core isReplacedBy']),
     'family': 'structure', 'note': 's308-D28 (e), #311 lane D3: each line carries `version` (and `released` false while that version is uncut) and `ruling`',
     'why': {'field': 'why', 'required': False, 'floor': None, 'servedBy': 'ruling',
             'basis': 'not required: every line names the ruling that replaced it, which serves (s308-D20)',
             'today': {'spelled': None, 'carried': '0', 'note': 'the ruling and the version ride on the line'}}},
]
for r in ROWS:
    r['$measured'] = measured(r['word'])
by = {r['word']: i for i, r in enumerate(reg['types'])}
for r in ROWS:
    if r['word'] in by:
        reg['types'][by[r['word']]] = r
    else:
        reg['types'].append(r)
reg['types'].sort(key=lambda r: r['word'].lower())
# (c) defaultFor points at the theme node kind
df = next(r for r in reg['types'] if r['word'] == 'defaultFor')
df['to'] = ['theme']
df['note'] = ("s308-D28 (c), #311 lane D3: theme is a node kind (theme:<id>, from knowledge/tokens/themes/_themes.json, "
              "and the two colour modes the records name as a theme); the explorer points each defaultFor line declared "
              "null with a `theme` qualifier at theme:<that>. Storage (knowledge/_logo_nodes.json) is unchanged.")
df['verb']['unread'] = "logo: → theme: — s230-D2 names the default lockup per theme; the theme is a node (s308-D28 c). Not a reading."
df['shape']['basis'] = 'its two ends are different kinds, so it cannot point at itself or loop'
reg['$schema']['rulings']['s308-D24'] = 'item 9 — the four edges a-d (#311 lane D3, as extended by s308-D28)'
reg['$schema']['rulings']['s308-D28'] = 'item 9 v2 — five edges (aliasOf, providesCapability, ariaRole, replacedBy; defaultFor → theme) and the theme node kind (#311 lane D3)'
d = reg.get('$doc') or {}
if isinstance(d.get('owed'), dict):
    d['owed'].pop('item 9 (s308-D24)', None)
ac = next(r for r in reg['types'] if r['word'] == 'acceptsCapability')
ac['note'] = 'the accepting half; its providing half is providesCapability (s308-D28 b, #311 lane D3)'
with open(REG, 'w', encoding='utf-8') as f:
    f.write(json.dumps(reg, indent=1, ensure_ascii=False) + '\n')
print('rows', len(reg['types']), '· added/replaced', [r['word'] for r in ROWS], '· measured',
      {r['word']: r['$measured']['edges'] for r in ROWS})
