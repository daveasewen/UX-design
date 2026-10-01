#!/usr/bin/env python3
"""gen_kg_standards.py — the five edges the outside world has and Apollo lacked, and the theme node kind.

Ruling: s308-D28 (Dave, chat #308, 2026-09-29 12:13 BST, verbatim: '9. Five edges the outside world has and
Apollo lacks Changed in v2 — Take it'), extending s308-D24. Built #311 overnight lane D3. Rows: W-308iq (a-d),
W-308in (e).

WHAT IT LANDS — knowledge/_standard_nodes.json (family per edge; read by knowledge/_build_kg_explorer.py pass E4):
  (a) aliasOf             token:<group> → token:<group>   a semantic or primitive token's `$alias` (per mode),
                          read from every knowledge/tokens/*.json leaf; drawn at the graph's GROUP grain (the
                          token nodes are groups, s277-D12), each line carrying its leaf pairs. THE LOOP CHECK
                          (the design-token format: circular references must be detected) runs at LEAF grain
                          here and REFUSES TO LAND on a cycle; a leaf with more than one target per mode is
                          refused too (Canonical's dt:aliasOf, 'only one allowed'). A leaf aliasing inside its
                          own group is counted, not drawn (it is not a line between two nodes).
  (b) providesCapability  component → capability:<name>  the other half of acceptsCapability: a component
                          provides the capability that carries its own name (capability:breadcrumbs is
                          provided by component:breadcrumbs). Name match ONLY — a capability no component is
                          named for is listed under `unprovided`, never guessed.
  (c) theme:<id>          THE THEME NODE KIND: the four registered themes (knowledge/tokens/themes/_themes.json)
                          and the two colour modes the records name as a theme (light, dark — s230-D2 says
                          'theme=dark'). `defaultFor` lines that were declared nulls carrying a `theme`
                          qualifier now point at theme:<that> (the explorer resolves them; storage unchanged).
  (d) ariaRole            component → aria:<role>          the WAI-ARIA roles the meta's own
                          `accessibility.role` (or `roles`) field names with role=<x>, or the field when it
                          is one role word. A role named after NOT / never is refused, not drawn.
  (e) replacedBy          component → component, token → token, with the VERSION it happened in, read from
                          the ratified lines in knowledge/_replaced_by.json (each names its ruling).

Usage:  python3 knowledge/gen_kg_standards.py [--check | --land | --selftest]
  (no flag) prints what it would land · --check exits 1 when the landed file differs from a fresh compute ·
  --land writes it · --selftest plants one bad input per refusal and expects each caught.
"""
import json, glob, os, re, sys, copy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _dtcg_load import load_legacy as _load_legacy  # s311-D8 DTCG 2025.10 read-site seam (#312 J)
from _helpgate import help_gate as _help_gate  # noqa: E402
_help_gate(__doc__, __name__, __file__)
OUT = '_standard_nodes.json'
REPLACED = '_replaced_by.json'
ME = 'gen_kg_standards.py'
RULING = 's308-D28'
ARIA_ROLES = set("""alert alertdialog application article banner blockquote button caption cell checkbox code columnheader
combobox complementary contentinfo definition deletion dialog directory document emphasis feed figure form generic
grid gridcell group heading img insertion link list listbox listitem log main marquee math menu menubar menuitem
menuitemcheckbox menuitemradio meter navigation none note option paragraph presentation progressbar radio radiogroup
region row rowgroup rowheader scrollbar search searchbox separator slider spinbutton status strong subscript
superscript switch tab table tablist tabpanel term textbox time timer toolbar tooltip tree treegrid treeitem""".split())
ROLE_RX = re.compile(r'(?<![\w-])role\s*=\s*[\\\'"]*([a-z]+)')
NEG_RX = re.compile(r'(?i)\b(not|never)\b[^.;]{0,20}$')
MODES = ('light', 'dark')


class Refused(Exception):
    pass


def _load(p, default=None):
    try:
        return json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        return default


