status: observed
provenance: #80 · 2026-08-02 · MEASURED against `api.anthropic.com/v1/messages/count_tokens`, not estimated

# The tape unit is an OpenAI number, and `ds-021` was never closed — it moved one seam downstream

> ## ⛔ CORRECTION BLOCK — ADDED AT THE #80 WRAP, BY ADDITION, NOTHING BELOW DELETED
>
> **The measurement below is NOT new, and this note presented it as if it were.** Found by the wrap
> sub while doing ritual step 3 (a memory hook named it), then **verified in the repo, which is the
> record**:
>
> - **#53 (2026-07-30) already measured it** — ×1.559 aggregate over five registers, with a
>   purpose-built, re-runnable instrument: `knowledge/_measure_tokenizer.py`. Ledger:
>   `notes/_MEMENTO-DECISIONS.md:1716–1785`. Dossier: `_DECISION-HISTORY/2026-07-30-the-gauge-re-denomination.md`,
>   whose §"(a) The counter already existed" makes this note's "already wired" observation *verbatim*.
>   Also `notes/_GAUGE-LOG.md:461`.
> - ⛔ **#54 (Dave) RULED IT.** *"ONE unit — real Claude tokens. `cl100k` demoted to a LABELLED free
>   estimator, never a unit a cap is stated in."* With his own caveat: **"NOT ENACTED THIS WINDOW —
>   the three homes are untouched."** ⇒ **the UNIT question is not open and must not be re-opened by
>   an agent.** What is open is the ENACTMENT SHAPE (A/B/C/D below), owed since #54, standing in
>   `GOOD-MORNING.md` §C·4 and `knowledge/_DS-IMPROVEMENTS.md:1422`.
> - ⇒ **Two claims below are FALSE and are struck here rather than edited away:** *"The project's own
>   provisional guess was RIGHT and was never checked"* — **it WAS checked, at #53.** And *"both stood
>   for five days as an honest UNPROVEN"* — **they stood one to two days and were then measured and
>   ruled.** The "cost one API call" line is right about the price and wrong about who paid it: **#53
>   already paid it.**
>
> ### ★★ What survives, and it is sharper than the ratio
>
> **(1) The ROOT CAUSE below is genuinely new** — #53's dossier never names `measurement_degraded()`
> or the vocabulary. *The guard is present, wired, pinned against drift, and blind*, because
> `measure_tokens()` has no word for REAL. That is why a RULED unit could sit unenacted for 26
> sessions while every gate read green. **It also corrects a standing §C·4 claim** that the remaining
> work was *"a write-up, smaller than the title implies"* — it is a CODE change (struck at source in
> GM).
>
> **(2) A RULED, INSCRIBED MEASUREMENT DID NOT REACH THE SESSION THAT NEEDED IT.** It was in the
> ledger, a dossier, the gauge log, a memory hook, and a re-runnable script — and #80 still
> re-derived it from scratch and nearly filed it as a discovery. ⚠ **#77's own periphery inventory
> had already predicted this**: `notes/2026-08-02-handoff-periphery-inventory.md:33` lists
> `_measure_tokenizer.py` as reported **"nowhere", 0 consumers.** **An instrument ships WITH ITS
> READER; a measurement nothing re-reads decays into a rediscovery.**
> [[instrument-without-a-consumer]] [[premise-ages-faster-than-rule]]
>
> **(3) The five whys still earn their place** — the reasoning is sound and the root cause is right.
> ⚠ **But why #6 was never asked: *"why did I not check whether this had already been found?"*** The
> answer is the retrieval step this session skipped, and it is the honest lesson of the note.

