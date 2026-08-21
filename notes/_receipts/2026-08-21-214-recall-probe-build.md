# Receipt — `knowledge/_recall_probe.py` BUILT (session #214, `s214-D3`)

**Date:** 2026-08-21 · **Seat:** Opus build sub, session #214 · **Enacts:** `s214-D3` (the recall
probe ordered built), serving `s214-D1` condition (3) (the 200,000–256,000 conditional band).

---

## 1. WHAT WAS BUILT

One file, stdlib-only, 405 lines (`wc -l`, measured): **`knowledge/_recall_probe.py`**.

| Mode | Behaviour |
|---|---|
| `--plant --session N` | Generates **4** random fact-pairs (random key `K1..K9`, random subject phrase, random category → random value; categories and subjects drawn *without replacement*, so no two facts are alike in shape or content). Prints them **once** under a banner saying they are to be read into the window now. Writes `knowledge/_probe/session-N.json` holding **only** keys, question phrasings, per-key `secrets.token_hex(16)` salt, `sha256(salt + normalized answer)`, and `planted_at` ISO. Refuses **rc 2, loud and named**, if a plant file for that session already exists. |
| `--quiz --session N` | Prints the questions only, plus the honesty rule **verbatim**: *"Answer from window memory. Re-reading the transcript, this store, or the plant output is the defect this instrument exists to catch."* Selftest asserts the quiz output leaks no answer. |
| `--check --session N K=v …` (or `--stdin` JSON) | Normalizes (casefold · strip · collapse whitespace · drop trailing sentence punctuation), hashes with the stored salt, compares. **GREEN** = per-key ✓, rc 0. **RED** = names exactly which keys missed, prints `BAND CLOSED for this session per s214-D1 condition (3) — judgment work stops`, rc 1. A **missing key counts as a miss**. Malformed pair, un-parseable stdin, duplicate key, unplanted key, absent plant file → **rc 2**, loud and named. Records `last_check` (at / verdict / missed) back into the store — hashes only, no plaintext. |
| `--status --session N` | One line for a check-in to consume: not planted / planted-but-unchecked / last verdict. Always rc 0 (a status read is not a verdict). |
| `--selftest` | End-to-end in a `TemporaryDirectory`, driving the **real code path** by subprocess (`APOLLO_PROBE_DIR` redirects the store — the selftest never writes to the live `_probe/`). Eleven legs, printed as they run. Any leg failing = rc 1. |

**⛔ Plaintext answers exist nowhere on disk.** Selftest leg 2 proves it by searching the whole
serialized store for each planted value.

**Docstring names the CONSUMER** (the conductor, at every check-in past 150K FILL and mandatorily
in-band per `s214-D1` (3) / the runbook band section) and the **unit discipline**: the probe
measures RECALL — a boolean per key, n = planted keys — and its verdict may never be quoted as a
token figure. It also states the honest limit of the hash design: it makes store-reading
impossible and transcript-scrollback *detectable-by-honesty*, not impossible; and that a green
probe is necessary, never sufficient (judgment work stays illegal in-band regardless).

---

## 2. SELFTEST TRANSCRIPT (verbatim, cold second call — not a claimed run)

```
$ python3 knowledge/_recall_probe.py --selftest
RECALL PROBE — SELFTEST (temp store: /sessions/upbeat-compassionate-darwin/tmp/tmpv0z61kyd)
  ✓ plant runs rc 0 and prints 4 facts — rc=0, parsed ['K1', 'K2', 'K4', 'K6']
  ✓ plaintext answers absent from the store — leaked: []
  ✓ quiz rc 0, carries the honesty rule verbatim, leaks no answer
  ✓ MUTATION (green): all-correct answers → rc 0 GREEN — rc=0
  ✓ MUTATION (red): one wrong answer → rc 1 RED, names the key, closes the band — rc=1
  ✓ MUTATION (red): a MISSING key → rc 1 RED, counted as a miss — rc=1
  ✓ malformed input → rc 2, loud and named — rc=2
  ✓ malformed --stdin JSON → rc 2, loud and named — rc=2
  ✓ double plant → rc 2 refusal (no silent re-plant) — rc=2
  ✓ check with no plant file → rc 2, named — rc=2
  ✓ status line rc 0 and reports the recorded verdict — rc=0

SELFTEST GREEN — mutation-proven BOTH ways; the gate can go red.
RC=0
```

