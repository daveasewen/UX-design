# CORRECTIONS — by addition, never by rewrite

**Lane CH (hygiene) · #277 · 2026-09-15 · model: opus**

Four figures in two committed lane reports are wrong. **Nothing in `notes/_lanes/277/charts/` or
`notes/_lanes/277/judgement/` has been edited** — a lane's committed claim is its own, and a correction
that overwrites it destroys the record of the disagreement. This file is the correction, and it is
additive: the wrong figure, the right figure, and the command that decides between them.

Every figure below was re-driven in this lane, in this sandbox, at 22:1x. Not one was copied out of
`VERIFY.md` — a correction taken on trust is a second error, and the brief says so.

---

## C-1 · `REPORT.md` §5 (line 179): "**11** of the 57 would be false" → **8**

CO's option (a) row reads *"attach all 19 to each | **57** | Simple. **11 of the 57 would be false**"*.

The denominator is CO's own `FAMILY` matrix in `_author_metas.py`, and the matrix says 8:

```
$ python3 -c "import importlib.util; spec=...('_author_metas.py'); F=m.FAMILY
  print(sum(len(F[r]) for r in F), sum(1 for r in F for c in F[r] if F[r][c][0]))"
57 cells · 49 binding · 8 false
per component binding: chart-bar 18 · chart-line 16 · chart-pie 15   (= 49)
```

**57 − 49 = 8.** Eleven is lane CJ's number (57 − 46 = 11, off CJ's matrix, which differs from CO's in
exactly three cells). CO's report imported the other lane's arithmetic into a sentence about its own
matrix.

⚠ **The review page is right and the report is wrong**, which is the wrong way round: the page computes
this at build time and prints 8. The figure a conductor carries forward comes from the report.

**Confirms CV's R-1.** Independently re-driven here.

---

## C-2 · `REPORT.md` §4 (line 141): "12 of **139** metas carry a family edge" → **12 of 137**

The count of 12 is right. The denominator is not.

```
$ ls knowledge/components/*.meta.json | wc -l                    138
    minus EXAMPLE-button.meta.json                                 1
    (meta.schema.json is not a *.meta.json and never counted)
  =                                                              137 metas
  of which carry edges.family                                     12
$ python3 knowledge/_validate_kg.py | grep "metas checked"        139
```

**139 is `_validate_kg.py`'s denominator**, and it is correct *for the gate*: the gate additionally
validates `knowledge/_proforma/icon-button.meta.json` and counts the EXAMPLE file, because both must
satisfy the schema. Neither is a component that could carry a family edge, so neither belongs in this
ratio. The twelve are:

```
cards · headers · input-fields · links · list-items · modals · navigations ·
notifications · pagination · segmented-control · selection-controls · view-options
```

**Confirms CV's R-2.** Independently re-driven here. The review page prints 12 of 137 and is right.

---

## C-3 · `REPORT.md` §11 (lines 458–465): the commit receipt describes an object that is not the one that shipped

The report quotes:

```
b4d42ebccdb62fa57781abd7455d899175186e52   #277 … lane CO: the three charts authored …
460   0   notes/_lanes/277/charts/REPORT.md
```

`b4d42eb` is a real object — `git cat-file -t` returns `commit` — but it is the **pre-amend** object. The
commit that shipped, and the one on the branch, is:

```
$ git show --numstat --format='%H%n%s' 8c80aa2
8c80aa278b16a3b3d750e9f5d0a2ea6101e6c7b4
#277 2026-09-15 — lane CO: the three charts authored, 29 obeys proposed, 3 drops declared, nothing landed

 52   0  notes/_lanes/277/charts/BRIEF.md
482   0  notes/_lanes/277/charts/REPORT.md          <- 482, not 460
433   0  notes/_lanes/277/charts/REVIEW-charts-2026-09-15-v1.html
403   0  notes/_lanes/277/charts/_author_metas.py
616   0  notes/_lanes/277/charts/_build_page.py
234   0  notes/_lanes/277/charts/_drive_page.py
178   0  notes/_lanes/277/charts/_dry_run.py
132   0  notes/_lanes/277/charts/_mutate.py
 39   0  notes/_lanes/277/charts/charts-decisions-2026-09-15.json
 20   0  notes/_lanes/277/charts/dry-run.json
 31   0  notes/_lanes/277/charts/dry-run.txt
238   0  notes/_lanes/277/charts/proposed-metas/chart-bar.meta.json
298   0  notes/_lanes/277/charts/proposed-metas/chart-line.meta.json
227   0  notes/_lanes/277/charts/proposed-metas/chart-pie.meta.json
  -   -  notes/_lanes/277/charts/screenshot.png
```

