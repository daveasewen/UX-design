#!/usr/bin/env python3
"""_validate_edges.py — every edge in the knowledge graph against its row in the edge register.

Rulings: s308-D16 (Dave 2026-09-29 09:26 BST, '1. Write one edge register — Take it') and s308-D17
('2. Check every edge’s two ends against its row — Take it'). Built #308 lane E.

THE REGISTER is knowledge/_edge_register.json: one row per edge type in the graph the explorer
builds (knowledge/_build_kg_explorer.py extract() + extract_extra(), the census denominator every
other KG reader uses). This script reads it and the graph, and never writes either.

TWO CHECKS, TWO TIERS.

  --check     THE ENDS (ADVISORY, s308-D17 "advisory first"). For every edge:
                UNKNOWN-TYPE      its type has no row
                WRONG-FROM        its start's kind is not in the row's `from`
                WRONG-TO          its end's kind is not in the row's `to`
                WRONG-PAIR        both kinds are legal but the row's `pairs` do not admit the combination
                NULL-NOT-ALLOWED  a declared null on a type whose row says nulls are not legal
                OVER-COUNT        a start with more DISTINCT targets than the row's count.perStart.max
                                  (counted once per start, not per edge)
              and THE SHAPE (s308-D18 + s308-D19, #308 lane E round 2), same tier:
                SELF-LINE         an edge from a node to itself on a type whose shape.self is false
                LOOP              a cycle (named once, by its members) on a type whose shape.loops is false
                BOTH-WAYS-STORED  a symmetric type (shape.bothWays) stored in both directions for one pair
                READ-SIDE-STORED  an edge of a type whose row says it is the READ side of its opposite
                                  (opposite.stored false) — the line belongs on the opposite's side —
                                  unless the row names it in opposite.kept (s308-D35: lines Dave kept)
              and THE ACCEPTS (s308-D40, advisory first; s308-D43's four limits; #309 lane B). Every
              containedBy line, child → parent, against the parent's kind-bearing slots
              (`slots.<n>.accepts.kind`) or, with none, what the parent's KIND accepts
              (register `$containers.kinds`). Component kinds are read from each meta's `kind`
              (an alias seat is its owner's kind); a subcomponent: node is a part; a line carrying
              `part` is accepted by the parent's own part row (subComponents).
                NOT-ACCEPTED      the parent does not accept the child's kind
                CARD-HOLDS        a record (a card) holding a layout, a housing or another record
                TOO-MANY          a tile (register `$containers.tiles`) accepting through a multiple slot
                TILE-IN-TILE      a tile directly inside a tile (nest through a bento)
                MIXED-SLOTS       a sameKind slot (a carousel's slides) accepting two kinds
                MISSING           a required kind-bearing slot that accepts no line
                NO-KIND           a component meta with no kind (an alias seat excepted)
                LONE-CARD         WARNS only: a record accepted by a housing through no multiple slot
                                  (a lone card is a tile) — never turns the exit red
              and THE WHY AND THE MAKER (s308-D20 + s308-D21, #311 overnight lane D1), same tier:
                WHY-MISSING       an edge of a type whose row says why.required, carrying no `why`
                WHY-SHORT         a `why` shorter than the row's why.floor (40 on obeys, kept by s308-D20)
                NO-MAKER          an edge with no `maker` (the explorer stamps one from the row's maker rule)
                BAD-MAKER         a `maker` that is not `<hand|generated|ratified>:<by>`
                AUTHORED-FLAG     an edge still carrying the retired `authored` flag (s308-D21 replaces it)
              A node's kind is its id's prefix before the first colon. Prints COUNTS first, then every
              failure by name. Exit 1 on any failure, 0 on none — routed ADVISORY in _build_all.py, so
              the build warns and goes on.

  --coverage  THE REGISTER COVERS THE GRAPH (BLOCKING). Refuses:
                NO-ROW            a type in the graph with no row
                ROW-WITHOUT-EDGES a row whose type has no edge in the graph (invented, or retired
                                  without moving it to `$absent`)
                UNREGISTERED-NAME a type named by the meta schema, the verbs map or the explorer's
                                  FAMILY map that is neither a row nor declared in `$absent`
                ABSENT-HAS-EDGES  a `$absent` entry that now carries edges (it needs a row)
                FOLD-MISSING      a type of the older decision graph (knowledge/_decision-graph.json) that the
                                  register's `$folded` map does not name (s308-D23, #311 lane D2)
                FOLD-DANGLING     a `$folded` target that is neither a row nor a `$proposed` type
                PROPOSED-HAS-EDGES an edge in the graph of a type that is only a `$proposed` entry (make it a row)
                REGISTER-SHAPE    a row missing a checked field (incl. opposite / reads / shape), or two rows
                                  with one word
                SKIPPED-UNDECLARED an edge the explorer READ from storage and did not link, whose
                                  "<pass> <type>" is not named in the builder's SKIP_DECLARED
                                  (#308 lane L — the class that hid 14 of Dave's defaultActive
                                  answers from 1.15 to 1.31: counted, drawn by nothing, said by no one)
              Exit 1 on any. WHY BLOCKING: it had zero backlog when it was born (65 of 65), it is the
              one thing that keeps "defined once" true — the way inFamily entered with no verb — and
              the remedy is always one row, written by the lane that adds the type.

  --selftest  a control arm on the real graph and register, then one PLANTED-RED arm per refusal
              class above, each on a copy; every planted arm must go red, by exactly one.

  --json      with --check: print the counts as one JSON object instead of prose.

If the explorer module cannot be imported, the check REFUSES (exit 77, a COULD-NOT-ASK: line) —
never a silent pass. numpy, which only the explorer's layout uses, is stubbed if absent: extract()
and extract_extra() never touch it.

  python3 knowledge/_validate_edges.py --check
  python3 knowledge/_validate_edges.py --coverage
  python3 knowledge/_validate_edges.py --selftest
"""
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)  # help gate (#158)
import sys, os, io, re, json, copy, types, contextlib
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTER = os.path.join(HERE, '_edge_register.json')
ENDS_CLASSES = ('UNKNOWN-TYPE', 'WRONG-FROM', 'WRONG-TO', 'WRONG-PAIR', 'NULL-NOT-ALLOWED', 'OVER-COUNT')
COVER_CLASSES = ('NO-ROW', 'ROW-WITHOUT-EDGES', 'UNREGISTERED-NAME', 'ABSENT-HAS-EDGES', 'REGISTER-SHAPE',
                 'SKIPPED-UNDECLARED', 'FOLD-MISSING', 'FOLD-DANGLING', 'PROPOSED-HAS-EDGES')   # FOLD/PROPOSED: s308-D23 (#311 D2)
