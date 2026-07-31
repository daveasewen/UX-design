provenance: #64 sub draft (Worker B, Sonnet), phase 2 (mutation-test the 30 UNCOVERED rows) ·
status: DRAFT — not ratified

# Bite matrix — `knowledge/_capture_gate.py` — PHASE 2: MUTATION-TEST THE 30 UNCOVERED ROWS

Method: `knowledge/_capture_gate.py` (and its imports `_gauge_tokens.py`, `_gm_usage.py`,
`_search_core.py`, `_gen_lanes.py`, `_build_memento_index.py`, `_gen_chain.py`) copied
READ-ONLY into a tempdir (`/sessions/.../outputs/workerB/knowledge_ro/`, never the live repo)
and imported in-process. For every one of the 30 rows Phase 1 marked UNCOVERED: a minimal
fixture was built (via the file's own `_gm_fixture` helper where the claim is a `check_budgets`
branch, hand-built markdown/text otherwise), the EXACT defect the claim forbids was injected,
the relevant function was called DIRECTLY (not via `--wrap`/subprocess — the sandbox
call-boundary lesson), and the control (unmutated / correctly-shaped fixture) was run alongside
it. No file under the live repo was ever opened for writing; `knowledge/_capture_gate.py` itself
was never edited — only its own already-exported constants/functions were monkeypatched
**in-process, in a throwaway Python process**, for the handful of rows where the shipped
constant makes a branch structurally dead (named per-row below). Nothing here repairs the gate;
every defect found is RECORDED, not fixed.

Columns: **CLAIM** (Phase 1's number + one-line restatement) · **BITES** (was it covered before
this pass) · **MUTATION-RED** (the fixture, the exact red text, verbatim) · **CONTROL** (does the
unmutated/correct fixture stay green) · **CANNOT-SEE** (unchanged from Phase 1 unless this pass
found something new) · **VERDICT**.

---

## HEADLINE — CLAIM #39 (ds-022 / Dave #58, `check_budgets` ~1509–1530)

**CLAIM:** a 2f strata block whose session key is ALREADY present in `notes/_GAUGE-LOG.md` (and
not one of the three closed `STRATA_EXEMPT` numbers 40/41/42) must FAIL LOUD, naming the block —
this is the literal condition `_gm_move.py`'s `roll_2f` duplicate-key guard will refuse, and
Dave's #58 ruling was explicit: *"if a fourth unrollable block ever turns up, fail loud and come
back to me."* This is the largest coverage gap Phase 1 found — the mechanism had never fired in
any selftest.

**BITES (before this pass):** UNCOVERED — confirmed by Phase 1's direct search; no fixture ever
wrote a `notes/_GAUGE-LOG.md` alongside a colliding strata key.

**MUTATION-RED.** Fixture: `_gm_fixture(strata_keys=[99], strata_pad=3)` (one LIVE, non-exempt
strata block keyed `#99`) + `notes/_GAUGE-LOG.md` containing `#### 2026-07-29 #99`.
`check_budgets(repo)` → **1 fail**:

> `GOOD-MORNING.md: strata block(s) #99 already keyed in notes/_GAUGE-LOG.md — roll_2f's
> duplicate-key guard will refuse them, the same permanent condition #40/#41/#42 are stuck in.
> STRATA_EXEMPT is a CLOSED list of three (Dave #58): this is a NEW unrollable block and needs
> Dave's ruling, not an addition to the list.`

**CONTROL, two arms, both green on the target fail:**
- A: same GM fixture, **no** `_GAUGE-LOG.md` at all (the "fixture repo" shape every other selftest
  uses) → `gauge_log_keys is None` → check silently SKIPPED (not passed) → 0 fails.
- B: same GM fixture, `_GAUGE-LOG.md` present but keyed `#### 2026-07-29 #77` (non-colliding) →
  `newly_unrollable` empty → 0 fails.

Both controls confirm the fail is keyed on the actual collision, not on GM-fixture shape or
log-file presence alone — this is a real, not accidental, bite now that it has actually fired.

**CANNOT-SEE (unchanged from Phase 1):** the check is a NAME collision only — it infers
`roll_2f`'s refusal from the shared key format rather than invoking the mover; a defect in
`_gm_move.py`'s own guard logic would not be caught here.

