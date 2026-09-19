"""#287 wrap — the store row for LANE X's filed report, written through _state.py's module API.

⚠ A JUDGMENT THIS SEAT MADE AND DECLARES RATHER THAN LEAVING TO BE DISCOVERED — the same one lane C
declared for rows W-287i / W-287w / W-287c. Lane X filed AFTER lane C's commit, so its report had no
row and `_gate_doc_rows.py` refused this wrap's staging, correctly. The `closes_when` is taken from
lane X's OWN filed verdict and nothing is re-worded; the alternative was `DOC_ROW_ACK`, which would
have shipped an invisible document to pass a gate. Named here so the conductor can CORRECT a
close-condition rather than inherit it.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'knowledge'))
import _state

doc = _state.load()
ok, fails, notes = _state.check(doc)
print('PRE  check ok=%s fails=%d items=%d' % (ok, len(fails), len(doc['items'])))
if any(i['id'] == 'W-287x' for i in doc['items']):
    print('W-287x already present — nothing written'); sys.exit(0)
_state.add(doc,
    id='W-287x',
    title='#287 lane X — the GPT-6 Spider v1.0.13 spacing handoff tested claim by claim',
    state='open', owner='dave', opened=287, project='apollo',
    closes_when=("Dave has ruled the two decisions lane X found genuinely open — the bento template's "
                 "status (meta PROPOSED / NOT REGISTERED against showroom/index.json's `beta`) and "
                 "whether a `composes` edge type is added to meta.schema.json — or said the report "
                 "needs nothing further"),
    home='notes/_subreports/2026-09-19-287-X-spider-spacing-handoff-verified.md',
    links=['notes/_lanes/287/GPT-SPIDER-SPACING-HANDOFF-2026-09-18.md',
           'notes/_lanes/287/DAVE-RULINGS-2026-09-19.md',
           'knowledge/components/template-dashboard-bento.meta.json',
           'knowledge/_render/_bento_edit_rails.json',
           '_HANDOFF-138-the-rulings-land-and-the-strand-map-is-ordered.md'],
    body=("Dave brought a GPT-6 handoff from Apollo Spider v1.0.13 on his work machine: \"don't take it "
          "on face value, use your judgment, but what it did worked.\" READ-ONLY lane, no gate and no "
          "generator run. 5 of 6 claims VERIFIED at file:line, 1 PARTLY (the 33 pass / 8 FAIL split is "
          "arithmetically exact against v1.0.13's 41 RUNNABLE gates, but the attribution is roughly 3 "
          "screen-caused, 4 pack-baseline, 1 placement-dependent and the agent ran no --baseline). Its "
          "one real analytical miss is the same miss twice: it read 0 and 40/4 as defects when both are "
          "ruled values. The template pins Mono's 40/4 as literals because the s219-D3 generation arm "
          "was never built and _bento_edit_rails.json is $groundwork_only. Inline-style census: 596 in "
          "knowledge/snippets/, 62 percent defensible, zero inline layout dials repo-wide, and 88 raw "
          "px/rem values with no var() - that 88 is the actionable number. No ruling on inline styles "
          "exists across all 622. Two statuses ship for one template: meta PROPOSED / NOT REGISTERED "
          "against showroom/index.json's beta, which is the surface the skill tells builders to search."))
ok, fails, notes = _state.check(doc)
print('POST check ok=%s fails=%d items=%d' % (ok, len(fails), len(doc['items'])))
for f in fails: print('  FAIL:', f[:200])
assert ok, 'store check FAILED — nothing saved'
_state.save(doc)
print('SAVED W-287x')
