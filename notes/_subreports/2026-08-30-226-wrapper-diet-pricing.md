# `#226`-`wrapper-diet-pricing` — the `_gen_chain.py` wrapper, measured block by block, and three trims priced

session: `#226` · 2026-08-30
window: `#226` conductor window — Opus analysis sub
sub index: `wrapper-diet-pricing`
brief: conductor's inline brief (PRICE, DO NOT CUT; hard fence listed in §Fence honoured)
tokens: `UNMEASURED — this seat cannot read its own message.usage; the conductor holds the figure`
review page: `reviews/WRAPPER-DIET-2026-08-30-v1.html` (live, four readings side by side)

## VERDICT

**The wrapper is not prose. It is your open-work list, printed in full, on the boot path.**
Of `_gen_chain.py`'s **13,061 tape** of generated wrapper, **12,555 (96.1%) is `state_block()`** —
the ⬛ OPEN WORK section — and **11,407 of that is Dave's 125 items rendered as
`id + title + closes_when`, one row each**. The BANNER, the title line and the FOOTER — *all* the
ratified guidance prose a cold session reads — total **506 tape**.

⇒ **`#225`'s question 1 option (a) — "cut >~9,000 of 12,741 tape out of `_gen_chain.py`'s
generated prose" — cannot be done.** There is only 506 tape of prose in the wrapper. Priced and
measured: an aggressive prose diet buys **258 tape** and moves the ratio from **55.82% → 55.19%**.
Both reds survive it. That option is dead, and it should be struck rather than deferred.

The live lever is a different decision, and it is Dave's: **does the chain print the worklist's
bodies, or a pointer to them?** Three readings are priced below and rendered side by side on the
review page. One of them (**C**, ids-only) takes the ratio to **29.61%** and clears **all four** of
today's red selftest lines. One (**D**, titles kept / close conditions dropped) keeps the worklist
skimmable at boot and clears two of four. A variant (**D′**) squeaks green at **39.20%** with
0.80 points of headroom.

COUNTS: findings `12` · ruling-shaped `4` · UNPROVEN `4`

⚠ **UNIT, STATED ONCE AND IT GOVERNS EVERY FIGURE BELOW:** all numbers are
**`tiktoken cl100k_base` tape**, taken from `_capture_gate.measure_tokens` — the same call
`_gen_chain.build()`'s fixed point and `read_chain_tk` use. No second counter was written for this
work. See finding 10: the chain file *calls* these numbers `real` and they are not.

## Findings

