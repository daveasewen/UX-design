# #304 R4c — the eval harness, and the v1.0.13 baseline briefs

**Seat 4c of Run 4, Saturday 26 September 2026. Nothing committed, nothing pushed, no git calls, no Project memory,
nothing under `knowledge/`, `showroom/`, `apollo-spider/` edited.**

## The answer first

The harness exists and passes its own test: a planted bad page (the pack's bento template traced whole, on the
wrong theme, with its chart cut off) and a known good page separate on every planted defect and on the total,
each single-defect mutant moves only its own detector, and an independent re-run reproduces every score and
every earning fact. The three baseline cold runs have NOT run: this seat has no Agent tool. Their brief is
written and ready to dispatch; so is the candidate's, with a placeholder for 4a's pack.

## How to run it

One seat call per phase group; the seat env must be sourced in the same call:

```
cd "$HOME/mnt/Projects--UX-design" && export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; \
  source knowledge/_render/seat_env.sh; \
  python3 notes/_lanes/304/R4c/harness/score.py all --run-id cold-v1013-r1 --kind "cold run" --label v1013-r1 \
    --pack apollo-spider/dist/Apollo-Spider-v1.0.13.zip \
    --copy-out notes/_lanes/304/R4c/cold/v1013-r1/out --page notes/_lanes/304/R4c/cold/v1013-r1/out/index.html
```