GRADES = ('exact', 'close', 'loose')                               # s308-D22: SKOS's three grades (#311 lane D2)
DECISION_GRAPH = os.path.join(HERE, '_decision-graph.json')       # s308-D23: the older ruling vocabulary
ROW_FIELDS = ('word', 'from', 'to', 'nulls', 'count', 'opposite', 'reads', 'shape', 'why', 'maker', 'outside')   # why/maker: s308-D20/D21; outside: s308-D22/D27
WHY_CLASSES = ('WHY-MISSING', 'WHY-SHORT')                         # s308-D20 (#311 lane D1)
MAKER_CLASSES = ('NO-MAKER', 'BAD-MAKER', 'AUTHORED-FLAG')         # s308-D21 (#311 lane D1)
MAKER_KINDS = ('hand', 'generated', 'ratified')                    # s308-D21: 'There are three values'
MAKER_RX = re.compile(r'^(hand|generated|ratified):\S.*$')
SHAPE_CLASSES = ('SELF-LINE', 'LOOP', 'BOTH-WAYS-STORED', 'READ-SIDE-STORED')   # s308-D18/D19 (#308 lane E r2)
SHAPE_KEYS = ('self', 'loops', 'bothWays', 'chains')
ACCEPT_CLASSES = ('NOT-ACCEPTED', 'CARD-HOLDS', 'TOO-MANY', 'TILE-IN-TILE', 'MIXED-SLOTS', 'MISSING', 'NO-KIND',
                  'LONE-CARD')   # s308-D40 / s308-D43 (#309 lane B)
ACCEPT_WARN_ONLY = ('LONE-CARD',)   # s308-D43: 'the first three refuse, and the lone-card rule warns'


class CouldNotAsk(Exception):
    pass


def kind_of(node_id):
    return str(node_id).split(':', 1)[0] if node_id else None


def load_graph(K=HERE, skips=None):
    """(nodes, edges, how) — the explorer's own extract, stdout swallowed. Pass a dict as `skips` to
    receive {'by': rep['skipped_by'], 'declared': B.SKIP_DECLARED} (#308 lane L)."""
    if K not in sys.path: sys.path.insert(0, K)
    how = '_build_kg_explorer.extract() + extract_extra()'
    try:
        import numpy  # noqa: F401 — the explorer imports it at top level for its layout only
    except ImportError:
        sys.modules['numpy'] = types.ModuleType('numpy')
        how += ' (numpy absent here: stubbed, the extract never uses it)'
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import _build_kg_explorer as B
            n, e = B.extract(K=K)
            xn, xe, _rep = B.extract_extra(n, e, K=K)
            if skips is not None:
                skips['by'] = dict(_rep.get('skipped_by') or {})
                skips['declared'] = dict(getattr(B, 'SKIP_DECLARED', {}) or {})
    except Exception as ex:
        raise CouldNotAsk(f'the explorer extract could not be run here ({type(ex).__name__}: {str(ex)[:160]})')
    nodes = {x['id']: x for x in n + xn}
    return nodes, e + xe, how


def load_register(path=REGISTER):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def register_rows(reg):
    """({word: row}, [shape problems])."""
    rows, probs = {}, []
    for i, r in enumerate(reg.get('types') or []):
        if not isinstance(r, dict):
            probs.append(f'row {i} is not an object'); continue
        miss = [f for f in ROW_FIELDS if f not in r]
        if miss:
            probs.append(f"row {i} ({r.get('word')!r}) lacks {miss}"); continue
        if r['word'] in rows:
            probs.append(f"two rows carry the word {r['word']!r}"); continue
        sh, op = r.get('shape'), r.get('opposite')
        if not (isinstance(sh, dict) and all(isinstance(sh.get(k), bool) for k in SHAPE_KEYS)):
            probs.append(f"row {r['word']!r}: shape must carry booleans {list(SHAPE_KEYS)}"); continue
        if not (isinstance(op, dict) and isinstance(op.get('stored'), bool) and 'type' in op):
            probs.append(f"row {r['word']!r}: opposite must carry `type` and a boolean `stored`"); continue
        wy, mk = r.get('why'), r.get('maker')
        if not (isinstance(wy, dict) and isinstance(wy.get('required'), bool)
                and (wy.get('floor') is None or isinstance(wy.get('floor'), int))):
            probs.append(f"row {r['word']!r}: why must carry a boolean `required` and an integer or null `floor` (s308-D20)"); continue
        if not isinstance(mk, dict):
            probs.append(f"row {r['word']!r}: maker must be an object (s308-D21)"); continue
        if mk.get('made') == 'none':
            if op.get('stored', True):
                probs.append(f"row {r['word']!r}: maker `none` is legal only on a read-side row (opposite.stored false)"); continue
        elif not (mk.get('made') in MAKER_KINDS and isinstance(mk.get('by'), str) and mk.get('by')
                  and mk.get('value') == mk['made'] + ':' + mk['by']
                  and all(isinstance(c, dict) and MAKER_RX.match(str(c.get('value') or '')) for c in mk.get('cases') or [])):
            probs.append(f"row {r['word']!r}: maker must say made (one of {list(MAKER_KINDS)}), by, and value = made:by (s308-D21)"); continue
        ou = r.get('outside')
        if not (isinstance(ou, dict) and ou.get('grade') in GRADES + (None,) and (ou.get('term') is None) == (ou.get('grade') is None)
                and isinstance(ou.get('name'), dict) and isinstance(ou['name'].get('adopted'), bool)):
            probs.append(f"row {r['word']!r}: outside must carry a term graded one of {list(GRADES)} (or both null) and a "
                         f"`name` with a boolean `adopted` (s308-D22/D27)"); continue
        rows[r['word']] = r
    return rows, probs


def named_types(K=HERE):
    """{type: {where it is named}} across the files that each hold a partial definition today."""
    out = defaultdict(set)
    try:
        s = json.load(open(os.path.join(K, 'components', 'meta.schema.json'), encoding='utf-8'))
        for t in (s.get('properties', {}).get('edges', {}).get('properties') or {}):
            if not t.startswith('$'): out[t].add('meta.schema.json')
    except Exception:
        pass
    try:
        v = json.load(open(os.path.join(K, '_kg_verbs.json'), encoding='utf-8'))
        for k, x in v.items():
            if k == 'unread' and isinstance(x, dict):
                for t in x: out[t].add('_kg_verbs.json unread')
            elif not k.startswith('$') and isinstance(x, dict):
                for t in x.get('reads') or []: out[t].add('_kg_verbs.json ' + k)
    except Exception:
        pass
    try:
        tpl = open(os.path.join(K, '_kg_explorer.template.html'), encoding='utf-8').read()
        m = re.search(r'const FAMILY\s*=\s*\{(.*?)\};', tpl, re.S)
        if m:
            body = re.sub(r'//[^\n]*', '', m.group(1))
            for t in re.findall(r'([A-Za-z_]\w*)\s*:\s*[\'"]', body): out[t].add('_kg_explorer.template.html FAMILY')
    except Exception:
        pass
    return dict(out)


