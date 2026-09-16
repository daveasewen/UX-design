# A2F — FIX REPORT — the KG audit page, v2 on A2V's verdict, with the thin slice
#277 · 2026-09-16 · lane A2F (Fable) · applies `../kg-audit-verify/VERIFY.md` (A2V, `3a37bcd`: PRESENT WITH THESE 5 FIXES) to A2's page (`e958e6d`) · adds the section Dave asked for after the audit shipped · **corrections BY ADDITION**: v1 (`REVIEW-kg-audit-2026-09-16-v1.html`, `_build_page.py`, `_drive_page.py`, `kg-audit-decisions-2026-09-16-v1.json`), `A2-AUDIT.md`, `A3-AUGMENT.md`, `A3-shortlist.json` and A2V's folder are untouched · nothing under `knowledge/` written · no generator run, `_build_kg_explorer.main()` never called, no `git stash`

Dave's words (`DAVE-RULINGS-2026-09-16.md`, verbatim): *"also lets consider how this effects our thin slice technique for design knowledge retrieval at build time."*

## What shipped (all under `notes/_lanes/277/kg-audit/`)
| file | what |
|---|---|
| `REVIEW-kg-audit-2026-09-16-v2.html` | the page — six decisions, D-1 rewritten, D-3 now carries the thin slice, Part A added |
| `kg-audit-decisions-2026-09-16-v2.json` | the builder input (storage key `apollo-277-kg-audit-v2`; export filename `…-v2-export.json`, so it can never be copied over the input) |
| `_build_page_v2.py` | reads A1/A2-measure.json + A2V's `verify-figures.json` + `slice-measure-v2.json`; asserts seven figures; 124 measured figures on the page, none typed |
| `_measure_slice_v2.py` → `slice-measure-v2.json` | the thin slice measured: step-1 reads, three `build_slice()` runs, A3's table corrected, the 14 `obeys→ux` edges, the group census |
| `_drive_page_v2.py` | v1's 21 checks + 7 new (F, G, H, I, J) = 28, DRIVE PASS both themes at 1280 and 390 |
| `a2f-light-1280.png` · `a2f-dark-1280.png` · `a2f-390-light.png` · `a2f-390-dark.png` · `a2f-decisions-light.png` · `a2f-decisions-dark.png` | screenshots, from a fresh never-driven context |

---

## The five fixes — before / after

### Fix 1 — D-3 / G2: 730K → about 415K tokens (1.6 MB) — RED F21
- **Before (v1):** D-3 lede "read the metas — 137 files, about 730K tokens"; Part D G2 "the agent reads ~730K tokens of metas". Source: `_compose_slice.py`'s stale docstring line 13, typed into `A2-measure.json` as `metas_tokens_docstring: "730"`.
- **After (v2):** D-3 lede "the library is 138 files, **about 415K tokens (1.6 MB)**"; G2 "~415K"; hero stat "415K → 19K". Read from `slice-measure-v2.json → today.metas_all` = 414,755 tokens / 1,606,913 bytes (tiktoken cl100k, re-measured this session; matches A2V's 414,755 and A3's table). The builder asserts `metas_tokens_k == 415`.
- The D-3 argument is unchanged: 415K does not fit beside a design task either.

### Fix 2 — D-1's ruling citations — RED (judgement)
- **Before (v1) D-1(a):** "Supersedes the 'behind its own chip' clauses of **s274-D11** and s275-D6 by name; is the named lane s275-D4 deferred to." D-1(c): "Loses what s274-D11 and s275-D6 wanted visible." Part B: "s274-D11 and s275-D6 (the 'behind its own chip' clauses become sub-chips …)".
- **After (v2):** s274-D11 is **not cited anywhere on D-1** (driver check G asserts it); it is cited on D-3(a) as the ruling D-3 enacts ("an instrument without a consumer is refused, the reader lands in the same commit") and named in Part C as "belongs to D-3, not here (it has no chip clause)". s275-D6: "**Refines** s275-D6 ('behind its own chip' — a sub-chip is still its own chip)" — the word "supersedes" does not appear in D-1(a) (asserted). s275-D4: D-1(a) now says "It is **not** the lane s275-D4 deferred the 20 standards-family joins to: those are new authored edges of a new type and are priced separately in Part E (G3)" — the contradiction (a re-cut that touches no edge type claiming to be the lane that adds 20 edges of a new type) is resolved by separating them: G3 in Part E prices the template re-cut and the 20-sentence authored lane as two lanes.