def token_leaves(K):
    """{leaf path: {mode: target path}} for every token leaf carrying `$alias`, with its source file."""
    out = {}
    for f in sorted(glob.glob(os.path.join(K, 'tokens', '*.json'))):
        if re.search(r'-pre-s\d+\.json$', f) or os.path.basename(f).startswith(('EXAMPLE', '_')) \
                or f.endswith('.resolver.json'):
            continue
        d = _load_legacy(f)   # s311-D8: the pre-s311 view ($alias restored from the {ref} / $extensions)

        def walk(x, p):
            if not isinstance(x, dict):
                return
            if '$alias' in x:
                a = x['$alias']
                out[p] = {'alias': a, 'file': os.path.relpath(f, K)}
            for k, v in x.items():
                if not k.startswith('$'):
                    walk(v, p + '/' + k if p else k)
        walk(d, '')
    return out


def alias_edges(K, leaves=None):
    leaves = token_leaves(K) if leaves is None else leaves
    groups = {n['id'] for n in (_load(os.path.join(K, '_token_nodes.json'), {}) or {}).get('nodes', [])}
    graph, refusals = {}, []
    for p, v in leaves.items():
        a = v['alias']
        if isinstance(a, str):
            a = {'all': a}
        if not isinstance(a, dict) or not all(isinstance(t, str) for t in a.values()):
            refusals.append(('ALIAS-NOT-ONE', p, f'$alias must name one target per mode, got {a!r}'))
            continue
        for mode, t in a.items():
            graph.setdefault((p, mode), t)
    # LEAF-grain loop check, per mode (an 'all' target serves every mode)
    def nxt(p, mode):
        return graph.get((p, mode)) or graph.get((p, 'all'))
    seen_cycles = set()
    for (p, mode) in list(graph):
        path, cur = [p], p
        for _ in range(64):
            cur = nxt(cur, mode)
            if cur is None:
                break
            if cur in path:
                cyc = tuple(path[path.index(cur):])
                key = (frozenset(cyc), mode)
                if key not in seen_cycles:
                    seen_cycles.add(key); refusals.append(('ALIAS-LOOP', ' → '.join(cyc + (cur,)), f'mode {mode}'))
                break
            path.append(cur)
    pairs, inside, unknown = {}, 0, 0
    for (p, mode), t in sorted(graph.items()):
        gs, gt = 'token:' + p.split('/')[0], 'token:' + t.split('/')[0]
        if gs == gt:
            inside += 1; continue
        if gs not in groups or gt not in groups:
            unknown += 1; continue
        pairs.setdefault((gs, gt), []).append(f'{p} → {t}' + ('' if mode == 'all' else f' ({mode})'))
    edges = [{'s': s, 't': t, 'type': 'aliasOf', 'fam': 'tokens', 'maker': 'generated:' + ME,
              'note': f'{len(v)} leaf alias(es): ' + '; '.join(v[:6]) + (' …' if len(v) > 6 else ''),
              'leaves': len(v)} for (s, t), v in sorted(pairs.items())]
    return edges, refusals, {'leaves': len(leaves), 'leafAliases': len(graph), 'insideOneGroup': inside,
                             'endsNotAGroupNode': unknown, 'groupLines': len(edges)}


def component_stems(K):
    return sorted(os.path.basename(f)[:-len('.meta.json')] for f in glob.glob(os.path.join(K, 'components', '*.meta.json'))
                  if not os.path.basename(f).startswith('EXAMPLE-'))


def capability_edges(K):
    caps = sorted(n['id'] for n in (_load(os.path.join(K, '_source_nodes.json'), {}) or {}).get('nodes', [])
                  if n.get('type') == 'capability')
    stems = set(component_stems(K))
    edges, unprovided = [], []
    for c in caps:
        name = c.split(':', 1)[1]
        if name in stems:
            edges.append({'s': 'component:' + name, 't': c, 'type': 'providesCapability', 'fam': 'sources',
                          'maker': 'generated:' + ME, 'note': f'provides the capability that carries its own name ({name})'})
        else:
            unprovided.append(c)
    return edges, unprovided


