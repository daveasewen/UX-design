#!/usr/bin/env python3
"""304-J: ask Jev one Noul per sampled edge through knowledge/_jev.py (receipts appended by the adapter).
The authored $why/$note is NOT sent — Jev sees only what the two nodes ARE and what the relation means."""
import sys, os, json, time
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
sys.path.insert(0, os.path.join(REPO, 'knowledge'))
import _jev as J
MEAN = {
 'obeys': 'The source component is designed to follow the target rule or principle: the target constrains or shapes how this component looks or behaves.',
 'providesRole': 'The source component can fill the target role: when a page slot asks for this role, this component is a suitable thing to put there.',
 'answersIntent': 'The source component answers the target intent: it is a suitable way to show someone the question the intent describes.',
 'hasDataShape': 'The source component takes data of the target shape: the shape describes the data this component is fed and draws.',
 'yieldsTo': 'The source component should give way to the target component in some circumstance: the two do overlapping jobs, and under some condition the target is the better choice instead of the source.',
 'bindsToken': "The source component's styling uses at least one design token from the target token group.",
 'appliesTo': 'The source WCAG success criterion applies to the target component: an accessibility audit of this component would need to check this criterion.',
 'tensionWith': 'The two principles pull in opposite directions in some design situation: following one fully can work against the other, so a designer has to balance them.',
}
Q = J.noul(
  "Does the relation described in `relation.meaning` genuinely hold from `source` to `target`, judged from what each of them is?",
  true="The relation holds: given what the source is and what the target says, a design-system expert would accept this link as correct.",
  false="The relation does not hold or is a stretch: the target is about something else, fits a different kind of component, or the two do not relate in the stated way.")
here = os.path.dirname(os.path.abspath(__file__))
cands = json.load(open(os.path.join(here, 'candidates.json')))
lo, hi = int(sys.argv[1]), int(sys.argv[2])
res_path = os.path.join(here, 'results-edges.jsonl')
for c in cands[lo:hi]:
    state = {'relation': {'name': c['edge_type'], 'meaning': MEAN[c['edge_type']]}, 'source': c['source'], 'target': c['target']}
    try:
        r = J.ask(state, {'holds': Q}, note='304-J edge probe %s %s (%s)' % (c['eid'], c['edge_type'], c['origin']))
        a = r['answers']['holds']
        row = {'eid': c['eid'], 'edge_type': c['edge_type'], 'origin': c['origin'], 'p_true': a.get('noul', a.get('probability')),
               'raw': a, 'latency_ms': r['_latency_ms'], 'request_id': r['_request_id'], 'model': r.get('model'), 'usage': r.get('usage')}
    except Exception as ex:
        row = {'eid': c['eid'], 'edge_type': c['edge_type'], 'origin': c['origin'], 'error': type(ex).__name__ + ': ' + str(ex)[:200]}
    open(res_path, 'a').write(json.dumps(row, ensure_ascii=False) + '\n')
    print(row['eid'], row.get('p_true'), row.get('latency_ms'), row.get('error', ''))
