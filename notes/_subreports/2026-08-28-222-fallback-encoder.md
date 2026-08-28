# `#222` — `s222-D3` option B: the pure-Python EXACT fallback encoder

session: `#222` · 2026-08-28 · model: Opus · one lane
brief: `notes/_briefs/2026-08-28-222-fallback-encoder-brief.md`
predecessors: `notes/_briefs/2026-08-28-222-encoder-vendoring-brief.md` ·
`notes/_subreports/2026-08-28-222-encoder-vendoring.md`
ruling: `s222-D3` (Dave, 2026-08-28) — read from `knowledge/_rulings.json` at HEAD (266 entries),
not from the brief
region: `apollo-spider/gumdrop/machinery/_encoder_home.py` · `apollo-spider/FIRST-SESSION.md` ·
`apollo-spider/build-designer-pack.sh` · `apollo-spider/gumdrop/_GUMDROP-MANIFEST.md` ·
`apollo-spider/gumdrop/_encoder-cache/README.md`
⛔ **NOT touched:** `memento-package/**` (the frozen copies — see ⑤ Q1, this is the STOP) ·
`apollo-spider/dist/` · `knowledge/_rulings.json` (read only) · `knowledge/_state.json` except
one minted row of my own · any gate file · the conductor's dirty `_pack_manifest.json` /
`_pack_gate_probe.json` · no commit, no push, no bake, no `_build_all.py`

**VERDICT: BUILT AND PROVEN — then STOPPED at the frozen shim, as the brief instructs.** The
engine, the equality gate, the dispatch, the timings and the docs are done and driven. The last
wire — making `_gen_chain.py` actually *reach* the fallback — cannot be laid inside the brief's
fence, and the reason is not the one the brief expected. See ⑤.

**COUNTS:** files added 1 · files edited 5 · gate files edited **0** · gates re-run 10 (9 as
baseline, 1 pre-existing red, named) · equality-gate corpus 1,910 files / 69,483,685 chars /
21,813,749 tokens, **0 divergent tokens** · new selftest bites 4 (9 total) · mutation directions
driven 4 · proof runs 2 environments × 2 engines · ruling-shaped questions 2 · findings against
an existing gate 1 (serious) · UNPROVEN 3 · COULD-NOT-RUN 2

---

## ⓪ THE PREMISE, REPLAYED FIRST

At HEAD `36754e2` + the conductor's dirty `_pack_manifest.json` / `_pack_gate_probe.json` /
`_rulings.json` (all three left alone). Baselines taken **before** the first edit:

| instrument | baseline at `36754e2` |
|---|---|
| `knowledge/_validate_package_delta.py` | `0 failure(s)` |
| `knowledge/_validate_package_delta.py --selftest` | all bites pass |
| `knowledge/_release/_gen_pack_manifest.py --selftest` | 195 bites, 0 fail |
| `knowledge/_release/_gate_release_audit.py --manifest-check` | PASS at `36754e247a2c` |
| `knowledge/_release/_gate_release_audit.py --pack` | ⛔ **already RED** — see ④ |
| `knowledge/_release/_gate_release_audit.py --drift` | PASS (manifest generated at HEAD) |
| `knowledge/_release/_gate_frozen_release.py` | PASS, 3 arms |
| `knowledge/_release/_gate_ci_template.py` | PASS |
| `knowledge/_release/_gate_pack_docs.py --stage` | 45 findings, ADVISORY, exit 0 |

**One brief premise did not survive the replay, and it is the whole story of this lane.** The
brief's fence says the frozen copies may gain the dispatch "via the same delta-legal shim route
the prior lane proved (new-names-only, **AST arm untouched**)". Driven, not reasoned: **the AST
arm does not read the shim at all.** ⑤ Q1 carries the measurement.

---

## ① THE MECHANISM AS BUILT

Everything is in the ONE helper the ruling names, `apollo-spider/gumdrop/machinery/`
`_encoder_home.py` (→ packs to `memento-package/machinery/_encoder_home.py`). No second module,
no second file, no new name anywhere else — requirement 3's "extend it there, nowhere else".

**The gate was built FIRST and the engine was developed against it**, as the brief instructs.
The first working version of the pretokenizer was wrong in three places (Python's `$` matches
before a trailing newline where Rust's does not; `\p{L}` needed deriving; the possessive
quantifiers needed justifying rather than dropping) and the gate is what said so, each time,
naming the token index.

**The engine.** `PurePyEncoding` — cl100k_base in stdlib Python over the SAME vendored
`_encoder-cache/` file:

