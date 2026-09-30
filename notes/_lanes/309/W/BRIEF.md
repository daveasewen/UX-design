# #309 W — delegated wrap brief (conductor Opus 5.5, cloud, linked to Dave's seat)

cut: Wed 2026-09-30 ~13:15 BST · Dave, 13:08 BST, verbatim: "i think we need to wrap" (just after "how hot are you")
provenance: 309 · 2026-09-30 · status: observed

## The session in one line
DATE SPLIT (s294-D11 shape): opened Tue 2026-09-29 20:47 BST ("Good Morning!"), lanes B and C that night, resumed
Wed 2026-09-30 07:07 BST, ritual 2026-09-30. Rulings 834 → 841 (s309-D1..D7). Commits `3457115c..fc203264`, all pushed.

## Fill (hand sum — YOU compute it; never trust a typed figure)
Conductor transcript (cloud, this container): `/root/.claude/projects/-home-claude/c90b4000-f5d3-5ec7-b472-e34bacefa744.jsonl`
Sub transcripts: `/root/.claude/projects/-home-claude/c90b4000-f5d3-5ec7-b472-e34bacefa744/subagents/agent-*.jsonl`
(6 lanes: B a6fdde73a92468c71, C a4d60ba2c9971a8f1, E a039b3aeb0b41dbf7, D ab8a026ccb7550513, F a4a3a0449b7b896e9, G a68df49b6010ba72c).
Copy them to the gitignored `knowledge/_tmp/wrap309/` (stage via /mnt/user-data/outputs + device_commit_files, the #307/#308 W route)
and run `_wrap_facts.py` with `--until` = Dave's "i think we need to wrap" (13:08 BST = 12:08Z). The conductor's own quick
read: boot 133,692; 326,997 at 12:08Z — past stop 300,000 and limit 320,000, under hard 350,000 (s305-D62). Verify and report crossings.

## His words (quote, never paraphrase) — all in `notes/_lanes/309/`
- `DAVE-WORDS-2026-09-29-2137.md` — "1. good" / "2. go" (tabs/accordion/popover are blocks; Metric rebuilt properly)
- `DAVE-WORDS-2026-09-30-0707.md` — four items (move to Metric with the right RAG ink; re-cut end of week; "I'm worried that the checks weren't made…"; "Please delete")
- `DAVE-RULINGS-2026-09-30-1104-metric-and-the-arrow.md` — his review-page export
Chat-only lines: Tue 20:50 "go" (build the cards and tiles) · Wed 10:24 "Can I have a review doc rather than pngs. there are a few comments I want to make" · 13:08 "how hot are you" · 13:08 "i think we need to wrap".

## What happened (the arc, for banner/delta/dossier)
1. Opener: #308's addendum CI green on 3457115c. Lane B built the cards-and-tiles model: five kinds (layout, housing, record, block, part), the advisory "accepts" check in `_validate_edges.py --check`, container/surface/panel, chart-panel → chart, the four nesting limits; the carousel ruling now derived. Metric stopped on scale (canon.css 193 mentions, 27 chart receipts). W-308ir/is/it/iv closed.
2. His 21:37 answers → s309-D1 (tabs, accordion, popover are blocks — accepts check 110/110, 0 refusals) and s309-D2 (Metric rebuilt properly). Lane C built Metric (one block, trend optional slot, stat-card and kpi-tile aliases), 27 chart receipts re-driven, explorer rebuilt v1.35. W-308iu closed.
3. CI RED on 528e8318: ASSERT-009 (component meta count 138 → 139, metric.meta.json) — lane C skipped the re-base step. Conductor re-based (054aee4b), green.
4. His 07:07 worry about the checks → lane E: state-contrast runs sliced at the seat (8 slices, ~4.3 min, byte-matches CI); hit-area finds $RENDER_SHELL at the seat (it has NEVER run in CI — no browser there); a /tmp-clone chunked survey gives CI's whole blocking verdict before a push (~7 min, 12 with the sweep). Leftovers outputs/309/{B,C} (141 MB) deleted on his "Please delete" (delete permission granted at the prompt).
5. Lane D: s309-D3 (stat card pages move to Metric, arrow in RAG ink — rise #137F3C/#66CC8D, fall #DA1A00/#F6604C, all themes) and s309-D4 (re-cut end of the week) inscribed; banking demo, progress dashboard, receipt test, FAB overlay moved; the full state-contrast audit regenerated (it covered only 3 snippets since lane C).
6. His 10:24 ask → lane F built `notes/_REVIEW-309-metric-and-the-arrow-2026-09-30-v1.html`. ⚠ Publishing it into the artifact "Apollo 304 review" was REFUSED by a permission check (rebuilding the artifact's index from a read of it); the page lives in the repo only and he opened it from Finder.
7. His 11:04 export → lane G: s309-D5 (a metric may say "up is bad", NOT the recommendation), s309-D6 (no-change mark full ink), s309-D7 (every lane runs the pre-push check — now Worker checklist step 5). Metric `upIsBad` option (on no live page). Receipt sparkline stretched to 1360 px — caused by the move — fixed (e649da06). Three looks pre-date the move: filters stack (old `.ftb-row` markup, W-309g3), receipt chart script not loaded + CSS drops a rule after each splice (W-309g4), one-tile stat group vs the ≥2 rule (W-309g4). Dark ground/tile colour → W-309g2 (his).
8. CI RED on 99ba4a6e: [131] schematic stale — lane G's regen left `knowledge/_graph-mark-observations.jsonl` uncommitted. Conductor committed it (fc203264). CI on fc203264 OWED — read it back first.

## Commits
Write `notes/_lanes/309/W/COMMITS.txt` from `git log --reverse 3457115c..HEAD`. Lane reports:
`notes/_subreports/2026-09-29-309-{B,C}-*.md`, `notes/_subreports/2026-09-30-309-{D,E,F,G}-*.md`.

## OWED TO #310, IN ORDER — each as the question it is
1. Dave's: the arrow — keep Metric's thin line arrow, or bring the filled triangle back, in the RAG ink? (unanswered on the review page; the thin arrow stands meanwhile)
2. Dave's: which live metrics are "up is bad"? (the option exists, s309-D5; no page uses it)
3. Dave's: dark-mode ground and tile colour (W-309g2) — his words: "the background should be the darkest grey and the tiles black. Anyway this is something we need to decide separatly."
4. Mine, small: banking demo filters onto one row (`.ftb-row` → `.ftb-primary`, W-309g3). Receipt page: load the chart script, fix the CSS splice drop; one-tile stat group is his call (W-309g4).
5. The designer pack re-cut towards the end of the week (s309-D4).
6. Dave's: container types (W-308iw). Then `_HANDOFF-159` OWED 3–6 still standing (edge register items 5–9, W-308ie; the bento-matrix selftest's two reds; picture-page rows; older carries).
7. The review surface: the #309 page is not in the artifact — how should review pages reach him now the publish step is refused?
8. Findings not acted on: hit-area has never run in CI; `_HIT-AREA-ADVISORY.md` dates from 2026-08-19; the stat card's own drawing still exists (showroom, gallery, frozen #227 pair).

## THINGS A COLD SEAT SHOULD KNOW (learned this session)
- ⛔ Pre-push routine is now the Worker checklist step 5 (s309-D7): /tmp clone, chunked survey 1:12, 13:55, 56:140, 141:167 with --include-mutating, test_gates, _validate_evidence, sliced state-contrast when snippets/canon change.
- ⛔ Adding or removing a component meta ⇒ re-base ASSERT-009 in the same change (`notes/_lanes/309/cond/assert009_rebase.py`).
- ⛔ A regen that appends to `knowledge/_graph-mark-observations.jsonl` must commit it WITH the schematic, or CI's [131] reads stale (red twice now: #308 lane I's rule, #309 99ba4a6e).
- ⛔ device_bash defaults to a 120 s timeout: pass timeout_ms (≤180000) for a commit, or it is killed before it lands.
- ⚠ The commit gate refuses a report with no store row (lane F passed on DOC_ROW_ACK; W-309f1 added after).
- ⚠ The artifact publish of the review index was refused by a permission check this session.

## Rules for the wrap seat
- The capture ritual: `knowledge/_RUNBOOK-capture-ritual.md` (PHASE 1 block, its additions, "★ THE ORDER AFTER THE COMMIT"). `_wrap_regen.py --run --session 309` runs the titles as step 0.
- `--fill-token` replaces the token, not the line — keep the 5b text SHORT.
- NEVER `git status`. After every gate run: `python3 knowledge/_wrap_commit.py unlock --tag 309-W`. Keep a `--wrap` commit under ~30 paths; pass timeout_ms 178000 on commit calls.
- Push: plain `git push origin master` (fast-forward first; `git ls-remote` = HEAD), then `_ci_readback.py` and put the verdict in the 5b addendum. A red goes FIRST in the handoff.
- ⛔ Project memory: NOT written by the wrap seat. Write the payload and `notes/_lanes/309/WRAP-MEMORY-HOOK.md`; the conductor places the note after Dave says he is done.
- The summary for Dave: SHORT BULLETED, under Decisions / Outputs / Problems (s305-D63), in `notes/_lanes/309/W/SUMMARY.md`.
- Suggested next title (reconcile with `_gen_titles.py`; declare any difference): `Apollo - #310: the arrow, the dark ground and the loose ends`.