> **Dave asked the question that found this** (#80, verbatim): *"why does tiktoken keep failing? is
> this the openai method? are there others doesn't anthropic have its own?"* — then, when I began
> answering with a fix: *"I find '5 whys' is better than patching what we have."* This note is the
> five whys. The patch it displaced was "install tiktoken", which would have made the wrong number
> arrive more reliably. [[premise-ages-faster-than-rule]]

## THE MEASUREMENT — the thing that had been called uncheckable

Anthropic **does** have its own tokenizer, it is **already wired in this repo**, and it **works from
the sandbox**: `_gauge_tokens.py` posts to `https://api.anthropic.com/v1/messages/count_tokens`
with `MODEL = "claude-opus-5"` and returns `method='real'`. Measured #80: **0.26s**, key present,
no proxy involved. The envelope overhead is **7 tokens** — negligible, so the comparison below is
clean rather than confounded.

| text | `cl100k` ("tape") | **REAL Claude** | ratio |
|---|---|---|---|
| `_CHAIN.md` — the actual boot payload | 5,761 | **9,079** | **×1.576** |
| `GOOD-MORNING.md` | 27,171 | **42,435** | **×1.562** |
| plain ASCII prose control | 201 | **359** | ×1.786 |

⇒ **every "tape" figure in this project under-reports by ~36%.** The chain's own closing sentence
says it is *"5,761 tape — the unit is THE WHOLE FILE ... held exact by a fixed point"*. It is held
exact. It is exact **in the wrong unit**.

★ **The project's own provisional guess was RIGHT and was never checked.**
`notes/_briefs/2026-07-28-a-subdivision-worker-brief.md:98` records *"ds-021: charged ≈ ×1.55,
provisional"* and `notes/2026-07-29-context-degradation-research.md:217` is titled *"`cl100k` is the
wrong tokenizer, and ds-021 names the wrong unit"*. Both stood for five days as an honest UNPROVEN.
**An honest UNPROVEN is a PRICED TODO, and this one cost one API call.**
[[check-ran-never-reached-plan]] [[measure-dont-convert-units]]

## THE FIVE WHYS

**1. Why is every size figure wrong?**
Because `_capture_gate.py::measure_tokens()` (`:1296`) and `_checkin.py` count with `cl100k_base` —
GPT-4's encoding. Not similar to Claude's. **×1.57 apart on this repo's own files.**

**2. Why is an OpenAI tokenizer being used at all?**
Because tiktoken is a local pip library and Claude's tokenizer is not. There is no offline Anthropic
encoder, so the obvious local implementation reached for the nearest available thing. ⚠ **Note what
this makes of "why does tiktoken keep failing": it never failed. It is ABSENT, because the sandbox
is fresh every session and pip does not persist.** The symptom Dave asked about and the defect
underneath it are not the same problem, and fixing the symptom would have hidden the defect.

**3. Why did the nearest available thing become the shipped unit?**
Because it was never compared against the real one. `_checkin.py:` prints *"D1 rules this an
UNVERIFIED proxy for Claude's tokenizer"* on every run. **The gap was DECLARED — which is exactly
why it passed.** A declared gap passes and a silent one fails; that asymmetry is the mechanism, and
here it worked as designed and still let a wrong unit ship for five days. **Declaring a gap parks
it. Nothing in the ritual ever comes back for a parked declaration.**

**4. Why was it never compared, when the exact measurement was already in the repo?**
Because the three measuring paths were born separately, for separate purposes, and nobody asked
whether they agreed:

| instrument | purpose | unit |
|---|---|---|
| `_gauge_tokens.py::count()` | the BUDGET | **REAL** (API first, cl100k fallback) |
| `_capture_gate.py::measure_tokens()` | FILE SIZES / the GM stamps | cl100k only |
| `_checkin.py` | THROUGHPUT / the live gauge | cl100k only |

One repo, one quantity, **two different answers, and the one that is right is the one nobody reads.**

**5. Why did no gate catch two instruments disagreeing by 57% about the same quantity?**
Because **every gate checks an instrument against ITSELF** — its own selftest, its own fixtures, its
own controls. There has never been a CROSS-INSTRUMENT check. `assert_budget_clears_floor()` compares
a **cl100k-derived floor** against a **real-token budget** (`160,000 / 200,000 / 256,000` are context
-window sizes; they are real tokens by definition) — the comparison is **dimensionally invalid** and
cannot notice, because by the time the two numbers meet they are both bare `int`.

## ROOT CAUSE — the unit is carried in prose, not in the type

`count()`'s docstring already states the whole defence, and it is worth quoting because it was
right: *"The method travels WITH the number, as a tuple, on purpose. A function returning a bare int
invites a caller to publish an estimate as a measurement, which is the `ds-021` defect that put an
OpenAI tokenizer's output into every price this project ever quoted."*

**That sentence describes `ds-021` in the past tense. It is present tense.**

⚠ **I got this wrong first and the correction is the sharper finding.** My first draft said "every
consumer discards the tuple, eleven call sites" — a number taken from a **truncated grep**, which is
the [[unmatched-grep-is-not-an-absence]] defect committed inside a note about wrong numbers. Counted
properly: **17 discard sites** (`_gen_chain.py:179, 219, 235, 264, 325, 335, 337` ·
`_capture_gate.py:565, 585, 1100, 1209, 1212, 1264, 1518, 1527, 1665, 2978`; `:134` and `:1330` are
comments naming the pattern, so it was *seen* and not read as a defect) — **but eight sites DO keep
the method, and there is a whole mechanism built to police it.** `measurement_degraded()`
(`_capture_gate.py:1324–1341`) exists for exactly this, and `:3624` even pins it against
`measure_tokens()`'s own fallback so the two cannot drift.

★★ **So the guard is present, wired, tested — and blind.** `measure_tokens()` can return only two
methods: `"tiktoken cl100k_base"` or `"bytes/N ESTIMATE"`. `measurement_degraded()` asks
`"ESTIMATE" in method` (`:1341`). **cl100k answers "no — I am healthy", because inside this module's
vocabulary cl100k IS the gold standard.** The instrument has no word for the state it is actually
in. It can distinguish cl100k from bytes/4 and cannot distinguish cl100k from REAL — and REAL is the
only distinction that was ever load-bearing.

⇒ **`ds-021` was not closed.** The tuple fixed the *producer*, the vocabulary was never widened, and
the defect moved one seam downstream and got written up as history.
[[scope-blindness-gate-vocabulary]] — the fix is to normalise the vocabulary once and fail loud on
an unknown, never to enumerate the cases. [[honest-refusal-needs-a-legal-form]] — when a gate calls
a wrong state healthy, suspect the VOCABULARY before the data.
[[assertion-propagation-gap]] · [[conflated-fix-guarantees-recurrence]] · [[gate-narrows-its-own-rule]]

## WHAT THIS IS NOT

⚠ **Not a reason to distrust today's build.** #80's refusal (`MeasurementRefused`) is orthogonal and
correct: it governs *whether we measure at all*, not *which ruler*. It stands.

⚠ **Not yet a re-pricing of any past session.** #79's *"159,902 tape against Dave's 200,000"* was a
`_checkin.py` reading, so it is cl100k, so the real figure is ~×1.57 higher — **but that arithmetic
is a CONVERSION, and converting is the defect this note is about.** It must be RE-MEASURED, not
multiplied. What can be said without converting anything: **the amber line was closer than the
banner showed, and possibly already crossed.** [[measure-dont-convert-units]]

## THE FIX IS NOT "SWAP THE TOKENIZER" — ⬛ UNRULED, DAVE'S

Swapping `measure_tokens()` to the API is the patch, and it inherits the same root cause: the next
seam still passes a bare int. Four candidates, and picking among them is Dave's, not an agent's:

- **(A) Make the unit a type.** A `Tokens(n, unit)` value that refuses `<`/`-` against a different
  unit. Kills the class. Touches 11 call sites. [[translate-prose-into-machinery]]
- **(B) One measuring authority.** Delete two of the three paths; everything routes through
  `_gauge_tokens.count()`. Fewest lines, but binds every size stamp to a network call.
- **(C) A CROSS-INSTRUMENT gate.** The cheapest thing that would have caught this: one build step
  asserting the three instruments agree on one fixture, within a stated tolerance, or refusing.
  ★ Catches the *next* one of these too, which (A) and (B) do not.
- **(D) Calibrate and keep cl100k.** Store the measured ×1.576 and convert. **Named for
  completeness and I argue against it** — it is a conversion where a measurement is available, and
  the ratio is not constant (×1.79 on plain prose vs ×1.56 on this repo's files).

⚠ **Whichever is ruled, the re-measurement lands on the GM size stamps, `ds-025`'s floor, and the
amber/working lines' relationship to them.** That is a bigger change than it looks and is why it is
being put to Dave rather than shipped.
