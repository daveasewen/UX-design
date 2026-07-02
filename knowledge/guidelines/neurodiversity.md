# Neurodiversity — brand guidance (ingested)

*Source: create.hsbc → Foundations and identity → Accessibility →
`accessibility/Neurodiversity-Guidelines.html` + 15 subpages + the accessibility hub +
`accessibility/communication.html`, captured 2026-07-02 via Dave's authenticated session
(login-walled; ADR-0005 clearance). Engine-era format. Raw snapshots + per-page coverage
table: `guidelines/_sources/neurodiversity/`. Provenance of the standard: 2019 Hassell
Inclusion research for the National Autistic Society (400-person survey + expert
interviews + focus groups) — "the first set of guidelines based on solid empirical
evidence." 40 guidelines / 14 sections, for autism · dyslexia · ADHD · learning
difficulties. Many checkpoints cite WCAG equivalents as "met as part of the
accessibility criteria" — those receipts are marked below.*

## Scope note

This is the strongest new source of GENERATION-TIME checkable numbers since the icons
standard: view-length caps, banner-height caps, bright-colour area caps, sentence/
paragraph limits, column-layout limits. Per ADR-0005 §5, new checks enter at ADVISORY
and earn promotion by bite-testing. The workplace communication-styles section is
people-manager guidance — captured as skeleton, out of engine scope.

## Page layout

