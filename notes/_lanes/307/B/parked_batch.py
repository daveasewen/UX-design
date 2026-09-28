#!/usr/bin/env python3
"""#307 lane B — three parks with a tripwire appended to knowledge/_parked.json TEXTUALLY, modelled on #305 H1's
parked_batch.py (the register is hand-authored and does not round-trip through json.dump; no writer tool exists —
`_parked.py` reads it and never writes). PROVEN: removing the inserted span gives back the original bytes; the result
parses, `_parked.load()` accepts it, and every existing item is equal.   python3 parked_batch.py [--write]"""
import json, sys
sys.path.insert(0, 'knowledge'); import _parked
WRITE = '--write' in sys.argv
P = 'knowledge/_parked.json'
orig = open(P, encoding='utf-8').read(); data = json.loads(orig)
AT = {"date": "2026-09-28", "session": 307, "at_version": "v1.0.14", "at_commit": sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else None}
assert AT['at_commit'], 'pass the HEAD short sha first'
EXP = 'notes/_lanes/307/DAVE-RULINGS-2026-09-28-reopened-78.md'
def why(rid, hhmm, label):
    return f"{rid} (Dave, by click on the #307 sitting page at {hhmm} BST 2026-09-28, export 21:18 BST {EXP}), verbatim: '{label}' — the recommendation."
NEW = [
 {"id": "P-307-1", "parked": AT,
  "what": "W-99zm — the bento EDIT-PASS RAILS manifest's two open questions: does s219-D1(2)'s 'every role' reach dials a role has no surface for, and is s217-D5's never-tight absence on the dashboard main dial retired. They only matter once the bento editor exists.",
  "why": why('s307-D77', '21:17', 'Park it until the bento editor is built') + " ⚠ DECLARED: the trigger is a PROXY (P-305-1's): a commit to the rails manifest, which a regen can touch without any editor being built; the reader decides.",
  "owner": "Dave (the two questions); the bento edit-mode lane when it is briefed",
  "status": "parked", "trigger": {"kind": "file-changed", "path": "knowledge/_render/_bento_edit_rails.json"}},
 {"id": "P-307-2", "parked": AT,
  "what": "W-99zn — the #219 lane-A edit-pass option grammar report's seven ruling-shaped questions (notes/_subreports/2026-08-25-219-enactA-rails.md), to be settled by use once the bento editor is built.",
  "why": why('s307-D78', '21:18', 'Park it until the bento editor is built') + " ⚠ DECLARED: the trigger is a PROXY (P-305-1's): a commit to the rails manifest, which a regen can touch without any editor being built; the reader decides.",
  "owner": "Dave (the seven questions); the bento edit-mode lane when it is briefed",
  "status": "parked", "trigger": {"kind": "file-changed", "path": "knowledge/_render/_bento_edit_rails.json"}},
 {"id": "P-307-3", "parked": AT,
  "what": "W-51's three promotion candidates (P-2 the duplicate-id / unresolved-IDREF scan, P-4 the premise-vs-store scan, P-5 the stale-figure grep; notes/_briefs/2026-08-19-207-addendum-206-report-critique.md §1), each with one live catch at #206 plus mined history. Under s307-D21 only live catches count toward s204-D1's twice-caught bar, so each waits for a second LIVE catch.",
  "why": why('s307-D21', '20:59', 'No, only live catches count; park the three until they catch something live') + " ⚠ DECLARED: the trigger is a PROXY: a commit to the candidature record knowledge/_DS-IMPROVEMENTS.md, where a new catch would be logged; it can fire on an unrelated edit, and a live catch that is not logged there will not fire it.",
  "owner": "Dave (promotion stays his); the seat that records a live catch",
  "status": "parked", "trigger": {"kind": "file-changed", "path": "knowledge/_DS-IMPROVEMENTS.md"}},
]
have = {i['id'] for i in data['items']}
assert not have & {n['id'] for n in NEW}, 'ids exist'
tail = orig.rstrip().rfind(']')
last = orig.rfind('}', 0, tail)
block = ''.join(',\n     ' + json.dumps(n, indent=1, ensure_ascii=False).replace('\n', '\n     ') for n in NEW)
new = orig[:last + 1] + block + orig[last + 1:]
after = json.loads(new)
assert len(after['items']) == len(data['items']) + len(NEW)
assert after['items'][:len(data['items'])] == data['items'] and after['items'][len(data['items']):] == NEW and after['$comment'] == data['$comment']
assert new.replace(block, '', 1) == orig, 'reconstruction FAILED'
open('notes/_lanes/307/B/_parked.test.json', 'w', encoding='utf-8').write(new)
assert len(_parked.load('notes/_lanes/307/B/_parked.test.json')) == len(after['items'])
print('OK: reconstruction proven, parses, _parked.load accepts,', len(data['items']), '->', len(after['items']), 'items')
if WRITE:
    open(P, 'w', encoding='utf-8').write(new); print('written')
