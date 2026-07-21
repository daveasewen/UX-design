# Common Toolkit — Notifications family (Figma-sourced distillation)

*Provenance: Figma file `mI8hvIkV98nquoqWzKh5Kn` "HSBC Common Toolkit (MCP)",
Notifications page `45002:355009`, captured 2026-07-03 via Figma MCP (desktop
bridge text extraction + set census). Surfaces: guide components `00 Global
notification guide` 1688:84478 · `00 Contextual notification guide` 1686:83216 ·
`00 Inline notification guide` 1679:86681 · `00 Snackbar notification guide`
1683:83228, plus FOUR "Standard" frames carrying REAL create.hsbc standard text
(not lorem shells): Banners (mobile app) 45022:41410 · Notifications (browser)
45024:50309 · Snackbars (mobile app) 45011:44140 · Snackbars (browser)
45011:44174 — the two snackbar standards sit NESTED inside the Snackbar section
rather than at page level. Component sets censused: global 208:9480 · Inline
2301:63517 · contextual 208:10369 · snackbar 1660:82018 · form multi-link
211:6706. Guide vintage: "Version 0.0.0 | May 2023"; sets last touched 2026-06 —
layered vintages (td-002 kin). "Versions and states" frames noted per section but
not deep-captured (canon's state model already reconciled at the 06-24 rebuild).
NEW METHOD GOTCHA: text nodes containing U+2028 (line separator) kill the bridge
transport (ERR_HTTP2_PROTOCOL_ERROR) — hex-escape non-ASCII on extraction.
Second `ctk*` file of the toolkit tranche-1 pass; canon meta
(notifications.meta.json) was rebuilt from THIS node set 2026-06-24, so structure
and tokens already reconcile 1:1 — this pass's value is the RULES layer:
stacking, placement, timing, and copy contracts canon didn't carry.*

## Taxonomy and usage

- **The toolkit's four web taxa — global / inline / contextual / snackbar — with
  the app kin named "Banners".** The guides route to DIFFERENT create.hsbc
  standards: global → "banner standard", snackbar → "snackbar standard",
  contextual + inline → "notification standard". [RECORDED — Q1 ruling receipt
  (4-way split adopted 2026-07-03); canon's `type` prop already models the four
  placements; the create.hsbc standard names matter for the channels-batch
  capture] {#ctkn-001}
- **Notifications are NOT alerts**: notifications are static (page load or user
  action); alerts are dynamic, real-time events at system or network level. The
  library's `Alert` set is not a message at all — it is the notification BELL
  trigger (Size 18/24/36px × Active × Badge, node 65696:468427) with companion
  `Add Alert` (65696:468482). [RECORDED — vocabulary boundary; Alert/Add Alert =
  canon-lacks entries, queue with the survey inventory correction] {#ctkn-002}
- **Notifications should not be used for marketing purposes** (eg drawing
  attention to an offer). [ADVISORY — content-policy lint candidate at
  composition time] {#ctkn-003}
- **Snackbars are non-essential "nice to know" communications**: timely, polite,
  no input required, disappear automatically. [ADVISORY — placement-choice
  heuristic; pairs with canon's antiPattern "no Snackbar for errors"] {#ctkn-004}
- **There is no error snackbar anywhere in the toolkit**: the set has 3 variants
  (warning/success/information), the snackbar guide's screen-reader list omits
  "Error", and the app standard's types are warning/success/neutral. [IN FORCE —
  canon already omits error from snackbar; three independent receipts] {#ctkn-005}

## Placement and stacking

- **Global notifications display ABOVE the masthead**, flagging globally
  applicable issues affecting the whole site. [ADVISORY — blocking candidate —
  composition-layer placement contract; canon meta says "page-level top" but not
  above-masthead] {#ctkn-006}
- **Contextual notifications appear at the top of the page content, BELOW the
  page title, triggered by user actions** (eg a form completed incorrectly).
  [ADVISORY — blocking candidate — composition-layer placement contract]
  {#ctkn-007}
- **Severity stacking order — most severe first: error → warning → success →
  information.** Stated three ways: the global guide ("most severe sits on top"),
  the app banner standard ("errors first, warning second, success third and
  information last"), the browser snackbar standard ("most severe first").
  [ADVISORY — blocking-capable ordering check at composition time] {#ctkn-008}
- **Stack spacing numerics**: global↔global 1px between banners; global↔
  contextual 8px; snackbars 8px from the header and 8px between snackbars (app).
  [ADVISORY — blocking-capable numerics — render-axis check candidate] {#ctkn-009}
- **Multiples of the SAME type share one container; different types stack in
  SEPARATE containers.** Form errors: one container, with anchor links per error.
  [ADVISORY — composition contract; the anchor-link clause xrefs ctkl-012 (anchor
  links) + ctkn-020] {#ctkn-010}
- **Snackbar placement: resting position below the main navigation; elevated
  above page-level content INCLUDING modals and navigation; centre-aligned and
  no wider than six columns on large screens (avoids a long gap between message
  and close button); full content width (twelve columns) on small screens.**
  Large-screen width/alignment "depends on the snackbar notification requirements
  for your programme". [ADVISORY — blocking-capable layout numerics; the
  programme deferral is a source gap, ctkl-021 kin] {#ctkn-011}

## Structure contracts

- **Web notification anatomy**: severity icon · title summarising in 3–5 words
  using Medium weight (eg "Application submitted" / "Payment failed") ·
  description of 1–2 concise sentences · optional link, self-contained and
  descriptive · optional close icon ONLY when the notification is non-critical or
  has no associated action · container (NOT used for inline). [ADVISORY —
  blocking candidates: title word-count, close-icon policy, no-container-on-inline;
  canon builds to this anatomy already] {#ctkn-012}
- **App banner anatomy**: optional title of THREE words or fewer · message up to
  two sentences · maximum of two actions, primary first, undecorated buttons ·
  container height dynamic on content. Banners do not disappear automatically and
  CANNOT be closed — they resolve by user action or back-end updates. [RECORDED —
  app platform (Q2 ruling); kept as comparative receipts: note the app/web close
  policy split] {#ctkn-013}
- **Snackbar anatomy**: type icon · message · close button · container ·
  elevation (shadow around the container). [IN FORCE — canon matches 1:1
  including elevation/functional (DROP_SHADOW blur 16)] {#ctkn-014}

## Behaviour and motion

- **Notifications are static**: they appear on page load or in response to a user
  action, and stay until resolved or dismissed (where dismissal is allowed — see
  ctkn-012's close-icon policy). [ADVISORY — behaviour contract] {#ctkn-015}
- **Snackbar timing and motion**: appears with motion + opacity; rests 4–10
  seconds, duration set by reading length; on timeout it FADES OUT with no
  motion; on manual dismiss it disappears INSTANTLY. [ADVISORY —
  blocking-capable numerics (4–10s window); receipts canon's "persist long enough
  to read" a11y rule with real numbers; motion spec belongs to the motion canon at
  the ★ pass] {#ctkn-016}
- **App snackbars can be swiped up to dismiss.** [RECORDED — app platform;
  aid-010 (ID-16 swipe rules) kin — binds if an app project lands] {#ctkn-017}

## Copy contracts (the four RAG registers)

- **System errors**: active voice ("Payments cannot be processed by HSBC" →
  "We can't process payments at the moment"); plain English, no error codes;
  "We're sorry" at the START of the description ONLY when the fault is HSBC's and
  the user's experience is impacted. [ADVISORY — agrees with copy-035 (error-code
  placement, apology scope) + tov-028 (sorry once, only our faults); the toolkit
  adds the before/after example pair] {#ctkn-018}
- **User errors: never write an error message without a clear instruction to fix
  it; instruction-first copy; no "Please…" before each error instruction; no
  "We're sorry" for user-caused errors.** 📌 RULED (Dave, 2026-07-03): 'Please'
  banned per-instruction, allowed ONLY in the exact standard form-error title
  string (ctkn-020) — the politeness lint flags any other 'Please' in error
  copy; copy-035's optional-please is narrowed accordingly for error contexts.
  [REVIEW — ruled; tension with copy-035's "optional 'please' opener"
  (create.hsbc copywriting standard, testing receipt) resolved as above]
  {#ctkn-019}
- **Form errors**: standard title copy "Please correct the following errors"
  (exact string); instructions begin "Enter…" + what to do, or "The [field name]
  field can't be left blank"; reference the field label (2–3 words) for
  accessibility; the message link is an ANCHOR LINK to the field; individual
  messages replicated below each field. [ADVISORY — blocking candidates: the
  exact title string + below-field replication are testable; xrefs forms
  validation + ctkl-012 anchor links + aca-004 descriptive links] {#ctkn-020}
- **Warnings**: never use "Warning" as the heading; state the issue AND its
  effect on the user, in "you" terms ("You won't be able to access your accounts
  between…"); human and conversational — dial up urgency, not fear. [ADVISORY —
  agrees with copy-036's issue+effect rule; the no-"Warning"-heading ban is exact
  and lintable] {#ctkn-021}
- **Success messages**: positive signifier terms ("successfully", "completed",
  "finished") — users scan for them; active voice ("We've added…" not "…has been
  added"); success notifications occur ONLY at page level (browser standard).
  [ADVISORY — signifier-term list is a cost-0 lint candidate; the page-level-only
  clause is a placement contract] {#ctkn-022}

## Colour and accessibility receipts

- **Warning = yellow + warning icon; success = Jade; global warning notifications
  ALWAYS black text (#333333) on the yellow container (#FFBB33)** "to make the
  colour contrast of the text accessible". [IN FORCE — receipts canon's exact
  tokens (rag/warning #ffbb33 + rag/text/on-light #333) and the meta's "warning
  yellow uses dark text" rule; the toolkit names the pair at HEX level]
  {#ctkn-023}
- **Screen readers announce the severity icon: "Error" / "Warning" / "Success" /
  "Information"** — icons that aid understanding must have an announcement
  associated. The snackbar guide lists only Warning/Success/Information
  (consistent with ctkn-005). [IN FORCE — canon's announce rule (4.1.3, CD-38)
  now has the exact announcement strings] {#ctkn-024}
- **Target area minimum 44×44px, with named coverage: on global notifications the
  target covers THE ACTION BUTTONS; on snackbars it covers THE ENTIRE LIST ITEM
  BUT NOT THE DIVIDERS.** [ADVISORY — aid-009 receipt #3 at component level
  (after ID-26, axs-003, ctkl-016); the coverage clauses are NEW hit-area
  contracts — Tooltip-pattern kin, testable at render] {#ctkn-025}
- **Guides prescribe default NATIVE focus states.** Canon exceeds with the custom
  ring + VD-9 numerics. [RECORDED — intentional divergence, keep and record;
  ctkl-019/F5 kin] {#ctkn-026}
- **The a11y quartet, verbatim on all four guides**: 400% text size must not
  break · never disable pinch-and-zoom · visible focus outline when tabbing ·
  adhere to the HSBC Accessibility Framework + Brand Design Team review before
  release. [IN FORCE — same receipts as ctkl-023 (acd-005, acd-010/check J,
  acd-017, gai-* checkpoint); the quartet's repetition is the toolkit's
  per-component gate ritual] {#ctkn-027}

## Token census (confirmation, not discovery)

- **Global + inline ride SOLID RAG fills** (rag/error #a8000b · warning #ffbb33 ·
  success #00847f · information #305a85) with reverse text/icon; **contextual +
  snackbar ride the RAG TINTS** (error-tint #f9f2f3 · warning-tint #fff8ea ·
  success-tint #e5f2f2 · information-tint #ebeff4) with solid accents; snackbar
  adds elevation/functional; contextual + form multi-link still carry the two
  `rag/icon (depricate)` tokens. **No On Light/On Dark pairing exists for this
  family** — the toolkit has no dark-mode story for notifications. [IN FORCE —
  census confirms canon meta's tokenValidation (2026-06-18) exactly; the
  deprecate leak is already receipted with clean rebinds; canon EXCEEDS on dark
  (interim dark treatment stands, see dark-rag token notes)] {#ctkn-028}

## Findings

- **F1 — the rules layer is the new value.** Canon meta was rebuilt from this
  exact node set (2026-06-24) so structure, variants, and tokens reconcile 1:1
  with zero deltas. What canon lacked — and now has receipts for — is the
  behavioural spine: severity stacking order (ctkn-008), stack spacing numerics
  (ctkn-009), placement contracts (ctkn-006/007/011), snackbar timing (ctkn-016),
  and the four copy registers (ctkn-018…022).
- **F2 — aid-009 receipted a third time, now with coverage clauses** (ctkn-025):
  the toolkit doesn't just repeat 44×44, it names WHAT the target covers per
  component — a new, testable hit-area contract class.
- **F3 — Alert is not a notification** (ctkn-002): it's the bell trigger with
  badge + size ranks, plus Add Alert. Survey inventory line "4 taxa + Alert"
  corrected; Alert/Add Alert move to the canon-lacks vocabulary list.
- **F4 — copy tension for Dave** (ctkn-019): toolkit's per-instruction "Please"
  ban + mandated "Please correct the following errors" title vs copy-035's
  optional-please. One REVIEW flag raised, resolution shapes the
  apology/politeness lint. 📌 RULED (Dave, 2026-07-03): banned per-instruction,
  allowed only in the standard title — lint derivation unblocked.
- **F5 — hygiene deltas (appended to survey)**: snackbar set description reads
  "Notification contextual - scale 1" (debris, td-006) · lorem stubs at "Form
  errors" in BOTH the Banners and Notifications Standard frames (td-005
  extension) · "See XXX standard" placeholder + orphaned "Headline (optional)/
  Subject 2" template fragments in the browser standard's Accessibility section ·
  typos: "Tapabble" (global + snackbar guides), "warps" (snackbar guide),
  "experience of prevent" (browser standard) · U+2028 line separators inside text
  nodes (extraction hazard + content hygiene) · two snackbar Standard frames
  nested inside the section while the other two sit at page level.
- **F6 — no dark story in the toolkit for this family** (ctkn-028): canon's
  interim dark treatment isn't reconciling AGAINST anything — it's ahead of the
  source. Keep the dark-rag token-gap notes as the authority trail.
