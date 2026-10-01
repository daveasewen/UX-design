#!/usr/bin/env python3
"""#313 lane D4 (W-308ie, s308-D16) — give the edge register the two columns its consumers kept copies of.

  meta  — the `definitions` entry the meta schema's `edges.<word>` key takes its items from ("edge" or
          "obeysEdge"), or null when the type is not stored on a component meta. Read from
          knowledge/components/meta.schema.json as it stands, so the schema's key set is unchanged.
  chip  — the explorer's chip family the type is drawn under (`FAMILY[type]` on the page), or null when the
          type has no chip of its own (its edges carry `fam`). Read from the literal FAMILY map in
          knowledge/_kg_explorer.template.html as it stands; the map's comments move VERBATIM to `$chips`.

and carries inFamily, which neither the verbs nor `unread` named since #281, as unread (a null carried; a verb
for it is a ruling, not a default). Idempotent: a second run changes nothing. `--check` writes nothing.
Run from the repo root.
"""
import json, os, re, sys

K = 'knowledge'
REG = os.path.join(K, '_edge_register.json')
SCHEMA = os.path.join(K, 'components', 'meta.schema.json')
TPL = os.path.join(K, '_kg_explorer.template.html')
STAMP = '#313 lane D4, 2026-10-01'


def family_map(tpl):
    m = re.search(r'const FAMILY\s*=\s*\{(.*?)\};', tpl, re.S)
    if not m:
        return None, []
    body = m.group(1)
    comments = [ln.strip()[3:] if ln.strip().startswith('// ') else ln.strip()[2:]
                for ln in body.split('\n') if ln.strip().startswith('//')]
    fam = dict(re.findall(r'([A-Za-z_]\w*)\s*:\s*[\'"](\w+)[\'"]', re.sub(r'//[^\n]*', '', body)))
    return fam, comments


