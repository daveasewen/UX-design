# #246 — the library dictates: two baselines that came out the same, a page of principles, seven rulings in Dave's words, and a verify that is the next session's job

```
provenance: 246 · 2026-09-05
status: observed
```

*Spine entry: `_LIVE-STATE.md` § `## ⏱ LATEST DELTA — 2026-09-05 … #246`. Ledger: `knowledge/_rulings.json`
§ `s246-D1` … `s246-D7`. Banner: `GOOD-MORNING.md` § ★ LATEST #246. Reports:
`notes/_subreports/2026-09-05-246-B-baseline.md` · `notes/_subreports/2026-09-05-246-O-opus-baseline.md` ·
`notes/_subreports/2026-09-05-246-P-principles.md` (with § P2 and § P3) · `notes/_subreports/2026-09-05-246-wrap.md`.
Briefs: `notes/_briefs/2026-09-05-246-lane-B-baseline-brief.md` · `…-lane-O-opus-baseline-brief.md` ·
`…-lane-P-dashboard-principles-brief.md` · `…-246-delegated-wrap-brief.md`. Review surfaces:
`reviews/BASELINE-246-2026-09-05-v1.html` · `reviews/BASELINE-246-OPUS-2026-09-05-v1.html` ·
`reviews/DASHBOARD-PRINCIPLES-2026-09-05-v1.html`. Both-way: each of those files names this dossier's session.*

*This is the WHY and HOW. The WHAT — figures, paths, scores, receipts — lives in the ⏱ delta, the banner, the
stratum and the three reports, and is not restated here except where the reasoning needs the number.*

## 1. Why the session opened on a stale premise, and why the chain corrects it and not a hand

The chain said "7 ahead, NOT PUSHED". `git rev-parse origin/master` at the opener said `4dc12b6` — Dave had
pushed after #245's wrap, and CI #483 had already run on it (release GREEN 9/9; the gates job red at steps 5
and 6, which is [18], his). The chain was not wrong when it was written; it was wrong by the time it was read,
which is the assertion-propagation class again: a generated record that nothing chases. The correction is
made the only way the record allows — the new banner and delta state the true push state, and `_gen_chain.py`
regenerates `_CHAIN.md` from them. Nobody edits `_CHAIN.md`.

## 2. Why the focus narrowed to one sentence

Dave, at the opener: the Sutherland demo is about two weeks out and *"the focus is getting the dashboards
one-shotable"* from the frozen prompt. Everything else on the queue — the cold test of v1.0.6, [18], the radius
build, the 4px audit — stayed his and stayed carried. The session's shape follows from the sentence: if a
dashboard must come out of one prompt, the first thing to know is what comes out of one prompt today, before
anyone touches the library. That is why the session was read-only against `knowledge/` by design, and why the
first two lanes built dashboards instead of fixing anything.

## 3. Why two baselines, and why one of them was Opus

The consumer of the pack is a Copilot-class model inside VS Code with no vision and no Playwright. Dave
ratified agency-side testing — the pack is tested here, not at Sutherland — and Opus 5 stands in as the GPT
proxy, because a second model family is the nearest thing to a second reader. Lane B (Fable) and lane O (Opus)
ran the same frozen prompt cold, blind then sighted. The point of two arms per lane was to separate what the
pack gives a blind builder from what sight buys it; the point of two lanes was to separate what the model
brings from what the library dictates.

## 4. The finding, and why it is the library's and not the models'

All four dashboards — Fable blind, Fable sighted, Opus blind, Opus sighted — are the template's specimen
arrangement: four KPI tiles at 3·3·3·3 in a 2×2, a permanently open filter toolbar that filters nothing, an
attention rail with no actions, two equal columns beneath. Sight moved defects (a truncated CSS copy, a
serif-tab font dependency, a viewport that did not fill), never richness. The model changed what broke, not
what was composed. The reasons are all in the pack: the template meta says how many groups is Dave's and the
brief skipped six questions; the rules index carries 470 rules and zero about composition; `behaviour` is typed
on 20 of 137 metas and on none of data-grid, filter-toolbar-bar, tabs, segmented or any chart; the template
ships its chart stripped; irregular spans `data-c` 1–6 exist in canon and the dashboard template never uses
them; there is no `<footer>` in the template, so both pages inherited a groundless shell. A builder with
nothing to decide with ships the specimen. That is the sentence the session is named for.

Two contradictions surfaced as facts, not fixes. The receipt gate rewards splicing while the compose gate fails
every spliced page — and, lane O's control run showed, fails the library's own gated template on the same 130
hex colours. And "Net FX exposure" fell and was painted red: the stroke binds to arithmetic direction and no
field says which direction is good. Both are ruling-shaped and carried; neither was patched by a read-only lane.

