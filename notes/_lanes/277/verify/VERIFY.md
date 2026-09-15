# LANE CV — VERIFY — grading lane CO (`8c80aa2`), reconciled against lane CJ (`f84eb78`)
#277 · 2026-09-15 · model: opus · **READ-ONLY — nothing landed, nothing fixed, corrections BY ADDITION**

```
GREEN  21      the claim was re-driven and holds
RED     8      the claim is false as written, or the page carries a figure this lane measured otherwise
AMBER   8      true but overstated, non-reproducible, or a defect in the instrument rather than the claim
```

Every figure below was produced by running the command in this lane, in this sandbox, at 22:0x. Not one
number was copied out of `REPORT.md` or `RECOMMEND.md`.

⚠ **Two receipts in this wave describe commits that do not exist.** CO's `REPORT.md` §11 and CJ's
`RECOMMEND.md` § Commit both quote a pre-amend sha and a pre-amend line count. `--numstat` is the
receipt — but only when it is the receipt **of the commit that shipped**. See R-3 and R-8.

---

# PART 1 — grading `notes/_lanes/277/charts/REPORT.md`

## GREEN — 21

**G-1 · the per-file counts 10 / 11 / 11 / 19 and the 470 total.** GREEN, exactly.
```
$ python3 -c "import json,collections; d=json.load(open('knowledge/guidelines/_rules-index.json'));
  c=collections.Counter(r['file'] for r in d['rules']); print(len(d['rules']));
  [print(f,c[f]) for f in (...)]"
470
data-visualisation-bar-charts.md    10
data-visualisation-line-charts.md   11
data-visualisation-pie-charts.md    11
data-visualisation.md               19
```
The id sets are contiguous and complete (`dv-bar-001..010`, `dv-line-001..011`, `dv-pie-001..011`,
`dv-001..019`) — no id is missing and none is duplicated, so the counts are not an artefact of the join.

**G-2 · 32 rules in the three spec files · 29 bind · 3 declared drops.** GREEN. 10+11+11 = 32;
`proposed-metas/` carries 10 + 9 + 10 = 29 `obeys` entries; `DROPPED` carries 3. BIND ∪ DROP = the file,
exactly, for all three (bite 5, re-driven).

**G-3 · 81 live `obeys` · 29 proposed · 110 simulated · 470 `rule:` nodes · 0 unresolved · 0 schema errors.**
GREEN, all six. `python3 notes/_lanes/277/charts/_dry_run.py` re-driven; output matches the committed
`dry-run.txt` on every integer except the ownership block (see A-5).

**G-4 · schema validation of the three proposed metas, including the `$why` requirement.** GREEN, and the
negative controls are the reason this counts. All four go red on a mutated copy: `$why` removed · `$why`
under 40 chars · a `ref` that is neither `rule:` nor `ux:` · a stray key in an entry. A validator that
cannot go red proves nothing; this one can, four ways.

**G-5 · `--selftest` 20/20 bites green.** GREEN, re-driven.

**G-6 · `_mutate.py` — 16 mutants, all 16 caught.** GREEN, re-driven. `BASELINE red=[] crashed=False`.

**G-7 · M9 survived 19 bites; bite 20 catches it. RE-DRIVEN BOTH WAYS.** GREEN — and this is the claim I
was most prepared to fail. A mutation test that is not driven is a claim, so I drove the counterfactual:
```
M9 WITH bite 20    -> FAILS: [20]
M9 WITHOUT bite 20 -> FAILS: []          # bite 20 excised from the source, M9 still applied
```
Bites 15 and 16 are round-trip invariants against whatever text `splice()` started from, so a
re-serialised meta satisfies both. Bite 20 re-reads the live file's bytes independently. CO's finding is
exactly right, and the memory hook it cites is exactly why it is a finding and not a pass.

**G-8 · `_validate_kg.py` OK on the live tree.** GREEN. 139 metas checked, 90 declared `ref:null` + note,
s135-D4 resolutions consumed, `gen_kg_edges.py` idempotent-clean. Run at the start and again at the end
of this lane; identical.

**G-9 · the three declared drops are correct and correctly declared.** GREEN, all three, verified against
the source files rather than the index:
- `dv-line-009` and `dv-line-010` sit under `data-visualisation-line-charts.md`'s own `## Spark charts`
  heading. `chart-sparkline.meta.json` is a separate live meta and **already cites `dv-line-009` twice in
  its own prose** (`"wide aspect 6.4:1"`, antiPattern `"A tall/square spark (dv-line-009)"`). The rule is
  the spark's.
- `dv-pie-003` is `"Doughnut centre: total value + descriptor together"`. `chart-pie.meta.json`'s
  `purpose` says verbatim: *"the DV-D13 centre-total wiring removed (donut-only, per brief)"*, and its
  antiPatterns carry *"Porting the donut's centre-total / DV-D13 selection-follow wiring across
  (donut-only, explicitly fenced by the brief)"*. A pie with no centre has no centre contract.
Each drop carries a reason over 60 chars (bite 6) and BIND ∪ DROP partitions the file (bite 5).

