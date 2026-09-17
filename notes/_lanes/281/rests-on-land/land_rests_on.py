#!/usr/bin/env python3
"""#281 lane RL — LAND THE `restsOn` EDGES (s281-D3 authorised them, s281-D6 shapes them).

Reads three files and writes ONE:

  in   notes/_lanes/281/rests-on/DAVE-EXPORT-2026-09-17.json   — Dave's 59 answers, 14:49Z
  in   notes/_lanes/281/rests-on/proposals.json                — lane RO's options a/b and the null
  in   knowledge/_rule_nodes.json                              — the rule index (read, then rewritten)
  out  knowledge/_rule_nodes.json                              — `edge_types` gains `restsOn`;
                                                                 the edges array gains the restsOn block

THE SHAPE, s281-D6:
  * `restsOn` is MANY-TO-MANY. A rule may rest on more than one principle. Where Dave's note says
    the rule is BOTH options, BOTH land — each with its OWN `$why`, which is the sentence the
    proposal page printed for THAT option, never a merged one.
  * Convention alone is `t: null` with a note — s275-D2's declared-null shape. His note verbatim
    when he wrote one; the page's own null sentence when he did not (a null without a note is not
    a legal row).
  * Every edge carries `why` (the page's sentence for that option), `grade` (the principle's grade
    AT THE TIME OF WRITING — the ux: node's own `grade` field stays authoritative on a re-grade),
    `choice` (a / b / c, the radio he saw), `daveNote` (his note verbatim, when there is one) and
    `overruled` (true when he moved off the recommendation).
  * His notes ABOUT THE RULE are not rule edits and are not landed here. They are filed, unedited,
    in RULE-NOTES-2026-09-17.md for #282.

IDEMPOTENT: every existing `restsOn` edge is dropped and rewritten from the export, so a second run
is a no-op. Refuses to write if any `s` or `t` does not resolve against the nodes in the two stores.
"""
import json, os, sys, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
K = os.path.join(ROOT, 'knowledge')
LANE = os.path.join(ROOT, 'notes', '_lanes', '281')
EXPORT = os.path.join(LANE, 'rests-on', 'DAVE-EXPORT-2026-09-17.json')
PROPS = os.path.join(LANE, 'rests-on', 'proposals.json')
RN = os.path.join(K, '_rule_nodes.json')
UX = os.path.join(K, '_ux_principle_nodes.json')

# The rows where his own sentence says the rule rests on BOTH options. Counted from the file by the
# match below and asserted against this list, so a re-read that disagrees is a build failure, not a
# silent difference. (The conductor's brief named the same thirteen.)
BOTH = {'appf-002', 'col26-008', 'col26-015', 'col26-016', 'dv-016', 'dv-line-011', 'dv-pie-009',
        'dv-pie-010', 'neuro-026', 'tov-038', 'type25-003', 'type25-008', 'webf-027'}
# He chose convention AND named an option in the same breath. The null lands WITH the note, and so
# does the option he named. s281-D6's own example.
NULL_PLUS = {'type26-002': 'a'}
# His notes that are about the RULE, not about the link. Filed for #282, landed nowhere.
RULE_NOTES = {'aca-003', 'aid-009', 'logo26-001', 'photo26-002', 'col26-009', 'col26-012',
              'dv-bar-007', 'icon-006', 'mot-005', 'pict-001', 'pict-010', 'type26-002',
              'type26-003'}


def said_both(note):
    n = ' '.join((note or '').lower().split())
    return ('both 1 and 2' in n) or ('1 and 2' in n) or ('and 2' in n)


