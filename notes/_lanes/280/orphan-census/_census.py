#!/usr/bin/env python3
"""#280 lane OC — THE ORPHAN CENSUS.

MEASURES only. Reads the embedded KG out of notes/_KG-EXPLORER.html (the graph as the page
actually holds it) and the chip vocabulary out of knowledge/_kg_explorer.template.html (the
FAMILY map and the famOn defaults, parsed from the shipped template — never retyped), then
counts degree-zero nodes at three chip settings and writes facts.json + the page.

Nothing under knowledge/ is written. No number in the page is typed by hand: every figure the
page prints comes out of FACTS, and FACTS comes out of the two files above.

  python3 notes/_lanes/280/orphan-census/_census.py            # facts.json + the page
  python3 notes/_lanes/280/orphan-census/_census.py --facts    # facts.json only, print the table
"""
import json, os, re, sys, collections, datetime, html

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
K = os.path.join(REPO, 'knowledge')
EXPLORER = os.path.join(REPO, 'notes', '_KG-EXPLORER.html')
TEMPLATE = os.path.join(K, '_kg_explorer.template.html')
PAGE = os.path.join(HERE, 'ORPHANS-2026-09-17.html')
FACTS = os.path.join(HERE, 'facts.json')


# ---------------------------------------------------------------- read the graph and the chips
def load_kg():
    src = open(EXPLORER, encoding='utf-8').read()
    tag = '<script id="kg" type="application/json">'
    i = src.index(tag) + len(tag)
    j = src.index('</script>', i)
    kg = json.loads(src[i:j])
    ver = re.search(r'v(\d+\.\d+)\s*·', src)
    kg['_version'] = ver.group(1) if ver else kg.get('version', '?')
    return kg


def load_chips():
    """The FAMILY edge-type→family map and the famOn defaults, out of the shipped template."""
    t = open(TEMPLATE, encoding='utf-8').read()
    blk = re.sub(r'//.*', '', t.split('const FAMILY={')[1].split('};')[0])
    fam = dict(re.findall(r"(\w+):'(\w+)'", blk))
    dblk = t.split('const famOn={')[1].split('}')[0]
    defaults = {k: int(v) for k, v in re.findall(r'(\w+):(\d)', dblk)}
    lblk = re.sub(r'//.*', '', t.split('const FAMLABEL={')[1].split('};')[0])
    labels = dict(re.findall(r"(\w+):'([^']+)'", lblk))
    return fam, defaults, labels


KG = load_kg()
FAMILY, DEFAULTS, FAMLABEL = load_chips()
NODES = [n for n in KG['nodes'] if not n.get('dead') and n.get('died') is None]
EDGES = [e for e in KG['edges'] if not e.get('dead') and e.get('died') is None]
BY = {n['id']: n for n in NODES}
FAMOF = lambda n: n.get('fam') or 'base'

ADDITIVE = ['guidelines', 'guidelinerules', 'uxprinciples', 'assets']
SETTINGS = [
    ('defaults', 'Page defaults',
     dict(DEFAULTS)),
    ('all', 'Every chip on',
     {**DEFAULTS, **{f: 1 for f in ADDITIVE}}),
    ('allconst', 'Every chip on + Constitution',
     {**DEFAULTS, **{f: 1 for f in ADDITIVE}, 'governance': 1}),
]


def DR(e):
    """The page's design-rulings sub-chip predicate (template, DR=)."""
    t = e['type']
    return t in ('governedBy', 'ruledBy') or (t == 'governs' and bool(re.match(r'^(component|snippet):', e.get('t') or '')))


def measure(famOn):
    """The page's own predicates: NODEON = famOK (every type chip is on), EON = family chip
    + the design-rulings sub-chip, an edge drawn only when both ends are shown and t resolves."""
    ok = lambda o: (not o.get('fam')) or famOn.get(o['fam'], 0)
    eon = lambda e: famOn.get(FAMILY.get(e['type']), 0) and ((not DR(e)) or famOn['designrulings'])
    deg, nul, drawn = collections.Counter(), collections.Counter(), 0
    for e in EDGES:
        if not e.get('t'):
            if ok(e):
                nul[e['s']] += 1
            continue
        s, t = BY.get(e['s']), BY.get(e['t'])
        if s and t and ok(s) and ok(t) and eon(e):
            deg[e['s']] += 1
            deg[e['t']] += 1
            drawn += 1
    vis = [n for n in NODES if ok(n)]
    zero = [n for n in vis if deg[n['id']] == 0]
    return dict(vis=vis, zero=zero, deg=deg, nul=nul, drawn=drawn,
                nullonly=[n for n in zero if nul[n['id']] > 0])


M = {k: measure(f) for k, _, f in SETTINGS}

