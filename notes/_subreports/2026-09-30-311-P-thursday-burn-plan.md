# #311 lane P — the Thursday burn plan: eight jobs, forty-eight lanes, three waves, on the record

COUNTS: jobs 8 · lanes 48 (Fable 21, Opus 5.5 24, Sonnet 3) · sub tokens est. 15.9M + ~2M conductor and wrap · all-models est. ~28% of the 36% left · Fable est. ~50% of the 76% left · store read 548 live (274 his, 274 mine) · rulings read 851, 450 with a `ruled` status, 42 of them s307, 30 s308, 20 s305 · carries residual → #311 read whole (333 items, ages 0–86) · draft briefs written 8 (`notes/_lanes/312/A..H/BRIEF.md`) · page verified 1440 and 390, no side scroll, Copy as text 10 of 10 calls

machinery: 0 (page builder, verifier and brief writer under notes/_lanes/311/P/)

REPLAY-THESE: `python3 notes/_lanes/311/P/build_page.py` · `python3 notes/_lanes/311/P/verify_page.py` (seat, after `ensure_env.sh` + `seat_env.sh`) · `python3 notes/_lanes/311/P/write_briefs.py`

## What landed

- `notes/_PLAN-311-thursday-burn-2026-10-01-v1.html` — the plan page in the #311-B review shell (localStorage key `plan-311-thursday-burn-v1`): 01 the day on one screen (SVG timeline of three waves, a fuel table with the derivation), 02 the eight jobs ranked with a Run-it-tomorrow call each, 03 what was left out, 04 the running order with the recommendation first. Ten calls; Copy as text returns all ten.
- `notes/_lanes/312/{A..H}/BRIEF.md` — a draft lane brief per job: the ask with every source cited, lanes × model with file ownership, Dave's one moment, done-when, and the common hard rules (no push, no `git status`, no `rm` in the mount, commits only through `_git_commit.sh` by the one commit seat, single-writer files named, pre-push routine, report form).

## The jobs, ranked (lanes × model · est. sub tokens)

1. A · the 78's work, wave one — 6 Opus build + 1 Opus commit seat + 1 Sonnet chores + 2 Fable verifiers · 3.3M. Source: `s307-D1..D78`, 42 still `ruled`; 38 open `W-307q*/y*` rows; `_CARRIES.md` residual → #311 age 3 (the proposed order).
2. B · the reworks from his picture page — 4 Fable rework + 1 Fable forks + 2 Opus + 1 Fable verifier · 2.6M. Source: `s308-D1..D15`, rows `W-308i1..i9`, `ia`, `ib`, `ic`; loose ends from `_HANDOFF-161` items 3 and 7 and the #311 A/B reports.
3. C · Launchpad, day one — 1 Opus schema + 1 Fable spec + 3 Fable build + 1 Opus renderer spike + 1 Fable verifier · 2.3M. Source: `s305-D45..D53`, `s305-D50` (October, once calls 14–19 are in the tree; `s305-D17`, `D18`, `D19`, `D58` still `ruled`), the v2 proposal's build path, the R5 probe.
4. D · the edge register items 5–9 and the consumers — 3 Opus + 1 Opus consumers + 1 Sonnet + 1 Fable verifier · 2.0M. Source: `s308-D20..D28`, rows `W-308ii`, `ij`, `ip`, `il`, `iq`, `in`, `ie`.
5. E · the wrap redesign phase 3 — 1 Fable design + 2 Opus build + 1 Opus replay + 1 Fable verifier · 1.7M. Source: `s306-D4`, `D5`, `D8`, `D9`, `D10`, row `W-305wr`, lane W1's table.
6. F · the pictures he is owed — 2 Fable explore + 3 Opus render/page · 1.7M. Source: `W-308iw`, `s308-D33` (held selftest), `W-305n2`/`s305-D59`, `W-305e1..e5`, `W-305w2`, the two token names, lane B's roundels, lane D's six.
7. G · the re-cut candidate — 1 Opus build + 2 Opus cold runs + 1 Fable judge · 1.3M. Source: `s309-D4`, `s307-D66`, `s308-D15`, `W-305v2`, the R4c harness.
8. H · Studio on paper — 2 Fable research + 1 Opus page · 1.0M. Source: the two #304 side-quest receipts (permutation matrix, Assembly/Studio modes). The first job to drop if the all-models line runs hot.

Running order (the recommendation): 07:30 A, B, D, E and C's schema and spec lanes; 12:30 first wave commit and push, verifiers for A and B, C's builds and D's consumers on the schema commit, F; 17:30 second wave commit, G on the last green sha, H in the cloud, verifiers for C, D, E; wrap at 22:00 so the wrap lands before the 23:00 reset.

## How the fuel was estimated (estimates, all of it)

Per lane: the `subs` line of `notes/_lanes/306..310/W/FACTS.json` averages 264k, 350k, 354k, 297k, 324k (largest 722k); the plan uses 330k. Per percent: this week's 64% bought 101 filed lane reports (`notes/_subreports/2026-09-25..30-*`) plus nine conductor windows, so about half a percent a lane with the conductor folded in; 10 of those reports were Fable's against 24% of the Fable week, so about 2.4% of it per Fable lane. Fable lanes count against both lines.

## Found, not fixed

1. The seat's own volume `/sessions` is 99% full (124M free; `df`), while `/` has 3.7G free and the repo is the Mac's disk through the FUSE mount (293G free). Writes into the repo are safe; writes into the seat home are not. `/tmp` is clear tonight (lane B's report said three clones stood; they are gone now).
2. The store's status stamps lag the tree: `s308-D16..D19`, `s308-D39..D44` and `s310-D2` are built and read `ruled`. Job A's chore lane stamps them with their shas after checking each.
3. `_wrap_carries.py` does not count `[NEW — 0]` items (`_AGE_RE`, #308 W report); job E's E2 lane fixes it on the way.
4. `s305-D50`'s condition (calls 14–19 in the tree) is not met tonight: D17, D18, D19 and D58 read `ruled`. The plan makes them the morning's first lane so the ruling's own start date can hold.

## Ruling-shaped questions

- The order for the 78's work (job A): the conductor's proposed order from #307 stands unless he says otherwise by 07:30. Put on the page as the one moment of job A.
- Whether the Launchpad PoC starts tomorrow or after the re-cut is out of the way: on the page as job C's second chip.
- Nothing else on the page needs his word before launch; every other moment is a review page at the end.

## Files

`notes/_PLAN-311-thursday-burn-2026-10-01-v1.html` · `notes/_lanes/312/A..H/BRIEF.md` · `notes/_lanes/311/P/{BRIEF.md,body.html,build_page.py,verify_page.py,write_briefs.py}` · this report. Screenshots under `notes/_lanes/311/P/shot-*.png` are scratch and are not committed.
