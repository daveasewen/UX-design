#!/usr/bin/env python3
"""gen_edge_copies.py — write the edge register's columns into the two files that used to keep their own lists.

Row W-308ie (s308-D16, Dave 2026-09-29 09:26 BST: '1. Write one edge register — Take it'): "the meta schema, the
verbs map and the explorer read it instead of holding their own partial copies". Built #313 lane D4.

THE RECORD is knowledge/_edge_register.json, one row per edge type. Three consumers read it:

  1. knowledge/components/meta.schema.json — `properties.edges.properties`. Its edge-type KEYS and each key's item
     shape (`items.$ref` → `#/definitions/<meta>`) are WRITTEN here from each row's `meta` column (a row with
     `meta: null` is not stored on a component meta and has no key). A key the register gains is added with the
     plain array shape; a key whose row is gone, or whose `meta` is null, is removed. What stays the schema's own:
     the `$`-prefixed annotation keys (`$obeys-contract`, `$contract`), each key's `description`, and every
     other part of the schema. JSON Schema cannot read another file, so the copy is generated, never hand-kept.
  2. knowledge/_kg_verbs.json — each of the twelve verbs' `reads` list and the `unread` block are WRITTEN here from
     each row's `verb` column (`verb.reads[].verb` names the verbs that read the type; `verb.unread` is the note of a
     type no verb reads). What stays the map's own: every verb's force, direction, definition, source and `$splits`.
     A verb's `count` keeps its measured branch counts for the types it still reads; a type newly read or newly
     unread takes the row's `$measured` tallies (a snapshot, as the map's own counts always were — `--verbs` in
     knowledge/_compose_slice.py re-measures live).
  3. the explorer — NOT written here: knowledge/_build_kg_explorer.py bakes the `chip` column into the page as
     KG.fam and the `reads` column as KG.read. This script only refuses a template that keeps its own copy
     (a literal `const FAMILY={…}` or a literal READ map).

  --check     (the default) write nothing; print COUNTS and every drift by name. Exit 1 on any:
                SCHEMA-DRIFT   the schema's edge keys or item shapes differ from the register's `meta` column
                VERBS-DRIFT    a verb's `reads`, or the `unread` block's types or notes, differ from the `verb` column
                VERB-UNKNOWN   a row names a verb the map does not define (a thirteenth verb is a ruling)
                FORCE-DIFF     a row's `verb.reads[].force` differs from that verb's own force in the map
                DEF-MISSING    a row's `meta` names a definition the schema does not have
                TEMPLATE-COPY  the explorer template holds a literal FAMILY or READ map again
              knowledge/_validate_edges.py --coverage carries the same refusals, as COPY-DRIFT (BLOCKING).
  --write     write both files (only the lines that change; every other byte kept), then re-check.
  --selftest  a control arm on the real files, then one planted drift per class on copies; each must go red.

  python3 knowledge/gen_edge_copies.py --check
  python3 knowledge/gen_edge_copies.py --write
  python3 knowledge/gen_edge_copies.py --selftest
"""
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)  # help gate (#158)
import copy, difflib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTER = os.path.join(HERE, '_edge_register.json')
SCHEMA = os.path.join(HERE, 'components', 'meta.schema.json')
VERBS = os.path.join(HERE, '_kg_verbs.json')
TEMPLATE = os.path.join(HERE, '_kg_explorer.template.html')
CLASSES = ('SCHEMA-DRIFT', 'VERBS-DRIFT', 'VERB-UNKNOWN', 'FORCE-DIFF', 'DEF-MISSING', 'TEMPLATE-COPY')
FAMILY_RX = re.compile(r'const\s+FAMILY\s*=\s*\{')
READ_RX = re.compile(r'const\s+READ\s*=\s*Object\.assign\(\s*\{')


def _load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def _rows(reg):
    return [r for r in reg.get('types') or [] if isinstance(r, dict) and r.get('word')]


def _verb_names(verbs):
    return [k for k, v in verbs.items() if not k.startswith('$') and k != 'unread' and isinstance(v, dict)
            and isinstance(v.get('reads'), list)]