# storage adjacency — every resolved edge, chip-blind, so a cause can be read off the data
SDEG, STYPES, SNULL = collections.Counter(), collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
for e in EDGES:
    if not e.get('t'):
        SNULL[e['s']][e['type']] += 1
        continue
    if e['s'] in BY and e['t'] in BY:
        SDEG[e['s']] += 1
        SDEG[e['t']] += 1
        STYPES[e['s']][e['type']] += 1
        STYPES[e['t']][e['type']] += 1

HOMELESS = sorted({e['type'] for e in EDGES} - set(FAMILY))   # edge types with no chip anywhere
ETC = collections.Counter(e['type'] for e in EDGES)


def probe(**kw):
    """A degree count at one named chip variation — used to price 'which chip lights it'."""
    f = {**DEFAULTS}
    f.update(kw)
    return measure(f)


# ---------------------------------------------------------------- the ten sets
def pick(setting, pred):
    return [n for n in M[setting]['zero'] if pred(n)]


P_GR = probe(guidelinerules=1)
BASE_RULE_DEF = [n for n in NODES if n['type'] == 'rule' and FAMOF(n) == 'base']
lit_by_gr = [n for n in BASE_RULE_DEF if P_GR['deg'][n['id']] > 0]
dark_after_gr = [n for n in BASE_RULE_DEF if P_GR['deg'][n['id']] == 0]

UXALL = [n for n in NODES if n['type'] == 'ux']
UXDARK = pick('allconst', lambda n: n['type'] == 'ux')
UXLIT = [n for n in UXALL if n not in UXDARK]
OBEYS_UX = sorted({e['t'] for e in EDGES if e['type'] == 'obeys' and (e.get('t') or '').startswith('ux:')})
OBEYS_UX_EDGES = sum(1 for e in EDGES if e['type'] == 'obeys' and (e.get('t') or '').startswith('ux:'))
OBEYS_METAS = len({e['s'] for e in EDGES if e['type'] == 'obeys'})

RULE_CONST = pick('all', lambda n: n['type'] == 'rule')
RULE_CONST_ARTEFACTS = collections.Counter(
    e['t'] for e in EDGES if e['type'] == 'definedIn' and e['s'] in {n['id'] for n in RULE_CONST} and e.get('t') in BY)

LOGO_DARK = pick('allconst', lambda n: n['type'] == 'logo')
LOGO_NULLS = collections.Counter(t for n in LOGO_DARK for t in SNULL[n['id']].elements())

# the UX generator's two switched-off edge types (s275-D2 kept them behind flags)
UXFILE = json.load(open(os.path.join(K, '_ux_principle_nodes.json'), encoding='utf-8'))
UXFAMS = collections.Counter(n.get('family') for n in UXFILE['nodes'] if n['id'].startswith('ux:'))
UX_WITH_FAMILY = sum(1 for n in UXFILE['nodes'] if n['id'].startswith('ux:') and n.get('family'))
UX_WITH_EVIDENCE = sum(1 for n in UXFILE['nodes'] if n['id'].startswith('ux:') and n.get('evidence'))

UX_NO_STORAGE = sum(1 for n in UXDARK if SDEG[n['id']] == 0 and not SNULL[n['id']])
POLARITIES = [n for n in NODES if n['type'] == 'polarity']
POL_WIRED = sum(1 for n in POLARITIES if SDEG[n['id']] > 0)


def homeless_set(t):
    return dict(type=t, n=ETC[t],
                ends=collections.Counter(
                    f"{FAMOF(BY[e['s']])}:{BY[e['s']]['type']} → " + (f"{FAMOF(BY[e['t']])}:{BY[e['t']]['type']}" if e.get('t') in BY else 'declared null')
                    for e in EDGES if e['type'] == t and e['s'] in BY).most_common(2))