**VERDICT: PROVEN-BY-MUTATION.** The #58 ruling now has a fixture that exercises it, genuinely
red on the defect and genuinely green on both the absent-log and non-colliding-log shapes.

---

## G0 — `check_file` (702–753)

**CLAIM #4.** `status: ruled` pointer matches no file on disk → WARN.
BITES (before): UNCOVERED.
MUTATION-RED: file with `status: ruled -- see notes/_NONEXISTENT-LEDGER.md`.
> `2026-07-31-x.md: ruled-pointer \`notes/_NONEXISTENT-LEDGER.md\` matches no file`
CONTROL: same file, pointer rewritten to an existing path (`notes/_DECISION-HISTORY/README.md`)
→ 0 fails, 0 warns.
CANNOT-SEE: unchanged (`PATHISH_RE` only fires on `.md`-suffixed tokens).
VERDICT: PROVEN-BY-MUTATION.

**CLAIM #5.** Missing `provenance:` line entirely → WARN.
BITES (before): UNCOVERED.
MUTATION-RED: file with `status: observed` and no `provenance:` line anywhere.
> `2026-07-31-y.md: missing \`provenance:\` line (soft — add \`<session-id> · <date>\`)`
CONTROL: same file + a `provenance:` line → warn gone.
CANNOT-SEE: unchanged.
VERDICT: PROVEN-BY-MUTATION.

---

## G1 — `check_preflight`, percentage form (927–1051)

**CLAIM #10.** No total stated (`= N%`) → FAIL.
MUTATION-RED: `pre-flight: fill 10% job 20% wrap 10% GREEN reserve 15%` (no `=`).
> `GOOD-MORNING.md: pre-flight stamp states no projected total (\`= N%\`)`
CONTROL: same line + `= 40%` → fail gone. VERDICT: PROVEN-BY-MUTATION.

**CLAIM #11.** No band named → FAIL.
MUTATION-RED: `pre-flight: fill 10% job 20% wrap 10% = 40% reserve 15%` (no GREEN/AMBER/RED).
> `GOOD-MORNING.md: pre-flight stamp names no band — state the NUMBER and the BAND together so a mismatch is visible in one glance`
CONTROL: same line + `GREEN` → fail gone. VERDICT: PROVEN-BY-MUTATION.

**CLAIM #18.** ds-023: total > 63% (beyond `MARKED_MAX`), MARKED → WARN (not FAIL).
MUTATION-RED: `pre-flight: fill 40% job 20% wrap 10% = 70% RED reserve 15% RESERVE SPEND -- forked to Dave`.
> `GOOD-MORNING.md: pre-flight 70% is beyond the 63% tolerance, marked and forked to Dave — allowed on the receipt. ⚠ above 63% is UNRULED — Dave has ruled the band (45–60) and the marked tolerance (63), and nothing beyond. This gate keeps the pre-#36 shape here rather than inventing a stop he did not pick; FORKED TO DAVE, ds-023. In flight, STOP AT 50% (60 − the 10%-priced wrap).`
CONTROL: same total, marker removed → the SAME text now appears as a FAIL (`UNMARKED`), proving
the marker — not the total — is what flips the tier. VERDICT: PROVEN-BY-MUTATION.

**CLAIM #20.** Wrap term below `WRAP_FLOOR`(5) → WARN.
MUTATION-RED: `pre-flight: fill 27% job 20% wrap 3% = 50% AMBER reserve 15%`.
> `GOOD-MORNING.md: wrap reserved at 3% (runbook says ~5%) — the ritual is not free`
CONTROL: wrap raised to 10% (total re-balanced to 50%) → warn gone. VERDICT: PROVEN-BY-MUTATION.

**CLAIM #21.** No ring-fenced reserve mentioned → WARN.
MUTATION-RED: `pre-flight: fill 20% job 20% wrap 10% = 50% AMBER` (no `reserve NN%`).
> `GOOD-MORNING.md: pre-flight names no ring-fenced reserve (~15%) — the fence is what makes the gauge a throttle rather than a thermometer`
CONTROL: `reserve 15%` added back → warn gone. VERDICT: PROVEN-BY-MUTATION.

