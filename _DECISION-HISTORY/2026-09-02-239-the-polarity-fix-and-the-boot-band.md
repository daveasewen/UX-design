# 2026-09-02 · #239 — the polarity fix and the boot band: a CI read-back that cost 55K, forty-four escapes closed by CLASS not by row, six green controls that turn out to have been false, and Dave's own "shrink first"

provenance: 239 · 2026-09-02
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #239 · `GOOD-MORNING.md` ★ LATEST #239.
⛔ **NO RULING WAS INSCRIBED THIS SESSION.** `s238-D1` … `s238-D7` are the standing frame and not one
word of them is re-worded here.
Lanes (brief → filed report, evidence beside the first at `notes/_subreports/assets/2026-09-02-239-F-polarity-fix/`):
F `notes/_briefs/2026-09-02-239-F-polarity-fix-brief.md` (`W-379`) → `notes/_subreports/2026-09-02-239-F-polarity-fix.md` (`W-381`) ·
R `notes/_briefs/2026-09-02-239-R-assert-009-rebase-brief.md` (`W-380`) → `notes/_subreports/2026-09-02-239-R-assert-009-rebase.md` (`W-382`).
Common rules: `notes/_briefs/2026-09-02-239-COMMON-lane-rules.md` (`W-378`). This wrap's brief:
`notes/_briefs/2026-09-02-239-delegated-wrap-brief.md` (`W-383`). The boot-band brief Dave's paste
became: `notes/_briefs/2026-09-02-240-boot-band-derive-brief.md` (`W-384`).
Written by the delegated wrap sub from the wrap brief and the two filed reports. The WHY is the
conductor's arc as the brief records it; the HOW is what the reports say they did, quoted off the
files. Where this seat could not see a thing first-hand it says so rather than smoothing it.*

---

## 1 · The opener was a read-back, and the read-back was the session's first expensive lesson

