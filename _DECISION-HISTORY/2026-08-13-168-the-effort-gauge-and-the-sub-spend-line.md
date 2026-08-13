# #168 — the effort gauge, the sub-spend line, and the rung whose light legs are placeholders

provenance: 168 · 2026-08-13
status: observed

*Narrative dossier (capture-ritual step 1b) for session #168 — OPUS conductor + ELEVEN OPUS subs +
this OPUS wrap sub, Dave live, on a day he declared a **quota rinse** (panel at the opener: session
5% · weekly 72% · Fable 91%, resetting Thu 10:59PM). **Four rulings, all Dave's: `s168-D1` …
`s168-D4`.** The terse WHAT lives in `knowledge/_rulings.json`, the ★ LATEST banner of
`GOOD-MORNING.md` and the ⏱ LATEST delta of `_LIVE-STATE.md`; this file holds the WHY and HOW,
including the parts that did not resolve.*

---

## 1. The dashboard review, and the proxy that was never a measurement

#167 closed by declaring a consequence up front: repairing the 400-char `_state.json` body cap moved
the dashboard's PROPOSAL ranking for seven rows, because the priority score's **effort criterion was
reading body LENGTH**. Dave reviewed the dashboard and ruled three things in one export (`s168-D1`):

- **DC1 — `tooltip.tip` is closed.** The carried "one unruled row" of `s142-D1` had already been
  settled by `s162-D1`, and there is **no store row for it**: nothing is owed. This is the
  [[premise-ages-faster-than-rule]] shape again, and the repair was made **by ADDITION** — a
  `superseded_note_s168_D1` key was added to the `s142-D1` entry and its original
  `"open": "tooltip.tip unruled…"` text was left **untouched**. A warning label may not be trimmed
  to tidy a record; it may only be annotated.
- **DC2 — the length proxy is removed.** Body length was standing in for effort and was never a
  measure of it: a long derivation is not an expensive job. The remaining criterion ratios were
  **renormalised proportionally and computed at generation, never typed**, so Dave's declared
  weightings survive the removal without anyone re-authoring them.
- **DC3 — the moved ranking is accepted as PROPOSAL SHAPE.** Not row by row. `s165-D2` makes the
  score a proposal regenerated every build and never written back, so what his eye ratified is the
  shape of the instrument, not any position in it.

★ **The finding worth keeping: a proxy is a measurement's costume.** It passed review for three
sessions because it produced a plausible ORDER, and an order looks like knowledge even when its
input is unrelated to the quantity named on the axis.

## 2. What replaces it — and why the edges are declared DERIVED

Option C of `notes/_PROPOSAL-effort-gauge-2026-08-13-v1.md` was put to Dave with its alternatives;
he ruled it (`s168-D2`, *"this sounds good"*): a **token-banded effort gauge**, rungs S/M/L, unit =
**real Claude tokens of the JOB WINDOW**, with **boot and wrap excluded** and — the clause that
matters — **delegated sub spend excluded**, because a sub is nearly free in this window's FILL and
5–10× in the weekly QUOTA [[budget-vs-quota-vocabulary]]. Mixing the two would produce a gauge whose
unit changes with the delegation shape.

The band edges — currently **45K / 85K at n=21** — are **DERIVED AT BUILD from gauge-log quartiles**.
★ **The ruled thing is the derivation method, not the two numbers**, and that distinction is written
into the ruling on purpose: an edge that moves as the corpus grows is the design working, and a
future session that "corrects" a moved edge back to 45K/85K would be enforcing a stale measurement
against the mechanism that was ruled. The companion clause matches the standing refusal discipline:
**an absent effort value drops the criterion and renormalises** — absence is never defaulted into a
number [[feedback-measuring-tool-must-not-guess]]. **All 37 item values remain Dave's; none was
authored.** Receipts: `_state.py --selftest` 46 green, `gen_dashboard.py --selftest` 23 green.

## 3. The sub-spend line, and a gate whose real job is containment

