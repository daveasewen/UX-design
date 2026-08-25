# `#218`-`cA` — filed-sub-report machinery (`s218-D7`) + the frozen itinerary column

session: `#218` · 2026-08-25
window: `#218 crank conductor window`
sub index: `cA`
brief: `notes/_briefs/2026-08-25-218-filed-reports-and-column-brief.md`
tokens: `UNMEASURED` — this seat has no `message.usage` reader. The platform counter fell
`14,966,688 → 14,782,331` across the lane (**184,357**), which is CUMULATIVE per-turn cost —
quota-shaped, not window FILL. Reported as what it is, not converted
[[measure-dont-convert-units]].

## VERDICT

**BOTH HALVES DONE, every new check red-arm driven before it counted.** Half 1 ships the fenced
directory + skeleton, the doc-row gate widened to `notes/_subreports/*.md`, a new ADVISORY wrap
check (`subreport_citation_check`) with 9 arms including the planted-uncited-report red, and the
runbook addition. Half 2 renames the frozen column at the writer, emits a fresh **v4** snapshot
beside an untouched v3, and fixes both code consumers — one of which the rename would have broken
*silently and in the shape of a green*. **Two things need the conductor before this is closed:**
the emitted field name deviates from the brief's literal string on a wrong fence date (finding 1,
question 1), and this report has no `_state.json` row (finding 5) because the store is fenced
from this seat. Everything is uncommitted.

COUNTS: findings 7 · ruling-shaped 4 · UNPROVEN 3

## What was done

**Half 1 — `s218-D7`**

| # | region | file |
|---|---|---|
| 1 | the fenced directory + skeleton | `notes/_subreports/_TEMPLATE.md` (new) |
| 2 | doc-row gate glob widened | `knowledge/_gate_doc_rows.py` |
| 3 | the wrap citation check | `knowledge/_capture_gate.py` |
| 4 | runbook addition | `knowledge/_RUNBOOK-capture-ritual.md` |

- **The skeleton** carries the header block (session · window · sub index · brief pointer · token
  spend), VERDICT, the parsed COUNTS line, a mandatory **RULING-SHAPED QUESTIONS** section, an
  **UNPROVEN / CLAIMED** section naming ADR-0016 by name, an Evidence section pointing at
  `notes/_subreports/assets/<report-stem>/`, and the priced **REPLAY-THESE** line. It states in
  its own prose that the FILE is sole authority and stub figures are copied off it, that evidence
  never goes to session scratch, and that reports are dated history under ADR-0017.
- **Gate A** (`_gate_doc_rows.py`): one `in_population()` membership test now serves both the
  committed scan and the staged scan — two copies would drift, and drift there fails OPEN. The
  glob is deliberately narrow: flat, `.md` only, `_TEMPLATE.md` exempt by name, `assets/**` is
  evidence not a document. Four negative controls in the selftest hold it there.
