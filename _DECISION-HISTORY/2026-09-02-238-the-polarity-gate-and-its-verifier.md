# 2026-09-02 · #238 — the polarity gate and its verifier: seven rulings in one reply, six lanes on a quota-burn licence, and a gate whose builder said 45/45 while its attacker said 48 walked through

provenance: 238 · 2026-09-02
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #238 · `GOOD-MORNING.md` ★ LATEST #238.
Rulings: `knowledge/_rulings.json` § `s238-D1` … `s238-D7` (the store went **321 → 328** at the conductor's
seat; every id was read back from the file at the wrap seat). Not one word of them is re-worded here — this
file quotes ids and Dave's own short phrases and nothing else.
Lanes (brief → filed report, evidence beside each at `notes/_subreports/assets/2026-09-02-238-<X>-…/`):
P `notes/_briefs/2026-09-02-238-P-polarity-gate-brief.md` (`W-363`) → `notes/_subreports/2026-09-02-238-P-polarity-gate.md` (`W-364`) ·
A `…-A-plan-v2-brief.md` (`W-365`) → `…-A-plan-v2.md` (`W-366`) + `_PLAN-designers-brain-2026-09-02-v2.html` (`W-375`) ·
B `…-B-L2-behaviour-address-brief.md` (`W-367`) → `…-B-L2-behaviour-address.md` (`W-368`) + `_REVIEW-L2-behaviour-address-2026-09-02-v1.html` (`W-376`) ·
C `…-C-licence-tiering-brief.md` (`W-369`) → `…-C-licence-tiering.md` (`W-370`) ·
M `…-M-runbook-and-W355-brief.md` (`W-371`) → `…-M-runbook-and-W355.md` (`W-372`) ·
V `…-V-polarity-verifier-brief.md` (`W-373`) → `…-V-polarity-verifier.md` (`W-374`).
Common rules for all six: `notes/_briefs/2026-09-02-238-COMMON-lane-rules.md` (`W-362`). This wrap's brief: `…-delegated-wrap-brief.md` (`W-377`).
Written by the delegated wrap sub from the wrap brief and the filed reports; the WHY is the conductor's arc as the brief
records it, the HOW is what the reports say they did. Where this file cannot see a thing first-hand it says so.*

---

## 1. Why the question was "edges or nodes" and why the answer was neither of the two on the page

#237 ended with two of the twelve §8 questions still open, and the first of them — **R1 Q4, tensions as edges or
nodes** — had a review page built for it with two readings drawn side by side. Dave's opener did not pick one. He
asked a different question: *"is the edges on edges such a daft idea???"* — a relationship whose parties are
themselves relationships, which neither reading on the page allowed for.

The conductor drew three readings instead of two: **(a)** a plain edge between two register nodes, **(b)** a reified
edge — a node that stands for the relationship and carries its own typed parties, and **(c)** a hyper-relational
node with N parties of any register kind. The observation that settled it was structural, not aesthetic: (a) and
(c) both **project down** from (b) — a reified node with two principle parties IS a plain edge; a reified node
whose party list is open IS the hyper-relational case. Dave heard that and answered *"that's sort of what you are
saying aren't you?"* — the reading he took was (b), and `s238-D1` records it as the ONE home: a polarity is a node
with N typed parties, each resolving to a register node, typed out-links only, pairwise edges DERIVED for consumers
and never authored, and a second stored shape for the same concept REFUSED.

**Why this mattered more than a data-model choice.** The T review had priced the whole tensions schema on the
assumption that the shape was a two-ended thing. Once the shape is a node with parties, the five ruling-shaped
questions lane T left behind stop being independent and start following from it — which is how the rest of the
morning's rulings came in one reply rather than five.

## 2. How "make the risks dissolve" became five refusals

Dave's next move was *"how do we make the risks dissolve"*. The conductor's answer was not a list of cautions but
**five refusals** — things a gate would say no to, each aimed at one way the node shape could rot: a party or link id
that resolves to nothing; an untyped link; a judgement text field on a polarity (its only judgement is a typed link to
a ruling id); an authored edge file (edges exist only under a generated path with a freshness check); a typed
status. He answered the six-item list with *"I'm happy with your recommendations on all"*, and that one sentence
is the `says` field of `s238-D3` … `s238-D7`.