def main(argv):
    raw = open(REG, encoding='utf-8').read()
    reg = json.loads(raw)
    schema = json.load(open(SCHEMA, encoding='utf-8'))
    props = schema['properties']['edges']['properties']
    meta = {k: v['items']['$ref'].rsplit('/', 1)[1] for k, v in props.items()
            if not k.startswith('$') and isinstance(v, dict) and isinstance(v.get('items'), dict)}
    tpl = open(TPL, encoding='utf-8').read()
    fam, comments = family_map(tpl)
    if fam is None:
        prior = reg.get('$chips') or {}
        fam = {}
        comments = prior.get('history') or []
        for r in reg['types']:
            if r.get('chip'):
                fam[r['word']] = r['chip']
        if not fam:
            print('REFUSED: the template holds no FAMILY map and the register carries no chip column'); return 2
    words = {r['word'] for r in reg['types']}
    try:
        vmap = json.load(open(os.path.join(K, '_kg_verbs.json'), encoding='utf-8')).get('unread') or {}
    except (OSError, ValueError):
        vmap = {}
    # #308 lane E cut each copied unread note at 300 characters: where the register's note is a cut prefix of the
    # verbs map's, the register takes the full text (it becomes the record the map is written from). A note that
    # differs otherwise is the register's newer word (defaultFor, #311 D3) and is kept.
    for r in reg['types']:
        v = r.get('verb') or {}
        full = ((vmap.get(r['word']) or {}).get('$note') or '')
        if v.get('unread') and full != v['unread'] and len(v['unread']) >= 300 and full.startswith(v['unread']):
            v['unread'] = full
    out_types = []
    for r in reg['types']:
        w = r['word']
        nr = {}
        for k, v in r.items():
            if k in ('meta', 'chip'):
                continue
            nr[k] = v
            if k == 'family':
                nr['meta'] = meta.get(w)
                nr['chip'] = fam.get(w)
        if 'family' not in r:
            nr['meta'] = meta.get(w); nr['chip'] = fam.get(w)
        if w == 'inFamily' and 'missing' in (nr.get('verb') or {}):
            v = nr['verb']
            nr['verb'] = {'reads': [], 'unread': ("ux:<principle> → family:<research family> — the THEORY view's own lines "
                                                  "(s281-D1). Read by no verb: a verb for it is a ruling, not a default."),
                          'was': ('missing from #281 to #313: ' + v['missing'] + '; carried as unread by ' + STAMP),
                          'source': 'this register (' + STAMP + ')'}
        out_types.append(nr)
    reg['types'] = out_types
    unknown_meta = sorted(set(meta) - words)
    unknown_chip = sorted(set(fam) - words - set(reg.get('$absent') or {}))
    f = reg['$schema']['fields']
    nf = {}
    for k, v in f.items():
        if k in ('meta', 'chip'):
            continue
        nf[k] = v
        if k == 'family':
            nf['meta'] = ("W-308ie (#313 lane D4): the `definitions` entry a component meta's `edges.<word>` list takes its "
                          "items from (\"edge\" or \"obeysEdge\"), or null when the type is not stored on a meta. "
                          "knowledge/components/meta.schema.json's `edges` keys are WRITTEN from this column by "
                          "knowledge/gen_edge_copies.py (the $-prefixed annotation keys and each key's description stay "
                          "the schema's own); _validate_edges.py --coverage refuses drift (COPY-DRIFT).")
            nf['chip'] = ("W-308ie (#313 lane D4): the explorer's chip family the type is drawn under (the page's "
                          "`FAMILY[type]`), or null when the type has no chip of its own and its edges carry `fam`. "
                          "Not the same as `family` (the storage family the builder stamps). The builder bakes this "
                          "column into the page as KG.fam; the template holds no copy. The map's comments, as they "
                          "stood, are kept verbatim in `$chips.history`.")
    nf['verb'] = (f.get('verb', '') + " SINCE W-308ie (#313 lane D4) THIS COLUMN IS THE RECORD: the twelve verbs' "
                  "`reads` lists and the `unread` block in knowledge/_kg_verbs.json are WRITTEN from it by "
                  "knowledge/gen_edge_copies.py (each verb's force, direction and definition stay the map's own), and "
                  "_validate_edges.py --coverage refuses drift (COPY-DRIFT). `source` names where the row's reading "
                  "was first taken from.") if 'SINCE W-308ie' not in f.get('verb', '') else f['verb']
    reg['$schema']['fields'] = nf
    reg['$doc']['not_yet'] = (
        "DONE (W-308ie, #313 lane D4): the three consumers read this file. The meta schema's `edges` keys and their item "
        "shape are written from the `meta` column, and the twelve verbs' `reads` lists and the `unread` block of "
        "knowledge/_kg_verbs.json from the `verb` column, both by knowledge/gen_edge_copies.py (--write; --check refuses "
        "drift, and _validate_edges.py --coverage carries the same refusal as COPY-DRIFT); the explorer's chip map is "
        "baked from the `chip` column (KG.fam) and its two readings from `reads` (KG.read) — the template holds neither "
        "map. History: since s308-D18 (#308 lane E round 2) the explorer took each type's two readings from here and "
        "the three named the stored side of each pair as this file does; until #313 they held their own lists of types.")
    reg['$chips'] = {
        'what': ("THE CHIP MAP (W-308ie, #313 lane D4). The explorer page drew each edge type under the chip its "
                 "literal FAMILY map named (knowledge/_kg_explorer.template.html, to 1.37). That map is now the `chip` "
                 "column of each row, baked into the page by knowledge/_build_kg_explorer.py as KG.fam. The map's own "
                 "comments are kept here VERBATIM, in the order they stood, because they are the reasons each chip "
                 "was chosen."),
        'from': 'knowledge/_kg_explorer.template.html const FAMILY at cdf17a12',
        'notInRows': {t: fam[t] for t in sorted(set(fam) - words)},
        'notInRowsNote': ("keys the map carried that are not rows: `overrides` is in `$absent` (no edge of it exists), "
                          "so the page no longer lists a chip for it; nothing else is dropped."),
        'history': comments,
    }
    if 'overrides' in (reg.get('$absent') or {}):
        a = reg['$absent']['overrides']
        a['namedIn'] = [x for x in a.get('namedIn') or [] if 'FAMILY' not in x] + [
            '_build_kg_explorer.py VERB_STEMS (a mention-verb stem; the page\'s FAMILY map no longer names it, #313 D4)']
    new = json.dumps(reg, indent=1, ensure_ascii=False) + '\n'
    print(f"rows {len(out_types)} · meta non-null {sum(1 for r in out_types if r.get('meta'))} · chip non-null "
          f"{sum(1 for r in out_types if r.get('chip'))} · schema keys not rows {unknown_meta} · chip keys not rows "
          f"{unknown_chip} · history lines {len(comments)} · changed {new != raw}")
    if unknown_meta or unknown_chip:
        print('REFUSED: a consumer names a type with no row'); return 1
    if '--check' not in argv and new != raw:
        open(REG, 'w', encoding='utf-8').write(new)
        print('written', REG)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