### Fix 3 — D-1 rewrite for a one-letter answer; 432/62 → 435/59 — AMBER F9 + Part 2
- **Before (v1):** one letter bought four things — the view re-cut, the name "Codex", a derived `scope` on every ruling, and "the dozen fences written once as the Constitution — the precedence ladder". (b) folded two of Dave's three words into one line. No letter existed for "three views but call it case law and write no constitution".
- **After (v2):**
  - **One letter for the views**: (a) one graph, three views by force — storage untouched, the WCAG criteria + accessibility rules + design rulings shown as **one obligation** with provenance sub-chips; (b) keep the five, relabel; (c) no views.
  - **One word for the record**: a free-text box on the card — "The name of the ruling record — one word · Codex · Constitution · System management · or your own word". It travels in D-1's exported note as the first line `record: <word>`; the export shape `{page, at, decisions[6]{id, choice, note}}` is unchanged (driver check H).
  - **Moved OUT of the options into the why, marked "Not asked on this card, and unratified — lane A2's proposal for you to author or refuse later"**: (i) the precedence ladder (with A2V's point that nothing in `_rulings.json` orders a ruling against a WCAG criterion and s277-D3 left the one known conflict open), (ii) the derived `scope` (named as a proxy that over-counts s269-D3, s274-D12, s275-D4 as "system"), (iii) the Constitution (four fences named, the rest not). Driver check G asserts "precedence ladder" is absent from the options and present in the why with "unratified".
  - **The 14 `obeys→ux` edges (s276-D3)** — the leak in "force by node kind" A2V found — named on the card with how the view handles it: *force is a property of the edge, not the node* — an `obeys`, `appliesTo` or design-scoped `governs` edge is an obligation wherever it lands; the 14 edges (6 metas: button, icon-button, links, notifications, tags, tags-input → 4 of the six A-grade laws: pr-fitts, pr-hick, pr-speed-accuracy, pr-graphical-perception) are drawn in Design governance, the principle node stays in Explanation, no edge is renamed. D-4(a) writes the same reading down: *must* = appliesTo / obeys→BLOCKING / design governs; *rests-on* = obeys→ux. Measured by `_measure_slice_v2.py` (`obeys_to_ux`), read on the page from the file.
  - **432/62 → 435/59**: the lede now says "measured, by the extractor's own `gov_target()` test, as **435 of 593** … 99 … 59 both — a proxy from `governs[]` targets, not a reading of each ruling". Read from A2V's `verify-figures.json → ruling_scope_by_governs_target`. Part C prints v1's 432/62 beside it as "a looser test that counted the snippet glob as a component". "161 design-scoped" → `rul_design + rul_both` = 158. Builder asserts `rul_system == 435`.
  - "By force" is labelled "lane A2's preference argued in prose — any re-cut fixes the measured symptom".

### Fix 4 — the small integers — AMBER F5 / F13 / F25 / F12 / RED F11
| where | before (v1) | after (v2) | read from |
|---|---|---|---|
| Part B Q8 | "19 resolved on **17** components" | **15** components + 51 declared nulls | `VERIFY.md` F5 (parsed: "19 live `mustNotNeighbour` on **15** components"); the null count from `verify-figures.json` |
| hero stat + D-3 lede | "12 types, **3,125** edges" | **3,110 live edges** (47%) | `verify-figures.json → consumers.nc12_edges`; denominator 6,616 live |
| D-3 lede | "**nine of the twelve** answer a designer's question directly" | "**four** of the twelve (`evidencedBy`, `appliesTo`, `ruledIn`, `definedIn`)" | `VERIFY.md` F25 (parsed) |
| D-2 lede | "8 of 34 guideline files — the files named after a component" | "the **7** named after a component (s276-D5) plus the data-visualisation family file (s277-D3)"; and "52 of the 350 are accessibility rules, and 51 of those already cite an SC that names components, so they are not facet rules" | `verify-figures.json → rules.files_reached_n − 1`, `a11y.acc_rule_to_sc_cites` |
| Part D rule row / G1 | 363 (v1 page was already right) | 363, now read from `verify-figures.json → rules.rules_no_component` instead of `470 − 107` | — |
| D-2 lede (added) | — | "4 of the 50 reach a component in two hops through `cites` → `appliesTo`; 46 reach nothing by any path" | `verify-figures.json → rules.blocking_reaching_via_cites_appliesTo / blocking_unbound_even_counting_cites_path` |
| D-3 lede (F22) | "self-measured 19,113 tokens against 111,468" (typed into A2-measure.json) | "**19.1K tokens against 111K for the 31 metas it replaces** on a dashboard task (5.8×; 2.6× on a four-meta bar-chart task; 3.8× on a fourteen-meta form)" | `slice-measure-v2.json → slice_runs` (build_slice() re-run in-process, three named tasks) |
| receipts (F30) | "none typed" | "v1 read three integers (19,113 / 111,468 / 414,184) that had been typed into `A2-measure.json`; v2 re-measures them" | — |
- `A2-AUDIT.md`'s "316 of 470" (§2, §7 G1) and the `e958e6d` commit message are **not edited** (A2's committed file); the correction stands here and in A2V: 316 = 470 − 154 `obeys` *edges*, the distinct-rule count is 363.

