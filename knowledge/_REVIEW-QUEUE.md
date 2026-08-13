# Review queue — confidence-tagged assertions

> Every assertion in the component metas that is **not** directly observed canon. Formalises the in-prose confidence convention (Graphify-borrow #1). 🔴 **review** = verify before trusting; 🟡 **inferred** = reasoned, lower urgency. `asserted` items (the default) are not listed. Generated — regenerate after editing metas: `python3 knowledge/_build_review_queue.py`. Vocabulary in `_CONFIDENCE.md`; machine detail in `_REVIEW-QUEUE.json`.

**Totals:** 172 items across 56 components — 159 🔴 review, 13 🟡 inferred. By category: other 65, anti-pattern 52, token-rebind 29, accessibility 26.

Most-flagged components: Confirmation (10), Account card (9), Action bar (8), Tab-bar (7), Badge (6), Eyebrow (6), Avatar (5), Button (5).

## Token-rebind — verify before the Sutherland migration (29)

These gate the deprecated-token rebind: each names a best-guess replacement that must be confirmed against the real Sutherland values. Cross-ref `tokens/_manifests/depricate-replacement-map.json` and `_blast-radius.json`.

**Button**
- 🟡 `tokenValidation.depricateUsage.on-dark.auditedNodes` — On Dark primary 641:103685 (representative — tertiary/quaternary on-dark likely similar, not exhaustively queried)

**Dropdown**
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW (form/border/default or scrollbar/foreground — same value)
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW (form/background/hover — same value)

**Headers**
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW — no live subtle-surface token (same gap family as Avatar surfaces)

**Hero**
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW (no clean live border)
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW (white border on dark)

**Input fields**
- 🟡 `tokenValidation.depricateUsage.notExhaustive` — Input Field Large, Multi-line, and Input label not individually queried — expected same pattern (Large/multi-line = same effects; label likely clean).

**Links**
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW — NO live equivalent (same blocker as Avatar on-dark disabled)
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW — NO live equivalent (same blocker as Avatar on-dark disabled)

**List items**
- 🔴 `tokenValidation.depricateUsage.blockersNoEquivalent.rebind` — REVIEW — no live subtle-surface (Avatar/Headers gap family)
- 🔴 `tokenValidation.depricateUsage.blockersNoEquivalent.rebind` — REVIEW — no live subtle-surface
- 🔴 `tokenValidation.depricateUsage.blockersNoEquivalent.rebind` — REVIEW — no live on-dark surface (Avatar/Hero gap)
- 🔴 `tokenValidation.depricateUsage.blockersNoEquivalent.rebind` — REVIEW — no live (Avatar on-dark border blocker)

**Navigations**
- 🔴 `tokenValidation.depricateUsage.blockersNoEquivalent.rebind` — REVIEW — no live subtle-surface (Avatar/Headers/List gap family)
- 🟡 `tokenValidation.depricateUsage.namespaceFlags` — LIVE 'interactive/on-light/*' namespace seen on the SEARCH FLYOUT (interactive/on-light/surface/primary/default #fff, interactive/on-light/border/active/default #000, interactive/on-light/surface/brand-1/default #db0011 + /disabled #d7d8…

**Notifications**
- 🟡 `tokenValidation.depricateUsage.note` — Only the Contextual family surfaced deprecated rag/icon tokens (error + success). The information badge glyph is likely also rag/icon (depricate)/information/icon and warning uses rag/text/on-light (#333) — all map cleanly to rag/text/on…

**Pagination**
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW form/border/default
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — divider/border/subsection (REVIEW)

**Quick actions**
- 🔴 `tokenValidation.depricateUsage.blockersNoEquivalent.rebind` — REVIEW — no live subtle-surface (Avatar/Headers/List/Nav gap family)

**Selection controls**
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW — no clean live #333 surface
- 🔴 `tokenValidation.depricateUsage.blockersNoEquivalent.rebind` — REVIEW — no live subtle-surface
- 🔴 `tokenValidation.depricateUsage.blockersNoEquivalent.rebind` — REVIEW — no live subtle-surface

**Slider**
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW — form/border/default | scrollbar/foreground (both #767676); replacement-map lists neutral-6 as review (mode-aware on dark)

**Status indicator**
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW — no rag/neutral-tint exists. Approved/declined/pending disabled use rag/*-tint; cancelled has no tint sibling, so it falls back to neutral-3. PROPER FIX: add a rag/neutral-tint token, then rebind.

**Tags**
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW — on-dark surface, no clean live equivalent
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW — on-dark surface
- 🔴 `tokenValidation.depricateUsage.tokens.rebind` — REVIEW — on-dark border
- 🔴 `tokenValidation.depricateUsage.blockersNoEquivalent.rebind` — REVIEW — no live subtle-surface (Avatar/Headers/List/Nav/Quick-actions gap family)
- 🔴 `tokenValidation.depricateUsage.blockersNoEquivalent.rebind` — REVIEW — no live on-dark surface (Avatar/Hero/List gap)

## Accessibility — verify in code/with the a11y team (26)

**Accordion**
- 🔴 `accessibility.focus` — REVIEW: the Figma component set defines default/hover/pressed but no explicit focus-visible state — confirm a visible focus indicator exists in code

**Account card**
- 🔴 `accessibility.screenReader` — REVIEW (inferred): the status dot is decorative (aria-hidden) — meaning is in the chip label text. Confirm the masked number ('···4821') reads acceptably, and whether the balance needs an explicit aria-label (e.g. 'Balance £3,248.55').

**Action bar**
- 🔴 `accessibility.focusOrder` — REVIEW (inferred): DOM order is tertiary→secondary→primary (Back → Cancel → Confirm) so keyboard focus runs back-out → forward; the visual reorder at narrow widths (primary top, Back bottom) is CSS order only — confirm this does not conf…

**Avatar**
- 🔴 `accessibility.screenReader` — REVIEW (inferred): image/icon avatars need an accessible name (e.g. the person's name) or be marked decorative if adjacent text already names them

**Badge**
- 🔴 `accessibility.role` — REVIEW: badge is a decorative/status adornment on a host element; the host element (link/button/icon) is the focusable control
- 🔴 `accessibility.screenReader` — REVIEW (inferred): a colour dot alone is not accessible — expose the meaning in text (e.g. 'Inbox, 1 new message'); for the number version, ensure the count is announced. Confirm how this is implemented in code.

**Breadcrumbs**
- 🔴 `accessibility.structure` — REVIEW (inferred): mark up as a nav landmark labelled 'Breadcrumb' with an ordered list; current page exposed via aria-current='page' (matches the 'no-link' state)

**Cards**
- 🔴 `accessibility.interactive` — REVIEW (inferred): an interactive card should be a single focusable control (or have one clear primary link); avoid nested interactive elements that create multiple tab stops with unclear order

**Confirmation**
- 🔴 `accessibility.screenReader` — REVIEW (inferred): confirm the message reads naturally after the title; consider whether the success should be announced via a live region when it appears mid-flow.

**Countdown timer**
- 🔴 `accessibility.announce` — REVIEW (inferred): expose remaining time to assistive tech (e.g. role=timer / polite aria-live updates at sensible intervals) — don't rely on the depleting ring alone
- 🔴 `accessibility.timingAdjustable` — REVIEW (inferred): where the countdown triggers an action (e.g. session timeout), provide a way to extend/turn off/adjust the limit (WCAG 2.2.1)
- 🔴 `accessibility.motion` — REVIEW (inferred): respect prefers-reduced-motion for the animated ring

**Divider**
- 🔴 `accessibility.semantics` — REVIEW (inferred): decorative dividers should be hidden from assistive tech; if a divider conveys a meaningful grouping boundary, expose it as a separator (role=separator)

**Dropdown**
- 🔴 `accessibility.keyboard` — REVIEW (inferred): full keyboard operation — open/close, arrow navigation, type-ahead, Enter/Escape; native family inherits browser behaviour
- 🔴 `accessibility.roles` — REVIEW (inferred): non-native must implement combobox/listbox semantics (aria-expanded, aria-activedescendant, option roles, aria-selected); prefer native where possible for robustness

**Eyebrow**
- 🔴 `accessibility.screenReader` — REVIEW (inferred): read inline before the heading it precedes. If purely decorative it may be redundant with the heading — confirm it adds meaning, otherwise consider aria-hidden.

**Headers**
- 🔴 `accessibility.headingSemantics` — REVIEW (inferred): map header titles to the correct heading level (h1/h2…) for screen-reader structure; display header is typically the screen's h1
- 🔴 `accessibility.processing` — REVIEW (inferred): the Headers Display processing state should announce status (aria-live)

**Hero**
- 🔴 `accessibility.heading` — REVIEW (inferred): hero headline is typically the page h1; ensure correct heading level
- 🔴 `accessibility.video` — REVIEW (inferred): background video must be pausable and must not autoplay audio; respect prefers-reduced-motion

**Input fields**
- 🔴 `accessibility.datePicker` — REVIEW (inferred): calendar must be keyboard-navigable (arrow keys, Esc), day cells expose selected/disabled/unavailable states to AT

**List items**
- 🔴 `accessibility.processing` — REVIEW (inferred): processing state should announce status (aria-live/aria-busy)

**Loading indicator**
- 🔴 `accessibility.motion` — REVIEW (inferred): continuous animation should respect prefers-reduced-motion

**Modals**
- 🔴 `accessibility.focusTrap` — REVIEW (inferred): focus must be trapped within the modal while open and returned to the trigger on close

**Progress tracker**
- 🔴 `accessibility.announce` — REVIEW (inferred): step changes should be announced (aria-live) as the user advances

**Summary**
- 🔴 `accessibility.screenReader` — REVIEW (inferred): confirm amounts read naturally (e.g. '£250.00' as 'two hundred and fifty pounds'); the value carries meaning, not its right-alignment.

## Anti-patterns — confirm or promote to asserted (52)

**Accordion**
- 🔴 `antiPatterns` — REVIEW (inferred): hiding required or critical information inside a collapsed panel
- 🔴 `antiPatterns` — REVIEW (inferred): deeply nesting accordions within accordions
- 🔴 `antiPatterns` — REVIEW (inferred): hard-coding the header text colour or rule colour instead of binding text/default and border/subtle tokens

**Account card**
- 🔴 `antiPatterns` — REVIEW (inferred): conveying account status by the dot colour alone — keep the meaning in the label (1.4.1).
- 🔴 `antiPatterns` — REVIEW (inferred): rounding the card corners — cards are square (angular rule; Badge + Avatar are the only round exemptions).
- 🔴 `antiPatterns` — REVIEW (inferred): hard-coding the balance type instead of a display/amount token once one exists.

**Action bar**
- 🔴 `antiPatterns` — REVIEW (inferred): more than ~3 actions in the bar — overflow secondary actions into a menu instead.
- 🔴 `antiPatterns` — REVIEW (inferred): two competing primary (red) buttons — exactly one primary per bar.
- 🔴 `antiPatterns` — REVIEW (inferred): giving Back a filled (primary/secondary) treatment — it is the lowest-emphasis action (tertiary/outlined).
- 🔴 `antiPatterns` — REVIEW (inferred): rounding the buttons or the bar — brand is square/angular.
- 🔴 `antiPatterns` — REVIEW (inferred): relying on the CSS reorder while leaving DOM order such that keyboard focus reaches Confirm before Cancel — keep DOM order logical (2.4.3).

**Avatar**
- 🔴 `antiPatterns` — REVIEW (inferred): using an avatar as the sole accessible label for a control — pair with a text name
- 🔴 `antiPatterns` — REVIEW (inferred): shrinking the tappable area below 44×44 even when the visual avatar is small (36px)
- 🔴 `antiPatterns` — REVIEW (inferred): relying on the deprecated surface/border tokens long-term (see tokenValidation)

**Badge**
- 🔴 `antiPatterns` — REVIEW (inferred): using a badge to convey critical information that must not be missed — it's a passive indicator, not an alert
- 🔴 `antiPatterns` — REVIEW (inferred): showing a number badge where a count is not meaningful (use the simple dot instead)
- 🔴 `antiPatterns` — REVIEW (inferred): hard-coding the badge fill instead of binding color/primary (and, once migrated, a semantic primary surface token)
- 🔴 `antiPatterns` — REVIEW (inferred): leaving the on-icon badge bound to the deprecated surround token (see tokenValidation)

**Breadcrumbs**
- 🔴 `antiPatterns` — REVIEW (inferred): making the current page (no-link) a clickable link
- 🔴 `antiPatterns` — REVIEW (inferred): relying on colour alone to show the hover/pressed state — here states share text/default (#333333), so a non-colour cue (underline) is required (see WCAG state-contrast guidance)
- 🔴 `antiPatterns` — REVIEW (inferred): using breadcrumbs as the primary navigation rather than a secondary location aid

**Button**
- 🔴 `antiPatterns` — REVIEW (inferred): using a tertiary/quaternary button for the main action where a primary is expected
- 🔴 `antiPatterns` — REVIEW (inferred): relying on the deprecated on-dark surface tokens long-term (see tokenValidation — on-dark needs migration)

**Cards**
- 🔴 `antiPatterns` — REVIEW (inferred): nesting multiple independent links/buttons inside an interactive (basic) card
- 🔴 `antiPatterns` — REVIEW (inferred): using an interactive card style for non-interactive content (use basic-non-interactive)

**Confirmation**
- 🔴 `antiPatterns` — REVIEW (inferred): conveying success by the green icon alone — the heading text must state what happened (1.4.1).
- 🔴 `antiPatterns` — REVIEW (inferred): two primary (red) buttons — one primary action; secondaries are ghost.
- 🔴 `antiPatterns` — REVIEW (inferred): auto-dismissing the confirmation before the user has read/acted on it.
- 🔴 `antiPatterns` — REVIEW (inferred): rounding the panel or buttons — brand is square/angular.
- 🔴 `antiPatterns` — REVIEW (inferred): UPPERCASE heading or message — house type rule is sentence case.

**Countdown timer**
- 🔴 `antiPatterns` — REVIEW (inferred): conveying the countdown only via the ring graphic without an accessible/textual time value
- 🔴 `antiPatterns` — REVIEW (inferred): using a countdown to force an action with no way to extend the time

**Divider**
- 🔴 `antiPatterns` — REVIEW (inferred): overusing dividers where whitespace would group content adequately

**Dropdown**
- 🔴 `antiPatterns` — REVIEW (inferred): using a non-native dropdown without full combobox keyboard/ARIA support where native would be more robust

**Eyebrow**
- 🔴 `antiPatterns` — REVIEW (inferred): marking the eyebrow up as a heading (h1–h6) — it is supplementary; the real heading must own the level (1.3.1).
- 🔴 `antiPatterns` — REVIEW (inferred): using an accent/brand-red eyebrow on a light surface — 13px red on white fails 1.4.3 (text < 4.5:1); keep it text/secondary.
- 🔴 `antiPatterns` — REVIEW (inferred): writing a sentence in the eyebrow — it is a 1–3 word kicker, not a subtitle.

**Headers**
- 🔴 `antiPatterns` — REVIEW (inferred): using a display header where a section title suffices (visual-hierarchy inflation)

**Hero**
- 🔴 `antiPatterns` — REVIEW (inferred): autoplaying background video with sound / no pause control

**Icon button**
- 🔴 `antiPatterns` — REVIEW (inferred): using an icon button where a labelled Button is clearer (unfamiliar action)

**Loading indicator**
- 🔴 `antiPatterns` — REVIEW (inferred): using an indeterminate spinner where a determinate progress bar (known duration) would be clearer

**Modals**
- 🔴 `antiPatterns` — REVIEW (inferred): stacking multiple modals/dialogs at once

**Progress tracker**
- 🔴 `antiPatterns` — REVIEW (inferred): using a progress tracker for an unknown number of steps (use an indeterminate loading indicator instead)

**Slider**
- 🔴 `antiPatterns` — REVIEW (inferred): using a slider where precise numeric entry is required (pair with an input)

**Summary**
- 🔴 `antiPatterns` — REVIEW (inferred): using a <table> for a simple two-column name/value list — a description list (dl) is the correct structure.
- 🔴 `antiPatterns` — REVIEW (inferred): centre-aligning values — keep keys left / values right so amounts align on a common edge.
- 🔴 `antiPatterns` — REVIEW (inferred): conveying the total only by size — it must also read as 'Total' in the key (1.3.1).

**Tab-bar**
- 🔴 `antiPatterns` — REVIEW (inferred): using a tab bar for in-page section switching — that is the Tabs component; a tab bar is app-level navigation.
- 🔴 `antiPatterns` — REVIEW (inferred): signalling the current tab by colour alone — also swap to the filled glyph + set aria-current (1.4.1).
- 🔴 `antiPatterns` — REVIEW (inferred): more than ~5 destinations — targets get too narrow; move overflow into a Menu item.
- 🔴 `antiPatterns` — REVIEW (inferred): labels in UPPERCASE — house type rule is sentence case.
- 🔴 `antiPatterns` — REVIEW (inferred): applying the pills variant's rounding/elevation to the standard bar — those are fenced to the exploratory pills variant; the standard bar stays flat/angular.

## Other (65)

**Account card**
- 🔴 `tokens.$balance-type-finding` — REVIEW: the balance uses a display/amount type (30px / line-height 1.1 / tabular-nums / -0.01em) with NO dedicated typography token. The gap report flagged 'display/amount type + money-format' as missing — confirm the size/role and add a…
- 🔴 `relationships.commonPatterns` — tappable account row that opens account detail (REVIEW: interactive variant?)
- 🔴 `behaviour.passive` — REVIEW: drafted as a passive display card (no states). Decide whether an INTERACTIVE variant is needed (whole card tappable → account detail), which would add hover/pressed/focus like the Cards link variant + a focusable role.
- 🔴 `tokenValidation.$note` — REVIEW: this is a CANDIDATE from the gap report, not yet reconciled against a Figma component. If HSBC already has an account/balance card, bind to its node + tokens; if net-new, it needs design review + a Figma source.
- 🔴 `provenance.$note` — REVIEW: no Figma node yet — surfaced by knowledge/_PAYMENTS-JOURNEY-GAPS.md. Needs a design owner + Figma source before promotion from candidate to gated.

**Account selector**
- 🔴 `slots.accounts.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Action bar**
- 🔴 `provenance.$note` — REVIEW: no Figma node yet — surfaced by the journey gap report (the .c-actionbar hand-util) and Button.meta commonPatterns. Needs a design owner + Figma source before promotion from candidate to gated.
- 🔴 `slots.actions.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Alert**
- 🟡 `props.$status` — s142-D1 (Dave, 2026-08-10) class C4 -- bind:rag-map. status IS the RAG semantic. ADDRESS-INTENT recorded now (rag.<value> pattern, matching the account-card/stat-card precedent already in this repo) -- the colour spine is NOT yet DTCG-mi…

**Amount display**
- 🟡 `props.$status` — s158-D3 (Dave, 2026-08-12) ADDRESS RE-KEY, THE SYMMETRIC CLOSE -- the NEGATIVE seat now binds rag.error-ink, not rag.error. This closes the open item s158-D2 declared and handed to Dave: rag/error-ink is the CANONICAL rung for coloured m…
- 🔴 `tokens.$directional-out-of-scope` — REVIEW: directional gain/loss colour (data/delta/gain + data/delta/loss) is deliberately NOT bound here — colour is handled in the RAG/delta workstream and layers on as an opt-in modifier later. Contrast note kept for when it lands: dark…
- 🔴 `provenance.$note` — REVIEW: surfaced as a P1 foundation in reviews/ITINERARY-2026-07-14-apollo-component-library and by the account-card $balance-type-finding. Needs a design owner + Figma source before promotion from candidate to gated.

**Avatar**
- 🟡 `props.$status` — s142-D1 (Dave, 2026-08-10) class UNMAPPED -- bind. Surface enum selects a single mode-adaptive token directly (background.default self-resolves light/dark within the spine). ADDRESS-INTENT -- colour spine not yet DTCG-migrated, value lan…

**Banner**
- 🟡 `props.$status` — s142-D1 (Dave, 2026-08-10) class C4 -- bind:rag-map. status IS the RAG semantic. ADDRESS-INTENT recorded now -- the colour spine is NOT yet DTCG-migrated, the token VALUE lands at that migration. This prop's own $note names a background-…
- 🔴 `slots.actions.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Bar chart**
- 🔴 `slots.series.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Box plot**
- 🔴 `slots.categories.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.outliers.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Bullet chart**
- 🔴 `slots.rows.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.ranges.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Butterfly chart (horizontal)**
- 🔴 `slots.series.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Butterfly chart (vertical)**
- 🔴 `slots.series.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Button**
- 🟡 `props.$note` — default height 44px; 'Large' variant exists for primary (and likely all types) — confirm Large height.
- 🟡 `props.$status` — s142-D1 (Dave, 2026-08-10) class UNMAPPED -- bind. Surface enum selects a single mode-adaptive token directly (background.default self-resolves light/dark within the spine). ADDRESS-INTENT -- colour spine not yet DTCG-migrated, value lan…

**Candlestick chart**
- 🔴 `slots.sessions.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Cards**
- 🔴 `slots.content.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Combo chart**
- 🔴 `slots.series.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Confirmation**
- 🔴 `tokens.$icon-note` — success-solid glyph: the tick is a cutout, so it shows the page colour behind (white tick on light, dark tick on dark). REVIEW: confirm the dark-mode tick reads acceptably or add a backing.
- 🔴 `responsive.$desktop-todo` — REVIEW: a DESKTOP variant is still needed (wider / dialog-style layout, not full-bleed centred). Logged in _COMPONENT-GAPS.md (Dave, 2026-06-30).
- 🔴 `provenance.$note` — REVIEW: no Figma node yet — surfaced by the journey gap report. Needs a design owner + Figma source before promotion from candidate to gated.
- 🔴 `slots.actions.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Data grid**
- 🔴 `slots.columns.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.filters.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Divider**
- 🟡 `props.$status` — s142-D1 (Dave, 2026-08-10) class UNMAPPED -- bind. Surface enum selects a single mode-adaptive token directly (background.default self-resolves light/dark within the spine). ADDRESS-INTENT -- colour spine not yet DTCG-migrated, value lan…

**Donut chart**
- 🔴 `slots.slices.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Drawer**
- 🔴 `slots.actions.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Eyebrow**
- 🔴 `tokens.$type-finding` — REVIEW: uses 13px / line-height 1 / 500, sentence case, with NO dedicated 'eyebrow' type token — confirm the size/role or bind to a label type token if one exists.
- 🔴 `provenance.$note` — REVIEW: no Figma node yet — surfaced by the journey gap report (the .c-eyebrow hand-util). Needs a design owner + Figma source before promotion from candidate to gated.

**Histogram**
- 🔴 `slots.bins.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Input fields**
- 🟡 `dimensions.$description` — Geometry. BOXED captured from node 65570:211753 (2026-06-22): box padding 9px top / 11px bottom / 16px inline, 16px gap (prefix·value·icon), 1px form/border, ~46px standard height, Large ~+10px. UNDERLINE geometry below was INFERRED 2026…

**Line chart**
- 🔴 `slots.series.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Modal lightbox**
- 🔴 `slots.items.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Modals**
- 🔴 `build.a11y` — role=dialog + aria-modal + aria-labelledby + aria-describedby; focus moves in + Tab trapped within + Esc closes + focus returns to trigger; background inert; trigger disabled while open. Closes the meta's focus-trap REVIEW item.

**Pie chart**
- 🔴 `slots.slices.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Popover**
- 🔴 `slots.content.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Scatter plot**
- 🔴 `slots.series.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Slider**
- 🔴 `tokens.tick-marker (DEPRECATED)` — non-interactive (depricate)/border/on-light/neutral-6 (#767676) → REVIEW (rebind form/border/default | scrollbar/foreground — both #767676)

**Sparkline**
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Stacked area chart**
- 🔴 `slots.series.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)
- 🔴 `slots.data.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Stepper**
- 🔴 `slots.steps.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Summary**
- 🔴 `provenance.$note` — REVIEW: no Figma node yet — surfaced by the journey gap report (the .c-summary hand-util). Needs a design owner + Figma source before promotion from candidate to gated.

**Tab-bar**
- 🔴 `provenance.$note` — REVIEW: no Figma node yet — surfaced by the journey gap report (the .c-tabbar hand-util). Needs a design owner + Figma source before promotion from candidate to gated.
- 🔴 `slots.items.$status` — ruled s140-D2 (Dave, 2026-08-09, via SLOTS-DRAFT-REVIEW s140-v1 export)

**Toast**
- 🟡 `props.$status` — s142-D1 (Dave, 2026-08-10) class C4 -- bind:rag-map. status IS the RAG semantic. ADDRESS-INTENT recorded now -- value lands at the colour-spine migration. 'plain' OMITTED from the map: this prop's own $note says plain is statusless ('no …
