# Motion — brand guidance (ingested)

*Source: create.hsbc → Foundations → Motion (`foundations-and-identity/motion.html` +
`motion/motion-specifications.html`, **v1.0, updated 21 July 2022**), captured 2026-07-02 via
Dave's authenticated session (login-walled; ADR-0005 provenance applies). Engine-era format.
Capture note: one text range on the specifications page was unreadable through the extraction
tooling (video example captions — "expression curves applied to motion types" examples);
judged non-rule content from the surrounding structure and the visual pass. The After Effects
Motion Principles Toolkit (472 MB ZIP) exists but was not downloaded.*

## Scope note (important)

This is the BRAND motion standard — campaign film, OOH, social, hexagon animation (After
Effects toolkit). But its principles claim reach "across all platforms … all the way through
to app experiences", so it constrains UI micro-interaction motion unless a digital toolkit
says otherwise. Our UI motion canon lives in `tokens/motion.json` + `_MOTION-THEMES.md` +
`_PROMOTION-QUEUE.md`; the tension below is the headline finding.

## Key principles

- **Move along 45° and 90° angles.** [ADVISORY-derivable for generated animation —
  transform-vector check; note illustration uses 45°/22° (`illustration-standards.md`),
  motion uses 45°/90° — different angle grammars per medium] {#mot-001}
- **Use masks, not fades**; straight cuts for scene transitions; never fade or crossfade.
  Transitioning without a hexagon = straight cut. [ADVISORY-derivable — for UI: opacity-only
  transitions are the fade analogue; our scale-fade Modal motion may sit near this line]
  {#mot-002}
- **"Move with confidence — motion should be deliberate and not playful or bouncy."**
  [TASTE at brand level — but see Findings: collides with our promoted spring physics]
  {#mot-003}
- Motion complements and enhances; never distracts. [TASTE] {#mot-004}
- **Any motion over 5 seconds needs play and pause.** [BLOCKING-derivable — WCAG 2.2.2
  pause/stop/hide class; sibling of our gated prefers-reduced-motion rule] {#mot-005}
- Don't overuse motion principles in a timeline; deploy at key points, let content shine.
  [TASTE] {#mot-006}

## Structure — the motion equation

Three motion types: **Opening** (the hook, primary focus), **Advancing** (supporting role,
transitions/typography), **Emulating** (subject-matter-inspired). Usable individually or
combined (simultaneous or consecutive).

Equation: **motion type × asset × expression × speed** — asset ∈ {Open Hexagon, Cropped
Hexagon, Typography, Shape/block (digital)}; expression ∈ {Grow, Jump, Push, Slide,
Catalyst}; speed ∈ {Regular, Slow, Fast}. Expression curves are combinations of easing
curves; named eases: **ease out · ease in · ease in-and-out** — easing "simulates natural
forces like gravity and friction". Numeric curve values are NOT published on the page (they
live in the AE toolkit). [structure]

## Findings

1. **"Not playful or bouncy" vs our promoted spring physics.** Button "Refined
   scale-physics" (canon, 2026-06-22) uses an overshoot spring (`motion/easing/spring`
   ≈ cubic-bezier(.5,1.7,.4,1)); Selection-controls exploration is "deliberately springy".
   The brand standard says deliberate-not-bouncy across all platforms including apps. Read
   available: our scale-only, small-amplitude physics IS "confident and deliberate" (it was
   chosen over the unrestrained 3D-depress for exactly that reason), and this 2022 standard
   predates the refresh's own scale-physics-friendly direction (cheat-sheet principle 7).
   But the promotion queue should carry the tension explicitly and future motion promotions
   should cite it. NOT self-resolvable — Dave's call whether to (a) treat brand-film rules
   as out-of-scope for micro-interactions, or (b) constrain future promotions.
   [REVIEW] {#mot-007}
2. **Easing values are toolkit-locked.** The only retrievable curve facts are the three
   named ease families — no beziers published. Our `motion/easing/standard` etc. remain the
   operative source; if the AE toolkit's curves are ever needed, that's an asset-pipeline
   job (472 MB ZIP), not a page ingestion. [structure note]

## Cross-references

`_MOTION-THEMES.md` (our 6-theme exploration family) · `_PROMOTION-QUEUE.md` (promotion
path; tension noted there 2026-07-02) · `tokens/motion.json` · a11y gate
(prefers-reduced-motion, gated) · `illustration-standards.md` (angle grammar per medium) ·
brand-refresh cheat-sheet (`_BRAND-REFRESH-DIRECTION.md`).
