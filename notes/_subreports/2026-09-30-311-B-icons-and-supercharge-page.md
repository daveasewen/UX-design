# #311 lane B — the icons follow the ink (s311-D1) and Supercharge's dark page and section take warm/4 (s311-D2), built, and one look page for his eye

COUNTS: rulings built 2 of 2 (s311-D1, s311-D2), enacted 0 (both stay `ruled` until he has looked) · token source edits 2 files (semantic-colour: icon/default dark + the digital-black note; Supercharge override set: icon/default, background/default, surface/section) · generator edits 1 (`gen_theme_cascade.py` `_expand_aliases` unlock + selftest 4f, mutation-tested) · canon.css by hand 0 · canon.css lines moved 168 (1 base dark `--icon-default`, 167 Supercharge dark page seats) · Mono/Console/Common/SC-light/option blocks moved 0 · snippets re-projected 68 + 9 tranches · showroom pages 137 · pure-white icons on the banking demo, dark: Mono 2 → 0, Console 2 → 0, Common 2 → 0, Supercharge 0 → 0 · SC tile on page 1.08 → 1.18, on section 1.00 → 1.18, text on page 16.11 → 14.81 · look page 1, 5 pictures, 3 calls (2 "does it stand", page note) · state-contrast 137 of 137 swept (8 slices, CI fonts), 0 text failures, audit unchanged · chart receipts 27 of 27 fresh (13 hashes moved, no figure) · pre-push clone survey NOT RUN (root disk full, see below) · pushed no

machinery: 1 (the generator's unlock probe in `gen_theme_cascade.py --selftest`)

## What landed

- **76ac038e — both builds at the source, regenerated in order.** s311-D1: `icon/default` dark aliases `color/neutral/12` #E1E1E1 (was neutral/15 #FFFFFF). Supercharge pins `icon/default` to warm/15 #F7F6F4 (light restated warm/2 #13110E), because its DNA tier would have rebound neutral/12 to warm/12 #CDC8C6. Not moved, by scope: `icon/default-reverse`, `icon/on-inverse`, `--pri-icon`/`--pri-glyph`, Common's `button/primary/icon/default`, and the hard-coded dark RAG roundel `.ic{color:#FFFFFF}` rules (nine components; the 2026-07-02 white-shape-black-mark policy). s311-D2: `_expand_aliases` skipped every path already in `ov`, so `background/default` (written in pass 1 via its light target) kept the Mono dark base #1A1A1A before `surface/digital-black` expanded; it now skips only the theme's own overrides and re-derives to the fixed point. Alone, that gives SC's page #13110E (the tile). The ruling: SC `background/default` and `surface/section` dark → `color/warm/4` #25211C (light restated warm/15 #F7F6F4, warm/13 #DFDEDC). `surface/digital-black`'s stale "SC dark page = warm/4" corrected. Selftest 4f checks both values and an unlock probe; with the old line put back it fails. Regen: gen_canon_tokens → gen_snippet_tokens → gen_token_ramp → gen_canon_components → gen_theme_cascade → gen_showroom; dark-mode, text/icon, indicator audits and icon delta rebuilt. Gates at the seat: snippets 0, token tiers 0 strict, state-snap OK, dark surfaces 0, forks green, coverage 0, every generator --check in sync.
- **39852610 — chart receipts re-driven** in three `--page` batches (one run exceeds a seat call); 13 canon.css hashes moved, no contrast figure; `--receipts-fresh` 27/27.
- **3a3d800e — the look page**, drivers, composition, five pictures, facts.

## canon.css, per theme (compared line by line with 84bd8c93)

Base dark: `--icon-default` #FFFFFF → #E1E1E1 (Mono, Console, Common inherit it). Supercharge dark: `--background-default`, `--surface-section` → #25211C; `--page` ×135, `--menu-surface` ×10, `--cell` ×6, `--surface` ×4, `--nav-page` ×3, `--tbl-cell` ×2, `--panel`, `--pane`, `--stack-ring`, `--qr-plate-theme` #1A1A1A → #25211C; Template-dashboard-bento `--wall-ground` #13110E → #25211C. Nothing else.

## Measured

Glass on the header search bar (black) 21.00 → 16.06, on the toolbar field (#1A1A1A) 17.40 → 13.31, equal to the text beside it. Supercharge after: page and section #25211C, tile #13110E, header band #13110E, tile on page 1.18, tile on section 1.18, text on page 14.81, text on tile 17.45. The icon contrast delta (advisory, every icon × every surface) reads 44 exhaustive combos under 4.5 (was 46); declared dead-zone 0.

## Page

`notes/_REVIEW-311-B-icons-and-supercharge-page-2026-09-30-v1.html` (key `review-311-B-icons-and-supercharge-page-v1`). 01 the icons: Console dark before/after with the header search bar open, a 4x crop of both glasses beside their words, one line for Mono and Common. 02 Supercharge's dark page: `notes/_lanes/311/B/sc-page.html` (the demo's masthead, page header and metric tiles, verbatim, real canon.css, no overrides) before/after, tiles on the page and on a section. Verified at 1440 and 390: 5 images, 0 broken, no side scroll, Copy as text returns all three answers.

## Pre-push check (s309-D7) — NOT RUN

The clone could not be made: `/` has 0 bytes free (9.6G used). Lane A's two clones `/tmp/pp311a` and `/tmp/pp311a2` (1.3G each) and this lane's failed partial clone `/tmp/pp311b` (1.1G) hold it; the brief forbids `rm`, so they stand. `/sessions` (the seat home) has ~124M left. Deleting the three clones frees ~3.7G; then the survey (four chunks with `--include-mutating`, tests, evidence) can run on 3a3d800e. What did run at the seat: every generator check, the gates listed above, the state-contrast sweep, chart receipts.

## Found, not fixed

1. The banking demo's two masthead buttons (search, account) lack `.nv-btn`, so their SVGs are 0×0 and they draw as small light UA boxes in dark, before and after. Pictured on the page.
2. The dark RAG roundel rules paint pure white by policy (Notifications, Input fields, Amount input, Combobox, Date picker, Date range picker, File upload, Form layout, Multi-select). Status icons, left; named on the page for his word.
3. Supercharge's header band (`--nav-surface`) stays #13110E, now a step darker than the page.
4. With `data-dark-tiles="grey"` in Supercharge the tiles are #2A2621 on the #25211C page, 1.06:1.
5. Everything projecting `background/default` in SC dark moved with the page (menus, cells, field boxes, QR plate); on the demo the payments search box is #25211C on the #13110E tile.
6. The disk: see above.

## Files

Token source `knowledge/tokens/semantic-colour.json`, `knowledge/tokens/themes/apollo-supercharge.overrides.json`; generator `knowledge/canon/gen_theme_cascade.py`; drivers `notes/_lanes/311/B/render_311B.py` (count|icons|scpage; before = canon.css at 84bd8c93 served to /dev/shm copies), `probe_icons.py`, `build_page.py`, `verify_page.py`, `sc-page.html`; facts `img/facts-*.json`. Scratch (uncommitted): `outputs/311/B/` (canon-before, sweep slices, drive logs, commit logs, the mutant generator).
