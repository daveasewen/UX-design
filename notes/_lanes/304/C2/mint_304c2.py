# #304 C2 commit seat - mint the store rows for the wave-two filed reports (doc-row gate, s218-D7),
# and add the skill path to W-333's links (V2 Run 4a fix 2; the row stays OPEN, owner Dave).
# Modelled on notes/_lanes/304/C1/mint_304.py. ID_RE allows at most two suffix characters, so the
# Run 4 seats take W-304ra / rb / rc / rs (R4a / R4b / R4c / R4s) - "r4a" and "r4b" are illegal,
# the same reason wave one minted R6a/R6b as W-304da/db.
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/'
R3 = S + '2026-09-26-304-R3-ruled-now-built.md'
R4A = S + '2026-09-26-304-R4a-skill-composes.md'
R4B = S + '2026-09-26-304-R4b-geometry-and-size.md'
R4C = S + '2026-09-26-304-R4c-eval-harness.md'
R4S = S + '2026-09-27-304-R4s-cold-run-scores.md'
V2 = S + '2026-09-27-304-V2-verifier-wave-two.md'
C2 = S + '2026-09-27-304-C2-commit-seat-wave-two.md'
SKILL = 'apollo-spider/skills/generate-from-canon/SKILL.md'
REVIEW = 'notes/_REVIEW-304-v1013-vs-candidate-2026-09-27-v1.html'
rows = [
 dict(id='W-304r3', home=R3, owner='claude',
      links=['notes/_lanes/304/R3/RENDER-PAIRS-s245-D10.html', 'notes/_lanes/304/R3/survey/verdicts-before-after.json', 'knowledge/gen_kg_tokens.py'],
      title="#304 Run 3 - ruled, now built: s245-D10 console radii and s277-D12 tokens-in-the-graph enacted; s135-D1 border half, s269-D1 step 5, s269-D6 stopped at their ratification clause",
      body="s218-D7 filed report, Run 3 (#304). Row as the report specifies, minted by the #304 C2 commit seat. OWED, named by the verifier (V2 fix 1): knowledge/gen_kg_tokens.py is UNWIRED - neither --check nor --selftest is in _build_all.STEPS or any workflow; its only consumer is _build_kg_explorer.py reading _token_nodes.json. Same shape as its siblings gen_kg_principles.py and the rule/icon/logo node files (the unwired-validators class, inherited not introduced). The card padding 20 -> 8 is the one derived line s245-D10 does not itself name (s201-D4 / s200-D1 (c) derivation; no gate forces it, nothing reads it) - for Dave's page.",
      closes_when="the wave-two commit carrying Run 3 is pushed with CI read back by name, s245-D10 and s277-D12 are stamped enacted with that sha, Dave has looked at the render pairs (his eye closes the radius row), and gen_kg_tokens.py --check/--selftest is wired into _build_all.STEPS (owed, V2) or Dave has declared it exempt"),
 dict(id='W-304ra', home=R4A, owner='dave',
      links=[SKILL, 'notes/_lanes/304/R4a/build_candidate.sh', 'notes/_lanes/304/R4a/verify-skill-results.json', 'W-333'],
      title="#304 Run 4 seat 4a - the generate skill composes from the graph (65 of 65 hard-rule anchors carried), the drafts are ready, the v1.0.14 candidate rebuilds byte-identical",
      body="s218-D7 filed report, Run 4 seat 4a (#304). Row minted by the #304 C2 commit seat. The skill rewrite ships only at a v1.0.14 cut, which is Dave's word; the frozen v1.0.13 zip is untouched. The skill's new step 1 routes off the reader - that is W-333's question built ahead of his ruling on the routing home (V2 fix 2); W-333 stays open. The candidate zip is kept out of the repo by .gitignore (rebuilt by build_candidate.sh). Known at the cut: the Gumdrop stamp rewrites three historical rulings, knowledge/brain/ is in no ship group, and rule 3a's width ban is broader than any ruling (Claude's widening, for Tuesday's page).",
      closes_when="Dave has answered the report's questions (the zero-invented-markup scoping first) and the skill has shipped in a cut pack or been withdrawn by his word"),
 dict(id='W-304rb', home=R4B, owner='claude',
      links=['knowledge/_validate_geometry.py', 'knowledge/_validate_own_size.py', 'knowledge/_tests/geometry/geometry-planted.html', 'knowledge/_tests/geometry/own-size-planted.html', 'notes/_lanes/304/R4b/baseline/geometry.json', 'notes/_lanes/304/R4b/baseline/own-size.json'],
      title="#304 Run 4b filed report - the geometry and own-size gates: 11 + 3 clauses, every planted defect caught, wired advisory at steps 147-148",
      body="s218-D7 filed report, Run 4 lane 4b (#304). Two advisory render gates for the #288 sloppiness class and Dave's own-size sentence (Thu 24 Sep 15:46); wired as _build_all steps 147-148; lane 4c's harness is the second consumer. Row as the report specifies (its id W-304r4b is illegal under ID_RE, so W-304rb), minted by the #304 C2 commit seat. The pack roster question (58 -> 60 via the _validate_* glob) is Dave's at the v1.0.14 cut.",
      closes_when="a Fable verifier that built neither gate re-runs both --selftest at the seat and files under notes/_subreports/ citing this report by path, and Dave has ruled whether each gate stays advisory or blocks"),
 dict(id='W-304rc', home=R4C, owner='claude',
      links=['notes/_lanes/304/R4c/harness/score.py', 'notes/_lanes/304/R4c/cold/brief-v1013.md', 'notes/_lanes/304/R4c/cold/brief-candidate.md', 'notes/_lanes/304/R4c/STATUS.md'],
      title="#304 Run 4c - the eval harness (score, render, drive, compare) and the v1.0.13 / candidate cold-run briefs",
      body="s218-D7 filed report, Run 4 lane 4c (#304). Row minted by the #304 C2 commit seat (the report's own spec used a doc-304 id and a different shape). The cold runs it asked the conductor to dispatch were run and scored (R4s); the scoring seat names harness defects to fix here.",
      closes_when="the harness defects the R4s scoring report names are fixed in the harness, or carried by Dave's word"),
 dict(id='W-304rs', home=R4S, owner='dave',
      links=[REVIEW, 'notes/_lanes/304/R4s/review-data.json', 'notes/_lanes/304/R4s/build_review.py'],
      title="#304 R4s - the six cold runs scored, v1.0.13 against the v1.0.14 candidate: composing stopped the tracing (trace index 0.379 -> 0.178), quality tied at 10.0 of 12",
      body="s218-D7 filed report, Run 4 scoring seat (#304). Row minted by the #304 C2 commit seat. Recommendation for Dave's decision: do not cut v1.0.14 as the candidate stands; four fixes (Kpi-tile label crop, the Common gutter key, a full-height side-nav shell, one ruled chart receipt address) and one confirming cold run first. The review page rides as a link.",
      closes_when="Dave has ruled the v1.0.14 cut question on the review page"),
 dict(id='W-304v2', home=V2, owner='claude',
      links=[R3, R4A, R4B, R4C],
      title="#304 V2 - verifier, wave two: Run 3 PASS WITH FIXES, Run 4a PASS WITH FIXES, Run 4b PASS, Run 4c PASS (lane-folder only)",
      body="s218-D7 filed report, Fable verifier seat, wave two (#304). Row minted by the #304 C2 commit seat, which applied its fixes: the candidate zip and pre-R4b copy kept out by .gitignore, the gen_kg_tokens.py debt named in W-304r3, the skill path linked on W-333.",
      closes_when="the wave-two commit carries its fixes and CI's gates job reads back with no red outside the named set"),
 dict(id='W-304c2', home=C2, owner='claude', links=['knowledge/_git_commit.sh'],
      title="#304 C2 - the commit seat, wave two: Runs 3, 4a, 4b, 4c and the cold-run scoring in one commit, the two enactment stamps in a second, pushed, CI read back",
      body="s218-D7 filed report, commit seat, wave two (#304). The interim copy rides the wave-two commit; the final copy with the CI read-back rides the next commit.",
      closes_when="the final copy of this report, carrying both shas, the push range and CI verdict by job, is committed"),
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
w = have['W-333']
if SKILL not in w['links']:
    w['links'].append(SKILL)
    w['body'] += (" #304 (V2 fix 2, minted by the C2 commit seat): the pack's generate skill now routes off the knowledge-graph reader "
                  "(its new step 1) pending Dave's ruling on the routing home - built ahead of his word, ships only at a v1.0.14 cut. Row stays OPEN.")
    print('W-333 linked', w['links'])
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '304' in f or '333' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
