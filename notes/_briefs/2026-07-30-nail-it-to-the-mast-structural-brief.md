# Brief — nail it to the mast: why the bloat returns, and the three mechanisms that stop it

```
provenance: local_4ed75a66-d418-4ebf-862e-e583c6703c93 · #39 conductor · 2026-07-29
status: observed
```

*Written at #39's close on Dave's ruling. His words, and they are the brief's whole premise:
**"we've done this before, assumed everything is okay just for everything to grunge up again…
and again."** Deadline: **Friday 2026-07-31.** Item 3 LANDED at #39; items 1 and 2 are Thursday's.*

⚠ **Read §1 before touching anything.** Every previous attempt cut the file and every one was
undone, because they were all the same kind of thing: a decision to write less. §1 is why that
class cannot work.

---

## §1 — THE MECHANISM. Why it comes back, stated so it cannot be mistaken for a discipline problem

**The cap fires at WRAP — after the session's record is written.** By then the only response
available is to cut something already written. That is the loop:

```
session records work (correctly — that IS the job)
  → cap fires at wrap
    → session shaves live record to fit
      → session records the shaving
        → file is bigger than before
```

**#35 did six trimming rounds. #38 did three. The region grew through both.** It is now 12,734 tape
against a 12,000 block — bigger than when the block was introduced.

★ **And trimming cannot work, which #38 measured rather than assumed: retiring a VERIFIED-DEAD item
netted +16 tape.** A retirement must leave a legible clause and the clause costs what the line cost.
⇒ **the region has a FLOOR that retirement cannot lower.** Dead weight is not what is left to cut.
Live record is. **The gate was inside the growth loop, not braking it.**

⇒ **"Add less" is a behaviour. The growth is structural.** A behaviour has to be re-chosen every
session and eventually is not. The ritual *mandates* additions — banner, state lines, findings,
corrections, receipts. A resolution to add less fights the ritual and loses. **Every fix below
removes a mechanism instead.**

### The second half, and it reframes the whole problem

**Since #33 cut the read chain, most of that growth costs nothing.** Measured #39 (Lane A):

| region | tape | paid at cold start? |
|---|---|---|
| read chain (HDR + ★ LATEST + LS ⏱ delta) | **4,801** | ✅ every session |
| compactable (the capped region) | **12,734** | ❌ ~8,000 of it never |
| corpus (GM + LS whole) | 37,540 | ❌ retrieval only |

**The cap was charging boot prices for a retrieval queue.** It says so in its own comment, dated
2026-07-27 — *"true cold-start cost"* — which was correct on the day it was written and was
falsified by #33 the next day. [[premise-ages-faster-than-rule]].

---

## §2 — ITEM 3, DONE #39. The receipt, so Thursday does not re-derive it

⛔ **`SIZE_BUDGET_TK["compactable_block"]` 12,000 → `None` (ADVISORY).** Ruled by Dave #39.
`knowledge/_capture_gate.py`. Flag + selftest pin + fixture moved as a set, the standing discipline.

- The **WARN at 8,000 STANDS**, deliberately — an un-instrumented region is how this one reached
  21K before anyone looked (`_capture_gate.py:357`). It now prints the grunge instruction in its own
  message: *"if this number is climbing session on session, that is the grunge signal — say so in the
  banner and re-open the contract. Do NOT shave live record to quiet it."*
- The over-block fixture was **flipped `True`→`False`, not deleted.** It still proves the region is
  measured, and **it turns red the moment a block is restored** — which is exactly what §3 does.
  The swap gets caught by a test rather than by a session noticing.
- Verified: selftest exit 0, all failure classes bite, green control passes. Live wrap went
  `❌ FAIL` → **31 in scope · 0 fail · 5 warn.**

⚠ **THE GAP THIS OPENS IS DECLARED, NOT OVERLOOKED.** M10 `read_chain_tk` — the cap on the region
that *does* cost — is **still ADVISORY.** Right now **nothing binding guards cold-start cost.**
That is a known hole for ~one day and closing it is §3.

---

## §3 — ITEM 1: SPLIT BY COST. The seam, and the swap that is owed

**The defect is one file under one contract holding two things with different costs.**

| | today | after |
|---|---|---|
| chain content (paid every boot) | inside `GOOD-MORNING.md`, no binding cap | **its own file, small, HARD BLOCKING cap** |
| retrieval content (paid on demand) | inside `GOOD-MORNING.md`, was blocked | stays, **warn only, no block** |

**Then you cannot bloat the expensive thing, because the expensive thing is a separate small file.**
Not "must not" — *cannot*. That is the difference between this and every previous attempt.

**THE SWAP IS THE POINT: one enforcement out, one in.** #39 removed the block on the free region.
Thursday must add the block on the costly one, or the net effect of this whole programme is
*less* enforcement than it started with — which is how it grunges up again.

