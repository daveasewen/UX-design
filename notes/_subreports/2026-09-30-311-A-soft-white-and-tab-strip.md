# #311 lane A — the soft white (s310-D7) and the tab strip (s310-D8), built, and one picture page for his eye

COUNTS: rulings built 2 of 2 (s310-D7, s310-D8), enacted 0 (both stay `ruled` until he has looked) · token source edits 3 files (semantic-colour, Common override, Supercharge override) · snippet source edits 4 (Tabs and Page-header contrast pairs; Filter-toolbar-bar and Dropdown chevron) · gate edits 1 (`_validate_token_tiers.py` alias) · canon.css by hand 0 · canon.css lines moved ~210 (dark ink #FFFFFF → #E1E1E1 on every text-bound seat; tabs-background gone from Supercharge and option blocks) · snippets projected 137 + 9 tranches · showroom pages 137 · picture page 1, 18 inline pictures, 4 calls (2 "does it stand", 1 Supercharge page call, page note) · state-contrast 137 of 137 swept (8 slices, CI fonts), 0 text failures, audit unchanged · chart receipts 27 of 27 re-driven twice, 7 contrast_series_min 17.404 → 13.309 · clone survey 167 steps at 77e3521d: 0 FAIL · 2 ⏱ (68 hit-area, 73 state-contrast full run: seat has a browser, each takes > 60 s; both run in full separately, advisory rc 0 and 0 text failures) · 3 ADVISORY (pre-existing 140, 150, 163) · tests 32/32 · evidence PASS · found and fixed on the way 1 (state-snap red) · found not fixed 5 · pushed no

machinery: 0 (drivers only, under notes/_lanes/311/A/)

## What landed

- **6faaca8d — both builds at the token source, regenerated in order.** s310-D7: `text/default` and `text/secondary` dark → `color/neutral/12` #E1E1E1 (cached followers `button/tertiary/label/default`, `button/quaternary/label/default` re-stamped). Common: `text/default` dark #E1E1E1; its `text/secondary` dark stays its own #9B9B9B (not the white the ruling softens; #E1E1E1 would brighten it — a reading, declared). Supercharge: `text/default` and `text/secondary` pinned to `color/warm/15` #F7F6F4 (its neutral/12 is warm/12 #CDC8C6), light restated #13110E. The two "literal-white" chevrons in the banking demo were `.chev{color:var(--icon)}` (icon/default, #FFFFFF in dark) in Filter-toolbar-bar and Dropdown; the ▾ is a text glyph, so it now takes `--text`. s310-D8: `tabs/background` → `surface/transparent` both modes; Tabs' contrast pairs re-point to `background/default`, `surface/section`, `surface/raised`; Page header's to `background/default`; `_validate_token_tiers.py` learns the alias. Regen: gen_canon_tokens → gen_snippet_tokens → gen_token_ramp → gen_canon_components → gen_theme_cascade → gen_showroom; dark-mode, icon-delta, text and indicator audits rebuilt. Gates at the seat: snippets 0, token tiers 0 strict, fork ban green, dark surfaces 0, coverage 0, all generator checks in sync.
- **b8240a7b — the picture page**, drivers, 18 pictures, facts, bloom scores.
- **d65d6478 — chart receipts re-driven** (canon.css hash), 27 fresh; state-contrast sweep merged, 0 text failures.
- **77e3521d — the clone survey's one red, fixed.** Step 52 `_validate_state_snap.py`: `tabs/inactive` stores the colour-only equivalent of text/default at α 0.70 over the page; with the ink at #E1E1E1 no mono rung snapped (mono/10 drift 17.7, mono/9 8.3, tol 8). Re-derived α 0.70 → 0.67 and dark rung mono/10 → mono/9 #9D9D9D (light drift 3.6, dark 2.3; 6.42:1). No snippet paints this token. Common's `tabs/inactive` dark restated white and now follows its text (#E1E1E1). Both on the page (section 02, "Found on the way") because the 0.70 was set with R-D23. Receipts re-driven again (hash only).

Page: `notes/_REVIEW-311-A-soft-white-and-tab-strip-2026-09-30-v1.html` (localStorage key `review-311-A-soft-white-and-tab-strip-v1`; verified at 1440 and 390: 18 images, 0 broken, no side scroll, no links to PNGs, Copy as text returns all four answers).

## Measured (after, banking demo, WCAG)

Mono/Console/Common text on the black tile 16.06 (was 21.00), on the grey ground #1F1F1F 12.60 (was 16.48), on the page #1A1A1A 13.31 (was 17.40); the demo's 60% secondary line 5.85 (was 7.37). No text pair under 4.5. Pure-white text elements on the demo: 138 → 0 (Mono/Console), 118 → 0 (Common). Supercharge unchanged: #F7F6F4 on #13110E 17.45. Pairs under their floor are all status marks, none moved by this build: Console/Supercharge red mark #B92F1E on ground/page 2.5–2.9; Common red #A8000B and blue #305A85 marks 2.1–2.9. Bloom model (`bloom_311A.txt`): text 2px 29.1 → 16.5 on the tile, 28.7 → 16.2 on the ground. Tab strip: transparent in every context; unselected label lowest 6.44 (light, #F0F0F0 ground), 7.18 in dark.

## Calls for Dave (on the page)

1. The soft white, built — does it stand? (Yes, it stands / Change it)
2. The tab strip, built — does it stand? (same)
3. Supercharge's dark page and section — **warm/4 #25211C (the recommendation)**, because it mirrors Mono (tile the darkest, page one step up) and tiles then separate on page and section (1.18:1, Mono 1.21); alternatives drawn: the generator fixed as it stands (#13110E = the tile, tiles vanish on page and section) and as is (#1A1A1A page, tiles already vanish on the #13110E section). Pictures only, scratch overrides; nothing built. warm/4 is also the s310-D5 interim pressed/active value (stated on the page). The banking demo is not affected: its page is the bento ground #2A2621.
4. Page note.

## Found, not fixed

1. `icon/default` dark is still #FFFFFF (the header search glass), now brighter than the text beside it; not in the ruling, stated on the page.
2. QR modules, filled rating star, neutral status, flat sparkline and similar seats bind text/default in their manifests, so they softened with the ink; intended by "it moves all dark text", named so nobody is surprised.
3. The survey's per-step 60 s timeout ⏱s steps 68 and 73 whenever the seat's browser is present (`seat_env.sh` sourced); the #310 wrap's survey showed ⊘ for both because Playwright was not importable there. Hit-area run alone: 163 s, advisory rc 0.
4. `_drive_chart_engine.py` still hard-codes `channel="chromium"` (used `outputs/310/A/drive_wrap.py` twice).
5. The `surface/digital-black` note's "SC dark page = warm/4" is stale either way until call 3 is answered.

## Files

- Token source: `knowledge/tokens/semantic-colour.json`, `knowledge/tokens/themes/apollo-legacy.overrides.json`, `knowledge/tokens/themes/apollo-supercharge.overrides.json`
- Snippets: `Tabs`, `Page-header-lockup`, `Filter-toolbar-bar`, `Dropdown` (`.reference.html`); gate `knowledge/_validate_token_tiers.py`
- Drivers: `notes/_lanes/311/A/render_311A.py` (ink|crop|tabs|scpage; before = canon.css at 6faaca8d~1 served to /dev/shm copies), `build_page.py`, `verify_page.py`, `bloom_311A.py`, `tabs-context.html`; facts `img/facts-*.json`
- Pre-push logs: `notes/_lanes/311/A/_prepush2-*.txt` (the survey at 77e3521d), `_prepush-2.txt` (the red at d65d6478), `_hitarea.txt`
- Scratch (uncommitted): `outputs/311/A/` (canon-before, sweep slices, probes, commit logs, three identical SC demo renders in `unused/`). Clones `/tmp/pp311a`, `/tmp/pp311a2` left in place (no rm at this seat).