**G-10 · finding (i): `_rules-index.json`'s `dv-019` row carries `dv-017`'s sentence. CONFIRMED, verbatim.**
The index's `dv-019.rule` field reads *"Only palette colours in charts … the unified supporting palette.
[BLOCKING-derivable — the compose gate's 0-rogue-hex, applied to chart fills] **{#dv-017}** ⚠ SCOPED
OVERRIDE …"* — it literally ends in the **other rule's id tag**. The source,
`knowledge/guidelines/data-visualisation.md` lines 66–70, shows `dv-019` is its own rule: *"NEW
APOLLO-ADDED RULE — avoid vibrating boundaries … fail-candidate when pair value-ratio <1.25 AND hue-sep
≥135° AND both HSL sats ≥0.5"*, tagged `{#dv-019}`. CO's diagnosis of the cause (the indexer takes the
whole bullet from the leading `-` to the closing `{#…}`) is consistent with what is on disk. Reported and
not fixed is the right call — `gen_rules_index.py` is the generator and this is not CO's file.
⚠ **The blast radius is wider than CO says.** `dv-019` also has a node in `knowledge/_rule_nodes.json`
and a row in `knowledge/_consult-index.json`, both generated from the index, so the wrong sentence is in
the graph and in the consult surface today, not only in the index.

**G-11 · finding (ii): the two driver reds (export shape, nam-002 caps).** GREEN on both. The export-shape
fix is in `charts-decisions-2026-09-15.json` (the page name now carries `.html`) and the driver asserts
the RK shape `{page, at, decisions:[{id, choice, note}]}` — re-driven, passes. The two nam-002 exclusions
are **declared in `_drive_page.py`'s own source with the reason written next to them** (line 21: *"a file
path in code voice is not a name in caps"*; line 96: the `$why` sentences and drop reasons are the
artefact under review). Excluding with the reason in the source is the honest form; rewording a ruling to
pass a gate would not be.

**G-12 · §7, the `type.css` / #261 disagreement — CO is RIGHT on the substance.** GREEN, driven, not read.
- The page has **0 `srcdoc`, 0 `<iframe>`, 0 references to `type.css`**. There is genuinely nothing to
  bake into. Baking it would be an instrument with no consumer.
- The thing #261 protects **is** enforced, and I drove it myself rather than trusting the report:
  computed `font-family` on `body` resolves to `"Univers Next for HSBC"` and the driver's font-load
  assertion returns `True` — so the descender probe runs against the **real** face, not a fallback, which
  is the only way the check is non-vacuous.
- The probe is non-empty: **25 elements across 8 tight-box selectors, per theme, worst clip 0.00px**, plus
  `no element crops its own content: []` in light and dark.
- The one `text-transform` string in the file is prose (`"text-transform (nam-002): tracking and weight"`),
  not a CSS declaration.
The brief's instruction was written for a page with specimens. This page has none, the protected property
is driven directly in both themes, and the deviation is declared. That is the right disagreement, made
the right way.

**G-13 · the 29 `$why` sentences are authored, not restatements.** GREEN — **zero outright restatements**,
with two AMBER noted at A-6. This is the half no gate can see, so I read all 29 against the rule text and
then checked every mechanism they name against the live meta.

*The mechanism audit* — each `$why` names a concrete thing in the meta; I grepped for all of them:
| named in a `$why` | found in | verdict |
|---|---|---|
| `series` prop, markers `r4.2` / `8.4` / `±4.9` | chart-line | ✓ |
| `dvTip` popover, `motion.hover` | chart-line, chart-pie | ✓ |
| `legendFilter` prop | chart-line | ✓ |
| `viewBox` pinned 1:1 | chart-line | ✓ |
| `labelling` = spider default · `direct labels` variant | chart-pie | ✓ |
| `valueMode` prop | chart-pie | ✓ |
| `data-total`, no centre figure | chart-pie | ✓ |
| `.dv-barkey`, `orientation` prop, `data-domain-min="0"` | chart-bar | ✓ |
| `DV-D07` (`data/axis`, `data/grid`), `DV-D02`, `span.cols` 4–12 | chart-line, chart-bar | ✓ |
Not one sentence names a mechanism that is not there — with the single exception at A-6.

A textual-similarity sweep (`difflib`, rule text vs `$why`) puts the highest overlap at **0.63**
(`dv-pie-001`) and everything else at or below 0.53. Every sentence opens with a compressed paraphrase of
the rule and then turns to a reason. That shape is legitimate — the paraphrase is the lead-in, the reason
is the sentence. `dv-bar-008` is the model of it: it states plainly that the meta declares **no** projected
variant and that the rule is a constraint on any future one. A restatement could not say that.

**G-14 · `s276-D5`'s text, quoted on the page, is verbatim.** GREEN. Checked against
`knowledge/_rulings.json` character for character, including *"Then STOP and look again."*

**G-15 · the precedent figure — `icon-button` cites 6 of the buttons spec's 14.** GREEN (both lanes assert
it; both are right).