def roles_in(text):
    """The ARIA roles a sentence names with role=<x>, minus any named after NOT / never."""
    if not isinstance(text, str):
        return [], []
    if text.strip() in ARIA_ROLES:
        return [text.strip()], []
    got, refused = [], []
    for m in ROLE_RX.finditer(text):
        r = m.group(1)
        if r not in ARIA_ROLES:
            continue
        if NEG_RX.search(text[max(0, m.start() - 24):m.start()]):
            refused.append(r); continue
        if r not in got:
            got.append(r)
    return got, refused


def aria_edges(K):
    edges, refused, roles = [], [], set()
    for stem in component_stems(K):
        m = _load(os.path.join(K, 'components', stem + '.meta.json'), {}) or {}
        a = m.get('accessibility') if isinstance(m.get('accessibility'), dict) else {}
        field = next((k for k in ('role', 'roles', 'ariaRole') if k in a), None)
        if not field:
            continue
        text = a[field] if isinstance(a[field], str) else json.dumps(a[field], ensure_ascii=False)
        got, no = roles_in(text)
        refused += [(stem, r) for r in no]
        for r in got:
            roles.add(r)
            edges.append({'s': 'component:' + stem, 't': 'aria:' + r, 'type': 'ariaRole', 'fam': 'guidelines',
                          'maker': 'generated:' + ME, 'note': (f'accessibility.{field}: ' + text)[:320]})
    nodes = [{'id': 'aria:' + r, 'type': 'aria', 'label': r, 'fam': 'guidelines',
              'source': 'WAI-ARIA 1.2 role'} for r in sorted(roles)]
    return nodes, edges, refused


def theme_nodes(K):
    reg = _load(os.path.join(K, 'tokens', 'themes', '_themes.json'), {}) or {}
    nodes = [{'id': 'theme:' + tid, 'type': 'theme', 'label': (t or {}).get('label') or tid, 'fam': 'assets',
              'attr': (t or {}).get('attr'), 'source': 'knowledge/tokens/themes/_themes.json'}
             for tid, t in sorted((reg.get('themes') or {}).items())]
    nodes += [{'id': 'theme:' + m, 'type': 'theme', 'label': m, 'fam': 'assets', 'mode': True,
               'source': 'the colour mode the records name as a theme (s230-D2: theme=' + m + ')'} for m in MODES]
    return nodes


def replaced_edges(K):
    d = _load(os.path.join(K, REPLACED), {}) or {}
    edges, refusals = [], []
    for ln in d.get('lines') or []:
        s, t = ln.get('s'), ln.get('t')
        ks, kt = str(s).split(':')[0], str(t).split(':')[0]
        if ks != kt or ks not in ('component', 'token'):
            refusals.append(('REPLACED-ENDS', f'{s} → {t}', 'replacedBy runs component → component or token → token'))
            continue
        if not (ln.get('version') and ln.get('ruling')):
            refusals.append(('REPLACED-NO-VERSION', f'{s} → {t}', 'a replacement names the version it happened in and its ruling'))
            continue
        edges.append({'s': s, 't': t, 'type': 'replacedBy', 'fam': 'structure', 'version': ln['version'],
                      'released': ln.get('released'), 'ruling': ln['ruling'], 'maker': 'ratified:' + ln['ruling'],
                      'note': (ln.get('note') or '')[:320]})
    return edges, refusals


def compute(K=HERE):
    a_edges, a_ref, a_meas = alias_edges(K)
    c_edges, unprovided = capability_edges(K)
    r_nodes, r_edges, r_refused = aria_edges(K)
    t_nodes = theme_nodes(K)
    x_edges, x_ref = replaced_edges(K)
    refusals = a_ref + x_ref
    pay = {
        '$description': ('Generated by knowledge/gen_kg_standards.py under s308-D28 (#311 overnight lane D3): the five '
                         'edges the outside world has and Apollo lacked (aliasOf, providesCapability, ariaRole, '
                         'replacedBy, and defaultFor given a theme to point at) and the theme and aria node kinds. '
                         'Regenerate with `python3 knowledge/gen_kg_standards.py --land`; never hand-edit. Replacements '
                         'are ratified lines in knowledge/_replaced_by.json.'),
        'family': 'standards', 'ruling': RULING,
        '$measured': {'aliasOf': a_meas, 'providesCapability': {'lines': len(c_edges), 'unprovided': unprovided},
                      'ariaRole': {'lines': len(r_edges), 'roles': len(r_nodes), 'refusedAfterNot': r_refused},
                      'theme': {'nodes': len(t_nodes)}, 'replacedBy': {'lines': len(x_edges)}},
        'nodes': t_nodes + r_nodes,
        'edges': a_edges + c_edges + r_edges + x_edges,
    }
    return pay, refusals