- **the real pretokenizer, not BPE alone.** cl100k's published pattern uses two things stdlib
  `re` does not have — Unicode general-category classes and possessive quantifiers — and the
  `regex` package that has both is exactly the dependency this ruling exists to remove. So the
  pattern is TRANSLATED, and the module justifies the translation term by term rather than
  asserting it. Two of those terms are load-bearing and were found by the gate, not by reading:
  - `\p{L}` / `\p{N}` are built from `unicodedata.category()` at first use (~0.21 s, measured),
    not typed in as a range table. A hard-coded table is a claim about Unicode that nothing
    checks, and it would be wrong on a different Python.
  - `\s++$` becomes `\s+\Z`, **not** `\s+$`. Python's `$` also matches immediately before a
    final newline; the Rust `$` this pattern was written for means end-of-text only. With `$`
    the engine mis-splits the tail of every file that ends `"\n\n"` — which is most of them.
  - every possessive quantifier is shown to be equivalent to its greedy form *in this pattern*
    (the optional class in alt 2 excludes letters, so the backtrack it would permit can never
    succeed; `[\r\n]` are `\s` so they cannot be in the class before `[\r\n]*`; the rest have
    nothing following them to backtrack for). That argument is written into the module.
- **the merges, in rank order** — repeatedly merge the adjacent pair with the lowest rank, which
  is what tiktoken does. Whole pretokenized pieces are memoised, which is why the cost is 4×
  rather than the 100× a naive implementation costs.
- **special-token semantics**, including the part people forget: `encode()` with no
  `allowed_special` RAISES `ValueError` on a literal `<|endoftext|>` rather than encoding five
  ordinary tokens. Callers that wrap `encode()` in a try/except (the shim does) must see the
  SAME failure from both engines, or the fallback changes behaviour on exactly the inputs nobody
  tests. The gate has an arm for it.
- **a loud refusal on a corrupt table**: an unparseable line raises rather than being skipped,
  because a rank table with holes produces confident wrong numbers.

**The dispatch — `count(text) -> (tokens, engine)`.** The order IS the ruling: real `tiktoken`
whenever importable (speed), else this engine, else `MeasurementRefused`. There is deliberately
**no estimate tier here at all** — a caller that wants a byte divisor must reach for it itself,
in the open, with its own label.

**NAMED, never silent (requirement 2).** Two engine strings, and nothing else may name an
engine: `tiktoken cl100k_base` and `purepy cl100k_base (exact, equality-gated)`. Neither
contains the word `ESTIMATE`, deliberately — the #82-D1 tier vocabulary classifies by that
substring, and both of these are exact cl100k measurements, so both must land in the `cl100k`
tier. Proven downstream: a chain generated by one engine is **byte-identical** to one generated
by the other, and `--check` under either engine calls the other's file FRESH (②D2/D3).

⛔ **The module deliberately does NOT register itself in `sys.modules` as `tiktoken`.** That is
the one shortcut that would have made every existing caller work with no edit anywhere — and it
is precisely what `s222-D3` forbids, because every line that today prints `tiktoken cl100k_base`
would keep printing it on a machine with no tiktoken. A fallback that borrows the real library's
name is a silent fallback. The refusal to take that shortcut is what ⑤ Q1 is about.

**The refusal is untouched (requirement 4).** Both engines read the same file, so a missing or
wrong-size file fails both, identically, through the same loud named `ENCODER-HOME: ⛔` block.
Driven both ways with tiktoken present AND absent (②E1/E2).

**The equality gate — `--equality-gate [paths…]`.** Three arms, and it compares **token
SEQUENCES, not counts**: two wrong sequences can share a length, and a gate that compared
lengths would pass a pretokenizer wrong in compensating ways.

1. 68 adversarial cases, always, whatever the corpus: whitespace runs, trailing newlines,
   contractions in both cases, Arabic-Indic and Roman numerals, fractions, superscripts, CJK,
   Hangul, Greek, Cyrillic, RTL, emoji ZWJ families, flag pairs, mathematical alphanumerics,
   `\v\f\x85\xa0`, ideographic space, ZWSP, BOM, and the pack's own `tape (cl100k ESTIMATE)`
   footer sentence.
2. special-token semantics, comparing the RAISE as well as the tokens.
3. the real corpus, refusing on the first divergent token, naming the file, the token index and
   the decoded text either side of it.

With no `tiktoken` to compare against it exits **COULD-NOT-RUN (rc 2)**, never green — a gate
that cannot reach its reference must say so [[instrument-without-a-consumer]].

**`--check` (the § Before you start check) now names the engine** and passes with tiktoken
absent: `ENCODER OK — engine: … — 4 tokens, …`. `--timings` prints requirement 5's numbers.
`--selftest` grades **failures and could-not-runs separately** (rc 0 / 1 / 2), because a bite
that could not be driven is neither a pass nor a fail [[a-crash-is-not-a-fail]].

---

## ② PROOF — DRIVEN, NOT REASONED

Fresh stage at `/var/tmp/s222d3/Apollo-Spider-vnext/`, built by replaying `SEED_PREFIXES` by
hand exactly as the predecessor lane's REPLAY-THESE does, plus `GOOD-MORNING.md` and
`_LIVE-STATE.md` written from FIRST-SESSION §4b's own skeletons.

