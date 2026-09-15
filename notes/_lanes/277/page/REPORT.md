# LANE CP — REPORT — the decision page rebuilt on one number, cards first
#277 · 2026-09-15 · model: opus · **PROPOSE-ONLY — nothing under `knowledge/` was written**

Lane CV graded lane CO's page **21 GREEN · 8 RED · 8 AMBER** and returned the #268 verdict: *"the page
passes its driver … then fails on sight, because the card carrying the biggest number on the page says two
different things about it."* This lane rebuilt the page. Lane CO's files were never opened for writing;
every correction is **by addition**, in `notes/_lanes/277/page/`.

The deliverable is `notes/_lanes/277/page/REVIEW-charts-2026-09-15-v2.html`.

---

## 1. Item by item, against lane CV's "what the conductor must change" list

| # | CV's item | before (v1) | after (v2) |
|---|---|---|---|
| 1 | the unattributed CJ paragraph under D-2 and D-3 | the `why` slot carried CJ's recommendation with **no attribution in the card** — the only "(lane CJ)" was ~1,900px down in Receipts, so it read as the card's own conclusion | every card now carries `Recommendation.` followed **immediately** by an `.attrib` line naming the lane: *"Lane CO proposed the citations; lane CJ reached the same three drops independently; lane CV re-drove both"* (D-1), *"Lane CJ's recommendation, its words"* (D-2), *"Lane CJ recommended (b) at 46; lane CO measured 49; lane CV reconciled the two matrices cell by cell to 47"* (D-3). A driver check fails the build if a `.why` is not followed by an `.attrib` naming a lane. |
| 2 | rebuild D-3 on one number: **47** | card prose **49**, option (b) **49**, footer **46** — three numbers, one card | the matrix is built once, in the builder, as CO's `FAMILY` with two **declared** overrides; the page's figure is **47** and the builder `assert`s it. The lede leads with *"Two blind lanes read all 19 against all three and **agreed on 16 of 19**"*, then *"of the 57 cells they agreed on 54; three disagreed"*. |
| 3 | fix D-3's derived figures to match | option (a) said **8** false (CO's own matrix), the footer said **11** (CJ's); option (b) said **13** bind all three | recomputed from the one matrix: option (a) **10 of 57** false; option (b) **47 edges — 17 bar / 15 line / 15 pie**; **13** bind all three (13 survives the reconciliation, and now it is derived rather than asserted). |
| 4 | move the three decision cards above Parts A and B | page 9,558px; D-1 began at **6,081px = 64% down**; 43 table rows before the first ask | page 11,576px; **D-1 at 1,211px, the first radio at 1,435px = 12.4%**; section order is `headline · decisions · evidence · parta · family · q3 · receipts`, and an `#evidence` divider says in its own words that everything below it is working. The driver fails if `#decisions` is not before every evidence section or if the first ask is past 25%. |
| 5 | reword D-1 so (a) and (b) are exclusive | (a) *"land all 29 as proposed"* / (b) *"review per component first … then land what survives"* — (b) was (a) with a gate in front | (a) **"Land now."** / (b) **"Land after a per-component read."** (a) also names what he is landing unread: *"You would be landing 29 sentences you have not read; Part A prints all 29 of them plus the 3 drop reasons, so 'not read' is your choice, not a shortage of material."* |
| 6 | add to D-2 that (b) strands `dv-pie-003` | not said anywhere | option (b) carries it: *"⚠ Choosing this **strands dv-pie-003**: chart-pie drops it as donut-only and nothing else takes it, so an ingested rule ends the wave governing no component at all — a visible zero created by us, not found by us."* |
| 7 | surface `≤ 5 parts` vs `max 6` as its own line, **do not resolve it** | absent from the page | its own flagged block under the cards, headed *"Flagged, not a decision"*, with the file list (`roles.json` line 104, `chart-pie.meta.json` line 16, `chart-donut`, `chart-bar`), the fact that **`chart-pie.meta.json` carries both numbers eight lines apart**, that the gate `_validate_dataviz.py` carries the 6, and that **no ingested guideline file carries the 5**. Not resolved, not an option — the driver fails if `dv-pie-009` appears in any option text. |
| 8 | state the combined cost once, in the hero | headline stat said **110**, which is D-1 alone | hero sentence and first stat: **76 edges** (29 + 47), corpus **81 → 157**. The driver fails if the hero still contains `110`. |
| 12 | rewrite two `$why` sentences | `dv-pie-001` cited `data-a1`/`-a2`, which are in `Chart-donut.reference.html` and in neither of `chart-pie.meta.json`'s strings; `dv-bar-002` named no checkable mechanism | rewritten in `notes/_lanes/277/page/proposed-metas/` **by addition** — see §3. The third (`dv-013` on bar) is conditional on Dave and is written out in §3 rather than authored. |

**Also carried forward from CV, without being asked to:** the wider blast radius of the `dv-019` index
defect (it has already propagated into `_rule_nodes.json` and `_consult-index.json`, and the page says so),
and CV's measured capitalisation radius — **278 tracked files in the union, 111–156 per component** —
replaces CO's unmeasured "fifty-file diff" in Part C.

## 2. The one matrix, and why it is 47

CO's `FAMILY` dict, with **two declared overrides** and **one cell left open**. Both overrides are in the
builder's source with the reason beside them, and both appear on the page in a table of their own:

```
dv-008 / chart-pie   CO binds · CJ refuses   SETTLED FOR CO   chart-pie.meta.json responsive.rule:
                                                              ".dv-stage scrolls if the container is narrower"
dv-015 / chart-line  CO binds · CJ refuses   SETTLED FOR CJ   the rule routes BETWEEN chart types and
                                                              roles.json's chart-panel `when` fields already
                                                              route; CO's own eye-pass called dv-015 a taxonomy
dv-013 / chart-bar   CO binds · CJ refuses   OPEN — DAVE'S    held at NOT BINDING, so the page's figure is the
                                                              LOWER of the two, and named as the single open cell
```

```
$ python3 notes/_lanes/277/page/_build_page.py
family: CO 49 · CJ 46 · reconciled 47 (bar 17 · line 15 · pie 15) · 48 if dv-013 stays on bar
combined cost: 29 + 47 = 76 edges · 81 -> 157
```

Agreement, measured rather than asserted: **54 of the 57 cells** and **16 of the 19 rules** agree between
two lanes that did not read each other. That sentence, not a total, leads the card.

The builder refuses to write the page if the reconciliation does not hold:
`assert n["family_b_total"] == 47 and n["family_bar"] == 17` and
`assert n["combined"] == 76 and n["corpus_after"] == 157`.

## 3. The corrected `$why` sentences — by addition

`python3 notes/_lanes/277/page/_correct_whys.py` copies lane CO's three proposed metas **byte for byte**
and replaces exactly one textual span in two of them (#179: never re-serialise a JSON file to change a
string inside it). It refuses if a span is not unique, if the edit moves anything but a `$why`, or if the
count of moved sentences is not the count of intended edits. `chart-line.meta.json` comes through
identical, which is the control.

```
$ diff notes/_lanes/277/charts/proposed-metas/ notes/_lanes/277/page/proposed-metas/
chart-bar.meta.json   line 128 only
chart-line.meta.json  identical
chart-pie.meta.json   line 119 only
```

- **`dv-pie-001`** — was *"…the segments this meta bakes as data-a1/-a2 at generation time."* Now
  *"…the angle contract for the sweep this meta's motion.entry bakes (data-cx/-cy/-ro/-a1/-a2, no
  data-ri), which is where the start angle and the segment order are fixed, at generation time."* The
  pointer now names a field that is in `chart-pie.meta.json`, which the old one was not.