def selftest():
    import tempfile, shutil
    ok_all = True

    def bite(n, desc, cond):
        nonlocal ok_all
        try: ok = bool(cond())
        except Exception as ex: ok = False; desc += f' [raised {type(ex).__name__}: {ex}]'
        ok_all &= ok; print(f"  {'✓' if ok else '✗'} {n} {desc}")
    pay, ref = compute()
    bite(0, f"CONTROL: the live tree computes with no refusal ({len(pay['edges'])} edges, {len(pay['nodes'])} nodes)", lambda: not ref)
    lv = token_leaves(HERE)
    k = sorted(lv)[0]
    lv1 = copy.deepcopy(lv); first_t = list(lv1[k]['alias'].values())[0] if isinstance(lv1[k]['alias'], dict) else lv1[k]['alias']
    lv1[first_t] = {'alias': {'light': k, 'dark': k}, 'file': 'planted'}
    bite(1, f'ALIAS-LOOP: {first_t} planted to alias back to {k} goes red', lambda: any(c == 'ALIAS-LOOP' for c, *_ in alias_edges(HERE, lv1)[1]))
    lv2 = copy.deepcopy(lv); lv2[k] = {'alias': {'light': ['a/b', 'c/d']}, 'file': 'planted'}
    bite(2, 'ALIAS-NOT-ONE: a leaf aliasing two targets in one mode goes red', lambda: any(c == 'ALIAS-NOT-ONE' for c, *_ in alias_edges(HERE, lv2)[1]))
    bite(3, "NOT-ROLE: 'deliberately NOT role=combobox' names no role", lambda: roles_in('a plain input, deliberately NOT role=combobox')[0] == [])
    bite(4, "a one-word field ('button') is that role; aria-roledescription is not a role", lambda: roles_in('button')[0] == ['button']
         and roles_in('the region carries aria-roledescription="carousel"')[0] == [])
    tmp = tempfile.mkdtemp(prefix='gks-')
    try:
        json.dump({'lines': [{'s': 'component:a', 't': 'token:b', 'version': '1', 'ruling': 'x'},
                             {'s': 'component:a', 't': 'component:b'}]}, open(os.path.join(tmp, REPLACED), 'w'))
        r = replaced_edges(tmp)[1]
        bite(5, 'REPLACED-ENDS and REPLACED-NO-VERSION: a component replaced by a token, and a replacement with no version, both go red',
             lambda: {c for c, *_ in r} == {'REPLACED-ENDS', 'REPLACED-NO-VERSION'})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print('SELFTEST: ' + ('PASS' if ok_all else 'FAIL'))
    return 0 if ok_all else 1


def main(argv):
    if '--selftest' in argv:
        return selftest()
    pay, ref = compute()
    for c, w, d in ref:
        print(f'  ✗ {c:20} {w}   {d}')
    print('COUNTS: ' + json.dumps(pay['$measured'], ensure_ascii=False)[:900])
    target = os.path.join(HERE, OUT)
    text = json.dumps(pay, indent=2, ensure_ascii=False) + '\n'
    if '--check' in argv:
        cur = open(target, encoding='utf-8').read() if os.path.exists(target) else ''
        ok = cur == text and not ref
        print('gen_kg_standards --check: ' + ('FRESH' if ok else 'STALE or REFUSED — run --land'))
        return 0 if ok else 1
    if '--land' in argv:
        if ref:
            print('REFUSED: nothing landed (fix the refusals above)'); return 2
        open(target, 'w', encoding='utf-8').write(text)
        print(f'LANDED {OUT}: {len(pay["nodes"])} nodes, {len(pay["edges"])} edges')
    return 1 if ref else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