# ---------------------------------------------------------------- the schema
def schema_from(reg, schema):
    """(new schema, [problems]) — the schema with its edge keys written from the register's `meta` column."""
    out, probs = copy.deepcopy(schema), []
    props = out['properties']['edges']['properties']
    defs = out.get('definitions') or {}
    want = {}
    for r in _rows(reg):
        m = r.get('meta')
        if m is None:
            continue
        if m not in defs:
            probs.append(('DEF-MISSING', f"{r['word']}: meta {m!r} is not a definition in meta.schema.json")); continue
        want[r['word']] = m
    new = {}
    for k, v in props.items():
        if k.startswith('$'):
            new[k] = v; continue
        if k not in want:
            continue                                   # a key with no row, or a row not stored on a meta
        v = copy.deepcopy(v) if isinstance(v, dict) else {}
        v['type'] = 'array'
        items = v.get('items') if isinstance(v.get('items'), dict) else {}
        items['$ref'] = '#/definitions/' + want[k]
        v['items'] = items
        new[k] = v
    for r in _rows(reg):
        if r['word'] in want and r['word'] not in new:
            new[r['word']] = {'type': 'array', 'items': {'$ref': '#/definitions/' + want[r['word']]}}
    # keep the annotation keys where they stood (after the edge keys), the edge keys in their old order + new ones
    ordered = {k: new[k] for k in props if k in new and not k.startswith('$')}
    ordered.update({k: v for k, v in new.items() if k not in ordered and not k.startswith('$')})
    ordered.update({k: new[k] for k in props if k.startswith('$')})
    out['properties']['edges']['properties'] = ordered
    return out, probs


# ---------------------------------------------------------------- the verbs map
def verbs_from(reg, verbs):
    """(new verbs map, [problems]) — reads lists and the unread block written from the register's `verb` column."""
    out, probs = copy.deepcopy(verbs), []
    names = _verb_names(out)
    rows = _rows(reg)
    want = {v: [] for v in names}
    measured = {}
    for r in rows:
        w = r['word']
        measured[w] = r.get('$measured') or {}
        for x in (r.get('verb') or {}).get('reads') or []:
            vn = (x or {}).get('verb')
            if vn not in want:
                probs.append(('VERB-UNKNOWN', f"{w}: reads verb {vn!r}, which knowledge/_kg_verbs.json does not define")); continue
            want[vn].append(w)
            force = out[vn].get('force')
            if (x or {}).get('force') != force:
                probs.append(('FORCE-DIFF', f"{w}: verb {vn!r} carries force {x.get('force')!r} in the register, {force!r} in the map"))
    for vn in names:
        old = out[vn].get('reads') or []
        new = [t for t in old if t in want[vn]] + [t for t in want[vn] if t not in old]
        out[vn]['reads'] = new
        cnt = out[vn].get('count')
        if isinstance(cnt, dict):
            c2 = {t: n for t, n in cnt.items() if t in new}
            for t in new:
                if t not in c2 and measured.get(t, {}).get('edges') is not None:
                    c2[t] = measured[t]['edges']
            out[vn]['count'] = c2
    old_un = out.get('unread') if isinstance(out.get('unread'), dict) else {}
    un_want = {r['word']: (r.get('verb') or {}).get('unread') for r in rows
               if isinstance((r.get('verb') or {}).get('unread'), str) and r['verb']['unread'].strip()}
    new_un = {}
    for t, e in old_un.items():
        if t in un_want:
            e = dict(e) if isinstance(e, dict) else {}
            e['$note'] = un_want[t]
            new_un[t] = e
    for r in rows:
        t = r['word']
        if t in un_want and t not in new_un:
            m = measured.get(t) or {}
            e = {'$note': un_want[t]}
            if m.get('edges') is not None: e['count'] = m['edges']
            if m.get('nulls') is not None: e['nulls'] = m['nulls']
            new_un[t] = e
    out['unread'] = new_un
    return out, probs


# ---------------------------------------------------------------- the template
def template_copies(text):
    probs = []
    if FAMILY_RX.search(text or ''):
        probs.append(('TEMPLATE-COPY', 'knowledge/_kg_explorer.template.html holds a literal FAMILY map — the chip map is '
                                       'the register\'s `chip` column, baked as KG.fam'))
    if READ_RX.search(text or ''):
        probs.append(('TEMPLATE-COPY', 'knowledge/_kg_explorer.template.html holds a literal READ map — the two readings '
                                       'are the register\'s `reads` column, baked as KG.read'))
    return probs


# ---------------------------------------------------------------- drift
def _diff_keys(a, b, label):
    """Name what differs between two dicts at the top level, briefly."""
    out = []
    for k in sorted(set(a) | set(b)):
        if k not in a: out.append(f'{label}: {k} missing')
        elif k not in b: out.append(f'{label}: {k} not in the register')
        elif a[k] != b[k]: out.append(f'{label}: {k} differs')
    return out


