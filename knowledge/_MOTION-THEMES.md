# Motion themes — first-pass distillation (DRAFT for joint review)

Not canon. A starting point for the review-together session: the Route A explorations across the
eight components clustered into a small **family of reusable motion themes**, so we adopt *themes*
(and a handful of `motion/*` tokens) rather than per-component one-offs. Each theme below notes the
feel, where it already appears, a candidate curve/duration, and what it would tokenise to.

Today `tokens/motion.json` holds only `duration` (instant/fast/fade/standard) + `easing` (standard/linear).
The themes imply ~3 new easings and ~2 new durations.

## The candidate family

### 1. Reveal — "grow from the anchor"
Things appear by growing/scaling out of their origin rather than just fading.
- **Seen in:** Links underline grows from the left · Dropdown menu scales from the top + options stagger · Tooltip scales from the icon · Input focus underline grows.
- **Feel:** purposeful, directional, calm.
- **Candidate:** `motion/easing/soft` ≈ `cubic-bezier(.33,1,.68,1)`, duration `standard` (220ms); stagger ≈ 40ms/step.

### 2. Settle — "spring / overshoot"
State changes land with a slight overshoot for liveliness — reserved for confirmation moments.
- **Seen in:** Selection controls (check-draw, radio dot, switch thumb) · Badge pop-in · Dropdown chevron.
- **Feel:** lively, responsive, a touch playful.
- **Candidate:** `motion/easing/spring` ≈ `cubic-bezier(.5,1.6,.4,1)`, duration `motion/duration/spring` ≈ 320ms.
- **Caution:** use sparingly — too many springs reads frenetic (cf. the dropdown accent we rejected for being too much).

### 3. Tactile — "press physics"
Direct manipulation gets an immediate physical response on `:active`.
- **Seen in:** Button press squish (scale .97) · Switch thumb stretch.
- **Feel:** physical, satisfying, instant.
- **Candidate:** `motion/duration/press` ≈ 90ms, ease-out. No overshoot.

### 4. Roll-off — "fast in, slow out (trail)"
Hover cues snap in and linger out — asymmetric timing. **Chosen for the Dropdown accent (V2).**
- **Seen in:** Dropdown hover accent (130ms in / 620ms out).
- **Feel:** crisp to acquire, gentle to release; leaves a trail when scanning quickly.
- **Candidate:** in = `motion/duration/fast` (120ms); out = `motion/duration/slow` ≈ 600ms. Documented as an asymmetric *rule* (the entry rule is fast, the base/exit rule is slow), not a single token.

### 5. Attention — "pulse"
Passive, non-interactive draw — for things the user hasn't acted on yet.
- **Seen in:** Badge active dot ping.
- **Feel:** ambient, low-key, looping.
- **Candidate:** ~1.8s ease-out loop; honour `prefers-reduced-motion` (disable).

### 6. Transform — "morph through states"
A single control transforms through a sequence rather than swapping elements.
- **Seen in:** Button loading → success morph (spinner → drawn tick).
- **Feel:** continuous, reassuring on async actions.
- **Candidate:** composed of the above (fade + draw); duration per step `standard`/`fade`.

## Cross-cutting rules (apply to all themes)
- Every theme must degrade under `prefers-reduced-motion: reduce` (the showcases already do).
- Motion is decoration on top of an already-correct, accessible static state — never the only signal.
- Promotion to canon follows `_PROMOTION-QUEUE.md`: tokenise → meta `motion` block → gated reference.

## For the review
Decide: (a) which of the six themes we keep / merge / cut; (b) the exact curves + durations → `motion/*` tokens;
(c) per component, which theme(s) apply; (d) then promote per `_PROMOTION-QUEUE.md`.
