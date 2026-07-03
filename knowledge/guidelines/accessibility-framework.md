# Digital Accessibility Framework — standard, testing, checklists (ingested)

*Sources: create.hsbc → Processes and tools → accessibility →
`digital-accessibility-framework.html` + `testing-and-auditing.html` + `qa-checklists.html`,
captured 2026-07-03 via Dave's authenticated session (login-walled; ADR-0005 provenance
applies). Engine-era format. NOTE the site moved: the queue's old `/accessibility/...`
paths 404 (nav restructure, redirects incomplete) — live paths are under
`/processes-and-tools/accessibility/`. Supersedes nothing yet: legacy `accessibility.md`
(pre-engine) upgrade remains queued; this file carries the FRAMEWORK layer.*

## The standard (rules)

- **The HSBC digital accessibility standard is WCAG 2.2 AA** — desktop web: all framework
  standards; mobile web + apps: WCAG 2.2 AA enriched/mapped against BBC Mobile
  Accessibility Guidelines v1.0 and Funka Nu mobile guidelines, including some WCAG AAA.
  Process guidance draws on BS 8878:2010. [REVIEW — our gate baseline says "WCAG 2.1 AA
  (+2.5.8 from 2.2, +2.3.3 advisory)" (`_A11Y-AUDIT.md`); the source bar is 2.2 AA, so
  the gates need a 2.2 re-baseline (delta: the six 2.2 additions beyond 2.5.8) — Dave to
  rule scope/timing] {#axf-001}
- **Two-element standard** — (1) international legal compliance (the WCAG 2.2 bar above);
  (2) assured experience: the named disabled/older user groups can "effectively complete
  the product's core user journeys" with the default AT list. Acceptance is
  journey-completability, not checkpoint-passing alone. [ADVISORY — the source's own
  version of "gates green ≠ done"; pairs with the fitness-test discipline] {#axf-002}
- **Named user groups** — blind (screen readers) · vision-impaired (magnifiers) · low
  vision (font resizers) · deaf/hard-of-hearing · motor-impaired (voice activation;
  switch) · dyslexic + learning difficulties · older 75+. [RECORDED — persona anchor for
  the neuro-* family and Dave's dyslexia-informed comms preferences] {#axf-003}
- **Default AT/browser/OS matrix** — two most recent versions of Android/iOS/Windows/
  macOS; VoiceOver (iOS+macOS), TalkBack, JAWS, NVDA, Dragon NaturallySpeaking;
  **keyboard-only on desktop AND mobile**; browsers: Edge, Chrome (desktop+mobile),
  Firefox, Android default, Safari (IE internal-only). Per-project matrices are agreed
  early, starting from this list. [RECORDED — upstream anchor for decision B
  (native-keyboard AT); keyboard-only is in the default matrix] {#axf-004}
- **Global scope, suppliers included** — applies to all external-facing HSBC digital
  products worldwide; external suppliers "will also be expected to comply"; territory
  exceptions via Global Marketing Digital Approvals. Governance under FIM B.5.4.
  [RECORDED] {#axf-005}
- **Role-sliced guidance** — the framework splits into 9 audience pages: information
  architects · interaction designers · visual designers · client-side developers ·
  content authors · QA/CX testers · project managers · product managers · procurement
  managers. [RECORDED — the rule-bearing payload; all 9 discovered → queue] {#axf-006}
- **Annual review cycle** — HSBC Digital Design reviews the framework annually.
  [RECORDED — vintage discipline: capture dates matter] {#axf-007}

## Testing + auditing (rules)

- **QA owns accessibility testing; everyone monitors** — a11y defects are functionality
  defects; testers need enough understanding to write accurate defect reports.
  [RECORDED] {#axf-008}
- **AbilityNet is the named third-party test partner** — test specs come either through
  the Digital Design Accessibility team, or are agreed between AbilityNet and the
  product team and sent to the Accessibility team BEFORE testing starts. [PROCESS]
  {#axf-009}
- **The test-scoping question set** — product importance (red-carpet/pillar or not) ·
  type (app/responsive/desktop) · formats + platforms + browsers · AT list as a SUBSET
  of the framework matrix · production stage (design review / code review / pre-launch)
  · prior testing · scope + journey priorities · team's known-unsure areas · count of
  known challenge patterns (tabbed/multi-level/burger nav, complex transactional forms,
  carousels/sliders/maps, infographics) · page count · timing + confidence. [PROCESS —
  this is a criteria-contract intake questionnaire, human-shaped] {#axf-010}
- **Modularity reduces audit surface** — the scoping asks whether the site is "built
  from modular reusable library components (so components reused across site)… This
  affects how many pages with the same element need to be tested — one or two."
  [RECORDED — the source states the certified-component economics: reuse shrinks
  testing; pairs with gdea-003's reuse exemption] {#axf-011}
- **QA checklists exist as maintained artefacts** — four WCAG 2.2 checklists (browser ·
  Android hybrid · iOS hybrid · native app), PDF downloads for manual validation across
  the lifecycle, defined against the framework. [RECORDED — staff-only downloads;
  capture on demand → assets/] {#axf-012}

## Findings

- **F1 — the version gap is real and ours** (axf-001): the standard is WCAG 2.2 AA;
  our audit header says 2.1 AA + partial 2.2. Re-baseline is gate work (likely small —
  contrast math unchanged; the new 2.2 criteria are structural: focus-not-obscured,
  dragging alternatives, consistent help, redundant entry, accessible authentication,
  target size already adopted). Dave to rule scope/timing — carried on axf-001, this
  file's one REVIEW item.
- **F2 — the institution keeps arguing our case at source:** journey-completability over
  checkpoint-passing (axf-002) = fitness tests; modularity-shrinks-testing (axf-011) +
  GDEA's reuse exemption (gdea-003) = certified components; the scoping questionnaire
  (axf-010) = criteria contracts. Strategy material for the transformation strand.
- **F3 — discovered (→ queue):** the 9 role pages (rule-dense, especially visual
  designers / interaction designers / content authors / client-side developers) ·
  training page · 4 checklist PDFs · `platforms-and-channels/Accessibility_Standards.html`
  (found via the about-us hub).
- **F4 — site nav restructured:** old `/accessibility/…` URLs 404; update queue paths
  before capture (done for this tranche).
