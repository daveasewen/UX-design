# Button decisions ledger (B-D#)

Running record of button-tier rulings + WHY, so feedback doesn't evaporate. Sibling to
`_TYPE-DECISIONS.md` / `_RAG-DECISIONS.md`. Architecture-level rulings promote to ADRs; this
ledger holds the button-specific calls and their provenance.

---

## B-D1 — Apollo Mono primary carries NO red (2026-07-20). Source: Dave. FIRM.
Dave: *"no red primary isn't a legitimate choice to Apollo Mono… Mono is [named] because the UI is
monochromatic, the only colour [is] dataviz, RAG and status."* So red is not "Legacy-only as a
carve-out" — it is **out of bounds for Mono, full stop**. The Mono primary is the highest-emphasis
**monochrome** button: near-black ground in light that **inverts to near-white in dark**. The legacy
red `primary/*` group is untouched (Legacy theme keeps it). Rule of thumb recorded.

Edges: bounds(R-D15)

## B-D2 — Mono primary token ladder minted; completes `button/*` (2026-07-20).
Following the 3-tier stack (component → semantic → primitive, `_STANDARDS.md §1`), same shape as the
secondary/tertiary/quaternary ladder:
- **Component:** `button/primary/{background/{default,hover,pressed,disabled}, label/{default,disabled}, icon/default}`.
- **Semantic (new):** `surface/action-primary`, `surface/action-primary-hover`, `surface/action-primary-pressed`;
  `icon/on-inverse`; `text/on-disabled` (see B-D4). Label reuses `text/on-inverse` (its own spec already
  names "primary pressed").