def check_ends(edges, rows):
    """{'checked', 'pass', 'fail', 'byClass', 'byClassType', 'failures'}; failures are (class, type, s, t, detail)."""
    failures, bad = [], set()
    targets = defaultdict(set)
    for i, e in enumerate(edges):
        ty, s, t = e.get('type'), e.get('s'), e.get('t')
        row = rows.get(ty)
        if row is None:
            failures.append(('UNKNOWN-TYPE', ty, s, t, 'no row in the register')); bad.add(i); continue
        fk = kind_of(s)
        if fk not in row['from']:
            failures.append(('WRONG-FROM', ty, s, t, f"starts on {fk!r}; the row allows {row['from']}")); bad.add(i)
        if t is None:
            if not (row.get('nulls') or {}).get('allowed'):
                failures.append(('NULL-NOT-ALLOWED', ty, s, t, 'a declared null; the row says nulls are not legal')); bad.add(i)
            continue
        tk = kind_of(t)
        if tk not in row['to']:
            failures.append(('WRONG-TO', ty, s, t, f"ends on {tk!r}; the row allows {row['to']}")); bad.add(i)
        elif row.get('pairs') and fk in row['from'] and [fk, tk] not in row['pairs']:
            failures.append(('WRONG-PAIR', ty, s, t, f"{fk}→{tk} is not one of the row's pairs {row['pairs']}")); bad.add(i)
        targets[(ty, s)].add(t)
    for (ty, s), ts in sorted(targets.items()):
        mx = ((rows[ty].get('count') or {}).get('perStart') or {}).get('max')
        if mx is not None and len(ts) > mx:
            failures.append(('OVER-COUNT', ty, s, None, f'{len(ts)} distinct targets; the row allows at most {mx}'))
    byc, bycT = Counter(), defaultdict(Counter)
    for c, ty, *_ in failures:
        byc[c] += 1; bycT[c][ty] += 1
    return {'checked': len(edges), 'pass': len(edges) - len(bad), 'fail': len(bad),
            'byClass': {c: byc[c] for c in ENDS_CLASSES}, 'byClassType': {c: dict(bycT[c]) for c in bycT},
            'failures': failures}


def check_shape(edges, rows):
    """s308-D18 + s308-D19 (#308 lane E round 2). {'byClass', 'byClassType', 'failures'}; a failure is
    (class, type, s, t, detail). SELF-LINE and READ-SIDE-STORED count edges, LOOP counts cycles, BOTH-WAYS-STORED
    counts unordered pairs."""
    failures = []
    pairs = defaultdict(set)
    for e in edges:
        ty, s, t = e.get('type'), e.get('s'), e.get('t')
        row = rows.get(ty)
        if row is None or t is None:
            continue
        sh, op = row.get('shape') or {}, row.get('opposite') or {}
        if not op.get('stored', True) and [s, t] not in (op.get('kept') or []):   # s308-D35: lines Dave kept, named
            failures.append(('READ-SIDE-STORED', ty, s, t, f"{ty} is read as {op.get('type')} walked backwards; the line belongs on that side"))
        if s == t and not sh.get('self', True):
            failures.append(('SELF-LINE', ty, s, t, 'points at itself; the shape says it may not'))
        pairs[ty].add((s, t))
    for ty, P in sorted(pairs.items()):
        sh = rows[ty].get('shape') or {}
        if sh.get('bothWays'):
            for (a, b) in sorted(P):
                if a < b and (b, a) in P:
                    failures.append(('BOTH-WAYS-STORED', ty, a, b, 'a symmetric fact stored in both directions; store it once'))
        if not sh.get('loops', True):
            for cyc in _cycles({(a, b) for (a, b) in P if a != b}):
                failures.append(('LOOP', ty, cyc[0], cyc[-1], 'a loop: ' + ' → '.join(cyc + [cyc[0]])))
    byc, bycT = Counter(), defaultdict(Counter)
    for c, ty, *_ in failures:
        byc[c] += 1; bycT[c][ty] += 1
    return {'byClass': {c: byc[c] for c in SHAPE_CLASSES}, 'byClassType': {c: dict(bycT[c]) for c in bycT}, 'failures': failures}


def check_why_maker(edges, rows):
    """s308-D20 + s308-D21 (#311 overnight lane D1). {'byClass', 'byClassType', 'failures'}; a failure is
    (class, type, s, t, detail). One count per edge per class."""
    failures = []
    for e in edges:
        ty, s, t = e.get('type'), e.get('s'), e.get('t')
        row = rows.get(ty)
        if row is None:
            continue
        wy = row.get('why') or {}
        why = e.get('why')
        if wy.get('required') and not (isinstance(why, str) and why.strip()):
            failures.append(('WHY-MISSING', ty, s, t, 'a required reason is missing (s308-D20)'))
        elif wy.get('floor') and isinstance(why, str) and why.strip() and len(why.strip()) < wy['floor']:
            failures.append(('WHY-SHORT', ty, s, t, f"why is {len(why.strip())} characters; the floor is {wy['floor']}"))
        mk = e.get('maker')
        if not mk:
            failures.append(('NO-MAKER', ty, s, t, 'no maker on the edge (s308-D21)'))
        elif not MAKER_RX.match(str(mk)):
            failures.append(('BAD-MAKER', ty, s, t, f"maker {str(mk)[:40]!r} is not <hand|generated|ratified>:<by>"))
        if 'authored' in e:
            failures.append(('AUTHORED-FLAG', ty, s, t, 'the retired authored flag is still on the edge (s308-D21)'))
    byc, bycT = Counter(), defaultdict(Counter)
    for c, ty, *_ in failures:
        byc[c] += 1; bycT[c][ty] += 1
    return {'byClass': {c: byc[c] for c in WHY_CLASSES + MAKER_CLASSES}, 'byClassType': {c: dict(bycT[c]) for c in bycT},
            'failures': failures}


