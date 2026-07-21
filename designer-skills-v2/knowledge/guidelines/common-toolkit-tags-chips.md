# Common Toolkit — Tags + Chips/Pills families (Figma-sourced distillation)

*Provenance: Figma file `mI8hvIkV98nquoqWzKh5Kn` "HSBC Common Toolkit (MCP)",
captured 2026-07-03 via Figma MCP (bridge text extraction, U+2028-safe escape +
one screenshot for the shared-target diagram). TAGS: Tags page `413:10962` —
`00 Tags guide` 1887:90493 · Standard frames 44397:143942 + 44423:158328
(EXACT DUPLICATES, 42 nodes/3737 chars each — td-009) · sets `On Light:/On Dark:
Tag` 413:12198/2348:64312 + `On Light:/On Dark: Tag link` 414:11661/2346:64245.
CHIPS: live in the **Chips section of the Selection controls page**
(45105:252063 → section 45132:331551) — `00 Chips guide` 1824:89053 · "Pills"
Standard frame 45132:334258 (12,091px tall, the richest standard captured so
far) · sets Chip toggle 1719:84595 · Chip multiple selection 1719:84636 · Chip
delete 1738:86848 · Chip single selection 1738:86780. Guide vintage "Version
0.0.0 | May 2023"; sets touched 2026-06 (td-002 kin). Canon counterparts:
tags.meta.json + selection-controls.meta.json — both already receipt the
deprecate-token leaks at tokenValidation, so as with Notifications the value
here is the RULES layer. Third `ctk*` file of tranche 1; feeds the Tags ★ pass
and the tab-bar-islands revisit (Chip toggle kin).*

## Tags — usage and taxonomy

