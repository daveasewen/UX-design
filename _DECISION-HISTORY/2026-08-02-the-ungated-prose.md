# The ungated prose — #83, and the rule that stopped at a file extension

provenance: 83 · 2026-08-02
status: observed

*Spine: `_LIVE-STATE.md` ⏱ #83 delta · ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #83 ·
predecessor: `_DECISION-HISTORY/2026-08-02-the-real-tier.md` (#82) · this session enacts items
(a) and (c) of #82's own carryover, named at `GOOD-MORNING.md`'s #83-opener banner and
`_LIVE-STATE.md` ⏱ #82 delta.*

---

## 1. The lane, ruled at the opener

Dave's opener: *"good morning, lets get this nailed."* The lane was already drawn by #82's own
wrap — seven items forked forward, (a) through (g) — and he narrowed it to two: **(a)** the
runbook's retired unit, still teaching the superseded tape/bill system at
`_RUNBOOK-context-gauge.md:463–505`, and **(c)** wiring `_checkin.py` — the very instrument that
had just decided when to wrap #82 — to the real tier #82 built. He ruled **ONE window, with
delegation to subagents**, rather than #82's solo shape. [[delegation-inversion-ruled]]: subs by
default, delegate what a gate can check, keep the ruling and the ratified record in-window.

## 2. The finding that reframed the job, before either item was touched

Two probes ran before a line changed. The load-bearing one: `unit_vocabulary_audit()`
(`knowledge/_capture_gate.py:524`) — the ds-021 (C) gate #81 built and #82 hardened into an AST
check — walks `knowledge/` like this (:544–545):

```
for fn in sorted(os.listdir(kdir)):
    if not fn.endswith(".py"):
        continue
```

It reads no `.md` file, ever. That is not a bug — the gate is correctly scoped to what it exists
to catch, an unregistered *counting site*, and counting sites are Python. But it had produced an
asymmetry nobody had named:

- Item (c), `_checkin.py`, was pinned `estimate-only` in `MEASURERS` (:485). The gate NAMED it as
  a declared gap on every single run since #81 — honest, visible, WARNING by name, every time.
- Item (a), the runbook, taught a retired unit *and* a retired percentage band in the section
  `GOOD-MORNING.md` itself calls **"the band table's ONLY copy"** (GM:93 — *"Throttle + pace
  canon → `_RUNBOOK-context-gauge.md` § ★ Half 0b … — the band table's ONLY copy; grep it, never
  recall it"*) — and no gate could see it, because the rule stopped at the file extension.

The gated half stayed honest. The ungated half rotted silently, and got *worse* underneath its own
fix: #82 wired the real counter, so by this session's opener the runbook was teaching a retired
unit **and** a superseded instrument at the same time, with nothing positioned to flag either.

⇒ ★★ **The lesson, and it is this dossier's spine: a rule is only as wide as its gate's glob.**
[[gate-glob-scope-rule]] — ds-021 (C)'s rule ("every counting site declares its tier") was
enforced on `.py` and stopped dead at `.md`. But the `.md` is the file a cold session actually
reads to *learn* the unit, before it ever calls a counting site. A gate that watches only the code
cannot watch the prose that explains the code, and unwatched prose is exactly where staleness is
free — nothing runs it, so nothing can catch it drifting. [[read-chain-is-where-staleness-is-free]]

## 3. What the two workers found that their own briefs got wrong

Both subagents were told to report a false premise loudly rather than route around it quietly.
Both did — one about a file the conductor had waved through, one about a gate built the session
before.

**Worker A — the runbook, and a provenance error with nothing to do with the runbook itself.**
Found the conductor's brief wrong to call `_gauge_tokens.py:51–83` "already correct." The
*numbers* had not moved — 160,000 / 200,000 / 256,000 stood. The *authority column* was wrong,
and had been for 25 sessions:

- `BUDGET_WORKING` (200,000) was relabelled **DAVE'S → SOURCED** at **#58b**, on his own words:
  *"the 200K and 256K come from established research, its been worked out already."*
- `BUDGET_AMBER` (160,000) was relabelled **DERIVED → PICKED** at **#59** — 80% of working is a
  round fraction, not a derivation, and calling a pick "derived" makes it immune to the very rule
  meant to catch that class of error.

Both corrections had sat in `_gauge_tokens.py:63–83` the whole time. Neither had reached
`GOOD-MORNING.md`'s own band clause (:9), which still read *"working 200,000 (DAVE'S)"* — so
every cold session since #58b was handed the wrong provenance first, in the read chain, before it
read anything else. [[read-chain-is-where-staleness-is-free]], a second file, the same shape.

Worker A also found a *third*, unruled number pair sitting in the runbook's own prose:
*"Triggering at 70%, not 95%"* — matching neither the retired 45/60/63 band nor #56's
160,000/200,000/256,000 replacement, with no ruling for it anywhere. It did **not** delete the
line. It fenced it as flagged drift — *"no ruling for 70/95 was found while fixing this file
(2026-08-02); treated as drift, not a citation"* — and corrected the paragraph
(`:682–688`) to the ratified stop-line rule. Recorded here as the right handling of an orphaned
number: name it and its absence of provenance, don't silently absorb it, and don't silently
delete it either.

**Worker B — `_checkin.py`, and a coverage gap in machinery #82 had already trusted.** Found that
a mutation making `_checkin.py` *swallow* `gauge.MeasurementRefused` — catching the refusal and
quietly returning an estimate instead of propagating it — stays **GREEN** against
`_produces_real_tier()`, the AST gate #82 built to stop a registry entry lying about its own code
(`knowledge/_capture_gate.py:446–478`). The reason is exactly what that gate checks and no more:
a `return` whose value is a **tuple ending in `'real'`** proves that shape *exists* somewhere in
the source — `measure_real()`'s success path still has it (`_checkin.py:116`) — not that every
path which *could* fail actually reaches it undegraded. The check is a claim about structure; a
swallow is a claim about behaviour, and the two are different claims. Not fixed this session — a
genuine coverage gap in existing #82 machinery, declared rather than patched over or hidden.
[[a-new-tier-silently-bypasses-its-tests]]: a healthy suite is not evidence its tests are running,
and this is that same family, found one layer further out than #82 left it.

## 4. What was built

**(a) The runbook — 622 → 726 lines** (`git show HEAD:knowledge/_RUNBOOK-context-gauge.md | wc -l`
against the file on disk now). Not a rewrite-in-place: the retired tape/bill duality and the
retired 45/60/63 percentage band are **fenced as history, not deleted** — a new section, `### ⬛
RETIRED UNITS AND BANDS — HISTORY, NOT INSTRUCTION` (:526), states plainly *"This section exists
so Dave's rulings are not lost — it is not a second place to read current numbers from"* and
points back to the one live table. The ruling that built tape/bill is Dave's (#31/#34), and the
record of why the unit later changed is load-bearing — deleting it would have been the same false
economy #82's dossier refused when it declined to re-denominate history (§6 there: *"they need a
labelled unit, never a new number"*). What had been several separate restatements of the
percentage band collapsed to the one at `### ★★ THE UNIT AND THE BUDGET` (:29, RULED #56);
everything downstream of it — the trigger section, the authoring-time stamp, `ds-025`'s floor —
now reads that table instead of repeating its own copy of it.

**(c) `_checkin.py` — wired to the real tier in one call.** `measure_real()` (:97–117) calls
`gauge.count()` once on the whole concatenated conversation-half blob and returns `(n, 'real')`.
The naive per-record wiring was explicitly *ruled out*, not merely avoided: #82 had already
measured that shape at **232 API round-trips against the sandbox's 45s call wall** on a live
transcript, and `count()` is content-hash cached, so the one-call shape costs nothing on a re-run
of an unchanged transcript. `gauge.MeasurementRefused` is deliberately not caught inside
`measure_real()` itself (:109–112 — *"catching it and returning an estimate instead would be
exactly the ds-025 defect this module refuses to commit"*); it propagates to `main()`, which exits
named rather than downgrading (see Worker B's finding, §3, for what that design still leaves
unverified). The old cl100k per-type breakdown survives as a labelled sideband, explicitly marked
as not summing to the headline and never scaled toward it — kept for SHAPE only, per D1's own rule
that converting a proxy into a measurement's clothes is #54's defect.

## 5. Two corrections at source, made by the conductor, not delegated

**`GOOD-MORNING.md`'s own provenance line.** The band clause (:9) read *"working 200,000
(DAVE'S)"* for 25 sessions after Dave had already corrected it in code. Fixed to *"amber 160,000
(PICKED) · working 200,000 (SOURCED) · hard 256,000 (SOURCED)"*, with the correction dated and
quoted at source rather than silently swapped — a silent swap would have been exactly the class of
error being fixed.

**`_gen_chain.py`'s hard-coded unit word.** The fixed-point writer called `cg.measure_tokens(...)`
and discarded index `[1]`, the method, then hard-coded the literal `tape` into every banner and
footer string the generator produces. Since #82-D1 that number *is* real, so the reader was
publishing the retired unit's name for the same figure `_CHAIN.md`'s own footer publishes as
`real` — the same count, two units, two files, in the one artefact every cold session reads first.
Fixed by making the method travel *with* the number (`measured, how = cg.measure_tokens(text)`,
:264) — **not** by hard-coding the word `'real'` in its place, which would have claimed a tier the
offline fallback cannot deliver. The old docstring had flagged the discard; nobody had flagged
that the *label*, not only the omission, was a lie.

## 6. The cost, stated honestly

The header correction alone grew the read chain: `_CHAIN.md`'s own fixed-point footer moved
**11,032 → 11,396 real, +364** (`git diff _CHAIN.md`, the closing sentence). `GOOD-MORNING.md`'s
own size stamp moved the same +364, 43,555 → 43,919. That growth is the conductor's own — the
price of stating the correction in full at source rather than a silent one-line swap — and it is
attributed here rather than folded into the session's other numbers. It is paid by every future
cold session that reads the chain.

## 7. What is still open

**Finding 3 stands unresolved: the prose is still ungated.** The runbook rewrite this session is
not itself protected by anything — `unit_vocabulary_audit()` still walks only `.py` files, so a
future edit could reintroduce a stale band or a stale unit word into
`_RUNBOOK-context-gauge.md` and nothing would fail, exactly as happened between #56 and this
session. That is the item for #84, and unlike most items on this project's owed list it has teeth:
the mechanism that let this session's own finding happen is still standing, unchanged, at the
close of the session that found it.

Also carried forward, untouched this session: **(b)** headroom, still unmeasured (78 B free, #80)
· **(d)** seed the trigger index further (9 rulings ≠ coverage, and this session minted no new
entry) · **(e)** `_measure_tokenizer.py` still 0 consumers · **(f)** §C over its warn cap
(191 > 150) · **(g)** the six `_decision-graph.json` edge types, unruled since #71 · and Worker
B's coverage gap in `_produces_real_tier()` (§3, above), which has no ticket of its own yet beyond
this record.

## 8. How the session ended

`_checkin.py` — the instrument this session wired — read **162,251 real** on the conversation
half, **~194,000 with boot** priced in. Past amber (160,000), against Dave's working line
(200,000). The wrap was put to him as a declared crossing rather than smoothed into a band label,
and he ruled: **"wrap tight, declare the crossing."**

The small irony worth recording plainly: the instrument built *this* session is the one that
called time on it — the same shape as #82, where `_checkin.py`'s old cl100k reading decided when
to wrap the session that made it obsolete, except this time the reading that stopped the session
was the correct unit, doing precisely the job item (c) built it to do.

---

**Both-way links.** Ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #83 (the rulings, in full, with
why). Spine: `_LIVE-STATE.md` ⏱ #83 delta, ending `History:
_DECISION-HISTORY/2026-08-02-the-ungated-prose.md` per this archive's rule 2. Predecessor:
`_DECISION-HISTORY/2026-08-02-the-real-tier.md` (#82 — the enactment this session's two items
were carried forward from). Files touched: `knowledge/_RUNBOOK-context-gauge.md` ·
`knowledge/_checkin.py` · `knowledge/_capture_gate.py` (the `MEASURERS` entry for `_checkin.py`
only) · `knowledge/_gen_chain.py` · `GOOD-MORNING.md` · `_CHAIN.md`.