Re-run in a **fresh bash call** (cold start, no state carryover): `COLD-RC=0`, final line
identical — *green tests can't see scope*, so it was driven twice, once cold.

### 2b. BLIND-HARNESS GUARD — proving the SELFTEST itself can fail

*A mutation test proves the clause, not the feature.* A selftest that cannot go red is a zombie,
so the selftest was itself mutated: a copy of the file with `--check`'s verdict return sabotaged
to always `return 0` was run in `/tmp`.

```
$ sed 's/    return 0 if verdict == "GREEN" else 1/    return 0/' knowledge/_recall_probe.py > /tmp/mp/_recall_probe.py
$ python3 /tmp/mp/_recall_probe.py --selftest | tail
  ✓ double plant → rc 2 refusal (no silent re-plant) — rc=2
  ✓ check with no plant file → rc 2, named — rc=2
  ✓ status line rc 0 and reports the recorded verdict — rc=0

SELFTEST RED — 2 leg(s) failed: ['MUTATION (red): one wrong answer → rc 1 RED, names the key, closes the band', 'MUTATION (red): a MISSING key → rc 1 RED, counted as a miss']
SABOTAGED-RC=1
```

The harness detects a broken red arm. The live file is untouched by this experiment (the sabotage
lived only in `/tmp`, inside the sandbox, and is gone with the call).

---

## 3. WIRING DECISION — `_checkin.py` NOT TOUCHED (deliberate, priced below)

**Decision: DO NOT WIRE this session.** The brief's safety rule ("if there is ANY doubt, do not
touch `_checkin.py`") binds. The doubt is not vague — it is three concrete, named obstacles found
by reading the code:

1. **`verify_block()` leg 0 is an EXACT-SHAPE check.** `knowledge/_checkin.py:521-526`:
   `if len(lines) != len(BLOCK_FIELDS) or got != list(BLOCK_FIELDS): return (False, [SHAPE …])`.
   A sixth-plus `PROBE:` line makes every previously-emitted block fail SHAPE outright, and the
   refusal explicitly says *"nothing further was checked"* — the whole seam check goes dark, not
   just the new line.
2. **The integrity digest hashes the WHOLE body list** (`_digest()`, `:474-486`), so adding a
   line is not additive: it changes `BLOCK_FIELDS`, `render_block()`, `verify_block()`'s leg-3
   field indexing (`for i, field in enumerate(…, start=1)`), and the hand-forging inside
   `selftest_block()` (`:690-704`) which retypes a body and recomputes the digest by index. That
   is four coupled edit sites — the opposite of a minimal diff.
3. **A probe line is NOT re-derivation-stable, and that is the killer.** Leg 3 re-derives every
   non-BUDGET field from live state and demands textual equality. The probe's status *changes
   between render and verify* precisely when it is doing its job (the conductor quizzes itself
   between the two), so a correctly-emitted block would go `NON-REGENERATED` for an honest
   reason. BUDGET is excluded by construction for exactly this reason; a probe line would need
   the same carve-out, which is a design change, not a wiring change.

A broken check-in is far worse than an unwired probe, and *a conflated fix guarantees
recurrence*. So the wiring is priced rather than performed.

### PRICED WIRING NOTE (for Dave / the conductor, not ruled here)

