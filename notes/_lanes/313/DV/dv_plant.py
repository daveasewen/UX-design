#!/usr/bin/env python3
"""#313 lane DV — plant edges at their SOURCE files, run every consumer of the edge register, and prove each one
catches the plant BY NAME; then break each guard on purpose once and prove the same plant then goes through.

Brief: notes/_lanes/312/D/BRIEF.md, lane DV ("plants one bad edge per new rule and one good edge per type, expects
each caught or kept"). The rules are Dave's s308-D16..D28 (edge register items 1–9), built by #308 E, #311 D1–D3 and
#313 D4.

Read-only on the repo. Everything happens in a scratch copy of `knowledge/` (assets excluded — no consumer reads
them; the graph extracted without them is the same 12,137 edges): each plant edits files there, runs the consumers as
subprocesses, and restores the bytes. Mutations rewrite one guard line in the scratch copy only.

Consumers (the processes that read the register or the files the register governs):
  C1 _validate_edges.py --check      ends, shape, why, maker      (ADVISORY, build step 164)
  C2 _validate_edges.py --coverage   register shape, fold, copies (BLOCKING, build step 165)
  C3 gen_edge_copies.py --check      schema / verbs / template written from the register (D4)
  C4 _build_integrity.py --check     the metas against meta.schema.json (Draft 7)
  C5 gen_kg_standards.py --check     the five edges and the theme kind at their sources (D3; refusals by name)

A plant is CAUGHT by a consumer when a line that was not in that consumer's clean output carries the expected class
name and every needle (the planted edge's ends or the word). A good edge is KEPT when no class moves.

Usage: python3 notes/_lanes/313/DV/dv_plant.py [--json OUT]       exit 0 = every expectation met (caught, kept,
and every mutant went blind)
"""
import copy, json, os, re, shutil, subprocess, sys, tempfile
from collections import Counter

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
SRC = os.path.join(REPO, 'knowledge')
CONSUMERS = {
    'C1': ('_validate_edges.py', ['--check']),
    'C2': ('_validate_edges.py', ['--coverage']),
    'C3': ('gen_edge_copies.py', ['--check']),
    'C4': ('_build_integrity.py', ['--check']),
    'C5': ('gen_kg_standards.py', ['--check']),
}
LONG_WHY = 'Planted by lane DV to prove the edge is kept when its ends, shape, reason and maker are all legal.'


# ---------------------------------------------------------------- scratch tree
def make_scratch():
    d = tempfile.mkdtemp(prefix='dv-plant-')
    shutil.copytree(SRC, os.path.join(d, 'knowledge'), ignore=shutil.ignore_patterns('assets', '__pycache__'))
    return d


def run(scr, c):
    script, args = CONSUMERS[c]
    p = subprocess.run([sys.executable, os.path.join(scr, 'knowledge', script)] + args, cwd=scr,
                       capture_output=True, text=True, timeout=170)
    return p.returncode, (p.stdout + p.stderr).splitlines()


class Edit:
    """Edit files in the scratch tree; restore their exact bytes on exit."""
    def __init__(self, scr, edits):
        self.scr, self.edits, self.saved = scr, edits, {}

    def __enter__(self):
        for rel, fn in self.edits:
            p = os.path.join(self.scr, 'knowledge', rel)
            raw = open(p, encoding='utf-8').read()
            self.saved.setdefault(p, raw)
            new = fn(raw)
            assert new != raw, f'edit to {rel} changed nothing'
            open(p, 'w', encoding='utf-8').write(new)
        return self

    def __exit__(self, *a):
        for p, raw in self.saved.items():
            open(p, 'w', encoding='utf-8').write(raw)


def J(fn):
    """An edit on a JSON file's object; written back with indent 1 (the scratch copy only)."""
    def go(raw):
        d = json.loads(raw); fn(d); return json.dumps(d, indent=1, ensure_ascii=False) + '\n'
    return go