- **Gate B** (`_capture_gate.py` → `subreport_citation_check`): a report filed since the last
  capture-ritual commit (`after #<n>`) that this session's own record does not name **by path**
  warns. It also PARSES each report's `COUNTS:` / `REPLAY-THESE:` lines and its `RULING-SHAPED
  QUESTIONS` heading — the stub's figures are copied off those lines, so an unparseable line
  means the stub's numbers came from somewhere else [[no-gate-parses-the-artefact]]. Wired in
  `wrap_checks()` above the `if lane:` split, so it runs for lane wraps too. **ADVISORY AT
  BIRTH**, tier at `SUBREPORT_CITE_BLOCKING = False`; not promoted.

**Half 2 — the frozen column** (`knowledge/gen_itinerary_status.py`)

- `FROZEN_STATUS_KEY = "itinerary_status_2026_07_14_FROZEN"` replaces the bare
  `itinerary_status` in every emitted row; `frozen_status()` is the ONE reader, imported by the
  consumers rather than re-typed, and it spans both eras (v1–v3 keep the old name) and REFUSES on
  a row carrying neither.
- `$caveat` names the class in full, with both misreads (#203, #218) and their counts; a new
  `$columns` block states per-field what is history and what is the live fact.
- HTML column headers changed from `Itinerary` / `Itinerary says` to `FROZEN 2026-07-14 cell` +
  `MEASURED derived`, so the surface speaks the same grammar as the field.
- `STAMP` → `2026-08-25-v4`, `SESSION` → `#218`, `MEASURED` → `2026-08-25`, `PRIOR` → v3. Emitted
  `reviews/ITINERARY-STATUS-2026-08-25-v4.{html,json}`; **v3's bytes are untouched** (`git status
  reviews/` shows two `??` adds and no `M`).

**Declared side-effect, for the worktree reconcile.** `notes/_REHEARSAL-LOG.jsonl` shows as
modified. That is not an edit — `_capture_gate.py` appends a machine line to it on *every*
wrap-mode run, and this lane ran `--wrap` once (to drive gate B live) plus the selftest suite. It
is the one tracked file the verification instruments themselves write, which is exactly why
`s137-D1` excludes it from the `--push` clean-tree assertion. Named so no path in `git status` is
unaccounted for.

## Findings

1. **The brief's fence date names a day the column does not come from.** The brief and the
   lane-α receipt that proposed the fix both write `itinerary_status_1907_FROZEN`. The source
   workbook is `reviews/ITINERARY-2026-07-14-apollo-component-library.xlsx`; the generator's own
   docstring says *"It was written 2026-07-14"*; the brief's own half-2 opening says *"the
   2026-07-14 spreadsheet cell"*. `1907` is not that date. Since the brief's stated mechanism is
   *"the date in the name is the fence"*, a fence carrying the wrong date is the same defect one
   level down, so the emitted name uses the full unambiguous snapshot date:
   **`itinerary_status_2026_07_14_FROZEN`**. ⬛ DECLARED, NOT RULED — one constant
   (`FROZEN_STATUS_KEY`) is the only place that changes if #218 wants the literal string. See
   question 1.
2. **The rename would have broken the gamma verifier silently, and in the shape of a green.**
   `knowledge/_render/verify_wave3_gamma_218.py` reads the *newest* register by design
   (`newest_register()`, which explicitly refuses to pin v3), so it picked up v4 the moment it
   existed. Its old reader was `r.get("itinerary_status")`. **Driven counterfactual on the real
   v4 bytes:** legacy-name hits on v4 = `0`; `sum(r.get("itinerary_status") == "Gap")` = `0` vs
   `78` under the new key. At 0, gate G4's clause *"the frozen and measured columns no longer
   disagree … RETIRE this gate"* fires — the gate would have announced its own defect as
   RESOLVED. Fixed by importing `frozen_status`; gamma now runs green against v4 (all four rows,
   `frozen column reads Gap on 78 rows`).
3. **`gen_itinerary_status.py` has no consumer in `_build_all.py`.** `grep -n "itinerary"
   knowledge/_build_all.py` → **no hits**. Its `--check` (built to be meaningful — both outputs
   are deterministic) is never run by the build, which is why v3 sat four days stale while three
   receipts described it as current. Pre-existing, not created here; priced in question 3.
4. **`_capture_gate.py --selftest` is RED in this tree, and it is NOT mine.** The single failure
   is `#70/#71 non-catch: _gen_chain.py --selftest is NOT green`. Chased to its cause: the
   failing bite is `_gen_chain`'s own *"is materially smaller than GOOD-MORNING.md (30,494 vs
   75,342 tape, <40%)"* — the chain is **40.5%** of GM, just over the pin. `_gen_chain.py`,
   `GOOD-MORNING.md`, `_LIVE-STATE.md` and `_CHAIN.md` are all outside this brief's regions and
   were not touched (`git status` confirms). With that one arm excluded, every other arm of the
   capture-gate selftest passes, including all nine new ones.