def print_why_maker(wm):
    f = {c: n for c, n in wm['byClass'].items() if n}
    print(f"WHY+MAKER COUNTS: {f or 'none'}")
    for c in WHY_CLASSES + MAKER_CLASSES:
        if wm['byClass'][c]:
            print(f"  {c}: {wm['byClass'][c]} — by type {wm['byClassType'][c]}")
    for c, ty, s, t, d in wm['failures']:
        print(f"  ✗ {c:16} {ty:18} {s} → {t}   {d}")
    print('EDGE WHY: ' + ('every required reason is present' if not any(wm['byClass'][c] for c in WHY_CLASSES)
                          else 'FAILURES above (ADVISORY, s308-D20)'))
    print('EDGE MAKER: ' + ('every edge names its maker, none carries authored' if not any(wm['byClass'][c] for c in MAKER_CLASSES)
                            else 'FAILURES above (ADVISORY, s308-D21)'))


def load_metas(K=HERE):
    """{'component:<stem>': meta} for every knowledge/components/<stem>.meta.json."""
    d = os.path.join(K, 'components')
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith('.meta.json'):
            with open(os.path.join(d, f), encoding='utf-8') as fh:
                out['component:' + f[:-len('.meta.json')]] = json.load(fh)
    return out


def node_kind(nid, metas):
    """The container kind of a node: a subcomponent is a part; a component is its meta's `kind`, an alias
    seat its owner's; anything else has none (None)."""
    if kind_of(nid) == 'subcomponent':
        return 'part'
    m = metas.get(nid)
    if not isinstance(m, dict):
        return None
    if isinstance(m.get('aliasOf'), dict):
        own = m['aliasOf'].get('component')
        return node_kind(own, metas) if own and own != nid else None
    return m.get('kind')


def kind_slots(meta):
    """{slot: slotEntry} for the slots that say which kinds they accept."""
    sl = (meta or {}).get('slots')
    return {n: v for n, v in (sl.items() if isinstance(sl, dict) else [])
            if not n.startswith('$') and isinstance(v, dict) and ((v.get('accepts') or {}).get('kind'))}


def check_accepts(edges, metas, containers):
    """s308-D40 + s308-D43 (#309 lane B). {'lines', 'accepted', 'derived', 'byClass', 'failures'}; a failure is
    (class, 'containedBy', s, t, detail). `derived` lists (s, t, slot) for every line a kind-bearing slot accepted."""
    kinds = containers.get('kinds') or {}
    tiles = set(containers.get('tiles') or [])
    failures, derived, filled = [], [], defaultdict(list)
    for nid, m in sorted(metas.items()):
        if isinstance(m, dict) and 'aliasOf' not in m and m.get('kind') not in kinds:
            failures.append(('NO-KIND', 'containedBy', nid, None, f"declares kind {m.get('kind')!r}; one of {sorted(kinds)} is required"))
    lines = [e for e in edges if e.get('type') == 'containedBy' and e.get('t')]
    accepted = 0
    for e in lines:
        s, t = e['s'], e['t']
        ck, pk = node_kind(s, metas), node_kind(t, metas)
        if ck not in kinds or pk not in kinds:
            continue            # NO-KIND names the meta; the line cannot be judged without it
        pm = metas.get(t) or {}
        part = e.get('part') or (s.split('/', 1)[1] if kind_of(s) == 'subcomponent' and s.startswith(
            'subcomponent:' + t.split(':', 1)[1] + '/') else None)
        if part:                  # a part line (s308-D18) or a subcomponent (s308-D26): the parent's own part row
            sc = pm.get('subComponents')
            if isinstance(sc, dict) and part in sc:
                accepted += 1; continue
            failures.append(('NOT-ACCEPTED', 'containedBy', s, t, f"names part {part!r}, which {t}'s subComponents do not")); continue
        if ck in (kinds[pk].get('never') or []):
            failures.append(('CARD-HOLDS', 'containedBy', s, t, f"a {pk} (a card) holding a {ck}; a card never holds a layout, a housing or another record")); continue
        if s in tiles and t in tiles:
            failures.append(('TILE-IN-TILE', 'containedBy', s, t, 'a tile directly inside a tile; nest through a bento')); continue
        slots = kind_slots(pm)
        slot = None
        if ck == 'part' and ck in (kinds[pk].get('accepts') or []):
            ok = True                 # a part fills its parent's part row, not a content slot
        elif slots:
            slot = next((n for n, v in slots.items() if ck in v['accepts']['kind']), None)
            ok = slot is not None
        else:
            ok = ck in (kinds[pk].get('accepts') or [])
        if not ok:
            where = (f"its slots accept {sorted({k for v in slots.values() for k in v['accepts']['kind']})}" if slots
                     else f"a {pk} accepts {kinds[pk].get('accepts')}")
            failures.append(('NOT-ACCEPTED', 'containedBy', s, t, f"a {ck} in a {pk}; {where}")); continue
        accepted += 1
        sv = slots.get(slot) if slot else None
        if slot:
            derived.append((s, t, slot)); filled[(t, slot)].append((ck, s))
        if t in tiles and sv and sv.get('multiple'):
            failures.append(('TOO-MANY', 'containedBy', s, t, f"tile slot {slot!r} is multiple; a tile holds exactly one thing"))
        if ck == 'record' and pk == 'housing' and not (sv and sv.get('multiple')):
            failures.append(('LONE-CARD', 'containedBy', s, t, 'a record alone in a housing: a lone card is a tile (warns)'))
    for (t, slot), kids in sorted(filled.items()):
        if kind_slots(metas.get(t)).get(slot, {}).get('sameKind') and len({k for k, _ in kids}) > 1:
            failures.append(('MIXED-SLOTS', 'containedBy', None, t, f"slot {slot!r} holds {sorted({k for k, _ in kids})}; its slides all hold the same kind"))
    for t, m in sorted(metas.items()):
        for n, v in kind_slots(m).items():
            if v.get('required') and not filled.get((t, n)):
                failures.append(('MISSING', 'containedBy', None, t, f"required slot {n!r} (accepts {v['accepts']['kind']}) accepts no containedBy line"))
    byc = Counter(c for c, *_ in failures)
    return {'lines': len(lines), 'accepted': accepted, 'derived': derived,
            'byClass': {c: byc[c] for c in ACCEPT_CLASSES}, 'failures': failures,
            'refusals': sum(n for c, n in byc.items() if c not in ACCEPT_WARN_ONLY)}


