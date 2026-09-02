# 2026-09-02 · #236 — the designer's brain: what happens when you grade the evidence instead of collecting the laws

provenance: 236 · 2026-09-02
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #236 · `GOOD-MORNING.md` ★ LATEST #236.
Research half: `notes/_briefs/2026-09-02-236-R1-principles-survey-brief.md` (`W-347`) → filed
`notes/_subreports/2026-09-02-236-R1-principles-survey.md` (`W-351`), and
`notes/_briefs/2026-09-02-236-R2-sdlc-playbook-brief.md` (`W-348`) → filed
`notes/_subreports/2026-09-02-236-R2-sdlc-playbook.md` (`W-352`).
Assembly half: `notes/_briefs/2026-09-02-236-P-plan-build-brief.md` (`W-350`) →
`_PLAN-designers-brain-2026-09-02-v1.html` (`W-349`) + filed
`notes/_subreports/2026-09-02-236-P-plan-build.md` (`W-353`).
Evidence beside each report at `notes/_subreports/assets/2026-09-02-236-*/`.
⛔ **Nothing in this session was ruled.** `knowledge/_rulings.json` was probed at **311** at the
wrap seat and carries no `s236-D*`. This file holds the WHY and HOW; the WHAT is in the spine and
the three filed reports, and is not repeated here.*

---

## 1. The session opened by not doing what it was named for

The chain title said `l2 — the behaviour address`. Dave opened with something else: the link #235
had missed — https://lawsofux.com/ — and then, in the same breath, refused the cheap version of the
job. His words, kept because the whole day is downstream of them: *"do some research first rather
than just use this site alone, lets find more principle, laws etc and validate them, i want the
brain to be powerful… we might also find contradictions… so it need rigour… a solid plan, with all
the usual dependencies, pitfalls and externalities mapped"*, then *"and ideas for other tasks, lets
not miss that"*, and then a third thread: *"lets think about claude's SDLC links… we might borrow
from it for memento and for the Apollo deployments and the final Apollo product as one of a few
options for the first phase of a design task."*

Three instructions, three different shapes: **collect and grade**, **find the contradictions**, and
**read the thing we parked**. L2 did not run. That is a carry, not a drop, and it is written as one.

The first mechanical act of the day was smaller and had been blocking for two sessions: the push.
`0f77b1a` (#234) and `be52c30` (#235) had both sat unpushed because `knowledge/_tmp/` was untracked
and undeclared, and the push gate refuses a dirty tree. Dave ruled it in chat — gitignore — and
`ce9aa40` carried `.gitignore` + the directory out of the way. The remote caught up. Worth recording
because the block was never the code: it was one directory nobody had a licence to decide about.

## 2. The finding that mattered was not a principle — it was the shape of the evidence

R1 was briefed to find at least 80 principles. It found 145, across 32 source families, 10 of them
absent from the candidate list it started with. If the lane had stopped there it would have handed
back a bigger version of the thing Dave already had.

What makes the report load-bearing is the **ladder**. Every one of the 145 rows carries an evidence
grade, and the distribution is the finding: **A 6 · B 28 · C 75 · D 9 · L 27**. Roughly eight rows
in ten are expert consensus wearing the word "law". Thirty-eight rows carry an explicit *alternative*
grade with the reason written out, rather than a single confident letter — which is the honest form
when two readings are defensible.

The second-order finding is sharper, and it is a warning about our own schema instinct: **grade L is
not a fifth rung.** DSA Article 25, the FCA Consumer Duty, EN 301 549 are legal obligations. A ladder
metaphor implies they can lose an argument to Jakob's Law. They cannot. The lane's recommendation is
that L becomes a distinct node *type*, and that recommendation is a question for Dave, not a decision
taken here.

The third is the one that will bite retrieval if nobody looks: **the contradictions are dense and
mostly unmediated in public.** Nielsen's own heuristics 6 and 8 pull against each other; the
evaluator-effect literature says two experts applying that list will not agree. The lane drew the
consequence out loud — the factory rubric (`s234-D2`) cannot be a heuristic score — and then stopped,
which is the right place to stop.

## 3. The correction the lane made on itself

R1's Finding 6 is a recall-vs-fetch failure the lane caught in its own brief and recorded rather than
quietly repairing. That is the discipline the report is built on: 43 live URL fetch attempts, 30
yielding usable text, and **the 13 failures listed in `fetch-receipts.json` rather than hidden**;
52 Crossref lookups, 52 resolved. Eighteen claims are declared UNPROVEN with a price against each.

Three of those eighteen are the ones that must not reach a client unproven, and they are carried:
ISO 9241-110's seven interaction-principle **names** are paywalled (title and date only were
fetched — they must not be entered from memory); DSA Article 25's text came from a **mirror**,
because EUR-Lex answered this agent with HTTP 202 and zero bytes; and the INP "good" threshold is
simply not in the fetched text, because the table is JS-rendered. One fetch each. None was faked.