**Sha wrong, line count wrong.** The report's own parenthetical at line 481 acknowledges the splice and
then leaves the stale sha standing next to it, which is worse than not quoting one — a reader who checks
the sha gets a real commit with a different tree.

**The corrected receipt for lane CO is `8c80aa2` · `482 0 REPORT.md`.**

**Confirms CV's R-3.** The sibling defect in lane CJ (`RECOMMEND.md` § Commit quotes `edb5f09`/`148`; the
shipped commit is `f84eb78`/`154`) is CV's R-8 and is **not** re-driven here — it is the same class and
the conductor should take both from CV.

**The lesson is the memory hook, not the two slips.** `--numstat` is the receipt *of the commit that
shipped*. A lane that commits and then amends to splice its own receipt in has killed the sha it just
wrote; the only safe forms are to quote no sha at all (lane CV's choice) or to re-read `git show HEAD`
after the final amend. Both lanes did the first and neither did the second, so this is a wave-level
pattern.

---

## C-4 · `RECOMMEND.md` (lines 113, 136): "**29–50** non-generated files per component" → **114–159 tracked per component, 279 in the union**

CJ's figure is not wrong so much as **unqualified**: it is the `knowledge/`-only count, presented as the
repo-wide one. Re-measured here, live, per stem:

```
$ for s in Chart-boxplot … Chart-scatter; do git grep -l "$s" | wc -l; done

                     tracked (repo-wide)   knowledge/ only
Chart-boxplot                159                33
Chart-bullet                 145                41
Chart-butterfly-h            130                31
Chart-butterfly-v            114                27
Chart-candlestick            129                30
Chart-histogram              135                27
Chart-scatter                156                42

union of all seven, tracked repo-wide        279 files
union of all seven, knowledge/ only           78 files
```

**CV is right; CJ is understated by 3–5×.** The `knowledge/`-only range is **27–42**, so even CJ's
subtree figure is stated a little wide at the top (50 against a measured 42).

**My repo-wide numbers are one higher than CV's** (159 vs 158, 279 vs 278). That is not a disagreement:
CV measured before its own commit landed, and `notes/_lanes/277/verify/VERIFY.md` now names the seven
stems itself, so it counts. `git grep -l … | grep -c notes/_lanes/277/verify` returns **1**, which is the
whole of the difference. The `knowledge/`-only union is **78 in both lanes**, unchanged — the subtree CV
measured has not moved. Where the two differ, **CV's figures are the ones taken at the time of grading and
mine are the ones live now**; both support the same conclusion.

**The conclusion survives the correction and gets stronger.** A case-only rename of seven files touches
**279 tracked files** in the union, needs the two-step `git mv` on this case-insensitive filesystem (a
one-step `git mv Chart-x chart-x` records nothing), and moves node ids — the filename stem *is*
`component:Chart-boxplot` in the graph. It is its own lane. All three lanes refused to do it inside the
charts lane and all three are right. Parked as **P-277-2**.

---

## What this file does NOT correct

- **The three judgement cells** (`dv-008` on pie, `dv-013` on bar, `dv-015` on line) and the reconciled
  **47**. That is CV's §3 and it is analysis, not arithmetic — neither lane made a counting error and
  this lane has no standing to re-decide it. It is the conductor's to put on the page and Dave's to rule.
- **The page defects** (CV's items 1–8 and 12). Lane CP's, running in parallel. Nothing under
  `notes/_lanes/277/page/` was opened by this lane.
- **The `≤ 5 parts` vs `max 6` conflict** (CV's §5). Ruling-shaped and Dave's; CV has already surfaced it.
