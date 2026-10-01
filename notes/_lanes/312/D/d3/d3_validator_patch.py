"""#311 lane D3 — selftest bites in knowledge/_validate_edges.py for the s308-D28 rows."""
P = 'knowledge/_validate_edges.py'
s = open(P, encoding='utf-8').read()
A = """    print('SELFTEST: ' + ('PASS — every planted arm went red' if ok_all else 'FAIL'))"""
assert s.count(A) == 1
s = s.replace(A, """    # — s308-D28 (#311 overnight lane D3): the five edges and the theme node kind
    al = next((e for e in edges if e['type'] == 'aliasOf'), None)
    bite(50, 'LOOP: an aliasOf line planted back from its target to its start goes red (the alias loop check between groups)',
         lambda: al and check_shape(edges + [{'s': al['t'], 't': al['s'], 'type': 'aliasOf'}], rows)['byClass']['LOOP']
         > check_shape(edges, rows)['byClass']['LOOP'])
    rb = next((e for e in edges if e['type'] == 'replacedBy'), None)
    tok = next((i for i in sorted(nodes) if kind_of(i) == 'token'), None)
    bite(51, 'WRONG-PAIR: a component replaced by a token goes red (replacedBy runs component → component or token → token)',
         lambda: rb and tok and planted('WRONG-PAIR', {'s': rb['s'], 't': tok, 'type': 'replacedBy'}))
    bite(52, 'OVER-COUNT: a second replacement for one component goes red (max 1)',
         lambda: rb and planted('OVER-COUNT', {'s': rb['s'], 't': comp if comp != rb['t'] else real('component'), 'type': 'replacedBy'}))
    df = [e for e in edges if e['type'] == 'defaultFor']
    bite(53, f"CONTROL (theme kind): every defaultFor line points at a theme: node ({sum(1 for e in df if kind_of(e.get('t') or '') == 'theme')} of {len(df)}), "
             "and one ending on a logo goes red", lambda: df and all(kind_of(e.get('t') or '') == 'theme' for e in df)
         and planted('WRONG-TO', {'s': df[0]['s'], 't': logo, 'type': 'defaultFor'}))
""" + A)
open(P, 'w', encoding='utf-8').write(s)
print('patched')
