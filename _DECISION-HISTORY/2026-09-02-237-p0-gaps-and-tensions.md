# 2026-09-02 · #237 — P0: ten answers in one message, seven gaps closed, and thirty tensions that turned out not to be a grill

provenance: 237 · 2026-09-02
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #237 · `GOOD-MORNING.md` ★ LATEST #237.
Rulings: `knowledge/_rulings.json` § `s237-D1` … `s237-D10` (the store went **311 → 321**; every id
was read back from the file at the wrap seat).
Gap half: `notes/_briefs/2026-09-02-237-G-gap-discharge-brief.md` (`W-356`) → filed
`notes/_subreports/2026-09-02-237-G-gap-discharge.md` (`W-357`).
Schema half: `notes/_briefs/2026-09-02-237-T-tensions-schema-brief.md` (`W-358`) → filed
`notes/_subreports/2026-09-02-237-T-tensions-schema.md` (`W-359`) +
`_REVIEW-tensions-schema-2026-09-02-v1.html` (`W-360`).
Evidence beside each report at `notes/_subreports/assets/2026-09-02-237-*/`.
This file holds the WHY and HOW; the WHAT is in the spine, the two filed reports and the ruling
store, and is not repeated here.*

---

## 1. The shape of the morning-after: a decision surface that actually got decided

#236 ended by handing Dave a plan and twelve ruling-shaped questions in its §8. The interesting
thing about #237 is what that cost him: **one message**. Ten of the twelve came back answered in
his own words, and the wrap's job was to inscribe them rather than to negotiate them.

That is the case for the decision-surface pattern, made empirically rather than argued. The
alternative — asking twelve questions across twelve exchanges as they arise — was what #233–#235
had been doing, and it spends a window on turn-taking. A page that collects every open question
with its options and its recommendation converts a conversation into a single reading.

⚠ **The two that did NOT come back are the informative half.** R1 Q4 (tensions as edges or nodes)
came back unanswered because the plan deliberately carried **no recommendation** on it — lane P
was fenced from that lane's schema. And R2 Q3 (the first question) came back *rewritten*: Dave
did not pick an option, he restated all three in his own words. ⇒ **A question with no
recommendation and a question whose options are wrong both fail in the same visible way — they
come back without a "firm".** The remedy in both cases is another artefact, not another ask: for
Q4 that is lane T's review page, for Q3 it is his own wording carried verbatim until he confirms.

## 2. Why the grade names were the expensive part

Five words arrived mid-session and became `s237-D1`'s body: **REPLICATED · STUDIED · PRACTISED ·
DEBUNKED · OBLIGATION**. R1 had graded 145 principles A/B/C/D/L and the letters were placeholders;
they were about to be imported into a knowledge graph where a letter grade would have travelled
as a schema field with no meaning outside this repo.

Naming them cost one exchange and closed a class of future defect: **a letter is a label whose
meaning lives in a document; a word is a label whose meaning lives in the reader.** The
definitions have exactly one home (`s237-D1`), and everything downstream — the plan, the graph,
any gate — derives from that one home rather than restating it [[generation-chain-not-copy-chain-234]].

## 3. Lane G: seven gaps, and the two that closed by an unexpected route

The gap lane existed because #236's research had five UNPROVEN claims and #236's own wrap carried
them as a priced carry: *"R1's UNPROVEN 1, 4 and 5 are priced and must not reach a client
unproven."* Lane G took seven gaps and discharged all seven — but the discharges are not uniform,
and the report refuses to smooth them:

- **`R1-1` (the ISO 9241-110 interaction-principle names)** discharged **at names-only depth**,
  from Molich's licensed **draft** reproduction rather than the published standard. That is a
  genuine discharge for the purpose it serves and it is NOT the standard; the qualification is
  written into the strike so it travels with the fact.
- **`R1-4` (DSA Article 25)** discharged from EUR-Lex directly, and the mirror verdict came back
  **SAME** — which retires #236's own worry that the mirror text might have drifted. §§2–3 turned
  out to be new material, and §3's three named practices are all generator decisions.
- **`R1-5` (the INP thresholds)** discharged with the qualifier that matters more than the
  numbers: good ≤200 ms / needs-improvement >200–500 / poor >500, **at the 75th percentile of
  field page loads, mobile and desktop separately**. A threshold quoted without its population is
  not a threshold.
- **`R2-2` (the video)** was **dropped by Dave**, not discharged. A dropped gap and a closed gap
  read identically in a count; they are recorded differently on purpose.
