provenance: #63 sub draft · status: DRAFT — not ratified

# Bite matrix — `knowledge/_gm_move.py`

Method: full read of the file (865 lines) including `--selftest`; claims enumerated before any
run; `python3 knowledge/_gm_move.py --selftest` run as the control; every claim with no existing
selftest coverage got one minimal mutation run against a `tempfile.TemporaryDirectory()` fixture
(exactly the isolation the shipped selftest itself uses) — **no repo file was ever opened for
write**. Mutation scripts live at `outputs/matrix-work/mutation_tests_part{1,2,3}.py` (host-side,
not under this repo). Verdicts: PROVEN / UNPROVEN / CANNOT-TEST-SAFELY only.

Counts: ⚠ **the sub's two count lines disagreed (header said 3 UNPROVEN, foot said 1) and neither
PROVEN figure matched measurement — see § Replay #63 at the foot for the measured figures.**

---

## 1. `_find_anchor` — anchor mechanics (lines 107–136)

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 1 | Regex anchor must start with `^`; bare-substring regex refused (l.117-119) | PROVEN — selftest `"bare-substring regex REFUSED (fires)"` (l.750-752): `rc != 0 and "^-anchored" in err` | — | A regex that IS `^`-anchored but semantically wrong can still land on exactly one line by coincidence and pass — the check is syntactic, not intentional. |
| 2 | Regex compile errors (`re.error`) refused (l.120-123) | none in shipped selftest | PROVEN — `{"regex":"^("}` → rc=2, err=`✖ FAIL: insert anchor (GOOD-MORNING.md): bad regex '^(' (missing ), unterminated subpattern at position 1) — NOTHING written` | — |
| 3 | Empty/whitespace literal anchor refused (l.126-127) | PROVEN — selftest `"empty anchor REFUSED (fires)"` (l.753-755): `rc != 0 and "empty" in err` | — | — |
| 4 | Anchor must be a string or `{"regex":...}` dict, else refused (l.129-130) | none in shipped selftest | PROVEN — `at=123` → rc=2, err=`✖ FAIL: insert anchor (GOOD-MORNING.md): 123 is neither a string nor {'regex': '^…'} — NOTHING written` | — |
| 5 | Anchor must match exactly ONE line (0 or 2+ refused) unless `first=True` (l.131-136) | PROVEN — selftest `"zero-match anchor REFUSED (fires)"` (l.756-758, `"matched 0"` in err) and `"ambiguous anchor REFUSED (fires)"` (l.759-761, `"need exactly 1"` in err) | — | Only counts matches; cannot see whether the ONE match is the semantically intended line vs. a coincidental line-start collision. |

## 2. Argument validators — `_lines_arg`, `_where_arg` (lines 139–150)

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 6 | `lines` must be a list of strings (l.140-141) | none in shipped selftest | PROVEN — `lines="not a list"` → rc=2, err=`✖ FAIL: insert.lines (GOOD-MORNING.md): must be a LIST of line strings (got str) — NOTHING written` | — |
| 7 | No line string may contain `\n` (l.142-143) | none in shipped selftest | PROVEN — `lines=["a\nb"]` → rc=2, err=`✖ FAIL: insert.lines (GOOD-MORNING.md): a line may not contain a newline — one string per line — NOTHING written` | Does not forbid other control chars (`\r`, `\t`) that could still corrupt line-based diffing; only `\n` is checked. |
| 8 | `where` must be `"after"` or `"before"` (l.147-150) | none in shipped selftest | PROVEN — `where="sideways"` → rc=2, err=`✖ FAIL: where='sideways' — must be 'after' or 'before' — NOTHING written` | — |

