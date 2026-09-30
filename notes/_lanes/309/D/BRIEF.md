# #309 lane D — the stat card pages move to Metric, the arrow in the right RAG ink (Opus 5.5)

provenance: 309 · 2026-09-30 · conductor Opus 5.5 (cloud, linked to Dave's computer)
Dave's words, verbatim (`notes/_lanes/309/DAVE-WORDS-2026-09-30-0707.md`):
"1. Moving to metric is probably a good idea but the arrow must be the the right RAG ink"
"2. We'll recut towards the end of the week"

## Where you work
The repo is on Dave's computer, reached ONLY through mcp__remote-devices__device_bash. Every command starts
`cd "$HOME/mnt/Projects--UX-design"`. Each call is a fresh shell, ~170 s cap; split long jobs into steps that
leave files behind. Rendering at the seat, ONE call per render: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh;
source knowledge/_render/seat_env.sh; python3 <driver>` with executable_path=$RENDER_SHELL; `goto("file://…")`,
never `set_content()`.

Read first: lane C's report `notes/_subreports/2026-09-29-309-C-metric-and-reclass.md` (what Metric is, why the
stat card snippet was left alone: the #227 banking demo measured by two gates, the progress dashboard, the receipt
tests built on `.cn-stat-card`), lane E's report `notes/_subreports/2026-09-30-309-E-checks-at-the-seat.md`
(the sliced state-contrast sweep, hit-area at the seat, and the pre-push routine you MUST follow), and
the rulings on red and ink (search: `python3 knowledge/_memento_search.py "two reds RAG ink carriers"` →
`--fetch`; s151-D1 two-red law, s149-D1 mono error ink camp, s308 opener "The red is correct for Supercharge and
Common, the black is correct for console and mono").

## Pieces, in order
1. INSCRIBE his two answers through `knowledge/_inscribe_ruling.py` (entry file, `--dry-run`, then `--write`), in
   lane I's shape (`notes/_subreports/2026-09-29-308-I-inscribe-15.md` line 15), answers given in chat, words
   verbatim, the item they answered quoted from the words file:
   - s309-D3: the stat card pages move to Metric, and the trend arrow must be the right RAG ink.
   - s309-D4: the designer pack is re-cut towards the end of the week (not now).
2. FIND THE RIGHT RAG INK before building. Establish from canon and the rulings, and write down in the report
   with sources: which ink the trend arrow takes for a good change, a bad change and no change, in every theme
   and both modes; whether "good" follows direction or the metric's sense (a cost going up is bad) if canon
   says so; and what the stat card and Metric each do today. If canon does not settle it, STOP piece 3 and
   report the question in plain words with the options — that is Dave's call.
3. MOVE every page, demo and receipt test built on `.cn-stat-card` to Metric, the arrow in that RAG ink.
   Change sources; let generators write outputs; never hand-edit a generated file. Every figure on a page comes
   from canon, never a specimen. Retire the stat card's own drawing only if nothing still needs it; the
   `stat-card` alias must keep resolving to Metric. Re-drive any receipts the change touches (the 27 chart
   receipts if canon.css changes) and every one must read green.
4. RENDER BEFORE AND AFTER for Dave's eye: each moved page, before (HEAD before your work) and after, side by side,
   light and dark, at 1440, one PNG per page, saved at `notes/_lanes/309/D/`. Crop in on the arrows too.
5. CHECK BEFORE HANDING BACK, by lane E's pre-push routine: clone to /tmp, the chunked survey `1:12`, `13:55`,
   `56:140`, `141:167` with `--include-mutating`, `test_gates` and `_validate_evidence`, plus the sliced
   state-contrast sweep (snippets change). The committed `knowledge/_STATE-CONTRAST-AUDIT.md` covers only 3
   snippets since lane C's partial run — regenerate it from the full merged sweep, as CI writes it (CI's fonts
   if the result must byte-match CI). Report every red, and which are seat-only.

## Scope (s172-D3 (a), verbatim)
"Use the minimum complexity that solves the current task. No abstractions for hypothetical future
needs. No defensive code for scenarios that cannot occur here. Make the changes requested and those
clearly necessary to them — nothing else."
Dave's fence: "careful of externalities, I don't want to fix something only to break other constituent parts."
If a gate goes red and you cannot make it green again, stop at the last green commit and report.
Report `machinery: <n> instrument / <n> feature`.

## Traps (each has bitten on this mount)
- ⛔ NEVER `git status`. After every gate run: `python3 knowledge/_wrap_commit.py unlock --tag 309-D`.
- ⛔ A no-op `git add` strands `.git/index.lock`. Name only paths that differ from HEAD. Under ~30 paths a commit.
- ⛔ Commits ONLY via `SESSION_N=309 bash knowledge/_git_commit.sh --reconciled <msgfile> <paths…>`
  (message file in the gitignored `knowledge/_tmp/`). Do NOT push.
- ⛔ `gen_kg_sources.py` is not in `_wrap_regen.py`'s serial: after meta changes `--check`, then `--land --ratified s305-D26`.
  After records change, `_wrap_regen.py --checks-only --session 309` names what is stale (ignore `_gen_titles`, a wrap step);
  run the write forms in its order.
- ⛔ If component metas are added or removed, ASSERT-009 in `knowledge/_assertions.json` must be re-based in the
  same change (pattern: `notes/_lanes/309/cond/assert009_rebase.py`) — lane C's skip turned CI red.
- ⛔ A `_build_survey.py` run on the mount appends to `notes/_BUILD-VERDICT-LOG.jsonl`; restore it from HEAD
  before any regen. Survey in the /tmp clone instead.
- ⛔ Do NOT run `_build_all.py`. CI caps each survey step at 60 s. Never `git checkout` a shared directory.
- ⛔ Keep each JSON file's own formatting when writing back. Do NOT read or write Project memory. Don't ask Dave.
- Clean `outputs/309/D/` and any /tmp clone at the end (deletion is enabled this session).

## Report
File `notes/_subreports/2026-09-30-309-D-stat-card-to-metric.md` (with a `COUNTS:` line), commit it.
Reply to the conductor in under 300 words: the RAG ink rule you found and its sources, the pages moved, the
before/after PNG paths, the pre-push check result (reds, seat-only or real), commit hashes, what stayed open.
