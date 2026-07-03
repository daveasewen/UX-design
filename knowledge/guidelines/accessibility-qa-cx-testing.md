# Accessibility for QA and CX testers — framework role page (ingested)

*Source: create.hsbc → Processes and tools → accessibility → digital-accessibility-framework →
`accessibility-for-qa-and-cx-testers.html`, captured 2026-07-03 via Dave's authenticated
session (login-walled; ADR-0005 provenance applies). Engine-era format. No numbered
checkpoints — this is the METHOD page (BS 8878 lineage): test-plan staging, scope rules,
independence, and the launch-with-deficiencies process. Mostly [PROCESS], but it receipts
the engine's architecture more directly than any page yet (F1).*

## Framing (rule)

- **Journey experience over checkpoint conformance**: "customers buy the car based on a
  test drive, not its specification sheet" — authors self-check checkpoints; testers
  check BOTH checkpoint compliance AND that combined work yields journeys completable
  by the named user groups with the standard AT matrix. [RECORDED — the source's own
  gates-green-≠-done; pairs with axf-002 journey-completability] {#aqa-001}

## Test-plan rules

- **Accessibility testing at EVERY lifecycle stage, stage-appropriate methods**: unit ·
  integration · QA · CX-with-users · post-launch regression; planned at project START
  with fix-time reserved. [PROCESS — the staged-gate architecture stated at source;
  our build gates = the unit/integration tier, fitness tests = the CX tier] {#aqa-002}
- **Scope rule — standards always; CORE-PORTFOLIO products (global style guides, UI
  LIBRARIES) test against ALL guidelines and recommendations too.** [ADVISORY — bears
  directly on us: the canon IS a UI library, so the source holds library-grade work to
  the guideline+recommendation tier, not just standards. Receipt for treating
  GUIDELINE-tier rules as binding on canon components — see F2] {#aqa-003}
- **Defect reports enable cost-benefit prioritisation**: per-defect — quick
  understanding, severity × affected disabled audiences, fix, fix-cost; the
  Accessibility Issue Prioritisation Matrix is the named template (staff artefact).
  [PROCESS — kin of our severity + blast-radius reporting; template capture on demand]
  {#aqa-004}
- **Design-stage testing BEFORE code**: wireframes/visuals manually tested against the
  ID-*/VD-* checkpoints, deficiencies remedied pre-implementation. [PROCESS — the
  source's version of test-at-design-time; our render-based pre-code checks are the
  mechanisation] {#aqa-005}
- **Unit/integration testing incorporates the CD-* checkpoints**: keyboard tab/enter
  walks for structure + keyboard checks; named tools (WAVE toolbar, aDesigner, W3C
  validator, NVDA+Firefox for non-SR-users) — vintage list, see F3; don't test with AT
  you don't know how real users drive. [PROCESS — our static gates are the modern
  equivalent of this tier] {#aqa-006}
- **Content-stage testing against the CA-* checkpoints** post-build-pack. [PROCESS]
  {#aqa-007}

## Launch rules

- **Pre-launch UAT conformance testing is MANDATORY for all products** — against ALL
  framework checkpoints, by an expert in the framework + WCAG 2.2 **who has not worked
  on the product** (internal or external). [PROCESS — independence-of-verification
  stated at source; the fresh-eyes clause is the anti-self-certification rule]
  {#aqa-008}
- **Fail → fix, or JUSTIFY**: every checkpoint failure is fixed or carries a recorded
  justification (not reasonable at all / not before launch, with constraints named).
  [PROCESS — fix-or-justify = the named-risk-acceptance discipline (gdea kin)]
  {#aqa-009}
- **CX testing with disabled users — optional by size/budget, agreed with GMDA at
  project start**: three-option cost ladder (expert cognitive walkthrough → disabled
  reps INTEGRATED into general user-testing [named best value] → separate group
  testing); participant roster mirrors the axf-003 groups (SR user, magnifier user,
  font-resizer, voice-activation, switch, Deaf/HoH, dyslexic, ADHD/Aspergers, moderate
  learning difficulty, 75+); AT users join at LATER stages (coded interface needed),
  non-AT users test from paper-prototype stage. [PROCESS — roster destiny on axf-003;
  the staging insight (non-AT early, AT late) is the schedulable part] {#aqa-010}
- **Sourcing rules**: walkthrough experts + facilitators from GMDA preferred suppliers;
  internal disabled staff OK as participants IF representative and unfamiliar with the
  product. [PROCESS] {#aqa-011}
- **AT-difference testing — optional, agreed with HSBC Digital Design at start**:
  screen-reader × browser matrix consistency (the section-2 matrix = axf-004); lists
  updated annually (WebAIM SR survey is the named source). [PROCESS — destiny on
  axf-004] {#aqa-012}
- **Launching WITH deficiencies is a governed path**: MVP v1 may ship not-fully-
  accessible IF the gaps are (a) noted in the product's Accessibility Statement,
  (b) GMDA-approved, (c) carried with an action plan for post-launch fixes; new
  versions update the Statement (fixed AND newly introduced deficiencies). [PROCESS —
  the known-signature discipline stated at source: ship with LOGGED, owned exceptions,
  never silent ones — institutional receipt for the _DS-IMPROVEMENTS / allow-list
  pattern] {#aqa-013}
- **Post-launch content maintenance is where a11y rots**: content authors check their
  own additions; content-rich products get YEARLY automated audits (WAVE API /
  SiteImprove named). [PROCESS — regression tier; our gates run per-build, the
  source's yearly floor is for un-gated content pipelines] {#aqa-014}

## Findings

- **F1 — this page receipts the engine wholesale**: staged gates (aqa-002) ·
  independence of verification (aqa-008) · fix-or-justify (aqa-009) · ship-with-logged-
  exceptions (aqa-013) · regression tier (aqa-014). The institution's own method page
  describes what the pipeline mechanises. First-order strategy material for the
  transformation strand — pull quotes live here.
- **F2 — the scope rule elevates the canon's bar** (aqa-003): UI libraries test against
  guidelines AND recommendations, not just standards. Our destiny mapping already
  treats most guideline-tier rules as advisory checks; the source says for
  library-grade work they're in scope, full stop. Worth a line in the next desk batch
  discussion — philosophy confirmation, not a gate change.
- **F3 — tool vintage**: aDesigner (Eclipse), WAVE toolbar, snook contrast, W3C
  validator — a pre-CI toolchain. The gates are the modern equivalent of exactly this
  list (contrast maths, structure lint, keyboard walk pending V3). Useful contrast for
  the harness pitch.
- **F4 — duplicates carried once**: user-group roster → axf-003 · AT/browser matrix →
  axf-004 · fix-or-justify kin → gdea-* · journey-completability → axf-002.
