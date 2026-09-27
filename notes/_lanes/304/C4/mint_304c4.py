# #304 C4 commit seat - mint the store rows for the wave-four filed reports (doc-row gate, s218-D7),
# and close W-304c3 (its final copy rides this commit, as its own row says). Modelled on C3's mint_304c3.py.
# IDs at most two suffix characters (ID_RE).
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/'
W4A = S + '2026-09-27-304-W4a-chart-engine-ink.md'
W4B = S + '2026-09-27-304-W4b-instruments-see-ink.md'
J = S + '2026-09-27-304-J-jev-edge-node-probe.md'
V4 = S + '2026-09-27-304-V4-verifier-wave-four.md'
C4 = S + '2026-09-27-304-C4-commit-seat-wave-four.md'
rows = [
 dict(id='W-304ga', home=W4A, owner='claude',
      links=["knowledge/canon/dv-behaviour.js","knowledge/canon/dv-render.js","knowledge/canon/dv-render-donut.js","knowledge/snippets/Template-dashboard-bento.reference.html","knowledge/canon/canon.css","notes/_lanes/304/W4a/compare.json","notes/_lanes/304/W4a/renders/"],
      title="#304 W4a filed report - chart engine: axis-gutter fit on by default (ds-012b), measured label thinning, ring frame fixed and deterministic (ds-030); dense-series markers STOPPED for Dave",
      body="s218-D7 filed report, wave four seat W4a (#304); row minted by the C4 commit seat from the report's own spec. ds-012(b) gutter fit is the default (opt-out data-pl-fit=none); category labels thinned at fit time from measured widths (8px clearance borrowed from the kit's label offset, declared); the ring keeps its authored frame and is no longer stretched by the bento template's fluid release (ds-030) - 8/8 loads 300x260 where HEAD was bistable. Six cold runs, same 60 views, HEAD engine vs W4a: ink/view 6.62 -> 5.53, G8 148 -> 36 (remainder = held-back Kpi-tile), G7 752 -> 225, G12 14 -> 2, nothing up. 148-step clone survey: no green-to-red. 27 receipts re-driven, measurements byte-identical. Page budget now 34,704/34,816. Markers-on-dense-series and tile hug/fill + ring narrow column are Dave's, rendered. V4 (PASS WITH FIXES, none to code): label thinning - its existence, the 8px clearance, anchoring on the last category - is enacted WITHOUT a ruling and goes to Dave on Tuesday.",
      closes_when="a verifier that built none of it re-runs _drive_chart_engine --check, _validate_behaviour and the W4b views phase on one restaged cold run at the seat, matches its row in compare.json, and files under notes/_subreports/ citing this report; Dave has seen DAVE-markers-* and DAVE-ring-tile-* and said which"),
 dict(id='W-304gb', home=W4B, owner='claude',
      links=["knowledge/_validate_geometry.py","knowledge/_tests/geometry/geometry-planted.html","notes/_lanes/304/R4c/harness/views.py","notes/_lanes/304/R4c/harness/score.py","notes/_lanes/304/W4b/runs/compare-six.html","notes/_lanes/304/W4b/determinism.txt","notes/_lanes/304/W4b/probe_ring_bistable.txt"],
      title="#304 W4b filed report - the instruments see ink: G6 lone-panel, app-shell scroll and own-clip blind spots repaired with levers; G11 marks-on-every-point and G12 chart-lost-in-box added; harness views phase + floor/ink score; six cold runs re-baselined",
      body="s218-D7 filed report, wave four seat W4b (#304); row minted by the C4 commit seat from the report's own spec. Geometry gate: 13 clauses, 4 planted sub-cases, 3 cause levers, W3b's v1013-r2 ring tile as a real-page leg; 0 new-clause findings on 137 snippet references and 138 showroom pages. Harness w4b-2.0: every view, rendered text, theme both ways, floor pass/fail + ink per view. New baseline: all six pass the floor; ink per view v1.0.13 6.2 vs candidate 7.0 (cut ink 0.4 vs 1.9). Engine finding: ring diameter is bistable across loads on v1013-r2/r3 Trade. G11 tolerance 12 and G12 35% are declared, not ruled. The four *.pre-W4b.py.txt rollback copies are left unstaged.",
      closes_when="a verifier that built neither re-runs the geometry --selftest and score.py selftest-views at the seat, re-scores one cold run and matches its ink row, and files under notes/_subreports/ citing this report; Dave has seen the ink row and said whether the G11 threshold (12) stands"),
 dict(id='W-304jv', home=J, owner='dave',
      links=["notes/_lanes/304/J/results.json","knowledge/_jev-receipts.jsonl"],
      title="#304 J - Jev edge + node-title probe: advisory; four edge types usable as a suggester, titles are a mechanical fix",
      body="s218-D7 filed report, wave four seat J (#304); row minted by the C4 commit seat from the report's spec. 70 of 80 calls (50 edges + 20 titles), 0 errors, key never printed; receipts +70/-0. Advisory; governs nothing (s294-D10 holds). V4: PASS, no graph or canon file touched.",
      closes_when="Dave has ruled whether to (a) cut a hand-run advisory sweep over obeys/providesRole/answersIntent/hasDataShape with the two-band rule, (b) cut the mechanical title fix for the 1,135 code-only labels, (c) look at amount-display in roles.json input providers"),
 dict(id='W-304v4', home=V4, owner='claude',
      links=[W4A, W4B, J, "notes/_lanes/304/V4/"],
      title="#304 V4 - verifier, wave four: W4a PASS WITH FIXES (none to code; label thinning unruled, to Dave), W4b PASS, J PASS",
      body="s218-D7 filed report, Fable verifier seat, wave four (#304); row minted by the C4 commit seat. Clone survey with all three overlaid: 148 steps, 9 FAIL as wave three, 0 green-to-red; four plants of its own caught on the new gate and blind on the old; cand-r1 re-scored twice identical. Five canon items Dave has not ruled listed for Tuesday's page.",
      closes_when="the wave-four commit carries W4a, W4b and J whole as the door says (rollback copies out, other-seat paths declared) and CI's gates job reads back with no red outside the named set"),
 dict(id='W-304c4', home=C4, owner='claude', links=['knowledge/_git_commit.sh'],
      title="#304 C4 - the commit seat, wave four: W4a, W4b, J, the V4 report and C3's final copy in one commit, pushed, CI read back, candidate 2 built",
      body="s218-D7 filed report, commit seat, wave four (#304). The interim copy rides the wave-four commit; the final copy with the sha, push range, CI verdict by job and the candidate-2 zip sha256 rides the next commit.",
      closes_when="the final copy of this report, carrying the sha, the push range, CI verdict by job and the candidate-2 zip sha256, is committed"),
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
    st.add(doc, project='apollo', opened=304, state='open', **r)
    print('added', r['id'])
c3 = have['W-304c3']
if c3['state'] != 'done':
    c3['state'] = 'done'
    c3['closed_by'] = ("#304 C4 commit seat: the FINAL copy of notes/_subreports/2026-09-27-304-C3-commit-seat-wave-three.md "
                       "(sha 86249459, push aaf3bb7e..86249459, CI run 36281589292 by job) and its transcripts in "
                       "notes/_lanes/304/C3/ ride the wave-four commit, as the row's close condition says")
    print('closed W-304c3')
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '304' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
