# Lane B — #310 — the interim pressed value, and one review page: the white ink and the tab strip

Conductor: #310, Opus 5.5, cloud seat linked to Dave's Mac. You are an Opus 5.5 build lane. Dave rules by eye. You build, measure, render, and hand back ONE review page. You do NOT push.

## Read first
- Lane A's report: `notes/_subreports/2026-09-30-310-A-dark-tiles.md` (what the dark-tiles default and the `data-dark-tiles` option changed, and how it built them — reuse its drivers in `notes/_lanes/310/A/` and `outputs/310/A/`).
- Lane A's review page (your page's SHELL — copy it: styles, back link, Copy-as-text bar; new localStorage KEY and PATH): `notes/_REVIEW-310-A-dark-tiles-2026-09-30-v1.html`.
- Dave's words, verbatim: `notes/_lanes/310/DAVE-WORDS-2026-09-30-1624.md`. Quote them; never paraphrase.

## Job 1 — build `s310-D5` (small, first)
Supercharge's pressed and active tile states move to `#25211C` (they were `#13110E`, now the resting tile colour, so a press shows nothing). INTERIM: his words, "lets do that for now, I have some proper specs for this but cant access the figma files at teh moment". Build it at the source lane A found (token/theme source + generator, never by hand in canon.css), regenerate in order, and mark in the source's own note that the value is interim pending his Figma specs. Show it on the page as one small before/after (rest, hover, pressed, active). Then `python3 knowledge/_inscribe_ruling.py --set-status s310-D5 enacted --evidence-sha <sha>`.

## Job 2 — the white ink on black tiles (his item 2, verbatim: "we can avoid halation by choosing a different white ink maybe, of maybe we reverse the decision, I think we need a review of the options.")
A review of the options, each shown ALIVE on the banking demo's top (dark, Console, 1440, plus a 4x crop of a metric and a table row), text measured:
1. As built: black tiles, `#FFFFFF` text.
2. Black tiles, a softer white from the existing primitives (e.g. `--color-grey-100 #F3F3F3`, `--color-grey-200 #EDEDED`, `#D7D8D6`) — pick the two most sensible, name why.
3. The reverse (the `data-dark-tiles="grey"` option he already has): grey tiles on the black ground, white text.
4. Any other option the research turns up that uses only existing colours (e.g. a near-black tile from the palette) — only if it is real.
For each: the contrast of body text, secondary text, and both RAG inks against the tile (measured, WCAG ratio), and what it does to the secondary grey text (does it still pass 4.5 where it must?). Desk research on halation (dated, sources named in the Technical fold: why pure white on pure black blooms for astigmatic readers — Dave is astigmatic — and what published dark themes do). One call: which option, with your recommendation and one-clause reason.

## Job 3 — the tab strip in context (his item 3, verbatim: "I need to see this, it gets complicated when we have page backgrounds and bento sections")
Lane A found the tab strip now draws a black band on the dark page, where light draws no band. Show, for LIGHT and DARK, Console (plus Supercharge dark once), the Tabs component placed:
(a) directly on the page ground; (b) inside a bento section (the ground the dashboard uses); (c) inside a tile; (d) on a page with a section background (find the real snippets/templates that do this — Template-detail, Page-header-lockup, Template-dashboard-bento were named by lane A).
Each context in two readings: as built now, and "the strip takes its container's colour" (no band). If a third reading is real (a band only when the strip sits on a different surface than its panel), show it. Use real snippets composed the way Apollo composes them, not mock-ups; say which files. One call with a recommendation.

## Page
`notes/_REVIEW-310-B-white-ink-and-tab-strip-2026-09-30-v1.html`, sections: 01 the pressed value (done, look), 02 the white ink (call), 03 the tab strip (call), 04 anything else. Plain prose first in every section, the machinery in a Technical fold. Pictures inline `<img>` only — no `<a>` to PNGs (a dead end in the artifact). Keep it under ~25 pictures. Verify in context at 1440 and 390: no broken images, no side scroll, Copy as text returns every call.

## Checks, report
- Pre-push check (s309-D7, Worker checklist step 5 of `knowledge/_RUNBOOK-parallel-conductor.md`) on your commits in a /tmp clone, four chunks with `--include-mutating`, tests, evidence; the state-contrast sweep if you touched canon/snippets; chart receipts if canon changed. Fix any ❌/⏱ you caused.
- Report at `notes/_subreports/2026-09-30-310-B-white-ink-and-tab-strip.md` (COUNTS line first), with the doc rows the gate asks for.

## Seat mechanics (hard rules — same as lane A's brief, `notes/_lanes/310/A/BRIEF.md` § Seat mechanics; read it)
Everything via `mcp__remote-devices__device_bash` at `$HOME/mnt/Projects--UX-design`, `timeout_ms` ≤178000; renders `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh` with `executable_path=os.environ["RENDER_SHELL"]` and `goto("file://…")`; commits only `SESSION_N=310 bash knowledge/_git_commit.sh --reconciled --quiet <fresh msgfile, no T3 prefix> <paths>` with the two attribution lines (`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, `Claude-Session: https://claude.ai/code/session_01XRZhnwzLJQXjzvn972TQtm`); never `git status`; `python3 knowledge/_wrap_commit.py unlock --tag 310-B` after gate runs; no `rm`; no push; no Project memory. Budget ~90 minutes; if a step balloons, commit what is clean and report.

## Hand back
Plain prose, short: what is on the page for his eye, the two calls with your recommendations, the commits, the pre-push verdict, the page path, found-not-fixed.
