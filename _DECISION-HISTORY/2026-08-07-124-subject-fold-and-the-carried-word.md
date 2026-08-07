# #124 — the carried five: a folded subject, a word that superseded itself, and a fence that had already lifted

```
provenance: 124 · 2026-08-07
status: ruled — knowledge/_rulings.json entry 62 (`s124-D1`)
```

Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA (#124) · Banner: `GOOD-MORNING.md` ★ LATEST #124 ·
Ledger: `knowledge/_rulings.json` (`s124-D1`) · Register: `knowledge/_REVIEW-SIGNOFF.md` (digest row +
item-4 tombstone) · Predecessor arc:
`_DECISION-HISTORY/2026-08-07-123-rag-world-signoff-and-tint-opacities.md` (#123).

---

## Why this session existed

It opened as a carried-items session — the residual list #123 handed forward was five deep and one of
its entries had been rolling for ten sessions. What the session actually became was three things it
could not have planned: a defect discovered in its own first bash call, a Dave ruling that its own work
then made obsolete inside the hour, and a fence that turned out to have lifted a session earlier without
anyone checking.

---

## Finding 1 — the 83,000-character commit subject, and why it was a *scheduled* defect

**What happened, mechanically.** The session's first bash probes broke. The cause was commit `0eacf2d`:
its subject is roughly **83,000 characters**. The msgfile that produced it carried a JSONL body with **no
blank line after the headline**, and git's `%s` takes everything up to the first blank line as the
subject. So the entire body became the subject, and any tool that reads `git log` inherited it.

**Why this is not simply a bug.** The fold was **already documented** — in `_test_git_commit.py`'s own
comment, describing it as *"not a script defect"*, a note dating back to #78's declared residuals. It was
true as a statement about `_git_commit.sh`'s responsibility and useless as a defence: nothing enforced the
blank line, so the hazard sat in the record as a description rather than a guard. The generalisation the
session took from it:

> **A documented-but-ungated hazard is a scheduled defect.** Writing down that something *can* go wrong
> is not a control; it is a prediction with no expiry date.

**What Dave ruled.** Gate it and harden it, and **keep the history** — no rewrite, no force-push. That
ordering matters: the cheap-feeling repair (rewrite the subject out of history) would have rewritten a
pushed commit to make a record look tidier than it was. The ruling chose an honest log with a gate in
front of it over a clean log with nothing behind it.

**What was built.** `_git_commit.sh` T3 inserts the blank separator; a post-commit **200-character subject
cap fails loud**; `_test_git_commit.py` grew `subject_fold_blank_line_inserted_124` and
`MUTATION_blank_insert_removed_bites_124` — the second exists because the first, alone, is an assertion:
it would stay green if the insert were deleted, unless something proves it bites. 22 arms green.

**The honest residual.** *How* JSONL got into that msgfile is **unattributed**. The gate does not care —
it bites regardless of cause — but the cause is unknown and is recorded as unknown rather than guessed at.
It is homed in `_LIVE-STATE.md` § OPEN so it cannot quietly evaporate.

---

## Finding 2 — a ruling that was superseded by its own enactment, in the same session

The memento-package delta-audit had been red since #120 and blocked on Dave's #64/#114 open questions.
Asked for the word, he ruled **WAIT**: the red stands until the #115 graph-mark tally is judged, and only
then does the package sync.

Then the session judged the tally. The 79 raw marks were distilled into
`reviews/outputs/graph-mark-tally-digest-v1.html` — 10 live-surface cards plus 27 records of archive bulk —
and Dave went through it: *"i've gone with all your recommendations"*, which resolved to **SAVE ×3, DROP
×7**. The close condition his own ruling had named was now met, **inside the same window**. So the sync ran.

**The interesting part is what the sync alone produced.** It left a **dead import**: the delta-audit
reported green and the artefact was broken. This is the #122 class again — `no gate parses the artefact` —
transposed from CSS to Python. The audit compares *files against manifests*; nothing was asking whether the
package could still be imported. An **import-closure probe** caught it, and `_graph_edges.py` was added to
`VERBATIM_SET` and to both copies and both manifests. Final state: **delta-audit 0 failures, validator
selftest green, package import proven.**

> **A synchroniser that verifies its own bookkeeping has verified its bookkeeping.** The first check on a
> generated artefact must be made in the grammar of the thing that consumes it — for CSS, a parser; for a
> package, an import.

**The SAVE ×3** were enacted as citation repairs in `_LIVE-STATE.md`, each tagged *"s124 tally SAVE"*:
R-D1 re-anchored to R-D7/R-D15 · R-D4's hexes `#2B7E4F`/`#306EC6` marked **superseded as fill values** per
R-D12.B · the `ls:OPEN` Sonnet-build instruction re-pointed at "R-D10 dark set **as amended by R-D11**".
⚠ The first attempt at the R-D4 fix called the old hexes *"DARK-leg values"*, which was wrong; it was
caught against LS:185 before the commit. Worth recording because the wrong version was fluent and specific,
which is exactly the shape of a confident false inscription.

---

## Finding 3 — `s124-D1`: the demote is retired, and the programme closes properly

With the tally judged, the last open item of the #115 graph programme — candidates-brief item 4,
**DEMOTE** — could be ruled on evidence rather than taste. The evidence: **76 of 79 marks were noise.**
The mark records that a result *mentions* a superseded node; it cannot tell mention-as-history from
mention-as-authority. A demote built on it would mostly bury healthy records, and worse, it would
institutionalise this project's single most-recurrent failure class — **retrieval quietly hiding a ruling**
(#32, #81).

Dave ratified the recommendation. `s124-D1`: the graph-mark stays **MARK-ONLY, permanently** — the #115
ABSOLUTE CONSTRAINT is no longer provisional. Nothing was built, because the ruling forbids a build.

**The arc is the finding.** *Instrumented → tallied → judged → ruled.* The observation window was opened
precisely so this decision would have provenance instead of recollection, and it delivered exactly that.
⚠ Probe pollution was declared on the digest's own card face — roughly half the raw marks were this
session's own queries — because a tally that quietly counts its own measuring is not evidence.

---

## Finding 4 — the fence that had already lifted

Carried into this session as fact: *"chromium is TLS-blocked in-sandbox."* It was inherited from #123's
declared render gap and repeated without being tested. Dave caught it in one line:

> *"and there is a runbook for chromium and playwright"*

`knowledge/_RUNBOOK-render-verify.md` was then followed end to end and **it works** — headless-shell
download, no-root libs, render *and drive* at 1180/480, PNGs seen. The digest was rendered and driven,
not merely asserted.

This is the read-the-runbook lesson recurring, and its precise shape here is worth naming: the conductor
did not disbelieve the runbook, it **never reached** the runbook, because a carried note had already
answered the question. **A fence inherited as a fact is a premise, and premises age faster than rules.**
The felt difficulty was zero, which is the tell — the cheapest-feeling claims are the ones no one re-tests.

---

## What we got wrong

1. **The stale TLS fence** above — claimed from a carried note, not from the runbook. Caught by Dave.
2. **One commit amend ran outside `_git_commit.sh`** (an append to `_REVIEW-SIGNOFF.md`). It left a
   `HEAD.lock`, cleared by `mv` per the standing rule. A shortcut taken in the session whose entire
   subject matter was the commit seam — named here rather than smoothed over.
3. **The first R-D4 fix mislabelled the superseded hexes**, self-caught against LS:185 before commit.

---

## The gauge, and the reason this wrap was delegated

No opener measurement was taken. The **check-in at the seam measured FILL 174,347 real against the
150,929 stop line — crossed by 23,418**, and the cause is attributable: **two full-page PNG reads**. An
image is priced by the reader, not by the file, and a render already asserted numerically did not need
reading back at full page height. The wrap was delegated to one Opus sub for exactly that reason —
roll, don't ride. Both this lesson and #123's *(exclude `_memento-index.json` from repo-wide greps)* were
inscribed into `_RUNBOOK-context-gauge.md` at this wrap by the EXIT CHECK, because both had been living
only in dated post-mortem strata, which do not count.

Dave's quota panel was **given**: session 0% · weekly all-models 9% · weekly Fable 13%, resets Thursday.

---

## Resolved state, and what is still open

**Closed:** the subject-fold hazard (gated, history kept) · the memento-package delta-audit re-baseline ·
the #115 graph programme in full (`s124-D1`).

**Still open:** the **fall-through class** has no gate — remedy unruled and unpriced (from #123) · the
**msgfile-JSONL attribution** is unproven and declared not chased · and the carried set rolls on:
`s116-D4`/`s116-D5` · `s114-D2` · the stale-mount seam · the P4 chain trim · `89-D2` enactment · `ds-032` ·
`ds-025` · the boot-rent plan · the attribution re-probe (eleventh roll).

**#125's opening lane is Dave's own pick** — *"we can do the schematic next"*: one live HTML diagram of the
whole Memento mechanism (chain · store · search · marks · gates · package), **driven from the real file
inventory so it cannot drift**, closing on his sign-off eye.
