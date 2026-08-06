# #114 — the clerical re-file, the eight offenders that were six decorations, and a retrieval self-miss

```
provenance: 383e10dd-42d4-4e5e-8ef1-0dd5ddbeb367 · 2026-08-06
status: observed
```

*Ledger (the WHAT + the pins): `notes/_MEMENTO-DECISIONS.md` § ★ #114 · rulings `knowledge/_rulings.json`
`s114-D1`…`s114-D7` · spine `_LIVE-STATE.md` ⏱ LATEST DELTA #114. This file holds the WHY and HOW.
Written at #114's wrap by a delegated Opus wrap sub, from the conductor's session record.*

⚠ **Honest provenance caveat, stated once and not repeated:** the wrap sub did not witness the
session. Every quote below is Dave's, transferred verbatim from the conductor's record; every
measurement is a figure the conductor published. Where the sub could verify a claim against the repo
it did (commit hashes, file paths, the roll state, the gate output). Where it could not — the
conductor's own fill figure, chiefly — it is labelled ESTIMATE and not smoothed.

---

## The arc, in one line

A session opened to stage `deferred_tools` and close the attribution re-probe, and **never reached
it** — because the ds-016 dossier turned out to have a clerical remedy Dave could rule on the spot,
and everything downstream of that ruling was more valuable than the probe. The probe rolls to #115
**intact, for the second consecutive session.** That is worth saying plainly: two sessions in a row
have carried the same top-line item without touching it, and the reason both times was that
something cheaper and readier was in front of it.

## Finding 1 — the re-file was CLERICAL, and naming it that is what made it rulable

The ds-016 remedy (b) proposal could have been put to Dave as *"should these 5 anchors be
category-4?"* — a design question, which would have been a promotion, which is his alone and slow.
It was instead put as **recording tiers he had already set on 2026-07-03**. He answered *"I'm happy
for you to do that clerical re-filing"* and the work landed in the same window (`0678f7f`).

★ **The lesson is about the SHAPE of the question, not the answer.** A question that reads as
*"decide this"* costs a ruling; the same work framed as *"record what you already decided"* costs a
confirmation. **The framing was legitimate because it was true** — the tiers existed and were
dated. Had the tiers not existed, the same framing would have been a laundered premise, which Dave
ruled against at #112-D2 ([[feedback-dont-launder-a-premise-into-a-ruling]]). The discipline is:
**check that the prior decision actually exists, then say so.**

And the honest tail: **ds-016 is not closed.** 259 untagged anchors of 698 remain. The published
*"12 under-instrumented"* is a **FLOOR**, and this session did not move it. Recording that in the
same breath as the win is the point — a partial remedy that reads as a closure is how a floor
becomes a count.

## Finding 2 — eight offenders were two controls and six decorations

Dave ruled the hidden hit-area expander onto the 8 sub-24px-floor offenders: *"yes expand the hit
area..."*. Enacting it found that **only 2 were real controls** (`.fl-tip`, `.help-btn`, fixed in
`994cd25`); **6 were decorations sitting inside ≥44px parents.**

★ **So the ruling was correct and the gate's evidence was not.** This is the [[attribute-the-diff]]
family: the number 8 was never a count of a11y failures, it was a count of *things the checker's
selector could see*. The remedy is not to fix six non-problems; it is to fix the measurement — which
is exactly what Dave then signed off (D5, *"good lets do it"*), and why D5 was scoped to own **both**
the six phantoms **and** the `axs-003` detector quirk in one build. Splitting those would satisfy
[[conflated-fix-guarantees-recurrence]]'s failure condition precisely: one cause, two symptom sets,
fix one, guarantee the other returns.

And the sequencing ruling (D6) follows from the same reading: **44 promotes to blocking AFTER D5
lands.** Promote first and the gate fails day one on six things that are not defects — a gate that
fails on correct behaviour, which the ds-022 (a) docstring already names as the thing that teaches
sessions to fake discharges.

His nuance is inscribed where the next builder will meet it (`notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md`):
chart tooltip trigger-points are a **lesser** concern, the table fallback always exists, and a11y
rulings in that region are more nuanced than a single pixel floor.

## Finding 3 — the expensive one: BOTH "unknowns" were already in the record

Two questions were put to Dave as open unknowns this session: what the designer-pack v2 was for, and
what the hit-area solution should be. **Both were answered in the repo, and both documents were
indexed:**

- `notes/_receipts/2026-07-21-worker-designer-pack-v2.md`
- `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md`

Two causes, and they are different failures wearing the same coat:

1. **The conductor did not search before asking.** [[feedback-verify-before-asking]] is standing and
   simply was not run. No mechanism failed here; a step was skipped.