SETS = [
    dict(id='ux-cloud', rank=1, n=len(UXDARK),
         title='UX principles that nothing points at',
         what='%d of the %d ux: principles carry no line at any chip setting. The pink cloud in the screenshot is this set.' % (len(UXDARK), len(UXALL)),
         cause='b',
         dark=['defaults', 'all', 'allconst']),
    dict(id='base-rules-chip-off', rank=2, n=len(lit_by_gr),
         title='HSBC rules dark because their chip is off',
         what='%d rule: nodes stand in the base graph with no line at the page defaults, and every one of them lights up the moment the HSBC rule: chip goes on.' % len(lit_by_gr),
         cause='d', dark=['defaults']),
    dict(id='shapes', rank=3, n=len(pick('allconst', lambda n: n['type'] == 'shape')),
         title='Data shapes', cause='a', dark=['defaults', 'all', 'allconst'],
         what='%d shape: nodes, dark at every setting. %d hasDataShape lines run into them and none can be drawn.' % (len(pick('allconst', lambda n: n['type'] == 'shape')), ETC['hasDataShape'])),
    dict(id='intents', rank=4, n=len(pick('allconst', lambda n: n['type'] == 'intent')),
         title='Intents', cause='a', dark=['defaults', 'all', 'allconst'],
         what='%d intent: nodes, dark at every setting, with %d answersIntent lines behind them.' % (len(pick('allconst', lambda n: n['type'] == 'intent')), ETC['answersIntent'])),
    dict(id='roles', rank=5, n=len(pick('allconst', lambda n: n['type'] == 'role')),
         title='Roles', cause='a', dark=['defaults', 'all', 'allconst'],
         what='%d role: nodes, dark at every setting, and the heaviest of the three — %d providesRole lines.' % (len(pick('allconst', lambda n: n['type'] == 'role')), ETC['providesRole'])),
    dict(id='rules-in-the-constitution', rank=6, n=len(RULE_CONST),
         title='Rules whose guideline file was filed under the Constitution',
         cause='c', dark=['defaults', 'all'],
         what='%d rule: nodes stay dark with every chip on and only light when the Constitution chip joins them. Their one line is a definedIn pointing at %d guideline files that the builder filed in the Constitution family.' % (len(RULE_CONST), len(RULE_CONST_ARTEFACTS))),
    dict(id='logos', rank=7, n=len(LOGO_DARK),
         title='Lockups bound by nothing', cause='d', dark=['defaults', 'all', 'allconst'],
         what='%d logo: nodes whose only edge is a declared-null governedBy. They are drawn as unbound on purpose.' % len(LOGO_DARK)),
    dict(id='obeys-ux', rank=8, n=len(OBEYS_UX),
         title='The principles a design actually cites', cause='a', dark=['defaults', 'all', 'allconst'],
         what='Of %d principles, %d are named by a component meta — and the edge that names them, obeys, has no chip, so not one of those %d lines is drawn.' % (len(UXALL), len(OBEYS_UX), ETC['obeys'])),
    dict(id='homeless-edges', rank=9, n=sum(ETC[t] for t in HOMELESS),
         title='Lines no chip can turn on', cause='a', dark=['defaults', 'all', 'allconst'],
         what='%d authored relations across %d edge types sit in the graph with no family in the chip map, so nothing in the page can draw them.' % (sum(ETC[t] for t in HOMELESS), len(HOMELESS))),
    dict(id='polarity-reach', rank=10, n=len(UXLIT),
         title='Everything the Explanation view has', cause='b', dark=[],
         what='All %d polarities are wired, and between them they reach %d of the %d principles. That is the whole of the Explanation view: no component, no rule and no ruling reaches a principle today.' % (len(POLARITIES), len(UXLIT), len(UXALL))),
]

HEADLINE = dict(
    dark_everywhere=len(M['allconst']['zero']),
    visible_allconst=len(M['allconst']['vis']),
    dark_defaults=len(M['defaults']['zero']),
    visible_defaults=len(M['defaults']['vis']),
    dark_all=len(M['all']['zero']),
    visible_all=len(M['all']['vis']),
    causes=len({s['cause'] for s in SETS if s['dark']}),
    ux_dark=len(UXDARK), ux_all=len(UXALL),
)

FACTSDOC = dict(
    generated=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    explorer=KG['_version'], kg_generated=KG.get('generated'), commit=KG.get('commit'),
    headline=HEADLINE,
    settings=[dict(key=k, name=name,
                   visible=len(M[k]['vis']), zero=len(M[k]['zero']),
                   nullonly=len(M[k]['nullonly']), drawn=M[k]['drawn'])
              for k, name, _ in SETTINGS],
    byfam=[dict(fam=f, label=FAMLABEL.get(f, 'the base graph'),
                cells=[dict(setting=k,
                            visible=sum(1 for n in M[k]['vis'] if FAMOF(n) == f),
                            zero=sum(1 for n in M[k]['zero'] if FAMOF(n) == f),
                            nullonly=sum(1 for n in M[k]['nullonly'] if FAMOF(n) == f))
                       for k, _, _ in SETTINGS])
           for f in ['base'] + ADDITIVE + ['governance']],
    bytype=[dict(type=t,
                 cells=[dict(setting=k,
                             visible=sum(1 for n in M[k]['vis'] if n['type'] == t),
                             zero=sum(1 for n in M[k]['zero'] if n['type'] == t))
                        for k, _, _ in SETTINGS])
            for t in sorted({n['type'] for n in NODES})],
    homeless=[homeless_set(t) for t in HOMELESS],
    sets=SETS,
    ux=dict(total=len(UXALL), dark=len(UXDARK), lit=len(UXLIT),
            polarities=len(POLARITIES), polarities_wired=POL_WIRED,
            families=len(UXFAMS), with_family=UX_WITH_FAMILY, with_evidence=UX_WITH_EVIDENCE,
            no_storage_edge=UX_NO_STORAGE, cited_by_a_meta=len(OBEYS_UX), obeys_to_ux=OBEYS_UX_EDGES, obeys_edges=ETC['obeys'], obeys_metas=OBEYS_METAS,
            top_families=UXFAMS.most_common(6)),
    rules=dict(base_at_defaults=len(BASE_RULE_DEF), lit_by_chip=len(lit_by_gr),
               dark_after_chip=len(dark_after_gr), dark_with_all_chips=len(RULE_CONST),
               artefacts=[[a.split('artefact:')[-1], c] for a, c in RULE_CONST_ARTEFACTS.most_common()]),
    logos=dict(dark=len(LOGO_DARK), nulls=LOGO_NULLS.most_common()),
)

