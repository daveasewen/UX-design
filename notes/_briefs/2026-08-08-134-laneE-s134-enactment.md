# s134 enactment (D1/D2/D3) — brief

## Diffs

**`knowledge/snippets/Alert.reference.html`** (s134-D3): `--warn:#C58900` → `#E0A61F` at
lines 85 (light) and 92 (dark), matching the ruled mono amber (line-71 comment / s122-D2).

**Same file** (s134-D2): the unconditional `[data-theme="dark"] .alert .ic{ color:#FFFFFF;
--mark:#000000; }` (line 123) is commented out with a citation — this file is the MONO
reference, and s134-D2 scopes the white-shape/black-mark flip to legacy alone. Mono dark now
falls through to the same `.alert.warn/.ok/.info .ic` / default(.err) mark rules as light — by
declaration, not silent fall-through.

**`knowledge/_validate_state_contrast.py`** (s134-D1): added a mark-leg check inside the
existing `svg` block in `MEASURE`. Walks each roundel svg's descendants for an inner
`fill:var(--mark)` node whose resolved fill differs from the shape's own fill, and gates it at
4.5:1 as a real `kind:'text'` failure (named `[MARK] …`, counted, rc-failing). The pre-existing
shape-on-surface check (`kind:'icon'`, 3.0, WARN-only, never blocks) is untouched — it already
satisfied "report, don't gate" and needed no change. Unreadable mark colours still propagate
through the existing `StateContrastParseError` path (no new catch added).

## Contrast figures (computed, not re-composited)

Light (unchanged mechanism, warn shape now `#E0A61F`):
err 4.71 · warn mark-on-shape 7.99 · warn shape-on-tint(report) 1.76 · ok 5.00 · info 5.03.

Dark, flip removed (same marks as light per s134-D2):
- err mark-on-shape **3.68** (fails 4.5 gate)
- warn mark-on-shape 7.99 (passes) · warn shape-on-tint(report) 6.17
- ok mark-on-shape **3.63** (fails 4.5 gate)
- info mark-on-shape 4.55 (passes, thin)

Warn tint pair vs new amber (report only, per the s134-D3 watch — not re-composited):
light `#F6E5CC` vs `#E0A61F` = 1.76 · dark `#3C2C13` vs `#E0A61F` = 6.17.

## Residual — flagged, not fixed

Removing the legacy-only dark flip per s134-D2 leaves **mono dark error (3.68) and mono dark
success (3.63) below the 4.5 mark-on-shape gate**. DO-NOT-RULE forbids picking a new value here
— flagged loudly in the snippet comment (line ~127) and here. This needs a Dave call: either a
mono-specific dark mark treatment (not "same marks both themes" for these two families) or a
different dark tint/shape pairing. Unresolved.

## Mutation evidence

`_validate_state_contrast.py --selftest`: rc=2, `StateContrastSelftestError` (playwright not
installed, no network in sandbox to fetch it) — correct per the existing contract; all 18
non-browser arms passed before the browser-dependent measurement.

Logic-level mutation test (`node`, pure functions copied verbatim from the new code path,
checked directly, not through a pipe):
- Case A — failing mark leg (mono dark err, 3.68) → gates as `kind:'text'`. PASS.
- Case B — failing shape-on-surface leg alone (warn shape-on-tint, 1.76) → reports as
  `kind:'icon'`, never `'text'`, does not gate. PASS.
- Case C — passing mark leg (7.99) → no failure record. PASS.
All three arms passed; rc=0.

## Not done (DO-NOT-RULE)

No token spine edits, no new colour values, no tint re-composites, no commits, no chain/GM/
state/rulings edits.