- **`dv-bar-002`** — was *"…the meta's axis tokens have to carry either way."* Now
  *"…the meta's tokens.font-family composite routes labels, axis, legend and values through one type role,
  .t-cm-chart-label at 12/500, and tokens.axis mints data/axis (DV-D07) for them, so the get-out clause
  changes what is drawn and never which token pays for it."* Both named things are greppable in the meta.
- **`dv-013` on `chart-bar`, NOT written** — it is a family rule, so it is in no proposed meta, and it is
  the open cell. If Dave keeps it, the sentence to author is: *"Combination charts: colour differentiates
  the data sets — this meta declares `grouped-column` and `stacked-column` multi-series variants and its
  `series` prop mints `data/series/1–5` for them, which is where colour carries the set identity;
  `orientation` is about sign, not about differentiating sets."* CV is right that `orientation` was the
  weaker of the two reasons available.

## 4. The gates

```
$ source knowledge/_render/seat_env.sh && python3 notes/_lanes/277/page/_drive_page.py
  ok    font loaded (HSBC_MtUnivers_Latin)                                    True
  ok    0 console errors / warnings / page errors                             0 bad, 0 page error(s)
  ok    descenders intact on the tight boxes                                  31 elements / 9 selectors · worst clip 0.00px
  ok    no element crops its own content                                      []
  ok    no text-transform:uppercase (nam-002)                                 []
  ok    no ALL-CAPS runs in visible text (nam-002)                            []
  ok    decisions before every evidence section, first ask in the top quarter page 11,576px · first ask 1,435px = 12.4%
  ok    D-3 states one family total, and it is 47                             lede ['47'] · option (b) ['47']
  ok    D-3's open cell is named as open, and both outcomes are priced        47 / 48
  ok    D-3 carries no at-most-one / none-of-the-three contradiction (R-5)    neither phrase present
  ok    every recommendation is followed, in the card, by its lane
  ok    the hero states the combined cost once: 76 edges, 81 -> 157           v1's 110 absent
  ok    the 5-vs-6 cap conflict is its own flagged line, names the gate, is not an option
  ok    D-2 says that (b) strands dv-pie-003
  ok    D-1's options are exclusive (land now / land after a read)
  ok    export is the RK shape, and page carries its .html                    "REVIEW-charts-2026-09-15-v2.html"
  ok    localStorage round-trips the choice and the note across a reload
  ok    390px light / dark: no horizontal scroll, nothing cropped             {"s": 390, "c": 390}
  ok    light: accent is the two-red law value (s151-D1)                      rgb(218, 26, 0)
  ok    dark:  accent is the two-red law value (s151-D1)                      rgb(246, 96, 76)
DRIVE PASS
```