---

## G2 — `check_preflight_tokens`, #56 absolute form (813–924)

**CLAIM #24.** No `= N of N` total clause → FAIL, early return. (Phase 1: structurally dead on
the normal `check_preflight` dispatch path — only reachable by calling `check_preflight_tokens`
directly, which nothing in the file's own selftest does.) Called directly here, as Phase 1 said
the only route in would be.
MUTATION-RED: `boot 5000 (disk 5000 measured) job 2000 est wrap 1000 est GREEN` (no `=...of...`).
> `GOOD-MORNING.md: pre-flight stamp states no total against a budget (\`= N of 200,000\`)`
CONTROL: `= 8000 of 200000 GREEN` appended → 0 fails. VERDICT: PROVEN-BY-MUTATION (confirms the
branch's own logic is sound; Phase 1's "dead on the normal path" finding stands unchanged — this
is still only reachable by a direct call, which is now what the test does honestly).

**CLAIM #27.** No band word (absolute form) → FAIL.
MUTATION-RED: `boot 5000 (disk 5000 measured) job 2000 est wrap 1000 est = 8000 of 200000` (no band).
> `GOOD-MORNING.md: pre-flight names no band — state the NUMBER and the BAND together so a mismatch is visible in one glance`
CONTROL: `GREEN` appended → 0 fails. VERDICT: PROVEN-BY-MUTATION.

---

## G3 — `check_budgets` structural (1470–1546)

**CLAIM #35.** `GOOD-MORNING.md` missing → FAIL, early return.
MUTATION-RED: empty tempdir, no GM file.
> `GOOD-MORNING.md: missing — ritual step 2`
CONTROL: GM file present (`_gm_fixture()`) → that fail absent. VERDICT: PROVEN-BY-MUTATION.

**CLAIM #41.** Section line cap: WARN band (DO-FIRST 120–179) under block.
MUTATION-RED: `_gm_fixture(do_first=150)` → 152 charged lines.
> `GOOD-MORNING.md DO-FIRST: 152 lines, cap 120 — ritual step 2e`
(and confirmed NOT a FAIL — no `block 180` message for DO-FIRST in the same run.)
CONTROL: `_gm_fixture(do_first=10)` → no DO-FIRST warn at all. VERDICT: PROVEN-BY-MUTATION.

---

## G4 — TITLE THE NEXT CHAT, #60-D8 (1548–1567)

**CLAIM #42.** No `TITLE THE NEXT CHAT` line → FAIL. This is the row Phase 1 flagged as
DOUBLY uncovered: the fixture helper's own comment (line ~2869) claims `title=False` is how this
path is "bitten deliberately", but no call site anywhere in the file's selftest actually passes
`title=False`. Run here for the first time.
MUTATION-RED: `_gm_fixture(title=False)`.
> `GOOD-MORNING.md: no \`TITLE THE NEXT CHAT\` line found in the header — ritual step 2/4b. An ABSENT title must not read as a pass: #60-D8 caps the line, it does not licence deleting it.`
CONTROL: `_gm_fixture(title=True)` (the default) → that fail absent.
VERDICT: PROVEN-BY-MUTATION — and the documentation gap Phase 1 named is now closed by evidence
rather than left standing: the mechanism the comment claimed IS sound, it was simply never
invoked. The defect (a comment claiming a bite the suite never took) is unchanged and stands as
its own finding — running the arm once here does not put a permanent pin into the file's own
selftest suite, and nothing in this pass edits that suite.

**CLAIM #43.** TITLE line over `TITLE_CAP_TAPE`(120 tape) → FAIL.
MUTATION-RED: baseline fixture's title line replaced with a long padded title (~171 tape).
> `GOOD-MORNING.md: \`TITLE THE NEXT CHAT\` line measures 171 tape (tiktoken cl100k_base), cap 120 tape (RULED #60-D8) — ritual step 2/4b. The title is a LABEL: at 1,073 tape it was 18% of the 5,969-tape read chain with ZERO consumers anywhere in the toolchain. REMEDY: shorten it back to a label — role comes from Dave's opener line, never the title.`
CONTROL: default short title → fail absent. VERDICT: PROVEN-BY-MUTATION.