5. **This report has no `_state.json` row, and the doc-row gate cannot see it yet.** Two separate
   facts. (a) Store edits are on this seat's fence, so no row was minted — the #185 class,
   declared exactly as the α/β/γ lanes declared it. (b) The gate's population is COMMITTED +
   STAGED (`git diff --cached`); an *untracked* file is invisible to it. So `--check` reads PASS
   today and will flag this report the moment the conductor runs `git add`. The fix is one
   `_state.add()` — and a single **directory home `notes/_subreports/`** rows every future report
   at once (the #215 directory-address clause, already proven by the selftest's directory-arm).
6. **The field name has exactly three code consumers; every other hit is prose.** `grep -rln
   itinerary_status --include=*.py --include=*.js --include=*.html --include=*.json` returns 9
   paths. Code: `gen_itinerary_status.py` (the writer), `verify_wave3_alpha_218.py` (pins v3 —
   fixed anyway, so repointing it cannot KeyError), `verify_wave3_gamma_218.py` (finding 2).
   `verify_wave3_beta_218.py` names the field only in a docstring sentence about v3, which
   remains true of v3 — left alone. The rest (`_state.json`, `_memento-index.json`,
   `_instrument-fit.json`, `transaction-row.meta.json`, `MEMENTO-SCHEMATIC-…v2.html`, the
   receipts) are prose/history: write-once, deliberately not rewritten.
7. **v3 is intact and still readable.** `v3` carries the legacy key on all 124 rows and its bytes
   are unchanged; `frozen_status()` reads it. The generator's arm 7 asserts both directions —
   including that a row carrying NEITHER key raises rather than returning `None`, because a
   silent `None` here is the original misread in a new costume.

## RULING-SHAPED QUESTIONS

1. **The frozen field's name.** (a) `itinerary_status_2026_07_14_FROZEN` — shipped; the fence
   date matches the snapshot, unambiguous, ~0 to keep. (b) `itinerary_status_1907_FROZEN` — the
   brief's literal string; one constant + one re-emit (~5 min), but inscribes a date the column
   does not come from into every future JSON. (c) `itinerary_status_1407_FROZEN` — the brief's
   shape with the right day, but `1407` still reads as a time or a year to a cold reader.
   **Recommend (a).** ⛔ Whichever is chosen, changing it AFTER v4 is committed means a v5:
   emitted snapshots are write-once.
2. **Promotion of the citation check from ADVISORY to BLOCKING.** Dave's word only, and
   deliberately not taken here. The line is `SUBREPORT_CITE_BLOCKING` in `_capture_gate.py`. The
   honest argument for waiting: it has never yet run at a real wrap, so its false-fire rate on
   live receipts is unmeasured — the #111/#161/#163 pattern (warn provisionally, ratify, flip)
   applies exactly.
3. **Should `gen_itinerary_status.py --check` be wired into `_build_all.py`?** (a) Wire it —
   the stamp-drift becomes visible the day it happens, ~20 min. ⚠ Consequence, stated: the build
   goes red every time the working tree gains a snippet before the generator is re-run, which is
   *routine*, and a gate that reds on normal work gets muted rather than fixed. (b) Wire it as
   ADVISORY only. (c) Leave it manual and accept that a snapshot ages silently — the status quo
   that produced finding 3. **Recommend (b).**
4. **Should the doc-row gate see UNTRACKED files, not just committed + staged?** Today a report
   filed and never staged is invisible to it (finding 5b) — the same *"the gate could only ever
   fail on the commit AFTER"* shape the #207 postscript already fixed once. Widening is ~10 lines
   (`git ls-files --others`). ⚠ Consequence: every scratch `.md` a session drops in
   `notes/_briefs/` starts failing the gate before the author has decided to keep it. This is a
   scope PICK like `BASELINE_DATE`, which the gate's own docstring says is Dave's.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN — the citation check has never run inside a real `--wrap` at a real wrap.** It was
  driven directly on the live tree and through 9 selftest arms on a real git fixture repo,
  including a live `--wrap` run with this report present (below). What is *not* established is
  its behaviour across a full ritual where the receipt is written mid-run. Price to prove: the
  conductor's own wrap, zero extra.
- **UNPROVEN — the BLOCKING path.** `SUBREPORT_CITE_BLOCKING = True` was never driven; the
  promotion is Dave's and driving it would have been rehearsing a ruling. Price: one selftest arm
  (~10 min) at promotion time, not before.
- **UNPROVEN — the v4 HTML was not RENDERED.** The two `<th>` changes are markup-only and were
  verified as strings in the emitted bytes, not in a browser; no four-theme × light/dark pass, no
  responsive check at 480/720. Correct for the change made (a header relabel), but stated so it
  is not read as a visual pass. Price: one render matrix if wanted.
- **CLAIMED, not re-read: the `78 Gap` / `1 GAP` figures in `$caveat`.** They come from
  `notes/_receipts/2026-08-25-wave3-gamma.md` and were re-derived from the live v4 emission
  (`frozen column reads Gap on 78 rows`, `measured GAP total = 1`), so they hold as of today's
  measurement — but they are properties of a MOMENT and will move with the store
  [[conclusions-are-debt-s129-d5]].

## Evidence

`notes/_subreports/assets/2026-08-25-218-cA-filed-reports/` —
- `counterfactual-v4-old-reader.txt` — the driven proof of finding 2 (0 vs 78).
- `wrap-mode-citation-live.txt` — the live `--wrap` excerpt showing this very report warned as
  UNCITED before the conductor cites it: the check firing on a real, unplanted case.
- `selftest-arms.txt` — the green runs of all three touched selftests plus the mutation that
  proves the generator's arm 7 can go red.

REPLAY-THESE: `notes/_subreports/2026-08-25-218-cA-filed-reports.md` findings 1–2 and questions
1–4 in full (~2,400 tk) · `knowledge/gen_itinerary_status.py` §`FROZEN_STATUS_KEY` block if
question 1 is answered anything but (a) (~600 tk) · `knowledge/_capture_gate.py`
§`subreport_citation_check` header comment before any promotion decision (~900 tk)
