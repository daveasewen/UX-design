# The trigger index — the session where Dave named the root cause and it was not tokens

provenance: 1490dc90-ba45-48c6-9a1b-66ef3e2a8d3b · 2026-08-02
status: ruled — #81-D1 (shape) + the trigger-index build; ledger `notes/_MEMENTO-DECISIONS.md` § ★ #81

*Session #81, 2026-08-02, OPUS 5 solo Cowork conductor, Dave live, one window.*
*Spine entry: `_LIVE-STATE.md` ⏱ #81 delta. Sibling note (the measurements):*
*`notes/2026-08-02-81-cross-instrument-gate-blast-radius.md`.*

---

## The arc in one paragraph

The window opened to enact `ds-021` — a unit ruling Dave made at **#54** and that #80 had
re-derived from scratch. He picked enactment shape **(C)**, a cross-instrument gate, and attached
a condition: *"be careful, i want rigorousness, check for peripheral effects."* The sweep did find
the peripheral effects, and it found something better: the repo **already had** a working real
measurer that the file sizing every artefact never called. Then, twice, Dave stopped the session —
*"we've identified this as a problem already, again we are going round in circles"*, then *"we seem
to have a knowledge transfer problem between sessions, isn't this being stored anywhere?"* — and
the second question turned out to be the actual finding. **It was stored. Ten times.** What ships
from this window is therefore not the token fix he asked for at the opener; it is the thing that
stops the token fix being rediscovered a fourth time.

---

## Finding 1 — the peripheral-effects sweep found the fix already built and unwired

**Why it was run:** Dave's condition. Not a formality — the sweep was supposed to establish what a
new gate would collide with.

**What it found, MEASURED live rather than traced.** Same input file, two producers that both live
inside `_capture_gate.py`'s own namespace:

| producer | `_CHAIN.md` | method |
|---|---|---|
| `_gauge_tokens.count()` | **10,766** | `'real'` — Anthropic `count_tokens` API, key present |
| `_capture_gate.measure_tokens()` | **6,816** | `'tiktoken cl100k_base'` |

And `_capture_gate.py:58` reads `import _gauge_tokens as gauge`. ⇒ **The real measurer was already
imported into the file that produces every size stamp in the project, and not called.** The defect
was never a missing capability. It was two instruments in one process disagreeing, with nothing
positioned to notice.

★ **The word for REAL existed too — in the orphan.** `_measure_tokenizer.py:79` prints a
`tape | real | ratio | drift` header. #77's periphery inventory had recorded it as **0 consumers**;
re-probed #81, still zero. [[instrument-without-a-consumer]]

**What it corrected in #80's account.** #80 wrote that `measurement_degraded()` is *"present, wired,
pinned — and blind."* True, and the CONDITION matters for how a gate must be written: with tiktoken
**absent** it returns `True` (correctly, but for the wrong reason — it is seeing bytes-vs-cl100k);
with tiktoken **present** it returns `False` while blessing an OpenAI count. The root cause holds.

---

## Finding 2 — the collision inventory, and the one it would have broken

Three selftests pin the retired tape/bill apparatus: `:3572` (both units must appear in output),
`:3579` (`ratio_status()` must declare itself PROVISIONAL), `:3953` (`TAPE_TO_BILL == 1.57`,
`RATIO_FIRM_N == 4`). Retiring that machinery as a side effect of enacting (C) would have silently
killed **`ds-021 (c)`** — the standing practice that logs one measured pair per wrap and **forks the
constant to Dave at n≥4**. That fork is his. ⇒ Dave ruled it **kept as labelled legacy**, and the
new gate sits BESIDE it rather than routing through it.

