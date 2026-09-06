# `#249` — W2 DEBT REVIEW: DP-08 and DP-18 analysed, three rendered options each, nothing landed

session: `#249` · 2026-09-06 · conductor (Fable) + 2 Fable lanes (DP18, DP08)
window: Dave out — "just analyse and come back with some proposals, and show me visually"
brief: chat, this session (Dave's words: "these three, just analyse … screens and diagrams are useful to me … its key that all these rules and principles work")

## VERDICT
DONE as analysis. Page `reviews/W2-DEBT-DP08-DP18-2026-09-06-v1.html` (263 KB, rendered at 1280, 0 page errors, eyeballed). Lane reports `notes/_subreports/2026-09-06-249-DP18-fit-analysis.md` (findings 9 · RSQ 4) and `…-DP08-status-surface-analysis.md` (findings 11 · RSQ 4). Evidence `outputs/w2-debt/` (gitignored). ⛔ Nothing in `knowledge/` touched; nothing ruled; no commit, no push.

COUNTS: findings `4` · ruling-shaped `6` (on the page § Decide) · UNPROVEN `3`

## Findings
1. 13 of the 16 W2 misses belong to waves not yet run (W3 3 · W4 5 · W5 5 · W6 1); 2 are debt in waves already run (DP-08 W1, DP-18 W2); DP-12/19/25 n/a. Token: DP-TEST-PLAN wave table + `notes/_dp-scores/w2.json`.
2. DP-08: tiles 4 and 6 are states (count-of-total, ratio-to-limit), no period delta possible; Undrawn sparkline = 12 points at y=23.0 (page L316). No option moves first-chart-y (710.6 in 7 renders). DP-20 already 5 carriers vs 3.
3. DP-18: two engines on one selector (`svg.dv-fit`), last writer pins viewBox 260; VFIT lacked FOUR y paths for line charts (polyline, circle, rect-mark centre, polygon-mark). Prototype in `__dvBehaviour`: 821×260 → 821×304, slack 44.1 → 0, 19/19 physics PASS, live resize returns.
4. Sandbox had no Playwright/chromium; installed to `~/.local` + `~/.cache/ms-playwright`, needs `LD_LIBRARY_PATH=/tmp/libs/usr/lib/aarch64-linux-gnu` (libXdamage extracted from a .deb, no root). Ephemeral — `/tmp` dies with the sandbox.

## RULING-SHAPED QUESTIONS
On the page § Decide (6): DP-08 surface A/B2/both/C · four-track row · DP-20 dominant · DP-18 fit home a/b/c · rail stretch · the two provisional constants.

## UNPROVEN / CLAIMED
- UNPROVEN dark theme + 820/1100 for DP-08 options · other 12 dataviz members + JS-off for DP-18 · the review page under the real HSBC face.
- Gauge at write: FILL 185,911 real, PAST the 150,929 advisory by 34,982; wall 200K. Wrap NOT run at this seat — owed when Dave returns and rules.

## Evidence
`reviews/W2-DEBT-DP08-DP18-2026-09-06-v1.html` · `outputs/w2-debt/{dp08,dp18}/` · `outputs/w2-debt/_page.tpl.html` + `_build_page.py` (rebuild) · `outputs/w2-debt/_review-full.png`
