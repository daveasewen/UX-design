# Receipt — #210 Wave 5 · Lane D · Lock-ups (Sonnet)

**Lane:** D (Sonnet) · **Session:** #210 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-210-wave5-layer2-p2-fanout-brief-v1.md` (THE JOB, Lane D)
**Members:** itinerary row 115 (Page-header-lockup) · row 120 (Filter-toolbar-bar)

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Both lock-ups are PROPOSED, not ruled. No registry,
> `MIGRATED_SNIPPETS`, `CATEGORIES`, spine, canon.css, `_rulings.json` or git operation was
> touched — the serial set is the conductor's. This lane created NEW FILES ONLY, plus this
> receipt and its store row.

---

## 0 · THE JOB, RESTATED

Layer-2 rows 115/120 carry `derived: NO-ARTEFACT-CLASS` in the itinerary — no shell/template/
lock-up artefact class exists in the store. Per the wave-5 brief's ARTEFACT CLASS convention,
each ships as `knowledge/snippets/<Name>.reference.html` + `knowledge/components/<name>.meta.json`
with `"layer"` (and, since the schema's `additionalProperties:false` has no `layer` key, also
`"$layer"` so schema validation and the brief's own instruction both hold — declared, not
silent). **THE CARDINAL RULE: COMPOSE, NEVER RE-DRAW.** Every visible atom in both files traces
to an existing gated/proposed `knowledge/snippets/*.reference.html` source, borrowed verbatim
and diff-proven below.

---

## 1 · FILE LIST — four new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/Page-header-lockup.reference.html` | 27,997 |
| 2 | `knowledge/components/page-header-lockup.meta.json` | 5,715 |
| 3 | `knowledge/snippets/Filter-toolbar-bar.reference.html` | 27,847 |
| 4 | `knowledge/components/filter-toolbar-bar.meta.json` | 5,494 |
| 5 | `notes/_receipts/2026-08-20-210-wave5-laneD-lockups.md` | this file |

**No existing file was edited.** Renders used during the build live OUTSIDE the repo
(`NON-REPO: the session outputs folder, w5d_renders/*.png` — 12 PNGs, light+dark × 3 widths ×
2 files) per `s191-D2` home-or-declare; they are working artefacts, not deliverables.

---

## 2 · COMPOSITION — what was borrowed, from where, and what was arrangement-only

**Page-header-lockup.reference.html** (itinerary row 115) composes, verbatim:
`Breadcrumbs.reference.html` (`.crumb`/`.sep`/nav), `Eyebrow.reference.html` (`.eyebrow`),
`Tabs.reference.html` (`.tablist`/`.tab`/`.indicator`/`.overflow*` **and its own unedited
ResizeObserver JS**), `Button.reference.html` (`.btn` + 4 tiers + press-physics partial),
`Badge.reference.html` (`.badge`, standalone form). Three arrangement variants: **A** simple
(eyebrow+title+actions), **B** breadcrumb+title+Tabs, **C** eyebrow+title+badge+meta+actions.

