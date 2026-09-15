# LANE CO — REPORT — the three charts: chart-line · chart-pie · chart-bar
#277 · 2026-09-15 · enacting `s276-D5` · model: opus · **PROPOSE-ONLY — NOTHING LANDED**

---

## 1. The counts, with the command that produced each

```
$ python3 -c "import json,collections
d=json.load(open('knowledge/guidelines/_rules-index.json'))
c=collections.Counter(r['file'] for r in d['rules'])
for f in [...]: print(f, c[f])"

data-visualisation-bar-charts.md    10
data-visualisation-line-charts.md   11
data-visualisation-pie-charts.md    11
data-visualisation.md               19
```

**The brief's measured line is CORRECT and mine agrees with it exactly**: bar 10 · line 11 · pie 11 ·
family 19. Index total 470. The same figures are re-asserted every run by `_author_metas.py --selftest`
bite 4, which reads them from the index rather than from this report.

| figure | value | where from |
|---|---|---|
| rules in the three spec files | **32** | index, filename join |
| `obeys` edges proposed | **29** | `_author_metas.py` RULES table |
| rules dropped, declared | **3** | `_author_metas.py` DROPPED table |
| `ux:` law citations proposed | **0** | out of scope, §7 |
| `obeys` edges live in `knowledge/components/` today | **81** | `_dry_run.py` §3, lane TO's six metas |
| `obeys` edges after landing (simulated) | **110** | `_dry_run.py` §3 |
| `rule:` nodes in `_rule_nodes.json` | **470** | `_dry_run.py` §2 |
| proposed refs that do not resolve to a node | **0** | `_dry_run.py` §2 |
| schema errors on the three proposed metas | **0** | `_dry_run.py` §1 |

---

## 2. Per-rule bind / no-bind

Produced by `python3 notes/_lanes/277/charts/_author_metas.py --table`. The join is on the FILENAME. Not
one id came from a regex over rule prose (`s274-D12`, `s276-D5`: the name-match tier is not widened).

### chart-line <- `data-visualisation-line-charts.md` — 11 in file · **9 bind · 2 dropped**

| rule | destiny | verdict |
|---|---|---|
| dv-line-001 | ADVISORY | obeys — the line side of the deliberate zero-baseline asymmetry |
| dv-line-002 | ADVISORY | obeys — the meta's `series` prop already cites it by id |
| dv-line-003 | ADVISORY | obeys — the parts DV-D07 mints `data/axis` and `data/grid` for |
| dv-line-004 | ADVISORY | obeys — the dvTip popover, and the both-axes clause |
| dv-line-005 | TASTE | obeys — why `responsive` pins the viewBox 1:1 |
| dv-line-006 | ADVISORY | obeys **by yielding** — the meta's `when` hands different units to chart-combo |
| dv-line-007 | ADVISORY | obeys — the `legendFilter` prop |
| dv-line-008 | ADVISORY | obeys — end-line markers and projected-state labelling on the multi-series variant |
| **dv-line-009** | ADVISORY | **DROPPED** |
| **dv-line-010** | ADVISORY | **DROPPED** |
| dv-line-011 | BLOCKING | obeys — the meta's first antiPattern cites it by id |

### chart-pie <- `data-visualisation-pie-charts.md` — 11 in file · **10 bind · 1 dropped**

| rule | destiny | verdict |
|---|---|---|
| dv-pie-001 | ADVISORY | obeys — the angle contract for the baked `data-a1`/`-a2` segments |
| dv-pie-002 | ADVISORY | obeys — the spider leader IS the rule's indicator line |
| **dv-pie-003** | ADVISORY | **DROPPED** |
| dv-pie-004 | ADVISORY | obeys — the meta's second declared variant |
| dv-pie-005 | TASTE | obeys — why labels sit outside the ring |
| dv-pie-006 | ADVISORY | obeys — the order the segment focus stops are read in |
| dv-pie-007 | ADVISORY | obeys — why there is no exploded variant |
| dv-pie-008 | ADVISORY | obeys — the meta's `when` gate from the guidance side |
| dv-pie-009 | BLOCKING | obeys — the `slices` prop cites it by id |
| dv-pie-010 | BLOCKING | obeys — and binds HARDER here than on the donut, there being no centre figure |
| dv-pie-011 | ADVISORY | obeys — the contract the `valueMode` toggle has to honour |

