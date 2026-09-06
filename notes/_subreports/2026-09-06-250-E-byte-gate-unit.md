# `#250`-`E` — option (e) BUILT: the byte gate measures code-only bytes and sums the page `consumes`-aware; the caps did not move

session: `#250` · 2026-09-06
window: build lane (byte gate, option e)
sub index: `E`
brief: chat brief (no file) — "Dave ruled option (e)… build it", 8 numbered regions
tokens: `UNMEASURED — the lane could not read `message.usage` from inside a subagent`

## VERDICT

**All 8 regions DONE.** `knowledge/_validate_behaviour.py` now measures every behaviour source in
**code-only bytes** — `//` and `/* */` comments and blank lines stripped by a hand-rolled,
string- and regex-literal-aware scanner **at measure time**, with no canon file modified — and
`check_group` sums the page **per member** from each member's `consumes` declaration, so the
group's figure is the worst member page rather than a registry sum. Both caps are UNMOVED
(`MAX_BYTES = 16*1024`, `PAGE_BYTES = 34*1024`). The gate is **GREEN, exit 0**: `dv-behaviour`
**13,048** code-only of 19,768 raw; worst member `Chart-donut` **24,671** of 34,816 (71%). Those
two figures are **64 B and 143 B below** the brief's expected ≈13,112 / ≈24,814 — reconciled in
finding 6, and the gate's reading is the stricter one. The unfinished `#96-D5` re-dial is
finished: the three "32 KB" strings that had been stale for 32 days are corrected, and the
published `_BEHAVIOUR-GATE.md` no longer prints `39.5 KB of 32 KB, 116%`. ADR-0015 gains
**Amendment 3** by addition — including the strongest case against (e) ("a re-dial in disguise")
and a three-part answer whose first part is mechanical, not rhetorical. All three commanded
mutations pass, and they are permanent `--mutate` entries in the `_validate_fit_physics.py` house
style rather than throwaway probes. **One thing (e) does NOT answer is flagged, not decided:**
Amendment 1 renamed the 16 KB cap's job LEGIBILITY, and a code-only byte count does not measure
legibility any better than a raw one did.

COUNTS: findings `7` · ruling-shaped `2` · UNPROVEN `2`

CITES: `s234-D6` (`knowledge/_rulings.json` — real solutions not patches) · `#96-D5`
(`notes/_MEMENTO-DECISIONS.md:3874` — the 32→34 KB re-dial) · `s182-D1` (mechanical claims carry a
probeable token) · `s215-D3` (rule-5 verification) · `ADR-0015` §4 + `ADR-0015-A1` +
`ADR-0015-A2`, amended here as `ADR-0015-A3`

## What was done

Three files modified, in the brief's own order. **No commit. `_build_all.py` NOT run. No
`knowledge/canon/*.js` source touched** — not one byte, which is the entire distinction between
option (e) and option (c).

1. **`knowledge/_validate_behaviour.py`** (+317/−44 lines) — the unit, the page sum, the stale
   prose, the converted bites and the mutation harness. Detail in findings 1–5.
2. **`docs/decisions/ADR-0015-behaviour-partials-dataviz.md`** (+129 lines) — Amendment 3,
   appended immediately before `## Consequences`. **By ADDITION:** no sentence above it was
   edited or deleted, per the dated-history posture. The three stale "32 KB" mentions
   (A1 §3 twice, A2 §4 once) are corrected in a `⚠ PROSE CORRECTION` paragraph that quotes each
   one and names `#96-D5` as the re-dial that never reached the document.
3. **`knowledge/_BEHAVIOUR-GATE.md`** — regenerated. Finding 5 records how: it is written by
   `write_report()` **inside the gate itself**, so running the gate IS the regeneration. No
   separate generator script exists (`grep -rn "_BEHAVIOUR-GATE" --include=*.py .` returns only
   `_validate_behaviour.py` and two `_to_delete/` copies).

## Findings