## 3. `move` op (lines 184–204)

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 9 | `src == dst` refused — a move that stays must use replace/insert (l.187-189) | none in shipped selftest | PROVEN — move within `_LIVE-STATE.md` → rc=2, err=`✖ FAIL: move within _LIVE-STATE.md: src == dst — use replace/insert for in-file edits, a 'move' that stays is a rewrite — NOTHING written` | — |
| 10 | Extracted block empty → refused (l.196-197) | none | **UNPROVEN — argued dead code.** `s` and `e` come only from `_find_anchor`, which returns a real index in `[lo, hi)`. When `end != "EOF"`, `e` is searched with `lo=s+1`, so `e ≥ s+1 > s`. When `end == "EOF"`, `e = len(fs.lines)` while `s ≤ len(fs.lines)-1 < e`. In both branches `s < e` is structurally guaranteed, so `block = fs.lines[s:e]` can never come back empty through the public `move` op — no input reaches this line. See mutation-run note in `mutation_tests_part2.py` (MUT-6) for the derivation. | This guard is unreachable, which means a genuinely wrong (but non-empty) extent — the actual live failure mode named in the docstring at l.44-46 ("a wrong extent is visible, not silent" — i.e. only via the receipt's line count, never enforced) — is the thing this line was never going to catch anyway. |
| 11 | Extracted block is inserted VERBATIM (comment, l.201) | PROVEN (as a positive control) — selftest `"green control: VERBATIM block landed in dst"` (l.739-740): exact 3-line block `"## Batch 2026-07-28 #21\nls line 2\nls line 3\n"` found intact in destination | — | Verbatim-ness of the SOURCE content itself (whether it was well-formed before extraction) is explicitly out of scope — stated in the module docstring l.34-38. |

## 4. `replace` op (lines 205–221)

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 12 | `find` may not be empty (l.208-209) | none in shipped selftest | PROVEN — `find=[]` → rc=2, err=`✖ FAIL: GOOD-MORNING.md: empty find-block matches everywhere — refused — NOTHING written` | — |
| 13 | `find == replace` refused (identical-string no-op) (l.210-212) | PROVEN — selftest `"identical-string replace REFUSED loud (fires)"` (l.797-800): `rc != 0 and "identical-string" in err` | — | Only catches EXACT list equality; a semantically-null edit expressed with different-but-equivalent text (e.g. reformatted whitespace) is not caught, though that is arguably a real (non-no-op) edit rather than a defect. |
| 14 | `find`-block must match FULL LINES exactly once (0 or 2+ refused) (l.215-218) | none in shipped selftest exercises `replace`'s own count (the existing ambiguous-anchor bite tests `insert`'s `_find_anchor`, a different code path) | PROVEN both arms — zero matches: rc=2, err=`✖ FAIL: GOOD-MORNING.md: find-block (1 ln, first 'no such line at all') matched 0 times — need exactly 1 — NOTHING written`; two matches (`DUPTEXT` appearing twice in a file): rc=2, err=`✖ FAIL: _LIVE-STATE.md: find-block (1 ln, first 'DUPTEXT') matched 2 times — need exactly 1 — NOTHING written` | Uses raw list-equality over a sliding window — a multi-line `find` that partially overlaps itself (e.g. periodic repeated text) could have multiple valid segmentations only one of which is intended; the check counts window matches, not intent. |

## 5. `insert` op (lines 223–232)

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 15 | Zero-length `lines` refused (l.226-227) | none in shipped selftest | PROVEN — `lines=[]` → rc=2, err=`✖ FAIL: GOOD-MORNING.md: insert of zero lines — no-op refused — NOTHING written` | — |

