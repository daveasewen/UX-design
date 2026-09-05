# #247 · W1 — DENSITY. Lane D (the edit) → Lane R (the re-run) → Lane J (the blind judge)

Plan: `reviews/DP-TEST-PLAN-2026-09-05-v1.html` § 01 W1. Ruled by `s246-D5` (KPI row default, 2×2 REMOVED) and `s247-D1` (29, carefully, test). Principles: DP-06 07 08 09 on `reviews/DASHBOARD-PRINCIPLES-2026-09-05-v1.html`.

Register probe (#244 rule, done by the conductor): `knowledge/_enactment-register.json` carries no row for kpi-tile or Template-dashboard-bento — nothing here is a typed count.

## THE ONE EDIT (lane D)

File: `knowledge/snippets/Template-dashboard-bento.reference.html`, GROUP 1 · the lead group (L843–905): today four `kpi-tile` at `data-c="3"` = a 2×2 board at six columns.

Target (DP-06): headline metrics in ONE compact row across the top, so the first chart starts above the fold at 1440.

⛔ The snippet's own constraint (L60–74): a static snippet cannot run the squaring pass, so spans must be square AT EVERY BAND (6 → 3 → 2 → 1) with no new band rule. Options, in order of preference — pick the FIRST that is square by construction, and say which:
1. **Six tiles at `data-c="1"`** using the existing `compact` variant of kpi-tile (`kpi-tile.meta.json` variant `compact`, 24px figure): 6 → 3+3 → 2+2+2 → 1. Square everywhere. DP-07 allows 3–6.
2. Four tiles at `data-c="1"`: orphans at the 3-col band (3+1). REJECTED unless you can show it square.
3. A `--bento-columns:4` override on the lead group: needs band rules the snippet says not to hand-copy. Do NOT do this without reporting why 1 failed.

Also: `.c-bento.tpl-group-lead{ --bento-row-unit:120px; }` — keep unless the compact tile needs less; if you change it, one line in the report with the measured tile height.
DP-08 (value · signed delta vs named period · sparkline): only if the kpi-tile already carries those slots — do NOT add markup slots to the component. Report what it carries.
DP-09 (space not borders): already the wall's rule 7 (frame yields). Confirm, don't edit.

Update the GROUP 1 comment (L844–845) to say what it now is. Nothing else in the file changes. `git diff --stat` must show ONE file.

## GATES (lane D, after the edit)
- `python3 knowledge/_validate_snippets.py` (or whatever validates this snippet — find it, name it) — exit code + first 20 lines.
- Render the snippet at 1440 · 1100 · 820 · 520, light + dark, mono theme → `outputs/w1-density/template/*.png`. Playwright runbook: `knowledge/_ROBUSTNESS-PORTABILITY.md`.
- Measure: at 1440 light, the y of the first chart's top edge, before (git stash / `git show HEAD:`) and after. That number IS the finding.
- ⛔ `_validate_screen.py` writes into `knowledge/` — if you run it, restore `knowledge/_SCREEN-GATE.md` via `git show HEAD:` after, and say so.
- Do NOT run `_build_all.py` (fenced). If canon.css / showroom regenerate from the snippet, name the generator and whether it was run; if not run, that is a DECLARED skip with its reason.

## RE-RUN (lane R, after D returns) — exactly the #246 lane-B protocol
Brief: `notes/_briefs/2026-09-05-246-lane-B-baseline-brief.md` — same prompt (P0, verbatim, typo included), same two arms in the same order (A blind, then B sighted), same reading fence, same measurement 1–7. Differences ONLY:
- Output root `outputs/w1-density/` (arm-A-blind · arm-B-sighted).
- Score sheet C: `notes/_dp-scores/w1.json` — 29 rows `{id, verdict: met|missed|n/a, fact}` + seeds `{1..6: pass|fail, fact}` + richness `{rich,full,persistent,interactive}` per arm. DP-06/07/08/09 rows MUST carry a file+line fact.
- Review page `reviews/W1-DENSITY-2026-09-05-v1.html` (swiss-design-system): baseline B render beside W1 render at 1440 light, the first-chart-y before/after, the seed-1 verdict, richness delta vs B 2/2/0/2, the 29-row sheet, a CONFLICT LEDGER section (any DP pair that pulled opposite on one tile; empty is a legal answer, say so), RSQs.
- Subreport `notes/_subreports/2026-09-05-247-W1-density.md` in `notes/_subreports/_TEMPLATE.md` form, WITH a `COUNTS:` line and a `RULING-SHAPED QUESTIONS` heading (#246 lanes missed both).

## JUDGE (lane J, runs beside R's measurement, not after)
Gets ONLY: `outputs/baseline-246/arm-B-sighted/*1440*light*.png` and `outputs/w1-density/arm-B-sighted/*1440*light*.png`, unlabelled (copy them as `x.png` / `y.png` to `outputs/w1-density/judge/`), and this instruction: "Two dashboards. Which reads denser above the fold, and what is the first thing you would change on each? Three lines." Writes `outputs/w1-density/judge/verdict.md`. The key (which is which) is appended by R after J returns.

## RULES (all lanes)
- ⛔ Edit NOTHING under `knowledge/` except the ONE snippet (lane D only). No `apollo-spider/`, no `showroom/`, no meta, no canon. No commit, no push.
- ⛔ Rule nothing of Dave's. RSQs go on the review page. In particular: do NOT decide six-vs-four beyond the squareness test; if both are square, the pick is his — build option 1 and say so.
- Claims carry a probeable token (path · line · sha · exit code · playwright assertion · a y in px).
- Lanes are >15K: check in at the seam (D: after the edit, before gates · R: between arms · J: n/a).
- Return to the conductor in ≤250 words: paths, the first-chart-y before/after, seed-1 pass/fail, richness per arm, the top three findings one line each, tokens used.
