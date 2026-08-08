# #130 — the pointer repairs, and the subject that certified the wrong session

```
provenance: 130 · 2026-08-08
status: observed
```

**Spine entry:** `_LIVE-STATE.md` ⏱ LATEST DELTA #130 · **Ledger:** `notes/_MEMENTO-DECISIONS.md` § ★★ #130
(rulings `s130-D1`…`s130-D6`) · **Banner:** `GOOD-MORNING.md` ★ LATEST #130 · **Measurements:**
`notes/_GAUGE-LOG.md` § `#### 2026-08-08 #130`.
Both-way links per `_DECISION-HISTORY/README.md`.

---

## Why this dossier exists

Two threads ran, and they turned out to be the same thread. One was the nine-session-old red in
`_capture_gate.py --selftest` — thirty rotten pointers in `knowledge/_rulings.json` that Dave had
ruled off-limits to agent repair. The other was #129's finding that **both #128 commits certify the
wrong session**. Both are records that were true when written and that nothing re-checked; both were
closed by moving from a stored conclusion to a generated one. `s129-D5`, one day old, describing its
own next session.

## The arc

### 1. The green that was false on the committed bytes

#129 published *"`_governs` selftest: 30"*. #130 booted and measured **32**.

The attribution mattered more than the number. `_rulings.json` was last written at `29b4c2e`;
`_governs.py` has not changed since #127. So the delta could not be code and could not be a fresh
write — it was **`s129-D1`'s own anchor**, born red, because the #129 wrap's step-2f roll relocated
the gauge stratum the anchor named **after** the green had been measured. The ritual invalidated its
own receipt, in the same session, and nothing looked again.
[[check-after-its-own-remedy]] [[no-gate-parses-the-artefact]]

### 2. "One rotten pointer" was never one, and the gate said so in the singular

`_capture_gate.py`'s cross-instrument check appended `g_fail[0]` — **the first failure, alone**. At
#127 that produced the sentence *"one rotten pointer"* against a real population of thirty. The count
was never published. A repair of the first would have re-run the gate, seen a **different** single
line, and filed it as a new defect: an infinite, plausible, wrong loop.

The widening publishes the **count** first and then **every** line as its own failure. It was
mutation-tested — two injected breaks, both surfaced where only the first would have shown before,
file restored and sha-verified. ★ A reporter that truncates its own evidence is indistinguishable
from a reporter with nothing left to say. [[a-crash-is-not-a-fail]]

### 3. The route, not the repair, was the ruling

Dave's `s130-D1` is about **who may speak**. The 18 class-B entries are missing `evidence`/`status`,
and the obvious fix — read the code, write what it appears to say — is the defect, because those
fields record what **he** ruled and a reconstruction from an enactment is an assertion wearing a
citation. So: drafts quote his ratified records, he ratifies, then they are written. Ten drafts, all
ratified.

Two dispositions came with it. The `s123-D1` count conflict was **re-measured** (`gen_theme_cascade
--check` → 198 paths / 206 projections) and **all three figures inscribed with labels** — arc 198,
receipt 189, measured-#130 198 — precisely because a measurement taken today describes today's tree
and cannot adjudicate what #123 saw. And the `s123-D3` TLS clause was annotated `[superseded #129]`
**by addition**, in the store and in the arc file, no dated stratum touched.

Under `s130-D2`'s mechanical licence: class C's 12 prose-in-`evidence` entries became `#127` durable
anchors, and the legacy line-number pointers were converted — ⚠ **9 of them, not the recorded 11**.
The stale `+11` at `_LIVE-STATE.md:75` was **left alone and the delta declared**, because correcting
a record is not a mechanical repair. **Result: `_governs --selftest` rc=0 and `_capture_gate
--selftest` rc=0, green for the first time since #121.**

### 4. The subject that certified the wrong session

