# Canon model + motion promotion queue

## The model (decided 2026-06-19, Dave)

Two tiers, with explicit promotion:

- **Canon** = the gated `snippets/*.reference.html` files. Token-faithful, accessible by default, enforced by the build gates, conservative motion (standard ease only). This is what ships.
- **Exploration** = the `_fitness-test/*-AB-showcase.html` files. Route A is the unconstrained "quality ceiling" — richer motion, a recorded **menu of options**. NOT canon, NOT gated.

**Promotion path** (a Route A treatment enters canon only when Dave explicitly blesses it):
1. Tokenise the motion — its easing curve(s) and duration(s) become `motion/*` tokens in `tokens/motion.json` (today they're hardcoded magic numbers in the showcases).
2. Write it into the component's `motion` block in its `*.meta.json`.
3. Add it to the gated `*.reference.html` so it's enforced.

Canon stays deliberate and accessible-first; the showcases stay a safe sandbox. **Token proposals live in `tokens/_proposals/` — OUTSIDE the resolving stores — until Dave's sign-off physically moves them in. A `$confidence` tag is not a fence; the store boundary is the fence (rule learned 2026-07-02).** **A review pass is owed** to walk the queue below and decide each.

## Pending promotion candidates (awaiting review)

| Treatment | Lives in | Notes |
|---|---|---|
| **Already promoted** — Input fields two-state focus (animated underline + keyboard-only ring) | canon ✓ | promoted because it's an accessibility feature, not just polish |
| **Already promoted** — Tabs responsive overflow + round count badge + softer press (2026-06-21) | canon ✓ | first prototype-grade promotion; build green; collapse animation deliberately dropped as over-complex (canon stays conservative) |
| **Already promoted** — Button "Refined scale-physics" (grow-toward-cursor on hover + press recede/darken, SCALE only — no shadow/translate) (2026-06-22) | canon ✓ | chosen over the unrestrained 3D-depress; realises refresh principle 7 brand-safely; tokenised motion/easing/spring + motion/duration/spring + motion/duration/press + motion/easing/out; build green; see button.meta `motion` |
| Dropdown hover accent — **V2** (black bar, fade, asymmetric roll-off trail: 130ms in / 620ms out) | `dropdown-AB-showcase.html` Route A | Dave approved the look ("2 is good"); not yet folded into the gated reference |
| ~~Button — hover lift (translateY −1px) + press squish~~ → **PROMOTED 2026-06-22** as Refined scale-physics | `button-3up-showcase.html` Refined tier | shipped as SCALE-only (grow + recede/darken). The translateY-lift + inset-shadow 3D-depress stay a recorded exploration **ceiling** (Unrestrained), NOT canon |
| Button — loading → success morph (spinner → drawn tick) | `button-AB-showcase.html` Route A | exploration; not reviewed for canon |
| Selection controls — spring/overshoot on check-draw, radio-dot, switch-thumb + press-stretch | `selection-controls-AB-showcase.html` Route A | "deliberately springy"; canonical reference uses standard ease |
| Links / Badge / Tooltip — Route A motion | `*-AB-showcase.html` (being built) | TBD |
| **`inverse/surface` role** — brand dark surface for light-mode use, derived from dark-theme values | charter §4 ratification (2026-07-02, Dave) | **PROPOSED 2026-07-02, holding pen** (`tokens/_proposals/` — inverse/surface + inverse/text, derived from grey/dark-mode/600). NOT in the store; enters only on Dave's V6 sign-off. Was candidate token #1 on the balanced SME screen |
| **Expressive elevation/gradient ramp** — the defined ramp that unlocks flatness in *expressive* only | charter §4 ratification (2026-07-02, Dave) | **PROPOSED 2026-07-02, holding pen** (`tokens/_proposals/` — gradient/expressive hero|neutral stops, derived from complimentary ramp + dark-mode neutrals). NOT in the store; expressive gets legal gradient values only on V6 sign-off |

## Tags / chips — notes for the promotion pass
- Chip motion settled (exploration `_fitness-test/tags-chip-animation.html`): **V1 collapse+fade** exit;
  subtle chip press (scale 1.05 / 0.97); prominent **tactile cross** (1.4 / 1.15) — same physics as the button.
- Chip is now **em-based** (height/padding/gap/cross all track the label's font-size) → scales with type.
  When promoting to the gated reference, use em sizing throughout (not fixed px). **TODO (future):** the
  em ratios are tuned for ~13px; **may need adjustment at larger sizes** — padding/height proportions and the
  cross can feel heavy when scaled up (optical sizing).
- **Icon line width is already proportional** — `stroke-width` lives in the SVG's viewBox units, so scaling the
  SVG via em scales the stroke with it. Levers if we want different behaviour: `vector-effect:non-scaling-stroke`
  pins the line to a constant device-px regardless of size (keeps fine lines crisp at large sizes); or set
  `stroke-width` per size for optical balance (thinner relative stroke at large sizes — aligns with the
  refresh's "elegant / thinner" type direction). Worth a deliberate call at promotion.

## Motion tokens needed if/when promoting

`tokens/motion.json` currently has only basic duration (instant/fast/fade/standard) + easing (standard/linear). Promoting the richer treatments would add, e.g.:
- `motion/easing/spring` (overshoot, ~`cubic-bezier(.5,1.7,.4,1)`)
- `motion/easing/soft` (gentle decel, ~`cubic-bezier(.33,1,.68,1)`)
- `motion/duration/slow` (~600ms, for the roll-off trail) and a `motion/duration/spring` (~300–340ms)
- asymmetric in/out pattern documented as a rule (fast in, slow out) rather than a single token
