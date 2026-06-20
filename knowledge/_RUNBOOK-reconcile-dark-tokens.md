# Runbook — reconcile a dark token group

Procedure for fixing tokens that are flat, wrong, or invisible in dark mode. Companion to
`_RUNBOOK-gated-component.md`. Trigger: the dark-surface gate fails, a snippet drifts, or an audit
surfaces a dark defect.

## The defect classes (what to look for)
1. **Flat-white surface** — a background/surface/border/divider token whose dark value is `#FFFFFF`
   (a white block hiding content). Caught by `_validate_dark_surfaces.py`.
2. **Lost alpha** — a transparent light value (`#RRGGBB00`) that became opaque in dark (e.g. the old
   `form/background/default` → opaque white field). Restore the alpha.
3. **Indistinguishable pair** — two related fills that collapse to the same value in dark (e.g.
   `progress/complete` == `progress/incomplete` both white → no progress shown).
4. **Invisible-on-page** — a fill/handle bound to `background/default` (#000 in dark) sitting on the
   #000 page (e.g. the slider handle). Rebind to a raised surface + a visible border.
5. **Inverting label gap** — a label on a surface that flips light↔dark, bound to flat `text/reverse`
   → white-on-white. Use `text/on-inverse`.

## Steps
1. **Identify the role.** Foreground (text/icon) going white in dark is CORRECT — skip. Only surfaces,
   fills, borders, and the inverting cases are defects.
2. **Pick the dark value from existing primitives** — never invent. Greys: `color/grey/dark-mode/200…700`
   (`#656565`→`#101010`); brand red stays `color/primary` (#DB0011, works on both); raised surface
   `dark-mode/600` (#1D1D1D). Keep the `$alias.dark` honest (point it at the primitive you used).
3. **Verify ≥3:1** for borders/indicators against their surface (`_contrast_utils.contrast_ratio`);
   text ≥4.5:1. If it can't reach the bar with an existing primitive, that's a finding, not a hack.
4. **Annotate intentional whites** with `$darkNote` (the gate's allowlist) — e.g. an active border or an
   inverting button fill that is *meant* to be white in dark.
5. **Rebuild** (`python3 knowledge/_build_all.py`) — must end green. Record the change as a meta
   `$finding` / `$darkNote` and (if it's a decision, e.g. a new value) flag for Dave.

## Reference reconciliations (already done — patterns to copy)
- `form/*` (alpha + greys), `tabs/*`/`tertiary/*` (raised greys), the 24-token surface sweep,
  `progress/*` (red + grey), `tooltip/background` (raised). See `_FINDINGS-INDEX.md`.
