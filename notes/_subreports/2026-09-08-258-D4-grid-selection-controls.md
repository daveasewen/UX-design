# 258-D4 — Data-grid composes Selection-controls

Ruling **s258-D4**: the grid's row/header checkboxes are COMPOSED from Selection-controls
(`.cn-selection-controls` scope, hidden `<input>` + sibling `<label>` holding `<span class="box">`)
instead of carrying native inputs, so a verbatim copy passes `_validate_screen.py` /
`_validate_compose.py` check 7. **The gate was not touched.**

## What changed

- `knowledge/snippets/Data-grid.reference.html`
  - Header select-all and the row checkbox both rewritten from
    `<label class="cbx"><input>…<span class="box">` (input INSIDE the label, `~` sibling CSS)
    to Selection-controls' own pattern:
    `<span class="cn-selection-controls cbx"><input id=…><label for=…><span class="box">…</label></span>`.
  - Row inputs gained a real id (`selRow-${r.id}`) so the `for` binding is unique; the grid's
    `aria-label` per row and `id="selAll"` + `:indeterminate` on the header are unchanged.
  - CSS: `.cbx` rules restated on the canon selectors (`input:checked + label .box`,
    `input:indeterminate + label .box`, `input:focus-visible + label .box`,
    `label:hover .box`), input hidden the canon way (`position:absolute; opacity:0; width:0; height:0`)
    rather than as a 22×22 transparent overlay.
  - `th.sel,td.sel{padding:0; width:44px}` + a 44×44 label — the checkbox hit target used to be
    22×22 inside cell padding; it is now a REAL 44px target. The now-redundant
    `thead th.sel{padding:…}` rule was dropped.
  - Doc comment moved Selection-controls out of "MINED, NEVER MODIFIED" into COMPOSED.
  - Nothing inside an `APOLLO-DEMO` fence was touched.
- `knowledge/components/data-grid.meta.json` — new `$composes` naming Selection-controls first,
  `relationships.composes` array, and `subComponents.selection-checkbox.use` rewritten from
  "verbatim anatomy" to "COMPOSED". Surgical text edits; the file's compact formatting is intact.
- `knowledge/canon/canon.css` — regenerated (`.cn-data-grid` scope now carries the new selectors).

## Gates

| gate | result |
|---|---|
| `gen_canon_components.py` then `--check` | exit 0 — 136 components in sync |
| `_validate_snippets.py` | 136 snippets, 0 failures |
| `gen_component_partials.py --check` (lives at `knowledge/`, NOT `knowledge/canon/`) | exit 0 |
| `_validate_compose.py` | RESULT: PASS ✅ |

## Driven (playwright, chromium, 1440×1000, light + dark)

- select-all → 8/8 rows `aria-selected="true"`, tick shown, box fill `#000` light / `#FFF` dark.
- uncheck one row → header `indeterminate=true`, mixed dash shown, tick hidden, 7 rows.
- select-all off → 0 rows, neither tick nor dash.
- single row check → 1 row, header indeterminate.
- keyboard: roving cell focus onto `td.sel` + Enter toggles the row (rows 0→1).
- label hit box MEASURED 44×44 for both header and row; duplicate ids 0; **0 pageerrors,
  0 console errors** in both themes.

## Screen-gate proof (on a COPY — the frozen arm was not edited)

`/tmp/p258/dashboard-258d4-probe.html` = a copy of
`outputs/coldrun-258-v5/arm-A-blind/dashboard.html` with its two checkbox sites swapped for the
new composition. `_validate_screen.py` → **verdict PASS ✅, compose ✅**.

MUTATION TEST of the clause: the same file with `cn-selection-controls ` stripped →
**verdict FAIL ❌, `compose: ❌ 2 native radio/checkbox not composed from .cn-selection-controls
(.radio/.box)`**. The check is real and the composition is what passes it.

Both probe subjects were removed from `knowledge/_screen-gate/` afterwards and
`knowledge/_SCREEN-GATE.md` was restored from `git show HEAD:` — directory verified byte-identical
to before the run.

## Undone / noted

- `_validate_screen.py` refuses to REBUILD its index while an untracked subject sits in
  `_screen-gate/` (dream-11 P4(b)) — it still wrote and evaluated the subject file, so the verdict
  above is genuine; only the index rebuild was refused, and the index was restored anyway.
- Pre-existing, NOT a regression: focusing a `td.sel` cell with `.focus()` rather than through the
  roving-tabstop path leaves `current` stale, so Enter toggles the previously-current cell. HEAD
  behaves identically (checked side by side). Left alone — out of this lane's scope.