The ordering of the six was deliberate and is worth keeping: the rename came first (`s238-D4` — "tension" was
already a confirmed `s202`-class collision, 43 hits, and the term of art for two true things you manage rather than
solve is **polarity**), because every generator and every gate below it would otherwise have been born with the
wrong word in its filenames. Then the settlement of the 21 open rows by DERIVED defaults with only four ask-whens
for Dave (`s238-D3`) — the standing grill grows by zero, which was lane T's headline and now has a mechanism. Then
the declaration cap (`s238-D5`) — declare only the defaults that bent away from the conservative side, so the field
built for six is not widened. Then typed links (`s238-D6`) — `resolvedBy` / `explainedBy` / `challengedBy` /
`touches`, the generator refusing an untyped one, with the `apollo_touch` slot migrated row by row and any row the
evidence does not settle marked UNPROVEN. Then the gate itself (`s238-D7`), whose last sentence is the one the rest
of the session tested: *a gate that is not a consumer of every commit is not a gate.*

`s238-D2` sits beside these and is the other #237 open question — the first question's three answers, in Dave's
own words from #237, carried un-inscribed and confirmed firm here.

## 3. Why six Fable lanes ran at once, and what that licence actually bought

Dave's words were *"rinse fable"*, *"max out the tokens"* and *"just test the crap out of it"*. That is a QUOTA
licence, not a FILL licence [[budget-vs-quota-vocabulary]], and the conductor spent it as one: six lanes, each with a
brief and a COMMON rules file, each filing under `s218-D7`, each forbidden git, the store, the spine and memory.
Sub spend as the harness reported it: **P 466,406 · A 346,542 · B 393,936 · C 391,884 · M 258,600 · V 317,298 —
2,174,666 tokens (n=6)**, UNMEASURED at the subs' own seats and never added to any FILL figure.

What the licence bought, lane by lane, off each file's own COUNTS line:

- **P** built the gate and its home. `knowledge/brain/` was DECLARED by the lane because plan v1 §P1 named no
  path. Rows 30 · parties 68 · stubs 15 · links 21 (resolvedBy 7 · explainedBy 1 · challengedBy 4 · touches 9) ·
  refusals 5 · **selftest arms 55, red 45/45** · generated files 3 · findings 15 · ruling-shaped 8 · UNPROVEN 6.
  The gate was wired at the commit seam of `_git_commit.sh` and as `_build_all.py` steps [141]/[142].
- **A** re-cut the plan as v2, GENERATED from the store so all 17 quoted rulings are verbatim by machine (17/17)
  and the old word is absent from prose (0 of 34). Findings 9 · ruling-shaped 0 · UNPROVEN 4; renders 4/4 with
  overflow NONE; sha256 `98f00e9a…`. Its §0/§10 is Dave's surface — 28 open items, each with an owner.
- **B** built L2 as a PROPOSAL: the address schema, 20 migrations that validate 20/20 with 136/136 live metas still
  green, a generator and a gate, and a review page for Dave's eye. Metas UNTOUCHED. Findings 13 · ruling-shaped
  5 · UNPROVEN 5 — all 14 of the `fallback` readings among them.
- **C** tiered 12 of the 13 untiered licence families on fetched notices (families 13 · fetched ok 12 / failed
  1 · tiered 12 · UNPROVEN-licence 1 · names-only 7). Shneiderman stays UNPROVEN because the site carries no
  notice at all; finding 1 is ISO's AI clause. Findings 11 · ruling-shaped 5 · UNPROVEN 10.
- **M** filed the render-runbook correction as the **EIGHTH** stratum — the file already carried #233's seventh,
  so the carry's "seventh" was a stale premise, corrected at the source — and made the `W-355` fix as a DECLARED
  form (`SESSION_N` + `SESSION_ACK` together; 9/9 arms, whole harness 42/42). Findings 18 · ruling-shaped 2 ·
  UNPROVEN 4. `W-355` stays OPEN by its own `closes_when`: the form exists, no post-wrap handoff has yet gone
  through it from a live seat.
- **V** attacked P's gate under `s172-D3` (depth cap 1: report, never fix). That is section 4.

## 4. The headline, and why the builder's 45/45 and the verifier's 48 are both true

P's self-test says every one of its 45 refusal arms goes red. V drove **111 attacks** through the three real doors
(CLI, the `_build_all.py` STEPS entry, the commit seam) and found the doors agree with each other **96/96** and the
live tree is **GREEN**. Both of those hold at this seat too. And **48 hostile rows walked through all three doors**
— RULED 16, PROMISED 26, UNRULED 6 — with **10** inputs that CRASH rather than refuse by name, and **3** refusals
that fire under the wrong name.

