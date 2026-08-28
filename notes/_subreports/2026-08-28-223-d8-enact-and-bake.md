# #223 — s223-D8 ENACTED, AND THE v1.0.2 BAKE

**Sub:** Opus build sub · **Conductor:** Fable, session #223 · **Band:** L (~35K)
**Store row:** `W-259` (minted before filing, per the doc-row gate)
**Date:** 2026-08-28
**Rulings enacted:** `s223-D8` (both legs) · `s223-D7` (the bake word, carried to the fixed sha per D8)

> ⏳ **THIS FILE IS WRITTEN IN TWO PASSES.** §1–§3 (legs A and B) are complete and were true at the
> landing commit. §4–§7 (the release surface, the bake, the final push, CI) are filled in after
> that commit, because the bake cannot run against a dirty tree — see §3.3.

---

## 1. LEG 1 — THE LITERAL SWEEP (`s223-D8` clause 1)

### 1.1 How `FIRST-SESSION.md` is built — read before editing

The brief asked me to prefer *deriving* the directory name over typing a new literal **if the doc
is templated**. It is not. Two measurements:

```bash
$ grep -n "FIRST-SESSION" apollo-spider/build-designer-pack.sh
258:- \`FIRST-SESSION.md\` — **start here.** …          # prose ABOUT it, inside the generated README
292:carries its own exact encoder … \`FIRST-SESSION.md\` § Before you …
```