- **Option A — zero-risk, no code (recommended first):** the conductor runs
  `python3 knowledge/_recall_probe.py --status --session N` **beside** `_checkin.py` at each
  check-in past 150K and pastes its one line into the check-in report. Cost: one extra command
  per check-in. Touches nothing hashed. **Available today.**
- **Option B — proper wiring, ~M:** add `PROBE` to `BLOCK_FIELDS` *and* to the BUDGET-style
  re-derivation exclusion list, update `render_block`, `verify_block` leg 3, `selftest_block`'s
  forger, and any fixture blocks; then prove the seam both ways (a hand-edited probe line must
  still fail INTEGRITY). Estimate: 4 coupled edit sites + 2 selftests, one focused session-lane,
  **planning estimate, not a measurement**. Should only be done with the `--verify-block`
  selftest driven before *and* after.
- **Option C — reject:** leave the probe deliberately out-of-band of the plan block, on the
  argument that the block is a *rendering of committed state* and a live probe verdict is not
  that. Cheapest, and Option A already covers the operational need.

**This is Dave's / the conductor's call — not ruled by this sub.**

---

## 4. DOC-ROW GATE

```
$ python3 knowledge/_gate_doc_rows.py --check
doc-row gate: population 35 (added >= 2026-08-15, PICKED) · of which staged-in-THIS-commit 0 (#207 postscript: the single-commit blindspot) · unrowed 0
✅ PASS — every in-scope document has a store row.
GATE-RC=0
```

⚠ **Gate glob scope rule** — this gate's population is *git-tracked* `notes/_briefs/*` and
`_BRIEF-*` only (`_gate_doc_rows.py:8-9,99`). Neither `knowledge/_recall_probe.py` nor this
receipt is in its scope, so its PASS is **not** evidence that they are rowed. Per the
forgotten-document class (#185), the conductor still owes store rows for both. `_state.json` was
not edited by this sub, as instructed.

⚠ Also note: two **untracked** briefs are sitting in the tree
(`notes/_briefs/2026-08-21-214-conditional-band-200-256-proposal-v1.md`,
`notes/_briefs/2026-08-21-214-context-territory-strategy-v1.md`). They are outside today's
population *because they are untracked* — the moment the conductor commits them they enter the
gate's scope and will be flagged unless rowed in the same commit (that is precisely the #207
single-commit blindspot the gate's own header names).

---

## 5. RESIDUALS, PRICED

| # | Residual | Price / owner |
|---|---|---|
| R1 | **Not yet driven on real data.** `s214-D3` requires it to RUN this session. The selftest is end-to-end but synthetic; no live plant was made (the sub is forbidden a real plant). | Conductor: `--plant --session 214` early, then `--quiz`/`--check` at each check-in past 150K. ~1 min. **Until then `s214-D3`'s "must RUN this session" is UNMET** — the build is enacted, the drive is not. |
| R2 | Check-in wiring unbuilt (§3). | Option A costs nothing and is available now; Option B ~M, Dave's call. |
| R3 | Store rows for `_recall_probe.py` + this receipt not created (out of the doc-row gate's glob, and `_state.json` is do-not-touch for this sub). | Conductor, at the wrap. |
| R4 | **Transcript scrollback is not preventable.** The hash design makes store-reading impossible; it makes re-reading the plant output *detectable only by honesty*. Declared, not papered over. | Unfixable by construction. The rule is printed in the tool's own output at plant and at quiz. |
| R5 | `n=4` and the fact vocabulary are **PICKED, not derived**. `s214-D3` says 3–5; 4 was chosen as the midpoint. Difficulty is uncalibrated — no evidence yet on whether these facts are too easy at 250K. | Re-visit after ~3 real in-band sessions; a probe that never goes red on a real regression is a zombie in the other direction. |
| R6 | `--status`'s verdict is only as fresh as the last `--check`; a stale GREEN from 80K FILL says nothing about 240K. | The status line prints the check timestamp; a consumer must read the time, not just the word. Option B wiring should enforce an age limit like the block's. |
