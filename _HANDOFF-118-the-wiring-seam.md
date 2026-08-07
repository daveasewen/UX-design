# HANDOFF #118 → #119 — THE WIRING SEAM

> ⚠ **This file is NEWER than `_CHAIN.md` and therefore OUTRANKS it.** Read it first, then the chain.
> ⛔ **It will also trip `_session.py`'s R3 CHAIN OVERTAKEN at your wrap.** That is expected and it is
> not a bug. **Fix it at the cause: run the GM/LS roll and `_gen_chain.py` FIRST**, which advances the
> chain past #118 and clears R3 honestly. Both declared escape hatches (`--acknowledge`, `SESSION_ACK`)
> are **DEAD** — tried once each at #117, both rejected. **Do not brute-force the syntax.**
> ⬛ Making ONE hatch real, mutation-testing it with a false reason, and deleting the other name from
> the refusal message is still OPEN and still bucket B. Nobody needs to decide it.

---

## ⛔ STEP ZERO — VERIFY THE PREMISE OF THIS FILE BEFORE YOU TRUST IT

**#118 opened by telling Dave two things that were false**, both read off a mount serving `_CHAIN.md`
at its 20:03 state while disk held 21:30. The handoff's premise and the stale file agreed with each
other, which is exactly why nothing caught it.

★★★ **A STALE MOUNT LOOKS LIKE A QUIET REPO, and two stale sources corroborating each other feel like
verification.** Before acting on anything below:

```bash
cd /sessions/<your-session>/mnt/UX-design
git log --oneline -3
ls -la --time-style=full-iso _CHAIN.md GOOD-MORNING.md    # compare against git log's timestamp
grep -n "YOU ARE #" _CHAIN.md
```

If the newest commit is newer than `_CHAIN.md`'s mtime, **your mount is stale — stop and re-read.**

---

## ★★★ THE #118 FINDING: THE PROOF CASE WAS WRONG, AND THE REAL DEFECT IS A CLASS

`_HANDOFF-117` named `_validate_type_composites.py` as bucket D's proof case:
*"The gate has never been built… Three months of knowledge, zero enforcement."*

**It was built on 2026-07-18.** 10,602 bytes, three checks, Dave's own scope ruling encoded, green
selftest. **`MEMORY.md` said "NOT built" (false); #117 archived it claiming a gate enforced it (false,
the other way).** Three records, one file, three different wrong answers, three weeks.

⇒ **It is not missing. It is UNWIRED — no reference in `_build_all.py`.**

### ★★ AND IT IS NOT ALONE. MEASURED: 29 validators on disk, 25 wired, **FOUR ORPHANED.**

**Each of the four failed for a DIFFERENT reason, and driving them is the only thing that revealed it:**

| Validator | Written | `--selftest` | Live run | Diagnosis |
|---|---|---|---|---|
| `_validate_compose.py` | 2026-08-05 | **rc=0 PASS** | **rc=0 PASS** | ✅ **Pure oversight.** Green, harmless, two days old. **Wire it immediately — zero risk, zero cost** |
| `_validate_type_composites.py` | 2026-07-18 | **rc=0 OK** | **rc=1** — 1,101 violations / 90 files | ✅ Works, fails **honestly**. Real debt. **Tier is Dave's call — see below** |
| `_validate_screen.py` | 2026-06-29 | **rc=1 CRASH** | **rc=1 CRASH** | ⛔ **ROTTED.** `ValueError: too many values to unpack (expected 3)` — a data shape moved under it. **A crash is not a fail.** Repair or retire |
| `_validate_state_contrast.py` | 2026-07-03 | **rc=1 CRASH** | **rc=1 CRASH** | ⚠ `ModuleNotFoundError: playwright`. **Environmental, not logical.** May be fine in CI. `pip install playwright --break-system-packages` + browser download before judging it |

★★★ **THE LESSON, and it is the whole session:** *building* the instrument was never the hard part —
**wiring** it was, and wiring is the one step with no gate on it. A validator can be written, reviewed,
committed, remembered, and cited in memory without ever entering the build list. **A file's existence
is not evidence of its enforcement.** [[instrument-without-a-consumer]]