### chart-bar <- `data-visualisation-bar-charts.md` — 10 in file · **10 bind · 0 dropped**

dv-bar-001 · -002 · -003 · -004 · -005 · -006 · -007 · -008 · -009 · -010, all obey, each with an
authored sentence. Two notes worth reading:

- **dv-bar-006** (grouped extras) binds because the meta declares `grouped-column` and `stacked-column`
  variants; nothing else in the meta supplies their anatomy.
- **dv-bar-008** (label past vs projected) binds even though the meta declares NO projected variant. It
  is a constraint any future one must satisfy. A rule can bind a component without the component having
  a feature for it, and the `$why` says exactly that rather than pretending the variant exists.

---

## 3. The three drops, and why each one is a finding

`s276-D5` makes "reviewed by eye" part of the ruling. A declared drop is a finding; a silent drop is the
`s214-D6` failure. All three come from **structure inside the file**, not from taste.

| rule | dropped from | the reason |
|---|---|---|
| **dv-line-009** | chart-line | Sits under the line file's own `## Spark charts` heading and governs the SPARK's aspect ratio against surrounding content. `chart-sparkline` is a separate meta; the rule is its. |
| **dv-line-010** | chart-line | Same heading — "in tables, group all data related to the spark sequentially". A table-composition rule about sparklines. chart-line is never placed inside a table row; chart-sparkline is. |
| **dv-pie-003** | chart-pie | "Doughnut centre: total value + descriptor together" is donut-only. `chart-pie.meta.json`'s own `purpose` records that the DV-D13 centre-total wiring was REMOVED ("donut-only, per brief") and its antiPatterns ban porting it across. A pie with no centre has no centre contract to obey. |

