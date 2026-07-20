# Worker receipt — dedicated `button/*` semantic tier + tranche rebind

*Written 2026-07-19 (session date read via `date`; wall-clock at commit time was 2026-07-20 — noted for
the timestamp trail, filename kept as instructed). Worker session. Worked directly in the existing tree
(`/sessions/keen-zen-einstein/mnt/UX-design`). No worktree/branch created. **No git writes** —
`git add`/`commit`/`stash` never called; left dirty for the conductor.*

## What this does
Adds `button/secondary/*`, `button/tertiary/*`, `button/quaternary/*` as a **new, dedicated** semantic
token group (Apollo Mono's real button ladder — no `button/primary`; red primary is Legacy-only and
stays parked), and rebinds the 9 pro-forma tranches' filled/outline buttons to it — without touching the
existing `secondary/*`/`tertiary/*` tokens, which stay exactly as they were (still overloaded, still used
by checkboxes/radios/tab-bar-checked and card/modal/panel surfaces respectively).

## Files changed
```
knowledge/tokens/semantic-colour.json     — NEW "button" top-level group (secondary/tertiary/quaternary)
knowledge/canon/canon.css                 — regenerated (gen_canon_tokens.py) — 16 new --button-* vars
knowledge/_contrast_utils.py              — bug fix + 3 new CONTRAST_ALLOWLIST entries (see "Gate fixes")
knowledge/_proforma/Tranche-1-interactive.html  — manifest rebind + --ter-border + border-color swap
knowledge/_proforma/Tranche-2-interactive.html  — same
knowledge/_proforma/Tranche-3-interactive.html  — same
knowledge/_proforma/Tranche-4-interactive.html  — same
knowledge/_proforma/Tranche-5-interactive.html  — same
knowledge/_proforma/Tranche-6-interactive.html  — same
knowledge/_proforma/Tranche-7-interactive.html  — same (no .ib classes — border-color swap N/A there)
knowledge/_proforma/Tranche-8-interactive.html  — same
knowledge/_proforma/Tranche-9-interactive.html  — same (no .ib classes at all — btn.ghost only)
```
`knowledge/snippets/*` — **untouched** (0 changes reported by the projector; confirmed no snippet file
was written). No memory/GOOD-MORNING/_LIVE-STATE files touched.

## Task 1 — the `button/*` token group (resolved values, as ruled)

| Token | Light | Dark | Alias (light / dark) |
|---|---|---|---|
| `button/secondary/background/default` | `#626262` | `#808080` | `color/mono/7` / `color/mono/8` |
| `button/secondary/background/hover` | `#484848` | `#9D9D9D` | `color/mono/6` / `color/mono/9` |
| `button/secondary/background/pressed` | `#313131` | `#B7B7B7` | `color/mono/5` / `color/mono/10` |
| `button/secondary/background/disabled` | `#E1E1E1` | `#484848` | `color/mono/12` / `color/mono/6` (exempt) |
| `button/secondary/label/default` | `#FFFFFF` | `#000000` | `color/white` / `color/black` (**intentional per-mode flip**) |
| `button/secondary/label/disabled` | `#9D9D9D` | `#808080` | `color/mono/9` / `color/mono/8` (exempt) |
| `button/tertiary/background/default` | `#FFFFFF00` | `#FFFFFF00` | `color/grey/transparent/white-0` both |
| `button/tertiary/background/hover` | `#F0F0F0` | `#232323` | `color/mono/13` / `color/mono/raise-2` |
| `button/tertiary/border/default` | `#1A1A1A` | `#FFFFFF` | `color/mono/4` / `color/white` |
| `button/tertiary/border/disabled` | `#E1E1E1` | `#484848` | `color/mono/12` / `color/mono/6` (exempt) |
| `button/tertiary/label/default` | `#1A1A1A` | `#FFFFFF` | `color/mono/4` / `color/white` |
| `button/tertiary/label/disabled` | `#B7B7B7` | `#808080` | `color/mono/10` / `color/mono/8` (exempt) |
| `button/quaternary/background/default` | `#FFFFFF00` | `#FFFFFF00` | `color/grey/transparent/white-0` both |
| `button/quaternary/background/hover` | `#F0F0F0` | `#232323` | `color/mono/13` / `color/mono/raise-2` |
| `button/quaternary/label/default` | `#1A1A1A` | `#FFFFFF` | `color/mono/4` / `color/white` |
| `button/quaternary/label/disabled` | `#B7B7B7` | `#808080` | `color/mono/10` / `color/mono/8` (exempt) |