**How `tiktoken` was made unimportable, and why that way.** A **venv without it** —
`python3 -m venv /var/tmp/s222d3/nokit` — not a shadow module. A venv excludes system
site-packages by default, so `import tiktoken` raises `ModuleNotFoundError` for the same reason
it does on a designer's machine: the wheel was never installed. A shadow module raising
`ImportError` would have modelled a *broken* install, which is a different failure and would
also have left `_heal_tiktoken()`'s `pip install` able to "succeed" into a state the shadow then
re-breaks. The venv also lets `_heal_tiktoken()` run for real and fail for the real reason.

Every run used:

```
env -u TIKTOKEN_CACHE_DIR -u DATA_GYM_CACHE_DIR \
    https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 http_proxy=http://127.0.0.1:9 \
    TMPDIR=/var/tmp/s222d3/emptytmp
```

`/tmp/data-gym-cache`, `/var/tmp/data-gym-cache` and `~/.cache/tiktoken` were confirmed **absent**
before the runs. Port 9 is dead, so any network read raises.

### A — the pack AS THE TREE STANDS, tiktoken unimportable

| # | command | result |
|---|---|---|
| A1 | `…/nokit/bin/python3 memento-package/machinery/_encoder_home.py --check` | `ENCODER OK — engine: purepy cl100k_base (exact, equality-gated) — 4 tokens, measured with the encoder data inside this pack (no download, no environment variable to set).` **rc 0** |
| A2 | `…/_encoder_home.py --equality-gate` | `⛔ EQUALITY GATE COULD-NOT-RUN — the reference engine is not here…` **rc 2** (correct: not green) |
| A3 | `…/_encoder_home.py --selftest` | `0 failure(s), 1 could-not-run` **rc 2** (the mutation arms need the reference) |
| A4 | `…/_gen_chain.py` | ⛔ `MEASUREMENT REFUSAL`, **rc 1, no file** — see A5 |
| A5 | `…/_capture_gate.measure_tokens("the quick brown fox")` | `(5, 'bytes/3.53 ESTIMATE (tiktoken absent)')` · tier `estimate` · `measurement_degraded()` **True** |

**A4/A5 are the STOP, measured.** The `_encoder_home` bootstrap ran fine — `encoder_home_note()`
confirms the helper was found and `TIKTOKEN_CACHE_DIR` set — but the frozen shim's ported
`measure_tokens` never asks the helper for a count, so it falls to the byte divisor and reports
5 tokens where the truth is 4. Nothing in `_encoder_home.py` can change that from outside. ⑤ Q1.

### C — THE SAME STAGE WITH THE ONE MISSING WIRE, applied to the STAGE ONLY

⚠ **This overlay was applied to `/var/tmp` copies and to NOTHING in the repo.** It exists so the
conductor can price ⑤ Q1 against a measurement instead of an argument. The exact patch is in ⑦.

| # | command | result |
|---|---|---|
| C1 | `…/nokit/bin/python3 …/_gen_chain.py` | `✅ _CHAIN.md: 867 purepy cl100k_base (exact, equality-gated) · … fixed point in 2 pass(es)` **rc 0** |
| C2 | `…/nokit/bin/python3 …/_gen_chain.py --check` | `✅ _CHAIN.md is FRESH` **rc 0** |
| C3 | `…/_capture_gate.measure_tokens(…)` | `(4, 'purepy cl100k_base (exact, equality-gated)')` · tier `cl100k` · degraded **False** |
| C4 | the plugin mirror, three levels deeper, same env | `(4, 'purepy cl100k_base (exact, equality-gated)')` |

### D — THE EQUIVALENCE (this is the measurement that matters)

| # | command | result |
|---|---|---|
| D1 | same stage, **system python3 (real tiktoken)**, egress still dead | `✅ _CHAIN.md: 867 tiktoken cl100k_base · … fixed point in 2 pass(es)` rc 0 |
| D2 | `cmp` of the two generated `_CHAIN.md` | **BYTE-IDENTICAL**, sha256 `fe70784b35f2507637e8449e90157c3e0604894014e5387e6690e6ac96b08205` both |
| D3 | chain built by **purepy**, `--check` run under **tiktoken** | `✅ _CHAIN.md is FRESH — byte-matches the live chain` rc 0 |
| D4 | `--equality-gate` on the stage, reference present | `✅ PASSED — 68 adversarial cases · 35 files · 564,959 characters · 145,490 tokens — every token identical` |

D2/D3 are the strongest form of the exactness claim available: the two engines are
*substitutable inside the pack's own artefact*, in both directions, including the tier stamp.

### E / F — THE MUTATIONS, BOTH WAYS, BOTH DIRECTIONS

