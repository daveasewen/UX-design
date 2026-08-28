# #223 — arm 2 of the delta gate opened the packed shim (s223-D4)

**Sub:** Opus build sub · **Conductor:** Fable, session #223 · **Band:** L
**Ruling enacted:** `s223-D4` — *"THE BLIND DELTA-GATE ARM IS REPAIRED BEFORE THE BAKE — THE ARM
MUST ACTUALLY OPEN THE PACKED SHIM BODIES, TOLERATING ONLY THE DECLARED OPTIONAL-IMPORT
DIFFERENCE."*
**File changed:** `knowledge/_validate_package_delta.py` — **272 insertions, 0 deletions**
(purely additive; no reformat, git blame preserved).
**Files NOT changed:** the shim copies were **never edited** — the declared-difference mechanism
did not demand a declaration line in the shim. **The port provenance question is NOT re-opened.**
`PORT_COMMIT_A` (`ba2c9f5`, the fresh route-(a) provenance Dave confirmed at `s223-D1`) is
**untouched and does not appear in the diff.** No re-port, no bump was forced.

---

## 1. Verdict

| | |
|---|---|
| Defect reproduced | ✅ yes, quoted below — gate GREEN with real code drift in **both** packed copies |
| Repair | ✅ `check_shim_bodies()` — opens both packed copies, compares to source **at the port commit** |
| Clean pack still green | ✅ 0 failures (the naive-repoint trap avoided) |
| Both-copies mutation now RED | ✅ names the drifted body, both copies, and the diverging line |
| Other arms moved | ✅ **none** — all 11 pre-existing bites unchanged; 6 new bites added, 17 total pass |

---

## 2. What was actually wrong — and it was wider than the brief assumed

The brief's premise was that the shim's `measure_tokens` differs from source **by one declared
optional import**. Measured, that premise is **too narrow**. Comparing the shim's ported bodies
to `knowledge/_capture_gate.py`, **five of twelve** ported names differ, not one:

```
chain_parts              shim==src:False
read_chain_tk            shim==src:False
measure_tokens           shim==src:False
measurement_degraded     shim==src:False
dofirst_index            shim==src:False
_heal_tiktoken           shim==src:True
BYTES_PER_TOKEN          shim==src:True
DOFIRST_ITEM_RE          shim==src:True
DOFIRST_HOOK_MAX         shim==src:True
DOFIRST_INDEX_TK_MAX     shim==src:True
LS_DELTA_RE              shim==src:True
_TIKTOKEN_HEAL_TRIED     shim==src:True
```

Reading the diffs, the five split into two very different kinds:

* **Prose differences (all five).** The shim deliberately rewrites every ported docstring and
  comment to strip Apollo-internal narration ("Extracted #41…", "[[measure-dont-convert-units]]",
  bite post-mortems). The shim's own docstring declares this per name: *"Ported verbatim,
  `knowledge/_capture_gate.py` lines 1164-1243, with the source's … replaced by …"*.
* **Code differences (only three).** `read_chain_tk` and `measurement_degraded` differ **in prose
  only** — their code is byte-identical once normalised.

Normalising through `ast.unparse` with docstrings stripped, the residual code diff is exactly
**three names, six substitutions**, and every one is already declared in the shim's own prose:

```
!! chain_parts: 12 diff lines      (the _gm_usage import guard dropped; .GM_VOCAB / .LS_VOCAB localised)
== read_chain_tk: IDENTICAL (code-only)
!! measure_tokens: 17 diff lines   (gauge -> _real_gauge() optional import)
== measurement_degraded: IDENTICAL (code-only)
!! dofirst_index: 10 diff lines    (the _gm_usage import guard dropped; .GM_VOCAB localised x2)
== _heal_tiktoken: IDENTICAL (code-only)   ... and all six constants IDENTICAL
```

That measurement **is** the design. It is why a naive repoint goes red on a correct pack, and it
is where the honest tolerance boundary sits.

---

## 3. The design taken

**`check_shim_bodies(repo, git_root)`** — a second half to arm 2, called from
`check_shim_provenance` after the two existing chain checks.

1. **It opens both packed copies** (`memento-package/machinery/` and
   `memento-package/claude-plugin/memento/machinery/`), which is the thing the arm never did.
2. **It compares each declared-ported name to that name's source AT THE PORT COMMIT**
   (`PORT_COMMIT_A`), not at HEAD. Two questions, two checks, composed:
   * *"Does the pack carry what it says it ported?"* → new, `check_shim_bodies`.
   * *"Has the source moved since?"* → existing, unchanged, `_chain(...)`.
   Comparing to the port commit is what lets the check stay stable while the source legitimately
   evolves — **so it never needs a re-port or a `PORT_COMMIT_A` bump to stay honest.**
