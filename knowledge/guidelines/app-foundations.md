# App foundations — platform guidance (ingested)

*Source: create.hsbc → Platforms and channels → App → App foundations
(`platforms-and-channels/app/app-foundations/` — three subpages: type_scale, dark-mode,
elevation), captured 2026-07-02 via Dave's authenticated session (login-walled; ADR-0005
clearance applies — agency machine). Engine-era format. Raw snapshots:
`guidelines/_sources/app-foundations/`. Two of the three pages are word-for-word mirrors
of the web pages — recorded as mirrors, not re-encoded.*

## Scope note

The app channel's foundation layer is thin by design: dark mode and elevation are shared
with web (mirrored pages), and the type scale collapses the web's three TScales to a
single scale. The genuinely app-specific content is the iOS Dynamic Type requirement
(appf-002) and the single-scale simplification (appf-001). The app hub also lists Design
toolkits and Legacy standards — toolkit destinations, not ingestable standards.

## App type scale

- **One scale, no TScale variants.** Seven sizes anchored on the 16px baseline; the
  values are IDENTICAL to the web's TScale:1 column (S1 33/40/20 · S2 28/36/18 ·
  S3 23/30/15 · S4 19/27/14 · S5 16/24/12 · S6 14/20/10 · S7 12/16/8 — font/leading/
  paragraph px). The store's font-5..7 match ✓ (same receipt as webf-024); app never
  needs the scale-2/3 mode values. [structure — the webf-033 export-gap check matters
  for WEB targets only] {#appf-001}
- **iOS: use Dynamic Type and test that the layout adapts to ALL accessibility font
  sizes, including the largest.** [BLOCKING-derivable for app-target generation — the
  platform analogue of WCAG 1.4.4 resize-text; our web gates don't cover it; becomes a
  criteria-pack item if/when an app target exists] {#appf-002}
- **Titles/section headers/subtitles use S4 and above (≥19px)**; page titles/subtitles in
  light + regular weight; subtitle sizes divide sections. (Web says "S sizes from the
  scale... 19px and above" — same rule, cleaner statement here.) [ADVISORY-derivable —
  same type-role check as webf-025] {#appf-003}
- **Brand font: "Univers Next for HSBC, whenever possible."** [receipt — store's
  `typography/font-family/default` matches; another nail in dissolved type26-001]
  {#appf-004}

## Dark mode (mobile app) — MIRROR

- Word-for-word identical to the web dark-mode page (same 18 April 2021 date; only the
  title differs). **webf-001 through webf-010 apply to the app channel verbatim** — do
  not maintain duplicate rules; cite the webf IDs for app work. [structure — mirror
  recorded in `_sources/app-foundations/dark-mode-MIRROR.txt`] {#appf-005}

## Elevation — MIRROR

- Word-for-word identical to the web Elevation page, including the "browser tooltips"
  example (the copy-paste tell). **webf-011 through webf-016 apply to the app channel
  verbatim.** Level taxonomy, shadow/overlay split, and scroll-trigger behaviours are
  channel-invariant. [structure — mirror recorded in
  `_sources/app-foundations/elevation-MIRROR.txt`] {#appf-006}

## Findings

1. **The app layer is mostly channel-invariant** — HSBC publishes shared foundations with
   a thinner app specialisation (one type scale, Dynamic Type, nothing else app-only).
   Engine consequence: our web-first canon is closer to app-ready than the channel split
   implies; an app criteria pack = canon + appf-002 + app grid values (which exist in
   `layout.json`: app margin/gutter 16/16 from the toolkit export — NOT published on
   these pages; toolkit is the operative source, same stance as the grey ramp).
   [structure note] {#appf-007}
2. **No app-specific grid/spacing/forms pages exist under app foundations.** Web has six
   foundation subpages, app has three. App grid values live only in the toolkit export.
   ⚠ Source gap kin of webf-017 — if an app project lands, the Common Toolkit access
   decision covers this too. [REVIEW — fold into the webf-017 Common Toolkit decision;
   no separate action] {#appf-008}

## Cross-references

`web-foundations.md` (webf-001..016 apply verbatim via appf-005/006; type table
webf-024) · `tokens/layout.json` (app margin/gutter 16/16, toolkit-sourced) ·
`tokens/typography.json` (S5–S7 receipt) · `typography-standards-2026.md` (type26-001
dissolved — appf-004 is another receipt) · webf-017 (Common Toolkit access decision,
now covering app element/pattern standards too).