`s203-D1` owes a CI verdict on every push. #238 pushed, so #239 opened by going to look. What came
back was not one verdict but a wall of them: run **#478 FAILURE**, and every run from **#227 through
#238** reading "failed" off the Actions list — **twelve consecutive**. The first blocker since
`e7cf3db` (the last green, after #231) is **`ASSERT-009`: metas 136 ≠ 137**, the 137th being
`knowledge/components/template-dashboard-bento.meta.json`. The `Survey the COMMITTED tree` step also
failed and its body is **UNPROVEN** — `_build_survey.py` exceeds the sandbox call wall, so no seat in
this session could read what that step actually said.

**The cost, and why it is written here rather than excused.** Getting that read-back moved the
conductor's FILL from **84,635 @ 4 turns** to **140,327 @ 34 turns** — roughly **55K real** for one
verdict and one blocker name. That is a third of a window spent on a browser route: the Actions list,
then a run page, then a step, then another step. The finding, homed here so a future opener can price
it: **cap the CI read-back at the run page plus one JS grep for the first failing step.** The list
view is where the money goes, and the list view answers a question nobody asked — the blocker is on
the newest run and the older runs are a count, not a read.

⚠ Its own honest residual: *twelve consecutive failures* is a claim read off a list, not off twelve
run pages. It is written that way in the record and is not upgraded here.

## 2 · "Okay rebase, do both" — two lanes, and the smaller one is the one that unblocks CI

Dave's answer to the blocker was four words. **"Do both"** meant the `ASSERT-009` re-base AND the
polarity fix lane that #238 had already named as #239's first beat, in the same session. So the
session ran two: a Sonnet chore (**R**) on the assertion, and a Fable lane (**F**) on the gate.

The interesting part of the pairing is the asymmetry. **R is nine lines of JSON and it is the one
that moves CI.** F is a 900-line rewrite that CI has never yet reached, because the build dies at
step 10 of 142 on R's assertion. Both were worth running; only one of them changes what the next
green verdict looks like.

## 3 · Chore R — a re-base BY ADDITION, and the three homes that turned out to be history

R re-measured before it edited — `ls knowledge/components/*.meta.json | wc -l` → **137**, and
`ls knowledge/components | wc -l` → **141** — and the figures matched the brief's FACT line exactly,
so no STOP fired. It then read `_validate_assertions.py:152-157` to find **which field the gate
actually reads** (`predicate["n"]`, with `op` defaulting to `eq`) rather than guessing from the shape
of the JSON. The edit: predicate `:191`, claim `:185`, provenance **appended** at `:202` in the
form the file has used six times, and `knowledge/README.md:13`. Gate after:
`✅ assertion gate passed — 8 claim(s) still true.`

**The finding that was not in the brief.** `ASSERT-009`'s `asserted_in` names three other homes.
R grepped all three and classified every hit: **every one was HISTORY** — dated strata, frozen by
ADR-0017 — and **zero LIVE hits existed to repoint**. So nothing was touched in `_LIVE-STATE.md`,
`notes/_MEMENTO-DECISIONS.md` or the `_DECISION-HISTORY` file. That is a negative result with a
probe behind it, which is the only kind worth recording: `notes/_MEMENTO-DECISIONS.md` has been
frozen at **92** since #207/208 — six re-bases behind — and the question of whether it should stay in
`asserted_in` at all is now a live, priced question rather than a suspicion.

And R surfaced a rule tension it was right not to resolve: **the #238 COMMON forbids any write to
`_LIVE-STATE.md`, while a re-base brief's step 4 assumes repointing live hits there is normal.**
This pass found no live hit, so the two rules never collided — but the next re-base may not be so
lucky. R named it and stopped. That is the correct move and it is why the item reaches #240 as a
carry rather than as a defect.

## 4 · Lane F — the fix is EIGHT CLASSES, not forty-eight rows

The `s238-D7` proof standard set at #238 was V's `escaped-repro.txt`, not the builder's arm table:
**the builder's self-test proves the builder's clauses.** F's brief took V's own recommended answers
to its Q1–Q8 as **declared defaults** (`s238-D3` / `s238-D5`) so the lane could build without
stopping to ask, and every default it bent toward is written out in the report's DEFAULTS TAKEN
table with its FLOATED figures beside it.

The result, copied off the file: **48 → 4 ESCAPED** · **RULED 16 → 0** · **PROMISED 26 → 0** ·
**CRASH 10 → 0** · **MISNAMED 3 → 0**. Selftest **125 arms, red 113/113** (**+72 new**), commit-script
selftest **14/14**, live `--check` **GREEN**, determinism **OK** against V's own three body hashes,
and the three doors — CLI, the build's subprocess form, the `_git_commit.sh` seam — still agree
**96/96**.

**Why eight classes and not forty-eight patches.** Every one of the eight is a rule about a kind of
claim, not about a row:

- **Q1 — what "live" means** now reads the store's own prose: another ruling saying it supersedes
  this one, or the ruling's own `status` saying superseded; plus whole-word OPEN / PARKED / DEFERRED
  / FORKED as `NOT-LIVE`. Scoped to `resolvedBy` only, which is where V said the damage was.
- **Q2 — the pin.** The schema is fixed by sha AND by **47 floors in code**, so a loosened schema is
  refused *at the seam* and the data-level refusal still prints. V's cleverest escape was to loosen
  the schema and let the next build accept the mutant; that door is now shut in the same run.
- **Q3 — the quote oracle** reads only the frozen R1 register, a `resolvedBy` needs a verified
  quote, and the migration receipt is a **bijection**: one frozen row, one node.
- **Q4** a clock is a clock. **Q5** every descriptive string is verbatim from its source row or
  bounded, and an invisible character is refused. **Q6** the home directory is closed at every
  level. **Q7** a crash is a NAMED refusal. **Q8** an absent home in the source repo is rc 1, and
  the seam's redirect is declared while the tree's own home is gated anyway.

Two of those carry a lesson wider than this gate. **Q7's** catch-all means the crash class is closed
*by construction*: arm 110 forces a `TypeError` inside the gate and gets `REFUSED (S-SHAPE)` with the
exception class and site named, no traceback — so "the refusal is NAMED above" is now true for any
exception, not for the ten V happened to find. And **Q8** killed a stale premise: V had assumed
"`knowledge/` absent ⇒ this is the shipped pack", but the pack ships **1,160 files under
`knowledge/`**. The real discriminator is `knowledge/_rulings.json`, which the pack excludes. A
premise aged out between the verifier and the fix, and the fix probed it rather than inheriting it.

## 5 · The honest consequence: six of seven green controls turn out to have been false

This is the part of the lane that could easily have been smoothed and was not.

Q3 as V recommended it **flips six of V's own seven green controls red.** Their sources were
fictional paths (`/etc/hostname`, `x`, `selftest`) or phrases that cannot be verified against the
frozen register — and V's own basis text had called five of them "observation" or "green by the
letter". So they were never green in the sense that matters; they were green because nothing was
checking. F drove the **legal analogue** of each one and filed it green in
`green-controls-recut.txt`.

**Except two, and the exception is the whole finding.** Under Q3 as built, every one of the 30 frozen
rows is claimed by exactly one node. That means **a brand-new polarity has no legal row to cite, and
a retired one leaves an unclaimed row** — so there is currently **NO LEGAL FORM for adding or
retiring a polarity.** F stopped and priced two options (a second register on the allow-list; a
`retired` list under `$migration` with a ruling id per row) and built neither. ⛔ **This is Dave's,
and it gates V2**: a fresh verifier run against the fixed gate without this ruling will re-report the
six false-reds as regressions, which is exactly the reading pitfall 6 of F's own report warns about.

## 6 · The four that still escape are UNRULED — they are not bugs

Rows **241** and **301** rewrite a principle statement or a grade letter in `principles.json` and
pass every door, because the register carries no receipt against its R1 seed — the gate pins the
*schema*, not the *register*. Row **243** has one ruling both resolving and challenging the same
polarity, and nothing ruled says that is a contradiction. Row **245** deletes all 21 typed links,
and nothing derivable from the frozen rows says how many there must be.

F's fix for 241/301 would have edited `principles.json`, outside the lane's declared files, so it
**STOPPED at the file boundary and priced the work** instead of reaching across it. That restraint is
the reason `W-374` stays open at ESCAPED 4 rather than being closed on a lane's own say-so: **four
unruled escapes are a sitting for Dave, not a defect list.**

## 7 · Dave's mid-turn paste — the boot band, and "we need to get this fixed soon"

Mid-session, with the conductor already past the advisory, Dave pasted an instruction about the boot
band: **derive the band, shrink-only ceiling, shrink first**, and *"we need to get this fixed soon"*.

There was no budget left to act on it — FILL read **168,576** when it arrived — so it was **FILED
VERBATIM-IN-SUBSTANCE** as `notes/_briefs/2026-09-02-240-boot-band-derive-brief.md` and carried. It is
**RULING-SHAPED, it is Dave's, and it is the #240 opener's FIRST question.** Part 3 of it is already
`s228-D6`.

**Why filing it was the right move and not a deferral.** The boot figure has read **75–77K** for the
last six sessions against an `s208-D1` band of **55,595–57,903** — this session's own boot was
**75,619 real**, read first-hand at two seats. A band that has been wrong six times running is not a
band; but re-basing it *inside a window that is already past its advisory* is precisely the move
`s208-D1`'s own rider forbids without a boot-REDUCTION option priced beside it. ⛔ Nothing was
re-based at any seat this session, and this wrap did not evaluate the proposal either.

The same paste has a sibling that lands on the same desk: **`MEMORY.md` is 19.8 KB against a 24.4 KB
read limit.** Dave's own words are "shrink first". A compaction pass is owed at the #240 opener.

## 8 · The gauge — a session that went past the advisory on purpose, and said so

Moments, stated separately and never converted: boot **75,619 real** · opener FILL **84,635 @ 4
turns** · post-CI-read-back **140,327 @ 34 turns** · post-lanes **168,576 @ 42 turns — past the
150,929 advisory by 17,647, DECLARED IN CHAT, judgment CLOSED there and mechanical-only after**. The
recall probe was planted at **17:07:48Z** and quizzed **BLIND 4/4 GREEN** at that reading. Subs cost
**531,802 tokens (n=2)** — quota, never window fill.

The `s214-D5` hand-over term, read first-hand at this wrap seat: **sub-cut 198,428 real @ 58 turns**
against the brief's declared **168,576** — a **29,852** hand-over. That is the largest delta the field
has carried, and its cause is visible rather than mysterious: the conductor committed the lane work,
wrote memory, and cut two briefs between the last declared moment and the hand-over.

★ **The lesson that held for a third time:** a lane costs roughly **19K of conductor FILL all-in**
(`n=5`, #238's measure). Two lanes at #239 plus a 55K read-back is the whole of a 168K window, and
that arithmetic is what left no room for the boot band.

## 9 · What is still open at the end of it

Dave's, and none of it touched: **the four UNRULED escapes** (241/301 want a register receipt · 243
is a contradiction only if he reads it as one · 245 wants a links receipt) · **a legal form for a NEW
or RETIRED polarity**, which gates V2 · **F's ruling-shaped 5–9** (the `R1-NOT-LIVE` name · `.DS_Store`
by bytes as built · the FLOATED figures block · a quote on `explainedBy`/`challengedBy` · the prose
readings' false positives) · **R's two** (the `asserted_in` trim; the COMMON-vs-brief tension) · and
**the boot band**, which is the first question of the next window.

Mine, and priced: **V2 against the fixed gate**, gated by the legal-form ruling · the **`s203-D1` CI
read-back for this wrap's push**, where the next blocker past step 10/142 is genuinely unknown and
the `Survey` step's failing check is still UNPROVEN · **`MEMORY.md` compaction** · and
`_validate_wiring.py`'s pre-existing red on #235's orphan `_validate_receipt.py`, which F saw,
quoted, and correctly did not fix.
