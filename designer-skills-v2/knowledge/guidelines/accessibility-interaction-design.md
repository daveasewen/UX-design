# Accessibility for interaction designers — framework role page (ingested)

*Source: create.hsbc → Processes and tools → accessibility → digital-accessibility-framework →
`accessibility-for-interaction-designers.html`, captured 2026-07-03 via Dave's authenticated
session (login-walled; ADR-0005 provenance applies). Engine-era format. Checkpoint IDs at
source: ID-1…ID-28 (ID-6/7/24 do not exist at source; ID-13/14 are summary-only — see F3).
Tiering at source: STANDARD (must) · GUIDELINE (should) · RECOMMENDATION (consider).
Duplicates xref'd per the F4 rule — destiny carried once.*

## Navigation + structure (rules)

- **ID-3 — pages findable via BOTH search and structured navigation** (SC 2.4.5 AA +
  3.2.3 AA): more than one way to locate a page, except mid-process steps. [ADVISORY —
  journey-level → screen/journey criteria contracts; pairs with the 3.2.6
  consistent-help route on the axf-001 map] {#aid-001}
- **ID-4/5 — navigation simple, consistent within site/app, recognisably similar
  ACROSS a product's site and app versions** (SC 3.2.3 AA): mega-menus fail on mobile;
  menu may render differently per breakpoint but wording stays recognisably similar.
  [ADVISORY — composition/journey rule; feeds the Navigations organism review (V2)]
  {#aid-002}
- **ID-8 — content order must be logical** (SC 1.3.2 A): duplicate of CA-2.
  [RECORDED — destiny carried on aca-002] {#aid-003}
- **ID-9 — group elements that belong together (proximity)**: labels close to controls;
  form errors close to their fields; **too much whitespace confuses** (magnifier users
  see a small viewport); responsive reflow must keep related content directly AFTER the
  section it relates to, not dumped at page bottom. [ADVISORY — composition-layer
  proximity rule; COMPLEMENTS the neuro-042 whitespace floor (≥20px section whitespace
  ≠ unlimited whitespace — both bind)] {#aid-004}
- **ID-10 — instructions where necessary, and only where necessary** (SC 3.3.2 AA):
  on-screen text or icon+text (icon needs contrast — VD-2 family; icon-015 already
  blocking at 4.5:1); extraneous audio output disorients. [ADVISORY — microcopy/forms
  rule; joins the copywriting vocabulary] {#aid-005}
- **ID-11/12 — buttons/links in clear rows, consistently placed**: same function → same
  screen position, muscle memory; clear orientation must survive zoom/resize.
  [ADVISORY — composition rule; kin of avd-005 consistent identification] {#aid-006}
- **ID-13/14 — mobile button-placement guidance**: named in the source summary but NO
  detail sections exist in the page body. [RECORDED — source gap; see F3] {#aid-007}

## Touch targets + gestures (rules)

- **ID-15 — actionable elements large enough to tap** (SC 2.5.5 AAA basis): >9.6mm /
  44×44 CSS px with equivalent/inline/UA/essential exceptions; **≥1px inactive space
  around each actionable element**; A-Z-listing letters get a linked CONTAINER, not a
  linked glyph. [RECORDED — superseded as requirement by ID-26's formal 2.2 framing
  (aid-009); the 1px-gap + container-link details remain live guidance] {#aid-008}
- **ID-26 [introduced 2024] — target size, the formal 2.2 rule: HSBC DEFAULT 44×44,
  minimum exception 24×24** (SC 2.5.8 + 2.5.5): 24 only with the spacing/equivalent/
  inline/UA/essential outs; "HSBC already has formal design guidance… 44×44 is therefore
  considered the default requirement." [RULED 2026-07-03 (Dave): ENACTED — <24 now BLOCKING in _validate_a11y.py
  (EITHER-dimension semantics per the SC), 24–43 signals advisory against the 44
  default; promotion of the 44 tier waits on modelling the exception outs. Sole
  floor offender (Selection-controls chip dismiss, 18×18) fixed via the Tooltip
  hit-area pattern. Bite-tested (test_gates target24)] {#aid-009}
- **ID-16 — swipe areas clearly indicated** (SC 4.1.2 A): visual affordance (arrow etc.)
  + alt + audible cue on load; swipe content is routinely missed. [ADVISORY — binds any
  future carousel/swipe pattern; no swipe surface in canon today] {#aid-010}
- **ID-25 — gesture functionality also available one-finger via visible controls**
  (SC 2.5.1 A): duplicate of CD-17. [RECORDED — destiny carried on acd-014] {#aid-011}

## Layout, scrolling + text (rules)

- **ID-17 — minimise scrolling**: fewer objects, accordion/fold-out concealment (with
  obvious affordance), minimal header depth. [ADVISORY — register rule; kin of the
  neuro-042 calm ceilings — same sober-layout family] {#aid-012}
- **ID-18 — layout must let users PREDICT where things are**: consistent, logical
  placement + orientation aids (back/next/previous). [ADVISORY — composition/journey]
  {#aid-013}
- **ID-19 — nothing breaks at 200% text resize** (SC 1.4.4 AA + 1.4.10 reflow): reflow
  at 320px-wide / 256px-tall equivalents; named check = text in bounding boxes (nav
  items) spilling or truncating. [ADVISORY — already queued as V4 (zoom/reflow) in
  `_VISUAL-CHECK-QUEUE.md`; render-based check candidate — text-resize is NOT the same
  axis as viewport-responsive] {#aid-014}
- **ID-20 — line length ≤70 characters HARD, 55–60 target** (SC 1.4.8 basis): adapted
  to screen width; no sideways scroll to read a line. [ADVISORY — cost-0-adjacent
  candidate (max-width in ch on text blocks is statically checkable); distinct from
  neuro's ≤240 chars/SENTENCE — this is chars/LINE] {#aid-015}
- **ID-21 — consider text-size personalisation settings** (SC 1.4.8 / 1.4.12): browsers
  don't always provide it. **Style-switchers: consult Global Marketing Digital Approvals
  BEFORE building any** — HSBC is standardising a strategic solution. [PROCESS — the
  GMDA consult is the operative rule] {#aid-016}

## Forms (rules)

- **ID-22 — minimise text input**: lists-of-choices over typing; autocomplete.
  [ADVISORY — forms/journey rule; pairs with acd-024's inputmode/autocomplete]
  {#aid-017}
- **ID-23 — label placement contract**: portrait → label ABOVE the field; radio/checkbox
  → label RIGHT of control **with a group heading ABOVE the group**; landscape → label
  LEFT of field; **placeholder is NOT a label** (named at source: insufficient default
  contrast). [ADVISORY — Input-fields supercharge payload; the placeholder half is the
  source receipt for advisory check B (placeholder-as-label)] {#aid-018}

## WCAG 2.2 additions (rules, introduced 2024)

- **ID-27 — help mechanisms easy to locate, consistent order across pages** (SC 3.2.6):
  contact link on every page is good practice; not every help option must be everywhere.
  [RECORDED — receipt for the axf-001 map's 3.2.6 route → journey criteria contracts]
  {#aid-019}
- **ID-28 — authentication flexible, no cognitive-function-test-only step** (SC 3.3.8):
  offer in-app notification/biometric/OTP alternatives; **mechanisms like pasting from
  password managers must work**; applies to existing-user auth only; legal/regulatory
  exemptions possible. [RECORDED — receipt for the axf-001 map's 3.3.8 route. The
  paste-must-work clause is a cost-0 gate candidate: no paste-blocking on inputs — next
  desk batch] {#aid-020}

## Mobile-first (rules)

- **ID-1/2 — works in both orientations (SC 1.3.4 AA); full↔mobile version switch links
  if two versions exist**: mobile-first named as the good strategy. [RECORDED —
  orientation is a screen-level render concern; version-switching predates responsive
  canon, kept for provenance] {#aid-021}

## Findings

- **F1 — the 2.2 additions section receipts this morning's axf-001 map**: ID-27 (3.2.6)
  and ID-28 (3.3.8) arrive exactly on the routes ruled (journey criteria contracts), and
  ID-26 adds the NUMERIC the map lacked: **44 default / 24 minimum-exception** →
  aid-009 — RULED 2026-07-03, enacted as fail<24 / advisory<44.
- **F2 — Input-fields supercharge payload keeps growing**: aid-018's label-placement
  contract (portrait-above, radio-right + group-heading-above, landscape-left,
  placeholder≠label) joins the deferred Input-fields rework scope.
- **F3 — source gaps**: ID-6/7/24 don't exist; ID-13/14 appear in the summary but have
  no body sections (checked in-page, not an extraction loss). Logged, not chased.
- **F4 — duplicates carried once**: ID-8→aca-002 · ID-25→acd-014 · ID-23's placeholder
  clause → advisory check B receipt.
