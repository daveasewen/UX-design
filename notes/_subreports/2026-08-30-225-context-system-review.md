# `#225`-`ctx` — deep analysis of the context/memory system: what a cold session pays, and why

session: `#225` · 2026-08-30
window: analysis lane (read-only)
sub index: `ctx`
brief: conductor's inline commission (Dave, `#225`, verbatim in § Commission below)
tokens: `UNMEASURED — a sub cannot observe its own transcript usage from this seat` (the
conductor's `_checkin.py` reads the main chain only; this seat writes to a transcript it
cannot see, the same structural blindness `#222`/`#223` declared)

## VERDICT

**The architecture is right and the instrument that prices it is broken, and the second fact
has been hiding the first for at least seventeen sessions.** The shape Dave built — a generated
contract at the front, everything else behind two-stage retrieval, stores as the authority,
rituals to roll it forward — is the correct shape, and `_CHAIN.md:4` states the design
intention exactly. But `_CHAIN.md` has grown to **52.6% of the file it exists to avoid reading**
(45,656 cl100k vs `GOOD-MORNING.md`'s 86,879 cl100k), the chain generator's own `<40%` floor is
structurally red because of it, and the boot constant the whole gauge rests on is **out of band
for the fifteenth consecutive session** (live `_checkin.py` this morning: **boot 79,074 real**
against `BOOT_FIRSTTURN_TK = 56_749 ± 1_154`). Underneath both sits a defect neither had been
attributed to: **`_capture_gate._tier_probe()` measures the one-character string `"x"`, which is
a permanent cache hit, and therefore reports tier `real` in an environment where every actual
measurement falls back to cl100k.** Consequences: the chain's own footer inscribes
"**45,656 real**" onto a cl100k number; `_gauge_tokens.measure_boot()` sums a cl100k term and a
real term and prints the total under the header "unit: REAL Claude tokens"; the COULD-NOT-ASK
tier refusal built precisely to catch this cannot fire; and the apparent 33% chain reduction at
`#224` (68,404 → 45,656) is, on the arithmetic, **a unit switch rather than a diet**. Every
region of the brief was covered. Nothing was written outside this file.

COUNTS: findings 14 · ruling-shaped 6 · UNPROVEN 5

## Commission (Dave, `#225`, verbatim)

> "I'd really like to find other ways to streamline this, are we using progressive reveal
> techniques, indexing, on demand retrieval etc well. Are there tasks to take care of to strip
> out some of the information being carried forward. Maybe we need a deep analysis of this whole
> system, have we even designed it well?"

## A note on units before any figure is read

⛔ **Every figure below carries its unit, and the units are NOT interchangeable**
[[measure-dont-convert-units]]. Two units appear:

- **real** — Claude tokens, `message.usage` or the `count_tokens` API. Reachable only via
  `API-KEY.txt` or a `knowledge/.token-cache.json` hit (`_gen_chain.py:693`).
- **cl100k** — `tiktoken cl100k_base`. What this seat can measure directly.

**The count-tokens API is NOT reachable from this sandbox** (probe: `_gauge_tokens.count(chain)`
returned `(45656, 'cl100k-estimate')` in 0.34s — a fast fall-through, not a timeout on a real
call). So file sizes here are **cl100k, MEASURED**. Where a real figure is needed it is either
quoted from a first-hand `message.usage` reading, or presented as an explicitly-labelled
**CONVERSION** with its ratio's provenance — never as a measurement.

**THE RATIO, MEASURED IN THIS REPO'S OWN CACHE.** `knowledge/.token-cache.json` holds 6,909
real counts keyed on content hash. Thirteen of them belong to files still on disk unchanged, so
both units are available for the same bytes:

| real | cl100k | ratio | file |
|---|---|---|---|
| 237,203 | 153,924 | 1.541 | `notes/_MEMENTO-DECISIONS.md` |
| 4,259 | 2,844 | 1.498 | `knowledge/_RUNBOOK-decision-audit.md` |
| 4,209 | 2,805 | 1.501 | `_STANDARDS.md` |
| 2,799 | 1,858 | 1.506 | `AGENTS.md` |
| 2,087 | 1,344 | 1.553 | `README.md` |
| *(+8 more runbooks, 1.447–1.590)* | | | |

**n=13 · median 1.510 · mean 1.526 · range 1.447–1.590.** Independently corroborated by the
runbook's own retired `TAPE_TO_BILL = 1.57` (n=2, provisional —
`knowledge/_RUNBOOK-context-gauge.md:645`) and by `MEMORY.md`, measured at **8,470 real** at
`#109` and **5,669 cl100k** today → 1.494.

---

## 1. PROGRESSIVE REVEAL — what a cold session pays before doing any work

### 1a. The floor, decomposed