def S(old, new):
    """A one-place source substitution; the old text must be there exactly once."""
    def go(raw):
        n = raw.count(old)
        assert n == 1, f'mutation anchor found {n} times: {old[:70]!r}'
        return raw.replace(old, new)
    return go


# ---------------------------------------------------------------- the plants
def first(d, ty):
    return next(e for e in d['edges'] if e['type'] == ty)


def plants():
    """[(id, ruling, what, [edits], [(consumer, CLASS, [needles], mutation)])]; a mutation is [(file, edit)]."""
    V = '_validate_edges.py'
    def mute(f, cls, tail=''):
        return [(f, S(f"failures.append(('{cls}'{tail}", f"failures.append(('MUTED'{tail}"))]

    def obeys0(fn):
        return [('components/button.meta.json', J(lambda m: fn(m['edges']['obeys'][0])))]
    B0 = json.load(open(os.path.join(SRC, 'components', 'button.meta.json'), encoding='utf-8'))['edges']['obeys'][0]['ref']
    STD = json.load(open(os.path.join(SRC, '_standard_nodes.json'), encoding='utf-8'))
    AL, RB, AR, PC = (first(STD, t) for t in ('aliasOf', 'replacedBy', 'ariaRole', 'providesCapability'))
    LOGO = json.load(open(os.path.join(SRC, '_logo_nodes.json'), encoding='utf-8'))
    LOB = next(e for e in LOGO['edges'] if e['type'] == 'obeys')
    LDF = next(e for e in LOGO['edges'] if e['type'] == 'defaultFor')

    def logo_line(match, fn):
        def f(d):
            for e in d['edges']:
                if all(e.get(k) == v for k, v in match.items()):
                    fn(e); return
            raise AssertionError('logo line not found')
        return [('_logo_nodes.json', J(f))]

    def std_add(e):
        return [('_standard_nodes.json', J(lambda d: d['edges'].append(e)))]

    def reg_row(word, fn):
        def f(d):
            fn(next(r for r in d['types'] if r['word'] == word))
        return [('_edge_register.json', J(f))]

    def schema(fn):
        return [('components/meta.schema.json', J(fn))]

    P = []
    # — s308-D20: one reason field, required by type (D1; spelled `why` on the metas since D4)
    P.append(('why-missing', 's308-D20', f"Button's first obeys line ({B0}) loses its reason", obeys0(lambda o: o.pop('why')), [
        ('C1', 'WHY-MISSING', ['component:button', B0], mute(V, 'WHY-MISSING')),
        ('C4', 'schema', ["'why' is a required property"],
         schema(lambda s: s['definitions']['obeysEdge']['required'].remove('why'))),
    ]))
    P.append(('why-short', 's308-D20', "Button's first obeys reason cut to 18 characters (floor 40)",
              obeys0(lambda o: o.__setitem__('why', 'Because it says so')), [
        ('C1', 'WHY-SHORT', ['component:button', B0], mute(V, 'WHY-SHORT')),
        ('C4', 'schema', ['is too short'], schema(lambda s: s['definitions']['obeysEdge']['properties']['why'].pop('minLength'))),
    ]))
    P.append(('why-old-spelling', 's308-D20 + W-308ie (D4)', "Button's first obeys reason spelled the pre-D4 way, `$why`",
              obeys0(lambda o: o.__setitem__('$why', o.pop('why'))), [
        ('C4', 'schema', ["'why' is a required property"],
         schema(lambda s: s['definitions']['obeysEdge']['required'].remove('why'))),
    ]))
    # — s308-D21: one maker field on every edge (D1)
    P.append(('maker-bad', 's308-D21', f"the logo obeys line {LOB['s']} → {LOB['t']} carries maker 'drawn:solid'",
              logo_line({'s': LOB['s'], 't': LOB['t'], 'type': 'obeys'}, lambda e: e.__setitem__('maker', 'drawn:solid')), [
        ('C1', 'BAD-MAKER', [LOB['s'], LOB['t']], mute(V, 'BAD-MAKER')),
    ]))
    P.append(('maker-rule-gone', 's308-D21', "the usesLogo row's maker rule says made 'drawn' (not hand / generated / ratified)",
              reg_row('usesLogo', lambda r: r['maker'].__setitem__('made', 'drawn')), [
        ('C2', 'REGISTER-SHAPE', ["'usesLogo'", 'maker must say made'],
         [(V, S("elif not (mk.get('made') in MAKER_KINDS and", "elif False and not (mk.get('made') in MAKER_KINDS and"))]),
    ]))
    # — s308-D22 / D27: the outside term, graded (D2)
    P.append(('outside-grade', 's308-D22', "the obeys row's outside grade set to 'near'",
              reg_row('obeys', lambda r: r['outside'].__setitem__('grade', 'near')), [
        ('C2', 'REGISTER-SHAPE', ["'obeys'", 'outside must carry'],
         [(V, S("ou.get('grade') in GRADES + (None,)", "ou.get('grade') is not 0"))]),
    ]))
    # — s308-D23: the two ruling-to-ruling vocabularies folded into one (D2)
    P.append(('fold-missing', 's308-D23', "the fold map loses the older type 'relates'",
              [('_edge_register.json', J(lambda d: d['$folded']['types'].pop('relates')))], [
        ('C2', 'FOLD-MISSING', ['relates'], [(V, S("out += [('FOLD-MISSING', f'", "out += [('MUTED', f'"))]),
    ]))
    P.append(('fold-dangling', 's308-D23', "the older type 'relates' folded onto 'noSuchRow'",
              [('_edge_register.json', J(lambda d: d['$folded']['types']['relates'].__setitem__('to', 'noSuchRow')))], [
        ('C2', 'FOLD-DANGLING', ['relates', 'noSuchRow'], [(V, S("out += [('FOLD-DANGLING', f\"", "out += [('MUTED', f\""))]),
    ]))
    # — s308-D24 / D28: the five new edges and the theme kind (D3)
    P.append(('alias-loop', 's308-D28 (a)', f"an aliasOf line back from {AL['t']} to {AL['s']} (a loop between groups)",
              std_add(dict(AL, s=AL['t'], t=AL['s'])), [
        ('C1', 'LOOP', ['aliasOf', AL['s'], AL['t']], mute(V, 'LOOP')),
    ]))
    P.append(('cap-wrong-to', 's308-D28 (b)', f"providesCapability from {PC['s']} ending on a component",
              std_add(dict(PC, t='component:cards')), [
        ('C1', 'WRONG-TO', ['providesCapability', PC['s'], 'component:cards'], mute(V, 'WRONG-TO')),
    ]))
    P.append(('cap-dangling', 's308-D28 (b) + #308 L', f"providesCapability from {PC['s']} to 'component:card', a node that does not exist",
              std_add(dict(PC, t='component:card')), [
        ('C2', 'SKIPPED-UNDECLARED', ['standard providesCapability'],
         [(V, S("out += [('SKIPPED-UNDECLARED', f\"", "out += [('MUTED', f\""))]),
    ]))
    P.append(('theme-wrong-to', 's308-D28 (c) / s308-D24', f"the logo defaultFor line from {LDF['s']} pointed at a logo, not a theme",
              logo_line({'s': LDF['s'], 'type': 'defaultFor'}, lambda e: (e.__setitem__('t', LDF['s']), e.pop('theme', None))), [
        ('C1', 'WRONG-TO', ['defaultFor', LDF['s']], mute(V, 'WRONG-TO')),
    ]))
    P.append(('aria-wrong-from', 's308-D28 (d)', f"an ariaRole line starting on a token, to {AR['t']}",
              std_add(dict(AR, s='token:background')), [
        ('C1', 'WRONG-FROM', ['ariaRole', 'token:background', AR['t']], mute(V, 'WRONG-FROM')),
    ]))
    P.append(('replaced-ends-source', 's308-D28 (e)', "a ratified replacement line: the Button replaced by a token",
              [('_replaced_by.json', J(lambda d: d['lines'].append(
                  {'s': 'component:button', 't': 'token:background', 'version': '1.0.15', 'released': False, 'ruling': 's308-D42'})))], [
        ('C5', 'REPLACED-ENDS', ['component:button', 'token:background'],
         [('gen_kg_standards.py', S("refusals.append(('REPLACED-ENDS'", "refusals.append(('MUTED'"))]),
    ]))
    P.append(('replaced-no-version', 's308-D28 (e)', "a ratified replacement line with no version",
              [('_replaced_by.json', J(lambda d: d['lines'].append(
                  {'s': 'component:badge', 't': 'component:tag', 'ruling': 's308-D42'})))], [
        ('C5', 'REPLACED-NO-VERSION', ['component:badge', 'component:tag'],
         [('gen_kg_standards.py', S("refusals.append(('REPLACED-NO-VERSION'", "refusals.append(('MUTED'"))]),
    ]))
    P.append(('replaced-pair', 's308-D28 (e)', f"a replacedBy line in the graph: {RB['s']} replaced by a token",
              std_add(dict(RB, t='token:background')), [
        ('C1', 'WRONG-PAIR', ['replacedBy', RB['s'], 'token:background'], mute(V, 'WRONG-PAIR')),
    ]))
    P.append(('replaced-twice', 's308-D28 (e)', f"{RB['s']} replaced by a second component",
              std_add(dict(RB, t='component:cards')), [
        ('C1', 'OVER-COUNT', ['replacedBy', RB['s']], [(V, S("failures.append(('OVER-COUNT', ty, s, None", "failures.append(('MUTED', ty, s, None"))]),
    ]))
    # — W-308ie / s308-D16: the meta schema, the verbs map and the explorer read the register (D4)
    P.append(('copy-schema', 'W-308ie (s308-D16)', "meta.schema.json grows an edge key 'plantedEdge' the register lacks",
              schema(lambda s: s['properties']['edges']['properties'].__setitem__(
                  'plantedEdge', {'type': 'array', 'items': {'$ref': '#/definitions/edge'}})), [
        ('C2', 'COPY-DRIFT', ['plantedEdge'], [(V, S("out += [('COPY-DRIFT', f'", "out += [('MUTED', f'"))]),
        ('C2', 'UNREGISTERED-NAME', ['plantedEdge'], [(V, S("out += [('UNREGISTERED-NAME', f\"", "out += [('MUTED', f\""))]),
        ('C3', 'SCHEMA-DRIFT', ['plantedEdge'], [('gen_edge_copies.py', S("out += [('SCHEMA-DRIFT', x) for x in d]", "out += []"))]),
    ]))
    P.append(('copy-verbs', 'W-308ie (s308-D16)', "_kg_verbs.json's unread block loses ariaRole",
              [('_kg_verbs.json', J(lambda d: d['unread'].pop('ariaRole')))], [
        ('C2', 'COPY-DRIFT', ['ariaRole'], [(V, S("out += [('COPY-DRIFT', f'", "out += [('MUTED', f'"))]),
        ('C3', 'VERBS-DRIFT', ['unread lacks ariaRole'],
         [('gen_edge_copies.py', S("out.append(('VERBS-DRIFT', f'_kg_verbs.json unread lacks", "out.append(('MUTED', f'_kg_verbs.json unread lacks"))]),
    ]))
    P.append(('copy-template', 'W-308ie (s308-D16)', "a literal FAMILY map put back into the explorer template",
              [('_kg_explorer.template.html', lambda raw: raw + "\n<script>const FAMILY={containedBy:'structure'};</script>\n")], [
        ('C2', 'COPY-DRIFT', ['FAMILY'], [(V, S("out += [('COPY-DRIFT', f'", "out += [('MUTED', f'"))]),
        ('C3', 'TEMPLATE-COPY', ['FAMILY'],
         [('gen_edge_copies.py', S("probs.append(('TEMPLATE-COPY', 'knowledge/_kg_explorer.template.html holds a literal FAMILY",
                                   "probs.append(('MUTED', 'knowledge/_kg_explorer.template.html holds a literal FAMILY"))]),
    ]))
    P.append(('meta-new-type', 's308-D16', "Button's meta carries an edge list 'plantedEdge' with no register row",
              [('components/button.meta.json', J(lambda m: m['edges'].__setitem__('plantedEdge', [{'ref': 'component:card'}])))], [
        ('C4', 'schema', ['plantedEdge'], schema(lambda s: s['properties']['edges'].__setitem__('additionalProperties', True))),
    ]))
    return P