def drift(reg=None, schema=None, verbs=None, template=None):
    """[(class, detail)] — every way the two written copies and the template differ from the register."""
    reg = _load(REGISTER) if reg is None else reg
    schema = _load(SCHEMA) if schema is None else schema
    verbs = _load(VERBS) if verbs is None else verbs
    if template is None:
        try:
            template = open(TEMPLATE, encoding='utf-8').read()
        except OSError:
            template = ''
    s2, p1 = schema_from(reg, schema)
    v2, p2 = verbs_from(reg, verbs)
    out = list(p1) + list(p2)
    a, b = schema['properties']['edges']['properties'], s2['properties']['edges']['properties']
    if a != b or list(a) != list(b):
        d = _diff_keys(a, b, 'meta.schema.json edges') or ['meta.schema.json edges: key order differs']
        out += [('SCHEMA-DRIFT', x) for x in d]
    for vn in _verb_names(verbs):
        if verbs[vn].get('reads') != v2[vn].get('reads'):
            out.append(('VERBS-DRIFT', f"_kg_verbs.json {vn}.reads {verbs[vn].get('reads')} ≠ register {v2[vn].get('reads')}"))
    ua, ub = verbs.get('unread') or {}, v2.get('unread') or {}
    for t in sorted(set(ua) | set(ub)):
        if t not in ub: out.append(('VERBS-DRIFT', f'_kg_verbs.json unread names {t}, which the register does not carry as unread'))
        elif t not in ua: out.append(('VERBS-DRIFT', f'_kg_verbs.json unread lacks {t}, which the register carries as unread'))
        elif (ua[t] or {}).get('$note') != (ub[t] or {}).get('$note'):
            out.append(('VERBS-DRIFT', f"_kg_verbs.json unread {t} $note differs from the register's verb.unread"))
    out += template_copies(template)
    return out


# ---------------------------------------------------------------- writing (only changed lines)
def _dumps_like(old_raw, new_obj):
    """Serialise new_obj in the file's own indent, keeping every unchanged line's ORIGINAL bytes (a file may carry
    escapes such as \\u2014 that a plain dump would rewrite) and the original final-newline convention."""
    for indent in (1, 2):
        try:
            norm_old = json.dumps(json.loads(old_raw), indent=indent, ensure_ascii=False)
        except ValueError:
            break
        raw_lines = old_raw.rstrip('\n').split('\n')
        if len(norm_old.split('\n')) == len(raw_lines):
            break
    new = json.dumps(new_obj, indent=indent, ensure_ascii=False)
    a, b = norm_old.split('\n'), new.split('\n')
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == 'equal' and len(raw_lines) == len(a):
            out += raw_lines[i1:i2]
        else:
            out += b[j1:j2]
    return '\n'.join(out) + ('\n' if old_raw.endswith('\n') else '')


def write():
    reg, schema, verbs = _load(REGISTER), _load(SCHEMA), _load(VERBS)
    s2, p1 = schema_from(reg, schema)
    v2, p2 = verbs_from(reg, verbs)
    if p1 or p2:
        for c, d in p1 + p2: print(f'  ✗ {c:13} {d}')
        print('NOT WRITTEN: fix the register first'); return 1
    n = 0
    for path, obj in ((SCHEMA, s2), (VERBS, v2)):
        raw = open(path, encoding='utf-8').read()
        new = _dumps_like(raw, obj)
        if json.loads(new) != obj:
            print(f'REFUSED: the line-keeping writer did not round-trip {os.path.relpath(path, HERE)}'); return 1
        if new != raw:
            open(path, 'w', encoding='utf-8').write(new); n += 1
            print(f'  written knowledge/{os.path.relpath(path, HERE)}')
    print(f'WRITTEN: {n} file(s)')
    return check()


def check():
    reg = _load(REGISTER)
    rows = _rows(reg)
    d = drift(reg)
    print(f"COUNTS: rows {len(rows)} · on a meta {sum(1 for r in rows if r.get('meta'))} · read by a verb "
          f"{sum(1 for r in rows if (r.get('verb') or {}).get('reads'))} · unread "
          f"{sum(1 for r in rows if (r.get('verb') or {}).get('unread'))} · with a chip {sum(1 for r in rows if r.get('chip'))}"
          f" · drift {len(d)}")
    for c, x in d: print(f'  ✗ {c:13} {x}')
    print('EDGE COPIES: ' + ('the schema, the verbs map and the template agree with the register' if not d
                             else 'DRIFT above — run python3 knowledge/gen_edge_copies.py --write'))
    return 1 if d else 0


