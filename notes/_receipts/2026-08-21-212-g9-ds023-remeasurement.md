# G9 · ds-023 RE-MEASUREMENT PROGRAMME — every old-unit ceiling re-measured on its artefact in REAL tokens

**Mandate:** `s212-D7` (Dave, 2026-08-21, `knowledge/_rulings.json`). G5's four caps are the core set;
the wider G9 class (`_capture_gate.py:1445` — *"it is a CLASS, not an instance: every ceiling in this
repo stated in `tape` is now being compared against REAL tokens and is ~1.55× tighter than whoever set
it intended"*) is enumerated below the core table.

**status:** observed (all figures measured this session, `_gauge_tokens.count`, `claude-opus-5`
count_tokens endpoint, method `real` on every cell labelled REAL) · **the restamps are PROPOSED, NOT
RULED — ratifying is Dave's, G5's close condition** · provenance: session #212 · 2026-08-21 ·
repo HEAD `5a366b7`

---

## METHOD, and what it deliberately does NOT do

1. **No conversion.** `TAPE_TO_BILL = 1.57` and the measured ×1.559 corpus ratio were used for
   **nothing**. Converting is the ds-025 defect. Every figure here is a direct measurement.
2. **The gate's own extractors, imported — never reimplemented.** `_capture_gate.section_spans`,
   `read_chain_tk`, `chain_file_tk`, `_banner_unit_samples`, `banner_budget_tk`, `dofirst_index`,
   `TITLE_LINE_RE`, `BANNER_LATEST_RE`, `measure_tokens`.
3. **The baseline is measured, not inferred.** Each cap's artefact was recovered **as it stood at its
   own ruling** (`git show <commit>:<file>`), the SAME gate extractor run over it in cl100k to
   **reproduce the recorded figure** (proof the right region was cut), then the same bytes measured in
   REAL. So the restamp needs no ratio at all: it is *the artefact-at-ruling, in real tokens, times the
   headroom the ruling actually granted.*
4. **Derivation rule for every proposed ceiling, stated once:**
   `restamp = REAL(artefact at ruling) × (cap ÷ cl100k(artefact at ruling))`, **rounded UP to the
   nearest 100** — the gate's own `up()` convention in `banner_budget_tk`, which rounds up so a cap is
   never silently tightened. This is a **RESTATEMENT, not a re-dial**: it preserves the ruling's own
   tightness against its own artefact. Anything else — including "give it headroom over today's
   measurement" — is a **RE-DIAL and is Dave's alone**.
5. Cross-checked in both units throughout by toggling the gate's own `CAPTURE_GATE_NO_REAL` switch.

### Baseline reproductions (the proof the region is the right one)

| cap | ruling commit | recorded at ruling | reproduced today, cl100k | verdict |
|---|---|---|---|---|
| `SECTION_A_WARN_TK` | `e53afc4` 2026-07-27 (M-set enact) | §A **4,208 tk** | **4,208** | EXACT |
| `CORPUS_BUDGET_TK` | `31c3a94` 2026-07-28 (#33) | corpus **34,094 tk** | **34,094** | EXACT |
| `CHAIN_BUDGET_TK` | `b8b388e` 2026-07-30 (#48) | `_CHAIN.md` file **4,604** | **4,604** | EXACT |
| `BANNER_*_FALLBACK` | `19d785d` 2026-07-30 (#53) | median **1,515**, n=**58** | **1,515**, n=**58** | EXACT (header 1,939 vs the 1,968 recorded — 29 tk drift between the measurement and the wrap commit; **declared**) |

---

## ⬛ THE PROPOSAL TABLE — G5's four caps

| # | constant · current value | unit stamped in | artefact / region measured (gate extractor) | REAL today | **PROPOSED restamped ceiling (real)** | today vs the restamp |
|---|---|---|---|---|---|---|
| 1 | `CORPUS_BUDGET_TK = 36000` (`:1059`, warn-only) | **cl100k tape** (born #33, agent-derived over 34,094 cl100k) | GM whole + `_LIVE-STATE.md` whole (`check_budgets`: `corpus`) | **184,746** (GM 84,096 + LS 100,650) | **55,700** — = 52,736 real @`31c3a94` × 1.0559 (the 5.59% headroom the cap granted) | **3.32× OVER.** ⚠ the breach is **GROWTH, not the unit**: the corpus is 3.47× its #33 size in cl100k too |
| 2 | `CHAIN_BUDGET_TK = (4917, 6417)` (`:1055`, ADVISORY) | **cl100k tape** (the ruled (4500,6000) on the slice + the measured 417-tape wrapper, #48) | whole `_CHAIN.md` file — `chain_file_tk(repo)` (live render, not disk) | **19,189** (slice 14,096 + wrapper 5,093) | **(7,700 · 10,000)** — = 7,147 real @`b8b388e` × 1.0680 / × 1.3938 | **1.92× over the block-candidate.** Growth again (12,353 cl100k today vs 4,604 at #48 = 2.68×). ★ the **wrapper alone is 5,093 real** — 12× the 417 pinned as "a snapshot, not a constant" |
| 3 | `BANNER_BUDGET_FALLBACK_TK = (4000, 5000)` (`:950`) | **cl100k tape** (born as the cap, M-set 2026-07-27; demoted to declared fallback #53) | ⚠ **NO ARTEFACT OF ITS OWN — PICKED, never measured.** It fires only when `_banner_unit_samples` returns < `BANNER_ARCHIVE_MIN_N` (10) | **n/a — path UNREACHABLE in this repo today: the archive yields n=211 samples** | **(6,400 · 7,800)** — the fallback's *position relative to the derived cap* held constant and measured in real: #53's derived pair was (5,000 · 6,100) cl100k = **(7,900 · 9,500) real**; 4000/5000 and 5000/6100 of that. **ALTERNATIVE, simpler:** adopt **(7,900 · 9,500)** = #53's derived pair in real | dormant — cannot fire while the archive parses. Live cap today is `banner_budget_tk()` = **(10,700 · 15,200) real**, derived from header 3,001 + 2 × banner (median 3,845 / p75 6,095), n=211 |
| 4 | `SECTION_A_WARN_TK = 4500` (`:929`, ADVISORY, warn-only) | **cl100k tape** (§A measured 4,208 cl100k at the 2026-07-27 ruling) | GM `§A` span — `section_spans(lines)["§A"]` | **6,957** (198 lines) | **7,200** — = 6,716 real @`e53afc4` × 1.0694 (the 6.94% headroom the ruling granted) | ✅ **PASSES with 3.4% to spare.** ★ **The warn the gate prints today is a PURE UNIT ARTEFACT — a false positive.** §A has not grown: 4,208 → 4,375 cl100k in 25 days (+4.0%) |

### What the live gate says right now (`check_budgets(repo)`, tier `real`, unedited)

```
[WARN] §A 6,957 tape … past the 4,500 tape backstop
[WARN] M10 corpus (GM + _LIVE-STATE whole): 184,746 tape … warn 36,000 tape
[WARN] M10 read chain OVER THE BLOCK-CANDIDATE … 19,189 tape … block-candidate 6,417 tape
[WARN] banner region: 36,539 tape … block ~23,864 bill (AT 2c MINIMUM, 1 PRIOR)
[WARN] compactable: 77,139 tape … warn ~12,560 bill
```

⚠ **Every one of those figures labelled `tape` is a REAL measurement.** `measure_tokens` has returned
`real` since #82-D1 (`API-KEY.txt` present), so the gate is already comparing real tokens against
cl100k ceilings — **which is exactly the condition G9 exists to close**, live and printing today.

### ⛔ SECOND FINDING, NOT IN SCOPE TO FIX — the `bill` figures are DOUBLE-COUNTED

`bill_of()` (`:407`) multiplies by `TAPE_TO_BILL = 1.57` and the gate applies it to numbers that are
**already real**. #53 proved there is no separate `bill` phenomenon — 1.57 *was* the cl100k→Claude
mismatch. So every `~N bill` figure the gate prints today is **real × 1.57, overstated by ~57%**
(e.g. corpus "~290,051 bill" against a true 184,746). The comparison verdicts are unaffected —
`bill_of` is monotone linear and both sides pass through it — but every published `bill` figure is
wrong. ⬛ **Dave's: retire `bill_of` or re-rule it.** Named here, untouched.

---

## THE WIDER G9 CLASS — every other ceiling stated in an old unit

| constant | value · unit | artefact measured | REAL today | status / proposal |
|---|---|---|---|---|
| `SIZE_BUDGET_TK["compactable"] = 8000` (`:365`, warn-only, block withdrawn #39) | cl100k tape | GM whole − §A (`check_budgets`: `compactable`) | **77,139** (cl100k 48,837; region ratio ×1.580) | ⚠ **NOT restampable by measurement — 8,000 was PICKED by Dave (D7 amendment 2026-07-27), not derived from a measurement.** A restamp would be a conversion. ⬛ **Dave re-picks in real.** Today's region is 9.6× the ceiling either way |
| `TITLE_CAP_TAPE = 120` (`:915`, BLOCKING, ruled #60-D8) | cl100k tape | the `TITLE THE NEXT CHAT` line (`TITLE_LINE_RE`) | **55** (cl100k 30) | ✅ **binds fine — no action forced.** Ruling-era title (`affe15d`) = 29 cl100k / **63 real**, so the cap granted 4.14× headroom. Headroom-preserving restamp would be **260**; recommended instead: **keep 120 and relabel the unit real** — it is still 2.2× today's line, and 260 would make a blocking label cap meaningless. ⬛ Dave's pick between the two |
| `DOFIRST_INDEX_TK_MAX = 700` (`:1445`, G1) | **already REAL** — re-picked #82 over a measured 531 real | `dofirst_index(gm_lines)` | **681** (28 items; cl100k 417) | ✅ **NOT an old-unit ceiling** — already restamped. ⚠ **BUT: at 681/700 it has 2.7% left.** ⛔ **AND ITS COMMENT LIES:** the block says *"RAISED 700 → 800 AT #110"*; `#111` (`c853b0a`) reverted the value to **700** and left the comment standing. Two readers of one constant. ⬛ Dave's (G1) |
| `STAMP_PRECISION_TK = 100` (`:930`) | cl100k tape | — | — | **NOT A CEILING.** It is the granularity of the `§A N.NK tk` stamp, which is 100 in whatever unit the stamp writes. Carries over unchanged. No restamp owed |
| `BYTES_PER_TOKEN = 3.53` (`:369`) | cl100k, measured on GM 2026-07-27 | GM whole | **2.149 bytes/real-token** (180,706 bytes ÷ 84,096 real; cl100k today 3.396) | ⚠ the ESTIMATE tier's divisor reads **~58% high** against real, so any ESTIMATE-labelled figure understates by that much. Restamp candidate: **2.15**. ⬛ Dave's — it only fires when both real and tiktoken are unreachable |
| `TAPE_TO_BILL = 1.57` (`:401`) | — | — | — | see the double-count finding above. ⬛ Dave's |
| `BANNER_ARCHIVE_MIN_N = 10`, `BANNER_HEADROOM_PCTL = 75` | counts / percentile | — | — | **unit-free.** Untouched by the re-denomination |

### Measured real ÷ cl100k, per region, today (reported — never applied)

GM whole **1.580** · `_LIVE-STATE.md` **1.545** · §A **1.590** · banner region **1.600** ·
`_CHAIN.md` file **1.553** · corpus **1.561** · archived-banner median **1.589** · DO-FIRST index
**1.633** · title line **1.833**. Spread 1.55–1.83 across registers — **confirms #53's finding that no
single multiplier can re-denominate this corpus, which is why nothing above was converted.**

---

## ARTEFACT-GONE / REFUSALS

- **None ARTEFACT-GONE.** Every one of the four core caps' artefacts exists and was measured.
- **One NO-BASELINE:** `BANNER_BUDGET_FALLBACK_TK` was never derived from a measurement (picked at the
  M-set, demoted to fallback at #53), and its code path is **unreachable in this repo today** (n=211
  archived banner samples against a minimum of 10). Both proposals for it are stated above; neither is
  a measurement of that constant's own artefact, because it has none.
- **One EXTRACTOR-DIVERGENCE, declared:** running today's `chain_file_tk` against the `b8b388e` tree
  returns **8,283 cl100k, not the recorded 4,604** — because it re-renders with **today's**
  `_gen_chain`, whose wrapper has grown from 417 to 3,454 cl100k. The baseline in the table is
  therefore the **on-disk `_CHAIN.md` at `b8b388e`**, which reproduces 4,604 exactly. Named, not
  papered over.
- **No refusals from the gauge.** `tiktoken` present, API key readable, `measurement_tier()` = `real`
  on every call.

## NOTHING WAS CHANGED

No constant edited. `_capture_gate.py`, `_gauge_tokens.py`, `GOOD-MORNING.md`, `_LIVE-STATE.md`,
`_CHAIN.md`, `knowledge/_rulings.json`, `knowledge/_state.json` untouched. `_build_all.py` not run.
This receipt is the only write.

---

## EXACT COMMANDS RUN

```bash
pip install tiktoken --break-system-packages          # gauge refuses without it — that refusal is correct
cd /sessions/charming-practical-davinci/mnt/UX-design

# key + real tier reachable
python3 -c "import _gauge_tokens as g; print(bool(g.read_key()), g.count('hello world'))"   # True (9,'real')

# live regions, both units, via the gate's own extractors  (/tmp/ds023/m1.py)
#   section_spans / chain_file_tk / read_chain_tk / BANNER_LATEST_RE, each measured twice:
#   once with CAPTURE_GATE_NO_REAL unset (real) and once set (cl100k)
python3 /tmp/ds023/m1.py

# banner dataset + derived cap, both units            (/tmp/ds023/m2.py, m3.py)
#   _banner_unit_samples(REPO) ; banner_budget_tk(REPO, lines, latest_idx)
python3 /tmp/ds023/prewarm.py && python3 /tmp/ds023/m2.py && python3 /tmp/ds023/m3.py

# title line + DO-FIRST index                          (/tmp/ds023/m4.py)
python3 /tmp/ds023/m4.py

# the live gate verdicts, read-only                    (/tmp/ds023/m5.py)
python3 -c "import _capture_gate as G; print(G.measurement_tier()); print(G.check_budgets('<repo>'))"

# baselines: the artefact AS IT STOOD AT ITS RULING    (/tmp/ds023/hunt.py, base.py, chain.py)
#   git show <c>:GOOD-MORNING.md|_LIVE-STATE.md|_CHAIN.md|_GM-ARCHIVE.md  → temp tree
#   → same gate extractor → reproduce the recorded cl100k figure → then measure REAL
python3 /tmp/ds023/hunt.py e53afc4 559b9ee 3ecd2ea 8ab6ee0 31c3a94 eb24fa8 b8b388e 19d785d
python3 /tmp/ds023/base.py
python3 /tmp/ds023/chain.py

# the DOFIRST 800→700 revert
git show c853b0a -- knowledge/_capture_gate.py | grep "DOFIRST_INDEX_TK_MAX = "
```

⚠ Measurement scripts live in the sandbox's `/tmp/ds023/` and **do not survive the session**
(NON-REPO). Everything they produced is transcribed above; each is ~30 lines of `import
_capture_gate` plus the extractor calls named in the comments, re-writable from this receipt.

---

## ⬛ WHAT IS OWED FROM DAVE (G5's close condition)

1. **Ratify or re-dial the four restamps:** corpus **55,700** · chain **(7,700 · 10,000)** · banner
   fallback **(6,400 · 7,800)** *or* **(7,900 · 9,500)** · §A **7,200**.
2. **Note what ratification alone does NOT fix:** three of the four are still breached after the
   restamp, and the breach is **real growth**, not the unit. Corpus 3.3× over, chain 1.9× over, banner
   region 2.4× over its own live derived block. Only §A goes green.
3. **The `bill_of` double-count** — retire or re-rule.
4. **`SIZE_BUDGET_TK["compactable"]` and `TITLE_CAP_TAPE`** need a **re-pick**, not a restamp: their
   numbers were picked, not measured, so no measurement can restate them honestly.
5. **`DOFIRST_INDEX_TK_MAX`'s comment/value contradiction** (700 in code, "raised to 800" in its own
   comment) — a G1 item, one line to settle.
