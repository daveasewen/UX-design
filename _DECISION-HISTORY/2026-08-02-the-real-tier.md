# The real tier — #82, and the three bugs that were invisible because the suite was healthy

provenance: local_abea69dc-b187-48bb-b55b-1b183bd96323 · 2026-08-02
status: ruled — `notes/_MEMENTO-DECISIONS.md` § ★ #82 (#82-D1, Dave)

*Spine: `_LIVE-STATE.md` ⏱ #82 delta · ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #82 ·
trigger index: `knowledge/_rulings.json` id `ds-021-D1-82` · predecessor:
`_DECISION-HISTORY/2026-08-02-the-trigger-index.md` (#81) and
`notes/2026-08-02-81-cross-instrument-gate-blast-radius.md` (the sweep this session built on).*

---

## 1. The ruling, and what it did not reopen

Dave, at the #82 opener, choosing from a priced set: **wire `measure_tokens()` to the native
counter, and re-stamp the LIVE budget claims in the same pass.**

⚠ **The UNIT was not on the table and was not reopened.** It is his, ruled at **#54**: one unit,
real Claude tokens; `cl100k` a labelled estimator, *"never a unit a cap is stated in."* #81 ruled
the enactment SHAPE (C) and built the gate that named the defect. #82 is the enactment itself —
28 sessions after the unit was ruled, which is the fact the whole #80/#81/#82 arc is about.

★ **The recommendation came after a probe, not before one.** The option Dave picked carried a
measured blast radius (35 call sites in 3 files; 3 `measurement_degraded()` consumer files) rather
than an assurance. A recommendation without a probe is a preference.

---

## 2. What the probe changed before a line was written

**The premise verified, and the mechanism was not what a reasonable check would have found.**
`gauge.count()` returned `(10351, 'real')` in a sandbox whose environment holds **no API key** —
`os.environ` names nothing. The key lives in a gitignored `API-KEY.txt` at the repo root, read by
`_gauge_tokens.read_key()`. A session probing `os.environ` would have concluded "offline, real tier
unreachable" and built the wrong thing. **The decisive probe was novel text** — content that cannot
be in the content-keyed cache — which returned `(34, 'real')` and settled it.

**Two corrections to #81's own blast-radius note, at source.**

- That note lists `_validate_package_delta.py` (6 refs) as a `measurement_degraded()` consumer
  **reaching the shipped Memento package**. Quoting all six: they are **symbol-parity** checks —
  `PORTED_FUNCS_A` (:86) names the function, ARM2(b) (:479) deletes it to prove the check bites.
  **Not one reads the return value.** The package risk was real for the NAME and nil for the
  SEMANTICS. [[unmatched-grep-is-not-an-absence]], with the sign flipped: a *matched* grep is not a
  presence either, and the fix is the same — quote the line.
- The risk the note did **not** name is the one that shaped the build: **`_gen_chain.py:156`
  consumes `measurement_degraded()` as a HARD REFUSAL** (`return None, …`).

⇒ **This is why `measurement_degraded()` was deliberately NOT widened to mean "not real".** The
obvious follow-through would make `_CHAIN.md` ungenerable on any machine without a key — the build
dies offline, and the read chain is the one artefact a cold session cannot start without. Same
shape as `ds-022 (d)` vs `roll_2f`: **a new gate making a correct state unreachable.**

---

## 3. What was built

**Add-on-top, never replace.** `measure_tokens()` tries `gauge.count()` first and returns
`(n, 'real')`; the cl100k → bytes cascade beneath it is untouched and keeps its exact method
strings, so #59's two guards, M6's bites and every pinned label still mean what they meant. Where
the real tier is unreachable the function behaves exactly as it did the day before. Replacing the
cascade would have welded a unit change to a fallback rewrite — one sentence, two problems, one
fixed.

**Three questions, three functions, one vocabulary.**

| function | asks | consumer |
|---|---|---|
| `measurement_degraded()` | *is this reading a GUESS?* — **unchanged on purpose** | `_gen_chain.py`'s refusal |
| `measurement_tier()` | *`real` · `cl100k` · `estimate`* — **the word the vocabulary lacked** | the stamps, `unit_word()` |
| `measurement_mixed()` | *did this PROCESS use two instruments?* | the fixed point |

`measurement_mixed()` was born from the fixed point, not from tidiness: `_CHAIN.md` asserts its own
size, real and cl100k differ by ~1.55×, and a run that reached the API on one iteration and fell
back on the next would either oscillate forever or bake two units into one file — **both of which
look exactly like a content change from outside.** #59 refused a chain built on a *guess*; this
refuses one built on *two instruments*.

**And the unit WORD is now measured, not typed.** Both `_gen_chain.py` templates said `tape` as a
literal for 49 sessions. The moment the numbers became real tokens the word stayed `tape` — **a
real measurement wearing the estimator's name, in the one file every cold session reads.** The
generator now asks the instrument on every build; offline it will honestly say
`tape (cl100k ESTIMATE)`. ★ The generalisation: **the ds-021 defect was never the arithmetic. It is
a claim about a unit that nothing checks** — and it reappears one layer out every time the layer
below is fixed.

---

## 4. The three bugs mutation-testing found, and why each was invisible

★★ **All three were invisible precisely BECAUSE the suite was healthy.** That is the thread.

**(1) The mutation that should have bitten and did not.** Deleting the real tier out of
`measure_tokens()` left the audit **green**. Two reasons, neither reachable by any regex:
a **classifier is not a producer** (`_tier_of()` ends `return "real"` — it sorts method strings, it
never measures), and a **test fixture is not code** (this file holds the string literal
`'    return n, "real"\n'` as a bite fixture; scanned as text it is indistinguishable from the
thing it is a fixture *for*).

⇒ The check now reads **structure, not text**: `_produces_real_tier()` walks the AST for a `return`
whose value is a **tuple ending in `'real'`**. The tuple requirement is not a trick — it is this
project's own rule made checkable: *the method travels WITH the number, as a tuple, on purpose.* A
producer hands back `(n, 'real')`; anything returning the bare word is talking *about* the tier.

★ **This was a hole in #81's audit, not only in my new bite** — `unit_vocabulary_audit()` did the
same whole-file regex. Fixed at the class. [[gate-must-quote-what-it-forbids]] pushed one level
further: **where SCOPE is not enough, read the STRUCTURE.**

**(2) A guard that could not fail, hiding in the suite's own health.** The probe-pollution check —
`_tier_probe()` must not write into `_TIERS_SEEN`, or a health probe makes `measurement_mixed()`
true by its own footprint — was written the obvious way: snapshot, probe, compare. It
mutation-tested **green**. By the time it ran, the process had already measured with `cl100k`, so a
polluting probe added a member **the set already had**. The fix is to empty the set first, so the
delta can exist where the assertion reads it. [[invariant-cannot-discriminate-reversal]].

**(3) Three test arms had silently stopped testing anything.** The repo-wide idiom *"hide tiktoken,
therefore the measurer is degraded"* was sound until a REAL tier sat **above** the whole cascade.
On a machine with a key, hiding tiktoken now degrades nothing: `_capture_gate.py`'s M6 and #59 arms
and `_gen_chain.py`'s degraded-instrument arm would all have gone **green by bypass**. The
`_gen_chain` arm *failed* rather than passing — the bite working — which is what exposed the class.

⇒ **The general rule, now written into all three sites: forcing a fallback means suppressing EVERY
tier above it, not just the one you were thinking of.** [[scope-blindness-gate-vocabulary]].

**Result: 5 mutations, 5 distinct named bites, revert green.**

---

## 5. The selftest runs on the deterministic tier — a declared choice, with its measurement

With the real tier live the suite made **232 API round-trips** (the content cache went 19 → 251
entries) at ~0.24s each and blew the sandbox's 45s call wall. Suppressed, the identical suite is
**16.3s, EXIT=0**. The cause is structural: a selftest measures hundreds of *synthetic* fixtures,
every one a fresh content hash and therefore a guaranteed cache miss.

★ **The justification is not speed, it is what the numbers are for.** A fixture's token count is
never published against a budget; it exists to prove a code path bites. The rule the project
actually holds — **one instrument per PUBLISHED number** — is untouched: build and wrap, where every
stamp is produced, run on the real tier. And the suppression is **not silent**:
`selftest_real_tier_reachable()` unsuppresses for one probe and PRINTS the tier it observed, so a
run always says which instrument it reached. [[instrument-without-a-consumer]] — a switch nothing
reports on is a switch nobody audits.

---

## 6. The re-stamp, and the one thing it was forbidden to do

Verified **against the artefacts**, never a banner: GM stamped **43,555** = measured 43,555, method
`real`; `_CHAIN.md` footer **11,032** = measured 11,032, method `real`, fixed point in 2 passes.

⛔ **History was NOT re-denominated.** Readings in `notes/_GAUGE-LOG.md` and the archived strata are
*correct as written* — they record what was measured, in the unit it was measured in. Re-writing
them would be a false inscription. They need a labelled unit, never a new number.

⛔ **And no delta may be read across the #81/#82 boundary without the like-for-like pair**, which is
why it is published beside the new figures: on the **inherited** text, before any #82 edit, GM was
28,757 tape / 45,069 real and LS 18,658 tape / 28,854 real — **flat** against #81's stamp. The step
from 28.8K to 43,555 is a **re-denomination**, not a gain of a single word. ★ A unit change is the
easiest place in this corpus for real growth to hide, and the pair is what stops it hiding.

**What it costs, in the unit Dave's line is denominated in (working 200,000):** the read chain is
**5.5%** and GM in full is **21.8%**. Every session up to #81 under-priced its own boot by ~37%.

---

## 7. What is open, and why it is open rather than quietly carried

- **#81's per-section attribution in the GM `size:` stamp is its SOLE home** — probed before
  touching it: two matches repo-wide, GM:9 and its generated copy in `_CHAIN.md`;
  `notes/_GAUGE-LOG.md` has no 27.2K/28.2K entry. So it was **kept**, not trimmed.
  [[home-by-addition-then-cut]] — the cut is never the same motion as the move, and the move belongs
  to the 2f roll, which owns that file and whose block form `_build_memento_index.py` refuses to
  have hand-rolled.
- **`_RUNBOOK-context-gauge.md:463–505` still teaches the retired tape/bill system**, contradicting
  line 31 of its own file — and it is now *worse* than it was at #81, because it teaches a retired
  unit **and** a superseded instrument. Assigned to window 2
  (`notes/2026-08-02-82-divvy-window-2.md`), along with `ds-025`'s floor, which is measurable in
  real tokens now and must be **re-measured, not converted**.
- **`_checkin.py` still reports THROUGHPUT in cl100k** and is still registered `estimate-only`. It
  was the instrument used to decide *when to wrap this very session* — so the wrap decision was
  taken on a proxy, and said so.
- **`_measure_tokenizer.py` still has 0 consumers**, re-probed and still zero.
- **§C is over its warn cap** — the mover reported *projected 191 charged lines > cap 150 (block
  225)*, proceeding as designed. Warn ≠ block, and it is declared here rather than absorbed.

---

## 8. The lesson, stated so it can bite something

★★ **A test suite's health is not evidence that its tests are running.** Every one of this
session's three bugs lived in a passing suite: a mutation that could not bite because a *classifier*
satisfied a *producer* check; a guard whose delta could not exist where it was read; three arms
whose forcing idiom had been silently bypassed by a tier added above them. **None was findable by
reading the code, and all three were findable by breaking it on purpose.**

⇒ The operational form: **when you add a layer above an existing cascade, every test that forces a
path through that cascade has just become a candidate for silent bypass.** Go and find them before
you trust the green.