---

## G6 — compactable region / M8 banner (1672–1732)

**CLAIM #50.** Compactable region ≥ BLOCK (bill) → FAIL. Phase 1: structurally dead code under
the shipped constant `SIZE_BUDGET_TK["compactable_block"] = None` — the `else:` branch containing
this FAIL cannot execute while that constant holds, and nothing re-arms it to prove the FAIL
logic itself is sound.
**Method note:** tested by RE-ARMING the constant **in-process, in a throwaway Python
process only** (`gate.SIZE_BUDGET_TK["compactable_block"] = 100`, restored immediately after) —
`knowledge/_capture_gate.py` on disk was never touched. This is exactly the re-arm Phase 1 said
would go live untested if Dave ever restores the block; doing it here in a disposable process is
how the branch's own arithmetic gets checked without shipping the re-arm.
MUTATION-RED (re-armed): `_gm_fixture(sec_c=5, fat_c=80)` with the block re-armed to a low value.
> `GOOD-MORNING.md compactable: 19,612 tape / ~30,791 bill (derived ×1.57, PROVISIONAL), block ~157 bill — ritual step 2`
CONTROL (shipped state, `compactable_block=None` restored, same fixture): 0 compactable-block
fails — confirms the branch is genuinely dead under the current constant, as Phase 1 said.
VERDICT: PROVEN-BY-MUTATION (re-armed logic sound) + Phase 1's dead-code finding CONFIRMED, not
contradicted — both facts now rest on a run, not an inference.

**CLAIM #52.** M8: §A precedes DO-FIRST → banner region cannot be isolated → FAIL. Phase 1:
`_gm_fixture` has no parameter to reorder sections, so this was never driven through the fixture
helper. Tested here with a hand-built GM file (bypassing `_gm_fixture`, which cannot produce this
shape) carrying `# §A` before `## ⬛ DO THIS FIRST`.
MUTATION-RED:
> `GOOD-MORNING.md: §A precedes DO-FIRST, so the banner region can no longer be isolated from the exempt section — the M8 budget REFUSES to measure rather than charge §A. Restore the order, or re-rule the region.`
(A second, unrelated fail also fired in this run — a 0.00K-stamp staleness fail from the
hand-built file's placeholder size stamp — noted so it is not mistaken for silence on the target
check; it is orthogonal to what this row tests.)
CONTROL: `_gm_fixture()` default (correct order) → the reorder fail absent.
VERDICT: PROVEN-BY-MUTATION.

---

## G7 — M10 corpus (1761–1770)

**CLAIM #58b.** M10 corpus (GM+LS whole) > `CORPUS_BUDGET_TK`(36,000 tape) → WARN, never blocks.
MUTATION-RED: `_gm_fixture(fat_a=260)` (inflates whole-file `tk` without inflating the charged
DO-FIRST/§C line caps, since §A is exempt from those but still counted in the whole-file/corpus
tape figure) → corpus measured 63,433 tape.
> `M10 corpus (GM + _LIVE-STATE whole): 63,433 tape / ~99,590 bill (derived ×1.57, PROVISIONAL), warn 36,000 tape / ~56,520 bill — the RETRIEVAL SURFACE, not the chain a session reads. WARN ONLY: growth here costs a retrieval, not a cold start. Never a trim order.`
CONTROL: `_gm_fixture()` default → no corpus warn (under budget). VERDICT: PROVEN-BY-MUTATION.

---

## G14 — `index_freshness_check` (2176–2231)