| # | mutation | result |
|---|---|---|
| E1 | vendored data file moved aside, **tiktoken unimportable** | `--check` names all 7 candidate paths then `⛔ REFUSED` **rc 1**; `_gen_chain.py` prints the `ENCODER-HOME:` block then `MEASUREMENT REFUSAL` **rc 1**, `_CHAIN.md` **not written** |
| E2 | same, **tiktoken present** | `--check` **rc 1**; `_gen_chain.py` `MEASUREMENT REFUSAL` — requirement 4 holds on BOTH engines |
| E3 | file restored | `--check` green again, both interpreters |
| F1 | **merge ranks corrupted** (`b" the"` ↔ `b" and"` swapped — table keeps its size, merge ORDER changes) | `⛔ EQUALITY GATE FAILED on adversarial case 67 … token 6 differs — tiktoken says 279, purepy says 323. Context (tiktoken) '…real — the unit is THE WHOLE' vs (purepy) '…real — and unit is THE WHOLE'.` **rc 1** |
| F2 | corruption undone | `✅ EQUALITY GATE PASSED` **rc 0** — the gate is not reporting on its own footprint |

F1/F2 also run automatically as selftest arm 8, so "exact" stays a checked word rather than a
decorative one [[mutation-tests-the-clause-not-the-feature]].

### THE EQUALITY-GATE CORPUS

| corpus | files | characters | tokens | divergences |
|---|---|---|---|---|
| the pack's own text (default, in the stage) | 35 | 564,959 | 145,490 | **0** |
| `knowledge notes apollo-spider memento-package reviews` | 1,910 | **69,483,685** | **21,813,749** | **0** |
| + 68 adversarial cases + 4 special-token cases | — | — | — | **0** |

---

## ③ TIMINGS — REQUIREMENT 5, MEASURED

Sandbox Linux, Python 3.10.12. `purepy` cold start (1.68 MB rank table + Unicode class
derivation, once per process): **0.24 s**.

| artefact | chars | `tiktoken cl100k_base` | `purepy cl100k_base` |
|---|---|---|---|
| `_gen_chain.py` (largest packed text, 60,309 ch) | 60,309 | 0.005 s | **0.022 s** |
| `_state.py` | 51,163 | 0.004 s | **0.020 s** |
| `_GUMDROP-MANIFEST.md` (largest packed prose) | 10,047 | 0.001 s | **0.003 s** |
| `_CHAIN.md` | 3,002 | 0.000 s | **0.001 s** |
| **the whole `_gen_chain.py` step, wall clock, same stage** | — | **0.14 s** | **0.27 s** |
| 69.4 M characters (the wide gate corpus) | 69,483,685 | 5.42 s | **23.14 s** |

**Steady-state ratio ≈ 4×**, dominated by the piece memoisation. The conductor's expectation was
sub-second at pack sizes and a finding if anything real exceeded ~30 s: **the whole chain step
costs 0.27 s on the fallback against 0.14 s on tiktoken**, so there is no finding to raise. The
0.24 s cold start is the larger share of that, and it is paid once per process.

---

## ④ GATE VERDICTS

| gate | verdict |
|---|---|
| `knowledge/_validate_package_delta.py` | **0 failure(s)** (unchanged — this lane touched nothing it globs) |
| `knowledge/_validate_package_delta.py --selftest` | all bites pass |
| `knowledge/_release/_gen_pack_manifest.py --selftest` | **195 bites, 0 fail** |
| `knowledge/_release/_gate_release_audit.py --manifest-check` | **PASS** at `36754e247a2c` |
| `knowledge/_release/_gate_release_audit.py --drift` | **PASS** — manifest generated at HEAD |
| `knowledge/_release/_gate_frozen_release.py` | **PASS**, 3 arms, no frozen surface moved |
| `knowledge/_release/_gate_ci_template.py` | **PASS** |
| `knowledge/_release/_gate_pack_docs.py --stage <my stage>` | **45 findings, ADVISORY, exit 0 — identical to the baseline of 45.** This lane's doc edits add **zero** net findings |
| `_encoder_home.py --selftest` (repo, tiktoken present) | **0 failures, 0 could-not-run**, 9 arms |
| `_encoder_home.py --selftest` (stage, tiktoken absent) | 0 failures, **1 could-not-run**, rc 2 — correct and named |
| `knowledge/_release/_gate_release_audit.py --pack` | ⛔ **RED — PRE-EXISTING, NOT THIS LANE'S** |

⚠ **`--pack` is red at baseline and this lane cannot have caused it.** `check_pack()` compares
the zip against **the manifest commit's git blobs**, never the working tree, so no uncommitted
edit is visible to it. The cause is the conductor's dirty regeneration: the committed manifest is
at `3f7a63a`, the working-tree manifest is at `36754e2` (post-`s222-D2`), and
`Apollo-Spider-v1.0.1.zip` was baked before `s222-D2` — so it is missing
`memento-package/_encoder-cache/*` and 3 other paths, carries 2 the manifest does not name, and
differs on 29 files including several this lane never opened (`ci-template/run-gates.py`,
`knowledge/_validate_descender_computed.py`). **This is the #220 category error one release
later**: the arm already learned to SKIP older zips as frozen history, but here the *current*
version's zip has been outrun by a manifest regenerated at a newer commit. Re-cutting is Dave's
under `s219-D4(2)`. ⬛ **Conductor: this red will clear on the bake and not before.**