**Corroboration.** Lane CJ (Fable, parallel, independent — it states it did not open this lane's files)
reached the same three drops by the same reasoning, in its Q1 table and its Q3 sparkline section. Two
seats converging on `dv-pie-003` and the two spark rules, from opposite directions, is the strongest
signal this lane produced.

---

## 4. Q1 — `chart-donut` and the pie file. Facts only; not ruled.

The question: does `chart-donut` share `data-visualisation-pie-charts.md` the way `icon-button` shares
the buttons spec?

**The precedent, measured.** `icon-button.meta.json` (landed by `577c82d`) carries **6** `rule:` citations,
all from `common-toolkit-buttons.md`, which holds **14**. So "shares the spec" has never meant "takes
every rule" — it means the file is in scope and each rule is judged.

**Does the pie file's prose name the donut? YES, in four places.**

1. `## Types` — "**Doughnut** — inner circle punched out, used to emphasise the total value." The file's
   own structure declares the donut one of its two types.
2. `dv-pie-009`, a BLOCKING rule, in its normative text: "Maximum 6 slices — **both pie and doughnut**."
3. `dv-pie-003` exists ONLY for the donut: "Doughnut centre: total value + descriptor together."
4. The file's last line: "Gauge pattern: a series of single-value doughnuts."

**Does `chart-donut.meta.json` describe itself as a pie variant?** Not in those words — its `purpose` is
"Composition / proportion as a ring with a centre total". But it **already cites the pie file's two
BLOCKING rules by id, in its own antiPatterns**:

```
$ grep -o 'dv-pie-[0-9][0-9][0-9]' knowledge/components/chart-donut.meta.json | sort -u
dv-pie-009
dv-pie-010
```

And the provenance runs the OTHER way: `chart-pie.meta.json`'s `purpose` says it was "ported from
`Chart-donut.reference.html` … with the inner radius dropped to 0", and `chart-pie`'s
`provenance.code_path` is `knowledge/snippets/Chart-donut.reference.html`. In this repo the **pie is the
derived component and the donut is the source**.

**Is there a `family` edge between them in the graph? NO.**

```
12 of 139 metas carry a family edge: cards · headers · input-fields · links · list-items ·
modals · navigations · notifications · pagination · segmented-control · selection-controls ·
view-options.  chart-pie: none.  chart-donut: none.  icon-button: family = null.
```

Worth noting for the comparison: **`icon-button` has no `family` edge to `button` either**. The precedent
is not carried by a `family` edge at all — it is carried by the spec file naming the variant plus the
meta's own purpose prose. On that test the pie/donut pair is a *stronger* case than the precedent, not a
weaker one.

What DOES exist in the graph between them: `chart-pie.edges.yieldsTo -> component:chart-donut`, and
`chart-pie["not-with"]` naming `chart-donut` ("pick one, pie or donut, not both").

**Not ruled here.** Presented as D-2 on the review page with both sides.

---

## 5. Q2 — the 19 family rules in `data-visualisation.md`. Options laid out; not ruled.

**What the corpus does today for above-the-component rules: NOTHING.**

```
button           14 x common-toolkit-buttons.md          + 3 ux:
icon-button       6 x common-toolkit-buttons.md          + 2 ux:
links            15 x common-toolkit-links.md, 1 x buttons + 3 ux:
notifications    17 x common-toolkit-notifications.md    + 2 ux:
tags              9 x common-toolkit-tags-chips.md       + 2 ux:
tags-input        5 x common-toolkit-tags-chips.md       + 2 ux:
```

`common-toolkit-foundations.md` holds **4** rules (ctkf-002, -003, -007, -009) that sit above all four
components lane TO authored — grid variants, a reserved type tier, light-bleed compensation. **Zero**
were attached to any meta. There is no precedent to follow here, only one to set.

### The three options, with the count each implies

| option | edges | what it is |
|---|---|---|
| **(a)** attach all 19 to each | **57** | Simple. **11 of the 57 would be false** — a rule that does not bind, carrying an authored-looking sentence. That is the `s274-D12` shape wearing a sentence. |
| **(b)** the authored subset per component | **49** | bar **18** · line **16** · pie **15**. Each read against that chart. |
| **(c)** a chart family / parent node | **19** once | Nothing can carry it today — see below. |

### (b), measured per component

Full matrix in `_author_metas.py --table`. Summary of the non-binding cells:

- **dv-013** (combination charts) — off line and pie. Combination charts are `chart-combo`'s job, and a
  pie holds one variable's parts.
- **dv-015** (choose line/spark/bullet/candlestick for change over time) — off bar and pie. Neither is
  one of the four the rule names.
- **dv-001 / dv-002** (scale range, reasonable scales) — off pie. A pie has no scale.
- **dv-004** (2px between colour blocks) — off line. Strokes are not adjacent colour blocks.
- **dv-019** (vibrating boundaries) — off line, same reason.

### (c) — what would have to exist for it to work

1. `obeys` is defined on **component metas only** (`meta.schema.json`, `edges.obeys`). A family node is
   not a component meta, so there is nowhere to write the block.
2. `role:chart-panel` is the nearest existing family node — **12** of the 14 chart metas provide it, and
   `chart-sparkline` (none) and `Chart-bullet` (`headline-metric`) do not. Wrong membership.
3. It would need: a new node kind, an inheritance/`memberOf` edge type, a propagation rule for `obeys`
   through it, and an explorer chip. Three or four vocabulary changes, each Dave's.

### Two findings inside this question

**(i) `_rules-index.json`'s row for dv-019 is WRONG.** The index gives dv-019 dv-017's sentence ("Only
palette colours in charts…") with the scoped-override annotation appended. But
`knowledge/guidelines/data-visualisation.md` line 70 shows dv-019 is a rule in its own right: the
Apollo-added **avoid vibrating boundaries** rule, `[ADVISORY-derivable -> gate check in
_validate_dataviz.py; APOLLO-ADDED rule] {#dv-019}`. The indexer appears to take the whole bullet from
the leading `-` to the closing `{#…}` tag, so the dv-017 bullet's text was captured for both ids.
**Reported, not fixed** — `_rules-index.json` is not this lane's to write, and `gen_rules_index.py` is
its generator. My Q2 matrix reads the SOURCE FILE for dv-019, not the index row, and says so in the cell.
It does not touch the 29 Part-A edges: dv-019 is in no spec file.

**(ii) My first pass had dv-019 as a duplicate and dv-009 off chart-line; both were wrong.** I corrected
them against the source file and against `chart-line`'s `markers` prop (the markers ARE filled shapes, so
the flat-fill rule reaches the component through them). The correction moved (b) from 46 to 49. Recorded
because a lane that only shows its final numbers is not showing its work.

### Disagreement with lane CJ, declared

CJ also recommends (b) and also arrives at a per-component subset. Our totals differ (CJ 46, mine 49) and
some cells disagree. Neither of us decides this; the conductor reconciles.

| rule | CJ | me | who has the evidence |
|---|---|---|---|
| dv-008 on pie | no ("a pie never scrolls") | **binds** | Me. `chart-pie.meta.json` `responsive.rule`: "`.dv-stage` scrolls if the container is narrower." |
| dv-013 on bar | no | **binds** | Open. The rule's own example is "positive/negative", which `chart-bar`'s `orientation` prop handles (dv-bar-007). CJ reads "combination chart" as a chart type none of the three is. Both defensible; CJ's is the more conservative. |
| dv-015 on line | no (binds the ROLE, not a component) | **binds** | Open. The rule names "line" explicitly; CJ's point that a chart-CHOICE rule belongs on `role:chart-panel` is the better architectural argument. |
| dv-009 on line · dv-019 on bar/pie | binds | **binds** | agreed after my correction |

---

## 6. Q3 — the other 11 chart components. Flagged only; not authored.

`knowledge/components/` holds **14** chart metas. Three have a spec file of their own. The filename-join
route does not reach the other eleven — after this lane it is exhausted.

Applying the Q1 test mechanically to the three spec files' text (does the component's word appear in a
Types bullet, a heading, or a rule's normative clause?), **exactly two of the eleven pass**:

| meta | named by | why it is obvious |
|---|---|---|
| **chart-donut** | `data-visualisation-pie-charts.md` | Q1 above. The file's `## Types` and `dv-pie-009`'s normative text name the doughnut, and the meta already cites dv-pie-009 and dv-pie-010 by id. |
| **chart-sparkline** | `data-visualisation-line-charts.md` | The line file's `## Types` names "Spark (sparkline)" as its second type, and the file has a whole `## Spark charts` section — the source of the two rules this lane drops from chart-line. |

The other nine — `Chart-boxplot` · `Chart-bullet` · `Chart-butterfly-h` · `Chart-butterfly-v` ·
`Chart-candlestick` · `Chart-histogram` · `Chart-scatter` · `chart-combo` · `chart-stacked-area` — are
named by no spec file's structure. `chart-combo` is the interesting near-miss: no file names "combo", but
its meta cites 8 distinct `dv-` ids about which half of the composite each governs, so it is the first
genuinely cross-file case. **Not authored here. Flagged.**

A caution about the last column of the Q3 table: it counts `dv-` ids each meta ALREADY cites. It is a
measurement, never a proposal — a meta can cite a rule to record that it ESCAPES it.
`Chart-candlestick` cites dv-bar-009 to say its partial computes its own domain because a zero floor
would smear a price series. Lifting cited ids into `obeys` would be `s274-D12` one level up, with a
better alibi.

### The capitalisation split is real, and it is load-bearing

**7 uppercase** (`Chart-boxplot`, `Chart-bullet`, `Chart-butterfly-h`, `Chart-butterfly-v`,
`Chart-candlestick`, `Chart-histogram`, `Chart-scatter`) and **7 lowercase** (`chart-bar`, `chart-combo`,
`chart-donut`, `chart-line`, `chart-pie`, `chart-sparkline`, `chart-stacked-area`).

The meta filename stem is the node id, so the graph carries both `component:Chart-boxplot` and
`component:chart-bar`. It is already referenced across registries — `chart-line.meta.json`'s `yieldsTo`
points at `component:Chart-candlestick` with the capital preserved. **Reported as a probable defect; not
renamed, and no rename proposed in this lane** — a case-only rename on this filesystem needs a two-step
`git mv` plus a reference sweep, and it would arrive as a fifty-file diff under a commit message about
`obeys`, which is the `#179` class of receipt. It wants its own lane.

---

## 7. Scope notes and one disagreement with the brief

**No `ux:` law citations.** Lane TO's authored pass had two halves: `rule:` refs by filename join and
`ux:` grade-A law refs. `s276-D5` scopes this lane to "the same shape: **filename join** on the three
`data-visualisation-*-charts.md` spec files". The laws are not in that sentence, so none are authored
here. Declared, not omitted — bite 9 asserts zero `ux:` refs so this cannot drift silently. If the
conductor reads the ruling as including them, it is a small following pass over the same three metas.

**No schema diff.** `edges.obeys` and `$obeys-contract` already exist in `meta.schema.json`, landed by
`s276-D3` at `577c82d`. Bite 17 asserts the live schema already admits `rule:` and already requires
`$why`, so the absence of a diff is proved rather than assumed.

**The brief said "bake `type.css` into the srcdoc (label crop pattern, #261). I did not, and here is
why.** This page renders **no component specimens**, so it has no `srcdoc` iframe to bake anything into.
Loading `type.css` into a page that consumes none of it is an instrument without a consumer. The thing
the instruction protects — the #261 label crop — is honoured directly in the page's own CSS (`.label`:
no `text-transform`, `line-height: 1.6`) and is **driven**: `_drive_page.py` runs the canvas descender
probe from `knowledge/_validate_demo_page.py` over 25 elements across 8 tight-box selectors, per theme,
and reports worst clip 0.00px. Recorded here as the brief instructs.