**G-16 · `chart-donut.meta.json` already cites `dv-pie-009` and `dv-pie-010` by id.** GREEN. Both appear in
its antiPatterns (*"More than 6 slices (dv-pie-009 — combine into 'Other')"*, *"Segment values that don't
sum to the centre total (dv-pie-010)"*) and `dv-pie-009`/`-010` are both named in its `slices` prop.

**G-17 · no family edge between `chart-pie` and `chart-donut`; 12 metas carry one.** GREEN — see R-2 for
the denominator.

**G-18 · `chart-pie.edges.yieldsTo → component:chart-donut` and `not-with` naming chart-donut.** GREEN,
both present verbatim.

**G-19 · `role:chart-panel` has 12 providers and `Chart-bullet` is not one.** GREEN. `roles.json` lists 12
providers; `Chart-bullet` and `chart-sparkline` are both absent. Option (c)'s "wrong membership" argument
is correct on the file.

**G-20 · `common-toolkit-foundations.md` holds 4 above-the-component rules, 0 attached to any meta.**
GREEN. There is no precedent for Q2, only one to set — as both lanes say.

**G-21 · the capitalisation split is 7 up / 7 down and the slug is the node id.** GREEN.
`Chart-boxplot · Chart-bullet · Chart-butterfly-h · Chart-butterfly-v · Chart-candlestick ·
Chart-histogram · Chart-scatter` against `chart-bar · chart-combo · chart-donut · chart-line · chart-pie ·
chart-sparkline · chart-stacked-area`. CJ's sharper claim — that `df44e51` created **both cases in one
commit** — is also GREEN, and the `--numstat` is unambiguous:
```
$ git show --numstat df44e51 | grep meta.json
63  0  knowledge/components/Chart-boxplot.meta.json
67  0  knowledge/components/Chart-bullet.meta.json
64  0  knowledge/components/Chart-butterfly-h.meta.json
64  0  knowledge/components/Chart-butterfly-v.meta.json
64  0  knowledge/components/Chart-candlestick.meta.json
65  0  knowledge/components/Chart-histogram.meta.json
72  0  knowledge/components/chart-pie.meta.json          <- lowercase, same commit
72  0  knowledge/components/chart-stacked-area.meta.json <- lowercase, same commit
```
One wave, both cases. It is a habit, not a signal. Both lanes are right to refuse to rename it here.

---

## RED — 8

**R-1 · REPORT §5: "(a) attach all 19 to each = 57 — **11 of the 57 would be false**." FALSE against CO's
own matrix.** The matrix in `_author_metas.py`'s `FAMILY` gives 49 binding cells of 57. 57 − 49 = **8**.
Eleven is **CJ's** number (57 − 46 = 11). CO's report has imported the other lane's arithmetic into a
sentence about its own.
```
$ python3 -c "import importlib.util,sys; ... ; F=m.FAMILY
  print(sum(1 for r in F for c in F[r] if not F[r][c][0]))"
8
```
The review page, which computes this at build time, gets it right and prints **8**. So the defect is in
the prose of `REPORT.md` §5 only — and it is the number a reader of the report would carry into D-3.

**R-2 · REPORT §4: "12 of **139** metas carry a family edge." FALSE. The measured denominator is 137.**
```
$ ls knowledge/components/*.meta.json | wc -l          -> 138   (includes EXAMPLE-button.meta.json)
$ <excluding EXAMPLE* and meta.schema>                  -> 137 metas, 12 with a family edge
$ python3 knowledge/_validate_kg.py | grep checked      -> metas checked: 139
```
139 is the **gate's** denominator — it adds `knowledge/_proforma/icon-button.meta.json` and counts the
EXAMPLE file. Neither belongs in "metas that could carry a family edge". The review page prints **12 of
137**, which is correct. Again the page is right and the report is wrong, which is the wrong way round
for a document the conductor will read first.

**R-3 · REPORT §11: the commit receipt describes a commit that does not exist.** The report quotes
`b4d42ebccdb62fa57781abd7455d899175186e52` and `460 REPORT.md`. The commit that shipped is:
```
$ git show --numstat --format='%H %s' 8c80aa2 | head -3
8c80aa2...  #277 2026-09-15 — lane CO: the three charts authored, 29 obeys proposed, 3 drops declared, …
52   0  notes/_lanes/277/charts/BRIEF.md
482  0  notes/_lanes/277/charts/REPORT.md
```
Sha and line count both wrong. The report's own parenthetical acknowledges the splice but then leaves the
stale sha standing. `--numstat` is the receipt precisely because a message can drift; a `--numstat` of a
superseded object drifts the same way.

**R-4 · THE PAGE: decision card D-3 carries two mutually contradictory arithmetics, and the second is
unattributed.** This is the #268 failure and it is visible in a single screenshot
(`notes/_lanes/277/verify/verify-decisions-dark.png`). Inside one card, top to bottom:
```
card prose : "Reading all 19 against all three by eye gives 49 that bind, not 57: 18 on bar, 16 on line, 15 on pie."
option (a) : "57 edges. Simple, and  8  of them would be false …"
option (b) : "… 49 edges … dv-013 and dv-015 land on AT MOST ONE, and the 13 that bind all three …"
footer     : "… about 46 entries, not 57, with dv-013 and dv-015 on NONE of the three … because 11 of the 57
              blanket edges would be false and the 30 that repeat identically …"
```
**49 / 8 / 13** against **46 / 11 / 30**, four inches apart, with nothing on the page saying the footer
paragraph belongs to a different lane. The only attribution is the word "(lane CJ)" in the Receipts block
roughly 1,900px further down. A reader choosing (b) cannot tell whether they are choosing 49 edges or 46.
**No decision card may contain two answers to its own question.**

**R-5 · THE PAGE: D-3 option (b) says `dv-013` and `dv-015` "land on at most one"; the footer says "on none
of the three".** The same defect as R-4, but this one is a flat contradiction of fact rather than of
count, and it is the exact cell the conductor has to resolve. Measured truth is at M-3 below: CO binds
`dv-013` to bar and `dv-015` to line; CJ binds neither anywhere.

**R-6 · THE PAGE: the recommendation is not first.** Per-decision it is (each card carries a `Recommended`
chip, and the page says so in its own words). Page-level it is buried:
```
page height                         9,558 px
first decision card (D-1) top       6,081 px   = 64% down
D-3 top                             7,632 px   = 80% down
```
Dave reads two full-width rule tables — 32 rows of Part A plus 11 rows of Part B — before the first thing
he is asked to decide. `[[decide-fast-dave-is-the-bottleneck-254]]` is explicit: lead with the
recommendation and the one item with weight; context goes behind. The material is good; the order is
inverted.

**R-7 · `_dry_run.py` writes into the lane it audits.** Running the gate rewrites
`notes/_lanes/277/charts/dry-run.json` and `dry-run.txt`, so a second seat re-driving CO's receipt dirties
CO's committed files. It did here; I restored both with
`git restore --source=HEAD --worktree -- <the two paths>` and `git status` is clean of them. A receipt
that mutates when you check it is not a receipt. (Filed against the instrument, not the finding — the
figures it printed were correct.)

**R-8 · CJ's receipt is stale in the same class as CO's.** `RECOMMEND.md` § Commit quotes `edb5f09` and
`148 0 RECOMMEND.md`. The commit that shipped is `f84eb78` with `154 0`. Both lanes amended and neither
re-read its own receipt afterwards. This is now a wave-level pattern, not a lane slip.

---

## AMBER — 8

**A-1 · REPORT §8 quotes `changed paths: 6`; the committed `dry-run.txt` says `changed paths: 7`.** The
report's pasted gate block does not match the receipt file committed beside it in the same commit.
Neither is dishonest — the tree moved between the two runs — but the report presents the block as *the*
output.

**A-2 · REPORT ownership: "all predate this lane, by mtime" is no longer reproducible.** Re-driven, the
lane's own §4 now prints the opposite for two of the four:
```
OUTSIDE notes/_REHEARSAL-LOG.jsonl           mtime 21:50:02  *** NEWER THAN THIS LANE — INVESTIGATE ***
OUTSIDE notes/_dream/_GRADE-DECISIONS.jsonl  mtime 21:50:03  *** NEWER THAN THIS LANE — INVESTIGATE ***
```
Both are harness-written files that move on their own; the claim was true when made and is false now. An
ownership assertion pinned to a wall-clock mtime decays. The two are still not CO's, and not mine.

**A-3 · the stray files are unchanged — confirmed, not swept.**
```
artefact   0 B   mtime 21:33:10   md5 d41d8cd98f00b204e9800998ecf8427e  (the empty-file hash)
rule?     49 B   mtime 21:33:10   md5 4919f39261aedefd24f9e5129c87681d
```
Both still untracked. Neither opened, moved, nor deleted by this lane.

**A-4 · the selftest's counter is hardcoded and cannot report a missing bite.** `print("selftest: %d/%d
bites green" % (20 - len(fails), 20))`. When I excised bite 20 for the M9 counterfactual, the run still
printed `selftest: 20/20 bites green` — with 19 bites. A bite can be deleted and the headline stays
green. Nothing in this lane exploits it; it is the class of defect the lane's own bite 20 exists to catch,
one level up.

**A-5 · `_dry_run.py` §4 flags but does not fail.** `VERDICT: OK` prints even with two `*** INVESTIGATE
***` lines above it. An advisory arm is fine; it should say it is advisory.

**A-6 · two `$why` sentences out of 29 are weaker than the other 27.** Neither is a restatement; both are
correctable in one edit each.
- `dv-pie-001` — *"…the segments this meta bakes as `data-a1`/`-a2` at generation time."* The attributes
  are real but they live in `knowledge/snippets/Chart-donut.reference.html` (9 × `data-a1`, 7 × `data-a2`),
  **not in `chart-pie.meta.json`**, which contains neither string. The meta's `motion.entry` says
  *"segments bake the sweep contract (data-cx/-cy/-ro/-a1/-a2, NO data-ri)"* — so the claim is defensible
  via the motion block but as written it points at the wrong file. Highest similarity to its rule text of
  all 29 (0.63).
- `dv-bar-002` — *"…and the meta's axis tokens have to carry either way."* Every other sentence names a
  prop, a token role, a variant or an antiPattern by name; this one gestures. It is the only one of the 29
  that a reader could not check against the meta in one grep.

**A-7 · CJ's sparkline figure "≈ 4 entries" mixes measurement with judgement.** `chart-sparkline.meta.json`
cites exactly two line-file rules (`dv-line-009` ×2, `dv-line-011`). The other two in CJ's four
(`dv-line-001`, `dv-line-010`) are CJ's own judgement, correctly argued but not measured. Stated as one
figure, it reads as four measured citations.

**A-8 · the combined cost of D-1 + D-3 appears nowhere.** If Dave takes D-1(a) and D-3(b), the wave lands
29 + 47 = **76** `obeys` edges (using the reconciled 47 from §3; 78 on CO's 49, 75 on CJ's 46), taking the
corpus from 81 to **157**. Neither report nor page states that number, and the page's headline stat says
**110** — which is D-1 alone. The single largest figure in the decision is not on the decision page.

---

# PART 2 — CO vs CJ, reconciled by measurement

| # | claim | CO | CJ | MEASURED (this lane) | who is right |
|---|---|---|---|---|---|
| 1 | **scope** — how many components this wave | 3 (the ruling's three) | 3 + `chart-donut` + `chart-sparkline` + `chart-combo`, **"in the same wave"** | `s276-D5`: *"ARE AUTHORED IN THE NEXT LANE … **Then STOP and look again.**"* Dave's own ask, quoted in the ruling's `says`: *"yes, and maybe flag any extra you think are applicable"* | **CO on scope; CJ on analysis.** See §1 below — it is a judgement, and the word that crosses the line is "wave". |
| 2 | **pie/donut polarity** — is the pie derived from the donut | says so in §4, does not act on it | makes it the argument: the spec is a circular-charts spec filed under "pie" | `chart-pie.purpose`: *"ported from Chart-donut.reference.html … inner radius dropped to 0 … DV-D13 centre-total wiring removed (donut-only, per brief)"*; `provenance.code_path` = `knowledge/snippets/Chart-donut.reference.html`; `provenance.source` = `"code"`. `chart-donut.provenance.source` = `"proforma-promotion"`. **Both lanes' provenance claim is exactly right.** | **Both right on the fact. CJ right that it changes the question.** |
| 3 | **family arithmetic** | **49** — bar 18 · line 16 · pie 15 | **46** — bar 17 · line 15 · pie 14 | **Both are internally correct.** Neither is an arithmetic error. The matrices differ in **exactly three cells**, and 49 − 3 = 46. | **Neither. It is three judgement calls, not a sum.** See §3. |
| 4 | **`dv-013` / `dv-015`** | `dv-013` binds bar; `dv-015` binds line | both bind none of the three | `dv-013` = judgement (see §4a). **`dv-015`: CJ is right, and CO's own §8 is the proof** (§4b). | **CJ on `dv-015`. Dave on `dv-013`.** |
| 5 | **`≤ 5 parts` vs `max 6`** | not raised | raised as a conflict in `roles.json` / `chart-pie.when` vs `dv-pie-009` | **CONFIRMED, and wider than CJ states** — see §5 for every file. | **CJ, understated.** |
| 6 | **capitalisation blast radius** | "a fifty-file diff", not measured | "29–50 non-generated files per component" | **111–156 tracked files per component; 278 in the union.** `knowledge/` alone: 27–42 per component, 78 in the union. | **CJ's figure is the `knowledge/`-only count, stated without that qualifier. True radius is 3–5× larger.** |

### §1 — is CJ's Q3 a widening of the ruling, or the "look again" it asked for?

**Plainly: the analysis is the "look again"; the word "in the same wave" is a widening.**

`s276-D5` reads *"ARE AUTHORED IN THE NEXT LANE … **Then STOP and look again.**"* The stop sits **after** the
three and **before** anything else. Authoring a fourth, fifth or sixth component in this wave steps over
the stop. But the ruling's `says` field records Dave's actual ask verbatim — *"yes, and maybe flag any
extra you think are applicable"* — so **flagging** extras is not merely permitted, it is the thing he
asked for. CJ did the flagging Dave asked for and then attached a verb Dave did not rule.

There is a second, sharper distinction the page does not draw. The three candidates are not alike:
- **`chart-donut` is already inside the ruling.** `s276-D5` says in its own words that the next lane *"must
  also take one word on whether `chart-donut` shares the pie file"*. Authoring it is one word away, not a
  widening. **It is D-2, and D-2 already exists on the page.**
- **`chart-sparkline` is reachable by the same test as the donut** — `data-visualisation-line-charts.md`'s
  `## Types` names *"Spark (sparkline)"* and the file has a whole `## Spark charts` section. CJ's
  consistency argument holds: accepting the donut on "the file's structure names it" and refusing the
  spark on the same evidence is incoherent. But it is a **new** question the ruling did not pose.
- **`chart-combo` is a different tier entirely.** No file names "combo". Its four entries are *cross-file*
  citations, and `s276-D5` scopes this lane to *"filename join"*. Admitting combo is not a scope change,
  it is a **tier** change — the thing the ruling's last sentence refuses by name.

**The count, either way, so Dave can decide with a number in front of him:**

| scope | new `obeys` this wave | authority |
|---|---|---|
| the three, as ruled (D-1) | **29** | `s276-D5`, already ruled |
| + `chart-donut`, 11 (D-2a) | **40** | `s276-D5` invites the question; one word |
| + `chart-sparkline`, 2 measured / 4 judged | **42–44** | NEW — same test as the donut, not in the ruling |
| + `chart-combo`, 4 cross-file | **46–48** | NEW **and** a tier change — refused by the ruling's last sentence unless Dave lifts it |
| + the family subset (D-3b) | **+49 or +46** on top of any row above | D-3, already on the page |

### §2 — the pie/donut polarity, verified against the files and git

Every element of the provenance claim is on disk, verbatim, and it is the strongest single finding of
either lane:

```
chart-pie.meta.json  purpose         "…ported from Chart-donut.reference.html (wave-2 lane ③, 2026-08-05)
                                      with the inner radius dropped to 0 and the DV-D13 centre-total
                                      wiring removed (donut-only, per brief)."
chart-pie.meta.json  provenance      {"source": "code",
                                      "code_path": "knowledge/snippets/Chart-donut.reference.html"}
chart-donut.meta.json provenance     {"source": "proforma-promotion",
                                      "code_path": "knowledge/_proforma/DataViz-interactive.html"}
chart-pie.meta.json  behaviour.$note "THERE IS NO dv-render-pie: dv-render-donut registers BOTH `donut`
                                      and `pie` off one ring(ctx, hole) routine (a pie is that ring with
                                      ri = 0), so Chart-pie COMPOSES the donut partial…"
git log --diff-filter=A chart-pie.meta.json  ->  df44e51 (2026-08-05), the wave-2 commit
```
The pie is the derived component at the meta, the snippet **and** the render partial. CJ's reading is
therefore correct: *"does the donut share the pie spec"* has the polarity backwards; the file is a
circular-charts spec that happens to be filed under "pie".

**The consequence CO leaves open, and the page does not name.** CO drops `dv-pie-003` from `chart-pie` and
proposes nothing for `chart-donut`. If D-2 is not taken in the same breath, **`dv-pie-003` ends the wave
governing nothing** — a BLOCKING-adjacent rule with no component attached, which is exactly the visible
zero both lanes say they want to avoid creating by accident. D-2's card should say that choosing (b)
strands a rule.

### §3 — the family arithmetic, with the working

I rebuilt CO's matrix from `_author_metas.py`'s `FAMILY` dict and transcribed CJ's table from
`RECOMMEND.md`, then diffed them cell by cell. Both totals are arithmetically correct against their own
matrix. **Neither lane made a counting error.** The brief's suspicion — that CO's per-component figures
exceed the 19 family rules — does not hold: 18, 16 and 15 are all ≤ 19, and these are family-rule counts
only, entirely separate from the 29 filename-join edges.

```
rule       CO(bar line pie)   CJ(bar line pie)
dv-001     Y Y .              Y Y .
dv-002     Y Y .              Y Y .
dv-003     Y Y Y              Y Y Y
dv-004     Y . Y              Y . Y
dv-005     Y Y Y              Y Y Y
dv-006     Y Y Y              Y Y Y
dv-007     Y Y Y              Y Y Y
dv-008     Y Y Y              Y Y .     <<< DIFFER
dv-009     Y Y Y              Y Y Y
dv-010     Y Y Y              Y Y Y
dv-011     Y Y Y              Y Y Y
dv-012     Y Y Y              Y Y Y
dv-013     Y . .              . . .     <<< DIFFER
dv-014     Y Y Y              Y Y Y
dv-015     . Y .              . . .     <<< DIFFER
dv-016     Y Y Y              Y Y Y
dv-017     Y Y Y              Y Y Y
dv-018     Y Y Y              Y Y Y
dv-019     Y . Y              Y . Y

CO  bar 18 · line 16 · pie 15  = 49
CJ  bar 17 · line 15 · pie 14  = 46
```

**16 of the 19 rules are agreed, unanimously, across two independent seats.** The gap is three cells. That
is the true shape of this disagreement and it is the sentence the page should carry instead of two rival
totals.

**Cell 1 — `dv-008` (horizontal scroll) on `chart-pie`. CO IS RIGHT; CJ IS WRONG ON THE FILE.**
CJ's reason is *"a pie never scrolls"*. The meta says otherwise, verbatim:
```
chart-pie.meta.json  responsive.rule:
  "Same DV-D02 exclusion as the donut — fixed geometry (compressing a circle distorts);
   .dv-stage scrolls if the container is narrower."
```
`chart-donut` carries the identical clause. A pie has fixed geometry precisely **because** it cannot
compress, which is what makes the container scroll — so `dv-008` binds harder here, not less. **Measured:
+1 to pie. This one is settled, not a judgement.**

**Cell 2 — `dv-013` (combination charts) on `chart-bar`. JUDGEMENT — Dave's.**
Rule text: *"Combination charts (e.g. positive/negative): colour differentiates the data sets."* CO reads
the parenthetical as the rule's own example and points at `chart-bar`'s `orientation` prop. CJ reads
"combination chart" as a chart type none of the three is, and refuses the name-match. Both defensible.
⚠ **But CO's stated reason is the weaker of the two available to it.** `orientation`/positive-negative is
about sign, not about differentiating data sets. The stronger reason — which CO does not give — is that
`chart-bar` declares `grouped-column` and `stacked-column` multi-series variants where colour genuinely
*does* differentiate the sets, and its `series` prop mints `data/series/1–5` for exactly that. If Dave
takes CO's side here, **the `$why` must be rewritten to cite the grouped/stacked variants, not
`orientation`.**

**Cell 3 — `dv-015` (choose line/spark/bullet/candlestick) on `chart-line`. CJ IS RIGHT — and CO's own
report proves it.**
- CJ's architectural claim is verified on the file. `roles.json`'s `chart-panel` providers **are** the
  enactment of `dv-015`: `chart-line` `when: "change-over-time"`, `Chart-candlestick` `when: "OHLC per
  period"`, `Chart-histogram` `when: "distribution, one variable"`, and nine more. The rule is a routing
  predicate and `roles.json` already routes.
- `dv-015` is graded **TASTE** in the index — the only one of the three disputed cells that is.
- **The decisive point is CO's own §8 eye-pass finding (2).** CO excluded `data-visualisation.md` from the
  Q3 "named by a spec file" test with this reason: *"dv-015 lists 'line, spark, bullet, candlestick' — a
  chart-choice taxonomy — so the family file named all fourteen and the column was noise."* CO ruled that
  a component appearing in `dv-015`'s list is **noise** when the column was Q3's, then let the same
  appearance count as a **binding** when the column was Q2's. One test, two answers, in one report.
  **Measured: −1 from line. `dv-015` binds the role.**

**Reconciled total, applying measurement where measurement decides and leaving judgement to Dave:**
```
CO 49  −1 (dv-015 off line, CJ right)  = 48 , with dv-013-on-bar still Dave's
       if Dave also refuses dv-013 on bar        = 47
CJ 46  +1 (dv-008 on pie, CO right)              = 47
```
**The two lanes converge on 47 once the two settled cells are applied.** 47 = bar 18/17 · line 15 · pie 15.
The page must carry one number, and the honest one is **47, with `dv-013`-on-bar flagged as the single
open cell (47 or 48)**. It must not carry 49 and 46 side by side.

### §4a/§4b — see cells 2 and 3 above.

### §5 — the `≤ 5 parts` vs `max 6` conflict: CONFIRMED, and it is in more files than CJ names

The conflict is real and it is **inside a single meta**, which is worse than CJ's framing of it as a
registry-vs-spec mismatch.

**Files carrying "≤ 5 parts":**
| file | where |
|---|---|
| `knowledge/roles.json` | line 104 — `chart-pie` provider `when: "composition, no centre figure, ≤ 5 parts"` |
| `knowledge/components/chart-pie.meta.json` | line 16 — `when: "answers=composition AND parts ≤ 5 AND total=not printed"` |
| `knowledge/components/chart-donut.meta.json` | line 16 — quotes chart-pie's `when` verbatim in its own routing prose |
| `knowledge/components/chart-bar.meta.json` | line 16 — quotes it again, same string |
| `knowledge/_memento-index.json` | derived (three entries) |

**Files carrying "maximum 6":**
| file | where |
|---|---|
| `knowledge/guidelines/data-visualisation-pie-charts.md` | `dv-pie-009`, **BLOCKING** — *"Maximum 6 slices — both pie and doughnut"* |
| `knowledge/guidelines/_rules-index.json` | the `dv-pie-009` row |
| `knowledge/_rule_nodes.json` | `rule:dv-pie-009` |
| `knowledge/components/chart-pie.meta.json` | `slices` prop *"Maximum 6 (dv-pie-009)"* **and** antiPattern *"More than 6 slices"* |
| `knowledge/components/chart-donut.meta.json` | `slices` prop **and** antiPattern, same two |
| `knowledge/_validate_dataviz.py` | **a gate carries the 6** |
| `knowledge/_consult-index.json`, `knowledge/_XREF-INDEX.json`, `knowledge/_instrument-fit.json`, `knowledge/tokens/_manifests/sutherland-fixtures.json`, `knowledge/_proforma/_DATAVIZ-METHOD.md` | derived / ancillary |

⚠ **`chart-pie.meta.json` carries both numbers, eight lines apart** — `when: parts ≤ 5` at line 16 and
`slices: "Maximum 6 (dv-pie-009)"` in its props. So does `chart-donut.meta.json`. And
`chart-donut.tokenValidation` records *"5 slices"* as the validated figure. There is **no source for the 5
in any ingested guideline file** — CJ's point, confirmed: it appears first as a routing preference and
then propagates by copy-paste through three metas and `roles.json`.

**Not resolved here. It is ruling-shaped and Dave's.** Flagging only that a `$why` written against
`dv-pie-009` will have to state which number the component obeys, so the decision cannot be deferred past
D-1 in practice.

### §6 — capitalisation blast radius, measured

```
$ for s in Chart-boxplot … Chart-scatter; do git grep -l "$s" | wc -l; done
Chart-boxplot      158 tracked   (156 excluding the known generated indexes)
Chart-bullet       144           (141)
Chart-butterfly-h  129           (127)
Chart-butterfly-v  113           (111)
Chart-candlestick  128           (125)
Chart-histogram    134           (132)
Chart-scatter      155           (152)

union of all seven, tracked            278 files
union of all seven, knowledge/ only     78 files
per component, knowledge/ only       27–42 files
```
CJ's **"29–50 non-generated files per component"** is the `knowledge/`-only figure and is accurate **for
that subtree** — but it is stated without the qualifier, and the true repo-wide radius is 111–156 per
component, 278 files in the union. CO's unmeasured "fifty-file diff" is low by the same factor.
**Both lanes' conclusion survives the correction and gets stronger: this is its own lane, with a two-step
`git mv` on a case-insensitive filesystem and a 278-file reference sweep. Do not do it here.**

---

# PART 3 — the page, by eye

**Screenshots (the two the brief asks for):**
- light, full page, 1280 px — `notes/_lanes/277/verify/verify-light-1280.png`
- dark, full page, 1280 px — `notes/_lanes/277/verify/verify-dark-1280.png`

Also written, because the defect is only legible up close and at width:
- `notes/_lanes/277/verify/verify-decisions-dark.png` — the D-3 card, where R-4 and R-5 are visible in one frame
- `notes/_lanes/277/verify/verify-decisions-light.png`
- `notes/_lanes/277/verify/verify-390-light.png` · `verify-390-dark.png`

**What is right, driven not read.** Both themes render (light `rgb(255,255,255)`, dark `rgb(17,17,17)`).
The accent is the two-red law value in both — `rgb(218,26,0)` light, `rgb(246,96,76)` dark (`s151-D1`).
`Univers Next for HSBC` resolves on `body`, so the type is the real face. Worst descender clip 0.00px
across 25 elements and 8 selectors, per theme. At 390 px I measured the document myself in both themes:
`scrollWidth 390 = clientWidth 390`, and **zero** elements overflow their box outside a declared
`overflow-x` container. Nothing is clipped at 390. Typography, grid and rhythm are good Swiss work and the
prose is genuinely well written — the Part A table's authored sentences read as reasons, which is the
whole point of the lane.

**Is the recommendation first?** Per decision, yes — a `Recommended` chip on D-1(a), D-2(a), D-3(b).
Page-level, no: **R-6**, the first decision sits 64% down a 9,558px page.

**Are the options genuinely exclusive?**
- **D-2** — yes. (a) yes / (b) no. Clean.
- **D-3** — yes. 57 / 49 / 19-once are three different shapes.
- **D-1 — no.** (a) is *"land all 29 as proposed"*; (b) is *"review per component first … then land what
  survives"*. (b) is not an alternative to (a), it is (a) with a gate in front. A reader who wants to read
  the sentences before landing has to pick (b) even if he agrees with every one of them, and a reader who
  picks (a) is being asked to land 29 authored sentences he has not read. **AMBER — D-1 is really "land
  now" vs "land after review", and should say so.**

**Does any decision card contain a figure this lane found to be wrong?** **Yes — D-3, twice.** R-4 (49/8/13
against 46/11/30 in one card, the second set unattributed) and R-5 (`dv-013`/`dv-015` "at most one" against
"none of the three"). Measured truth is 47, per §3. **D-3 cannot go to Dave as it stands.**

**The #268 verdict.** The page passes its driver — 11 checks × 2 themes, all green, and I re-drove every
one of them. It then **fails on sight**, in the one place that matters: the card carrying the biggest
number on the page says two different things about it. A green driver is not a review; this is the
demonstration.

---

# What the conductor must change before Dave sees this page

1. **Delete the unattributed CJ paragraph from under D-2 and D-3, or label it.** As it stands it reads as
   the card's own conclusion and contradicts the options above it. (R-4)
2. **Rebuild D-3 on one number: 47.** `dv-008` binds pie (CO right, on `chart-pie.responsive.rule`);
   `dv-015` does not bind line (CJ right, and CO's own §8 says so). Show 47 with `dv-013`-on-bar named as
   the single open cell (47 or 48), and say "two independent lanes agreed on 16 of 19 rules" — that is the
   sentence that earns Dave's trust, not a total. (R-4, R-5, §3)
3. **Fix D-3's derived figures to match:** option (a) "8 of them would be false" → recompute against 47;
   option (b) "the 13 that bind all three" → recompute; card prose "49 that bind, not 57" → 47. (R-1)
4. **Move the three decision cards above Part A and Part B.** Decisions first, tables behind. Today the
   first decision is 6,081 px down a 9,558 px page. (R-6, `[[decide-fast-dave-is-the-bottleneck-254]]`)
5. **Reword D-1 so the options are exclusive** — "land all 29 now" vs "land after a per-component read" —
   and say which sentences he would be landing unread under (a). (PART 3)
6. **Add to D-2 that choosing (b) strands `dv-pie-003`.** CO drops it from the pie and nothing else takes
   it; if the donut is not authored, a rule ends the wave governing no component. (§2)
7. **Surface the `≤ 5 parts` vs `max 6` conflict on the page as its own line.** It is BLOCKING-rule vs
   routing-predicate, it sits inside `chart-pie.meta.json` itself, and a `$why` written against
   `dv-pie-009` has to pick a number. Do not resolve it — put it in front of him. (§5)
8. **State the combined cost once, in the hero.** D-1(a) + D-3(b) = 29 + 47 = **76** edges, 81 → 157. The
   headline stat currently says 110, which is D-1 alone. (A-8)
9. **Correct `REPORT.md` §5 (11 → 8) and §4 (139 → 137) before either figure is quoted forward.** The page
   has both right; the report a conductor reads first has both wrong. (R-1, R-2)
10. **Re-cut both lanes' commit receipts against the shipped shas** — CO §11 (`b4d42eb`/460 → `8c80aa2`/482)
    and CJ § Commit (`edb5f09`/148 → `f84eb78`/154). (R-3, R-8)
11. **Correct CJ's blast-radius figure by addition: 278 tracked files in the union, not 29–50 per
    component.** The conclusion (its own lane) is unchanged and stronger. (§6)
12. **Rewrite two `$why` sentences:** `dv-pie-001` (point at `motion.entry`, not at attributes that live in
    the snippet) and `dv-bar-002` (name a mechanism). And if Dave keeps `dv-013` on bar, rewrite that one
    to cite the grouped/stacked variants rather than `orientation`. (A-6, §3)
13. **File the `_rules-index.json` `dv-019` defect against `gen_rules_index.py` with the note that it has
    already propagated to `_rule_nodes.json` and `_consult-index.json`.** (G-10)
14. **Make `_dry_run.py` read-only, or write its receipt outside the audited path.** Re-driving a receipt
    should not dirty the lane. (R-7)
15. **Sweep the two strays** (`artefact` 0 B, `rule?` 49 B, both 21:33:10, both untracked, both confirmed
    unchanged by this lane). The conductor's, as the brief says. (A-3)

---

## Ownership and gates

```
$ python3 knowledge/_validate_kg.py
_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has provenance,
edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4 resolutions input was consumed.

$ git status --porcelain
 M notes/_REHEARSAL-LOG.jsonl          <- harness, not mine (mtime 21:50, moved during this lane)
 M notes/_dream/_GRADE-DECISIONS.jsonl <- harness, not mine
?? artefact                            <- stray, 21:33:10, untouched
?? notes/_lanes/277/judgement/BRIEF.md <- lane CJ's
?? notes/_lanes/277/verify/            <- THIS LANE, the only thing committed
?? rule?                               <- stray, 21:33:10, untouched
```
Nothing under `notes/_lanes/277/charts/` or `notes/_lanes/277/judgement/` is modified. Running CO's
`_dry_run.py` and `_drive_page.py` overwrote `dry-run.json`, `dry-run.txt` and `screenshot.png`; all three
were restored with `git restore --source=HEAD --worktree` and the tree is clean of them (R-7). No
`git stash` was used. No `.git/index.lock` was encountered. `gen_kg_edges.py` and `_build_all.py` were
never run.

## The commit

`--numstat` is the receipt, never the commit message — and, per R-3/R-8, the receipt of the commit that
actually shipped:

This lane commits once and then amends in place to splice this block in, so the pre-amend sha is dead the
moment it is written. **No sha is quoted here** — quoting one is precisely the R-3 / R-8 defect. The
`--numstat` below is the shape of the shipped commit; the only line that moves between the pre-amend
object and the shipped one is `VERIFY.md`'s own count, which grows by exactly the size of this block.

```
$ git show --numstat HEAD
41   0  notes/_lanes/277/verify/BRIEF.md
663  0  notes/_lanes/277/verify/VERIFY.md
-    -  notes/_lanes/277/verify/verify-390-dark.png
-    -  notes/_lanes/277/verify/verify-390-light.png
-    -  notes/_lanes/277/verify/verify-dark-1280.png
-    -  notes/_lanes/277/verify/verify-decisions-dark.png
-    -  notes/_lanes/277/verify/verify-decisions-light.png
-    -  notes/_lanes/277/verify/verify-light-1280.png
```

Six screenshots, two of them the light/dark full-page pair the brief asks for. Nothing outside
`notes/_lanes/277/verify/` is in this commit.
