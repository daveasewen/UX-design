# Accessibility for client-side developers — framework role page (ingested)

*Source: create.hsbc → Processes and tools → accessibility → digital-accessibility-framework →
`accessibility-for-client-side-developers.html`, captured 2026-07-03 via Dave's authenticated
session (login-walled; ADR-0005 provenance applies; code samples at source omitted from
capture — prose rules carried). Engine-era format. Checkpoint IDs at source: CD-1…CD-48.
The densest role page: heavy overlap with what the gates already enforce — those rules are
RECORDED with their enforcement receipts rather than re-opened. Duplicates xref'd per F4.*

## Framing (rule)

- **Semantics are the developer's responsibility**: "a button should be coded as a
  button and then styled… not coded as a graphic with a link"; technique choice must
  respect the product's browser/AT support matrix; non-Latin/RTL → consult GMDA.
  [RECORDED — the canon enacts this (native elements first); decision A/B kin]
  {#acd-001}

## Structure + semantic markup (rules)

- **CD-1 — meaning never by visual formatting alone** (SC 1.3.1 A): semantic markup
  (strong/em, lists, headings) over CSS-only styling. [RECORDED — enforced in spirit by
  requiredAria + semantic-markup review; composition keeps heading hierarchy (aca-001)]
  {#acd-002}
- **CD-2 — bypass mechanism on ALL pages** (SC 2.4.1 A): skip-to-content link; long
  pages add section shortcuts (may be visually hidden until focused). [ADVISORY —
  REAL GAP: composed `*.canon.html` screens carry NO skip link today (swept
  2026-07-03). Screen-gate candidate — RULED + WIRED 2026-07-03 (Dave): advisory check H; all 5 composed screens signal at wiring — real gap, fix at the composition touch] {#acd-003}
- **CD-3/4 — grouped controls read as ONE accessible component, and groups are proper**
  (SC 1.3.1 + 4.1.2 A): composite widgets (spinners etc.) must not decompose into
  meaningless fragments for AT; radio groups grouped so keyboard behaviour works.
  [ADVISORY — component-review axis; Selection-controls/Dropdown already enact]
  {#acd-004}
- **CD-5 — landmarks/containers describe page structure** (2.4.1-adjacent): ARIA
  landmarks assist speech-output navigation. [ADVISORY — composition-layer rule for
  assembled screens: main/nav/banner landmarks on composed screens] {#acd-005}
- **CD-6 — content order logical** (SC 1.3.2 A): duplicate of CA-2. [RECORDED — destiny
  carried on aca-002] {#acd-006}
- **CD-7/8 — page language declared; in-page language CHANGES declared** (SC 3.1.1 A +
  3.1.2 AA). [ADVISORY — composed screens all carry `<html lang>` today (swept
  2026-07-03); keep-it-true screen-gate candidate (cost-0); bilingual snippets would
  need `lang` on parts — pairs with the type26 bilingual mechanics. RULED + WIRED 2026-07-03: advisory check I (keep-true; 0 signals)] {#acd-007}
- **CD-9 — degrade gracefully without CSS** (recommendation): content/function survive
  styling loss; off-screen-text fallbacks for custom controls. [RECORDED] {#acd-008}

## Text sizing + personalisation (rules)

- **CD-10 — code text so it can resize: "code all text in ems, not pixels"**
  (SC 1.4.4 AA). [RULED 2026-07-03 — REAL DELTA: canon.css types EVERYTHING in px (checked
  2026-07-03: 20 font-size declarations, all px). Browser full-page zoom works with px;
  Firefox text-only resize does not. Dave's ruling: rem-for-ALL is the
  destination — queued as a STANDALONE canon task, explicitly NOT gated on the
  supercharge and not now (a distraction from the current spine). px stands
  documented until the rem pass: browser zoom covers 1.4.4 in practice; user-set
  default font size is the accepted, recorded interim gap] {#acd-009}
- **CD-11/12 — interface zoomable; consider text/colour personalisation settings**
  (SC 1.4.8 / 1.4.10): **never disable pinch-to-zoom**; style-switchers → GMDA consult
  first (same clause as aid-016). [ADVISORY — the pinch-zoom half is a cost-0 gate
  candidate: ban `user-scalable=no` / `maximum-scale=1` in viewport meta (0 signals
  today). RULED + WIRED 2026-07-03: advisory check J] {#acd-010}

## Non-text content (rules)

- **CD-13 — purpose-alt for every non-text element; NEVER the element type**
  (SC 1.1.1 A): action images describe the ACTION ("Play"); decorative = AT-ignorable;
  "alternatives MUST NOT include information about the type of object. Avoid 'Image
  of…', 'Link to…', 'Picture of…', 'Add button'." [RECORDED — destiny carried on
  avd-006. NOTE: the source states the role-suffix ban as MUST for standard controls —
  strengthens the case for promoting advisory check G once the Cards "Example link"
  signals are fixed] {#acd-011}
- **CD-14 — informational background images need a visible, programmatic alternative**
  (SC 1.1.1 A): CSS backgrounds can't carry alt. [RECORDED — canon carries no
  informational background images; binds hero/expressive work] {#acd-012}
- **CD-15 — decorative/hidden/inactive content hidden from AT** (SC 1.1.1 A):
  **content behind lightboxes/modals must be hidden from AT** or users think they can
  interact with it. [ADVISORY — Modal criteria: background inert/aria-hidden while
  open. Component-touch item for the Modals revisit (true modals already in
  `_COMPONENT-GAPS.md`)] {#acd-013}

## Assistive-technology plumbing (rules)

- **CD-16 — accessibility properties set on everything** (SC 4.1.2 A): role, name,
  value, state; platform defaults for standard elements, explicit for custom.
  [RECORDED — enforced per-snippet by `requiredAria` (snippet gate check 2)] {#acd-014}

## Touch events + gestures (rules)

- **CD-17 — gesture functionality also one-finger via visible controls** (SC 2.5.1 A):
  one-finger alternative for pinch-zoom etc. — destiny holder; ID-25 duplicates this.
  [ADVISORY — binds future gesture surfaces; canon has none today] {#acd-015}
- **CD-18 — activate on UP-event, not down** (SC 2.5.2 A): no-down-event / abort-undo /
  up-reversal / essential; drag-drop released outside target REVERTS. [ADVISORY —
  cost-0 gate candidate: no action handlers on mousedown/touchstart in canon JS
  (0 signals expected — canon drives on click); Reorder's drag semantics already
  conform. RULED + WIRED 2026-07-03: advisory check K (inline down-attrs always;
  down-listeners only when the body navigates/submits/clicks — modality + drag
  listeners exempt by pattern; 0 signals)] {#acd-016}

## Keyboard + focus (rules)

- **CD-19…22 — the keyboard quartet** (SC 2.1.1 / 2.1.2 / 2.4.3 / 2.4.7): active
  elements focusable (inactive NOT focusable) · no keyboard traps · logical tab order ·
  visible focus on everything actionable. [RECORDED — visible focus enforced (snippet
  gate check 5, :focus-visible); native-first keyboard = decision B; traps + announce
  order stay in the human/AT queue (V3)] {#acd-017}
- **CD-23 — actionable visually distinguishable from non-actionable** (SC 1.4.1 A):
  users must not resort to discovery. [RECORDED — links-underlined + button-affordance
  canon rules enact this; 1.4.1 audit passed 2026-06-20] {#acd-018}
- **CD-24/25 — no automatic focus/context change on focus or input** (SC 3.2.1 /
  3.2.2 A): no auto-submit, no auto-advance out of a maxed field; shifts only on user
  request. [ADVISORY — forms rule; cost-0 candidate: no submit/navigation inside
  onchange/oninput handlers. RULED + WIRED 2026-07-03: advisory check L (0 signals)] {#acd-019}

## Notifications of dynamic change (rules)

- **CD-26/28 — state changes + dynamic updates communicated programmatically AND
  visually** (SC 1.1.1 + 4.1.2 A): selected/added/deleted announced; stale AT view is
  the failure mode. [RECORDED — live regions enforced on Countdown-timer /
  Loading-indicator / Notifications; state pairs in requiredAria] {#acd-020}
- **CD-27 — speech-output users notified of layout changes**: new panels, editable
  switches, grid→list. [ADVISORY — composition rule for dynamic screens] {#acd-021}
- **CD-29 — avoid automatic page refreshes**: AT loses place. [RECORDED] {#acd-022}
- **CD-30 — added content: move focus to it OR announce it; place it AFTER its
  trigger** (4.1.2-adjacent): [ADVISORY — accordion/disclosure pattern already enacts
  (content follows trigger in DOM); binds composition] {#acd-023}

## Forms (rules)

- **CD-31/32 — explicit labels; instructions ASSOCIATED with their field; required
  notation INSIDE the label + aria-required** (SC 3.3.2 A): asterisk goes in the
  label, not beside it. [ADVISORY — Input-fields supercharge payload with aid-018;
  cost-0 candidate: required fields carry aria-required (exact attribute check).
  RULED + WIRED 2026-07-03: advisory check M (0 signals — canon declares no
  required fields yet)] {#acd-024}
- **CD-33 — adapt the virtual keyboard + autocomplete** (SC 1.3.5 AA): numeric keyboard
  for numeric fields; auto-complete/search suggestions reduce errors. [ADVISORY —
  cost-0 candidate: inputmode/autocomplete attributes on typed inputs — Input-fields
  supercharge scope. RULED + WIRED 2026-07-03: advisory check N — fires on canon
  email inputs (8 signals), evidence banked for the supercharge] {#acd-025}

## Feedback + status (rules)

- **CD-34/35/36 — feedback for every action; clear error messages; correction help**
  (SC 3.3.1 A / 3.3.3 AA): action feedback visible + programmatic ("add to favourites"
  → "remove from favourites"); errors described in text at form top + inline highlight;
  suggest corrections unless security forbids. [RECORDED — Notifications + Input-fields
  error patterns enact; copywriting copy-* family carries the microcopy] {#acd-026}
- **CD-37/39 — audible/vibration feedback CONSIDERED and switchable; standard OS
  alerts where available** (recommendations). [RECORDED — native-app scope mostly;
  kept for provenance] {#acd-027}
- **CD-38 — clear status information, programmatically determinable** (SC 4.1.3 AA):
  loading progress visible; role=status without stealing focus. [RECORDED —
  Loading-indicator + Countdown-timer enact (role=status live regions)] {#acd-028}

## User protections (rules)

- **CD-40 — transactions: check + review + correct BEFORE submission** (SC 3.3.4 AA):
  source states HSBC transactions are effectively irreversible → the checked/confirmed
  arms are mandatory. [RECORDED — the payments journey's review step is the enactment;
  journey-gate criterion for any transactional flow] {#acd-029}
- **CD-41 — time limits removable/adjustable/extendable, with warning** (SC 2.2.1 A):
  warn before expiry, ≥20s to extend, ×10 extensions. [ADVISORY — Countdown-timer
  criteria contract: the session-timeout pattern must ship the extend affordance]
  {#acd-030}

## Media + animation (rules)

- **CD-42/43 — no autoplay audio; moving content pausable** (SC 1.4.2 / 2.2.2 A):
  >3s audio needs pause/volume; >5s parallel animation needs pause/stop/hide; carousels
  are the modern offender — **consider default-PAUSED with a play button**. [RECORDED —
  no autoplay in canon (audited); reduced-motion enforced (2.3.3 gate); the
  default-paused carousel stance binds any future carousel] {#acd-031}

## Markup + components (rules)

- **CD-44 — well-formed markup** (old SC 4.1.1, **reclassified 2024**): [RECORDED —
  consistent with the 2.2 map (4.1.1 removed as obsolete); integrity lint covers
  structural sanity] {#acd-032}
- **CD-45 — platform standard controls whenever possible**: custom controls need extra
  AT measures. [RECORDED — the canon's native-first rule (decisions A/B); enforcement
  receipt = accordion/reorder native-button patterns] {#acd-033}
- **CD-46 — content on hover/focus: dismissible, hoverable, persistent** (SC 1.4.13 AA):
  Esc-dismiss without moving pointer; pointer can travel onto the popup; stays until
  dismissed/invalid. [ADVISORY — Tooltip criteria contract; check at Tooltip's ★ pass]
  {#acd-034}

## WCAG 2.2 additions (rules, introduced 2024)

- **CD-47 — focused element never FULLY obscured** (SC 2.4.11): sticky headers/footers,
  cookie notices, modals, virtual assistants must not entirely cover focus;
  scroll-padding is the named technique. [RECORDED — receipt + detail for the axf-001
  map's queued render axis: the bar is "not ENTIRELY hidden" (minimum), and the named
  offenders give the render check its test cases] {#acd-035}
- **CD-48 — dragging operations get a single-pointer alternative** (SC 2.5.7):
  buttons/menus as the alternative. [RECORDED — Reorder's move buttons already conform
  (2.2 map, audited 2026-06-20)] {#acd-036}

## Findings

- **F1 — the gates already hold most of this page**: acd-014 (requiredAria), acd-017
  (focus-visible), acd-020/028 (live regions), acd-031 (reduced-motion, no autoplay),
  acd-036 (Reorder). The source keeps receipting the built enforcement — strategy
  material, same class as axf-011/gdea-003.
- **F2 — two REVIEWs, RULED 2026-07-03**: acd-009 ems-vs-px (rem-for-all queued as a
  standalone task, px documented interim) and aid-009 target-44-default (fail <24 /
  advisory <44, enacted in _validate_a11y.py). Ruled together with the harvest below.
- **F3 — cost-0 gate-candidate harvest (advisory-first per ADR-0005 §5)**: skip-link
  on composed screens (acd-003) · `<html lang>` keep-true (acd-007) · pinch-zoom never
  disabled (acd-010) · no action-on-down-event (acd-016) · no onchange
  submit/navigation (acd-019) · aria-required on required fields (acd-024) ·
  inputmode/autocomplete (acd-025) · no paste-blocking (aid-020). Eight candidates,
  one sitting — RULED + WIRED 2026-07-03 as advisory checks H…O, all bite-tested.
- **F4 — duplicates carried once**: CD-6→aca-002 · CD-13→avd-006 (with the MUST
  strengthening noted for check G's promotion case) · CD-17 holds destiny for ID-25 ·
  CD-11/12's GMDA clause shared with aid-016.
- **F5 — component-touch payloads routed**: Modal background-inert (acd-013) → Modals
  gap entry · Tooltip 1.4.13 contract (acd-034) → Tooltip ★ · Countdown-timer extend
  affordance (acd-030) → its criteria · Input-fields (acd-024/025 + aid-018) →
  supercharge.
