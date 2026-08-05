# #104 — chain-diet measurement brief

**Written mid-window #104, 2026-08-05.** Home-by-addition for the chain-diet pass Dave added to
the #104 worklist at the opener. **Measurement only — no cut is enacted by this file.**

---

## ⛔ FINDING 1 — THE BRIEF'S SIZE PREMISE IS A CROSS-UNIT COMPARISON

Dave's opener: *"`_CHAIN.md` is 10,288 real vs its 4,917 warn line"*.

**Those are two different units.** `CHAIN_BUDGET_TK = (4917, 6417)` is denominated in **TAPE**
(cl100k), stated at its own definition and at every consumer:

- `_capture_gate.py:1035` — `CHAIN_BUDGET_TK = (4917, 6417)`
- `_capture_gate.py:1021` — *"new: file 4,604 vs warn 4,917 → PASS, **313 tape** of headroom"*
- `_capture_gate.py:2208,2216` — prints `warn {c_warn:,} **tape**`
- `#48` restatement: *"the ruled (4500, 6000) on the SLICE + the measured **417-tape** wrapper"*

**MEASURED on the artefact 2026-08-05, both units, never converted:**

| unit | `_CHAIN.md` | warn line | verdict |
|---|---|---|---|
| **tape** (cl100k) | **6,577** | **4,917 tape** | **OVER by 1,660 tape — 34% over** |
| **real** (`_gauge_tokens.count`) | **10,292** | *(no real-denominated ceiling exists)* | not comparable |

⇒ **What this INVALIDATES:** the apparent ~109% overshoot. The chain **is** over its warn, but by
**34%**, not 2×. The cut required to clear the ceiling is **~1,660 tape (≈2,600 real)** — not the
~5,400 real the cross-unit reading implies. Any diet sized from the 10,288-vs-4,917 pairing would
have over-cut by roughly double. [[measure-dont-convert-units]] [[tape-unit-is-not-real-tokens]]

