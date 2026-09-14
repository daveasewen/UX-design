# #271 HARVEST LANE — when-to-use rules for the WHOLE library, from external systems

**Dave's ask, verbatim (post-#270-wrap, `notes/_lanes/270/DAVE-RULINGS-2026-09-14.md`):**
> "can we harvest all of these for the library seeing as we don't have access to anything meaningful from the company, I can then select the rules to confirm that are not unanimous"

**GO on his word.** #271 opener: "Go".

## What the lane produces (per slice)
1. `notes/_lanes/271/harvest/<slice>/SOURCES.json` — same shape as `notes/_lanes/270/when-research/SOURCES.json` (`ours` / `external` / `refused`). Every external entry = `sys`, `url`, `quote` (VERBATIM, < 15 words), `disc` (what the quote discriminates, `a-vs-b`), `component` (our meta stem).
2. `notes/_lanes/271/harvest/<slice>/PROPOSED-WHEN.json` — same shape as `notes/_lanes/270/when-research/PROPOSED-WHEN.json`: per component `when_gate` (machine-checkable clause), `when_prose` (beats/yields sentence, s253-D1), `confidence` from the same 4-word scale (`canon` / `consensus-external` / `single-external` / `none`), `sources`, `disagreements`, `daves_call`.
3. `notes/_lanes/271/harvest/<slice>/DECISION-TABLE.json` — ONLY the non-unanimous rules: one row per rule, columns = each system's position (verbatim quote or `silent`), plus `options` for Dave (2–4, each one sentence) and a `recommendation` LABELLED as the lane's.
4. `notes/_lanes/271/harvest/<slice>/RECEIPT.md` — counts: components covered / rules found / unanimous / non-unanimous / none; systems consulted; fetch failures named.

## Rules
- READ-ONLY on canon. Touch NOTHING under `knowledge/` — no meta, no schema, no roles.json, no rules index. Write only under `notes/_lanes/271/harvest/<slice>/`.
- `knowledge/_RUNBOOK-external-claims.md` governs: every external claim carries source + quote, marked EXTERNAL, never presented as ours.
- Quotes VERBATIM from the fetched page, < 15 words, one per source per rule. Paraphrase is not a quote.
- "Unanimous" = every consulted system that SPEAKS on the rule says the same KIND of thing (silence is not disagreement; record silence). Where the KIND agrees and the NUMBER differs (the #270 radio→dropdown finding: Polaris 4 · M3 5 · Ant 5 · Spectrum 6 · USWDS 7), that is NON-unanimous — a decision-table row.
- Already-ruled: `s270-D1` = single-select cut-off 5 (radio ≤ 4, dropdown ≥ 5, provisional). Do NOT re-litigate; cite it as `canon`. Record-list `when`s exist in `knowledge/roles.json` — `canon`. #270's selection/record-list proposals exist in `notes/_lanes/270/when-research/PROPOSED-WHEN.json` — do not redo them; reference and extend.
- Systems to consult (at minimum, in this order): GOV.UK Design System, USWDS, Material 3, Carbon (IBM), Polaris (Shopify), Spectrum (Adobe), Atlassian, Ant Design, Fluent 2, Apple HIG, NN/g articles. Fetch the component's own page; if a fetch fails, name it in `refused` and move on — never guess the text.
- Our own prose first: read each component's meta (`knowledge/components/<stem>.meta.json` — `purpose`, `when`, `relationships`, `antiPatterns`) so the external rule is matched to OUR discriminator, not a generic one.
- NEVER INVENT ATOMS: every `component` value is an existing meta stem. If a system has a component we don't, record it under `external` with `component: null` and a note — it is a finding, not a proposal.
- Budget: you are one Opus lane. Stay bounded — depth over breadth is WRONG here, Dave wants COVERAGE. If you cannot cover every component in your slice, cover every ROLE's main discriminators first and name what was skipped in RECEIPT.md. A declared gap passes; a silent one fails.
- Final message back to the conductor: the four file paths + the RECEIPT counts + the three most contested rules in one line each. Nothing else.

## Slices (one lane each)
- **A — input + action + feedback + overlay**: selection-controls, dropdown, combobox, multi-select, segmented-control, cascader, input-fields, textarea, amount-input, search-field, date-picker, date-range-picker, time-picker, calendar, file-upload, range-slider, slider, rating, tags-input, transfer-list, secure-entry, form-layout, stepper, reorder · button, icon-button, split-button, fab, action-bar, quick-actions, links, cta-lockup · alert, banner, toast, notifications, confirmation, popconfirm, empty-state, loading-indicator, skeleton-loader, progress-bar, progress-tracker, countdown-timer · modals, modal-lightbox, drawer, popover, tooltip, command-palette.
- **B — record-list + chart-panel + headline-metric + status-surface**: table, data-grid, list-items, cards, document-row, transaction-row, standing-order-mandate-row, account-card, timeline, tree, accordion, carousel, pagination, filter-toolbar-bar, view-options, legend · chart-bar, chart-line, chart-combo, chart-donut, chart-pie, chart-sparkline, chart-stacked-area, Chart-boxplot, Chart-bullet, Chart-butterfly-h, Chart-butterfly-v, Chart-candlestick, Chart-histogram, Chart-scatter · stat-card, kpi-tile, summary, meter, limits-meter, runway-bar, amount-display, stats-band-lockup · badge, tags, status-indicator, avatar, avatar-group, payment-card-visual, qr-code.
- **C — page-frame + page-title + wayfinding + arrangement**: app-shell-* (7), headers, footer, footer-doormat-lockup, hero, hero-variants, template-* (13) · page-header-lockup, section-heading-lockup, card-header-lockup, eyebrow, feature-grid-lockup · navigations, sidebar-nav, tab-bar, tabs, breadcrumbs, anchor-nav, back-to-top, account-selector · layout-utilities, divider, splitter, image-block, video-player, headers.