| component | figure | unit | method |
|---|---|---|---|
| **first turn** (system prompt + tool schemas + deferred-tool list + MCP server instructions + `MEMORY.md` + `CLAUDE.md`) | **79,074** | real | MEASURED — `_checkin.py` on the `#225` conductor transcript, run from this seat 2026-08-30 |
| — of which `MEMORY.md` | 5,669 | cl100k | MEASURED — tiktoken over `/mnt/.auto-memory/MEMORY.md`, 19,503 chars, **121 hooks** |
| — of which remainder | ~70,500 | real | **UNSPLIT** — this is `ds-025` item 1, open since `#37` |
| **`_CHAIN.md`** (lands at turn 2, ADDITIVE) | **45,656** | cl100k | MEASURED — `_gen_chain.py --check`, byte-fresh |
| **⇒ floor** | **≈148,000** | real | **CONVERSION**, labelled: 79,074 real + (45,656 cl100k × 1.510) = 147,995; at the ratio's min/max, 145,100–151,600 |

**FINDING 1 — the floor is 78% of this session's own stop line, and 98% of the standing one.**
`_checkin.py`'s SEAM block this morning reads `STOP: FILL 190,000, real` (the `s214-D4`
delegated-wrap advisory in force). A ≈148,000-real floor leaves **≈42,000 real of job room**.
Against the standing `150,929` line it leaves **≈3,000**. The gauge's own CLI prints
`⇒ room for job + wrap: ~97,595 tokens` — **2.3× the honest figure**, for the reason in
FINDING 3.

**FINDING 2 — the boot's harness half is the growth, and nobody has ever split it.** Boot
series from `notes/_GAUGE-LOG.md`, all first-hand `message.usage`, all real:

```
#208 57,050  (the s208-D1 base)   #217 60,433   #221 69,692
#211 57,716   #212 63,258         #218 66,845   #222 75,422
#213 61,605   #214 61,633         #219 67,175   #223 75,741
#215 60,248   #216 60,366         #220 69,565   #224 79,055
                                                #225 79,074 (live, this seat)
```

**+22,325 real (+39%) across 17 sessions, monotone since `#215`, fifteen consecutive readings
outside the `s208-D1` band (55,595–57,903).** The repo-side term (`MEMORY.md`, 5,669 cl100k ≈
8,560 real) is ~11% of the boot and has been roughly flat. **The growth is in the ~70,500-real
remainder that no instrument in this repo can see** — the MCP server rosters, the deferred-tool
listing and the skills catalogue. `_gauge_tokens.py:104` has carried the warning
*"RE-MEASURE WHEN THE SESSION SHAPE CHANGES — a new MCP server moves this figure"* since `#37`;
it is the one component that grew, and it is the one component nobody measures.
⚠ This seat's own boot carries **~200 deferred tool names across 13 MCP servers plus 20 skill
descriptions** — an observable, countable surface. **Splitting it is cheap and has never been
attempted.** [[instrument-without-a-consumer]]

### 1b. Contract vs retrieval-on-demand — the chain, decomposed

`_CHAIN.md`, 225 lines, 45,656 cl100k:

| lines | cl100k | % | what |
|---|---|---|---|
| 4–31 | 484 | 1.1% | the contract statement itself — **this part is excellent** |
| 32–43 | 2,340 | 5.1% | GM header: size stamp, band table, standing warnings |
| 44–55 | 2,253 | 4.9% | ★ LATEST heading + the ten `#224` bullets |
| **57** | **24,873** | **54.5%** | **`residual → #225:` — ONE LINE.** *(the `s225-D2` carries restructure owns this; measured here only as the baseline the rest is read against)* |
| 58–65 | 830 | 1.8% | exit checks, worklist presence index, queue |
| 68–82 | 2,319 | 5.1% | LS ⏱ LATEST delta |
| 83–226 | 12,348 | 27.0% | ⬛ OPEN WORK, generated from `_state.json` |

**FINDING 3 — the chain is 52.6% of the file it exists to avoid, and the generator's own floor
gate is structurally red.** `_gen_chain.py:752-756` asserts `out_tk < 0.40 * gm_tk`. Live:
45,656 / 86,879 = **52.6%**, against a `<40%` floor. The chain's own footer says so in prose to
every cold session: *"you have paid for 53% of it."* This is the CI red the conductor already
carries — and it is **not** a threshold that will be met by tidying: with the carry line at
24,873 cl100k it is arithmetically out of reach until that line is restructured.

**FINDING 4 — even after `s225-D2`, the chain does not clear its own floor.** Chain minus line
57 = **20,783 cl100k**, which is still **23.9% of GM** — inside the floor, but the point is
sharper than that: **20,783 cl100k is ~31,400 real (CONVERSION), still ~3× the `s214-D6` clause's
own ~10–12K aim.** The carry line is the biggest single item; it is not the only structural one.

**FINDING 5 — the OPEN WORK block carries 4,872 cl100k of prose that has a cheaper home three
lines below it.** `_CHAIN.md:83-226` itemises Dave's 123 open rows as
`` `id` **title** — *closes when:* <prose> ``. Measured split: **ids alone 648 · titles+ids
5,517 · `closes_when` prose 4,872**. The block's own last line already names the cheaper home:
*"Bodies, conditions and provenance: `python3 knowledge/_state.py`."* The other 138 rows
("MINE") are **already ids-only** — the precedent for the cut exists inside the same block.