The build script never writes `FIRST-SESSION.md`. It is staged verbatim, by
`_gen_pack_manifest.py --stage`, out of `git archive` at the cut commit
(`knowledge/_release/_gen_pack_manifest.py:2518` maps
`apollo-spider/FIRST-SESSION.md` → the pack root's `FIRST-SESSION.md`). Only three files in the
pack are *generated* — `README.md`, `PROVENANCE.json`, `_MANIFEST.json` — and those already read
`$VERSION` / the manifest rather than typing it.

So there is no template to hang the name on, and the mechanical enactment is the literal. **No
new mechanism was invented; that would have been a ruling.**

### 1.2 The fix

```diff
--- a/apollo-spider/FIRST-SESSION.md
+++ b/apollo-spider/FIRST-SESSION.md
@@ -51 +51 @@
-`Apollo-Spider-v1.0.1` directory). Copilot reads `.github/copilot-instructions.md` from a
+`Apollo-Spider-v1.0.2` directory). Copilot reads `.github/copilot-instructions.md` from a
```

### 1.3 The sweep — every path the manifest carries, every hit, classified

Driven over all **1,647** paths in `knowledge/_release/_pack_manifest.json` (`groups[].paths`),
every extension, not just `.md`. All 1,647 resolved on disk; none missing. **7 hits.**

| # | hit | classification | action |
|---|---|---|---|
| 1 | `apollo-spider/FIRST-SESSION.md:51` — ``` `Apollo-Spider-v1.0.1` directory) ``` | **LIVE POINTER** — the directory a designer is told to open, inside a pack that unzips to `Apollo-Spider-v1.0.2/` | **FIXED** (§1.2) |
| 2 | `apollo-spider/gumdrop/_state.json:17` — `"built_by": "Memento — Gumdrop v1.0.0 (empty starter store)"` | **OUT OF CLASS** — see §1.4 | left, **declared** |
| 3 | `apollo-spider/gumdrop/runbooks/_RUNBOOK-capture-ritual.md:3` — `*Memento — Gumdrop v1.0.0, for VS Code + GitHub Copilot.*` | **OUT OF CLASS** — §1.4 | left, **declared** |
| 4 | `apollo-spider/gumdrop/runbooks/_RUNBOOK-context-gauge.md:3` — same line | **OUT OF CLASS** — §1.4 | left, **declared** |
| 5 | `knowledge/_validate_wiring.py:98` — `"Its known-answer test DOES fire — driven against the frozen v1.0.0 zip it reports the "` | **HISTORY** — names the frozen v1.0.0 zip, which is exactly what it drives against | left |
| 6 | `memento-package/machinery/_capture_gate.py:117` — `# UNIMPORTABLE — shipping an unimportable machinery file is the v1.0.0 defect this release` | **HISTORY** — prose about a defect v1.0.0 had | left |
| 7 | `memento-package/claude-plugin/memento/machinery/_capture_gate.py:117` — same line, the ported copy | **HISTORY** — same | left |

Two further `v1.0.1` mentions live in `apollo-spider/build-designer-pack.sh:182-183`, which is a
pack *source* but not a *shipped* path — they are the #220 comment explaining the Gumdrop-version
defect. **HISTORY**, left.

### 1.4 ⚠ HANDED BACK, NOT RULED — hits 2, 3 and 4

These three say **`Memento — Gumdrop v1.0.0`** inside a pack whose `PROVENANCE.json` and
`_MANIFEST.json` both say it carries **Gumdrop v1.0.2**. I did **not** touch them, and I did not
classify them HISTORY either. The honest classification is *a different class from the one
`s223-D8` swept*, and whether they should move is a call I am not making. The evidence:

- **The gate's own class definition excludes them.** `_gate_pack_docs.py:90`:
  `VERSION_RE = re.compile(r"Apollo-Spider-v(\d+\.\d+\.\d+)")`. Arm 3 is *"the pack's own version
  string"* — the **Spider** version. A `Gumdrop v1.0.0` string is not in it, and the gate is silent
  on all three.
- **They are the CARRIED cut's version, whose one home is elsewhere.** `s223-D2` named four homes
  and `MEMENTO_CUT_VERSION` is one of them; `build-designer-pack.sh:180-186` is an explicit #220
  comment saying the Gumdrop version must be **read** from the manifest, never typed. These three
  type it — a real instance of that defect, in files the #220 fix did not reach.
- **This is not new drift.** Measured: `MEMENTO_CUT_VERSION` moved to `v1.0.1` at `3f7a63a`
  (#220) and these three did not move, so **v1.0.1 shipped with the same disagreement**. Leaving
  them is the status quo Dave has already released once; moving them would be a change nobody
  ruled, inside a starter store and two runbook headers.
- `_state.json`'s is a `built_by` field, which reads at least as plausibly as a *provenance record
  of when that starter store was authored* as it does a live self-claim. I could not settle that
  by measurement, which is precisely the DO-NOT-RULE trigger.

**Owed:** one word — leave them, or move all three to `v1.0.2` and put a `Memento — Gumdrop vX`
arm in `_gate_pack_docs.py` so the class cannot come back. This did **not** block the bake:
`s223-D8` names the Spider literal and the class the gate defines, and that is what was swept.

### 1.5 `_gate_pack_docs.py --stage` — before and after

Driven over a real staged tree (`git archive` at `004ddc9`, 1,647 paths + 2 closure copies, with
the manifest copied in as `_MANIFEST.json` so arm 4 could run):

```
BEFORE (staged from the commit, FIRST-SESSION.md as committed):
  === VERSION — 1 finding(s) ===
  [FIRST-SESSION.md] Apollo-Spider-v1.0.1  →  this pack is v1.0.2 — a version string was not swept at bake
  216 finding(s). ADVISORY — exiting 0. This gate is not blocking; promotion is Dave's word.

AFTER (the fixed FIRST-SESSION.md copied over the staged one):
  === COMMAND — 16 finding(s) ===
  === COUNTS — 1 finding(s) ===
  === PATH — 198 finding(s) ===
  215 finding(s). ADVISORY — exiting 0. This gate is not blocking; promotion is Dave's word.
```

**The VERSION arm is now empty — 1 finding → 0.** Total 216 → 215.

⚠ **The brief's "45 baseline" does not match anything this gate produces.** Measured baseline on
the real staged pack is **216** (the bake sub's report quotes **217** from the build's inline run,
which stages one more file — the generated `README.md` — and grades it too). I am reporting the
number I measured, not reconciling it to a figure I cannot reproduce
[[measure-dont-convert-units]]. **The delta is what matters and the delta is exactly the one
finding s223-D8 named.** The other 215 are the COMMAND/PATH/COUNTS arms — pre-existing, advisory,
and out of this brief's scope.

---

## 2. LEG 2 — THE STAMP MOVES OUTSIDE THE ZIP (`s223-D8` clause 2)

### 2.1 The shape of the change

Three edits, all surgical:

**(a) `knowledge/_release/_gen_pack_manifest.py` — the derivation, in one place.**

```python
PACKED_DROP_KEYS = ("status",)

def packed_manifest_text(repo_text):
    """The bytes that ship as `_MANIFEST.json`, derived from the repo-side manifest text."""
    man = json.loads(repo_text)
    for k in PACKED_DROP_KEYS:
        man.pop(k, None)
    return canonical(man)
```

**(b) the same file — a CLI arm, `--pack-copy <out>`,** which refuses if there is no repo-side
manifest (the packed copy is *derived*, never written independently).

**(c) `apollo-spider/build-designer-pack.sh` — what ships, and what gets stamped.**

```diff
-  MAN_SHA="$(… sha256 …)' "$MANIFEST")"          # the REPO-SIDE file
   COMMIT_DATE="$(git … %cI "$COMMIT")"
   …
-  cp "$MANIFEST" "$STAGE/_MANIFEST.json"
+  python3 "$GEN" --pack-copy "$STAGE/_MANIFEST.json"
+  MAN_SHA="$(… sha256 …)' "$STAGE/_MANIFEST.json")"   # THE BYTES THAT ACTUALLY SHIP
```

`MAN_SHA` is the value stamped into `PROVENANCE.json`'s `manifest_sha256` and into the README
provenance table, so both stamps are now computed over the status-free packed content — and, as a
side effect, they are now a fingerprint a designer holding the zip can actually reproduce with
`sha256sum _MANIFEST.json`. It never was before.

### 2.2 The repo-side contract is untouched — and the audit arms stay meaningful

`knowledge/_release/_pack_manifest.json` keeps `status` exactly as before. Checked, not assumed:

- **`--manifest-check`** (`_gate_release_audit.py:100-110`) compares
  `gen.canonical(gen.build_manifest(sha, probe))` against the **repo-side** file's text.
  `build_manifest` still writes `status=ratification_status()`, so the arm still compares like
  with like and still bites. Unchanged.
- **`--drift`** measures the distance between the manifest's named commit and the repo. Never
  read `status`. Unchanged.
- **`--pack`** already excluded the three generated files from byte fidelity
  (`_gen_pack_manifest.py:2306`: `generated = {p for p in got if p in ("README.md",
  "PROVENANCE.json", "_MANIFEST.json")}`), so it never compared the packed manifest to the
  repo-side one. Unchanged.
- **`ratified || die`** in `build-designer-pack.sh` still fences `--release` on the **repo-side**
  status. Dave's word still gates the bake; it just no longer moves the bytes.

**Nothing in the pack ever read the key.** Driven: the pack's readers of `_MANIFEST.json` are
`ci-template/run-gates.py`, `ci-template/gates.yml`, `gumdrop/_helpgate.py`, the canon generators,
`_gen_chain.py` and `_gate_pack_docs.py` — they take `groups`, `verdicts`, `schema` and `totals`.
`grep` for a `status` read of a manifest across the pack sources returns nothing but the
generator's own writer and the rulings-store read.

### 2.3 The selftest — **203 → 214 bites, 0 fails**

Eleven new bites, all under `packed/`:

| bite | what it holds |
|---|---|
| `packed/repo-side-states-differ` | the control — the two repo-side manifests MUST differ, or the next bite is vacuous |
| `packed/word-independent` | **PROPOSED and RATIFIED pack to byte-identical content** |
| `packed/no-status-key` | the packed copy carries no `status` |
| `packed/nothing-else-dropped` | it drops that key and nothing else |
| `packed/mutation-restores-the-defect` | with `PACKED_DROP_KEYS = ()` the two states diverge again |
| `packed/mutation-was-restored` | the in-bite mutation does not leak |
| `packed/real-manifest-has-status` | repo-side keeps the stamp |
| `packed/real-packed-has-none` | the shipped copy of *this cut's actual manifest* has none |
| `packed/bake-derives-the-copy` | the bake calls `--pack-copy` |
| `packed/bake-does-not-cp-the-manifest` | the raw `cp` is gone |
| `packed/stamp-is-over-the-shipped-bytes` | `MAN_SHA` fingerprints the staged file |

The last three exist because the generator can be perfect and the pack still ship the wrong bytes
if the bake copies the file [[instrument-without-a-consumer]].

```
$ python3 knowledge/_release/_gen_pack_manifest.py --selftest
selftest: 214 bites, 0 fail(s)
```

### 2.4 The mutation, DRIVEN in the source and restored

Not the in-bite mutation — the real one, edited into the file:

```
$ sed -i 's/^PACKED_DROP_KEYS = ("status",)$/PACKED_DROP_KEYS = ()  # MUTATION/' knowledge/_release/_gen_pack_manifest.py
$ python3 knowledge/_release/_gen_pack_manifest.py --selftest
selftest: 214 bites, 5 fail(s)
  RED [packed/word-independent] got '…"status": "PROPOSED — no ruling is keyed to v1.0.2 yet"…',
                                wanted '…"status": "RATIFIED — s223-D7 names v1.0.2 in the store"…'
  RED [packed/no-status-key] got True, wanted False
  RED [packed/nothing-else-dropped] got ['commit','groups','schema','status','version'],
                                    wanted ['commit','groups','schema','version']
  RED [packed/mutation-was-restored] got (), wanted ('status',)
  RED [packed/real-packed-has-none] got True, wanted False
```

**Restored** from a pre-mutation copy, and re-driven:

```
$ grep -n "^PACKED_DROP_KEYS" knowledge/_release/_gen_pack_manifest.py
1797:PACKED_DROP_KEYS = ("status",)
$ python3 knowledge/_release/_gen_pack_manifest.py --selftest
selftest: 214 bites, 0 fail(s)
```

And the arm driven for real against this cut's own manifest:

```
$ python3 knowledge/_release/_gen_pack_manifest.py --pack-copy /var/tmp/packed-man.json
packed manifest -> /var/tmp/packed-man.json  (status-free, s223-D8)
  sha256 4bc7e3941201b4ada20f969c2dd468234cc31ad615cd6f0cb69f1d65c7c19815
status in packed:    False
status in repo-side: RATIFIED — s223-D7 names v1.0.2 in the s…
```

---

## 3. LANDING THE PRE-BAKE COMMIT

*(§3 completed in pass 2 — see below.)*

---
