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

## B-D3 — Hover = dual token; mechanism is selectable (2026-07-20). → ADR-0009.
Dave, iterated: hover is stored as **both** a colour token (`…/hover`, portable / chromatic-ready) **and**
an operational opacity (`…/hover-opacity`), *"still both but operationally different."* A theme/consumer
selects the render mechanism per state — **colour, opacity, or both** (*"we still allow the user to select
either or both"*). Mono's default hover = **opacity** (fill fades over `background/default`; the colour
value is the ramp-snapped opaque equivalent). Carried now as `$extensions.apollo.state` (non-breaking);
migrates to a first-class number/opacity token with the style-builder. Architecture formalised in
**ADR-0009**; a fully chromatic mode (red default / blue hover / green active) is the same skeleton with
mechanism `[colour]`.

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