---

## ⑤ RULING-SHAPED QUESTIONS → DAVE / CONDUCTOR

### Q1 — THE STOP. How does the frozen shim reach the fallback? (blocks requirement 6)

**The mechanical fact, measured.** `_gen_chain.py` prints the engine from
`cg.measure_tokens(text)[1]`, and in that function both the call and the label are frozen
literals:

```python
    try:
        tiktoken = importlib.import_module("tiktoken")
    except Exception:
        if not _heal_tiktoken():
            _TIERS_SEEN.add("estimate")
            return (…, f"bytes/{BYTES_PER_TOKEN} ESTIMATE (tiktoken absent)")
        tiktoken = importlib.import_module("tiktoken")
    try:
        out = len(tiktoken.get_encoding("cl100k_base").encode(text)), "tiktoken cl100k_base"
```

The only route a module-level, new-names-only block could take is to satisfy
`import_module("tiktoken")` with a stand-in — and then the printed engine says
`tiktoken cl100k_base` on a machine with no tiktoken, which is exactly what `s222-D3` forbids
("the engine named in every output line — never silent"). A new-names-only change **cannot**
carry requirement 2. Per the fence: **STOP and return.**

### ⛔ AND A FINDING THE CONDUCTOR NEEDS REGARDLESS: arm 2 has never audited the shim

The brief's fence assumes the AST arm blocks a shim edit. It does not. Driven:

| probe | result |
|---|---|
| edit `measure_tokens` in **both** shim copies identically, run `_validate_package_delta.py` | **0 failure(s) — GREEN** |
| edit `measure_tokens` in `knowledge/_capture_gate.py` (the source) | **RED** — `SHIM PROVENANCE chain(a): 'measure_tokens' … has CHANGED since the port commit 9dcf62d` |

The cause is one argument, `knowledge/_validate_package_delta.py:313`:

```python
    _chain("knowledge/_capture_gate.py", SHIM_SOURCE_FILE_A, PORT_COMMIT_A, …)
```

`cur_relpath` is the **source**, not `memento-package/machinery/_capture_gate.py`. So the arm
compares `knowledge/_capture_gate.py` @ HEAD against itself @ `9dcf62d` and **never opens the
shim's ported bodies at all**. What it actually enforces — usefully — is *"the source has not
drifted since the port commit"*, i.e. the #114/#149 re-port alarm. What nothing enforces is that
the shim's copies still match anything. This is [[no-gate-parses-the-artefact]] with a green
light on: the gate's own docstring says it hashes the segment "in both the historical git blob
and the current file", and "the current file" turns out to be the source.

⚠ **And the fix is not a one-line repoint.** Measured: the shim's `measure_tokens` is 2,267
characters, the source's is 2,531, sha `a2812a23…` vs `268c5508…`. They *legitimately* differ —
the shim declares one intended difference (`_real_gauge()` as an optional import instead of a
hard `import _gauge_tokens`). Point arm 2 at the shim naively and it goes red on a correct pack.
So repairing it is design work with a ruling in it, not a patch. **Priced, not done, and no gate
file was touched.**

### Q1's three routes, priced

**(a) Re-port through the gate's OWN documented remedy — RECOMMENDED.** Add the fallback tier to
`knowledge/_capture_gate.py`'s `measure_tokens`, re-port it verbatim into both shim copies,
commit, then bump `PORT_COMMIT_A`. Keeps the shim's declared provenance TRUE, makes the dispatch
auditable, and is literally what the gate's failure message asks for ("re-review and re-port").
Costs: one gate-constant edit and a two-commit dance — **both outside this lane's fence** (no
commit, no gate file). Apollo itself is unaffected: `knowledge/` has no `_encoder-cache/` or
`_encoder_home.py` above it, so the optional import fails there and the cascade is unchanged.
The exact patch is in ⑦ and it is 14 lines.

**(b) A new-name wrapper that rebinds `measure_tokens` in the shim.** Passes every gate today
(and would pass even if arm 2 were repaired, since the `def` still comes first in the module
body). **I did not take it and recommend against it**: it makes `cg.measure_tokens` a different
function from the audited one, which is the guarantee arm 2 exists to give.

**(c) Edit `_gen_chain.py` as a matched triple.** Arm 1 compares working tree to working tree, so
`knowledge/` + both copies edited identically stays green with no commit. But it is a
VERBATIM-SET file and it changes Apollo's own chain generator — region ownership is the
conductor's, and the brief fenced this lane to the shim route.

### Q2 — Requirement 6's doc demotion is BLOCKED BY Q1, and the docs say only what is true

