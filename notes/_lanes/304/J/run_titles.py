#!/usr/bin/env python3
"""304-J step 3b: hand labels for the 20 sampled titles (frozen in this file, hashed below) then one Noul each."""
import sys, os, json, hashlib
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
sys.path.insert(0, os.path.join(REPO, 'knowledge')); import _jev as J
here = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(here, 'node-titles-sample.json')))
# hand label: does the title ALONE say what kind of thing the node is and what it is about?
HAND = [False]*5 + [True, True, True, True, False] + [False]*5 + [False, False, True, True, True]
assert len(HAND) == len(S) == 20
frozen = hashlib.sha256(json.dumps([[s['id'], h] for s, h in zip(S, HAND)]).encode()).hexdigest()
Q = J.noul("Reading only `title`, can someone new to this project tell what this item is — both what kind of thing it is and what it is about — without looking anything up?",
           true="Yes: the title names or clearly implies the kind of thing and its subject in plain words.",
           false="No: the title is a code, an identifier, a single ambiguous word, or internal jargon that only makes sense to someone who already knows the project.")
out = []
for s, h in zip(S, HAND):
    try:
        r = J.ask({'title': s['label']}, {'says_what_it_is': Q}, note='304-J node-title probe %s' % s['id'][:80])
        p = r['answers']['says_what_it_is'].get('noul'); ms = r['_latency_ms']; rid = r['_request_id']
    except Exception as ex:
        p = None; ms = None; rid = type(ex).__name__
    row = dict(s, hand=h, mech_says_nothing=s['class'] in 'AB', mech_opaque_or_slug=s['class'] in 'ABC', p_says=p, latency_ms=ms, request_id=rid)
    out.append(row); print(s['class'], h, p, ms, s['label'][:60])
json.dump({'hand_labels_sha256': frozen, 'rows': out}, open(os.path.join(here, 'results-titles.json'), 'w'), indent=1, ensure_ascii=False)