**CLAIM #70.** `_build_memento_index` unimportable → FAIL.
**Method note:** simulated via `sys.modules["_build_memento_index"] = None` before the call
(the same technique the file's own selftest uses on `tiktoken`), restored after — no file edited.
MUTATION-RED:
> `retrieval index: _build_memento_index.py unimportable (import of _build_memento_index halted; None in sys.modules) — the freshness check cannot run; fix it, never close blind`
CONTROL: import restored → that fail absent (a DIFFERENT, expected fail about corpus refusal
appears instead, from the empty fixture repo — noted, not the target). VERDICT: PROVEN-BY-MUTATION.

**CLAIM #71.** `build_records()` raises an exception → FAIL.
MUTATION-RED: `_build_memento_index.build_records` monkeypatched to raise `RuntimeError`, restored after.
> `retrieval index: rebuild raised (synthetic mutation: build_records raised) — retrieval is unverifiable this wrap`
CONTROL: function restored → fail absent. VERDICT: PROVEN-BY-MUTATION.

---

## G15 — `usage_history_probe` (2244–2292)

**CLAIM #75.** `_gm_usage` unimportable → issue (currently WARN tier).
MUTATION-RED (`sys.modules["_gm_usage"] = None`):
> `usage-history: _gm_usage.py unimportable (import of _gm_usage halted; None in sys.modules) — the series is UNREAD, never assumed clean`
CONTROL: import restored → issue absent (empty-repo "no testimony found" note appears instead).
VERDICT: PROVEN-BY-MUTATION.

**CLAIM #76.** `history_report` returns refusals → issue.
MUTATION-RED: `_gm_usage.history_report` monkeypatched to return `(text, [], ["synthetic mutation refusal: malformed testimony"])`.
> `usage-history: synthetic mutation refusal: malformed testimony`
CONTROL: function restored → issue absent. VERDICT: PROVEN-BY-MUTATION.

**CLAIM #77.** Deferral candidates found → NOTE published with real names (the positive case
Phase 1 said no fixture anywhere constructs). Built a genuine 7-session `notes/_GAUGE-LOG.md`
using the file's own `GOOD_USAGE` testimony shape (from `_gm_usage.py`'s selftest), with
`LS:LANES` testified `U` (unread) in every one of 7 sessions — never once `C` (cited), streak 7
≥ `DEFER_STREAK`(6).
MUTATION-RED (NOTE, not a fail — this check only ever publishes):
> `usage-history ⬛ 1 sections NEVER CITED in 7 sessions and unread 6+ running: LS:LANES. Remedy UNRULED (OFFLOAD / TRIM / KEEP — Dave's, not this gate's). Threshold 6 is AGENT-PROPOSED, ADVISORY — awaiting Dave (#35).`
CONTROL: identical 7-session log with `LS:LANES` testified `C` (cited) every time → that NOTE
absent, replaced by "no section is both never-cited and long-unread." VERDICT:
PROVEN-BY-MUTATION — genuinely, with real candidate names, closing the one positive-case gap
Phase 1 named for this function.

---

## G16 — `consult_receipt_probe` (2295–2338)

**CLAIM #78.** `_search_core` unimportable → issue.
MUTATION-RED (`sys.modules["_search_core"] = None`, GM carrying a `### ⏱ SESSION STRATA` marker
so the probe does not skip before reaching the import):
> `consult-receipts: _search_core.py unimportable (import of _search_core halted; None in sys.modules) — probe cannot run; fix it, never close blind`
CONTROL: import restored → issue absent (the expected "NO consult-receipts line" issue appears
instead). VERDICT: PROVEN-BY-MUTATION.

---

## G17 — `lane_routing_check` (2341–2366)

**CLAIM #81.** `_gen_lanes` unimportable → FAIL.
MUTATION-RED (`sys.modules["_gen_lanes"] = None`):
> `lane-routing: _gen_lanes.py unimportable (import of _gen_lanes halted; None in sys.modules) — check cannot run; fix it, never close blind`
CONTROL: import restored → fail absent. VERDICT: PROVEN-BY-MUTATION.

**CLAIM #82.** Lane records invalid (`_gen_lanes.load_lanes()` returns errors) → FAIL.
MUTATION-RED: `_gen_lanes.load_lanes` monkeypatched to return `([], ["synthetic mutation: malformed lane record"])`.
> `lane-routing: records invalid — synthetic mutation: malformed lane record`
CONTROL: function restored → fail absent. VERDICT: PROVEN-BY-MUTATION.

---

## G18 — `dofirst_index_present_check` (2369–2414)