### Fix 5 — D-5 / D-6 — AMBER (s269-D3 call, F27, F28, S31)
- **D-5 before (v1):** "(a) **Tier grain, now.** The 10 live token files — or the dozen groups that carry most references — as `token:` nodes … Consistent with s269-D3". The "10 files" is the #269 proposal's *file* option, which the ruling rejected in favour of tier.
- **D-5 after (v2):** lede quotes the ruling's `ruled` text verbatim — *"TOKENS ENTER THE GRAPH AT TIER GRAIN - semantic versus primitive - and NEVER as 932 leaf nodes."* (hyphens as in `_rulings.json`) — and (a) is "**Group grain with its tier, now — as `_compose_slice.py` already reads it.** The token group (about 128 of them, the top twelve carrying 70% of references) as the `token:` node, each carrying its tier as an attribute … Roughly a hundred nodes and a thousand edges … The ruling's word is *tier*; group-with-tier is how the repo has operationalised it since #269 (`_compose_slice.py`: 'a slice names the token GROUP and its tier, never the leaves')." (c) leaf grain now names the counts (932 by the ruling, 792 live, 1,043 in `_blast-radius.json`) and says A3's ≈950-node TOKENS is this option "whatever its tier is called". The 128 / 1,587 / 70% figures are measured by `_measure_slice_v2.py` with A2's own regex (`_measure_a2.py:144`), not typed.
- **Q9 595K → ≈25K (F28):** the D-5 lede says "an honest today-cost for Q9 is about 25K tokens (the meta plus the blast-radius file), not the 595K A3 charged by reading `canon.css`"; D-6(d)'s plain sentence is kept as A3 wrote it with the phrase "as A3 costed it" and an **A2V correction** sentence appended inside the option; Part A's cost table prints `595,242 → **25,335**` on the Q9 row. 25,335 = A3's own "the meta" figure (5,286, its Q8 row) + `_blast-radius.json` 20,049 (measured) — A2V's ≈25K, on A3's own row.
- **2.6M labelled (F27):** D-6's lede: "A3 measured the twelve questions at about 2.6M tokens of file reads today — **summed per question**, counting `_rulings.json` three times and the metas twice; the de-duplicated read is about 1.0M with Q9 corrected". Part A's table carries the Σ row `2,603,214 → 2,033,307 → 1,035,142` (A3 summed → with Q9 corrected → de-duplicated over the union of files) against 2,139 for the slices. A2V's "≈1.5M de-duplicated" was computed with Q9 still charging `canon.css`; with Q9 corrected the union is ≈1.0M — both figures are honest, the page prints the corrected one and this report records A2V's. Ratios 949 : 1 summed, 483 : 1 de-duplicated; conclusion unchanged.
- **S31 dropped:** the v1 page never cited S31 (it lives in `A3-AUGMENT.md` §2.9 / §6 only); v2's D-6 lede says "of its 33 sources A2V spot-checked nine and eight hold — S31 does not carry the claim it is cited for and is dropped here". `A3-AUGMENT.md` is not edited.
- D-6's why: "about 950 nodes — a leaf count whatever its tier is called"; (d) says "Under D-5(a) this lands as group nodes with a tier, not ≈950 leaves" (A2V's "grey (d) out under D-5(a)", done as a sentence rather than a disabled control so Dave can still pick it).

