# #304 Run 4 · lane 4b — the geometry gate and the own-size check (FULL SUB-REPORT, for filing)

Seat 4b, Sat 2026-09-26 night. HEAD `6af293df`; `canon.css` md5 was `2f84568d…` when measured. Run 3 is moving canon in parallel; the geometry fixtures load no canon CSS, so that cannot move them. Nothing was committed or pushed. No `git status`, no git writes, no `_build_all.py` run, no Project memory.

## The answer first

Two advisory gates now measure, in a real browser at the seat, what Dave called "alignment, spacing and dimensions" (#288) and "buttons and table headings way smaller than they should" (Thu 24 Sep, 15:46).

**`knowledge/_validate_geometry.py`**
- Eleven clauses: G1–G10 plus G1b.
- Every planted defect on its fixture is caught, 11 of 11, on the planted element.
- The clean fixture passes at 1440 and 390 with zero findings.
- The reference bento at 1440 shows only one finding, and it is true: the sparkline end dot is drawn as an ellipse.
- On the real #288 page it names four of the conductor's five observations.
- Mutations: switching any one clause off lets exactly its own planted defect through (11 of 11).

**`knowledge/_validate_own_size.py`**
- Three clauses: S1 height, S2 own minimum width, S3 type size.
- Every planted part-defect is caught, 9 of 9: a button and three column headings under their reference height and type size, and #288's `.mini` button under its 96px minimum.
- The clean fixture passes, and so does the whole showroom (136 pages, 1,304 parts matched, 0 findings).
- Mutations: 3 of 3.

**Wiring:** both are ADVISORY `_build_all.STEPS` 147 and 148. They were appended to the end, and their route rows went in the same edit. The second consumer is lane 4c's harness, which calls `<gate> PAGE --json out.json`.

**Runtime:**
- Geometry: about 1.7 s per page for both widths (median of 27; range 1.4–2.0 s; 4.5 s for the 28,000px canon gallery). Selftest 6.2 s.
- Own-size: 0.5–2 s per page at 1440, including the reference renders (20 s for the canon gallery's 383 parts). Selftest 10 s.
- `--build`: 8.9 s for geometry, 18.3 s for own-size.

## 1. The geometry gate

**Terms.**
- A *tile* is a `.c-bento__tile`, or any painted card of at least 120×60 that is a child of a grid or flex container.
- A *wall* is a grid or flex container holding two or more tiles.
- A *group* is a tile that holds a wall.

The tolerances are argued in full in the script's docstring.

| Clause | Designer-facing rule | Tolerance |
|---|---|---|
| G1 unequal gutters | One gutter per wall; sibling walls at one level share it. | ±1px. `fr` rounding; 1 is also the smallest ruled stop. |
| G1b mixed wall levels | Nested bentos beside bare cards. Rows then show 4px gutters in some places and 40px in others (#288's "gutters differ between the KPI row and the rows below"). | The inner gutter differs from the wall's own. |
| G2 off-scale spacing | Bento gutters sit on the ruled stops `{1,2,4,16,24,40}`, read at run time from `_render/_bento_edit_rails.json` (s219-D1(4)). Everything else sits on the 4px grid as `_validate_grid.py` defines it. | ±0.25px. |
| G3 edges that nearly line up | Left or right edges in different rows of one wall system, or tops in one row, that are 1–16px apart. | 16 is the first ruled stop above sub-spacing. |
| G4 unshared bottom edge | The last tile in each column reaches the wall's bottom. | ±1px. |
| G5 bar narrower than its table | A filter bar within 32px above a table spans the table at both edges. | ±2px. |
| G6 dead space | An empty band between measured ink of 48px or more. | 40, the largest spacing canon uses in a tile, plus one 8px step. |
| G7 overlap | Tiles, or ink on ink between different elements. Line boxes are shrunk to ink with `measureText` and clipped by overflow ancestors. Overlay layers and closed `<details>` are skipped. | More than 2px across and more than max(2px, 15%) deep. |
| G8 clipped text | Glyph ink cut by `overflow:hidden\|clip`. This includes the ds-005 trim + overflow trap. | At least 0.5px of ink at the top or bottom; at least 2px at the sides with no ellipsis. |
| G9 horizontal overflow | The page scrolls sideways at 1440 or 390; the outermost offending boxes are named. | 1px. |
| G10 stretched part | A `preserveAspectRatio="none"` SVG holding text, circles or raw strokes, or a `fill` image, scaled non-uniformly. | More than 10%. |

G1 and G2 skip two cases, both learned from false positives on the baseline:
- an axis where the wall shares out free space (`space-between`, `around`, `evenly`);
- a gap that has a heading or loose text inside it (on `payments-journey`, 102px of "gutter" was text between two cards).

**The verdict object (`--json`).**
- Fields: `gate, page, widths{…font_ok}, findings[{clause, name, severity, width, where, measured, expected, fix, planted}], counts, kinds, score, score_by_width, verdict (CLEAN|FINDINGS|UNPROVEN-FONT), font_ok, runtime_ms`.
- There is also a human list on stdout, or markdown with `--out`.
- Every finding carries a fix sentence.

**The score, specified for 4e.**
- It counts defect *kinds*: one clause, at one width, on one selector shape, with quotes, ids and numbers stripped. Four KPI labels clipped the same way count once.
- 3 = no kinds. 2 = no major kind and at most 3 minor kinds. 1 = at most 2 major kinds, or more than 3 minor. 0 = 3 or more major kinds.
- Major means G7, G8, G9 or G10.
- `score` is taken at 1440, because the CEO Common prompt says "wide desktop". The 390 score is carried in `score_by_width`.
- Why kinds: counting instances made every baseline page score 0, because nothing was built for 390. A flat 0 cannot separate v1.0.13 from the candidate.

**The face.**
- `document.fonts.check()` answers true for any system family, so it is vacuous. That also makes `_validate_hit_area.py`'s font check vacuous, a side finding.
- Both gates instead measure the width of a string in `"<face>", monospace` against plain monospace.
- Under a fallback face the verdict is UNPROVEN-FONT and the score is null.
  - The geometry selftest still binds its fixture and mutation legs, and declares the reference and #288 legs unproven. This was measured by forcing a fallback fontconfig: the reference bento gains a 50px G6 band.
  - The own-size selftest refuses with exit 77.

## 2. The own-size check

**What it compares.** For each element wearing `cn-<slug>` whose `<Name>.reference.html` exists (the `gen_canon_components.slug` rule), it measures every part and compares it with the same part in that snippet's render, at the same width.

**What counts as a part.**
- Controls: `button`, `[role=button]`, `.btn`, text-like `input`, `select`, `textarea`, `[role=tab]`.
- Column and row headers: `th`, `[role=columnheader]`.
- Cells: `td`.

**How parts are matched.**
- A part belongs to its nearest canon component.
- Its key is tag + role + head/body position + the classes it shares with the reference. State classes and page-invented classes such as `.mini` are dropped, so the part is still matched and the page's effect on it is what gets measured.
- A part whose classes the reference never uses is the page's own control. It is listed as unmatched and not judged.
- The legal range is every value the reference shows for that key.

**What is never measured:** APOLLO-DEMO harness fences, the showroom review overlay (the page is opened with `#chrome=0`), and closed `<details>`.

**The clauses.**
- S1: a control or header below 0.92× the smallest reference value, or a control above 1.25× the largest.
- S2: narrower than 0.92× the reference's computed `min-width`.
- S3: font-size below 0.92× or above 1.15× the reference.

## 3. Test it hard

**The fixtures.** Four pages sit in `knowledge/_tests/geometry/`. They come from one template per pair (`notes/_lanes/304/R4b/gen_fixtures.py`); each planted page is byte-identical to its clean twin except at the marked defects. The geometry pair loads no canon CSS, so it tests the instrument. The own-size pair is a canon page with two Buttons and a Table.

**Planted defects, and what caught them** (evidence: `notes/_lanes/304/R4b/selftest-*.txt`). Every one was caught.
- G1: a 12px margin (4px against 16px).
- G1b: bare cards beside a bento.
- G2: a 20px bento gap and a 14px padding.
- G3: a column line 8px off.
- G4: `align-items:start`, leaving a tile 28px short.
- G5: a filter bar at 60% of its table's width.
- G6: 141px of empty band.
- G7: a label pulled 24px up onto another.
- G8: a label with cap-alphabetic trim and `overflow:hidden`; 3px of ink cut.
- G9: a 1600px element.
- G10: an SVG at 3.28× by 1×.
- S1 and S3: the Approve button at 32px / 12px, and three column headings at 13px / 11px.
- S2: the `.mini` Review button at 72px against its 96px minimum.

No finding lands on an unplanted element. Each mutation drops exactly its own catch.

**Real defects: the #288 page**, the artefact the finding came from. The selftest asserts all four of these:
- G1b: bare cards at 40px beside bentos at 4px.
- G3: right edges at x=930.7 and x=942.7.
- G5: a 560px bar over an 848.7px table.
- G6: 174px and 372px bands in two cards; 50–114px in the KPI tiles.

The fifth observation, bottoms not shared, does not reproduce: both cards end at y=1944.1. The report says so rather than faking the test.

**Confirmed by eye.** Crops are in `notes/_lanes/304/R4b/`.
- #288's KPI labels lose 2px of descender ink (`288-kpilbl-1440.png`).
- The reference sparkline's end dot is an ellipse (`ref-spark-1440.png`).
- Axis labels collide: "MarAprMayJun" (`crop-w1-jun.png`) and the gallery histogram (`crop-gallery-hist.png`).
- The #292 one-shot's table overflows its card at 1440 (`292-1440.png`).
- #288 at 390 is overlapping cards (`288-390.png`).
- The reference at 390 scrolls sideways, and its figures overlap and clip (`ref-390.png`).

**Clean-page verdicts.**
- Clean fixtures: 0 findings at both widths.
- Reference bento at 1440: only the four true G10 findings. They are allow-listed by name in `REFERENCE_KNOWN_TRUE`; anything else fails the selftest.
- Reference bento at 390: 17 findings, all true. "Passes the reference bento" holds at 1440 but not at 390, and the gate is right both times.
- Showroom: 0 findings (102 CLEAN, 34 with no measurable parts).

**False positives found and fixed at their cause:**
1. Line-box touch on trimmed labels. G7 and G8 now measure ink.
2. Chart data tables parked off-tile, and closed `<details>`. Visible-rect clipping and `checkVisibility()` now handle them.
3. Text-in-gap and `space-between` distances being read as gutters.
4. Foreign controls inside `cn-tabs`.
5. The showroom review overlay.
6. Charts measured mid-fit. There is now a settle loop.

**Determinism.**
- 5 of 5 runs were identical on #288 and coldrun-267.
- `dashboards/international-banking-dashboard.canon.html` is bistable in itself: its second row renders at 356px or 479px, about 50/50, giving 1 or 3 findings. 4c should render once per run and record the result.

## 4. Baseline: 26 distinct one-shot and composed pages, plus the reference

Data is in `notes/_lanes/304/R4b/baseline/`: `geometry.json`, `.md`, `-table.md`, `own-size.json`, `-table.md`, and `showroom-1/2.json`.

**Geometry at 1440.**
- Score 3 on three pages: regen-v2-receipt, payments-journey and sme-payments-swiss.
- Score 2 on three pages.
- Score 1 on nineteen pages.
- Score 0 on the canon gallery.
- Every traced cold run carries the template's sparkline end-dot G10.
- At 390, twenty of the 27 pages (the 26 plus the reference) score 0; nothing was built for a phone.

Selected rows (score at 1440 / at 390; findings at 1440 with kinds in brackets):
- #288 composed: 1 / 0; 15 (5): G1b, G3, G5, G6:8, G8:4.
- #292 one-shot: 1 / 0; 13 (3): G1b, G6:7, G8:5.
- coldrun-267: 1 / 0; 6 (2): G6:2, G10:4.
- coldrun-258, v3, v4, v5: 1 / 0; 4 (1): G10:4.
- coldrun-258-v2: 1 / 0; 7 (3): G5, G6:2, G10:4.
- baseline-246 and -opus (arms A and B): 1 / 0; 4 (1).
- w1-density and w2-rhythm (arms A and B): 1 / 0; 8 (2).
- international-banking canon: 2 / 1 (bistable).
- regen-v1: 2 / 1.
- Reference bento: 1 / 0.

**Own-size at 1440.**
- Nine pages report NO-PARTS: they have no `cn-` wrappers, so the check is blind to them. That is a coverage limit, not a pass.
- Real findings:
  - coldrun-267: the "Markets" sidebar nav button is 725px tall, stretched by its flex group (probe-confirmed).
  - coldrun-267: data-grid pagination buttons render at 24×16 against a 44px minimum and 24px height.
  - #288: four `.mini` buttons at 79–88px against a 96px minimum.
  - coldrun-258-v3 and v4: sort headers at 36px against 44px.
  - international-banking: navigation icon buttons at 21px against 44px.
  - Every fitness page that links `canon.css` without `type.css`: buttons, inputs and textareas at the browser's default 13.33px instead of 16px. Button's type "comes from the canon composite … in canon/type.css" (`Button.reference.html:127`). That is a concrete cause for Dave's "buttons way smaller"; the #288 DECISIONS file names the same trap at A2.

## 5. Wiring, and what the commit seat must do

**The `_build_all.py` edit.** I re-read it at HEAD first; the file's md5 matched `git show HEAD:` (`c27d742f…`). Two STEPS entries were appended after the polarity selftest:

```
("geometry gate — alignment, gutters, edges, bar width, dead space, overlap, clipped text, "
 "overflow, stretch on generated pages (ADVISORY, built #304)", "_validate_geometry.py", ["--build"]),
("own-size gate — every part at its reference size on generated pages (ADVISORY, built #304)",
 "_validate_own_size.py", ["--build"]),
```

Two ADVISORY rows were added to `ROUTE_ROWS` in the same edit. Existing step indices are unchanged; the total goes from 146 to 148.

**Checks after the edit.**
- `check_routes()` = 148.
- The wiring gate: 55 wired, 4 exempt, 0 failures.
- The help gate: both files are guarded. Its three failures are pre-existing, in `knowledge/_tmp/`.
- Exit codes are correct: `--help` 0; no arguments 2 (worded to match the pack probe's `ARGS_REFUSAL`); no playwright 77 COULD-NOT-ASK, which the build reads as declared. The CI gates job has no browser, so it will declare COULD-NOT-ASK, the `_validate_hit_area` precedent.
- The rollback copy is `notes/_lanes/304/R4b/_build_all.pre-R4b.py.txt`. Do not stage it.

**The regen.** `_gen_schematic.py --check` is now stale (measured: "146 steps" became "148 steps"). Run the C1 serial on the mount, in order:

`_render_rulings.py → tokens/_build_blast_radius.py → _build_memento_index.py → _build_graph_mention_map.py → _gen_chain.py → _gen_schematic.py`

Every `--check` must come back fresh, then run the clone survey.

**Files to add.**
- `knowledge/_validate_geometry.py`
- `knowledge/_validate_own_size.py`
- `knowledge/_tests/geometry/{geometry-clean,geometry-planted,own-size-clean,own-size-planted}.html`
- `knowledge/_build_all.py`
- this report, at `notes/_subreports/2026-09-26-304-R4b-geometry-and-size.md`
- `notes/_lanes/304/R4b/` (generator, baseline, selftest logs, evidence PNGs, probe scripts), excluding the `.pre-R4b.py.txt` copy.

`knowledge/__pycache__/_validate_geometry.cpython-310.pyc` was written; it is gitignored.

**The pack roster is for 4g and Dave.** `_gen_pack_manifest.py` globs `knowledge/_validate_*.py`, so the next manifest will claim both gates and move the ruled roster of 58 by two, with nobody having decided. Its own comment (lines 439–459) forbids that. Hold them out of the candidate, or ship them and name the new count on Tuesday's page; either way it is Dave's word. Two consequences if they ship:
- `knowledge/_tests/` does not ship, so the selftest cannot run from the pack; page mode works.
- Own-size imports the browser harness from geometry, so the two must ship together.

**Optional.** A `continue-on-error` step `python3 knowledge/_validate_geometry.py --build` in the CI render job (which has chromium) would really run, and would report PARTIAL because CI has no HSBC face. I did not add it: `gates.yml` is outside this lane.

**Blocking is Dave's**, after Tuesday.

## 6. The `_state` doc row (spec)

```json
{"id":"W-304r4b","title":"#304 Run 4b filed report - the geometry and own-size gates: 11 + 3 clauses, every planted defect caught, wired advisory at steps 147-148","home":"notes/_subreports/2026-09-26-304-R4b-geometry-and-size.md","links":["knowledge/_validate_geometry.py","knowledge/_validate_own_size.py","knowledge/_tests/geometry/geometry-planted.html","knowledge/_tests/geometry/own-size-planted.html","notes/_lanes/304/R4b/baseline/geometry.json","notes/_lanes/304/R4b/baseline/own-size.json"],"project":"apollo","opened":304,"state":"open","owner":"claude","condition":"stated","body":"s218-D7 filed report, Run 4 lane 4b (#304). Two advisory render gates for the #288 sloppiness class and Dave's own-size sentence (Thu 24 Sep 15:46); wired as _build_all steps 147-148; lane 4c's harness is the second consumer. Row as the report specifies, to be minted by the Run 4 commit seat.","closes_when":"a Fable verifier that built neither gate re-runs both --selftest at the seat and files under notes/_subreports/ citing this report by path, and Dave has ruled whether each gate stays advisory or blocks"}
```

## 7. Limits

- Own-size sees only `cn-` wrapped components.
- References render in the snippet's default theme.
- G6 counts every SVG mark as ink, so a chart with headroom and no gridline could read as dead space.
- G7 skips painted overlay layers, so a badge over a label is not called an overlap.
- G3 compares edges within one outermost wall only.
- Every measurement was taken at the arm64 seat with the HSBC face.
