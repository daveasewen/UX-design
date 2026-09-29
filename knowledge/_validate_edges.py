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
                REGISTER-SHAPE    a row missing a checked field, or two rows with one word
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
COVER_CLASSES = ('NO-ROW', 'ROW-WITHOUT-EDGES', 'UNREGISTERED-NAME', 'ABSENT-HAS-EDGES', 'REGISTER-SHAPE')
ROW_FIELDS = ('word', 'from', 'to', 'nulls', 'count')


class CouldNotAsk(Exception):
    pass


def kind_of(node_id):
    return str(node_id).split(':', 1)[0] if node_id else None


def load_graph(K=HERE):
    """(nodes, edges, how) — the explorer's own extract, stdout swallowed."""
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


def check_coverage(edges, reg, names):
    rows, probs = register_rows(reg)
    live = Counter(e.get('type') for e in edges)
    absent = reg.get('$absent') or {}
    out = [('REGISTER-SHAPE', p) for p in probs]
    out += [('NO-ROW', f'{t} ({live[t]} edges in the graph)') for t in sorted(live) if t not in rows]
    out += [('ROW-WITHOUT-EDGES', t) for t in sorted(rows) if not live.get(t)]
    out += [('UNREGISTERED-NAME', f"{t} (named in {sorted(w)})") for t, w in sorted(names.items())
            if t not in rows and t not in absent]
    out += [('ABSENT-HAS-EDGES', f'{t} ({live[t]} edges)') for t in sorted(absent) if live.get(t)]
    return out


def drift(edges, rows):
    live = Counter(e.get('type') for e in edges)
    return [(t, (r.get('$measured') or {}).get('edges'), live.get(t, 0)) for t, r in sorted(rows.items())
            if (r.get('$measured') or {}).get('edges') is not None and r['$measured']['edges'] != live.get(t, 0)]


def print_ends(res, rows, how, dr):
    fails = {c: n for c, n in res['byClass'].items() if n}
    print(f"COUNTS: types registered {len(rows)} · edges checked {res['checked']} · pass {res['pass']} · fail {res['fail']}"
          f" · by class {fails or 'none'}")
    print(f"  graph: {how}")
    for c in ENDS_CLASSES:
        if res['byClass'][c]:
            print(f"  {c}: {res['byClass'][c]} — by type {res['byClassType'][c]}")
    for c, ty, s, t, d in res['failures']:
        print(f"  ✗ {c:16} {ty:18} {s} → {t}   {d}")
    for t, was, now in dr:
        print(f"  · drift (not a failure): {t} {was} → {now} edges since the row was measured")
    print('EDGE ENDS: ' + ('all edges match their rows' if not res['fail'] and not res['byClass']['OVER-COUNT']
                           else 'FAILURES above (ADVISORY, s308-D17)'))


def main(argv):
    if '--selftest' in argv:
        return selftest()
    try:
        nodes, edges, how = load_graph()
    except CouldNotAsk as ex:
        print(f'COULD-NOT-ASK: {ex}'); return 77
    reg = load_register()
    rows, _ = register_rows(reg)
    if '--coverage' in argv:
        probs = check_coverage(edges, reg, named_types())
        print(f"COUNTS: rows {len(rows)} · graph types {len(set(e.get('type') for e in edges))} · declared absent "
              f"{len(reg.get('$absent') or {})} · refusals {len(probs)}")
        for c, d in probs: print(f'  ✗ {c:18} {d}')
        print('EDGE REGISTER COVERAGE: ' + ('OK' if not probs else 'REFUSED (BLOCKING) — add or fix the row(s) in knowledge/_edge_register.json'))
        return 1 if probs else 0
    res = check_ends(edges, rows)
    if '--json' in argv:
        print(json.dumps({k: v for k, v in res.items() if k != 'failures'}, sort_keys=True)); 
    else:
        print_ends(res, rows, how, drift(edges, rows))
    return 1 if (res['fail'] or res['byClass']['OVER-COUNT']) else 0


# ------------------------------------------------------------------ selftest
def selftest():
    ok_all = True

    def bite(n, desc, cond):
        nonlocal ok_all
        try: ok = bool(cond())
        except Exception as ex: ok = False; desc += f'  [raised {type(ex).__name__}: {ex}]'
        ok_all &= ok
        print(f"  {'✓' if ok else '✗'} {n:>2} {desc}")

    try:
        nodes, edges, how = load_graph()
    except CouldNotAsk as ex:
        print(f'COULD-NOT-ASK: {ex}'); return 77
    reg = load_register(); rows, probs = register_rows(reg); names = named_types()
    base = check_ends(edges, rows)
    cov = check_coverage(edges, reg, names)
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

    def cov_red(cls, e2=None, reg2=None, names2=None):
        c = check_coverage(e2 if e2 is not None else edges, reg2 if reg2 is not None else reg, names2 if names2 is not None else names)
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
    print('SELFTEST: ' + ('PASS — every planted arm went red' if ok_all else 'FAIL'))
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
