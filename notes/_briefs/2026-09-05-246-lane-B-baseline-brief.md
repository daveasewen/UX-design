# #246 lane B brief — BASELINE: the demo prompt, run cold, BLIND then SIGHTED

**Model: Fable. Conductor: Fable (#246). Dated period record (ADR-0017). Read-only against canon/knowledge — this lane MOVES NOTHING in the library and RULES NOTHING.**

## WHY (Dave, 2026-09-05, his words)

> "I have a meeting with a senior stakeholder soon, maybe 2 weeks time, I need to show good results from one prompt rather than coaxing good results out of Apollo. The initial results need to be visually, and interactively richer, fuller and more persistent to impress the SH."
> "The retrieval seems to rely on very basic components … the charts are only partially retrieved, the interactions, controls and animations are always missed the first time round."
> "we do not have vision in VS, and we cant install playwright … I'm sure this is affecting results."

This lane produces the BEFORE picture. Nothing is fixed here; what is measured here is what #247+ fixes.

## THE PROMPT (verbatim, FROZEN — do not improve it)

```
/generate-from-canon build me a financial dashboard for corporate international banking. Please make the all the interactive elements work such as filtering and navigation.
```

Dave's note: the second sentence was appended in VS because earlier builds missed interactivity. Keep it. Record separately, in findings, what you judge sentence 1 alone would have produced — a judgement, labelled as one, not a third arm.

## TWO ARMS, SAME PROMPT, IN THIS ORDER

### Arm A — BLIND (the VS Code condition)
Simulate a Copilot session that has ONLY the pack surfaces and no eyes:
- You may read: `apollo-spider/skills/generate-from-canon/SKILL.md`, `apollo-spider/skills/grill-me/SKILL.md`, `showroom/index.json`, `knowledge/components/*.meta.json`, `knowledge/snippets/*.reference.html`, `knowledge/canon/*.css`, `knowledge/guidelines/`, `knowledge/tokens/`, `knowledge/assets/icons/`.
- You may NOT read `notes/`, `_CHAIN.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md`, `reviews/`, `_DECISION-HISTORY/`, `knowledge/_rulings.json`, or any `_*.py`. No `_memento_search.py`.
- NO render, NO screenshot, NO gate, NO playwright, NO validator during the build. You build blind and stop when the skill says you are done.
- `briefs/` does not exist ⇒ grill-me fires. Do NOT ask Dave. Answer the six standard questions with the skill's own declared defaults, write each as *skipped/defaulted* into `outputs/baseline-246/brief.md`, and proceed. Theme: whichever the skill defaults to — say which.
- Follow the skill HONESTLY, as a capable model would in VS: read files the way you naturally would, copy what the skill tells you to copy. Do not game it in either direction. Keep a log `outputs/baseline-246/arm-A-blind/READ-LOG.md` of every file you opened, how much of it you read (lines/bytes), and what you copied vs re-drew.
- Output: `outputs/baseline-246/arm-A-blind/dashboard.html` (single file, self-contained, per the skill's output rules) + the Gaps list the skill requires.

### Arm B — SIGHTED (the sandbox condition)
Same prompt, same rules on what you may read, but now with eyes and the gate: after a first build you may render (playwright), look, run `knowledge/_validate_screen.py` and `knowledge/_validate_receipt.py`, and iterate — ⛔ **cap 3 iterations**, each logged (what the render/gate showed, what you changed). The point is to measure how much sight buys, not to produce a perfect page.
- Output: `outputs/baseline-246/arm-B-sighted/dashboard.html` + `ITERATION-LOG.md`.

Playwright is NOT installed in a fresh sandbox — runbook: `knowledge/_ROBUSTNESS-PORTABILITY.md` (chromium-headless-shell + `libXdamage` user-space fix). Price it; ~4 calls.

## MEASURE BOTH ARMS THE SAME WAY (after Arm A is frozen — never go back and touch A)

For each arm, at 1440 and 820, light and dark, in the arm's theme:
1. **Render** → PNGs in the arm folder.
2. **Gates** → `_validate_screen.py`, `_validate_receipt.py`: exit codes + first 20 lines each.
3. **Inventory** → components used (slug, level), count by level; which dashboard-set components were AVAILABLE but NOT used (kpi-tile, stat-card, chart-*, data-grid, runway-bar, limits-meter, quick-actions, filter-toolbar-bar, page-header-lockup, stats-band-lockup, template-dashboard-bento, sidebar-nav / app-shell-*).
4. **Chart completeness** → for every chart on the page: is the snippet's `<script>` present byte-for-byte (sha256 vs the source snippet's script block)? controls present? animation present? legend/tooltip working when driven?
5. **Interactions driven** → with playwright, actually click: each nav item, each filter, each tab/segmented control, a data-grid sort. Record works / dead / missing. "Persistent" = does state survive (filter still applied after nav, tab remembered).
6. **Data believability** → is the content plausible corporate international banking (currencies, entities, FX, liquidity, payments) or placeholder?
7. **Richness score** → your judgement in one line each: visually rich / full / persistent / interactive — 0–3, with the one fact that earned the score.

## DELIVERABLES
- `outputs/baseline-246/` — both arms, renders, logs (repo-root `outputs/` is the review surface, not `notes/`).
- `reviews/BASELINE-246-2026-09-05-v1.html` — ONE page, swiss-design-system idiom (skill at `.claude/skills/swiss-design-system`), Dave reads this: the two renders side by side per breakpoint/mode, the inventory table, the chart-completeness table, the interaction table, the scores, and a **Findings** section: numbered, each finding = one fact + the file/line that proves it. End with **Ruling-shaped questions** for Dave (things only he can decide) — do NOT answer them.
- `notes/_subreports/2026-09-05-246-B-baseline.md` — the lane report: what was done, what was NOT done (declared), tokens used, paths.

## RULES
- ⛔ Do NOT edit anything under `knowledge/`, `showroom/`, `apollo-spider/`, or any snippet/meta/canon file. Do NOT run `_build_all.py`. Do NOT commit or push.
- ⛔ Do NOT rule anything of Dave's; RSQs go in the review page.
- Claims carry a probeable token (file path, sha, exit code, playwright assertion) — no "looks good".
- Mid-lane check-in: you are a >15K lane; at the seam between Arm A and Arm B, note your context use in the report.
- Return to the conductor: the review page path, the subreport path, the two dashboard paths, the four scores per arm, and the top three findings in one line each.