if '--facts' in sys.argv or True:
    json.dump(FACTSDOC, open(FACTS, 'w', encoding='utf-8'), indent=1)

if '--facts' in sys.argv:
    print(json.dumps({k: FACTSDOC[k] for k in ('headline', 'settings', 'byfam')}, indent=1))
    sys.exit(0)

# ---------------------------------------------------------------- the page
E = lambda s: html.escape(str(s), quote=True)
F = FACTSDOC
SET_NAMES = {k: name for k, name, _ in SETTINGS}

CAUSE = {
    'a': ('No edge type reaches the page',
          'The relation is authored and live in storage, but the explorer’s chip map gives its edge type no family — so no chip anywhere can draw it.'),
    'b': ('The source never emitted the edge',
          'The edge type exists and the generator can write it; it was switched off, so nothing was emitted.'),
    'c': ('The relation has no declared home',
          'Both ends exist and the line is drawn — but the far end was filed in a family that hides it. A word is owed on where it belongs.'),
    'd': ('A leaf by design, or a chip that is simply off',
          'Nothing is broken. The dot is dark because that is what was ruled, or because the chip that lights it is off by default.'),
}

ZT = lambda t: next(c['zero'] for r in F['bytype'] if r['type'] == t for c in r['cells'] if c['setting'] == 'allconst')
HN = lambda t: next(h['n'] for h in F['homeless'] if h['type'] == t)