**CLAIM #84.** Presence index could not be built at all → FAIL.
MUTATION-RED: GM with no `## ⬛ DO THIS FIRST` heading at all + a present `_CHAIN.md`.
> `dofirst-index: the presence index could not be built, so the read chain does NOT represent the open worklist — GOOD-MORNING.md has no ⬛ DO THIS FIRST section — presence index NOT built. The chain would otherwise tell a cold session there is no open work, which is a confident false negative, not a small index.`
CONTROL: GM with a well-formed DO-FIRST section (two real `> **N. ...**` items) + a `_CHAIN.md`
naming both → 0 fails, a green NOTE instead. VERDICT: PROVEN-BY-MUTATION.

**CLAIM #85.** Open DO-FIRST item(s) not individually named in on-disk `_CHAIN.md` → FAIL, names
the missing numbers. Phase 1: never driven through this function by any selftest.
MUTATION-RED: GM with items `1` and `2`; `_CHAIN.md` naming only `` `1` ``.
> `dofirst-index: 1 open DO-FIRST item(s) are in GOOD-MORNING.md but NOT named in _CHAIN.md — 2. A cold session reading the chain cannot learn they exist. Run \`python3 knowledge/_gen_chain.py\` and stage the result. (This is the #60 defect: items 9-12, silently absent.)`
CONTROL: `_CHAIN.md` naming both `` `1` `` and `` `2` `` → 0 fails, green NOTE.
VERDICT: PROVEN-BY-MUTATION.

---

## G19 — `wrap_checks` git status (2503–2513)

**CLAIM #89.** `git status --porcelain` reports uncommitted paths → WARN, count only.
MUTATION-RED: a real `git init`+commit fixture repo, then one tracked-file edit + one untracked
new file left uncommitted (2 porcelain lines).
> `git: 2 uncommitted path(s) — commit before close (step 5)`
CONTROL: identical repo, fully committed (clean tree) → 0 git warns.
VERDICT: PROVEN-BY-MUTATION.

---

## G20 — measurement engine internals (1291–1408)

**CLAIM #93b.** `section_a_digest()` raises (`KeyError`) if either `§A` or `§C` is absent from
`spans` — rather than silently mis-slicing.
MUTATION-RED: `section_a_digest(["a","b"], {"§C": (0,1)})` (missing `§A`) → `KeyError: '§A'`.
Second arm: missing `§C` → `KeyError: '§C'`. Both raise, neither silently returns a wrong-region
hash.
CONTROL: both markers present → returns a hash normally, no exception. VERDICT:
PROVEN-BY-MUTATION — both halves.

**CLAIM #94.** `chain_parts()`/`dofirst_index()` internal refusals — the five not already proven
via claim #56. All five driven directly:

- **(a) no `_gm_usage` importable** (`chain_parts`): `sys.modules["_gm_usage"]=None` →
  `(None, None, "_gm_usage unavailable (...) — chain UNMEASURED, not assumed clean")`. Control
  (import healthy, on an empty repo): different, expected refusal ("_LIVE-STATE absent"), not
  this one.
- **(b) no `⬛ DO THIS FIRST` section found** (`dofirst_index`): GM with `§A` but no DO-FIRST
  heading → `(None, "GOOD-MORNING.md has no ⬛ DO THIS FIRST section — presence index NOT
  built...")`. Control: GM with the heading + one item → returns a built index, not `None`.
- **(c) DO-FIRST found but ZERO items match `DOFIRST_ITEM_RE`**: heading present, body is plain
  prose with no `> **N. ...**` line → `(None, "⬛ DO THIS FIRST found at line 2 but ZERO items
  matched \`^>\s*\*\*(\d+[a-z]?)\.\s*(.+)$\` — presence index NOT built...")`. Control: same as
  (b)'s control.
- **(d) assembled index exceeds `DOFIRST_INDEX_TK_MAX`(420 tape)**: 40 items with long padded
  hooks → measured 552 tape → `(None, "presence index is 552 tape, over its 420 ceiling — NOT
  emitted...")`. Control: 1 short item → 79 tape, index returned, not `None`.
- **(e) `_LIVE-STATE.md` has no `⏱` delta section** (`chain_parts`): `_LIVE-STATE.md` present with
  ordinary prose but no `## ⏱` heading → `(None, None, "_LIVE-STATE.md has no ⏱ delta section —
  chain UNMEASURED, not assumed zero")`. Control: `_LIVE-STATE.md` with a `## ⏱ DELTAS` heading →
  returns a real `(gm_part, delta, how)` triple, refusal absent.