**1 · The unit: `code_only()` is a scanner, not a regex, and that is load-bearing.**
`knowledge/_validate_behaviour.py` gains `code_only(js)`, `measure(js)`, `_regex_can_start()` and
`_KW_BEFORE_REGEX`. The scanner walks the source character by character tracking string (`'`,
`"`, backtick), regex-literal and comment state, so a `//` inside `"http://x"` or inside
`/a\/\/b/` is never read as a comment. Regex-vs-division uses the standard
previous-significant-token heuristic, with a keyword set (`return`, `typeof`, `case`, `throw`, …)
so `return /x/.test(s)` scans correctly. `check_source` returns `(fails, raw, code)` and compares
**code** against `MAX_BYTES`; **banned patterns are still matched against the RAW text**, so a
banned call cannot hide behind the strip. Both figures reach the report and stdout with the
delta, per the brief.

**2 · The page sum: `check_group` is now `consumes`-aware, and the numbers move by a lot.**
Signature `check_group(sources, label, names=None, consumes=None)` — the optional pair keeps the
existing unit bites working with bare source lists. With them, each member's total is the sum of
the sources it declares, `consumes` absent still means universal (ADR-0015 A2), a `consumes`
naming an unknown behaviour REFUSES, and the group's figure is the **worst member page**.
`run()` reads `$members[m]["consumes"]` from the registry. Per-member figures print in both the
report and stdout. Live effect, from the gate's own output:

```
Chart-donut                   24671  consumes dv-behaviour, dv-legend, dv-donut-sweep
Chart-{bar,butterfly-h,butterfly-v,combo,line,pie,scatter,stacked-area}
                              20782  consumes dv-behaviour, dv-legend
Chart-{boxplot,bullet,candlestick,histogram,sparkline}, Template-dashboard-bento
                              13048  consumes dv-behaviour
```

The probe's finding 11 is confirmed and closed: 14 of 15 members were being charged for sources
they had declared away since 2026-07-28.

**3 · The `#96-D5` re-dial is finished — and the three converted bites are the real risk this
lane carried.** The report header now reads `per member page ≤34KB`, the per-group report line
`of 34 KB`, the `main()` PASS line `of 34`. Two "32KB" strings survive **deliberately** and are
labelled as history: the `PAGE_BYTES` comment narrating #96, and the page-budget bite's comment
explaining why it needs a third pad.

Separately and more importantly: the pre-existing size bite was
`big = ok_src + "/*" + "x"*MAX_BYTES + "*/"` and the page-budget pad was
`"var x=1;/*" + "y"*(MAX_BYTES-20) + "*/"` — **both padded with COMMENT**. Under the new unit
they would have measured ~0 added bytes and **stopped biting silently on the first run**, leaving
a green selftest guarding nothing. Both are converted to real code via a new `CODE_PAD(n)` helper
(`COMMENT_PAD(n)` is its control). This is the first rot the unit change could have caused and it
is closed in the same beat.

**4 · Nine new selftest bites, all green.** Five on the scanner (line+block+blank strip · `//`
inside a string · `//` inside a regex · `6/2/1` not misread as a regex · a regex after `return`
not misread as division), two on the comment-vs-code delta (4,000 comment bytes must not move the
code figure; they MUST move the raw figure — the second one is what keeps "both are reported"
honest), and four on the `consumes`-aware sum (a wide member's overage caught · a narrow member
NOT charged for what it declared away · an all-narrow group not failed by a registry sum · an
unknown `consumes` name refused). `python3 knowledge/_validate_behaviour.py --selftest` →
`_validate_behaviour selftest OK`, exit 0.

**5 · `_BEHAVIOUR-GATE.md` is generated by the gate itself.** `write_report()` at
`_validate_behaviour.py`; `REPORT = os.path.join(HERE, "_BEHAVIOUR-GATE.md")`. Running the gate
regenerated it. No other script was run — `_build_all.py` was not invoked, per the brief.

**6 · The gate reads 64 B / 143 B tighter than the probe, and the difference is real, not a
defect.** Expected ≈13,112 and ≈24,814; measured **13,048** and **24,671**. The probe computed
`raw − block − line − blank` by subtraction. That arithmetic leaves behind the **indentation and
newline of every line that was nothing but a block comment** — bytes that are whitespace in the
finished file and are not code. The scanner drops those lines outright. Reproduced side by side:

```
canon/dv-behaviour.js   raw 19768  gate-code 13048  probe-style 13201  delta 153
canon/dv-legend.js      raw 15131  gate-code  7734  probe-style  7898  delta 164
canon/dv-donut-sweep.js raw  5511  gate-code  3889  probe-style  3920  delta  31
```

(The probe's published 13,112 sits between the two, so its own subtraction differed slightly again
in how the block-comment regex bounded leading whitespace.) **The gate is the stricter reading**,
which is the direction an error should point in a gate.

**7 · Three mutations, in the `--mutate` house style, all behaving as declared.** Modelled on
`knowledge/_validate_fit_physics.py --mutate` (`MUTATIONS` dict, named choices, expectation
printed beside the observed verdict). ⛔ They mutate an **in-memory copy** of the live source —
nothing on disk is written, so nothing needed restoring. Each exits 0 only when the gate returned
the verdict the mutation DECLARED (`s182-D1`):

```
$ python3 knowledge/_validate_behaviour.py --mutate code-pad
MUTATION code-pad — +4000 bytes of REAL CODE appended to dv-behaviour.js
  baseline : raw 19768 · code-only 13048 · cap 16384
  mutated  : raw 23774 (+4006) · code-only 17054 (+4006)
  X MUTATION code-pad (dv-behaviour.js): 17054 code-only bytes (23774 raw) > 16384 (ADR-0015 size gate)
  expected RED · got RED — OK                                                      EXIT=0

$ python3 knowledge/_validate_behaviour.py --mutate comment-pad
MUTATION comment-pad — +4000 bytes of COMMENT appended to dv-behaviour.js
  baseline : raw 19768 · code-only 13048 · cap 16384
  mutated  : raw 23769 (+4001) · code-only 13048 (+0)
  expected GREEN · got GREEN — OK                                                  EXIT=0

$ python3 knowledge/_validate_behaviour.py --mutate string-slash
MUTATION string-slash — a // inside a STRING LITERAL, which is code and must be counted
  baseline : raw 19768 · code-only 13048 · cap 16384
  mutated  : raw 23777 (+4009) · code-only 17057 (+4009)
  X MUTATION string-slash (dv-behaviour.js): 17057 code-only bytes (23777 raw) > 16384 (ADR-0015 size gate)
  expected RED · got RED — OK                                                      EXIT=0
```

`code-pad` is the mechanical answer to "(e) is a re-dial in disguise": the gate is **exactly as
strong against code** as it was. Under option (a) at `MAX_BYTES = 20 KB` those same 4,000 code
bytes would pass.

### The gate, in full

```
$ python3 knowledge/_validate_behaviour.py
  [PASS] dataviz/dv-behaviour — 13048 code-only bytes (12.7 KB of 16) · 19768 raw, 6720 comment/blank · 15 member(s)
  [PASS] dataviz/dv-legend — 7734 code-only bytes (7.6 KB of 16) · 15131 raw, 7397 comment/blank · 15 member(s)
  [PASS] dataviz/dv-donut-sweep — 3889 code-only bytes (3.8 KB of 16) · 5511 raw, 1622 comment/blank · 15 member(s)
  [PASS] dataviz page budget — worst member 24671 code-only bytes (24.1 KB of 34) across 3 source(s)
         Chart-donut                   24671  consumes dv-behaviour, dv-legend, dv-donut-sweep
         Chart-bar                     20782  consumes dv-behaviour, dv-legend
         Chart-butterfly-h             20782  consumes dv-behaviour, dv-legend
         Chart-butterfly-v             20782  consumes dv-behaviour, dv-legend
         Chart-combo                   20782  consumes dv-behaviour, dv-legend
         Chart-line                    20782  consumes dv-behaviour, dv-legend
         Chart-pie                     20782  consumes dv-behaviour, dv-legend
         Chart-scatter                 20782  consumes dv-behaviour, dv-legend
         Chart-stacked-area            20782  consumes dv-behaviour, dv-legend
         Chart-boxplot                 13048  consumes dv-behaviour
         Chart-bullet                  13048  consumes dv-behaviour
         Chart-candlestick             13048  consumes dv-behaviour
         Chart-histogram               13048  consumes dv-behaviour
         Chart-sparkline               13048  consumes dv-behaviour
         Template-dashboard-bento      13048  consumes dv-behaviour
Behaviour-contract gate OK — see knowledge/_BEHAVIOUR-GATE.md
EXIT=0
```