⚠ **And a contradiction inside canon, found while reading it:** `_RUNBOOK-context-gauge.md` says
*"REAL Claude tokens"* at line 31 (#56) and still teaches the two-unit tape/bill system with
`×1.57` at lines 463–505 — including the line that dates it: *"the moment a real bill measurement
is available the cap binds on the measured thing and the ratio stops mattering."* **That moment
arrived.** It is one of the three homes #54 declared untouched. **STILL UNFIXED at the close of
#81** — declared here rather than quietly carried.

---

## Finding 3 — ★★★ the root cause, and Dave found it, not the sweep

Twice he named the circling before the repo did. The second time he asked the question that
resolved it: *"isn't this being stored anywhere?"*

**Probed, and the answer is the finding.** #54's ruling lives in **ten places**:
`notes/_MEMENTO-DECISIONS.md:1716`, `notes/_GAUGE-LOG.md:461`, `knowledge/_DS-IMPROVEMENTS.md:1422`,
and **eight** `_DECISION-HISTORY` dossiers. Meanwhile a `_memento_search.py` query on the topic,
run in this session, returned **the current week's banners**.

★★★ **THE RULE, and it generalises far past tokens:**

> **Every mechanism this project has for REMEMBERING is write-optimised. Every mechanism for
> READING is triggered by SUSPICION — and you can only search for what you already suspect
> exists. So a settled ruling is invisible precisely to the session about to re-derive it.**

**A better search does not fix this.** A better search still has to be CALLED, by someone who
already doubts. That is why #80 re-derived, and why #81 began to.

⇒ **THE TRIGGER MUST BE THE WORK ITSELF, NOT A QUERY.** `git diff --name-only` already knows what
a session touched. That is the one signal available without anyone suspecting anything.

---

## What was built — and it ships as a PAIR, deliberately

**`knowledge/_rulings.json`** — a POINTER index: ruling → the files and symbols it governs → where
canon actually lives. Eight rulings seeded (ds-021, ds-021-C, ds-023, gauge-band, gauge-refusal,
chain-cut, delegation-inversion, derivation-governance). ⚠ **Pointers only. If substance ever lands
in it, it has become the eleventh copy and the defect is back** — that warning is inside the file.

**`knowledge/_governs.py`** — the reader. Fires off `changed_files()`, renders every ruling
governing them. `IndexUnreadable` raises **loud and named**: an index that fails open would report
*"nothing is governed"* in the same voice it would use if it had checked.

**Wired into `_capture_gate.py::run()`, both modes** — not offered as a command. ★ **That choice is
the whole lesson of Finding 1:** `_measure_tokenizer.py` was correct, runnable and unread for
fourteen sessions. An index nothing consults repeats it exactly.

**Plus the (C) gate Dave ruled:** `MEASURERS` + `unit_vocabulary_audit()` — a registry of every
cl100k counting site. **Unregistered ⇒ FAIL** (this is the half that catches the next instrument);
**declared estimate-only ⇒ WARN by name**. It checks **vocabulary, never the live reading** —
demanding a REAL reading would refuse an honest offline estimate, which is the ds-022(d)/`roll_2f`
shape: a new gate making a correct state unreachable.

---

## What went wrong on the way — two bugs mutation-testing found at birth

**Neither would have been caught by the passing selftest.** Both are the class this project keeps
re-meeting.

1. **`def load(path: str = INDEX)` binds the default when the function is DEFINED.** Reassigning
   `_governs.INDEX` afterwards silently kept reading the old file — so the module constant *looked*
   like the single source of truth and was not. Mutation M4 ("make the index unreachable") stayed
   **GREEN** because the test could not reach the path it thought it was breaking. ★ A green that
   cannot fail is an assertion, and here the assertion was hiding inside Python's own semantics.
2. **`except ImportError` was too narrow to hold `IndexUnreadable`.** Once M4 bit, it bit as a
   **CRASH** — which would have taken all 39+ checks of the gate down with it. [[a-crash-is-not-a-fail]]
   ★ Note the symmetry with **#79-D1**, which reasoned about the same seam from the other side
   (would a `BaseException` slip `except Exception`?). Both answers come from one rule: **the
   handler's breadth is a property of the CALL SITE, not of the repo.**

**Final mutation state: 5 mutations, 5 distinct named bites, revert green.**

---

## Resolved state

- ✅ `ds-021` enactment shape **(C) RULED #81-D1**; tape/bill **kept as labelled legacy** (Dave).
- ✅ Cross-instrument unit audit BUILT, wired into both gate modes, 6 bites.
- ✅ Trigger index BUILT and CONSUMED — surfaced 6 rulings on this session's own diff.
- ✅ Gates at the wrap: `_capture_gate.py` build **61 in scope · 0 fail · 4 warn** (the 4 are the
  DECLARED gaps, by design) · `--selftest` EXIT=0 · `_governs.py --selftest` EXIT=0 ·
  `_gauge_tokens.py --selftest` EXIT=0 · `_build_all.py --selftest` EXIT=0 (85 steps).

## Still open — declared, not carried quietly

- ⬛ **Wiring `measure_tokens()` to the native counter.** The actual cure; NOT done. It moves the GM
  size stamps, `_CHAIN.md`'s fixed point, `ds-025`'s floor, the amber line, and
  `_validate_package_delta.py` (the shipped Memento package). **Dave's, and priced, not smuggled.**
- ⬛ **`_RUNBOOK-context-gauge.md` lines 463–505** still teach the retired two-unit system.
- ⬛ **`_measure_tokenizer.py` — still 0 consumers.** Wire it into the gate, or retire it?
- ⬛ Item (b), **headroom before the legend wave** — untouched this window.
- ⚠ **Seed the trigger index further.** Eight rulings is a start, not coverage. A missing entry is
  the exact failure it exists to prevent, so this is the one that decays if nobody adds to it.
