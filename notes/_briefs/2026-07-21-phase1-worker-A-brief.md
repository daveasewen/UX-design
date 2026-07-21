# Phase-1 Worker A brief — radius migration + theme-response audit (controls & indicators)

*Written by the Phase-1 conductor, 2026-07-21 (date from `date`). You are a WORKER per
`knowledge/_RUNBOOK-parallel-conductor.md`: create only NEW files + edit your assigned snippets,
NO git, NO writes to `GOOD-MORNING.md`/`_LIVE-STATE.md`/`_FUTURE-STATE.md`. Receipt at the end
(path below). The conductor reconciles + commits.*

## Your 10 files (21 declarations, from `knowledge/_RADIUS-GATE.md`)

| File | decls | likely role(s) — YOUR judgment call |
|---|---|---|
| `snippets/Input-fields.reference.html` | 4 | control |
| `snippets/Selection-controls.reference.html` | 4 | control (radio circles = `50%`, stay literal) |
| `snippets/Dropdown.reference.html` | 2 | control |
| `snippets/Slider.reference.html` | 1 | control or indicator (track vs thumb) |
| `snippets/Icon-button.reference.html` | 1 | control |
| `_proforma/Icon-button.reference.html` | 1 | control — ⚠ see BASENAME WARNING |
| `snippets/Badge.reference.html` | 1 | indicator (pill `999px` stays literal if used) |
| `snippets/Tags.reference.html` | 2 | indicator or control (dismissible = interactive) |
| `snippets/Status-indicator.reference.html` | 2 | indicator |
| `snippets/Progress-tracker.reference.html` | 3 | indicator |

⚠ **BASENAME WARNING:** `MIGRATED_SNIPPETS` in `knowledge/_validate_radius.py` is basename-keyed.
Adding `Icon-button.reference.html` flips BOTH the snippets/ and _proforma/ copies into STRICT —
**migrate both in the same change**, never one without the other.

## Per-file loop (the ruled Phase-1 brief, GOOD-MORNING ★ LATEST)

1. **Rebind radius onto the ROLE token** — pattern proofs: `snippets/Button.reference.html`
   (control) + `snippets/Cards.reference.html` (surface). Mechanics per file:
   - Declare the local var in **both** theme blocks (`[data-theme="light"]` + `"dark"`), e.g.
     `--border-radius-control:0;` (0 = the projected Mono value; the projector checks it).
   - Rules use `border-radius:var(--border-radius-control)`. **`50%` + `999px` idioms stay literal.**
   - Add the manifest binding in `#token-manifest`, e.g.
     `"--border-radius-control": "border-radius/control"`.
   - Roles: `border-radius/control | surface | indicator` (layout.json, alias→default). Taxonomy is
     PROVISIONAL-agent — judgment per ELEMENT (a card inside a control component still binds
     surface). Census: dossier addendum in
     `_DECISION-HISTORY/2026-07-21-phase0-theme-resolution-layer.md`. Record every role choice
     in your receipt.
   - Add the basename to `MIGRATED_SNIPPETS` in `_validate_radius.py` **in the same change**.
     Never hand-edit `_RADIUS-GATE.md` (generated).
2. **Theme-response audit** — render the component's showroom page across 4 themes × light/dark
   (render recipe: GOOD-MORNING §Renders / memory `sandbox-html-rendering`). Hunt roles the theme
   SHOULD override but doesn't reach — the Button success-background miss + Cards red-accent drift
   are the patterns. Findings → receipt (propose, don't enact token changes — promotion is Dave's).
3. **Regenerate + verify:** `python3 knowledge/gen_snippet_tokens.py && python3
   knowledge/canon/gen_theme_cascade.py && python3 knowledge/gen_showroom.py` then
   `python3 knowledge/_build_all.py` → **42/42 green** before moving on.
4. **CONSULT first when unsure:** `python3 knowledge/_consult.py "border-radius"` (or the component
   name) before judgment calls. Blocked/ambiguous → record in receipt, don't improvise canon.

## Receipt (mandatory, last act)

`notes/_receipts/2026-07-21-worker-A-radius-phase1.md` — what landed · per-element role choices ·
theme-response findings · open questions · files touched · proposed §C lines · NO commits made.