**Five of those checks are new, and they exist because a green driver shipped the defect.** CO's driver
went eleven-for-eleven on a page whose D-3 card carried two arithmetics. So the five added checks are
written against that failure by name: section order and the position of the first ask; one family total
inside the D-3 card; recommendation-then-attribution in every card; the combined cost in the hero with
v1's 110 asserted **absent**; and the cap conflict present as a flag and absent from every option.

**Two of them went red on the first drive, and both were real:**
1. **390px horizontal scroll — `scrollWidth 448` against `clientWidth 390`.** The hero stat `81 → 157` is
   the widest unbreakable string on the page and `1fr` floors at min-content, so the two-column grid could
   not shrink. Fixed by dropping to one column below 520px and taking the figure to 1.875rem below 760px.
   CO's v1 had no such string and passed; the number this lane was asked to add is what broke it.
2. **D-2's recommendation read as unattributed.** A false red — the attribution was there, capitalised at
   the start of a sentence, and the check's regex was case-sensitive. Fixed in the check.

```
$ python3 knowledge/_validate_kg.py
_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has provenance,
edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4 resolutions input was consumed.
```

`gen_kg_edges.py` and `_build_all.py` were never run. No `git stash`. No `.git/index.lock` was
encountered.

## 5. The eye pass — what I saw, as a reader who has to decide

`[[art-director-reviews-lane-output-268]]`. I opened the screenshots rather than the check list.

**What is right.** The page now asks before it explains. The hero says what the wave costs in one
sentence and one large figure, and the four stat cards read as an answer rather than an inventory — 76 ·
81 → 157 · 16 of 19 · **1 cell still open, and it is yours**. That last card is the one I would keep if I
could keep only one: it tells him in four words that this page has done its arithmetic and left him
exactly one thing. D-3 now reads top to bottom as one argument — agreement, then the reconciled figure,
then the open cell in a red-ruled block, then the three options — and I could not find a second number in
it. The reconciliation table under the family matrix (CO / CJ / status / what decided it) is the honest
form of a disagreement: it shows both lanes being wrong in one cell each and says which file settled it.
Both themes are the same page; the dark ground at `#111` with the `#F6604C` accent holds the red-ruled
open-cell block without it shouting.

**Three things I found by eye that no check would have caught.**
1. **`dv-019`'s row printed dv-017's sentence.** The index defect lands in the table as two rows with
   identical text, and a reader skimming the matrix concludes the rule is a duplicate — which is the exact
   wrong conclusion CO's first pass reached and corrected. The cell now prints the **source** sentence and
   says in the cell, in accent colour, that it is reading past the index row. Fixed before shipping.
2. **A class collision.** `.opencell` and a `.tag.open` in the matrix both matched `.open`, so the inline
   table tag inherited a 2px accent border-left and block margins. Visible as a misaligned chip in the
   `dv-013` row. Renamed.
