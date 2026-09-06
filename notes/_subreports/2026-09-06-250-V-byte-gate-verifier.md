# `#250`-`V` — ADVERSARIAL VERIFICATION of option (e): the byte gate holds; `consumes` is trusted and never cross-checked

session: `#250` · 2026-09-06
window: verifier seat (MODEL-ROUTING rule 5 / rule 7), different seat from the builder
sub index: `V`
brief: chat brief (no file) — "BREAK the build lane's claims", 7 numbered attack surfaces
tokens: `UNMEASURED — a subagent seat cannot read `message.usage` for its own turn`

## VERDICT

**I could not break it.** Thirteen builder claims were put under probe: **12 CONFIRMED, 0
CONTRADICTED, 1 REFINED** (the composition-selftest drift, which the builder left undated and
which I dated to `deb172a` `#247` 2026-09-05). The caps are unmoved to the byte
(`MAX_BYTES = 16 * 1024`, `PAGE_BYTES = 34 * 1024`, and `git diff` touches only their trailing
comments). The scanner survived 15 adversarial JS constructs including the six the brief named.
**I attempted six separate UNDER-COUNT constructions — the direction that would weaken the gate —
and all six failed to lose a single byte**, which upgrades the builder's declared "errs toward a
LARGER figure, never a smaller one" from an assertion to a probed property with a structural
reason (finding 3). All three commanded mutations and the selftest re-run green from my seat, and
**two mutations the builder did not run** — the page-budget clause alone on live registry data,
and a comment-free minified source at exactly `cap+1` and `cap+0` — behave exactly as the clause
demands.

**The one thing I found that the builder did not: the page sum TRUSTS `consumes` and never reads
the snippet.** A member that silently under-declares is silently under-charged, and the gate stays
green — `V-MUT-5` charges `Chart-donut` **16,937** instead of 24,671 with no failure raised. This
is **not a live defect**: I extracted the injected `AUTO-BEHAVIOUR` blocks from all 15 member
snippets and every one matches its declaration exactly (finding 5), so the gate's numbers are
right today. It is an **unguarded invariant** — the same seam shape Amendment 3 says it was sewing
— and it is the one ruling-shaped item this seat carries.

COUNTS: findings `10` · ruling-shaped `1` · UNPROVEN `3`

