# #310 lane B — the interim pressed value, and one review page: the white ink and the tab strip

COUNTS: rulings enacted 1 of 1 (s310-D5 at 896b2b0e) · token source edits 1 file (Supercharge override, 2 paths) · canon.css by hand 0 · canon.css lines moved 28 (Supercharge dark pressed/active + the component-tier literals that bake them) · showroom pages 12 · snippets projected 0 · review page 1, 19 inline pictures, 2 calls + page note · ink options shown 5 · tab contexts 4 × 2 readings × (Console light, Console dark, Supercharge dark) + 2 real templates · state-contrast 137 of 137 swept, 0 text failures, audit unchanged · chart receipts 27 of 27 re-driven, 0 measurements moved · clone survey 167 steps: 155 pass · 0 FAIL · 0 timed out · 3 ADVISORY (pre-existing: 140, 150, 163) · 9 COULD-NOT-ASK (environment) · tests 32/32 · evidence PASS · calls for Dave 2 · found not fixed 5 · pushed no

machinery: 0 (drivers only, under notes/_lanes/310/B/)

## What landed

- **896b2b0e — s310-D5 built.** `knowledge/tokens/themes/apollo-supercharge.overrides.json` gains `tertiary/background/pressed` and `tertiary/background/active`: dark `color/warm/4` #25211C (was #13110E via neutral/4 → warm/2, equal to the s310-D4 rest tile); light restates what Supercharge rendered (#493F39, #000000), because a per-mode override falls back to the Mono base. Each `$note` carries his words verbatim and says INTERIM pending his Figma specs; the s310-D4 note now points at them. Regen in order: gen_canon_tokens → gen_snippet_tokens (0) → gen_token_ramp (0) → gen_canon_components (no change) → gen_theme_cascade → gen_showroom (12). Dark-mode and icon-delta audits unchanged. Measured after: rest #13110E, hover #2E2A25, pressed #25211C, active #25211C, page #1A1A1A.
- **9a0ebe86 — the review page**, drivers, pictures, and s310-D5 stamped enacted (`_inscribe_ruling.py --set-status … --write`, reconstruction proof passed).
- **10821801 — `notes/_RULINGS.html` re-rendered** (s263-D10 freshness after the stamp).
- **7e4602db — chart receipts re-driven** (canon.css changed, so the clone survey's step 102 read all 27 as stale; re-driven via `outputs/310/A/drive_wrap.py`, only the pinned canon.css hash and the timestamp moved) and **`_node_titles.json` regenerated** (step 88: the two rulings inscribed at 93cdb12a had no titles, 845 → 847; not this lane's change but in the path of green).

Review page: `notes/_REVIEW-310-B-white-ink-and-tab-strip-2026-09-30-v1.html` (19 inline pictures, no links to PNGs; verified at 1440 and 390: 0 broken, no side scroll, Copy as text returns all three answers; localStorage key `review-310-B-white-ink-and-tab-strip-v1`).

## Calls for Dave (on the page, each with a recommendation)

1. **The white ink on black tiles.** Measured on the banking demo, Console dark (main text / secondary 60% text, on the tile): as built #FFF 21.00 / 7.37; #F0F0F0 18.43 / 6.58; **#E1E1E1 16.06 / 5.85**; the reverse (grey tiles) 16.48 / 6.69 but the page ground turns #000 so header text is 21:1 and the red status dot is 2.74:1 on the tile; a #0F0F0F tile 19.17 / 7.24 with tile/ground separation down from 1.27 to 1.16. Recommend **#E1E1E1 (neutral/12) on black**, because it keeps his black tiles and brings the edge under the digital-black note's own 17.4:1 with every secondary line still passing; Supercharge keeps its existing #F7F6F4 (17.45:1 on its tile) rather than follow to warm/12 (11.37:1). Building it is `text/default` + `text/secondary` dark → `color/neutral/12` plus a Supercharge pin at warm/15; it moves all dark text (ground text 16.48 → 12.60).
2. **The tab strip.** `tabs/background` aliases `surface/raised`, painted by `.cn-tabs`, `.cn-page-header-lockup` and `.cn-template-detail`. It bands wherever the strip sits on anything but a tile, **in light too**: white strip on #F0F0F0 bento and section grounds; light looked right only because its page is also white. Recommend **the strip takes its container's colour in both modes** (`tabs/background` → `surface/transparent`), because then it never draws a band and light and dark read the same. The third reading (band only when the panel differs) collapses into the second for every composition found, so it is argued, not shown. Build note: the Tabs manifest's contrast pairs are against `tabs/background`; they must be measured against the ground once transparent (tab label at 72% on #F0F0F0 = 6.44:1).

## Desk research (dated 2026-09-30, in the page's Technical fold)

Material Design dark theme codelab (Google): #121212 surfaces, pure white "appears to bleed or blur", text at 87/60/38%. Level Access, "Accessibility for people with astigmatism": ~half the population ≥0.5 D; "avoid using white text on pure black backgrounds"; checkers do not flag it. a11ywithdiana (Substack): halation stronger with astigmatism, small type, dim rooms; suggests #EAEAEA on #121212 etc. Counterpoint named from a search listing only, not re-read: Apple's dark mode uses a true black base.

## Found, not fixed

1. **Supercharge dark: tiles vanish on a section background.** `surface/section` (neutral/4 → warm/2) and the s310-D4 tile are both #13110E (page picture, Supercharge pair, context d). Sits with lane A's found-not-fixed 1 (SC dark page frozen at #1A1A1A).
2. Two dropdown chevrons in the banking demo paint a literal white; they would not follow a softer ink.
3. With the grey-tiles option on, the avatar disc (tertiary hover #232323) is 1.03:1 on the #1F1F1F tile.
4. The state-contrast sweep takes ~2 min per slice at this seat, not the runbook's ~4.5 min for all eight; run three or four slices in parallel per call (done here).
5. `_state.py` has no command to add a report row; rows are hand-inserted into `_state.json` (lane A did the same).

## Files

- Token source: `knowledge/tokens/themes/apollo-supercharge.overrides.json`
- Drivers: `notes/_lanes/310/B/render_states.py`, `render_ink.py`, `render_tabs.py`, `render_real.py`, `probe_inks.py`, `build_page.py`, `states.html`, `tabs-context.html`; facts `img/ink-facts.json`, `img/tabs-facts.json`
- Scratch (uncommitted): `outputs/310/B/` (before canon.css, probes, sweep slices, verify screenshots)