`pip install tiktoken` could not honestly become "recommended, not required" while Step 4c still
fails without it. So the docs landed at exactly the true line: the § Before you start **check**
now passes without tiktoken and names the engine (that IS true today, and the old doc quoted the
old output string verbatim, so it was stale the moment `--check` changed); the pack's own engine,
its equality gate and its speed are documented; and the `pip install` paragraph now says *"today
Step 4c reaches that encoder through `tiktoken`"* rather than promising more than the tree does.
**When Q1 lands, three sentences change** — they are quoted ready-to-paste in ⑦.

---

## ⑥ FILES TOUCHED (for the conductor's reconcile)

**Added (1):**
- `notes/_subreports/2026-08-28-222-fallback-encoder.md` — this file (row minted, ⑧)

**Edited (5):**
- `apollo-spider/gumdrop/machinery/_encoder_home.py` — the engine, the dispatch, the equality
  gate, the timings, 4 new selftest arms, `--check` rewritten to name the engine. All 5 pre-existing
  selftest arms kept, unchanged in intent.
- `apollo-spider/FIRST-SESSION.md` — § Before you start: the expected `--check` output string
  (was stale), the engine-naming sentence, the fallback + equality-gate paragraph, and the
  narrowed `pip install` claim.
- `apollo-spider/build-designer-pack.sh` — the generated pack README's "What you need installed".
- `apollo-spider/gumdrop/_GUMDROP-MANIFEST.md` — new section documenting the fallback engine,
  the translation, the gate and the measured timings (#185 forgotten-document class).
- `apollo-spider/gumdrop/_encoder-cache/README.md` — "two engines read this one file", and the
  wheel is now stated as RECOMMENDED for speed.

**Deliberately NOT edited:** `memento-package/**` (both `_capture_gate.py` copies, `_gen_chain.py`
in any copy) · every gate file · `knowledge/_capture_gate.py` · the conductor's dirty
`_pack_manifest.json` / `_pack_gate_probe.json` / `_rulings.json` · `apollo-spider/dist/` ·
`W-244`/`W-245`/`W-246` (not mine).

⬛ **Conductor:** `notes/_briefs/2026-08-28-222-fallback-encoder-brief.md` is untracked and has
**no store row** — the #185 class. I did not mint one because it is your document; W-246 is the
precedent shape.

---

## ⑦ REPLAY-THESE (verifier — exact commands)

```sh
# --- the instrument, in the repo
python3 apollo-spider/gumdrop/machinery/_encoder_home.py --selftest       # 0 fail, 0 could-not-run, 9 arms
python3 apollo-spider/gumdrop/machinery/_encoder_home.py --check          # ENCODER OK — engine: tiktoken cl100k_base
python3 apollo-spider/gumdrop/machinery/_encoder_home.py --timings
python3 apollo-spider/gumdrop/machinery/_encoder_home.py --equality-gate \
        knowledge notes apollo-spider memento-package reviews
#  -> ✅ 68 adversarial cases · 1910 files · 69,483,685 characters · 21,813,749 tokens — every token identical
#     (a LIVE corpus: the file count moves with the tree; what must not move is `0 divergences`)

# --- ⛔ THE FINDING: arm 2 does not read the shim. Both halves, in order.
cp memento-package/machinery/_capture_gate.py /var/tmp/a.bak
cp memento-package/claude-plugin/memento/machinery/_capture_gate.py /var/tmp/b.bak
python3 - <<'EOF'
old='        out = len(tiktoken.get_encoding("cl100k_base").encode(text)), "tiktoken cl100k_base"'
new='        out = len(tiktoken.get_encoding("cl100k_base").encode(text)), _ENGINE_NAME'
for p in ('memento-package/machinery/_capture_gate.py',
          'memento-package/claude-plugin/memento/machinery/_capture_gate.py'):
    s=open(p).read(); assert old in s; open(p,'w').write(s.replace(old,new))
EOF
python3 knowledge/_validate_package_delta.py        # ⛔ 0 failure(s) — GREEN on an edited ported body
cp /var/tmp/a.bak memento-package/machinery/_capture_gate.py
cp /var/tmp/b.bak memento-package/claude-plugin/memento/machinery/_capture_gate.py
# and the other direction — the source edit DOES fire:
cp knowledge/_capture_gate.py /var/tmp/src.bak
python3 -c "p='knowledge/_capture_gate.py';s=open(p).read();o='        out = len(tiktoken.get_encoding(\"cl100k_base\").encode(text)), \"tiktoken cl100k_base\"';open(p,'w').write(s.replace(o,o+'   # probe'))"
python3 knowledge/_validate_package_delta.py        # ⛔ 1 failure: SHIM PROVENANCE chain(a) measure_tokens CHANGED
cp /var/tmp/src.bak knowledge/_capture_gate.py

# --- build the stage (SEED_PREFIXES replayed by hand) + a venv WITHOUT tiktoken
S=/var/tmp/replay/Apollo-Spider-vnext
rm -rf /var/tmp/replay; mkdir -p "$S" /var/tmp/replay/emptytmp /var/tmp/replay/aside
cp apollo-spider/FIRST-SESSION.md "$S/"; cp -r apollo-spider/.github "$S/"
mkdir -p "$S/memento-package"; cp -r apollo-spider/gumdrop/. "$S/memento-package/"
cp -r memento-package/machinery memento-package/claude-plugin "$S/memento-package/"
cp memento-package/README.md memento-package/WHAT-MEMENTO-IS.md "$S/memento-package/"
find "$S" -name __pycache__ -type d -exec rm -rf {} + ; rm -f "$S/memento-package/_CHAIN.md"
# then write GOOD-MORNING.md and _LIVE-STATE.md into "$S/memento-package/" from
# FIRST-SESSION.md §4b's two skeletons, verbatim.
python3 -m venv /var/tmp/replay/nokit
P=/var/tmp/replay/nokit/bin/python3; $P -c "import tiktoken"   # must raise ModuleNotFoundError
cd "$S"
B="env -u TIKTOKEN_CACHE_DIR -u DATA_GYM_CACHE_DIR https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 http_proxy=http://127.0.0.1:9 TMPDIR=/var/tmp/replay/emptytmp"

# --- A: out of the box, tiktoken UNIMPORTABLE, egress dead
$B $P memento-package/machinery/_encoder_home.py --check          # rc 0, "engine: purepy cl100k_base (exact, equality-gated)"
$B $P memento-package/machinery/_encoder_home.py --equality-gate  # rc 2, COULD-NOT-RUN (no reference)
$B CAPTURE_GATE_NO_HEAL=1 $P memento-package/machinery/_gen_chain.py   # rc 1 TODAY — the STOP (⑤ Q1)

# --- E: the mutation, both engines
mv memento-package/_encoder-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4 /var/tmp/replay/aside/
$B $P memento-package/machinery/_encoder_home.py --check          # rc 1, names all 7 paths tried
$B python3 memento-package/machinery/_encoder_home.py --check     # rc 1 with tiktoken present too
mv /var/tmp/replay/aside/9b5ad71b2ce5302211f9c61530b329a4922fc6a4 memento-package/_encoder-cache/

# --- F: the equality gate's mutation, both ways (also selftest arm 8)
$B python3 - <<'EOF'
import sys; sys.path.insert(0,"memento-package/machinery")
import _encoder_home as eh; eh.ensure()
path,_ = eh.locate(); ranks = eh.load_ranks(path); enc = eh.PurePyEncoding(ranks)
a,b = b" the", b" and"
ranks[a],ranks[b] = ranks[b],ranks[a]; enc._cache={}
print("MUTATED  ->", eh.equality_gate(roots=["memento-package"], encoding_override=enc)[0])   # 1
ranks[a],ranks[b] = ranks[b],ranks[a]; enc._cache={}
print("RESTORED ->", eh.equality_gate(roots=["memento-package"], encoding_override=enc)[0])   # 0
EOF

# --- gates (all as at baseline; --pack is PRE-EXISTING red, see ④)
python3 knowledge/_validate_package_delta.py                       # 0 failure(s)
python3 knowledge/_validate_package_delta.py --selftest             # all bites pass
python3 knowledge/_release/_gen_pack_manifest.py --selftest         # 195 bites, 0 fail
python3 knowledge/_release/_gate_release_audit.py --manifest-check  # PASS
python3 knowledge/_release/_gate_release_audit.py --drift           # PASS
python3 knowledge/_release/_gate_frozen_release.py                  # PASS, 3 arms
python3 knowledge/_release/_gate_ci_template.py                     # PASS
python3 knowledge/_release/_gate_pack_docs.py --stage "$S" | tail -2 # 45 finding(s), exit 0
```

### ⑦b — THE 14-LINE PATCH Q1 ROUTE (a) NEEDS (applied to the stage for run C, NOT to the repo)

In `knowledge/_capture_gate.py`, then re-ported verbatim into both `memento-package` copies.
Two hunks. First, a new module-level accessor beside `encoder_home_note()`:

```python
def encoder_home_module():
    """The `_encoder_home` module this file's bootstrap loaded, or None when it found none."""
    return globals().get("_eh_mod")
```

Second, inside `measure_tokens`, in the branch where the heal failed — the ONLY edit to the
function, and it goes strictly BEFORE the estimate return so no tier is displaced:

```python
        if not _heal_tiktoken():
            # ---- s222-D3: the PACK'S OWN EXACT ENGINE, before any estimate. Same vendored
            # cl100k data, real pretokenizer + merges, equality-gated against tiktoken. It
            # NAMES ITSELF (`purepy cl100k_base (exact, equality-gated)`) — never borrows the
            # library's label. This is the cl100k TIER, not a new one: the numbers are
            # byte-identical by construction and by gate, so a chain stamped by one engine
            # still byte-matches a check by the other.
            _eh = encoder_home_module()
            if _eh is not None:
                try:
                    _n, _which = _eh.count(text)
                    _TIERS_SEEN.add("cl100k")
                    return _n, _which
                except Exception:
                    pass
            _TIERS_SEEN.add("estimate")
```

In Apollo's own tree `_eh_mod` is never bound (no helper above `knowledge/`), so
`encoder_home_module()` returns `None` and the source's behaviour is unchanged — verified by the
same reasoning the prior lane's optional-import block declares, and cheap for the conductor to
re-drive.

### ⑦c — THE DOC DELTA THAT FOLLOWS Q1 (ready to paste, do NOT land before the wiring)

`apollo-spider/FIRST-SESSION.md` § Before you start — replace *"Install it. Step 4 of this
session… Today Step 4c reaches that encoder through `tiktoken`, so without the package that step
fails and your first session does not survive the night."* with:

> **Recommended, not required.** Step 4 of this session regenerates the chain — the file that
> makes tomorrow's "good morning" work — and the generator that writes it **refuses to write
> anything at all** unless it can count tokens exactly. It will not guess and then label the
> guess. Without `tiktoken` it still counts exactly, with the encoder this pack carries itself,
> and it says which one it used; `tiktoken` is simply several times faster.

`apollo-spider/build-designer-pack.sh` — replace *"the only one … so the first wrap fails without
it"* with *"the only one, and it is RECOMMENDED rather than required: the pack carries its own
exact encoder for machines that cannot install it."*

---

## ⑧ STORE ROW MINTED

One row, for this document only, via `knowledge/_state.py`'s `add()`:

- `W-247` — `#222 filed report - s222-D3 option B built and proven (exact purepy cl100k engine,
  equality gate 69.4M chars 0 divergences); STOPPED at the frozen shim, and arm 2 of the delta
  gate found not to read the shim at all` · owner `claude` · project `apollo` · opened `222` ·
  closes_when: *"Dave or the conductor has ruled Q1's route (a)/(b)/(c) for wiring
  `measure_tokens` to the fallback, the wiring has landed with the ⑦c doc delta, and the
  `_validate_package_delta.py` arm-2 finding has been ruled (repair, re-scope, or park)"*

No row of Dave's was touched. `W-244`/`W-245`/`W-246` untouched.

---

## ⑨ UNPROVEN / COULD-NOT-RUN — declared and priced

1. **COULD-NOT-RUN — the manifest has never been regenerated with the new module.** Same wall the
   predecessor lane hit: `_gen_pack_manifest.py --probe/--manifest/--stage` all read a NAMED
   COMMIT via `git archive`, and the fence forbids committing. `_encoder_home.py` is already on
   the worktree manifest's file list (it landed at `s222-D2`), so no new path is introduced by
   this lane and no seed-map collision is possible; but `import_closure`, `companion_closure` and
   the gate probe have not been driven over the **new content**. **The conductor must re-run
   `--probe --commit <sha>` and `--manifest --commit <sha>` after the commit and read the closure
   block.** Note also: `_encoder_home` is NOT in `_pack_gate_probe.json`'s gate set today; if it
   is ever added, its `--selftest` returns **rc 2** on a machine without tiktoken, by design.
2. **COULD-NOT-RUN — the `--pack` arm cannot be green before the bake** (④). Pre-existing.
3. **UNPROVEN — Unicode-version drift between the two engines.** `unicodedata` follows the
   running interpreter's Unicode (13.0.0 on this sandbox's Python 3.10.12); the Rust engine
   inside `tiktoken` follows its own, newer, table. A codepoint that is a letter in one and
   unassigned in the other would pretokenize differently. The 69.4 M-character corpus and the 68
   adversarial cases found **zero** such cases, and this is the honest boundary of the word
   "exact": it is exact *as gated*, over real text, not proven over every codepoint in the
   standard. The gate prints the interpreter's Unicode version on every run so the claim always
   carries its conditions. ⬛ Worth re-running the wide gate on a newer Python before the bake.
4. **UNPROVEN — a real designer machine.** Everything here was driven in this Linux sandbox with
   egress broken by proxy and a venv standing in for "never installed". That is a faithful model,
   but it is not a Windows/macOS corporate laptop behind a TLS-inspecting proxy running VS Code +
   Copilot. `s222-D2`/`s222-D3` should both be confirmed on the machine that produced the
   original refusal.
5. **UNPROVEN — same-size scrambled data through the purepy path.** `tiktoken` re-checks the
   content hash of what it reads from the cache; the pure-Python engine does not (a full sha256
   on every cold start is a cost this fallback cannot carry). Same-size corrupted bytes would be
   caught by `--check`'s 4-token assertion and by the equality gate, not at load. Declared in the
   module docstring; `verify(deep=True)` does the full hash on demand.
