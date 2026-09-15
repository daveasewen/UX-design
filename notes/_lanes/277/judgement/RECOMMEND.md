# Lane CJ — RECOMMEND — the judgement call on the three chart questions
#277 · 2026-09-15 · `s276-D5` "then STOP and look again" · model: fable · READ-ONLY · one file, one commit

Independence held: `notes/_lanes/277/charts/REPORT.md` and its proposed metas were not opened. Everything
below was measured from the four guideline files, the 14 chart metas, `_rules-index.json`, `_rule_nodes.json`,
`meta.schema.json`, `roles.json`, `component-types.json`, git history, and the six landed `obeys` blocks.

---

## Q1 — does `chart-donut` share the pie spec?

**RECOMMENDATION (a):** Yes — `chart-donut` takes `data-visualisation-pie-charts.md` as its home spec because the file itself names the doughnut as one of its two types, so author all 11 pie rules on the donut and only 10 on the pie: `dv-pie-003` (doughnut centre) binds the donut alone and stays off `chart-pie`.

### Evidence
1. **The file names the donut, in three places.** `## Types` lists "Doughnut — inner circle punched out"; `dv-pie-009` reads *"Maximum 6 slices — both pie and doughnut"*; `dv-pie-003` is *"Doughnut centre: total value + descriptor together"* — a rule that exists only for the donut. This is a stronger signal than the `s276-D4` precedent, where the buttons spec merely "NAMES icon-only as one of its three structural variations": here the file carries a rule that binds the shared component and NOT the file's namesake.
2. **Rule-by-rule, the encoding rules bind unchanged.** I read each of the 11 against the donut meta (`chart-donut.meta.json`: ring, `parts-of-whole`, slices, centre total, leaders, legend):

| rule | text (short) | binds donut? | binds pie? | note |
|---|---|---|---|---|
| dv-pie-001 | start 12 o'clock, largest → smallest | yes, unchanged | yes | neither meta states a start angle — `$why` must say "governs; not yet enacted in this meta" |
| dv-pie-002 | label + exact value per slice, leaders, key | yes, unchanged | yes | donut meta: "spider = letter on a short leader … direct = name + value" |
| dv-pie-003 | doughnut centre: value + descriptor | **yes — donut only** | **no** | donut meta: "Centre total — .t-cm-figure-3"; pie meta: "DV-D13 centre-total wiring removed (donut-only)" |
| dv-pie-004 | direct labelling adjacent to segments | yes, unchanged | yes | both metas: leaders + direct-label variant |
| dv-pie-005 | inside-slice labels only when readable | yes (a ring is narrower — binds harder) | yes | |
| dv-pie-006 | slice direction vs AT | yes, unchanged | yes | |
| dv-pie-007 | never enlarge / pull out slices | yes, unchanged | yes | |
| dv-pie-008 | proportion of a total only | yes, unchanged | yes | donut `when`: "parts sum to a whole" |
| dv-pie-009 | max 6, "both pie and doughnut" | yes, by name | yes | both metas' `slices` prop: "Maximum 6 (dv-pie-009)" |
| dv-pie-010 | values sum to total, value indicators | yes, unchanged | yes | donut: "sum to the displayed centre total (dv-pie-010)" |
| dv-pie-011 | indicate when rounded | yes, unchanged | yes | neither meta mentions rounding — same "governs; not enacted" `$why` |

**11 of 11 bind the donut; 10 of 11 bind the pie.** That is not resemblance, that is governance.
3. **The provenance runs the other way.** `chart-pie.meta.json` `purpose`: *"ported from Chart-donut.reference.html … with the inner radius dropped to 0"*; `chart-pie` `provenance.code_path` is `knowledge/snippets/Chart-donut.reference.html`. The pie is the derived component in this repo; the donut is the source. "Does the donut share the pie's spec" has the polarity backwards — the spec is a circular-charts spec that happens to be filed under "pie".
4. **The precedent's shape is a subset, not the whole file.** Measured on the six landed metas: `icon-button` cites 6 of the buttons file's 14 rules, `tags-input` 5 of 23. "Shares the spec" has never meant "takes every rule"; it means the file is in scope and each rule is judged. Here the judgement comes out 11/11 — but it was made per rule, not by file.