def print_accepts(acc):
    shown = {c: n for c, n in acc['byClass'].items() if n}
    print(f"  accepts: {acc['lines']} containedBy lines · accepted {acc['accepted']} · through a kind-bearing slot "
          f"{len(acc['derived'])} · by class {shown or 'none'}")
    for s, t, slot in acc['derived']:
        print(f"  · derived: {t} accepts {s} (slot {slot!r}, by kind)")
    for c, ty, s, t, d in acc['failures']:
        print(f"  {'!' if c in ACCEPT_WARN_ONLY else '✗'} {c:16} {ty:18} {s} → {t}   {d}")
    print('EDGE ACCEPTS: ' + ('every containedBy line is accepted by its parent' if not acc['refusals']
                              else 'REFUSALS above (ADVISORY first, s308-D40)')
          + (f" · warnings {sum(acc['byClass'][c] for c in ACCEPT_WARN_ONLY)}" if any(acc['byClass'][c] for c in ACCEPT_WARN_ONLY) else ''))


def _cycles(P):
    """The strongly connected components of size > 1 (Tarjan, iterative), each as a sorted member list — one
    report per loop, whatever its length."""
    adj = defaultdict(list)
    for a, b in P: adj[a].append(b)
    index, low, onstack, stack, out, n = {}, {}, set(), [], [], [0]
    for root in sorted(adj):
        if root in index: continue
        work = [(root, iter(sorted(adj[root])))]
        index[root] = low[root] = n[0]; n[0] += 1; stack.append(root); onstack.add(root)
        while work:
            v, it = work[-1]
            w = next(it, None)
            if w is not None:
                if w not in index:
                    index[w] = low[w] = n[0]; n[0] += 1; stack.append(w); onstack.add(w)
                    work.append((w, iter(sorted(adj[w]))))
                elif w in onstack:
                    low[v] = min(low[v], index[w])
                continue
            work.pop()
            if work: low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    x = stack.pop(); onstack.discard(x); comp.append(x)
                    if x == v: break
                if len(comp) > 1: out.append(sorted(comp))
    return out


def check_coverage(edges, reg, names, skips=None):
    rows, probs = register_rows(reg)
    live = Counter(e.get('type') for e in edges)
    absent = reg.get('$absent') or {}
    out = [('REGISTER-SHAPE', p) for p in probs]
    out += [('NO-ROW', f'{t} ({live[t]} edges in the graph)') for t in sorted(live) if t not in rows]
    out += [('ROW-WITHOUT-EDGES', t) for t in sorted(rows) if not live.get(t)
            and (rows[t].get('opposite') or {}).get('stored', True)]   # a READ-side row (s308-D18) stores nothing
    out += [('UNREGISTERED-NAME', f"{t} (named in {sorted(w)})") for t, w in sorted(names.items())
            if t not in rows and t not in absent]
    out += [('ABSENT-HAS-EDGES', f'{t} ({live[t]} edges)') for t in sorted(absent) if live.get(t)]
    # s308-D23 (#311 lane D2): ONE ruling-to-ruling vocabulary — every older type folded, every target real
    folded = ((reg.get('$folded') or {}).get('types')) or {}
    proposed = ((reg.get('$proposed') or {}).get('types')) or {}
    out += [('FOLD-MISSING', f'{t} (used by the older decision graph; name it in $folded)') for t in sorted(older_types())
            if t not in folded]
    out += [('FOLD-DANGLING', f"{t} → {(v or {}).get('to')!r} (no row and no $proposed entry)") for t, v in sorted(folded.items())
            if (v or {}).get('to') not in rows and (v or {}).get('to') not in proposed]
    out += [('PROPOSED-HAS-EDGES', f'{t} ({live[t]} edges; a proposal carrying edges needs a row)') for t in sorted(proposed)
            if live.get(t)]
    sk = skips or {}
    out += [('SKIPPED-UNDECLARED', f"{k} ({n} edge(s) read from storage and not linked) — draw it, or name it in "
             f"_build_kg_explorer.SKIP_DECLARED with the reason")
            for k, n in sorted((sk.get('by') or {}).items()) if k not in (sk.get('declared') or {})]
    return out


def older_types(path=DECISION_GRAPH):
    """The edge types the older decision graph spells (s308-D23). A missing file is an empty set."""
    try:
        d = json.load(open(path, encoding='utf-8'))
    except (OSError, ValueError):
        return set()
    return {e.get('type') for e in d.get('edges') or [] if isinstance(e, dict) and e.get('type')}


def drift(edges, rows):
    live = Counter(e.get('type') for e in edges)
    return [(t, (r.get('$measured') or {}).get('edges'), live.get(t, 0)) for t, r in sorted(rows.items())
            if (r.get('$measured') or {}).get('edges') is not None and r['$measured']['edges'] != live.get(t, 0)]


def print_ends(res, rows, how, dr, shp=None):
    fails = {c: n for c, n in res['byClass'].items() if n}
    shf = {c: n for c, n in ((shp or {}).get('byClass') or {}).items() if n}
    print(f"COUNTS: types registered {len(rows)} · edges checked {res['checked']} · pass {res['pass']} · fail {res['fail']}"
          f" · by class {fails or 'none'} · shape {shf or 'none'}")
    print(f"  graph: {how}")
    for c in ENDS_CLASSES:
        if res['byClass'][c]:
            print(f"  {c}: {res['byClass'][c]} — by type {res['byClassType'][c]}")
    for c, ty, s, t, d in res['failures']:
        print(f"  ✗ {c:16} {ty:18} {s} → {t}   {d}")
    for c in SHAPE_CLASSES:
        if shf.get(c):
            print(f"  {c}: {shf[c]} — by type {shp['byClassType'][c]}")
    for c, ty, s, t, d in (shp or {}).get('failures') or []:
        print(f"  ✗ {c:16} {ty:18} {s} → {t}   {d}")
    for t, was, now in dr:
        print(f"  · drift (not a failure): {t} {was} → {now} edges since the row was measured")
    print('EDGE ENDS: ' + ('all edges match their rows' if not res['fail'] and not res['byClass']['OVER-COUNT']
                           else 'FAILURES above (ADVISORY, s308-D17)'))
    print('EDGE SHAPE: ' + ('every edge matches its type\'s shape and stored side' if not shf
                            else 'FAILURES above (ADVISORY, s308-D18/D19)'))


