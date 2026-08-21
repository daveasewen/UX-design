# Receipt — #211 findings-repair **wave 2, LANE R2** · the container-type SELF-QUERY class

**Lane:** R2 (Opus) · **Date:** 2026-08-21 · **Brief:** `notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md`
(DO-NOT-RULE both halves + RETURN-CONTRACT bind; the lane list there is overridden by this lane's own job)
**Repo HEAD at lane open:** `fc6b35d` · **Commits made by this lane: NONE** (fenced).

---

## OUTCOME IN ONE LINE

`.l-split` in the gated **Layout-utilities** primitive declared `container-type` on the very element
its own `@container` rule targeted, so **it could never collapse** — repaired at cause by moving the
collapse declaration onto the split's CHILDREN, where the query actually resolves. The three
`.tpl-split-host` workarounds are removed, the four dead copies now carry the fixed recipe, and
Transfer-list's `.tl` got the ruled `.hv-frame` wrapper shape. **P-7: 6 findings + 3 WARN → 0 + 0.**

---

## ⛔ A PREMISE IN MY OWN BRIEF WAS WRONG — CORRECTED BY MEASUREMENT

My brief said *"Four templates carry workarounds for it, plus an unnamed Transfer-list instance."*
Measured against the tree, the population is **3 + 4 + 1**, not 4 + 1:

| group | count | files | what they actually carry |
|---|---|---|---|
| carry the `.tpl-split-host` **workaround** AND use `.l-split` in markup | **3** | `Template-dashboard`, `Template-detail`, `Template-settings` | the WARN tier — the host worked, the split DID collapse |
| carry the **defect verbatim**, no workaround, and never use `.l-split` in markup at all | **4** | `Template-confirmation`, `Template-empty`, `Template-error`, `Template-report` | FAIL tier · dead CSS, no consumer |
| the Transfer-list instance | **1** | `Transfer-list` (`.tl`) | FAIL tier · **a LIVE, RENDERED defect** |

Probe: `grep -c "tpl-split-host" knowledge/snippets/*.reference.html | grep -v ":0"` → exactly 3 files.
`grep -c 'class="[^"]*l-split' knowledge/snippets/Template-{confirmation,empty,error,report}.reference.html`
→ **0** in all four. [[premise-ages-faster-than-rule]] — the brief's count was a reading, not a measurement.

---

## THE CLAIM TABLE (`s182-D1` — every mechanical claim carries its probeable token)

Environment for every render row: `PYTHONPATH=/var/tmp/pylibs`,
`PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s197`,
`LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu`, `TMPDIR=/var/tmp`
(the `_RUNBOOK-render-verify.md` n=6 recipe, reused read-only; **`/` is 100% full, `/sessions` has 7.0 G** —
that is the *inverse* of the runbook's usual ENOSPC shape and is recorded below).

| # | claim | probeable token | verdict |
|---|---|---|---|
| 1 | P-7 measured **6 findings + 3 WARN** before this lane | `python3 knowledge/_probe_registry/probe_container_self_query.py --check` → `P-7 … 6 finding(s) · 3 WARN-tier` / `PROBE P-7 — findings=6` | **DRIVEN** (baseline) |
| 2 | P-7 measures **0 findings + 0 WARN** after | same command → `135 file(s) … 0 finding(s) · 0 WARN-tier` / `PROBE P-7 — findings=0`, rc=0 | **DRIVEN** |
| 3 | P-7 still BITES — the green is not a blind harness | `python3 knowledge/_probe_registry/probe_container_self_query.py --selftest` → `✅ P-7 selftest PASS`, plant VERIFIED planted, removal green, WARN tier held, named-query precision held | **DRIVEN** |
| 4 | `.l-split` never collapsed at ANY width before the repair | drive `Layout-utilities.reference.html`, set `.l-split` width, read computed `grid-template-columns` + child rects — table A below. At **420px** it computed `116px 280px`, `STACKED=no` | **DRIVEN** |
| 5 | `.l-split` now collapses, and the breakpoint is EXACT | table A below: `761 → [457, 280] STACKED=no` · `760 → [760, 760] STACKED=YES` | **DRIVEN** |
| 6 | The repair changes NOTHING above the breakpoint | table A: 900/780/761 rows are **byte-identical** before and after (`596/280`, `476/280`, `457/280`) | **DRIVEN** |
| 7 | Layout-utilities' own demo caption ("has already collapsed") is now TRUE | natural read, no width injection, viewport 1400: the split inside `.frame.narrow` is `ownW=394`, `kids=[394,394]`, `STACKED=YES` (it was `90px 280px`, not stacked, at #210) | **DRIVEN** |
| 8 | Removing `.tpl-split-host{container-type}` does **not** regress the three templates | table B: dashboard/detail/settings at vp 420 give `kids=[388,388] STACKED=YES` **before AND after**; at vp 1400 `[776,280]` before AND after | **DRIVEN** |
| 9 | A repaired TEMPLATE collapses at the exact breakpoint | `Template-dashboard`, set `.l-split` width: `761 → [449,280] no` · `760 → [760,760] YES`; console errors **NONE** | **DRIVEN** |
| 10 | Transfer-list's `.tl` was a LIVE rendered defect | vp 420, before: `.tl` `ownW=340` (well under its 480 breakpoint), `flex-direction: row`, panel widths **`[54, 200, 54]`** — two 54-pixel panels | **DRIVEN** |
| 11 | Transfer-list now stacks, exact breakpoint, same measured width | vp 420 after: `flex-direction: column`, `[340,340,340]`, `STACKED=YES`. Edge: `481 → row [203,44,203]` · `480 → column [480,480,480]`. vp 1400 unchanged: `640` wide, `[282,44,282]` | **DRIVEN** |
| 12 | The standing gates stay green over the eight touched files | `_validate_snippets.py` rc=0 `135 snippet(s), 0 failure(s)` · `_validate_grid.py` rc=0 `GRID GATE PASS (151 file(s))` · `_validate_a11y.py` rc=0 `0 failure(s)` · `_validate_descender_clip.py` rc=0 `PASS` | **DRIVEN** |
| 13 | The type-composite shrink-only ratchet did not move | `_validate_type_composites.py` → `1097 violation(s)` — the exact #203-measured figure, unchanged | **DRIVEN** |
| 14 | No render stray landed in the tree | `ls -a knowledge/assets/fonts/_desktop/TTF/ \| grep -c '^\.uuid'` → `0`; `git status --short --untracked-files=all -- knowledge/ \| grep '^??' \| wc -l` → `0` | **DRIVEN** |
| 15 | **All nine showroom pages still carry the UNREPAIRED snippet** | decode the base64 `#payload` blob per page: `layout-utilities`/`template-{dashboard,settings,detail,confirmation,empty,error,report}` all `OLD-dead-rule=True, NEW-fix=False`; `transfer-list` `tl-OLDwidth=True, tl-frame=False` | **DRIVEN — and NOT repaired (fenced)** |
| 16 | P-7 is structurally BLIND to the showroom leg | P-7 `--glob 'showroom/*.html'` → `136 file(s) · 0 finding(s)` while claim 15 shows the defect IS in those files, inside base64 | **DRIVEN** |
| 17 | A **7th** live instance of the class survives, outside P-7's glob | P-7 `--glob 'reviews/*.html'` → `reviews/REVIEW-204-layout-utilities-four-themes-v1.html:119 .cn-layout-utilities .l-split { container-type }` … `1 finding(s)` | **DRIVEN — REPORTED, NOT TOUCHED** |

---

### TABLE A — `Layout-utilities.reference.html`, `.l-split` width driven across the 760px breakpoint

Two specimens per row (the top-level split and the one inside `.frame.narrow`); both agreed at every
width, so one line each is shown.

| container width set | BEFORE — computed cols | BEFORE — child widths | BEFORE stacked? | AFTER — child widths | AFTER stacked? |
|---|---|---|---|---|---|
| 900 | `596px 280px` | `[596, 280]` | no | `[596, 280]` | no |
| 780 | `476px 280px` | `[476, 280]` | no | `[476, 280]` | no |
| **761** | `457px 280px` | `[457, 280]` | no | `[457, 280]` | **no** |
| **760** | *(not sampled before)* | — | — | `[760, 760]` | **YES** |
| 759 | `455px 280px` | `[455, 280]` | no | `[759, 759]` | **YES** |
| 700 | `396px 280px` | `[396, 280]` | no | `[700, 700]` | **YES** |
| 500 | `196px 280px` | `[196, 280]` | no | `[500, 500]` | **YES** |
| **420** | `116px 280px` | **`[116, 280]`** | **no** | `[420, 420]` | **YES** |

⚠ **Read the `computed cols` column carefully, because it is the one honest surprise in this repair.**
After the fix the element still computes two tracks (e.g. `456px 280px` at 760). It collapses because
**every child spans `grid-column: 1 / -1`**, so no item ever sits in a single track and the rendered
result is a full-width stack. The old repair reset `grid-template-columns` to one track, so an
inspector used to see `388px`. **The rendered geometry is identical** — claim 8 proves it, child rect
for child rect — but anyone auditing by reading `grid-template-columns` alone will now read two tracks
and must not misread that as "still broken". *This is named here rather than smoothed over.*

### TABLE B — the three host-carrying templates, natural read, no injection

| file | vp | BEFORE `.l-split` kids / stacked | AFTER `.l-split` kids / stacked |
|---|---|---|---|
| `Template-dashboard` | 1400 | `[776, 280]` / no | `[776, 280]` / no |
| `Template-dashboard` | 420 | `[388, 388]` / **YES** | `[388, 388]` / **YES** |
| `Template-detail` | 1400 | `[776, 280]` / no | `[776, 280]` / no |
| `Template-detail` | 420 | `[388, 388]` / **YES** | `[388, 388]` / **YES** |
| `Template-settings` | 1400 | `[776, 280]` / no | `[776, 280]` / no |
| `Template-settings` | 420 | `[388, 388]` / **YES** | `[388, 388]` / **YES** |

**The host was never broken.** It was a correct workaround for a broken parent, and the numbers prove
the parent's repair carries the same result without it. **No visual change to any template.**

### TABLE C — `Transfer-list`, `.tl` across the 480px breakpoint

| frame width | BEFORE `flex-direction` | BEFORE panel widths | AFTER `flex-direction` | AFTER panel widths |
|---|---|---|---|---|
| 640 (natural, vp 1400) | `row` | `[282, 44, 282]` | `row` | `[282, 44, 282]` |
| 482 | — | — | `row` | `[203, 44, 203]` |
| **481** | — | — | `row` | `[203, 44, 203]` |
| **480** | — | — | **`column`** | **`[480, 480, 480]`** |
| 340 (natural, vp 420) | **`row`** | **`[54, 200, 54]`** | **`column`** | **`[340, 340, 340]`** |

---

## WHAT WAS CHANGED, FILE BY FILE

### 1 · `knowledge/snippets/Layout-utilities.reference.html` — **THE CAUSE**

```
WAS:  @container (max-width: 760px){
        .l-split{ grid-template-columns:minmax(0, 1fr); }
        .l-split[data-side="start"]{ grid-template-columns:minmax(0, 1fr); }
      }
NOW:  @container (max-width: 760px){
        .l-split > *{ grid-column:1 / -1; }
      }
```

`.l-split` declares `container-type:inline-size`, which makes it a query container **for its
descendants and for nothing else** — a `@container` rule resolves against the matched element's
nearest ANCESTOR container, and an element is never its own. The old rule was aimed at the one
element it could never match. The new rule is aimed at the split's **children**, for whom `.l-split`
*is* the nearest ancestor container, so it fires. One rule covers `data-side="start"` too: spanning
`1 / -1` collapses either track order. A ~16-line comment block above the rule carries the whole
diagnosis and the driven numbers in place.

**Why this shape and not a wrapper.** `.l-split` is a *utility class a consumer puts on their own
element*. Requiring a wrapper is a MARKUP CONTRACT, and it is exactly that contract which produced
three hand-rolled `.tpl-split-host` hosts and four silently-dead copies. The child-declaration shape
needs no wrapper, so **one file repairs every consumer**.

### 2–4 · The three workaround-carrying templates — workaround REMOVED

| file | removed | kept, deliberately |
|---|---|---|
| `Template-dashboard` | `.tpl-split-host{ container-type:inline-size; }` | the class + `.tpl-split-host > .l-split{ align-items:start; }` (composition rule 13, a real visual relationship) + the `<section aria-label>` element |
| `Template-detail` | same declaration | the class + rule 7's `align-items:start` + the `role="tabpanel"` element. **`.tl`'s own `container-type` is untouched** — different element, different query (360px) |
| `Template-settings` | same declaration | the wrapper `<div>` (see pitfalls). **`.tpl-setting-host` is untouched** — a different host for a different 460px query on `.tpl-section` |

Each file's `@container` block was updated to the fixed recipe. **`.tpl-split-host` and composition
rule 12 were SUPERSEDED IN PLACE, never deleted** — the #210 measurements (the `90px 280px`, the
`44px 280px`, the 26px clientWidths, the mutation control) are carried verbatim as history, with the
repair recorded above them. [[header-wins-over-audit]] / add-never-trim.

### 5–8 · The four dead-copy templates — fixed recipe, no consumer

`Template-confirmation` · `Template-empty` · `Template-error` · `Template-report` each got the same
`@container` replacement plus a comment naming what was there and why it could not fire. They are
faithful copies of the primitive and stay faithful copies. ⬛ **None of the four uses `.l-split` in
its markup**, so there is nothing to drive — this is UNPROVEN BY ABSENCE OF A CONSUMER, declared, not
smoothed (see pitfalls: they are dead CSS either way, and *deleting* them is a call I did not make).

### 9 · `knowledge/snippets/Transfer-list.reference.html` — the `.hv-frame` shape

```
WAS:  .tl{display:flex; … width:var(--demo-width, 640px); max-width:100%; container-type:inline-size;}
NOW:  .tl-frame{width:var(--demo-width, 640px); max-width:100%; container-type:inline-size;}
      .tl{display:flex; … width:100%;}
```
plus a `<div class="tl-frame">` wrapper around `<div class="tl" id="tl1">` in the markup.

⛔ **THE ASYMMETRY IS DELIBERATE AND IS NAMED, NOT HIDDEN.** `.l-split` got the child-declaration fix;
`.tl` got a wrapper. The reason is a CSS language fact, not a preference: `grid-column` is a **child**
property, so a grid's collapse *can* be expressed on the children. `flex-direction` is a **parent**
property and has no child-side equivalent, so `.tl` genuinely needs an ancestor container. The
wrapper carries `.tl`'s old width so **the 480px query measures exactly the number it always
measured** — table C's `481 → row` / `480 → column` is the proof it did not drift. This mirrors
Hero-variants' ruled `.hv-frame` (wave-5 lesson 3), which the P-7 docstring already cites as an
accepted repair shape.

⚠ Note the half-right symptom that made this one easy to miss: the `.moves{flex-direction:row}` leg of
the *same* query DID fire all along, because `.moves` is a descendant. Only the leg aimed at the
container itself was dead.

---

## P-7 BEFORE / AFTER, BY NUMBER

| | findings | WARN-tier | rc |
|---|---|---|---|
| **before** (baseline, and the brief's mint figure) | **6** | **3** | 1 |
| **after** | **0** | **0** | 0 |

The six findings cleared, each by name:
`Layout-utilities:242 .l-split` · `Template-confirmation:156 .l-split` · `Template-empty:143 .l-split` ·
`Template-error:145 .l-split` · `Template-report:190 .l-split` · `Transfer-list:90 .tl`
The three WARNs cleared: `Template-dashboard:263` · `Template-detail:168` · `Template-settings:169` —
all three were "`.l-split` self-queries but a `.tpl-split-host` may host it"; with the hosts gone and
the rule fixed there is no overlap left to report.

### Other probes, read at lane close (deltas ATTRIBUTED, never claimed)

| probe | mint (brief) | now | whose |
|---|---|---|---|
| `P-1` | 0 | 0 | — |
| `P-2` | 0 | 0 | — |
| `P-4` | 5 | **6** | **NOT MINE.** The +1 is `UNROWED-DOC notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md is named by no store row's home`. The brief was created after the mint; the probe names the repair itself (`one _state.add() row`) and calls it the conductor's. [[forgotten-document-class]] |
| `P-5` | 0 | 0 | — |
| `P-7` | 6 | **0** | **MINE** |
| `P-8` | 58 | **12** | **LANE R1's** (`gen_token_ramp`), not mine — reported so the conductor is not surprised by a number moving under an R2 receipt |
| `P-3`, `P-6` | NOT RUN (sandbox-render) | not run | lane R4's |

---

## `git status --short` AT LANE CLOSE — VERBATIM, EVERY PATH ATTRIBUTED

```
 M knowledge/_119-sweep-recheck.json
 M knowledge/_RADIUS-GATE.md
 M knowledge/_probe_registry/probe_dangling_var_pixel.py
 M knowledge/_probe_registry/probe_input_trim_enactment.py
 M knowledge/gen_token_ramp.py
 M knowledge/snippets/Button.reference.html
 M knowledge/snippets/Chart-butterfly-h.reference.html
 M knowledge/snippets/Date-picker.reference.html
 M knowledge/snippets/Drawer.reference.html
 M knowledge/snippets/Form-layout.reference.html
 M knowledge/snippets/Layout-utilities.reference.html
 M knowledge/snippets/Template-confirmation.reference.html
 M knowledge/snippets/Template-dashboard.reference.html
 M knowledge/snippets/Template-detail.reference.html
 M knowledge/snippets/Template-empty.reference.html
 M knowledge/snippets/Template-error.reference.html
 M knowledge/snippets/Template-list-index.reference.html
 M knowledge/snippets/Template-report.reference.html
 M knowledge/snippets/Template-settings.reference.html
 M knowledge/snippets/Transfer-list.reference.html
 M notes/_REHEARSAL-LOG.jsonl
 M notes/_dream/_GRADE-DECISIONS.jsonl
?? notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md
?? notes/_receipts/2026-08-21-211-wave1-laneR1-token-ramp.md
?? notes/_receipts/2026-08-21-211-wave1-laneR3-a11y-repairs.md
?? notes/_receipts/2026-08-21-211-wave1-laneR4-probe-hygiene.md
```

| path | owner |
|---|---|
| `knowledge/snippets/Layout-utilities.reference.html` | **R2 (mine)** |
| `knowledge/snippets/Template-{confirmation,empty,error,report,settings}.reference.html` | **R2 (mine)** |
| `knowledge/snippets/Transfer-list.reference.html` | **R2 (mine)** |
| `knowledge/snippets/Template-dashboard.reference.html` | ⚠ **CO-OWNED** — R1 (AUTO-TOKENS region) **and** R2 (`.l-split` region). Disjoint regions; both survive (`git diff` shows 6 AUTO-TOKENS/alpha hunks **and** 2 `l-split > *` occurrences) |
| `knowledge/snippets/Template-detail.reference.html` | ⚠ **CO-OWNED**, same shape, same verification |
| `knowledge/_RADIUS-GATE.md` | **R2 gate SIDE-EFFECT** — `_validate_radius.py` rewrites its own audit file on every run. Declared, never swept. See the finding below |
| `knowledge/{_119-sweep-recheck.json,gen_token_ramp.py}`, `knowledge/_probe_registry/probe_{dangling_var_pixel,input_trim_enactment}.py`, `knowledge/snippets/{Button,Chart-butterfly-h,Date-picker,Drawer,Form-layout,Template-list-index}.reference.html` | **wave 1 (R1/R3/R4)** — not touched by me |
| `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` | **wave 1 / gate side-effects** — not touched by me |
| `?? notes/_briefs/…wave1…`, `?? notes/_receipts/…wave1-lane{R1,R3,R4}…` | **wave 1** |
| `notes/_receipts/2026-08-21-211-wave2-laneR2-lsplit.md` | **R2 (this file)** — will appear as `??` once written |

**No commits. No `git checkout`. No `_build_all.py`.** No file outside the fence was edited.

---

## ⛔ A GATE WENT RED AND IT IS NOT MINE — the `_RADIUS-GATE` finding

Running `_validate_radius.py` (rc=1) rewrote `knowledge/_RADIUS-GATE.md` from the committed
**`## ✅ STRICT surfaces clean (canon + 81 migrated snippet(s))`** to
**`## ❌ STRICT failures (4)`** — four literal `border-radius:0` declarations in `canon/canon.css`:

```
canon/canon.css:11459  .cn-hero-variants .hv-media .img{… border-radius:0;}
canon/canon.css:11466  .cn-hero-variants .stat-card{… border-radius:0; …}
canon/canon.css:14428  .cn-stats-band-lockup .stat-card{… border-radius:0;
canon/canon.css:14439  .cn-stats-band-lockup .kpi-tile{… border-radius:0;
```
plus a new advisory: `snippets/Hero-variants.reference.html — 2 hardcoded declaration(s)`.

**Attribution, measured not assumed:** `git status --short -- knowledge/canon/canon.css
knowledge/_validate_radius.py knowledge/snippets/Hero-variants.reference.html` returns **nothing** —
gate, input and snippet are all **at HEAD**. So a fresh run of the committed gate over the committed
input disagrees with the committed audit. **The committed `_RADIUS-GATE.md` was already stale before
this session.** Both offending components (`Hero-variants`, `Stats-band-lockup`) were built at #210
wave-6 lane C, which is exactly the **regen-last-before-commit** class the hook already tracks
([[ritual-output-is-not-evidence]]). ⬛ **NOT MINE TO FIX** — `canon/canon.css` is outside my fence,
and both components sit on Dave's eye queue (`W-81`). **Priced to the conductor.**

I left the regenerated audit in the tree rather than reverting it: the brief says *declare, never
sweep*, and the regenerated file is the TRUE one.

---

## ⬛ PRICED RETURNS — things I did NOT settle

| # | item | why it is not mine | price |
|---|---|---|---|
| 1 | **P-7 promotion or park** | DO-NOT-RULE, human half: *"P-7 / P-8 promotion or park (registered ADVISORY #210 on his word; repair ≠ promotion)"* | Untouched. P-7 is still ADVISORY. It now reads 0/0 with a passing selftest, which is the strongest possible input to that decision, and nothing more |
| 2 | **9 showroom pages carry the unrepaired snippet** (claim 15) | regeneration needs the build; `_build_all.py` is HARD-FENCED for this lane | One regeneration pass in the conductor's serial. **Until then the repo holds two truths**: repaired snippets, stale showroom. ~30 min if chunked (`--range`) |
| 3 | **P-7 is blind to base64 showroom payloads** (claim 16) | a probe widening is a gate change; DO-NOT-RULE: *"ANY threshold, constant or count in gates (s208-D1 rider — a repair never dials a gate)"* | A `--glob 'showroom/*.html'` run is useless without a base64-decode step in `stylesheets()`. ~20 lines. **PRICED, NOT WIRED** |
| 4 | **A 7th live instance survives** — `reviews/REVIEW-204-layout-utilities-four-themes-v1.html:119` (claim 17) | review pages are Dave's eye queue (*"do not touch, do not improve"*), and outside P-7's ruled glob [[gate-glob-scope-rule]] | Dave's call whether review artefacts are in scope for repair at all. **REPORTED, NOT TOUCHED** |
| 5 | **`_RADIUS-GATE` red on `canon/canon.css` ×4 + Hero-variants advisory ×2** | outside my fence; both components are on `W-81` | Conductor's triage. Genuinely pre-existing |
| 6 | **`P-4` +1 unrowed-doc** for the wave-1 brief | the probe itself names it as the conductor's | One `_state.add()` row |
| 7 | **`Template-settings`'s now-inert `<div class="tpl-split-host">`** | removing a DOM wrapper can change flex/grid item counts and gap participation in its parent; I judged the visual risk higher than the tidiness gain | Cosmetic. If wanted, delete the div + its `</div>` and re-drive table B's settings rows. ~5 min |
| 8 | **The four dead `.l-split` copies with no consumer** | deleting a primitive's recipe from a template is a composition decision, not a repair | They are now *correct* dead CSS instead of *broken* dead CSS. Whether Layer-2 templates should carry unused primitives at all is a real question and it is Dave's |
| 9 | **The breakpoint scale** (760px, 480px) | DO-NOT-RULE: *"the breakpoint scale (unruled; three shells carry three unruled pairs)"* | **Every literal in this repair is the one that was already there.** No number was changed, invented or moved |

---

## ⛔ CONSEQUENCES / PITFALLS — mandatory (Dave #165)

**What this repair does NOT fix.**
1. **The showroom.** Nine pages still render the broken layout to anyone who opens the showroom today
   (claim 15). The repair reaches the *snippets*; the *product surface* is stale until a build runs.
   **If the conductor commits without regenerating, the tree ships a repaired source and a broken
   artefact, and every gate stays green over the pair.** This is the single highest-consequence item
   on the page.
2. **The review page** (claim 17) is unrepaired and outside the probe's glob.
3. **The four consumer-less copies** are unproven by absence of a consumer, not by measurement.
4. **`grid-template-columns` still reads two tracks** after collapse. An auditor reading that property
   instead of the rendered geometry will get a false negative. Table A's warning exists for that reader.

**What could recur, and the class it belongs to.**
- **The class is [[no-gate-parses-the-artefact]], and it is not closed.** P-7 catches the *exact
  selector-string* overlap only — its own docstring declares it blind to `@container{ .a .b{} }`
  against `.b{container-type}`, to the DOM, to split `container-name`, to cross-file containers, and
  (measured today, claim 16) to base64 payloads. **The same defect written slightly differently is
  still invisible.** The only thing that actually caught this shape *as rendered* was driving a
  browser and reading child rectangles.
- **The copy-paste primitive is the real generator.** `.l-split` exists in **eight** files as eight
  independent copies of the same text. One defect became eight. My repair edited all eight by hand
  and *that is the same mechanism that spread it*. Until a template consumes the primitive rather
  than transcribing it, the next primitive-level defect propagates identically. [[gate-dont-patch]] —
  the class fix is composition, not a gate, and it is unbuilt and unpriced here.
- **A workaround that WORKS hides the cause indefinitely.** The three `.tpl-split-host` hosts were
  correct, driven, and green (table B) — which is precisely why the parent stayed broken for a whole
  session. The #210 lane did the right thing and wrote *"⬛ THE REAL REPAIR IS DAVE'S"*, and the note
  then sat. **A workaround should carry an expiry, not just an owner** ([[conclusions-are-debt-s129-d5]]).
- **The `.moves` half-fire is the nastiest tell in this whole class.** In Transfer-list, one leg of the
  query fired and one did not, so the page looked *partly* responsive. A reviewer's eye reads "the
  breakpoint works" from the leg that fires. Half-firing is more dangerous than not firing.
- **Gate side-effects double as findings.** Running one blocking gate for reassurance surfaced a
  pre-existing red that had been committed as green. Worth the conductor's attention as a pattern:
  *the audit files in this repo are only as fresh as the last person who ran the gate.*

---

## DRIVEN vs UNPROVEN — the honest ledger

**DRIVEN** (real browser, real geometry, both sides of every breakpoint): the Layout-utilities
primitive (2 specimens × 8 widths, before and after); `Template-dashboard` at the exact 760/761 edge;
all three host-carrying templates before/after at 2 viewports; `Transfer-list` at the exact 480/481
edge and at 2 natural viewports; console errors NONE on both driven pages.

**MUTATION CONTROL** — the "can this test fail?" arm is not synthetic here: **the BEFORE column of
every table IS the mutation**, taken on the real unmodified file. `.l-split` produced `[116, 280]
STACKED=no` at 420px and `.tl` produced `[54, 200, 54] flex-direction:row` at 340px. The probe's own
`--selftest` independently confirms P-7 still bites with a VERIFIED plant [[mutation-tests-the-clause-not-the-feature]].

**UNPROVEN, each a priced TODO, none smoothed:**
- The four consumer-less templates: **no rendered proof possible** — nothing in their markup uses
  `.l-split`. Text-level parity with the repaired primitive is all that is claimed.
- **Themes:** every drive was `data-theme="light"` default. The repair touches `grid-column` /
  `flex-direction` / `container-type` only — no colour, no token, no type — so per-theme re-drive was
  judged unnecessary. That is a JUDGEMENT, declared, not a measurement.
- **Dark mode / the other three themes:** not driven, same reasoning.
- **Font fidelity:** the HSBC-cut canvas probe was **not run**. This lane measured element geometry
  (`getBoundingClientRect`, `getComputedStyle`), which is font-independent for grid tracks and flex
  direction. Declared per the runbook rather than quietly skipped.
- **`Template-detail`'s `.tl`** (its own 360px query, a different element) was neither flagged by P-7
  nor touched; it reads `kids=[726]` / `[338]` before and after, i.e. unchanged.

---

## ENVIRONMENT NOTE FOR THE RUNBOOK (offered, not inscribed)

`_RUNBOOK-render-verify.md`'s ENOSPC potholes n=3…n=6 all describe **`$HOME`/`/sessions` full, `/` with
room**. Today it was **inverted**: `/` at **100% (75 M avail — treat as zero, per pothole n=6)** and
`/sessions` at **25% (7.0 G free)**. The n=6 recipe still worked *because it reuses `/var/tmp` farms
read-only* (`pylibs` playwright 1.62.0, `pw-browsers-s197`, `chromelibs`) and writes nothing there —
`TMPDIR=/var/tmp` carried a headless-shell launch fine on 75 M. Scratch went to `$HOME/r2/`, **outside
the repo mount**, which is why claim 14 reads zero strays. ⬛ Offered to the conductor as a runbook
addition; **not inscribed by this lane** (the runbook is not in my fence).

---

## SUB SPEND

⛔ **UNMEASURED, and I will not default it.** I cannot read my own usage meter from inside a lane, and
`knowledge/_checkin.py` reads the *conductor's* transcript, not a sub's — running it would also append
to `notes/_REHEARSAL-LOG.jsonl`, a rolling file wave 1 has already dirtied, muddying attribution for
no gain. [[measuring-tool-must-not-guess]]: UNKNOWN is never defaulted.
**The conductor should take this lane's figure from its own `message.usage` for the R2 spawn**, which
is the REAL number [[boot-measurable-via-usage]]. Measurable proxies, if useful: ~30 tool calls,
9 files edited, 5 browser-driven measurement passes, 6 gates + 6 probes run, no full-file reads of any
snippet (targeted `sed`/`grep` ranges throughout).
