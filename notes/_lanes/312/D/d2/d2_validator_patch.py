"""#311 lane D2 — patch knowledge/_validate_edges.py for s308-D22/D27 (outside column) and s308-D23 (the fold)."""
P = 'knowledge/_validate_edges.py'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:60], s.count(a)); s = s.replace(a, b)

rep("""                ABSENT-HAS-EDGES  a `$absent` entry that now carries edges (it needs a row)
""", """                ABSENT-HAS-EDGES  a `$absent` entry that now carries edges (it needs a row)
                FOLD-MISSING      a type of the older decision graph (knowledge/_decision-graph.json) that the
                                  register's `$folded` map does not name (s308-D23, #311 lane D2)
                FOLD-DANGLING     a `$folded` target that is neither a row nor a `$proposed` type
                PROPOSED-HAS-EDGES an edge in the graph of a type that is only a `$proposed` entry (make it a row)
""")
rep("""COVER_CLASSES = ('NO-ROW', 'ROW-WITHOUT-EDGES', 'UNREGISTERED-NAME', 'ABSENT-HAS-EDGES', 'REGISTER-SHAPE',
                 'SKIPPED-UNDECLARED')""", """COVER_CLASSES = ('NO-ROW', 'ROW-WITHOUT-EDGES', 'UNREGISTERED-NAME', 'ABSENT-HAS-EDGES', 'REGISTER-SHAPE',
                 'SKIPPED-UNDECLARED', 'FOLD-MISSING', 'FOLD-DANGLING', 'PROPOSED-HAS-EDGES')   # FOLD/PROPOSED: s308-D23 (#311 D2)
GRADES = ('exact', 'close', 'loose')                               # s308-D22: SKOS's three grades (#311 lane D2)
DECISION_GRAPH = os.path.join(HERE, '_decision-graph.json')       # s308-D23: the older ruling vocabulary""")
rep("""ROW_FIELDS = ('word', 'from', 'to', 'nulls', 'count', 'opposite', 'reads', 'shape', 'why', 'maker')   # why/maker: s308-D20/D21""",
    """ROW_FIELDS = ('word', 'from', 'to', 'nulls', 'count', 'opposite', 'reads', 'shape', 'why', 'maker', 'outside')   # why/maker: s308-D20/D21; outside: s308-D22/D27""")
rep("""            probs.append(f"row {r['word']!r}: maker must say made (one of {list(MAKER_KINDS)}), by, and value = made:by (s308-D21)"); continue
""", """            probs.append(f"row {r['word']!r}: maker must say made (one of {list(MAKER_KINDS)}), by, and value = made:by (s308-D21)"); continue
        ou = r.get('outside')
        if not (isinstance(ou, dict) and ou.get('grade') in GRADES + (None,) and (ou.get('term') is None) == (ou.get('grade') is None)
                and isinstance(ou.get('name'), dict) and isinstance(ou['name'].get('adopted'), bool)):
            probs.append(f"row {r['word']!r}: outside must carry a term graded one of {list(GRADES)} (or both null) and a "
                         f"`name` with a boolean `adopted` (s308-D22/D27)"); continue
""")
rep("""    out += [('ABSENT-HAS-EDGES', f'{t} ({live[t]} edges)') for t in sorted(absent) if live.get(t)]
""", """    out += [('ABSENT-HAS-EDGES', f'{t} ({live[t]} edges)') for t in sorted(absent) if live.get(t)]
    # s308-D23 (#311 lane D2): ONE ruling-to-ruling vocabulary — every older type folded, every target real
    folded = ((reg.get('$folded') or {}).get('types')) or {}
    proposed = ((reg.get('$proposed') or {}).get('types')) or {}
    out += [('FOLD-MISSING', f'{t} (used by the older decision graph; name it in $folded)') for t in sorted(older_types())
            if t not in folded]
    out += [('FOLD-DANGLING', f"{t} → {(v or {}).get('to')!r} (no row and no $proposed entry)") for t, v in sorted(folded.items())
            if (v or {}).get('to') not in rows and (v or {}).get('to') not in proposed]
    out += [('PROPOSED-HAS-EDGES', f'{t} ({live[t]} edges; a proposal carrying edges needs a row)') for t in sorted(proposed)
            if live.get(t)]
""")
rep("""def drift(edges, rows):""", """def older_types(path=DECISION_GRAPH):
    \"\"\"The edge types the older decision graph spells (s308-D23). A missing file is an empty set.\"\"\"
    try:
        d = json.load(open(path, encoding='utf-8'))
    except (OSError, ValueError):
        return set()
    return {e.get('type') for e in d.get('edges') or [] if isinstance(e, dict) and e.get('type')}


def drift(edges, rows):""")
# selftest bites, appended before the verdict line
rep("""    print('SELFTEST: ' + ('PASS — every planted arm went red' if ok_all else 'FAIL'))""",
"""    # — s308-D22/D27 + s308-D23 (#311 overnight lane D2): the outside column and the fold
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
    print('SELFTEST: ' + ('PASS — every planted arm went red' if ok_all else 'FAIL'))""")
open(P, 'w', encoding='utf-8').write(s)
print('patched')
