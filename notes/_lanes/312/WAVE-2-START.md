# Wave 2 start — the bridge from #311's overnight wave 1 (lane K, 04:35–05:30 BST Thu 2026-10-01)

## REVISED 2026-10-01 12:00 BST by #311 lane R — this section supersedes § 2 below

Dave ruled the multi-library proposal at 11:10 (`s311-D3..D9`, inscribed at `2fbc8184`; export at `notes/_lanes/311/DAVE-RULINGS-2026-10-01-1110-apollo-for-other-libraries.md`) and asked how it rolls into the other plans. The night review (`notes/_REVIEW-311-X-why-the-night-was-slow-2026-10-01-v1.html`) set the seat rule. The panel at 08:04 read 80% all-models and 50% Fable, both resetting 23:00. The revised plan page: `notes/_PLAN-311-revised-wave-2-2026-10-01-v1.html` (five calls for Dave; silence by 12:30 takes each recommendation). New briefs: `notes/_lanes/312/J/BRIEF.md`, `L/BRIEF.md`, `N/BRIEF.md`; every A–H brief carries a REVISED header.

### Seat rule, every lane
At most TWO lanes on the Mac at once, one of them the single committer AC. Text and research lanes work in the CLOUD on a clone of the GitHub repo taken after the noon push, and hand named, changed paths to AC. A cloud lane never commits, never regenerates, never runs the survey on the mount. The conductor pushes and reads CI back at 12:00, about 16:00 and about 20:30.

### The revised order (ranked)
1. **AC** · Opus · SEAT, 12:00 → the wrap · the single committer: canon.css, the chart receipts, `_state.json`, `_rulings.json`, the token files (from J) and the schema (from L). Regen serial once per wave (15:00, 20:00) plus a small commit about 14:00 for L1's schema. Survey in a /tmp clone. Checks `.git` for stale locks before every commit and moves them into `.git/_stale-locks/`. Stamps `s311-D4`, `D7`, `D8` enacted by `--set-status` with the landing shas, each checked against the tree. Renders L3's page at 1440/390 (the one seat call L needs).
2. **J** · Fable · CLOUD · tokens to DTCG 2025.10 (`s311-D8`): `knowledge/tokens/gen_dtcg.py` + `_validate_tokens_dtcg.py`; spine byte-equal, 137 snippet theme blocks byte-equal, moved keys recoverable. AC, 15:00 wave.
3. **L1, L2, L3** · Fable · CLOUD · the spec into the metas (`s311-D4`): L1 the four fields in `meta.schema.json` + ADR-0013 addendum (AC ~14:00); L2 `extract_spec.py` and cohort one's drafts on L1's sha; L3 the review page `notes/_REVIEW-312-L-cohort-one-trees-2026-10-01-v1.html` for Dave's eye (read tonight, rule Friday). L owns the metas and the schema from noon to its 20:00 commit.
4. **N1** · Fable · CLOUD · the adapter schema (`s311-D7`): `adapters/schema.json`, `_validate_adapter.py` in `test_gates`, `adapters/sutherland-react.json` from the four `codeBindings` (unverified; `codeBindings` blocks stay). AC, 15:00 wave.
5. **F** · Opus · SEAT (the second slot), 12:30 → ~18:30 · F3 + F4 renders then F5 the page, in series. AC, 20:00 wave.
6. **E-build, E-replay** · Fable · CLOUD · wrap phase 3: E1+E2 in one lane (AC 15:00), E3+EV in one lane (AC 20:00); `knowledge/_tmp/` inputs staged from the seat. The wrap at 21:00 takes E's path if the replay is green on all three fixtures.
7. **C1** · Fable · CLOUD · the Launchpad catalogue on CS + C0 (`a4198fc3`, `5227ccc4`). AC, 15:00 wave. **C2 is DROPPED** (superseded by `s311-D9`: the renderer is emitter E1).
8. **V** · Fable · CLOUD, from 16:30 · one verifier for J, L, N, C1: PASS / PASS WITH FIXES / FAIL per job, filed before 20:00.
9. **The conductor** · push + CI read-back at each wave; the wrap seat opens 21:00; wrap landed by 22:30; Dave's short bulleted summary (Decisions / Outputs / Problems) after.

### Dropped, deferred
- DROPPED: C2 (the renderer spike).
- FRIDAY 2026-10-02 07:30, fresh week, same order as the briefs: A2–A6 + AV1/AV2; B1–B4, B6, B7, BV (B7's "showroom pane cannot project an option" item moves to phase 2); C3, C4, CV; D4 (on L1's sha), D5, DV; G1–G3, GV; H3 (Friday or later).
- LATER, per `s311-D9`: phase 2 (snippets regenerated, cohort one of five, behind `_validate_roundtrip.py`; recommended Saturday as a weekend run after Dave rules cohort one's trees); phases 3 and 4 (Lit, light DOM, wrappers; `_validate_apg_keys.py`, `_validate_wrappers.py`).

### Fuel
Eleven lanes (9 Fable, 2 Opus) plus the conductor and the wrap: about 6.2M sub tokens, about 10.5% of the all-models week (ending near 93%) and about 22.5% of the Fable week (ending near 80%). Stop lines 95% / 90%. If all-models reads 90% at 16:00, drop in order: V's check of C1, E-replay, L3's page.

### Still Dave's
The seven questions in § 5 below stand; F's page carries the ones a picture answers. New today: the five calls on the revised plan page; cohort one's fifteen trees, Friday.

---

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
