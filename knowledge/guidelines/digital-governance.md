# Digital governance — GDEA engagement + self-certification (ingested)

*Source: create.hsbc → Processes and tools → `Digital_Governance.html`, captured
2026-07-03 via Dave's authenticated session (login-walled; ADR-0005 provenance applies).
Engine-era format. Pure [PROCESS] destiny — but this is the regime every generated screen
ultimately ships through, so the criteria are strategy-bearing for Promenaut (the engine's
certificates should be evidence a GDEA review can consume).*

## GDEA approval criteria (rules)

- **All digital applications need GDEA approval** — internal AND external facing; Group
  Digital Experience & Accessibility governs consistency, accessibility and digital-
  channel risk. [PROCESS] {#gdea-001}
- **Approval triggers** — new website/app · significant change: design-UI change (incl.
  moving from a historic standard to the LATEST brand standards/toolkits — i.e. the
  refresh migration itself is governed) · new features/functionality/journeys/sections ·
  deploying journeys to other markets · navigation changes (tabs, structure, content) ·
  new tools (calculators, forms) · platform migration / major front-end upgrade.
  [PROCESS — note how many triggers are exactly the surfaces our engine composes]
  {#gdea-002}
- **BAU exemptions** — minor content/imagery/banner/video/copy changes · new page within
  an existing approved design+experience standard (unless it changes a journey —
  ambiguity resolved by contacting GDEA) · reuse of previously-approved assets/templates
  (landing pages, page templates, tools) · short-term online marketing campaigns.
  [PROCESS — "reuse of approved templates is exempt" is the certified-component value
  proposition at source] {#gdea-003}
- **Engagement, step 1: start governance** — online engagement form at project start →
  GDEA-ID issued, process overview, governance checklist template, pointers to standards
  on create.hsbc, which design team to engage, named accessibility lead. [PROCESS]
  {#gdea-004}
- **Step 2: design & experience review** — the relevant design team reviews designs
  AGAINST THE STANDARDS on create.hsbc, feeds back, approves amendments; an approved
  third-party accessibility auditor is booked; an Accessibility Manager is briefed; risk
  partners may join. [PROCESS] {#gdea-005}
- **Step 3: build review** — UAT/build goes back to the design team; all design feedback
  actioned before launch; third-party a11y audit report → remediate → **retest report**;
  anything outstanding needs GDEA endorsement + formal business risk acceptance.
  [PROCESS — audit → fix → RETEST is the loop; residual fails need explicit risk
  acceptance, the upstream mirror of our known-signature discipline] {#gdea-006}
- **Step 4: project approval** — complete the GDEA checklist (external) or approval
  submission (internal); evidence of design team + Accessibility Manager + other
  approvals (Analytics, Legal, Regulatory Compliance); Digital Governance Manager
  approves → go-live; local business release processes may add steps. [PROCESS]
  {#gdea-007}
- **Self-certification route** — for projects re-releasing an already-governed
  experience (e.g. additional country/region): engagement form → GDEA-ID → short online
  form (~10 min) with GDEA-ID of first release, representative screenshots + first-
  approval evidence, the first release's a11y audit report and/or a multi-language audit
  (required for languages not previously approved); WPB adds analytics (MCTAG ticket)
  and, for customer-facing, Local Legal + RC + Resilience/Cyber sign-offs. Outcome in ~3
  business days. [PROCESS] {#gdea-008}

## Findings

- **F1 — the engine's certificates map onto GDEA evidence.** Steps 2–4 consume exactly
  what the gate stack produces: standards-alignment evidence (design review), audit +
  retest artefacts (a11y), and checklists. A composed screen that ships with its
  criteria-contract + gate receipts + rendered state-contrast audit arrives at
  governance pre-evidenced. Strategy material for `digital-experience-transformation/`
  and the Promenaut pitch (gdea-003: certified reuse is EXEMPT from re-approval — the
  strongest institutional argument for the certified-component model).
- **F2 — third-party auditor + retest (gdea-006)** is the human-shaped version of the
  render-based sweep: the system already believes in "re-run the check after the fix";
  residual defects need named risk acceptance — kin to ds-002's known-signature rule.
- **F3 — GDEA-ID appears across processes** (naming stage 6 requires it too) — it's the
  join key between naming, governance and accessibility processes.