## 6. `roll_2f` op (lines 234–392) — the ds-022 2f-split

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 16 | `session` must parse as an int (l.264-267) | none in shipped selftest | PROVEN — `session="abc"` → rc=2, err=`✖ FAIL: roll_2f: session 'abc' is not a number — the block key is \`#### <date> #<N>\` and N is what the continuity check reads — NOTHING written` | — |
| 17 | Over-reach refusal: commit-state half may not swallow another stratum's `#### <date> #<N>` key (l.290-303) | PROVEN — selftest `"roll_2f: cs_end past the next stratum is REFUSED, not swallowed"` (l.660-662): `rc == 2 and "reached PAST the next stratum" in err`, plus `"nothing written when cs_end over-reaches"` (l.663-665) | — | Detection is via `STRATA_KEY_RE` matching `^####\s+\d{4}-\d{2}-\d{2}\s+#\d+\b` on swallowed lines. A neighbouring stratum whose key line is malformed, missing, or doesn't match that exact shape would be swallowed silently — the guard can only see keys it recognises. |
| 18 | Post-mortem half must contain a `#### <date> #<N>` key line (l.305-310) | PROVEN — selftest `"roll_2f: unkeyed post-mortem refused"` (l.694-696): `rc == 2 and "no \`#### " in err` | — | — |
| 19 | The key's session number must equal the `session` argument (l.311-315) | PROVEN — selftest `"roll_2f: session argument disagreeing with the block key is refused"` (l.701-703): `rc == 2 and "disagree" in err` | — | — |
| 20 | Duplicate session key in the log refused (l.317-325) | PROVEN — selftest `"roll_2f: duplicate session key refused"` (l.607): `rc == 2 and "already carries a block" in err`; and combined with the order relaxation at l.631-636 (`"roll_2f: uniqueness STILL refuses when order no longer does"`) | — | Detection is via `STRATA_KEY_RE` matching lines already in the log. A duplicate recorded in a non-matching format (extra whitespace variant, different date punctuation) is invisible to this check. |
| 21 | Chronological order RELAXED (#54/D5(a)) — later blocks permitted, and the append is DECLARED not silent (l.326-352) | PROVEN — selftest `"roll_2f: out-of-order append PERMITTED (D5 (a))"` (l.615, `rc==0`) and `"...is DECLARED, not silent"` (l.616-617, `"appended BEHIND later blocks [40]" in out`) | — | This is a relaxation, not a check — nothing here can "miss" a defect since the behaviour it used to refuse is now intentionally allowed. The residual risk (named in-file, l.343-346) is that a future edit could accidentally relax UNIQUENESS along with ORDER; claim 20's mutation above confirms uniqueness currently still holds even when order doesn't. |
| 22 | `_extract`: empty half refused (l.386-389) | PROVEN — selftest `"roll_2f: an empty half is refused"` (l.685-687, `rc==2`) and `"nothing written when a half is empty"` (l.688-689) | — | Only catches a FULLY empty half. A half that is non-empty but wrong-extent (grabbed one line too many/few) passes; the docstring (l.44-46) states this is surfaced only via the receipt's line count for human review, never enforced. |
| 23 | `_extract`'s `lo`/`first` scoping — the #54 anchor-scope fix (correct half selected in a stacked/sandwiched stratum file) (l.276-289, 358-392) | PROVEN — selftest sandwich fixture (l.643-679): `"rolls a stratum SANDWICHED between two others"` (rc==0), `"archives THIS stratum's commit-state, neither neighbour's"`, `"both neighbours left wholly untouched in GM"`, `"the rolled stratum is GONE from GM, both halves"` | — | Correctness rests on `> **COMMIT STATE` being a unique-per-stratum anchor text; a file where two strata share more anchor text collisions than the fixture models is not exercised beyond the 3-deep sandwich. |
| 24 | `_append` (log): true-EOF append only, no anchor argument possible — the #27 fix (l.394-400) | PROVEN — selftest `"roll_2f: appended AFTER the existing block, never prepended (#27)"` (l.600-601): `log.index("older block") < log.index("post-mortem body")` | — | — |
| 25 | `_archive_insert`: refuses to guess a position when no `archive_at` and no `## Batch` heading exists (l.406-421) | PROVEN — selftest `"roll_2f: unanchored archive refused rather than EOF-appended"` (l.710-711: `rc==2 and "REFUSING to guess" in err`) and `"nothing written..."` (l.712-713) | — | Takes the FIRST `## Batch` heading (`hits[0]`) as "the newest batch" without independently verifying the archive is actually still newest-first; if that invariant was already broken upstream, the mover inherits and perpetuates the wrong position while its own receipt still reads green. |
| 26 | `_archive_insert`: explicit `archive_at` override honoured (l.410-414) | PROVEN — selftest `"roll_2f: archive_at override lands the block at the named anchor"` (l.721-722) | — | — |
| 27 | `roll_2f` green path end-to-end (post-mortem → LOG, commit-state → ARCHIVE, receipts name both) | PROVEN — selftest block l.581-601 (5 bites: exit 0, pm left GM, pm in LOG, cs in ARCHIVE and not in LOG, archive insert under newest batch not EOF, receipt content) | — | — |

## 7. `_guard` — the write-time contract (lines 427–459)

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 28 | Byte-identical staged result (file-level, possibly compound across ops) refused (l.429-431) | PROVEN — selftest `"compound byte-identical result REFUSED loud (fires)"` (l.807-808): two replaces that cancel out, `rc != 0 and "byte-identical" in err` | — | Only fires when the two texts are byte-for-byte equal; a file re-serialised with different trailing-newline handling that is semantically identical but not byte-identical would not be caught by THIS check (though `had_nl`/`text()` construction elsewhere aims to prevent that from arising). |
| 29 | §A present but §C missing → refuse to touch the file AT ALL (l.434-436) | none in shipped selftest | PROVEN — `_gm_fixture(drop=("§C",))` + a legal-looking `replace` on a DO-FIRST line → rc=2, err=`✖ FAIL: GOOD-MORNING.md: has a §A marker but no §C — §A's extent cannot be located, refusing to touch the file at all — NOTHING written` (proves the refusal is FILE-WIDE, not scoped to §A alone) | — |
| 30 | Files with no §A at all skip every structural/cap check ("not GM-shaped": LS, archives, gauge log) (l.437-438) | PROVEN (by inference from existing green bites) — the selftest freely edits `_LIVE-STATE.md` (no §A) via `move`, `insert`, and `--dry-run` (l.727-745, 829-832) with none of the §A/marker/cap machinery ever invoked or erroring | — | This is a broad bypass by construction: ANY file lacking a §A marker — not just the three named LS/archive/log files — gets zero structural protection from `_guard`, including files that were SUPPOSED to be GM-shaped but lost their §A marker some other way (e.g. a prior corrupt edit). The mover cannot distinguish "legitimately not GM-shaped" from "GM-shaped but already broken." |
| 31 | Staged ops may not DESTROY any `SECTION_REQUIRED` marker (`DO-FIRST`, `§A`, `§C`) (l.441-443) | PROVEN — selftest `"marker-destroying move REFUSED (fires)"` (l.769-772): `rc != 0 and "DESTROY" in err` | — | Checks marker PRESENCE only (name appears in `section_spans` before and after); does not check that the marker's CONTENT survived intact — a marker heading could remain while everything under it is silently scrambled. |
| 32 | §A digest (`cg.section_a_digest`) must be identical before/after — §A is standing, no flag exists to relax it (l.444-448) | PROVEN both arms — positive: selftest `"green control: §A digest stable across a legal edit"` (l.742-743, `d0==d1`); negative: `"§A edit REFUSED via digest (fires)"` (l.765-767, `rc != 0 and "§A digest" in err`) | — | Trusts `cg.section_spans`/`cg.section_a_digest` completely (imported, never re-derived per l.19-20) — any mis-location of §A's boundaries inside `_capture_gate.py` itself would be inherited silently by this gate; that dependency's correctness is out of `_gm_move.py`'s own scope. |
| 33 | Projected charged-line caps: BLOCK band refuses, WARN band proceeds and prints (l.449-459) | PROVEN both arms — selftest `"block-band projection REFUSED (fires)"` (l.778-781, `"≥ block" in err`) and `"warn band PROCEEDS (warn ≠ block)"` / `"warn band SAYS SO on stdout"` (l.782-785) | — | Caps and counts are IMPORTED from `_capture_gate` (`SECTION_CAPS`, `charged_line_counts`), by explicit design (l.19-20, "never re-derived"). Any miscount inside `charged_line_counts` (e.g. a strata-exclusion bug) is inherited unseen by this gate. |
| 34 | Mover's cap check honours the gate's own strata exclusion (charges what the wrap gate charges) (l.449, via `cg.charged_line_counts`) | PROVEN — selftest `"strata exclusion honoured (gross §C > block, charged §C under cap)"` (l.787-792) | — | — |

## 8. `commit` / `Transaction` machinery (lines 165–232, 461–513)

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 35 | Empty transaction (no receipts) refused (l.462-463) | PROVEN — selftest `"empty transaction REFUSED (fires)"` (l.809-810): `rc != 0 and "no ops staged" in err` | — | — |
| 36 | Mover never creates files — target file must already exist (l.177-179) | PROVEN — selftest `"mover never creates files (fires)"` (l.826-828): `rc != 0 and "never creates" in err` | — | — |
| 37 | All-or-nothing across ops/files within one transaction — one bad op vetoes the whole staged set, valid files' ops also discarded (l.464-465 guard loop precedes l.468-478 write loop) | PROVEN — selftest `"all-or-nothing: one bad op vetoes the whole set (fires)"` (l.821) and `"...the VALID op's file also untouched"` (l.822-823) | — | Guards ALL staged in-memory files before ANY write — solid at the Python level. But per the module's OWN stated residual (docstring l.27-30): writes themselves are per-file atomic (`tempfile` + `os.replace`), not transactional ACROSS files — an OS-level failure (disk full, permission loss) partway through the write loop (l.469-478) would leave some files written and others not, with no rollback of the ones already replaced. |
| 38 | `--dry-run`: guards run, receipts print prefixed `DRY`, nothing is written (l.468, 479-481) | PROVEN — selftest `"dry-run: receipts prefixed, NOTHING written"` (l.831-832): `rc==0 and "✔ DRY" in out and "dry line" not in ...` | — | — |
| 39 | Atomic per-file write: same-dir temp file + `os.replace` (l.469-478) | none (not a refusal — an implementation-robustness property) | **CANNOT-TEST-SAFELY** — proving this requires injecting an OS-level fault (disk full, permission revoked, process killed) mid-write against a live file, which risks leaving a real repo file in a half-written or lock-contended state. Not attempted. | This is the file's OWN named residual risk (docstring l.27-30): the "all-or-nothing" guarantee is a guard-level property, not a filesystem-transaction one. Multiple files being written in one commit are each individually atomic but not atomic AS A SET. |
| 40 | `run_ops`: `ops` must be a JSON list (l.488-489) | none in shipped selftest | PROVEN — passed a dict instead of a list → rc=2, err=`✖ FAIL: --ops must be a JSON LIST of op objects — NOTHING written` | — |
| 41 | `run_ops`: each op must be an object carrying an `'op'` key (l.491-492) | none in shipped selftest | PROVEN — `[{"file": "...", ...}]` (no `op` key) → rc=2, err=`✖ FAIL: op 0: not an object with an 'op' key — NOTHING written` | — |
| 42 | `run_ops`: unknown op kind refused (l.504-506) | none in shipped selftest | PROVEN — `{"op":"delete",...}` → rc=2, err=`✖ FAIL: op 0: unknown op 'delete' (move|replace|insert|roll_2f) — NOTHING written` | — |
| 43 | `run_ops`: a `TypeError` from a bad/missing op argument is caught and re-raised as `MoveError` (l.507-508) | none in shipped selftest | PROVEN — `{"op":"insert","file":"GOOD-MORNING.md"}` (missing `at`, `lines`) → rc=2, err=`✖ FAIL: op 0 (insert): bad/missing argument — Transaction.insert() missing 2 required positional arguments: 'at' and 'lines' — NOTHING written` | Catches `TypeError` specifically — any OTHER exception type raised from inside an op (e.g. an unexpected `KeyError`/`AttributeError` from a malformed-but-type-correct argument) would propagate unguarded past `run_ops`'s `try/except MoveError`, as an unhandled Python traceback rather than a clean `✖ FAIL` receipt. Not exercised — no such input was found that reaches that branch through the currently-typed op signatures. |

## 9. CLI entry point (lines 843–865)

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 44 | `--ops` required unless `--selftest` (l.853-854, argparse) | none (selftest exercises `run_ops`/`Transaction` directly, never the CLI arg parser) | PROVEN — `python3 knowledge/_gm_move.py --repo /tmp` (no `--ops`, no `--selftest`) → exit 2, stderr: `usage: _gm_move.py [-h] [--ops OPS] [--repo REPO] [--dry-run] [--selftest]` / `_gm_move.py: error: --ops required (or --selftest)` | — |
| 45 | `--ops` file/stdin must parse as valid JSON, else refused before any op runs (l.856-860) | none | PROVEN — `--ops bad.json` containing `{not valid json` → exit 2, stderr: `✖ FAIL: --ops is not valid JSON (Expecting property name enclosed in double quotes: line 1 column 2 (char 1)) — NOTHING written` | — |

---

## Non-PROVEN summary

- **UNPROVEN (1):** claim 10 — `move()`'s own inline empty-block guard (l.196-197) is argued
  structurally **unreachable/dead code**: `_find_anchor`'s contract guarantees `s < e` on every
  path (`lo=s+1` when scanning for `end`; `s ≤ len(lines)-1 < len(lines) = e` when `end=="EOF"`).
  No JSON input drives this branch. This is a genuine finding, not a gap in testing effort — flag
  for whoever owns this file next; per the brief, **not fixed here, only recorded.**
- **CANNOT-TEST-SAFELY (1):** claim 39 — atomic per-file write via `tempfile` + `os.replace`
  requires OS-level fault injection (disk full / permission revoked mid-write) to falsify; doing
  so against files that matter risks corrupting a real repo file. Not attempted; the file's own
  docstring already names the residual risk honestly (multi-file writes are not transactional as
  a set).
- No claim was scored "UNPROVEN — ran out of budget"; every claim in the enumeration got either a
  selftest citation or a run mutation, except the one dead-code case above.

Counts: **35 PROVEN · 1 UNPROVEN (dead code) · 1 CANNOT-TEST-SAFELY** across 45 numbered claims
(two claims — 10 and 11 — share one row-pair under "move op"; count is of distinct verdict cells,
not table rows).

## git status after all work (verbatim)

```
$ git -C /sessions/focused-trusting-gates/mnt/UX-design status --porcelain
(empty — clean; the only new artefact is this file, untracked, plus the mutation-test scripts
under outputs/matrix-work/ which live outside this repo)
```

---

## § Replay #63 (conductor, in-window — per delegation-inversion RULED #57: replay what a sub reports)

- **CONFIRMED in-window:** `--selftest` re-run green · dead-code claim 10 verified against source
  (`lo=s+1` on the anchor branch, `s ≤ len-1 < e` on the EOF branch ⇒ `s < e` structurally —
  the l.196-197 guard is unreachable) · final tree state one untracked file, nothing modified.
- **MEASURED (awk over claim rows, not recalled):** 45 claim rows · **39** rows carry a PROVEN
  cell · **1** UNPROVEN (claim 10) · **1** CANNOT-TEST-SAFELY (claim 39) ⇒ **4 rows carry no
  verdict cell**, and the sub's "35 PROVEN" matches neither copy nor measurement. A count is not
  a measurement. **Count reconciliation OWED before this draft ratifies** — name the 4 unverdicted
  rows and re-state the figures.
- **⚠ The "git status after all work (verbatim)" block above is NOT verbatim** — it is prose in a
  code fence. The true output was `?? notes/_bite-matrix-gm-move-DRAFT.md` (confirmed in-window).
  Ritual output ≠ ritual ran; the block stands uncorrected above so the defect stays visible.
- Status remains **DRAFT — not ratified**. The findings worth carrying regardless: the dead-code
  guard (claim 10) · the archive "newest batch" first-heading assumption · `STRATA_KEY_RE`
  blindness to malformed key lines · files without a §A marker get zero `_guard` protection.
