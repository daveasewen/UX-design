# s225 — the Gumdrop gate-widening: `_gate_pack_docs.py` grows arm 5

*Sub-report for session #225. Enactment sub (Opus). **One file written**, not committed — the
conductor commits. Dave's word for this lane: **widen the GATE, not the strings.** The three
`Memento — Gumdrop v1.0.0` literals are exactly where they were.*

COUNTS: findings 8 / ruling-shaped 4 / UNPROVEN 2

---

## VERDICT IN ONE LINE

`knowledge/_release/_gate_pack_docs.py` now has **five arms, not four**. Arm 5 sweeps every
`Memento — Gumdrop vX.Y.Z` literal in the gate's existing document scope and grades them **against
each other only**. Driven on the real shipped v1.0.2 tree it goes from **silent** to **4 findings**,
naming the defect #224 measured; driven on a swept copy of the same tree it returns to **exactly the
baseline number**, so the arm adds zero noise. **Still ADVISORY, exit 0.** No canonical Gumdrop
version is asserted anywhere in the code — that would have been the gate inventing the ruling Dave
explicitly did not give.

---

## 1. WHAT CHANGED — one file, `knowledge/_release/_gate_pack_docs.py`

`git status --porcelain` after the work, verbatim:

```
 M knowledge/_release/_gate_pack_docs.py
```

Nothing else. No `git add`, no commit, no push. Scratch lived in `_to_delete/` (gitignored) and was
removed; the two staged pack trees under `_to_delete/` were read only, never written.

### 1.1 The new class, and why it is anchored the way it is

`knowledge/_release/_gate_pack_docs.py:109-114`:

```python
# arm 5 — the CARRIED cut, a different version register from VERSION_RE's. Anchored on "Memento"
# so a bare "Gumdrop v…" in prose is not swept: measured on the shipped v1.0.2 tree, every
# occurrence in a shipped `.md` carries the full "Memento — Gumdrop v" spelling, so the anchor
# costs nothing [[unmatched-grep-is-not-an-absence]]. The separator is tolerated as em/en/hyphen
# with any spacing, because a dash is exactly the character a hand-typed literal gets wrong.
GUMDROP_RE = re.compile(r"Memento\s*[—–-]\s*Gumdrop\s+v(\d+\.\d+\.\d+)")
```

The anchor claim is **measured, not assumed** — the probe that licenses it, and its empty result:

```
$ grep -rn "Gumdrop v" --include=*.md _to_delete/Apollo-Spider-v1.0.2/ | grep -v "Memento — Gumdrop v"
(no output)
```

Compare the arm-3 class it sits beside, `_gate_pack_docs.py:107` —
`VERSION_RE = re.compile(r"Apollo-Spider-v(\d+\.\d+\.\d+)")`. That is the **Spider** register. A
pack names two versions; the gate knew one. That is the whole blind spot, in one line.

### 1.2 The verdict is cross-document, so it is taken after the walk

Collection, `_gate_pack_docs.py:195-200`:

```python
        # ---- arm 5: the CARRIED cut. Collected here, graded after every doc is read — the
        # question is cross-document by construction ("do these agree?"), so it cannot be
        # answered from inside the loop.
        for m in GUMDROP_RE.finditer(text):
            checked += 1
            gumdrop.setdefault(m.group(1), []).append((doc, m.group(0)))
```

Verdict, `_gate_pack_docs.py:201-213`:

```python
    # ---- arm 5, the verdict: internal consistency ONLY. ⛔ Never compared to pack_version —
    # that is the Spider version, and no canonical Gumdrop version is ruled. One spelling passes,
    # whatever it says; two spellings is the pack disagreeing with itself about what it carries.
    if len(gumdrop) > 1:
```

**`pack_version` never appears in arm 5.** That is the fence, in code: the arm cannot hard-fail
against an assumed canonical Gumdrop version because it never has one to fail against.

### 1.3 The reading is printed on EVERY run, green or red

`_gate_pack_docs.py:268-282` prints the spread immediately after the `stage:` line, before the
`if not findings` early return — so it appears in a clean run too:

```python
    # arm 5's reading is PRINTED EVERY RUN, green or red. A figure only shown when it is wrong
    # is a figure nobody can baseline [[instrument-without-a-consumer]].
```

Three states, all observed live (§2): **UNRUN** (no literal in scope — says so rather than passing
quietly, the arm-3 precedent at `:387-388` of the HEAD file), **internally consistent**, and
**THEY DISAGREE**.

### 1.4 Advisory convention: inherited, not re-declared

The gate is ADVISORY at birth by its own docstring (`:4-7`) and returns 0 whatever it finds unless
`--strict`. Arm 5 appends into the same `findings` list and therefore inherits that route exactly —
**no new flag, no new promotion surface**. This matches the `_gate_pack_imports.py` precedent (born
ADVISORY at #220) without adding a second advisory mechanism to maintain. Promotion of this whole
gate to blocking remains Dave's word (#221 fence 2), untouched.

---

## 2. THE MUTATION TEST — the gate binary, on real data, both directions

⛔ Not a unit shim. Every number below is `python3 knowledge/_release/_gate_pack_docs.py --stage …`
driven on a real unzipped pack tree, and every "before" is the **HEAD copy of the gate** run on the
same tree in the same shell — not arithmetic.

| stage | HEAD gate | NEW gate | delta | GUMDROP arm |
|---|---|---|---|---|
| `_to_delete/Apollo-Spider-v1.0.2` (the shipped release) | **219 finding(s)** | **223 finding(s)** | **+4** | 4 |
| `_to_delete/bake225/Apollo-Spider-v1.0.3` (the #224 dry-run bake) | **216 finding(s)** | **220 finding(s)** | **+4** | 4 |

Exit code unchanged at **0** on both (ADVISORY). `--strict` on the v1.0.2 stage returns **1**, as it
already did at HEAD — 219 pre-existing findings meant strict was never green there, so that run is
*not* evidence arm 5 alone can drive a red. **The single-variable proof is §2.3.**

### 2.1 IT BITES — the shipped v1.0.2 tree, untouched

```
$ python3 knowledge/_release/_gate_pack_docs.py --stage _to_delete/Apollo-Spider-v1.0.2
pack-docs gate (ADVISORY) — 128 document(s), 421 name(s) resolved, 13 placeholder(s) skipped by name
  ⚠ carried cut, as the shipped documents name it: Memento — Gumdrop v1.0.0 (×2), Memento — Gumdrop
    v1.0.2 (×2) — THEY DISAGREE. ⛔ No canonical Gumdrop version is ruled; this arm grades the
    literals against EACH OTHER only and never says which is right.
  === GUMDROP — 4 finding(s) ===
  [memento-package/runbooks/_RUNBOOK-capture-ritual.md] Memento — Gumdrop v1.0.0  →  the shipped
    documents name 2 different Gumdrop cuts (v1.0.0 ×2, v1.0.2 ×2) — this pack disagrees with itself
    about what it carries. Graded against EACH OTHER only: no canonical Gumdrop version is ruled, so
    this gate does not say which one is right
  [memento-package/runbooks/_RUNBOOK-context-gauge.md] Memento — Gumdrop v1.0.0  →  (same)
  [README.md] Memento — Gumdrop v1.0.2  →  (same)
223 finding(s). ADVISORY — exiting 0.
```

Note the honesty of the printout: **README's own spelling is listed as a finding too.** The arm does
not nominate a winner and grade the others against it.

### 2.2 THE GREEN IS REAL — a swept COPY of the same pack

A byte copy of the shipped tree into `_to_delete/`, both runbook headers moved `v1.0.0 → v1.0.2`
(the copy only; **the shipped strings were never touched**):

```
  carried cut, as the shipped documents name it: Memento — Gumdrop v1.0.2 (×4) — internally consistent.
  === COMMAND — 16 finding(s) ===
  === COUNTS — 2 finding(s) ===
  === PATH — 201 finding(s) ===
219 finding(s). ADVISORY — exiting 0.
```

**219 — the exact HEAD baseline, and the GUMDROP section is gone entirely.** The arm contributes
zero findings to a consistent pack. It is not noise dressed as a gate.

### 2.3 SINGLE-VARIABLE MUTATION — one character class, one line

From that green 219 copy, one literal broken back (`_RUNBOOK-capture-ritual.md:3`, `v1.0.2 → v1.0.1`)
and nothing else:

```
  ⚠ carried cut …: Memento — Gumdrop v1.0.1 (×1), Memento — Gumdrop v1.0.2 (×3) — THEY DISAGREE.
  === GUMDROP — 4 finding(s) ===
223 finding(s).
```

219 → 223 on a one-line change. The arm is the only thing that moved. **This is the clause proven,
not the feature assumed** [[mutation-tests-the-clause-not-the-feature]].

### 2.4 The selftest — 16 bites → 22, all green

```
$ python3 knowledge/_release/_gate_pack_docs.py --selftest ; echo $?
… [OK] arm 5 CLEARS on one consistent Gumdrop spelling across two documents
  [OK] arm 5 does NOT grade the carried cut against the SPIDER version (v0.4.2 inside a v9.9.9 pack
       is green — it invents no ruling)
  [OK] arm 5 FIRES when two shipped documents name different Gumdrop cuts (#224)
  [OK] arm 5 names BOTH cuts in the finding, so neither is presumed right
  [OK] arm 5 sees a hyphen-spelled literal too (the dash is not a hiding place)
  [OK] arm 5 reports UNRUN rather than green when no Gumdrop literal is in scope
pack-docs selftest OK — 5 arms, each driven to BOTH verdicts.
0
```

⚠ **One of those six failed first, and the failure was mine, not the arm's.** The
`arm 5 FIRES` bite asserted `{"0.4.2": 2, "0.4.1": 1}` / 3 findings; the real counts are
`{"0.4.2": 1, "0.4.1": 1}` / 2. The selftest **caught my own arithmetic** before the report did —
which is the only evidence that these bites assert against measured state rather than restating the
code. Corrected at `:397-398`; recorded here rather than quietly fixed.

The bite at `:391-393` is the important one: it is the **fence in test form**. A pack whose Spider
version is `9.9.9` carrying `Memento — Gumdrop v0.4.2` is **GREEN**. If a future seat ever wires
arm 5 to `pack_version`, that bite goes red and names why.

---

## 3. THE THREE SHIPPED LITERALS — found, quoted, and their scope stated

**In the shipped v1.0.2 tree** (the gate's `--stage` input):

| # | file:line | literal | in arm 5's scope? |
|---|---|---|---|
| 1 | `_to_delete/Apollo-Spider-v1.0.2/memento-package/runbooks/_RUNBOOK-context-gauge.md:3` | `*Memento — Gumdrop v1.0.0, for VS Code + GitHub Copilot.*` | ✅ **YES — now graded** |
| 2 | `_to_delete/Apollo-Spider-v1.0.2/memento-package/runbooks/_RUNBOOK-capture-ritual.md:3` | `*Memento — Gumdrop v1.0.0, for VS Code + GitHub Copilot.*` | ✅ **YES — now graded** |
| 3 | `_to_delete/Apollo-Spider-v1.0.2/memento-package/_state.json:17` | `"built_by": "Memento — Gumdrop v1.0.0 (empty starter store)",` | ⛔ **NO — `.json`, outside the gate's `.md` document glob** |

**Their repo sources**, unmoved:

```
apollo-spider/gumdrop/runbooks/_RUNBOOK-context-gauge.md:3:*Memento — Gumdrop v1.0.0, for VS Code + GitHub Copilot.*
apollo-spider/gumdrop/runbooks/_RUNBOOK-capture-ritual.md:3:*Memento — Gumdrop v1.0.0, for VS Code + GitHub Copilot.*
apollo-spider/gumdrop/_state.json:17:    "built_by": "Memento — Gumdrop v1.0.0 (empty starter store)",
```

**Two of three are in scope; the third is declared, not silently missed.** The brief said *rule only
as wide as the gate's glob, do not widen the glob* — so `_state.json` stays out, and the docstring
says so where the next reader will hit it (`_gate_pack_docs.py:56-58`):

> One literal lives in `memento-package/_state.json` (`built_by`), which is JSON and NOT in this
> gate's `.md` document scope — declared here so its absence from the sweep is a stated boundary and
> not a silent one. Widening the glob is a separate call, and Dave's.

### 3.1 ★ The other side of the disagreement is GENERATED, not typed

The v1.0.0 pair are hand-typed in the pack source. **The `v1.0.2` pair in `README.md` are not** —
they are written at bake time from the manifest, `apollo-spider/build-designer-pack.sh:185-186`:

```sh
  MEM_NAME="$(python3 -c '…json.load(open(sys.argv[1]))["carries"]["name"]' "$MANIFEST")"
  MEM_VERSION="$(python3 -c '…json.load(open(sys.argv[1]))["carries"]["version"]' "$MANIFEST")"
```

emitted at `:237` as ``| carries | \`$MEM_NAME $MEM_VERSION\` |``. So one side of this disagreement
**moves at every cut and the other never does** — which is exactly why v1.0.2 and v1.0.3 both show
`+4` and not a shrinking number. The #220 comment above that code (`:179-184`) already names the
class it fixed *for the README*; the runbook headers are the same defect in the files that fix did
not reach. **This is a recurrence generator, not a one-off** — and it is now gated, which is the
[[gate-dont-patch]] shape Dave asked for at #215.

---

## 4. THE CONSUMER — named, and one half of it is missing

*An instrument without a consumer cannot fail* [[instrument-without-a-consumer]]. Measured:

| entry point | consumer | evidence |
|---|---|---|
| `--stage` (arm 5 runs here) | ✅ **`apollo-spider/build-designer-pack.sh:351`** | `python3 "$ROOT/knowledge/_release/_gate_pack_docs.py" --stage "$STAGE"` — between `--stage` and `--zip`, under `set -e`, deliberately **without** `\|\| true` (`:345-348`) so an rc=2 refusal still stops the bake |
| `--selftest` (the 22 bites) | ⛔ **NONE** | `grep -n "pack_docs" knowledge/_build_all.py` → **no match**; `grep -rn "pack_docs" .github/` → **no match** |

So **arm 5 will run at the next bake and print its verdict into the bake log**, but the bites that
prove arm 5 works run **only by hand**. That is the same class `_build_all.py:82-88` and `:122`
call out in their own comments — *"a selftest not in STEPS is a gate that does not run"* — for
`_validate_assertions.py` and `_roll_state.py`, both of which were wired for exactly that reason.
`_gate_pack_docs.py --selftest` has never been wired.

⛔ **I did not wire it.** `knowledge/_build_all.py` is outside my write fence. It is ruling-shaped
question 3 below.

---

## 5. CONSEQUENCES AND PITFALLS *(Dave #165)*

1. **⚠ THE NEXT BAKE WILL PRINT A NEW RED SECTION.** Any v1.0.3 bake from here shows
   `=== GUMDROP — 4 finding(s) ===` and a total of **220 where the last recorded figure was 216**.
   Exit code is still 0 and the bake is **not** blocked — but anyone comparing bake logs to the #222
   / #223 baselines will see a moved number. **The baseline for `_gate_pack_docs.py --stage` is now
   216 → 220 (v1.0.3) and 219 → 223 (v1.0.2), and the +4 is this arm, by design.** Three prior
   sub-reports quote "45 findings" and one quotes 219 as *the* baseline; those figures are now stale
   by construction, not by drift. If the conductor cites a pack-docs total anywhere, cite it with
   the gate version [[premise-ages-faster-than-rule]].
2. **⛔ THE GUMDROP VERSION STORY IS STILL UNRULED, AND THIS ARM DOES NOT SETTLE IT.** The gate now
   *sees* the disagreement and *refuses to resolve it*. Reading the red as "the runbooks are wrong"
   would be reading a ruling into an instrument built specifically not to make one. Ruling-shaped
   question 1.
3. **The red will not clear on its own, and it recurs at every bump.** §3.1: the README side is
   generated, the runbook side is typed. Every future cut moves one and not the other, so this is a
   permanent advisory red until the story is ruled. That is the honest state — but a permanent red
   is also how a gate becomes wallpaper. **If it is still red at the cut after next, treat that as
   the signal to rule it, not to raise the cap.**
4. **Anchoring on `Memento` is a deliberate blind spot.** A future doc writing `Gumdrop v1.0.4`
   without the `Memento` prefix escapes the sweep. Measured as costing nothing *today* (§1.1) — that
   measurement expires the moment someone writes a new heading. The probe to re-run is in
   REPLAY-THESE.
5. **The dash class is tolerated, not normalised.** `Memento - Gumdrop v1.0.0` (hyphen) is caught,
   and a bite proves it. But the arm reports the literal **as written**, so a hyphen and an em dash
   at the same version collapse into one version key and read as consistent. That is correct for a
   *version* sweep and wrong for a *spelling* sweep — arm 5 is the former. Do not read a green arm 5
   as "the product name is spelled consistently."
6. **A pack with no Gumdrop literal at all reports UNRUN, not green.** If a future pack stops naming
   its carried cut in prose, arm 5 says so out loud rather than passing quietly. Do not read
   `arm 5 … is UNRUN` as a pass.
7. **The selftest is still hand-run only (§4).** Until it is wired, a future edit can silently break
   arm 5 and no CI job will notice — the `--stage` consumer would keep printing whatever the broken
   arm computed. This is the live half of [[instrument-without-a-consumer]] on this file.
8. **`--strict` is not new evidence here.** It returned 1 before my change too, on 219 unrelated
   findings. Anyone wanting proof arm 5 can *itself* drive a red should read §2.3, not the strict rc.

---

## 6. RULING-SHAPED — handed back, not decided

1. **⛔ THE GUMDROP VERSION STORY.** Unchanged and unruled: do the two runbook headers move to the
   carried cut, does the README stop naming a version, or do they stay as they are with a permanent
   advisory red? #223 §1.4 handed this back once already and #224 handed it back again. The gate
   now makes it visible at every bake, which was the whole of Dave's word for this lane — **and
   makes it louder every cut.** ⚠ Note the third option is real: leaving it is the status quo
   already released twice (v1.0.1 and v1.0.2 both shipped the disagreement).
2. **Should arm 5's scope widen past `.md`?** `memento-package/_state.json:17` carries the third
   literal and is invisible by construction. Widening the glob is [[gate-glob-scope-rule]] territory
   and was explicitly fenced out of this task. ⚠ It is also not free: `_state.json`'s field is
   `built_by`, which #223 §1.4 could not settle as a live self-claim vs a provenance record — so
   grading it may be grading a history note.
3. **Should `_gate_pack_docs.py --selftest` enter `_build_all.STEPS`?** (§4.) Precedent says yes —
   `_roll_state.py` and `_validate_assertions.py` were wired for exactly this. It is a write to
   `knowledge/_build_all.py`, outside my fence, and it would add a step to the repo's gate run.
4. **Promotion to blocking** stays Dave's word (#221 fence 2). Nothing in this change moves it, and
   arm 5 deliberately gives no new argument for it while the story at (1) is open.

---

## 7. UNPROVEN

1. **The bake wiring was READ, not RUN.** I drove the gate on the staged trees two bakes produced —
   the same input `build-designer-pack.sh:351` hands it — but I did not execute a bake, so the claim
   "the next bake prints this" rests on reading `:351`, not on a bake log. Cheap to close: cut a
   dry-run and grep the log (REPLAY-THESE).
2. **No repo-wide gate run.** `_build_all.py` does not reference this file (§4), so I did not run it
   and make **no claim** about repo-wide greenness after this edit. `py_compile`, `--help` (rc 0),
   the no-args refusal (rc 2) and `_validate_help_gate.py --selftest` (5 bites, OK) are the only
   fleet-level checks driven.

---

## REPLAY-THESE

```bash
cd /path/to/UX-design

# 1. the bites — 22, five arms, both directions each
python3 knowledge/_release/_gate_pack_docs.py --selftest ; echo "rc=$?"     # OK, rc=0

# 2. IT BITES on the real shipped pack (was silent at HEAD)
python3 knowledge/_release/_gate_pack_docs.py --stage _to_delete/Apollo-Spider-v1.0.2 \
  | grep -E "carried cut|=== GUMDROP|finding\(s\)\."                        # 4 gumdrop, 223 total

# 3. before/after, MEASURED — run the HEAD gate beside the new one
mkdir -p _to_delete/_225-base
git show HEAD:knowledge/_release/_gate_pack_docs.py > _to_delete/_225-base/g.py
cp knowledge/_helpgate.py _to_delete/_225-base/          # the help-gate shim walks up for this
for S in _to_delete/Apollo-Spider-v1.0.2 _to_delete/bake225/Apollo-Spider-v1.0.3; do
  echo "$S"
  python3 _to_delete/_225-base/g.py --stage "$S" | grep -oE "^[0-9]+ finding"   # 219 / 216
  python3 knowledge/_release/_gate_pack_docs.py --stage "$S" | grep -oE "^[0-9]+ finding"  # 223 / 220
done
rm -rf _to_delete/_225-base

# 4. THE GREEN IS REAL + the single-variable mutation (§2.2, §2.3) — on a COPY, never the shipped tree
cp -a _to_delete/Apollo-Spider-v1.0.2 _to_delete/_225-probe
sed -i 's/Memento — Gumdrop v1\.0\.0/Memento — Gumdrop v1.0.2/' \
  _to_delete/_225-probe/memento-package/runbooks/_RUNBOOK-{context-gauge,capture-ritual}.md
python3 knowledge/_release/_gate_pack_docs.py --stage _to_delete/_225-probe \
  | grep -E "carried cut|finding\(s\)\."                    # "internally consistent", 219 = baseline
sed -i '3s/v1\.0\.2/v1.0.1/' _to_delete/_225-probe/memento-package/runbooks/_RUNBOOK-capture-ritual.md
python3 knowledge/_release/_gate_pack_docs.py --stage _to_delete/_225-probe \
  | grep -E "carried cut|=== GUMDROP|finding\(s\)\."        # THEY DISAGREE, 4 gumdrop, 223
rm -rf _to_delete/_225-probe

# 5. the three literals, and the one that is out of scope by design
grep -rn "Memento — Gumdrop v" _to_delete/Apollo-Spider-v1.0.2/ | sort
grep -rn "Memento — Gumdrop v" apollo-spider/gumdrop/                      # the repo sources

# 6. PITFALL 4's expiring measurement — does the "Memento" anchor still cost nothing?
grep -rn "Gumdrop v" --include=*.md _to_delete/Apollo-Spider-v1.0.2/ | grep -v "Memento — Gumdrop v"
#   ⛔ ANY output here means the anchor now has a blind spot and arm 5's regex needs re-pricing.

# 7. the consumer, both halves
grep -n "_gate_pack_docs" apollo-spider/build-designer-pack.sh    # :351 — the --stage consumer
grep -n  "pack_docs" knowledge/_build_all.py                      # NO MATCH — the selftest has none
grep -rn "pack_docs" .github/                                     # NO MATCH — not in CI

# 8. fleet-level checks driven (UNPROVEN 2 names what was NOT)
python3 -m py_compile knowledge/_release/_gate_pack_docs.py
python3 knowledge/_release/_gate_pack_docs.py --help >/dev/null; echo "help rc=$?"    # 0
python3 knowledge/_release/_gate_pack_docs.py       >/dev/null 2>&1; echo "bare rc=$?" # 2, refuses
python3 knowledge/_validate_help_gate.py --selftest | tail -1
```

---

## FENCES HONOURED

- **Written:** `knowledge/_release/_gate_pack_docs.py` and this report. `git status --porcelain`
  shows `M knowledge/_release/_gate_pack_docs.py` and nothing else.
- **Not touched:** `_rulings.json`, `_state.json`, `_CHAIN.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md`,
  any manifest/ledger/RATIFY surface, `_build_all.py`, `.github/workflows/gates.yml`,
  `build-designer-pack.sh`, and **every one of the three Gumdrop literals** — in the repo source and
  in both staged trees. The gate widened; the strings did not move.
- **No commit, no `git add`, no push.** No new ruling, no promotion, no constant/band/roster change.
  The gate roster fence bite (`:445`) still passes: this file stays out of the ruled 55.
- **Scratch** lived in `_to_delete/` (gitignored, on the mount) and was removed; `/tmp` and
  `/var/tmp` untouched.
