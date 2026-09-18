# `#286`-`T` — the seam's in-seat arm and `--quiet` on the commit script

session: `#286` · 2026-09-18
window: lane `T` (Opus, one lane)
sub index: `T`
brief: conductor's lane brief, in-session (no `notes/_briefs/` file cut for this lane)
tokens: `UNMEASURED — this lane's own transcript is not on the mount`. `_checkin.TRANSCRIPT_GLOB`
(`/sessions/*/mnt/.claude/projects/*/*.jsonl`) matches exactly ONE file and it is the
CONDUCTOR'S session (`f00a81c6-…`, first user record `"Good Morning!"`). A lane cannot read its
own `message.usage` from inside the sandbox, so this is an ABSENCE OF A MATCH, not a spend of 0.

## VERDICT

Both of #285's unbuilt moves are BUILT, to the record's spec, and both are green. `--quiet` on
`knowledge/_git_commit.sh` prints verdict lines only and writes the full transcript to a file;
default behaviour is unchanged, verified by diffing three read-only paths before and after (the
only delta is the script's own row in a `git status` listing). The seam's in-seat arm is a new
`INSEAT` block in `knowledge/_seam.py` — the conductor's own non-sidechain `tool_result` tokens
since the last seam, lane returns split out, warned above a PICKED 10,000 — printed between
`DISK` and `SCRATCH`, so `STANDING` is still LAST. The second cl100k counting site is registered
in `_capture_gate.py::MEASURERS['_seam.py']` and `unit_vocabulary_audit()` returns 0 failures.
`_checkin.py --window 200000 --no-block` still reports **6 STRUCTURAL fail(s)** — the inherited
six; no seventh. Nothing was committed, pushed, or generated.

COUNTS: findings `6` · ruling-shaped `3` · UNPROVEN `2`

## THE SPECS, QUOTED — what the record actually says

Both moves are #285's, carried unbuilt into #286 by `_HANDOFF-136…md` § #286 FIRST MOVES item 5:

> 5. **The seam's in-seat arm** and **`--quiet` on `_git_commit.sh`** — #285's moves 2 and 3, still
>    unbuilt; the commit ran as a lane today, which was the third of them.

Their bodies are in `_HANDOFF-135-the-logo-masters-land-and-the-disk-lever-is-found.md`
§ ⬛ #285 — FIRST MOVES, IN ORDER (lines 134–139), verbatim:

> 2. **THE SEAM'S IN-SEAT ARM** — `_seam.py` measures the conductor's own tool-output tokens since the
>    last seam and warns above a threshold. **One Opus lane.**
> 3. **`--quiet` ON `_git_commit.sh`** (verdict lines only) and **the commit run AS A LANE by default.**
>    **One Opus lane.**

The same file's § ⬛★★ THE DELEGATION LAPSE (lines 110–118) is the arm's WHY, verbatim:

> The conductor did lane work **IN SEAT four times** — the disk lever and its spec (~15K) · **SIX runs
> of the commit script (~30K)** · two screenshots read in-seat · the window research in-seat — **and
> only the drawing was a lane.**
> ★ **The one delegated lane cost the conductor's window about 300 tokens**, against 159,965 of quota.
> **The conductor's proposed mechanical fix, PROPOSED AND NOT BUILT:** `_seam.py` gains a **conductor
> in-seat tool-output arm** (tokens since the last seam, warned above a threshold) · the **opener
> states its routing** before the first beat · **the commit is a lane by default.** ⚠ **A conductor's
> proposal is not Dave's ruling.**

⛔ **GAPS IN THE SPEC, NAMED, NOT INVENTED** (all three are in RULING-SHAPED QUESTIONS below):
1. **The threshold has no number anywhere in the record** — `grep -rn "in-seat arm" notes/ *.md`
   returns `_HANDOFF-135` line 118, `_HANDOFF-136` line 204, `notes/_lanes/284/WRAP-MEMORY-HOOK.md`
   line 53 and `notes/_GAUGE-LOG.md` line 3712, and none of them states one. 10,000 is PICKED by
   this lane from #284's own measured numbers and says `PICKED` on the line it prints on.
2. **The spec does not say where in the seam the block goes.** It goes between `DISK` and
   `SCRATCH` because `_seam.py`'s own docstring forbids anything after `STANDING`.
3. **Half of move 3 — "the commit run AS A LANE by default" — was ALREADY DONE at #285**
   (`_HANDOFF-136` item 5: *"the commit ran as a lane today, which was the third of them"*), and it
   is a routing habit, not a line of code. This lane built the `--quiet` half only.
4. The record says nothing about whether a LANE'S RETURN counts as in-seat cost. This lane
   measures both and prints them separately rather than choosing for Dave (question 2).

## What was done

**A. `knowledge/_git_commit.sh` — `--quiet` (+61 / −4, `assets/…/git_commit.diff`).**
Three edits, no behaviour touched outside them:
- the USAGE header gained its line (the brief's requirement):

```
#   --quiet        VERDICT LINES ONLY on the terminal (#286, #285's move 3): the full transcript
#                  is written to a file and its path is printed. Gate chatter is filtered; a
#                  refusal, a gate fail and a non-zero exit are NEVER filtered — on any non-zero
#                  exit the WHOLE transcript is replayed to stderr. `--quiet=<path>` picks the
#                  transcript file. Works on every mode (--push / --selftest / --declare-dirt too).
```

- the block itself, immediately after `RECONCILED=0` so it covers `--push`, `--selftest` and
  `--declare-dirt` as well as the commit path (key hunk, comment elided):

```bash
QUIET=0; QUIET_LOG=""; QUIET_ARGS=()
for _a in "$@"; do
  case "$_a" in
    --quiet)   QUIET=1 ;;
    --quiet=*) QUIET=1; QUIET_LOG="${_a#*=}" ;;
    *)         QUIET_ARGS+=("$_a") ;;
  esac
done
QUIET_KEEP_RE='^(✗|⛔|⚠|✅|✓|— )|REFUS|FAIL|not clean|✗'
if [ "$QUIET" -eq 1 ] && [ -z "${GIT_COMMIT_QUIET_CHILD:-}" ]; then
  [ -n "$QUIET_LOG" ] || QUIET_LOG="outputs/_gitcommit-transcript-$(date +%s%N).log"
  echo "— --quiet: verdict lines only; FULL transcript → $QUIET_LOG"
  set -o pipefail
  GIT_COMMIT_QUIET_CHILD=1 bash "$0" ${QUIET_ARGS[@]+"${QUIET_ARGS[@]}"} 2>&1 |
    tee "$QUIET_LOG" | grep --line-buffered -E "$QUIET_KEEP_RE"
  QRC=${PIPESTATUS[0]}
  if [ "$QRC" -ne 0 ]; then
    echo "⛔ --quiet: the run exited $QRC — REPLAYING THE FULL TRANSCRIPT (quiet never hides a refusal):" >&2
    cat "$QUIET_LOG" >&2
  fi
  echo "— --quiet: $(wc -l < "$QUIET_LOG" | tr -d ' ') transcript lines at $QUIET_LOG · exit $QRC"
  exit "$QRC"
fi
```

- `--quiet|--quiet=*) ;;` added to the main argument `case` so a stray flag can never be taken
  for the msgfile or a path to stage.

⚠ **WHY A RE-EXEC AND NOT `exec > >(tee … | grep …)`:** a process-substitution filter on the
parent races the parent's exit and can TRUNCATE THE TAIL — and the tail is the sha line. The
re-exec takes the child's status from `PIPESTATUS[0]`, never from `grep` (which exits 1 when it
matches nothing). `outputs/` is gitignored, so the transcript never dirties the tree.

**B. `knowledge/_seam.py` — the INSEAT block (+213 / −7, `assets/…/seam.diff`).**
New: `INSEAT_WARN_TK = 10_000` (named PICKED), `INSEAT_STATE` (`outputs/_seam-inseat-state.json`),
`LANE_TOOLS = ("Task", "Agent")`, and the functions `_block_text()`, `inseat_scan()` (PURE — it
takes records and a marker, so every selftest arm drives it in memory with no file and no `/tmp`),
`inseat_tokens()`, `inseat_verdict()`, `_read_state()`, `_write_state()`, `find_transcript()`,
`inseat_block()`. Wired in `main()` as:

```python
    if not a.no_inseat:            # BEFORE scratch, and never after STANDING (see the docstring)
        print(inseat_block())
    print(scratch_line(clean=not a.no_clean))
```

The module docstring now says FIVE blocks and carries a THE INSEAT BLOCK section quoting #285's
move 2 and #284's measured lapse. `--no-inseat` suppresses the block AND leaves the marker where
it was. `find_transcript()` single-sources `_checkin.TRANSCRIPT_GLOB` rather than re-spelling it,
and returns `None` instead of `sys.exit`ing (`_checkin`'s own exit is right for a check-in and
fatal for an advisory seam).

**C. `knowledge/_capture_gate.py` — the ds-021 registration (the `_seam.py` entry only).**
⚠ `git diff --stat` on this file shows 49 changed lines because ANOTHER LANE is editing it this
session; the `MEASURERS["_seam.py"]` prose is this lane's only hunk in it
(`assets/…/capture_gate-SHARED-WITH-OTHER-LANES.diff`).

## Findings

1. **`--quiet` drops 92% of a commit run's gate output and keeps every verdict.** MEASURED, not
   asserted: each gate this script consumes was run alone, its output measured in cl100k, then
   filtered through the exact `QUIET_KEEP_RE`.
   `_capture_gate.py --wrap` **23,794 → 1,839** · `_validate_polarities.py --check` 754 → 20 ·
   `_build_live_state.py --selftest` 107 → 0 · `_gate_doc_rows.py` 63 → 14 ·
   `_gen_chain.py --check` 64 → 0 · `gen_showroom.py --check` 29 → 0.
   **TOTAL 24,811 cl100k → 1,873 kept, 92% dropped**, for ONE run. #284's six runs at ~30K is the
   number this makes affordable. Probe: `assets/…/gate-output-sizes.txt` and the inline python in
   this lane's log; raw gate outputs kept at `notes/_lanes/286/T/gate-*.out`.
2. **Default behaviour is unchanged — diffed, not reasoned.** The script has three read-only
   paths and all three were run before and after:
   `--selftest` → **byte-identical** (`diff` silent; `✓ selftest OK — 14 bites`).
   `--declare-dirt` and the no-`--reconciled` refusal → identical **except one added line,
   ` M knowledge/_git_commit.sh`**, i.e. the script's own dirty row in the `git status` listing
   those paths print. `diff <(grep -v '_git_commit.sh$' before) <(grep -v … after)` is silent for
   both. Files: `assets/…/{before,after}-{selftest,declaredirt,refusal}.out`.
3. **`--quiet` provably does not hide a refusal.** Driven on the refusal path
   (`bash knowledge/_git_commit.sh --quiet <msgfile>`, no `--reconciled`): rc **1**, the `✗
   refusing to stage` line streamed live, and the FULL transcript was replayed to stderr
   including all nine dirty paths (`assets/…/quiet-refusal.out`).
   ⚠ **AND THE HONEST COST:** on a SHORT refusal quiet is a NET LOSS — the same run measured
   **194 cl100k loud vs 468 quiet** (replay + two frame lines). Quiet pays off only on the long
   runs, which is precisely the design: the run nobody needs to read is the one it shrinks.
4. **The in-seat arm read a real number at its first run, and it is over the line.**
   `python3 knowledge/_seam.py --no-clean`, first run of this session (no marker yet):
   `INSEAT 36,829 cl100k own tool output since transcript start (no prior seam marker) · 18
   results (+3 lane returns, 1,110 cl100k) · ⚠ 36,829 in seat since the last seam, over the
   PICKED 10,000 — this is lane work being done in the seat (#284's lapse); ROUTE IT`.
   The split is the argument in two numbers, live and unprompted: **36,829 in seat against 1,110
   for three delegated lanes** — the same shape as #284's ~15K/~30K against ~300, now a reading
   rather than a post-mortem.
5. **The marker works.** The second run printed
   `INSEAT 0 cl100k own tool output since the last seam · 0 results (+0 lane returns, 0 cl100k) ·
   ✅ under the PICKED 10,000 in-seat line`, and
   `outputs/_seam-inseat-state.json` holds `{"transcript": "…f00a81c6….jsonl", "last_uuid":
   "7f422ca4-…"}`. ⚠ **THIS LANE MOVED THE CONDUCTOR'S MARKER TWICE** by running the seam — the
   conductor's next seam reads "since the last seam" from here, which is the mechanic working,
   not a defect, but it is named so nobody reads a small next number as a small session.
6. **No new structural gate fail.** `python3 knowledge/_checkin.py --window 200000 --no-block`
   after all three edits: `rehearsal [wrap-gate, early]: 6 STRUCTURAL fail(s)` — the inherited six
   (boot-drift ceiling breach + five `boot double-count` rows for #243/#264/#272/#273/#274), none
   of them mine. The only trace of this lane in that output is a WARN, and it is the registration
   receipt: `· CHANGED SINCE 2026-09-18 — ds-021 (C) DECLARED GAP — knowledge/_seam.py counts in
   cl100k and cannot name a REAL tier…`. File: `assets/…/checkin-after.out`.

### Receipts asked for by the brief

```
$ python3 knowledge/_seam.py --selftest
seam selftest: 15 arms, all GREEN                      # was 7; +8 INSEAT arms

$ python3 knowledge/_seam.py            # the run as specified (scratch IS cleaned)
FILL  138,556 real / 10 turns · boot 73,832 · ✅ 41,444 real under the 180,000 stop line
DISK  /sessions 0.4% · 9,643,780 KB free · ✅
INSEAT 0 cl100k own tool output since the last seam · 0 results (+0 lane returns, 0 cl100k) · ✅ under the PICKED 10,000 in-seat line
SCRATCH 8 own entries · removed 8/8
STANDING
Everything is delegated: the conductor orchestrates and judges; lane work done in-seat is a lapse (#57 / s204-D1, restated #284).
The four generators that undo hand-authored state — gen_kg_rules.py, land_rests_on.py, gen_kg_icons.py, _build_all.py single-process — never run without Dave's word (H-135 open 11).
Commits only through knowledge/_git_commit.sh, as a lane by default; push is the conductor's call with a CI read-back (H-135 move 3).
180,000 FILL is the QUALITY line and stands; 256,000 is not a wall for this model in Cowork (Dave's correction, #284).
Strike nothing from a carry without a receipt (s183-D1 / s188-D2).
Dave rules from plain prose and visuals, never ID codes; render readings side by side for a visual ruling (#66-D5, s172-D1).
Every sub files its full report at notes/_subreports/ (s218-D7).
A ruling is Dave's word inscribed; a proposal, a lane's finding or his enthusiasm is not one (s271-D4).
STANDING 8 lines · 246 cl100k
```

⚠ **STANDING IS STILL LAST** and the INSEAT block sits between DISK and SCRATCH, as the seam's own
docstring requires. ⚠ That run's `SCRATCH … removed 8/8` deleted eight top-level `/tmp` entries
belonging to this sandbox user — the seam's designed behaviour, and the reason this lane kept
every working file under `notes/_lanes/286/T/`.

**The ds-021 registration receipt (the new counting site):**

```
$ python3 -c "import sys; sys.path.insert(0,'knowledge'); import _capture_gate as g; \
              f,w = g.unit_vocabulary_audit('.'); print('FAILURES:', len(f))"
FAILURES: 0
WARNINGS naming _seam.py:
 - ds-021 (C) DECLARED GAP — `knowledge/_seam.py` counts in cl100k and cannot name a REAL tier.
   BORN #283 …; the FIRST COUNTING SITE was added at #285 …, the SECOND at #286 by lane T with
   the INSEAT block … `inseat_tokens()` encodes the CONDUCTOR'S OWN `tool_result` text … with
   tiktoken cl100k ONLY … the threshold it is judged against (`INSEAT_WARN_TK` = 10,000) is
   PICKED, NOT RULED … NEVER a FILL claim … Unavailable tiktoken makes the line read `?` …
```

The registry is per-FILE, so `_seam.py` needed no new key — but the entry named exactly one
counting site while the file now has two, which is the stale-pin shape this gate exists to
catch, so the entry declares the second explicitly rather than letting it ride.

```
$ git diff --stat knowledge/_seam.py knowledge/_git_commit.sh knowledge/_capture_gate.py
 knowledge/_capture_gate.py |  49 +++++++---      ← SHARED: another lane's 22 insertions included
 knowledge/_git_commit.sh   |  61 ++++++++++++-
 knowledge/_seam.py         | 220 +++++++++++++++++++++++++++++++++++++++++++--
 3 files changed, 312 insertions(+), 18 deletions(-)
```

## RULING-SHAPED QUESTIONS

1. **`INSEAT_WARN_TK = 10,000` is PICKED by this lane, not ruled — and nothing in the record
   states a threshold.** It sits between #284's two worlds (in-seat lane work ~15K and ~30K; the
   one delegated lane ~300). Option (a) keep 10,000 as a picked figure, reviewed after a session
   of readings; option (b) Dave names a number now; option (c) the arm prints the number with NO
   verdict until a line is ruled. Recommend (a): a picked line that says it is picked has been
   the project's own form since `DISK_WARN_PCT`, and one session of readings prices (b) honestly.
2. **Should a LANE'S RETURN count against the in-seat line?** It lands in the conductor's window
   like anything else, but it is the cost of DELEGATING — the behaviour the arm exists to reward
   (this session: 1,110 for three lanes against 36,829 in seat). Option (a) keep the current
   split — the verdict judges own-tool output only and the lane figure prints beside it;
   option (b) judge the sum. Recommend (a): (b) would penalise the routing it is meant to
   encourage.
3. **Is the arm ADVISORY forever, and is `--quiet` ever the DEFAULT?** The seam is advisory by
   Dave's standing (promotion is his), and `--quiet` is opt-in by construction. Option (a) leave
   both opt-in/advisory; option (b) make `--quiet` the default for an IN-SEAT commit only, with
   `--verbose` to opt out; option (c) promote the INSEAT verdict to blocking at some figure.
   Recommend (a) now and (b) only once the commit-as-a-lane habit is inscribed — a default that
   quiets a script the conductor should not be running in the first place rewards the wrong fix.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** `--quiet` on a FULL GREEN COMMIT RUN. The chain was stale from other lanes' work
  all session (`✗ _CHAIN.md is STALE` at every attempt) and this lane is fenced from committing,
  so the end-to-end path — T3 headline, staging list, sha line, the post-commit asserts — was
  never exercised under `--quiet`. The 92% figure in finding 1 is a per-gate measurement summed,
  not one observed green run. Price to prove: the next real commit run with `--quiet` (~0 extra
  tokens; the flag pays for itself).
- **UNPROVEN:** the INSEAT arm under COMPACTION. `inseat_scan()` falls back to "since transcript
  start" when the stored uuid is absent and says so on the line, and a selftest arm drives that
  path — but no live compaction was observed. Price to prove: one session that compacts.
- **CLAIMED:** that the transcript's non-sidechain `tool_result` blocks are exactly "the
  conductor's own tool output". Read from the live file's shape (18 `('user', False,
  'tool_result')` blocks, 22 `tool_use`, 0 sidechain records in this session), not from a
  documented schema. Re-read costs ~1K.
- **CLAIMED:** that `outputs/` is gitignored — read from `.gitignore` ("scratch render output
  (sandbox cannot unlink…)" → `outputs/`), and relied on by both the transcript file and the
  INSEAT state file.

## Evidence

`notes/_subreports/assets/2026-09-18-286-T-seam-inseat-and-quiet-commit/` —
`seam.diff` / `git_commit.diff` (this lane's full diffs) ·
`capture_gate-SHARED-WITH-OTHER-LANES.diff` (contains another lane's hunks too) ·
`before-/after-{selftest,declaredirt,refusal}.out` (the byte-identity probe for finding 2) ·
`quiet-selftest.out`, `quiet-refusal.out` (finding 3, including the stderr replay) ·
`gate-output-sizes.txt` (finding 1) · `seam-selftest.out`, `seam-run.out` (the receipts) ·
`checkin-after.out` (finding 6, the 6-not-7 line).
Working files, including the raw per-gate outputs and the two `--quiet` transcripts, are under
`notes/_lanes/286/T/`.

REPLAY-THESE: `notes/_subreports/assets/2026-09-18-286-T-seam-inseat-and-quiet-commit/seam.diff` (~2,600 tk — the new arm in full, if the conductor wants to check the placement claim itself) · `RULING-SHAPED QUESTIONS` above (~400 tk — all three need Dave's word, none is inscribed)
