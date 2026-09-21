# 2026-09-21 · #293 — the dream backlog was cut down and the review page is owed

provenance: 293 · 2026-09-21
status: observed

*The narrative dossier: the WHY and HOW, not the WHAT. The terse records hold the what — the ★ LATEST
banner, the ⏱ LATEST DELTA, `_CARRIES.md` § `residual → #294`, `notes/_subreports/2026-09-21-293-W-wrap.md`.
Both-way links at the foot. **Nothing here is a ruling**: `knowledge/_rulings.json` stands at 622 and
he did not say* "inscribe".

---

## The question he opened with, and why it was a good one

> Good Morning! we should probably look at the latest dream pass, in fact some previous ones may not have been enacted

The dream pass is a weekly consolidation lane that **floats proposals**; a proposal becomes a change
only when Dave rules it and someone enacts it. Three separate mechanisms in this repo are supposed to
stop a floated proposal from evaporating — the wrap's 2c EXIT CHECK, the carry set, and the pass's own
dated note — and **none of them tracks enactment**. They track *presence*. So his suspicion was
structurally well-founded: nothing in the system could have told him the answer, and nothing had ever
been asked to.

The honest shape of the first move was therefore an **audit, not a fix**. Lane DA was cut READ-ONLY on
git, with an explicit instruction not to run `_checkin.py` — because that arm appends to
`notes/_REHEARSAL-LOG.jsonl` and `notes/_dream/_GRADE-DECISIONS.jsonl`, both counted datasets, and
**an audit sub must not move the population it is auditing**. That constraint cost the lane its own
token measurement and it was declared rather than quietly dropped.

## The correction that made the audit trustworthy

The brief handed DA a premise: `2026-08-08` = dream pass 6. DA did not take it. Each proposals file
**states its own number in its first line**, and the primary sources disagreed with the brief:
`2026-08-09-proposals.md` opens *"# Dream pass 6 — floated proposals"* while `2026-08-08-proposals.md`
calls itself the *"Fifth pass"* in its own standfirst, corroborated by the #137 triage dossier.

This matters more than a numbering nicety. **An audit that inherits a wrong index produces a
confident, wrong census** — it would have reported on nine files as if they were eight, and every
"never ruled" verdict would have been about the wrong pass. The published mapping (08-08 = 5 · 08-09 =
6 · 08-15 = 7 · 08-16 = 8 · 08-23 = 9 · 08-30 = 10 · 09-06 = 11 · 09-13 = 12 · 09-20 = 13) is the
audit's real first finding, and it is the reason the rest of it can be believed.

## What the census actually found — and the shape of the answer surprised the question

**39 proposals over passes 6–13: 22 ruled and enacted with a commit behind them · 1 ruled and NOT
enacted · 13 never ruled and still live · 3 honestly overtaken.**

The interesting part is the **distribution**, not the totals. Passes 6, 7, 8, 11 and 12 were disposed
of in full, usually within 24–48 hours of firing — pass 12 is the best-served in the set: four
proposals, four separate verbatim words from Dave at #271, all four enacted the next day. So the
system *does* work when Dave is in the room when a pass fires.

The failures cluster where he was **not**:

- **Pass 9 has no disposition ruling at all.** Six proposals, and nothing in any of the four ruling
  surfaces answers the pass as a pass. Three are dead by other events; three are still live at 29
  days. This had never been written down anywhere before this session.
- **Pass 13 fired on schedule on 2026-09-20 with Dave absent** — *"7 proposals floated, 0 ruled"* —
  and three consecutive wrap briefs recorded it as unruled without anything moving.
- **Pass 6 P1 is the only RULED-and-NOT-enacted item in the whole audit**, and it had been sitting for
  **36 days** since he firmed it on a full read-back (*"Firm — ratify all"*, `s186-D2`).

⇒ **The dream pass does not have an enactment problem. It has an attendance problem**, and the
backlog is what accumulates in the weeks Dave is not there to say a word.

## Why the plan was three moves and not one

His answer to the audit named two different jobs in one sentence:

> okay lets get these cut these down, I don't like all these loose ends, lets get the no-brainers done first. Give me a plan to get this of our desk. then wen they are cut down lets get a new review page with anything that needs mu judgement on it excluding anything settled

The sentence carries an **ordering constraint**: the no-brainers first, *then* the review page, and
the page must exclude anything settled. Running them together would have produced exactly the surface
he was complaining about — a page mixing things that need him with things that do not.

So the plan split into three, and the split was on **who can act**, not on convenience:

1. **Move 1 — the eight no-brainers, one lane.** Items where the smallest correct step is obvious and
   reversible, and where a lane can prove it with a selftest.
2. **Move 2 — the memory archive shard, conductor in seat.** ⚠ **Not a choice.** Only the conductor's
   seat can reach the claude.ai Project memory store (the #278 addition to the ritual's step 3), so
   this one could not be delegated at all. It is a **seat limit**, and calling it a departure from
   `s204-D1` would be wrong.
3. **Move 3 — the review page.** Judgement-only, each item with a recommendation and a one-word rule,
   **replacing DA's audit as the ruling surface**: the audit is evidence; the page is where he rules.

He answered `go`.

## Move 1, and the two items that turned out to be different jobs

Lane E1 landed **8 of 8, 0 blocked**, one commit, **no constant moved**. Two of the eight were not the
jobs the brief described, and both were published as findings rather than smoothed over.

**The first is the session's sharpest result, and it is an absence.** The brief told E1 to find the
generator that writes the `⛔ NOT CAPTURED` pre-flight line into `notes/_GAUGE-LOG.md`. **There is
none, and there never was.** Every one of those lines was hand-typed into a
`knowledge/_tmp/wrap<n>/stratum*.py` by that session's wrap sub, each copying the previous session's
text with the ordinal bumped — the literal phrase, file after file, is *"Reason unchanged from
#199…#<n-1>"*. That ran from **#199 to #291: 93 consecutive sessions, 185 occurrences.**

Two things make it worse than a stale line, and both are general:

- **The stated reason was answering a question nobody asked.** *"A sub cannot read its own
  `message.usage`"* is true and irrelevant — the pre-flight line wants the **conductor's** window, and
  the conductor's top-level transcript has always been readable from a sub seat, at the same glob
  `find_transcript()` has always used. Several of those same strata say `_checkin.py` **was** run on
  the conductor's transcript *in the paragraph that refuses*.
- **Nothing re-derived the claim, so nothing could notice when it stopped being true.** A generated
  line goes stale loudly; a copied line goes stale silently. ⇒ The enactment is therefore the
  generator itself, `preflight_line()`, which returns a string and **appends to no log** — so taking
  the reading moves no counted dataset. This wrap's block carries the first `✅ CAPTURED` pre-flight
  in 94 sessions.

**The second** is smaller and the same class: #278 promised that the runbook's *"auto-memory"* wording
at step 3 would become *"Project instructions + cloud memory"*. `grep -i "auto.memory"` over the
runbook returns **nothing** — the step never used the word. **A promise with no matching literal is
the shape that silently goes unpaid**, so the change was made BY ADDITION against the step's actual
text and the mismatch was recorded rather than the promise quietly marked done.

Two more decisions inside Move 1 deserve keeping because they are restraint, not output:

- **`s276-D6`'s condition was met VACUOUSLY and the receipt says so.** Nothing has ever run
  `_validate_lane_ownership.py` — 0 hits across the build, CI, the commit script and 2,994 lines of
  the rehearsal log — so *"it comes OFF at the next dream pass if the tripwire never fired"* is
  satisfied **by construction**. The guard was **moved**, never `rm`'d, and the receipt was inscribed
  where a future reader will actually hit it: a comment in `_validate_wiring.py`'s `EXEMPT` dict,
  because `_to_delete/` is gitignored.
- **`P-276-1` was left `parked` and NOT closed, on purpose.** Its `what` asks Dave to rule the
  deletion on a corrected premise. **Flipping it to `enacted` from a lane would answer his question on
  his behalf**, which is the one thing a lane may never do.

## Move 2, and why the ceiling turned out to be a decision and not a wall

#292 had proved, with seven server-side refusals each quoting a projected byte count, that the memory
index cap is real and enforced. It closed with `index.md` at **49,152 of 49,152 bytes — zero
headroom** — and `MEMORY-ARCHIVE.md` at 48,990 of the same cap. Six wraps before it had described that
state as *arithmetic*; #292 turned it into a measured refusal.

What #292 could not do was decide what to do about it, because **truncating a verbatim move is not a
move** — and every line that should have rolled ran to thousands of bytes. Dave had already picked the
shape at #289 (shard by strand and age), and it had never been started.

Move 2 started it: **a second archive shard**, `MEMORY-ARCHIVE-2.md` at 35,063 B, taking the #283→#289
wrap lines and the #286–#291 suspension notes verbatim; `index.md` cut back to the newest three and
now **15,605 B of 49,152**; the frontmatter `description` — which #292 recorded as wrong and
uncorrectable at zero headroom — corrected. And the part that makes it durable rather than a one-off
tidy: **a standing rule written into the index itself — open the next shard, never truncate, never
suspend.**

⇒ That is why #292's owed item 12 could be **struck at this wrap** and item 13 could not. The strike
form (`s188-D2`) asks a retraction to name **the session that proved the claim false and where the
correction is inscribed**. Both exist for item 12, and the inscription is in the store because the
**seat limit is structural** — requiring a commit sha would make anything memory-side permanently
unstrikable. Item 13 fails a different test: six of dream pass 13's seven were *enacted* and the
seventh was *carried*, but **not one was ruled**, and its headline says *unruled*. `s183-D1` strikes a
headline, never a clause.

## Why Move 3 did not happen, and why that is the correct outcome

The seam check read **222,464 real / 24 turns — outside the 220,000 tolerance** — and the conductor
quoted it with a recommendation to wrap rather than take a third override. Dave's reply, verbatim and
entire: **`wrap`**.

This is worth recording precisely because of what the last two sessions did. #291 and #292 each
overrode the instrument once with one more note and then obeyed; two identical shapes, and both wraps
said out loud that **n=2 is an observation and no rule is invented from it**. #293 had the same
opportunity — the review page was one lane away — and **the instrument was obeyed.**

⇒ **`s283-D1`'s override shape stays at n=2.** The evidence for a blocking tolerance arm did not grow
today, and the evidence against it did not either. What #293 adds is a third session in the
obeyed column (#283, #290, #293), and the standing question — advisory or blocking — is still his.

The cost is honest and is carried, not minimised: **the review page he asked for in the same breath as
the no-brainers is not built**, and it is #294's first job, with its five judgement items named at the
wrap so the next seat does not have to re-derive them.

## What went wrong at this seat, and what it cost

- **A stale `.git/index.lock`** (0 bytes, 14:56) was stranded by lane E1's commit. It was **`mv`'d
  aside, never `rm`'d** — the standing rule — and cost nothing.
- **One commit refusal**, and it was the *right* one: `s130-D3` refused a non-wrap commit with no
  `SESSION_N`, because a subject generated from a stale on-disk banner is the #128 wrong-subject
  defect. **Nothing was staged by the refused run.** The doc-row gate, which cost three refusals in
  each of #289–#291, cost none — because `W-293da` and the regenerated `_CHAIN.md` went in **before**
  the first attempt, which is the reordering #292 proved.
- **A stray lane J appeared mid-ritual** — two files written at 15:01–15:03, with no sub transcript in
  this session's `subagents/` directory and no mention anywhere in the record. It is **uncommitted**,
  and its **provenance is not established from this seat**, which is the honest form; declaring it
  UNKNOWN would be a claim about the world, and staging it would be the #70 defect the `add -A`
  retirement exists to prevent.
- **The ★ LATEST banner closed at exactly 1,200 of 1,200 tape — zero headroom**, after eleven
  shortenings from a 1,252 first draft. #292 closed with two tokens and called the cap a shaper of the
  record rather than a constrainer of girth. **That complaint is now literal.**

## What is resolved, and what is still open

**Resolved.** The enactment question he opened with is answered with a census and receipts. The only
ruled-and-unenacted item in the record is built. Six of dream pass 13's seven are enacted. The memory
ceiling is discharged by a shard and a standing rule. The pre-flight line has a generator.

**Open, and every one of them is a question put, never a state of the world.** Move 3, the review
page, with its five judgement items · pass 9's disposition · the B3 grader, re-point-or-review · lane
E1's six ruling-shaped questions and lane DA's nine · the push and its CI read-back, which is the
first surface that will honestly ask `_capture_gate.py --selftest` · and everything #292 owed that
#293 did not touch, carried at its true age.

---

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA (#293). Ledger: nothing inscribed —
`knowledge/_rulings.json` stands at 622. Filed report:
`notes/_subreports/2026-09-21-293-W-wrap.md`. Lane reports:
`notes/_subreports/2026-09-21-293-DA-dream-enactment-audit.md` ·
`notes/_subreports/2026-09-21-293-E1-dream-enactment.md`. His words:
`notes/_lanes/293/DAVE-RULINGS-2026-09-21.md`. Handoff:
`_HANDOFF-144-the-dream-backlog-was-cut-down-and-the-review-page-is-owed.md`.*