**FINDING 6 — the LS delta is a second telling of the GM banner.** `_CHAIN.md:46-55` (GM ★
LATEST bullets) and `:72-78` (LS ⏱ LATEST delta bullets) are **both exactly 2,076 cl100k**.
Vocabulary overlap, per LS bullet against its best-matching GM bullet: **93% · 74% · 71% · 69% ·
39% · 21% · 13%** (mean 54%). Two bullets are near-restatements. This is not pure duplication —
the LS delta carries lane framing the GM banner does not — but ~1,100 cl100k of it is a second
telling of the same day, inside the boot contract.

### 1c. What the architecture gets RIGHT — measured, not assumed

Three components are doing progressive reveal properly and should be left alone:

- **The archives.** `_GM-ARCHIVE.md` (857,930 cl100k) and `_LIVE-STATE-ARCHIVE.md` (423,305
  cl100k) are **never read at boot** and are reachable as 194 + 397 indexed records. That is
  1.28M cl100k correctly held off the boot surface.
- **The memory detail files.** 300 files, 298,345 cl100k, mean 994 — behind a **5,669-cl100k,
  121-hook index**. A 53:1 reveal ratio. This is the best-performing part of the whole system.
- **`knowledge/_RUNBOOKS.md`.** 1,732 cl100k, generated from the filesystem, 17 runbooks with
  one-line heads. A real router, not carried at boot, cheap to open. The pattern the chain's
  OPEN WORK block should copy.

---

## 2. INDEXING / RETRIEVAL — is `_memento_search` good?

**Short answer: the two-stage SHAPE is right; the ranker and the coverage are not. Stage 1
costs 3,796–6,742 cl100k per query and its top results are the boot surface the session has
already paid for.**

### 2a. Size, granularity, coverage — measured

`knowledge/_memento-index.json`: 9.67 MB · 2,824,822 cl100k on disk · **1,836 records** across
**289 files** · full body text carried (`text` field) · section-level granularity · median
record **702 cl100k**, mean 1,412, **max 43,690**.

**FINDING 7 — 727 of 1,836 records (39.6%) are indexed but UNREACHABLE through the door.**
`_memento_search.bucket_for()` (`:74-75`) returns the kind only if it is in `KIND_ORDER`;
`_search_core.search()` (`:103-104`) does `if b is None: continue`. Three kinds are in the index
and absent from `KIND_ORDER`: **`pattern-node` (374) · `context-node` (216) ·
`component-meta` (137)**. They are built, stored, rebuilt at every wrap, freshness-gated — and
no query can ever return one. [[instrument-without-a-consumer]]

**FINDING 8 — the corpus omits the four record classes the project's own rules send you to
first.** Indexed file counts, probed directly against the index:

| corpus | on disk | indexed |
|---|---|---|
| `notes/_subreports/*.md` (the `s218-D7` filed reports) | **65** | **0** |
| `docs/decisions/ADR-*.md` | **17** | **0** |
| `knowledge/_rulings.json` (279 rulings) | 1 | **0** |
| `knowledge/_state.json` (343 items) | 1 | **0** |
| `knowledge/_RUNBOOK-*.md` | **18** | **5** |
| `notes/_briefs/*.md` | 129 | 129 ✅ |

⛔ **This is the same defect as the carry-forward bloat, seen from the other end.** `s218-D7`
rules that subs file full reports and the conductor **cites them BY PATH** — because retrieval
cannot find them. A path that must be known in advance has to ride forward on the banner. **The
banner is long because retrieval is blind.** Identically: `MEMORY.md` says *"Reference the ADR,
don't duplicate — check ADRs before a 'new' ruling"* and *"⛔ grep `_rulings.json` BEFORE
presenting anything as open — store > chain"* — neither is reachable through the door that
exists to answer exactly those questions.

### 2b. Ranking — driven on five real queries

Five queries a `#225` session would actually ask, run live:

| query | stage-1 cost | refs | top refs returned |
|---|---|---|---|
| "boot floor constant re-base" | 3,796 cl100k | 32 | `gm:HDR` · `gm:DOFIRST` · `gm:C4` · `ls:OPEN` · `ls:SPIN` · `ls:HDR` … |
| "two-red law error ink" | 5,004 | 34 | `lane:lane-2-apollo-charts` · `lane:lane-1-memento` · `gm:PRIOR` · `gm:LATEST` … |
| "conditional band recall probe 200 256" | 5,090 | 34 | `lane:lane-1-memento` · `gm:PRIOR` · `gm:LATEST` · `gm:HDR` · `ls:HDR` … |
| "wrap ritual stratum roll gm_move" | 4,548 | 35 | `lane:lane-1-memento` · `gm:HDR` · `gm:STRATA` · `gm:PRIOR` · `ls:OPEN` … |
| "carry retirement rule banner discipline" | 6,742 | 35 | `lane:lane-2-apollo-charts` · `gm:STRATA` · `gm:C4` · `gm:PRIOR` · `ls:SPIN` … |