`all` is resumable: it skips finished phases and stops before a phase when the call is short of time, so run
it again until `CARD` prints. Phases can also be run one by one (`stage static gates render drive ext card`).
Side by side: `score.py compare --runs a,b,c --out <file>.html`. The harness's own test:
`score.py selftest` (after the fixture runs listed in `harness/selftest.py`'s docstring).

## What it measures

Per run it writes `notes/_lanes/304/R4c/runs/<id>/scorecard.json` and `scorecard.html`, plus the phase files
and the light and dark renders.

1. The four-part rubric (visually rich, full, persistent, interactive, 0 to 3), each with the one fact that
   earned it and the rule that turned the fact into a number. For the CEO prompt, "visually rich" follows the
   prompt's "be liberal with data visualisation": chart count and chart variety carry it. Pages built to the
   older prompts use the hand-rubric equivalent (component breadth plus a chart that renders).
2. Composed or traced. The page's DOM, as written and as rendered, is compared with every `Template-*`
   snippet in the pack under test and in v1.0.13, on three signals: structural shingles (tag plus class
   5-grams), the template's own text reused verbatim, and classes only the template uses. The cut was
   calibrated on pages whose provenance the record states. The seven bento-first splices (#246, #258 runs 1–5,
   #267) read between 0.334 and 0.561, and the two template-closed compositions (#288 P, #292 D) both read
   0.041. Anything at 0.30 or above is TRACED, anything under 0.15 is COMPOSED, and the band between is
   PARTLY TRACED.
3. Component variety. A part counts when its `cn-` scope class is present, when a class named for it is
   present, or when two or more classes that canon uses only for that part are present. Templates are listed
   but not counted.
4. Charts against the ask: how many charts rendered with marks, how many types out of the pack's 14, how many
   are on the overview, legend and table presence, tooltips on hover, and any CLIPPED chart. A chart counts
   as clipped when an overflow-hiding ancestor, the figure itself, or the SVG viewport cuts it by more than
   2px.
5. Theme (Common): the root carries `class="canon"` and `data-apollo-theme="common"` (or the `legacy`
   alias), not on `<body>`; the Common tokens resolve when rendered (`--button-primary-background-default`
   is `#DB0011` and `--border-radius-default` is 0); no hex owned by another theme; the switch flips the
   theme on `<html>`.
6. Accessibility, rendered: controls with no name, targets under 24px, images with no alt, duplicate ids,
   skipped heading levels, landmarks. The pack's a11y gate line is kept beside it.
7. The pack's own gates run on the page from a per-run copy of the pack, so their writes never touch the
   repo: `_validate_screen.py` (receipt, compose, composition, icons, a11y) and `_validate_dataviz.check_file`.
8. 4b's gates, found by path: `knowledge/_validate_geometry.py` and `knowledge/_validate_own_size.py` (both
   now exist). The geometry 0 to 3 score is read from the gate's own JSON and reported beside the /12, never
   folded into it. If a gate is absent the card says ABSENT. The gate's sha256 is recorded with its result.
9. Render facts: the real platform face, read through CDP (the HSBC face resolved on every run so far),
   horizontal overflow, page errors, console errors, and clipped elements.

Left to judgment, printed unscored on every card: taste; alignment the signals cannot name; whether each
chart is the right chart; data believability; whether the overview answers the three CEO questions as a
person reads it; whether workflows make sense end to end; whether the composition is good composition.

How the drive works. It is deterministic: a fixed enumeration order, fixed waits, no randomness, and a fresh
browser context for each section, so stored state never leaks from one section into the next. A control
counts as live only if the click changed visible text, an aria or form state, or the theme, or if it
navigated, downloaded or opened a dialog. Raw mutation counts are kept for information only, because
hover scripts mutate class lists on any pointer move. A bare `#` link and an in-page anchor jump are not
counted as navigation.

## Test it hard: the results

`python3 notes/_lanes/304/R4c/harness/score.py selftest` returns **SELFTEST PASS**, with 8 of 8 assertions
passing (`runs/selftest.json`, `runs/compare-fixtures.html`).

| run | rich/full/persistent/interactive | total | trace | theme | clipped charts |
|---|---|---|---|---|---|
| known good (`fx-good`) | 1/1/3/1 | 6 | COMPOSED 0.041 | PASS | 0 |
| planted bad (`fx-bad`) | 1/0/0/1 | 2 | TRACED 1.000 | FAIL | 1 |
| good, wrong theme | 1/1/3/1 | 6 | COMPOSED | FAIL | 0 |
| good, clipped chart | 1/1/3/1 | 6 | COMPOSED | PASS | 1 |
| good, no persistence | 1/1/0/1 | 3 | COMPOSED | PASS | 0 |
| good, independent re-run | 1/1/3/1 | 6 | COMPOSED | PASS | 0 |

The fixtures are rebuilt deterministically by `harness/build_fixtures.py`, with source shas in
`fixtures/SOURCES.json`. The known good is the #292 D cold one-shot (composed with the template closed), put on
Common, plus a thin fixture layer that makes views, a theme switch, a filter, search and sort work and persist.
It is good only on the measured axes; its interactive score is 1 because the source page's own buttons are
inert, and the harness says so. A stub gate proved the 4b pickup contract (FINDINGS on the planted page,
PASS on the good one, ABSENT without it); the real 4b gates then replaced it.

Calibration against the hand scores of the past series (same pages, `runs/compare-extra-baselines.html`):

| page | hand | harness |
|---|---|---|
| #258 run 1 | 3/2/0/2 | 1/2/0/2 |
| #258 run 2 | 3/2/3/3 | 1/3/3/2 |
| #258 run 3 | 3/2/3/2 | 1/3/3/2 |
| #258 run 4 | 3/2/3/3 | 1/3/3/2 |
| #258 run 5 | 3/3/3/2 | 1/3/3/2 |
| #267 run 6 | 2/3/3/2 | 2/3/3/2 |

- **Persistent** agrees 6 of 6.
- **Interactive** agrees 4 of 6; where they differ, the harness reads one lower.
- **Full** agrees 3 of 6. On the other three the harness reads one higher: the hand scorer held "full" at 2
  for a grid dead band, which is now 4b's geometry axis.
- **Visually rich** agrees 1 of 6, and the harness always reads lower. It cannot see the component breadth
  the hand scorer counted in template-spliced markup: parts spliced without their scope and without their
  own classes are invisible to it.

All six also read TRACED, as the record says they were built. Caveat: the #258 pages link the repo's canon, so
they render against today's canon, not v1.0.7's.

## Baseline scores so far (extra points, other prompts, labelled)

The #292 D one-shot and the #288 P probe both score 3/1/0/0 (total 4), COMPOSED, geometry 0. #267 cold run 6
scores 2/3/3/2 (10), TRACED. #258 runs 2 to 5 score 9 each and run 1 scores 5; all are TRACED. Every one of
the eight pages has 4b geometry findings. These were built to other prompts, so the Common and CEO rows do
not apply to them. **No v1.0.13 run of the CEO Common prompt exists yet.**

## What the conductor must dispatch

Three fresh Opus 5.5 agents, one each, with no shared context. Each gets the brief
`notes/_lanes/304/R4c/cold/brief-v1013.md` verbatim and its run id: `v1013-r1`, `v1013-r2`, `v1013-r3`. They
freeze to `notes/_lanes/304/R4c/cold/<RUN>/out/` with a `RUN-REPORT.md`. Then score each run with the
command above, and run `compare`. For the candidate, fill `{{CANDIDATE_PACK_ZIP}}` and its sha in
`cold/brief-candidate.md` (the two briefs differ only there) and dispatch `cand-r1..r3` the same way, with
`--pack <candidate zip>`.

## Not done (declared)

- The cold runs themselves, and so no v1.0.13 CEO-prompt baseline scores yet.
- No render pair for Dave: that needs the runs.
- The "persistent" drive tries one change per family. A filter whose menu paints at opacity 0 cannot be set,
  so it reads as "not changed", as in the #258 run 3 finding.
- Sub-pages are probed light only, within the call's budget. Any not reached are listed on the card.
- 4b's gates were still changing while I worked. Their scores are pinned to the gate sha recorded in each
  `ext.json`.
- `runs/_to_delete/` holds stale stub output, QA pngs and a `__pycache__` that the mount would not let me
  `rm`. Delete them by hand.

## Files

- `notes/_lanes/304/R4c/harness/score.py` (the command-line tool) · `browser.py` (render and drive) ·
  `probe.js` · `selftest.py` · `build_fixtures.py` · `profiles/ceo-common.json`, `profiles/generic-dashboard.json`
- `notes/_lanes/304/R4c/harness/fixtures/`: 5 pages plus `SOURCES.json`
- `notes/_lanes/304/R4c/cold/brief-v1013.md` · `cold/brief-candidate.md`
- `notes/_lanes/304/R4c/runs/`: 14 scored runs, 4 static-only calibration runs, `selftest.json`,
  `compare-fixtures.html`, `compare-extra-baselines.html`
- `notes/_lanes/304/R4c/STATUS.md`: resumable notes
- this report

## `_state` doc-row spec

`{"id": "doc-304-R4c-eval-harness", "kind": "doc", "title": "#304 R4c eval harness + cold-run briefs",
"path": "notes/_subreports/2026-09-26-304-R4c-eval-harness.md", "session": 304, "lane": "R4c",
"status": "open", "blocks": ["4f cold runs v1013-r1..r3 (conductor dispatch)", "candidate brief needs 4a pack path"],
"evidence": ["python3 notes/_lanes/304/R4c/harness/score.py selftest → SELFTEST PASS"]}`
