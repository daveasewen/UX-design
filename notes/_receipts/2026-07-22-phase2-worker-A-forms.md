# Worker A receipt — Phase-2 wave 1 · FORMS & ENTRY lane

*2026-07-22 (date from `date`). Fable worker per `_RUNBOOK-parallel-conductor.md` — NEW files only,
NO commits made, no writes to handoff files or shared registries. Brief:
`notes/_briefs/2026-07-22-phase2-worker-A-brief.md`.*

## Landed — 4 of 9, each `_build_all` GREEN before the next

| # | Component | Files (all NEW) |
|---|---|---|
| 1 | **Form layout + validation** (row 13) | `knowledge/snippets/Form-layout.reference.html` + `knowledge/components/form-layout.meta.json` |
| 2 | **Amount input** (row 17) | `knowledge/snippets/Amount-input.reference.html` + `knowledge/components/amount-input.meta.json` |
| 3 | **Textarea** (row 20) | `knowledge/snippets/Textarea.reference.html` + `knowledge/components/textarea.meta.json` |
| 4 | **Secure entry** (row 19) | `knowledge/snippets/Secure-entry.reference.html` + `knowledge/components/secure-entry.meta.json` |

**★ CUT LINE (context gauge, in-head tally at Red ~60% — orientation reads were heavy):** items
5–9 NOT started — Date picker (14) · Date-range picker (15) · Time picker (16) · File upload (18) ·
Interactive stepper (34). A fresh worker-A window continues from the same brief; survey debt for it:
Progress-tracker (stepper visuals + `.nav button` member precedent), Input-fields tail calendar
button (date picker), Tranche-6 sprite (chevrons/calendar/time/upload/document glyphs all
LIBRARY-MATCHED — verified this session, no icon gaps).

## Registry proposals — conductor only (`component-types.json` `$members`, button-family)

```json
"Form-layout": { "selector": ".fl-btn" },
"Secure-entry": { "selector": ".se-btn" }
```

Both snippets already carry: empty `/* ===== AUTO-PARTIAL press-physics START (button-family) ===== */`
+ `END` pair on the control · `--phys-size:120` declared ON the control rule (not :root — mixed-size
files can then scope per control) · `--spring`/`--press` byte-equal to Button's (matchValues) ·
`transform var(--spring)` in the control's transition · manifest binds for `--press-travel`/`--press-darken`
+ per-theme declarations (2 / 0.94). **`gen_component_partials --check` did NOT object to the
unregistered markers (two green builds carried them) — markers left ACTIVE, not commented.**
After registration, run the generator to inject; no other edits needed.

## MIGRATED_SNIPPETS basenames (radius gate — all four bind role tokens from birth)

`Form-layout.reference.html` · `Amount-input.reference.html` · `Textarea.reference.html` · `Secure-entry.reference.html`
(all bind `border-radius/control`; no other radius roles used.)

## Showroom category proposal

All four → the Input-fields category (forms). If a new bucket is cut instead: **"Forms & entry"**
= Input-fields, Search-field, Dropdown, Selection-controls, Slider + these four.

## Judgment calls (per component)

1. **Form-layout** — field anatomy consumed VERBATIM from gated Input-fields (boxed language:
   hover fill · focus black border + 4px bottom-stroke · error 4px red stroke, dark full-red
   border · message text INK + roundel). Organism structure from Tranche-6 (ruling 3): fieldset/
   legend, pair row (stacks ≤520), action bar stacks primary-on-top. Error summary = ctkn-020
   EXACT title string, role=alert, tabindex=-1 focus target, links focus fields. Copy: instructions
   begin "Enter…"; placeholders EMPTY except formats (copy-040); required-by-default with
   "(optional)" ink markers + an intro line stating it.
2. **Amount-input** — Amount-display conventions mined: code-before-value no space (copy-025),
   typographic minus (display of debits only; entry rejects negatives), tabular figure composites
   (.t-cm-figure-5 standard / figure-4 display size). Normalises on blur (en-GB grouping + 2dp);
   `type=text` + `inputmode=decimal` (never type=number — anti-pattern recorded in meta).