**GRADE: 0 of 5 answered.** For "what is the boot floor constant and who ruled it" the correct
answer is `knowledge/_gauge_tokens.py:178` `BOOT_FIRSTTURN_TK = 56_749`, ruled `s208-D1` — the
door returned lane records about bento and charts. **Mean stage-1 cost 5,036 cl100k**, and the
top of every page is `gm:LATEST` / `gm:PRIOR` / `gm:HDR` / `ls:OPEN` — **records the session has
already paid for in the chain.**

**FINDING 9 — the score has nine possible values and 107 records tie at the top.**
`_search_core.score_record()` (`:81-91`) is `matched_original*2 + matched_expanded`, where
`matched` is *"does any stem of this query token appear ANYWHERE in the record blob"* — a
**boolean coverage count**. No term frequency. No IDF. **No length normalisation.** For
"boot floor constant re-base" (4 tokens, 0 lexicon expansions) the ceiling is **8**, **749
records score > 0**, and **107 of them tie at 8** — median length of those 107 is **9,507
chars** against 5,126 for all scored records. Below the ceiling there is no ranking signal at
all; among the 107 at the ceiling the tie-break is `len(text)` **ascending** (`:114`), i.e.
**shortest wins**, which is a proxy for least-informative.

**FINDING 10 — flat per-bucket quotas guarantee irrelevant buckets occupy the page.**
`DEFAULT_CAP` sums to **35**, emitted per bucket with **no cross-bucket relevance comparison**.
For the boot-floor query:

```
gauge-block          emitted 3 of 184     ← the bucket that holds the answer
ls-archive-section   emitted 4 of 231
gm-archive-section   emitted 4 of 160
ledger-section       emitted 4 of  58
gm-section           emitted 3 of  10     ← always emits, always the big banners
dream                emitted 3 of   6
```

The honest denominators are **printed, and that is the design working** — but a "3 of 184" with
**no score shown** tells the reader nothing about whether those three are the answer or a coin
flip. ⚠ A bucket with 6 candidates and a bucket with 231 both get 3–4 slots.

**FINDING 11 — the two-stage promise breaks at the tail.** `--fetch` returns the **whole
record**, and the ten largest are 17,742–43,690 cl100k: `gm-archive:batch-2026-08-08-129`
(43,690) · `gm:LATEST` (27,847) · `gm:PRIOR` (27,210) · `ls:OPEN` (25,100). *"A cold session
spends tokens on the records it needs"* (`_memento_search.py:19`) holds for the median 702-token
record and fails badly for the tail — a single `--fetch gm-archive:batch-2026-08-08-129` costs
more than the entire OPEN WORK block.

**Staleness mechanics: GOOD, and rightly built.** `_capture_gate.index_freshness_check()`
(`:3406`) rebuilds records **in-process** and **byte-compares** — deliberately not mtime
(*"mtimes are reset by any checkout and would read GREEN on a file that had been reverted"*).
It fires as a STRUCTURAL fail in `--wrap` and in `_checkin.py`'s early rehearsal, and it is
**red right now** for `#225` (quoted from this morning's run). This part of the system is
well-designed and does its job.

---

## 3. CARRY-FORWARD DIET — what rides forward that has a cheaper home

*(The `s225-D2` carries restructure is being enacted in parallel and owns `_CHAIN.md:57`. It is
measured above as the baseline and is not analysed here.)*

**FINDING 12 — the boot drift is structural, and it is in the one component the repo cannot
see.** Per FINDING 2: `MEMORY.md` (the repo-side boot term) is roughly flat; the harness
remainder grew +22,325 real in 17 sessions. Dave's `s208-D1` rider — *"a re-base arrives WITH a
boot-REDUCTION option priced beside it"* — has been unsatisfiable for four consecutive
declarations (`#222` +8,930 · `#223` +11,439 · `#224` +13,991 · `#225` live +22,325) **for one
reason: nothing can price a reduction in a term nobody has split.** Splitting it is the
precondition for satisfying his own rider.

Everything else that rides forward every session, with its cheaper home:

| carried | cl100k | cheaper home | ruling-shaped? |
|---|---|---|---|
| `closes_when` prose for Dave's 123 rows | 4,872 | `python3 knowledge/_state.py` (already named in the block) | **yes** |
| LS ⏱ LATEST delta's overlap with the GM banner | ~1,100 of 2,319 | merge at authoring | **yes** — GM-D7-am names three things |
| GM header standing warnings (`set_content` ban, band table, render-sandbox note) | ~1,500 of 2,340 | `_RUNBOOKS.md` router + the runbooks that already carry them | **yes** |
| titles for Dave's 123 rows | 5,517 | **keep** — this is his open work, and it is what he actually reads | no |
| the contract statement `:4-31` | 484 | **keep** — 1.1% for the whole design intent is the best-value text in the repo | no |

**FINDING 13 — DO-FIRST and §C are already off the boot surface, and that half is working.**
`gm:DOFIRST` (10,140) · `gm:C1` (2,927) · `gm:C2` (1,769) · `gm:C4` (11,926) — **26,762 cl100k
total, none of it in the chain.** The chain carries a **39-cl100k presence-index line** plus a
344-cl100k id list at `:62-64` instead. **That is the pattern that works, it was built here
already, and OPEN WORK is the block that has not adopted it.**

---

## 4. DESIGN VERDICT — where the design fights itself

### The shape is right

Generated contract → two-stage retrieval → stores as authority → rituals that roll it forward
is the correct architecture for this problem, and `_CHAIN.md:4-17` states it better than most
published work on the subject: *"Ask for what you need; do not read a file to find out whether
you need it."* Position-awareness (the U-shaped-recall argument at
`_RUNBOOK-context-gauge.md:104`) is genuinely sophisticated and is the reason canon sits at the
two strong ends of the window. The write-once principle (ADR-0017,
`docs/decisions/ADR-0017-write-once-live-facts.md`) and the enactment register (ADR-0016,
`docs/decisions/ADR-0016-enactment-proof-register.md`) are the right two invariants. **Nothing
below argues for a different shape.**

