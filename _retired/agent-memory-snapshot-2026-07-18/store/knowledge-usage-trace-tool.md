---
name: knowledge-usage-trace-tool
description: "Reusable tool (Dave: 'great tool, reuse'): retrieved-vs-invented + rule-adherence trace over generated artifacts, rendered as a Swiss interactive dossier with a live knowledge-graph viz"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7b86f842-66c3-4882-b0d1-4f5299d1a517
---

**STOOD UP 2026-07-07 (§9 session). Dave: "this is a great tool, note that we should reuse."**

Two scripts in `knowledge/`:
- `_trace_knowledge_usage.py` — measurement only. Reconstructs, from any generated HTML (no
  self-report needed), what was RETRIEVED from the KB vs INVENTED freehand. Reuses
  `_validate_icons.py`'s byte-match + resolves `var(--x)` against canon.css's defined vars +
  `.cn-*` set. Writes `_KNOWLEDGE-USAGE-TRACE.md`. Posture per screen: PURE-RETRIEVAL / HYBRID /
  INVENTED. Colour is cardinal → any live hex = cardinal violation = headline invention signal.
- `_build_trace_dossier.py` — presentation. Entity-level (NOT a score): every component, token,
  colour, icon PLUS a **rule-adherence layer** (WCAG SCs + create.hsbc principles probed from the
  artifact: focus-visible, aria/role, alt, prefers-reduced-motion, landmarks, square-corners,
  no-ALL-CAPS, canon-linked) with verdict honoured/violated/not-detected. Also builds the DS
  knowledge graph from `_XREF-INDEX.json`. Writes `_KNOWLEDGE-USAGE-ENTITIES.json` +
  `_KNOWLEDGE-USAGE-TRACE.html`. Run: `python3 _build_trace_dossier.py [LABEL=path ...]`.

The HTML dossier (Swiss skill + `_REVIEW-DOSSIER-charter` idiom): sticky nav + progress, **left
rail scroll-spy**, hand-rolled **canvas force-directed knowledge graph** (no CDN — robust offline;
views: Structure / Blast-radius / Retrieval-overlay), flat stacked-bar provenance charts per
screen, layout section (the KB governs the *measure* — 12-col grid/breakpoints/spacing tokens —
but has **no page-template layer**; composition always inferred; shows each lineage's actual
grid-template-columns), and an **entity explorer**: filter by lineage/type/verdict, **accordion**
rows (click name → read entity detail in-tool), mark targets + notes, export markdown worklist,
localStorage-persisted.

**Verification pattern (no browser in sandbox):** `node --check` + a stubbed-DOM node harness
(fake document/canvas/rAF) runs init + one sim frame to catch runtime errors. Playwright chromium
download is BLOCKED in-session — can't pixel-render; present live HTML for Dave to view
([[review-preview-html]]).

**Enhancements 2026-07-07 (Dave's asks, all shipped):** (1) left-rail scroll-spy side nav;
(2) sticky table header (offset computed from filter-bar height); (3) **rule-adherence layer** —
WCAG SCs + create.hsbc principles probed from the artifact (focus-visible, aria/role, alt,
prefers-reduced-motion, landmarks, square-corners, no-ALL-CAPS, canon-linked) → honoured/violated/
not-detected, answering "the create docs & A11y ARE in the KG but primitive-matching couldn't see
them"; (4) **accordion full-text reading** — click an entity to read in-tool: a11y→WCAG name+desc,
principle→embedded guideline doc (23 referenced create.hsbc docs + 31 WCAG descs + 38 component
records inlined; ~349KB self-contained; mini md→html renderer). Verified via node stub harness
(no browser in sandbox — playwright download blocked). Rule finding: governed screens honour 5-7/
violate 0-2; diagnostic honours 1/violates 6 → freer layout & rule-honouring pull OPPOSITE.
**Named next probe:** composition-tier probe (is any retrieved unit above organism? → [[library-composition-tier-gap]]).

**Reuse targets:** any generation run (governed vs unconstrained, model spreads, future lineages)
— point it at new dirs. Natural home = the harness "checks" pillar. Extends toward the
whole-corpus graph ([[ds-knowledge-graph-revisit]]): the rule layer is the first surfacing of
guidelines/WCAG *usage*, not just primitives.

Related: [[register-inference-ramp]] (the §9 question it serves), [[pipeline-mental-model]]
(gates/checks), [[icon-source-rule]] (byte-match origin).