3. **Textarea** — Input-fields channel stretched vertically; counter warns by WEIGHT at 90% + a
   polite live region (T6 used a warn COLOUR — I judged colour-alone + amber-text-AA risk against
   it; review welcome). Vertical-only resize; disabled kills resize.
4. **Secure-entry** — Tranche-9 OTP atom surveyed FIRST per brief; cell 48×56 numeral = EXACTLY
   `.t-cm-figure-3` (24/500 tabular) → zero-visual-change composite bind. The tranche's `.filled`
   weight bump is a no-op at figure-3 → dropped. Auto-advance/backspace/paste-distribute;
   `autocomplete=one-time-code`; per-cell "Digit n of N"; PIN = native password masking.
   **Deliberate delta:** ≤480px cells shrink 40×48 but numeral HOLDS figure-3/24 (T9 downshifted
   to raw 20px — re-typing a composite via media query is exactly what T-D9/T-D12 forbid).

## Open questions → Dave (via conductor)

- **Q1 · Form label weight.** Gated Input-fields labels = 16/**500**; Tranche-6 = 14/**500**; the
  composite `.t-cm-label` = 16/**400**. All four new components bind the composite (rule-driven) →
  labels render 400, visibly lighter than Input-fields'. Either rule 400 (and Input-fields migrates
  later) or mint/bind a 500 form-label composite (one type.css line, conductor).
- **Q2 · `input-error` flex slot.** The ADR-0010 null slot Dave anticipated is NOT declared in the
  token store (checked: zero hits in tokens/). All four bind semantic `rag/error`. Propose the
  conductor (or the enact-queue) declares the null slot so themes can flex it later.
- **Q3 · Secure-entry narrow numeral** — is holding 24 in the 40px cell right, or does the figure
  ramp want a responsive story? (T9 evidence says 20px was reviewed once.)
- **Q4 · fl-summary vs Worker B's Alert.** The form-level error summary (error-tint box + roundel +
  link list) visually neighbours Alert/Banner (B's lane). Built form-scoped on purpose; flag for
  the pro-forma dedup/reconcile pass rather than cross-lane coupling now.

## Gate/infra observations (for the conductor's reconcile)

- Generated surfaces regenerated repeatedly this session by both lanes (worker B's Alert/Toast
  visible mid-session): `canon/canon.css` (AUTO blocks), `showroom/`, `_*-GATE.md` reports,
  `canon/_bindings-applied.json` etc. All deterministic — your final SERIAL build is authoritative;
  dirty paths beyond the 8 files above + B's are generator output, not hand edits.
- Edge-weight advisory: 12px@400 floor is 500 — my Form-layout tooltip set to 500; gated
  Input-fields' own `.tip` is still 12/400 (pre-existing census item, NOT touched).
- The 4px-grid gate caught a 26px padding first build (fixed 24) — gates biting as designed.
- Icon gaps: **none** — date/time/upload/document/file/pdf glyphs verified present + byte-matched
  in `assets/icons/media/` for the remaining worklist.

## Proposed §C lines

- **Worker-A lane (forms & entry): 4/9 LANDED green** (Form-layout · Amount-input · Textarea ·
  Secure-entry — snippets + metas, composites-only type, R-D20 error set, empty partial markers).
  **Remaining 5/9** (Date, Date-range, Time, Upload, Stepper) → fresh worker-A window, same brief.
- **Conductor serials:** register 2 `$members` + inject partials · MIGRATED_SNIPPETS + showroom
  category · queue Q1–Q4 for Dave (Q1 label-weight + Q2 input-error slot are the material two).

**Commit state: NO commits made** (worker discipline). All 9 files above are hand-authored NEW;
everything else dirty is generator output.

**⚠ Final-state note (live race, expected):** at my close, `_build_all` shows cascade/showroom
STALE — Worker B was still landing files mid-check (Modal-lightbox, Popover, Drawer appeared
between my regen and the gate). Each of MY four components was verified green against the tree as
it stood (three green full builds this session). I stopped regenerating rather than chase B's
moving tree — per the runbook, the conductor's final SERIAL build (regen cascade + showroom, then
`_build_all`) is the authoritative green.
