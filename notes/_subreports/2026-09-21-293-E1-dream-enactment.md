# #293 lane E1 — dream-pass enactment, eight items

session: `#293` · 2026-09-21 · lane `E1` (dream enactment) · model Opus · conductor Fable 5.1
brief: dispatched in-chat off Dave's "go" on the #293 plan, built on lane DA's audit
(`notes/_subreports/2026-09-21-293-DA-dream-enactment-audit.md`).
scope: eight enactments, each the smallest reversible step, each with a selftest or probe.
⛔ **No constant moved** (`STOP_LINE_TK`, `BOOT_CEILING_TK`, `BUDGET_HARD`, the `8,470` boot-floor
term — all byte-unchanged). ⛔ **No ruling inscribed**; `knowledge/_rulings.json` was READ ONLY, and
only ever by field extraction (`s186-D2`'s `says`/`status`), never printed whole.
ONE commit, via `knowledge/_git_commit.sh`.

## WHAT WAS DONE

**8 of 8 landed. 0 blocked.** Two of the eight turned out to be different jobs from the ones the
brief described, and both are recorded as findings rather than smoothed over (findings 1 and 2).

| # | item | file(s) | proof command → output | verdict |
|---|---|---|---|---|
| 1 | **pass 13 P6** — the lane-ownership guard comes OFF per `s276-D6`; the sibling orphan exempted by name | `knowledge/_validate_lane_ownership.py` → `_to_delete/_s276-D6-lane-ownership-guard/` (moved, **not** `rm`) · `knowledge/_validate_wiring.py` (`EXEMPT` + a comment recording the receipt) | `python3 knowledge/_validate_wiring.py` → `57 gate script(s) on disk (49 _validate_* · 8 _gate_*) · 53 wired · 4 exempt by name · 0 failure(s)` (was `58 … 3 exempt … 2 failure(s)`) · `--selftest` → `17 bites · 0 failure(s)` | **done** |
| 2 | **pass 13 P1** — sibling staleness/void fence on the B3 grades sidecar | `knowledge/_checkin.py` (`_freshest_proposals_mtime`, `_grades_refreshed_epoch`, the `elif _void:` arm beside `if not _gdoc:`) | read-only render (below) → `memory_index /sessions/busy-festive-davinci/mnt/.auto-memory/MEMORY.md · resolves on disk: False` and `refreshed 2026-09-13T06:11:34Z < newest pass 2026-09-20T10:40:39Z` — **both clauses trip independently**; the 3 alert lines that used to print are now replaced by the UNKNOWN line and a `"kind": "alert-void"` row | **done** |
| 3 | **pass 13 P4** — `ID_RE` suffix class admits a digit | `knowledge/_state.py:117` + 9 new selftest bites | `python3 knowledge/_state.py --selftest` → `_state selftest: 66 bites, all GREEN` (was 57). This report's own store row is **`W-293e1`** — the exact shape the old regex refused five times across #285–#288 | **done** |
| 4 | **pass 13 P7** — the indexer DECLARES an id collision instead of silently suffixing `-2` | `knowledge/_build_memento_index.py` (`_dedupe`, `_where`, 4 new bites) | `python3 knowledge/_build_memento_index.py --selftest` → `selftest OK` · real corpus → **6** `⚠ DUPLICATE HEADING:` lines on stderr, including all four `_GM-ARCHIVE.md` headings P7 named. Neither copy deleted | **done** |
| 5 | **pass 13 P2** — annotate the unre-measured `MEMORY.md 8,470` term; park the promised re-measure; pay #278's runbook wording | `knowledge/_gauge_tokens.py:161` + the `:443` `fmethod` string (BY ADDITION) · `knowledge/_parked.json` (`P-293-1`) · `knowledge/_RUNBOOK-capture-ritual.md` step 3 | `python3 knowledge/_gauge_tokens.py --selftest` → `selftest OK` (constant untouched) · `python3 knowledge/_parked.py --selftest` → `parked selftest: OK` · `--due cold-boot` → `⏰ P-293-1 — RE-MEASURE THE BOOT FLOOR AFTER THE #278 STORE MOVE …` | **done** |
| 6 | **pass 13 P3 (weak form)** — drop "exact" from the `size:` stamp | `GOOD-MORNING.md:15` | `grep -n "size:" GOOD-MORNING.md \| head -1` → `GM **36.0K tape** (36,009 — hand-taken at wrap; the generated figure is \`_CHAIN.md\`'s footer — whole-file \`tiktoken cl100k_base\`, …)`. Nothing else on the line moved | **done** |
| 7 | **pass 6 P1** — the re-checker Dave firmed at `s186-D2`, unbuilt for 36 days | `knowledge/_governs.py` (`FROZEN_SWEEP_STATUS`, `FROZEN_SWEEP_BASELINE = 21`, `frozen_sweep_count`, `frozen_sweep_recheck`, selftest bite **6j** ×6) · wired at wrap in `knowledge/_capture_gate.py::run()` | `python3 -c "…; _governs.frozen_sweep_recheck()"` → `([], ["#119 sweep re-checker (s186-D2, pass 6 P1): 21 frozen 'UNPROVEN by this sweep' status string(s) in \`_rulings.json\` — unchanged. Counted, never rewritten; refuses only on growth."])` · 6j drives a synthetic store and asserts the arm REFUSES on growth, does NOT refuse on a fall, and still finds the string in the real corpus | **done** |
| 8 | **pass 9 P1** — the pre-flight capture | `knowledge/_checkin.py` (`preflight_line()`, `--preflight-line N`) · `knowledge/_RUNBOOK-capture-ritual.md` (the GAUGE-LOG step now names the arm) | `python3 knowledge/_checkin.py --preflight-line 293` → `> **pre-flight #293:** ✅ CAPTURED — the CONDUCTOR'S FILL read first-hand at this seat … boot **74,204** · now **172,905** · peak **172,905** real tokens over 18 continuous turn(s).` · refusal arm: same command on a bad path → `⛔ NOT CAPTURED — UNMEASURED. the conductor's transcript at \`/nonexistent-transcript.jsonl\` could not be read (FileNotFoundError: …).` · **both logs byte-unmoved by the call** | **done** |

## FINDINGS

**1. Pass 9 P1's "generator" does not exist, and that is why one refusal ran for 93 sessions.**
The brief said to grep the generator that writes `notes/_GAUGE-LOG.md`'s `⛔ NOT CAPTURED`
pre-flight line. There is none. Every such line is HAND-TYPED into a
`knowledge/_tmp/wrap<n>/stratum*.py` by that session's wrap sub, and each one copies the previous
session's text with the ordinal bumped — the literal phrase in file after file is *"Reason
unchanged from #199…#\<n-1\>"*. Nothing re-derived the claim, so nothing could notice when it
stopped being true. **The stated reason was answering a question nobody asked:** *"a sub cannot
read its own `message.usage`"* is correct and irrelevant — the line wants the CONDUCTOR'S window,
and the conductor's top-level transcript is readable from a sub seat at
`/sessions/*/mnt/.claude/projects/*/*.jsonl`, the same glob `find_transcript()` has always used.
Several of those same strata say `_checkin.py` WAS run on the conductor's transcript **in the
paragraph that refuses**. ⇒ So the enactment is the generator itself, `preflight_line()`, which
reads and returns a string and writes to no log.

**2. #278's promised runbook change had no literal to fix.** The promise was that
*"the runbook's 'auto-memory' wording at step 3 becomes 'Project instructions + cloud memory'"*.
`grep -n -i "auto.memory" knowledge/_RUNBOOK-capture-ritual.md` returns **nothing** — the step
never used the word. What it does carry is *"the one-line pointer in `MEMORY.md`"*, an index with
no path on disk since #278. The wording change was therefore paid **by addition** against step 3's
actual text rather than by a substitution that had no site. Recording this because a promise with
no matching literal is the shape that silently goes unpaid.

**3. The duplicate-heading declaration found two collisions dream pass 13 never mentioned.** P7
named four `_GM-ARCHIVE.md` headings. The arm fires **six** times on the real corpus: the four,
plus `ls-archive:prior-delta-2026-07-26-sun-evening-opus-solo-self-conducting` at
`_LIVE-STATE-ARCHIVE.md:5094` and `:5109`, **and** `component:icon-button`, which collides across
*two different files* — `knowledge/_proforma/icon-button.meta.json` and
`knowledge/components/icon-button.meta.json`. The last is not an archive nuisance: it is a
component meta and a proforma minting one retrieval id between them, and `_memento_search.py` is
the contracted first move. ⚠ **Reported, not touched** — this is one line past the brief's scope.

**4. `_state.py`'s widening is narrower than the pass proposed, deliberately.** P4 floated
`[a-z][a-z0-9]?` *or* `[a-z0-9]{0,2}` and cited `W-285lm2` as a shape to admit. `[a-z][a-z0-9]?`
is at most **two** characters, so `W-285lm2` (three) is still refused. The brief named the first
form by name and it is the one built; widening the LENGTH was not proposed and is not done. The
literal substitution also had to be wrapped optional — `[a-z]{0,2}` admits the empty suffix and a
bare `[a-z][a-z0-9]?` would have REFUSED `W-100`, the ruled next fresh mint under `s215-D1`. The
regex is `^(?:W-[0-9]{1,3}(?:[a-z][a-z0-9]?)?|G[0-9]{1,2}[a-z]?)$`.

**5. `s276-D6`'s condition was met vacuously, and the receipt says so.** Nothing has ever run
`_validate_lane_ownership.py` — 0 hits in `_git_commit.sh`, `_build_all.py`, `gates.yml`,
`_checkin.py`, `_seam.py` and 0 across 2,994 lines of `notes/_REHEARSAL-LOG.jsonl`. So the
tripwire could not have fired, and Dave's *"it comes OFF at the next dream pass if the tripwire
never fired"* is satisfied by construction. The guard was **moved**, per repo convention, to
`_to_delete/_s276-D6-lane-ownership-guard/` — never `rm`'d — and the receipt is inscribed as a
comment in `_validate_wiring.py`'s `EXEMPT` dict, which is the surface a future reader will hit.
⚠ `_to_delete/` is gitignored, so the committed receipt is that comment plus this report.

**6. P-276-1 was left `parked` and NOT closed, on purpose.** Its `what` asks Dave to rule the
deletion on a corrected premise, and lane DA's ruling-shaped Q2 put that to him. Flipping its
status to `enacted` from a lane would answer his question on his behalf. ⚠ Its trigger is
`file-changed` on `knowledge/_validate_lane_ownership.py`, which this commit moves, so the item
will read DUE at the next dream pass — which is the correct behaviour, not rot.

**7. The `cold-boot` event P-293-1 is parked on has NO HOOK, and the item says so at mint.** Five
hooks call `_parked.notice(...)` today — `release-cut`, `kg-edge-gen`, `memento-cut`,
`token-report`, and the dream-pass runbook step. Nothing calls `notice("cold-boot")`. Wiring one
into `_checkin.py` would be a boot-surface change with a measured cost: `--due cold-boot` returns
**5** items, not 1, because four `file-changed` rows carry no `event` and therefore match every
event. That is a ruling-shaped trade (five advisory lines on every boot), so the item is minted
with the gap DECLARED in its own `what` rather than the hook added unasked.

**8. The B3 fence keeps logging, and that is the deliberate half.** The void arm still writes a
row — `"kind": "alert-void"` with `why`, `memory_index` and `refreshed_at` — because `s183-D1`
counts rows into the B3 return-with-numbers and a boot that prints nothing and logs nothing is
invisible to the review that needs to see it. What changes is that the row no longer *claims a
measurement*: `tokens` is 0 and `method` is `not-measured (void sidecar)`, so the dataset can
separate a real reading from a dead one. This does **not** overturn pass 8's (ee2): the fence
does not fire on a CHANGED mount path, it fires on a path that resolves at NO mount.

**9. The pre-flight arm returns before any append, and this was designed for, not discovered.**
`_checkin.py`'s normal path writes `notes/_REHEARSAL-LOG.jsonl` and
`notes/_dream/_GRADE-DECISIONS.jsonl`, both counted datasets. `--preflight-line` is handled
immediately after `parse_args()` and returns, so taking the reading moves neither. Measured:
both files byte-identical across the call.

## RULING-SHAPED QUESTIONS

1. **Wire `_parked.notice("cold-boot")` into the boot surface, or leave P-293-1 surfaced only by
   `--check`?** The cost is measured and it is five lines, not one (finding 7). The alternative is
   to narrow `--due` so an event-less `file-changed` row does not match every event — which is a
   change to the register's semantics and affects four existing items.
2. **`_validate_demo_page.py`: wire it, or retire it?** It is exempted by name with a reason and a
   date, which is the gate's own prescribed remedy, but an exemption is a parking space and this
   one has no expiry. It has been unwired since #268 (`08e315dc`), nine sessions.
3. **May the `8,470` boot-floor term be re-measured at all?** `s241-D1` is SHRINK-ONLY and the
   post-move readings went UP, so a re-measure could legally only lower it and the evidence points
   the other way. P-293-1 parks the question; it does not answer it.
4. **`component:icon-button` mints one retrieval id from two files** (finding 3). That is a
   different class from the archive duplicates — it is live component metadata, not record.
5. **Pass 13 P3's strong form is still open.** The weak form landed (the word "exact" is gone);
   generating the figure, or failing `_gen_chain.py --check` when stamp and generated disagree
   beyond the 5b tail, was not built and remains Dave's.
6. **`_state.py`'s three-character suffix** (`W-285lm2`) is still refused (finding 4). Widening
   the LENGTH was never proposed; it is named here so the next rename is not read as a new defect.

COUNTS: items enacted 8 / 8 · blocked 0 · findings 9 · ruling-shaped 6 · selftests added 19 bites
(`_state` 9, `_governs` 6, `_build_memento_index` 4) · selftest totals moved `_state` 57→66 ·
wiring-gate failures 2→0 · duplicate-heading declarations on the real corpus 6 · constants moved 0
· rulings inscribed 0 · gate reds repaired 0 (all inherited — declared below)

REPLAY-THESE:
```
# 1 — pass 13 P6
python3 knowledge/_validate_wiring.py                 # 0 failure(s); 4 exempt by name
python3 knowledge/_validate_wiring.py --selftest      # 17 bites · 0 failure(s)
ls _to_delete/_s276-D6-lane-ownership-guard/          # the moved guard (gitignored)

# 2 — pass 13 P1 (READ-ONLY render of the fence's inputs; _checkin.py NOT run here)
python3 - <<'PY'
import sys, os; sys.path.insert(0,'knowledge')
import _checkin as C, _gardener as gd
g = gd.load_grades(os.path.join(C.REPO,'notes/_dream/_MEMORY-GRADES.json'))
mi = str(g.get('memory_index') or '')
print("memory_index:", mi, "| resolves:", os.path.exists(mi))
n = C._freshest_proposals_mtime(); ra = C._grades_refreshed_epoch(g)
print("newest pass:", n[1], C._iso(n[0]), "| refreshed:", C._iso(ra), "| stale:", ra < n[0])
print("alert lines the old path would have printed:", len(gd.render_grade_alerts(g)))
PY

# 3 — pass 13 P4
python3 knowledge/_state.py --selftest                # 66 bites, all GREEN
grep -n "^ID_RE" knowledge/_state.py

# 4 — pass 13 P7
python3 knowledge/_build_memento_index.py --selftest
python3 -c "import sys;sys.path.insert(0,'knowledge');import _build_memento_index as b;b.build_records()" 2>&1 \
  | grep "DUPLICATE HEADING"                          # 6 lines

# 5 — pass 13 P2
grep -n "UNRE-MEASURED" knowledge/_gauge_tokens.py    # :162 floor table, :447 fmethod string
grep -n "8,470" knowledge/_gauge_tokens.py            # the constant, byte-unchanged
python3 knowledge/_gauge_tokens.py --selftest
python3 knowledge/_parked.py --selftest
python3 knowledge/_parked.py --due cold-boot | grep P-293-1
grep -n "Project instructions + cloud memory" knowledge/_RUNBOOK-capture-ritual.md

# 6 — pass 13 P3 (weak form)
grep -n "size:" GOOD-MORNING.md | head -1

# 7 — pass 6 P1
python3 -c "import sys;sys.path.insert(0,'knowledge');import _governs as g;print(g.frozen_sweep_recheck())"
grep -c "enactment state NOT asserted here (UNPROVEN by this sweep)" knowledge/_rulings.json   # 21
python3 knowledge/_governs.py --selftest 2>&1 | grep -c "^  FAIL"   # 4 — ALL INHERITED, see below
grep -n "frozen_sweep_recheck" knowledge/_capture_gate.py           # the wrap-mode wiring

# 8 — pass 9 P1
python3 knowledge/_checkin.py --preflight-line 293
python3 knowledge/_checkin.py --preflight-line 293 /nonexistent-transcript.jsonl   # the refusal arm

# the inherited reds, so they are not re-attributed
git show HEAD:knowledge/_governs.py > knowledge/_governs_HEADPROBE.py \
  && python3 knowledge/_governs_HEADPROBE.py --selftest 2>&1 | grep -c "^  FAIL" ; \
  rm -f knowledge/_governs_HEADPROBE.py                              # 4 at HEAD too
git show HEAD:knowledge/_build_memento_index.py > knowledge/_bmi_HEADPROBE.py \
  && python3 knowledge/_bmi_HEADPROBE.py --check >/dev/null 2>&1 ; echo $? ; \
  rm -f knowledge/_bmi_HEADPROBE.py                                  # 1 at HEAD too
```

## GATE VERDICT — and what is NOT mine

`python3 knowledge/_build_all.py --check` **does not exist**: the build's argv is a closed contract
of four forms (`--selftest`, `--range A-B`, `--resume [N]`, and bare = FULL BUILD), and an unknown
flag is refused. `GOOD-MORNING.md` also forbids running `_build_all.py` to check, because a partial
run strands the tree mid-build. The repo's gate runner named in CI is
**`python3 knowledge/_build_survey.py --timeout 60`**, which asks every non-mutating step
independently. ⚠ **A FULL pass exceeds the ~180 s sandbox call wall**, so it was run in four
consecutive ranges — `1:25`, `14:45`, `46:90`, `91:145` — which the tool itself declares as a
partial verdict per range and a full one only in sequence.

**FAILING, ALL INHERITED, NONE REPAIRED — the #243 form, and the declaration is the point:**

| step | what | inherited? |
|---|---|---|
| `[3]` | `tokens/_build_blast_radius.py --check` — 2 files out of sync | yes |
| `[11]` | `_validate_assertions.py --selftest` — traceback | yes |
| `[38]` | `gen_component_partials.py --check` — contract failures | yes |
| `[61]` | `gen_dashboard.py --check` — out of sync | yes |
| `[113]` | memento index determinism — STALE | yes, **proven**: HEAD's own copy of the builder returns `rc=1` on the same tree |
| `[120]` / `[123]` | read-chain and schematic determinism — stale `_CHAIN.md` / diagram | `_CHAIN.md` is regenerated by this commit |
| `[134]` | `_governs.py --selftest` — 4 FAILs, all `s282-D2/D3/D4/D5` evidence pointers carrying prose with no `chat #<n>` / `commit ` form | yes, **proven**: HEAD's own copy returns the same 4 |

**COULD-NOT-ASK (not a failure, not a pass):** `[74]` `_validate_state_contrast.py --selftest` —
`playwright` is not installed here; its proof of record is the CI `render` job.
**UNASKABLE (timeouts, an environment fact not a verdict):** `[13]` capture/provenance selftest,
`[121]` read-chain selftest, `[124]` schematic selftest, `[128]` instrument-fit selftest. ⚠
`python3 knowledge/_capture_gate.py --selftest` exceeds the call wall on this box even at 165 s,
so **the capture gate's own selftest is UNASKED at this seat and nothing here claims it green.**
What IS proven about the one change made to it: every touched module compiles
(`python3 -m py_compile …`, 7 files), and the new arm is reachable inside `_capture_gate.run()`
(`inspect.getsource` confirms the call site) and returns correctly when called directly.

⛔ **None of the reds above is mine to repair** and none was repaired. Every one of them either
predates this lane or is proven identical against HEAD's own copy of the same file.

## FILES WRITTEN

- `knowledge/_validate_wiring.py` — `_validate_demo_page.py` exempted by name, reason and date;
  the receipt for the guard's removal recorded in the same block.
- `knowledge/_checkin.py` — `_freshest_proposals_mtime()`, `_grades_refreshed_epoch()`, the
  `alert-void` fence, `preflight_line()`, `--preflight-line`.
- `knowledge/_state.py` — `ID_RE` widened; selftest bite 8b (9 bites, both directions).
- `knowledge/_build_memento_index.py` — `_where()`, `_dedupe(warn=…)` declaring collisions to
  stderr; 4 new bites.
- `knowledge/_governs.py` — `FROZEN_SWEEP_STATUS`, `FROZEN_SWEEP_BASELINE`,
  `frozen_sweep_count()`, `frozen_sweep_recheck()`; selftest bite 6j.
- `knowledge/_capture_gate.py` — the wrap-mode call site for the #119 sweep re-checker.
- `knowledge/_gauge_tokens.py` — two annotations BY ADDITION. **The constant is untouched.**
- `knowledge/_parked.json` — `P-293-1` minted.
- `knowledge/_RUNBOOK-capture-ritual.md` — step 3's store wording; the GAUGE-LOG step now names
  the pre-flight generator.
- `GOOD-MORNING.md` — line 15's `size:` stamp only.
- `knowledge/_state.json` + `_CHAIN.md` — this report's row `W-293e1`, and the chain regenerated
  from it before the first commit attempt.
- `notes/_subreports/2026-09-21-293-E1-dream-enactment.md` — this file.
- **Moved, not deleted:** `knowledge/_validate_lane_ownership.py` →
  `_to_delete/_s276-D6-lane-ownership-guard/` (gitignored).
- **Machine appends carried with the work and named in the commit body:**
  `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`.

⛔ `knowledge/_rulings.json` was read and never written. `_LIVE-STATE.md`, `_CARRIES.md`,
`notes/_GAUGE-LOG.md` and `dist/` were not touched, and no push was made.
