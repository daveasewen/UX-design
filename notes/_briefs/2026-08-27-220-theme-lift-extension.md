# #220 sub brief — extend the dark-mode caption-ground lift to ALL themes, aligned to neutral primitives

**Model: Opus. Dave's ruling (verbatim, 2026-08-27): "yes the other themes need an appropriate lift too, align with the neutral primitives please."** Inscribed as `s220-D1` by the conductor. The RULE is his; the per-theme VALUES you derive are PROPOSED to his eye.

## Context
Console is done: `CAPTION_GROUND_MINTS[("console","dark","darkgrey")] → color/neutral/5 #313131` (commit `7debc1a`, his pick #303030 → nearest primitive). Ladder report `notes/_subreports/2026-08-27-220-caption-dark-ladder.md`: mono and legacy carry the identical 1.00:1 dark-mode vanish; supercharge's caption ground is DARKER than its page (inverted). Rung report `notes/_subreports/2026-08-27-220-rung-enact.md` has the mint-site pattern. ⚠ Also from the rung lane's red flag (a): the shipped grey DEFAULT caption in console dark was nearly as invisible as the darkgrey option — Dave's "yes" extends the lift to *the other themes*; treat the console grey DEFAULT as in scope too (same vanish, same rule) but name it separately in the report so his eye can veto it alone.

## Mission
1. MEASURE first, per theme (mono · legacy · console · supercharge), dark mode: every caption-ground member the chord/defaults expose, resolved rgb vs the effective ground behind it (pageBg and bentoBg cases). Table before any edit.
2. For every member that vanishes (or inverts): select the NEUTRAL-RAMP PRIMITIVE (knowledge/tokens/colour.json — color/neutral/*, color/mono/* where the theme's ramp says so) whose lift off that theme's dark page best matches the console calibration (neutral/5 #313131 over #1A1A1A — ΔL* ≈ 10). State the target band you used and each candidate you rejected. ⛔ If a theme's ramp has NO suitable primitive, NAME the gap as ruling-shaped — never invent a value ([[feedback-measuring-tool-must-not-guess]]).
3. Enact dark-only at the same cause site (`CAPTION_GROUND_MINTS` in gen_bento_matrix_217.py, per-theme rows; extend gen_foundations_217.py's mode-flat refusal arm to the new rows). Light modes UNTOUCHED. ⛔ X6 UNTOUCHED: mono's access to the dark-caption CHORD (a light-mode option) is EXPRESSLY OPEN, s219-D3(3) — fixing mono's dark-MODE rendering must not grant or imply that chord; assert the verifier's X6 refusal arm still bites.
4. Regenerate + drive: matrix + foundations selftests, verify_bento_matrix/foundations per theme light+dark, mutation arms (all named-red, counts stated before/after).
5. Proof page `reviews/THEME-LIFT-2026-08-27-v1.html`: four themes × dark, BEFORE/AFTER, measured rgb + lift printed per card, the console grey-default case in its own labelled section (vetoable alone). Copied-from-artefact method; banked build sources under notes/_subreports/assets/ are the pattern.

## Fences
No git (conductor commits at the seam). No `_rulings.json`/`_state.json`/memory. No release paths. No light-mode or chord-grammar changes. No new tokens — the neutral ramp as it exists is the palette; a gap is reported, not filled. Regions: the two generators + their regenerated artefacts, the proof page, your filed report + assets.

## Pitfalls (Dave #165)
- Aligning to a primitive by HEX SIMILARITY instead of LIFT repeats the defect: the same grey lifts differently over different theme pages — measure lift, then pick.
- Supercharge's inversion means its "nearest" primitive may sit on the other side of its page value — the target is lift ABOVE the page, not proximity to console's pick.
- An alias repoint can strip a theme override silently — verify per-theme resolution after every mint.

## Report
FILE at `notes/_subreports/2026-08-27-220-theme-lift.md`: the measure-first table, per-theme pick + rejected candidates, COUNTS, RULING-SHAPED QUESTIONS (chiefly any ramp gap + the console grey-default veto), REPLAY-THESE. Chat stub ≤6 lines.