### Where it fights itself — four places, each measured

**FINDING 14 (the root one) — the tier probe measures a one-character string, so the whole
system's "real" figures are cl100k wearing the real label.** Probed in one process:

```
_capture_gate.measurement_tier()          -> 'real'
_gen_chain.stamped_tier(_CHAIN.md)        -> 'real'
_capture_gate.measure_tokens(_CHAIN.md)   -> (45656, 'tiktoken cl100k_base')
_gauge_tokens.count(_CHAIN.md)            -> (45656, 'cl100k-estimate')
```

The tier probe and the measurer **disagree in the same process at the same moment**. Cause,
proven: `_capture_gate.py:1892` — `_tier_probe()` returns `_tier_of(measure_tokens("x")[1])`.
`"x"` is a **permanent cache hit** (`sha256('x')[:32]` is in `knowledge/.token-cache.json`,
value **7**), so it returns tier `real` in 0.00s. A 156 KB file is not cached, the API is
unreachable, and it falls to tiktoken in 0.34s. **The real tier's reachability is
size-dependent, and the probe uses the smallest possible input.** Four consequences, each
verified:

1. **The boot contract inscribes a false unit.** `_CHAIN.md`'s footer reads *"**45,656 real** —
   the unit is THE WHOLE FILE"*. It is cl100k. Cross-check: the same footer says
   *"`GOOD-MORNING.md` is 86,879 real"*; a tiktoken cl100k measure of that file today returns
   **86,879**. Two different measurers cannot agree to the token on an 87K file when they differ
   by ~1.51×. Same proof at `_gm_usage.py --sizes`, which prints
   `section-sizes (real): … LATEST:27847 …` — and `gm:LATEST` tokenises to **27,847 cl100k**
   exactly.
2. **The gate built to catch this cannot fire.** `_gen_chain.check()` (`:670-700`) compares
   `stamped_tier(have)` to `measurement_tier()` and issues a COULD-NOT-ASK refusal on
   divergence. Both return `real`, so it passes the tier gate and prints **FRESH**. The refusal
   is unreachable whenever `"x"` is cached — i.e. permanently, locally.
   [[instrument-without-a-consumer]] [[gate-cannot-pass-in-one-environment]]
3. **The gauge publishes a mixed-unit sum.** `_gauge_tokens.py:305` returns
   `"total": disk + BOOT_FIRSTTURN_TK` = 45,656 (cl100k) + 56,749 (real) = 102,405, printed at
   `:350` under the header `context gauge — unit: REAL Claude tokens`. The `± 1,154` error bar
   covers only the first-turn term; the ~50% unit gap on the chain term is not in it. **This is
   [[measure-dont-convert-units]] committed inside the instrument that rules it** — the same
   self-referential failure `#56` found and fixed once already (`_RUNBOOK-context-gauge.md:40`).
4. **A unit switch is on the record as a diet.** `#223`'s footer: chain **68,404 real** = slice
   49,427 + wrapper 18,977. `#224`/today: **45,656** = slice 32,915 + wrapper 12,741. Slice
   ratio **1.502**, wrapper ratio **1.489** — *both terms scaled by the same ~1.49–1.50*. A
   banner roll removes CONTENT; it cannot scale the generator's own boilerplate wrapper by the
   same factor as the content slice. **On the arithmetic this is a measurer change, not a
   reduction** — and a future session reading `notes/_GAUGE-LOG.md` will read a 33% win that did
   not happen. ⚠ Marked as high-confidence INFERENCE, not measurement: `#223`'s chain cannot be
   re-measured in real tokens from this seat.