def main(argv):
    if '--selftest' in argv:
        return selftest()
    skips = {}
    try:
        nodes, edges, how = load_graph(skips=skips)
    except CouldNotAsk as ex:
        print(f'COULD-NOT-ASK: {ex}'); return 77
    reg = load_register()
    rows, _ = register_rows(reg)
    if '--coverage' in argv:
        probs = check_coverage(edges, reg, named_types(), skips)
        print(f"COUNTS: rows {len(rows)} · graph types {len(set(e.get('type') for e in edges))} · declared absent "
              f"{len(reg.get('$absent') or {})} · skipped on read {sum((skips.get('by') or {}).values())}"
              f" (declared {len(skips.get('declared') or {})}) · refusals {len(probs)}")
        for c, d in probs: print(f'  ✗ {c:18} {d}')
        print('EDGE REGISTER COVERAGE: ' + ('OK' if not probs else 'REFUSED (BLOCKING) — add or fix the row(s) in knowledge/_edge_register.json'))
        return 1 if probs else 0
    res = check_ends(edges, rows)
    shp = check_shape(edges, rows)
    acc = check_accepts(edges, load_metas(), reg.get('$containers') or {})
    wm = check_why_maker(edges, rows)
    if '--json' in argv:
        out = {k: v for k, v in res.items() if k != 'failures'}
        out['shape'] = {k: v for k, v in shp.items() if k != 'failures'}
        out['accepts'] = {k: v for k, v in acc.items() if k not in ('failures', 'derived')}
        out['whyMaker'] = {k: v for k, v in wm.items() if k != 'failures'}
        print(json.dumps(out, sort_keys=True))
    else:
        print_ends(res, rows, how, drift(edges, rows), shp)
        print_accepts(acc)
        print_why_maker(wm)
    return 1 if (res['fail'] or res['byClass']['OVER-COUNT'] or any(shp['byClass'].values()) or acc['refusals']
                 or any(wm['byClass'].values())) else 0