- **`R2-3`** is the one worth remembering. The probe proved the repo, mount and sandbox hook
  layers clear and then hit a **tool fence**: the user-level and managed layers are not reachable
  from any seat we own. It was filed as DISCHARGED-with-residual, closing on two terminal
  commands — and Dave then **ran them and pasted the output in chat**, which closed it inside the
  same session. The output is recorded inside `s237-D8`'s `says` field, because a terminal paste
  in chat is un-retrievable [[capture-ritual]] and the ruling store is the durable home.

★ **The generalisable half: a fence is not a failure, it is a hand-off with a stated close
condition.** The lane could not have crossed it; naming the two commands is what let the one seat
that could — his — close it in minutes.

## 4. Lane T, and the finding that changed the question

The tensions lane was commissioned to answer "edges or nodes" and came back saying the question
was less expensive than it looked. Thirty tensions sorted into **6 settled-by-obligation · 3
resolved-here · 21 open**, and of the 21, only **four** are questions — the other **17** are
default-and-declare.

⇒ **The standing grill grows by ZERO.** The four questions are all conditional, so none of them
becomes a permanent thing Dave is asked. What grows instead is the `Defaults used:` declaration,
and there the number is uncomfortable: **21 lines into a field designed for about six**. The cost
did not vanish, it MOVED, and it moved into a surface nobody has capped. That is the shape of the
ruling-shaped question the lane filed rather than answered.

Two side findings that are not decoration:

- **Finding 5 — "tension" is a confirmed `s202`-class vocabulary collision**, 43 hits, and
  `s143-D1` already downgrades TENSION → CROSS-REFERENCE. This is the second such collision in two
  sessions (the first being "gestalt" at #236). ⇒ **Importing a body of external vocabulary into a
  house with its own vocabulary produces collisions at a rate worth budgeting for, not treating as
  a surprise each time** [[vocabulary-collision-switch-202]].
- **Finding 11 — the stored `fonts.conf` hardcodes another seat's mount path**, which is a second,
  independent cause under the render-runbook seventh-stratum correction already owed since #236
  (the `playwright install` failure). Two causes, one correction, still not made.
- **Finding 12 — the 390-width overflow on the review page was fixed AT THE CAUSE**, not by
  clamping the symptom. Worth recording because the alternative was available and cheaper.

## 5. The gauge lesson, which is new and is the reason this session ran hot

The measured arc: opener **FILL 109,659 @ 4 turns** → lane-G seam **163,186 @ 26 turns**, past the
**150,929** advisory by 12,257 and declared in chat → post-lane-T **204,725 @ 38 turns**, past the
**200,000** working wall, declared in chat, judgment closed there.

★ **THE LESSON: a lane launched past the advisory returns INTO the band.** Lane T went out at
~185K. Launching a sub is nearly free in window FILL — that is the whole delegation-inversion case
[[delegation-cost-inversion-110]] — but its **return** is not: the stub, the REPLAY-THESE read and
the reconcile all land in the conductor's window, and they landed him at 204,725.

⇒ **The decision to launch a lane must be priced at its RETURN, not at its launch.** The existing
advisory prices the launch. This is a distinct term and it is the reason the wall was crossed:
nothing was wasted, and nothing was mis-measured, but the arithmetic that said "a sub is free" was
answering a different question from the one being asked at 185K.

Recorded in the `#### 2026-09-02 #237` block of `notes/_GAUGE-LOG.md` rather than left in chat, so
it becomes a datapoint rather than an anecdote.

## 6. What is still open, and who owns it

- **R1 Q4 and R2 Q3** — Dave's, and both have their artefact ready (the review page; his own three
  sentences quoted verbatim in the carry).
- **Lane T's five ruling-shaped questions** — who settles the 21 open, whether "tension" is
  renamed, a cap on the `Defaults used:` declaration, typed ruling links.
- **Plan v2** — the plan re-cut against what #237 closed. Never an edit of v1.
- **`W-355`** — mine, not his: a post-wrap `_HANDOFF-<n+1>.md` cannot be committed from either
  seat while it exists, because `SESSION_N` trips R3 CHAIN OVERTAKEN and `SESSION_ACK` is only
  read when `SESSION_N` is absent. Reproduced at this seat; the fix is priced, not made.
- **L2**, and L1's three questions, rolled from #236 — L2 did not run and is carried, not dropped.

⚠ **Nothing in section 6 was decided at the wrap seat.** Where this session's brief gave no
judgment, the wrap wrote `UNPROVEN — conductor's` rather than choosing.
