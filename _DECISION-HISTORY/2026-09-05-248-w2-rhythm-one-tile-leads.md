# #248 — W2 rhythm, one tile leads: the wall landed, the chart became the finding, two edits could not reach the page, and the judge said "nothing leads" a second time

```
provenance: 248 · 2026-09-05
status: observed
```

*Spine entry: `_LIVE-STATE.md` § `## ⏱ LATEST DELTA — 2026-09-05 … #248`. Ledger: `knowledge/_rulings.json`
§ `s248-D1` … `s248-D4` (inscribed by the conductor via `_inscribe_ruling.py`, 360 → 364, read back at the wrap).
Banner: `GOOD-MORNING.md` § ★ LATEST #248. Reports: `notes/_subreports/2026-09-05-248-W2-D-rhythm-edit.md` ·
`…-W2-D2-chart-fit.md` · `…-W2-D3-reflow-vfit.md` · `…-W2-R-rerun.md` (+ `…-W2-D-SEAM.md` · `…-W2-R-SEAM.md`) ·
`notes/_subreports/2026-09-06-248-wrap.md`. Brief: `notes/_briefs/2026-09-05-248-W2-rhythm-brief.md`. Review surface:
`reviews/W2-RHYTHM-2026-09-05-v1.html`. Score sheet: `notes/_dp-scores/w2.json`. Judge: `outputs/w2-rhythm/judge/verdict.md`
(gitignored, on disk). Carries: `_CARRIES.md` § `## residual → #249`. Both-way: each of those files names this dossier's session.
⚠ WRAP DATE SPLIT: the session ran 2026-09-05; the capture ritual ran 2026-09-06 (this file is dated from the session, per the
#241 precedent; the wrap report is dated from the day it was written).*

---

## 1. Why one edit became three lanes

W2's brief was the W1 shape: ONE edit to the template (the wall below the lead row goes from 3+3 to 4+2, the plan's DP-14/15
defaults), a P0 re-run blind then sighted, a blind judge. Lane D made the edit and reported that DP-18 was **inverted** in the
specimen — the context tiles carried 0px of empty ground, and the CHART was the stretched tile: 155px of air below its fixed
260px canvas and 276px to its right, because the template's rule 9 pinned the canvas at 580px and let the tile grow around it.
Dave looked at the 1440 render and said the thing that re-shaped the day: *"this is mostly fine as long as the chart is
responsive. rule 9 is possibly a mistake"* — then, sharper, *"What is teh chart not responsive, it should be"* (`s248-D2`).
So lane D2 carried Chart-bar's FIT module into the template (width fit; the physics assertion — labels 12px = 12px, strokes 1px =
1px while the chart area moved 856 ≠ 988 — is the probeable token that fit re-positions and never scales). Then Dave's two crops
of the 1100 render (*"so this should fill"* / *"and, thsi could be two columns too"*, `s248-D1`) and *"the charts should
probably be vertically responsive to, the aspect ratio doesn't need to be constant either"* sent lane D3 to build the re-flow
(rule 6b) and the vertical fit (VFIT). Three lanes, one file, 274 lines changed — the wave was still one variable to the
score sheet (the wall's spans), but the library learned that its chart had never fit its tile in either axis.

## 2. Why "edit mode is coming" is a ruling and not a roadmap line

Between D2 and D3 Dave added *"there will be a edit mode ultimately where we should be able to edit the bento somewhat, and
the user can prompt changes if needed, this does mean the components should be responsive"* (`s248-D3`). The conductor
inscribed it as a **design constraint on the library**, not a feature order: a tile's span is no longer fixed at authoring time,
so every component placed in a tile must answer the tile it is given in width AND height. It is the reason the vertical fit
was built at all (a fixed 260px canvas is fine in a specimen and wrong in an editor), and it is the reason #249's job is to move
that fit OUT of the template and INTO the components — the template cannot be the one place a behaviour lives if every tile
can be re-spanned by a user. `s246-D5` had already marked the KPI-row default PROVISIONAL "revisit when edit mode exists";
D3 is that revisit arriving early as a constraint rather than late as a rewrite.

## 3. Why two of the three edits did not reach the composed page — and what that says about where fit lives

Lane R re-ran P0 on the D+D2+D3 library and measured the wall exactly as the template promised: 4+2, evidence 893.3px beside the
rail 426.7px, every edge on a column line, seed 4 (the symmetric wall) gone. But (i) `s248-D1`'s rule 6b lives in the snippet's
own `<style>`, and canon.css was not regenerated (the build is fenced for lanes and sandbox-impossible in one process), so the
composed page at 1100 still orphans the rail 2-of-3 while the template re-flows; and (ii) the template's hand-carried VFIT stub
and Chart-line's own `dv-behaviour.js` both claim every `svg.dv-fit` and **fought** over the line chart — gridlines re-derived
for 415px, viewBox re-pinned to 260, series at baked y. The sighted builder dropped the stub at its third iteration, so the page's
chart is 821×260 with 44.1px of ground under it: DP-18 met on the template, missed on the page. The lesson is structural, not a
bug: a behaviour carried into a template by hand is a second copy of an engine, and two engines on one svg is a race. Fit belongs
in the chart components (`Chart-bar`, `Chart-line`, `dv-behaviour.js`'s FIT module), regenerated into the partial, with the
template's stub deleted — lane D3 RSQ 2 and lane R RSQ 1 both say so; it is `Apollo - #249: fit lives in the chart — D2 to the
components`. The two PROVISIONAL constants (`PL_MAX_FRAC`, `PL_EDGE_PAD`) now in a second file and the "sane" 200px floor travel
with it.

## 4. Why the composition gate is red three times over a render that is orphan-free

C9's per-tile arm (`_validate_composition.py` L296, `cols % eff`) rejects `data-c="4"` at base even though 4+2 fills the row, and
its row-sum arm (L301) catches the REAL 3-col orphan (3+3+2 = 8) that rule 6b then removes in the browser — but the gate reads
static clamps and cannot see a scoped `grid-column:1 / -1`. The gate encodes the snippet's own header law ("ONLY 6 and 3",
L69–75), so the plan's DP-15 default and the library's own squaring law disagree, and `s248-D1` sharpened the law's PURPOSE
(orphan cells, not re-packing) without changing the gate. No lane edited the gate; every lane said so and carried the question.
The two stale "only 6 and 3" comments carried from W1 stop being a comment edit here: the law they state is the gate's, so the
carry is re-framed as "C9's law vs `s248-D1`" — Dave's. And the spans dial (`s246-D3`) cannot be built to a chord the gate
rejects (the #244 rule), so it waits behind that question.

## 5. Why "12 columns" is a vocabulary question before it is a build question

Dave, describing the grid he means: 12 columns, minimum tile 2, rows like 3-3-2-2-2 or 4-3-6 (written "13" — carried as
written). The template declares `--layout-bento-columns:6`; the #216 showcase counts 12. A 6-col `data-c="4"` IS his 8-of-12 if
the unit is 2 — and is not, if 3-3-2-2-2 (five tiles, an odd count) is a legal row. This is the `s202` class: when Dave rejects
and every assert stays green, suspect the vocabulary first. It is carried as his, ahead of the gate and the dial, because both
would be built to whichever grammar the library is ruled to speak.

## 6. Why the judge was blind again, and why "nothing leads" twice is a standing row

Lane R wrote the judge folder FIRST (x = template re-flow, z = W1 sighted; y = W2 sighted added after arm B froze; seed
248005, KEY unopened). The first judge lane timed out at 45K quota with no verdict; the retry wrote it: *"all three are ordered,
none scattered — the failure is rhythm, not order; y is closest because its lower band has a head, x and z have nothing that
leads at all"*, and its first change on W2 is the same instruction the W1 judge gave — pull Group liquidity out as the lead tile.
Two blind readers, two waves, one sentence. That makes DP-07/DP-14 against DP-06 the conflict ledger's STANDING row rather than an
entry, and it is Dave's: `s247-D4` rules the ROW, not the weights. Arm L (one lead tile at `data-c="2"`) was rendered for the
judge and Dave retired it for stats in his own words (*"might work in other cases but not for stats"*), describing instead a
headline stat as a text stat with a chart to the right and sub-stats below, or inverted — a composite, not a wider tile.
Nothing was drawn; the shape is carried in his words.

## 7. Why the blind arm's harness defect is reported as a count and not fixed

The Tabs L80/L120 demo width recurred byte-for-byte on the W2 blind arm (cols 1, chart y 1554.4, page 2719px — W1's exact
figures). The brief said report, do not fix under the arm, so the arm stays comparable to W1's 1/1/0/2. Third occurrence; the
count is the fact; the fence under a DEMO CHROME marker is still Dave's out-of-group fix (the plan's RSQ 4).

## 8. Why the wrap was delegated, and what it could not commit

The conductor's FILL was 183,983 real at the brief cut (42 turns), past the 150,929 advisory; this seat read 184,553 first-hand.
The recall probe was not planted (declared). The ritual ran whole. But the 2f roll put #247's boot (70,822) into the gauge log,
and the ceiling arm — BLOCKING — graded it: a new breach, AND #242's discharge un-discharged ("a later breach is a new breach
and un-discharges the older one"). The `s244-D1` form cannot be written for a newest-reading breach, and #248's own boot
(70,974) is over too, so #249 cannot write it either. The remedy the gate names is to CUT THE BOOT; the literal is Dave's. The
wrap sub's brief said: if a gate refuses, name the first obstacle and stop — so the record is written, the chain generated, the
index rebuilt, and the commit is left to the conductor with the #243 precedent (an `after #248` commit DECLARED not-a-wrap, the
`--wrap` FINAL owed) named as the one legal state short of Dave's word. Nothing re-dated, nothing moved.

## 9. What the lanes cost

Subs ≈699K quota before the wrap (n=6: D ≈131K · D2 ≈110K · D3 ≈131K · R ≈235K · J 45K timed out · J retry 47K), the
conductor's declared figures by the harness counter; the wrap sub's own spend unmeasured. Pace panel at the opener, declared by
Dave: All 13% · Fable 24%, reset Thu 23:00. QUOTA, never window FILL.

## Resolved

`s248-D1` (re-flow at 3 cols) · `s248-D2` (chart responsive both axes, rule 9 retired) · `s248-D3` (edit mode ⇒ tile components
fit their tile) · `s248-D4` (W2 as rendered approved) — all in Dave's verbatim words, in the store. The 4+2 wall on the composed
page: seed 4 passes, DP-14/15/16 met, sheet 10 · 16 · 3.

## Open

Fit into the components (#249) · canon.css rebuild (`s248-D1` on the composed page) · C9's law vs `s248-D1` · 12 vs 6 columns ·
which tile leads / the headline-stat composite · the spans dial · the status surface (`s247-D3`) · the Tabs fence · "some other
messiness" (his, unlocated) · the boot over the ceiling, three post-diet breaches, the arm un-dischargeable · the `--wrap` FINAL
commit · everything at its age in `_CARRIES.md` § `## residual → #249`.
