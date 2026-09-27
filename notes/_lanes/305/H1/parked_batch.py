#!/usr/bin/env python3
"""#305 H1 — call 39 (P-272-1, P-277-4 -> enacted; s246-D3, s114-D2 parked) and call 38 kind 4 (seven open halves parked)
written into knowledge/_parked.json TEXTUALLY (the register is hand-authored and does not round-trip through json.dump):
two `"status": "parked"` literals become `"status": "enacted"` + a `closed_by` line, and nine items are appended before the
closing `]`. PROVEN: removing the inserted spans and restoring the two literals gives back the original bytes; the result
parses, `_parked.load()` accepts it, and every other item is equal.   python3 parked_batch.py --dry-run | --write"""
import json, sys
sys.path.insert(0, 'knowledge'); import _parked
WRITE = '--write' in sys.argv
P = 'knowledge/_parked.json'
orig = open(P, encoding='utf-8').read(); data = json.loads(orig)
AT = {"date": "2026-09-27", "session": 305, "at_version": "v1.0.14", "at_commit": "d3b809a7"}
D39 = "s305-D39 (Dave, sitting call 39, 2026-09-27 14:29 BST, verbatim \"retire, park, yes\")"
D38 = "s305-D38 (Dave, sitting call 38, 2026-09-27 14:29 BST, verbatim \"yes to all six\") kind 4 — part-enacted, the open half parked with a tripwire"
CLOSE = {
 'P-272-1': f"{D39}: \"yes\" to moving it to enacted — answered by s274-D1..D6 (#274, 2026-09-15; the list/card line is surface alone, list-items the default of record-list), commits 58f56ef5 and 3a752d1f; the uncertain-stamps page: \"List against card: answered by your six rulings of 15 September, now stamped enacted.\" Moved by #305 lane H1.",
 'P-277-4': f"{D39}: \"yes\" to moving it to enacted — answered by s282-D5 (#282, his own export of 18 September), commit eaf12365; the uncertain-stamps page: \"The logo review: answered by your own export of 18 September, now stamped enacted.\" Moved by #305 lane H1.",
}
def item(pid, what, why, owner, trigger):
    return {"id": pid, "parked": AT, "what": what, "why": why, "owner": owner, "status": "parked", "trigger": trigger}
