# Illustration standards — brand guidance (ingested)

*Source: create.hsbc → Foundations → Illustration (`foundations-and-identity/illustration.html` +
`illustration/style.html`, **v2.1, updated 01 December 2022** — pre-refresh), captured 2026-07-02
via Dave's authenticated session (login-walled; ADR-0005 provenance item applies). Enforcement
destinies as per `colour-standards-2026.md`. ⚠ The refresh's illustration style guidelines are
"currently in development" (per the 2026 supporting-palette page) — this standard is the operative
one but its palette rules are already partially superseded; tensions marked inline.*

## Key takeaways (source's own list)

- Never use illustration as the principal creative medium — **photography first**. [TASTE] {#ill-001}
- **Never use data visualisation or RAG palettes for illustrations.** ⚠ **SUPERSEDED 2026:** the
  unified supporting palette explicitly grants "the full supporting palette" to illustration
  (see `colour-standards-2026.md`). Under the refresh this rule inverts from "separate palettes"
  to "one palette, shared". Old rule kept for pre-refresh work only. [REVIEW — enforcement must
  key off which standard a brief targets] {#ill-007}
  Edges: conflicts-with(colour-standards-2026, resolution=ruled)
- Limit the number of colours within an illustration; use HSBC Red tactically to draw focus.
  [ADVISORY-derivable — distinct-fill count] {#ill-002}
- Build illustrations from **geometric shapes** — squares, circles, triangles. [TASTE] {#ill-003}
- **Stick to a single level of illustration through a customer experience.**
  [ADVISORY-derivable — per-journey consistency check; same class as the data-vis
  categorisation-consistency rule] {#ill-008}

## Style system — one style, three levels

Fixed attributes (all levels): **colours, defined angles (45° and 22°), geometric shapes, content
consideration.** Flexible attributes: level of detail, perspective, shading.

- **Level 1** — low detail; full palette prioritising Base colours; no shading; no perspective;
  clear geometry; exaggerated features.
- **Level 2** — medium detail; full palette prioritising Base colours; shading with solid colours;
  optional perspective; exaggerated features.
- **Level 3** — high detail; full palette; shading with texture; realistic features; optional
  perspective.

Three overarching characteristics: **colour and texture** (clean block colours + subtle texture),
**geometry** (45°/22° angles, simple shapes), **content consideration** (refined, simple, elegant —
understandable at a glance).

## Considerations (do/don't)

- Don't use object illustrations as icons or pictograms — those have their own visual style.
  [ADVISORY — aligns with our icon-source rule: icons come from the icon library, never from
  illustration assets] {#ill-009}
- Don't mix mediums — no illustration composited with photography. [ADVISORY-derivable] {#ill-004}
- Don't use 3D rendered objects. [ADVISORY-derivable — consistent with the flatness charter §4] {#ill-005}
- **Don't use typography within illustrations.** [BLOCKING-derivable — text-node-in-illustration
  check on generated SVG] {#ill-010}
- Don't use caricatures; don't make illustrations cartoonish; no keyline styles; no over-complex
  characters or fine detail; abstract only if understandable at a glance; present wide cultural
  diversity, tailored per market. [TASTE] {#ill-006}

## Brand Effect Model (recorded, out of engine scope)

Illustration may Engage in-market, Connect, Guide in-system, Convert, Deliver experience —
**never Prime the out-of-market** (sole exception: social media). Campaign-placement governance,
not a component-level rule.

## Findings

1. **Pie-emphasis exception is one-directional.** `data-visualisation-pie-charts.md` records:
   "never enlarge or pull out slices … exception, explicitly granted: infographic/illustration
   contexts may emphasise slices (see the illustration standards)". The illustration standards
   (main + style pages, searched 2026-07-02) contain **no pie or slice-emphasis content** — the
   grant exists only on the data-vis side. The exception stands (it's explicit at its source) but
   has no illustration-side detail to ingest; anyone "seeing the illustration standards" for it
   comes back empty. Logged as a source xref gap.
2. **#4587A7 provenance receipted.** The legacy illustration palette page
   (`foundations-and-identity/colour/illustration0.html`) lists **Blue 5 = #4587A7**
   (C60 M12 Y0 K33 · R69 G135 B167); Blue 4 (Base) = #63C2EF. This confirms the
   `_DARK-MODE-AUDIT` suspicion: dark `rag/information` + `focus/ring` alias a missing
   `color/blue/400` whose hex leaked in from the legacy illustration palette — an
   illustration-only colour (this page's own scope rule) doing indicator duty in the dark theme.
   Strengthens the REVISIT case for the dark rag/information re-basing. The legacy palette page
   itself is superseded by the supporting palette and is deliberately NOT ingested beyond this
   receipt.

## Cross-references

`colour-standards-2026.md` (supersession + supporting palette scope) ·
`data-visualisation-pie-charts.md` (the exception's source) · `_ICON-GAPS.md` /
icon-source rule (illustration ≠ icon) · `_DARK-MODE-AUDIT.md` (blue/400 gap).