OWNER_ONLY = [
    ('_validate_edges.py', 'AUTHORED-FLAG',
     S("failures.append(('AUTHORED-FLAG'", "failures.append(('MUTED'"), 41,
     "the builder's link() strips `authored` from every stored line (explorer 1.36), so no file can carry it into the graph"),
    ('_validate_edges.py', 'PROPOSED-HAS-EDGES',
     S("out += [('PROPOSED-HAS-EDGES', f'", "out += [('MUTED', f'"), 48,
     'the explorer builder names neither conflictsWith nor divergesFrom (grep: 0 lines; both are $proposed, s308-D23), so this lane found no file that draws one'),
    ('gen_kg_standards.py', 'ALIAS-LOOP',
     S("refusals.append(('ALIAS-LOOP'", "refusals.append(('MUTED'"), 1,
     "not planted in a token file tonight: the loop is checked at leaf grain over the DTCG files read through the s311-D8 legacy view, and this lane did not write a DTCG plant; the generator's own bite plants it in memory"),
    ('gen_kg_standards.py', 'ALIAS-NOT-ONE',
     S("refusals.append(('ALIAS-NOT-ONE'", "refusals.append(('MUTED'"), 2,
     'the same: not planted in a token file tonight; the generator bite plants a two-target alias in memory'),
]