# ------------------------------------------------------------------ selftest
def selftest():
    ok_all = True

    def bite(n, desc, cond):
        nonlocal ok_all
        try: ok = bool(cond())
        except Exception as ex: ok = False; desc += f'  [raised {type(ex).__name__}: {ex}]'
        ok_all &= ok
        print(f"  {'✓' if ok else '✗'} {n:>2} {desc}")

    skips = {}
    try:
        nodes, edges, how = load_graph(skips=skips)
    except CouldNotAsk as ex:
        print(f'COULD-NOT-ASK: {ex}'); return 77
    reg = load_register(); rows, probs = register_rows(reg); names = named_types()
    base = check_ends(edges, rows)
    cov = check_coverage(edges, reg, names, skips)
    print(f'_validate_edges selftest — control on the real graph ({len(edges)} edges, {len(rows)} rows), then one planted red per refusal')

    # control: the tool, not the graph — the real graph's verdict is whatever it is today
    bite(0, f"CONTROL: register parses clean, every edge classified once (pass {base['pass']} + fail {base['fail']} = {len(edges)}), "
            f"a second run agrees; coverage on the real graph: {len(cov)} refusal(s)",
         lambda: not probs and base['pass'] + base['fail'] == base['checked'] == len(edges)
         and check_ends(edges, rows)['byClass'] == base['byClass'])

    def real(kind_):
        return next(i for i in sorted(nodes) if kind_of(i) == kind_)
    comp, rul, rule, logo = real('component'), real('ruling'), real('rule'), real('logo')
    ux, snip = real('ux'), real('snippet')

    def planted(cls, e):
        r = check_ends(edges + [e], rows)
        return r['byClass'][cls] == base['byClass'][cls] + 1 and r['fail'] + r['byClass']['OVER-COUNT'] > base['fail'] + base['byClass']['OVER-COUNT']

    bite(1, 'UNKNOWN-TYPE: a type with no row goes red', lambda: planted('UNKNOWN-TYPE', {'s': comp, 't': rul, 'type': 'noSuchEdgeType'}))
    bite(2, "WRONG-FROM: governedBy from a logo (the s308-D17 case) goes red", lambda: planted('WRONG-FROM', {'s': logo, 't': rul, 'type': 'governedBy'}))
    bite(3, 'WRONG-TO: governedBy ending on a rule goes red', lambda: planted('WRONG-TO', {'s': comp, 't': rule, 'type': 'governedBy'}))
    bite(4, 'WRONG-PAIR: obeys from a logo to a principle goes red (both kinds legal, pair not)',
         lambda: planted('WRONG-PAIR', {'s': logo, 't': ux, 'type': 'obeys'}))
    bite(5, 'NULL-NOT-ALLOWED: a declared null on bindsToken goes red', lambda: planted('NULL-NOT-ALLOWED', {'s': comp, 't': None, 'type': 'bindsToken'}))
    rend = next(e for e in edges if e['type'] == 'renderedBy')
    other = next(i for i in nodes if kind_of(i) == 'snippet' and i != rend['t'])
    bite(6, 'OVER-COUNT: a second renderedBy snippet on one component goes red (max 1)',
         lambda: planted('OVER-COUNT', {'s': rend['s'], 't': other, 'type': 'renderedBy'}))

    def cov_red(cls, e2=None, reg2=None, names2=None, skips2=None):
        c = check_coverage(e2 if e2 is not None else edges, reg2 if reg2 is not None else reg,
                           names2 if names2 is not None else names, skips2 if skips2 is not None else skips)
        return sum(1 for k, _ in c if k == cls) == sum(1 for k, _ in cov if k == cls) + 1
    r1 = copy.deepcopy(reg); gone = r1['types'].pop(0)['word']
    bite(7, f'NO-ROW: the register without its {gone!r} row goes red', lambda: cov_red('NO-ROW', reg2=r1))
    r2 = copy.deepcopy(reg); r2['types'].append(dict(copy.deepcopy(r2['types'][0]), word='ghostEdgeType'))
    bite(8, 'ROW-WITHOUT-EDGES: a row for a type with no edges goes red', lambda: cov_red('ROW-WITHOUT-EDGES', reg2=r2))
    n3 = dict(names); n3['strayEdgeType'] = {'_kg_verbs.json unread'}
    bite(9, 'UNREGISTERED-NAME: a type the verbs map names, with no row and no $absent entry, goes red',
         lambda: cov_red('UNREGISTERED-NAME', names2=n3))
    r4 = copy.deepcopy(reg); r4.setdefault('$absent', {})['governs'] = {'why': 'planted'}
    bite(10, 'ABSENT-HAS-EDGES: a $absent entry whose type carries edges goes red', lambda: cov_red('ABSENT-HAS-EDGES', reg2=r4))
    r5 = copy.deepcopy(reg); r5['types'].append(copy.deepcopy(r5['types'][1]))
    bite(11, 'REGISTER-SHAPE: two rows with one word go red', lambda: cov_red('REGISTER-SHAPE', reg2=r5))
    r6 = copy.deepcopy(reg); del r6['types'][2]['from']
    bite(12, "REGISTER-SHAPE: a row without `from` goes red", lambda: cov_red('REGISTER-SHAPE', reg2=r6))
    bite(13, 'the exit is red when a planted failure is present (check_ends → non-zero verdict)',
         lambda: check_ends(edges + [{'s': comp, 't': None, 'type': 'noSuchEdgeType'}], rows)['fail'] > 0)
    s14 = {'by': dict(skips.get('by') or {}, **{'asset plantedSkipType': 14}), 'declared': dict(skips.get('declared') or {})}
    bite(14, "SKIPPED-UNDECLARED: an edge type read and not linked, with no SKIP_DECLARED line, goes red (the defaultActive class)",
         lambda: cov_red('SKIPPED-UNDECLARED', skips2=s14))
    s15 = {'by': s14['by'], 'declared': dict(s14['declared'], **{'asset plantedSkipType': 'planted: declared with its reason'})}
    bite(15, "SKIPPED-UNDECLARED: the same skip DECLARED with its reason does not go red",
         lambda: sum(1 for k, _ in check_coverage(edges, reg, names, s15) if k == 'SKIPPED-UNDECLARED')
         == sum(1 for k, _ in cov if k == 'SKIPPED-UNDECLARED'))
    bite(16, "the real extract reports its skips by type (the tally exists, whatever it holds today)",
         lambda: isinstance(skips.get('by'), dict) and isinstance(skips.get('declared'), dict))
    # — s308-D18 / s308-D19 (#308 lane E round 2): the shape and the stored side
    shp0 = check_shape(edges, rows)

    def shape_red(cls, planted):
        return check_shape(edges + planted, rows)['byClass'][cls] == shp0['byClass'][cls] + 1
    comps = sorted(i for i in nodes if kind_of(i) == 'component')
    a_, b_, c_ = comps[0], comps[1], comps[2]
    bite(17, 'SELF-LINE: a containedBy line from a component to itself goes red',
         lambda: shape_red('SELF-LINE', [{'s': a_, 't': a_, 'type': 'containedBy'}]))
    bite(18, 'LOOP: a three-step composedOf loop goes red, once',
         lambda: shape_red('LOOP', [{'s': a_, 't': b_, 'type': 'composedOf'}, {'s': b_, 't': c_, 'type': 'composedOf'},
                                    {'s': c_, 't': a_, 'type': 'composedOf'}]))
    tw = next(e for e in edges if e['type'] == 'tensionWith' and e.get('t'))
    bite(19, 'BOTH-WAYS-STORED: a tensionWith line stored the other way round too goes red',
         lambda: shape_red('BOTH-WAYS-STORED', [{'s': tw['t'], 't': tw['s'], 'type': 'tensionWith'}]))
    bite(20, 'READ-SIDE-STORED: a hasPart line (the read side of containedBy) goes red',
         lambda: shape_red('READ-SIDE-STORED', [{'s': b_, 't': a_, 'type': 'hasPart'}]))
    bite(21, 'LOOP is not raised on a type whose shape allows loops (a consumes two-step loop stays quiet)',
         lambda: check_shape(edges + [{'s': a_, 't': b_, 'type': 'consumes'}, {'s': b_, 't': a_, 'type': 'consumes'}],
                             rows)['byClass']['LOOP'] == shp0['byClass']['LOOP'])
    r22 = copy.deepcopy(reg); r22['types'][3]['shape'].pop('chains')
    bite(22, 'REGISTER-SHAPE: a row whose shape lacks `chains` goes red', lambda: cov_red('REGISTER-SHAPE', reg2=r22))
    r23 = copy.deepcopy(reg); r23['types'][4]['opposite'] = {'type': None}
    bite(23, 'REGISTER-SHAPE: a row whose opposite has no boolean `stored` goes red', lambda: cov_red('REGISTER-SHAPE', reg2=r23))
    r24 = copy.deepcopy(reg); w24 = next(r for r in r24['types'] if r['word'] == 'hasPart')
    bite(24, 'ROW-WITHOUT-EDGES spares a READ-side row (hasPart, 0 edges), and still refuses it once it claims to be stored',
         lambda: not any(k == 'ROW-WITHOUT-EDGES' and d == 'hasPart' for k, d in cov)
         and (w24['opposite'].__setitem__('stored', True) or True)
         and (w24.__setitem__('maker', {'made': 'generated', 'by': 'planted.py', 'value': 'generated:planted.py'}) or True)
         and any(k == 'ROW-WITHOUT-EDGES' and d == 'hasPart' for k, d in check_coverage(edges, r24, names, skips)))
    gb_row = rows.get('governedBy') or {}
    kept = (gb_row.get('opposite') or {}).get('kept') or []
    bite(25, "READ-SIDE-STORED spares a governedBy line the row names in opposite.kept (s308-D35), and still refuses one it does not",
         lambda: bool(kept)
         and check_shape(edges + [{'s': kept[0][0], 't': kept[0][1], 'type': 'governedBy'}], rows)['byClass']['READ-SIDE-STORED']
         == shp0['byClass']['READ-SIDE-STORED']
         and shape_red('READ-SIDE-STORED', [{'s': kept[0][0], 't': 'ruling:s001-D1', 'type': 'governedBy'}]))
    # — s308-D40 / s308-D43 (#309 lane B): the accepts check and the four nesting limits
    metas, cont = load_metas(), reg.get('$containers') or {}
    acc0 = check_accepts(edges, metas, cont)

    def acc_red(cls, e2=None, metas2=None, cont2=None):
        a = check_accepts(e2 if e2 is not None else edges, metas2 if metas2 is not None else metas,
                          cont2 if cont2 is not None else cont)
        return a['byClass'][cls] == acc0['byClass'][cls] + 1
    CB = lambda s_, t_: {'s': 'component:' + s_, 't': 'component:' + t_, 'type': 'containedBy'}
    d34 = ('component:cards', 'component:carousel', 'slides')
    bite(26, f"CONTROL (accepts): {acc0['lines']} containedBy lines judged, {acc0['accepted']} accepted, "
             f"{acc0['refusals']} refusal(s) on the real tree; s308-D34 'a carousel holds cards' is DERIVED — Cards (record) "
             f"accepted by Carousel's slides slot, no authored pair",
         lambda: d34 in acc0['derived'] and check_accepts(edges, metas, cont)['byClass'] == acc0['byClass'])
    bite(27, "CARD-HOLDS: the s308-D34 line reversed (a carousel inside Cards) goes red",
         lambda: acc_red('CARD-HOLDS', edges + [CB('carousel', 'cards')]))
    bite(28, "NOT-ACCEPTED: a layout (template-dashboard) inside a block (button) goes red",
         lambda: acc_red('NOT-ACCEPTED', edges + [CB('template-dashboard', 'button')]))
    c29 = dict(cont, tiles=['component:drawer', 'component:modals'])
    bite(29, "TILE-IN-TILE: with two housings declared tiles, one directly inside the other goes red",
         lambda: acc_red('TILE-IN-TILE', edges + [CB('drawer', 'modals')], cont2=c29))
    c30 = dict(cont, tiles=['component:carousel'])
    bite(30, "TOO-MANY: a tile whose accepting slot is multiple (Carousel planted as a tile) goes red",
         lambda: acc_red('TOO-MANY', cont2=c30))
    bite(31, "MIXED-SLOTS: an image block beside Cards in Carousel's slides goes red",
         lambda: acc_red('MIXED-SLOTS', edges + [CB('image-block', 'carousel')]))
    bite(32, "MISSING: Carousel's required slides slot with its one line taken away goes red",
         lambda: acc_red('MISSING', [e for e in edges if not (e['type'] == 'containedBy' and (e['s'], e['t']) == d34[:2])]))
    m33 = copy.deepcopy(metas); m33['component:button'].pop('kind', None)
    bite(33, "NO-KIND: Button without its kind goes red", lambda: acc_red('NO-KIND', metas2=m33))
    bite(34, "LONE-CARD WARNS: a record alone in a housing (account-card in a drawer) is named, and the refusal count does not move",
         lambda: acc_red('LONE-CARD', edges + [CB('account-card', 'drawer')])
         and check_accepts(edges + [CB('account-card', 'drawer')], metas, cont)['refusals'] == acc0['refusals'])
    # — s308-D20 / s308-D21 (#311 overnight lane D1): the one why and the one maker
    wm0 = check_why_maker(edges, rows)

    def wm_red(cls, planted):
        return check_why_maker(edges + planted, rows)['byClass'][cls] == wm0['byClass'][cls] + 1
    ob = next(e for e in edges if e['type'] == 'obeys' and e.get('t'))
    bite(35, f"CONTROL (why+maker): every real edge names its maker ({wm0['byClass']['NO-MAKER']} without) and none carries authored "
             f"({wm0['byClass']['AUTHORED-FLAG']}); the why backlog on the real graph is {wm0['byClass']['WHY-MISSING']} missing",
         lambda: wm0['byClass']['NO-MAKER'] == 0 and wm0['byClass']['AUTHORED-FLAG'] == 0 and wm0['byClass']['BAD-MAKER'] == 0)
    bite(36, 'WHY-MISSING: an obeys line with no why goes red',
         lambda: wm_red('WHY-MISSING', [dict(ob, why=None)]))
    bite(37, 'WHY-SHORT: an obeys line whose why is 12 characters (floor 40) goes red',
         lambda: wm_red('WHY-SHORT', [dict(ob, why='because so.')]))
    bt = next(e for e in edges if e['type'] == 'bindsToken')
    bite(38, 'WHY-MISSING is not raised on generated structure (a bindsToken line with no why stays quiet)',
         lambda: check_why_maker(edges + [dict(bt, why=None)], rows)['byClass']['WHY-MISSING'] == wm0['byClass']['WHY-MISSING'])
    bite(39, 'NO-MAKER: an edge with no maker goes red',
         lambda: wm_red('NO-MAKER', [{k: v for k, v in bt.items() if k != 'maker'}]))
    bite(40, "BAD-MAKER: a maker outside the three values ('drawn:solid') goes red",
         lambda: wm_red('BAD-MAKER', [dict(bt, maker='drawn:solid')]))
    bite(41, 'AUTHORED-FLAG: an edge still carrying authored goes red',
         lambda: wm_red('AUTHORED-FLAG', [dict(bt, authored=True)]))
    r42 = copy.deepcopy(reg); r42['types'][5].pop('why')
    bite(42, 'REGISTER-SHAPE: a row without `why` goes red', lambda: cov_red('REGISTER-SHAPE', reg2=r42))
    r43 = copy.deepcopy(reg); r43['types'][6]['maker'] = dict(r43['types'][6]['maker'], made='solid')
    bite(43, "REGISTER-SHAPE: a row whose maker is 'solid' (not one of the three) goes red", lambda: cov_red('REGISTER-SHAPE', reg2=r43))
    # — s308-D22/D27 + s308-D23 (#311 overnight lane D2): the outside column and the fold
    r44 = copy.deepcopy(reg); r44['types'][3]['outside'] = dict(r44['types'][3]['outside'], grade='near')
    bite(44, "REGISTER-SHAPE: a row whose outside grade is 'near' (not exact / close / loose) goes red", lambda: cov_red('REGISTER-SHAPE', reg2=r44))
    r45 = copy.deepcopy(reg); r45['types'][4].pop('outside')
    bite(45, 'REGISTER-SHAPE: a row without `outside` goes red', lambda: cov_red('REGISTER-SHAPE', reg2=r45))
    r46 = copy.deepcopy(reg); f46 = (r46.get('$folded') or {}).get('types') or {}; k46 = sorted(f46)[0] if f46 else None
    if k46: f46.pop(k46)
    bite(46, f"FOLD-MISSING: the fold map without the older type {k46!r} goes red", lambda: k46 and cov_red('FOLD-MISSING', reg2=r46))
    r47 = copy.deepcopy(reg); r47.setdefault('$folded', {}).setdefault('types', {})['relates'] = {'to': 'noSuchRow'}
    bite(47, 'FOLD-DANGLING: an older type folded onto a word with no row and no proposal goes red', lambda: cov_red('FOLD-DANGLING', reg2=r47))
    bite(48, 'PROPOSED-HAS-EDGES: a conflictsWith line drawn while conflictsWith is only a proposal goes red',
         lambda: cov_red('PROPOSED-HAS-EDGES', e2=edges + [{'s': rul, 't': rul, 'type': 'conflictsWith'}]))
    bite(49, 'CONTROL (fold): every older decision-graph type is folded and every target is a row or a proposal on the real register',
         lambda: older_types() and not any(k in ('FOLD-MISSING', 'FOLD-DANGLING', 'PROPOSED-HAS-EDGES') for k, _ in cov))
    print('SELFTEST: ' + ('PASS — every planted arm went red' if ok_all else 'FAIL'))
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