Every value above matches the brief's ruled spec **exactly** (verified against `knowledge/tokens/colour.json`
primitives before writing — `color/mono/1..15` = `#000000…#1A1A1A(4)…#313131(5)…#484848(6)…#626262(7)…
#808080(8)…#9D9D9D(9)…#B7B7B7(10)…#E1E1E1(12)…#F0F0F0(13)…raise-2 #232323`, `color/white #FFFFFF`,
`color/black #000000`, `color/grey/transparent/white-0 #FFFFFF00`). Nothing invented, rounded, or
substituted. **No `button/primary` created** — noted in the group's `$description` as Legacy-only/parked.

Shape mirrors `surface/*`/`secondary/*` exactly: per-mode `$value` + `$alias` (to a primitive — same
pattern as the existing `secondary`/`tertiary` groups, which also alias primitives directly, not another
semantic token), plus `$note`/`$darkNote` on the leaves that need one (disabled exemption, the
intentional per-mode label flip, the intentional dark-mode border inversion). Group carries one
`$description` explaining the WHY (dedicated group vs. recolouring the overloaded existing tokens).

**Contrast — verified before adding anything to a gate** (WCAG relative-luminance, computed independently
before touching `contrastPairs`):
- `button/secondary/label/default` on `button/secondary/background/default`: **6.10:1 light / 5.32:1
  dark** (text, need 4.5) — matches the brief's stated 6.1/5.32 exactly.
- `button/secondary/background/default` vs `background/default`: **6.10:1 light / 4.41:1 dark** (non-text,
  need 3.0).
- `button/tertiary/border/default` vs `background/default`: **17.40:1 both modes** (non-text, need 3.0) —
  matches the brief's stated 17.4 exactly.
- Disabled pairs (label/border/background `disabled` leaves) are all under floor by design and are
  WCAG-exempt (inactive components) — flagged as such in the token `$note`s and added to the contrast
  gate's `CONTRAST_ALLOWLIST` (see Gate fixes below) rather than silently skipped.

Nothing came out under floor for a non-exempt pair. No STOP condition hit.

## Task 2 — canon.css regeneration
`python3 knowledge/canon/gen_canon_tokens.py` — wrote cleanly, 16 new `--button-*` root vars + 16 dark
overrides (`444 root vars, 157 dark overrides` total after). Since every `button/*` alias points straight
at a `color/*` primitive (same as `secondary`/`tertiary` today), the generator bakes the resolved hex
rather than emitting a `var()` chain — that's the existing, correct behaviour of
`gen_canon_tokens.py::walk()` (only semantic→semantic aliases get a `var()` chain; semantic→primitive
bakes). Verified all 16 vars land correctly in both `:root` and `[data-theme="dark"]`, values match the
table above exactly.

## Task 3 — the 9 tranches, rebind summary
Same treatment applied to all 9 (`Tranche-1..9-interactive.html`), via a small Python transform script
(not hand-edited file by file, to guarantee consistency) followed by the standard projector:

1. **Manifest `vars`**: `--pri` repointed from `text/default` → `button/secondary/background/default`;
   added `--pri-h` → `button/secondary/background/hover`, `--pri-lbl` → `button/secondary/label/default`,
   `--icon-rev` → `button/secondary/label/default` (all four were local-only literals before — now real
   manifest-bound vars). Added `--ter-border` → `button/tertiary/border/default` (brand new var).
2. **CSS**: `.btn.ghost` and `.ib.ter` (where present) border-color changed from `var(--line)` to
   `var(--ter-border)`. `.btn.link` (quaternary) left untouched, as instructed — it's already transparent
   + `var(--ink)`/`text/default`. Hover border-color (`var(--ink)`) on both `.ghost:hover`/`.ib.ter:hover`
   left unchanged, out of scope this pass.
3. **Theme blocks**: `--ter-border:<value>;` inserted into both `[data-theme="light"]` and
   `[data-theme="dark"]` blocks in every file; `gen_snippet_tokens.py` then projected the real resolved
   values into all of `--pri`/`--pri-h`/`--pri-lbl`/`--icon-rev`/`--ter-border` (54 values changed total —
   6 vars × 9 tranches, exactly as expected).
4. **`.ib.sec`**: only Tranche-1 has this class (a duplicate of `.ib.pri`, byte-identical rule body —
   `background:var(--pri);color:var(--icon-rev);border-color:var(--pri);`). No separate handling needed —
   it inherits the same `--pri`/`--icon-rev` rebind automatically and consistently.
5. **No separate "pressed" colour var exists** anywhere in these files for filled buttons — `:active`
   states use `filter:brightness(.85)` (a CSS filter, not a swapped background var) uniformly across all
   9. Nothing to bind there; flagging per the brief's "or flag anything ambiguous" instruction, not a gap.
