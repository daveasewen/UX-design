# LANE CJ — BRIEF — the judgement call on the three chart questions
#277 · 2026-09-15 · `s276-D5`'s "must take one word on" · written by the conductor · **model: fable** · READ-ONLY, JUDGEMENT

## Why a separate lane
`s276-D5` ends *"Then STOP and look again."* Lane CO is doing the mechanical half — the filename join and the authored `$why` sentences. You are doing the half that is judgement, and you are doing it **independently**, without reading CO's conclusions, so the recommendation is not just CO agreeing with itself. Dave's instruction for this wave: *"use a lot of fable judgement."*

⛔ **Read-only. Nothing lands. No review page.** One file: `notes/_lanes/277/judgement/RECOMMEND.md`.

## Read first
1. `knowledge/guidelines/data-visualisation.md` (19 rules) · `-bar-charts.md` (10) · `-line-charts.md` (11) · `-pie-charts.md` (11) — **the prose, not just the index rows.**
2. `knowledge/components/chart-*.meta.json` and `Chart-*.meta.json` — all 14.
3. `knowledge/components/meta.schema.json` — the `edges.obeys` contract (`{ref, $why}`, `$why` REQUIRED) as landed by `577c82d`.
4. `s274-D12` · `s276-D4` · `s276-D5` in `knowledge/_rulings.json` — the refused name-match tier is the boundary of what you may recommend.
5. `notes/_lanes/276/tie-off/REPORT.md` — how the six metas were authored, for the house style of a `$why` sentence.

## The three questions — recommend ONE option each, with the argument for the other side stated fairly
**Q1 — does `chart-donut` share the pie spec** the way `icon-button` shares the buttons spec? The precedent is `s276-D4`'s treatment of `icon-button`/`split-button`. Test it: does the pie file's prose govern the donut, or merely resemble it? A donut is a pie with a hole — but the pie rules that matter are about *encoding* (two-datum legality, slice count, label placement). Say which of the 11 pie rules would bind a donut unchanged, which would not, and whether that is enough to call it shared. ⚠ A wrong yes here manufactures 11 false edges with authored-looking `$why` sentences on them, which is worse than 0 edges.

**Q2 — where do the 19 family rules in `data-visualisation.md` attach?** Options: (a) all 19 onto each of the three (57 edges, cheap, and possibly 57 half-true claims); (b) per-component authored subset (fewer, defensible, more work, and a rule that binds nothing is then visible); (c) a family/parent node the three inherit from (structurally right, but nothing like it exists in the graph — say exactly what would have to be built and whether `s269-D1`'s remaining steps already imply it). Recommend one. ★ The test is not tidiness: it is whether a designer reading the graph gets a TRUE answer to "what governs this chart?"

**Q3 — the other 11 chart components.** No spec file of their own, so the filename route does not reach them. Is the honest answer "they wait for step 5 / the family node", or is there a defensible route today? ⚠ Also: `Chart-boxplot`/`Chart-bullet`/`Chart-butterfly-*`/`Chart-candlestick`/`Chart-histogram`/`Chart-scatter` are **capitalised** while `chart-bar`/`chart-line`/`chart-pie`/`chart-combo`/`chart-donut`/`chart-sparkline`/`chart-stacked-area` are not. Judge whether that split is meaningful (two provenances?) or a defect, and say which — with evidence from the files, not a guess.

## RECOMMEND.md shape
For each question: **RECOMMENDATION in one line** → the evidence → the strongest case against → what would have to be true for the other option to win → the cost in edges/nodes. Then a closing section: **"what I would refuse"** — anything in this space that looks attractive and is actually the `s274-D12` false-positive shape.

Write for Dave's page: each recommendation must survive being pasted into a decision card as the "(a)" text. One sentence, no hedging.

## Cautions
Do not write outside `notes/_lanes/277/judgement/`. Do not read `notes/_lanes/277/charts/REPORT.md` or its proposed metas — independence is the point. Never `git stash`. One commit at the end: `#277 2026-09-15 — lane CJ: …` with `--numstat` in the file.