DP = {"kind": "event", "name": "dream-pass"}
NEW = [
 item('P-305-1', "s246-D3 — THE SPANS DIAL: importance-weighted spans as a new bento dial in the rails (a spans chord: 4+2 · 2+4 · 3+3 · 6), the edit pass picking a chord. Ruled 2026-09-05 as a trial (\"lets try (a) new dial, edit-pass picks a chord · and see how it works\"); not built (R2 probe: _bento_edit_rails.json carries 0 'spans').",
      f"{D39}: \"park\". The stamps page: \"the dial when bento edit mode is built, because neither is on the path to v1.0.14 or the catalogue.\"",
      "Dave (whether the trial still stands); the bento edit-mode lane when it is briefed",
      {"kind": "file-changed", "path": "knowledge/_render/_bento_edit_rails.json"}),
 item('P-305-2', "s114-D2 — THE ADOPTION-TIME CITATION GATE (ds-016 remedy (a)): ruled #114 with four binding conditions (advisory with the 7 named rules; a named promotion trigger in code; an honest waiver form; detection and discharge mutation-tested separately). Not built. Also carries W-05 part (2) and W-06 (folded here under s305-D35).",
      f"{D39}: \"park\". The stamps page: \"the gate reopens when the next gate is added\". ⚠ DECLARED: the trigger is a PROXY — a commit touching knowledge/_build_all.py (where gates are wired) — so it can fire on a change that adds no gate; the reader decides.",
      "Dave (promotion stays his, per s114-D2); the next lane that adds a gate",
      {"kind": "file-changed", "path": "knowledge/_build_all.py"}),
 item('P-305-3', "s131-D2 open half — the Dave's-eye half of 'the design KG must be as robust as the Memento graphs': edge migration where prose becomes a reference (s133-D1). The mechanical half is enacted (5b590996: typed edges + parse-gate + index 642->1077).",
      D38 + ".", "Dave (the eye half)", {"kind": "file-changed", "path": "knowledge/gen_kg_edges.py", "event": "kg-edge-gen"}),
 item('P-305-4', "s136-D1 open half — the three-axis model's four enact lanes (slots key rollout, props.binds audit, DTCG re-encode, fork-ban gate), found only PARTLY (A1); the precondition is enacted (8b548b87, 0cff8055).",
      D38 + ".", "the next lane that touches the meta schema", {"kind": "file-changed", "path": "knowledge/components/meta.schema.json"}),
 item('P-305-5', "s143-D1 open half (B) — amount-display.sign stays Treatment A with an a11y colour-value adjustment owed (carried to #144 and not traced since); half (A) is enacted.",
      D38 + ".", "the next lane that touches amount-display", {"kind": "file-changed", "path": "knowledge/components/amount-display.meta.json"}),
 item('P-305-6', "s172-D1 open half — B3: the grades sidecar fork returns to Dave with numbers after one full dream-pass cycle; the project field half is built (gen_dashboard.py:91, e5ab8eed).",
      D38 + ".", "Dave (the fork); the dream-pass seat brings the numbers", DP),
 item('P-305-7', "s174-D1 open half — GATE 5 of the component-scaffold brief: the separate correction lane, never run; gate 2 enacted the same session (the progress bar), gates 3-4 honoured.",
      D38 + ".", "the next component-scaffold lane", DP),
 item('P-305-8', "s177-D1 open half — dream pass 7's P1, DEFERRED pending the four-item liveness check; P2/P3/P4a/P4b enacted (69fba90).",
      D38 + ".", "the dream-pass seat", DP),
 item('P-305-9', "s273-D2 open half — authoring pass two: the DESK gates (when + priority + shape + answers) AUTHORED for the 49 silent providers; 3b9d89be records it partial, not proven complete.",
      D38 + ".", "the next roles/DESK authoring lane", DP),
]
have = {i['id'] for i in data['items']}
assert not have & {n['id'] for n in NEW}, 'ids exist'
new = orig; spans = []
for pid, text in CLOSE.items():
    a = new.index(f'"id": "{pid}"'); b = new.index('"status": "parked"', a)
    assert b < (new.find('"id": "P-', a + 5) if new.find('"id": "P-', a + 5) > 0 else len(new))
    ls = new.rfind('\n', 0, b); ind = new[ls + 1:b]
    rep = '"status": "enacted",\n' + ind + '"closed_by": ' + json.dumps(text, ensure_ascii=False)
    new = new[:b] + rep + new[b + len('"status": "parked"'):]
tail = new.rstrip().rfind(']')
assert new[tail:].strip() == ']\n}'.strip() or new[tail:].replace(' ', '').replace('\n', '') == ']}'
last = new.rfind('}', 0, tail)
block = ''.join(',\n     ' + json.dumps(n, indent=1, ensure_ascii=False).replace('\n', '\n     ') for n in NEW)
new = new[:last + 1] + block + new[last + 1:]
after = json.loads(new)
assert len(after['items']) == len(data['items']) + len(NEW)
for x, y in zip(data['items'], after['items']):
    if x['id'] in CLOSE:
        assert {k: v for k, v in y.items() if k not in ('status', 'closed_by')} == {k: v for k, v in x.items() if k != 'status'} and y['status'] == 'enacted'
    else:
        assert x == y, x['id']
assert after['items'][len(data['items']):] == NEW and after['$comment'] == data['$comment']
recon = new.replace(block, '')
for pid, text in CLOSE.items():
    recon = recon.replace('"status": "enacted",\n' + recon[recon.rfind('\n', 0, recon.index('"closed_by": ' + json.dumps(text, ensure_ascii=False))) + 1:recon.index('"closed_by": ' + json.dumps(text, ensure_ascii=False))] + '"closed_by": ' + json.dumps(text, ensure_ascii=False), '"status": "parked"')
assert recon == orig, 'reconstruction FAILED'
open('/dev/shm/_parked.test.json', 'w', encoding='utf-8').write(new)
assert len(_parked.load('/dev/shm/_parked.test.json')) == len(after['items'])
print('OK: reconstruction proven, parses, _parked.load accepts,', len(data['items']), '->', len(after['items']), 'items; enacted', sorted(CLOSE))
if WRITE:
    open(P, 'w', encoding='utf-8').write(new); print('written')