### Neighbour gates

| gate | command | exit | note |
|---|---|---|---|
| snippets | `python3 knowledge/_validate_snippets.py` | **0** | `136 snippet(s), 0 failure(s)` |
| composition | `python3 knowledge/_validate_composition.py knowledge/snippets/Template-dashboard-bento.reference.html` | **1** | the **3 pre-existing C9 reds**, exactly as the brief predicted — `line 985 data-c=4` span-4-of-6 · `line 1043 data-c=2` span-2-of-3 at ≤1100px · `'Account overview'` spans sum to 8 at ≤1100px. **NOT FIXED, not in scope.** |
| composition | `python3 knowledge/_validate_composition.py --selftest` | **1** | ⚠ a **different, also pre-existing** failure: `AssertionError` at `_validate_composition.py:378` — the `KPI` anchor string is no longer found exactly once in the real bento snippet. **Not caused by this lane** (nothing here touches that gate, the bento snippet or any canon CSS). Raised, not fixed — see ruling-shaped 2. |

### `git diff --stat`

```
 MODEL-ROUTING.md                                   |   1 +
 .../ADR-0015-behaviour-partials-dataviz.md         | 129 +++++++++
 knowledge/_BEHAVIOUR-GATE.md                       |  31 +-
 knowledge/_graph-mark-observations.jsonl           |  28 ++
 knowledge/_validate_behaviour.py                   | 317 ++++++++++++++++++---
 notes/_REHEARSAL-LOG.jsonl                         |   2 +
 notes/_dream/_GRADE-DECISIONS.jsonl                |   2 +
 7 files changed, 466 insertions(+), 44 deletions(-)
```

⚠ **Only three of those seven are this lane's.** `MODEL-ROUTING.md`,
`knowledge/_graph-mark-observations.jsonl`, `notes/_REHEARSAL-LOG.jsonl` and
`notes/_dream/_GRADE-DECISIONS.jsonl` were already dirty in the working tree when the lane opened
and were **not touched here**. This lane's diff is `_validate_behaviour.py` +
`ADR-0015-…md` + the regenerated `_BEHAVIOUR-GATE.md`, plus this report.

## What was NOT done

- **No commit.** Forbidden by the brief. The working tree carries the change.
- **`_build_all.py` NOT run.** Forbidden by the brief. Whether the full build is green end to end
  is therefore UNPROVEN (below) — as it was after the probe.
- **No `knowledge/canon/*.js` source touched.** Not one byte. The 15,573 bytes of provenance
  comment that option (c) would have spent are all still there.
- **The 3 C9 composition reds NOT fixed**, and the composition `--selftest` anchor assertion NOT
  fixed. Both pre-existing, both out of scope.
- **The 14 `knowledge/snippets/*.reference.html` contract banners NOT regenerated.** They still
  say `≤16KB raw` inside the injected AUTO-BEHAVIOUR blocks. The cap value is unchanged so they
  are not wrong about the number, but the word "raw" is now stale. Regenerating them means
  `gen_component_partials.py` and a byte-exact re-injection across 14 files — a build-adjacent
  move this brief did not authorise. **Carried, declared.**
- **The `_decision-graph.json` / `_DECISION-GRAPH.md` node title** still reads *"the 16KB cap
  becomes per-source legibility plus a 32KB per-group page budget"* in three files. Stale since
  `#96-D5`, not this lane's edit to make. Declared.
- **No structural legibility check built** — flagged in Amendment 3 and below, not decided.

## RULING-SHAPED QUESTIONS

