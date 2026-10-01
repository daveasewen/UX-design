#!/usr/bin/env python3
"""#311 overnight lane D1 — s308-D20 (item 5, one `why` field required by type) and s308-D21 (item 6, one
maker field on every edge) written into knowledge/_edge_register.json. Run once from the repo root; it
rewrites the register (indent 1, ensure_ascii False, the file's own form) and prints what moved.

Per row it replaces `reason` with `why` and rewrites `maker` from its measured `today` into the one rule
the explorer stamps on every edge. It never touches storage; the metas are lane C0's tonight.
"""
import json, os, sys

REG = 'knowledge/_edge_register.json'
reg = json.load(open(REG, encoding='utf-8'))

REQUIRED = ['obeys', 'restsOn', 'mustNotNeighbour', 'yieldsTo', 'groupsWith', 'composedOf', 'delegatesTo',
            'drivesConsumer', 'governedBy']          # s308-D20, verbatim list
RULING_TO_RULING = ['bounds', 'confirms', 'corrects', 'enacts', 'extends', 'narrows', 'refines', 'retires',
                    'supersedes', 'supersedesClause']  # 'The ruling-to-ruling types already carry evidence that serves'

D21 = "s308-D21 (Dave 2026-09-29 09:26 BST, '6. One maker field on every edge — Take it')"

# the hand-made rows: whose hand, and the ruling it was written under (read from each row's own maker note)
HAND = {
    'composedOf': ('claude/s268-D5', 'a Claude lane wrote the line into the meta under s268-D5; carried verbatim through a gen_kg_edges.py rebuild (s268-D6)'),
    'delegatesTo': ('claude/s268-D5', 'a Claude lane wrote the line into the meta under s268-D5'),
    'drivesConsumer': ('claude/s268-D5', 'a Claude lane wrote the line into the meta from its $contract under s268-D5 (s263-D4)'),
    'groupsWith': ('claude/s245-D7', 'a Claude lane wrote the line into the meta under s245-D7'),
    'obeys': ('claude/s276-D3', 'the metas\' lines: a Claude lane wrote each line and its reason into the meta under s276-D3 (s277-D1..D3 for the four chart metas)'),
    'restsOn': ('Dave/s281-D6', 'Dave\'s own answers — his export of the 59-card page (s281-D3 authorised, s281-D6 landed); #281 lane RL keyed them into _rule_nodes.json'),
}
CASES = {
    'obeys': [{'when': {'fam': 'assets'}, 'made': 'hand', 'by': 'Dave/s282-D5',
               'note': 'the 12 logo lines: Dave\'s own export of the logo-review page (s282-D5), keyed into _logo_nodes.json by #282 lane LL; each stored line carries this maker itself'}],
    'evidencedBy': [{'when': {'fam': 'uxprinciples'}, 'made': 'generated', 'by': 'gen_kg_principles.py',
                     'note': 'a principle\'s sources (s281-D1)'}],
    'containedBy': [{'when': {'from': 'subcomponent'}, 'made': 'generated', 'by': '_build_kg_explorer.py',
                     'note': 'a subcomponent\'s line, derived from its container\'s own subComponents entry (s308-D26)'}],
}
SCRIPT_BY = {'evidencedBy': '_build_kg_explorer.py'}


def base_script(s):
    first = (s or '').split()[0] if s else ''
    return os.path.basename(first)