6. **`contrastPairs`** added to all 9 manifests (T1–8 had none at all; T9 already had 3 unrelated pairs —
   appended, not replaced):
   ```json
   { "fg": "button/secondary/label/default", "bg": "button/secondary/background/default", "context": "text" },
   { "fg": "button/secondary/background/default", "bg": "background/default", "context": "non-text" },
   { "fg": "button/tertiary/border/default", "bg": "background/default", "context": "non-text" }
   ```
   **Caveat, worth flagging explicitly**: `_validate_snippets.py` (the script that actually *enforces*
   `contrastPairs`) globs `knowledge/snippets/*.reference.html` only — it does not run over
   `_proforma/*.html` at all (confirmed by reading the glob). `_validate_proforma.py` (the gate that *does*
   run over tranches) checks hardcode/icons/ALL-CAPS only, not `contrastPairs`. So these declarations are
   currently **documentation of intent, not gate-enforced** for the tranches — I verified the ratios by
   hand instead (see Task 1 contrast section) so the build stays honest either way. Flagging this as a
   possible follow-on: either widen a gate to read tranche `contrastPairs`, or accept it stays
   documentation-only until the tranches graduate to snippets.
7. **`knownFindings`** updated in all 9 manifests: removed the now-stale "GAP (no semantic token yet)" /
   "DEVIATION" entries that described `--pri`/`--pri-lbl`/`--icon-rev` as unresolved local-literal
   workarounds, replaced with a "RESOLVED" entry describing the new binding + the exact same landmine
   maths this file previously worked around (now solved by the token's own intentional per-mode flip,
   verified 6.1/5.32 instead of the old hand-verified 17.4 literal) — plus a new entry for `--ter-border`.

## FLAGGED — blast radius of the `--pri`/`--icon-rev` rebind (read this before treating as final)
`--pri` and `--icon-rev` are **shared CSS custom properties**, not button-scoped ones. Across the 9
tranches they're also used for non-button "accent" surfaces: progress-bar fills, tab underlines/active
indicators, checkbox/radio checked state, avatar "+N more" badges, tooltip/banner fills, stepper-dot
fills, the back-to-top FAB, and the active floating-tab background. Repointing `--pri`'s *manifest*
binding — exactly as instructed — recolours **all** of these from near-black/near-white to the new
mid-grey `button/secondary` fill, not just `.btn.pri`/`.ib.pri`/`.ib.sec`. This is what the brief
explicitly asked for ("repoint the filled-button vars: `--pri` → …"), and I've done it as specified — but
because the var is shared far beyond buttons, I want this confirmed as the intended visual outcome (every
accent mark in the tranches becomes the secondary-button grey) rather than something that slipped through
because the var name says "pri" and the brief said "button." Recorded this same flag inside each tranche's
`knownFindings` too, so it isn't lost if this receipt is skimmed.

## Gate fixes (found while running Task 5, root-caused and fixed — not patched around)
Running the full build surfaced two real gate defects, both caused by this being the **first** token
group to co-locate a fully-transparent (`#FFFFFF00`) background with a text/label leaf in the same group
(`button/tertiary/*`, `button/quaternary/*`):

1. **`_build_surface_contrast_audit.py` crashed** (`ValueError: Invalid hex: FFFFFF00` in
   `_contrast_utils.hex_to_rgb`). Root cause: `resolve_dark_surface()` collects every sibling
   `*/background/*` token in a group as a candidate "worst-case surface" a co-located label might sit on;
   `button/tertiary/background/default` (transparent) was fed into `hex_to_rgb`, which only accepts
   6-digit hex. **Fix**: `_leaf_dark_hex()` in `knowledge/_contrast_utils.py` now excludes fully-transparent
   (`AA=00`) 8-digit values from the surface pool — a transparent fill isn't a real paint surface for this
   stacking model (the actual surface behind it is already covered by the existing
   default-dark/raised-dark fallback candidates). Checked this doesn't silently drop anything real: the
   *only* `background`/`surface`-named tokens in the store with an 8-digit dark value are
   `form/background/default`, `button/tertiary/background/default`, `button/quaternary/background/default`
   — all three fully transparent, none partially. Comment left in the source explaining why, dated,
   attributed to this task.
