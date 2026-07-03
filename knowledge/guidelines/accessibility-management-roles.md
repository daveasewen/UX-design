# Accessibility for project / product / procurement managers — framework role pages (ingested)

*Sources: create.hsbc → Processes and tools → accessibility → digital-accessibility-framework →
`accessibility-for-project-managers.html` + `accessibility-for-product-managers.html` +
`accessibility-for-procurement-managers.html`, captured 2026-07-03 via Dave's authenticated
session (login-walled; ADR-0005 provenance applies). Combined per the dsp- precedent (three
thin pages, one governance layer). All BS 8878 lineage, all [PROCESS] — no UI rules — but
the product-managers page states the decision-receipt discipline at source (F2). This
completes ALL 9 role pages.*

## Project managers (rules)

- **The BS 8878 16-step process** — Research (1–6: purpose · audiences · needs ·
  platform/tech preferences · relationship · goals+tasks) → Decide (7–12: UX degree ·
  inclusive-vs-personalised · platforms · browser/OS/AT matrix · make-or-buy · web
  technologies) → Do (13–15: guideline-directed production · assurance through
  production · communicate decisions at launch) → Repeat (16: post-launch updates +
  user feedback). Process-based, territory-insensitive, applies everywhere. [PROCESS —
  upstream frame of the axf-010 scoping questionnaire; see F3 for the pipeline mapping]
  {#amr-001}
- **Four strategic workshops drive the process** — page details two: kick-off (~5h, as
  early as possible, steps 1–12 → first-draft Web Product Accessibility Policy) and
  implementation planning (~7h, steps 13–14 → **accessibility as a quality requirement
  ON EACH USER STORY, referencing the specific applicable guidelines** + separate
  accessibility-functionality stories + resource estimation + test-plan embedding).
  Workshops 3/4 not detailed at source. [PROCESS — per-story criteria referencing =
  criteria-contracts at backlog grain; source gap logged F4] {#amr-002}
- **PM estimating duties** — accessibility cost = dev overhead on ALL sprints +
  dedicated functionality sprints + planned testing + planned FIX TIME; plus flex
  handling when progress lags (scope/quality/budget/timing trade-offs). [PROCESS —
  fix-time-is-planned pairs with aqa-002] {#amr-003}

## Product managers (rules)

- **The product manager OWNS the product's accessibility** — defines the level to
  deliver, sets decision-making tone, ensures the PM drives BS 8878. [PROCESS]
  {#amr-004}
- **The decision discipline** — team members are EMPOWERED to decide, as long as they:
  recognise it as a decision · consider all options and implications · can justify it ·
  **note it in the Web Product Accessibility Policy** (ONE policy document across the
  product's whole lifecycle and every iteration project). Explicitly cost-benefit
  ("places accessibility back in the sphere of cost-benefits like all other
  decisions"), explicitly handles the "tail wagging the dog" case and WCAG-infeasible
  edges. [PROCESS — the decision-receipt discipline stated at source: recognise /
  consider / justify / RECORD = the register + desk-ruling method, institutionally
  blessed. First-order transformation-strand material — see F2] {#amr-005}
- **Decisions are monitored against accessibility risk thresholds** — the product
  manager reviews the policy's accumulating decisions against the required level and
  challenges quickly. [PROCESS — the promotion-queue review loop, at source] {#amr-006}
- **The Accessibility Statement contract** — launch REQUIRES one; it must: use simple
  language (readable by users with learning difficulties even if the rest of the site
  isn't) · explain how to customise/get AT help · **declare known limitations AND fix
  plans** · give contact mechanisms (pointing at WAI's feedback guidance) · optionally
  describe production approach without jargon · carry a last-updated date, reviewed
  each version. GMDA checks before publication. **Recommends AGAINST publishing
  compliance certificates/accreditations.** Generic HSBC template "available later in
  2014" — the vintage tell (F1). [PROCESS — the Statement is the PUBLIC face of the
  ship-with-logged-deficiencies discipline (aqa-013 pairing)] {#amr-007}

## Procurement managers (rules)

- **Procured = still bound** — accessibility requirements (compliance with this
  framework's checkpoints) go in the brief/ITT · shortlisted agencies/products are
  SCORED on accessibility alignment · no-compliant-option situations route to GMDA ·
  accessibility improvements are negotiated, costed and tested with the supplier ·
  resulting level communicated via the Accessibility Statement. [PROCESS — supplier
  scope pairs with axf-005; scoring-on-alignment is certified-component economics
  applied to procurement] {#amr-008}

## Findings

- **F1 — vintage layering confirmed**: "will become available later in 2014" survives
  in the live product-managers page — BS 8878-era (≈2014) text carried for a decade
  with WCAG 2.2 additions patched in 2024. Framework pages are LAYERED VINTAGES; the
  axf-007 annual review evidently touches sections, not pages. Capture dates and
  per-section vintage sniffing both matter (kin of va25's F1 refresh-contamination,
  inverse direction).
- **F2 — amr-005 is the strategy pull-quote of the whole role-page family**: the
  institution mandates recognise/consider/justify/record into one lifecycle policy
  document — i.e. decision receipts, owned by a named human, reviewed against risk
  thresholds (amr-006). This is the register + desk-rulings + _DS-IMPROVEMENTS method,
  described in the source's own governance. Pairs with aqa-013 (logged deficiencies)
  and gdea-003 (certified reuse) as the transformation strand's institutional spine.
- **F3 — BS 8878's 16 steps map onto the pipeline frame**: research→criteria (steps
  1–6 = scoping), strategic decisions (7–12 = charter/fixed-flex dials), guideline-
  directed production (13 = generation against canon), assurance through production
  (14 = gates + fitness tests), communicate decisions (15 = statements/receipts),
  repeat (16 = regression tier). Worth a note in the promenaut strategy pack — the
  discovery spine has a British-Standard ancestor.
- **F4 — source gaps**: PM page names 4 workshops, details 2; procurement page has no
  numbered checkpoints (5 duties). Logged, not chased.
- **F5 — ROLE PAGES COMPLETE**: all 9 ingested (avd · aca · aid · acd · aia · aqa ·
  amr×3). Remaining a11y queue: `Accessibility_Standards.html` + the three
  accessibility hub pages + channels pages.