### Strongest case against
"A donut is a pie with a hole, and `s276-D5` said the name-match tier is NOT widened. `chart-donut` is not named in any filename; admitting it by prose-reading is the first step of the slope that produced `Avatar` from `va25-013`." Fair — and the answer is that the admission is not by name-match on rule prose but by the file's own `## Types` heading and by a rule (`dv-pie-009`) that names the doughnut in its normative text. The discriminator I would apply, and which also decides Q3: **a component shares a spec file when the file's own structure (a Types heading or a rule's normative clause) names it, not when a rule's prose happens to contain its word.**

### What would have to be true for "no" to win
Either the pie file would have to be silent on doughnuts (it is not), or the donut would have to break one of the encoding rules by construction (it breaks none — the ring only changes what the centre carries, and the file has a rule for exactly that).

### Cost
+11 `obeys` entries on `chart-donut`; `chart-pie` takes 10 (not 11). 0 new nodes, 0 new edge types, 0 schema change. One visible inconsistency surfaces and should be written into a `$why`, not smoothed over: `roles.json` and `chart-pie.when` say **"≤ 5 parts"** while `dv-pie-009` says **maximum 6** — a routing preference sitting one below the spec's cap, with no source for the 5 in any ingested file.

---

## Q2 — where do the 19 family rules in `data-visualisation.md` attach?

**RECOMMENDATION (b):** Per-component authored subset — about 46 entries, not 57, with `dv-013` and `dv-015` on none of the three and five further rules left off the chart they do not reach — because 11 of the 57 blanket edges would be false and the 30 that repeat identically across the three are the measured shape of a family node that does not yet exist.

### Evidence — every rule read against every chart
Binding was judged from the rule's normative text against what each meta says the component draws (bar: categorical axis, bars, grouped/stacked; line: time axis, lines, markers; pie: ring, no axes).

| rule | short text | bar | line | pie | note |
|---|---|---|---|---|---|
| dv-001 | complete scale range, no truncation | yes | yes, `$why` must cite `dv-line-001` (zero optional ≠ licence to truncate) | **no** — no scale | file itself says "axis-min ≠ 0 detection on bar charts" |
| dv-002 | full charts, reasonable scales | yes | yes | **no** — no scale | |
| dv-003 | show the full data set | yes | yes | yes | |
| dv-004 | ≥2px separation between colour blocks | yes | **no** — a line has no colour blocks | yes | pie & donut metas already enact it ("2px page stroke") |
| dv-005 | tabular alternative + link | yes | yes | yes | all 14 metas already cite it |
| dv-006 | labelling (compound: title · key · tooltips · direct labels in circular · past/projected) | yes (title/key/tooltip/projected) | yes (same) | yes (**the circular clause**) | compound rule — `$why` MUST name the clause |
| dv-007 | responsive ordering, grid, text-resize | yes | yes | yes | |
| dv-008 | horizontal scroll last resort | yes | yes | **no** — a pie never scrolls | |
| dv-009 | flat fills, no 3D/gradient | yes | yes | yes | |
| dv-010 | uncluttered overlays | yes | yes | yes | |
| dv-011 | not colour alone | yes | yes | yes | |
| dv-012 | colour never as chart background | yes | yes | yes | |
| dv-013 | combination charts: colour differentiates sets | **no** | **no** | **no** | a rule about a chart none of the three is |
| dv-014 | same data = same colour across a journey | yes | yes | yes | all 14 metas cite it |
| dv-015 | four chart-type categories; choose by data | **no** | **no** | **no** | a rule about CHOOSING a chart — it is what `roles.json`'s `chart-panel` `when` predicates enact, and it binds the role, not a component |
| dv-016 | building-block contrast ≥3:1 | yes | yes | yes (title/labels; no axis clause) | |
| dv-017 | palette colours only | yes | yes | yes | |
| dv-018 | different colour per variable — names bar, circular, line explicitly | yes (bar clause) | yes (line clause) | yes (circular clause) | the one family rule that binds each chart by a DIFFERENT clause — the model `$why` |
| dv-019 | vibrating boundaries (Apollo-added) | yes (fills) | **no** — no adjacent fills | yes | |
| **count** | | **17** | **15** | **14** | **46 of 57** |

- **Option (a) manufactures 11 false edges**: 6 from `dv-013`/`dv-015` (bind none), `dv-004` and `dv-019` on the line, `dv-001`/`dv-002`/`dv-008` on the pie. Every one of those would carry an authored-looking `$why` — the `s274-D12` shape wearing a sentence.
- **10 rules bind all three identically** (003, 005, 007, 009, 010, 011, 012, 014, 016, 017) = 30 of the 46 entries. Their `$why` sentences will differ only by which meta field enacts them (bar: `tokens.series` names `data/series-1..5` for dv-017; pie: the 2px stroke for dv-004). That repetition is not waste — it is the first measurement of which rules are truly family-level, which is what a family node would need to carry and what nobody has yet measured.
- **Nothing today can carry an inheritance.** I checked the three candidates for option (c): (i) `artefact:knowledge/guidelines/data-visualisation.md` exists in `_rule_nodes.json` and the 19 rules hang off it by `definedIn` — but it is a document node (`docOf: rules`); a component→artefact edge would be a new edge type and would say "this file governs" with no per-rule `$why`, so a reader would traverse it to all 19 including `dv-013`/`dv-015` — the same 11 half-truths, one hop shorter. (ii) `component-types.json` has `dataviz` with all 14 charts as `$members` — a real family, but it is a CSS-contract registry, not a graph node, and it includes `chart-sparkline` and `Chart-bullet`. (iii) `role:chart-panel` is a graph node with 12 members — `chart-sparkline` left it (s254-D2) and `Chart-bullet` provides `headline-metric`, so it is the wrong family. Option (c) therefore needs: a new node kind, a new `memberOf`/`inheritsFrom` edge type, a propagation rule for `obeys` through it, and an explorer chip — three or four vocabulary changes, each Dave's (#75).
- **`s269-D1`'s remaining steps do not imply it.** Step 4 is icons then logos; step 5 is the four edge types `setIn` / `behaviourFrom` / `capturedFrom` / `acceptsCapability`. None is a family or inheritance edge. A family node is a NEW proposal, not a pending one.

### Strongest case against
"(b) is 46 hand-written sentences, 30 of them near-duplicates, for one family — and there are eleven more charts behind these three. That does not scale; build the family node now and write ten sentences once." The scaling argument is right and I would make it myself at the point where the nine unreachable charts (Q3) come due. It is wrong NOW for two reasons: the family node's rule list would be a guess until the three are authored (I count 10 family-wide rules; the authored pass will confirm or correct that), and `s269-D1` says every new edge type PROPOSES its schema diff and Dave ratifies — so (c) cannot land in this lane regardless. (b) is the only option that produces a true graph this wave and the only one that produces the evidence (c) needs.

### What would have to be true for (a) or (c) to win
(a): every one of the 19 would have to bind every chart — `dv-013` and `dv-015` already fail that on their own text. (c): a family node with a ratified `inheritsFrom` edge and a propagation rule would have to exist — it does not, and nothing queued creates it.

### Cost
(b): ~46 `obeys` entries (bar 17 · line 15 · pie 14), 0 nodes, 0 edge types, 0 schema change. (a): 57 entries, 11 false. (c): 1 node kind + 1–2 edge types + a propagation rule + explorer work, all pre-ratification; 0 edges this wave.

---

## Q3 — the other 11 chart components

**RECOMMENDATION:** Two of the eleven pass the Q1 test today and should be authored in the same wave — `chart-sparkline` (the line file's `## Types` names spark as its second type and `dv-line-009`/`dv-line-010` are spark-only) and `chart-combo` (its bar half obeys `dv-bar-009`, its line half `dv-line-001`/`-006`/`-011`, each cross-file citation naming the half it binds, `s276-D4` links→ctkb-004 shape) — the other nine are named by no spec file and wait for the family node, and their capitalised filenames are a naming defect from the 08-05 wave, not a second provenance: log it, do not rename it this wave.

### Evidence — sparkline
- `data-visualisation-line-charts.md` `## Types`: *"Spark (sparkline) — simplified high-level overview"*; a whole `## Spark charts` section; `dv-line-009` (aspect ratio) and `dv-line-010` (never split in tables) are spark-only rules, exactly the `dv-pie-003` pattern. The sparkline meta already enacts `dv-line-009` ("wide aspect 6.4:1", antiPattern "A tall/square spark (dv-line-009)") and cites `dv-line-011`.
- Consequence for `chart-line`, mirror of Q1: **`dv-line-009` and `dv-line-010` stay OFF `chart-line`** — they are the spark's rules in the line's file. Lane CO's line pass must not take all 11 by filename.
- Of the remaining line rules, the sparkline takes `dv-line-011` (straight), `dv-line-001` (zero optional — the meta says the atom "computes its OWN value domain" for this reason); it does NOT take `dv-line-003`/`-004`/`-006` (axis titles, tooltips on both axes, dual axes — the spark is axis-free by definition). Roughly 4 entries, not 11.

### Evidence — combo
- `chart-combo.meta.json` is the most rule-literate meta in the set: `dv-line-006` cited seven times and it is the rule that makes the component legal (`when`: "units=different … (dv-line-006)"; antiPattern "Dual axes for the SAME unit (dv-line-006)"); "bar axis zero-based ALWAYS (dv-bar-009)"; "the line's secondary axis MAY FLOAT (dv-line-001)"; "Curved series paths (dv-line-011)". These are authored statements about which half of the composite each rule governs — the precise thing a `$why` is. Four cross-file entries, each saying which half.
- **`dv-013` ("Combination charts … colour differentiates the data sets") must NOT be attached to combo.** "Combination" ≈ "combo" is a name match; the family file's example is "positive/negative", and whether HSBC's "combination chart" is a bar+line dual-axis chart is not established by any ingested text. This is the exact `s274-D12` shape and I refuse it below.

### Evidence — the nine wait
`Chart-boxplot` · `Chart-bullet` · `Chart-butterfly-h` · `Chart-butterfly-v` · `Chart-candlestick` · `Chart-histogram` · `Chart-scatter` · `chart-stacked-area` (and `Chart-bullet` provides `headline-metric`, not `chart-panel`). None is named by any spec file's Types heading or by any rule's normative clause; `dv-015` lists "histogram, box plot … bullet, candlestick" only as entries in a chart-choice taxonomy. Each has at most one cross-file rule it genuinely obeys (histogram → `dv-bar-009`; stacked-area → `dv-line-011`), and a single edge on a component answers "what governs this chart?" with a false "one rule", which is worse than a visible zero. Two of them cite a rule to say they ESCAPE it: `Chart-candlestick` — *"dv-render.js floors every domain at zero (dv-bar-009) and a price series 90.41–108.52 against a zero floor is a smear, so the partial computes its own"*; `Chart-butterfly-h` — "Negative values inside either series (dv-bar-007-style — the mirror direction already encodes the second series". A meta citing an id is not a meta obeying it. What must exist first: the family node from Q2(c), with the 10 family-wide rules (as confirmed by the Q2 authored pass) hung on it once — then the nine get a TRUE answer ("the family rules, and nothing type-specific yet") with zero fabricated entries.

### Evidence — the capitalisation split is a defect
- **Same commit, both cases.** `df44e51` (2026-08-05, "CHART WAVE 2 … 8 MEMBERS, 3 SONNET LANES") created eight metas: `Chart-boxplot` · `Chart-bullet` · `Chart-butterfly-h` · `Chart-butterfly-v` · `Chart-candlestick` · `Chart-histogram` capitalised AND `chart-pie` · `chart-stacked-area` lowercase. `Chart-scatter` (`00abdf3`, 07-23) and `chart-combo` (`ecf6e56`, 07-24) were created a day apart in opposite cases. Not two waves.
- **`provenance.source` does not align with case.** gap-report: `Chart-boxplot`, `Chart-bullet`, `Chart-candlestick`, `Chart-scatter`, **`chart-combo`**. code: `Chart-butterfly-h/-v`, `Chart-histogram`, **`chart-pie`**, **`chart-stacked-area`**. proforma-promotion: `chart-bar`, `chart-line`, `chart-donut`, `chart-sparkline`. Not two provenances.
- **Every other register is uniform.** All 14 snippets are `Chart-*.reference.html`; `component-types.json` `dataviz.$members` lists all 14 as `Chart-*`. Only the meta filename — and therefore the graph slug — is mixed, so the meta case is whichever lane author's habit, not a signal.
- **It is load-bearing.** The slug is the node id (`component:Chart-boxplot` in `_kg_history.json`) and is referenced in 29–50 non-generated files per component (`roles.json`, `shapes.json`, `_validate_dataviz.py`, `_HIT-AREA-ADVISORY.json`, lane notes…). A rename is 7 two-step `git mv`s on a case-insensitive filesystem plus a reference sweep across ~50 files plus regeneration — a lane of its own, and one whose commit message says "rename" while touching 50 files, the `#179` class of diff. Not this wave; a parked item with a tripwire on the next graph regen.

### Strongest case against
"Sparkline and combo are cross-file judgement calls, and `s276-D5` says the filename-join route ends at the three." True of combo, half-true of sparkline. The sparkline is reachable by the same test as the donut — the file names it — so refusing it while accepting the donut is inconsistent. Combo IS the first genuinely cross-file component; the defence is that every one of its four entries lifts a binding the meta already states in its own words about its own halves, and the precedent (`links` obeys `ctkb-004`, "stated from the buttons side") is exactly one cross-file citation with the reason in the `$why`. If Dave wants the wave to stay strictly at "the file names it", drop combo and keep sparkline; that is a one-word narrowing, and the recommendation survives it.

### What would have to be true for "all eleven wait" to win
The line file would have to not name the spark (it does, with two rules of its own), and the combo meta's four bindings would have to be inference rather than authored statements (they are its `when` and its antiPatterns).

### Cost
sparkline ≈ 4 entries; combo 4 entries; nine components 0 entries and one parked item (naming defect, tripwire). `chart-line` loses 2 it would otherwise have taken by filename (`dv-line-009`, `-010`).

---

## What I would refuse

Everything here is attractive, cheap, and the `s274-D12` false-positive shape.

1. **All 11 pie rules onto `chart-pie` by filename.** `dv-pie-003` is a doughnut rule that lives in the pie file. Filename join is the entry test, not the exit test — every entry still has to survive the rule's own text. Same for `dv-line-009`/`-010` on `chart-line`.
2. **All 19 family rules onto anything by file.** `dv-013` and `dv-015` bind no component at all (one is chart-combo's-or-nobody's, one is the role's). Eleven of 57 would be false with a sentence on them.
3. **Lifting `dv-xxx` ids out of meta prose into `obeys` by regex.** It looks authored — the id was typed by a lane. It is not: `Chart-candlestick` and `chart-sparkline` cite `dv-bar-009` to record that they ESCAPE it, and `Chart-butterfly-h` cites `dv-bar-007` to say the mirror is not a negative value. An id-match over metas is `s274-D12` one level up — the same failure with a better alibi.
4. **`dv-013` → `chart-combo` on the word "combination".** The family file's example is "positive/negative"; nothing ingested says HSBC's combination chart is a dual-axis bar+line. Name match on prose, verbatim the refused tier.
5. **A component → `artefact:…data-visualisation.md` edge as a cheap family node.** It resolves (the node exists) and it is one hop — and it silently asserts all 19 with no `$why`, which is option (a) without the sentences. If a family node is wanted, it is a new node kind with a propagation rule, proposed to Dave, not a reuse of a document node.
6. **One cross-file edge on each of the nine "because it's better than nothing".** A single true edge on a component makes the graph's answer to "what governs this chart?" a confident "this one rule" — a half-truth with the shape of completeness. A visible zero tells the designer the truth: not yet authored.
7. **Renaming the seven capitalised metas inside the charts lane.** Right fix, wrong commit: 50-file blast radius under a message about `obeys`, and a case-only rename on this filesystem needs the two-step `git mv` or git records nothing. Park it, tripwire it, do it as its own lane.

---

## The three lines for the decision card
- **Q1 (a):** Yes — `chart-donut` takes `data-visualisation-pie-charts.md` as its home spec because the file itself names the doughnut as one of its two types, so author all 11 pie rules on the donut and only 10 on the pie: `dv-pie-003` (doughnut centre) binds the donut alone and stays off `chart-pie`.
- **Q2 (b):** Per-component authored subset — about 46 entries, not 57, with `dv-013` and `dv-015` on none of the three and five further rules left off the chart they do not reach — because 11 of the 57 blanket edges would be false and the 30 that repeat identically across the three are the measured shape of a family node that does not yet exist.
- **Q3:** Two of the eleven pass the Q1 test today and should be authored in the same wave — `chart-sparkline` (the line file names spark as its second type; `dv-line-009`/`-010` are spark-only) and `chart-combo` (four cross-file citations, each naming the half of the composite it binds) — the other nine are named by no spec file and wait for the family node, and their capitalised filenames are a naming defect from the 08-05 wave, not a second provenance: log it, do not rename it this wave.

---

## Commit
`edb5f09` (amended in place with this receipt — still ONE commit) `#277 2026-09-15 — lane CJ: the judgement call on the three chart questions …`

```
148	0	notes/_lanes/277/judgement/RECOMMEND.md
```

The `.git/index.lock` found at commit time was 13 minutes stale (mtime 21:26:03, no git process alive); it was MOVED to `.git/_orphan-locks/index.lock.20260915T213854.laneCJ`, never deleted. The sandbox cannot unlink `HEAD.lock`/`tmp_obj_*` after a commit (the known delete-permission class); those were moved to `.git/_orphan-locks/` too.