**Fight 2 — retrieval is blind to exactly what the rituals tell you to cite, so the banner
carries it instead.** FINDING 8. `s218-D7` requires citation by path; 0 of 65 filed reports are
indexed. `MEMORY.md` requires grepping `_rulings.json` first; 0 of 279 rulings are indexed. The
banner is the only surface that carries these pointers forward, so **the banner cannot shrink
while retrieval stays blind.** These are one defect.

**Fight 3 — `s214-D6` (compress the banner) against `s188-D2`/`s183-D1` P2 (carries verbatim,
retraction receipt required).** Named at ten consecutive wraps, quoted verbatim from
`notes/_GAUGE-LOG.md`: *"A CARRY LIST THIS LONG CANNOT BE COMPRESSED BY A WRAP SUB WITHOUT
DROPPING CARRIES, WHICH IS EXACTLY WHAT THE CLAUSE FORBIDS."* This is `s225-D2`'s territory and
is noted only to record that the system correctly diagnosed its own deadlock ten times and
correctly refused to resolve it without Dave.

**Fight 4 — the contract lines are PARSED and mostly unparseable, and it is WORSE than dream
pass 10 reported.** Dream pass 10 P1 (`notes/_dream/2026-08-30-proposals.md:24`) reports 3/15
recent reports with a parseable `COUNTS:`. **Re-measured here across all 65 filed reports
excluding this one:** parseable `COUNTS:` **7/65 (10.8%)** · `REPLAY-THESE:` **22/65 (33.8%)** ·
`## RULING-SHAPED QUESTIONS` heading **27/65 (41.5%)**. Corpus **467,752 cl100k, mean 7,196**.
So the machine-readable spine of the `s218-D7` contract is present in **one report in ten** —
and none of the 65 are indexed (FINDING 8), so a conductor's only route to any of them is a path
carried on the banner.

⚠ **A PROCESS NOTE ON THIS PARAGRAPH, RECORDED BECAUSE IT IS THE REPORT'S OWN NEAR-MISS.** The
first version of this finding carried `21/65 · 28/65 · 41/65` and a corpus of `1,014,180`. The
measuring script had **crashed** on a tiktoken `disallowed_special` error and those figures were
written from expectation, not from output. They were caught by re-running the probe before
filing, and are replaced above by the real ones. **[[a-crash-is-not-a-fail]] — a helper that
dies must fail LOUD and NAMED, and a figure whose probe did not complete is not a measurement.**
The correction is recorded rather than smoothed away.

---

## 5. STRIP LIST — ranked, priced, with consequences replayed

⚠ Prices are **cl100k saved per session off the boot contract** unless stated. Real-token
equivalents are CONVERSIONS at the n=13 median 1.510 and are shown in brackets, labelled.

### S1 — Fix `_tier_probe()` to probe at working size. **Saves 0 tk. Do it first.**
`_capture_gate.py:1892`: probe with a string large enough to miss the cache (or probe the
actual text about to be measured), so `measurement_tier()` reports the tier the measurer will
actually deliver. **What breaks:** `_gen_chain.check()` starts issuing COULD-NOT-ASK refusals in
this sandbox instead of FRESH/STALE verdicts — *which is the correct answer* and is what `#173`
already ruled the behaviour should be. Chain regeneration in a no-API environment will refuse
rather than restamp. **Mitigation:** ship the token cache, or accept honest refusals.
**PITFALL (Dave #165):** this will make several currently-green things go amber, and the
temptation will be to widen the bar instead. Dave's own `s208-D1` rider covers this — *"I don't
want to move the goals just so the system stops complaining."* **Ruling-shaped: no** (a defect
fix), **but its fallout is** — see Q1.

### S2 — Split the harness remainder. **Saves 0 tk directly; unblocks ~70,500 real.**
The ~70,500-real remainder is 48% of the whole floor and 100% of its growth. It is
**countable** — deferred tool names, MCP server instruction blocks, the skills catalogue — from
inside any session's own prompt. **What breaks:** nothing; it is pure measurement. **PITFALL:**
a count is not a measurement [[measure-dont-convert-units]] — the split must be tokenised, not
inferred from item counts. **Ruling-shaped: no.** ⇒ This is what discharges `ds-025` item 1
(open since `#37`) and what makes Dave's boot-reduction rider satisfiable.

### S3 — Index the four missing corpora. **Saves ~0 at boot; enables S4 and the banner diet.**
Add `notes/_subreports/*.md` (65), `docs/decisions/ADR-*.md` (17), the 13 unindexed runbooks,
and a record per ruling in `_rulings.json` (279) / per open item in `_state.json` (343). Then
either add `pattern-node`/`context-node`/`component-meta` to `KIND_ORDER` **or drop them from
the index** — 727 dead records is 39.6% of the corpus. **What breaks:** the index grows (disk
only, never context); `index_freshness_check` gets slower; `_rulings.json` records need a
section splitter that does not exist yet. **PITFALL:** adding corpora to a ranker that already
cannot discriminate (FINDING 9) makes stage 1 *worse*, not better — **S3 must ship with S4 or
after it, never before.** **Ruling-shaped: partly** — see Q3.