1. **Does a STRUCTURAL legibility check now join this gate?** Amendment 1 §2 renamed the 16 KB
   cap's job LEGIBILITY — *"small enough for one person to hold in their head"*. Option (e) is
   honest that it does not answer that: `dv-behaviour.js` is still 19,768 bytes for a human to
   read, comments included, and a person holds the comments too. A byte count is a poor proxy for
   legibility whether it counts comments or not. Options: **(a)** leave it — the code-only cap is
   the tighter defensible reading of §4 and legibility stays a review-time judgement · **(b)** add
   a structural arm (module count / function length / nesting depth) beside the byte cap, advisory
   first per the ADR-0013 ratchet · **(c)** split the two jobs outright: bytes stay the complexity
   gate here, legibility moves to a named new gate. **Recommend (b)**, advisory, because it is the
   only option that produces a number to argue with before it blocks anything — but this is
   Dave's, and Amendment 3 records it as flagged, not decided.
2. **`_validate_composition.py --selftest` is broken at HEAD and nobody has said so.** Its
   `KPI` anchor assertion (`:378`) fails on the real bento snippet, so that gate's 17-arm bite
   suite has not run to completion for some unknown number of sessions. Not this lane's to fix and
   not this lane's to date. Options: **(a)** re-anchor the assertion to the snippet as it now
   stands · **(b)** treat the anchor drift as the finding — the snippet changed under a gate that
   pins its text — and investigate what changed first. **Recommend (b)**; (a) is the patch shape
   `s234-D6` warns against.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** that the full build is green end to end. `_build_all.py` was forbidden and not
  run; only `_validate_behaviour.py`, `_validate_snippets.py` and `_validate_composition.py` were
  executed. Price to prove: one `python3 knowledge/_build_all.py`, one command + its output.
- **UNPROVEN:** that `code_only()` is correct on JS constructs **absent from these three canon
  sources**. It is bitten on the five shapes that appear (strings, template literals, regex
  literals with escaped slashes and character classes, division chains, regex-after-`return`), and
  its declared failure mode errs toward a LARGER figure — but it is a heuristic scanner, not a
  parser. Price to prove properly: run it over a corpus (e.g. every `.js` in `knowledge/`) and
  diff against a real JS tokenizer, ~1 script + a dependency the image may not carry.
- **CLOSED, not unproven:** whether any OTHER consumer of `check_source` / `check_group` had its
  2-tuple unpacking broken by the new 3-tuple return.
  `grep -rn "check_group\|check_source\|_validate_behaviour" --include=*.py .` (excluding
  `_to_delete/`, `_tmp/`) finds **no Python importer at all**. The only in-repo callers are
  `_validate_behaviour.py` itself — where the one 2-tuple site was found and fixed
  (`f, _ = check_source(...)` → `check_source(...)[0]`), which is what turned the first selftest
  run RED and is the reason it is named here — and `knowledge/_build_all.py:213-214`, which
  invokes the gate and its `--selftest` **as subprocesses on the CLI**, so no signature couples
  across that boundary. `gen_component_partials.py:43` mentions the gate in prose only.
- **CLAIMED (from the probe, corrected here):** the expected figures ≈13,112 / ≈24,814. Re-measured
  from the artefact as **13,048 / 24,671** — see finding 6 for the reconciliation.
- **CLAIMED (from `notes/_MEMENTO-DECISIONS.md:3874`, not re-read from the #96 gate run):** that
  the `#96-D5` re-dial left the gate GREEN at the time. Unchanged from the probe's own carry.

## Evidence

No evidence files: every claim above quotes its probe inline (the command and its pasted output).

REPLAY-THESE: `docs/decisions/ADR-0015-behaviour-partials-dataviz.md` Amendment 3 — the
`⚠ PROSE CORRECTION` paragraph, the ruling's 6 clauses, and the case-against/answer pair (~1,600
tk) · `knowledge/_validate_behaviour.py` `code_only()` + `check_group()` (~1,200 tk) ·
`python3 knowledge/_validate_behaviour.py` · `python3 knowledge/_validate_behaviour.py --selftest`
· `python3 knowledge/_validate_behaviour.py --mutate code-pad|comment-pad|string-slash` ·
`python3 knowledge/_validate_snippets.py` ·
`python3 knowledge/_validate_composition.py knowledge/snippets/Template-dashboard-bento.reference.html`
(~900 tk for all seven commands)