---

## 8. Every gate's output line

```
$ python3 notes/_lanes/277/charts/_author_metas.py --selftest
selftest: 20/20 bites green
```

```
$ python3 notes/_lanes/277/charts/_mutate.py
BASELINE red=[] crashed=False — PASS
ALL 16 MUTANTS CAUGHT
```

**A mutant survived, and that is in this report because it is a finding, not a pass.** M9 — "the splice
RE-DUMPS the meta instead of a textual span", the `#179` defect proper — ran **GREEN** against the first
19 bites. Bites 15 and 16 are round-trip invariants: they hold against whatever text `splice()` started
from, so a re-serialised meta satisfies both. Bite 20 was written for it: it re-reads the live file's
bytes independently of `splice()` and demands the proposal be those bytes with one span inserted. M9 now
turns bite 20 red. The memory hook says a green gate will not catch a re-dump; it did not, until a bite
existed that could.

```
$ python3 notes/_lanes/277/charts/_dry_run.py
== 1. SCHEMA — the three proposed metas against meta.schema.json ==
  chart-bar.meta.json    obeys=10  schema errors: 0
  chart-line.meta.json   obeys= 9  schema errors: 0
  chart-pie.meta.json    obeys=10  schema errors: 0
  NEGATIVE CONTROL  $why removed             -> 1 schema errors (RED, good)
  NEGATIVE CONTROL  $why under 40 chars      -> 1 schema errors (RED, good)
  NEGATIVE CONTROL  ref not rule:/ux:        -> 1 schema errors (RED, good)
  NEGATIVE CONTROL  stray key in an entry    -> 1 schema errors (RED, good)
  schema: OK — 0 errors on the proposal, every negative control red

== 2. RESOLUTION — every proposed ref is already a node ==
  _rule_nodes.json nodes: 521  ·  rule: nodes: 470
  proposed refs: 29  ·  unresolved: 0

== 3. DRY RUN — the simulated tree ==
  obeys edges in knowledge/components/ TODAY: 81
  obeys edges this lane proposes:             29
  obeys edges after landing (simulated):      110
  _validate_kg.py against the SIMULATED tree (exit 0):
    _validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta
    has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4
    resolutions input was consumed.

== 4. OWNERSHIP — git status ==
  changed paths: 6  ·  outside notes/_lanes/277/: 4   (all predate this lane, by mtime)

VERDICT: OK
```