1. **THE WRAPPER, SECTION BY SECTION, ON THE REPO'S OWN INSTRUMENT.**
   Live tree at `e29c25b` + 4 unrelated dirty paths. `GOOD-MORNING.md` **40,957**; chain slice
   **9,803** (GM header+★LATEST **7,171** + LS ⏱ LATEST delta **2,632**); `_CHAIN.md` file
   **22,864**; **wrapper = file − slice = 13,061**; ratio **55.82%** against the `<40%` floor.

   | block the generator emits | tape | bytes | lines |
   |---|---:|---:|---:|
   | `BANNER` (head) | **331** | 1,192 | 19 |
   | `title_block` (#73 hoist) | **62** | 227 | 6 |
   | separator head↔body (`\n`) | 1 | 1 | 1 |
   | separator GM↔LS delta | 2 | 7 | 1 |
   | **`state_block()` — ⬛ OPEN WORK** | **12,555** | 46,046 | 141 |
   | `FOOTER` (fixed-point sentence) | **113** | 426 | 10 |
   | **wrapper, by difference** | **13,061** | — | — |

   Blocks sum to **13,064**; the 3-tape gap is tokenizer sub-additivity across the joins, not a
   missing block. **Marginal** cost (file minus file-without-block) was measured separately and
   agrees to ±1 on every block: BANNER 330, title 62, state_block 12,555, FOOTER 113.

2. **INSIDE `state_block()`, AND THIS IS THE WHOLE STORY.**
   heading **24** · counts line **34** · "no number here was typed" provenance note **69** ·
   DECLARED DEBT paragraph **89** · **DAVE'S 125 rows 11,407** · MINE 140 ids (one line) **878** ·
   store-gate line **26**. Dave's rows average **91.3 tape** (median 85; fattest `W-85` at 193).
   ★ Note the asymmetry already in the design: **"mine" is already pointer-shaped** — 140 items in
   878 tape, ids only, bodies in the store. Dave's 125 items cost **13× more** for **fewer items**.
   Inside the BANNER: do-not-hand-edit comment **144** · "do NOT open GM to check" **90** ·
   "everything else is RETRIEVAL" + the search command **95**.

3. **`#225`'s OPTION (a) IS ARITHMETICALLY IMPOSSIBLE — PRICED, NOT ASSERTED.**
   Candidate **B** below cuts the BANNER to four lines, drops the title's parenthetical and reduces
   the FOOTER to one sentence: **wrapper 12,803 (−258), file 22,606, ratio 55.19% — RED**, and all
   four M10-family selftest lines unchanged. The `#225` report's own phrasing ("that prose is
   ratified guidance a cold session reads") was right about the *cost* of cutting it and wrong
   about the *size* of it by a factor of ~25.

4. **FOUR RED LINES TODAY, NOT TWO, AND ALL FOUR TRACE TO THE SAME WRAPPER.**
   `python3 knowledge/_capture_gate.py --selftest` exits **1** with three selftest failures:
   - *"M10: a fat §A/§C warned the CHAIN — the re-point did not take"*
   - *"M10: an ordinary chain warned — the budget fires on everything"*
   - *"#70/#71 non-catch: `_gen_chain.py --selftest` is NOT green — the regime's only net for a
     skipped wrap (the stale-title bite, one session late) is broken"*

   and `python3 knowledge/_gen_chain.py --selftest` exits **1** on exactly one bite:
   *"✗ is materially smaller than GOOD-MORNING.md (22,864 vs 40,957 …, 55.8% of it, floor <40%)"*.
   ⛔ **The third `_capture_gate` failure is a CASCADE, not an independent defect**
   (`_capture_gate.py:7505-7508` calls `_gen_chain.selftest()` and fails on rc≠0). So the ratio red
   is also holding the skipped-wrap net's certification hostage. `#225` reported two reds; there
   are four red lines, from two roots, both in the wrapper.

5. **THE MECHANISM BY WHICH THE LIVE WORKLIST REACHES A TEMP-DIR FIXTURE: `state_block()` IS
   REPO-BLIND.** `_gen_chain.build(repo)` threads `repo` everywhere *except* here —
   `state_block()` takes no argument and calls `_state.load()`, whose default is
   `_state.STORE`, an **absolute** path at `<repo>/knowledge/_state.json`. So a selftest fixture
   whose entire GOOD-MORNING.md is 214–347 tape gets the production 125-row worklist stapled to its
   chain and lands at **13,232 tape**, past `CHAIN_BUDGET_TK`'s block-candidate of 10,000. Driven,
   not inferred: `_warns_for(td)` → *"M10 read chain OVER THE BLOCK-CANDIDATE … 13,232 tape …"*;
   with a lean block substituted the same call returns **no M10 warn at all**.

6. **THE THREE CANDIDATES, MEASURED THROUGH `build()`'s OWN FIXED POINT.**

   | reading | what changes | wrapper | chain file | chain ÷ GM | red lines left |
   |---|---|---:|---:|---:|---:|
   | **A — do nothing** | — | 13,061 | 22,864 | **55.82% RED** | 4 |
   | **B — prose diet** | BANNER/title/FOOTER trimmed hard | 12,803 | 22,606 | **55.19% RED** | 4 |
   | **C — OPEN WORK → pointer** | Dave's 125 print as **ids only** (the shape "mine" already uses) | **2,326** | **12,129** | **29.61% GREEN** | **0** |
   | **D — titles kept** | Dave's 125 print `id + title`; `closes_when` → retrieval | 7,117 | 16,920 | **41.31% RED** | 2 |
   | **D′ — D, plus MINE→pointer and the provenance sentence dropped** | as D | 6,254 | 16,057 | **39.20% GREEN** | 0 |

   Each candidate's rendered `_CHAIN.md` was written to scratch and re-measured; the fixed point
   converged in 2 passes in every case. ⚠ **D′ clears the floor by 0.80 points ≈ 328 tape ≈ 7 more
   of Dave's items** at today's 91-tape average row. C clears it by 10.4 points.

7. **THE M10 BITES ARE A TWO-SIDED VICE — A WRAPPER CAN BE TOO THIN.** The bite immediately after
   the two failing negative controls requires a 24-fat-line banner fixture **to** warn
   (`_capture_gate.py:6872-6875`). Driven with a ~336-tape wrapper the fat-banner fixture lands at
   **6,545 — under the 7,700 warn — and that bite flips red.** Candidates C (fixture file 8,376)
   and D (13,167) both stay above it. **The safe band for the wrapper is roughly 1,670–7,486 tape**,
   derived from the fixtures' own sizes against the 7,700 warn: below ~1,670 the fat-banner bite
   dies (its fixture base is ~6,030), above ~7,486 the two negative controls die again (their
   fixture base is 214). ⚠ **C at 2,326 sits comfortably inside; D at 7,117 sits ~370 tape below
   the ceiling — about EIGHT more title rows at 44.6 tape each before D re-breaks the very bites it
   was chosen to fix.** A further "while we're here" trim to C's BANNER would spend C's floor
   margin; a few more open items would spend D's ceiling margin. Both ends are live.

8. **NO CANDIDATE MAKES THE LIVE M10 BUDGET PASS, AND NOBODY SHOULD SAY IT DOES.**
   `CHAIN_BUDGET_TK = (7700, 10000)`; the live chain file is 22,864 today and **12,129 even under
   C** — still over the block-candidate, so *"M10 read chain OVER THE BLOCK-CANDIDATE"* keeps firing
   on the real repo. It is a **warn** by Dave's `#18` ruling and a bite asserts it may never reach
   FAILS. What the candidates fix is the **selftest**, whose fixtures were being poisoned by the
   live wrapper (finding 5). ⛔ Do not let this be reported as "M10 goes green".

9. **⛔ A NEGATIVE WRAPPER IS REACHABLE TODAY, AND THE FAT WRAPPER IS THE ONLY THING HIDING IT.**
   On the fat-banner fixture the generator prints, verbatim:
   `FILE 6,554 tiktoken cl100k_base = slice 9,107 + wrapper -2,553`. The slice measured **9,107
   `real`**; the whole file — which *contains* the slice — measured **6,554 `tiktoken
   cl100k_base`**. Two instruments in one sentence. **Cause, proven by single-variable isolation:**
   `_gauge_tokens.count()` returns `"real"` on any **cache hit** in `knowledge/.token-cache.json`
   (`_gauge_tokens.py:238-241`), and this environment cannot reach the API at all (a fresh random
   string measures `tiktoken cl100k_base`), so *cached* text reads `real` and *fresh* text does not.
   Re-run the identical probe with `CAPTURE_GATE_NO_REAL=1` — the CI shape — and it resolves:
   slice 6,070, file 6,574, **wrapper +504**. ⇒ The **M10 UNIT BITE** (*"the FILE figure does not
   exceed the SLICE"*) is one fixture away from firing on any machine holding that cache, and
   today's 13,061-tape wrapper is what keeps the sum positive. **A leaner wrapper unmasks this —
   locally only.** Class: [[gate-cannot-pass-in-one-environment]].

10. **THE CHAIN'S STAMPED UNIT WORD DISAGREES WITH THE METHOD THAT PRODUCED THE NUMBER — IN THE
    SAME COMMAND'S OUTPUT.** `_CHAIN.md`'s footer on disk reads **`22,864 real`**; the command that
    byte-matched it prints `FILE 22,864 tiktoken cl100k_base`. `unit_word()` asks
    `measurement_tier()`, which probes with the one-character string `"x"` — a cache hit, so it
    answers `real` — while every real-sized measurement in the same run falls to tiktoken. This is
    `W-273`'s *"`_tier_probe()` lies (`real` on cl100k)"* found from the other end, and it is
    **live in the one file every cold session reads**. It does not change the ranking of the
    candidates; it does mean the exact percentages would move on a machine that can reach the API.

11. **`#225`'s #226 FORECAST HAS LANDED AND IT WAS RIGHT — IT IS NOW A MEASUREMENT, NOT ARITHMETIC.**
    `#225` forecast GM ≈ 38,709 and the ratio ≈ **55.1% RED** once the #224 ★ PRIOR banner rolled.
    Measured today: GM **40,957**, ratio **55.82%**. The premise that a leaner GM makes this ratio
    worse is confirmed on the tree, not on paper. ⚠ And the numerator moved the *wrong* way too:
    the wrapper grew from `#225`'s 12,741 to **13,061 (+320)** across one wrap, because
    `state_block()` grows with the store.

12. **THE SWAP CANDIDATE C PROPOSES IS THE ONE `state_block()`'s OWN DOCSTRING ANTICIPATED.**
    It says, verbatim in `_gen_chain.py:407-415`: the block is additive *"and not yet a swap"*,
    *"ADD now, verify against the prose for the two drill passes (`#87-D1`, N=2), CUT at the swap"*,
    with the duplication called *"the declared price of doing it in the right order"*. Both drill
    passes are long past. **C is not an invention; it is the deferred half of a plan already written
    into the generator.** ⛔ It is still a cut on the boot path and therefore Dave's, not a sub's.

## RULING-SHAPED QUESTIONS

1. **WHICH READING — A, C, D or D′?** The live page renders all four with real text.
   **Recommend C.** It is the only reading that clears all four red lines, it clears the `<40%`
   floor with 10.4 points of headroom (so it survives store growth, which D′ does not), it is the
   swap the generator's own docstring deferred, and it makes the chain shippable inside a Gumdrop
   pack without carrying Apollo's private worklist. **The honest price of C is real and it is
   Dave's to accept:** a cold session boots knowing *how many* items are open and *which ids*, but
   not *what they are* without one `_state.py` call. If that trade is unacceptable, **D′** is the
   next-best and it is green — but it is green by 328 tape and will go red again within about seven
   new items, which is the same trap `#225` just escaped.

2. **DOES OPTION (a) FROM `#225` QUESTION 1 GET STRUCK?** It is priced dead (finding 3). Leaving it
   on the list costs a future session the same investigation. **Recommend: struck, with finding 3
   as the receipt.** ⚠ `#225`'s option (b) — re-defining the denominator — is *not* dead, and if C
   or D′ is taken it becomes unnecessary rather than wrong; that is worth saying out loud so the
   next lean-GM wrap does not re-derive it.

3. **THE UNIT WORD (finding 10): fix the WORD or fix the PROBE?** `_CHAIN.md` says `real` about a
   `tiktoken cl100k_base` number. (a) Make `unit_word()` take its tier from the *measurement that
   was actually taken* (the `how` that `build()` already holds and discards) rather than from a
   one-character probe. (b) Make `_tier_probe()` probe with text that cannot be a cache hit.
   (c) Leave it and record it against `W-273`. **Recommend (a)** — the method already travels with
   the number at that call site (`#83`'s own fix); the word is the one place it is dropped again.
   ⛔ Not touched here: it is a ds-021 vocabulary motion and outside this lane's fence.

4. **DOES THE `<40%` FLOOR STILL MEAN WHAT IT MEANT?** With the numerator now 57% store rows rather
   than prose, the assertion is largely comparing *the size of the worklist* to *the size of GM*.
   That is a defensible thing to assert — but it is not what the sentence in the FOOTER says it
   asserts (*"above it, the wrapper is carrying more than the slice"*). ⛔ **Dave's constant, not
   touched, not recommended for movement by a sub** — raised only because after C the floor would
   be passing for a reason different from the one its own prose gives.

## CONSEQUENCES AND PITFALLS (Dave `#165`)

- ⛔ **THE WRAPPER HAS A FLOOR AS WELL AS A CEILING: ~1,670 to ~7,486 tape.** Finding 7. Below the
  floor, *"M10: a 24-fat-line banner did not warn the chain"* goes red; above the ceiling the two
  negative controls that are red today come back. C at 2,326 has ~650 tape of floor margin;
  **D at 7,117 has only ~370 tape of CEILING margin — roughly eight more of Dave's items and D
  re-breaks the bites it was picked to fix.** D is a fix with an expiry date; C is not.
- ⛔ **DO NOT REPORT ANY CANDIDATE AS "M10 GREEN".** Finding 8: the live chain file stays over the
  block-candidate under every reading. What clears is the **selftest**.
- ⚠ **A LEANER WRAPPER UNMASKS THE NEGATIVE-WRAPPER DEFECT (finding 9) ON ANY MACHINE HOLDING
  `knowledge/.token-cache.json`.** In CI (no cache, no key) it does not arise — proven both ways
  with `CAPTURE_GATE_NO_REAL=1`. **If C is taken, expect a local-only UNIT-BITE red that CI cannot
  reproduce**, and recognise it as the tier defect rather than as the trim's fault.
- ⚠ **THE `#70/#71` CASCADE CUTS BOTH WAYS.** Any change that leaves `_gen_chain --selftest` red
  keeps a `_capture_gate` failure alive too. A wrap that fixes M10's negative controls but not the
  ratio (i.e. **D**) will still show `_capture_gate.py --selftest` exiting 1, and it will look like
  the fix did not take.
- ⚠ **CUTTING BODIES IS A BOOT-PATH CUT, AND THE ORDER MATTERS** —
  [[home-by-addition-then-cut]]. The bodies' other home already exists and was probed
  (`python3 knowledge/_state.py`), which is what makes C legal at all. **Do not cut and then look
  for the home.**
- ⚠ **NO GATE PARSES AN OPEN-WORK ROW — but one parses the block's shape.** The bites assert the
  heading is computed and that a failed store yields a REFUSAL, never an empty-looking worklist
  (`_gen_chain.py:423-434`). Any candidate must keep both refusal branches intact; a "pointer"
  block that renders an empty ids list on a store failure would be the confident-blank class the
  module's docstring exists to refuse.
- ⚠ **THE CHAIN SHIPS INSIDE EVERY GUMDROP PACK**, where `_state.json` is the designer's, not
  Apollo's. 125 rows of Apollo's private worklist in a shipped boot file is an argument for C that
  has nothing to do with the ratio — and an argument against D, which ships the titles.
- ⚠ **`state_block()`'s REPO-BLINDNESS (finding 5) IS A DEFECT IN ITS OWN RIGHT AND SURVIVES EVERY
  CANDIDATE.** Even under C, a fixture chain carries the live store's counts. Threading `repo`
  into `state_block()` is a small, local change and would make the selftest fixtures honest —
  ⛔ **not done here: `_gen_chain.py` is inside this lane's DO-NOT-EDIT fence.**
- ⚠ **THIS REPORT HAS NO `knowledge/_state.json` ROW** (the store is outside this lane's fence), so
  it **WILL red `_gate_doc_rows.py --check` at pre-stage** until the conductor mints one —
  the same standing behaviour `#225`'s report declared.
- ⚠ **THE REVIEW PAGE IS A NEW FILE AT `reviews/WRAPPER-DIET-2026-08-30-v1.html`** and is likewise
  unrowed. It is versioned `-v1` and overwrites nothing.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN — no candidate was enacted.** Every candidate figure comes from an in-memory render
  that reuses `build()`'s real fixed point and the real slicer, with `gc.state_block` substituted
  in-process. Nothing was written into the tree and `_gen_chain.py` was not edited. Price to prove
  properly: one edit + `python3 knowledge/_gen_chain.py` + `--check` + both selftests, ~6k tokens.
- **UNPROVEN — "C clears all four red lines" is proven BITE BY BITE, not by one green run.** The
  three M10-family bites were driven individually through `_capture_gate._warns_for()` and the
  ratio bite arithmetically against the same floor the bite uses; I did **not** run
  `_capture_gate.py --selftest` end to end against a patched generator. Price to prove: one patched
  run, ~3k tokens.
- **UNPROVEN — the API tier is unreachable from this sandbox**, so no figure here is a genuinely
  `real` measurement (finding 10). The ranking of the candidates is instrument-independent — every
  figure is on one instrument — but the exact percentages would move on a machine that can reach
  the endpoint. Price to prove: re-run finding 1's decomposition where the API is reachable, ~4k.
- **CLAIMED — D′'s "about seven more items" of headroom** uses today's 91.3-tape average Dave row
  against 328 tape of margin. It is arithmetic on today's store, not a measurement of a future one;
  a fat row (`W-85` is 193) halves it.

## Fence honoured

`_gen_chain.py` NOT edited · the `0.40` floor and `CHAIN_BUDGET_TK` NOT moved · `_CHAIN.md` NOT
regenerated into the tree (`--check` was run and is GREEN; the two selftests write and restore their
own copies, and `git status` was verified unchanged afterwards) · `GOOD-MORNING.md`,
`_LIVE-STATE.md`, `_CARRIES.md`, `knowledge/_rulings.json`, `knowledge/_state.json`, `dist/` and the
manifest all untouched · no commits, no pushes · scratch under
`/sessions/stoic-pensive-feynman/w226/` (sandbox-local; `/tmp` and `/var/tmp` were both ENOSPC).
Two files created, both new: this report and the review page.

## REPLAY-THESE

- `python3 knowledge/_gen_chain.py --check` — expect exit **0** and
  `✅ _CHAIN.md is FRESH … FILE 22,864 tiktoken cl100k_base = slice 9,803 + wrapper 13,061 · fixed
  point in 2 pass(es)`. **(~0.3k tk)** ★ Note the sentence names `tiktoken cl100k_base` while the
  file it just matched stamps `real` — finding 10 in one line.
- `python3 knowledge/_gen_chain.py --selftest` — expect exit **1**, exactly one bite:
  `✗ is materially smaller than GOOD-MORNING.md (22,8xx vs 40,957 …, 55.8% of it, floor <40%)`.
  **(~2.5k tk)**
- `python3 knowledge/_capture_gate.py --selftest` — expect exit **1** with three selftest failures:
  the two M10 negative controls and the `#70/#71 non-catch` cascade. **(~5k tk)**
- The wrapper decomposition (finding 1), one line, the repo's own instrument:
  `python3 -c "import sys,os;sys.path.insert(0,'knowledge');import _capture_gate as c,_gen_chain as g;print(c.measure_tokens(g.state_block())[0])"`
  — expect **12555** (± store growth). **(~0.5k tk)**
- The negative wrapper, both ways (finding 9), on a `fat_banner=24` fixture:
  with the cache → `wrapper -2,5xx`; with `CAPTURE_GATE_NO_REAL=1` → `wrapper +504`. **(~1k tk)**
- ⬛ **OWED, NOT RUN:** enact the chosen reading and run `--check` + both selftests end to end
  (~6k tk). Dave picks the reading first.
