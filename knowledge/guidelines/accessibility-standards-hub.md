# Digital accessibility standards hub — WCAG 2.2 adoption map (ingested)

*Sources: create.hsbc → Platforms and channels → `Accessibility_Standards.html` + subpages
`new-standards.html` + `wcag-2-1-to-wcag-2-2-changes.html` + `legacy-standards.html`,
captured 2026-07-03 via Dave's authenticated session (login-walled; ADR-0005 provenance
applies). Engine-era format. THE AUTHORITATIVE 2.2 ADOPTION MAP — validates the
2026-07-03 axf-001 re-baseline ruling line-for-line (F1). Upgrades the Tier-1 ◐ partial
capture of this page to a full ingest.*

## The bar (rules)

- **Minimum permitted level = the Digital Accessibility Framework, based on WCAG 2.2
  AA, governed by Group Digital Experience and Accessibility** — applies to ALL HSBC
  digital projects; "digital experiences must always be planned and built with
  accessibility in mind, as adaptations to existing experiences can be very costly".
  [RECORDED — confirms axf-001 + the gdea governance seat; build-it-in-not-retrofit is
  the certified-component pitch] {#axs-001}
- **The 2.2 adoption map (framework updated 2024)** — "meeting all Standards is broadly
  equivalent to WCAG 2.2 conformance"; Standards failures raise DEFECTS. Adopted as
  STANDARDS: 2.4.11 Focus Not Obscured (→CD-47) · 2.5.7 Dragging (→CD-48) · 2.5.8
  Target Size (merged+upgraded, →ID-26) · 3.2.6 Consistent Help (→ID-27) · 3.3.7
  Redundant Entry · 3.3.8 Accessible Authentication (→ID-28). Adopted as GUIDELINE:
  2.4.13 Focus Appearance (AAA, →VD-9). **4.1.1 Parsing re-categorised Standard →
  RECOMMENDATION** (kept, not dropped — refines our 2.2 map's "removed" note; CD-44 is
  its carrier). [RECORDED — the source-of-truth mapping for the `_A11Y-AUDIT.md`
  per-criterion table; matches the enacted map on all six + the 2.4.13 guideline tier]
  {#axs-002}
- **Target-size priority clause** — 2.5.8's 24×24 is the WCAG minimum, but "in many
  cases HSBC already has guidance in place which EXCEEDS this minimum requirement.
  Existing guidance of a target size of 44 x 44 pixels TAKES PRIORITY." [RECORDED —
  second source receipt for aid-009's REVIEW (first: ID-26). The 44 bar is stated
  twice at source; the gate-upgrade candidate (advisory <44, fail <24) now has a
  two-receipt case] {#axs-003}
- **Focus appearance gets NUMBERS (2.4.13 as Guideline = VD-9)** — a visible focus
  indicator must have: **solid ≥2 CSS px perimeter** + **≥3:1 contrast against its own
  UNFOCUSED state**; browser defaults may pass on links but often not on form
  controls. [ADVISORY — the queued render axis (2.4.11 family) now has its numeric
  spec: VD-9's focused-vs-unfocused pixel delta is officially ≥3:1 with a 2px floor.
  Feeds the focus-appearance render check design] {#axs-004}
- **Redundant entry detail (3.3.7)** — same-session journeys never prompt for the same
  information twice unless auto-populated or selectable; techniques: autofill, stored
  account data, pre-population; exceptions: invalidated info, security. [RECORDED —
  detail for the journey-criteria route on the 2.2 map] {#axs-005}

## Lineage (rules)

- **The institutional timeline** — WCAG 2.0 (2008) missed mobile/widgets → **HSBC
  created the framework in 2013** to fill the gap; 2.1 (2018) adopted into the
  framework 2019; 2.2 (Oct 2023) adopted 2024. Legacy page also preserves the 2.1
  delta grouping, including the editorial judgment "2.5.5 Target Size (AAA), but
  arguably should be AA" — the intellectual ancestry of the 44 bar. [RECORDED —
  hard dates for the layered-vintages model (amr F1): 2013 base · 2019 patch · 2024
  patch; per-section vintage sniffing now has anchors] {#axs-006}
- **Source cross-reference wobble** — the changes page maps 3.3.7 to "Standard VD-8"
  (a visual-designers slot) and files ID-28 under "guidelines" where the ID page says
  STANDARD; 3.3.8 once labelled (A), actually AA. [RECORDED — the framework role pages
  prevail on tiering; wobble logged, not chased] {#axs-007}

## Findings

- **F1 — the morning's ruling is validated at source**: the enacted `_A11Y-AUDIT.md`
  per-criterion map matches the institution's own adoption table on every SC and tier.
  One refinement folded in: 4.1.1 lives on as a Recommendation rather than vanishing.
- **F2 — the pending desk batch just got stronger**: aid-009 (target-44) now carries
  two source receipts (ID-26 + axs-003's "takes priority" clause), and the queued
  render axis has numerics (axs-004: 2px + 3:1-vs-unfocused). Both ready for one
  sitting.
- **F3 — `creating-accessible-content.html` swept in the same pass**: a video-tutorial
  hub (4 chapters: language/style · alt text · structure · accessible video) — staff
  training assets, no text rules; content duplicated by aca-*/avd-*; videos not
  capturable. Marked done in the queue as a hub note.