2. **`_validate_dark_surfaces.py` flagged `button/tertiary/border/default`** as a flat-white-in-dark
   defect (dark `#FFFFFF`, light `#1A1A1A`, no `$darkNote`). This is the intentional ruled inversion (white
   outline in dark), same class as the existing `secondary/background/default` exemption. **Fix**: added a
   `$darkNote` to that one leaf (the gate's own documented exemption mechanism) — no gate logic changed.
3. **`_build_surface_contrast_audit.py` then correctly flagged `button/secondary/label/disabled`** as a
   real gating failure (1.97:1, below the 3:1 UI floor) — this is the WCAG-exempt disabled state the token
   store already notes as exempt, but it wasn't in the script's `CONTRAST_ALLOWLIST`. **Fix**: added
   `button/secondary/label/disabled`, `button/tertiary/label/disabled`,
   `button/quaternary/label/disabled` to `CONTRAST_ALLOWLIST` in `_contrast_utils.py`, same pattern/reason
   as the existing `text/disabled` etc. entries.

All three are minimal, root-cause fixes to genuine defects the new (valid, ruled) tokens exposed — not
workarounds and not weakenings of any check (nothing that should fail still passes; the allowlist only
covers spec-declared, contrast-exempt disabled states).

## Task 5 — gate result
`python3 knowledge/_build_all.py` — final line:
```
✅ all generators ran and the integrity + contrast gates passed.
```
Exit code **0**. All **35/35** steps ran green (captured full log, grepped for `❌`/`FAIL` — none found
after the two fixes above). Confirmed idempotent afterwards:
```
python3 knowledge/gen_snippet_tokens.py --check
gen_snippet_tokens: 1127 manifest bindings across 39 snippets + 9 tranches; 0 value(s) would change; 0 canon.css literal(s) would change.
OK — snippets + tranches + canon.css in sync with tokens.
```
`_TOKEN-TIER-AUDIT.md`: 0 strict failures (the `button/*` tokens alias primitives directly, same pattern
as `secondary`/`tertiary` today — not added to the `_validate_token_tiers.py` `MIGRATED` strict set, so
they land as consistency-only, same tier as the tokens they mirror; not a new violation). No contrast
pair came out under floor for any non-exempt combination — the STOP condition in the brief was never hit.

## Task 4 — snippet follow-up list (untouched this pass, as instructed)
Surveyed (read-only) which `knowledge/snippets/*.reference.html` files bind actual **button** rendering to
the now-dedicated-elsewhere `primary/secondary/tertiary` tokens, vs. files using `secondary`/`tertiary` for
their *other*, correctly-overloaded roles (checked-state, surfaces) which should **not** move:

**Likely candidates for a future button/* rebind pass** (real button/action-button usage found):
- `Button.reference.html` — `--pri-*` → `primary/*` (red CTA, Legacy — stays), `--sec-hover/--sec-pressed`
  → `secondary/*`, `--ter-default/--ter-hover/--ter-border` → `tertiary/*`. The canonical button
  component — needs the most careful survey (light/dark + all 3 non-primary variants × all states).
- `Action-bar.reference.html` — `--sec`/`--sec-hover` and `--ter-border`/`--ter-hover` on its action
  buttons.
- `Modals.reference.html` — `--sec-bd`/`--sec-hover` (named "sec" but currently bound to
  `tertiary/border`+`tertiary/background/hover` — naming/binding already inconsistent, worth resolving in
  the same pass).
- `Pagination.reference.html` — `--current-bd`/`--pressed` on pager buttons, bound to `tertiary/border`
  and `tertiary/background/pressed`.
- `Progress-tracker.reference.html` — `--btn-border`/`--btn-hover`/`--btn-dis-text`/`--btn-dis-border`,
  literally named "btn" already, bound to `tertiary/*`.
- `Confirmation.reference.html` — `--pri`/`--pri-hover`/`--on-pri` (red CTA) + `--ghost-hover` →
  `tertiary/background/hover` for its secondary action.
- `Tabs.reference.html` — `--tertiary-hover`/`--tertiary-pressed` used on tab *buttons* specifically
  (distinct from `Tab-bar.reference.html`'s `--surface`, which is a genuine surface use).

**Confirmed NOT button usages — correctly stay on the existing overloaded tokens, do not move:**
`Selection-controls.reference.html`, `Tab-bar.reference.html`, `View-options.reference.html` (all
`secondary/background/default` = CHECKED-state fill, not a button); `Reorder.reference.html`,
`Quick-actions.reference.html`, `List-items.reference.html`, `Table.reference.html`,
`Avatar.reference.html`, `Cards.reference.html` (all `tertiary/background/*` = SURFACE, not a button
fill); `Links.reference.html` (`primary/background/default` used for an arrow glyph, not a button).

This list is a starting survey, not a rebind plan — the brief was explicit that the snippet pass needs its
own careful survey (button-vs-surface disambiguation is genuinely delicate in a few of these, e.g.
`Modals`' `--sec-bd` naming). No snippet file was edited this session.

## Recommendation
Token group is clean, gate-verified, matches the ruled spec exactly, and is live in all 9 tranches with a
green 35/35 build. Two open items for the conductor/Dave, both already flagged above rather than decided
unilaterally: (1) confirm the `--pri`/`--icon-rev` blast radius (non-button accents going grey) is the
intended reading of "repoint the filled-button vars," and (2) the tranche `contrastPairs` are currently
unenforced by any gate — decide whether that's acceptable for now or worth a small gate-glob widening.
