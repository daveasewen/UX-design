# #258 lane C brief — THE COLD RUN: the frozen prompt against the v1.0.7 ZIP, blind (the VS Code condition)

**Model: Opus 5 (GPT proxy, per Dave #246). Conductor: Fable (#258). Dated period record (ADR-0017). Read-only against canon/knowledge — MOVES NOTHING in the library, RULES NOTHING.**

## WHY

Dave, #246: *"the focus is getting the dashboards one-shotable"*. #246 measured the BEFORE (v1.0.5-era tree): Arm A blind **2 / 2 / 0 / 2** (rich / full / persistent / interactive), Arm B sighted the same. #247–#256 enacted DP-01…18, roles, 24 metas, the ADS- rename; v1.0.7 was ratified and baked at #257 (`s257-D3`, zip sha256 `13a593de…`). The frozen prompt has NOT been run against it. This lane is the AFTER picture. Nothing is fixed here.

## THE PACK UNDER TEST — the ZIP, not the tree

Unzip `apollo-spider/dist/Apollo-Spider-v1.0.7.zip` into a scratch dir (outside the repo, e.g. `/tmp/ads-1.0.7/`). Record the zip sha256 and the top-level listing in the READ-LOG. **Every read in Arm A comes from the unzipped pack** — a consumer never sees the repo. If a file the skill points at is missing from the zip, that is a FINDING, not something to fetch from the repo.

## THE PROMPT (verbatim, FROZEN — do not improve it)

```
/generate-from-canon build me a financial dashboard for corporate international banking. Please make the all the interactive elements work such as filtering and navigation.
```

## ONE ARM — BLIND (the VS Code condition)

Follow `notes/_briefs/2026-09-05-246-lane-B-baseline-brief.md` § Arm A exactly, with these overrides:
1. Output root `outputs/coldrun-258/arm-A-blind/` (dashboard.html, READ-LOG.md, brief.md with grill-me defaults marked *skipped/defaulted*, the Gaps list).
2. Reads come from the unzipped zip only (skill names are now `ADS-*`; dirs unchanged — note which path the prompt resolved to).
3. Forbidden reads unchanged: no `notes/`, chain, GM, LS, reviews, decision history, rulings, any `_*.py`, no `_memento_search.py`. No render, gate, playwright, validator during the build.
4. Do NOT read `outputs/baseline-246*/` until the arm is frozen; then you MAY read #246's review and subreport for the comparison section only.

## MEASURE (after the arm is frozen — never touch it again)

Same seven measurements as the #246 brief, at 1440 and 820, light and dark: render → gates (`knowledge/_validate_screen.py`, `_validate_receipt.py`, exit codes + first 20 lines; if a gate insists on writing under `knowledge/`, redirect and declare) → inventory (used / available-but-unused from the dashboard set) → chart completeness (snippet `<script>` sha256 vs source in the ZIP) → interactions driven with playwright (every nav item, filter, tab, a grid sort; works / dead / missing; persistence = state survives nav + reload) → data believability → four scores 0–3, each with the one fact that earned it.

Playwright: `python3 -c "import playwright"` first; if fresh, `knowledge/_ROBUSTNESS-PORTABILITY.md`. Price it, ~4 calls.

## DELIVERABLES
- `outputs/coldrun-258/` — arm, renders, `drive.json`, logs.
- `reviews/COLDRUN-258-2026-09-08-v1.html` — ONE page, swiss-design-system idiom (`.claude/skills/swiss-design-system`): renders per breakpoint/mode, inventory, chart completeness, interactions, scores, **#246 → #258 delta table** (same rows, both columns, differences named as facts), **Findings** (numbered, one fact + the file/line that proves it), **Ruling-shaped questions** for Dave — do NOT answer them.
- `notes/_subreports/2026-09-08-258-C-cold-run.md` — done / NOT done (declared) / tokens / paths.

## RULES
- ⛔ No edits under `knowledge/`, `showroom/`, `apollo-spider/`, snippets/metas/canon. No `_build_all.py`. No commit, no push.
- ⛔ Rule nothing of Dave's. Claims carry a probeable token (path, sha, exit code, playwright assertion).
- Mid-lane check-in: >15K lane — at the seam between build and measure, write your context use into the subreport.
- Return to the conductor: review path, subreport path, dashboard path, four scores with the earning fact, the #246→#258 delta in one line, top three findings one line each, tokens used.
