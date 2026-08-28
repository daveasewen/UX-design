# `#222` — `s222-D3` route (a): the re-port that wires `measure_tokens` to the fallback

session: `#222` · 2026-08-28 · model: Opus · one lane
predecessor: `notes/_subreports/2026-08-28-222-fallback-encoder.md` (its ⑤ Q1 route (a), its ⑦b
patch, its ⑦c doc delta) · brief fence: `notes/_briefs/2026-08-28-222-fallback-encoder-brief.md`
rulings read at HEAD from `knowledge/_rulings.json`: `s222-D2`, `s222-D3` (read only, untouched)
region: `knowledge/_capture_gate.py` · `memento-package/machinery/_capture_gate.py` ·
`memento-package/claude-plugin/memento/machinery/_capture_gate.py` ·
`apollo-spider/FIRST-SESSION.md` · `apollo-spider/build-designer-pack.sh`
⛔ **NOT touched:** any gate file (`_validate_package_delta.py` included — arm 2's defect is a
priced separate lane) · `knowledge/_rulings.json` · `apollo-spider/dist/` · the conductor's dirty
`_pack_manifest.json` / `_pack_gate_probe.json` / `_state.json` rows other than my own · no
commit, no push, no bake, no `_build_all.py`

---

**VERDICT: THE WIRE IS LAID AND FULLY PROVEN — AND ONE HALF OF THE GATE'S DOCUMENTED REMEDY
CANNOT LAND WITHOUT A COMMIT, SO THE DELTA GATE IS RED BY CONSTRUCTION UNTIL THE CONDUCTOR
COMMITS.** Every behavioural claim in the mission is now measured on the REPO's own files rather
than a `/var/tmp` overlay: out-of-box check green naming `purepy…`, chain generation green naming
the true engine, byte-identical chain across the two engines in both directions, both mutations
firing. The docs delta is landed. Nine of the ten gate readings are exactly at baseline. The
tenth — `_validate_package_delta.py`, 0 → **1 failure** — is the gate's own re-port alarm firing
correctly on an uncommitted source change, and its remedy's second half (bump the shim docstring
and `PORT_COMMIT_A` to the commit that carries the change) needs a sha that does not exist yet.
**That is ⑤ Q1, and it is the only thing standing between this tree and a green delta audit.**

**COUNTS:** files edited **5** · files added 1 (this report) · gate files edited **0** · lines
added to the three `_capture_gate.py` copies **33 each, byte-identical** · gates re-run **11**
(9 at baseline · 1 pre-existing red, named · 1 off-baseline by exactly the structural finding) ·
proof-matrix rows driven **17** · engines compared 2 · mutation directions driven **4** ·
equality-gate corpus 35 files / 566,317 chars / 145,848 tokens, **0 divergent tokens** ·
ruling-shaped questions **3** · UNPROVEN 3 · COULD-NOT-RUN 2

---

## ⓪ THE PREMISE, REPLAYED FIRST

HEAD `36754e2`, plus the conductor's dirty `_pack_manifest.json` / `_pack_gate_probe.json` /
`_rulings.json` / `_state.json` (all left alone) and two untracked conductor documents
(`notes/_briefs/2026-08-28-222-fallback-encoder-brief.md`,
`notes/_briefs/2026-08-28-222-release-plan-v1.md` — neither mine, neither touched).

**One premise of the mission did not survive the replay, and it is the whole story of this
report:** the mission expects "all pack gates back at their baselines … delta-audit 0". It cannot
be 0 in an uncommitted tree that carries route (a). ⑤ Q1 carries the measurement and the reason.

Two premises that DID survive, both re-driven rather than inherited:

| premise from the predecessor's report | replayed verdict |
|---|---|
| `_gen_chain.py` cannot reach the fallback as the tree stands | **TRUE** — and it does now, ② C1 |
| the source's behaviour in Apollo is unchanged by the patch | **TRUE, isolated** — `encoder_home_module()` → `None`, `measure_tokens('the quick brown fox')` → `(13, 'real')` in `knowledge/`, and the pre-existing `_CHAIN.md` STALE reading is byte-for-byte the same with the PRISTINE source swapped back in (single-variable isolation, ④) |

---

## ① WHAT WAS ENACTED — ROUTE (a), THE RE-PORT

Two hunks, and the **same two hunks in all three files**, which is what a re-port means. Applied
by one idempotent script that asserts each anchor is unique and `ast.parse`s the result before
writing, so a patch that does not parse is never a patch.

**Hunk 1 — a new module-level accessor.** New name, so no audited segment moves:

```python
def encoder_home_module():
    """The `_encoder_home` module this file's bootstrap loaded, or None when it found none.

    ⚠ A READ of what the bootstrap already did — it never imports, never searches, never
    falls back. Apollo's own tree carries no `_encoder_home.py` above `knowledge/`, so
    `_eh_mod` is never bound there, this returns None, and the measurement cascade below is
    byte-for-byte the behaviour it had before `s222-D3`. In the released pack the bootstrap
    DOES bind it, and `measure_tokens` can reach the pack's own exact encoder."""
    return globals().get("_eh_mod")
```

In the two shim copies it sits directly beneath `encoder_home_note()` (its natural neighbour —
the same bootstrap's other reader). In `knowledge/_capture_gate.py` there is no
`encoder_home_note()` to sit beside — the s222-D2 lane added the bootstrap to the shims only —
so it sits immediately above `measure_tokens`. **The function body is byte-identical in all
three:** sha256 `785bf3d71f7b…` × 3.

**Hunk 2 — the fallback tier, strictly before the estimate return**, inside the branch where the
heal failed. sha256 of the inserted block `1fb988018b27…` × 3, 961 characters each:

```python
        if not _heal_tiktoken():
            # ---- s222-D3: the PACK'S OWN EXACT ENGINE, before any estimate. Same vendored
            # cl100k data, real pretokenizer + merges, equality-gated against tiktoken. It
            # NAMES ITSELF (`purepy cl100k_base (exact, equality-gated)`) — never borrows the
            # library's label, because a fallback wearing the real library's name is a silent
            # fallback. This is the cl100k TIER, not a new one: the numbers are byte-identical
            # by construction and by gate, so a chain stamped by one engine still byte-matches
            # a check by the other. Nothing here can return an unlabelled number.
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

**And one docstring sentence**, because `measure_tokens`'s own first paragraph enumerated the
cascade and would otherwise have gone stale on the line that describes it — the exact defect
class the file argues against. "otherwise the MEASURED byte divisor, labelled ESTIMATE. All
three are declared…" becomes "otherwise — `s222-D3` — the pack's OWN exact cl100k engine over
its vendored data, which names itself; otherwise the MEASURED byte divisor, labelled ESTIMATE.
Every tier is declared…". Same sentence in all three files.

**Why this and not the shortcut.** Nothing registers itself as `tiktoken` in `sys.modules`; the
engine string is the fallback's own. `s222-D3` requirement 2 is carried at the only place that
can carry it — the function that prints it.

---

## ② THE DOCUMENTED REMEDY, QUOTED — AND WHERE IT RUNS OUT OF ROAD

The gate states its remedy in two places, and I followed the half that fits inside the fence.

**`knowledge/_validate_package_delta.py:308-311`** — the failure this lane's source edit trips,
and its instruction:

```python
                fails.append(f"SHIM PROVENANCE {chain_label}: {n!r} in {cur_relpath} has "
                             f"CHANGED since the port commit {commit} — {dl} line(s) differ. "
                             f"{COPY_A}/{SHIM_NAME} may now be stale against its declared "
                             f"source; re-review and re-port, or update the docstring.")
```

**`knowledge/_validate_package_delta.py:260-264`** — the other half, the pointer:

```python
    elif m_a.group(1) != PORT_COMMIT_A:
        fails.append(
            f"SHIM PROVENANCE: {COPY_A}/{SHIM_NAME}'s docstring now claims it was ported "
            f"from {SHIM_SOURCE_FILE_A} @ {m_a.group(1)}, but this gate is built against "
            f"{PORT_COMMIT_A} — the shim was re-ported and the gate was not updated to match.")
```

**`knowledge/_validate_package_delta.py:94-102`** — the precedent, in the gate's own words,
naming itself the remedy path:

```python
PORT_COMMIT_A = "9dcf62d"   # ★ #149 RE-PORT: chain_parts had drifted since c853b0a
# … All three were re-reviewed and re-ported into the shim, the shim's docstring
# now declares this commit, and this constant follows it — the gate's own remedy path ("the shim
# was re-ported and the gate was not updated to match.")
```

**"re-review and re-port" — DONE, and inside the fence.** Both shim copies received the identical
hunks; the byte-identity is measured above, and arm 3 (cross-copy) is green on it.

**"the shim's docstring now declares this commit, and this constant follows it" — CANNOT BE DONE
HERE, and the reason is structural rather than a judgement call.** Both pointers must name a
commit whose `knowledge/_capture_gate.py` blob already carries the new `measure_tokens`. My
change is uncommitted, so no such commit exists, and the fence forbids making one.

**Driven, not reasoned — the precedent has never faced this.** Every historical bump of
`PORT_COMMIT_A` pointed at an ALREADY-EXISTING, EARLIER commit:

| bump commit | date | pointed at | that commit's date |
|---|---|---|---|
| `c4bf3ff` (#149) | 2026-08-11 | `9dcf62d` | 2026-08-09 |
| `48403b7` (#113) | 2026-08-06 | (prior) | earlier |
| `01e8baa` (#78) | 2026-08-02 | (prior) | earlier |

In every prior case the source had drifted *in history* and the re-port was the catch-up. This is
the first time the source change and the re-port are being authored together, and in that
direction the remedy's second half is a **retrospective** pointer that can only be written after
the commit. **The remedy exists exactly as documented; it is not weakened, not re-scoped, and its
second half is the conductor's one motion.** ⑤ Q1.

---

## ③ PROOF — DRIVEN ON A FRESH STAGE, NOT AN OVERLAY

⚠ The predecessor's run C was an overlay applied to `/var/tmp` copies. **This one is not.** The
stage is built from the repo's own now-patched files, so every row below is a measurement of what
the conductor would commit.

Stage `/var/tmp/s222ra/stage/Apollo-Spider-vnext/`, built by replaying the predecessor's
`SEED_PREFIXES` recipe by hand, plus `GOOD-MORNING.md` and `_LIVE-STATE.md` written verbatim from
`FIRST-SESSION.md`'s two §4b skeletons. `tiktoken` made unimportable by a **venv without it**
(`/var/tmp/s222ra/nokit`, `ModuleNotFoundError` confirmed), not a shadow module — same reasoning
the predecessor gives: a venv models "never installed", which is the designer's real failure, and
it lets `_heal_tiktoken()` fail for the real reason. `/tmp/data-gym-cache`,
`/var/tmp/data-gym-cache` and `~/.cache/tiktoken` confirmed **absent** before the runs. Egress
broken by a dead proxy on port 9. Every run wrapped in:

```
env -u TIKTOKEN_CACHE_DIR -u DATA_GYM_CACHE_DIR \
    https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 http_proxy=http://127.0.0.1:9 \
    TMPDIR=/var/tmp/s222ra/emptytmp CAPTURE_GATE_NO_HEAL=1
```

### A — OUT OF THE BOX, tiktoken UNIMPORTABLE, EGRESS DEAD

| # | command | result | rc |
|---|---|---|---|
| A1 | `_encoder_home.py --check` | `ENCODER OK — engine: purepy cl100k_base (exact, equality-gated) — 4 tokens, measured with the encoder data inside this pack (no download, no environment variable to set).` | **0** |
| A2 | `_encoder_home.py --equality-gate` | `⛔ EQUALITY GATE COULD-NOT-RUN — the reference engine is not here…` — correctly NOT green | **2** |
| A3 | `_encoder_home.py --selftest` | `0 failure(s), 1 could-not-run` — 9 arms, the mutation arms need the reference | **2** |
| A5 | `_capture_gate.measure_tokens("the quick brown fox")` | **`(4, 'purepy cl100k_base (exact, equality-gated)')`** · tier `cl100k` · `measurement_degraded()` **False** | — |

**A5 is the STOP, cleared.** The predecessor measured `(5, 'bytes/3.53 ESTIMATE (tiktoken
absent)')` here — five tokens where the truth is four, on the estimate tier, degraded. The frozen
shim now asks the helper, and gets the exact count with the fallback's own name on it.

### C — THE CHAIN, THROUGH THE FALLBACK

| # | command | result | rc |
|---|---|---|---|
| C1 | `_gen_chain.py` | `✅ _CHAIN.md: 867 purepy cl100k_base (exact, equality-gated) · GM header+LATEST 144 tk · LS whole ⏱ section 45 tk · FILE 867 … = slice 189 + wrapper 678 · fixed point in 2 pass(es)` | **0** |
| C2 | `_gen_chain.py --check` | `✅ _CHAIN.md is FRESH — byte-matches the live chain` | **0** |
| C4 | the plugin mirror, three levels deeper, same env | `(4, 'purepy cl100k_base (exact, equality-gated)')` | — |

### D — THE EQUIVALENCE, BOTH DIRECTIONS

| # | command | result |
|---|---|---|
| D1 | same stage, **system python3 (real tiktoken)**, egress still dead | `✅ _CHAIN.md: 867 tiktoken cl100k_base · … fixed point in 2 pass(es)` rc 0 |
| D2 | `cmp` of the two generated `_CHAIN.md` | **BYTE-IDENTICAL** — sha256 `fe70784b35f2507637e8449e90157c3e0604894014e5387e6690e6ac96b08205` both, and the same sha the predecessor's overlay produced |
| D3 | chain built by **purepy**, `--check` run under **tiktoken** | `✅ _CHAIN.md is FRESH — byte-matches the live chain · FILE 867 tiktoken cl100k_base` rc 0 |
| D4 | `--equality-gate` on the stage, reference present | `✅ PASSED — 68 adversarial cases · 35 files · 566,317 characters · 145,848 tokens — every token identical` · timings on that corpus: `tiktoken 0.04s · purepy 0.18s (4× slower)` |

D2/D3 are the exactness claim in its strongest available form: the two engines are
**substitutable inside the pack's own artefact**, in both directions, tier stamp included.

### E / F — THE MUTATIONS, BOTH WAYS, BOTH ENGINES

| # | mutation | result |
|---|---|---|
| E1a | data file aside, **tiktoken unimportable**, `--check` | names all 8 candidate paths, then `⛔ REFUSED — this pack cannot measure tokens out of the box.` **rc 1** |
| E2a | same, **tiktoken present**, `--check` | **rc 1** — requirement 4 holds on BOTH engines |
| E1b | same, `_gen_chain.py`, tiktoken absent | `ENCODER-HOME:` block, then `✗ _CHAIN.md NOT generated — … MEASUREMENT REFUSAL` **rc 1**, `_CHAIN.md` **not written** (verified by `ls`) |
| E2b | same, `_gen_chain.py`, tiktoken present | **rc 1**, no file |
| E3 | file restored | `--check` green both interpreters; chain regenerates to the same sha `fe70784b…` **rc 0** |
| F1 | **merge ranks corrupted** (`b" the"` ↔ `b" and"` swapped — table keeps its size, merge ORDER changes) | `⛔ EQUALITY GATE FAILED on adversarial case 67 '**11,032 real — the unit is THE WHOLE FILE**'` **rc 1** |
| F2 | corruption undone | `✅ EQUALITY GATE PASSED … every token identical` **rc 0** — the gate is not reporting on its own footprint |

**The refusal never softened.** A missing data file still refuses on BOTH engines and still
writes no chain — the fallback is a second exact tier, not a second chance to guess.

---

## ④ GATE VERDICTS

| gate | baseline (predecessor's ⓪/④) | now | reading |
|---|---|---|---|
| `knowledge/_validate_package_delta.py` | 0 failure(s) | ⛔ **1 failure** | **THE ONE OFF-BASELINE READING** — the arm-2 re-port alarm, quoted in full below. Structural, ⑤ Q1 |
| `…_delta.py --selftest` | all bites pass | ⛔ **1 bite** — `real repo: clean (0 findings; got 1: …)` | the SAME finding seen through the selftest's own "no false positive on the live tree" bite. **Every mutation bite still passes** — the gate's teeth are intact, nothing was weakened |
| `knowledge/_release/_gen_pack_manifest.py --selftest` | 195 bites, 0 fail | **195 bites, 0 fail** | at baseline |
| `_gate_release_audit.py --manifest-check` | PASS at `36754e2` | **PASS** — byte-identical fresh generation at `36754e247a2c`, 1645 files, sha `0d5f969e9efe4120` | at baseline |
| `_gate_release_audit.py --drift` | PASS | **PASS** — manifest generated at HEAD | at baseline |
| `_gate_release_audit.py --pack` | ⛔ RED, pre-existing | ⛔ **RED, same shape** — 29 files differ, first five identical to the predecessor's list (`FIRST-SESSION.md`, `ci-template/README.md`, `ci-template/run-gates.py`, `knowledge/_render/_bento_edit_rails.json`, `knowledge/_validate_descender_computed.py`) | **PRE-EXISTING AND NOT THIS LANE'S.** `check_pack()` compares the zip to the manifest COMMIT's git blobs, never the working tree — no uncommitted edit is visible to it. Clears on the bake |
| `_gate_frozen_release.py` | PASS, 3 arms | **PASS, 3 arms, no frozen surface moved** | at baseline — and this is the arm that would have caught an illegal `memento-package` move |
| `_gate_ci_template.py` | PASS | **PASS** | at baseline |
| `_gate_pack_docs.py --stage <my stage>` | 45 findings, ADVISORY, exit 0 | **45 finding(s), ADVISORY, exit 0** | at baseline — **the doc delta adds ZERO net findings** |
| `_encoder_home.py --selftest` (repo, tiktoken present) | 0 fail, 0 could-not-run, 9 arms | **0 failure(s), 0 could-not-run**, 9 arms | at baseline |
| `_encoder_home.py --selftest` (stage, tiktoken absent) | 0 fail, 1 could-not-run, rc 2 | **same**, rc 2 | at baseline — correct and named |

**The one off-baseline reading, in full:**

```
memento-package delta-audit: 1 failure(s)
  ✗ SHIM PROVENANCE chain(a): 'measure_tokens' in knowledge/_capture_gate.py has CHANGED since
    the port commit 9dcf62d — 22 line(s) differ. memento-package/machinery/_capture_gate.py may
    now be stale against its declared source; re-review and re-port, or update the docstring.
```

⬛ **Read it precisely.** The gate is not reporting a defect in the wire — it cannot see the wire
at all. Arm 2 compares `knowledge/_capture_gate.py` @ working tree against itself @ `9dcf62d`
(the arm-2 defect the predecessor measured and priced, `:313`, untouched here). What it is
telling the conductor is exactly what it was built to tell: *the source moved; go re-port and
re-point.* The re-port is done and byte-proven; the re-point is the commit.

**Two reds that are NOT this lane's, isolated rather than asserted:**

1. `python3 knowledge/_capture_gate.py --selftest` is **RED at HEAD** with the same three bites
   (`M10: a fat §A/§C warned the CHAIN`, `M10: an ordinary chain warned`, `#70/#71 non-catch:
   _gen_chain.py --selftest is NOT green`). Proven by running it inside a pristine
   `git archive HEAD` extraction — same three, before any edit of mine. It is not on the
   predecessor's baseline list; it is on the record now.
2. `python3 knowledge/_gen_chain.py --check` reads **STALE** in the repo. Isolated by
   single-variable swap: with the PRISTINE `knowledge/_capture_gate.py` copied back in, the
   reading is byte-for-byte the same STALE line, then the patched file was restored and verified
   by `cmp`. It is the conductor's mid-session GM/LS drift, not this lane's. (The pristine
   archive cannot arbitrate this one at all — a bare checkout can never agree with a `real`
   stamp, `#173`, [[gate-cannot-pass-in-one-environment]].)

---

## ⑤ RULING-SHAPED QUESTIONS → CONDUCTOR / DAVE

### Q1 — THE ONE MOTION LEFT: the two-commit dance, and its unavoidable red middle

The remedy's second half needs a commit. Three sub-questions in one, and only the conductor can
answer them because all three live outside this lane's fence.

**The sequence, exactly:**

```
commit 1 — the wire:   knowledge/_capture_gate.py + both memento-package/_capture_gate.py copies
                       + apollo-spider/FIRST-SESSION.md + apollo-spider/build-designer-pack.sh
                       ⛔ the delta gate is RED at this commit, by construction
commit 2 — the point:  memento-package/machinery/_capture_gate.py:12          `9dcf62d` → <sha of commit 1>
                       memento-package/claude-plugin/memento/machinery/_capture_gate.py:12   likewise
                       knowledge/_validate_package_delta.py:94  PORT_COMMIT_A = "<sha of commit 1>"
                       ✅ the delta gate goes green here and not before
```

⚠ **Commit 1 is red on arm 2 and CANNOT be made green.** Both pointers must name commit 1, and
commit 1 cannot name itself. This is new: every prior bump (#78, #113, #149) pointed at an
already-existing earlier commit, so the precedent never had a red middle. **The question for the
conductor: is a knowingly-red intermediate commit acceptable here, or should the wire and the
point land as one commit followed immediately by an amend?** An amend rewrites commit 1's sha and
would falsify the pointers written against it, so the amend route needs care — the two-commit
sequence above is the one that terminates.

⛔ **Do not shortcut this by pointing `PORT_COMMIT_A` at `9dcf62d` and calling the shim's
declaration true.** That is the provenance lie route (a) exists to prevent.

### Q2 — the doc delta is landed; `_gen_chain.py`'s own refusal message is now stale

Requirement 6 is discharged (⑥) and pack-docs adds zero findings. But the refusal that fires when
the data file is missing still says, in `_gen_chain.py`'s frozen words (measured at E1b):

> `Re-run once tiktoken is installed and can reach openaipublic.blob.core.windows.net (the
> cl100k_base encoding file)`

That sentence names a network host the pack no longer needs and a package that is no longer
required — it is `s222-D2`+`s222-D3` stale, and it is the first thing a designer reads when
something goes wrong. **I did not touch it: `_gen_chain.py` is a VERBATIM-SET file and Apollo's
own chain generator, so the region is the conductor's** and a matched-triple edit there is
exactly what the predecessor's route (c) was fenced out of. ⬛ Conductor: worth a lane, and it is
cheap — one string, three copies.

### Q3 — arm 2 still does not read the shim, and this lane just relied on that

Untouched and unrepaired, as fenced. But note what it means for what you are about to commit:
**nothing in the tree checks that my two shim copies actually received the re-port.** The
byte-identity in ① is my measurement, not a gate's. Arm 3 (cross-copy) proves the two copies
agree with each other; nothing proves either agrees with the source. The predecessor priced the
repair and named why it is not a one-line repoint (the shim's `measure_tokens` legitimately
differs — `_real_gauge()` as an optional import — so a naive repoint goes red on a correct pack).
⬛ **That ruling is now load-bearing rather than theoretical**, because a real re-port has just
gone through the blind spot.

---

## ⑥ FILES TOUCHED (for the conductor's reconcile)

**Edited (5):**
- `knowledge/_capture_gate.py` — hunk 1 (`encoder_home_module()`), hunk 2 (the fallback tier),
  one docstring sentence. **+33 lines.** Behaviour in Apollo's own tree is unchanged and measured
  so: `encoder_home_module()` → `None`, `measure_tokens` → `(13, 'real')`.
- `memento-package/machinery/_capture_gate.py` — the same two hunks and the same sentence,
  byte-identical. **+33 lines.**
- `memento-package/claude-plugin/memento/machinery/_capture_gate.py` — likewise. **+33 lines.**
- `apollo-spider/FIRST-SESSION.md` — § Before you start: the predecessor's ⑦c paragraph pasted
  verbatim in place of *"Install it. Step 4 … does not survive the night."*, **plus one clause
  beyond the ⑦c text, declared here**: the lead sentence read "You need Python 3, VS Code with
  GitHub Copilot, and **one Python package**", which would have contradicted "Recommended, not
  required" two lines below it — the miscommunication class Dave paid hours for at #218. It now
  reads "You need Python 3 and VS Code with GitHub Copilot. There is **one Python package**, and
  it is recommended rather than required — see below."
- `apollo-spider/build-designer-pack.sh` — the generated pack README's "What you need installed",
  ⑦c's replacement plus the following sentence brought into line with it ("with `tiktoken` it does
  that faster, without it the pack's own engine does it").

**Added (1):** `notes/_subreports/2026-08-28-222-route-a-report.md` — this file (row minted, ⑧).

**Deliberately NOT edited:** every gate file · `knowledge/_rulings.json` ·
`knowledge/_release/_pack_manifest.json` / `_pack_gate_probe.json` (the conductor's dirty pair) ·
`memento-package/machinery/_gen_chain.py` in any copy (Q2) · `apollo-spider/dist/` ·
`apollo-spider/gumdrop/machinery/_encoder_home.py` (the predecessor's, already correct) ·
`W-244`–`W-247` (not mine) · both untracked conductor briefs.

---

## ⑦ REPLAY-THESE (verifier — exact commands)

```sh
# --- the re-port is byte-identical across all three copies (the claim ① makes)
python3 - <<'EOF'
import ast, hashlib
ps=['knowledge/_capture_gate.py','memento-package/machinery/_capture_gate.py',
    'memento-package/claude-plugin/memento/machinery/_capture_gate.py']
for p in ps:
    s=open(p).read(); t=ast.parse(s)
    for n in t.body:
        if isinstance(n,ast.FunctionDef) and n.name=='encoder_home_module':
            print(p, hashlib.sha256(ast.get_source_segment(s,n).encode()).hexdigest()[:12])
    i=s.index('        if not _heal_tiktoken():'); j=s.index('            _TIERS_SEEN.add("estimate")', i)
    print(' block', hashlib.sha256(s[i:j].encode()).hexdigest()[:12], len(s[i:j]))
EOF
#  -> 785bf3d71f7b × 3   and   block 1fb988018b27 961 × 3

# --- Apollo's own behaviour is unchanged (the source edit is inert above knowledge/)
python3 -c "import sys; sys.path.insert(0,'knowledge'); import _capture_gate as cg; \
print(cg.encoder_home_module(), cg.measure_tokens('the quick brown fox'), cg.measurement_degraded())"
#  -> None (13, 'real') False

# --- build the stage (SEED_PREFIXES replayed by hand) + a venv WITHOUT tiktoken
S=/var/tmp/s222ra2/stage/Apollo-Spider-vnext
rm -rf /var/tmp/s222ra2; mkdir -p "$S" /var/tmp/s222ra2/emptytmp /var/tmp/s222ra2/aside
cp apollo-spider/FIRST-SESSION.md "$S/"; cp -r apollo-spider/.github "$S/"
mkdir -p "$S/memento-package"; cp -r apollo-spider/gumdrop/. "$S/memento-package/"
cp -r memento-package/machinery memento-package/claude-plugin "$S/memento-package/"
cp memento-package/README.md memento-package/WHAT-MEMENTO-IS.md "$S/memento-package/"
find "$S" -name __pycache__ -type d -exec rm -rf {} + ; rm -f "$S/memento-package/_CHAIN.md"
# then write GOOD-MORNING.md and _LIVE-STATE.md into "$S/memento-package/" from
# FIRST-SESSION.md's two §4b skeletons, verbatim.
python3 -m venv /var/tmp/s222ra2/nokit
P=/var/tmp/s222ra2/nokit/bin/python3; $P -c "import tiktoken"   # must raise ModuleNotFoundError
cd "$S"
B="env -u TIKTOKEN_CACHE_DIR -u DATA_GYM_CACHE_DIR https_proxy=http://127.0.0.1:9 \
HTTPS_PROXY=http://127.0.0.1:9 http_proxy=http://127.0.0.1:9 TMPDIR=/var/tmp/s222ra2/emptytmp \
CAPTURE_GATE_NO_HEAL=1"

# --- A: out of the box, tiktoken UNIMPORTABLE, egress dead
$B $P memento-package/machinery/_encoder_home.py --check          # rc 0, "engine: purepy cl100k_base (exact, equality-gated)"
$B $P memento-package/machinery/_encoder_home.py --equality-gate  # rc 2, COULD-NOT-RUN
$B $P -c "import sys; sys.path.insert(0,'memento-package/machinery'); import _capture_gate as cg; \
print(cg.measure_tokens('the quick brown fox'), cg.measurement_degraded())"
#  -> (4, 'purepy cl100k_base (exact, equality-gated)') False      ← the STOP, cleared

# --- C/D: the chain, both engines, byte-identical
$B $P  memento-package/machinery/_gen_chain.py         # rc 0, "867 purepy cl100k_base (exact, equality-gated)"
$B $P  memento-package/machinery/_gen_chain.py --check # rc 0 FRESH
cp memento-package/_CHAIN.md /var/tmp/s222ra2/chain-purepy.md
$B python3 memento-package/machinery/_gen_chain.py --check   # rc 0 FRESH, "FILE 867 tiktoken cl100k_base"
rm -f memento-package/_CHAIN.md
$B python3 memento-package/machinery/_gen_chain.py           # rc 0, "867 tiktoken cl100k_base"
cmp /var/tmp/s222ra2/chain-purepy.md memento-package/_CHAIN.md && echo BYTE-IDENTICAL
sha256sum memento-package/_CHAIN.md    # fe70784b35f2507637e8449e90157c3e0604894014e5387e6690e6ac96b08205
$B python3 memento-package/machinery/_encoder_home.py --equality-gate   # ✅ 68 cases · 35 files · 566,317 ch · 0 divergences

# --- E: the data file aside — the refusal, both engines, no chain written
mv memento-package/_encoder-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4 /var/tmp/s222ra2/aside/
$B $P      memento-package/machinery/_encoder_home.py --check   # rc 1, names all 8 paths tried
$B python3 memento-package/machinery/_encoder_home.py --check   # rc 1 with tiktoken present too
$B $P      memento-package/machinery/_gen_chain.py; ls memento-package/_CHAIN.md  # rc 1, NO FILE
$B python3 memento-package/machinery/_gen_chain.py; ls memento-package/_CHAIN.md  # rc 1, NO FILE
mv /var/tmp/s222ra2/aside/9b5ad71b2ce5302211f9c61530b329a4922fc6a4 memento-package/_encoder-cache/

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

# --- gates (all at baseline except the ONE named structural finding)
python3 knowledge/_validate_package_delta.py                        # ⛔ 1 failure — arm 2 re-port alarm, ⑤ Q1
python3 knowledge/_validate_package_delta.py --selftest              # ⛔ 1 bite: "real repo: clean" — the SAME finding
python3 knowledge/_release/_gen_pack_manifest.py --selftest          # 195 bites, 0 fail
python3 knowledge/_release/_gate_release_audit.py --manifest-check   # PASS at 36754e247a2c
python3 knowledge/_release/_gate_release_audit.py --drift            # PASS
python3 knowledge/_release/_gate_frozen_release.py                   # PASS, 3 arms
python3 knowledge/_release/_gate_ci_template.py                      # PASS
python3 knowledge/_release/_gate_pack_docs.py --stage "$S" | tail -2  # 45 finding(s), exit 0
python3 apollo-spider/gumdrop/machinery/_encoder_home.py --selftest   # 0 fail, 0 could-not-run, 9 arms

# --- the two PRE-EXISTING reds, isolated rather than asserted
rm -rf /var/tmp/base222 && mkdir -p /var/tmp/base222
git archive HEAD | tar -x -C /var/tmp/base222
(cd /var/tmp/base222 && python3 knowledge/_capture_gate.py --selftest 2>&1 | grep -c "^  ❌ selftest: M10")
#  -> 2 at HEAD, before any edit of mine (plus the #70/#71 bite)
```

---

## ⑧ STORE ROW MINTED

One row, for this document only, via `knowledge/_state.py`'s `add()`:

- `W-250` — `#222 filed report - s222-D3 route (a) ENACTED: measure_tokens re-ported in the
  source and BOTH shim copies so the frozen shim reaches the exact purepy fallback (chain
  byte-identical across engines, docs delta landed); the delta gate is red-by-construction until
  the pointer commit` · owner `claude` · project `apollo` · opened `222` · closes_when: *"the
  conductor has landed the report Q1 two-commit sequence (commit 1 = the wire; commit 2 = the
  shim docstring line `:12` in BOTH memento-package copies and `PORT_COMMIT_A` at
  `knowledge/_validate_package_delta.py:94` bumped to commit 1's sha),
  `knowledge/_validate_package_delta.py` reads `0 failure(s)` again, and the pack manifest has
  been re-probed at that commit"*

⚠ **`W-248` was my first attempt and the store REFUSED it — `duplicate id — ids are stable and
NEVER reused`.** The conductor minted `W-248` and `W-249` (the fallback-encoder brief and the
release plan) after the predecessor's report was filed, so the next free id had moved. The refusal
rolled the row back cleanly — `_state.json` was byte-identical to its pre-call backup — and the
lesson is worth the line: **a sub must read the max id at mint time, never inherit it from a
report written earlier the same session.** No row of Dave's or the conductor's was touched;
`W-244`–`W-249` untouched, and a diff of the store before/after confirms exactly one row added,
none removed, none changed.

---

## ⑨ UNPROVEN / COULD-NOT-RUN — declared and priced

1. **COULD-NOT-RUN — the delta gate cannot be green in this tree.** ⑤ Q1. Not a defect and not a
   deferral: the remedy's second half is a retrospective pointer and there is no commit to point
   at. **The verifier must expect `1 failure(s)` here and read the message, not the count.**
2. **COULD-NOT-RUN — the manifest has never been regenerated with the new content.** Same wall as
   both predecessor lanes: `_gen_pack_manifest.py --probe/--manifest/--stage` read a NAMED COMMIT
   via `git archive`, and the fence forbids committing. No new path is introduced by this lane
   (all five edited files are already on the manifest's list, 1645 files, unchanged), so no
   seed-map collision is possible — but `import_closure`, `companion_closure` and the gate probe
   have not been driven over the new content. ⬛ **Conductor: re-run `--probe --commit <sha>` and
   `--manifest --commit <sha>` after commit 1 and read the closure block.**
3. **COULD-NOT-RUN — `--pack` cannot be green before the bake.** Pre-existing, ④, unchanged in
   shape (29 files, same first five). Re-cutting is Dave's under `s219-D4(2)`.
4. **UNPROVEN — the wide equality corpus was not re-driven this lane.** The predecessor's
   69,483,685-character / 21,813,749-token run with 0 divergences stands; I drove the 566,317-char
   stage corpus (0 divergences) because that is the corpus the wire actually feeds. The wide run
   is cheap (~23 s) and worth repeating before the bake, ideally on a newer Python — the
   Unicode-version boundary in the predecessor's ⑨(3) is untouched by this lane and still the
   honest limit of the word "exact".
5. **UNPROVEN — a real designer machine.** Unchanged from the predecessor: everything here is a
   Linux sandbox with a dead proxy and a venv standing in for "never installed". Faithful, but not
   a corporate Windows/macOS laptop behind a TLS-inspecting proxy running VS Code + Copilot.
   `s222-D2` and `s222-D3` should both be confirmed on the machine that produced the original
   refusal — that machine is the reason all three of these lanes exist.
