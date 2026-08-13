# PROPOSAL — a better effort gauge for the dashboard priority score

**Status: PROPOSAL. Nothing here is ruled, nothing is in the store, no code changed.**
Written 2026-08-13 (#168) in response to Dave's floated note: *"there must be a better way to
gauge effort, this seems quite arbitrary, can we explore this."* Dave ratifies; only then does
anything land.

---

## 1. What is actually there today (measured, not recalled)

**The arbitrary thing, quoted.** `knowledge/gen_dashboard.py:331`:

```python
sub["effort"] = max(0.0, min(1.0, 1.0 - (len(body) / 1200.0)))
```

…declared at `gen_dashboard.py:227-230` as criterion `("effort", "Effort (inverse)", 0.15, …)`
with the source string *"the item's OPTIONAL `effort` (S/M/L) where present — otherwise
**PROXY ONLY**: the length of the item's `body`."*

Three separate faults, and they are different faults:

1. **The unit is bytes of prose.** Bytes of prose is not a measurement of work
   [[measure-dont-convert-units]] — a COUNT is not a MEASUREMENT unless the unit is the thing
   you claim to be measuring. It is not even a proxy with a sign you can defend: it penalises
   the well-documented item and rewards the one-line stub.
2. **The denominator `1200.0` is a free parameter with no provenance.** No comment, no ruling,
   no measurement behind it. Measured against the live store: bodies run 68 → 964 characters
   (n=37), so *every* item lands in 0.20–0.94 and the term mostly encodes "how much did the
   scribe type."
3. **It is load-bearing at 0.15 of 1.00** and it fires on **37/37 items** — the real `effort`
   field is ABSENT on every item, so the proxy branch is what actually runs, every build.

**The honest machinery that is already right, and should be kept in every option below.**
The proxy already declares itself: `gen_dashboard.py:328-330` appends a named MISSING INPUT
(*"the item has no `effort` field — the score reads the byte-length of its body as a PROXY,
which measures the prose, not the work"*) and the item is flagged LOW CONFIDENCE. The score is
labelled PROPOSAL on every surface, is regenerated at build, and is never written back
(`gen_dashboard.py:195-209`). ⛔ **No option here may weaken any of that.**

**The gated field that exists and is empty.** `knowledge/_state.py:121-138` defines `deadline`
(ISO date) and `EFFORT = "effort"` (one of `S`/`M`/`L`) as OPTIONAL presence-gated fields, with
the comment *"⛔ NO AGENT MAY AUTHOR A VALUE… authoring an effort is grading one's own homework
and then reading it back."* Validation at `_state.py:341-359`, both-direction selftest at
`_state.py:586-601`. Measured: **0 of 37 items carry `effort`.** Ruling `s165-D5` records the
schema+gate as ENACTED and the value half as *"OPEN and Dave's."*

### Signals that provably exist in this repo (and the ones that do not)

| Signal | Where, proven | Unit | Joins to a store item? |
|---|---|---|---|
| `effort` S/M/L | `_state.py:138`, gated, selftested | ordinal T-shirt | **yes**, by construction — but 0/37 authored |
| item `body` length | `_state.json` | characters | yes — and it is the thing being retired |
| `opened` session no. | `_state.json`, values `{0, 86, 161}` | session number | yes, but 18/37 are `0` = UNKNOWN |
| `links` | `_state.json` | edges | **no — 0/37 populated** (`s165-D4` backfill still Dave's) |
| `governs` on rulings | `_rulings.json`, **138/138 entries carry it**, e.g. `s167-D1` → 4 token JSON paths | file paths | **weakly** — only 5 item ids (`G1 G3 G7 G8 G18`) appear anywhere in rulings text |
| session job price + closed band | `notes/_GAUGE-LOG.md`, **147 session blocks, 141 post-mortems, 21 blocks priced in real tokens** (`job 118,000`, `job 95,651`, `job 56,309`…) | **real Claude tokens** (`count_tokens`, unit ruled at `_gauge_tokens.py` docstring) | **no** — keyed by SESSION, not by item |
| git churn per path | `git log --numstat`, 724 commits, session-numbered subjects | files / lines / commits | **no** — `home` collapses all 37 items onto 2 files (19× `GOOD-MORNING.md`, 17× `_GOVERNING-RECORDS.md`) |
| `_SESSIONS.jsonl` | exists | events | **no** — 7 lines total, #89 only. Dead. |

**⚠ Do not invent the two missing joins.** There is no item→file map and no item→session map in
this repo. Any option that needs one must BUILD it as a gated, Dave-authored field, and must say
so in its price. That is the whole cost difference between the options below.

### ⚠ A carried premise that is measurably FALSE (found while doing this)

`_PROPOSAL-links-backfill-2026-08-13-v1.md` §"Two limits" states: *"The store's `body` is
truncated at 400 characters — measured: 7 of 37 items sit exactly on the cap."* Re-measured
against the live store today: **no body is 400 characters; 7 bodies EXCEED 400** (481, 500, 623,
678, 695, 956, 964 — `W-10 W-0b W-0c W-16 W-0d W-08 W-14`), and `grep 400 knowledge/_state.py`
returns nothing. The "7" is the count of items ABOVE 400, read as items ON a cap that does not
exist. The same claim is carried in MEMORY. It does not change any option here, but it is a
premise that has been quoted twice and should be corrected rather than inherited
[[premise-ages-faster-than-rule]]. ⛔ **Not fixed by me — this proposal touches no file but itself.**

---

## 2. The options

Costs are in **real Claude tokens of build window**, and they are **planning estimates, not
measurements** [[planning-estimate-is-not-a-measurement]] — the standard that applies is "what a
comparable wired-and-selftested change cost in `_GAUGE-LOG`", not a measurement of this work.

### Option A — THE NULL. Drop the effort criterion entirely; renormalise to five.

Delete the `effort` tuple from `CRITERIA`; the remaining five re-weight to sum 1.00 (unlock .35 /
rot .24 / deadline .18 / risk .12 / load .11, or whatever Dave rules). No new field, no new data.

- **Signal + UNIT:** none. The score stops claiming to know effort.
- **Data source:** n/a.
- **Cost to build:** ~4–7K. One tuple removed, `WEIGHTS_SUM` assertion still 1.0, the weights
  table on the page re-renders itself from `CRITERIA`.
- **Failure modes:** a two-minute job and a two-session job rank identically on everything else;
  the page silently stops answering a question Dave asked it. Renormalising redistributes 0.15
  into criteria that were never sized to carry it — the other five weights become *different
  numbers than the ones Dave ratified* without a ruling saying so.

### Option B — HAND-AUTHORED T-SHIRT. Keep the gated `effort` S/M/L; Dave writes the values.

Zero code. Dave writes `"effort": "S"|"M"|"L"` on the items he cares about. The real-input branch
(`gen_dashboard.py:315-316`, `EFFORT_SCORE = {"S":1.0,"M":0.5,"L":0.0}`) is already built,
already gated, already selftested — it has simply never had a value to read.

- **Signal + UNIT:** Dave's judgement, ordinal (three rungs, no interval meaning).
- **Data source:** `_state.py:138` + `_state.json` (proven: the gate refuses lowercase, ints and
  free text — selftest `_state.py:586-601`).
- **Cost to build:** **0 tokens of build.** Cost is Dave's attention: ~37 judgements, or fewer if
  partial (absent stays legal and keeps the LOW-CONFIDENCE flag).
- **Failure modes:** the rungs have **no declared standard** — is "S" an hour, a lane, or a
  session? Two items marked M by different readings are not comparable. It rots: an M scoped at
  #120 is an L by #168 and nothing re-asks. Partial authoring makes the ranking a mix of two
  populations (judged vs proxied) that the score cannot tell apart.

### Option C — TOKEN-BANDED EFFORT, calibrated against `_GAUGE-LOG`. ★ RECOMMENDED

Replace the S/M/L enum's *meaning* (not necessarily its spelling) with a band whose rungs are
**defined in real Claude tokens of job window**, the unit this project already rules and measures.
Dave still authors — the change is that the rung now has a stated standard he is picking against.

Proposed rungs, anchored to the 21 token-priced session blocks in `notes/_GAUGE-LOG.md`
(`job 30,000` … `job 118,000`; anchors to be RE-DERIVED from the log at build, not typed in):

| rung | means | anchor from the log |
|---|---|---|
| `S` | fits beside other work in one window | ≲ 20K job tokens |
| `M` | is the window's job | ~20–60K |
| `L` | does not fit one window — needs a lane or a sub | ≳ 60K |

The dashboard prints the rung definition next to the weights table, so the standard travels with
the number. `EFFORT_SCORE` mapping is unchanged.

- **Signal + UNIT:** Dave's estimate, expressed in **real Claude tokens of job window** (the unit
  ruled in `knowledge/_gauge_tokens.py`: *"real Claude tokens, from `client.messages.count_tokens()`"*).
- **Data source proven to exist:** `notes/_GAUGE-LOG.md` — 147 `#### ` session blocks, 141
  post-mortems, 21 carrying an explicit token job price (`grep -o "job [0-9][0-9,]\{3,\}"` → 21).
  The anchors are derived from measured history, not invented.
- **Cost to build:** ~12–18K. A small `--anchors` reader over `_GAUGE-LOG.md` that recomputes the
  three band edges from the priced blocks (report-only), plus the rung-definition block on the
  page, plus a selftest asserting the reader refuses a log block it cannot parse
  [[a-crash-is-not-a-fail]]. **No schema change** — the existing gate already accepts S/M/L.
- **Failure modes:** it is still an ESTIMATE and must never be printed as a measurement — the page
  must say *estimated in tokens*, not *costs*. The 21 priced blocks are a thin and biased corpus
  (they are the sessions that remembered to price themselves; several recent wraps record
  ⛔ UNMEASURED). Job price is per-SESSION, so an anchor derived from it prices a *window's work*,
  which is coarser than an item. Band edges will drift as the log grows — that is a feature only
  if the drift is visible, so the page must print the edge values and the n it derived them from.

### Option D — DERIVED BLAST RADIUS. New gated `touches` path array + git churn.

Add an OPTIONAL `touches: [path, …]` field to store items, same presence-gate shape as
`priority_override`/`deadline`/`effort`. An effort probe then measures, for the union of an item's
paths: **number of files**, and **lines changed in the last N session commits** (`git log
--numstat`). Big surface + hot history ⇒ bigger job.

- **Signal + UNIT:** files (count) and changed lines (count) over a named window of sessions.
- **Data source proven to exist:** git — 724 commits, session-numbered subjects, `--numstat`
  works (verified: `#167` touched `GOOD-MORNING.md 32/30`, `_CHAIN.md 41/35`, one new history
  file 152/0). Precedent for the path-list shape: **`governs` on 138/138 rulings** already carries
  exactly this kind of array (`s165-D3` → `knowledge/_build_all.py (ROUTE_ROWS: …)`).
- **Cost to build:** ~35–50K, plus Dave's authoring. Schema + both-direction gate + selftest
  (~15K, mirroring `s165-D5`), the churn probe + its own selftest (~12K), wiring + the page
  column (~8K) — **and the `touches` values are 37 more Dave-authored judgements**, because an
  agent that writes the paths it then scores itself against has closed the loop
  (the exact objection `s165-D4` raises about `links`).
- **Failure modes:** churn measures *where change has been*, not where it is *owed* — a
  well-settled hot file scores as expensive. Paths rot as the tree moves. `governs` strings are
  **not clean paths** (they carry parenthetical scope: `"knowledge/_build_all.py (ROUTE_ROWS…)"`),
  so any reuse of them needs a parser, and a parser that guesses is the `no-gate-parses-the-artefact`
  class. Worst case: an expensive instrument whose input is as unauthored as `links` is today —
  a second empty field flagging LOW CONFIDENCE forever.

### Option E — PRECEDENT PRICING from ruling families. ⛔ NOT VIABLE, priced to close it.

*Idea:* price an item from how many sessions its ruling family has already consumed
(unit: sessions). *Killed by measurement:* the join does not exist. Of 37 store items, exactly
**5** ids (`G1 G3 G7 G8 G18`) appear anywhere in the 138-entry `_rulings.json` corpus, and
`_SESSIONS.jsonl` holds 7 lines covering one session. Building the join is Option D's cost with a
worse signal. **Recorded so it is not re-proposed.**

---

## 3. Recommendation

**Take Option C, and take Option A's behaviour as its companion — not as an alternative.**

- **C is the only option that changes the KIND of number.** Every other live option leaves effort
  as an ungrounded ordinal or a prose count. C names a unit this project already rules, measures,
  and stores history for; it turns "S" from a feeling into a pick against a stated standard, and
  it costs less than a fifth of Option D.
- **A's behaviour is the required default, because 0/37 items carry a value today.** Concretely:
  *when `effort` is absent, the criterion does not fire at all* — the item is scored on the
  remaining criteria, renormalised, and flagged. That is strictly better than today's
  body-length branch and strictly more honest than scoring an absent input as 0.0. It is the
  same discipline `_deadline_score` already uses: `None` means "no usable field", *never* 0.0
  (`gen_dashboard.py:252-258`).
- **B alone is not enough** and should not be taken on its own: it is C without the standard, and
  an unstandardised rung is the arbitrariness Dave objected to, relocated from the code into his
  own head.
- **D is the right shape and the wrong session.** Revisit it only after `links` (`s165-D4`) has
  actually been ratified — if that field is still empty, a second Dave-authored array will be too.

**What I would NOT do:** keep the 1200-byte proxy while adding anything. The proxy and the real
input must not blend — `gen_dashboard.py:311-313` already rules that, and it is right: a blend
lets the prose keep a vote in a criterion Dave has answered, and makes the score unattributable.

---

## 4. Consequences and pitfalls (replayed, per standing rule)

1. **The ranking WILL move, on every option including the null.** Effort is 0.15 and currently
   fires on all 37 items, so any change here re-orders the dashboard. Home pointers into that
   order rot [[home-pointer-rot-class]]: at #167 the PROPOSAL ranking already moved 7 rows.
   ⇒ Whichever option lands, the enacting session must print a **before/after rank diff**, not
   just a green build.
2. **Renormalising weights silently changes numbers Dave ratified.** The five surviving weights
   would no longer be the values on the page he approved. ⇒ The new weights are a RULING, printed
   in the weights table with their provenance — not a division done in code.
3. **A calibrated band is still an estimate.** If the page ever prints C's rungs without the word
   *estimated*, the enactment register gets a CLAIMED that is not true
   [[enactment-register-adr-0016]]. ⇒ The rung block must name the standard and the n it was
   derived from, every build.
4. **⛔ No agent authors an effort value.** `_state.py:129-131` already forbids it and the gate
   enforces the enum, not the authorship. The gate cannot tell Dave's `"M"` from mine. ⇒ The
   authorship rule stays a written rule, and any enacting session must state, in the wrap, that it
   wrote zero values — the same declaration `s165-D5` made.
5. **A new anchor reader is an instrument with no consumer risk.** A `--anchors` reader that
   nothing runs cannot fail [[instrument-without-a-consumer]]. ⇒ It must be wired into
   `_build_all.py`'s dashboard step and must have a both-direction selftest (a planted unparseable
   log block must REFUSE), or it should not be built.
6. **A thin corpus can look precise.** 21 priced blocks out of 147 is a 14% sample, self-selected.
   Printing edges to the nearest thousand implies a precision the corpus does not have.
   ⇒ Round the rung edges hard, print the n, and never present a band edge as measured.
7. **The `_GAUGE-LOG` block grammar is gated.** `_build_memento_index.py` REFUSES any block not in
   the two legal forms (recorded in the log's own header, ds-024). ⇒ An anchors reader must parse
   only, never write, and must fail LOUD and NAMED on a block it cannot read — a crash is not a
   fail [[a-crash-is-not-a-fail]].
8. **Doing nothing has a cost too.** Every build between now and a ruling ships a 0.15-weight
   criterion that measures typing. It is flagged, but a flagged wrong number still sets the order
   of the page Dave reads first.

---

## 5. What is asked of Dave

1. Rule the option (A / B / C / D — E is closed).
2. If C: confirm or move the three rung edges, and confirm the rung spelling stays `S`/`M`/`L`
   (keeping it means **zero schema change** and the existing gate + selftest carry over intact).
3. Confirm the companion behaviour: **absent `effort` ⇒ criterion drops and renormalises**,
   replacing the body-length proxy outright.
4. Separately: the `_state.json` "400-char truncation" premise in §1 is measurably false and is
   carried in two places. Say whether it gets corrected in-place or logged.
