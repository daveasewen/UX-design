# Review queue — confidence-tagged assertions

> Every assertion in the component metas that is **not** directly observed canon. Formalises the in-prose confidence convention (Graphify-borrow #1). 🔴 **review** = verify before trusting; 🟡 **inferred** = reasoned, lower urgency. `asserted` items (the default) are not listed. Generated — regenerate after editing metas: `python3 knowledge/_build_review_queue.py`. Vocabulary in `_CONFIDENCE.md`; machine detail in `_REVIEW-QUEUE.json`.

**Totals:** 81 items across 25 components — 75 🔴 review, 6 🟡 inferred. By category: token-rebind 29, anti-pattern 27, accessibility 21, other 4.

Most-flagged components: Badge (6), Countdown timer (5), Dropdown (5), Hero (5), List items (5), Tags (5), Accordion (4), Avatar (4).

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

## Accessibility — verify in code/with the a11y team (21)

**Accordion**
- 🔴 `accessibility.focus` — REVIEW: the Figma component set defines default/hover/pressed but no explicit focus-visible state — confirm a visible focus indicator exists in code

**Avatar**
- 🔴 `accessibility.screenReader` — REVIEW (inferred): image/icon avatars need an accessible name (e.g. the person's name) or be marked decorative if adjacent text already names them

**Badge**
- 🔴 `accessibility.role` — REVIEW: badge is a decorative/status adornment on a host element; the host element (link/button/icon) is the focusable control
- 🔴 `accessibility.screenReader` — REVIEW (inferred): a colour dot alone is not accessible — expose the meaning in text (e.g. 'Inbox, 1 new message'); for the number version, ensure the count is announced. Confirm how this is implemented in code.

**Breadcrumbs**
- 🔴 `accessibility.structure` — REVIEW (inferred): mark up as a nav landmark labelled 'Breadcrumb' with an ordered list; current page exposed via aria-current='page' (matches the 'no-link' state)

**Cards**
- 🔴 `accessibility.interactive` — REVIEW (inferred): an interactive card should be a single focusable control (or have one clear primary link); avoid nested interactive elements that create multiple tab stops with unclear order

**Countdown timer**
- 🔴 `accessibility.announce` — REVIEW (inferred): expose remaining time to assistive tech (e.g. role=timer / polite aria-live updates at sensible intervals) — don't rely on the depleting ring alone
- 🔴 `accessibility.timingAdjustable` — REVIEW (inferred): where the countdown triggers an action (e.g. session timeout), provide a way to extend/turn off/adjust the limit (WCAG 2.2.1)
- 🔴 `accessibility.motion` — REVIEW (inferred): respect prefers-reduced-motion for the animated ring

**Divider**
- 🔴 `accessibility.semantics` — REVIEW (inferred): decorative dividers should be hidden from assistive tech; if a divider conveys a meaningful grouping boundary, expose it as a separator (role=separator)

**Dropdown**
- 🔴 `accessibility.keyboard` — REVIEW (inferred): full keyboard operation — open/close, arrow navigation, type-ahead, Enter/Escape; native family inherits browser behaviour
- 🔴 `accessibility.roles` — REVIEW (inferred): non-native must implement combobox/listbox semantics (aria-expanded, aria-activedescendant, option roles, aria-selected); prefer native where possible for robustness

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

## Anti-patterns — confirm or promote to asserted (27)

**Accordion**
- 🔴 `antiPatterns` — REVIEW (inferred): hiding required or critical information inside a collapsed panel
- 🔴 `antiPatterns` — REVIEW (inferred): deeply nesting accordions within accordions
- 🔴 `antiPatterns` — REVIEW (inferred): hard-coding the header text colour or rule colour instead of binding text/default and border/subtle tokens

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

**Countdown timer**
- 🔴 `antiPatterns` — REVIEW (inferred): conveying the countdown only via the ring graphic without an accessible/textual time value
- 🔴 `antiPatterns` — REVIEW (inferred): using a countdown to force an action with no way to extend the time

**Divider**
- 🔴 `antiPatterns` — REVIEW (inferred): overusing dividers where whitespace would group content adequately

**Dropdown**
- 🔴 `antiPatterns` — REVIEW (inferred): using a non-native dropdown without full combobox keyboard/ARIA support where native would be more robust

**Headers**
- 🔴 `antiPatterns` — REVIEW (inferred): using a display header where a section title suffices (visual-hierarchy inflation)

**Hero**
- 🔴 `antiPatterns` — REVIEW (inferred): autoplaying background video with sound / no pause control

**Loading indicator**
- 🔴 `antiPatterns` — REVIEW (inferred): using an indeterminate spinner where a determinate progress bar (known duration) would be clearer

**Modals**
- 🔴 `antiPatterns` — REVIEW (inferred): stacking multiple modals/dialogs at once

**Progress tracker**
- 🔴 `antiPatterns` — REVIEW (inferred): using a progress tracker for an unknown number of steps (use an indeterminate loading indicator instead)

**Slider**
- 🔴 `antiPatterns` — REVIEW (inferred): using a slider where precise numeric entry is required (pair with an input)

## Other (4)

**Button**
- 🟡 `props.$note` — default height 44px; 'Large' variant exists for primary (and likely all types) — confirm Large height.

**Input fields**
- 🟡 `dimensions.$description` — Geometry. BOXED captured from node 65570:211753 (2026-06-22): box padding 9px top / 11px bottom / 16px inline, 16px gap (prefix·value·icon), 1px form/border, ~46px standard height, Large ~+10px. UNDERLINE geometry below was INFERRED 2026…

**Modals**
- 🔴 `build.a11y` — role=dialog + aria-modal + aria-labelledby + aria-describedby; focus moves in + Tab trapped within + Esc closes + focus returns to trigger; background inert; trigger disabled while open. Closes the meta's focus-trap REVIEW item.

**Slider**
- 🔴 `tokens.tick-marker (DEPRECATED)` — non-interactive (depricate)/border/on-light/neutral-6 (#767676) → REVIEW (rebind form/border/default | scrollbar/foreground — both #767676)