- **Simple pages; only elements relevant to the current task.** Design-review-level rule;
  success depends on the rest of the section. [TASTE at generation — the register system's
  sober end is the natural fit] {#neuro-001}
- **Page-length caps (at 1280×1024): index pages ≤4 vertical view lengths (non-mobile),
  article pages ≤5.** [ADVISORY-derivable — measurable at render time in the visual-QA
  loop] {#neuro-002}
- **Separate sections clearly: ≥20px whitespace between sections; separators/control
  boundaries ≥3:1 contrast (best practice 4.5:1).** [ADVISORY-derivable — the 3:1 boundary
  leg is already our indicator-contrast framework; the 20px whitespace check is new]
  {#neuro-003}
- **Important information top, above the fold; page purpose determinable without
  scrolling (1280×1024); front-load information.** Equal-importance items: alphabetical or
  chronological. [ADVISORY-derivable in part (above-fold purpose = heading present in
  first viewport); TASTE for ordering] {#neuro-004}
- **Every page carries a short purpose summary** — in the heading structure, banner, or
  first paragraph. [ADVISORY-derivable — composition-level check] {#neuro-005}
- **Banner/hero caps: initial images/banners ≤30% of page height; carousels and videos
  ≤30% (at 1280×1024).** [ADVISORY-derivable — direct render measurement; NOTE tension
  with hero-led marketing layouts, see Findings neuro-042] {#neuro-006}
- **Size communicates importance** — prominence proportional to importance; heading/font
  sizing reflects hierarchy. **"Underline of text should only be on links."** [the
  underline leg is BLOCKING-derivable (style scan); already house practice] {#neuro-007}
- **Symmetry + layout stability: max 2 different column layouts per page**; no significant
  mid-page layout changes; grid on homepages, single column on content pages.
  [ADVISORY-derivable — composition-level column-count scan] {#neuro-008}

## Navigation

- **Consistent, simple navigation across the site.** WCAG 3.2.3 receipt — met via
  accessibility criteria. [IN FORCE via a11y framework] {#neuro-009}
- **Links and buttons visibly clickable: underline links; visited links change colour
  (best practice); button boundaries ≥3:1.** ⚠ The :visited leg is a REAL canon gap —
  no snippet or canon.css styles :visited at all (checked 2026-07-02). 📌 RULED (Dave,
  2026-07-02 eve): **neuro best practice adopted as direction** — visited links should
  differ in colour; implement at the next Links touch (supercharge candidate territory —
  don't over-polish pre-uplift), then review the result. [REVIEW — implementation +
  review pending; advisory check candidate once a `link/visited` token exists]
  {#neuro-010}
- **Carousels: next/prev ≥3:1 + AT-labelled; helpful labels ("next month" not "next");
  chevron iconography; NO auto-scroll (or pausable); dot nav ≥3:1 + AT-labelled; peek
  the next slide.** [component spec — we have no carousel component; this is its gate
  contract if one is ever built. The no-auto-scroll leg is kin of our reduced-motion
  gate] {#neuro-011}
- **Menus: sequential (point-and-click over mouse-over); all top-level items visible
  without scrolling; ≤2 sub-levels; ESC dismisses; hover content stays while pointer
  moves over it** (WCAG 1.4.14 kin). [component-relevant — Navigations/Dropdown
  contract] {#neuro-012}
- **Sticky main menu for pages >1 screen height; sticky/menu content ≤35% of screen;
  avoid OTHER sticky elements.** [component-relevant — Headers behaviour spec, pairs
  with webf-016's scroll-shadow] {#neuro-013}

## Colours

- **Avoid lots of bright colours: soft, harmonious combinations; bright colours ≤20% of
  screen content.** Autistic users prefer low-contrast schemes — note this is about
  AREA of saturation, not permission to break contrast floors (floors still apply).
  [ADVISORY-derivable — saturated-area measurement at render; see Findings neuro-042:
  direct input to the register/expressive question] {#neuro-014}
- **User colour customisation** (background/text) — platform-level; "no standard autistic
  colour preference"; third-party overlays under investigation. [structure — platform
  capability, out of component scope; our dual-mode theming is the existing partial
  answer] {#neuro-015}

## Fonts

- **Minimum font size 12pt** (exceptions: sub/superscript, T&Cs, related). ⚠ pt-vs-px:
  12pt = 16px CSS at the standard 96dpi reading — under which our S6 (14px) and S7 (12px)
  standard-text sizes would fail; under a loose "12pt≈12px" reading our scale complies
  (S7=12px floor, 12px reserved for legal = mirrors the exception). The web type scale
  page and the store both treat 14px/12px as legitimate. [REVIEW — pt/px ambiguity;
  strict reading indicts the type scale itself, so almost certainly loose-reading
  intended; get Create Direct clarification when convenient] {#neuro-016}
- **One typeface family per page (no serif + sans-serif mixing); only HSBC fonts.**
  [IN FORCE — single-stack Univers Next canon] {#neuro-017}
- **User font customisation** (type + size) — platform-level. [structure] {#neuro-018}

## Text

- **Line height ≥1.5× font size; paragraph spacing ≥2× font size.** WCAG 1.4.12 receipt.
  Our scale: S5 16/24 = 1.5 exactly ✓; S6 14/20 ≈ 1.43 ✗; S7 12/16 ≈ 1.33 ✗ — same
  family of tension as neuro-016/webf-031; the brand's own scale sits below the neuro
  floor for small sizes. [REVIEW — fold with neuro-016 into one "small-type
  neuro-compliance" clarification] {#neuro-019}
- **≤4 sentences per paragraph; ≤240 characters per sentence (incl. spaces).**
  [ADVISORY-derivable — content-lint at generation time; pairs with webf-026 line
  length] {#neuro-020}
- **Don't interrupt text flow with images; callout quotes only at section ends; no
  scroll-stoppers.** [ADVISORY-derivable — composition-level] {#neuro-021}
- **Bold for phrases only** — never whole sections/lists; emphasis not structure.
  [ADVISORY-derivable — style scan kin of the all-caps gate] {#neuro-022}

## Use of language

- **Clear, concise language at the audience's reading age** (WCAG 3.1.5 receipt; does not
  impact regulatory requirements). [ADVISORY-derivable — readability scoring at
  generation] {#neuro-023}
- **Avoid metaphors and ambiguity.** The standard EXPLICITLY flags the tension: tone of
  voice supports "conversational, informal" style, but literal readers need unambiguous
  writing. ✅ RECONCILED 2026-07-02 by the tone-of-voice ingest — the brand's own
  standard partitions the licence: expressive is SURFACE-scoped (headlines, good news,
  marketing), literalness is FUNCTION-scoped (actions, instructions, warnings) — see
  `tone-of-voice.md` F2 + tov-019/031/046 (three literalness receipts). Not a
  contradiction, a partition. [ADVISORY-derivable — ambiguity/idiom lint, pairs with
  tov-046; charter band-mapping rides tov-016's REVIEW] {#neuro-024}
- **Avoid jargon/abbreviations/acronyms/idioms**; define acronyms on the page (WCAG
  3.1.3/3.1.4 kin; Style Guide has further guidance). [ADVISORY-derivable — pairs with
  the all-caps gate's acronym exemption: exempted acronyms should be DEFINED somewhere
  on the page] {#neuro-025}

## Non-textual information

- **Icons/visuals support text, never replace it** — content must remain comprehensible
  with all images and icons removed. [BLOCKING-derivable kin — we already require
  icon+label on RAG; this generalises it] {#neuro-026}
- **Toggle for decorative graphics/images** — platform-level. [structure] {#neuro-027}

## Images

- **Simple images, understood within ~2 seconds; single object in focus.** Image content
  never the sole carrier of information. [TASTE + the sole-carrier leg is neuro-026]
  {#neuro-028}
- **Meaningful images only** — congruent with the page story, adding value/clarity.
  [TASTE] {#neuro-029}
- **Background images sparingly; no content/form inputs overlaid on decorative images;
  uniform-texture backgrounds acceptable; non-patterned backgrounds on content pages.**
  [ADVISORY-derivable — the no-text/forms-on-decorative-images leg pairs with the parked
  text-on-gradient rule (type26-015): both are "text on visually active surfaces"
  restrictions] {#neuro-030}

## Video content

- **No auto-play video/audio; animations ≤5s** (WCAG 2.2.2 receipt). [IN FORCE — our
  reduced-motion + motion gates carry this] {#neuro-031}
- **Captions AND transcripts for all video/audio** (38.5% of respondents need audio
  transcripts; WCAG 1.2.1/1.2.2/1.2.4 receipts). [component-relevant — Video-player's
  gate contract] {#neuro-032}
- **Closed captions (user-toggleable), not open.** [component-relevant — Video-player]
  {#neuro-033}
- **Text intro above every video** (what it's about + implied length). [ADVISORY-derivable
  composition rule — Video-player placement contract] {#neuro-034}

## Movement

- **No auto-playing movement; pause mechanism where unavoidable; animations ≤5s; NO
  flashing** (WCAG 2.2.2 + 2.3.3 receipts). [IN FORCE — a11y gate (2.3.3) + mot-005]
  {#neuro-035}
- **Attention-attracting movement is a LAST resort** — use size/colour/font emphasis
  first. BUT: "small, animated movement of an arrow when moused over communicated that
  the section was clickable... limited and explainable, users did not find it
  disturbing" — an empirical receipt that small, purposeful HOVER motion aids
  comprehension. [TASTE — directly relevant to our scale-physics: supports
  attract-on-hover as functional affordance, cautions against decorative ambient motion;
  cite in future motion promotions alongside mot-007] {#neuro-036}

## Help pages

- **Help in multiple channels** (phone, live chat, email, FAQ on-site); help easy to find;
  sufficient instructions for any expected action. [structure/journey-level — phone
  anxiety makes non-phone routes essential] {#neuro-037}

## Customisation

- **Essential customisation set: font type + size, text + background colours, decorative
  graphics off, captions off** — tools clearly visible and easy to use. Platform-level;
  overlays under investigation. [structure — the definitive list if a preferences
  pattern is ever built; our theme system is the foundation] {#neuro-038}

## Re-learnability

- **Announce changes in advance** — form/function changes, journey changes, common-feature
  changes all proactively communicated. [journey-level; interesting kin of our own
  refresh-reconciliation discipline] {#neuro-039}

## User research

- **Research with autistic users before AND after redesigns** — global function.
  [structure — process rule; input to the user-research skill when relevant] {#neuro-040}

## Findings

1. **Small-type neuro-compliance cluster.** neuro-016 (12pt minimum, strict reading =
   16px) + neuro-019 (≥1.5 line-height; S6/S7 sit at 1.43/1.33) both indict the brand's
   OWN type scale for small sizes if read strictly. Since the type scale page and the
   toolkit export agree on S6/S7, loose readings are almost certainly intended (12pt≈12px;
   1.5× aspirational for body = S5 ✓). 📌 RULED (Dave, 2026-07-02 eve): record-to-review
   only — "this is one that will definitely change anyway" (the refresh will re-cut the
   type scale); do NOT chase Create Direct on it. [REVIEW — dormant until the refresh
   type pages re-issue] {#neuro-041}
2. **Calm-by-default vs expressive register.** neuro-006 (hero ≤30% height), neuro-014
   (bright colours ≤20% of screen), neuro-001/-028 (simplicity) collectively define a
   measurable "calm ceiling". The expressive register (charter §4, dual-live palettes)
   pushes the other way. These are not contradictions — they're the two dials of the
   fixed/flex charter with NUMBERS on the sober side for the first time. Generation
   consequence: the register spread should treat neuro caps as the sober register's
   defaults and as advisory signals elsewhere. [REVIEW — feed into the fixed/flex
   charter's register-temperature dial when tone-of-voice lands] {#neuro-042}
3. **:visited styling gap** — see neuro-010; zero :visited rules in canon. {#neuro-043}
4. **Communication guidance is a hub we did not descend** — 7 scenario subpages
   (meetings, multimedia, media, digital content, internal comms, surveys, social media).
   Scenario 4 (digital content) is the engine-relevant one. [REVIEW — queue scenario-4
   capture; low priority, likely overlaps WCAG + these guidelines] {#neuro-044}
5. **WCAG receipts inventory** — 10 of the 40 guidelines explicitly cite WCAG equivalents
   (3.2.3, 1.4.14 ×2, 1.4.12, 3.1.5, 3.1.4, 3.1.3, 2.2.2 ×3, 2.3.3, 1.2.1/1.2.2/1.2.4) —
   these are already carried by the a11y gate framework; the NEW enforcement surface is
   the layout/content numbers (neuro-002/003/006/008/014/020) which no WCAG rule covers.
   [structure note] {#neuro-045}

## Cross-references

`_A11Y-GATE.md` + `_validate_a11y.py` (WCAG receipts) · `web-foundations.md` (webf-024
type numbers ↔ neuro-016/019; webf-026 line length ↔ neuro-020; webf-016 sticky
behaviour ↔ neuro-013) · `icons.md` (icon+label ↔ neuro-026) ·
`typography-standards-2026.md` (type26-015 text-on-gradient ↔ neuro-030) ·
`motion-standards.md` (mot-005/mot-007 ↔ neuro-035/036) · `_FIXED-FLEX-CHARTER.md`
(neuro-042 register dials) · `tone-of-voice.md` (neuro-024 ↔ tov-019/031/046
literalness partition RECONCILED; neuro-023 readability ↔ tov-008/009 FK numbers) ·
`snippets/Links.reference.html` (neuro-010 :visited gap) · Video-player component
(neuro-032/033/034 gate contract).
