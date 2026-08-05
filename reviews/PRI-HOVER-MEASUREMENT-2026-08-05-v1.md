# `--pri-hover` measurement + decision pack

*Measured 2026-08-05 (Sonnet sub, session #104, conductor Opus). This is a MEASUREMENT, not a
promotion — closing #99's residual ① ("`--pri-hover` stored equivalents at retired 0.70") is
Dave's call alone. Nothing in this document has been enacted, minted, or swept. Live specimen:
`reviews/PRI-HOVER-MEASUREMENT-2026-08-05-v1.html` (render-verified, screenshots below).*

---

## Plain summary

Nine places in the component library paint a button's hover state using the same idea — the
solid primary colour "fading" toward the page background. One of them (Button) was already moved
onto the new `--alpha-68` primitive back in #99. The other eight were left behind, still working
off the old 0.70 value in one of two ways: four of them compute the fade live in the browser at a
literal 70%, and four of them paint a frozen, pre-computed colour that was baked at 70% some time
ago and never recalculated.

**The good news: every one of these deltas is tiny.** Moving all eight to match Button's
`--alpha-68` shifts each colour by at most 5 shades out of 255 — imperceptible on a screen, and
every contrast ratio involved stays comfortably clear of the accessibility floor, in both light and
dark mode. None of the colours involved carry any hue at all (they're all pure neutral greys), so
none of this touches Dave's red/amber problem-hue territory.

**The one genuinely new finding:** the frozen "stored equivalent" colour (`#626262` / `#B7B7B7`)
was never a pure mathematical 70% mix in the first place — its own token description says it was
"opacity-derived then ramp-snapped" to the nearest named grey. Recomputing that snap at the *new*
68% target lands on **the exact same named grey, in both light and dark** — meaning if the frozen
sites keep their current "stored colour" architecture, closing this residual could cost **zero
pixels of change**, just a corrected description of what the number is. If instead the four frozen
sites are switched over to the same live formula Button uses, there's a small quantified shift
(worst case 5/255, contrast ratio moves from 6.3:1 to 5.96:1 dark — still far above the 4.5:1 text
floor).

**Recommendation (mine, not a decision):** treat this as a documentation correction plus one small
mechanical swap, not a redesign — see "The choice for Dave" below.

---

## The measurement table

| # | Site | Current mechanism | Classification | Delta if → `--alpha-68` |
|---|------|-------------------|-----------------|--------------------------|
| 0 | **Button** *(reference — already enacted, #99)* | live `color-mix(…, calc(var(--alpha-68)*100%), …)` | — already the target | none |
| 1 | Icon-button | live `color-mix(…, 70%, …)` | **(b) swap, quantified delta** | L +4/255, D −5/255 |
| 2 | Empty-state | live `color-mix(…, 70%, …)` | **(b) swap, quantified delta** | L +4/255, D −5/255 |
| 3 | Form-layout | live `color-mix(…, 70%, …)` | **(b) swap, quantified delta** | L +4/255, D −5/255 |
| 4 | Stepper | live `color-mix(…, 70%, …)` | **(b) swap, quantified delta** | L +4/255, D −5/255 |
| 5 | Modals | flat `background:var(--pri-hover)` (frozen `#626262`/`#B7B7B7`) | **(a) exact if ramp-snap kept** / (b) if unified to live formula | ramp-snap: **0** · unified: L +1/255, D −5/255 |
| 6 | Action-bar | flat `background:var(--pri-hover)` | same as Modals | same as Modals |
| 7 | Confirmation | flat `background:var(--pri-hover)` | same as Modals | same as Modals |
| 8 | Drawer | flat `background:var(--pri-hover)` | same as Modals | same as Modals |
| — | Legacy / Supercharge theme overrides | flat authored hex (`#BA1110` / `#493F39`,`#806E65`) | **(c) not promotable** — never opacity-derived | n/a — out of scope, flagged below |

All eight in-scope rows are **pure neutral grey (R=G=B)** at every stage — no hue, so no problem-hue
hit. The out-of-scope Legacy value (`#BA1110`) **is** a problem hue (red) — flagged, not actioned.

---

<details>
<summary><b>Technical detail — how every site was found and measured</b></summary>

### Survey method

`grep -rn "pri-hover" knowledge/canon/canon.css knowledge/snippets/` plus a full-corpus file
search. Nine snippet files declare `--pri-hover` in their component scope: `Action-bar`, `Button`,
`Confirmation`, `Drawer`, `Empty-state`, `Form-layout`, `Icon-button`, `Modals`, `Stepper`
(`knowledge/snippets/*.reference.html`, mirrored into `knowledge/canon/canon.css`).

### Ground truth (quoted, not recalled)

`knowledge/tokens/semantic-colour.json`:
```
button/primary/background/default : light #1A1A1A / dark #FAFAFA
button/primary/background/hover   : light #626262 / dark #B7B7B7
  $alias -> surface/action-primary-hover -> color/mono/7 (#626262) & color/mono/10 (#B7B7B7)
  $extensions.apollo.state: {mechanism:['opacity'], opacity:0.7, colourIsEquivalent:true,
    note:"Mono hover renders via OPACITY... fades: button/primary/background/default, over: background/default"}
button/primary/label/default      : light #FFFFFF / dark #333333  (== button/primary/icon/default)
background/default                : light #FFFFFF / dark #1A1A1A
tertiary/background/default       : light #FFFFFF / dark #1F1F1F   (Modals'/Drawer's own card)
```
`surface/action-primary-hover` carries its OWN, older `$note`, which **disagrees with the note
above**:
```
"Hover value is opacity-DERIVED then ramp-SNAPPED: the default ground faded toward the page
background (α≈0.90) and snapped to the nearest color/mono step, so the ergonomics are 'just
opacity' but the stored artifact is a compliant ramp colour... ruled 2026-07-20."
```
`knowledge/tokens/opacity.json`: 4%-step ladder, `alpha-68 = 0.68`, no `alpha-70` step exists
(ladder is …64, 68, 72…) — confirms #99-D3's "ties round down" (70 is equidistant, rounds to 68).

### The mixing formula, verified against #99's own proof before use

CSS `color-mix(in srgb, A P%, B)` = simple per-channel weighted average in gamma-encoded sRGB
(`result = A·P + B·(1−P)`), **not** linear-light. Verified by reproducing #99's own measurement
exactly before trusting the formula for anything else:

| check | computed | ledger's own #99 measurement | match |
|---|---|---|---|
| light, 68% mix of #1A1A1A over #FFFFFF | R = 99.28 | "srgb 0.389333 = 99.28" | ✓ exact |
| dark, 68% mix of #FAFAFA over #1A1A1A | R = 178.32 | "(dark 178.32 ✓)" | ✓ exact |

### The two "70%" numbers do not agree with each other

| | light channel | hex | dark channel | hex |
|---|---|---|---|---|
| Stored token (`#626262`/`#B7B7B7`) | 98 | `#626262` | 183 | `#B7B7B7` |
| Clean 70% color-mix, computed fresh | 94.70 → 95 | `#5F5F5F` | 182.80 → 183 | `#B7B7B7` |

**Dark matches exactly. Light is 3/255 off.** This confirms the older `$note`'s account (ramp-snap
from an approximate fade, not a precise formula) rather than the newer `$extensions` note's clean
"opacity: 0.7" framing — the stored light value was never a bit-exact 70% mix to begin with. This
drift **predates and is independent of** the alpha-ladder question; it is not something #99 or #102
introduced.

### Ramp-snap re-check at the new target

`color/mono` ramp (from `knowledge/tokens/colour.json`): `…6:#484848, 7:#626262, 8:#808080…` and
`…9:#9D9D9D, 10:#B7B7B7, 11:#CECECE…`. Nearest step to the **new** 68%-mix target
(light 99.28, dark 178.32):

- light: nearest step is **mono/7 = `#626262`** (distance 1) — the currently-stored step, unchanged.
- dark: nearest step is **mono/10 = `#B7B7B7`** (distance 5, next-nearest mono/9 is 21 away) — also
  unchanged.

**If the ramp-snap methodology is preserved, re-deriving at 0.68 produces the identical stored
values already in the token store.** Nothing to promote but the description.

### Per-row rendered CSS, quoted

```
Button        (enacted): .cn-button .btn.primary:hover{background:color-mix(in srgb, var(--pri-default) calc(var(--alpha-68) * 100%), var(--page));}
Icon-button:             .cn-icon-button .iconbtn.primary:hover{background:color-mix(in srgb, var(--pri-default) 70%, var(--page));}
Empty-state:             .ebtn:hover{ background:color-mix(in srgb, var(--pri) 70%, var(--page)); }
Form-layout:             .fl-btn.fl-primary:hover{background:color-mix(in srgb, var(--pri-default) 70%, var(--page));}   /* B-D3 operational 0.70 opacity over the page */
Stepper:                 .st-nav .st-primary:hover{background:color-mix(in srgb, var(--pri-default) 70%, var(--page));}   /* B-D3 operational 0.70 */
Modals:                  .cn-modals .btn.primary:hover{background:var(--pri-hover);}
Action-bar:               .cn-action-bar .action-bar .btn.primary:hover{background:var(--pri-hover);}
Confirmation:            .cn-confirmation .confirm .btn.primary:hover{background:var(--pri-hover);}
Drawer:                  .cn-drawer .dbtn.primary:hover{background:var(--pri-hover);}
```
All nine share the same `--pri-label`/`--pri-glyph` chain (`button/primary/label/default` /
`button/primary/icon/default`, white light / `#333333` dark) — confirmed by direct read of each
component's variable block, not assumed from the pattern.

</details>

---

<details>
<summary><b>Technical detail — contrast ratios (computed via <code>knowledge/_contrast_utils.py</code>, colours compared as colours)</b></summary>

Label (or Icon-button's glyph, same value) painted on the hover fill:

| state | light label on fill | dark label on fill |
|---|---|---|
| Current — stored token (Modals/Action-bar/Confirmation/Drawer) | `#FFFFFF` on `#626262` = **6.1:1** | `#333333` on `#B7B7B7` = **6.3:1** |
| Current — live 70% (Icon-button/Empty-state/Form-layout/Stepper) | `#FFFFFF` on `#5F5F5F` = **6.39:1** | `#333333` on `#B7B7B7` = **6.3:1** |
| Proposed — `--alpha-68` (all eight, and Button today) | `#FFFFFF` on `#636363` = **6.01:1** | `#333333` on `#B2B2B2` = **5.96:1** |

Hover fill against the surface it actually sits on (non-text, 3:1 UI floor):

| | light (vs `#FFFFFF` page/card) | dark, Button/Icon-button/Empty-state/Form-layout/Stepper/Action-bar/Confirmation (vs `#1A1A1A` page) | dark, Modals/Drawer (vs `#1F1F1F` own card) |
|---|---|---|---|
| stored token | 6.1:1 | 8.68:1 | 8.22:1 |
| live 70% | 6.39:1 | 8.68:1 | — |
| `--alpha-68` | 6.01:1 | 8.21:1 | 7.77:1 |

**Every cell clears both the 4.5:1 text floor and the 3:1 UI floor, before and after.** The worst
single movement is dark text-on-fill, 6.3:1 → 5.96:1 — still 1.46:1 of headroom above the 4.5:1
requirement. No promotion path considered here creates an accessibility regression.

</details>

---

## Problem-hue flag (Dave is astigmatic — red/amber are the problem hues, blue/green are stable)

- **All eight in-scope rows, both before and after promotion, are neutral grey** (`R=G=B` exactly
  at every stage measured). Zero hue in play. Nothing here needs the red/amber caution.
- **Found but explicitly out of scope:** a *different, unrelated* `--pri-hover` declaration exists
  at canon.css's generic root convenience block (`--pri-hover: var(--primary-background-hover)` →
  **`#BA1110`**, a dark brand red) and is repeated as a per-theme override on nine *other*
  components (`account-selector`, `breadcrumbs`, `chart-sparkline`, `divider`, `dropdown`,
  `file-upload`, `hero`, `modal-lightbox`, `status-indicator`) under `[data-apollo-theme="legacy"]`.
  This is a flat, authored brand-red hover — never opacity-derived — so there is no alpha value to
  map it to; it is unrelated to the Mono ADR-0009 mechanism this measurement covers. **It is red,
  which is a problem hue**, so it's named here for awareness even though it is not actionable in
  this pack. (Separately, `button/primary/background/hover` itself is overridden to this same
  `#BA1110` for Legacy and to `#493F39`/`#806E65` — a desaturated warm neutral, not a clear
  problem hue — for Supercharge; both bypass the opacity mechanism entirely per ADR-0009's
  per-theme `mechanism:[colour]` option, which is intentional and pre-existing, not a defect.)

---

## The choice for Dave

*(Options below — none pre-selected. ★ marks the one I'd recommend if asked, per the plain-summary
above; it is not applied.)*

1. **★ Recommended — close it as a documentation fix + one mechanical swap.** Group A (Icon-button,
   Empty-state, Form-layout, Stepper): swap the literal `70%` for `calc(var(--alpha-68) * 100%)` —
   identical edit to what Button already got in #99, same tiny quantified delta. Group B (Modals,
   Action-bar, Confirmation, Drawer): keep the frozen "stored colour" architecture as-is (still
   `#626262`/`#B7B7B7` — the ramp-snap re-check found no closer step), and correct
   `surface/action-primary-hover`'s `$note` to say 0.68 instead of the conflicting 0.70/0.90 it
   currently carries. **Net visual change: only the four Group A sites, ≤5/255.**
2. **Promote Group B by re-baking the stored hex** to the literal `--alpha-68` mix value
   (`#636363`/`#B2B2B2`) rather than keeping `#626262`/`#B7B7B7`. Slightly more "correct" to the
   formula, breaks the ramp-snap naming (`color/mono/7`/`/10` no longer literally describes the
   token), quantified delta L+1/255, D−5/255.
3. **Unify mechanism** — convert Group B from a flat frozen colour to the same live
   `color-mix(var(--pri-default), calc(var(--alpha-68)*100%), var(--page))` formula Button uses.
   Most architecturally consistent (tracks future page/pri-default changes automatically instead of
   freezing a snapshot); touches four components' CSS, not just a token value — bigger surface than
   options 1–2.
4. **Decline / leave at 0.70.** Keeps today's small, pre-existing three-way inconsistency between
   Button (0.68), the live-70% group, and the frozen-token group. No risk, no work, residual stays
   open.

---

## Residual / UNPROVEN — declared honestly

- **Not confirmed either way:** whether the nine Legacy/Supercharge-overridden components named in
  the problem-hue flag (`account-selector`, `breadcrumbs`, etc.) actually consume their own
  `--pri-hover` declaration in a live CSS rule — their own snippet source files don't contain the
  string "pri-hover" at all, which reads as unused/vestigial, but I have not read each of those
  nine components' full rule sets to rule out an indirect (partial-injected) consumer. Flagged, not
  asserted.
- **Not measured:** Legacy's and Supercharge's own internal consistency between Button's *live*
  formula (which would compute its own hover from *their* `--pri-default` + `--page`, not from
  `--pri-hover` at all) versus their flat `--pri-hover`/`--button-primary-background-hover`
  overrides — i.e. whether Legacy/Supercharge have the same live-vs-frozen split Mono does. Out of
  scope for this pack (Mono/ADR-0009's opacity residual only); flagged as a possible follow-on.
- **Working tree, not a fresh build:** measurements read `knowledge/canon/canon.css` and
  `knowledge/tokens/*.json` as currently on disk. `_build_all.py` was not run (per constraint), so
  this does not re-verify the generator would reproduce the same canon.css from the snippets today
  — only that the two currently agree at every site checked.
- **Specimen captions are pre-computed, not live-JS-verified.** The HTML specimen paints real
  `color-mix()` swatches (browser-computed), but the numeric captions under each chip are the
  Python-computed values transcribed in, not re-computed by in-page script. Render-verified at
  420px and 1280px (screenshots below) — font loads as the licensed HSBC cut, grid collapses to one
  column on mobile / two on desktop as intended.

---

## Render-verify (seen, not just produced)

Rendered via Playwright/Chromium-headless-shell in-sandbox, `goto("file://…")`, real HSBC font
(`document.fonts.check('16px HSBC_MtUnivers_Latin')` → `true` at both widths).

| width | rows painted | grid columns | font |
|---|---|---|---|
| 420px | 9 | 1 | HSBC_MtUnivers_Latin ✓ |
| 1280px | 9 | 2 | HSBC_MtUnivers_Latin ✓ |
