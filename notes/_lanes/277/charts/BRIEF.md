# LANE CO — BRIEF — the three charts: chart-line · chart-pie · chart-bar
#277 · 2026-09-15 · enacting `s276-D5` · written by the conductor · **model: opus** · PROPOSE-ONLY

## The ruling you are enacting — verbatim
`s276-D5` (Dave, 2026-09-15, export 19:08:48.621Z option **a** + "go"):

> THE THREE FLAGGED EXTRAS — chart-line, chart-pie, chart-bar — ARE AUTHORED IN THE NEXT LANE, in the same shape: filename join on the three `data-visualisation-*-charts.md` spec files, one sentence per citation, reviewed by eye. Then STOP and look again. They are the whole of what remains of the filename-join route: of 34 guideline files exactly 7 are named after a component, four claimed by s276-D4 and these three. The next lane must also take one word on whether `chart-donut` shares the pie file the way `icon-button` shares the buttons spec, and on the 19 family-level rules in `data-visualisation.md` that sit above all three. The name-match tier is NOT widened into (D-5 option a, not b or c) — that tier produced 'Avatar' from va25-013, the exact false positive s274-D12 refused.

His ask that produced it: *"yes, and maybe flag any extra you think are applicable"*.

## The job in one line
Mirror lane TO (#276): PROPOSE read-only, dry-run, selftest + mutants, a review page of **≤ 3 decisions**, **NOTHING LANDED**. Dave's export ratifies; a land lane lands.

## Read first, in this order (all read-only)
1. `notes/_lanes/276/tie-off/BRIEF.md` + `REPORT.md` + `VERIFY.md` — the shape of your work, report and page. Copy `_build_page.py` and adapt; do not reinvent it.
2. `notes/_lanes/276/tie-off/proposed-metas/` — the six metas landed by `577c82d`. **`edges.obeys` already exists in `meta.schema.json` (`{ref, $why}`, `$why` REQUIRED).** There is NO schema diff in this lane. If you think you need one, stop and say so in the report instead.
3. `knowledge/components/meta.schema.json` — the `edges.obeys` contract and `$obeys-contract`.
4. `knowledge/components/chart-line.meta.json` · `chart-pie.meta.json` · `chart-bar.meta.json` — the three you author against.
5. `knowledge/guidelines/_rules-index.json` — 470 rules. Measured for you: `data-visualisation-bar-charts.md` **10** · `data-visualisation-line-charts.md` **11** · `data-visualisation-pie-charts.md` **11** · `data-visualisation.md` **19**. Verify these counts yourself and report them; if they differ from this line, YOURS wins and you say so.
6. The four guideline files themselves — you must read the rule prose, not just the index row.

## PART A — the filename join (the mechanical half)
- `data-visualisation-bar-charts.md` → `chart-bar.meta.json` · `-line-` → `chart-line` · `-pie-` → `chart-pie`.
- **Filename join, NEVER a regex over prose.** `P-274-3` records that regex gave false positives; `s274-D12` refused the name-match tier and `s276-D5` refuses it again ("Avatar from va25-013").
- For each rule, one `edges.obeys` entry `{ref: "<rule id>", $why: "<one sentence>"}`. **`$why` is REQUIRED and it is AUTHORED** — you read the rule and the component and say why it binds. Not a restatement of the rule text.
- **Reviewed by eye** is part of the ruling: if a rule in the file does NOT bind the component (a spec file can carry a rule about something else), say so and leave it out, with the reason listed in the report. A dropped rule that is declared is a finding; a silent drop is the `s214-D6` failure.
- Write the three proposed metas to `notes/_lanes/277/charts/proposed-metas/`. **Do NOT touch `knowledge/components/`.**

## PART B — the three open questions (`s276-D5` says the lane "must take one word" on these)
⛔ **You do NOT decide these. You present each with both sides and the measured facts.** A parallel judgement lane (CJ, Fable) is writing a recommendation memo to `notes/_lanes/277/judgement/RECOMMEND.md` in the same wave; the conductor reconciles. Your job is the evidence.

- **Q1 — `chart-donut` and the pie file.** Does `chart-donut` share `data-visualisation-pie-charts.md` the way `icon-button` shares the buttons spec? Measure: does the pie file's prose name the donut? Does `chart-donut.meta.json` describe itself as a pie variant? Is there a `family` edge between them in the graph? Report the facts; do not rule.
- **Q2 — the 19 family rules in `data-visualisation.md`.** They sit ABOVE all three. Options to lay out, with the count each implies: (a) attach all 19 to each of the three (57 edges); (b) attach only those that bind, per component, authored (report the measured subset per component); (c) attach them to a family node / a `chart` parent instead, with what would have to exist for that to work. Say what the corpus does today for comparable above-the-component rules.
- **Q3 — the other 11 chart components.** `knowledge/components/` holds 14 chart metas (`Chart-boxplot`, `Chart-bullet`, `Chart-butterfly-h/-v`, `Chart-candlestick`, `Chart-histogram`, `Chart-scatter`, `chart-combo`, `chart-donut`, `chart-sparkline`, `chart-stacked-area` + the three). ⚠ Note the **capitalisation split** — report it, it may be a defect. None have a spec file of their own, so the filename-join route does NOT reach them. Flag only: which would the family rules obviously bind, and why. **Do not author them.**

## Review page — `notes/_lanes/277/charts/REVIEW-charts-2026-09-15-v1.html`
- **≤ 3 decisions**, recommendation first, (a)/(b) options, export button writing the same JSON shape lane TO's page did.
- Bake `type.css` into the srcdoc (label crop pattern, #261). Screenshot with chromium: `source knowledge/_render/seat_env.sh`.
- Leave the recommendation text for each decision as a clearly-marked placeholder `{{RECOMMENDATION}}` IF lane CJ's memo is not on disk when you build the page; the conductor fills it. Everything else — the evidence, the counts, the option text — is yours.

## Gates before you report
`python3 knowledge/_validate_kg.py` (must stay OK — you landed nothing) · schema-validate all three proposed metas against `meta.schema.json` including the `edges.obeys` `$why` requirement · your own `--selftest` on the builder + `_mutate.py`-style mutants (**≥ 10**, and a mutant that survives is a finding, not a pass) · a dry-run count: with the three metas present, how many new `obeys` edges enter the graph, and does `_validate_kg.py` still pass against the simulated tree · `git status` shows changes ONLY under `notes/_lanes/277/charts/`.

## Report — `notes/_lanes/277/charts/REPORT.md`
Measured, not narrated: every count with the command that produced it, the per-rule bind/no-bind table, the three questions' evidence, every gate's output line, FILL at close. Commit ONCE at the end: `#277 2026-09-15 — lane CO: …` and paste `git show --numstat` into the report — **`--numstat` is the receipt, never the commit message**.

## Cautions (each one is a scar)
- Never `git stash`. Never run `gen_kg_edges.py`. Never run `_build_all.py`.
- **Textual span only** if you must edit an existing JSON — a re-dump is the #179 defect and a green gate will not catch it.
- Stale `.git/index.lock` → `mv` it to `.git/_orphan-locks/`, never delete.
- `pip install tiktoken --break-system-packages` before `_checkin.py`.
- Commit serially — another lane is running in this wave under `notes/_lanes/277/icons/` and `notes/_lanes/277/judgement/`. Stay inside your own directory.
