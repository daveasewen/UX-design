# Lane B receipt — Dave's six opens, assembled for ruling

```
provenance: worker-lane-b-six-opens · 2026-07-29
status: observed
```

**Register: WORKER HAND-BACK. Nothing ruled, nothing enacted, no git, no serial-set writes.**
**Lane:** B of the divvy in `notes/_briefs/2026-07-29-cap-repoint-and-lane-divvy-brief.md`.
**Job, verbatim from the brief:** *"for each of the six opens in GM §C·4, assemble what Dave needs in
order to rule — his own verbatim words where they exist, what has changed since, and what each option
would cost. ASSEMBLING, NOT DECIDING. A lane that arrives at a recommendation has exceeded its brief."*

> ## ⚠⚠ THIS RECEIPT IS UNCOLLECTED
>
> **Dave assigned Lane B and stated that a DIFFERENT session conducts.** No conductor was running when
> this was written: `git log` showed `1e76621` (#38's red wrap, 11:45) as HEAD, and none of the three
> #39 lane receipts existed. **This receipt has no collector yet.** The brief's own warning is the
> reason this banner exists — *"#37 left a worker's receipt uncollected because it read the files as
> 'not my paths'; the conductor reconciles and commits, workers hand back and stop."*
>
> ⚠ **Lanes A and C had not run either.** The cap fork cannot be put without Lane A's numbers.

> ## ⚠ AUTHOR CONTAMINATION — DECLARED, because it bounds what this receipt is worth
>
> This window opened as **conductor** and was re-roled to **worker** mid-session. Before the re-role it
> had already read `GOOD-MORNING.md` lines 1–90 (header · ★ LATEST · ★ PRIOR · `DO THIS FIRST` ·
> pointers · the read-chain contract) and the full divvy brief — **more than Lane B's READ-EXACTLY-THIS
> list.** It did **not** read `_LIVE-STATE.md` at all.
> ⇒ **This lane cost more than a clean Lane B would have.** It is also why this window declined Lanes A
> and C when offered: A forbids GM prose and C forbids #37 state lines, and both had already been read.

---

## ★ THE CROSS-CUTTING FINDING — open 5 is not a sixth item, it is upstream of three others

**OBSERVED, not recommended. The ordering consequence is Dave's to draw, not this lane's.**

The FLOATED note (open 5) is carried in §C·4 as one open among six. Reading it — which no session has
done in three sessions — shows it **bears on opens 1, 2 and 3**, not only on (2) as the brief expected.
Its three load-bearing claims were **verified against the code this window, not taken from its prose:**

| The note's claim | Verified at | Holds? |
|---|---|---|
| The gauge divides by a hardcoded, never-measured window | `knowledge/_context_gauge.py:27` — `DEFAULT_WINDOW = 200_000` | ✅ **confirmed, literal** |
| `tape` is `cl100k`, which is OpenAI's tokenizer, not Claude's | `knowledge/_capture_gate.py:294` — *"`tape` — what tiktoken cl100k_base counts"* | ✅ **confirmed** |
| `MODEL-ROUTING.md`'s default tier names a superseded model | `MODEL-ROUTING.md:17` — *"Default — complex \| **Opus 4.8 · high**"* | ✅ **confirmed stale** |

**The dependency, stated flatly:**

- **Open 1 (above 63)** asks Dave to rule a threshold in **`%`**. The note's finding is that `%` **of
  what** is unset — the denominator is a guess in code. Ruling a number above 63 is ruling a point on
  an axis whose scale is unverified.
- **Open 2 (`ds-025`'s remedy)** is *"every load-bearing number in the throttle is one no session can
  observe from inside itself."* The note names a fourth such number — the **window** — and separately
  reports two platform capabilities that bear directly on ds-025's option (a)/(b)/(c): a
  **token-counting API** and **context awareness on Sonnet 5**, described as *"a free live meter."*
  ⚠ **This lane did not verify those two capabilities exist as described** — the note says it fetched
  them from platform docs on 2026-07-29; that verification is not this lane's and has not been done.
- **Open 3 (the chain's SCOPE)** is denominated in **`tape`**. If `tape` is a proxy in the wrong
  tokenizer, the `+3,415` figure for `DO THIS FIRST` is a proxy measurement, not a measurement.

⚠ **And it bears on the CONDUCTOR'S OWN JOB.** The cap fork asks which region the budget points at and
at what number. Every candidate number — 8,000 · 12,000 · 4,500 · 6,000 · 36,000 — is in `tape`.
**This is not a claim that the cap work is wrong.** It is a flag that the fork's unit has an open
question underneath it, which Dave may want to know before ruling, or may explicitly rule irrelevant.

★ **The shape is already named in this corpus:** [[premise-ages-faster-than-rule]] and
[[measure-dont-convert-units]] — *a count is not a measurement; name the unit.* The note's own framing
is that this is the instrument built to enforce that rule, failing it.

---

## Open 1 — What happens ABOVE 63

**Ledger:** `knowledge/_DS-IMPROVEMENTS.md` § ds-023. **State:** OPEN, and the *only* part of ds-023
still unruled.

**Dave's words that exist.** On the original miscalibration (#30): *"I think that calibration of the
headroom is wrong… I think it's calculating 60+15 headroom is okay and it definitely isn't, 60 should
be a hard stop."* On the band (#36): `45–60` preferred, **~60 livable** — *"I can live with it, it's
safe-ish"* — 63 tolerable when rare and marked. **On above-63 he has said nothing, and the silence is
deliberate on his side, not an omission.**

**What has changed since.** ds-023 was re-stated as a BAND at #36 and **enacted at #37**:
`PREFLIGHT_CEILING` is gone; `BAND_FLOOR` / `HARD_STOP` / `MARKED_MAX` are pinned to `(45, 60, 63)`.
#37 deliberately kept the pre-#36 escape-hatch shape above 63 (marked → WARN, unmarked → FAIL) rather
than inventing a harder stop, **and the gate prints `UNRULED` there on purpose.** A pinned assertion in
`selftest_preflight` fails if a later session quietly fills the silence.

**The options, and what each costs.**

| Option | Cost | Note |
|---|---|---|
| Leave UNRULED, keep the pin | zero | Status quo. The pin is doing real work — it is what makes the silence legible instead of accidental. |
| Rule a hard stop above 63 | small edit + bites | Changes gate behaviour; needs a number that is his. |
| Rule that >63 is always a fork, never a fail | small edit + bites | Preserves the escape-hatch shape as a ruling rather than an inheritance. |

⚠ **ds-023's own text:** *"Do not resolve this by reasoning; it needs his words."* The standing
cautionary case is ds-023 itself — `>=45 → FAIL` was **a delegated agent's pick that stood six
sessions as though Dave had ruled it.** ⚠ **Cross-reference open 5:** the number is a `%` of an
unverified denominator.

---

## Open 2 — `ds-025`'s remedy

**Ledger:** `knowledge/_DS-IMPROVEMENTS.md` § ds-025. **State:** OPEN. Measurement done and *not in
dispute*; the remedy is a ruling because **it changes what the agent is allowed to assert.**

**The three unobservable numbers, as measured at #37.**

1. **THE BOOT.** Never measured in 36 sessions; carried as *"~17 of a ~20-pt floor."* Disk-resident
   half alone measures **17,810 tape / ~27,961 bill / ~14.0 pts** (`MEMORY.md` 4,517 · skill
   descriptions 5,684 · GM 1–120 6,253 · LS delta 1,356). **The harness half is not on disk and not
   reachable from any mount.** ⇒ every pre-flight in this repo has been priced on the low figure.
2. **`bill`.** `notes/_GAUGE-LOG.md` has **never contained a single `tape`/`bill` pair** — `grep -i
   bill` returns 0 across all sessions. `TAPE_TO_BILL = 1.57` is still the original **n=2** from #30.
   Not laziness: *"a session cannot read its own meter."*
3. **`fill`.** `_capture_gate.py`'s own header concedes it: *"it has no access to the token tally, and
   a guessed number wearing a gate's authority is the failure this programme exists to stop."*

**The three options, verbatim from the ledger — deliberately not chosen there, and not chosen here.**

| | Option | What it costs |
|---|---|---|
| **(a)** | **Dave-supplied inputs** — `fill` and `bill` become pasted observations, like the pace panel already is | Recurring cost **on Dave, every session**. Worked precedent: he pasted the panel at #37 and it priced the session honestly in one line. |
| **(b)** | **REFUSE rather than estimate** — an unobservable term is `UNKNOWN`, and `UNKNOWN` blocks | Gate work + bites. ⚠ Would make the gate refuse in a fresh sandbox, where `tiktoken` is absent — the failure mode #36 measured (silent `bytes/3.53` estimate, under-reporting by **414 tape**, failing UNSAFE). |
| **(c)** | **Publish the split** — keep estimating, but every stamp states which terms are MEASURED and which ESTIMATED | Stamp-format work. ⚠ The `size:` stamp lives **inside the compactable region** — #38 measured that writing the measurement pushed GM back over its block twice. *The report costs what it measures.* |

**Cheap step the ledger says holds regardless of the ruling:** the boot's disk half is measurable in
~15 lines and should be **re-measured per session rather than inherited** — GM-D9 calls the floor
*"a variable this programme shrinks"*, and nobody has ever watched it move.

⚠ **`_DS-IMPROVEMENTS.md` IS NOT REACHABLE BY RETRIEVAL** (GM §C·4 ⚠ RETRIEVAL GAP #2). This lane
opened it by path, as instructed. **A session searching for ds-023 or ds-025 finds nothing** — the
ledger the throttle's own opens live in is invisible to the doors. That is a known defect, not an
answer.

---

## Open 3 — The read chain's SCOPE

**Where:** `_capture_gate.py::read_chain_tk` + the M10 block. **State:** ADVISORY, agent-derived,
awaiting Dave.

**The question, precisely:** does **`DO THIS FIRST` join the priced chain (+3,415 tape)**, or stay
outside it in the header region?

**What has changed since, and it sharpens the question.** #38 measured the chain at **4,585 tape —
already OVER M10's 4,500 warn** before any addition, trimmed to ~4,400 by the wrap. So the chain is at
its warn line *without* `DO THIS FIRST`; adding it would put the chain at roughly **7,800 tape**,
past the 6,000 block-candidate.

**The numbers in play are all agent-derived and none are ruled:** chain warn **4,500** /
block-candidate **6,000** · corpus warn **36,000**. Plus **the 28,000 promotion trigger is DISARMED**,
deliberately — re-pointing at #33 would have satisfied it **by redefinition rather than achievement**,
and arming a 28,000 block against a ~4,400 chain is precisely the ds-024 shape: *an instrument nobody
reads, that can never fire.*

| Option | Cost | Consequence |
|---|---|---|
| `DO THIS FIRST` **joins** the chain | none to enact; **+3,415 tape** priced at every cold start | Honest if sessions do read it. Blows the current warn and block-candidate immediately. |
| It **stays out** | none | Chain stays ~4,400. ⚠ But then the queue is retrieval-only *by contract*, and a session that reads it has ignored the contract, not saved time. |
| Re-point M10's numbers as part of the cap ruling | folds into the conductor's fork | ⚠ Two agent-derived advisory numbers **cannot be promoted by an agent noticing they should be** — the brief's words. |

⚠ **This open and the conductor's cap fork are the same question asked twice.** The brief's own
starting-point sketch says so: *"if the chain is what a cold start pays, then M10 is the real
cold-start budget and should be the binding one."* **Offered as a starting point only** — this lane
does not endorse it.

---

## Open 4 — The #35 LS offloads

**State: RULED #35, ENACTMENT OWED. Four sessions untouched.** This is the one open that is **not
waiting on a decision** — Dave already ruled it; the work simply has not been done.

**Dave's frame, verbatim (#35):** *"the best balance of efficiency and it being as lossless as
possible… driven by code rather than prose as much as possible where appropriate."*

**What was ruled, and what remains:**

- ✅ **DONE:** the four GM offloads — `GM:C2b` `C3` `C4b` `C5` → `_GM-ARCHIVE.md`, moved at #35's wrap
  **under duress** (six trimming rounds, ending 54 tape short).
- ⬛ **OWED:** `LS:DEAD` · `LS:SPINOFFS` · `LS:TARGETS` → archives.
- ⬛ **OWED:** **`LS:LIFECYCLE` DE-MATERIALISE** — verified generated by
  `knowledge/_build_live_state.py` between `AUTO-DECISION-LIFECYCLE` markers from
  `knowledge/_decision-graph.json`. A materialised view of code-held truth; the one candidate where
  *"code rather than prose"* applies literally.
- ⬛ **OWED:** the matching **DEFERRED REGISTER rows** in GM §C·4.

**The register is a CONDITION, not a nicety** — ruling 3, verbatim in effect: for a queue, *never
cited* is ambiguous between **not needed** and **invisible**, and the reader cannot separate them.
**Offloading without a register optimises the record by quietly discarding decided work.**

**Cost.** Mechanical; runs through `_gm_move.py`. ⚠ **Both `_LIVE-STATE.md` and `_GM-ARCHIVE.md` are
in the conductor's serial set — no worker lane may do this.** ⚠ `_gm_move.py`'s `roll_2f` takes **no
anchor for the log** (that argument is what produced #27's prepend) but the archive **requires** one
and refuses to guess.

⚠ **#35's own verdict on why this matters, and it is the cap finding in embryo:** *"A size cap that
can only be met by the newest session cutting its own record is charging the wrong party."*

---

## Open 5 — The FLOATED degradation note

**File:** `notes/2026-07-29-context-degradation-research.md`, **339 lines**, `status: floated`,
written by a worker lane, receipt `notes/_receipts/2026-07-29-context-degradation-worker.md`.

⬛ **FIRM CONDITION, Dave #38, deferring it:** ***"we must return to it when we get this fixed."***
His #38 choice was **(3) LEAVE the FLOATED note unread**, surfaced into §C·4 rather than paid for —
one of three cuts, all three his, at a projected 55–64 close.

**Status of the reading.** ⚠ **Read by this lane today for the first time — the brief tasked Lane B
with surfacing it.** Its §0 exec summary and §5 fork are summarised here; **§1, §2, §3 and §4 have not
been read by any session and are not summarised.**

**What it contains, by its own account.**

1. **The paste Dave supplied is roughly half-sound.** Every *paper* cited is real. Every
   *Claude-model-specific threshold* ("Opus 5 safe to 350K", "Fable 5 safe to 500K", "750K danger
   zone") is **unsupported** — sourced to YouTube, Medium, Instagram and vendor blogs.
2. **★ Its headline finding:** the degradation literature measures in **absolute tokens** (32K/128K/
   200K); Apollo's throttle measures in **% of window**; the two are interchangeable only if the
   window is known, **and Apollo's window is a hardcoded guess** — verified this window at
   `_context_gauge.py:27`.
3. **Three further gauge defects:** wrong tokenizer, uncounted thinking tokens (kept-by-default on
   newer models, stripped on Haiku — so a `fill` number means different things per model), and the
   stale routing tier (verified: `MODEL-ROUTING.md:17`).
4. **Five platform capabilities it says Apollo is not using** — token-counting API, context awareness
   on Sonnet 5, task budgets, server-side compaction, cache diagnostics. ⚠ **Not verified by this lane.**
5. **⛔ Its own fork to Dave:** the ruled refill arithmetic — *"a fresh window buys ~78%, not 100%"* —
   is a %-of-200K figure. **If the window is larger, flushing is cheaper than Apollo prices it, not
   dearer**, and `RULED (c) — a new session is a refill, not a penalty` rests on that arithmetic.

**Its three ways forward, its own words, and it explicitly declines to choose:**

| | | Cost |
|---|---|---|
| **(a)** | **Measure first, judge nothing.** Run P1 — one throwaway Sonnet 5 session, one tool call, quote the injected `<system_warning>`. | *"~2 min, one session"* |
| **(b)** | **Measure and re-price in the same window** — restate the refill arithmetic with the real denominator. | *"Bigger job — a re-price of ruled process, not a fix."* |
| **(c)** | **Rule the band stays relative regardless.** *"Defensible! A % band is a throttle on the session, not a model-accuracy prediction."* | Small — but then holding two units apart becomes **deliberate and inscribed**, not an unexamined inheritance. |

⚠ **A FLOATED item is not authority.** The register is *floated*, not *standing* and not *canon*
([[memento-three-registers]]) — surface the contradiction, **never auto-promote the newer text**. This
receipt surfaces it and does nothing else with it.

⚠ **The brief's sharper point stands and is now evidenced:** the note has gone **unread across three
sessions while two of them re-derived findings it may already contain.**

---

## Open 6 — The mid-flight-handover state the gauge log lacks

**Home:** `GOOD-MORNING.md` §C·4·6 · `notes/_GAUGE-LOG.md` § META #38. **State:** RAISED at #38,
**not filled**, explicitly Dave's to mint.

**The gap.** `notes/_GAUGE-LOG.md`'s vocabulary is **`block` / `HOLE` / `ABSENT`**, and a session that
hands over **mid-flight fits none of them.** #37 ran an Amber spine-flush (capture-ritual STEP 1 only),
priced the full wrap at **~73%** against the 45–60 band, chose the cheaper tier rather than under-price
to fit, and handed to #38 **without ever closing.** So:

- not a **`block`** — no closed band exists to write;
- not a **`HOLE`** in the #36 sense — it left real measured numbers (~55% at the flush decision, ~73%
  priced, tape figures throughout its four commits);
- not **`ABSENT`** — we know exactly what happened.

**Dave's ruling at #38, verbatim in effect:** take **`HOLE #37` now**, ***"because it invents
nothing"***, and leave the fourth state to him.

| Option | Cost |
|---|---|
| Mint a fourth state (name + contract + gate vocabulary) | Ledger + `_capture_gate.py` + bites. ⚠ Serial set. |
| Leave `HOLE` doing double duty, inscribed as deliberate | Zero. But `HOLE` then means two different things, and the log's continuity guard cannot tell them apart. |
| Widen `HOLE`'s definition to cover handover | Small. ⚠ Changes the meaning of every past `HOLE` line retroactively. |

⚠ **The tempting move is the forbidden one:** writing a block with the measured fields and `UNKNOWN`
for the close **is a new state minted by an agent**. ds-023 is the standing cautionary case — *this is
the exact failure it records.*

⚠ **`HOLE #36` stands permanently** (neither half of its 2f split ran, so nothing is recoverable),
while **`HOLE #35` was discharged by addition** at #38 — it was true of the log and false of the world.
⇒ *Before declaring a HOLE, check the other half of the split.*

---

## What this lane did NOT do, and will not

- **Did not decide, order, or recommend.** The cross-cutting finding above is a **dependency observed
  between opens**, not a running order. Sequencing them is Dave's.
- **Did not touch the serial set.** `GOOD-MORNING.md` · `_LIVE-STATE.md` · both archives ·
  `_GAUGE-LOG.md` · `_MEMENTO-DECISIONS.md` · `_capture_gate.py` · `_memento-index.json` · git. All
  read-only this window. **No commit, no wrap, no inscription.**
- **Did not put the cap fork.** That is the conductor's, and it needs **Lane A's numbers**, which do
  not exist.
- **Did not verify** the five platform capabilities in the floated note's §4, or read its §1–§4.
- **Did not run the wrap gate**, so no size stamp is claimed here.

## Also flagged, not acted on

- **⚠ The working tree was dirty on arrival and it is not this lane's:** `knowledge/_gen_lanes.py` ·
  `knowledge/_validate_edge_extremity.py` · `knowledge/gen_showroom.py` modified and uncommitted at
  HEAD `1e76621`. Not in the serial set; **any lane inherits them.** Standing rule is reconcile every
  path, never blind `git add -A`.
- **⚠ A falsification test for the cap re-point was proposed by Dave in chat this session** and is
  **not recorded anywhere.** In his words: the next session *"either comes to you and asks you to fix
  that limit — or it quietly starts cutting text again to fit. If it cuts, nothing was fixed."*
  ⚠ **It is not in the ledger, not in GM, and not in the brief.** Recording it is a serial-set write
  and therefore the conductor's. This lane raises it so it is not lost.

## Verification log — claims checked against code this window, not against prose

| Claim | Checked at | Result |
|---|---|---|
| `DEFAULT_WINDOW` is hardcoded | `knowledge/_context_gauge.py:27` | ✅ `DEFAULT_WINDOW = 200_000` |
| `tape` = cl100k | `knowledge/_capture_gate.py:294` | ✅ confirmed |
| Routing default tier is stale | `MODEL-ROUTING.md:17` | ✅ names *"Opus 4.8 · high"* |
| No #39 lane receipts exist | `ls notes/_receipts/` | ✅ latest is 07-29 09:16, pre-#39 |
| HEAD is #38's red wrap | `git log -5` | ✅ `1e76621`, 07-29 11:45 |
| §C·4 fetched by retrieval, not scrolled | `_memento_search.py --fetch gm:C4` | ✅ returned `GOOD-MORNING.md:341` |
| `_DS-IMPROVEMENTS.md` opened by path | brief instruction, RETRIEVAL GAP #2 | ✅ path read; retrieval not attempted |

**Sources read (the full list, so the next session can price its own re-read):**
`GOOD-MORNING.md` §C·4 via `_memento_search.py --fetch gm:C4` ·
`knowledge/_DS-IMPROVEMENTS.md` § ds-023 + ds-025 (by path) ·
`notes/_MEMENTO-DECISIONS.md` § ★ #35 / #36 / #38 ·
`notes/2026-07-29-context-degradation-research.md` §0 + §5 + heading index only ·
`notes/_briefs/2026-07-29-cap-repoint-and-lane-divvy-brief.md` ·
`knowledge/_capture_gate.py` (`SIZE_BUDGET_TK`, M7/M8/M10 blocks) · `knowledge/_context_gauge.py:27` ·
`MODEL-ROUTING.md:17`.
