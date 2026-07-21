# Phase-1 Worker B brief — radius migration + theme-response audit (surfaces & structure)

*Written by the Phase-1 conductor, 2026-07-21 (date from `date`). You are a WORKER per
`knowledge/_RUNBOOK-parallel-conductor.md`: create only NEW files + edit your assigned snippets,
NO git, NO writes to `GOOD-MORNING.md`/`_LIVE-STATE.md`/`_FUTURE-STATE.md`. Receipt at the end
(path below). The conductor reconciles + commits.*

## Your 10 files (23 declarations, from `knowledge/_RADIUS-GATE.md`)

| File | decls | likely role(s) — YOUR judgment call |
|---|---|---|
| `snippets/Tabs.reference.html` | 6 | control (largest file — start here) |
| `snippets/Modals.reference.html` | 4 | surface |
| `snippets/Account-card.reference.html` | 3 | surface |
| `snippets/Table.reference.html` | 3 | surface |
| `snippets/List-items.reference.html` | 2 | surface or control (interactive rows) |
| `snippets/Action-bar.reference.html` | 1 | surface or control |
| `snippets/Confirmation.reference.html` | 1 | surface |
| `snippets/Links.reference.html` | 1 | control (focus-ring radius, likely) |
| `snippets/Notifications.reference.html` | 1 | surface — ⚠ see LEGACY WARNING |
| `snippets/Video-player.reference.html` | 1 | surface |

⚠ **LEGACY WARNING — Notifications:** it is a **Legacy reference** (§A-AUTH DO-NOT-CONVERT in
`knowledge/_STYLE-PROVENANCE.md`). Rebind its **radius only**. Do NOT touch its RAG colours,
its `#A8000B` (correct Legacy red), or its `driftAllow` waivers.

## Per-file loop (the ruled Phase-1 brief, GOOD-MORNING ★ LATEST)

1. **Rebind radius onto the ROLE token** — pattern proofs: `snippets/Button.reference.html`
   (control) + `snippets/Cards.reference.html` (surface). Mechanics per file:
   - Declare the local var in **both** theme blocks (`[data-theme="light"]` + `"dark"`), e.g.
     `--border-radius-surface:0;` (0 = the projected Mono value; the projector checks it).
   - Rules use `border-radius:var(--border-radius-surface)`. **`50%` + `999px` idioms stay literal.**
   - Add the manifest binding in `#token-manifest`, e.g.
     `"--border-radius-surface": "border-radius/surface"`.
   - Roles: `border-radius/control | surface | indicator` (layout.json, alias→default). Taxonomy is
     PROVISIONAL-agent — judgment per ELEMENT (a button inside a modal binds control, the modal
     shell binds surface). Census: dossier addendum in
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

`notes/_receipts/2026-07-21-worker-B-radius-phase1.md` — what landed · per-element role choices ·
theme-response findings · open questions · files touched · proposed §C lines · NO commits made.
