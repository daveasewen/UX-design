# #305 C1 commit seat - mint doc rows for wave one's six reports (A, B1 from its own spec, B2, B4, V1, C1).
# Modelled on notes/_lanes/304/C6/mint_304c6.py.
import sys, os, json
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/2026-09-27-305-'
B1 = S + 'B1-look.md'
def spec(path):
    for line in open(path):
        if line.startswith('{"id"'):
            return json.loads(line)
    raise SystemExit('no spec in ' + path)
KEEP = ('id','home','links','title','body','closes_when','owner','condition')
b1 = {k: v for k, v in spec(B1).items() if k in KEEP}
b1['body'] += (" Follow-up after V1 F1: call 10 scoped to Common through four s158-D1 guards in apollo-legacy.overrides.json; "
               "mono, console and supercharge label inks identical to HEAD (renders/call10-scope-measure.json).")
rows = [
 dict(id='W-305a', home=S + 'A-inscription.md', owner='claude', condition='stated',
      links=['knowledge/_rulings.json', 'notes/_lanes/305/A/CALL-MAP.json', 'notes/_lanes/305/DAVE-RULINGS-2026-09-27-sitting.md'],
      title="#305 A - the inscription seat: Dave's 2026-09-27 sitting inscribed as s305-D1..D56 (+ D57 for call 27), six threads W-305n1..n6 minted, Friday recorded",
      body=("s218-D7 filed report. 638 -> 695 rulings through _inscribe_ruling.py only, each dry-run first; five enacted ratifications "
            "(D4, D7, D14, D43, D56) and D57 (call 27) at 4be130e5; five --amend-evidence lines from V1's findings; W-305n4 closed. "
            "CALL-MAP.json maps every call to its id, status and what is owed."),
      closes_when="the wave carrying the s305 inscriptions and their evidence files is committed and the builds' rulings are stamped enacted by the commit seat"),
 b1,
 dict(id='W-305b2', home=S + 'B2-brain.md', owner='claude', condition='stated',
      links=['knowledge/components/meta.schema.json', 'knowledge/gen_kg_sources.py', 'knowledge/_source_nodes.json', 'notes/_KG-EXPLORER.html'],
      title="#305 B2 the brain - the schema takes a part's states (137/137), the when-rules the chooser reads, step 5 in the graph (116 nodes, 402 edges), the canvas prints the code",
      body=("s218-D7 filed report. _build_integrity PASS 0 errors (was FAIL 13); _validate_roles_resolve PASS (was FAIL 6); chooser 19 of 20 on R5's tests; "
            "gen_kg_sources.py born and wired into _build_all.py by the C1 commit seat; explorer v1.30; 48 of 49 bare labels titled."),
      closes_when="the wave carrying these paths is committed with gen_kg_sources wired, the titles/integrity/explorer regens run, CI read back, and Dave has looked at call 18's four and the R4a wording"),
 dict(id='W-305b4', home=S + 'B4-pages.md', owner='claude', condition='stated',
      links=['notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html', 'notes/_SCAN-305-parked-questions-2026-09-27-v1.html', 'W-305n5'],
      title="#305 B4 two review pages - call 27 in pictures, and the 102 parked questions for Dave's scan",
      body=("s218-D7 filed report. Both pages rendered at 1440 and 390, light and dark, 0 overflow, 0 page errors; the 102 = A2's D2 ids still open; "
            "decision bars driven (reload keeps ticks). Every plain-words question and tripwire wording is this seat's, declared on the page."),
      closes_when="both pages are committed and published to the review artifact, and Dave has scanned the 102"),
 dict(id='W-305v1', home=S + 'V1-verifier-wave-one.md', owner='claude', condition='stated',
      links=['notes/_lanes/305/V1/tools/', 'notes/_lanes/305/V1/renders/'],
      title="#305 V1 verifier, wave one - PASS WITH HOLDS: every built number re-measured the same; two paths held out; F1-F3 for Dave's eye",
      body=("s218-D7 filed report, cold adversarial verifier. Rulings against his words clean (57 CALL-MAP entries, 0 misses); K3 0 non-chart moves on four canon pages x 4 themes x 2 modes "
            "apart from call 26's border; holds: _graph-mark-observations.jsonl and V1's before/after staging."),
      closes_when="the wave is committed without the held paths and F1 (answered by B1's Common scoping), F2 and F3 are put to Dave"),
 dict(id='W-305c1', home=S + 'C1-commit.md', owner='claude', condition='stated',
      links=['notes/_lanes/305/C1/', 'knowledge/_build_all.py'],
      title="#305 C1 commit seat, wave one - regens in order, the wave committed, s305 builds stamped enacted, the push credential moved to a helper (call 30), pushed, CI read back",
      body=("s218-D7 filed report, commit seat (interim-report pattern). The interim copy rides the wave-one commit; the final copy with both shas, "
            "the push range, the credential-helper outcome and the CI verdict by job rides the next commit."),
      closes_when="the final copy of this report, carrying both shas, the push range and the CI verdict by job, is committed"),
]
doc = st.load()
have = {i['id']: i for i in doc['items']}
for r in rows:
    assert os.path.exists(r['home']), r['home']
    for l in r['links']:
        assert l.startswith('W-') or os.path.exists(l), l
    assert st.ID_RE.match(r['id']), r['id']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=305, state='open', **r)
    print('added', r['id'])
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '305' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
