# #308 lane C — review page: the old claim tables

COUNTS: rows re-checked 9 · went stale 2 · checker misread 3 · never checkable 3 · CI-only 1 · rows (a) would clear 2 of 9 · rows (b) would clear 9 of 9 · pages 1 · renders 3 (1440, 390, 390 dark) · commits 0 · pushes 0

Page: `notes/_REVIEW-308-old-claim-tables-2026-09-29-v1.html` (self-contained, back link after <body>, light and dark via :root tokens, no horizontal scroll at 390; decision bar with two calls plus a page note, localStorage in try/catch, "Copy as text" headed "Session 308 · old claim tables · answers"). Renders: `notes/_lanes/308/C/render-1440.png`, `render-390.png`, `render-390-dark.png` (viewport only). Clicking a chip and typing a note was driven in Playwright: storage wrote, and the count went to 2 of 3.

Recommendation on the page: (b), dated notes by addition on all nine, and keep the CI step advisory.

## What the brief's premise got wrong (tested, not assumed)
The brief said the nine rows went stale because the tree moved on. That is true of only two.
- Stale, true at their commit: WIRE-14. At `9d552ddc`, STEPS=127 and ROUTE_ROWS=127 (read by ast from `git show`); today the seat has 166 and CI on 417ce218 had 163. WIRE-21: `grep -c 'fetch-depth: 0'` gives 3 at `9d552ddc` and 4 now; the fourth arrived with `801fe7cc` (#219, the release job).
- Checker misread, not stale: L1-1 ×2 (claim and challenge). The row quotes `_build_blast_radius.py`'s own stdout, which names `tokens/_blast-radius.json` relative to `knowledge/`. The file is at `knowledge/tokens/_blast-radius.json` at 541ffcc3, at 9d552ddc and at HEAD, and was never at the repo root. W2-13 (208 verifier): `notes/x.md…` is a made-up path the verifier fed the build on purpose, and the row says "a path that does not exist". It has never existed in history.
- Never checkable: L1-4, C-2, H-5. Their evidence points at other rows or gives bare counts. The linter as of `9d552ddc`, run on today's tables with --no-sample, flags the same six lint rows, so these have been failing since the day it was wired. That matches the #208 gates.yml comment ("6 lint failures").
- CI-only, the ninth: WIRE-20. `_governs.py --selftest` returns rc=0 at the seat but rc=77 (COULD-NOT-ASK, some evidence pointers absent in the checkout) in CI. Source: the gates log of run 36490341746, fetched through `_ci_readback.Client`. The #208-era CI run on 9d552ddc has no evidence-step lines.

## Corrections to lane F's § 3
1. "`tokens/_blast-radius.json` no longer exists" is wrong. See above.
2. "the mismatch count moves with the sampler's seed" is wrong. DEFAULT_SEED is 205 and both runs drew the same 20 rows. The seat-versus-CI difference is WIRE-20's environment.
3. The step count is 166 at the seat now, not 163.

## Is (a) buildable
Yes, with a cost. Per-row commit: `git blame --porcelain` (206-w45 was written in two commits). Old files: `git cat-file -e <sha>:<path>`, and the CI gates job checks out with fetch-depth 0 (gates.yml:231). Re-running commands needs a temporary worktree per commit (5 commits). After (a) alone the step cannot go blocking, because 6 lint rows plus WIRE-20 stay red. After (b) it technically could, but 12 more declared-observation rows in 208-wiring would age the same way. Blocking is only sensible with (a) as well. No claim table has been written since 2026-08-19.

## Housekeeping
- Two scratch copies I could not delete (delete is off): `notes/_lanes/308/C/scratch-linter-at-541ffcc3.py.txt` and `scratch-linter-at-9d552ddc.py.txt`, which are `git show` copies of the old linter. They are untracked; the conductor can drop them.
- Git use beyond log/show: `git cat-file -e` and one `git blame --porcelain -L` (both read-only). Nothing was written to the repo except the page, the renders, this report and the two scratch files.
- The ✅ and ⛔ glyphs in two quoted rows render as boxes in the headless shell because it has no emoji font. They are verbatim and will show on the Mac.