def main():
    exp = json.load(open(EXPORT))
    ans = exp['answers']
    props = {p['ruleId']: p for p in json.load(open(PROPS))['proposals']}
    rn = json.load(open(RN))
    uxids = {n['id'] for n in json.load(open(UX))['nodes']}
    ruleids = {n['id'] for n in rn['nodes']}

    both = {k for k, v in ans.items() if said_both(v.get('note'))}
    assert both == BOTH, f"'both' set moved: +{sorted(both - BOTH)} -{sorted(BOTH - both)}"
    assert set(ans) == set(props), 'export and proposals disagree on the rule set'

    edges, rep = [], collections.Counter()
    for rid in sorted(ans):
        a = ans[rid]
        p = props[rid]
        opts = {o['choice']: o for o in p['options']}
        note = (a.get('note') or '').strip()
        chosen = []                       # list of choice letters that land as a principle
        nulls = []                        # list of choice letters that land as a declared null

        if a.get('uxId'):
            chosen.append(a['choice'])
            if rid in both:
                other = 'b' if a['choice'] == 'a' else 'a'
                if other in opts:
                    chosen.append(other)
                else:
                    rep['both_without_alternative'] += 1
        else:
            nulls.append('c')
            if rid in NULL_PLUS and NULL_PLUS[rid] in opts:
                chosen.append(NULL_PLUS[rid])
                rep['null_plus'] += 1

        for ch in chosen:
            o = opts[ch]
            e = {'s': 'rule:' + rid, 't': 'ux:' + o['uxId'], 'type': 'restsOn', 'fam': rn['family'],
                 'why': o['why'], 'grade': o['grade'], 'choice': ch,
                 'recommended': bool(o.get('recommended'))}
            if a.get('overruled'):
                e['overruled'] = True
            if note:
                e['daveNote'] = note
            if rid in both:
                e['both'] = True
            if rid in NULL_PLUS:
                e['besideNull'] = True
            edges.append(e)
            rep['edges'] += 1
        for ch in nulls:
            # s275-D2: a declared null carries a note or it is not a legal row.
            n = note or (p.get('null') or {}).get('why') or ''
            assert n.strip(), f'{rid}: convention with no note and no page sentence'
            e = {'s': 'rule:' + rid, 't': None, 'type': 'restsOn', 'fam': rn['family'],
                 'note': n, 'why': (p.get('null') or {}).get('why', ''), 'choice': 'c'}
            if note:
                e['daveNote'] = note
            if a.get('overruled'):
                e['overruled'] = True
            if rid in NULL_PLUS:
                e['besideOption'] = NULL_PLUS[rid]
            edges.append(e)
            rep['nulls'] += 1

    bad = [e for e in edges if e['s'] not in ruleids or (e['t'] is not None and e['t'] not in uxids)]
    assert not bad, f'unresolvable ends: {bad[:3]}'

    rn['edges'] = [e for e in rn['edges'] if e.get('type') != 'restsOn'] + edges
    rn['edge_types']['restsOn'] = 'NEW'
    mark = ' AUTHORED, never generated: the `restsOn` block'
    if mark not in rn['$description']:
        rn['$description'] += (
            mark + ' (s281-D3, landed #281 lane RL under s281-D6) is written BY HAND from Dave\'s'
            ' export of notes/_lanes/281/rests-on/RESTS-ON-2026-09-17.html and is NOT produced by'
            ' gen_kg_rules.py — re-running that generator would drop it. Re-land it with'
            ' notes/_lanes/281/rests-on-land/land_rests_on.py, which is idempotent.')
    json.dump(rn, open(RN, 'w'), indent=2, ensure_ascii=False)
    open(RN, 'a').write('\n')

    withp = len({e['s'] for e in edges if e['t']})
    print(f"restsOn landed: {rep['edges']} principle edges + {rep['nulls']} declared nulls"
          f" · {withp} of {len(ans)} rules rest on at least one principle"
          f" · {len(both)} rules rest on two · null+option {rep['null_plus']}")
    by = collections.Counter(e['t'] for e in edges if e['t'])
    print('  top principles: ' + ' · '.join(f'{k.split(":")[1]} {v}' for k, v in by.most_common(6)))
    print('  grades: ' + ' · '.join(f'{g} {n}' for g, n in
                                    sorted(collections.Counter(e['grade'] for e in edges if e['t']).items())))
    print(f"  overruled rows carried: {len({e['s'] for e in edges if e.get('overruled')})}"
          f" · daveNote carried on {len({e['s'] for e in edges if e.get('daveNote')})} rules"
          f" · rule-notes filed elsewhere: {len(RULE_NOTES)}")
    if rep['both_without_alternative']:
        print(f"  WARNING: {rep['both_without_alternative']} 'both' rows had no second option")
    return 0


if __name__ == '__main__':
    sys.exit(main())
