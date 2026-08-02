provenance: 383e10dd-42d4-4e5e-8ef1-0dd5ddbeb367 · 2026-08-02
status: observed

# #84 — the gate that was built, unwired, and then had its unwiring reason re-measured

*Session #84. The conductor half of this session ran to **202,794 real** against Dave's 200,000
working line and only discovered it when Dave asked "how hot are you". Everything the conductor
concluded about the `.md` prose gate was authored **past that line**, and Dave's instruction was not
to transcribe it but to **reanalyse it**. This dossier is that reanalysis, run on a cold budget.*

**Both-way links:** ledger `notes/_MEMENTO-DECISIONS.md` § ★ #84 · spine `_LIVE-STATE.md` ⏱ #84 ·
predecessor `_DECISION-HISTORY/2026-08-02-the-ungated-prose.md` (#83) · handoff
`notes/2026-08-02-83-handoff-to-84.md`.

---

## §0 — THE ONE-LINE VERSION

**Dave's ruling was sound. The gate built to serve it was the wrong instrument. And the reason
written down for unwiring it was itself false, inscribed at the call site, and is now struck.**

Three of the conductor's four conclusions moved under probing. The one that mattered most — that
Dave had ruled the target vocabulary KEPT, so the whole item was a chase after nothing — **is dead**,
and it died on the primary record of the very ruling it cited.

---

## §1 — WHAT DAVE RULED, AND WHAT HAPPENED TO IT

At #84 Dave ruled the `.md` arm should be built:

> *"Option 2 under-delivers. tape/bill is where the observed rot actually happened, and it's
> demonstrably fenceable. Leaving it ungated to avoid a half-measure is the wrong half-measure."*

with two conditions: **(A)** the gate must announce its own scope in failure text *and* docstring —
*"a gate that doesn't say what it excludes will later be read as 'the prose is gated', and that's
this whole thread's founding defect eating its own tail"*; **(B)** fix Half 2 first.

**Both conditions were met.** A worker built `retired_unit_prose_audit()` with the scope sentence in
the docstring and repeated inside every failure string, five mutation tests including one
(`bite 5`) whose entire job is to fail if a future edit deletes the scope clause from the f-string.
Half 2 was fixed. That work is good and it is kept.

**Then the conductor measured the gate against the live tree, formed two conclusions, and unwired
it** — writing the reasons into the call site as a comment. That comment is where the damage was,
because a false reason inscribed at a call site is exactly the confident-false-inscription this
project fears most: it reads as a finding to every session after it.

---

## §2 — CLAIM B: DEAD. THE MOST CONSEQUENTIAL ONE, AND IT DIED ON ITS OWN CITATION

**The claim:** *"the premise is dead — `tape`/`bill` is NOT a retired vocabulary,"* resting on
`ds-021-C — RULED #81-D1 (Dave): "tape/bill machinery KEPT as labelled legacy, not retired"`.

**The conductor flagged their own probe honestly** — *"I read it off the gate's own generated report
line, which is a banner, and this project's standing rule is that repo-state claims are verified
against `git log` or a real run, never a banner."* They were right to flag it, and the flag was
correct.

**The primary record, read at `notes/_MEMENTO-DECISIONS.md` § ★ #81:**

> *"Second half of the same ruling: the tape/bill **machinery** is KEPT as labelled legacy, not
> retired — it is pinned by three selftests and carries `ds-021 (c)`, the standing practice that
> forks the ratio constant to Dave at n≥4. Retiring it as a side effect would have killed that
> fork."*

**The quote the conductor used is verbatim-accurate. The SCOPE is wrong.** Everything #81-D1 names
is CODE: constants, `bill_of`/`fmt_units`/`ratio_status`, three selftests, and a fork that lives in
a script. Not one word about `.md` prose.

**And the same record, eleven lines later, says the opposite about prose.** Under
`⬛ STILL OPEN, DECLARED`:

> *"`_RUNBOOK-context-gauge.md:463–505` still teaches the **retired** tape/bill system"*

⇒ **The session that made the ruling called the PROSE retired, in the same breath as keeping the
CODE, and listed fixing the prose as an open defect.** `notes/2026-08-02-81-cross-instrument-gate-blast-radius.md`
§2 says it a third time: *"the runbook section describing the condition for its own retirement has
outlived the condition."*

★★ **The failure has a name this corpus already owns: a MECHANISM CAN HAVE TWO PURPOSES WITH
OPPOSITE ANSWERS.** `tape` in `_capture_gate.py` is live machinery Dave kept. `tape` in a runbook
sentence teaching a cold session what unit to price in is retired instruction. One word, one
ruling cited, two answers — and reading the ruling off a banner collapsed them.
[[premise-ages-faster-than-rule]]

**The second leg — `TITLE_CAP_TAPE = 120` is a live tape-denominated cap (RULED #60-D8) — is TRUE**
(`_capture_gate.py:873`, consumed at `:1990`). It is also **irrelevant to the premise it was
offered for**: it is a cap in code, not prose instruction. A true fact in support of a false
conclusion.

⇒ **Item (a) was never chasing a vocabulary Dave ruled KEPT.** That sentence would have been the
single most useful line in the wrap if it were true. It is not, and saying so is more useful.

---

## §3 — CLAIM A: HALF-DEAD. THE GATE IS NOT 0-FOR-1; IT IS 1-FOR-2

**The claim:** the gate has zero true positives — the #83 rot was re-enacted verbatim in `/tmp` and
`retired_unit_prose_audit()` returned 0 failures.

**Re-run at #84 against the WHOLE pre-fix file** (`git show HEAD:knowledge/_RUNBOOK-context-gauge.md`,
which is #83 exactly as committed), the audit returns **1 failure**:

```
knowledge/_RUNBOOK-context-gauge.md:723 says 'tape' in region "Entry points"
  — NEITHER exemption
```
line 723, pre-fix: `` `knowledge/_checkin.py` (Half-2 throughput check-in, `tape`/cl100k, ``

**That is one of the two things #83 rotted.** The conductor's own edit list (§3 of their brief, item
2) names it: *"`_checkin.py` was indexed as `tape`/cl100k; corrected to `real` headline since
#83 (c)."* **They hand-fixed it, then measured the gate only against the other half, and generalised
to "never fires on the defect."** [[gap-in-record-vs-gap-in-evidence]] — check the other half before
declaring a hole. Here the other half was in their own change list.

**What survives, and it is the real finding:** the gate is blind to the `### Half 2` half, and the
two halves are different *kinds* of rot:

| rot | shape | word-presence sees it? |
|---|---|---|
| `## Entry points` | a **stale unit index** — a bare `tape` where the answer is now `real` | ✅ yes |
| `### Half 2` | a **false claim about which unit a tool reports**, wearing a *correct* retirement disclaimer | ❌ no — and device (ii) actively EXEMPTS it |

The `Half 2` region says `RETIRED` / `HISTORY` three times — truthfully, about the *original Half-2
design* and the *ds-021 duality*. Those declarations are correct prose. They also grant the region a
blanket exemption under device (ii), under which a *false factual sentence* sits untouched.

⇒ **A declaration marker exempts a REGION, but rot is a SENTENCE.** That is the design limit, and it
is not fixable by tuning the marker list.

### ★★ AND THE MUTATION THAT MATTERS — the gate's own positive control cannot fail

`selftest_retired_unit_prose()` opens with a POSITIVE CONTROL pinning the two regions Dave named,
quoting him: *"if it goes red on either, your exemption logic is wrong — do not fix the prose to
suit the gate."* Sound instruction. But **mutation-tested at #84 by running the control against the
ROTTED tree, both halves are GREEN**:

```
§ 'THE FLOOR IS NOT WILLPOWER'  -> control fires? False  (GREEN)
§ 'Half 2'                      -> control fires? False  (GREEN)
=> control is GREEN on the ROT
```

**A control that passes on the exact defect it was written beside is an assertion, not a test.** It
pins the regions against a *rewrite*; it can never witness a *re-rot*. Nobody wrote this wrong —
Dave's instruction was about false positives, and the worker implemented it faithfully. The gap is
that no one asked the mirror question. [[gate-must-quote-what-it-forbids]] — *or the green is an
assertion.*

### The 11 live failures, judged independently — and "11/11 correct prose" is WITHDRAWN

- **2** in `_ROBUSTNESS-PORTABILITY.md`:13 and :82 — the homonym **"duct tape"**. Correct prose, and
  the conductor is right about these. But they are a **regex defect** in `RETIRED_PROSE_WORDS_RE`
  (`\b(tape|bill)\b`), fixable in a line — not a refutation of the design.
- **7** in `_DS-IMPROVEMENTS.md` (:1709 :1721 :1730 :1732 :1733 :1747 :1751) — correctly cleared.
  Dated historical readings (#82-D1: *"Historical readings are NOT re-denominated"*) and live
  description of the `ds-021(c)` machinery #81-D1 KEPT.
- **2** in `_DS-IMPROVEMENTS.md`:1376–1377 — ⚠ **arguably a TRUE positive, and the conductor cleared
  it.** The line is a present-tense `★ Status: ENACTED #34` assertion reading *"Caps bind on
  `bill`"*, in a region with no retirement marker. #54 ruled one unit, real Claude tokens; #56
  replaced the band. **Caps do not bind on `bill`.** The #81 blast-radius note flagged the
  *identical sentence* in the runbook as the stale canon this whole thread is about — it is
  simultaneously live in a second file, and nobody has looked there.

⇒ Honest score: **1 true positive of 2 available · at most 9 of 11 hits are false · 1 further
suspected true positive in a file nobody had checked.**

---

## §4 — CLAIM C: ALIVE, AND STRONGER THAN ITS AUTHOR THOUGHT

**The claim:** the right gate is a cross-instrument claim check — `.md` prose naming an instrument
and stating its unit must agree with `MEASURERS`. The conductor shipped it as *"my proposal,
authored past the line, never tested… Dave has NOT approved it."*

**Both halves of that caveat are wrong in the useful direction.**

**(1) It would have caught the rot.** The `### Half 2` sentence named `_checkin.py` and stated its
unit as `tape`. `MEASURERS['_checkin.py']` says `real` (since #83 (c)). Prose contradicts registry
⇒ FAIL. **This is the one design checked at #84 that catches the half word-presence cannot see.**

**(2) `MEASURERS` covers the instruments prose actually names.** Measured, `knowledge/*.md`:
`_capture_gate.py` 29 mentions · `_checkin.py` 12 · `_context_gauge.py` and `_gauge_tokens.py` both
present. All four are registered. (Higher-count names like `_build_all.py` 32 are not measurers and
are correctly out of scope — they state no unit.)

**(3) It is not a new shape needing approval.** **#81-D1 (Dave) already ruled the `ds-021`
enactment shape is *(C) a cross-instrument gate*** and it was built as `MEASURERS` +
`unit_vocabulary_audit()`. What is proposed is a **GLOB WIDENING of a ruled shape from `.py` to
`.md`** — the same correction #83 found when it discovered the rule stopped dead at a file
extension. [[gate-glob-scope-rule]]

⚠ **Still not built, and deliberately not built here.** It is a design that survived a probe, not a
tested instrument, and this session's whole subject is the difference. **It is FORKED, priced, and
named as (a) at #85.**

---

## §5 — CLAIM D: TRUE AS HISTORY, NON-ACTIONABLE

The conductor's own first gate design — *"a region mentioning `tape` outside the fence must also
state the live unit"* — fires on `### ★★ THE FLOOR IS NOT WILLPOWER`, which is correct prose
declaring itself inline. **Verified: true.**

**But it was already solved before it was written.** The worker's gate ships **device (ii)**, the
inline declaration marker, precisely for that region — and `DECLARATION_MARKERS` is documented as
*"every marker below is quoted from one of those two [regions], not invented."* The live audit
returns **zero** failures in `_RUNBOOK-context-gauge.md`. Claim D killed a design that had already
been superseded by the one on disk. Recorded so no one re-derives it; not carried forward.

---

## §6 — THE PROCESS FAILURE, UNSOFTENED

Recorded because it is part of the record, not an aside. The conductor's own list, verified:

- **The pre-flight stamp was missed for the FIFTH consecutive session (#80–#84).** #83's handoff
  said in writing that four is *"a missing mechanism, not four accidents"* and that it is the
  instrument that would have caught the overrun **at the opener**. It was read, surfaced to Dave as
  a menu option, **ranked third, and never run.** ★ That is the diagnostic detail: it was not
  forgotten. It was *deprioritised by the session that most needed it*, which is
  [[feedback-read-the-runbook]]'s felt-difficulty inversion in its purest form.
- **Three probes re-priced the job and the gauge was consulted once, when prompted.** A throttle
  used on request is a thermometer.
- **A subagent was dispatched that burned 268,302 tokens, unpriced.**
- **101% was read, and six to eight more calls were then argued for** on a false urgency ("a live
  false claim in the tree overnight") when the fix was already safely on disk.
- Final: `_checkin.py --window 200000` → **202,794 real**, conversation half, THROUGHPUT not fill,
  boot half unmeasurable (`ds-025` item 1).

### ⬛ THE RECOMMENDED MECHANISM — and why the obvious one will not work

**The obvious fix — "add a pre-flight check to the wrap gate" — is already there and it is why the
miss is invisible.** `check_preflight` / `check_preflight_tokens` exist, are wired at `:3024`, and
grade a stamp *when one is present*. They validate CONTENT. **Nothing makes the ABSENCE of a stamp a
failure**, so five sessions in a row wrote no stamp, declared it honestly in the stratum, and passed.
★ **The gate checks the drift and not the presence** — the exact inversion
[[gate-inside-the-growth-loop]] names.

**And a wrap-time gate is the wrong seam anyway.** A pre-flight stamp's entire value is spent at the
OPENER; by the wrap, a session that never priced itself has already overspent. A wrap check can only
punish, never throttle.

⇒ **RECOMMENDED, and it reuses machinery that already exists and is already proven:**
**apply `gauge_log_continuity`'s three-state shape to the pre-flight stamp.** That check already
fails a wrap unless session N−1 has a block **or an explicit `HOLE #<N> — <why>`**. Mirror it:

| state | claim | gate |
|---|---|---|
| a graded `pre-flight #N:` stamp | the session priced itself | passes |
| `⛔ NOT CAPTURED — UNMEASURED` **+ a reason** | it declined, and we know why | passes (the #73 legal refusal) |
| **nothing at all** | silent | **FAILS** |

**Why this and not a reminder:** it converts a silent miss into a declared one, which is this
project's own founding asymmetry — *a declared gap passes, a silent one fails* — and it is the
identical mechanism that made `_GAUGE-LOG.md` account for every session 6→33 with zero invented
facts. It needs no new vocabulary: `PREFLIGHT_UNMEASURED_RE` (`:112`) already recognises the honest
refusal. **The rule exists, the vocabulary exists, the enforcement does not.**
[[gate-dont-patch]] — a recurring cross-session condition gets a gate, not a fifth reminder.

⚠ **Its own limit, declared:** this still fires at the wrap. It cannot make a session price itself
at the opener; it can only make skipping it *cost something the next session can see*. The
opener-side half is ungateable for the same reason the chat title is — no gate runs there. That is
honest scope, not a hedge.

---

## §7 — WHAT WAS DONE, AND WHAT WAS DELIBERATELY NOT

**Done:** the false premise was **struck at source** in `_capture_gate.py`'s call-site comment, with
the corrected measurements, the dead-premise autopsy, and the successor named. The gate stays
unwired — for the one reason that survived, not the one that died.

**Deliberately NOT done, and priced:**
- **The gate was NOT re-wired.** Claim A survives in the half that matters: as built it is a
  word-presence check and the commissioned defect is a false claim. Re-wiring today also blocks
  every wrap on 11 live hits, ≥2 of them a regex bug. Dave's ruling stands; the instrument does not
  yet serve it.
- **The cross-instrument claim check was NOT built.** It survived a probe. That is not a tested
  instrument, and building an untested design at a wrap is how this thread started.
- **`_DS-IMPROVEMENTS.md`:1376–1377 was NOT edited.** It restates a superseded binding rule, but it
  sits inside a ledger entry recording a ruling, and [[home-by-addition-then-cut]] forbids the cut
  before the probe. **Forked.**

---

## §8 — THE DURABLE LESSON

Three sessions running have now spent their largest finding on the same class, and #84 adds the
sharpest instance of it: **#83 found a rule that stopped at a file extension; #84 found a RULING
that was read as stopping nowhere.**

★★ **A verbatim quote is not a verified scope.** The conductor quoted Dave exactly and still got the
answer wrong, because the quote was fetched from a banner and the primary record contained — eleven
lines below it — the clause that reversed the reading. The corpus already knew this
([[unmatched-grep-is-not-an-absence]]: *a MATCHED grep is not a PRESENCE — quote the line*). What
#84 adds is the harder form: **quoting the line is not enough either, when the line is a summary.
Read the record the summary was made from.**
