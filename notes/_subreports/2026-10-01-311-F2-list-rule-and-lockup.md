# #311 overnight wave 1 · lane F2 (Fable) · the list rule and the page-header lock-up, drawn as calls

COUNTS: calls 2 (list rule W-305e1, lock-up W-305e3) · drawn options 3 + 3 · recommendation each (list Option 1, lock-up Option 2) · pictures 20 (12 list, 8 lock-up; light + dark, 390 for the lock-up) · rendered read-only against canon at 148fa6fc · fragment verified in the B-page shell at 1440 and 390 (0 broken images, no horizontal scroll, 8 chips) · rulings inscribed 0 · rows closed 0 · found-not-fixed 2

Headline: both stalled rows now have a picture and a wording to click. The banking demo already does what Dave said on the list (its payment tile is a list under a search, two filters, a switch, chips and pages); the sentence he rejected would have made that tile a data grid. Recommended list rule: list by default with its toolbar, table when a field is read down a column, data grid only for bulk select or edit in place. Recommended lock-up: keep the built one as the default, give it a foot for the tab strip, breadcrumb replaces the eyebrow on a drill-down, drop the badge-count arrangement.

Brief: `notes/_lanes/312/F/BRIEF.md` item 4, lane F2, under the rules of `notes/_lanes/312/OVERNIGHT-CHAINS.md` and its addendum (own committer under the seat-wide lock; render read-only against canon; no push).

## Built
- `notes/_lanes/312/F/F2/render_F2.py` — the driver (`list|header|all`), seat-run after `seat_env.sh`; composed pages in `/dev/shm/f311F2`, nothing under `knowledge/` written.
- `notes/_lanes/312/F/F2/img/` — 20 PNGs + `facts-*.json` (tile 1392px wide at 1440; 12 results / 6 rows shown, Europe 4 / 4; lock-up heights at 1440: option 1 126px, option 2 198px, option 3 162px; at 390: 210px and 282px).
- `notes/_lanes/312/F/F2/FRAGMENT.html` — two section-ready calls (`#list-rule`, `#lockup`) in the B review-page shell's classes, each with chips Option 1/2/3/None, `data-rec` set to the recommendation, a Technical fold, and image paths relative to `notes/`. The page lane (F5) replaces "0N" in the two labels with its numbering.

## The list rule (W-305e1)
Pictures: the demo's own tile as it stands and filtered to Europe through its own market filter; the same twelve payments (the demo's `DATA` array) composed as a `.cn-table`; the canon Data-grid reference cropped to the grid (its own 24 records — composing a grid by hand would re-draw it).
Options put to him: (1) toolbar does not change the shape — list default, searchable/filterable/sortable/paged; table when a field is read down a column (s274-D4); data grid only for bulk select or edit in place. (2) sort is the line — sorting by a field is reading it down, so a sorted list becomes a table. (3) list until it is edited — grid only for in-place edit. Recommendation: Option 1, with the reason that a checkbox column is a column read down, so bulk selection goes with the grid.
If taken, the inscription lane touches: `list-items.meta.json` `when` ("needs = none"), `roles.json` record-list → data-grid `when`, `notes/_lanes/304/R4a/drafts/when-rules.proposed.json`, row `W-305e1`.

## The page-header lock-up (W-305e3)
Pictures: the demo's header three ways, light and dark, composed from `.cn-page-header-lockup`'s own classes only: (1) as built; (2) breadcrumb above, title + meta + actions on one row, the s310-D8 tab strip on the foot; (3) two rows, title alone then meta level with actions (one inline `align-items:center` on the second row; the built `.ph-row` aligns to the top). Plus 390 for options 1 and 2.
Recommendation: Option 2 as the shape of the family — one lock-up with three optional parts (crumb-or-eyebrow, meta line, tab foot), actions always on the title row, the built ≤560px fold kept; drop arrangement C (badge count). If taken: `page-header-lockup.meta.json` (`arrangement` enum → the existing booleans), the reference's arrangement C, row `W-305e3`.

## Gates run
None touch this lane's change (pictures, a fragment and a report under `notes/`; nothing under `knowledge/`). `knowledge/_tests/test_gates.py` was attempted twice at the seat by the re-launched F2 (TMPDIR=/dev/shm, because the seat home is 99% full and the first try died there with ENOSPC copying `knowledge/assets`): both runs were cut by the seat's call ceiling under twelve concurrent lanes (16 s and 46 s, no output) — so it is NOT green by this lane's hand; the combined-HEAD survey runs it.

