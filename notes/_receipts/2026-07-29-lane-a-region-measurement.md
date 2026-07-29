# Lane A receipt — REGION MEASUREMENT (the evidence table for the compactable-cap decision)

```
provenance: local_2b2ae5b3-6db0-49f1-9156-f05072da6a68 · worker lane A · 2026-07-29 13:33 BST (from `date`)
status: observed
repo HEAD at measurement: e1649fb
encoder: tiktoken 0.13.0, cl100k_base — INSTALLED FIRST, verified present in every measuring call
unit: tape (what tiktoken cl100k_base counts). NOT bill (what the window charges).
```

> ★ **UNIT DISCIPLINE, and it is why this lane exists.** Every number below is **tape**. This receipt
> converts nothing into percentages, fill, points, or a band. The denominator is under an open
> question (§4) and converting through it is the exact failure this measurement exists to expose.
> **Every band, fill-%, and points figure this lane could have produced is `UNSTATED`.**
>
> ⚠ **`bill` is UNMEASURED for every figure here.** Only two measured tape/bill pairs exist in the
> corpus (`_capture_gate.py MEASURED_PAIRS`, both #30, n=2 < `RATIO_FIRM_N=4`). This lane did not add
> one and did not derive one. Where the gate publishes a bill it derives it ×1.57 and marks it derived.

---

## 0. WHAT IS MEASURED vs WHAT IS INHERITED vs WHAT IS UNKNOWN

| Class | Items |
|---|---|
| ✅ **MEASURED by this lane** | every GM/LS region tape · read-chain tape · GM/LS whole-file tape · compactable tape · banner-region tape · `MEMORY.md` tape · skills-description tape · the `section-sizes` series parse · the `DEFAULT_WINDOW` dependency grep |
| 📎 **INHERITED** (told, not measured here) | the brief's #38 figures (compactable 11,955 tape · chain 4,400 tape · ~2,924 in chain · ~9,000 never paid at boot) · `ds-025` unreachability · the "~414 tape under-report without tiktoken" figure · the 45 s sandbox call cap · `_build_all.py` = 72 steps / 3–4 min · `TAPE_TO_BILL = 1.57` |
| ⬛ **UNKNOWN — not estimated** | the **harness half** of cold start (system prompt, tool schemas, MCP server instructions) — unreachable from every mount, `ds-025` · the **true window denominator** (§4) · the **bill** for every tape figure below · `section-sizes` for sessions **#26, #36, #37** (no line exists in any reachable file) |

---

## 1. PER-REGION SIZE, NOW — and chain membership

**Measured this call**, `python3 knowledge/_gm_usage.py --sizes` + `_capture_gate.measure_tokens`,
tiktoken cl100k_base, no fallback taken.

**The chain is three things** (`_capture_gate.read_chain_tk`, as re-pointed #33): GM header → ★ LATEST
banner → the ⏱ LATEST delta in `_LIVE-STATE.md`. Everything else is retrieval-only.

### GOOD-MORNING.md

| region | tape now | in READ CHAIN? |
|---|---:|---|
| HDR | **1,566** | ✅ chain |
| LATEST | **1,758** | ✅ chain |
| PRIOR | **1,196** | ⬜ retrieval-only |
| DOFIRST | **2,252** | ⬜ retrieval-only |
| A | **4,208** | ⬜ retrieval-only *(also §A-exempt from the compactable budget)* |
| C1 | **842** | ⬜ retrieval-only |
| C2 | **874** | ⬜ retrieval-only |
| C4 | **3,021** | ⬜ retrieval-only |
| STRATA | **1,224** | ⬜ retrieval-only |
| **GM WHOLE FILE** | **16,942 tape** | — |

### _LIVE-STATE.md

| region | tape now | in READ CHAIN? |
|---|---:|---|
| HDR | **398** | ⬜ retrieval-only |
| LANES | **872** | ⬜ retrieval-only |
| SPIN | **1,794** | ⬜ retrieval-only |
| DELTAS | **5,215** | ◐ **PARTIAL — 1,476 tape of the 5,215 is the LATEST delta and IS in the chain; the remaining 3,739 tape is retrieval-only.** `read_chain_tk` reports `LATEST delta only (of 48 delta lines)`. |
| WEBFONT | **604** | ⬜ retrieval-only |
| LIVE | **4,928** | ⬜ retrieval-only |
| LIFECYCLE | **973** | ⬜ retrieval-only |
| DEAD | **432** | ⬜ retrieval-only |
| OPEN | **4,361** | ⬜ retrieval-only |
| TARGETS | **577** | ⬜ retrieval-only |
| SPINOFFS | **444** | ⬜ retrieval-only |
| **LS WHOLE FILE** | **20,598 tape** | — |

### Derived aggregates (sums of the above; no unit conversion)

| aggregate | tape now | the constant it is checked against | source of the constant |
|---|---:|---|---|
| **READ CHAIN** (HDR+LATEST+LS LATEST delta) | **4,801** | `CHAIN_BUDGET_TK = (4500, 6000)` tape | `_capture_gate.py:411` — **ADVISORY, agent-derived, awaiting Dave** |
| **COMPACTABLE** (GM whole − §A) | **12,734** | `SIZE_BUDGET_TK["compactable"] = 8000` warn / **12,000 block** (cap+50%) | `_capture_gate.py:275` — shape D8(a) Dave, **number agent-recommended** |
| **BANNER region** (file top → DO-FIRST) | **4,521** | `BANNER_BUDGET_TK = (4000, 5000)` tape | `_capture_gate.py` M8 |
| **CORPUS** (GM + LS whole, the retrieval surface) | **37,540** | — no budget — | — |
| chain's GM term, as one slice | **3,325** | — | HDR 1,566 + LATEST 1,758 = 3,324; the 1-tape difference is the slice-join boundary, not an error |

⚠ **Reported, not adjudicated:** all three budgeted aggregates sit above their warn constant, and
COMPACTABLE sits above its block constant. **The gate binds on `bill`, not tape** — it derives both
sides ×1.57, and its own comment (`_capture_gate.py` ~line 890) says the conversion cancels and is
"arithmetically identical to binding on tape, BY DESIGN". **This lane states the measurement and
stops.** What to do about it is not this lane's.

📎 **Disagreement with the inherited figures, stated as fact, not resolved:** the brief carries
compactable **11,955 tape** and chain **~4,400 tape** at #38's close. This lane measures **12,734 tape**
and **4,801 tape** at HEAD `e1649fb`. Both pairs may be correct at their own moment — GM was written to
after #38's stamp (see the STRATA artefact, §2). **Which is right is not a Lane A question.**

---

## 2. GROWTH PER REGION PER SESSION — the `section-sizes` series read as a series, for SIZE

**Source:** `notes/_GAUGE-LOG.md` (12 lines, #23–#35) + `GOOD-MORNING.md:407` (#38, the only reachable
copy) + **NOW** measured by this lane. All lines self-report method `tiktoken cl100k_base`.

⬛ **HOLES IN THE SERIES: #26, #36, #37 have no `section-sizes` line anywhere reachable.** Grepped
repo-wide across `*.md`. This is a gap in the record, reported as a gap — not interpolated.

⚠ **`NOW` is this lane's own measurement at HEAD `e1649fb`, 13:33 BST.** It is *not* a session stamp;
`--sizes --session 39` was invoked with `39` purely as a print label. **No session #39 is claimed.**

⚠ **SERIES ARTEFACT, and it distorts STRATA and the totals.** `STRATA:8` appears at #25 and #30–#38.
Two of those lines say so in the record itself (`*(measured pre-stratum)*` at #31, #32): the sizes line
is emitted **before** the session writes its own stratum block, so STRATA reads ~8 tape at stamp time
and is large minutes later. **`NOW` at 1,224 tape is post-stratum.** STRATA's row and every
`TOTAL-of-listed` are therefore **not like-for-like across the series.**

### GOOD-MORNING.md — tape per region per session

| # | HDR | LATEST | PRIOR | DOFIRST | A | C1 | C2 | C4 | STRATA | Σ listed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 23 | 1074 | 799 | 1117 | 2125 | 4208 | 929 | 1076 | 1204 | 632 | 13,164 |
| 24 | 1032 | 847 | 862 | 2126 | 4208 | 782 | 1076 | 1204 | 882 | 13,019 |
| 25 | 999 | 952 | 1001 | 2132 | 4208 | 820 | 1076 | 1204 | 8 | 12,400 |
| 26 | — | — | — | — | — | — | — | — | — | **NO LINE** |
| 27 | 1178 | 1239 | 1054 | 2297 | 4208 | 842 | 1076 | 1204 | 1167 | 14,265 |
| 28 | 1378 | 1627 | 1412 | 2310 | 4208 | 842 | 1157 | 1435 | 1276 | 15,645 |
| 29 | 1116 | 1048 | 1664 | 2474 | 4208 | 842 | 1157 | 1435 | 994 | 14,938 |
| 30 | 1363 | 1050 | 1111 | 2474 | 4208 | 842 | 1157 | 1435 | 8 | 13,648 |
| 31 | 1170 | 792 | 1113 | 2474 | 4208 | 842 | 1157 | 1435 | 8 | 13,199 |
| 32 | 1170 | 1325 | 855 | 2474 | 4208 | 842 | 1157 | 1435 | 8 | 13,474 |
| 33 | 1461 | 845 | 1388 | 2554 | 4208 | 842 | 1157 | 1868 | 8 | 14,331 |
| 34 | 1417 | 1025 | 858 | 2554 | 4208 | 842 | 1157 | 1788 | 8 | 13,857 |
| 35 | 1473 | 1346 | 1209 | 2554 | 4208 | 842 | 1157 | 1955 | 8 | 14,752 |
| 36 | — | — | — | — | — | — | — | — | — | **NO LINE** |
| 37 | — | — | — | — | — | — | — | — | — | **NO LINE** |
| 38 | 1776 | 1332 | 1196 | 2554 | 4208 | 842 | 1157 | 3213 | 8 | 16,286 |
| **NOW** | **1566** | **1758** | **1196** | **2252** | **4208** | **842** | **874** | **3021** | **1224** | **16,941** |
| **Δ #23→NOW** | +492 | +959 | +79 | +127 | **±0** | −87 | −202 | **+1,817** | +592 | +3,777 |
| **Δ / session** (÷16) | +31 | +60 | +5 | +8 | ±0 | −5 | −13 | **+114** | +37 | +236 |

⚠ **`Δ / session` divides by 16 elapsed sessions (#23→NOW), not by 14 observations.** Three sessions in
that span left no line. Stated so the divisor is not mistaken for a sample size.

### _LIVE-STATE.md — tape per region per session

| # | HDR | LANES | SPIN | DELTAS | WEBFONT | LIVE | LIFECYCLE | DEAD | OPEN | TARGETS | SPINOFFS | Σ listed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 23 | 255 | — | 1794 | 2242 | 604 | 4928 | 965 | 432 | 4361 | 577 | 444 | 16,602 |
| 24 | 255 | 674 | 1794 | 2221 | 604 | 4928 | 965 | 432 | 4361 | 577 | 444 | 17,255 |
| 25 | 255 | 727 | 1794 | 2336 | 604 | 4928 | 965 | 432 | 4361 | 577 | 444 | 17,423 |
| 27 | 255 | 872 | 1794 | 2651 | 604 | 4928 | 973 | 432 | 4361 | 577 | 444 | 17,891 |
| 28 | 255 | 872 | 1794 | 3045 | 604 | 4928 | 973 | 432 | 4361 | 577 | 444 | 18,285 |
| 29 | 255 | 872 | 1794 | 3578 | 604 | 4928 | 973 | 432 | 4361 | 577 | 444 | 18,818 |
| 30 | 255 | 872 | 1794 | 3646 | 604 | 4928 | 973 | 432 | 4361 | 577 | 444 | 18,886 |
| 31 | 255 | 872 | 1794 | 3339 | 604 | 4928 | 973 | 432 | 4361 | 577 | 444 | 18,579 |
| 32 | 255 | 872 | 1794 | 2934 | 604 | 4928 | 973 | 432 | 4361 | 577 | 444 | 18,174 |
| 33 | 255 | 872 | 1794 | 2950 | 604 | 4928 | 973 | 432 | 4361 | 577 | 444 | 18,190 |
| 34 | 255 | 872 | 1794 | 3321 | 604 | 4928 | 973 | 432 | 4361 | 577 | 444 | 18,561 |
| 35 | 255 | 872 | 1794 | 3520 | 604 | 4928 | 973 | 432 | 4361 | 577 | 444 | 18,760 |
| 38 | 398 | 872 | 1794 | 5215 | 604 | 4928 | 973 | 432 | 4361 | 577 | 444 | 20,598 |
| **NOW** | **398** | **872** | **1794** | **5215** | **604** | **4928** | **973** | **432** | **4361** | **577** | **444** | **20,598** |
| **Δ #23→NOW** | +143 | — | **±0** | **+2,973** | ±0 | ±0 | +8 | ±0 | ±0 | ±0 | ±0 | +3,996 |
| **Δ / session** (÷16) | +9 | — | ±0 | **+186** | ±0 | ±0 | +0.5 | ±0 | ±0 | ±0 | ±0 | +250 |

**Observations, flat:**

- **Every LS region except `HDR`, `DELTAS` and `LIFECYCLE` is byte-frozen across 16 sessions.**
  `SPIN`, `WEBFONT`, `LIVE`, `DEAD`, `OPEN`, `TARGETS`, `SPINOFFS` have not moved one tape since #23.
  `LANES` has been static at 872 tape since #27.
- **All LS growth is in `DELTAS`: +2,973 tape of the +3,996 tape total.**
- **LS is identical at #38 and NOW** — the file has not been written since #38's stamp.
- **In GM, `C4` carries the largest single-region growth: +1,817 tape**, and +1,258 of that lands in the
  single step #35 → #38.
- **`A` is frozen at 4,208 tape for all 16 sessions.** It is also the §A-exempt region.
- **`C1` and `C2` shrank** (−87, −202 tape).
- The `C2b · C3 · C4b · C5` columns present at #23–#35 vanish at #38: retired #35, offloaded to
  `_GM-ARCHIVE.md`. Their #35 values were `484 · 181 · 256 · 84` tape = **1,005 tape removed from GM**
  by that offload, and GM's Σ listed still rose #35→#38.

---

## 3. WHAT A COLD START ACTUALLY COSTS TODAY — itemised

⚠ **The skills figure measures the DESCRIPTION LINES AS RENDERED IN THE WINDOW, not the `SKILL.md`
files on disk.** Those are two different quantities; the disk files are ~10–100× larger and are not
loaded at boot. Method and its limits stated below.

| item | tape | how measured | status |
|---|---:|---|---|
| **READ CHAIN** — GM HDR + ★ LATEST + LS ⏱ LATEST delta | **4,801** | `_capture_gate.read_chain_tk` at HEAD `e1649fb` | ✅ MEASURED |
| **`MEMORY.md`** (the auto-memory index) | **4,630** | tokenised directly — the file **is** reachable at `mnt/.auto-memory/MEMORY.md` (17,309 chars, 116 lines) | ✅ MEASURED |
| **skills — description TEXT only**, 38 entries | **2,960** | frontmatter `description:` of every entry in the window's `<available_skills>` block | ✅ MEASURED (see caveat) |
| **skills — FULL `<available_skills>` block** (tags + qualified names + `<location>` host paths) | **7,022** | reconstruction, tokenised | ✅ MEASURED (see caveat) |
| ↳ *of which structural, non-description* | *4,062* | block − description text | ✅ MEASURED |
| **skills — second rendering**, `- <name>: <desc>` list under "available for use with the Skill tool", 38 of its ~43 lines | **3,233** | same descriptions, list form | ✅ MEASURED (partial — 5 lines not reconstructible, below) |
| **HARNESS half** — system prompt, tool schemas, deferred-tool list, MCP server instructions, `<available_agents>` | **⬛ UNKNOWN** | **UNREACHABLE from every mount (`ds-025`, inherited).** `find` across `mnt/` returns nothing. | ⬛ **NOT ESTIMATED** |
| **COLD-START TOTAL** | **⬛ UNSTATED** | cannot be totalled while one term is UNKNOWN | ⬛ |

**Sum of the measurable terms only, and it is a FLOOR, not a total:**
chain 4,801 + `MEMORY.md` 4,630 + `<available_skills>` block 7,022 = **16,453 tape**, plus the second
skills rendering **3,233 tape** if it is charged separately (whether both renderings are billed is
**UNKNOWN** to this lane). **⬛ The harness term is missing and is not small — any figure presented as
"the cold start" without it is understated by an unmeasured amount.**

### Method and its exact limits — the skills figures

The `<available_skills>` block was **reconstructed from disk, then verified**, rather than transcribed:

1. Every reachable `SKILL.md`/`commands/*.md` frontmatter `description:` was machine-extracted
   (37 `SKILL.md` + 4 command files under `mnt/.claude/skills` and `mnt/.remote-plugins`).
2. **Membership was reconciled, and the two sets are NOT the same** — this is the trap the brief names:
   - disk has **37** `SKILL.md`; the window block has **38** entries;
   - `consolidate-memory`, `video-interaction-mapper`, `generate-project-plan` are **on disk but not in
     the block**;
   - the four `pdf-viewer:` command entries in the block come from `commands/*.md`, **not** `SKILL.md`.
   - 37 − 3 + 4 = **38.** ✅ reconciles exactly.
3. The reconstruction's **name list and ordering reproduce the window block entry-for-entry, in order**
   (38/38 exact match, verified by eye against the rendered block).
4. **Description text verified byte-identical** on three verbatim spot-checks (`docx`, `dream-pass`,
   `design:ux-copy`) against the rendered block.

⚠ **What is therefore MEASURED and what is my own transcription:** the *description text* and the
*entry set* are machine-read and verified. The *wrapper* — XML tag punctuation and the `<location>`
host paths — is transcribed by me from the window (4 distinct formulaic path prefixes). **The 4,062
tape of structural overhead is accurate to my reading of the block, not machine-copied**, and is the
softest number in this receipt.

⬛ **The 3,233 tape second-rendering figure covers 38 of its ~43 lines.** `init`, `review`,
`security-review` and any other harness-native entries are not on a reachable mount and are **not
estimated**; that line is therefore a **partial measurement**, explicitly.

⬛ **Not measured, and stated so:** whether the window charges the block once or twice; per-token
harness framing; whether tool schemas for the ~140 deferred tools are billed at boot or on `ToolSearch`.

---

## 4. `DEFAULT_WINDOW = 200_000` — the denominator's blast radius

**Confirmed literal, at `knowledge/_context_gauge.py:27`:** `DEFAULT_WINDOW = 200_000`, comment
`# Window = model context budget … Measured, adjustable.` (adjacent: `DEFAULT_BASELINE = 35_000`).

⚠ **Three receipts already cite this as line `:27`; the *docstring* usage example at `:16` also carries
`--window 200000`, and one note cites it as "line 34".** At HEAD `e1649fb` the assignment is at **:27**.

⚠ **Measure, do not adjudicate — this lane does not say what the value should be, and did not change it.**

### Where it is READ — the complete list (grepped repo-wide, `*.py *.md *.json *.sh`)

| # | site | what it does |
|---|---|---|
| 1 | `_context_gauge.py:27` | **the only definition.** No other module defines or imports it. |
| 2 | `_context_gauge.py:63` | `ap.add_argument("--window", type=int, default=DEFAULT_WINDOW)` — **the only code read.** Overridable per-invocation; nothing in the repo passes an override. |
| 3 | `_context_gauge.py:16` | docstring usage example, restates `--window 200000` |

**`DEFAULT_WINDOW` is imported by nothing.** `_capture_gate.py` does **not** import `_context_gauge`.
No script, gate, runbook step or scheduled task invokes `_context_gauge.py` automatically — the runbook
instructs a **human/subagent** to run it (`_RUNBOOK-context-gauge.md:424`).

### What flows from it, inside the script

```
fraction = (transcript_tokens + baseline) / args.window      # line ~79
      ↓
band(fraction)  →  AMBER_AT = 0.50 · RED_AT = 0.60  →  "GREEN" / "AMBER" / "RED" + the action line
      ↓
printed: the bar, the "NN.N%" figure, the band word, the "= ~N / 200,000" line
```

**Everything the script prints except `transcript_tokens` and `method` passes through the denominator.**

### Reports and published numbers that depend on it

| dependent | where | how it changes if the denominator is wrong |
|---|---|---|
| **the gauge's own `%` + band + bar + action line** | `_context_gauge.py` stdout | scales **inversely and exactly** |
| **`BANDS = ((45,"GREEN"),(60,"AMBER"),…)`**, `BAND_FLOOR = 45`, `HARD_STOP = 60` | `_capture_gate.py:79, 123, 124` | the **constants** are %-of-window and do not move, but **what they mean in tokens does.** The gate *validates* the stamp's arithmetic and band word against this table — it never computes a % itself, so it **cannot detect a wrong denominator.** |
| **every `pre-flight:` stamp** — `fill N% + job N% + wrap N% = N% BAND` | **27 stamps** in `notes/_GAUGE-LOG.md`, plus the live GM stamp | every term is %-of-window; all 27 re-scale |
| **the ds-023 stop line** `HARD_STOP − wrap%` | `_capture_gate.py:567, 574, 580` | computed in points; the token value of the stop moves |
| **the #33 re-point comment's `pts` figures** | `_capture_gate.py:399–400` — `52,846 charged ≈ 26.4 pts` / `5,286 charged ≈ 2.6 pts` | ✅ **denominator CONFIRMED by reproduction:** 52,846 ÷ 200,000 = 26.4; 5,286 ÷ 200,000 = 2.64. *(This division identifies an already-published figure's denominator. It is not a conversion of any measurement in this receipt.)* |
| **`_RUNBOOK-context-gauge.md`** prose | lines **18, 209, 399, 428** — "~200k tokens for this model class", the resource table, the band table, the flags note | four prose restatements, none generated; each is an independent copy that can drift |
| **`notes/2026-07-29-context-degradation-research.md`** | lines 15, 17, 43, 181, 193, 202, 302, 306 | ⚠ `status: floated`. Already states the ~37%-vs-~7.5% split and the "cold floor ~22% vs ~4–5%" consequence |
| **`notes/_receipts/2026-07-29-lane-b-six-opens-assembled.md`** | lines 45, 226, 228, 235, 317 | today's Lane B, same finding |
| **`notes/_receipts/2026-07-29-context-degradation-worker.md`** | lines 17, 32 | |
| **`notes/_receipts/2026-07-29-worker-17-literal-sweep.md`** | line 23 | states plainly: *"`~29 pts` divides by `DEFAULT_WINDOW = 200_000`. I did not verify that denominator."* |
| **`notes/2026-07-23-harness-framework-spinoff.md`** | line 39 | "the ~200k" as an environment quirk to be exported to the spin-off |
| **`_FUTURE-STATE.md`** | line 742 | asserts the gauge's measuring half *"has been broken since ~07-21"* — **inherited, not verified by this lane** |
| **`knowledge/_memento-index.json`** | ≥4 chunks (`context-gauge` runbook text) | retrieval returns the ~200k prose verbatim |

**Grep noise excluded:** `200000`-substring hits in `knowledge/tokens/_raw/**/*.json` (colour alphas
`0.20000000298023224`) and `_validate_edge_extremity.py:162` (`0.7200000…`) are unrelated.

### The measured facts, stated without adjudication

- **One definition, one code read, zero imports, zero automated callers.** The *code* blast radius is
  a single file.
- **The *published-number* blast radius is much wider than the code radius**, because every consumer is
  a **prose or stamped copy** of a %-derived figure, not a call site: **27 pre-flight stamps · 4 runbook
  restatements · ≥4 retrieval chunks · 5 notes/receipts · 2 gate comment figures.** Changing the
  constant would re-scale none of them automatically.
- **No gate can catch a wrong denominator.** `check_preflight` checks that the stamped terms sum and
  that the band word matches the table — both hold identically under any denominator.
- **Three separate lanes hit this today** (Lane B, the degradation worker, the literal sweep) and
  **`notes/2026-07-29-context-degradation-research.md` reached it first, at `status: floated`.**
- ⬛ **The correct value is UNKNOWN to this lane.** Not measured, not estimated, not recommended.

---

## 5. WHAT THIS LANE REFUSED TO MEASURE, AND WHY

| refused | reason |
|---|---|
| **the harness half of cold start** | UNREACHABLE from every mount (`ds-025`). **Reported UNKNOWN. Never estimated.** |
| **any percentage, fill, points or band** | the denominator is under an open question (§4). **UNSTATED throughout.** |
| **any `bill` figure** | only 2 measured pairs exist (n=2 < `RATIO_FIRM_N=4`). This lane added none and derived none. |
| **`_build_all.py`** | 72 steps, ~3–4 min, against a measured 45 s call cap — and not this lane's to spend regardless. **Not run.** |
| **`GOOD-MORNING.md` / `_LIVE-STATE.md` prose** | **not read.** Only two machine reads touched them: `_gm_usage.split_sections` / `read_chain_tk` (region boundaries), and one `grep` for `section-sizes #3[6-9]` which returned the single `#38` line. |
| **whether the cap should be re-pointed, and to what** | **not this lane's.** ⬛ The shape is Dave's D8(a) ruling; re-pointing is a **RULING**. No fork is put here, no number is suggested, no recommendation is made. |
| **the #38-vs-now disagreement (§1)** | measured and stated; **not resolved.** |

## 6. GUARDRAILS OBSERVED

`tiktoken 0.13.0` installed as the first command and re-verified present in **every** measuring call —
no fallback path was taken; `measure_tokens` reported `tiktoken cl100k_base` throughout.
**No git. No commits. No writes to** `GOOD-MORNING.md` · `_LIVE-STATE.md` · any archive · any ledger ·
`_capture_gate.py` · `_context_gauge.py` · `_memento-index.json`. **One new file created: this one.**

**Entry points for the conductor:** `knowledge/_capture_gate.py` §`SIZE_BUDGET_TK` (:275) ·
`read_chain_tk` (:650) · `CHAIN_BUDGET_TK` (:411) · `knowledge/_gm_usage.py --sizes` ·
`knowledge/_context_gauge.py:27` · `notes/_GAUGE-LOG.md` `section-sizes` lines.
