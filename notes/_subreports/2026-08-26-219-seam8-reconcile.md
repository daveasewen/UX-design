# #219 seam 8 — THE SPIDER FLIP, and the reconcile of N1 + N2 + the conductor's inscriptions

**Seam:** 8 (stage 1) · **Model:** Opus · **Date:** 2026-08-26 · **Base:** `9ebd94c`
**Charter:** `s219-D8` (read verbatim), with `s219-D5` and the superseded `s219-D7` read as
history. Lane reports read FIRST and in full: `notes/_subreports/2026-08-26-219-N1-snoopy-rename.md`
and `notes/_subreports/2026-08-26-219-N2-four-reds.md`.

COUNTS: git status lines reconciled **40** (N1 24 · N2 9 · conductor 1 · seam 8 6 · UNCLAIMED
**0**; 9 lines are shared, attributed by hunk) · manifest at the synthetic commit **1,592 files**,
33,851,515 bytes · flip proof **0** snoopy references outside frozen/filed history (§ ②) ·
selftest bites re-driven **124 + 14 + 10 + 8 + 57 + 140-step routing + 214 scripts** · new bites
added **6** · mutations driven **2**, each RED by a named bite, control green either side · store
rows repointed **9** · store rows minted **1** · defects found and fixed at cause **1** (§ ⑤)

⛔ **NOTHING COMMITTED, NOTHING PUSHED.** The release audit is **designed-RED** and clears at
stage 2 — § ⑧.

---

## ① THE FLIP — `Apollo — Spider v1.0.0`, carrying `Memento — Gumdrop v1.0.0`

`s219-D8` superseded `s219-D7` **before any commit carried Snoopy**, so this is not a second
rename on top of a first. It is the SAME rename, re-aimed: the tree records
`designer-skills-v3` → `apollo-spider`, once.

**N1's § ① decision #3 is what made this cheap, and it is worth recording that the bill it
predicted arrived within hours.** Because the generator and its two artefacts took generic names
(`_gen_pack_manifest.py`, `_pack_manifest.json`, `_pack_gate_probe.json`) and the identity lives
in `PACK_NAME` / `PACK_SLUG` / `VERSION` as DATA, the second flip touched **no filename in
`knowledge/_release/`** and no ledger mechanism. A Snoopy-named generator would have been renamed
twice in one day.

| surface | now |
|---|---|
| directory | `apollo-spider/` (git rename detection: `designer-skills-v3/… -> apollo-spider/…`, no snoopy hop in the record) |
| zip / pack root | `Apollo-Spider-v1.0.0.zip`, flat root `Apollo-Spider-v1.0.0/` |
| page | `reviews/RELEASE-SPIDER-2026-08-26-v1{,.REVIEW}.html` |
| constants | `PACK_NAME = "Apollo — Spider"` · `PACK_SLUG = "Apollo-Spider"` · `PACK_SURFACE_PREFIX = "apollo-spider/"` |
| pack stamps ×3 | `README.md` · `PROVENANCE.json` · `_MANIFEST.json` all read **Apollo — Spider v1.0.0, carrying Memento — Gumdrop v1.0.0** (measured in the real bake, § ⑥) |
| ruling citation | `s219-D8 (naming) · s219-D5 (the five cards) · s219-D4 (the cut)` — in the manifest, PROVENANCE and the README table |
| ledger row | `apollo-spider`, `v1.0.0`, `renamed_from: "designer-skills-v3"` |
| gates.yml correction log | fifth entry amended in place (§ ④) |

### The naming GRAMMAR moved too, and the prose says so

`s219-D7` gave two families by module TYPE. `s219-D8` keeps that and adds the **STRICT MISSION
PAIR**: a release takes one mission's LM *and* CM. Spider and Gumdrop are both Apollo 9. That
sentence is now in three reader-facing places — the generator's IDENTITY comment, the pack
README, and Dave's page's naming note — and nowhere else, because it is one live fact.
⚠ The future missions' names are deliberately **not** copied into the machinery: they live in the
ruling. A pointer should not carry a copy of the value it points at, which is N1's own finding 1
applied one turn later.

### The ledger bridge — the lineage is CLEAN, verified rather than assumed

The brief asked that a transient id which never landed must not pollute the ledger. **It does
not.** `--seed --at 71bb2f7` re-measured the row (never hand-typed), and the diff **against
HEAD** is one rename:

```
-  "id": "designer-skills-v3",          +  "id": "apollo-spider",
-  "version": "v3.0.0"                  +  "version": "v1.0.0"
-  "designer-skills-v3/dist/"           +  "apollo-spider/dist/"
                                        +  "renamed_from": "designer-skills-v3"
```

v1's and v2's rows are **byte-identical** and `baseline_commit` does not move on any row. The
laundering arm matches by id against the PARENT commit's ledger — the parent is HEAD, whose row
id is `designer-skills-v3`, which is exactly what `renamed_from` names. Driven:
`--check` → **PASS — 3 arm(s) asked, no frozen surface moved**, and the 14-bite selftest
(including N1's three rename arms) is green.

---

## ② THE GREP PROOF — 0 snoopy references outside frozen and filed history

```
grep -rniIc "snoopy"  (whole tree, excluding .git and __pycache__)
```

Every surviving hit, with its category:

| where | n | category |
|---|---|---|
| `knowledge/_rulings.json` | 4 | **FROZEN HISTORY** — `s219-D7` verbatim and `s219-D8`'s supersession clause. Rewriting a ruling to match a later rename is what ADR-0017 and [[header-wins-over-audit]] forbid. |
| `notes/_subreports/2026-08-26-219-N1-snoopy-rename.md` | 28 | **FILED HISTORY** — N1's report, body untouched. A dated one-line correction is APPENDED at the end (§ ③). |
| `notes/_subreports/2026-08-26-219-N2-four-reds.md` | 8 | **FILED HISTORY** — N2's report, untouched. |
| `knowledge/_state.json` | 5 | `W-192`'s `home`/`links[0]`/`title` and `W-193`'s two links — all naming the FILED N1 report by its real filename. A pointer to filed history is correct, not stale. |
| `_CHAIN.md` | 1 | GENERATED from `W-192`'s title, above. |
| this report | 14 | **FILED HISTORY** — it is the record of the flip and has to name what flipped. |
| `_to_delete/_219-entry-inputs/*.json` | 4 | **GITIGNORED** conductor scratch holding the D7/D8 ruling-entry JSON verbatim. Untracked, never shipped — the same category as `_rulings.json`. |

**And zero in everything that matters**, run as its own probe rather than inferred from the
totals — `apollo-spider/` · `knowledge/_release/` · `knowledge/canon/` · `knowledge/_build_all.py`
· `knowledge/_helpgate.py` · `.github/` · `.gitignore` · `reviews/`:

```
grep -rniIl "snoopy" <those eight>   ->   ZERO
```

⚠ **Two of my own first-cut edits broke this proof and were caught by running it, not by
intending it.** The amended gates.yml entry originally named "Apollo — Snoopy" as the superseded
name, and the generator's IDENTITY comment spelled out Apollo 10's pair — both honest, both a
stale-name hit. Both were reworded to point at the ruling instead of copying it. Recording it
because "it is only history" is exactly how a dead name survives a rename wave.

**Stale `designer-skills-v3` references in hand-maintained files: 0.** The remaining hits are
`_gate_frozen_release.py` ×4 and `_frozen-releases.json` ×2 (the DECLARED rename bridge — deleting
them is the defect), gates.yml ×2 (the correction log naming what was renamed), `_rulings.json` and
the filed reports, and the two generated artefacts that are **stale by design** (§ ⑧).

---

## ③ N1's REPORT — appended, never rewritten

A dated correction note is appended at the END of `2026-08-26-219-N1-snoopy-rename.md`, stating
the flip, the ruling, the clean single-rename lineage, and that the body stands as this lane's
filed record. **Nothing in its body was edited.** Its § ① decision #3 is explicitly credited —
it is the reason the flip was cheap.

---

## ④ THE gates.yml CORRECTION LOG — amended in place, and why that is legal

The fifth entry is UNCOMMITTED. History freezes at COMMIT, not at keystroke, so an entry that no
commit carries is still a draft. It now reads `#219 N1 + seam 8, s219-D8`, names Spider and
Gumdrop, states the mission-pair grammar, and says in one sentence that D6 and D7 were both
superseded before any commit carried them **so the log records ONE rename, not a chain of three**
— with a pointer to `_rulings.json` for the names. Driven: `gates.yml` parses as YAML, 3 jobs,
the `release` job intact at **12 steps**, step names now reading *"any baked Spider zip"*,
*"Pack ship-list audit"*, *"Pack ship-list drift"*.

---

## ⑤ ⛔ THE DEFECT THIS SEAM FOUND — the pack gate refused IMPORTERS, and two shipped gates went RED

**Found by doing the one thing the brief asked for that neither lane had done: running the
pack's own runner, end to end, inside a REAL bake.**

First run of `ci-template/run-gates.py` from a foreign cwd against the baked pack:

```
33 pass · 2 FAIL · 0 could-not-ask            RUNNER EXIT=1
  FAIL (2)   _gate_minted_consumption.py
  FAIL (2)   _validate_state_snap.py
```

Both were exiting **2** with N1's own refusal text:

```
✖ REFUSED (pack-gate): gen_theme_cascade.py MINTS the theme cascade, and you are inside a
  shipped Apollo pack (/var/tmp/s8/bake1/Apollo-Spider-v1.0.0).
```

**The cause is one missing argument, and it is a sharper shape than "a bug".** `pack_gate` in
`knowledge/_helpgate.py` HAS the correct guard —

```python
def pack_gate(file=None, flag=PACK_FLAG, name="__main__", what=None):
    if name != "__main__":
        return None
```

— but it **defaults** to `"__main__"`, and **none of the four call sites passed `__name__`**:

```python
from _helpgate import pack_gate as _pack_gate; _pack_gate(__file__, what='the theme cascade')
```

So the guard had its value without its meaning. The sibling `help_gate` call one line above
passes `__name__` correctly, which is what makes the omission invisible on the page. Both gates
`import gen_theme_cascade` for its single definition of effective values — they are not minting
anything — and the module-level refusal `sys.exit(2)`'d them before their first line ran.

**Why neither lane's proof could see it, and the general shape:**

- **N1 drove the generators as SCRIPTS** and proved `pack_root()` is `None` in the repo. Both
  true, both about the `__main__` path. Their own UNPROVEN 3 named the gap exactly: *"The
  pack-side runner was not re-driven from inside this pack."*
- **N2's stage had no marker.** Their stage was copied from manifest paths and carried no
  `_MANIFEST.json` at its root, so `pack_root()` returned `None` and the guard never fired there
  at all — their `34 pass · 1 FAIL · 1 could-not-ask` could not have caught it.
- ⇒ [[instrument-without-a-consumer]], inverted: the fence was crossed only in a direction nobody
  tried. And [[mutation-tests-the-clause-not-the-feature]] — the existing bite asserted the CALL
  was WIRED; the clause is the ARGUMENT.

**Fixed at cause** — `name=__name__` at all four call sites. Not a carve-out in the two gates,
not an exception in the runner: the guard is for someone RUNNING a generator, and it now says so
in code as well as in its own docstring.

**Three new arms, both directions, and they are DRIVEN, not read:**

| bite | what it drives |
|---|---|
| `packguard/guard-is-argued:<gen>` ×4 | source arm — `name=__name__` present in each of the four generators |
| `packguard/import-is-a-no-op` | **behaviour arm** — a fake shipped GATE that `import`s a fake canon generator, inside a fake pack with a real marker, must exit 0 and print `GATE RAN 42` |
| `packguard/import-does-not-mint` | importing must not run the generator's own work either |

The selftest's fake generator was reshaped to match a real one — shared definitions at module
level, the WORK under `if __name__ == "__main__"` — which is what makes the import arm a real
question instead of a trivially true one. (Its first cut went RED for that reason, correctly.)

**MUTATION-PROVEN in both halves, control green either side:**

```
mutant A: name=__name__ removed from gen_theme_cascade.py
  -> RED [packguard/guard-is-argued:gen_theme_cascade.py]           124 bites, 1 fail
mutant B: name=__name__ removed from the DRIVEN fake generator
  -> RED [packguard/import-is-a-no-op] got (2, False), wanted (0, True)
restored, byte-identical to backup both times · 124 bites, 0 fail
```

**Repo behaviour unchanged, measured not asserted:** `_validate_state_snap.py` → *"OK — 7
opacity-state check(s) snapped to their theme ramps"*, `_gate_minted_consumption.py` → its
ADVISORY line, `gen_canon_components --check` → *135 components in sync*,
`gen_theme_cascade --check` → *230 override path(s), 387 component projection(s) in sync*, and
`knowledge/canon/canon.css` **byte-identical** either side of the fix.

---

## ⑥ THE CARRY-THROUGH AND THE BAKE — driven end to end at a synthetic commit

Two synthetic commits were built with `GIT_INDEX_FILE` (real index and HEAD untouched, verified
after; both are dangling objects, never pushed, nothing on disk names them):

| | |
|---|---|
| `f528fef109eb` | HEAD + the whole working tree, before the § ⑤ fix — used to measure the four reds clearing |
| `362121c69fad` | HEAD + the whole working tree **including** the § ⑤ fix — the stage everything below is measured at |

Unlike N1's, these include **N2's files**, which is the point: N2's `--check` arm must be IN the
commit for the declared invocation to survive the probe.

### THE FOUR REDS CLEAR — measured, by differencing two probes

Probe at `f528fef109eb` vs the probe on disk (R1's at `801fe7c`). **Exactly four gates moved, and
they are exactly the four:**

| gate | was | now |
|---|---|---|
| `_validate_token_forks.py` | RUNNABLE, *FAIL in the pack AND in the full repo* | **RUNNABLE, ran clean, verdict PASS** |
| `_validate_type_blast_radius.py` | RUNNABLE, *FAIL …* | **RUNNABLE, ran clean, verdict PASS** |
| `_validate_type_composites.py` | RUNNABLE, *FAIL …*, invocation `()` | **RUNNABLE, ran clean, verdict PASS**, invocation `--check` |
| `_validate_evidence.py` | RUNNABLE, *FAIL …* | **REPO-BOUND** — *"runs, but its verdict is about notes/_claims, which the pack does not ship"* |

Nothing else moved. Totals `36 RUNNABLE · 3 NEEDS-DEP · 8 REPO-BOUND` → `35 · 3 · 9`.

### N2's HANDOFF 1 — the carry-through works, probe → manifest → runner

The declared invocation is **kept, not disowned**, now that N2's `--check` arm is in the commit —
the trap N1 built `flag_rejected()` for is not sprung, and the fallback is not taken:

```
probe    : _validate_type_composites.py | invocation='--check' | verdict RUNNABLE
manifest : gates group carries the invocation
runner   : Apollo gates — 35 to run, from _MANIFEST.json
             _validate_type_composites.py  --check          <- --list, from a foreign cwd
```

**The run, from `/var/tmp/s8/proj2` — a directory that is not this repo:**

```
Apollo gates — 35 to run, from _MANIFEST.json
35 pass · 0 FAIL · 0 could-not-ask                       RUNNER EXIT=0
```

⚠ **This diverges from the briefed target `35 pass · 0 FAIL · 1 COULD-NOT-ASK` in ONE respect,
and the reason is a real change to what the pack ships — it is § ⑨ Q1.** N2's fix reclassified
`_validate_evidence.py` to REPO-BOUND, so the probe drops it **and its helper
`knowledge/_claimtable.py`** from the ship list. The pack now ships **55 gates, not 57**, and 35
runnable, not 36. The honest refusal did not disappear — it **moved from runtime to the ship
list**. Zero reds either way, exit 0 either way.

### THE DOUBLE DRY-RUN BAKE at `362121c69fad`

| proof | result |
|---|---|
| bake ×2, two out-dirs, through the REAL `build-designer-pack.sh` | **identical sha256 `743f00d433cdc699b32193232dd3af3d350fdde4ae6882f4ff556082700e9b80`**, 13M, `cmp` byte-identical |
| manifest | **1,592 files**, 33,851,515 bytes, sha256 `80eefc7b6a62b580` |
| ship-list delta vs the on-disk manifest | **−8 old-prefix, +8 new-prefix** (the rename, exactly), **−2** = `_validate_evidence.py` + `_claimtable.py` (above) |
| zip layout | 1,595 entries, **one root** `Apollo-Spider-v1.0.0/`, holding `skills/` · `ci-template/` · `knowledge/` · `showroom/` · `memento-package/` · `_MANIFEST.json` · `PROVENANCE.json` · `README.md` |
| stale path components in the zip | **0** snoopy, **0** `designer-skills-v3` |
| stale CONTENT anywhere inside the staged pack | **0** files match `snoopy\|Snoopy\|designer-skills-v3` |
| fonts | **54** in the manifest group, **54** in the zip |
| three stamps | README title + provenance table, `PROVENANCE.json`, `_MANIFEST.json` — all `Apollo — Spider` / `v1.0.0` / `Memento — Gumdrop v1.0.0` / `s219-D8` |
| `--check` on the baked zip | ✅ **CHECK GREEN — matches the manifest at `362121c69fad`** |
| pack-gate refusal, all four generators run as scripts | rc **2**, `✖ REFUSED (pack-gate)`, carrying Dave's framing verbatim (*"canon that never passed a gate"*, whitespace-flattened — the message wraps) and naming `--i-understand`; **minted nothing** |
| `--i-understand` proceeds | `gen_canon_tokens.py --i-understand` → `TOTAL: 577 root vars, 195 dark overrides / Wrote …`, rc **0** |

---

## ⑦ THE RECONCILE — every one of the 39 lines attributed

**UNCLAIMED: 0.**

### N1 (24 lines)

```
 M .github/workflows/gates.yml            (+ seam 8: the fifth entry amended, § ④)
 M .gitignore
 M knowledge/_build_all.py
 M knowledge/_helpgate.py                 (the pack_gate leg; see § ⑤ — the FIX is in its callers)
 M knowledge/_release/_frozen-releases.json          (+ seam 8: re-seeded to apollo-spider)
 M knowledge/_release/_gate_ci_template.py
 M knowledge/_release/_gate_frozen_release.py
 M knowledge/_release/_gate_release_audit.py
RM knowledge/_release/_gen_v3_manifest.py -> _gen_pack_manifest.py   (+ seam 8: flip + 6 bites)
R  knowledge/_release/_v3_gate_probe.json -> _pack_gate_probe.json   (⚠ STALE BY DESIGN)
R  knowledge/_release/_v3_manifest.json   -> _pack_manifest.json     (⚠ STALE BY DESIGN)
RM designer-skills-v3/build-designer-pack.sh -> apollo-spider/build-designer-pack.sh
R  designer-skills-v3/ci-template/{README.md,gates.yml} -> apollo-spider/ci-template/…
RM designer-skills-v3/ci-template/run-gates.py        -> apollo-spider/… (N2's W-189, taken by N1)
R  designer-skills-v3/skills/*/SKILL.md (5)           -> apollo-spider/skills/…
R  reviews/RELEASE-V3-MANIFEST-2026-08-26-v1{,.REVIEW}.html -> reviews/RELEASE-SPIDER-… (⚠ STALE INSIDE)
 M knowledge/canon/gen_canon_{tokens,components,bento}.py, gen_theme_cascade.py
                                          (N1's +4 lines each; + seam 8's one-argument fix, § ⑤)
?? notes/_subreports/2026-08-26-219-N1-snoopy-rename.md   (+ seam 8: correction appended, § ③)
```

### N2 (9 lines)

```
 M knowledge/_validate_evidence.py · _validate_token_forks.py · _validate_type_composites.py
 M knowledge/snippets/Navigations.reference.html
 M knowledge/_COMPOSE-AUDIT.md · knowledge/_TYPE-BLAST-GATE.md   (generated gate reports)
 M knowledge/canon/canon.css                                     (see the cross-lane note below)
?? notes/_subreports/2026-08-26-219-N2-four-reds.md
?? notes/_subreports/assets/2026-08-26-219-N2-navigations-searchbar.png
```

**The `canon.css` cross-lane flag is RESOLVED, and the resolution is measured.** N1 declared the
file as *N2's content, materialised by N1's run*. Verified by driving the whole canon chain rather
than by reading the diff: `gen_canon_tokens.py` re-run over the current source produces a file
**byte-identical** (`md5 c128269351f1966efb02077e0f16cad6`, `cmp` clean) to the one in the tree,
and `gen_canon_components --check` (135 in sync) and `gen_theme_cascade --check` (230 / 387 in
sync) are both green. ⇒ **The tree's `canon.css` IS what the current source produces.** Attribute
the line to N2; their own regen is a no-op over it. *(N1's finding 3 stands and is unaddressed
here: `gen_canon_tokens.py` still has no `--check` arm and silently WRITES when given one. Not
this seam's file, still priced ~15 lines.)*

### Conductor (1 line)

```
 M knowledge/_rulings.json
```

**Verified INSERTIONS-ONLY and included in the stage.** `git diff --numstat` → **62 insertions,
0 deletions**; 0 removed lines by direct probe; ruling count 254 → 258; the shared 254-ruling
prefix is byte-order-identical. ⚠ **FOUR ids entered, not the three the brief named:**
`s219-D5`, `s219-D6`, `s219-D7`, `s219-D8`. D5 was already readable by N1 and N2 at lane open, so
it too was inscribed uncommitted in this wave. Named so the conductor can confirm it is theirs.
**No conductor telemetry appears as a tracked path** — `GOOD-MORNING.md` and `_LIVE-STATE.md` are
unmodified, and nothing else in the tree is telemetry-shaped.

### Seam 8's own six (the rest are shared lines, attributed by hunk above)

```
 M _CHAIN.md                                              (regenerated, FRESH)
 M knowledge/_state.json                                  (9 rows repointed, 1 minted)
?? notes/_subreports/2026-08-26-219-seam8-reconcile.md    (this report)
```

plus, by hunk, inside N1's lines: `gates.yml` (the correction log, § ④) ·
`_gen_pack_manifest.py` (the flip + 6 bites) · `_frozen-releases.json` (the re-seed) · the four
canon generators (`name=__name__`, § ⑤) · N1's report (the appended note, § ③).

---

## ⑧ ⛔ REPLAY-THESE (conductor) — READ BEFORE COMMITTING

- **`_gate_release_audit.py --check` is RED and `--selftest` is 8/1, BY DESIGN, and both are
  BLOCKING** (`_build_all` `[135]`/`[136]` and the CI `release` job). The gate names the drift
  exactly and names nothing else:

  ```
  ❌ THE SHIP LIST ON DISK IS NOT WHAT THE GENERATOR PRODUCES at 801fe7cc2296.
     on disk: 1594 files, sha256 2e8fdd02e4481ba7
     fresh:   1586 files, sha256 912e826ac687e564
     8 path(s) the file ships that a fresh generation does not, first:
       ['designer-skills-v3/ci-template/README.md', … 'designer-skills-v3/skills/check-with-gates/SKILL.md']
  selftest: 8 bites, 1 fail(s)
    RED [manifest/matches-a-fresh-generation] the manifest on disk is NOT what the generator
        produces — that is the gate's own subject and it is red right now
  ```

  Those 8 are the 5 skills + 3 ci-template files at the OLD prefix — the same designed stage-1
  red N1 and seam 7 landed with, for the same reason, and it clears the same way. **Do not push
  before it is cleared.**

- **The three generated artefacts are STALE ON DISK and were deliberately RESTORED to that state
  after the bake.** `_pack_manifest.json`, `_pack_gate_probe.json` and
  `reviews/RELEASE-SPIDER-2026-08-26-v1.html` are back to pure renames of R1's `801fe7c`
  generation (`R`, no `M`, md5s re-verified). N1's reasoning holds and was re-applied: leaving the
  synthetic commit's artefacts on disk would make the audit go green locally **against a dangling
  object** and REFUSE (77) in CI — a gate passing on a commit that will never exist. The
  `.REVIEW.html` was never rewritten by the bake and remains a pure rename.

- **STAGE 2, after the landing commit `<sha>` exists** — expected values now measured, not
  predicted (they are the § ⑥ bake at `362121c69fad`, which is HEAD + this whole working tree):

  ```
  python3 knowledge/_release/_gen_pack_manifest.py --probe    --commit <sha>   # ~45s
  python3 knowledge/_release/_gen_pack_manifest.py --manifest --commit <sha>
  python3 knowledge/_release/_gen_pack_manifest.py --page reviews/RELEASE-SPIDER-2026-08-26-v1.html
  python3 knowledge/_make_review.py …          # the page rewrite strips the review pair's stamps
  python3 knowledge/_release/_gate_release_audit.py --check      # must go GREEN
  python3 knowledge/_release/_gate_release_audit.py --selftest   # must go 8/0
  ```

  **Expect 1,592 paths** (not 1,594 — § ⑥), fonts 54, skills 5, ci-template 3, all under
  `apollo-spider/`; probe `35 RUNNABLE · 3 NEEDS-DEP · 9 REPO-BOUND`; the pack's own runner
  `35 pass · 0 FAIL · 0 could-not-ask`, exit 0. **The fifth card's four gate names should be
  re-read** — `Q5_RED_GATES` is bitten for existence, not for still-being-red, and all four are
  now green or honestly REPO-BOUND.

- **Do not drop `renamed_from` and do not re-seed the whole ledger at HEAD** — that would move
  `baseline_commit` on v1 and v2 and light the laundering arm for both. (N1's warning, still live.)

- **The § ⑤ fix is a change to four canon generators mid-wave.** It is one keyword argument each,
  it is bitten in both directions, and canon.css is byte-identical either side — but the conductor
  should know the canon generators were touched by this seam and not only by N1.

---

## ⑨ RULING-SHAPED QUESTIONS — not decided here

**Q1 — the pack no longer ships the evidence linter, as a side effect of a correct fix. Is that
the intended cut?** `_validate_evidence.py` is now REPO-BOUND at the probe (its verdict is about
`notes/_claims`, which `s219-D4(1)` permanently excludes), so it and `knowledge/_claimtable.py`
fall out of the ship list: **55 gates, not 57**. The classification is honest and the gate could
never have said anything useful in a designer's project. But it is a change to WHAT DAVE'S PAGE
LISTS, arriving as a consequence rather than a decision, and `s219-D4(2)` makes the cut his. Two
readings, neither taken: **(a)** correct as-is — a gate with nothing to measure should not ship;
**(b)** ship it anyway so the pack's gate roster matches the repo's, and let it refuse with 77 in
the designer's run. This is also the same seam as N2's HANDOFF 3 (the runner has three verdicts,
the repo has four) and R2's Q4, and the three should be answered together.

**Q2 — N2's HANDOFF 3 and Q1/Q2 are still open and are not this seam's.** Recorded so they are
not lost in the flip: the pack ratchet's 427 of slack (N2 Q1), `notes/_claims` named in three
places (N2 Q2), the pack runner's missing ADVISORY verdict (N2 HANDOFF 3).

**Q3 — N1's four ruling-shaped questions are unchanged by the flip and still stand**, and its
§ ① decision #3 (generic machinery filenames) has now been *validated by events* rather than
merely argued: the second rename cost zero filename changes in `knowledge/_release/`.

---

## UNPROVEN, declared

1. **No commit and no CI run exists.** Every verdict here was driven in this working tree. R2's
   standing UNPROVEN — neither workflow has ever run on GitHub Actions — is **unchanged**.
2. **The bake was proved at a SYNTHETIC commit** (`362121c69fad` = HEAD + the entire working
   tree). If the conductor commits exactly this tree, the stage-2 numbers are the § ⑥ numbers. If
   anything is held back, the ship list moves.
3. **`_build_all.py` was not run end to end** (sandbox call wall ~178s). Its `--selftest` is green
   over 140 steps and every step this seam touches was driven individually and named above.
4. **The page was not verified for stage-2 content** — it is deliberately stale (§ ⑧). Its Spider
   naming, the mission-pair note and the five answered cards were rendered and read DURING the
   bake and then restored; they are stage 2's deliverable, not stage 1's.
5. **No render probe was taken.** N2's pixel-neutrality proof for the search-bar rename is
   inherited as filed, not re-driven.
6. **The pack-gate warning's WORDING has still not been past Dave** (N1's UNPROVEN 5, unchanged).

---

## Not touched

`GOOD-MORNING.md` · `_LIVE-STATE.md` · any constant, band, advisory, threshold or stop line ·
any Dave-owned row · `knowledge/_rulings.json` beyond INCLUDING the conductor's four inscriptions
in the stage (0 lines removed, verified) · `knowledge/_type_ratchet.json` ·
`knowledge/_TOKEN-FORK-LEDGER.json` · `designer-skills-v1/` · `designer-skills-v2/` ·
`memento-package/` · N1's and N2's report BODIES. No commit, no push, no memory write.
Everything under `/var/tmp/s8/` is a throwaway; both synthetic commits are dangling and unpushed.

## Store rows

One row minted through `_state.add()`: this filed report (`s218-D7`, forgotten-document class
#185). **Nine rows repointed** (path strings in `home`/`links` only — no title, state, owner or
close condition touched, [[home-pointer-rot-class]]): `W-188`, `W-189`, `W-191`, `W-99zt`,
`W-99zu`, `W-99zv`, `W-99zw`, `W-99zy`, `W-99zz`. `W-191`'s title and body additionally carry the
D7→D8 correction, because the row asserted "`s219-D7` enacted" about work that will land under D8
— declared here so the conductor can strike it. `W-192`'s pointers at N1's filed report are left
exactly as they are: they name a real file. `_state.py --check` → **0 UNRESOLVABLE** (was 2),
248 homes resolve by anchor; `--selftest` 57 bites green; `_gate_doc_rows.py` unrowed 0.