The negative controls matter: a schema validator that cannot go red proves nothing. All four `$why`
clauses of `obeysEdge` — REQUIRED, minLength 40, the `^(rule|ux):` ref pattern,
`additionalProperties: false` — were driven to red on a mutated copy.

```
$ python3 knowledge/_validate_kg.py                      # the LIVE tree, untouched
_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has
provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4
resolutions input was consumed.
```

```
$ source knowledge/_render/seat_env.sh && python3 notes/_lanes/277/charts/_drive_page.py
SEAT_ENV: OK seat=quirky-gracious-ptolemy faces=10/404 farm=10/10
  ok    font loaded (HSBC_MtUnivers_Latin)                                      True
  ok    0 console errors / warnings / page errors                               0 bad, 0 page error(s)
  ok    descenders intact on the tight boxes                                    25 elements / 8 selectors · worst clip 0.00px
  ok    no element crops its own content                                        []
  ok    no text-transform:uppercase (nam-002)                                   []
  ok    no ALL-CAPS runs in visible text (nam-002)                              []
  ok    export is the RK shape {page, at, decisions:[{id, choice, note}]}
  ok    localStorage round-trips the choice and the note across a reload
  ok    390px: no horizontal scroll                                             {"s": 390, "c": 390}
  ok    light: accent is the two-red law value, 0 crop, 0 overflow (s151-D1)    rgb(218, 26, 0)
  ok    dark:  accent is the two-red law value, 0 crop, 0 overflow (s151-D1)    rgb(246, 96, 76)
DRIVE PASS
```