def selftest():
    ok_all = True

    def bite(n, desc, cond):
        nonlocal ok_all
        try: ok = bool(cond())
        except Exception as ex: ok = False; desc += f'  [raised {type(ex).__name__}: {ex}]'
        ok_all &= ok
        print(f"  {'✓' if ok else '✗'} {n:>2} {desc}")

    reg, schema, verbs = _load(REGISTER), _load(SCHEMA), _load(VERBS)
    tpl = open(TEMPLATE, encoding='utf-8').read() if os.path.exists(TEMPLATE) else ''
    base = drift(reg, schema, verbs, tpl)

    def red(cls, **kw):
        args = dict(reg=reg, schema=schema, verbs=verbs, template=tpl); args.update(kw)
        return sum(1 for c, _ in drift(**args) if c == cls) == sum(1 for c, _ in base if c == cls) + 1

    print(f'gen_edge_copies selftest — control on the real files ({len(_rows(reg))} rows), then one planted drift per class')
    s2, _ = schema_from(reg, schema); v2, _ = verbs_from(reg, verbs)
    bite(0, f'CONTROL: the real files carry {len(base)} drift; writing twice is a fixed point',
         lambda: schema_from(reg, s2)[0] == s2 and verbs_from(reg, v2)[0] == v2)
    sa = copy.deepcopy(schema); sa['properties']['edges']['properties']['plantedEdgeKey'] = {'type': 'array', 'items': {'$ref': '#/definitions/edge'}}
    bite(1, 'SCHEMA-DRIFT: a schema edge key with no row goes red', lambda: red('SCHEMA-DRIFT', schema=sa))
    sb = copy.deepcopy(schema); sb['properties']['edges']['properties'].pop('containedBy')
    bite(2, 'SCHEMA-DRIFT: the schema without containedBy (meta: edge) goes red', lambda: red('SCHEMA-DRIFT', schema=sb))
    sc = copy.deepcopy(schema); sc['properties']['edges']['properties']['obeys']['items']['$ref'] = '#/definitions/edge'
    bite(3, "SCHEMA-DRIFT: obeys items pointed at `edge` (its row says obeysEdge) goes red", lambda: red('SCHEMA-DRIFT', schema=sc))
    bite(4, 'the writer puts a removed key back and drops a planted one (both drifts gone after schema_from)',
         lambda: schema_from(reg, sa)[0]['properties']['edges']['properties'] == s2['properties']['edges']['properties']
         and schema_from(reg, sb)[0]['properties']['edges']['properties'].keys() == s2['properties']['edges']['properties'].keys())
    va = copy.deepcopy(verbs); va['contains']['reads'] = [t for t in va['contains']['reads'] if t != 'consumes']
    bite(5, "VERBS-DRIFT: the verb `contains` without consumes (its row reads contains) goes red", lambda: red('VERBS-DRIFT', verbs=va))
    vb = copy.deepcopy(verbs); vb['unread']['plantedUnreadType'] = {'$note': 'planted', 'count': 1, 'nulls': 0}
    bite(6, 'VERBS-DRIFT: an unread entry with no row goes red', lambda: red('VERBS-DRIFT', verbs=vb))
    vc = copy.deepcopy(verbs); k = sorted(vc['unread'])[0]; vc['unread'][k] = dict(vc['unread'][k], **{'$note': 'planted'})
    bite(7, f'VERBS-DRIFT: the unread note of {k} edited in the map alone goes red', lambda: red('VERBS-DRIFT', verbs=vc))
    ra = copy.deepcopy(reg); ra['types'][0]['verb'] = {'reads': [{'verb': 'thirteenth', 'force': 'is'}]}
    bite(8, 'VERB-UNKNOWN: a row read by a verb the map does not define goes red', lambda: red('VERB-UNKNOWN', reg=ra))
    rb = copy.deepcopy(reg); i = next(i for i, r in enumerate(rb['types']) if (r.get('verb') or {}).get('reads'))
    rb['types'][i]['verb'] = dict(rb['types'][i]['verb'], reads=[dict(x, force='may') for x in rb['types'][i]['verb']['reads']])
    bite(9, f"FORCE-DIFF: {rb['types'][i]['word']} carrying force `may` against its verb's own goes red", lambda: red('FORCE-DIFF', reg=rb))
    rc = copy.deepcopy(reg); j = next(i for i, r in enumerate(rc['types']) if r.get('meta'))
    rc['types'][j]['meta'] = 'noSuchDefinition'
    bite(10, 'DEF-MISSING: a row whose meta names no schema definition goes red', lambda: red('DEF-MISSING', reg=rc))
    bite(11, 'TEMPLATE-COPY: a literal FAMILY map put back in the template goes red',
         lambda: red('TEMPLATE-COPY', template=tpl + "\nconst FAMILY={containedBy:'structure'};\n"))
    bite(12, 'TEMPLATE-COPY: a literal READ map put back in the template goes red',
         lambda: red('TEMPLATE-COPY', template=tpl + "\nconst READ=Object.assign({containedBy:['a','b']},KG.read);\n"))
    raw = '{\n "a": "x \\u2014 y",\n "b": 1\n}'
    bite(13, 'the writer keeps an unchanged line byte for byte (an escaped dash survives) and writes only the changed one',
         lambda: _dumps_like(raw, {'a': 'x — y', 'b': 2}) == '{\n "a": "x \\u2014 y",\n "b": 2\n}')
    print('SELFTEST: ' + ('PASS — every planted arm went red' if ok_all else 'FAIL'))
    return 0 if ok_all else 1


def main(argv):
    if '--selftest' in argv:
        return selftest()
    if '--write' in argv:
        return write()
    return check()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