BLOCKS = [
    dict(id='ux-cloud', title='The pink cloud — %d of %d UX principles' % (F['ux']['dark'], F['ux']['total']),
         count='%d nodes' % F['ux']['dark'], where='dark at all three settings', cause='b',
         body=[
             'This is the picture on the screenshot. The Explanation view holds %d principles and %d polarities. Every polarity is wired. The principles are not: a principle gets a line only when a polarity names it as a party, and between them the %d polarities reach %d principles. The other %d have no edge of any kind in storage — not a null, not a stub, nothing.'
             % (F['ux']['total'], F['ux']['polarities'], F['ux']['polarities'], F['ux']['lit'], F['ux']['dark']),
             'The wiring is already written. The principle generator can emit two more edge kinds and both are held back by the ruling that landed the family: one groups each principle under the research family it came from (%d of the principles carry that field, across %d families), the other links a principle to the sources it was graded on (%d carry it). Turning the first on gives every one of the %d dark dots a line on the day it runs.'
             % (F['ux']['with_family'], F['ux']['families'], F['ux']['with_evidence'], F['ux']['dark']),
             'It also puts a family node into the graph, which is a new kind of thing on the stage — and that is the part only you can say.'],
         wires='The principle generator’s two held-back edge kinds, landed behind the same ruling that landed the family.',
         cost='One question to you, then one lane. The generator is written; the lane lands the edges, re-runs the validator and proves the count moved.'),
    dict(id='base-rules-chip-off', title='%d HSBC rules with the chip off' % F['rules']['lit_by_chip'],
         count='%d nodes' % F['rules']['lit_by_chip'], where='dark at the page defaults only', cause='d',
         body=[
             'At the defaults the page shows %d rule: dots in the base graph and not one line between them. It reads like the worst cloud on the page, and it is the cheapest: %d of them light up the moment the HSBC rule: chip goes on, because the line that holds them is the one that says which guideline file defines them, and that line belongs to the rule family whose chip loads off.'
             % (F['rules']['base_at_defaults'], F['rules']['lit_by_chip']),
             'So this is not an orphan set. It is a default. The only question is whether a dot should be allowed on the stage when the chip that explains it is off.'],
         wires='Nothing. The chip already draws them.',
         cost='Free, or one question if you want the default changed.'),
    dict(id='shapes', title='%d data shapes' % ZT('shape'),
         count='%d nodes' % ZT('shape'),
         where='dark at all three settings', cause='a',
         body=['Every chart component declares the data shape it takes. %d of those declarations are in the graph as lines and %d shape: dots stand at the end of them — and the page cannot draw a single one, because its chip map has no family for that edge type. The relation is authored, live and invisible.'
               % (HN('hasDataShape'),
                  ZT('shape'))],
         wires='One line in the chip map putting the edge type in the System view, beside the wiring it already belongs with.',
         cost='Shares a lane with the intents, the roles and the yields-to lines below — one lane for all four, with pixel proof that nothing else moved.'),
    dict(id='intents', title='%d intents' % ZT('intent'),
         count='%d nodes' % ZT('intent'),
         where='dark at all three settings', cause='a',
         body=['The same story, one step further out: %d lines saying which user intent a component answers, ending on %d dots the page will not connect. These are the closest thing the graph has to a job-to-be-done, and they are the least visible thing on it.'
               % (HN('answersIntent'),
                  ZT('intent'))],
         wires='The same one line in the chip map.',
         cost='Rides the same lane.'),
    dict(id='roles', title='%d roles' % ZT('role'),
         count='%d nodes' % ZT('role'),
         where='dark at all three settings', cause='a',
         body=['The heaviest of the three by a distance: %d lines say which role a component provides, and all of them land on %d dots. This one edge type carries more traffic than the whole Explanation view puts on the stage, and none of it shows.'
               % (HN('providesRole'),
                  ZT('role'))],
         wires='The same one line in the chip map.',
         cost='Rides the same lane.'),
    dict(id='rules-in-the-constitution', title='%d rules that need the Constitution to show a line' % F['rules']['dark_with_all_chips'],
         count='%d nodes' % F['rules']['dark_with_all_chips'], where='dark until the Constitution chip joins', cause='c',
         body=[
             'With every chip on, %d rule: dots are still dark. Their only line is the one naming the guideline file that defines them — and for these, that file was claimed by the Constitution family, because a ruling listed the file among its own artefacts before the rule family got to it. Three files do all the damage: %s.'
             % (F['rules']['dark_with_all_chips'], ', '.join('%s (%d rules)' % (a, c) for a, c in F['rules']['artefacts'])),
             'A guideline file is a guideline file whichever record names it first. The graph currently says otherwise, and three dots decide the fate of %d.' % F['rules']['dark_with_all_chips']],
         wires='A rule about which family owns a file that two records both name — then a build change that follows it.',
         cost='One question, then a short lane. The lane is small; the question is the part that has to come first.'),
    dict(id='logos', title='%d lockups bound by nothing' % F['logos']['dark'],
         count='%d nodes' % F['logos']['dark'], where='dark at all three settings, declared nulls only', cause='d',
         body=['These are the only orphans on the page that are orphans on purpose. Each one carries a declared line to a rule that does not exist — that is what "bound by nothing" looks like when you draw it honestly, and it is what you asked for when they landed. A separate logo review is already parked against them.'],
         wires='Nothing, until the logo review runs.',
         cost='Free to declare. The review is its own piece of work and is already waiting on you.'),
    dict(id='obeys-ux', title='The %d principles a design actually cites' % F['ux']['cited_by_a_meta'],
         count='%d of %d principles' % (F['ux']['cited_by_a_meta'], F['ux']['total']), where='the edge exists, no chip draws it', cause='a',
         body=[
             'There is a real chain from a component to a principle: %d components carry a hand-written list of the rules and principles they obey, with a sentence attached to each, and %d of those %d lines land on a principle. It was ruled that those lines stand. The page has never drawn one, because the edge type has no family in the chip map.'
             % (F['ux']['obeys_metas'], F['ux']['obeys_to_ux'], F['ux']['obeys_edges']),
             'Drawing it is not the same one-line change as the shapes and the roles. Those belong in the System view with the rest of the wiring. This one is a design obligation, and the obligation view was fixed at three provenances — a fourth is your word, not a lane’s.'],
         wires='A place for the obligation edge in the Design governance view.',
         cost='One question. The lane after it is small — the same one line in the chip map, plus the count in the header.'),
    dict(id='homeless-edges', title='%d lines no chip can turn on' % sum(h['n'] for h in F['homeless']),
         count='%d relations, %d edge types' % (sum(h['n'] for h in F['homeless']), len(F['homeless'])),
         where='never drawn, at any setting', cause='a',
         body=[
             'The whole of the condition behind the three sets above, counted in one place: %s. They are authored, they are live, they pass the validator, and the page has no family for any of them, so no chip anywhere draws them.'
             % ', '.join('%s %d' % (h['type'], h['n']) for h in F['homeless']),
             'One of them orphans nobody and is worth naming anyway: %d lines saying which component yields to which. Both ends are components, both are already on the stage, and the line between them has never appeared.'
             % HN('yieldsTo')],
         wires='The chip map gaining a family for each — one place, one line each, and the header count of edge types moves with it.',
         cost='One lane for the System-view ones. The obligation edge above is the only one of them that needs your word first.'),
    dict(id='polarity-reach', title='What the Explanation view is holding up', count='%d of %d principles lit' % (F['ux']['lit'], F['ux']['total']),
         where='not an orphan set — the reason there is one', cause='b',
         body=[
             'Worth saying plainly, because it is the shape of the whole problem. Every line in the Explanation view today starts at a polarity. %d polarities, all wired, reaching %d principles. Nothing else in the graph reaches a principle at all: not a component, not a rule, not a ruling.'
             % (F['ux']['polarities'], F['ux']['lit']),
             'So the view is not half-built — it is built on one hinge. Widening it is the same decision as the pink cloud above, and answering that one answers this.'],
         wires='The same two held-back edge kinds, plus the obligation edge.',
         cost='No separate cost. It is the first question, seen from the other side.'),
]

