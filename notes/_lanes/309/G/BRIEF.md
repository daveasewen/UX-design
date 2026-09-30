# #309 lane G — his review answers: three rulings, three builds, three looks (Opus 5.5)

provenance: 309 · 2026-09-30 · conductor Opus 5.5 (cloud, linked to Dave's computer)
His answers, verbatim: `notes/_lanes/309/DAVE-RULINGS-2026-09-30-1104-metric-and-the-arrow.md`
The page he answered: `notes/_REVIEW-309-metric-and-the-arrow-2026-09-30-v1.html` (read its item text for each call).

## Where you work
Dave's computer, ONLY through mcp__remote-devices__device_bash; every command starts
`cd "$HOME/mnt/Projects--UX-design"`; ~170 s per call. Renders at the seat in ONE call:
`export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 <driver>`
with executable_path=$RENDER_SHELL, `goto("file://…")`, never `set_content()`.
Read first: lane D's report `notes/_subreports/2026-09-30-309-D-stat-card-to-metric.md`, lane C's
`notes/_subreports/2026-09-29-309-C-metric-and-reclass.md`, lane E's `notes/_subreports/2026-09-30-309-E-checks-at-the-seat.md`.

## A. Inscribe (through `knowledge/_inscribe_ruling.py`, entry → `--dry-run` → `--write`, lane I's shape
`notes/_subreports/2026-09-29-308-I-inscribe-15.md` line 15; answered BY CLICK on the page, so "by click";
quote his chosen label, the call's question and the recommendation verbatim from the page and the export)
- s309-D5 (6a): a metric may say "up is bad" — NOT the recommendation (which was keep direction only).
- s309-D6 (6b): the no-change mark is full ink, as ruled.
- s309-D7 (6c): every lane runs the pre-push check before handing back.
Item 2 (the arrow) is NOT answered — inscribe nothing for it. Items 3 and 5 are comments, not rulings: record
them verbatim as dated notes on the live rows they touch (or one new row each, owner claude, homed at the export
file) — his dark-mode tile colour note ("the background should be the darkest grey and the tiles black. Anyway this
is something we need to decide separatly") becomes ONE row, owner dave, "decide dark-mode ground and tile colour",
never built now. Also add the store row lane F's report lacked (it passed the commit gate on DOC_ROW_ACK).

## B. Build
1. s309-D6: Metric's no-change mark at full ink (it is 60% today). Stamp s309-D6 enacted with the sha.
2. s309-D5: Metric gains ONE optional setting that says "up is bad" (a rise takes the fall ink and a fall takes
   the rise ink; the arrow still points the way the number moved). Default stays direction. Name it in plain
   words in the meta (look at how Metric's other options are declared; reuse canon's RAG inks, no new colours).
   Do NOT switch any live page to it — which metrics are "up is bad" is Dave's content call. Render ONE Metric
   pair (default vs up-is-bad, a rise and a fall, light and dark) for his eye at `notes/_lanes/309/G/`.
3. s309-D7: write lane E's pre-push routine (drafted in its report) into the Worker checklist of
   `knowledge/_RUNBOOK-parallel-conductor.md`, BY ADDITION, citing s309-D7; plain and short, with the timings.

## C. Look, and say what you find (fix only what the move caused)
1. Banking demo: "the filters are stacking vertically here". Is that so before the move too (HEAD b690a19b) or
   only after? Find why (container width? a rule on the filter bar?). If the move caused it, fix it. If it was
   already so, report the cause and the likely fix in plain words — don't fix.
2. Receipt page (`dashboards/international-banking-dashboard.regen-v2-receipt.html`): (a) "the sparkline has
   become an area chart, but weird" — find what the trend slot draws there and why; (b) "I though we had a rule
   for the minimum items in a stat bar" — search the record (`python3 knowledge/_memento_search.py "<q>"`, the
   rulings, rules and metas: stats band / stat bar / KPI row minimum count) and quote what you find, or say plainly
   none exists; (c) "where has tall that blank space come from on the after" — find the cause. Fix what the move
   caused; report the rest. Render before/after of anything you change.

## Scope (s172-D3 (a), verbatim)
"Use the minimum complexity that solves the current task. No abstractions for hypothetical future
needs. No defensive code for scenarios that cannot occur here. Make the changes requested and those
clearly necessary to them — nothing else."
Dave's fence: "careful of externalities, I don't want to fix something only to break other constituent parts."
Report `machinery: <n> instrument / <n> feature`.

## Check before handing back — lane E's routine (s309-D7, now yours to follow)
Clone to /tmp, chunked survey `1:12`, `13:55`, `56:140`, `141:167` with `--include-mutating`, `test_gates`,
`_validate_evidence`, and the sliced state-contrast sweep if snippets or canon.css changed (regenerate the committed
audit from the full merged sweep, CI's fonts). Canon.css changes ⇒ re-drive the 27 chart receipts, all green.
If metas are added or removed ⇒ re-base ASSERT-009 (pattern `notes/_lanes/309/cond/assert009_rebase.py`).

## Traps
- ⛔ NEVER `git status`. After gate runs: `python3 knowledge/_wrap_commit.py unlock --tag 309-G`.
- ⛔ No-op `git add` strands the lock. Name only changed paths; under ~30 a commit.
- ⛔ Commit ONLY via `SESSION_N=309 bash knowledge/_git_commit.sh --reconciled <msgfile in knowledge/_tmp/> <paths…>`.
  Include `notes/_lanes/309/DAVE-RULINGS-2026-09-30-1104-metric-and-the-arrow.md` and this brief in your first commit.
  Do NOT push.
- ⛔ `gen_kg_sources.py` is outside the regen serial: `--check`, then `--land --ratified s305-D26` after meta changes.
  `_wrap_regen.py --checks-only --session 309` names what's stale (ignore `_gen_titles`); run write forms in order.
- ⛔ Survey in the /tmp clone, not the mount (it appends to `notes/_BUILD-VERDICT-LOG.jsonl`).
- ⛔ Never `git checkout` a shared directory; keep JSON formatting; no `_build_all.py`; no Project memory; don't ask Dave.
- Clean `outputs/309/G/` and /tmp clones at the end.

## Report
`notes/_subreports/2026-09-30-309-G-review-answers.md` (with a `COUNTS:` line), committed.
Reply to the conductor in under 300 words: rulings inscribed, what was built and its proof, the up-is-bad render
path, each of the four looks (cause, before-or-after-the-move, fixed or not), the pre-push result, commit hashes.