def caught(clean, out, cls, needles):
    base = Counter(clean)
    new = [l for l in out if not base.get(l)]
    hit = [l for l in new if cls in l and all(n in l for n in needles)]
    return hit, new


# ---------------------------------------------------------------- good edges, one per type (in-process)
def good_edges():
    sys.path.insert(0, SRC)
    import _validate_edges as VE
    nodes, edges, _ = VE.load_graph(SRC)
    reg = VE.load_register()
    rows, _ = VE.register_rows(reg)
    names = VE.named_types(SRC)

    def tallies(E):
        a = VE.check_ends(E, rows)['byClass']; b = VE.check_shape(E, rows)['byClass']; c = VE.check_why_maker(E, rows)['byClass']
        d = Counter(k for k, _ in VE.check_coverage(E, reg, names))
        return {**a, **b, **c, **{'cov:' + k: v for k, v in d.items()}}
    t0 = tallies(edges)
    by_kind = {}
    for i in sorted(nodes):
        by_kind.setdefault(VE.kind_of(i), []).append(i)
    out_of = {}
    for e in edges:
        out_of.setdefault(e['type'], set()).add(e['s'])
    res = []
    for w, r in sorted(rows.items()):
        if not r['opposite'].get('stored', True):
            res.append((w, 'read-side', None, 'stores nothing; its stored opposite ' + str(r['opposite'].get('type')) + ' is planted instead'))
            continue
        pairs = r.get('pairs') or [[f, t] for f in r['from'] for t in (r['to'] or [None])]
        e = None
        for fk, tk in pairs:
            if not by_kind.get(fk): continue
            # a start with no line of this type yet; where every node of the kind already has one (a max-1 type),
            # a fresh start id of that kind — the ends check reads the kind from the id, as the graph's ids carry it
            ss = [i for i in by_kind[fk] if i not in out_of.get(w, set())] or [fk + ':dv-planted-start']
            if tk is None:
                if (r.get('nulls') or {}).get('allowed'):
                    e = {'s': ss[0], 't': None, 'type': w}; break
                continue
            # a sink: a target with no line of this type leaving it (no loop), and not the start (no self-line)
            ts = [i for i in by_kind.get(tk, []) if i != ss[0] and i not in out_of.get(w, set())]
            if ts:
                e = {'s': ss[0], 't': ts[0], 'type': w}; break
        if e is None:
            res.append((w, 'no-plant', None, f'no node of the kinds {pairs} to plant on')); continue
        e.update(why=LONG_WHY, maker=r['maker'].get('value') or 'generated:dv')
        t1 = tallies(edges + [e])
        moved = {k: (t0.get(k, 0), v) for k, v in t1.items() if v != t0.get(k, 0)}
        res.append((w, 'kept' if not moved else 'FLAGGED', e, moved))
    return res, len(edges)