⚠ **A count would have found all four. Only RUNNING them told you which was which** — one oversight,
one rotted, one environmental, one real. **Do not let #119 sort these from the table above without
re-driving them.** [[green-tests-cannot-see-scope]]

---

## ⬛ THE ONE OPEN QUESTION FOR DAVE — PUT TO HIM AT #118, NOT ANSWERED

He was asked and did not rule. **It stays his. Do not absorb it, do not re-word it, do not re-put it
as a fresh option set.** His exact choice, as put:

> Wiring the type gate is mechanical; **choosing its tier is not.**
> **(a) BLOCKING now** — honest, build goes red immediately on 1,101 violations; nothing else ships
> until they're fixed.
> **(b) SHRINK-ONLY RATCHET at 1,101** — enforcing today against any new violation, existing debt
> declared and drawn down.
>
> **Claude's recommendation: (b)** — with the risk named by Claude, unprompted: **a baseline set to
> today's count has exactly the shape of "a cap raised to clear its own gate."** The claimed
> difference is that it may *only shrink* and is declared as debt rather than absorbed as a pass.
> **If Dave doesn't buy that distinction, (b) is not defensible and (a) is what's left.**

⚠ **If (b) is ruled: re-MEASURE the baseline at the moment of wiring.** Do not copy `1101` out of this
file — it is a measurement with a date on it, and [[measure-dont-convert-units]] applies.

---

## THE #119 EXECUTION PLAN, IN ORDER

### ① BUILD THE WIRING GATE (bucket D — Claude's, nobody decides it)

**The seam:** the moment a `_validate_*.py` lands on disk without an entry in `_build_all.py`.
**The gate:** assert every `knowledge/_validate_*.py` appears in `_build_all.py`'s step list **or**
carries an explicit, named exemption. Fail loud with the orphan's filename.

- Model it on the existing tuple format: `("human description", "_validate_x.py", ["--selftest"])`.
- **It must ship with its own bite-test and be wired in the same pass** — the standing rule is
  *"every new gate ships one AND wires it."* A wiring gate that is itself unwired is a joke that
  writes itself.
- **Mutation-test it properly:** remove a REAL entry and confirm it fires; add a fake orphan and
  confirm it fires. ⚠ [[mutation-tests-the-clause-not-the-feature]] — #104's lesson is that a mutation
  exercising only DETECTION never proves REMEDIATION. Test both directions.
- ⚠ `$?` after a pipe is the PIPE's exit code. Capture rc with no pipe, or `PIPESTATUS`. **#118 nearly
  mis-read the type gate as "reports FAIL but exits 0" for exactly this reason.**

### ② WIRE `_validate_compose.py` (green, zero risk) — then the other three per their diagnosis

### ③ DRAIN THE REST OF BUCKET B — all Claude's, none are Dave's

| # | Item | State verified at #118 | Next action |
|---|---|---|---|
| **15** | `#89-D2` ruled-not-enacted | ✅ **0 occurrences** in `_state.json` across 4 probes (`89-D2`, `89_D2`, `s89`, `witness`); ×6 in `_MEMENTO-DECISIONS.md` | Enact into the store |
| **13** | `CTRL` gate vocabulary unswept | ✅ `_DS-IMPROVEMENTS.md:676` states it verbatim; **1,869 selectors skipped** by the `CTRL` regex | Run the sweep |
| **9** | `--pri-hover`: 35 of 40 names | ✅ confirmed not started | ⚠ **Sweep PER THEME, not globally** — a global sweep manufactures ~35 false findings because the four themes are *expected* to diverge on one name. **The scope ruling that follows is DAVE'S** |
| **7** | surface-recorder constants | ⚠ PARTIAL — found `NOISE_FLOOR_TK = 708`, `55_025` refs; **all three not isolated** | Finish isolating, re-measure, refresh |
| **10** | `ds-025` — split the 56,308 | UNPROBED | Tokenisable off disk in one pass |
| **11** | G5 ceilings in TAPE | UNPROBED | ⚠ **Measure BOTH sides in the ceiling's own unit before sizing any cut** |
| **14** | p4/p6/p7 reachability | ⚠ **CONTRADICTED** — `_validate_standing_instructions.py` **PASSES**, 28 docs reachable | ⛔ **DO NOT CLOSE.** Known **P-SET COLLISION**: two sets share these numbers with **opposite** statuses. Confirm WHICH set before declaring anything |
| **17** | "ds-020 FENCED" | ⚠ Looks stale — `_DATAVIZ-DECISIONS.md:707`: **ds-020 ENACT APPROVED by Dave at #69 (D1)** | Confirm, then close **by addition** |