- **Two tag patterns — tags (non-interactive) and tag links** — each also
  available text-only "depending on the prominence required". The create.hsbc
  "tags standard" is the deferred authority (Web + App). [RECORDED — taxonomy
  frame for the Tags ★ pass; canon's `type` prop (tag / tag-link) matches]
  {#ctkt-001}
- **Tags surface KEYWORD DESCRIPTORS**: an item's content composition and its
  relationship to a broader content structure; keywords reusable by other UI
  patterns for search and filtering. [ADVISORY — usage-boundary heuristic for
  composition time] {#ctkt-002}
- **Do link tags to groups or lists of content. Do present tags consistently:
  ordered alphabetically OR by content priority (most important first), and the
  chosen order kept consistent throughout the same content structure.**
  [ADVISORY — ordering-consistency check candidate at composition time]
  {#ctkt-003}
- **Don't use tag styles for metadata that isn't a keyword descriptor** (date,
  read time), **for arbitrary classifications, or to highlight product
  features.** [ADVISORY — misuse boundary; the metadata clause is the sharp
  edge] {#ctkt-004}
- **Don't add icons to tags or associate actions other than a standard tag
  link** — "consider using selection pills if sorting or filtering based on
  keyword descriptors". [ADVISORY — blocking candidate — exact and testable
  (no-icon rule); also the tag↔pill boundary in one line] {#ctkt-005}
- **Affordance contract: non-interactive tags must READ as informational (not
  navigation); tag links must READ as clickable.** Two blessed tag-link styles
  exist (example A/B) — "be consistent in which style you apply throughout the
  entire section". [ADVISORY — affordance-differentiation heuristic + a
  consistency check candidate] {#ctkt-006}
- **Placement: tags at the start and/or end of content; NOT normally interactive
  at the top of an article; below the content, tag links provide useful
  navigation.** Be consistent so users learn the format. [ADVISORY —
  composition-layer placement heuristic] {#ctkt-007}
- **Visual style is deferred to "your programme toolkit".** [RECORDED — source
  gap, ctkl-021 kin — Sutherland-side for us] {#ctkt-008}

## Tags — layout and content

- **Label centred horizontally and vertically in the container; tags expand
  horizontally with the label; a GROUP that overflows one row wraps onto two
  rows; an individual too-long label wraps onto a second line.** [ADVISORY —
  render-axis check candidates (no truncation implied); xref canon Tags
  responsive rules at the ★ pass] {#ctkt-009}
- **Tag copy: keywords describing the content theme · sentence case · never more
  than THREE words.** [ADVISORY — ≤3-words is a cost-0 check candidate;
  sentence case is ALREADY BLOCKING (gate check 4); xref the tags-blessed desk
  ruling 2026-07-03] {#ctkt-010}

## Tags — target and focus

- **Target ≥44×44 CSS px for tags with containers, covering the whole tag item.
  For GROUPED tag links the guide gives the numeric recipe: the font-6 text row
  (20px line) extends 12px above + 12px below = 44px effective target, and
  ADJACENT ROWS MAY SHARE the 12px band** — "the space for target area can be
  'shared' so long as it doesn't overlap the actual physical target area"
  (diagram: 12/20/12/20/12 = 76px for two rows, each claiming 44). [ADVISORY —
  aid-009 receipt #4, and the SHARED-target clause is a genuinely new hit-area
  contract class — grouped text-links can legitimately claim overlapping
  clearance zones; directly relevant to the sub-44 revisit pile] {#ctkt-011}
- **Default browser/native focus states, with high contrast against non-focused
  elements.** Canon exceeds with the custom ring. [RECORDED — intentional
  divergence, ctkl-019/ctkn-026 kin] {#ctkt-012}
- **Set census (Tags)**: OL+OD pairs ship for both sets; Size = small (font-6
  14/20) / extra small (font-7 12/16); Background = true/false; Tag link's State
  = default + **a single merged "hover / pressed" variant**. Canon models hover
  and pressed separately and the WCAG state-contrast rule wants active > hover
  differentiation — canon EXCEEDS the toolkit here; keep and record. [RECORDED —
  state-model delta, feeds the Tags ★ pass] {#ctkt-013}
- **Token census (Tags)**: Tag background rides `non-interactive
  (depricate)/surface/neutral-2` #ededed; Tag link rides `interactive
  (depricate)` primary-surface/high-contrast-border + on-light hover deprecates;
  font-6/font-7 by size (`font-6/regular-link` style for links). [IN FORCE —
  canon tags.meta.json tokenValidation already records exactly this (the
  no-equivalent subtle-surface blocker); zero new gaps] {#ctkt-014}

## Chips/Pills — naming and usage

- **The naming register is THREE-way: create.hsbc standard says "Pills", the
  component sets say "Chip …", and the set descriptions say "Pill response /
  Pill multiple selection".** The Chips guide itself routes to "our create.hsbc
  pills standard". [RECORDED — td-007; hub-and-spoke absorbs it (node ID =
  identity) but retrieval must know both nouns; canon says Chips] {#ctkt-015}
- **Pills represent an input, attribute or action** — selections, filtering,
  contextual actions; normally in GROUPS rather than singular; NOT navigational
  links; presented with EQUAL hierarchy — no primary/secondary visual
  treatments within a group. [ADVISORY — the equal-hierarchy clause is a
  testable group contract] {#ctkt-016}
- **Type taxonomy**: Response pills (pre-set conversational responses, eg live
  messaging) · Selection pills (filtering, touch-friendly: single / multiple /
  delete) · Toggle pills (action "shortcuts" to on-screen functions; never nav,
  never a Switch replacement on settings pages). [ADVISORY — taxonomy frame;
  canon selection-controls models chip toggle/single/multi/delete 1:1]
  {#ctkt-017}
- **The four Don'ts: don't label content with pills (use tags) · don't represent
  process status (pills always provide a function) · don't use pills inside a
  standard form (use checkboxes/radios) · don't place pills directly alongside
  or in place of buttons.** [ADVISORY — blocking candidates — all four are
  composition-time testable boundaries; the pills↔tags mirror of ctkt-005]
  {#ctkt-018}

## Chips/Pills — structure and state semantics

- **Anatomy**: container · label · icon/action (may change with state) ·
  destructive action (deletes the pill and removes the associated selection) ·
  processing spinner (optional — for actions whose effect isn't visually
  apparent). [ADVISORY — structure contract; the spinner is a canon vocabulary
  gap (no chip-spinner state in canon)] {#ctkt-019}
- **Toggle-pill state change must be LEGIBLE: the label wording expresses the
  state change; a tick icon may signal it if the original pill had no icon;
  open→filled icon states may reinforce it in conjunction with the label.**
  [ADVISORY — state-legibility contract, kin of the WCAG state-contrast rule —
  label semantics carry the state, not colour alone] {#ctkt-020}
- **Icons are all-or-nothing: "If using icons, all pills should have icons
  across all states."** [ADVISORY — blocking candidate — exact group-consistency
  check] {#ctkt-021}
- **State ladders (per the standard)**: Response = unselected/hover/pressed/
  selected/with-icon/disabled (non-selected MAY be disabled after one is chosen)
  · Toggle = unselected + selected × default/hover/pressed (6) · Single
  selection = those 6 + unselected-disabled + selected-disabled (8) · Multiple
  selection = those 8 + INDETERMINATE for partial selection inside NESTED
  selection pills (9) · Delete = unselected/hover/pressed (3). A processing
  spinner state can be added to any. [ADVISORY — criteria-contract input for the
  ★ pass; note nested-pill indeterminate parallels the Checkbox indeterminate]
  {#ctkt-022}
- **Single-selection padding must reserve space for the tick so selection does
  NOT change the pill's width.** [ADVISORY — blocking candidate — exact,
  render-axis testable (no layout shift on select)] {#ctkt-023}
- **Delete pills display an APPLIED filter made elsewhere and allow its direct
  deletion — never shown directly alongside single/multiple selection pills.**
  [ADVISORY — composition boundary] {#ctkt-024}
- **An Apply button may action selection pills** (complex filter sets,
  minimising server calls) — always visually separate the pills from the
  button. [ADVISORY — pattern contract; xref ctkt-018's
  no-pills-alongside-buttons: separation is what reconciles them] {#ctkt-025}

## Chips/Pills — layout and content

- **Dynamic width from label with fixed side padding; 8px between chips; no
  truncation — at container max-width the label wraps to a second line
  PRESERVING the original corner radius.** The guide adds: chip copy SHOULD not
  wrap; if unavoidable, keep the same padding and alignment as single-line.
  [ADVISORY — blocking-capable numerics (8px gap) + render-axis wrap contract;
  guide and standard agree in direction: avoid wrap, tolerate it gracefully]
  {#ctkt-026}
- **Groups place horizontally or vertically; keep horizontal pills on one line
  where possible; NEVER force a single row with horizontal scroll — wrap onto
  the next row.** [ADVISORY — blocking candidate — the no-horizontal-scroll ban
  is exact; xref horizontal-scroll.md rules] {#ctkt-027}
- **Copy contracts**: Response + Toggle pills — sentence case, ≤5 words, ACTION
  VERBS, make the resulting action clear. Selection pills — sentence case,
  ≤5 words, AVOID verbs that sound like actions. [ADVISORY — ≤5-words is a
  cost-0 check candidate; the verb polarity split (action verbs vs no action
  verbs BY TYPE) is the sharp edge; sentence case already blocking] {#ctkt-028}
- **Target area covers the ENTIRE chip container, minimum 44×44.** [ADVISORY —
  aid-009 receipt #5 with coverage clause (whole container), ctkn-025 kin]
  {#ctkt-029}
- **Style deferred to "your programme toolkit"; default native focus states**
  (canon exceeds, keep). [RECORDED — source gap + focus divergence, same pair
  as ctkt-008/012] {#ctkt-030}

## Chips/Pills — set census vs standard (the reverse vintage)

- **The Figma sets model ONLY default / "hover (web)" / pressed (× Selected,
  × Icon on toggle) — none of the standard's disabled, selected-disabled,
  indeterminate, with-icon-all-states, or spinner states exist as variants.**
  The STANDARD is ahead of the SETS — layered vintages in reverse (the guides
  lag the sets, the sets lag the standard). Also: "hover (web)" bakes a platform
  annotation into a variant value (register hygiene tell, kin of S4). Canon
  selection-controls already models disabled + error beyond the sets. [RECORDED
  — td-010; at the ★ pass, criteria contracts should build to the STANDARD's
  ladder, not the sets'] {#ctkt-031}
- **Token census (Chips)**: form/* family (border #767676 · background
  transparent / hover #f3f3f3 / pressed #767676) + the deprecated `interactive
  (depricate)/on-light/surface/active/*` cluster for the selected fill
  (#000000 default / #333333 hover / #767676 pressed) + on-dark deprecate
  text/icon pairs; font-6 medium. [IN FORCE — canon selection-controls
  tokenValidation already records the active/* deprecate as the recurring
  selected-fill token; zero new gaps] {#ctkt-032}

## Findings

- **F1 — two genuinely new contract classes for the engine**: the SHARED target
  band for grouped text links (ctkt-011: 12+20+12=44 with row-overlap allowed —
  decodes the sub-44 question for dense link groups) and the no-layout-shift
  select rule (ctkt-023: padding reserves the tick's width). Both exact, both
  render-axis testable.
- **F2 — the tag↔pill↔button boundary is now fully sourced**: tags label, pills
  act, buttons commit (ctkt-004/005 + ctkt-016/018). Canon's Tags ★ and the
  fixed/flex vocabulary rules get their misuse boundaries from one place.
- **F3 — reverse vintage discovered** (ctkt-031, td-010): the Pills standard
  documents state ladders the component sets never received. Prior tells showed
  docs LAGGING sets (td-002); this is the standard LEADING them. Ratifies the
  survey's layered-vintages thesis from both directions — and means set-census
  alone under-counts criteria.
- **F4 — copy contracts have a verb-polarity split by type** (ctkt-028):
  response/toggle WANT action verbs, selection pills avoid them. A lint that
  knows the chip type is strictly stronger than a generic microcopy check.
- **F5 — hygiene deltas (appended to survey)**: td-007 Pills/Chips/Tag-link
  three-way naming register · td-008 `Chip single selection` AND `Chip delete`
  descriptions both read "Pill multiple selection" (debris, td-006 kin) ·
  td-009 the Tags page ships two EXACT-duplicate Standard frames · td-010 the
  reverse vintage (F3) · lorem stubs at every Pills-standard section intro +
  "See XXX standard" ×4 across Tags/Pills accessibility callouts (td-005
  extension) · "Tapabble" again (Chips guide) · merged "hover / pressed" Tag
  link variant vs split chip states — inconsistent state modelling across
  families on the same page tree.
- **F6 — canon exceeds twice, same pattern as Links/Notifications**: custom
  focus ring (ctkt-012/030) and split hover/pressed states (ctkt-013). Both
  intentional divergences to keep and record, per the ctkl-019 precedent.