⬛ **DAVE'S NUMBER #1 — the chain cap.** M10's current 4,500 warn / 6,000 block-candidate are
**agent-derived and have never been ruled.** Measured now: **4,801 tape, already over the warn.**
⚠ Do not let an agent promote them by noticing they should be promoted — that is precisely ds-023,
where an enforcement Dave never made hardened into a gate. **Put the number to him with the
measurement; he rules.**

⚠ **Where the seam goes wants Dave's eye.** §A is standing and uncapped; §C is retrieval; the banner
is chain. The LS `⏱ LATEST delta` is the awkward one — Lane A found it is the **only split region**
(1,476 tape chain, 3,739 retrieval, one file, one block).

---

## §4 — ITEM 2: AUTOMATIC DISPLACEMENT. Growth impossible by construction

**The mechanic already exists and already works.** Banner compaction (2c/2d) keeps LATEST + 1 PRIOR
and rolls the rest to `_GM-ARCHIVE.md` verbatim, by script, at wrap. **Nothing is lost and no
judgment is involved.** Sixteen sessions of evidence that it holds.

**Extend that exact mechanic to every growing region.** Each declares `N most recent`; `_gm_move.py`
rolls the overflow at wrap. Then:

- growth in the live file is **bounded by construction**, not by restraint;
- nothing is deleted, so **nobody has to decide what is worth keeping** — the decision that makes
  trimming slow, painful and lossy simply stops being asked;
- the floor problem in §1 dissolves: a roll is not a retirement, so it does not have to leave a
  legible clause, so **it actually reduces the file**.

★ Your own runbook already has the principle, from the parallel-lane work:
**"nothing clashes by construction, not by good behaviour."** This applies it to size.

⬛ **DAVE'S NUMBER #2 — `N` per region.** One number, possibly one per region. Cheap to change later
because rolling is lossless.

⚠ **`_gm_move.py` already has a selftest and hardened move mechanics (M5).** Extend it; do not write
a second mover. ⚠ Banner headings are BLOCKQUOTED — anchor on `> ## ★ PRIOR …`.

---

## §5 — THE TRIPWIRE. Because "we assumed everything is okay" is the actual failure

Dave's warning is not that the fix will not work. It is that **nobody will notice when it stops
working.** Every mechanism above is silent when healthy — which is what let the last one rot.

**So the deliverable is not three fixes. It is three fixes plus a way to find out.**

Cheapest honest instrument, and both fields are already written every session by hand:

```
per-session stamp:   band  |  self-reported error count
```

⚠ **CHECKED #39, and the dataset does NOT exist yet:** ~5 unstructured `WHAT I GOT WRONG` instances
across 38 sessions, and the gauge log carries band stamps without paired quality data. **It cannot
answer the degradation question today.** Structure the two fields and in ~10 sessions it can —
which is the only path to a threshold that does not rest on feel. **Dave, #39: "I wouldn't trust my
'feels', that might be the problem."** He is right, and this is the answer to it.

⚠ **WARN, NEVER BLOCK.** [[gate-narrows-its-own-rule]]. A blocking tripwire on an uncertain number
rebuilds the exact loop in §1.

---

## §6 — SEQUENCE, AND WHAT NOT TO DO

1. **Item 3** — ✅ DONE #39. Unblocks every session immediately.
2. **Item 2** (`_gm_move.py` extension) — worker-lane shaped, mechanical, needs Dave's `N`.
   Do this before item 1: it shrinks the file, so the seam in item 1 is cut on a smaller thing.
3. **Item 1** (the split + the M10 swap) — biggest, wants Dave's eye on the seam, and **carries the
   enforcement debt §2 declared.** Not done by Friday ⇒ say so out loud; do not let it go quiet.
4. **Item 5** (the tripwire fields) — fold into the wrap stamp while item 2 is open; same file.

⛔ **THE THINGS THAT WILL UNDO THIS, named so they can be refused:**

- **Shaving live record to quiet a warn.** That is the §1 loop. The warn is now advisory precisely
  so it can be *reported* instead of obeyed. #38's banner had to cut the very addendum describing
  the cap it was being cut by — **that is the shape to watch for.**
- **Promoting an advisory number because it obviously should be promoted.** ds-023. Dave rules.
- **Declaring it fixed.** Every mechanism here is silent when healthy. §5 exists for that reason.
- **Adding a fourth mechanism.** Three is the plan. A fourth is this programme eating another week
  that belongs to components — which is the real cost, and #33–#39 have already spent seven sessions.

## Entry points

`knowledge/_capture_gate.py` § `SIZE_BUDGET_TK` (the #39 amendment, with its full reasoning) ·
`knowledge/_gm_move.py` (M5 mover + selftest) · `knowledge/_RUNBOOK-capture-ritual.md` steps 2c–2f ·
`notes/_briefs/2026-07-29-cap-repoint-and-lane-divvy-brief.md` (#38's finding, still the source) ·
`notes/_receipts/2026-07-29-lane-a-region-measurement.md` (every number in §1) ·
`notes/2026-07-29-context-degradation-research.md` § P2 (absolute-token bands) — ⚠ `status: floated`.
