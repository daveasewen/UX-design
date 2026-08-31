# Brief — #229 eye-repairs (Opus repair sub): seg-control hover radii + FAB face component

**Dave's words at #229, off the live review page, banked verbatim — these are the contract:**

> "Okay this is almost perfect. One thing missing from the seg-controls on console, the hovers
> don't seem to have inherited the radii. The FAB overlay isn't using the fab component, unless
> there is a round variant that I've forgotten about. Everything else is great."

**RCA before patches is STANDING (`s228-D7`):** for each finding, five whys to the root cause,
then a tactical fix AND the permanent fix (or its priced path), permanent owner named. A patch
alone is a refusal of his standing instruction.

## Finding 1 — console segmented hovers didn't inherit the radii

Conductor's arming greps (verify, don't trust): canon mints
`--border-radius-segmented-thumb-{xs,s,m,l}` (console gets m/l = 8px per s227-D7) and aliases
them near canon.css:7139 — but no hover-state rule pairs with those radii. Likely shape: the
hover highlight is a separate rule that renders square behind a rounded thumb on console.

- Root-cause it, then fix the CLASS, not the pixel: check ALL interactive states
  (hover/focus/active) × all four scales × ALL FOUR THEMES (mono/legacy/console/supercharge —
  flexibility IS the requirement; mono/legacy/supercharge must stay 0 everywhere).
- The fix goes through the PROPER mint path, not hand-edited canon: s227-D7's change was a
  store re-mint (`SEGMENTED_CONCENTRIC_SCALES`) + regen. Find how the hover styling derives
  and fix at the generator/store level (mint-time derivation, s200-D1).
- ⛔ The regen serial is ORDERED — run the WHOLE serial per wave, ramp first, index last:
  `gen_radius_derive · gen_snippet_tokens · canon/gen_canon_tokens · canon/gen_canon_components
  · canon/gen_theme_cascade · gen_showroom · gen_component_partials`.
- Prove with the `--assert-mint`-style table across the 16 theme/scale pairs, hover state
  included, and by EYE in the render.
- Report: is there a gate that should have caught a state rule not inheriting a minted radius?
  If a gate is wanted, PRICE it in the report (gate-don't-patch) — do not build it unasked.

## Finding 2 — the FAB overlay isn't using the fab component

First-hand: `knowledge/_render/apollo-fab.js:135` hardcodes `border-radius:50%` on the face
button. The canon component is `knowledge/snippets/Fab.reference.html`.

1. FIRST check `Fab.reference.html` (and its tokens/variants) for a round variant — Dave
   explicitly allowed he may have forgotten one. If a round variant EXISTS and the face matches
   it: no code change; report which variant, quote the lines, done — the conductor takes it
   back to Dave.
2. If there is NO round variant: the face adopts the canon Fab component's approved geometry —
   COPIED from the reference (radius token, size, any face styling the reference rules), never
   re-drawn by eye. Touch only what geometry/styling requires; the FAB's behaviour
   (theme-follow s228-D2, hot-corner reveal) must not move. Per-theme check after — the FAB
   rides on all four themes.

## Deliverables + regions you own

- The fixes above (store/generator + regenerated outputs for F1; `apollo-fab.js` only-if-needed
  for F2).
- `reviews/FOUR-VISUALS-2026-08-31-v2.html` — copy of v1 with the fixes visible; ADD a hover
  demonstration to the segmented section (state forced via class or a note telling Dave to
  hover). v1 stays untouched (version-don't-overwrite).
- `notes/_subreports/2026-08-31-229-eye-repairs.md` — the report: RCA per finding, what
  changed, assert-mint table, SEEN-state per fix light+dark, UNPROVEN declared, RULING-SHAPED
  listed undecided, REPLAY-THESE, wrap-handover cost line.

## Render-verify

The previous sub left a working MOUNT-side render env — recipe + paths in
`notes/_subreports/2026-08-31-229-four-visuals-review.md` §7 (`outputs/_render-env-229` on the
mount; it persists). All exports + `TMPDIR=/dev/shm` in the SAME bash call; `set_content()`
banned — `goto("file://…")`; look at your PNGs.

## Pitfalls — replayed

- Nothing survives a tool-call boundary (~178s wall); everything mount-side.
- ⚠ An alias-repoint can strip a theme override SILENTLY — after regen, grep the console
  override survived; a dangling var renders SILENT BLACK and 13 gates are blind to it.
- A green regen is not the proof — the 16-pair table + your eye on pixels is.
- Sandbox can't `rm` — `mv` aside.

## DO-NOT-RULE

No `_rulings.json` access; no W-row changes; no memory writes; no git operations (conductor
commits and pushes); no edits beyond the regions above; nothing under apollo-spider/dist or the
release machinery. Dave's two findings are enactable on his words above; anything BEYOND them
that looks decidable goes in the report as RULING-SHAPED, undecided.

Final chat message = STUB: report path, v2 page path, one line per finding (FIXED+SEEN /
NO-CHANGE-round-variant-exists / UNPROVEN why), cost line.