VERDICT: PROVEN-BY-MUTATION, all five arms, each with its own control.

---

## Summary

**30 of 30 UNCOVERED rows attempted this pass. 30 PROVEN-BY-MUTATION (fixture + verbatim red +
green control on every row). 0 UNPROVEN. 0 CANNOT-TEST-SAFELY.** No row required a live-repo
mutation — everything ran against tempdir fixtures or in-process monkeypatches, restored before
the process exited, never touching `knowledge/_capture_gate.py` or any file under the real repo.

**Rows that required re-arming a shipped constant / faking an import, named so this cannot be
mistaken for a repaired gate:**
- #50 — `SIZE_BUDGET_TK["compactable_block"]` re-armed from `None` to `100` **in a throwaway
  process only**, to prove the dead `else:` branch's own arithmetic is sound. Control confirms
  the SHIPPED state (`None`) still leaves this branch genuinely unreachable — Phase 1's finding
  stands, now on a run rather than an inference.
- #70, #75, #78, #81 — `sys.modules[...] = None` used to simulate an import failure (the same
  technique the file's own `selftest_growth` uses on `tiktoken`).
- #71, #76, #82 — a single function attribute monkeypatched on the already-imported sibling
  module to force a refusal/exception, restored immediately after.

**Two documentation findings from Phase 1, now checked against a run rather than left as
inference:**
- #42 — the `_gm_fixture` comment claiming `title=False` "bites the absent-title path
  deliberately" is now CONFIRMED sound as a mechanism (the fixture, run directly, does produce
  the FAIL it claims) — the defect Phase 1 found (no call site in the file's own selftest ever
  passes it) is unchanged; this pass proves the arm works, not that the suite now covers it. That
  is Dave's/#63's call to make in the file itself, not this pass's.
- #18's control is the cleanest confirmation in this batch that the `RESERVE SPEND — forked to
  Dave` marker, and only the marker, moves the >63% case between FAIL and WARN — same total,
  same band, marker alone flips the tier.

**Surprises:**
- The headline #39 ds-022 mechanism worked exactly as Dave ruled it on the first fixture that
  actually exercised it — no defect found in the mechanism itself, only in its total absence of
  test coverage until now.
- #52 (M8 reorder guard) needed a hand-built GM file because `_gm_fixture` structurally cannot
  reorder its own sections — Phase 1 named this as the reason it was untestable via the normal
  fixture path; it is testable, just not through that specific helper.
- #77 needed reaching into `_gm_usage.py`'s own selftest fixture shape (`GOOD_USAGE`) to build
  valid multi-session testimony quickly — reused rather than reinvented, per the file's own
  "one implementation" discipline.

**Out of scope, not retested:** the `UNKEYED_BLOCKING` no-selftest-pin finding and the general
`_gen_lanes.py --selftest` / `_gm_move.py` boundary Phase 1 named — neither is one of the 30
numbered UNCOVERED claims (the first is a separate flag-note, already verified in-window by the
#63 conductor's replay; the second is explicitly out of this file's scope per the original
brief). Not touched here to avoid re-doing work already settled.

Status remains **DRAFT — not ratified.** Every quoted red above is reproducible from the method
described at the top of this file; nothing here has been folded into `_capture_gate.py`'s own
selftest suite, which remains exactly as Phase 1 left it.

---

## § Ratification #64 (Fable conductor, 2026-07-31)

**RATIFIED.** Conductor replay: the headline row (claim #39, ds-022 / Dave #58's
fail-loud-on-4th-unrollable cross-check) was RE-RUN LIVE in-window from the worker's own
fixture (`outputs/workerB/t1_headline.py`) — red fired verbatim, both controls green
(no-log → silent skip; non-colliding #77 → no fire); the red's text matches
`_capture_gate.py:1527-1529` at source. 30/30 UNCOVERED rows now carry a mutation-red plus a
green control; 0 UNPROVEN, 0 CANNOT-TEST-SAFELY. The #63 headline gap — "ds-022's #58
cross-check is UNTESTED" — is CLOSED by test, not assertion. Coverage findings stand as
recorded; no new defects in the gate's own logic. The gate under test was never modified.
