# 2026-09-08 · #256 — re-cutting v1.0.6 twice, enacting a dream pass in his order, and cutting the boot index at the one wrap that cannot measure the result

provenance: 256 · 2026-09-08
status: observed

*Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA #256 · banner: `GOOD-MORNING.md` § ★ LATEST #256 ·
carries: `_CARRIES.md` § `## residual → #257` · rulings: `knowledge/_rulings.json` § `s256-D1`, § `s256-D2` ·
lane report: `notes/_subreports/2026-09-08-256-DREAM-ENACT.md` · wrap report:
`notes/_subreports/2026-09-08-256-wrap.md`. Both-way linked; lands whole; never silently edited after.*

---

## Why this is a dossier and not just a ledger line

Three things happened today that a terse record cannot carry: a release cut had to be run **twice** and the
reason is a ruling that changed what a pack *contains*; a gate went **red without anything breaking**; and the
long-owed boot cut landed in the one seat that is structurally unable to observe whether it worked. Each of
those is a WHY, and each of them will be misread at #257 if only the WHAT survives.

## 1. The re-cut ran twice because the first cut asked a question

The session opened on a carry Dave owns: re-cut v1.0.6 at a gate-clean HEAD. #255 had left HEAD gate-clean for
the first time since #248 (the bento reds paid, C9 green), so the cut was cheap for the first time.

The first cut (`311723a`, manifest at `b15b7d9`) came back clean on every arm — 1,669 files,
`--manifest-check` PASS, `--drift` PASS, dry-run zip `--check` GREEN — and with one thing that was **not** a
failure: the runnability probe reported a **new REPO-BOUND entry**, `knowledge/_validate_roles_resolve.py`,
the validator lane C built at #253. REPO-BOUND means the shipped pack contains a gate that cannot run from the
pack, because the data it validates (`roles.json`, `shapes.json`, `when-fields.json`) is repo-side only.

★ **The finding is that a clean gate run produced a decision, not a verdict.** The probe was not complaining;
it was describing a pack that ships a lock without its key. Putting that to Dave as one weighted item got a
one-line answer — *"ship, I always lean toward completeness over convenience"* — which became `s256-D1`, put
the three data files into `GATE_DATA_CANDIDATES` (generator selftest 216/216) and forced the **second** cut at
`1f4c355` (`3c8832a`): 1,673 files, 43,160,016 B, manifest sha `abb080c52ea771ea`, and the probe moving the
roles validator from REPO-BOUND to **RUNNABLE** — 41/9/4 against 40/10/4.

⚠ **The second probe reading is the ruling's effect MEASURED, not asserted.** That is the whole reason the cut
was run again rather than the manifest hand-patched: a re-run is a proof, an edit is a claim.

## 2. A gate went red because its subject is half-updated by design

At the wrap seat, `_gate_release_audit.py --pack` prints:

```
❌ apollo-spider/dist/Apollo-Spider-v1.0.6.zip does NOT match the manifest at 1f4c35587f30
   6 manifest path(s) MISSING from the pack …
   79 file(s) differ from the commit's blobs …
   pack README does not carry the commit sha 1f4c35587f30
   the shipped _MANIFEST.json is not the status-free derivation of the repo-side manifest (s223-D8)
```

