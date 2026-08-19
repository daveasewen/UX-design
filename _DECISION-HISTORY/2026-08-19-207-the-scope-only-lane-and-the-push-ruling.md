# #207 — the scope-only lane that stayed scope-only, and the one-line ruling that retired half a split

```
provenance: 207 · 2026-08-19
status: observed
```

*Step 1b of the capture ritual (`knowledge/_RUNBOOK-capture-ritual.md`): the WHY and HOW, written by
the delegated OPUS wrap sub. The WHAT lives on `GOOD-MORNING.md`'s ★ LATEST banner and in
`_LIVE-STATE.md`'s ⏱ LATEST delta; the one ruling lives in `knowledge/_rulings.json` as `s207-D1`.
Both-way links: spine entry = `_LIVE-STATE.md` ⏱ LATEST DELTA #207 · ledger = `knowledge/_rulings.json`
`s207-D1` · brief = `notes/_briefs/2026-08-19-207-wrap-brief.md`.*

---

## The arc, in one line

The session opened with Dave criticising the record the previous session had produced, spent its
budget scoping a lane it was forbidden to build, and closed on a single sentence from Dave that
retired a rule which had stood for seventy-four sessions.

## Finding 1 — the opener was a critique of the record, not of the work

Dave's first message was an addendum critiquing the #206 report. The conductor homed it as a
document (`notes/_briefs/2026-08-19-207-addendum-206-report-critique.md`, store row `W-51`) rather
than summarising it into a banner line, which is the `s185`-era forgotten-document rule doing its
job: a critique that lives only in chat is an un-retrievable citation.

Two things came out of it. First, an instruction — fix `knowledge/README.md:13`, which typed
"(38 metas)" against a live population of 92. That is the defect `P-5` had reported at #206 and
which #206 deliberately did not repair. Dave's word converted a reported finding into a repair, on
the #205 "do it" precedent. The repair landed at `2103316`, `README.md` was added to ASSERT-009's
`asserted_in`, and — this is the part that matters — **`P-5` was re-driven after the fix and
returned 0 findings.** The repair is measured rather than asserted, which is the whole difference
between an enactment register entry and a claim.

Second, a framing rule: decisions go to Dave in PLAIN PROSE, not as ID codes. That is why this
session's three open build calls are written out as "the decision-capture page", "the mint-time
brief generator" and "the CI pixel leg" everywhere in the record, and not as proposal numbers.

## Finding 2 — the conductor got the seating premise wrong at the opener, and Dave caught it

The conductor opened by saying "no subs". Dave: *"whre did you get the idea we are not using
subs??? anyway makesure you read teh chain before enacting anything in the prose I gave you"*.

The interesting part is the diagnosis. The conductor's *reason* — lane-size judgment — was sound;
its *framing* was a false generalisation about a standing policy. It owned the mis-framing rather
than defending the reason, and the lane was then delegated to an Opus scope-PM (128,752 tk). This
is the [[premise-ages-faster-than-rule]] shape with the sign flipped: not a stale rule, but a rule
invented on the spot to justify a defensible call.

## Finding 3 — `W-46` was scoped and scope-only held

`W-46` returned three proposals plus a 23-row claim table (`notes/_claims/207-w46-claims.jsonl`).
**Nothing was built.** That is the finding, not the absence of one: `s204-D1` ordered `W-46` as a
scope-only lane and every prior session's residual has carried "scope-only means scope-only" as a
live warning. This is the first session in which the warning was actually under test, and it held.

The evidence gate (`_validate_evidence.py`) passed rc=0 — but only after two catches at the lane
seam, and both are worth naming because neither was found by the gate's first run:

- **a mis-declared rc, corrected 0→2.** A claim asserted a return code the command did not return.
- **an honest proposed-directory pointer**, moved to the `s182-D1` linter's trailing-slash
  non-pointer form. The pointer was truthful and still illegal, because the linter cannot
  distinguish "a directory I propose creating" from "a directory I am claiming exists".