CITES: `s234-D6` (`knowledge/_rulings.json` — *"I always lean to real solutions not patches, and
mechanical over inference"*, verified verbatim) · `#96-D5` (`notes/_MEMENTO-DECISIONS.md:3874` —
verified verbatim, and the receipt itself reads *"Enacted `_validate_behaviour.py:37`; gate re-run
GREEN"*) · `s182-D1` (`knowledge/_rulings.json` — *"a new memory hook that makes a mechanical claim
must carry the backticked path or quotable line that makes it probeable"*) · `s215-D3`
(`knowledge/_rulings.json` — *"canon rule 5's adversarial verifier STAYS for Fable-run and
high-stakes work"*, which is this seat's warrant) · `ADR-0015` §4 + `A1` + `A2` + `A3` (read in
full)

## ⚠ TREE HYGIENE — declared, because I touched two things

1. To run attack 6 I wrote `git show HEAD:knowledge/_validate_behaviour.py` to a temp file **inside
   `knowledge/`** (the gate resolves `REG` and `REPORT` from its own dirname, so it cannot be run
   from `/tmp`). **Running the OLD gate overwrote `knowledge/_BEHAVIOUR-GATE.md` back to its HEAD
   content.** I detected this from `git status` and **regenerated it with the new gate**; the file
   is `M` again and its header reads `**Unit: CODE-ONLY bytes**`. Verified:

   ```
   $ git status --short knowledge/
    M knowledge/_BEHAVIOUR-GATE.md
    M knowledge/_graph-mark-observations.jsonl
    M knowledge/_validate_behaviour.py
   ?? knowledge/_screen-gate/dashboard.md
   ```
2. Both temp copies are **deleted**; no `_oldgate_tmp.py` / `_old_gate_VERIFIER_TMP.py` remains
   (the `??` list above is clean of them). **I edited no repo file** — only this report, its
   `assets/` directory and the `.challenges.jsonl` beside it.

## THE CLAIM TABLE

| # | builder's claim | verdict | evidence (pasted in full below) |
|---|---|---|---|
| C1 | both caps UNMOVED, 16 KB / 34 KB | **CONFIRMED** | finding 1 |
| C2 | unit is code-only, stripped at MEASURE TIME, no canon file modified | **CONFIRMED** | finding 2 |
| C3 | scanner is string/regex/template-aware, not a regex | **CONFIRMED** | finding 3 (15 cases) |
| C4 | failure mode errs toward a LARGER figure, never smaller | **CONFIRMED** | finding 4 (6 undercount attempts, all failed) |
| C5 | 13,048 / 7,734 / 3,889 · worst member `Chart-donut` 24,671 | **CONFIRMED** | finding 6 |
| C6 | the `consumes` sum matches what a member page loads | **CONFIRMED for all 15** | finding 5 |
| C7 | `--mutate code-pad` RED · `comment-pad` GREEN · `string-slash` RED | **CONFIRMED** | finding 7 |
| C8 | `--selftest` green, exit 0 | **CONFIRMED** | finding 7 |
| C9 | gate GREEN exit 0; the OLD gate was RED | **CONFIRMED** | finding 8 |
| C10 | ADR-0015 A3 carries the case against honestly and names the A1 legibility conflict | **CONFIRMED** | finding 9 |
| C11 | `_validate_composition.py --selftest` `AssertionError:378` is PRE-EXISTING and undated | **CONFIRMED + REFINED** | finding 10 — I dated it |
| C12 | legibility is NOT measured by (e) | **CONFIRMED** | finding 9 |
| C13 | "#96-D5 left the gate GREEN" is CLAIMED, not re-read | **CONFIRMED, and corroborated** | the receipt line says so itself (CITES) |

**CONTRADICTED rows: none.** The lane's mechanical claims all held.

## Findings

**1 · The caps did not move. Only their comments did.**

```
$ grep -n "^MAX_BYTES =\|^PAGE_BYTES =" knowledge/_validate_behaviour.py
50:MAX_BYTES = 16 * 1024  # per SOURCE, code-only (ADR-0015 §4 + A3). UNMOVED at #250 — Dave's option
58:PAGE_BYTES = 34 * 1024  # ⚠ RE-DIALLED 32→34KB by DAVE, #96 2026-08-05: the 32KB cap predates the

$ git show HEAD:knowledge/_validate_behaviour.py | grep -n "MAX_BYTES =\|PAGE_BYTES ="
38:MAX_BYTES = 16 * 1024
43:PAGE_BYTES = 34 * 1024  # ⚠ RE-DIALLED 32→34KB by DAVE, #96 2026-08-05: the 32KB cap predates the
```

Both integers are byte-identical across the diff. The `git diff` hunk on line 38→50 is
`-MAX_BYTES = 16 * 1024` / `+MAX_BYTES = 16 * 1024  # per SOURCE, code-only …` — a comment append.
**No number moved. C1 CONFIRMED.**

**2 · No canon source was modified — the strip is genuinely at measure time.**

```
$ git status --short knowledge/canon/
(empty)
$ ls -la knowledge/canon/*.js
-rw------- … 19768 Sep  6 11:48 knowledge/canon/dv-behaviour.js
-rw------- …  5511 Aug  2 08:25 knowledge/canon/dv-donut-sweep.js
-rw------- … 15131 Aug  2 08:26 knowledge/canon/dv-legend.js
```

`dv-legend.js` and `dv-donut-sweep.js` still carry their **2026-08-02** mtimes; `dv-behaviour.js`'s
19,768 B is the `#249` VFIT size, unchanged. `code_only()` returns a string and never opens a
file handle. **C2 CONFIRMED — this is the whole distinction between (e) and (c) and it holds.**

**3 · The comment scanner: 15 adversarial constructs, all six the brief named among them, all
scanned correctly.** Harness:
`notes/_subreports/assets/2026-09-06-250-V-byte-gate-verifier/adversarial_scan.py` (imports the
LIVE gate module; nothing mocked).

```
CASE                                                 | code_only() OUTPUT (repr)
A1  // inside a double-quoted string                 | 'var u = "a//b";'                     ✓ kept
A2  http:// URL in code                              | 'var u = "http://example.com/x";'     ✓ kept
A3  /* inside a regex literal  /\/*foo/              | 'var r = /\\/*foo/;'                  ✓ kept
A4  template literal with ${} containing //          | 'var t = `a${b//c\n}d`;'              ✓ kept
A5  block comment containing */ inside a string      | 'var s = "/* x */";\nvar y=1;'        ✓ both lines
A6  division then line comment: a / b // comment     | 'var z = a / b; '                     ✓ comment gone, code kept
A7  regex after return                               | 'function f(s){ return /x/.test(s); }'✓
A8  6/2/1 chained division                           | 'var q = 6/2/1;'                      ✓
A9  NESTED template literal `a${`b`}c`               | 'var t = `a${`b`}c`;\nvar after = 1;' ✓ bytes intact
A10 regex immediately after )  if(x) /re/.test(y)    | 'if (x) /re/.test(y);\nvar after = 1;' ✓ bytes intact
A11 division after ] then //                         | 'var v = arr[0] / 2; '                ✓
A12 string with escaped quote then //                | 'var s = "he said \\"hi\\" // not a comment";\nvar after=1;' ✓
A13 keyword-suffix identifier: x.of / 2              | 'var w = x.of / 2;\nvar after=1;'     ✓ bytes intact
A14 block comment spanning lines, code after         | 'var a=1;  var b=2;'                  ✓
A15 regex with // inside char class /[//]/           | 'var r = /[//]/;\nvar after=1;'       ✓ kept
```

**A9, A10 and A13 are the three where the scanner's STATE is genuinely wrong** (a nested template
desyncs the backtick parity; a regex after `)` is read as division; `x.of` puts an unlisted
keyword in `prev_word`). In every one of the three the BYTE COUNT is still correct, because the
string and regex branches copy every character verbatim — a mis-scan relocates the boundary, it
does not delete anything. Which is finding 4.

**Do any of the wrong cases exist in the real canon files today? No.**

```
$ grep -c '\${`' knowledge/canon/*.js
knowledge/canon/dv-behaviour.js:0
knowledge/canon/dv-donut-sweep.js:0
knowledge/canon/dv-legend.js:0
$ grep -nE '\)\s*/[^/*= ]' knowledge/canon/*.js
knowledge/canon/dv-donut-sweep.js:18:     V=(S+w1+wN)/dur makes accel+cruise+decel sum to dur. …
```

The single `)/` hit is **inside a block comment** (line 18 of a provenance header) and is therefore
never reached by the scanner in code state. Zero nested templates. **C3 CONFIRMED.**

**4 · I could not construct an UNDER-COUNT, and there is a structural reason.** This is the attack
that matters: over-counting makes the gate stricter, under-counting makes it evadable. Six
constructions, each designed to desync the scanner OUT of a string while real JS is IN, landing on
a `//` or `/*` that must survive:

```
$ python3 /tmp/under.py
nested-tpl + block comment   in=  28 out=  27  KEEPME_present=True
nested-tpl + line comment    in=  27 out=  26  KEEPME_present=True
tpl w/ quoted backtick       in=  34 out=  33  KEEPME_present=True
3 inner backticks            in=  40 out=  39  KEEPME_present=True
tpl containing // plain      in=  33 out=  32  KEEPME_present=n/a
regex misread as division    in=  33 out=  32  KEEPME_present=n/a
```

`KEEPME_present=True` in all four cases where a marker was planted — **not one byte of real code
was stripped**; every `out` is `in` minus the trailing newline only. The reason is in the code
shape: bytes are dropped in exactly **two** branches (`c == "/" and nxt == "/"`, `c == "/" and
nxt == "*"`), so an under-count requires the scanner to be in CODE state at a comment opener that
is really inside a string. Every desync I could build leaves an **unmatched quote**, and the string
branch then runs to EOF appending verbatim — which over-counts, never under-counts. **C4 CONFIRMED,
and upgraded from a declared limitation to a probed property.**

**5 · The `consumes` sum vs what a member page ACTUALLY loads — I checked all 15, none
under-declares.** Rather than trusting the registry, I extracted the injected
`AUTO-BEHAVIOUR <name> START … END` blocks from each `*.reference.html` and measured them with the
gate's own `code_only()`:

```
MEMBER                       blocks actually IN the snippet           inj-code    gate#
Chart-bar                    dv-behaviour,dv-legend                      21012    20782
Chart-boxplot                dv-behaviour                                13166    13048
Chart-bullet                 dv-behaviour                                13166        -
Chart-butterfly-h            dv-behaviour,dv-legend                      21012        -
Chart-butterfly-v            dv-behaviour,dv-legend                      21012        -
Chart-candlestick            dv-behaviour                                13166    13048
Chart-combo                  dv-behaviour,dv-legend                      21012        -
Chart-donut                  dv-behaviour,dv-donut-sweep,dv-legend       25023    24671
Chart-histogram              dv-behaviour                                13166        -
Chart-line                   dv-behaviour,dv-legend                      21012        -
Chart-pie                    dv-behaviour,dv-legend                      21012        -
Chart-scatter                dv-behaviour,dv-legend                      21012        -
Chart-sparkline              dv-behaviour                                13166    13048
Chart-stacked-area           dv-behaviour,dv-legend                      21012        -
Template-dashboard-bento     dv-behaviour                                13166    13048
```

**The block set in the snippet equals the `consumes` declaration for every one of the 15.** The
`Template-dashboard-bento` case was the specific attack I expected to land — a dashboard embedding
a donut would load `dv-legend` and `dv-donut-sweep` while declaring only `dv-behaviour` — and it
does not: `grep -on "dvLegend\|dvDonutSweep\|donut-sweep\|dv-legend"` on that snippet returns
**nothing**. **C6 CONFIRMED. No under-counting member exists today.**

The 118–352 B gap (`inj-code` > `gate#`) is the HTML marker banners and `<script>` tags that wrap
each injected block — present in the page, absent from the source the contract is written against.
The gate is therefore ~1.4% below the true page weight. **Not a defect** (ADR-0015 §4 gates the
SOURCE), but it is the direction that under-counts, so it is declared here rather than left to be
found.

**6 · The published figures reproduce exactly from my seat.**

```
$ python3 knowledge/_validate_behaviour.py ; echo EXIT=$?
  … dataviz/dv-behaviour — 13048 code-only (19768 raw, 6720 comment/blank)
  … dataviz/dv-legend    —  7734 code-only (15131 raw, 7397 comment/blank)
  … dataviz/dv-donut-sweep — 3889 code-only ( 5511 raw, 1622 comment/blank)
  … worst member Chart-donut 24671 of 34816
Behaviour-contract gate OK
EXIT=0
```

13,048 + 7,734 + 3,889 = 24,671 = the `Chart-donut` page, which is the only member consuming all
three. Arithmetic closes. The A3 prose claim *"the three sources carry zero `//` comments"* also
checks: `grep -c "^\s*//"` returns `0` on all three. **C5 CONFIRMED.**

**7 · All three commanded mutations and the selftest re-run green from a different seat.**

```
$ python3 knowledge/_validate_behaviour.py --mutate code-pad      → expected RED · got RED — OK      EXIT=0
    baseline raw 19768 · code-only 13048 · cap 16384
    mutated  raw 23774 (+4006) · code-only 17054 (+4006)   → X 17054 > 16384
$ python3 knowledge/_validate_behaviour.py --mutate comment-pad   → expected GREEN · got GREEN — OK  EXIT=0
    mutated  raw 23769 (+4001) · code-only 13048 (+0)
$ python3 knowledge/_validate_behaviour.py --mutate string-slash  → expected RED · got RED — OK      EXIT=0
    mutated  raw 23777 (+4009) · code-only 17057 (+4009)   → X 17057 > 16384
$ python3 knowledge/_validate_behaviour.py --selftest
_validate_behaviour selftest OK
EXIT=0
```

`code-pad` is the load-bearing one and it does what Amendment 3 says: the gate is **exactly as
strong against code** as before. **C7, C8 CONFIRMED.**

**7b · TWO MUTATIONS THE BUILDER DID NOT RUN.** Harness:
`notes/_subreports/assets/2026-09-06-250-V-byte-gate-verifier/extra_mutations.py` (in-memory;
nothing on disk written).

```
=== V-MUT-1 page-clause-only (every source GREEN, worst member page RED) — expect RED ===
   source dv-behaviour     code-only  13048  cap 16384  green
   source dv-legend        code-only  15736  cap 16384  green
   source dv-donut-sweep   code-only  11891  cap 16384  green
   worst member page = 40675  cap 34816
   per-source fails: 0  |  group fails: ['dataviz (page budget): worst member page Chart-donut
                                          loads 40675 code-only bytes > 34816 (ADR-0015 page
                                          budget — splitting a source does not buy headroom)']
   expected RED · got RED — OK

=== V-MUT-2 minified, no comments, exactly MAX_BYTES±0 code bytes — boundary ===
   code-only  16385 (= cap+1) · comments 0 · got RED   expected RED   — OK
   code-only  16384 (= cap+0) · comments 0 · got GREEN expected GREEN — OK
```

**V-MUT-1 is the clause `s182-D1` would ask for and nobody had bitten on live data**: every source
individually legal, the page illegal, caught by name. It is the exact evasion the page budget was
written to stop, and the `consumes` rewrite did not break it. **V-MUT-2** proves there is no
off-by-one and no residual comment credit at the boundary — the only place where a minified source
could have exposed one.

**8 · Regression: the old gate was RED on this same tree; the new one is GREEN. Same inputs, both
exit codes captured without a pipe.**

```
$ git show HEAD:knowledge/_validate_behaviour.py > knowledge/_oldgate_tmp.py
$ python3 knowledge/_oldgate_tmp.py ; echo OLD GATE EXIT=$?
Behaviour-contract gate FAILED:
  X dataviz/dv-behaviour (canon/dv-behaviour.js): 19768 bytes > 16384 (ADR-0015 size gate)
  X dataviz (page budget): 40410 bytes across 3 source(s) > 34816 (ADR-0015 page budget …)
OLD GATE EXIT=1

$ python3 knowledge/_oldgate_tmp.py --selftest ; echo OLD SELFTEST EXIT=$?
_validate_behaviour SELFTEST FAIL:
  X LIVE registry failing: … 19768 bytes > 16384 …; … 40410 bytes … > 34816 …
OLD SELFTEST EXIT=1

$ python3 knowledge/_validate_behaviour.py ; echo NEW GATE EXIT=$?
NEW GATE EXIT=0
```

`1 → 0`, and the 40,410 the old gate printed is the registry sum Amendment 3 names as the seam. The
`#249` wrap line *"the byte gate is RED, his fork"* is corroborated at HEAD. **C9 CONFIRMED.**
(The `_BEHAVIOUR-GATE.md` overwrite this probe caused is declared under TREE HYGIENE and repaired.)

**9 · ADR-0015 Amendment 3 carries the case against honestly, and it does NOT hide the Amendment 1
conflict.** The strongest-objection block is stated in a blockquote, in the objection's own voice,
and it names the contradiction itself:

> *"a change that converts a red into a green with a comfortable margin, decided by the people the
> red was blocking, is a re-dial wearing a different word — and a worse one than (a) … Amendment 1
> §2 renamed the 16 KB cap's job **LEGIBILITY** … and a person holds the comments too."*

The answer's part 3 concedes rather than deflects — *"The legibility objection is real and is NOT
answered here — it is re-pointed"* — and closes **"Flagged for Dave, not decided."** The `Edges:`
line declares all three supersessions explicitly, including
`supersedes(ADR-0015-A2, claim=budgets-are-no-longer-untouched-consumes-now-drives-the-page-sum)`,
which is the sentence A3 is overturning. **This is not a re-dial in disguise dressed as a
definition: it prices its own worst reading and leaves the open question open.** The `⚠ PROSE
CORRECTION` block is by addition, quotes each stale "32 KB" and names `#96-D5`. **C10 CONFIRMED.**

**C12 CONFIRMED:** no structural check exists — `grep` for `nesting|cyclomatic|module count` in
`_validate_behaviour.py` matches nothing but the word "function" in ordinary Python. Legibility is
genuinely unmeasured, exactly as the builder flagged.

**10 · The composition-selftest break is real, pre-existing — and I DATED it, which the builder
did not.** Reproduced:

```
$ python3 knowledge/_validate_composition.py --selftest
  File "knowledge/_validate_composition.py", line 378, in selftest
    for a in (KPI, GROUP_GAP, WALL_GAP): assert real.count(a) == 1, a
AssertionError: <div class="c-bento__tile kpi-tile has-cta" role="group"
                 aria-label="Closing balance" data-c="3" data-r="1">
```

The builder wrote *"no longer found exactly once"*. It is found **zero** times, and the drift is
specific:

```
$ python3 -c "…count the anchor and the near-match…"
count = 0
near matches: 1
   <div class="c-bento__tile kpi-tile has-cta" role="group" aria-label="Closing balance" data-c="1" data-r="1">
```

`data-c` went **3 → 1**. And it is dateable:

```
$ git log --oneline -S'aria-label="Closing balance" data-c="3"' -- knowledge/snippets/Template-dashboard-bento.reference.html
deb172a #247 2026-09-05 — ★★★ 29, CAREFULLY, AND TEST — W1 LANDED −159px; THE JUDGE SAYS NOTHING LEADS
e7cf3db after #231 2026-08-31 — …
```

**The `#247` W1 density lane narrowed that KPI tile and did not re-anchor the gate that pins its
text.** The suite has been dark since **2026-09-05 — two sessions, not "some unknown number"**.
Neither `_validate_composition.py` nor the bento snippet appears in this lane's `git status`, so
**the builder is right that it is not #250's doing.** C11 CONFIRMED and refined. This strengthens
the builder's ruling-shaped 2 recommendation of **(b)** — the drift IS the finding, and it has a
commit.

Neighbour gates, re-run: `_validate_snippets.py` → `136 snippet(s), 0 failure(s)`, **EXIT 0**;
`_validate_composition.py knowledge/snippets/Template-dashboard-bento.reference.html` → **EXIT 1**,
10 `C9` lines. Both match the builder's table.

## RULING-SHAPED QUESTIONS

1. **The page budget TRUSTS `consumes` and never reads the snippet — should it cross-check?**
   The gate's per-member figure is computed entirely from the registry declaration; nothing
   compares it to the `AUTO-BEHAVIOUR` blocks actually injected into that member's snippet. A
   member that under-declares is silently under-charged and the gate stays green:

   ```
   === V-MUT-5 a member SILENTLY under-declaring (donut drops dv-legend) ===
     Chart-donut charged 16937 (25023 actually injected in the snippet); fails=NONE
   ```

   7,734 B vanish from the budget with no failure raised. The unknown-name direction IS guarded
   (`V-MUT-3` on the live registry → `"Chart-sparkline declares consumes ['dv-typo-does-not-exist']
   — not a behaviour of this group"`), and dropping a declaration is safe because absent means
   universal (`V-MUT-4` → sparkline recharged 13,048 → 24,671, still green). It is only the
   **shrinking** direction that is unpoliced — the one that buys headroom. Today no member does it
   (finding 5), so this is an unguarded invariant, not a live red.
   Options: **(a)** leave it — `gen_component_partials.py` writes both the declaration and the
   injection from the same registry, so drift is currently impossible by construction · **(b)** add
   one bite to `_validate_behaviour.py` asserting, per member, that the set of injected
   `AUTO-BEHAVIOUR <name>` blocks equals its `consumes` set — ~15 lines, the probe already written
   in finding 5's harness · **(c)** wire the same assertion into `gen_component_partials.py
   --check` instead, where the generator boundary already lives.
   **Recommend (b).** (a) is an inference about a generator, and `s234-D6` is explicit —
   *"mechanical over inference"*; the whole point of Amendment 3 was that a budget whose NAME said
   PAGE while the CODE summed a registry went unnoticed for 39 days, and this is the same seam one
   layer out. But it is a new gate arm, so it is Dave's.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** that `code_only()` agrees with a real JS tokenizer over a corpus. I raised the bite
  count from the builder's 5 constructs to **15 adversarial constructs plus 6 undercount
  attempts**, and I established the structural argument for the failure direction (finding 4) —
  but that is still not a parser diff. The builder's own UNPROVEN stands, narrowed. Price to prove:
  a Node/acorn tokenizer diff over every `.js` in `knowledge/` — ~1 script plus a dependency the
  image may not carry (`node` availability unchecked).
- **UNPROVEN:** that the full build is green end to end. `_build_all.py` is forbidden to this seat
  too and was not run. Price: one `python3 knowledge/_build_all.py`.
- **UNPROVEN:** that the 14 `*.reference.html` contract banners reading `≤16KB raw` do not mislead.
  I confirmed the builder DECLARED them stale but did not re-read all 14 to check whether any
  prints a number that is now wrong rather than merely a word that is now stale. Price: one grep
  across 14 files, ~300 tk.
- **CLAIMED (not re-read from a #96-era gate run):** that `#96-D5` left the gate green at the time.
  I read the receipt at `notes/_MEMENTO-DECISIONS.md:3874` verbatim and it asserts *"gate re-run
  GREEN"* — so the builder's carry is corroborated **in the cited source**, but the source is still
  a note, not a gate run. Unchanged in status, improved in provenance.

## Evidence

`notes/_subreports/assets/2026-09-06-250-V-byte-gate-verifier/` —
`adversarial_scan.py` (the 15-construct scanner probe of finding 3; imports the live gate module,
mocks nothing) · `extra_mutations.py` (V-MUT-1 page-clause-only and V-MUT-2 the cap boundary,
finding 7b; in-memory, writes nothing).
Every other claim quotes its command and output inline above.
The challenge table in `_claimtable.py` schema:
`notes/_subreports/2026-09-06-250-V-byte-gate.challenges.jsonl`.

REPLAY-THESE: the RULING-SHAPED QUESTION above — the `consumes` cross-check, with `V-MUT-5`'s
16,937-vs-24,671 line (~450 tk) · finding 10, the `deb172a` `#247` dating of the composition
selftest drift (~250 tk) · `python3 notes/_subreports/assets/2026-09-06-250-V-byte-gate-verifier/extra_mutations.py`
(~200 tk) · `python3 knowledge/_validate_behaviour.py --selftest` and the three `--mutate` arms
(~300 tk for all four)
