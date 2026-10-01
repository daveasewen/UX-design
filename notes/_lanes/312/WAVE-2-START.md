# Wave 2 start — the bridge from #311's overnight wave 1 (lane K, 04:35–05:30 BST Thu 2026-10-01)

Read with `notes/_lanes/312/OVERNIGHT-CHAINS.md` (its addendum still governs) and each job's `notes/_lanes/312/<job>/BRIEF.md`. Every wave-2 lane starts from the HEAD named in § 4, not from the wave-1 shas below; those say which work it builds on.

## 1. What wave 1 landed (nothing pushed)
- **A1** — link, don't paste: s307-D74 enacted at `50159e7a` (stamp `73b8611f`); s307-D75 built but for a legacy ledger; W-307yc closed, W-307yd left open with progress (15 sizing rules on four old fitness screens).
- **A7** — hit-area advisory regenerated and wired into CI's render job; ten stamps (s308-D16–D19, D39–D41, D43, D44, s310-D2) at `d1901fa2`.
- **B5** — the 29 colour forks settled on paper, nothing in canon moved: `814ef82c` (report, `forks-29.json`, `forks-29-table.html`, `forks_29.py`; row W-311b5 rode in `3756e3ec`).
- **C0** — s305-D17, D18, D19, D58 in 70 metas and the schema: `7eaae613`, stamps `5227ccc4`.
- **CS** — the Launchpad day-one build spec: `a4198fc3`.
- **D1–D3** — s308-D20, D21, D22, D23, D24, D28: `ccc094fe`, `a14eb4c5`, `e7e2f863`, `a7fdf39d`, `5d02c171`; W-308ij, il, iq, in closed; W-308ii, ip open.
- **E0** — the wrap phase-3 design: `3756e3ec` (that commit also carries H1's files and rows W-311b5, h1, f1); post-commit note `7325e089`.
- **F1** — top nav and shell IA, four calls: `d4e6a1a9`. **F2** — the list rule and the lock-up, two calls: `e75c8c1e`.
- **H1** — permutation-matrix research: inside `3756e3ec`. **H2** — Assembly/Studio modes proposal: `3d32433a`, `c58749e9`.
- **K** — the chain plan and three chain reports with rows W-311k1–k3: `c96f13d8`; the two survey reds fixed (help gate on `gen_kg_standards.py`; 13 chart receipts re-driven after A1's canon.css): `b644c952`; this page: the commit after it.

## 2. Wave-2 lanes and what each builds on
- **A2–A6, AV** on A1 + A7 (`73b8611f`, `d1901fa2`). A1 is the only canon.css writer so far; give the canon-regen right to one A lane at a time.
- **B6** (the third red, W-308ia) first — B5 rows 1–2 and the notification family wait on it. **B1–B4, B7, BV** after; B7 takes B5's finding on Template-error. B5's picks are a proposal: build none of rows 9, 10, 29 before Dave answers.
- **C1, C3, C4** (cloud) and **C2** (seat) on CS + C0 (`a4198fc3`, `5227ccc4`); **CV** last.
- **D4** on C0's schema commit (`5227ccc4`) and D3 (`5d02c171`); it owns `meta.schema.json` from then. **D5**, **DV** after.
- **E1–E3, EV** on E0's `notes/_lanes/312/E/DESIGN.md` (`3756e3ec`). E3 can replay #309 and #310 only until #311 wraps.
- **F3, F4** (seat renders), then **F5** (the page) taking F1's four calls and F2's two.
- **H3** on H1 + H2 (`3756e3ec`, `c58749e9`). **G** last, after the wave's final commit and its CI read-back.

## 3. Seat problems — tell every lane this
- **Root cause of the index.lock:** deletion is off in the mount (`rm` → Operation not permitted, re-confirmed by lane K). Git removes a lock it did not use by unlinking it, so every git call that takes a lock and writes nothing (a no-op `git add`, `git reset`, re-staging a path already staged) leaves `.git/index.lock`, `HEAD.lock` or `refs/heads/master.lock` behind. A commit, which renames its lock, is fine. Fix per lane: check for `*.lock` under `.git` (outside `_stale-locks/`) before each commit; if no git process runs (`pgrep -a git`), `mv` it into `.git/_stale-locks/` with a time and lane tag. Never re-run `_git_commit.sh` with paths already staged by a killed run: `git reset -q` first, then move the locks it leaves. The real fix is Dave's: allow deletion in the repo folder for the session (`device_request_delete_permission`), or keep using the mv.
- **Call cuts:** at 4–100 s overnight under twelve lanes; with one writer (lane K), calls ran to 165 s. A commit takes 75–105 s: run it alone in its call, under `timeout 165`, output to a log, then grep it.
- **The commit lock** `/tmp/apollo-commit.lock`: one writer at a time is the only thing that worked overnight. Stale after 30 minutes; say so before taking it.
- The help gate scans every `knowledge/**/*.py`: a new generator needs `_help_gate(__doc__, __name__, __file__)` after its imports. Any canon.css change needs the chart receipts re-driven (`outputs/310/A/drive_wrap.py --page …`, two batches).

## 4. Pre-push verdict on `b644c952` (+ this page)
Full survey in a /tmp clone, four chunks, `--include-mutating`: 0 FAIL after the two fixes. Advisory and could-not-ask only: [140] probe registry, [150] ship-list drift, [163] itinerary, [164] edge register (WHY-MISSING 138 is ADVISORY by its own route; it waits on row W-308ii, the metas' `why`), [61] dashboard (could-not-ask, inputs outside the tree). Memento index: fresh in the clone, stale only on the dirty mount. test_gates 36/0; evidence gate PASS; state-contrast swept at the seat in eight slices with CI fonts, audit byte-identical; hit-area sweep rc 0 (advisory). Clean to push.

## 5. Questions for Dave the lanes raised
1. B5: the mono hero's grey sub-line (#767676 / #9A9A9A) — keep a text grey in mono, or go to the ink?
2. B5: does the ink rule reach the outline border token `tertiary/border/default`, pure black in Supercharge and Mono?
3. C0: the data grid's applied search terms are called `terms` — keep, or name them.
4. C0: the bento wall's tiles accept headline metric, status surface, chart, record list — widen or narrow.
5. A1: the canon-gallery page — keep or retire (W-307q2); its two sizing rules wait on it.
6. F1: call 1 — the top nav as the default frame, mega menu for multiple levels — yes as drawn, or change (calls 2–4 on the same page).
7. F2: which list-rule wording stands (option 1 recommended), and which lock-up shape (option 2 recommended).

## 6. Left on disk, not committed, on purpose
- `notes/_lanes/312/B/B5-FORKS-PROPOSAL.md`, `B5-forks.json`, `b5_forks_table.py`, `notes/_subreports/2026-10-01-311-B5-forks.md` — a second, earlier B5 run (23:13 BST) with different picks (seven dead lines, three repairs). The conductor picks one record or files both.
- `notes/_lanes/312/F/F1/` (`SECTION-top-nav-shell.html`, `render_f1.py`, `img/`) — an earlier F1 run's page; `d4e6a1a9` is the one F1 named.
- `notes/_lanes/312/C/C0/backup/`, `notes/_lanes/312/D/d1/_msg-*`, `notes/_lanes/312/F/F2/test_gates.log`, `notes/_lanes/312/H/H2/.unlinktest` — lane scratch.
- `knowledge/_SCREEN-GATE.md` and six `knowledge/_screen-gate/*.canon.md` (a gate run's output, 23:13 BST, no lane named) and the older dirty notes (`_dream/`, `_lanes/293`, `294`, `304`, two September subreports) — not tonight's lanes'.