- **Primitive:** the `color/mono/*` ramp.
Registered in `_validate_token_tiers.py` (0 strict failures). **Snippet rebind deferred** — the Mono
button snippet still renders red primary until the batched `button/*` snippet rebind (queue #4); this
ruling lands the *token* foundation.

Edges: verified-by(knowledge/_validate_token_tiers.py)

## B-D3 — Hover = dual token; mechanism is selectable (2026-07-20). → ADR-0009.
Dave, iterated: hover is stored as **both** a colour token (`…/hover`, portable / chromatic-ready) **and**
an operational opacity (`…/hover-opacity`), *"still both but operationally different."* A theme/consumer
selects the render mechanism per state — **colour, opacity, or both** (*"we still allow the user to select
either or both"*). Mono's default hover = **opacity** (fill fades over `background/default`; the colour
value is the ramp-snapped opaque equivalent). Carried now as `$extensions.apollo.state` (non-breaking);
migrates to a first-class number/opacity token with the style-builder. Architecture formalised in
**ADR-0009**; a fully chromatic mode (red default / blue hover / green active) is the same skeleton with
mechanism `[colour]`.

Edges: refines(ADR-0009)

## B-D4 — Disabled label: contrast-exempt BUT must stay visible to sighted users (2026-07-20). Source: Dave.
Dave: *"it doesn't have to [be] accessible but invisible for normal sighted people isn't acceptable."*
The old `text/disabled` light value `#E1E1E1` **equalled the disabled ground** `#E1E1E1` → the label was
literally invisible (1.0:1). Fix: minted **`text/on-disabled` = `#808080`** (mono/8) both modes — a
deliberate ghost, ~3.0:1 (light) / 2.3:1 (dark): exempt from WCAG 1.4.3 (inactive component) yet clearly
perceptible. `button/primary/label/disabled` rebound onto it; added to the contrast allowlist. The other
button tiers likely share the old invisible-in-light defect (`button/{secondary,tertiary,quaternary}/label/disabled`
→ `text/disabled`) — flagged for the batched cleanup.

## B-D5 — Accessibility clamps the controls, not the ruling (2026-07-20). Source: Dave.
Dave: *"can I only have selections that pass Ally."* The review editor only offers AA-passing choices —
ramp steps failing label contrast are struck out & unclickable; the hover opacity dial is clamped to the
range where the flattened ground still passes. AA is a property of the *resolved* state, enforced at
selection time (per ADR-0004 / ADR-0009 §4).

Edges: refines(ADR-0004)

---

**Values — SETTLED (Dave, 2026-07-20, dialed on the v7 live editor):**
```
background/default : #1A1A1A m4  / #FAFAFA m14
hover.mechanism    : [opacity]  ·  hover.opacity 0.70 (operational)
hover (colour)     : #626262 m7  / #B7B7B7 m10   (stored equivalent — portable / chromatic-ready)
background/pressed : #000000 m1  / #FFFFFF m15
disabled fill      : #E1E1E1 m12 / #484848 m6    (surface/action-disabled)
disabled label     : #9D9D9D m9  / #808080 m8    (text/on-disabled — exempt, faint-but-visible by choice)
label / icon       : #FFFFFF / #333333           (text·icon/on-inverse)
```
Tokens synced to this; build green 35/35. Snippet rebind (render these operationally, incl. the 0.70
opacity hover) remains the deferred batched `button/*` pass (queue #4).

---

## B-D7 — Press physics: the Icon-button size-scoped model IS the family canon; motion is a THEME DIAL (2026-07-22). Source: Dave. FIRM.
Ruled during the ADR-0013 clean-room, in two beats — recorded both because the reversal is the ruling:
1. Asked whether Icon-button's documented size-scoped physics (+2px/−2px on the 44px target, darken .94)
   should flatten onto Button's shared proportional factors, Dave first ruled *"Switch to the shared 4%"* —
   then reversed within the hour: *"the movement in the icon button (its more subtle) is the one that
   should propagate to everything in console and Mono."* **The subtle, PIXEL-TRUE model wins**: travel =
   `motion/press/travel` (2px of size change), expressed as `scale(calc(1 ± travel/--phys-size))` where
   `--phys-size` is the member's LOCAL characteristic-size number (buttons ≈120 — the Tranche-1
   size-scoping; icon button 44, keeping its resolved values byte-identical). Darken = `motion/press/darken`
   (0.94). **Supersedes Button's promoted 2026-06-22 factor VALUES (1.04/0.95 + brightness .85); the rule
   shape survives** (grow toward cursor · press recede + darken · disabled stays put · reduced-motion snaps).
2. *"The movement should be absent from Legacy and Supercharge, just colour change. But of course this
   should be changeable in the future if finessing is needed."* **Motion is a THEME PROPERTY**: the Legacy +
   Supercharge override sets dial `travel→0, darken→1` (identity transforms — colour tokens alone carry
   state feedback); Mono carries the movement and Console inherits it (NOT added to the ADR-0014 locked
   fence, which was ruled for colour — flag if it should be). Constraint, Dave verbatim: *"as long as we
   don't use any js we may tune later"* — everything is CSS custom properties + calc (DEF-003 posture);
   tuning = editing a token value, no rule changes.
Enacted same hour: tokens `motion/press/{travel,darken}` + component-type tier caches
(`component-type/button-family/*`, knowledge/component-types.json) + theme-set overrides + the four
proof migrations (Button/Modals/Progress-tracker/Icon-button on the injected press-physics partial).
Visible deltas for Dave's eyeball: Button + Modals presses calm down; Progress-tracker translateY→scale;
Legacy/SC lose movement; Icon-button unchanged.

Edges: refines(ADR-0013) · verified-by(knowledge/_validate_partials.py)

## B-D6 — Mono success button = R-D14 GREEN fill, black label (2026-07-20). Source: Dave. FIRM.
The snippet rebind landed the `button/*` colours + operational-opacity primary hover (Mono, no red),
and folded the B-D4 disabled-label fix across all four tiers (siblings' `label/disabled` → `text/on-disabled`,
so light disabled labels are visible `#9D9D9D` not the invisible `#E1E1E1`). Then Dave caught the success
("Done") state still on the **Legacy teal** `#00847F`. Ruling: Mono success = the **R-D14 green FILL**
`rag/success-background` `#5DAC7B`/`#43AD6F`, with a **black** label per **type26-013** (white type is
red-only). Minted **`text/on-success`** (semantic, per-mode, both `#000000` today, alias `color/black`) —
kept per-mode deliberately so a future RAG can diverge light/dark without a structural change (Dave: tokens
must stay flexible). Black-on-green = 7.65:1 light / 7.45:1 dark; carve-out added in `_contrast_utils.py`
(on-success sits ONLY on the green fill, never the page ground — same shape as `text/on-action`). Build
green. **Leakage prevention → R-D17 + the new `_validate_legacy_leak.py` gate.**

Edges: refines(R-D14) · verified-by(type26-013)