## 4. Finding 1 is a vocabulary collision, and we have seen this movie

The probe was blunt and it is quotable: `grep -c -iE "fitts|hick's law|von restorff|doherty|tesler|
jakob's law|gestalt|peak-end|serial position|nielsen"` across the four structured KG files —
`_rulings.json`, `_consult-lexicon.json`, `_KNOWLEDGE-USAGE-ENTITIES.json`, `component-types.json` —
returned **zero, all four**. The graph genuinely does not know any of this.

The nuance is the dangerous part. "Gestalt" *does* appear in the prose corpus — as
`residual gestalt = human` in `knowledge/_FIXED-FLEX-CHARTER.md`, where it means **Dave's eye**, and
as the name of a **vendor design system** in `_memento-index.json`. Import Gestalt principles on top
of that and every retrieval for "gestalt" returns three unrelated senses. This is the `s202` class
exactly — the session where "switch" meant the thumb — and the cheapest moment to settle it is
before the import, not after.

## 5. The playbook we parked turned out to disagree with us about something we had already ruled

R2 read the AI-native SDLC playbook that had been carried as PARKED AND UNREAD since #233. Twelve
practices came back, sorted ADOPT/ADAPT/REJECT against three targets — Memento, the Apollo
deployments, the Apollo product's first phase — at **1/9/2 · 3/8/1 · 2/4/6**. Eight non-transfers
were named as non-transfers rather than forced through.

The headline is collision 1: **the playbook's artefact chain is a COPY chain.** Intent becomes spec
becomes plan, each artefact carrying the last one's content forward. `s234-D1` says the opposite for
this house — one home, derived consumers, never the same fact twice. So the borrow is *not* the
ladder; the borrow is the **deterministic tier**: hooks, bands, the advisory/deterministic pairing.
The lane's own recommendation on whether *any* of the ladder enters is (b) — the intent only, and
only if it **generates** the brief rather than sitting beside it — and it says out loud that the
generation would have to be real rather than a convention. That is question 1 of six, and it is
Dave's.

Reading it discharges the carry. The carry is **struck with its receipt**, not deleted, and the
strike is careful to close nothing else: the borrow decisions themselves are R2 Q1–Q6 and they ride
inside P0.

## 6. The plan, and the two things the build sub refused to smooth

Lane P assembled both reports into one Swiss HTML page — `_PLAN-designers-brain-2026-09-02-v1.html`,
84,593 bytes, seven phases, rendered and read back by eye in light and dark. Every figure on the page
was counted off the lanes' JSON assets rather than retyped, and that discipline paid twice: it
confirmed R1's grade line exactly, and a DOM probe on the rendered page caught the sub's **own**
drifted licence tally before it shipped.

Two findings were kept as findings rather than tidied away.

**(a)** `python3 -m playwright install chromium-headless-shell` **fails at this seat** —
`Download failure, code=1`. The renders happened only because a mount-side environment,
`outputs/_render-env-229/`, already existed. `_RUNBOOK-render-verify.md` still tells the next seat to
install. That correction is owed and was deliberately not made at the wrap, because a runbook
correction is a change to canon and this was a mechanical wrap.

**(b)** R1's licence tiers cover **16 safe-now / 3 pointer-only / 13 untiered** of 32 families, with
the EAA untiered. A membership rule written before the tiering would import text whose licence nobody
has read.

## 7. What is open, and why nothing here is a decision

Twelve ruling-shaped questions came back — six from R1, six from R2 — and they are collected in the
plan's §8 with options, receipts and each lane's recommendation. One of them (R1 Q4, tensions as
edges or nodes) deliberately carries **no** recommendation, because schema was fenced from that lane.
Not one was answered, ranked or pre-empted at any seat this session, and the plan says so on its own
face.

The resolved state: the research exists, the plan exists, and the decision surface exists. What does
not exist is a single ruling. **P0 for #237 is Dave answering those twelve**, and L2 — the behaviour
address, with L1's three questions still attached — is the beat behind it.

## 8. One thing the wrap itself learned

The carry count moved 160 → 171 while eight items were added. The arithmetic only works once you
know that `_capture_gate._carry_items()` counts `·`-separated segments carrying a **digit** bracket,
so a `[NEW — 0]` item is invisible until it ages. It has been declared at every wrap since #230 and
it was declared again here.

The new thing is smaller and worth writing down: while drafting this wrap's own pitfalls item, the
sentence explaining that mechanism contained a literal `` `[1]` `` — and the counter, which does not
mask backticks, counted the *explanation* as a carry. The count read 172 until the phrasing changed.
A measuring instrument that reads the prose describing it is a real hazard, and the fix was one
sentence, not a code change.