3. **Normalisation:** `ast.unparse` of the node with docstrings stripped recursively (nested defs
   too — `chain_parts._region_end` has its own rewritten docstring). Both sides are normalised by
   the *same* interpreter, so it is a like-for-like code comparison.
4. **`DECLARED_SHIM_DIFFS`** — a table of `{name: ((label, exact source text, exact shim text,
   times it must apply), ...)}`. Each allowance is a **named, exactly quoted rewrite** of the
   source's code into the shim's code, with a declared occurrence count. The source is rewritten
   by the rules; what remains must be **byte-identical**. Three entries, six rules, matching the
   three names measured above.

### Why this is not a threshold

A rule that stops matching **fails loud** — `"a DECLARED-DIFFERENCE rule no longer applies for
'x' — … expected 1x, found 0x. The allowance is stale, so this gate refuses to compare on a
rewrite it cannot perform"`. It never widens into a silent pass. There is no count, no ratio, no
"N lines of slack". Proven in §4 (d2) and (d3): an edit **inside** the tolerated region still
fires, and a rotted rule refuses.

### DECLARED SCOPE — the limit, stated

**This compares CODE, not prose.** Comments and docstrings are out of the comparison by design,
because the shim deliberately rewrites them and says so per name. **A prose-only edit to a ported
body is NOT caught by this arm.** That is written into the gate above `DECLARED_SHIM_DIFFS` and
into the module docstring as a declared limit, not a silent one. Declaring it was the only honest
option: there is no narrow way to enumerate ~200 lines of intentional prose divergence, and a
gate that went red on a correct pack would be turned off within a session.

### Alternatives rejected