Both are seam catches. A check-in at the ends of the lane would have seen neither
[[checkin-at-the-ends-cannot-catch-the-lane]].

## Finding 4 — the lane's three findings are reported, and none is repaired

1. `s204-D1`'s "rulings tagged Dave's" filter **selects 204 of 204 rows**. It is not a filter. A
   predicate that selects everything reads as a safeguard and is a no-op
   [[instrument-without-a-consumer]].
2. `P-3`'s honest refusal **lacks a COULD-NOT-ASK marker**, so CI would read the refusal as a
   failure. The refusal design is correct and its *vocabulary* has no legal form in the consumer
   [[honest-refusal-needs-a-legal-form]].
3. The one existing decision deck is **89 commits stale**.

None was repaired, because repair-or-park on each is Dave's. That is the same discipline #206 held
with its own three catches — and it means **six reported-but-unrepaired defects now stack across two
sessions with no repair lane open.** The backlog, not any single defect, is the risk.

## Finding 5 — `s207-D1`, and why a one-sentence ruling is a large one

Late in the session, immediately after pushing `2f4dd6e` himself via Desktop, Dave wrote:

> *"btw, you are free to push whanevr you like, im comfortable with that now."*

Read back before inscription, then inscribed as `s207-D1`. It retires the *"push still only on
Dave's explicit word"* half of `s133-D2`, which had stood since #133. What did **not** move is
stated as explicitly as what did: the ruled call form (`_git_commit.sh --push`, master, ff-only,
verified) and the CI read-back owed in chat (`s203-D1`).

Enactment was same-session and **by addition** — `knowledge/_RUNBOOK-git-commit.md` step 5 now
carries the superseded sentence struck through with the correction beside it, rather than deleted.
That is the [[feedback-header-wins-over-audit]] discipline: a reader who arrives with the old rule
in their head needs to see it die, not to find it silently absent.

The consequence is worth stating flatly, because it is the pitfall this ruling creates: **a freer
push makes an unread CI verdict cheaper.** The read-back is still owed under `s203-D1`, and the
condition under which it starts getting skipped is exactly the one this ruling just made
comfortable.

## Finding 6 — the wrap was handed over past the advisory line, and the brief did not say so

The wrap brief declared FILL **149,006 real** at the wrap-brief cut — under the ADVISORY stop line
150,929 by 1,923. Measured first-hand from the wrap sub's seat one turn later, FILL was **158,954
real** — **past the line by 8,025**. The window moved 9,948 during the hand-over itself.

Neither figure is wrong. Both are true of different moments, and the failure would have been to
round one into the other. The general form is already inscribed
[[conclusions-are-debt-s129-d5]]: *"verified" is a property of a moment.* A declared cut is a
timestamp, not a session property, and the act of handing a wrap over is itself expensive enough to
cross the line it was measured against.

Alongside it, a second measurement finding: **boot 57,903 real is above the `s171-D1` band**
(56,158 ± 849 → 55,309–57,007) by 896. Checking backwards, #206's 57,133 was also above the band
and was published as *"in band"*. So the drift is two datapoints, not one, and the #206 claim was
wrong against the constant in the file. Declared here; **re-basing the constant is Dave's**, never
a wrap's.

## What is still open at the close

Everything Dave owns, carried and settled by nobody:

- the three `W-46` build/park calls — the decision-capture page · the mint-time brief generator ·
  the CI pixel leg;
- the promotion-vocabulary question (does mined history count as a "catch"?) and promote/wait on
  the three twice-caught candidates, with its store search already run and quoted at `W-51`;
- `W-49` repair-or-park on the 46 duplicate-id/IDREF findings;
- the five `W-44` schema choices; whether `notes/_claims/` earns a store row; PM-topology
  permanence (`s203-D2`); the could-not-ask exit protocol;
- re-basing the boot constant, if the two-datapoint drift is worth it.

And two instruments — `W-44` and `W-45` — still wait on one consumer event.
