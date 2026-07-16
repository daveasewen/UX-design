# Good morning, Dave ☕

*Briefing — written end of 2026-07-16, session **"Apollo masthead — model, review tooling & switchable build" + dataviz kickoff.** Read this → `_LIVE-STATE.md` (LIVE + OPEN) → then the dataviz dossiers below. Dense on purpose.*

## The session in one line
Shipped the **unified switchable Masthead** end-to-end (model → build → ~6 review rounds → done), upgraded the **review tool**, fixed **playwright in-sandbox**, then pivoted to **DataViz**: desk research + KB mining + a framework verdict. Dataviz is the next big pillar and it's teed up to build.

## ⏭ FIRST TASK — the DataViz **method dossier**, then unblock the palette, then build round-one
> **UPDATE 2026-07-16 close: steps 1+2 DONE, CONFIRMED + ENACTED.** V7 resolved on renders through three markup
> rounds: **C = default · A = high-contrast alternate · D2 deltas (value-split)** — LIVE in `semantic-colour.json`
> (`data/series/*` · `data/series-high-contrast/*` · `data/delta/*`); override + NEW **vibrating-boundaries rule**
> recorded as `{#dv-019}`; ranges = palette-native proposals in `dataviz-ranges.proposals.json` (edit-mode dial,
> parked). Build green. **NEXT SESSION = step 3: the round-one kit** (KPI card → bar/column → line → donut),
> `_validate_dataviz.py` incl. the vibration check lands WITH the first chart. Dossier §08 items 1/5/6/7/8 still
> open — mark up `DATAVIZ-METHOD-2026-07-16.REVIEW.html` when you get a minute.

Everything needed is on disk. Order:
1. **Method dossier** (clean + review pair, like the masthead model) — pin down: approach, the variant-complete inventory, the round-one kit, gate mapping. Draft is task #15.
2. **Unblock V7 (series assignment)** — decide which supporting-palette family/step = series-1/2/3… **per mode**, using **real renders** in light+dark (respect each step's `indicatorOK`). This was deferred "for proper renders" — we can now render.
3. **Build round-one kit**: KPI **"metric + delta + spark"** card · line (+ sparkline) · bar/column (+ stacked) · donut. Covers most retail banking; exercises palette + flat-fill + table-fallback + CSS motion.

## DataViz — what's already in hand (don't re-research)
- **Desk research DONE** → `reviews/DATAVIZ-DESK-RESEARCH-2026-07-16.html` (+ REVIEW). Digital + finance charting, cited, reviewed by Dave.
- **HSBC rules already in the KB** → `guidelines/data-visualisation.md` (+ `-bar-charts` / `-pie-charts` / `-line-charts`): flat 2D fills only / **no gradient / no 3D**; building blocks ≥3:1; **palette-only fills**; ≥2px block gap; bars need a zero baseline (lines don't); straight lines only; 6-slice pie cap; **tabular alternative + link**. Many tagged BLOCKING-derivable = gate-able.
- **"Supercharge" palette = the SUPPORTING palette** → `tokens/_proposals/supporting-palette.proposals.json` (10 families × 5 steps, with per-mode contrast + `indicatorOK`). Primitives already **live** in `tokens/colour.json` as `color/supporting/<family>/<step>`. Families: midnight-blue · forest-green · olive-green · burnt-orange · dusk-purple · rose-pink · sky-blue · mint-green · sun-yellow · apricot-orange.
- **Approach RECOMMENDED (not yet ratified):** CSS-first **custom SVG + token layer** — **reject canvas** (can't tokenise/inspect/a11y); table-as-source (Charts.css idea) for simple types; D3-scale / Observable Plot for hard maths only; **CSS-only motion** (DEF-003-clean); a visually-hidden `<table>` doubles as the a11y tree + the required tabular alternative.

## DataViz — Dave's rulings this session (carry into the dossier)
1. **Red/green: not precious.** The never-red/green orthodoxy is overblown — use the gain/loss convention, pair with sign/arrow/position. ⚠ BUT the KB rule **"no red in charts"** ({#dv-017}) must be **explicitly overridden for gain/loss** — do it consciously, it's a documented brand rule.
2. **Texture: sparingly + stylishly** — one **chevron-style** pattern max per chart, still flat (no gradient/3D). Not a zoo of hatchings.
3. **Legends OK, but with an alphabetic signifier** — bars A·B·C on the element; legend shows **colour + letter + name** (letter = the colour-independent channel).
4. **Variant-complete inventory** — enumerate ALL sub-variants (bar → vertical/horizontal · grouped · stacked · segmented · **butterfly/tornado** · diverging · waterfall · bullet…; same depth for line / composition / relationship).

## Also DONE this session (context, not to-do)
- **Masthead LIVE + reviewed to done** → `knowledge/_proforma/Masthead-interactive.html`. One `data-mode` skeleton, **3 recipes** (L1 exposed · L1 + mega · Trigger mega), a **drill-down mobile drawer** variant, crescent brand mark, CSS-only motion, all 4 gates + full `_build_all.py` green. Model dossier `reviews/MASTHEAD-MODEL-2026-07-16.html` + KB `_MASTHEAD-MODEL.md`. **Supersedes** the T7 gheader + mm-masthead demos.
- **Review tool upgraded** (`knowledge/_review/`): draggable comment box + leader-line "noodle" + exact-element highlight; `_make_review.py` generalised (co-located clean/review pair). **Rule 16** in `_PROFORMA-RULES.md` = every doc ships a clean + review pair.
- **Playwright renders in-sandbox again** — full recipe (TLS trick + local-extracted libs) in memory `sandbox-html-rendering`. Reuse it, don't re-yak-shave.
- **2 provisional glyphs** (crescent brand `i-brand-apollo`, combined `i-menu-search`) logged in `_ICON-GAPS.md` — swap for real assets later (Dave: "later").

## On your desk / rules to hold
- **Uncommitted:** a LOT landed this session (masthead, dataviz dossiers, review-tool changes, `_LIVE-STATE`, rules, `_ICON-GAPS`). **Commit + push via GitHub Desktop** (Claude commits local; keep Desktop CLOSED during Claude commits — lock contention). Paste-ready commit line was given at the masthead wrap.
- **Working model:** deliverables land straight to the live repo as-made (not cloud scratch).
- **Every doc = clean + review pair** (rule 16). Feed edits by marking up the REVIEW copy → paste the exported prompt back.
- **Comms:** exec-summary first + numbered next-steps (dyslexia + time-poor).

## Queue after dataviz (from `_LIVE-STATE` OPEN)
- **Tranche 8** (nav completion: BottomTabBar · InPageNav/scrollspy · FooterNav · RelatedLinks · journey Stepper) + the **Shell/footer template tier** (the thing that makes screens *ship* — payments-journey-proof blocker).
- **Type-token system** — blocked on your Figma file.
- **Sidequests (harvest later):** research **knowledge-graph** · Swiss **state-ledger viewer** · the **component catalog** ("nicer Storybook") + retrofit T1–7 docs.

> Opener: **"Title this chat: <pick one>."** Then GOOD-MORNING → `_LIVE-STATE.md` (LIVE + OPEN) → the dataviz dossier + `supporting-palette.proposals.json`.