Sha: pictures rendered at `148fa6fc`; committed from `d1901fa2`. `git diff --stat 148fa6fc d1901fa2 -- knowledge/canon knowledge/snippets dashboards knowledge/components` is empty, so the pictures are what canon at `d1901fa2` draws.

## Found, not fixed
1. Inside the demo's payment tile the filter toolbar stacks its four controls in a column at 1392px wide (search, market, currency, switch one under another, chip row to the right), where the filter-toolbar reference runs them in a row. `dashboards/international-banking-dashboard.canon.html` — not this lane's file. Visible in `img/01-list-as-built-light.png`.
2. At 390 the tab strip in the composed lock-up copy runs off the right edge: the demo page does not carry Tabs' overflow script (the reference snippet does). A tab foot on a real page needs that script beside it. Visible in `img/02-lockup-b-390.png`.
3. The composed table's caption sub-line (`caption .sub`) sits tight under the caption in `.cn-table`; cosmetic, in my composition only.
4. Lane A7's commit `d1901fa2` wrote `knowledge/_state.json` whole and so carried this lane's born-closed row `W-311f2` (and H1's `W-311h1`) into HEAD before either report was committed: for the span between `d1901fa2` and this commit the row named a report that was not in the tree. The lock serialises writes but a whole-file commit still sweeps other lanes' rows; the conductor may want per-row staging or a `_state.json` commit only by the lane whose row it is.
5. Every commit tonight is refused by the showroom sync gate: `showroom/links.html` is stale because lane A1's `knowledge/snippets/Links.reference.html` edit (s307-D75) sits uncommitted in the shared working tree, and the gate reads the tree, not the staged paths (H1's `outputs/311/H1/commit2.log` shows the same refusal). This lane passed it with `SHOWROOM_ACK` naming that cause; A1's commit (with `gen_showroom.py`) clears it for everyone.
6. The seat-wide lock is not holding: `/tmp/apollo-commit.lock` was found held past 30 minutes twice (a marker-less holder 23:48–00:18, then E0 00:20–00:53 and the D1–D3 lane 00:54–01:26, each with a marker file inside, so `rmdir` fails and the stale rule needs `rm -rf`); lanes committed while the lock was held by others (CS at 23:5x, E0, D1 at ~00:59 and the D1 stamp at ~01:27 landed while this lane held the lock). Under twelve concurrent lanes the seat also cuts calls at 15–95 s whatever `timeout_ms` says, so a lane holding the lock across a cut call leaks it. The lock was taken by this lane at 01:26:53 after the D1–D3 marker had sat 32 minutes with no `.git/index.lock`.

## Ruling-shaped questions
- Which wording of the list rule stands (Option 1 recommended) — on the page.
- Which lock-up shape stands (Option 2 recommended), and whether the badge-count arrangement goes — on the page.
- Neither is inscribed; both rows stay open until he answers.

## Commit
Own paths only, under `/tmp/apollo-commit.lock`: `notes/_lanes/312/F/F2/**` and this report. The born-closed row `W-311f2` is already in HEAD (swept in by `d1901fa2`, see found-not-fixed 4), so `knowledge/_state.json` is not in this commit. No push.

How the commit landed (declared, not hidden): `_git_commit.sh --reconciled --quiet` was run five times from the lock (01:27–01:51 UTC). Every run's gates were green (chain fresh, doc rows, polarity, mention map, schematic, session witness; showroom sync passed as a DECLARED gap, see found-not-fixed 5), and every run was killed by the seat's call ceiling (58 s, 94 s, 86 s) between its last gate and its `git commit` line, or refused at `git add` by another lane's transient `.git/index.lock` (two runs). The script had staged exactly the named paths plus the auto-staged `notes/_REHEARSAL-LOG.jsonl` and rendered its T3 msgfile (`outputs/311/F2/msg-f2.txt.t3-rendered`). The commit was then made by hand with the script's own last step, `git -c user.name=Claude -c user.email=claude@anthropic.com commit --cleanup=verbatim -F <that rendered msgfile>`, and the script's two post-commit asserts (subject ≤ 200 chars; subject identical to the T3 headline) were run by hand and passed. Transcripts: `outputs/311/F2/commit{,2,3,4,5}.log`.