Nothing broke. `dist/` was deliberately untouched (v1.0.6 stays **PROPOSED**; ratification is `s219-D4(2)`,
Dave's alone), and the manifest moved twice today. The gate is comparing a #245-era pack against a #256
manifest and correctly says they differ.

⛔ **What makes this worth a dossier is the inversion.** One wrap ago, #255 used this same gate's **PASS** to
retract a carry that had been wrong for ten sessions ("the v1.0.6 zip is still missing"). One wrap later the
same gate is red on the same file. ★ **A gate whose subject is half-updated by design reads exactly like a
gate whose subject is broken** — and both readings are true statements about different questions. The record
therefore says which question each one answered, rather than carrying "the pack gate is red" forward as a
defect somebody should fix.

The honest state, written once: **the pack is #245's, the manifest is #256's, and closing the gap is a
ratification Dave has not given.**

## 3. Dream pass 11, enacted in his order

`s256-D2` — *"do it in your order"* — is a batch authorisation, and the order mattered because the four
proposals are not independent: P2 changes how many hooks the gardener grades, and P1(a) alarms on exactly that
count changing. Enacting P1(a) first and P2 second means the population alarm's first live reading is the
change P2 caused (`47 vs 33 (+14)`), which is growth and therefore only warns.

The lane (`af6fa00854d260f91`, 108,386 subagent tokens) proved each of the four with a mutation, which is the
standing test: a proof that the CLAUSE bites, not that the feature exists.

⚠ **One thing the lane did beyond the literal wording, and declared as such:** P1(a)'s refusal-on-shrink is
unpassable without an escape, because the sidecar keeps the old count and every subsequent run sees the same
shrink. `--accept-population-change` exists for that reason and the refusal names it
[[gate-cannot-pass-in-one-environment]]. That is a build decision, recorded as a call, not a ruling.

⛔ **And one premise expired between the proposal and the enactment.** P4(a) argued that
`knowledge/_screen-gate/dashboard.md` was untracked. At enactment `git ls-files` lists all ten subjects,
dashboard included, so the new P4(b) arm is green today and refuses nothing. **The premise expired; the
question did not** — whether dashboards are permanent gate subjects is still unanswered and still his.

## 4. The boot cut landed where it cannot be measured

`MEMORY.md` — the auto-memory index, **outside the repo** — went from 2,616 to 1,794 tape against a 1,802 cap,
with hooks #237–#251 moved verbatim into `hook-overflow-2026-09-08-256.md` and the index left as a declared
stub carrying only the ⛔/★★★ tier. `_memory_cap_check.py` reads ✓ WITHIN CAP.

This is half 2 of the `s214-D6` boot-reduction pair, owed since #214 and finally paid.

⛔ **And it changed nothing about today's reading.** Boot at #256 was **70,241** — 241 over the shrink-only
70,000 ceiling, 114 *above* #255's 70,127, the seventh reading in a rising series and the second consecutive
breach. ★ **The cut and the reading are in different budgets and on different clocks:** the index is read at
the *next* session's first turn, so a wrap that cut the boot still books a breach, and the only honest thing to
write is the breach plus the date the answer arrives.

⚠ **The failure mode this avoids is specific and tempting:** publishing "boot cut, 822 tape" beside "boot
70,241" invites the reader to net them into a claim nobody measured. They are reported separately, never
summed [[measure-dont-convert-units]], and the real figure is **#257's first turn**.

## 5. What the gardener says about the cut index, and why it is carried

A dry-run on the *cut* index grades **37 hooks — FRESH 24 · AGING 6 · STALE 2 · UNPROVABLE 5**. P2's own live
reading was **47**. Both are real; they are readings of two different files taken either side of the cut, and
neither is averaged into the other.

The two STALE hooks — `retrieval-default-hides-the-ruling.md` and `tape-unit-is-not-real-tokens.md` — both name
`_measure_tokenizer.py`, which is absent from the repo. ⛔ **Carried, not fixed:** the store is outside the
repo and invisible to every gate (D1a), and grading is the gardener's job, not a wrap's.

## Resolved state

- v1.0.6 manifest re-cut at `1f4c355`, **PROPOSED**, `dist/` untouched, ratification his.
- `s256-D1` and `s256-D2` inscribed by the conductor at entries 394/395, read back at the wrap seat, not
  re-inscribed.
- Dream pass 11: P1(a), P2, P3(b), P4(b) enacted with mutation proofs at `44c8061`.
- `MEMORY.md` cut to 1,794 tape, within its 1,802 cap.

## Still open

**His:** v1.0.6 ratification · P1(b) (grade the overflow) · `POPULATION_DELTA_THRESHOLD = 5` · dashboards as
permanent gate subjects · Q2–Q6 · R1 · the boot-ceiling literal and what to cut next · what a midnight-spanning
wrap stamps · which scopes may write a literal `repeat(n)`.

**Measured but unowned:** the `--pack` red above, which is a ratification away from green and a defect away
from nothing.