3. **The right third of the page is empty at 1280.** `max-width: 78ch` on prose inside a 1200px wrap
   leaves a wide gutter on every paragraph. It is the house Swiss measure and v1 did the same, so it is
   not a defect — but the tables use the full width and the prose does not, and at 1280 the page reads as
   two different grids. Not changed; declared, because changing the house measure is not this lane's call.

**What I would still flag to the conductor.** D-3's recommendation paragraph does contain the numerals 49
and 46 — attributed, in the past tense, and framed as *"both were arithmetically correct against their own
matrix, and the gap is three cells, not a sum."* That is reconciliation, not rivalry, and CV's item 2 asks
for exactly that sentence. But it is one line away from the defect that failed v1, so if the conductor
wants the card to carry no numeral but 47 and 48, it is a one-line edit to the `attrib` string in
`charts-decisions-2026-09-15-v2.json` and the page rebuilds.

## 6. What is on disk

| path | what |
|---|---|
| `notes/_lanes/277/page/REVIEW-charts-2026-09-15-v2.html` | **the deliverable** — 3 decisions, 2 flagged findings, 3 evidence tables |
| `notes/_lanes/277/page/_build_page.py` | bakes it; holds the one matrix, its two declared overrides and the open cell; asserts 47 / 76 / 157 |
| `notes/_lanes/277/page/charts-decisions-2026-09-15-v2.json` | the page's copy — no integers in it |
| `notes/_lanes/277/page/_drive_page.py` | 21 checks × the two themes, five of them new |
| `notes/_lanes/277/page/_correct_whys.py` | the two `$why` corrections, by textual span, with four refusals |
| `notes/_lanes/277/page/proposed-metas/` | 3 files — CO's proposals with 2 sentences corrected. **Not landed** |
| `v2-light-1280.png` · `v2-dark-1280.png` | full page, both themes |
| `v2-390-light.png` · `v2-390-dark.png` | full page at 390 |
| `v2-decisions-*.png` · `v2-D3-*.png` · `v2-hero-*.png` | the cards and the hero, where the v1 defect lived |

`knowledge/` is untouched: `git diff --stat knowledge/` is empty and `git status` shows nothing outside
this lane's directory that this lane wrote. Two files moved during this lane and are **not** this lane's —
`knowledge/_parked.json` and `notes/_lanes/277/charts/_dry_run.py` were modified at 22:17–22:18 by lane
CH, which was running in the same wave and has since committed them as `81e845a`.

## 7. The commit

`--numstat` is the receipt, and — per CV's R-3 and R-8, which caught two lanes today quoting shas they had
amended away — **the receipt is re-read from the sha that actually shipped**. This block is written before
the commit; the commit is made once and then amended in place to splice the receipt in, so any sha named
before the amend is dead. The `--numstat` below is pasted back from `git show --numstat <shipped sha>`.

```
$ git show --numstat HEAD    # no sha is quoted: quoting one IS the R-3 / R-8 defect,
38	0	notes/_lanes/277/page/BRIEF.md
224	0	notes/_lanes/277/page/REPORT.md
507	0	notes/_lanes/277/page/REVIEW-charts-2026-09-15-v2.html
748	0	notes/_lanes/277/page/_build_page.py
98	0	notes/_lanes/277/page/_correct_whys.py
319	0	notes/_lanes/277/page/_drive_page.py
42	0	notes/_lanes/277/page/charts-decisions-2026-09-15-v2.json
238	0	notes/_lanes/277/page/proposed-metas/chart-bar.meta.json
298	0	notes/_lanes/277/page/proposed-metas/chart-line.meta.json
227	0	notes/_lanes/277/page/proposed-metas/chart-pie.meta.json
-	-	notes/_lanes/277/page/v2-390-dark.png
-	-	notes/_lanes/277/page/v2-390-light.png
-	-	notes/_lanes/277/page/v2-D3-dark.png
-	-	notes/_lanes/277/page/v2-D3-light.png
-	-	notes/_lanes/277/page/v2-dark-1280.png
-	-	notes/_lanes/277/page/v2-decisions-dark.png
-	-	notes/_lanes/277/page/v2-decisions-light.png
-	-	notes/_lanes/277/page/v2-hero-dark.png
-	-	notes/_lanes/277/page/v2-hero-light.png
-	-	notes/_lanes/277/page/v2-light-1280.png
```