There is no contradiction, and naming why is the point of this section: **a self-test proves the builder's clauses,
not the ruling.** P's arms test that each refusal P wrote fires when P's own mutation is applied. V's attacks test
whether `s238-D7`'s five sentences hold against inputs P did not think of. V's three structural findings say where
the gap lives: (2) "live" for a ruling is read off ONE field (`superseded_by`, set on 1 of 328 rows) while four rows
say "superseded" in prose and are therefore live to the gate; (4) the verbatim-quote guard trusts an oracle the
node names for itself, so a broken pointer yields "UNVERIFIED" on every quote and a green last line; (6) the schema
is an unguarded loosening surface — nothing pins it, and the self-test copies the loosened schema along with the
rows. Finding 12 adds that the migration's rule-letter on tn-22 licenses a link by an inference the printed rule
does not describe, so the sort P reports as **6·4·20** (against the ruling's parenthetical 6·9·15) re-opens a row
under V's reading to **6·3·21** — UNPROVEN either way until Dave's eye is on the four quotes.

So the record at this wrap reads: **`s238-D7` is BUILT and NOT SATISFIED.** Its proof standard is
`notes/_subreports/assets/2026-09-02-238-V-polarity-verifier/escaped-repro.txt` — 48 rows, each with the command
that reproduces it — and not P's arm table. That is #239's first beat: a fix lane against the 48 (RULED 16 first),
then V again. Nothing about it was fixed at the wrap; the wrap's licence is to record, and a fix under wrap heat
is how a second self-test gets written that proves a second set of clauses.

## 5. The gauge, and the lesson that held for a second session

Boot **75,336 real** (first turn, outside the `s208-D1` band; ordinal not claimed, no constant moved). Opener FILL
**103,211 @ 8 turns**. Post-lanes FILL **198,667 @ 45 turns** — past the advisory 150,929 by **47,738**, declared in
chat, judgment closed there. The recall probe was planted at 14:24:04Z and quizzed blind **4/4 GREEN at 198,667**
(`knowledge/_probe/session-238.json`, `last_check.at` 15:37:14Z). Effort band **L**.

The measurement worth keeping is the one #237 named and #238 reproduced: **a lane costs about 19K of conductor
FILL all-in** — launch, stub, REPLAY-THESE read, reconcile — measured over five lanes as 103,211 → 198,667. The
#237 lesson was that a lane launched past the advisory returns INTO the band; the #238 reading prices what each
return costs. Both are in `notes/_GAUGE-LOG.md`, where they can be counted, not here, where they would be quoted.

## 6. What the wrap seat corrected, could not see, or left alone

- **The "seventh stratum" carry was a stale premise**, not a stale rule — the runbook already had a seventh. Filed
  as the eighth by M; the carry is struck with that receipt, and the strike names the correction rather than
  re-typing the item.
- **`_validate_wiring.py` is red on #235's orphan `_validate_receipt.py`** — seen by P and by M, pre-existing,
  deliberately NOT fixed at the wrap. It is carried, not smoothed.
- **`_build_all.py` now has 142 steps** ([141]/[142] are P's). The chain's "75 of 140" build-verdict sentence is a
  premise that has aged; the wrap names it and moves no number.
- **Lane A's ~11 MB of PNG assets are committed** (21 files, 10,967,092 B measured at this seat). Whether asset
  size wants a policy is ruling-shaped and Dave's; committing them is declared, not defended.
- **The wrap seat did not see Dave's answers first-hand.** They are chat testimony relayed by the brief; what IS
  repo-verifiable is that `s238-D1` … `s238-D7` stand in `knowledge/_rulings.json` with his phrases in their `says`
  fields, and that is what was read back.

## 7. Resolved state, and what is still open

**Resolved:** polarity = hyper-relational node, one home (`s238-D1`) · the first question's three routes (`s238-D2`)
· derived defaults with four ask-whens (`s238-D3`) · the rename (`s238-D4`) · the declaration cap (`s238-D5`) · typed
links (`s238-D6`) · the five-refusal gate, built and wired (`s238-D7`) · plan v2 exists · L2 exists as a proposal ·
12 of 13 families tiered · the eighth stratum and the `W-355` declared form both landed.

**Open, mine:** the fix lane against V's 48, then V again · the wiring red · the aged build-verdict premise · the
6·4·20 vs 6·3·21 sort · the committed asset size.

**Open, Dave's:** the four ask-whens · the conservative side of the 20 open polarities (0 declared / 20 UNPROVEN —
`s238-D5` cannot run until they are ruled or derived) · pl-02 / pl-29 link types and V's three migration
disagreements · P's Q1/Q2/Q6 · B's five · C's ruling-shaped questions and which families enter · M's two
(`render.py` / §6 still assert with `fonts.check`) · plan v2 §0/§10 · the "gestalt" collision · L1's three
questions, carried again at their own age. The full carry set, every prior item at its own age, is
`_CARRIES.md` § `## residual → #239`.