### S4 — Replace the boolean score with BM25 + cross-bucket ranking. **Saves ~3,000–4,000 cl100k per query.**
`_search_core.score_record():81` → term frequency, IDF over the 1,836 records, length
normalisation; `search():114` → rank across buckets and emit ~8 by score with the score
**printed**, instead of 35 by flat quota. At 3–5 queries per session this is
**~9,000–20,000 cl100k [~13,600–30,200 real, CONVERSION]** — and, more importantly, it is the
difference between 0 of 5 and a usable door. **What breaks:** the honest per-bucket denominators
(`3 of 184`) must survive the change — they are `#25`'s ruled shape and a genuine strength.
`--selftest`'s known-answer bites will need re-baselining. **PITFALL:** a ranker change silently
alters what every future session retrieves; it needs known-answer bites **written from the five
failed queries above** before it ships, or the fix is unfalsifiable
[[green-tests-cannot-see-scope]]. **Ruling-shaped: no** (defect fix) — but the cap shape is, Q4.

### S5 — Cut the `closes_when` prose from the chain's OPEN WORK block. **Saves 4,872 cl100k [~7,360 real, CONVERSION].**
Keep all 123 ids + titles; move the conditions behind `python3 knowledge/_state.py`, which the
block already names. Precedent: the 138 "MINE" rows in the same block are already ids-only.
**What breaks:** a cold session can no longer read what closes Dave's work without one call.
**Mitigation:** keep the generated counts line (`343 items · 261 live · 123 Dave's · … 14
UNCONDITIONED`) — that is the `#86` defence and it is 61 cl100k. **PITFALL:** `#86` measured a
*typed* inventory of "118 markers" against a real ~40; the defence is that the block is
GENERATED, not that it is long. Cutting bodies from a generated block keeps the defence intact —
**but only if the counts line stays and the store gate keeps running.** **Ruling-shaped: YES** —
Q2.