**Filter-toolbar-bar.reference.html** (itinerary row 120) composes, verbatim:
`Search-field.reference.html` (`.search`/`.mag`/`.clear`, boxed), `Dropdown.reference.html`
(`.dd`/`.trigger`/`.menu`/`.opt`, boxed), `Segmented-control.reference.html` (`.seg`/`.ind`,
**the 2026-07-24 promotion off View-options — this bar consumes Segmented-control, not the
superseded file**), `Tags.reference.html` (`.tag`/`.x`/`.filterbar`, incl. its own container-query
collapse). Two density variants: **A** full toolbar (search+2 dropdowns+view switch+applied-filter
chips), **B** compact (underline search + sm segmented control, "above a table/list" — the
itinerary row's own stated context).

The ONLY new CSS in either file is the `.ph-*`/`.ftb-*` arrangement layer (flex containers,
container queries) — the Meter organism precedent (`Meter.reference.html`, ruled #210): an
organism's own rules are arrangement only, zero new visual vocabulary. **s210-D3 discipline is
carried through**: neither `.ph-*` nor `.ftb-*` declares a width; `.demo-*` classes are demo
chrome only, deletable without changing the component.

**Two declared deviations from byte-for-byte verbatim**, both stated in the files' own banners:
1. Badge's `--surface`/`--number`/`--host` custom properties are renamed
   `--badge-surface`/`--badge-number`/`--badge-host` in Page-header-lockup, because Button's own
   `--surface` (unused demo-chrome var, dropped from this composition) would otherwise collide in
   *meaning* with Badge's `--surface` if both were merged under one name. VALUES are unchanged.
2. Several raw `font`/`font-weight`/`font-size` declarations present in the SOURCE atoms
   (Breadcrumbs' `nav ol`, Tabs' `.tab`/`.overflow__trigger`/`.ovcount`, Dropdown's
   `.trigger`/`.opt`, Tags' `.tag`) are **not** reproduced in this lane's copies — see §4.

---

## 3 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | Both files' visible atoms are gated/proposed sources, not re-drawn | manual diff: every non-`.ph-*`/`.ftb-*`/`.demo-*` CSS selector name (`.crumb`,`.tab`,`.btn`,`.badge`,`.search`,`.dd`,`.seg`,`.tag`, …) appears verbatim in its named source file — see §2 | ✅ |
| 2 | The Tabs JS in Page-header-lockup is unedited | `diff <(sed -n '/function positionIndicator/,/requestAnimationFrame(fit)/p' knowledge/snippets/Tabs.reference.html) <(sed -n '/function positionIndicator/,/requestAnimationFrame(fit)/p' knowledge/snippets/Page-header-lockup.reference.html)` → differs only in scoping (`document.` → `scope.`, required to run 1 instance per `.tabs-b` wrapper on a page that may host more than one Tabs region) and the removed second no-op `panelOf` line; selection/keyboard/overflow logic is byte-identical | ✅ |
| 3 | The Dropdown/Segmented-control/Tags JS in Filter-toolbar-bar is unedited | same technique: `wireDD`, `moveInd`/`placeAll`, and the dismiss handler are copied with zero logic changes (only re-pasted, not rewritten) | ✅ |
| 4 | The leading-trim block is the CURRENT one, byte-identical to Command-palette line 36 | `python3 -c "cp=open('knowledge/snippets/Command-palette.reference.html').read().split(chr(10))[35]; print(all(cp in open(f).read() for f in ['knowledge/snippets/Page-header-lockup.reference.html','knowledge/snippets/Filter-toolbar-bar.reference.html']))"` → **True** | ✅ |
| 5 | No colour invented; two-red law + mono error ink camp untouched | `grep -nE '#[0-9A-Fa-f]{6}' knowledge/snippets/{Page-header-lockup,Filter-toolbar-bar}.reference.html \| grep -vE '#F6604C\|#1A1A1A\|#FFFFFF\|#000000\|#E1E1E1\|#808080\|#305A85\|#4587A7\|#F0F0F0\|#232323\|#626262\|#484848\|#313131\|#FAFAFA\|#B2B2B2\|#9D9D9D\|#333333\|#767676\|#B7B7B7\|#66CC8D\|#D7D8D6\|#404040\|#212121\|#474747\|#F3F3F3\|#E1E1E1\|#000000D9\|#00000033\|#FFFFFF00\|#1F1F1F'` → **0 lines** (every hex is a value already carried by the borrowed atom's own manifest) | ✅ |
| 6 | Type-composite ratchet: 0 new violations (debt may not grow, DO-NOT-RULE) | `python3 knowledge/_validate_type_composites.py --ratchet` → **"TYPE RATCHET PASS — declared debt holds at 1097 (0 new)."** (BEFORE the fix pass: 1117, +20 new — see §4 for what was fixed and how) | ✅ |
| 7 | Snippet/token gate clean on both | `python3 knowledge/_validate_snippets.py 2>&1 \| grep -c "Page-header-lockup\|Filter-toolbar-bar"` → **0** | ✅ |
| 8 | a11y gate: 0 failures with both present | `python3 knowledge/_validate_a11y.py` → *"a11y gate: 114 snippet(s), 0 failure(s), …"* | ✅ |
| 9 | 4px-grid gate clean | `python3 knowledge/_validate_grid.py` → *"GRID GATE PASS — all layout dimensions on the 4px grid (130 file(s))."* | ✅ |
| 10 | Descender-clip gate passes | `python3 knowledge/_validate_descender_clip.py` → *"DESCENDER-CLIP GATE PASS … (130 file(s))."* | ✅ |
| 11 | Both metas are schema-valid | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → *"111 meta(s) checked · 0 finding(s)"* | ✅ |
| 12 | ⛔ binds-resolve check-D FAILS for both — DECLARED, not hidden | `python3 knowledge/_validate_binds_resolve.py` → *"108/114 canon blocks · 6 failure(s)"*, naming `Page-header-lockup`, `Filter-toolbar-bar` (+4 sibling-lane files) — no `.cn-page-header-lockup`/`.cn-filter-toolbar-bar` block exists in canon.css yet | ⛔ **CONDUCTOR'S** |
| 13 | Zero horizontal overflow at 3 widths × 2 themes × 2 files, driven | headless Chromium (`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage --disable-gpu`), widths 1400/700/340, both `data-theme`s: `document.documentElement.scrollWidth - clientWidth` → **0 in all 12 combinations** | ✅ **DRIVEN** |
| 14 | The responsive collapse actually happens, not just "no overflow" | at 340px: Page-header arrangement A's actions fall to their own full-width row; arrangement B's breadcrumb wraps and **Tabs' own overflow shows "More 4"** (its unmodified logic, live); Filter-toolbar arrangement A stacks every control full-width and the chip row goes one-per-row (Tags' own ≤360px rule, live) — all **screenshotted and looked at**, see §5 | ✅ **DRIVEN** |
| 15 | The composed interactions actually work | driven: Tabs tab-2 click → `aria-selected="true"` + indicator repositions (`left:111px`); Dropdown trigger click → `aria-expanded="true"`, option click → `.ddval` text updates to the chosen option; Segmented-control button click → `aria-pressed` flips to the clicked button only | ✅ **DRIVEN** |
| 16 | ⚠ Tag dismiss: the class is applied, DOM removal did not complete in headless — same as the untouched source | driven: clicking `.tag .x` adds class `removing` (confirmed via `className` read) but the element is not removed after 1.1s; **re-ran the identical probe against the UNTOUCHED `Tags.reference.html` and got the same result** (`before 3, after 3`) — a headless-`transitionend` rendering quirk pre-existing in the source, not introduced by this composition | ⚠ **DECLARED, pre-existing** |
| 17 | Tag dismiss hit target — visible box vs the invisible ≥24×24 target | driven: visible `.x` box measured **20.47×20.47px**, matching Tags' own em-based sizing (`1.54em` at 14px caption composite ≈ 21.6px CSS, browser rounds); the `::before` invisible target (24×24, WCAG 2.5.8) is present verbatim from source — untouched | ✅ |

---

## 4 · THE TYPE-RATCHET FIX — found by RUNNING the gate, not by inspection

**First draft measured 1117 violations (+20) against the frozen 1097 baseline — the ratchet
FAILED.** Composing an atom into a NEW file duplicates whatever raw (non-composite) font
declarations that atom's OWN file still carries (Breadcrumbs/Tabs/Dropdown/Tags all still have
some — that debt is part of the existing 1097, unrelated to this lane). The fix, verified with
`python3 knowledge/_validate_type_composites.py --ratchet` after each pass:

1. **Four selectors were REDUNDANT inventions** — `.btn`, `.badge`, `.search input`, `.seg
   button`/`.seg.sm button` never carry a raw font in their SOURCE files at all, because
   `canon/type.css` already appends those exact selectors to its `.t-cm-button`/`.t-cm-caption`/
   `.t-cm-label`/mini-ctl-ramp composite lists (T-D9). This lane's first draft had (wrongly)
   copied a `font:` shorthand into those rules anyway. Deleting it matches the source exactly.
2. **Genuinely inherited raw declarations** (Breadcrumbs' `nav ol`/`[aria-current]`, Tabs'
   `.tab`/`.overflow__trigger`/`.ovcount`, Dropdown's `.trigger`/`.opt`, Tags' `.tag`) were
   removed from the CSS and replaced with an EXISTING composite class added directly to the
   markup (the same technique `Carousel.reference.html` already uses: `class="ttl
   t-cm-heading"`) — `t-cm-caption` (14/400) for the breadcrumb `<ol>`, `t-cm-ctl-14` (14/500)
   for the current crumb and `.opt`'s tick-carries-the-selected-signal simplification, `t-cm-
   button` (16/500) for Tabs/overflow-trigger/Dropdown-trigger, `t-cm-ctl-12` (12/500) for the
   tab-overflow count badge (added inside the JS template string that builds it), `t-cm-label`
   (16/400) for Dropdown options, `t-cm-caption` (14/400) for Tags chips.
3. **One deliberate simplification, declared**: `.opt[aria-selected="true"]{font-weight:500;}`
   was dropped rather than composited — selection is already signalled by the `.tick` checkmark +
   `aria-selected` (not colour alone, 1.4.1 already satisfied); adding a second emphasis channel
   was not required to keep the meaning.
4. `.dd > label` was dropped entirely — the label is `sr-only` (inline-styled) in this bar, so no
   visible font rule was needed for it.
5. `.cap` (demo captions under each arrangement's heading) was renamed `.demo-note` — it matches
   the gate's own `CHROME_SEL` exemption pattern (`\bdemo-`), the same convention
   `Segmented-control.reference.html` already uses for its own `.demo-note`, and it genuinely is
   page annotation, not component text.

After the fix: **0 new violations, ratchet PASS, debt holds at 1097.**

---

## 5 · WHAT WAS DRIVEN — a real browser, light AND dark, 3 widths, both files

Headless Chromium (`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage
--disable-gpu`; system libs installed user-local via `apt-get download` per
`_RUNBOOK-render-verify.md` §4, no root). Widths **1400 / 700 / 340**, both `data-theme`s, both
files — **12 full-page screenshots taken and looked at** (home:
`NON-REPO: session outputs, w5d_renders/*.png`). Zero horizontal overflow measured in all 12.
Interactions driven live: Tabs selection + indicator, Dropdown open/select, Segmented-control
press state, Tag dismiss (class applied; DOM removal is a pre-existing headless quirk, §3 claim
16). No defect was found by looking beyond what §3/§4 already name — unlike #204/#209, this pass
did not surface a NEW visual defect the gates missed, which is itself worth stating plainly
rather than padding the receipt with a manufactured one.

---

## 6 · EVERY OPEN DESIGN QUESTION — NAMED, NOT SETTLED

**All of these are Dave's.**

### Q1 — Should the three Page-header-lockup arrangements be one flexible component or three named ones?
Drawn as one organism with an `arrangement` prop (A/B/C) rather than three files, on the theory
that a real page picks ONE shape per screen type and a designer should be able to see all three
options together. If Dave wants them split, the split is mechanical (each `.ph-outer .ph` block
is already self-contained).

### Q2 — Does Page-header-lockup ever need a SECOND action beyond "primary + one other"?
Only 2-button rows are drawn (arrangements A/B/C all show exactly 2). A row with 3+ actions would
need its own overflow treatment (echoing Tabs' "More") that nothing here builds — undrawn,
unscoped.

### Q3 — Filter-toolbar-bar's dropdown count: is 2 filters the right default, or should it be N?
Drawn with exactly 2 (Account, Date range) in arrangement A. `filterCount` is named as a prop in
the meta but the reference only shows the 2-filter case; a 3+ filter row's wrap behaviour at
680px is UNDRAWN.

### Q4 — Should the compact toolbar (arrangement B) ever carry filter dropdowns, or is it
search+sort only by definition?
Drawn as search+sort only, matching the itinerary row's own note ("Above tables/lists" — implying
a dense, secondary bar). If a dense row needs a filter too, that composition is undrawn.

### Q5 — ⛔ `role="progressbar"` vs `role="meter"` — NOT touched here, but the same "what's the
right ARIA primitive for a non-standard composite" question recurs for Tags-as-filter-chip. Tags
already ships with a plain `aria-label` per dismiss button (no group role wraps the applied-filter
row). Whether the chip ROW itself should carry `role="group"` with a label like "Applied filters"
is UNDRAWN and untouched by this lane (Tags.reference.html's own accessibility section doesn't
call for it either).

### Q6 — Segmented-control's `aria-label` in the toolbar ("View as" / "Sort by") — is that the
right accessible name pattern for a toolbar-embedded instance, or should the toolbar itself
provide the labelling context (e.g. via `aria-describedby` back to the search field)?
Drawn with the SAME per-instance `aria-label` pattern Segmented-control's own reference file
uses — no new pattern invented, but not specifically validated against a toolbar's landmark
structure.

### Q7 — The tag-dismiss headless quirk (§3 claim 16) — is `transitionend` reliability a real
production risk, or purely a headless-testing artefact?
**Declared UNPROVEN either way** — this lane only confirmed the SAME behaviour occurs in the
untouched source `Tags.reference.html`, so it is not new to this composition; whether a real
(non-headless) browser completes the dismiss animation was not independently re-verified this
session (§7 residual 3).

---

## 7 · WHAT STAYS UNPROVEN

1. **The canon-block projection.** `_validate_binds_resolve.py` check D FAILS for both
   (`.cn-page-header-lockup`, `.cn-filter-toolbar-bar` do not exist in `canon.css`) — 6 failures
   total in that gate run, shared with 4 sibling-lane files from the same wave. Until the
   conductor projects those blocks, **Console, Legacy and Supercharge are UNPROVEN for both
   lock-ups** — only the light/dark legs authored in each snippet have been seen.
2. **`_validate_kg.py`** was not re-run this lane (no new context/pattern names were introduced
   beyond what the four consumed atoms already carry, so no new node is expected, but this was
   not independently re-measured).
3. **Tag-dismiss `transitionend` in a real (non-headless) browser** — §3 claim 16 / §6 Q7.
4. **Hit-area gate (`_validate_hit_area.py --all`)** did not complete in this environment
   (browser-dependent invocation errored on a bare re-run without the LD_LIBRARY_PATH env
   re-exported in that specific call) — the dismiss-button hit area was instead verified by
   direct browser measurement (§3 claim 17), which is a narrower but real substitute, not
   equivalent to the gate's own full sweep.
5. **Only 3 widths were driven** (1400/700/340), and only ONE browser engine (headless
   Chromium), matching the #209 Lane A precedent's own declared limit.
6. **Nothing here has been seen by Dave**, and nothing is registered anywhere (no
   `MIGRATED_SNIPPETS`, `CATEGORIES`, `component-types.json`, `gen_showroom.py`,
   `gen_kg_edges.py` entry, `canon.css` block, or `_rulings.json` row).

---

## 8 · HANDOFF TO THE CONDUCTOR

1. `.cn-page-header-lockup`, `.cn-filter-toolbar-bar` blocks in `canon/canon.css` (clears 2 of
   the wave's 6 check-D failures).
2. Re-run `gen_kg_edges.py` if these two are kept (residual 7.2).
3. `component-types.json` · `CATEGORIES` · `gen_showroom.py` · `_validate_radius.MIGRATED_SNIPPETS`
   registrations, if kept.
4. **Q1 (biggest structural question)**: split Page-header-lockup's 3 arrangements into 3 files,
   or keep the single `arrangement`-prop organism? Affects how a future generator selects it.
5. This receipt's own store row (`W-75`, added at creation per the #185 forgotten-document
   class — see the wrap chain).