### ④ OWED CORRECTION — inscribe at #119's wrap, BY ADDITION

`notes/_GAUGE-LOG.md`'s **#117 post-mortem carries false compaction figures**: 18,367 / −12.1% /
105 entries. **Disk truth: 19,088 bytes / −8.69% / 107 entries**; `_HANDOFF-117` is the one that's
right. **Correct by ADDITION — leave #117's lines verbatim.** A known-false figure that nothing chases
is the assertion-propagation class.

---

## ⛔⛔ DO-NOT-RULE — ALL DAVE'S, UNTOUCHED BY #118

`CONTROL_TIER_44` NOT flipped · `MARK_TIER` stays `warn` · `BOOT_FIRSTTURN_TK = 65_400` NOT refreshed ·
boot floor **75,899** NOT changed · boot re-base to 54,859 ±850 **his and UNTAKEN** ·
`DOFIRST_INDEX_TK_MAX = 700` NOT raised · the three surface-recorder constants NOT refreshed ·
**`G1`–`G17` all open** · graph-mark demotion **NOT RULED** · v1 designer-pack
frozen-until-rebaked-vs-belt-and-braces · mono grey ramp (**he said NOT NOW**) · SC dark (G14) ·
dv-lockup's 3 placeholder titles · G8 retire-or-pin · **the type-gate tier (a)/(b) above.**

⛔ **Do NOT widen an error bar or edit a constant to fit a gate.** ⛔ **Do NOT raise a cap to make a
gate pass** — `_validate_behaviour.py`'s 32.9-vs-32 red is PRE-EXISTING and DECLARED; leave it red.
⛔ **Bucket A items keep their EXACT original wording** — a re-worded question is a new question.

---

## STATE AT HANDOFF

- ✅ **#117 IS COMMITTED** — `675a626`, Aug 6 21:30, subject self-certifies as #117 (verified by hash
  and diff, not by banner). Chain routes to #118. Structural rehearsal fails **8 → 0**.
- ✅ **The bucket sort is DONE and Dave has seen it** → `_TRIAGE-118-bucket-sort-v1.md`.
  **Result: 8 of 17 were never his** (+1 stale, + bucket D entirely Claude's), leaving 8 genuinely
  his — **2 of which are blocked on Claude, not on him.** The #117 claim *"roughly half was never
  Dave's"* **HOLDS.**
- ⚠ **Counter-evidence, declared:** **9 of the 17 were sorted on their nature without being probed.**
  Item 8 is this session's proof that a confident judgement about an unprobed item can be wrong in
  three directions at once. **#119 should probe before enacting any unprobed row.**
- ⬛ **Bucket D's own triage is INCOMPLETE.** #118 named two seams (the wiring seam; the stale-mount
  seam) and built neither. The wiring gate is spec'd above. **The stale-mount seam has no gate yet and
  may have none available** — if so, say so plainly and retire it rather than carrying it as a
  reproach.
- **Dirty at handoff:** `notes/_REHEARSAL-LOG.jsonl` (appends only) · `_TRIAGE-118-bucket-sort-v1.md`
  (new) · this file (new). Memory files are outside git.
- ⚠ A 0-byte `.git/index.lock` recurs from ordinary read-only `git status`. **It is the delete-guard
  signature — stale and safe.** `mv` it to `_to_delete/_stale_locks/`, **never `rm`**; a `mv` to
  `/tmp` FAILS. **Do NOT ask Dave whether GitHub Desktop is open** — he pushes via Desktop by design
  and never touches a shell; routing agent-solvable work to him is a defect in the step.
