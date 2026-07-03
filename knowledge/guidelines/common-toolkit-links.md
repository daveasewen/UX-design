# Common Toolkit — Links family (Figma-sourced distillation)

*Provenance: Figma file `mI8hvIkV98nquoqWzKh5Kn` "HSBC Common Toolkit (MCP)", Links
page `45015:45858`, captured 2026-07-03 via Figma MCP (desktop bridge text extraction
+ remote screenshots). Surfaces: "Standard" guidelines frame `45024:140851` + guide
components `00 Arrow link guide` 1259:75803 · `00 Back Link guide` 1249:75843 ·
`00 Icon link guide` 1259:75917 · `00 Inline link guide` 1281:73568. Guide vintage:
"Version 0.0.0 | May 2023"; component sets last touched 2026-06 — LAYERED VINTAGES
inside the toolkit (kin of td-002). Guides defer to "our create.hsbc text link
standard" (Web) — the channels-batch capture will close that loop. First `ctkl-*`
file of the toolkit tranche-1 pass; feeds the Links ★ pass directly.*

## Usage and taxonomy

- **Links are primarily navigation**; they may carry lower-priority actions or many
  same-priority actions — buttons take higher-priority/fewer actions. [ADVISORY —
  composition-time heuristic; canon Links meta already states the nav-first rule]
  {#ctkl-001}
- **Don't provide so many links it becomes unclear where to go** (Do/Don't pair).
  [TASTE — no mechanisable threshold given] {#ctkl-002}
- **The toolkit's link taxonomy**: chevron links (arrow · back · expand) · icon
  links (incl. download, external, anchor, add/remove) · inline links. [RECORDED —
  the reconciliation frame for the Links ★ pass; canon's set (standard/label/icon)
  lacks back, expander, and anchor concepts entirely] {#ctkl-003}

## Chevron links (arrow + back + expand)

- **Chevron links carry a red chevron** as signposting. [ADVISORY — canon uses
  currentColor chevrons in some contexts; check at ★ pass] {#ctkl-004}
- **Back links: chevron on the LEFT of the label, pointing left.** [ADVISORY — blocking candidate — exact; no back-link exists in canon yet] {#ctkl-005}
- **Expand links toggle additional content below** between hidden and shown.
  [RECORDED — expander pattern; overlaps canon Accordion/View-options territory,
  map at ★ pass] {#ctkl-006}
- **Arrow sizing is NUMERIC and font-tier-keyed**: font-1…4 → arrow = x-height,
  on the baseline, text gap = arrow/2 (e.g. font-1: x-height 22px → arrow 22px,
  gap 11px); font-5…7 → arrow = cap-height, gap = arrow/2 (e.g. font-5: cap 12px →
  arrow 12px, gap 6px). [ADVISORY — blocking-capable numerics — render-axis check candidate;
  canon's chevron sizing must be audited against this at the ★ pass] {#ctkl-007}
- **Wrap behaviour differs by type**: arrow links — chevron stays attached to the
  LAST word, never an orphan line; back/icon links — icon STAYS IN PLACE, aligned
  to the first line, text aligns left with sentence start. [ADVISORY — blocking render-axis
  candidate; exact and testable] {#ctkl-008}

## Icon links

- **Only globally recognised icons** (per the icons guidelines). [ADVISORY — pairs
  with the icon-source hard gate; our sprite-manifest rule is the stronger form]
  {#ctkl-009}
- **Download links: download icon on the LEFT + file format and size in brackets
  after the label text.** [ADVISORY — blocking candidate — exact microcopy contract; NOTE
  canon's download icon-gap (line-only glyph, no fill) is already logged in
  `_ICON-GAPS.md`] {#ctkl-010}
- **External links open in a new tab and carry an indicator icon** — the icon sits
  at the END of the text AS PART OF THE LINK (Default/Hover/Pressed shown in the
  inline guide). [ADVISORY — blocking candidate — this is CA-6's build spec at source; the
  Links ★ external-link variant (ruled IN 2026-07-03) builds to exactly this]
  {#ctkl-011}
- **Page anchor links: only when content length makes it absolutely necessary**;
  prefer short, well-sectioned content; use a standard preceding phrase ("In this
  page:"); anchor-up/anchor-down icons give the visual clue. [RECORDED pattern —
  no canon equivalent; composition-layer candidate] {#ctkl-012}
- **Add/remove (input fields) follows the Icon Link pattern** — "Add another input
  field" (+) / "Remove input field" (⊗). [RECORDED — routed to the Input-fields
  supercharge payload with aid-018] {#ctkl-013}

## Inline links

- **Underlined within body text**; weight MATCHES the surrounding text weight in
  ALL states (light text → light link, regular → regular). [ADVISORY — blocking candidate —
  exact; canon inline links underline but the weight-matching rule is new] {#ctkl-014}
- **Hyperlink ≤5 words; linked text descriptive of the destination**; prefer the
  link at the END of the sentence. [ADVISORY — ≤5-words is a cost-0 check candidate;
  descriptiveness overlaps aca-004 (already blocking)] {#ctkl-015}

## Target size, states, colour

- **"Text links have a surrounding target area of 44px, unless they are inline."**
  And the reasoning, verbatim: inline targets reflow and could overlap, so "targets
  which are contained within one or more sentences are excluded from the target
  size requirements". [IN FORCE — component-level receipt for the aid-009 ruling
  (fail<24/advisory<44) AND the named inline exception out; canon Links can claim
  this out where applicable] {#ctkl-016}
- **Internal links open in the current tab; external in a new tab.** [ADVISORY —
  pairs with ctkl-011] {#ctkl-017}
- **Hover: text underlines on mouse-over of text OR icon — icon and text behave as
  ONE wrapped link**; the target area wraps both. [ADVISORY — blocking candidate — canon's
  Links hover contract should assert the one-wrapped-link behaviour] {#ctkl-018}
- **Focus: default browser style around the container.** [RECORDED — DELTA: canon
  EXCEEDS this with a custom 2px focus ring + the new VD-9 numerics; keep canon's
  stronger form, log the divergence as intentional] {#ctkl-019}
- **On dark: links and associated icons are white.** [ADVISORY — canon's
  text/on-inverse token already encodes this; confirm icon parity at ★ pass]
  {#ctkl-020}
- **Icon size is relative to text size; exact specs live in "your programme
  toolkit".** ⚠ Source gap: the Common Toolkit defers numbers to programme
  toolkits (Sutherland-side for us). [RECORDED] {#ctkl-021}

## Copy rules

- **Link text: describe the action or destination; concise; sentence case;
  ≤8 words (~55 chars); NO 'Click here'/'Learn more'; NO full stop at the end.**
  [ADVISORY — ≤8-words/55-chars + terminal-full-stop are cost-0 check candidates;
  sentence case + bare-link bans are ALREADY BLOCKING (gate checks 4 + 7);
  xref copy-016 no-full-stops-in-microcopy] {#ctkl-022}

## Accessibility (the guide quartet, verbatim on all four guides)

- **400% text size must not break formatting** · **never disable pinch-and-zoom** ·
  **visible focus outline when tabbing** · **adhere to the HSBC Accessibility
  Framework + Brand Design Team review before release**. [IN FORCE — receipts for
  acd-005 (400%), acd-010/check J (pinch-zoom), acd-017 (focus), and the
  Living-Wall-style pre-release checkpoint (gai-* kin). The quartet repeating on
  every guide = the toolkit's own per-component gate ritual] {#ctkl-023}

## Findings

- **F1 — the 44 ruling is receipted at component level, with its exception out
  named** (ctkl-016): three independent sources now (ID-26, axs-003, toolkit
  Standard frame). The advisory <44 tier's exception modelling should honour the
  inline exclusion verbatim.
- **F2 — CA-6 build spec sourced** (ctkl-011): end-of-text icon, part of the link,
  new-tab behaviour. The Links ★ external-link variant has its contract.
- **F3 — canon vocabulary gaps confirmed**: back link, expander link, anchor
  links, add/remove pattern, download microcopy contract. None block current
  screens; all are ★-pass or supercharge scope.
- **F4 — toolkit hygiene deltas (appended to survey)**: guide vintage "0.0.0 May
  2023" under 2026-06 component edits (layered vintages, td-002 kin) · lorem-ipsum
  stubs in the shipped Standard frame (td-005) · icon-size numbers deferred to
  programme toolkits (source gap, ctkl-021).
- **F5 — canon exceeds on focus** (ctkl-019): browser-default focus vs canon's
  custom ring + VD-9 numerics. Intentional divergence, keep and record.
