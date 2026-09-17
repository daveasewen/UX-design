#!/usr/bin/env python3
"""#282 lane RN — s282-D1: the TWO new hand-authored `restsOn` edges, and the rule `text`
of the eleven edited rules brought into line with the regenerated `_rules-index.json`.

Written BY HAND beside the 73 edges lane RL authored at #281 (s281-D6). `gen_kg_rules.py`
is NOT run: it would delete the whole authored `restsOn` block, and it does not generate
`_rules-index.json` either (its own docstring, line 59: "this script never edits
_rules-index.json") — `knowledge/guidelines/gen_rules_index.py` does, and that generator
touches no edge. So the footgun is NOT tripped by this lane and is NOT fixed by it.

Only the eleven edited rules' `text` is refreshed; the 43 other nodes whose text already
drifted from the index are left exactly as they are (not this lane's to move).

IDEMPOTENT: a second run is a no-op.
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
RN = ROOT / 'knowledge' / '_rule_nodes.json'
UX = ROOT / 'knowledge' / '_ux_principle_nodes.json'
IDX = ROOT / 'knowledge' / 'guidelines' / '_rules-index.json'

EDITED = ['aca-003', 'aid-009', 'col26-009', 'dv-bar-007', 'icon-006', 'logo26-001',
          'photo26-002', 'pict-001', 'pict-010', 'col26-016', 'neuro-026']

# The two second edges. `why` is the field the 73 use (the brief's `$why`); `grade` is the
# ux: node's grade AT THE TIME OF WRITING (s281-D6); `daveNote` is his note verbatim,
# from notes/_lanes/282/rule-notes/DAVE-EXPORT-2026-09-17.json and the #281 rule notes.
NEW = [
 {"s": "rule:mot-005", "t": "ux:pr-wcag-operable", "type": "restsOn", "fam": "rules",
  "why": "The 5-second play/pause requirement is SC 2.2.2 Pause, Stop, Hide restated at brand "
         "level: moving content that starts automatically and lasts more than five seconds must "
         "have a mechanism to pause, stop or hide it. The obligation is statutory, so it rests "
         "on the operable principle as well as on the control principle it already names.",
  "grade": "L", "choice": "a", "recommended": True, "both": True,
  "daveNote": "The principle is correct here but is is also a Ally rule we adhere to so the "
              "grade is probably wrong"},
 {"s": "rule:type26-003", "t": "ux:pr-tog-readability", "type": "restsOn", "fam": "rules",
  "why": "\"All text legible\" is the readability claim, not the ratio: text must be readable by "
         "people with less than perfect sight, which is most people over forty. The contrast "
         "number is 1.4.3; legibility is the reason the number exists.",
  "grade": "C", "choice": "a", "recommended": True, "both": True,
  "daveNote": "linked to 2 as you stated"},
]


def main():
    rn = json.loads(RN.read_text(encoding='utf-8'))
    ux = {n['id'] for n in json.loads(UX.read_text(encoding='utf-8'))['nodes']}
    idx = {r['id']: r['rule'] for r in json.loads(IDX.read_text(encoding='utf-8'))['rules']}
    ruleids = {n['id'] for n in rn['nodes']}

    before = sum(1 for e in rn['edges'] if e.get('type') == 'restsOn')
    have = {(e['s'], e['t']) for e in rn['edges'] if e.get('type') == 'restsOn'}
    added = 0
    for e in NEW:
        assert e['s'] in ruleids, f"unresolvable source {e['s']}"
        assert e['t'] in ux, f"unresolvable target {e['t']}"
        if (e['s'], e['t']) in have:
            continue
        rn['edges'].append(e)
        added += 1
    after = sum(1 for e in rn['edges'] if e.get('type') == 'restsOn')

    retext = []
    for n in rn['nodes']:
        if n.get('type') == 'rule' and n.get('ruleId') in EDITED and n.get('text') != idx[n['ruleId']]:
            n['text'] = idx[n['ruleId']]
            retext.append(n['ruleId'])

    mark = ' s282-D1 (#282 lane RN) adds TWO more authored `restsOn` lines by hand'
    if mark not in rn['$description']:
        rn['$description'] += (
            mark + ' — rule:mot-005 -> ux:pr-wcag-operable and rule:type26-003 ->'
            ' ux:pr-tog-readability — and refreshes the `text` of the eleven rules his rule'
            ' notes edited. land_rests_on.py rebuilds the restsOn block FROM THE #281 EXPORT'
            ' and would drop these two: re-land them with'
            ' notes/_lanes/282/rule-notes-land/land_rule_notes.py, which is idempotent.')

    RN.write_text(json.dumps(rn, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'restsOn edges: before {before} -> after {after} (added {added})')
    print(f'rule text refreshed on {len(retext)}: ' + ' '.join(retext))
    return 0


if __name__ == '__main__':
    sys.exit(main())
