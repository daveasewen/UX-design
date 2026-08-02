# #81 — the ds-021 (C) cross-instrument gate: blast radius, MEASURED before building

*2026-08-02 14:39 Sun · session #81 · OPUS 5 solo Cowork conductor, Dave live.*

status: ruled — shape (C) is Dave's at #81-D1; the measurements are OBSERVED, run live this session; the three items under OPEN are explicitly NOT ruled
provenance: measured #81 2026-08-02 in-session — `_gauge_tokens.count()` vs `_capture_gate.measure_tokens()` on the same input, plus source greps scoped to `knowledge/*.py` and six named markdown files. Scope limits declared in the body.
*Written MID-window, on purpose — a finding carried to the wrap sits in the weakest region of
recall (`_RUNBOOK-context-gauge.md` § POSITION MATTERS).*

**#81-D1 — RULED BY DAVE at the opener:** the `ds-021` enactment shape is **(C) a cross-instrument
gate**, with his condition attached verbatim: *"be careful, i want rigorousness, check for
peripheral effects."* ⚠ The **unit** was never reopened — he ruled it at **#54** (ONE unit, real
tokens, `cl100k` demoted to a labelled estimator, *"never a unit a cap is stated in"*). Only the
shape was open. This note is the peripheral-effects sweep he asked for, run BEFORE any code moved.

---

## ★★ THE HEADLINE — the repo ALREADY HAS a real measurer, and the file-sizing gate does not use it

**MEASURED live, this sandbox, 2026-08-02 14:35** — not traced, not recalled. Same input file
(`_CHAIN.md`), two producers that both live in `_capture_gate.py`'s own namespace:

| producer | reading on `_CHAIN.md` | method string it returns |
|---|---|---|
| `_gauge_tokens.count()` | **10,766 tokens** | `'real'` — Anthropic token-counting API, `read_key()` **PRESENT** |
| `_capture_gate.measure_tokens()` | **6,609 tokens** | `'bytes/3.53 ESTIMATE (tiktoken absent)'` |
| `_CHAIN.md`'s own footer claims | **6,816 tape** | — (generated from the second one) |

`_capture_gate.py:58` reads `import _gauge_tokens as gauge  # noqa: E402 — the UNIT and the BUDGET
(Dave #56)`. **The real measurer is already imported into the file that sizes every artefact, and
every size stamp is produced by the other one.** That is not a missing capability. It is two
instruments in one process disagreeing about what they measure, which is exactly the defect class
(C) exists to catch — Dave's pick is aimed at the right thing.

★ **The word for REAL already exists too**, and in the orphan: `_measure_tokenizer.py:79` prints a
header reading `tape | real | ratio | drift`. #77's periphery inventory recorded that file as
**0 consumers**; re-probed #81, still **0 Python consumers repo-wide**.
[[instrument-without-a-consumer]]

### ⚠ #80's root cause CONFIRMED, and its condition made explicit

#80 wrote that `measurement_degraded()` is *"present, wired, pinned — and blind."* Sweep result:
**true, but conditionally**, and the condition matters for how the gate must be written.

- `measure_tokens()` (`_capture_gate.py:1296`) can return exactly two method strings:
  `"tiktoken cl100k_base"` or `"bytes/{BYTES_PER_TOKEN} ESTIMATE (…)"`.
- `measurement_degraded()` (`:1341`) is literally `return "ESTIMATE" in measure_tokens("x")[1]`.
- ⇒ **tiktoken ABSENT** (this sandbox, right now): returns `True`. Correct — but for the wrong
  reason: it is reporting *bytes-vs-cl100k*, not *cl100k-vs-real*.
- ⇒ **tiktoken PRESENT** (CI, and any sandbox after the mandated `pip install`): returns `False`,
  and the number it blesses is still an OpenAI count ~36–58% under the real one.

**The vocabulary has no word for REAL.** Confirmed at source, and the fix is a CODE change, as #80
struck §C·4 to say.

---

## THE COLLISION INVENTORY — what a (C) gate lands on

### 1. ⛔ The live tape→bill machinery is PINNED BY THREE SELFTESTS, and it teaches the retired system

`_capture_gate.py` still carries the whole two-unit apparatus #54 superseded:

- `:380` `TAPE_TO_BILL = 1.57` · `:387` `bill_of()` · `:392` `fmt_units()` · `:401` `ratio_status()`
- `:1706` and `:1860` call `ratio_status()` into live wrap output
- **Selftest pins that will fight a naive enactment:**
  - `:3572` — fails unless `fmt_units()` output contains **both** `"tape"` and `"bill"`
  - `:3579` — fails unless `ratio_status()` declares itself `PROVISIONAL`
  - `:3953` — pins `TAPE_TO_BILL == 1.57` and `RATIO_FIRM_N == 4` by value

★ **This is the [[unkeyed-gate-vs-roll2f-tension]] shape: a new gate can make a correct state
unreachable.** Deleting or re-denominating any of these without a ruling would silently retire
`ds-021 (c)` — the standing practice that logs one measured pair per wrap and **forks the constant
to Dave at n≥4**. That fork is his, not mine. ⇒ **(C) must sit BESIDE this machinery, not through
it.**

### 2. ⚠ `_RUNBOOK-context-gauge.md` CONTRADICTS ITSELF, and one half is 26 sessions stale

Same file, two sections, opposite units:

- **line 31** (§ THE UNIT AND THE BUDGET, ruled #56): *"The stamp is now ABSOLUTE, in **REAL Claude
  tokens**."*
- **lines 463–505** (§ ★ THE UNITS — `tape` and `bill`): still canon for a **two-unit** system,
  `TAPE_TO_BILL = 1.57`, *"Caps bind on `bill`"*, and — the line that dates it — *"the moment a
  **real** `bill` measurement is available the cap binds on the measured thing and the ratio stops
  mattering."*

**That moment arrived.** The real measurement is available, live, today (table above). The runbook
section describing the condition for its own retirement has outlived the condition. This is one of
the **three homes** #54 named as untouched, and it is the one a cold session is most likely to land
on, because the runbook is the canonical band table and gets grepped every session.

### 3. The unit-naming gate is an ENUMERATION, and it cannot tell `tape` from real

`_capture_gate.py:493`:

```python
BARE_TOKEN_UNITS = ("tape", "bill", "tk", "tokens", "bytes", "ln", "lines")
```

`"tokens"` is already legal, so a REAL figure written `10,766 tokens` **passes today**. ⇒ the gate
enforces *that a unit is named*, never *that the named unit is the one the budget is denominated
in*. [[scope-blindness-gate-vocabulary]] — and per that memory the fix is **normalise once + fail
loud on unknown**, never extend the enumeration.

### 4. The stamp surface — 100 occurrences of `tape`, and they are NOT all the same job

Counted 2026-08-02 (`grep -c`, so occurrences-per-file, not distinct claims):

| file | `tape` |
|---|---|
| `notes/_GAUGE-LOG.md` | 39 |
| `GOOD-MORNING.md` | 23 |
| `knowledge/_RUNBOOK-context-gauge.md` | 18 |
| `_CHAIN.md` | 11 |
| `knowledge/_DS-IMPROVEMENTS.md` | 6 |
| `_LIVE-STATE.md` | 3 |

⚠ **A count is not a measurement** — this is a count, and it is a FLOOR on the work, not a scope.
Two distinct kinds are mixed in it and they must not be treated alike:

- **Historical readings** (`_GAUGE-LOG.md`, archived strata) — these are *correct as written*: they
  record what was measured, in the unit it was measured in. **Re-denominating history would be a
  false inscription.** They need a labelled unit, not a new number.
- **Live claims compared against a budget** (the GM `size:` stamp, `_CHAIN.md`'s footer, `ds-025`'s
  floor, amber/working/hard) — these are **dimensionally invalid today** and are the actual target.

### 5. Downstream consumers that would see a changed number

- `measure_tokens()` call sites: **35**, in 3 files — `_capture_gate.py` 25 · `_gen_chain.py` 9 ·
  `_gm_usage.py` 1.
- `measurement_degraded()` consumers: **3 files** — `_capture_gate.py` 7 · `_gen_chain.py` 3 ·
  `_validate_package_delta.py` 6.
- ⚠ `_gen_chain.py` bakes size figures into `_CHAIN.md` and **iterates to a fixed point**. Any unit
  change moves the footer number that the file asserts about itself. The fixed point must still
  converge — that is a build-level risk, not a cosmetic one.
- ⚠ `_validate_package_delta.py` is the **#64 package-boundary gate**. It reads
  `measurement_degraded()`. A change there reaches the **shipped Memento package**.

⚠ **Probe scope, DECLARED:** greps were `--include=*.py` under `knowledge/` plus the six named
markdown files. **NOT swept:** `archive/`, `_retired/`, `runs/`, `projects/`, `showroom/`,
`memento-package/`, and every non-`.py` consumer. [[unmatched-grep-is-not-an-absence]] — nothing
here licenses a claim of absence outside that scope.

---

## THE PROPOSED SHAPE — and the one thing it must NOT do

**Gate the PRESENCE of a real-capable vocabulary, never the live reading.**

The tempting version fails: *"every size claim must be a REAL measurement."* That refuses a
correct state — a sandbox with no API key and no network can only estimate, honestly, and #79-D1
already ruled that an honest refusal is the right behaviour there. A gate demanding REAL readings
would make the build unrunnable offline, which is [[unkeyed-gate-vs-roll2f-tension]] again.

⇒ **What (C) checks instead — three things, all observable offline:**

1. **Every measurer in the repo can NAME a real tier.** A producer whose method vocabulary contains
   no REAL value fails, *whether or not it is currently able to reach one.* This is the check that
   catches the NEXT instrument, which is the entire reason Dave picked (C).
2. **`measurement_degraded()` is answerable from the vocabulary** — i.e. it must be able to
   distinguish *real* from *estimate*, not merely *estimate* from *cruder estimate*.
3. **A number compared against the budget names a unit the budget is denominated in.** Scoped to
   the quoted stamp forms, not to free prose — [[gate-must-quote-what-it-forbids]]: USE vs MENTION
   is unreachable by syntax, only SCOPE saves it. This note itself must remain legal.

**Ships as a PAIR** — the check and its reader — per [[instrument-without-a-consumer]], and
mutation-tested ×3 with distinct named bites before it is called green
([[gate-must-quote-what-it-forbids]]: *or the green is an assertion*).

---

## OPEN, AND NOT MINE TO DECIDE

- **(i) The tape/bill apparatus.** Retire it, or keep it as a labelled-legacy path with its `n≥4`
  fork to Dave intact? It is pinned by three selftests and carries a standing practice of his.
- **(ii) The historical stamps.** Confirmed above they should NOT be re-denominated — but that is
  my reading of *"never a false inscription"*, not a ruling.
- **(iii) `_measure_tokenizer.py`.** Still 0 consumers, two sessions after #77 flagged it and one
  after #80 re-derived what it already knew. Wire it into the gate, or retire it?

*(Related, unchanged: the six `_decision-graph.json` edge types unruled since #71; `ds-025` item 1
still stands — the boot half is unmeasured, not defaulted.)*