---

## The D-1 rewrite — before / after, in one table
| | v1 | v2 |
|---|---|---|
| what a letter buys | views + Codex + derived scope + Constitution/ladder | the views only |
| the name of the record | inside (a) as "Codex"; (b) "Codex (or system management)" | a one-word free-text box under the options; rides in the export as `record: <word>` |
| precedence ladder | stated as fact in Part B ("law, then ruling, then BLOCKING …") | in the why and Part C as A2's proposal, "unratified", with the s277-D3 open conflict named |
| derived `scope` | part of (a) | in the why as a proxy (435/99/59) that over-counts s269-D3, s274-D12, s275-D4 as "system" |
| the Constitution | part of (a): "the dozen fences written once" | in the why: four fences named, the rest not; Dave's to author |
| s274-D11 | cited as a chip clause (wrong) | not on D-1; cited on D-3 as the reader-in-the-same-commit ruling |
| s275-D6 | "supersedes" | "refines" |
| s275-D4 | "is the named lane" while claiming no edge-type change | "not that lane" — the 20 authored joins are priced as their own lane (G3) |
| the 14 `obeys→ux` edges | not mentioned | named; handled by "force is the edge's, not the node's" (and written into D-4's *must* / *rests-on*) |
| "by force" | "the cut that fixes it is by force" | "lane A2's preference argued in prose — any re-cut fixes the measured symptom" |

---

## The thin-slice section (Part A) and D-3 — summary
Placed as the first evidence section, directly after the decisions; D-3 is retitled "The thin slice at build time — wire the reader, or keep reading the metas?" and (a) is "Wire it, under the thin-slice contract". Six decisions, no seventh.

**Headline numbers (all measured this session, `slice-measure-v2.json`):**
- Today, step 1 of the generate skill: `showroom/index.json` **22,987** tokens → the metas the agent picks (median **2,576** each; library **414,755** / 138 files / 1.6 MB) → the snippet (**≈10K** each; 1,394,384 for all 137) → `canon.css` **588,102** (the only door to a token by intent) + `type.css` 3,472; `_rules-index.json` 49,450 if consulted; icons manifest 40,943. Not read: `_rulings.json` 232,648, the rule nodes, the principle nodes, the baked graph 798,152. `_consult.py`: 109,270-token index, 63 of 593 rulings, 2.7–5.6K per answer.
- The slice (`_compose_slice.build_slice()`, three tasks): dashboard **19,117** vs 111,468 for 31 metas (**5.8×**; 22× vs the library) — 31 components, 58 rules (32 BLOCKING; 28 authored, 30 routed by vocabulary), 8 must-nots, 24 token groups, 3 rulings, 23 declared unresolved; form **11,716** vs 44,237 for 14 metas (3.8×); bar chart **5,735** vs 14,703 for 4 metas (2.6×).
- The twelve questions: **2,139** tokens of typed slices vs 2,603,214 summed (A3) → 2,033,307 with Q9 corrected → **1,035,142** de-duplicated.
- What the slice reads and does not: it walks 11 edge types and never `governs`, `obeys`, `appliesTo`, `evidencedBy`, `ruledIn` — the edges that answer Q1, Q2, Q5, Q6, Q11; its rules leg is routed by `RULE_FILE_ROUTES` (a hand dictionary) — D-2's scope join done by hand.

**What each decision does to the slice (the table on the page):** D-1 changes its *order* (one obligations read, not two stages and no SC), not its size · D-2 changes it *most* (the routed rules leg becomes a derived structural join; 30/58 routed on the dashboard, 21/40 on the form) · D-3 *is* the slice · D-4 changes its *labels* (sections become the twelve verbs) · D-5 changes the *source* of the tokens leg (regex + tier map → `bindsToken` walk), not its output · D-6: ASK is the slice's second verb; CLOSURE gives it inverse starts; SHAPES never touches it; TOKENS is D-5's leg; NEIGHBOURS may trail it, advisory, never a row in it.

**The contract (on the page, two columns):** in — intent (task sentence / chart-intent word / question verb), shape, roles, an optional component set as seed, a token budget · out — components (and why; alternates + `when`), governs (ruling ids, date, sentence), obeys (rule ids, destiny, authored / derived / routed), must-not (resolved + declared nulls with `$note`, `groupsWith` beside), tokens (group + tier + count, never leaves), assets (`usesIcon`/`usesLogo` when RI lands), unresolved (`ref: null`, s274-D10), sized (slice tokens, replaced tokens, ratio, printed on the slice). Three fences: never invents a binding (s274-D12); never hands over leaves, `canon.css` or the library; lands with its consumer in the same commit (s274-D11). The budget is the one thing nothing in the repo has yet.

---

## What I saw (the page, as Dave)
1280 light and dark, 390 light and dark, all opened. The hero's third stat first rendered "19." / "1K" on two lines — rounded to "415K → 19K" and made unbreakable. The `<q>` quotes of s269-D3 and `_compose_slice.py` first rendered with mangled quote glyphs from a CSS `quotes` escape — replaced with literal typographic quotes. The contract's list terms first sat on their own line because the column's block-`b` rule caught them — scoped. D-1 now reads as one paragraph per option and a boxed one-word ask; the word box holds at 390 in dark. Part A's three tables scroll inside their wrapper at 390 (the CP contract's allowed scroller); nothing crops. D-6 (d) shows A3's sentence and the A2V correction in the same option, readable. 22K px tall at 1280 — long, but the first ask sits at 9.5% of the page.

## Driver
28 checks, DRIVE PASS, both themes at 1280 and 390. New in v2: F (the five fixes on, the six struck figures off — by string), G (D-1 names s275-D6 / s275-D4 / s276-D3 and never s274-D11; "refines" not "supersedes"; ladder in the why as unratified, not in the options; "14 obeys" present), H (one word box on D-1 only; export shape unchanged; word round-trips), I (Part A before Part B with the slice figures and the contract), J (fresh never-driven context: 0 radios, 0 notes, 0 words, `localStorage.length == 0`, asserted twice — lane RIF's finding that the page saves the DOM on `beforeunload`). The nam-002 caps check excludes `q.ruled` — a ruling's or a source file's own words quoted verbatim — declared in the driver.

## Receipts
`git diff bedf383 HEAD -- knowledge/` empty before and after; `git status` under `knowledge/` clean. `_compose_slice.build_slice()` and `.measure()` called in-process (prints nothing, writes nothing). tiktoken cl100k_base 0.14.0. s269-D3 quoted from `knowledge/_rulings.json` `ruled` (checked against the file, hyphens kept); `_compose_slice.py` quoted from its own docstring. `--numstat` below, re-read from the shipped sha.

## `--numstat` (re-read from the shipped sha, then amended into it)
```
ca89a71

100	0	notes/_lanes/277/kg-audit/FIX-REPORT.md
646	0	notes/_lanes/277/kg-audit/REVIEW-kg-audit-2026-09-16-v2.html
737	0	notes/_lanes/277/kg-audit/_build_page_v2.py
324	0	notes/_lanes/277/kg-audit/_drive_page_v2.py
185	0	notes/_lanes/277/kg-audit/_measure_slice_v2.py
-	-	notes/_lanes/277/kg-audit/a2f-390-dark.png
-	-	notes/_lanes/277/kg-audit/a2f-390-light.png
-	-	notes/_lanes/277/kg-audit/a2f-dark-1280.png
-	-	notes/_lanes/277/kg-audit/a2f-decisions-dark.png
-	-	notes/_lanes/277/kg-audit/a2f-decisions-light.png
-	-	notes/_lanes/277/kg-audit/a2f-light-1280.png
81	0	notes/_lanes/277/kg-audit/kg-audit-decisions-2026-09-16-v2.json
364	0	notes/_lanes/277/kg-audit/slice-measure-v2.json
```
