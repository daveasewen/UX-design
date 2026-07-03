# Design-system processes — standards, toolkits, component libraries (ingested)

*Sources: create.hsbc → Processes and tools → `Design-Standards.html` + `Toolkits.html` +
`Component-Libraries.html`, captured 2026-07-03 via Dave's authenticated session
(login-walled; ADR-0005 provenance applies). Engine-era format. Three sibling meta-pages
describing the design system's OWN operating model — standards → toolkits → component
libraries. Mostly process/record destiny: this is the regime our engine mirrors and must
slot into, not visual rules.*

## The three-layer model (rules)

- **Standards are the source of reference** — "primary source for our experience insights
  and design language"; used by product owners, designers, developers, copywriters,
  governance and testing teams for guidance, governance, resource and onboarding.
  [RECORDED — the knowledge layer's upstream mirror] {#dsp-001}
- **Standards have a documented anatomy** — "definition, usage, types, structure…" per
  standard, with a defined format and display. Anatomy page discovered → Tier 2 queue.
  [RECORDED] {#dsp-002}
- **Standards are created by the requesting team via New Pattern Request / Proposal**,
  with research, Design Thinking and user testing; the Central Guild guides and may
  undertake work itself; the same process applies regardless of who builds. [PROCESS]
  {#dsp-003}
- **The Central Chapter (Guild) maintains standards**; extensions follow the same process
  as new standards; "original research and findings are always retained for reference."
  [PROCESS — provenance-retention is policy at source] {#dsp-004}
- **Toolkits are the platform-specific manifestation of foundations + global standards**,
  "distilled into design-ready assets"; "all assets are rigorously tested and validated
  before their inclusion." [RECORDED — validation-before-inclusion = the promotion gate
  at source] {#dsp-005}
- **Toolkits set the benchmark for governance review** — "governance and project teams
  rely on the Design Toolkit to review and align all new design work against." [RECORDED]
  {#dsp-006}
- **Toolkit content spec** — foundational assets needed on every screen (colour palettes,
  type scales, icons) + frequently-used elements and patterns (buttons, text inputs,
  dropdowns, tabs). Anatomy + process subpages discovered → Tier 2 queue. [RECORDED]
  {#dsp-007}
- **Toolkits are created by a cross-bank working group of SMEs; each business line
  maintains its own platform-specific toolkits**; the working group guards consistency.
  [PROCESS] {#dsp-008}
- **Component libraries are the development equivalent of toolkits** — per channel
  (web browser, iOS/Android app), possibly duplicated per frontend framework (React,
  Angular named); future channels (ATM) get equivalents. [RECORDED — Sutherland's
  upstream category] {#dsp-009}
- **Certification chain** — every component is "certified against the behaviours and
  specifications within the Design Toolkits and to the HSBC Accessibility framework";
  recertification and contribution models keep alignment over time. [RECORDED — the
  system's own gate stack; our engine's certificates are this, mechanised] {#dsp-010}
- **Design tokens bind the chain** — "developed components utilise the Design Tokens
  ensuring that brand design decisions are applied accurately in to the core elements."
  [RECORDED — token-fidelity as policy at source; our snippet gate check 1 enforces the
  same contract] {#dsp-011}
- **Technology teams own component libraries** (dedicated or distributed contribution),
  working with Design Guild Chapters, "using version control." [PROCESS] {#dsp-012}
- **Claimed benefits of the chain** (design-to-development alignment · speed via off-the-
  shelf components · fewer defects and reviews · central guideline/brand updates) — the
  business case create.hsbc itself makes for what our engine mechanises. [RECORDED —
  strategy material for the transformation strand] {#dsp-013}

## Findings

- **F1 — the three-layer model is our architecture, named by the source.** standards →
  toolkits → component libraries maps 1:1 onto knowledge/ → canon (snippets/gallery) →
  Sutherland bindings. "Certified against the toolkit + accessibility framework" is the
  gate stack; "rigorously tested and validated before inclusion" is promotion; "visual
  source of truth" is the canon claim. The engine doesn't fight this regime — it
  mechanises it. Strategy material for `digital-experience-transformation/`.
- **F2 — provenance retention is upstream policy** (dsp-004), which retroactively blesses
  the register's receipts-first discipline.
- **F3 — discovered subpages (→ Tier 2 queue):** Design Standards anatomy · Design
  Standards process · Design Toolkit anatomy · Design Toolkit process.