## 5. Why a principles page, and why it came from Dave's seeds rather than from the literature first

Dave's reaction to the baselines was six paragraphs of taste — dense KPI rows, dismissible filters with a
designer-chosen default, actions on the overview page, irregular bentos for rhythm, preattentive signal and the
dark cockpit, and two tentative thoughts about horizons and proximity that he asked us to validate rather than
enact. Lane P pinned each seed to a baseline defect with a file, a line and a crop, then went to the sources
(Nielsen, Few, SAP, Carbon, Polaris, MOJ, and for P2/P3 Healey & Enns, EEMUA 191, Palmer, Fitts) to find out
whether the literature agreed. It did, nearly verbatim in places — Few's failure 9 is Dave's third seed. The
page therefore reads as principles with a source beside each, in the `_rules-index.json` shape, eighteen from
lane P and eleven more from P2 (signal) and P3 (locality), with the horizon thought HELD at Dave's own request.
The order — his words, then the defect, then the source — is deliberate: a principle that starts from the
literature arrives as someone else's; one that starts from his seed and finds the literature behind it arrives
as his.

## 6. Why seven of sixteen questions were ruled, and why the seventh is a test and not a pick

Sixteen ruling-shaped questions closed the page. Dave answered Q1–Q7 in one message, each in his own words,
and the wrap inscribed them verbatim as `s246-D1`…`D7`. The shape of his answers matters more than the letters:
Q1 everything ADVISORY until a second dashboard exists — a tier deferred, not a tier chosen; Q2 and Q6 defaults
with no grill-me question, on the #241 principle that the question load is what binds; Q3 a new spans dial,
*"lets try … and see how it works"*; Q4 a recipe now and a component only once `s234-D5` settles the behaviour
address; Q5 the KPI row as the default and the 2×2 removed, *"this for now"*. Four of the seven carry his own
revisit clause, and the store records them with it. Q7 he declined to pick — *"Id like to test all three
somehow"* — so `s246-D7` is inscribed as ruled-with-a-test, and designing that three-way test is #247's carry.
A wrap that had read "test all three" as a lean toward (a) would have ruled for him. Q8–Q16 were not answered
and stay his.

His closing line frames the whole batch: *"I like the Eighteen principles, in the rules-index shape, but I'm
wary of possible conflicts and complexity, lets do it and verify the results."* Two things follow. "Lets do it"
is the enact wave — DP-01…18 into canon, all ADVISORY per D1 — and "verify the results" is the frozen prompt
run again, Opus blind and Fable sighted, against the enacted library. That is the next session, whole. And he
said *eighteen*; the page holds twenty-nine. Whether DP-19…29 are inside "lets do it" is ruling-shaped and is
carried as such, not assumed either way.

## 7. What the lanes cost, and what the conductor could not do

Five lanes, seven subs, all Fable but O: B 298,810 · O 347,662 · P 244,924 · P2 196,636 · P3 161,939 —
1,249,971 tokens of quota. The conductor's own window ran to 165,789 at the brief cut, past the 150,929
advisory, which is why the seven inscriptions and the whole ritual were delegated. Three strays are declared
for Dave's side rather than fixed: `knowledge/_screen-gate/dashboard.md`, written by the screen gate during
lane B and un-removable on this mount (left untracked, not committed); `outputs/baseline-246-opus/review-top.png`;
and a `.git/index.lock` from 4 September that `_git_commit.sh` refuses to stage over and this wrap does not
delete. The two baseline output trees (3.1 MB and 6.9 MB) are under `outputs/`, which `.gitignore` covers, so
the evidence lives on disk and in the two review pages, not in git.

## 8. What is resolved, and what is still open

**Resolved.** Seven rulings in the store, 348 → 355, each in Dave's words. Two baselines measured and reviewed.
Twenty-nine principles drafted with sources, in the shape he asked for. The push state corrected in the chain.

**Open, and every one of them is Dave's or #247's.** The enact wave for DP-01…18 and the re-run of the frozen
prompt that verifies it. Whether DP-19…29 are inside "lets do it". The DP-17 three-way test. Q8–Q16. Whether
the template's chart ships whole. Glue versus a registered partial (lane B RSQ 1) and splice versus link across
the two gates (RSQ 2). Whether mono stays the default for the Sutherland demo. Parts-with-addresses for a
sightless consumer, with projection recommended. The cold test of v1.0.6 and the ratify / hold word. [18].
The radius build under `s245-D10`'s Console-only scope. The 4px audit, then ladder D. Each at its own age in
`_CARRIES.md` § residual → #247.