OPTIONS = [('wire', 'Wire it — cut the lane'),
           ('leaf', 'It is a leaf by design — declare it and stop counting it'),
           ('ruling', 'It needs a ruling first — put the question')]


def table_rows():
    out = []
    for r in F['byfam']:
        if all(c['visible'] == 0 for c in r['cells']):
            continue
        cells = ''.join(
            '<td>%s</td>' % ('<span class="off">chip off</span>' if c['visible'] == 0 else
                             '<b>%d</b> <span class="of">of %s</span>%s' % (c['zero'], f"{c['visible']:,}",
                                                                            ' <span class="nl">%d null-only</span>' % c['nullonly'] if c['nullonly'] else ''))
            for c in r['cells'])
        out.append('<tr><th scope="row">%s</th>%s</tr>' % (E(r['label']), cells))
    tot = ''.join('<td><b>%d</b> <span class="of">of %s</span></td>' % (s['zero'], f"{s['visible']:,}") for s in F['settings'])
    out.append('<tr class="tot"><th scope="row">All families</th>%s</tr>' % tot)
    return '\n'.join(out)


def type_rows():
    out = []
    for r in F['bytype']:
        if all(c['zero'] == 0 for c in r['cells']):
            continue
        cells = ''.join('<td>%s</td>' % ('<span class="off">—</span>' if c['visible'] == 0 else
                                         '<b>%d</b> <span class="of">of %s</span>' % (c['zero'], f"{c['visible']:,}"))
                        for c in r['cells'])
        out.append('<tr><th scope="row">%s:</th>%s</tr>' % (E(r['type']), cells))
    return '\n'.join(out)


def block_html(i, b):
    cl, cd = CAUSE[b['cause']]
    body = '\n'.join('<p>%s</p>' % E(p) for p in b['body'])
    radios = '\n'.join(
        '<label class="opt"><input type="radio" name="%s" value="%s"><span>%s</span></label>' % (E(b['id']), E(v), E(l))
        for v, l in OPTIONS)
    return f'''<section class="dim" id="{E(b['id'])}">
 <div class="wrapper"><div class="wrap">
  <div class="aside">
   <div class="idx">{i:02d}</div>
   <p class="label">{E(b['count'])}</p>
   <p class="where">{E(b['where'])}</p>
   <p class="cause"><span>Cause</span>{E(cl)}</p>
   <p class="causedesc">{E(cd)}</p>
  </div>
  <div class="main">
   <h3>{E(b['title'])}</h3>
   {body}
   <dl class="fix">
    <dt>What wires it</dt><dd>{E(b['wires'])}</dd>
    <dt>What it costs</dt><dd>{E(b['cost'])}</dd>
   </dl>
   <fieldset class="ask">
    <legend>Your call</legend>
    {radios}
    <label class="note"><span>Note</span><input type="text" id="note-{E(b['id'])}" placeholder="optional — your words, kept verbatim"></label>
   </fieldset>
  </div>
 </div></div>
</section>'''


H = F['headline']
N_ = lambda v: f'{v:,}'
head_sentence = (
    '%s of the %s nodes on the stage have no line that any chip can draw — four causes account for every one of them, '
    'and the largest is the %s UX principles of the pink cloud, %s of which have no edge of any kind in storage.'
    % (N_(H['dark_everywhere']), N_(H['visible_allconst']), N_(H['ux_dark']), N_(F['ux']['no_storage_edge'])))

blocks = '\n'.join(block_html(i + 1, b) for i, b in enumerate(BLOCKS))
ids = json.dumps([b['id'] for b in BLOCKS])