moved = {'why': 0, 'maker': 0}
for row in reg['types']:
    w = row['word']
    old_reason = row.pop('reason', None) or {}
    today = old_reason.get('today') or {}
    req = w in REQUIRED
    why = {'field': 'why', 'required': req, 'floor': 40 if w == 'obeys' else None}
    if w in RULING_TO_RULING:
        why['servedBy'] = 'evidence'
        why['basis'] = 'not required: the ruling-to-ruling types already carry evidence that serves (s308-D20); _ruling_edges.json carries evidence[] on every line and the graph folds it into the note'
    elif req:
        why['basis'] = 'required: a hand-made judgement named in s308-D20' + (
            '; the 40-character floor is kept (s308-D20, meta.schema.json definitions.obeysEdge)' if w == 'obeys' else '')
    else:
        why['basis'] = 'not required: generated structure or a type s308-D20 does not name'
    why['today'] = {'spelled': today.get('field'), 'carried': today.get('carried'), 'note': today.get('basis')}
    if w == 'obeys':
        why['today']['spelled'] = '$why in the metas (the one name `why` is owed there: the metas were lane C0\'s on the night #311 lane D1 ran); `why` in _logo_nodes.json; the explorer carries it as `why` on the edge'
    row['why'] = why
    moved['why'] += 1

    m = row['maker'].get('today') or {}
    made = m.get('made')
    if made == 'never stored':
        mk = {'made': 'none', 'by': None, 'value': None,
              'note': 'never stored — the read side of its opposite (s308-D18); no edge of it carries a maker'}
    elif made == 'hand':
        by, note = HAND[w]
        mk = {'made': 'hand', 'by': by, 'value': 'hand:' + by, 'note': note}
    elif made == 'ratified':
        by = 's267-D3' if w in RULING_TO_RULING else 's135-D4'
        note = ('lane E\'s #267 judgements, ratified by s267-D3, written by knowledge/_gen_ruling_edges_from_recs.py'
                if w in RULING_TO_RULING else
                'the s135-D4 ATTACH verdicts the ruling\'s own governs[] does not carry (s308-D18), kept by Dave (s308-D35); written by knowledge/gen_kg_edges.py')
        mk = {'made': 'ratified', 'by': by, 'value': 'ratified:' + by, 'note': note}
    else:
        by = SCRIPT_BY.get(w) or base_script(m.get('script'))
        mk = {'made': 'generated', 'by': by, 'value': 'generated:' + by, 'note': m.get('script')}
    if w in CASES:
        mk['cases'] = [dict(c, value=c['made'] + ':' + c['by']) for c in CASES[w]]
    mk['store'] = m.get('store')
    mk['basis'] = D21 + ' — one rule per type, stamped on every edge by knowledge/_build_kg_explorer.py; a stored line that carries its own `maker` keeps it'
    row['maker'] = mk
    moved['maker'] += 1

F = reg['$schema']['fields']
new_fields = {}
for k, v in F.items():
    if k == 'reason':
        new_fields['why'] = ("s308-D20: the ONE name for an edge's reason is `why`. `required` says whether every edge "
                             "of the type must carry one (true on the nine hand-made judgements s308-D20 names), "
                             "`floor` its minimum length in characters (40 on obeys, kept), `servedBy` where another "
                             "field serves (the ruling-to-ruling types' evidence), `today` how it is spelled and "
                             "carried in storage. CHECKED by _validate_edges.py --check: WHY-MISSING, WHY-SHORT.")
    elif k == 'maker':
        new_fields['maker'] = ("s308-D21: who made the type's edges, one of three — `hand` (by: whose/ruling), "
                               "`generated` (by: which script) or `ratified` (by: which ruling); `none` only on a "
                               "read-side row that stores nothing. `value` is the string every edge of the type "
                               "carries as its `maker` (`<made>:<by>`), stamped by knowledge/_build_kg_explorer.py; "
                               "`cases` override it by the edge's family (`fam`) or start kind (`from`); a stored line "
                               "carrying its own `maker` keeps it. It replaces the `authored` flag, which is retired "
                               "from the graph. CHECKED by _validate_edges.py --check: NO-MAKER, AUTHORED-FLAG.")
    else:
        new_fields[k] = v
reg['$schema']['fields'] = new_fields
reg['$schema']['rulings']['s308-D20'] = 'item 5 — `why` per row (#311 lane D1)'
reg['$schema']['rulings']['s308-D21'] = 'item 6 — `maker` per row, stamped on every edge; `authored` retired (#311 lane D1)'

with open(REG, 'w', encoding='utf-8') as f:
    f.write(json.dumps(reg, indent=1, ensure_ascii=False) + '\n')
print('moved', moved, '· required', sum(1 for r in reg['types'] if r['why']['required']),
      '· makers', {m: sum(1 for r in reg['types'] if r['maker']['made'] == m) for m in ('hand', 'generated', 'ratified', 'none')})