### S6 — Merge the LS ⏱ LATEST delta into the GM banner. **Saves ~1,100 cl100k [~1,660 real, CONVERSION].**
Measured overlap 93/74/71/69/39/21/13%. **What breaks:** GM-D7-am names *three* things the chain
carries; merging makes it two. The LS delta's lane framing is not redundant and must survive.
**PITFALL:** this is the cut most likely to lose something real — the overlap is 54% mean, not
95%. Recommend it only as an authoring discipline ("do not restate a GM bullet in the LS delta;
point at it"), never as a generator-side dedupe. **Ruling-shaped: YES** — Q5.

### S7 — Move the GM header's standing warnings to the runbook router. **Saves ~1,500 cl100k [~2,270 real, CONVERSION].**
`_CHAIN.md:34-43` carries the `set_content` ban, the band table and the render-sandbox note.
All three already live in runbooks. **What breaks:** these are `NOTICE-UNPROMPTED` items — the
`#49` rule is that look-up-by-name moves and notice-unprompted stays. **PITFALL: this one is
likely WRONG and is listed to be argued down.** The `set_content` ban exists because a session
that does not know it produces silently-passing false proofs; a warning you must retrieve is a
warning that fires too late. **Recommend: keep the band table pointer and the `set_content` ban;
move only the size stamp's prose.** Saving falls to ~600 cl100k. **Ruling-shaped: YES** — Q6.

### Priced summary

| | cl100k/session | [real, CONVERSION] | ruling-shaped |
|---|---|---|---|
| S1 tier probe | 0 (correctness) | — | no |
| S2 harness split | 0 (unblocks ~70,500 real) | — | no |
| S3 index the four corpora | 0 at boot | — | partly |
| S4 BM25 ranker | 9,000–20,000 *(per-query)* | 13,600–30,200 | no |
| S5 `closes_when` cut | 4,872 | 7,360 | **yes** |
| S6 LS delta merge | ~1,100 | ~1,660 | **yes** |
| S7 header warnings | ~600 | ~910 | **yes** |
| **boot-contract total (S5+S6+S7)** | **~6,570** | **~9,920** | |

⛔ **Read that total honestly.** ~6,570 cl100k against a ≈148,000-real floor is **~7% of the
floor**. **The strip list is not where the win is.** The win is S1 (stop lying about the unit),
S2 (find the +22,325 real), and `s225-D2` (the 24,873-cl100k carry line). Everything else is
housekeeping, and presenting it as the answer would be the third time this project mistook
tidying for a fix.

## RULING-SHAPED QUESTIONS

1. **S1's fallout, not S1 itself.** Fixing `_tier_probe()` will flip `_gen_chain.check()` from
   FRESH to COULD-NOT-ASK in every sandbox without API reach, and will make `_gauge_tokens`
   print two units instead of one total. Option (a) ship the fix and accept honest refusals as
   the normal state; option (b) ship the fix *and* provision the token cache / key into the
   sandbox so `real` is genuinely reachable and nothing refuses. **Recommend (b)** — (a) makes
   the chain unregenerable from the sandbox, which is where wraps run.
2. **May the `closes_when` prose leave the chain?** (a) cut all 123, keep ids + titles + the
   generated counts line (−4,872 cl100k); (b) keep them; (c) cut for the 138 "MINE" rows only —
   already done, so this is a no-op. **Recommend (a).** ⚠ These are **Dave's own open items**
   and the conditions are how he knows what closes them — this is his call, not a tidy.
3. **Should `_rulings.json` (279) and `_state.json` (343) become retrievable records?** (a) yes,
   one record per ruling/item; (b) no — keep `grep` as the ruled route (`MEMORY.md`:
   *"⛔ grep `_rulings.json` BEFORE presenting anything as open — store > chain"*).
   **Recommend (a) as an ADDITION that does not retire the grep** — a second route, never a
   replacement, because the grep rule exists to stop retrieval's ranking from hiding a ruling.
4. **The stage-1 cap shape.** (a) flat per-bucket quotas as today (35 refs, honest
   denominators); (b) global top-N by score with denominators retained; (c) hybrid — global
   top-N plus a guaranteed one slot per non-empty bucket. **Recommend (c)**: it keeps `#25`'s
   honest-denominator ruling intact while stopping a 6-record bucket from outranking a
   231-record one.
5. **Does the chain still carry three things or two?** GM-D7-am names GM header + ★ LATEST + LS
   ⏱ delta. (a) keep three, add an authoring rule forbidding restatement; (b) merge to two.
   **Recommend (a)** — the duplication is 54%, not 95%, and a generator-side merge would drop
   the lane framing.
6. **The GM header's standing warnings.** (a) move all to the runbooks (−1,500); (b) move only
   the size-stamp prose (−600); (c) leave alone. **Recommend (b)** — a `set_content` ban you
   have to retrieve fires after the false proof has already passed.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** every **real** figure for a file in this report. The count-tokens API is
  unreachable from this sandbox (probed: 0.34s fall-through, not a timeout). All file sizes are
  **cl100k, MEASURED**; real equivalents are **CONVERSIONS at the n=13 median 1.510** and are
  labelled at every occurrence. — price to prove: one `_gauge_tokens.py` run in an environment
  with `API-KEY.txt` reachable, ~3 calls.
- **UNPROVEN:** the ~70,500-real harness remainder's internal split (`ds-025` item 1). Not
  observable from this seat — a sub sees its own prompt, not the conductor's. — price to prove:
  one conductor-side turn tokenising its own system prompt sections, ~2,000 tk.
- **UNPROVEN (high-confidence INFERENCE):** that `#223`→`#224`'s chain drop (68,404 → 45,656)
  is a unit switch rather than a diet. The arithmetic is decisive (slice ratio 1.502, wrapper
  ratio 1.489 — a content roll cannot scale boilerplate by the content's factor) but `#223`'s
  chain cannot be re-measured in real tokens from here. — price to prove: `git show` the `#223`
  chain and measure it with a reachable `real` tier, ~1 call.
- **UNPROVEN:** that S4's BM25 rewrite would actually answer the five failed queries. The
  failure is measured; the fix is reasoned. — price to prove: a prototype scorer over the same
  index and the same five queries, ~1 sub-hour.
- **CLAIMED:** the boot series `#211`–`#224` is quoted from `notes/_GAUGE-LOG.md`'s own
  post-mortem lines, not re-derived from transcripts. `#225`'s 79,074 IS first-hand
  (`_checkin.py`, this seat). — re-read costs ~1,500 tk.
- **CLAIMED:** dream pass 10's P1–P4 headlines are read from
  `notes/_dream/2026-08-30-proposals.md`'s section headings; only P1's claim was independently
  re-measured here. ⚠ The two figures are **not comparable and must not be summed or averaged**
  [[measure-dont-convert-units]]: P1's 3/15 counts the reports filed *since the `#221` fix*;
  this report's 7/65 counts *all* filed reports excluding its own. Both point the same way. —
  re-read costs ~4,000 tk.
- **UNPROVEN:** whether the `COUNTS:`/`REPLAY-THESE:` compliance rate is improving or decaying.
  This report measured a single cross-section, not a trend. — price to prove: parse the 65
  reports in filing order and plot, ~1 call.

## Evidence

No evidence files: every claim above quotes its probe inline — the file:line, the command, or
the printed output. The two live instrument runs (`_checkin.py`, `_gen_chain.py --check`) are
reproducible and were run read-only; `_gen_chain.py` was driven with `--check` only, never bare.

REPLAY-THESE: `_capture_gate.py:1882-1904` `_tier_probe`/`measurement_tier` (~400 tk) ·
`_gauge_tokens.py:282-310` `measure_boot` mixed-unit sum (~500 tk) ·
`_search_core.py:81-118` `score_record`/`search` (~600 tk) ·
`_memento_search.py:60-93` `DEFAULT_CAP`/`bucket_for` (~300 tk) ·
`_CHAIN.md:83-88` the OPEN WORK block header + counts line (~700 tk)
