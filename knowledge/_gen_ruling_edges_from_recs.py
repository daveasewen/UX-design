#!/usr/bin/env python3
"""Derive knowledge/_ruling_edges.json — the AUTHORED ruling->ruling edge store — from
lane E's judgement record, under ruling s267-D3 (#267, 2026-09-10).

    python3 knowledge/_gen_ruling_edges_from_recs.py            # writes knowledge/_ruling_edges.json
    python3 knowledge/_gen_ruling_edges_from_recs.py --print    # report only, writes nothing

Inputs (read-only):
  notes/_lanes/267/E/edge-recs.json   78 rows; `type` and `dir` ARE the ratified edge set (s267-D3)
  knowledge/_rulings.json             for the store's own authored supersession FIELDS

Rules applied, each from the ruling:
  * `dir` == "t->s"  -> swap s/t (one row: #40, s172-D3 bounds s181-D1).
  * verdict REJECT / type "mentions" -> NOT an authored edge; the pair is listed in
    `ratified_plain_mentions` so the explorer's regex loop never re-proposes it.
  * Q1 — nine rows supersede or retire ONE CLAUSE of the target: their type becomes
    `supersedesClause` (recs #5, #19, #34, #42, #52, #55, #64, #69, #70 — the ruling's list,
    identical to the Q1 list on reviews/EDGE-JUDGEMENT-267-2026-09-10-v1.html:68).
  * Q2 — when ruling A RECORDS that B supersedes C, the edge is B -> C with A as evidence.
    One row is rewritten by this: #42, written inside s188-D3 about s188-D1 -> s183-D1.
    (#19 is NOT rewritten: the store's own s142-D1.superseded_note_s168_D1 field names
    s168-D1 as the closer, so the actor and the recorder are the same node there.)
  * the store's authored supersession FIELDS are scanned across every ruling (never typed as
    literal rows): `superseded_by: X` on C yields X -> C; a `superseded_note_<X>` key on C
    yields X -> C.  Each such edge carries source "store-field:<key>".
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECS = os.path.join(ROOT, 'notes', '_lanes', '267', 'E', 'edge-recs.json')
RULINGS = os.path.join(ROOT, 'knowledge', '_rulings.json')
OUT = os.path.join(ROOT, 'knowledge', '_ruling_edges.json')

CLAUSE_SCOPED = {5, 19, 34, 42, 52, 55, 64, 69, 70}          # s267-D3 Q1
Q2_REWRITE = {42: {'s': 's188-D1', 'recorder': 's188-D3'}}   # s267-D3 Q2


def from_recs():
    recs = json.load(open(RECS))
    assert len(recs) == 78, f'expected 78 recs, got {len(recs)}'
    edges, plain = [], []
    for r in recs:
        n, s, t = r['n'], r['s'], r['t']
        pair = [s, t]                       # the pair the regex loop proposed, before any swap
        if r['type'] == 'mentions' or r['verdict'] == 'REJECT':
            plain.append({'pair': pair, 'rec': n, 'reason': r['reason'][:200]})
            continue
        if r.get('dir') == 't->s':
            s, t = t, s
        ty = 'supersedesClause' if n in CLAUSE_SCOPED else r['type']
        ev = [f"lane E rec #{n} ({r['verdict']}, tier {r['tier']}, {r['confidence']} confidence)",
              r['phrase'][:220]]
        rw = Q2_REWRITE.get(n)
        if rw:
            ev.append(f"recorded in {s} (s267-D3 Q2: the edge is carried by the actor, {rw['s']}, "
                      f"not by the recorder)")
            s = rw['s']
        edges.append({'s': s, 't': t, 'type': ty, 'evidence': ev, 'ratified': 's267-D3',
                      'source': 'edge-recs#%d' % n, 'from_pair': pair})
    return edges, plain


FIELD_RX = re.compile(r'^superseded_by$|^superseded_note_(s\d{2,3}[-_]D\d+)$')


def from_store_fields():
    """Scan EVERY ruling for authored supersession fields. Nothing is typed by hand."""
    R = [x for x in json.load(open(RULINGS)).get('rulings', []) if isinstance(x, dict) and x.get('id')]
    ids = {x['id'] for x in R}
    out = []
    for r in R:
        for k, v in r.items():
            m = FIELD_RX.match(k)
            if not m:
                continue
            if k == 'superseded_by':
                actor = str(v).strip()
            else:
                actor = m.group(1).replace('_', '-')
            if actor not in ids or actor == r['id']:
                continue
            out.append({'s': actor, 't': r['id'], 'type': 'supersedes',
                        'evidence': [f"knowledge/_rulings.json: {r['id']}.{k}", str(v)[:220]],
                        'ratified': 's267-D3', 'source': 'store-field:' + k,
                        'from_pair': [actor, r['id']]})
    return out


def build():
    edges, plain = from_recs()
    have = {(e['s'], e['t']) for e in edges}
    field = []
    for e in from_store_fields():
        if (e['s'], e['t']) in have:
            continue                                     # already ratified from the recs
        # a field edge may be the clause-scoped shape the recs called out; keep the field's word
        have.add((e['s'], e['t']))
        field.append(e)
    if field and field[0]['t'] == 's142-D1':
        pass
    # s142-D1's note is clause-scoped by its own words ("SUPERSEDED IN PART")
    for e in field:
        if 'IN PART' in (e['evidence'][1] or '').upper():
            e['type'] = 'supersedesClause'
    all_edges = edges + field
    doc = {
        '_README': ("AUTHORED ruling->ruling edges, ratified by s267-D3 (#267, 2026-09-10): lane E's "
                    "78 judgements (notes/_lanes/267/E/edge-recs.json) with `dir` applied, Q1 "
                    "clause-scoped supersession typed `supersedesClause`, Q2 recorded supersessions "
                    "carried by the ACTOR with the recorder as evidence, plus the store's own "
                    "authored supersession fields. Regenerate with "
                    "knowledge/_gen_ruling_edges_from_recs.py; read by knowledge/_build_kg_explorer.py, "
                    "which draws these SOLID (authored) and must never re-propose a pair listed here "
                    "or in `ratified_plain_mentions`. `ratified_plain_mentions` are the 31 rows Dave "
                    "ratified as PLAIN CITATIONS: they stay derived `mentions`, never authored."),
        'ratified': 's267-D3',
        'generated_from': ['notes/_lanes/267/E/edge-recs.json', 'knowledge/_rulings.json'],
        'edges': all_edges,
        'ratified_plain_mentions': plain,
    }
    return doc, len(edges), len(field), len(plain)


if __name__ == '__main__':
    doc, n_recs, n_field, n_plain = build()
    from collections import Counter
    c = Counter(e['type'] for e in doc['edges'])
    print(f"authored edges {len(doc['edges'])}  (from recs {n_recs} · from store fields {n_field})")
    for k, v in sorted(c.items(), key=lambda x: -x[1]):
        print(f"  {k:18s} {v}")
    print(f"ratified plain mentions {n_plain}")
    for e in doc['edges']:
        if e['source'].startswith('store-field'):
            print('  store-field edge:', e['s'], '->', e['t'], e['type'], '|', e['source'])
    if '--print' not in sys.argv:
        json.dump(doc, open(OUT, 'w'), indent=1, ensure_ascii=False)
        print('wrote', OUT)