| Alternative | Why rejected |
|---|---|
| **Naive repoint** (point one half at the packed shim, compare raw text) | Measured: **6 findings across 3 names** on a *correct* pack (§4 d1). The trap the brief named. |
| **Diff-line-count tolerance** ("allow ≤ 20 changed lines") | Explicitly forbidden and rightly so — a blind spot that has learnt to count. It would also have to be ~200 to pass on prose, swallowing any real drift. |
| **Frozen expected-hash of the shim bodies baked into the gate** | Proves only "the shim has not changed since the gate was written" — a snapshot, not a *relation to source*. Goes stale on every legitimate re-port and re-introduces exactly the constant-bump coupling `s223-D1` just cleaned up. |
| **Compare to HEAD source rather than the port commit** | Couples the body check to unrelated source evolution; every legitimate source edit would demand a re-port to keep the gate green. Rejected for the same reason the port-commit design was chosen. |
| **Declared-differences block written INTO the shim** (a new repo-wide convention) | Would have re-opened port provenance (the shim copies are the ported artefact) and invented vocabulary on my own authority. Not needed — the shim *already* declares every difference in prose; the gate table is that prose made machine-checkable. **Surfaced as a ruling-shaped question instead (§6 Q2).** |
| **Widen the arm to `measurement_tier`** (ported #219, in the shim, not in `PORTED_FUNCS_A`) | DO-NOT-RULE — scope is Dave's. **Surfaced as §6 Q1.** |

---

## 4. Proof — every command, literal output

### (1) Baseline, HEAD state

```
$ python3 knowledge/_validate_package_delta.py
memento-package delta-audit: 0 failure(s)
  ✅ VERBATIM SET byte-identical (both copies) · shim provenance clean (both chains) · copies identical to each other · no unknown files
exit=0
```
Selftest baseline: **11 bites, all pass** (`✅ _validate_package_delta selftest: all bites pass`).

### (2) THE DEFECT, SEEN — both packed copies edited identically, PRE-repair

Mutation: a real **code**-level insert (`_DRIFT_MARKER = 999`) into `measure_tokens`, applied
identically to both packed copies.

```
mutated: memento-package/machinery/_capture_gate.py
mutated: memento-package/claude-plugin/memento/machinery/_capture_gate.py
=== gate WITH both packed copies mutated identically (pre-repair) ===
memento-package delta-audit: 0 failure(s)
  ✅ VERBATIM SET byte-identical (both copies) · shim provenance clean (both chains) · copies identical to each other · no unknown files
exit=0
=== git diff --stat (proof the mutation is real, in BOTH) ===
 memento-package/claude-plugin/memento/machinery/_capture_gate.py | 1 +
 memento-package/machinery/_capture_gate.py                       | 1 +
 2 files changed, 2 insertions(+)
```

**Blindness confirmed at #223, independently of #222.** Reverted clean (`git diff --stat` empty).

### (3) Repair

`knowledge/_validate_package_delta.py`, +272/−0.

### 4(a) Clean tree, post-repair → GREEN

```
memento-package delta-audit: 0 failure(s)
  ✅ VERBATIM SET byte-identical (both copies) · shim provenance clean (both chains) · copies identical to each other · no unknown files
exit=0
```

### 4(b) Both packed copies mutated identically, POST-repair → RED

```
memento-package delta-audit: 2 failure(s)
  ✗ SHIM BODIES: 'measure_tokens' in memento-package/machinery/_capture_gate.py (machinery/) has DRIFTED from knowledge/_capture_gate.py @ ba2c9f5 — 1 line(s) differ BEYOND the declared allowance(s) ['THE ONE DECLARED OPTIONAL IMPORT (the shim's `measure_tokens` docstring: "the real tier is reached through `_real_gauge()` (optional import) rather than a hard module-level `import _gauge_tokens`, because that module is deliberately not shipped here")']. line 2: expected 'if not os.environ.get(_REAL_TIER_ENV):', shim has '_DRIFT_MARKER = 999'
  ✗ SHIM BODIES: 'measure_tokens' in memento-package/claude-plugin/memento/machinery/_capture_gate.py (claude-plugin copy) has DRIFTED from knowledge/_capture_gate.py @ ba2c9f5 — 1 line(s) differ BEYOND the declared allowance(s) [...]. line 2: expected 'if not os.environ.get(_REAL_TIER_ENV):', shim has '_DRIFT_MARKER = 999'

❌ memento-package delta-audit FAILED — 2 finding(s) above.
exit=1
```
Names the drifted body, **both** copies, the allowance it exceeded, and the diverging line.
Reverted clean.

### 4(c) Source mutated → still RED as before (run in a /tmp fixture, real source untouched)

```
  ✗ SHIM PROVENANCE chain(a): 'measure_tokens' in knowledge/_capture_gate.py has CHANGED since the port commit ba2c9f5 — 1 line(s) differ. …
  chain(a) CHANGED-since-port fired: True
  shim-body check stayed quiet (source-only edit): True
```
The pre-existing behaviour is intact, and the new sub-check correctly says nothing about a
source-only edit — that is the other check's question.

### 4(d) The declared optional-import difference ALONE → GREEN

```
  check_shim_bodies on the real repo: GREEN (0 findings)
```

### (d1) The allowances are LOAD-BEARING — the naive-repoint result, measured

```
=== (d1) IS THE ALLOWANCE LOAD-BEARING? empty the table -> the naive repoint's result ===
  with NO allowances: 6 finding(s) — names: ['chain_parts', 'dofirst_index', 'measure_tokens']
  restored; real repo again: GREEN
```

### (d2) The allowance is NARROW — an edit *inside* the tolerated region still fires

```
  ✗ SHIM BODIES: 'measure_tokens' in memento-package/machinery/_capture_gate.py (machinery/) has DRIFTED from knowledge/_capture_gate.py @ ba2c9f5 — 2 line(s) differ BEYOND the declared allowance(s) [...]
  narrow (edit inside the allowance still fires): True
```
(`gauge = _real_gauge()` → `gauge = _real_gauge_RENAMED()` — inside the one tolerated region.)

### (d3) A rotted allowance fails LOUD

```
   SHIM BODIES: a DECLARED-DIFFERENCE rule no longer applies for 'read_chain_tk' — a rule whose source text does not exist — its source text was expected 1x, found 0x. The allowance is stale, so this gate refuses to compare on a rewrite it cannot perform (quoted source text: 'NO_SUCH_TEXT_XYZ')
```

### (5) No other arm's verdict moved

Full `--selftest`: **17 bites, all pass** (11 pre-existing verbatim, 6 new). Every pre-existing
bite's quoted output is character-identical to its baseline. Six new bites added so the repair has
a consumer:

* **ARM2(e)** — both packed copies edited identically → caught, names both copies.
* **ARM2(e) control** — the cross-copy arm stays **silent** in the same fixture, proving arm 2b is
  what saw it (the copies really are still identical to each other; arm 3 is not being silenced).
* **ARM2(f)** — an edit inside the declared-difference region still fails (narrowness).
* **ARM2(g)** — a rule that no longer matches fails loud (rot).
* **ARM2(h)** — with the real table restored the real pack is green (no vacuous pass).

### (6) Working tree, containment

```
$ git diff --numstat -- knowledge/_validate_package_delta.py
272     0       knowledge/_validate_package_delta.py
$ git diff -U0 -- knowledge/_validate_package_delta.py | grep '^-' | grep -v '^---'
(no output — zero deletions)
$ git status --short -- memento-package/
(empty — shim copies untouched)
$ git diff -- knowledge/_validate_package_delta.py | grep "PORT_COMMIT_A ="
(empty — the constant is NOT in the diff)
$ grep -n "^PORT_COMMIT_A" knowledge/_validate_package_delta.py
105:PORT_COMMIT_A = "ba2c9f5"   # ★ #222 RE-PORT: …
$ python3 -m py_compile knowledge/_validate_package_delta.py
compiles OK
```
Help gate still fires correctly on `--help`.

⚠ **Tree hygiene note:** `git status` at the end shows other modified files
(`apollo-spider/build-designer-pack.sh`, `knowledge/_release/_gate_frozen_release.py`,
`knowledge/_release/_gen_pack_manifest.py`, `knowledge/_validate_descender_computed.py`,
`knowledge/_validate_state_contrast.py`). **None of these are mine** — they were absent from my
baseline `git status` and appeared during my run, i.e. other #223 subs are working the same tree.
My change is confined to `knowledge/_validate_package_delta.py`.

---

## 5. UNPROVEN / COULD-NOT-RUN

* **UNPROVEN — cross-interpreter stability of the quoted allowances.** All work ran on **Python
  3.10.12**. The `DECLARED_SHIM_DIFFS` rules are literal strings matched against `ast.unparse`
  output; `ast.unparse` formatting is not contractually stable across CPython versions. If CI runs
  a different minor version and unparse renders (say) `(n, how) =` differently, the rules would
  stop matching. **This degrades safely** — it fails loud as a rotted allowance (ARM2(g)'s shape),
  never a silent pass — but it would be a CI red that is an artefact, not a drift. **I did not run
  this gate under any other Python version.** Priced todo: pin or probe the CI interpreter, or
  re-derive the rule text at runtime from the port-commit source.
* **UNPROVEN — the gate under CI.** I ran it locally only. The `--selftest` path calls `git show`
  against `ba2c9f5`, which requires full history; a shallow CI clone would fail loud
  (`SHIM BODIES: could not read … — <git error>`), not silently.
* **COULD-NOT-RUN — nothing.** No step was blocked.
* **Not attempted (out of scope, DO-NOT-RULE):** extending the body check to chain (b)'s
  `GM_VOCAB`/`LS_VOCAB` as they sit *in the shim*, and to `measurement_tier`.

---

## 6. Ruling-shaped questions for Dave

**Q1 — arm 2b's scope.** It currently covers the 12 names in `PORTED_FUNCS_A + PORTED_CONSTS_A`.
The shim also declares **`measurement_tier` (ported #219)** and **`GM_VOCAB` / `LS_VOCAB`** (chain
(b), ported *into* the shim) — both are ported bodies living in the packed copies with **no body
check on them**. `measurement_tier` is the one that bit before: the packed generator died on
`AttributeError` because the shim lacked it. Widen arm 2b to cover them? *(Left alone — the brief
names arm scope as Dave's.)*

**Q2 — where declared differences should live.** I put the allowance table in the **gate**, because
the shim already declares every difference in prose and putting it there touched no packed file.
The alternative is a machine-readable declared-differences block **in the shim** (the artefact
declaring its own deltas, gate merely reading them). That is a new repo-wide convention and it
re-opens port provenance, so I did not build it. Worth a ruling if this pattern recurs.

**Q3 — the declared prose blindness.** Arm 2b compares code, not comments/docstrings. A ported
body's *prose* can drift in the pack unseen. Accept as a permanent declared limit, or is a
follow-on wanted?

---

## 7. REPLAY-THESE

```bash
cd <repo>

# the repair, green on a correct pack
python3 knowledge/_validate_package_delta.py

# all 17 bites, including the 6 that did not exist before #223
python3 knowledge/_validate_package_delta.py --selftest

# THE DEFECT, RE-SEEN: stash the repair and watch the same mutation go green
#   (mutate BOTH packed copies identically, then run the gate)
python3 - <<'PY'
COPIES=["memento-package/machinery/_capture_gate.py",
        "memento-package/claude-plugin/memento/machinery/_capture_gate.py"]
OLD="    if not os.environ.get(_REAL_TIER_ENV):"
NEW="    _DRIFT_MARKER = 999\n    if not os.environ.get(_REAL_TIER_ENV):"
for p in COPIES:
    t=open(p).read(); assert t.count(OLD)==1
    open(p,"w").write(t.replace(OLD,NEW))
PY
python3 knowledge/_validate_package_delta.py     # post-repair: 2 findings, both copies named
python3 - <<'PY'
COPIES=["memento-package/machinery/_capture_gate.py",
        "memento-package/claude-plugin/memento/machinery/_capture_gate.py"]
NEW="    _DRIFT_MARKER = 999\n"
for p in COPIES:
    t=open(p).read(); assert t.count(NEW)==1
    open(p,"w").write(t.replace(NEW,""))
PY
git diff --stat -- memento-package/            # must be EMPTY

# containment
git diff --numstat -- knowledge/_validate_package_delta.py   # 272  0
```