#129 diagnosed it: T3 **replaces** the msgfile's first line with a headline derived from
`GOOD-MORNING.md`'s ★ LATEST banner, and a non-`--wrap` commit therefore inherits **whatever banner is
on disk**. #128 wrote no banner, so it inherited #127's. And the post-commit subject assert compared
the file T3 had just **rewritten** — true, and useless.

Because the behaviour was **by design** (#77-D2 plus #78-D3), the remedy was Dave's, not a repair.
He picked **generate, never inherit**:

- non-wrap commits never read the banner at all; the subject comes from the `SESSION_N` witness,
  today's `date`, and the msgfile's **own first line**, and T3 **refuses** without `SESSION_N` or on
  an empty first line;
- `--wrap` keeps banner derivation but now **asserts the banner's `#N` equals the declared
  `SESSION_N`** and refuses on mismatch.

Five mutation arms verified; subject-fold blank line intact; `bash -n` clean. ★ The general shape:
**the check belongs on the input, never on the artefact the checked step just produced.**
[[commit-subject-is-an-ordering-bug]]

### 5. The colour lane: six rulings, three enacted, and the split said out loud

`s130-D4` (banner actions: ghost/tint, transparent at rest, ink-derived wash, states remapped
pressed 14% / hover 8%, ruled red `#F6604C` → `#B92F1E`), `s130-D5` (check/selection labels always
ink; error on border + message, 17.40:1) and `s130-D6` (chips pressed from each theme's own ramp;
legacy `#767676` under Dave's escape clause) are **ruled and not enacted**. The lane did not fit the
window. They are recorded in three registers with the status *RULED #130 / NOT ENACTED*, and no value
moved in any token file. [[feedback-check-ran-never-reached-plan]]

Two things inside that lane are worth the ink. **Dark mode was ratified and then contradicted by
measurement:** Dave said *"(a) ~8%, (b) all three"*, and measurement showed two of the three already
invert via the cascade while the banner wash **must not** — RAG fills are mode-invariant by his own
`s122-D1/D2/D3`. Nothing was added; the discrepancy was declared back to him. And **the audit's
Banner 4.09 measured the wrong button** — the chromed ghost (`.abtn`, `canon.css:3959`), not the
quaternary that ships. Under the true quaternary the pressed failure **disappears** (15.27) and the
failure **migrates to rest** (8 of 48 readings). The audit and the snippet corpus were not touched:
that question is Dave's.

## What we got wrong

**(a) The instrument existed and was answered "UNKNOWN".** Asked *"how hot are you?"*, the conductor
said *"UNKNOWN — no instrument"* while `knowledge/_checkin.py` existed and was named in its own memory
index. Dave: *"we've had a mechanism for this for ages??"*. ★ #129's sentence *"the conductor could
not read its own `message.usage`"* **corroborated a stale premise**, which is what makes this a
recurrence and not a slip. [[unrun-search-indistinguishable-from-absent-record]]

**(b) Two accidental full dumps of `_LIVE-STATE.md` line 14** — `grep` without `-m`/`cut`. The single
biggest avoidable fill burns of the session, and purely mechanical.

**(c) The wrap opened late.** Fill was already **206,282** when first measured — past the stop line
150,929 *and* the working wall 200,000. No mid-lane check-in ran `_checkin.py`. The rule was honoured
in form (UNKNOWN declared) and not in substance (the instrument was there).
[[checkin-at-the-ends-cannot-catch-the-lane]]

## Resolved state, and what is still open

**Resolved:** the pointer red (nine sessions) · the #128 wrong-subject class, at its cause · the
truncating reporter · the class-B fill route.
**Open:** the enactment lane for `s130-D4/D5/D6` plus tabs and legacy reversed text (licence pending
Dave's word) · the error-mark image confirm (his image did not arrive) · mark-vs-fill 3.0 gate,
build-vs-worklist · two new ratified worklist items (console+SC information rest 3.81/4.13; legacy
success washed) · a named refusal for `_validate_state_contrast.py --selftest`'s silent environment
dependence · the quota panel, asked twice and not given.