Two of those checks were red on the first drive and are worth recording rather than smoothing away. The
export shape failed because the decisions file named the page without its `.html` extension — a real
mismatch with the RK shape, fixed in the input. The nam-002 caps check failed on 27 runs; some were my
own prose emphatics (now `<b>`), some were field values from `_rules-index.json` (now in code voice), and
two classes were neither: the verbatim `s276-D5` blockquote and the authored `$why` sentences in the
table. Those two are excluded in `_drive_page.py` with the reason written into the source — Dave's words
are not this page's naming, and the `$why` sentences are the artefact under review, data on this page
exactly as a file path in `<code>` is. Rewording a ruling to pass a gate would be the tail wagging the
dog.

### Ownership

```
$ git status --porcelain
 M notes/_REHEARSAL-LOG.jsonl
 M notes/_dream/_GRADE-DECISIONS.jsonl
?? artefact
?? notes/_lanes/277/charts/
?? notes/_lanes/277/judgement/BRIEF.md
?? rule?
```

Only `notes/_lanes/277/charts/` is this lane's. The other five are **not mine and were not touched by
me**, and mtime is the evidence rather than my word: `artefact` and `rule?` (two stray zero- and 49-byte
files at the repo root) are stamped **21:33:10**, and this lane's first file was written after that;
`_REHEARSAL-LOG.jsonl` and `_GRADE-DECISIONS.jsonl` were modified at **21:35:2x** by the harness; the
judgement BRIEF is lane CJ's. `_dry_run.py` §4 re-measures this every run and flags anything newer than
this lane's earliest script.

### The eye pass — because a green driver is not a review

`[[art-director-reviews-lane-output-268]]`. I opened `screenshot.png` and read it. Two defects the eleven
green driver checks did not see:

1. **`chart-donut` showed "—" in the Q3 "named by" column.** The test matched on the meta name's first
   word, "donut"; the guidance spells it **doughnut**. A false negative on the single row this whole lane
   turns on. Fixed with a declared `ALIAS` map (donut/doughnut, sparkline/spark) rather than a fuzzy
   match.
2. **Every chart matched `data-visualisation.md`.** dv-015 lists "line, spark, bullet, candlestick" — a
   chart-choice taxonomy — so the family file named all fourteen and the column was noise. The family
   file is now excluded from the test and the caption says so.

After both fixes the column reads exactly two hits, which is the Q3 finding stated cleanly.

---

## 9. What is on disk

| path | what |
|---|---|
| `notes/_lanes/277/charts/_author_metas.py` | the authored tables, the splice, 20 bites, `--table` |
| `notes/_lanes/277/charts/_dry_run.py` | schema + negative controls, resolution, simulated tree, ownership |
| `notes/_lanes/277/charts/_mutate.py` | 16 mutants |
| `notes/_lanes/277/charts/_build_page.py` | bakes the review page; every integer measured at build time |
| `notes/_lanes/277/charts/_drive_page.py` | drives the real page in chromium, 11 checks x 2 themes |
| `notes/_lanes/277/charts/charts-decisions-2026-09-15.json` | the page's copy — no integers in it |
| `notes/_lanes/277/charts/proposed-metas/` | **3 files. NOT landed.** Each a byte-for-byte copy of the live meta plus one inserted span |
| `notes/_lanes/277/charts/dry-run.json` · `dry-run.txt` | the gate receipts |
| `notes/_lanes/277/charts/REVIEW-charts-2026-09-15-v1.html` | the review page, 3 decisions |
| `notes/_lanes/277/charts/screenshot.png` | full-page desktop light, the artefact reviewed by eye |

`knowledge/` is untouched. `git diff --stat knowledge/` is empty.

---

## 10. FILL at close

```
$ python3 knowledge/_checkin.py
MEASURED  176,952 cl100k-estimate  (conversation half, ONE call — the headline)
```

Under the 180,000 stop line (`s271-D1`), with little room. Also raised by the check-in and passed
straight to the conductor: **`/sessions` disk is at 96.4%** (352,956 KB free) — at 100% the sandbox
cannot create its user and no session boots. This lane did not run the scratch-hygiene gate, because
clearing scratch is not inside its brief.

---

## 11. The commit

`--numstat` is the receipt, never the commit message:

```
$ git show --numstat --format='%H %s' HEAD
b4d42ebccdb62fa57781abd7455d899175186e52 #277 2026-09-15 — lane CO: the three charts authored, 29 obeys proposed, 3 drops declared, nothing landed

52	0	notes/_lanes/277/charts/BRIEF.md
460	0	notes/_lanes/277/charts/REPORT.md
433	0	notes/_lanes/277/charts/REVIEW-charts-2026-09-15-v1.html
403	0	notes/_lanes/277/charts/_author_metas.py
616	0	notes/_lanes/277/charts/_build_page.py
234	0	notes/_lanes/277/charts/_drive_page.py
178	0	notes/_lanes/277/charts/_dry_run.py
132	0	notes/_lanes/277/charts/_mutate.py
39	0	notes/_lanes/277/charts/charts-decisions-2026-09-15.json
20	0	notes/_lanes/277/charts/dry-run.json
31	0	notes/_lanes/277/charts/dry-run.txt
238	0	notes/_lanes/277/charts/proposed-metas/chart-bar.meta.json
298	0	notes/_lanes/277/charts/proposed-metas/chart-line.meta.json
227	0	notes/_lanes/277/charts/proposed-metas/chart-pie.meta.json
-	-	notes/_lanes/277/charts/screenshot.png
```

(`REPORT.md` shows 460 lines here because this block was spliced in after the commit; the
amend below is the only change.)