⚠ **This is #54's defect, re-made in a planning brief.** It is the fourth recurrence in the record
(#80 re-discovered it, #82-D1 enacted the unit, #90 caught it inside the size stamp itself). The
mechanism each time is identical: a number in the live unit set beside a ceiling in the retired one.

⬛ **AND IT RUNS STRAIGHT INTO `G5`, ALREADY OPEN AND ALREADY DAVE'S:**
> `G5` **Four advisory size caps as a set** — *closes when:* Re-measured in real (G9 first),
> then Dave ratifies the set in one pass

The chain warn is one of those four caps. It is **ADVISORY, agent-derived, awaiting Dave** by its
own comment, and it has never been re-measured in real. **An agent re-denominating it is the
derive-and-promote the engine forbids.** The diet can be *sized*; the *ceiling* is not mine.

---

## FINDING 2 — WHERE THE WEIGHT ACTUALLY SITS

Measured per-term with `_gauge_tokens.count()` on the live artefact, `_gen_chain.py --check`
concurring on the slice/wrapper split (`FILE 10,292 real = slice 7,724 + wrapper 2,568`).

| real | share | lines | term |
|---:|---:|---|---|
| 1,837 | 17.7% | L70–105 | `S` OPEN WORK block (generated from `_state.json`) |
| 1,475 | 14.2% | L44–52 | `B` ★ LATEST banner #103 |
| **1,437** | **13.9%** | **L35** | **`H2` STATE — one line** |
| **1,274** | **12.3%** | **L37** | **`H4` PRICE IN REAL TOKENS — one line** |
| **1,007** | **9.7%** | **L34** | **`H1` SIZE STAMP — one line** |
| 755 | 7.3% | L59–69 | `D` ⏱ LATEST delta #103 |
| 548 | 5.3% | L38 | `H5` render sandbox / pace |
| 534 | 5.2% | L53–58 | `I` OPEN WORKLIST presence index |
| 498 | 4.8% | L1–19 | `W1` generated header + contract preamble |
| 308 | 3.0% | L39–43 | `H6` RENAME + TITLE + labels |
| 222 | 2.1% | L25–31 | `W3` STOP block |
| 195 | 1.9% | L36 | `H3` `set_content` / ds-020 |
| 138 | 1.3% | L106–113 | `F` footer |
| 120 | 1.2% | L20–24 | `W2` YOU ARE #104 / title |
| 18 | 0.2% | L32–33 | `H0` "Good morning, Dave" |

**Grouped:**

| real | share | group |
|---:|---:|---|
| **4,787** | **46.2%** | **GM standing header (`H0`–`H6`)** |
| 2,230 | 21.5% | LATEST banner + delta (`B`+`D`) — per-session, rolls |
| 1,837 | 17.7% | OPEN WORK store block (`S`) — generated, row count IS the count |
| 978 | 9.4% | fixed wrapper proper (`W1`+`W2`+`W3`+`F`) |
| 534 | 5.2% | presence index (`I`) |

---

## THE DIAGNOSIS — ACCRETED CORRECTION-PROVENANCE IN THE BOOT PATH

**Three lines — `H1`, `H2`, `H4` — are 3,718 real, 36% of the entire chain.** They are the three
fattest terms in the file by a wide margin, and they share one shape: each carries the *history of
how the line became correct*, not the correct line.

Counted in those three lines: **9 `⛔ CORRECTED AT SOURCE #N` narratives** (#58, #61, #80, #83, #90
among them), each a full retelling of a defect, its mechanism, its escape and its fix.

- `H1` SIZE STAMP — the live claim is three figures. The other ~900 real is #90's re-enactment of
  its own defect plus the `CHAIN_STAMP_RE` scope-hole story (closed #94).
- `H2` STATE — the live claim is "the cut held, N sessions". The other ~1,300 real is the #47/#61/#62
  build-premise archaeology.
- `H4` PRICE — the live claim is three numbers and a unit. The other ~1,100 real is the #58/#59/#80/#83
  provenance corrections.

**This is retrieval material carried in the boot path, and every cold session pays for all of it,
forever.** The standing rule for exactly this already exists and has already been enacted on this
file: [[home-by-addition-then-cut]] — #90 discharged the 2f roll arithmetic from this same header
into `notes/_GAUGE-LOG.md` by addition, verified the home, then cut. No fresh ruling was needed;
it is enactment of a standing rule.

⚠ **`H1`/`H2`/`H4` are also the exact lines the record shows going stale**
([[read-chain-is-where-staleness-is-free]]): every one of them has been corrected at source *in
place*, which is why they grew. **Cutting the provenance is also the staleness fix** — a shorter
line has less surface to go false.

---

## PROPOSED CUT — NOT ENACTED, SIZED ONLY

Two motions, never one. Sole-home probe first; move before cut.

1. **HOME BY ADDITION** — the correction-provenance of `H1`/`H2`/`H4` into a dated section of
   `notes/_MEMENTO-DECISIONS.md` (⛔ **not** `notes/_GAUGE-LOG.md` — #96-D4 ruled that file
   ONE WRITER, `roll_2f` only). Verify by re-read against the artefact.
2. **THEN CUT** — each line reduced to its live rule plus a pointer to the home.

**Sized recovery: ~2,000–2,600 real from the three lines**, which is the whole of the tape overshoot
in Finding 1 and lands the chain under its warn *in the warn's own unit* without touching the
generated terms, the banner, or the delta.

⬛ **NOT ENACTED THIS WINDOW.** Two reasons, both declared:
- **Fill.** #104's boot measured **64,765 real (n=9)**; a cut of Dave's canon header is a
  full-line-read surgery, and #87/#94 both blew the stop line doing exactly that at peak fill
  ([[stop-line-repriced-93]]). Surgery on this file is a **wrap-open-adjacent** act, not a late one.
- **`G5`.** The ceiling the cut would be sized against is unratified and explicitly Dave's.
  The *cut* needs no ruling; the *target* does.

---

## RESIDUAL, DECLARED

- `MEMORY.md` was **not** measured in tokens — the memory directory is outside the sandbox mount,
  so no `_gauge_tokens` reading is reachable from bash. Its compaction is sized by **entry count
  (114 lines / 113 entries)**, which is a COUNT, not a measurement
  [[planning-estimate-is-not-a-measurement]].
- The per-term line segmentation above attributes blank lines and `---` rules to term boundaries;
  the segmented sum (10,366) therefore exceeds the file total (10,292) by 74 real. `_gen_chain`'s
  own slice/wrapper split is the authoritative decomposition and is quoted verbatim above.
