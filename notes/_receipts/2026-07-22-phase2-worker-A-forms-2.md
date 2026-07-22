# Worker A receipt №2 — Phase-2 wave 2 · FORMS & ENTRY lane CONTINUATION (items 5–9)

*2026-07-22 evening (date from `date`). Fable worker per `_RUNBOOK-parallel-conductor.md` — NEW files
only, NO commits made (HEAD verified `6e2dd56` at close), no writes to handoff files or shared
registries. Brief: `notes/_briefs/2026-07-22-phase2-worker-A-brief.md` (items 5–9). Wave-1 receipt
(items 1–4) = `2026-07-22-phase2-worker-A-forms.md` — ratified, untouched.*

## Landed — 5 of 5. ★ THE BRIEF IS COMPLETE (9/9 across two windows)

| # | Component (row) | Files (all NEW) |
|---|---|---|
| 5 | **Date picker** (14) | `knowledge/snippets/Date-picker.reference.html` + `knowledge/components/date-picker.meta.json` |
| 6 | **Date-range picker** (15) | `knowledge/snippets/Date-range-picker.reference.html` + `knowledge/components/date-range-picker.meta.json` |
| 7 | **Time picker** (16) | `knowledge/snippets/Time-picker.reference.html` + `knowledge/components/time-picker.meta.json` |
| 8 | **File upload** (18) | `knowledge/snippets/File-upload.reference.html` + `knowledge/components/file-upload.meta.json` |
| 9 | **Stepper** (interactive) (34) | `knowledge/snippets/Stepper.reference.html` + `knowledge/components/stepper.meta.json` |

## ⚠ VERIFICATION STATE — moving tree (attribute-the-diff, wave-1 endgame repeated)

**Workers C (Data-grid) + D (Charts: Chart-bar, Chart-line…) were landing in parallel THROUGHOUT this
window** — global `_build_all` red is attributable to their in-flight files at every red I saw
(their meta schemas · Chart-bar icon UNKNOWNs · `.seg button` blast escape · Chart-line 14px margin),
and their own builds regenerated shared reports under me repeatedly.