def main(argv):
    scr = make_scratch()
    report = {'plants': [], 'good': [], 'owner': [], 'ok': True}
    try:
        # the standards file is stale at HEAD by one aliasOf line (found by this lane); land it in the scratch copy so
        # C5's clean output is fresh and a plant's refusal is the only change
        subprocess.run([sys.executable, os.path.join(scr, 'knowledge', 'gen_kg_standards.py'), '--land'], cwd=scr,
                       capture_output=True, text=True)
        clean = {c: run(scr, c) for c in CONSUMERS}
        print('CLEAN: ' + ' · '.join(f'{c} exit {rc}' for c, (rc, _) in clean.items()))
        for pid, rul, what, edits, exps in plants():
            print(f'\n[{pid}] {rul} — {what}')
            with Edit(scr, edits):
                outs = {}
                for c, cls, needles, mut in exps:
                    if c not in outs: outs[c] = run(scr, c)
                    rc, out = outs[c]
                    hit, new = caught(clean[c][1], out, cls, needles)
                    ok1 = bool(hit)
                    with Edit(scr, mut):
                        rc2, out2 = run(scr, c)
                    hit2, _ = caught(clean[c][1], out2, cls, needles)
                    ok2 = not hit2
                    report['ok'] &= ok1 and ok2
                    print(f"  {'✓' if ok1 else '✗'} {c} {CONSUMERS[c][0]} {' '.join(CONSUMERS[c][1])} → exit {clean[c][0]}→{rc}, "
                          f"caught by name {cls}: {hit[0].strip()[:150] if hit else 'NOT CAUGHT; new lines: ' + repr(new[:3])}")
                    print(f"  {'✓' if ok2 else '✗'}    guard broken on purpose → {'the plant goes through (exit ' + str(rc2) + ')' if ok2 else 'STILL CAUGHT: the mutation did not reach the guard'}")
                    report['plants'].append({'id': pid, 'ruling': rul, 'what': what, 'consumer': c, 'class': cls,
                                             'caught': ok1, 'line': hit[0].strip() if hit else None, 'exit': [clean[c][0], rc],
                                             'mutantBlind': ok2, 'mutantExit': rc2})
        # the guards a source file cannot reach — their owners' selftests plant them in memory; break each guard
        # once and require the owner's selftest to name the bite that went blind
        print('\nGUARDS NO SOURCE FILE CAN REACH — each owner selftest, then the guard broken on purpose:')
        for f, cls, mut, bite_no, why_no_source in OWNER_ONLY:
            sc = os.path.join(scr, 'knowledge', f)
            p0 = subprocess.run([sys.executable, sc, '--selftest'], cwd=scr, capture_output=True, text=True)
            with Edit(scr, [(f, mut)]):
                p1 = subprocess.run([sys.executable, sc, '--selftest'], cwd=scr, capture_output=True, text=True)
            red = [l for l in p1.stdout.splitlines() if re.match(rf'\s*✗\s+{bite_no}\b', l)]
            ok = p0.returncode == 0 and p1.returncode != 0 and bool(red)
            report['ok'] &= ok
            report['owner'].append({'file': f, 'class': cls, 'bite': bite_no, 'cleanExit': p0.returncode, 'brokenExit': p1.returncode,
                                    'redLine': red[0].strip() if red else None, 'whyNoSource': why_no_source})
            print(f"  {'✓' if ok else '✗'} {f} {cls}: clean selftest exit {p0.returncode}; guard broken → exit {p1.returncode}, "
                  f"{red[0].strip()[:110] if red else 'NO BITE WENT RED'}")
            print(f"       no source plant: {why_no_source}")
        # two plants that must stay QUIET at one consumer by design — proved, not assumed
        LOB = next(e for e in json.load(open(os.path.join(SRC, '_logo_nodes.json'), encoding='utf-8'))['edges'] if e['type'] == 'obeys')
        def _auth(d):
            next(e for e in d['edges'] if e['type'] == 'obeys' and e['s'] == LOB['s'] and e['t'] == LOB['t'])['authored'] = 'hand'
        with Edit(scr, [('_logo_nodes.json', J(_auth))]):
            rc, out = run(scr, 'C1')
        quiet1 = not [l for l in caught(clean['C1'][1], out, 'AUTHORED-FLAG', [])[1] if 'AUTHORED-FLAG' in l]
        print(f"\n  {'✓' if quiet1 else '✗'} QUIET BY DESIGN: `authored` planted on {LOB['s']}'s obeys line in _logo_nodes.json — "
              f"C1 raises no AUTHORED-FLAG because the builder's link() strips the flag (1.36); the class fires only in memory")
        def _dollar(m):
            o = m['edges']['obeys'][0]; o['$why'] = o.pop('why')
        with Edit(scr, [('components/button.meta.json', J(_dollar))]):
            rc, out = run(scr, 'C1')
        quiet2 = not [l for l in caught(clean['C1'][1], out, 'WHY-', [])[1] if 'WHY-' in l]
        print(f"  {'✓' if quiet2 else '✗'} QUIET BY DESIGN: `$why` on Button's first obeys line — C1 raises nothing because the "
              f"builder still reads both spellings (#311 D1); only C4, the schema, refuses it (plant why-old-spelling above)")
        report['quiet'] = {'authored-stripped': quiet1, 'dollar-why-read': quiet2}
        report['ok'] &= quiet1 and quiet2
        # clean again after every restore: the scratch tree is back to the start
        again = {c: run(scr, c) for c in CONSUMERS}
        same = all(again[c][1] == clean[c][1] for c in CONSUMERS)
        report['ok'] &= same
        print(f"\n{'✓' if same else '✗'} RESTORE: every consumer's output after the plants equals its clean output")
    finally:
        shutil.rmtree(scr, ignore_errors=True)
    res, n = good_edges()
    print(f'\nGOOD EDGES — one legal edge planted per register row on the real graph ({n} edges), every class tallied before and after:')
    for w, verdict, e, info in res:
        ok = verdict in ('kept', 'read-side')
        report['ok'] &= ok
        report['good'].append({'type': w, 'verdict': verdict, 'edge': e, 'info': info if not isinstance(info, dict) else {k: list(v) for k, v in info.items()}})
        print(f"  {'✓' if ok else '✗'} {w:20} {verdict:9} " + (f"{e['s']} → {e['t']}" if e else str(info)) + ('' if verdict != 'FLAGGED' else f'   moved {info}'))
    kept = sum(1 for g in report['good'] if g['verdict'] == 'kept')
    caught_n = sum(1 for p in report['plants'] if p['caught'])
    blind_n = sum(1 for p in report['plants'] if p['mutantBlind'])
    print(f"\nCOUNTS: plants {len({p['id'] for p in report['plants']})} · expectations {len(report['plants'])} · caught by name {caught_n} · "
          f"mutants blind {blind_n} · good edges kept {kept} of {sum(1 for g in report['good'] if g['verdict'] != 'read-side')} "
          f"(read-side rows {sum(1 for g in report['good'] if g['verdict'] == 'read-side')})")
    print(f"OWNER SELFTESTS: {sum(1 for o in report['owner'] if o['redLine'])} of {len(report['owner'])} guards went blind when broken")
    print('DV: ' + ('PASS' if report['ok'] else 'FAIL'))
    if '--json' in argv:
        json.dump(report, open(argv[argv.index('--json') + 1], 'w'), indent=1, ensure_ascii=False, default=str)
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
