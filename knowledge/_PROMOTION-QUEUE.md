# Canon model + motion promotion queue

## The model (decided 2026-06-19, Dave)

Two tiers, with explicit promotion:

- **Canon** = the gated `snippets/*.reference.html` files. Token-faithful, accessible by default, enforced by the build gates, conservative motion (standard ease only). This is what ships.
- **Exploration** = the `_fitness-test/*-AB-showcase.html` files. Route A is the unconstrained "quality ceiling" — richer motion, a recorded **menu of options**. NOT canon, NOT gated.

**Promotion path** (a Route A treatment enters canon only when Dave explicitly blesses it):
1. Tokenise the motion — its easing curve(s) and duration(s) become `motion/*` tokens in `tokens/motion.json` (today they're hardcoded magic numbers in the showcases).
2. Write it into the component's `motion` block in its `*.meta.json`.
3. Add it to the gated `*.reference.html` so it's enforced.

Canon stays deliberate and accessible-first; the showcases stay a safe sandbox. **A review pass is owed** to walk the queue below and decide each.

## Pending promotion candidates (awaiting review)

| Treatment | Lives in | Notes |
|---|---|---|
| **Already promoted** — Input fields two-state focus (animated underline + keyboard-only ring) | canon ✓ | promoted because it's an accessibility feature, not just polish |
| Dropdown hover accent — **V2** (black bar, fade, asymmetric roll-off trail: 130ms in / 620ms out) | `dropdown-AB-showcase.html` Route A | Dave approved the look ("2 is good"); not yet folded into the gated reference |
| Button — hover lift (translateY −1px) + press squish (scale .97) | `button-AB-showcase.html` Route A | Dave liked it ("rise and squish"); shadow removed per his note |
| Button — loading → success morph (spinner → drawn tick) | `button-AB-showcase.html` Route A | exploration; not reviewed for canon |
| Selection controls — spring/overshoot on check-draw, radio-dot, switch-thumb + press-stretch | `selection-controls-AB-showcase.html` Route A | "deliberately springy"; canonical reference uses standard ease |
| Links / Badge / Tooltip — Route A motion | `*-AB-showcase.html` (being built) | TBD |

## Motion tokens needed if/when promoting

`tokens/motion.json` currently has only basic duration (instant/fast/fade/standard) + easing (standard/linear). Promoting the richer treatments would add, e.g.:
- `motion/easing/spring` (overshoot, ~`cubic-bezier(.5,1.7,.4,1)`)
- `motion/easing/soft` (gentle decel, ~`cubic-bezier(.33,1,.68,1)`)
- `motion/duration/slow` (~600ms, for the roll-off trail) and a `motion/duration/spring` (~300–340ms)
- asymmetric in/out pattern documented as a rule (fast in, slow out) rather than a single token