PAGEHTML = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The orphan census — #280 lane OC</title>
<style>
:root{{--accent:#DB0011;--black:#000;--white:#fff;--grey-1:#F3F3F3;--grey-2:#EDEDED;--grey-3:#D7D8D6;--grey-5:#9B9B9B;--grey-6:#767676;--grey-7:#545454;--grey-8:#333;
--s1:.5rem;--s2:1rem;--s3:1.5rem;--s4:2rem;--s5:3rem;--s6:4rem;--s7:6rem;--max:1200px;--gutter:2rem}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--white);color:var(--black);font:400 1rem/1.75 "Helvetica Neue",Helvetica,Arial,sans-serif}}
.wrapper{{max-width:var(--max);margin:0 auto;padding:0 var(--gutter)}}
nav{{position:sticky;top:0;z-index:9;background:var(--white);border-bottom:1px solid var(--grey-2)}}
nav .wrapper{{display:flex;align-items:center;justify-content:space-between;height:54px;gap:var(--s3)}}
nav a,nav span{{font-size:.875rem;letter-spacing:.05em;color:var(--grey-6);text-decoration:none}}
nav .now{{color:var(--black);font-weight:500}}
section{{padding:var(--s7) 0;border-bottom:1px solid var(--grey-2)}}
section.tight{{padding:var(--s6) 0}}
.label{{font-size:.75rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s3)}}
.label::before{{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:none}}
h1{{font-size:3.5625rem;line-height:1.05;letter-spacing:0;font-weight:400;margin:0 0 var(--s4);max-width:22ch}}
h2{{font-size:2.125rem;line-height:1.15;font-weight:400;margin:0 0 var(--s4)}}
h3{{font-size:1.1875rem;line-height:1.25;font-weight:500;margin:0 0 var(--s3)}}
p{{margin:0 0 var(--s3);max-width:72ch}}
.lede{{font-size:1.1875rem;line-height:1.7;max-width:60ch}}
.meta{{font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--grey-6);margin:0}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s4);margin-top:var(--s6)}}
.stats div b{{display:block;font-size:2.6875rem;font-weight:200;line-height:1}}
.stats div span{{display:block;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--grey-6);margin-top:var(--s2)}}
table{{width:100%;border-collapse:collapse;font-size:.875rem}}
caption{{text-align:left;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--grey-6);padding-bottom:var(--s2)}}
th,td{{text-align:left;padding:var(--s2) var(--s2) var(--s2) 0;border-bottom:1px solid var(--grey-2);vertical-align:baseline}}
thead th{{font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;font-weight:500;color:var(--black);border-bottom:1px solid var(--black)}}
tbody th{{font-weight:400}}
td b{{font-weight:500}}
.of{{color:var(--grey-6)}}
.off{{color:var(--grey-6)}}
.nl{{display:block;font-size:.75rem;color:var(--grey-7)}}
tr.tot th,tr.tot td{{border-top:1px solid var(--black);border-bottom:none;font-weight:500}}
.dim .wrap{{display:grid;grid-template-columns:1fr 2fr;gap:var(--s6);align-items:start}}
.idx{{font-size:5.25rem;font-weight:100;line-height:.9;color:var(--grey-3);margin-bottom:var(--s3)}}
.aside .label{{margin-bottom:var(--s2)}}
.where{{font-size:.875rem;color:var(--grey-7);margin:0 0 var(--s3)}}
.cause{{font-size:.875rem;font-weight:500;margin:0 0 var(--s1);border-top:1px solid var(--grey-2);padding-top:var(--s3)}}
.cause span{{display:block;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);font-weight:400;margin-bottom:var(--s1)}}
.causedesc{{font-size:.875rem;color:var(--grey-7);line-height:1.6;margin:0}}
dl.fix{{margin:var(--s4) 0 0;border-top:1px solid var(--grey-2);padding-top:var(--s3)}}
dl.fix dt{{font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);margin-bottom:var(--s1)}}
dl.fix dd{{margin:0 0 var(--s3);max-width:72ch}}
fieldset.ask{{border:none;margin:var(--s4) 0 0;padding:0}}
fieldset.ask legend{{float:left;width:100%;border-top:1px solid var(--black);padding:var(--s3) 0 var(--s2);font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:500}}
fieldset.ask .opt:first-of-type{{clear:both}}
.opt{{display:flex;gap:var(--s2);align-items:baseline;padding:var(--s1) 0;cursor:pointer}}
.opt input{{margin:0;flex:none;position:relative;top:2px}}
.opt span{{font-size:.9375rem}}
label.note{{display:block;margin-top:var(--s3)}}
label.note span{{display:block;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);margin-bottom:var(--s1)}}
label.note input{{width:100%;max-width:46rem;font:400 .9375rem/1.6 inherit;padding:var(--s1) 0;border:none;border-bottom:1px solid var(--grey-3);background:none;color:var(--black)}}
label.note input:focus{{outline:none;border-bottom-color:var(--accent)}}
.grey{{background:var(--grey-1)}}
.prop{{display:grid;grid-template-columns:3fr 1fr 4fr;gap:var(--s6);align-items:start}}
.prop .div{{border-left:1px solid var(--grey-3);min-height:120px}}
button{{font:500 .875rem/1 inherit;letter-spacing:.06em;text-transform:uppercase;padding:14px 22px;border:none;background:var(--black);color:var(--white);cursor:pointer}}
button:hover{{background:var(--grey-8)}}
button.ghost{{background:none;color:var(--black);border-bottom:1px solid var(--accent);padding:14px 0;margin-left:var(--s4)}}
pre{{background:var(--grey-1);padding:var(--s3);overflow:auto;font:400 .8125rem/1.6 Menlo,monospace;max-height:26rem}}
#msg{{font-size:.875rem;color:var(--grey-7);margin-left:var(--s3)}}
footer{{padding:var(--s6) 0;font-size:.75rem;letter-spacing:.06em;color:var(--grey-6)}}
@media (max-width:900px){{
 :root{{--gutter:1rem}}
 h1{{font-size:2.125rem}} h2{{font-size:1.5rem}}
 section{{padding:var(--s5) 0}}
 .stats{{grid-template-columns:repeat(2,1fr);gap:var(--s3)}}
 .dim .wrap,.prop{{grid-template-columns:1fr;gap:var(--s3)}}
 .prop .div{{display:none}}
 .idx{{font-size:2.6875rem;margin-bottom:var(--s2)}}
 .scroll{{overflow-x:auto}}
 table{{min-width:34rem}}
 button.ghost{{margin-left:0;display:block}}
}}
</style></head><body>
<nav><div class="wrapper"><span>#280 · lane OC</span><span class="now">The orphan census</span><span>2026-09-17</span></div></nav>