2. **Vocabulary drift.** Dave's phrasing and the record's phrasing do not collide lexically. So even
   a search that HAD been run, on his words, could plausibly have missed both — which means cause 1
   is the one that bit, but cause 2 would have been waiting behind it.

★ **The general form, and it is the sharper half:** *an unrun search is indistinguishable from an
absent document.* A question is not evidence of a gap in the record until a retrieval has actually
failed and the failure has been named [[unmatched-grep-is-not-an-absence]]. This is the same shape as
#80 re-deriving a ruling that sat in ten places — the record was fine; the reach for it was not.

⚠ **What this session did NOT do about it:** build anything. No gate, no vocabulary fix, no
retrieval change. Cause 2 (vocabulary drift in lexical search) is a real, measured, **unremediated**
mechanism and is left standing, declared. Pretending otherwise would be the [[assertion-propagation-gap]]
class — a claim nobody chases because it was never quite made.

## Finding 4 — frozen releases vs live mirrors, ruled in the same hour

Two rulings that look contradictory and are not:

- **D4:** *"anything that is a versioned release shouldn't change"* ⇒ the `designer-skills-v1`
  guideline edits **revert**. *"Yes I think the pack should revert."*
- **D7:** the memento-package **stays live** — *"lets keep it live and do the fix... versioning in
  the git only. lets call it and experiment."*

The distinction is **what the artefact CLAIMS to be**. A versioned release claims *"this is what
shipped at version N"* — editing it makes that claim false retroactively, which is confident false
inscription against a colleague's copy. A tracking mirror claims *"this follows main"* — freezing it
makes *that* claim false. ★ **The rule is not freeze-vs-live; it is that the artefact's own promise
decides.** [[designer-skills-packs-are-releases]] already carried half of this; D7 supplies the other
half, and the memento-package is now explicitly labelled an **experiment**, which is Dave's word.

## Finding 5 — a gate for a file that lives outside the repo

`92f8011` put ASSERT-007 in place: **`MEMORY.md` mount-reachability is now a checked predicate**
(roots repo + mount, `recheck_days 30`). #113 had found the file sitting in a hidden
`.auto-memory/` directory in the mount after ~113 sessions of nobody knowing where it was, three of
which had paid 8,470 / 9,178 / 7,996 real tokens to read it in order to measure it.

⚠ **The deliberate ugliness: off-sandbox runs go RED.** That is not a defect and was not softened —
a predicate about a mount is honestly FALSE where the mount is absent. The alternative (pass when
unmeasurable) is the exact pattern `unkeyed_testimony`'s docstring refuses: *an absent file is not a
clean file.* [[measuring-tool-must-not-guess]].

## Finding 6 — a second index defect, found and deliberately not fixed

The ds-016 dossier work surfaced this: the rules-index regex reads only
`[BLOCKING|ADVISORY|TASTE|REVIEW`, and **51 of the index's `BLOCKING` entries are
blocking-DERIVABLE candidates rather than enforced rules.** The index has no word for that state, so
it reports the nearest word it has — confidently.

Logged as **`ds-037`** in `knowledge/_DS-IMPROVEMENTS.md`, the stated home for DS errors, and
**deliberately not remedied in-window**: the candidate fix re-prices figures Dave has already been
shown. ★ *A vocabulary with no word for a state cannot report that state* — same family as
[[scope-blindness-gate-vocabulary]] and [[honest-refusal-needs-a-legal-form]], now seen in a third
place, which is the point at which it stops being an incident.

## What is still open, and why it was not closed

- **The attribution re-probe (#111-D3), `deferred_tools` first** — rolled from #113 **intact**, not
  reached. Second consecutive session.
- **D5 checker redesign** and **D2 citation gate** — both ruled, both unbuilt. D5 is #115's ①
  because D6 is gated on it.
- **D6's promotion** — ordered, and correctly not enacted.
- **P4 `_CHAIN.md` trim** — now **11,345**, not 10,499. The target grew.
- **The 19 `_state.LEGACY_IDS` + DO-FIRST item 22** — housework, unstarted.
- **Apollo enact queue** — still PARKED by Dave.

## The process note that should outlive the session

Four commits landed mid-wave (`92f8011`, `0678f7f`, `994cd25`, `48403b7`) and **all four carry
#113's banner subject**, because `_git_commit.sh` rewrites the subject from the chain banner and the
chain still held #113 at the time. This is a known convention, not damage — but it is precisely the
shape of [[wrap-skipped-chain-certifies-wrong-session]], where the record ends up certifying the
wrong session. It is flagged in the ledger and in the #114 banner for that reason. **Verify a
mid-wave commit by hash and diff, never by subject line.**