If sub spend is excluded from the gauge, the obvious next question is where it goes instead. Two
options were put to Dave; he took both halves and picked the second shape (`s168-D3`, *"I like
both… lets do option 2"*):

**(a) An optional gauge-log line**, `subs <N> tokens (n=<count>)`. Absent is legal and **never
defaulted** — there is no zero-line and no "n/a". The interesting constraint is the ban on the word
`job` anywhere on that line. It is **containment, not style**: `gen_dashboard.py`'s `_JOB_RE`
(`\bjob <number>\b`) sweeps the whole of `notes/_GAUGE-LOG.md`, and every match becomes a datapoint
in the corpus **the S/M/L band edges above are derived from**. A subs line spelled with `job` would
move a band edge with **no error, no crash and no reader** — precisely the
[[instrument-without-a-consumer]] failure mode, inverted: not an instrument nobody runs, but an
input nobody knows is an input. The guard (`_capture_gate.py::gauge_log_subs_line`, 12 arms) was
proven against the real `_JOB_RE`, not against a copy of it.

⚠ **`SUBS_LINE_BLOCKING=True` is a DECLARED CHOICE, not part of the ruling.** Dave ruled the line
and the gate; blocking was chosen by the build because the damage it prevents is invisible, and a
downgrade is his. Saying otherwise would launder a build decision into a ruling.

**(b) Effort-switch agent definitions** — `.claude/agents/opus-deep.md` (`effort: max`) and
`opus-fast.md` (`effort: low`). ⛔ **They were not registered mid-session**, so nothing this session
ran under them; **first live use is #169**, and that is recorded rather than implied.

## 4. The graphic-strength rung — and the honest part

Dave's words, verbatim: *"we already have red and green values for text in light mode, can we use
those… choose a new amber and blue. I'm happy with the current colours in dark mode."* That is
`s168-D4`: the `rag/*-graphic` **light** legs take the already-ruled text values — error `#DA1A00`
(`s151-D1`), success `#137F3C` (`s155-D1` via `s144-D1`) — and **all four dark legs stay as built**
(`#CC4333` / `#C58900` / `#4A9568` / `#2674DC`). The ruling **subsumes and ratifies 82-B**, his
graphic-strength-tier pick from `_PROPOSAL-148-reds-2026-08-13-v1.md`, pending his eye on specimen
v2. The rung NAME `-graphic` is a **declared default, unratified**.

⛔ **And the part that must not be smoothed:** the light **amber `#C58900`** and light **blue
`#306EC6`** now standing in `knowledge/canon/canon.css` are **ENACTED-PENDING-EYE PLACEHOLDERS**
written by the build lane so the tier renders. They are **not Dave's picks and not ruled values** —
they are the very things `reviews/REVIEW-168-graphic-amber-blue-picker-v1.html` exists to replace.
A placeholder that looks like a value in a token file is how an unruled colour becomes canon by
attrition, so it is declared here, on the ruling, and in the residual.

## 5. Three things measured, one thing not

- **#148 reds 36 / 45 / 51 measured GREEN and mutation-proven biting.** ⚠ The **closure provenance
  is UNPROVEN** — they may be collateral from other work rather than closed by intent, and the
  honest form is to say so rather than claim three closures.
- **Red 82 is consumed** via the graphic-strength tier above.
- **Red 30 is OPEN.** Dave asked *"which theme?"*; option C (theme-key the store) is the
  recommendation and is **unconfirmed** — carried, not decided.
- ⚠ **A `$note` discrepancy nobody has resolved:** an earlier sub inscribed *"3.66:1 on `#1A1A1A`"*
  for `#CC4333`; a later sub measured **3.42:1**. Same colour, same ground, two figures. The species
  may affect the other three dark figures, and until it is attributed **none of the four dark
  `$note` contrast figures should be quoted as measured** [[attribute-the-diff]].

## 6. Homes, and a flag that was flipped on an adequate-but-not-verbatim word

19 W-item homes plus G18 were repaired from line-number pointers to **content anchors** — the
[[home-pointer-rot-class]] #167 discovered, fixed at the level of the class rather than the seven
instances. Selftest 46 green, store round-trip proven. **`HOME_ROT_BLOCKING` was then flipped to
`True`** by the conductor on Dave's *"lets crack on"*, after the consequence was stated.

⚠ **That firmness is ADEQUATE BUT NOT VERBATIM**, and it is flagged here and in the banner for a
**one-line confirm at the #169 opener** rather than being recorded as a ruling. A tier flip is
exactly the kind of thing that is easy to inherit as settled and expensive to unwind
[[feedback-clarify-reflect-back]].

⚠ Also measured and **untouched**: `GOOD-MORNING.md`'s DO-FIRST carries **28 items** against the
store's **19 rows** — **9 unrowed**. Reported, not repaired; and **17 `G*` line-form home pointers
remain unverifiable by content**, so the home repair is complete for the class it could measure and
declared incomplete for the class it could not.

## 7. Why this wrap was delegated, and what the sub line says about the day

FILL at wrap-open **147,966** against the stop line **150,929** — roughly **3K of headroom against a
42–49K wrap price**, so the wrap was delegated to this OPUS sub. Boot measured **56,527** real,
**~490 above the 54,859 ±1,178 band**: a **DATAPOINT, declared out-of-band, never corrected into the
constant** [[boot-floor-measured-109]].

And the day's shape is now countable rather than anecdotal, because the convention ruled in §3 got
its first real use in the same wrap that ruled it: **`subs 936,521 tokens (n=11)`**. ⚠ That figure
**excludes this wrap sub's own spend**, which was not measured — and per the convention, an unknown
is not estimated in. Eleven subs against ~3K of remaining window fill is the
[[delegation-cost-inversion-110]] inversion drawn to scale: nearly free in the budget that was
binding, expensive in the one that was not.

---

## Where it stands

**RULED:** `s168-D1` (dashboard review — tooltip.tip closed · length proxy removed · ranking shape
accepted) · `s168-D2` (token-banded effort gauge, edges derived) · `s168-D3` (sub-spend line + gate,
effort-switch agent defs) · `s168-D4` (graphic rung light legs = ruled text values; dark legs stay).

**OPEN, and all of it Dave's:** the amber + blue light legs (picker built, placeholders on disk) ·
red 30's theme question · `s165-D4`'s per-line link ratification, 6/37, **never started — it was
this session's titled item and it carries to #169** · the `HOME_ROT_BLOCKING` confirm · the dark-leg
`$note` discrepancy · the 9 unrowed DO-FIRST items · the 17 unverifiable `G*` homes · the effort
selftest's absence from `_build_all.py`'s route table (~2–3K, touches join-key labels) ·
`_validate_state_contrast.py` unproven against the new rung · and the rendered look of the dashboard
rung block, which is his eye and nobody else's.

*Both-way links: `knowledge/_rulings.json` § `s168-D1`…`s168-D4` · `GOOD-MORNING.md` ★ LATEST
banner (#168) · `_LIVE-STATE.md` ⏱ LATEST delta (#168) · `notes/_GAUGE-LOG.md` `#### 2026-08-13
#168` · `notes/_PROPOSAL-effort-gauge-2026-08-13-v1.md` · `notes/_DELTA-168-effort-removal-v1.md` ·
`_PROPOSAL-148-reds-2026-08-13-v1.md` · `knowledge/_RUNBOOK-capture-ritual.md` § 2f subs line.*
