# #304 C1 commit seat - mint the store rows for the thirteen #304 filed reports (doc-row gate, s218-D7).
# Modelled on notes/_lanes/303/W/_work/mint_303.py. Rows for reports only; pages ride as links.
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/2026-09-26-304-'
P_V1 = 'notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html'
P_V2 = 'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'
PLAN = 'notes/_PLAN-304-roadmap-and-weekend-runs-2026-09-26-v1.html'
D = 'notes/_DECIDE-304-%s-2026-09-26-v1.html'
REP = {k: S + v for k, v in dict(
    M='M-apollo-mcp-proposal.md', A1='A1-proposals-inventory.md', A2='A2-open-work-analysis.md',
    A3='A3-future-state.md', A4='A4-health-and-dependencies.md', F='F-roadmap-plan.md',
    R1='R1-ci-sees-to-146.md', R2='R2-store-tells-the-truth.md', R5='R5-mcp-probe.md',
    R6a='R6a-decision-pages.md', R6b='R6b-decision-pages.md', V1='V1-verifier-wave-one.md',
    C1='C1-commit-seat-wave-one.md').items()}
ANALYSIS_CLOSE = "the #304 roadmap plan page cites it by path and the #304 wrap carries or strikes every open item it names"
rows = [
 dict(id='W-304m', home=REP['M'], links=[P_V1, P_V2, 'notes/_lanes/304/M/page.src.html'], owner='dave',
      title="#304 M filed report - the Apollo-MCP proposal page (v1, then v2): three routes, the recommended A2UI catalogue over MCP, a six-phase build path, seven decisions",
      body="s218-D7 filed report, lane M (#304). Row minted by the #304 C1 commit seat.",
      closes_when="Dave has answered or carried the seven decisions on the Apollo-MCP proposal page (v2)"),
 dict(id='W-304a1', home=REP['A1'], links=[PLAN], owner='claude',
      title="#304 A1 filed report - every proposed development of Apollo on record and its true status; eleven rulings probed ruled-not-enacted; the delivery-shape duplicate cluster",
      body="s218-D7 filed report, analysis lane A1 (#304), read-only. Row minted by the #304 C1 commit seat.", closes_when=ANALYSIS_CLOSE),
 dict(id='W-304a2', home=REP['A2'], links=[PLAN], owner='claude',
      title="#304 A2 filed report - the open-work backlog analysed: 746 live rows, 632 of them document rows, 482 closing on Dave's word; eight blanket decisions proposed",
      body="s218-D7 filed report, analysis lane A2 (#304), read-only. Row minted by the #304 C1 commit seat.", closes_when=ANALYSIS_CLOSE),
 dict(id='W-304a3', home=REP['A3'], links=[PLAN], owner='claude',
      title="#304 A3 filed report - the future state: what Apollo is meant to become, what Friday promised, the distance; Spider v1.0.14 as the pack the deck describes",
      body="s218-D7 filed report, analysis lane A3 (#304), read-only. Row minted by the #304 C1 commit seat.", closes_when=ANALYSIS_CLOSE),
 dict(id='W-304a4', home=REP['A4'], links=[PLAN], owner='claude',
      title="#304 A4 filed report - health, externalities and dependencies: CI never past step 8 since 09-09, the single-writer commit path, the ephemeral seat",
      body="s218-D7 filed report, analysis lane A4 (#304), read-only. Row minted by the #304 C1 commit seat.", closes_when=ANALYSIS_CLOSE),
 dict(id='W-304f', home=REP['F'], links=[PLAN, 'notes/_lanes/304/F/page.src.html'], owner='dave',
      title="#304 F filed report - the roadmap and the weekend runs: milestone Spider v1.0.14 as a candidate, six runs, the decisions for Dave",
      body="s218-D7 filed report, judgment seat F (#304). Row minted by the #304 C1 commit seat.",
      closes_when="Dave has ruled or carried the plan page's milestone and its decisions"),
 dict(id='W-304r1', home=REP['R1'], links=['notes/_lanes/304/R1/verdicts-before-after.json', 'knowledge/_git_commit.sh'], owner='claude',
      title="#304 Run 1 - CI sees to step 146: abort chain cleared, six mechanical reds fixed, his-word reds named",
      body="s218-D7 filed report, Run 1 (#304). Row as the report specifies, minted by the #304 C1 commit seat.",
      closes_when="the wave-1 commit carrying Run 1 is pushed, CI's gates job log shows _build_all asking step 146 with its failure set read back by name, and the Fable verifier (1v) has filed its report on the schematic door gate"),
 dict(id='W-304r2', home=REP['R2'], links=['notes/_lanes/304/R2/decisions.json', 'notes/_lanes/304/R2/close_plan.json', 'notes/_lanes/304/R2/for_tuesday_uncertain.json', 'knowledge/_state.py'], owner='claude',
      title="#304 Run 2 FILED - the store tells the truth: 184 rulings stamped enacted, 53 rows closed with receipts, the regrowth arm",
      body="s218-D7 filed report, Run 2 (#304). Row as the report specifies, minted by the #304 C1 commit seat. The verifier (V1) restored the twelve RATIFY_IDS rulings to ruled before commit.",
      closes_when="the Fable verifier's Run 2 sample (30 stamps + 30 closes) is filed under notes/_subreports/ citing this report by path, and Run 6's page 6 carries the UNCERTAIN list from notes/_lanes/304/R2/for_tuesday_uncertain.json"),
 dict(id='W-304r5', home=REP['R5'], links=['notes/_lanes/304/R5/run_all.sh', P_V2], owner='claude',
      title="#304 Run 5 filed report - the Apollo-MCP probe: 137 of 137 metas yield an A2UI entry, 132 pass the drift refusal, 17 ready for run time",
      body="s218-D7 filed report, Run 5 (#304). Row as the verifier (V1) specifies, minted by the #304 C1 commit seat.",
      closes_when="Dave has answered its seven decisions, or the PoC catalogue step is built citing this report by path"),
 dict(id='W-304da', home=REP['R6a'], links=[D % 'schema', D % 'delivery-shape', D % 'when-rules'], owner='dave',
      title="#304 Run 6 seat R6a - three decision pages for Tuesday: the schema, the delivery shape, the when-rules",
      body="s218-D7 filed report, Run 6 seat R6a (#304). Row minted by the #304 C1 commit seat.",
      closes_when="Dave has answered or carried every question on the three pages"),
 dict(id='W-304db', home=REP['R6b'], links=[D % 'ci-calls', D % 'uncertain-stamps', D % 'housekeeping-and-lines'], owner='dave',
      title="#304 Run 6 seat R6b - three decision pages for Tuesday: the CI calls, the uncertain stamps, housekeeping and lines",
      body="s218-D7 filed report, Run 6 seat R6b (#304). Row minted by the #304 C1 commit seat.",
      closes_when="Dave has answered or carried every question on the three pages"),
 dict(id='W-304v1', home=REP['V1'], links=[REP['R1'], REP['R2'], REP['R5']], owner='claude',
      title="#304 V1 - verifier, wave one: Run 1 PASS, Run 2 PASS WITH FIXES (twelve ratification words un-stamped), Run 5 PASS",
      body="s218-D7 filed report, Fable verifier seat (#304). Row minted by the #304 C1 commit seat, which applied its fixes.",
      closes_when="the wave-one commit carries the twelve RATIFY_IDS rulings as ruled and CI's gates job reads back with [139] and [140] not red"),
 dict(id='W-304c1', home=REP['C1'], links=['knowledge/_git_commit.sh'], owner='claude',
      title="#304 C1 - the commit seat, wave one: Runs 1, 2 and 5 and the day's pages in one commit, pushed, CI read back",
      body="s218-D7 filed report, commit seat (#304). The interim copy rides the wave-one commit; the final copy with the CI read-back rides the next commit.",
      closes_when="the final copy of this report, carrying the commit sha, push range and CI verdict by job, is committed"),
]
doc = st.load()
have = {i['id'] for i in doc['items']}
for r in rows:
    assert os.path.exists(r['home']), r['home']
    for l in r['links']: assert os.path.exists(l), l
    assert st.ID_RE.match(r['id']), r['id']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=304, state='open', **r)
    print('added', r['id'])
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '304' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