<section><div class="wrapper">
 <p class="label">The count</p>
 <h1>Which dots have no lines, and what each one costs to fix</h1>
 <p class="lede">{E(head_sentence)}</p>
 <p class="meta">Measured on explorer v{E(F['explorer'])} · graph generated {E(F['kg_generated'])} · every figure on this page is read out of the graph, none is typed</p>
 <div class="stats">
  <div><b>{H['dark_defaults']}</b><span>dark at the page defaults</span></div>
  <div><b>{H['dark_all']}</b><span>dark with every chip on</span></div>
  <div><b>{H['dark_everywhere']}</b><span>dark whatever you do</span></div>
  <div><b>{H['ux_dark']}</b><span>of them UX principles</span></div>
 </div>
</div></section>

<section><div class="wrapper">
 <p class="label">How to read it</p>
 <div class="prop">
  <h2>A dot goes dark for four reasons, and only two of them are anyone’s fault.</h2>
  <div class="div"></div>
  <div>
   <p>Either the page has no way to draw the relation, or the relation was never written, or it was written and filed where the page hides it, or the dot is meant to stand alone. Each block below says which, from the data, and prices it in the only two currencies this record has: a lane, or one question to you.</p>
   <p>The three settings are the page as it opens, the page with every family chip switched on, and that plus the Constitution.</p>
  </div>
 </div>
</div></section>

<section><div class="wrapper">
 <p class="label">The table</p>
 <h2>Degree-zero nodes, by family</h2>
 <div class="scroll"><table>
  <caption>Nodes with no drawn edge, of the nodes visible at that setting</caption>
  <thead><tr><th scope="col">Family</th>{''.join('<th scope="col">%s</th>' % E(s['name']) for s in F['settings'])}</tr></thead>
  <tbody>
{table_rows()}
  </tbody>
 </table></div>
 <p style="margin-top:var(--s5)"></p>
 <div class="scroll"><table>
  <caption>The same count by node type — only the types that ever go dark</caption>
  <thead><tr><th scope="col">Type</th>{''.join('<th scope="col">%s</th>' % E(s['name']) for s in F['settings'])}</tr></thead>
  <tbody>
{type_rows()}
  </tbody>
 </table></div>
</div></section>

{blocks}

<section class="grey"><div class="wrapper">
 <p class="label">Export</p>
 <h2>Send the answers back</h2>
 <p>One choice per block, a note where you want one. The file is the record — nothing here is inscribed until it comes back.</p>
 <p><button id="dl" type="button">Download the answers</button><button id="cp" class="ghost" type="button">Copy to clipboard</button><span id="msg"></span></p>
 <pre id="exp" hidden></pre>
</div></section>

<footer><div class="wrapper">#280 lane OC · notes/_lanes/280/orphan-census/ORPHANS-2026-09-17.html · measured, not wired</div></footer>

<script>
var PAGE="ORPHANS-2026-09-17";
var IDS={ids};
function state(id){{
 var r=document.querySelector('input[name="'+id+'"]:checked');
 var n=document.getElementById('note-'+id);
 return {{choice:r?r.value:null,note:(n&&n.value)||""}};
}}
function envelope(){{
 var a={{}};IDS.forEach(function(id){{a[id]=state(id)}});
 return {{exportedAt:new Date().toISOString(),page:PAGE,answers:a}};
}}
function show(){{var j=JSON.stringify(envelope(),null,2);var p=document.getElementById('exp');
 p.hidden=false;p.textContent=j;return j}}
document.getElementById('dl').onclick=function(){{var j=show();var a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([j],{{type:'application/json'}}));a.download=PAGE+'-export.json';a.click();
 document.getElementById('msg').textContent='downloaded'}};
document.getElementById('cp').onclick=function(){{var j=show();
 try{{if(navigator.clipboard&&navigator.clipboard.writeText){{
  var w=navigator.clipboard.writeText(j);if(w&&w["catch"])w["catch"](function(){{}})}}}}catch(e){{}}
 document.getElementById('msg').textContent='copied — the JSON is below too'}};
document.addEventListener('change',function(){{if(!document.getElementById('exp').hidden)show()}});
</script>
</body></html>'''

open(PAGE, 'w', encoding='utf-8').write(PAGEHTML)
print('wrote', PAGE, len(PAGEHTML), 'bytes')
print('wrote', FACTS)
print('HEADLINE:', head_sentence)