**My proof per component:** Date-picker landed on a QUIET tree — full serial `_build_all` **green,
51 steps, zero fails** (buildA4, before C/D appeared). Every later component: (a) regenerated
cascade + showroom, ran full `_build_all`; (b) every failure line naming MY files was fixed
same-minute and re-run clean; (c) at close, the three contested gates run DIRECTLY
(`_validate_coverage` · `_validate_grid` · `gen_snippet_tokens --check`) name **zero** of my five
basenames; icon audit rows = ✅ verified ×4 + ✅ ·5 bespoke (Time-picker's Dropdown ticks);
integrity PASS with all 5 metas schema-valid; **partials ratchet: 0 strict, census 32→32 — my lane
added ZERO press-shaped locals.** The conductor's final serial build remains the authoritative green.

## Registry proposals — conductor only (`component-types.json` `$members`, button-family)

```json
"Date-picker":       { "selector": ".dp-nav" },
"Date-range-picker": { "selector": ".dr-nav" },
"File-upload":       { "selector": ":is(.fu-browse, .fu-remove)" },
"Stepper":           { "selector": ".st-nav button" }
```

- All four snippets carry the empty AUTO-PARTIAL marker pair + `--spring`/`--press` byte-equal to
  Button's + `transform var(--spring)` in the control transition + manifest binds for
  `--press-travel`/`--press-darken` + per-theme declarations (2 / 0.94).
- **`--phys-size`:** `.dp-nav`/`.dr-nav` = **44** (Icon-button geometry, declared on the control
  rule) · `.fu-browse` = **120** · `.fu-remove` = **24 LOCAL** (the wave-1 mixed-size idiom —
  smaller control carries its own) · `.st-nav button` = **120**.
- **`Time-picker`: deliberately NO entry** — zero pressables (tail-btn follows Input-fields, which
  is not a member; list options are selection targets). No markers in the file.
- Unregistered empty markers again proved inert across many green gate runs (wave-1 finding holds).

## MIGRATED_SNIPPETS basenames (radius strict from birth — all bind role tokens only)

`Date-picker.reference.html` · `Date-range-picker.reference.html` · `Time-picker.reference.html` ·
`File-upload.reference.html` · `Stepper.reference.html`
(control everywhere; + surface on the three overlay panels; + indicator on Stepper's track.)

## Showroom category proposal

All five → the same forms bucket as wave 1 (Input-fields category / the proposed **"Forms & entry"**).
Stepper arguably belongs beside Progress-tracker if a Navigation/Progress bucket is cut — Dave's
re-bucket call (B-Q7) covers it.

## Judgment calls (per component)

5. **Date-picker** — NO calendar-panel prior art anywhere (surveyed snippets + _proforma: only the
   Input-fields tail-btn + sprite glyphs) — panel composed from surveyed parts: Input-fields field
   anatomy (via my wave-1 Form-layout restatement), Popover's anchored-elevation recipe, Icon-button
   44×44 nav geometry, chevrons/dbl-chevrons byte-matched from the Tranche-3 sprite. **Selected day
   = ink knockout** (bg `text/default` + numeral `background/default` — the tooltip precedent from
   gated Form-layout/Input-fields); **today = structural ring + `aria-current=date`** (never
   colour-alone). Cells 40×40/4px gap on the grid; week starts Monday (en-GB); typing free +
   blur-validation (acd-019: panel opens from the tail button ONLY). Roving-tabindex grid, month
   paging at the edges, PageUp/Down ±month, +Shift ±year.
6. **Date-range-picker** — extends Date-picker same-session: one shared panel, TWO bound fields in
   the Form-layout pair row. **Range protocol = restart-on-earlier-pick** (banking convention,
   recorded in meta as reference behaviour); endpoints = ink knockout, between = `form/background/
   hover` tint, **no new colour minted**; every cell's aria-label states its range role + a polite
   region announces progress (tint never the only channel). Cross-field rule errors the To field:
   "Enter an end date after the start date."
7. **Time-picker** — pattern chosen BY CONTROL TYPE: a time picker IS a listbox → consumed
   DROPDOWN's list language (menu chrome, 44px options, selected = weight 500 + its data-bespoke
   neutral tick, same reason string) — deliberately NOT the grid knockout. 48 half-hour slots,
   opens scrolled to selected-else-nearest-to-now; slot column = `.t-cm-figure-5` tabular so it
   aligns. 24-hour only (meta antiPattern: AM/PM ambiguity costs money).
8. **File-upload** — dropzone (dashed `form/border/default` → solid active + hover fill on
   drag-over; same field-chrome tokens). **Per-file determinate progress bar built inline: track =
   `form/background/hover`, fill = `text/default` INK — "progress is STRUCTURE, not status" (R-D22
   spirit); NO determinate indicator existed anywhere** (Loading-indicator is spinner-only; loader
   atom queued to §C·4b and NOT minted, per brief). Browse = secondary ladder; remove = the 24px
   close idiom (Toast/Banner precedent) with 36px extended hit target. Oversize files stage as
   error rows with suggestive ink copy. Nothing auto-submits.
9. **Stepper** — Progress-tracker's reworked visuals CONSUMED (28px dots · 4px/top-12 connector ·
   yes.svg done-check · 3px current ring · 1784-86051 collapse at the same 520px container query);
   interactive deltas only: **done dots become real buttons** (back-navigation; future steps NEVER
   clickable — gate integrity), panels with programmatic focus to each new heading, **step-2
   validation gate** in the Input-fields language (empty Next → error + focus, no advance).
   Back/Next = the journey's REAL actions → primary + quaternary ladder (Form-layout action bar),
   not PT's outlined demo nav. Consumed PT's state weight-shifts (.dot 500 · current label 500 ·
   count 500) on composite-bound text — the Input-fields `is-completed` precedent.

## Gates that BIT my lane (all fixed same-minute, re-run clean)

- **Coverage/aria:** Time-picker's static gallery list lacked `role="option"` in source markup →
  made it an honest listbox snapshot (roles + aria-selected + tabindex=-1).
