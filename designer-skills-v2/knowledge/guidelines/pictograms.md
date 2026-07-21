# Pictograms — brand guidance (ingested)

*Source: create.hsbc → Foundations → Icons and pictograms →
`icons-and-pictograms/pictograms.html` (+ asset-class rules from the hub page), captured
2026-07-02 via Dave's authenticated session (login-walled; ADR-0005 provenance applies).
Enforcement destinies + rule IDs per the engine-era format. Companion to `icons.md`;
a "legacy pictograms" collection exists on the site for the previous style.*

## Definition and scope

Idea-driven, **not interactive** (unless contained within a UI pattern), digital + physical
(presentations, print, signage, wayfinding). Larger and more detailed than icons; smaller and
less narrative than illustration. If a message can't be carried by a single metaphor, use a
photograph or illustration instead.

- **Every pictogram carries a label or copy that underpins its meaning** — no exceptions
  (unlike icons' universal-meaning carve-out). [BLOCKING-derivable — pictogram-without-label
  check] {#pict-001}
- Not a replacement for icons or illustrations; never interchange. [ADVISORY] {#pict-002}
- Don't use pictograms as a replacement for a hero illustration. [ADVISORY] {#pict-003}

## Levels (three treatments of one concept)

**Level 1 — Keyline · Level 2 — Grey · Level 3 — Full colour.** Prominence tracks the
message's importance; size is NOT a defining characteristic of level (large signage may be
L1 while a small brochure figure is L2).

- Use levels to reflect message importance; **don't mix levels in components representing
  messages of equal prominence.** [ADVISORY-derivable — per-view level-consistency check;
  same family as the data-vis categorisation-consistency rule] {#pict-004}

## Content

- Keep metaphors simple and globally recognisable; avoid unnecessary abstraction (bowl +
  steam, not the bowl's contents). Abstract designs only for figurative concepts (FX,
  sustainability) and never reliant on prior knowledge. [TASTE] {#pict-005}
- No designs without a clear relationship to the message they support. [TASTE] {#pict-006}

## Placement and colour

- **Don't place pictograms on a red background** — interferes with the red accent and
  causes contrast issues with the primary form. [BLOCKING-derivable — background check;
  sibling of col26-004's no-text-on-red] {#pict-007}
- **≥3:1 contrast against the background in all placements**, with clearly descriptive alt
  text. L1 on dark backgrounds only with white lines; L1 over photography only where the
  background doesn't compromise contrast; nothing on visually busy imagery.
  [BLOCKING-derivable for the ratio — indicator-contrast gate class; ADVISORY for the
  busy-imagery judgment] {#pict-008}
- **No drop shadows** — elevation is functional-only (an object moving over another), which
  a pictogram never needs. [BLOCKING-derivable — effects check; consistent with charter §4
  flatness] {#pict-009}

## Sizing

- **Digital: minimum 60px, maximum 192px, proportional scaling at 2px intervals.** Below
  60px, use an icon instead. [BLOCKING-derivable — rendered-size check] {#pict-010}
- **Never squash, stretch, skew or distort; scale with locked aspect ratio.**
  [BLOCKING-derivable — aspect-ratio check] {#pict-011}
- Don't position different-scale pictograms immediately next to one another in common
  components; max **3 distinct sizes per experience**, logically chosen. [ADVISORY-derivable
  — countable per view/journey] {#pict-012}
- Non-digital (print, physical): scale proportionally to the format with sufficient clear
  space; legibility at small sizes. [TASTE] {#pict-013}

## Findings

1. **Pictograms are a component-library gap.** The engine's 38 components include icons
   (sprite + gate) but no pictogram asset class at all — no tokens, no assets, no manifest
   entry. If generated experiences ever include pictogram-bearing patterns (empty states,
   onboarding, confirmation illustrations), this class needs onboarding: distinct contrast
   rule (3:1 + alt), distinct size floor (60px), level system, and a sourcing pipeline
   (create.hsbc asset library + "Pictogram creation" approvals process for new symbols).
   Parked — no current snippet uses pictograms. [REVIEW] {#pict-014}

## Cross-references

`icons.md` (companion; the 4.5:1 vs 3:1 asset-class split) · `illustration-standards.md`
(the third tier) · `colour-standards-2026.md` (red-background family) · charter §4
(flatness/no-shadow alignment).