- **ds-005 descender-clip:** File-upload's truncating filename span → `text-box-edge:text text`
  added (the override IS the fix, per the gate's own message).
- **★ Token-sync DRIFT (the lesson of the window):** Stepper's first draft wrote 4 values from
  RECALL (`--muted` #575757 · `--incomplete` #E1E1E1 · dark `--on-complete` #1A1A1A) — the gate
  caught all four; correct values RETRIEVED from gated Progress-tracker's declarations
  (`text/secondary` is R-D16-COLLAPSED to the single ink — my recall predated the collapse).
  Retrieval-not-recall enforced by the machine, working exactly as designed.
- **4px-grid + a11y + icon gates:** clean on my five from birth (26px padding class of error: none
  this window).

## Sandbox lessons (for the runbook if the conductor concurs)

- **pkill self-match, second bite:** cleaning stray builds, my kill pattern `"_build_al[l].py"`
  didn't match itself — but the SAME command line contained a plain `nohup … _build_all.py` launch,
  which DID match → SIGTERM'd my own shell (exit 143). Rule: the bracket trick must cover EVERY
  occurrence in the launcher line, or kill and launch in SEPARATE calls (I switched to separate).
- Competing builds interleave through shared generated files (reports flip red/green under you) —
  regenerate + judge only by (a) quiet-tree full runs and (b) direct gate runs grepped for your own
  basenames. Receipted so wave-3 workers expect it.

## Open questions → Dave (via conductor; numbering continues wave-1's A-Q1..Q4)

- **A-Q5 · Calendar-cell + dot-button physics.** Day cells (Date/Date-range) and Stepper's done-dot
  buttons carry NO press physics — judged selection targets / structural markers (the Tabs class),
  not buttons. Confirm, or extend the family to selection targets.
- **A-Q6 · Determinate progress bar.** File-upload built the library's FIRST determinate bar
  (ink-on-neutral, R-D22 spirit). If Data-grid/Charts/anything else needs one, it's an accretion
  candidate (progress-bar atom or partial) — evidence recorded here.
- **A-Q7 · Stepper ↔ Progress-tracker fold.** Stepper consumes PT's dots/track by copy (the B-Q2
  modal-family shape): fold into one snippet later, or accrete a stepper-visuals partial when a
  third consumer appears? (Also: PT's meta note "a real Back/Next drives it" now has its real
  driver — cross-reference when convenient.)
- **A-Q8 · Range-picker restart protocol.** Restart-on-earlier-pick inscribed as reference
  behaviour (vs swap-endpoints). Flag if HSBC source says otherwise.
- *(A-Q1 label weight + A-Q2 input-error slot ride unchanged — all five new components bind
  `.t-cm-label` (400) + semantic `rag/error`, same as wave 1; both retro-propagate.)*

## ★ Accretion evidence (ADR-0013 ruling 3 — propose-don't-promote)

- **Field-family strengthens again:** the Input-fields boxed chrome is now consumed by copy in
  **3 more files** (Date-picker, Date-range-picker, Time-picker; + Stepper's gated field = 4) on
  top of wave-1's ≥7 — the standout candidate's case is now overwhelming (§C·2 Q6).
- **Anchored-overlay chrome** (elevation recipe: surface + shadow-light/outline-dark + translateY
  reveal) now lives by copy in Tooltip, Dropdown, Popover, Toast(?), + my two panels + Time-picker's
  menu — a second observed-duplication family for the census watch.
- **Stepper visuals ×2** (A-Q7) · **determinate bar ×1** (A-Q6, first instance).

## Icon gaps

**None.** Wave-1's verification held: calendar/chevrons(×4)/time/upload/document/pdf/close/error/
success all byte-matched from the library. Time-picker carries Dropdown's data-bespoke neutral tick
(same reason string, counted bespoke-verified by the gate).

## Proposed §C lines

- **Worker-A lane (forms & entry): ★ BRIEF COMPLETE 9/9** — wave 2 landed the remaining 5 (Date ·
  Date-range · Time · File-upload · Stepper), 10 new files, composites-only, radius roles from
  birth, census zero-growth. Receipt №2 carries A-Q5..Q8 + the field-family/overlay accretion
  evidence.
- **Conductor serials:** register 4 `$members` (one `:is()` mixed-size) + inject · MIGRATED_SNIPPETS
  +5 · categories · fold A-Q5..Q8 into the Dave queue · authoritative serial build AFTER C/D land
  (my close-state red is attributed to their in-flight files — verify against this receipt).

**Commit state: NO commits made** (HEAD `6e2dd56` unchanged at close). All 10 files above are
hand-authored NEW; everything else dirty in my window was generator output or C/D's lanes.

## ⚠ FINAL-STATE FLAG for the conductor — FENCE BREACH OBSERVED (not mine)

At my close, three CONDUCTOR-ONLY serials are dirty — **none touched by me** (I never opened them
for writing; my proposals travel in this receipt only):
- `knowledge/component-types.json` **+3** — a `"Data-grid"` `$members` entry (worker C
  SELF-REGISTERED; registry is conductor-only per every wave brief).
- `knowledge/gen_showroom.py` **±4** — category map extended `"stat-card" → + "data-grid"`, comment
  says "wave 2 (worker C)".
- `knowledge/_validate_radius.py` **+2** — presumably C adding themselves to the strict list
  (do-not-edit per brief).
Reconcile path-by-path per the doctrine — C's receipt should confirm intent; the changes may be
CORRECT in content while wrong in channel. My 4 `$members` proposals remain receipt-only and
unregistered, awaiting you.
