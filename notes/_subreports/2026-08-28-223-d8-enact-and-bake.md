# #223 — s223-D8 ENACTED, AND THE v1.0.2 BAKE

**Sub:** Opus build sub · **Conductor:** Fable, session #223 · **Band:** L (~35K)
**Store row:** `W-259` (minted before filing, per the doc-row gate)
**Date:** 2026-08-28
**Rulings enacted:** `s223-D8` (both legs) · `s223-D7` (the bake word, carried to the fixed sha per D8)

> ## ✅ **BAKED. `Apollo-Spider-v1.0.2.zip` · 19,850,657 B · sha256 `3a7fe297140862b7…`**
> ## ✅ **The released zip is BYTE-IDENTICAL to its dry-run twin — which is the whole point of `s223-D8`, and it is now true for every future cut.**
>
> ⏳ Written in two passes: §1–§2 were true at the pre-bake commit; §3 onward were filled in
> after it, because `--release` refuses on a dirty tree.

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

## 3. LANDING THE PRE-BAKE COMMIT — `14af4d7`

### 3.1 The working tree, every path accounted for

I inherited the bake sub's declared uncommitted work. Nothing was discarded.

| path | whose | why it is dirty |
|---|---|---|
| `apollo-spider/FIRST-SESSION.md` | **mine** | leg 1, §1.2 |
| `apollo-spider/build-designer-pack.sh` | **mine** | leg 2, §2.1(c) |
| `knowledge/_release/_gen_pack_manifest.py` | bake sub's `RATIFY_IDS` v1.0.2 row **+ mine** (leg 2) | both kept |
| `knowledge/_release/_pack_manifest.json` | bake sub's | regenerated at `004ddc9`, status RATIFIED |
| `reviews/RELEASE-SPIDER-2026-08-26-v1.html` + `.REVIEW.html` | bake sub's | page regenerated from the RATIFIED manifest, overlay re-injected |
| `knowledge/_state.json` | bake sub's `W-258` **+ mine** | see §3.2 |
| `knowledge/_rulings.json` | **conductor's** — `s223-D7`/`s223-D8` | never written by me |
| `knowledge/_probe/session-223.json`, `notes/_dream/_GRADE-DECISIONS.jsonl` | conductor's | session bookkeeping |
| `notes/_REHEARSAL-LOG.jsonl` | conductor's + dry-run appends | — |
| `notes/_subreports/2026-08-28-223-bake-v102.md` | bake sub's report | untracked, carried in |
| `_CHAIN.md` | **mine** | `_gen_chain.py` before the commit |

### 3.2 ⛔ A REFUSAL I HAD TO CLEAR FIRST — `W-258` was malformed

`python3 knowledge/_state.py` was **exiting 1** on the bake sub's own row:

```
⛔ W-258: condition='UNCONDITIONED' but closes_when is "Dave's fifteen-minute Copilot first-session…" — say which it is
⛔ W-258: UNCONDITIONED and NOT in the frozen legacy set. You cannot open an item without stating
   what would end it. The 19 inherited items are exempt … a NEW item has no such excuse.
```

The row carried a real `closes_when` **and** `condition: "UNCONDITIONED"` — the one combination
the gate names as incoherent. `_state.add()` derives the field
(`it.setdefault("condition", CONDITIONED if it.get("closes_when") else UNCONDITIONED)`); the row
had been hand-shaped instead. **No judgment was available:** with a `closes_when` present the only
legal value is `stated`. Repaired through the module's own `load`/`save`, not by hand-editing the
JSON. The declared-debt count fell 15 → 14, and the frozen legacy set is untouched.

My own row, `W-259`, was minted through `_state.add()` with `home` pointing at this file — which
had to exist first, since `add()` refuses an unresolvable home (it did refuse, once, and that
refusal is why the report skeleton was written before the row).

```
items 332 · live 252 · conditioned 318 · UNCONDITIONED 14      (exit 0)
```

### 3.3 The commit

```
$ python3 knowledge/_gen_chain.py                    # or the commit script refuses STALE
$ SESSION_N=223 bash knowledge/_git_commit.sh --reconciled /var/tmp/msg-223-prebake.txt --all-dirty
  doc-row gate: population 146 · staged-in-THIS-commit 2 · unrowed 0
  ✅ PASS — every in-scope document has a store row.
  [master 14af4d7] … 14 files changed, 830 insertions(+), 60 deletions(-)
$ bash knowledge/_git_commit.sh --push
  ✅ pushed and VERIFIED: remote master == local 14af4d76c2eac378b6f72fdf4836a2bc6d201c94
```

**Landing sha 1 — `14af4d76c2eac378b6f72fdf4836a2bc6d201c94`.** Subject, read back from
`git log -1`:

> `after #223 2026-08-28 — the v1.0.2 pre-bake fix commit - s223-D8 enacted in both legs: the stale Apollo-Spider-v1.0.1…`

---

## 4. THE RELEASE SURFACE AT THE LANDING SHA — `bff12fe`

```
$ python3 knowledge/_release/_gen_pack_manifest.py --probe    --commit 14af4d76c2ea…   # 49s
$ python3 knowledge/_release/_gen_pack_manifest.py --manifest --commit 14af4d76c2ea…
  manifest -> knowledge/_release/_pack_manifest.json
    commit 14af4d76c2ea  files 1647  bytes 41678300  sha256 dfb9603b94065076

  version: v1.0.2   commit: 14af4d76c2ea
  status:  RATIFIED — s223-D7 names v1.0.2 in the store; s219-D4(2) satisfied by the store, not by prose
  GATES GROUP: gates   files: 58
```

- **Gates group 58 — exactly Dave's ruled `s223-D6` figure.** It did not move, so there was
  nothing to stop for. Derived from a fresh 49-second probe, not carried over.
- **Status RATIFIED via the `RATIFY_IDS` `v1.0.2 → s223-D7` row.** His word carried to the fixed
  sha; he was not re-asked, per `s223-D8`.
- Ship list unchanged from `004ddc9`: 1,647 files / 41,678,300 bytes.

```
$ python3 knowledge/_release/_gate_release_audit.py --manifest-check
PASS — the manifest … is byte-identical to a fresh generation at 14af4d76c2ea (1647 files, sha256 dfb9603b94065076)
$ python3 knowledge/_release/_gate_release_audit.py --drift
PASS — the manifest was generated at HEAD (14af4d76c2ea). The ship list is current.
```

Page + review pair regenerated from that manifest, then committed and pushed.

**Landing sha 2 — `bff12fe2a00a5540d3fe7322a27e95ffe09e9bd6`**, subject:

> `after #223 2026-08-28 — the release surface regenerated at the s223-D8 landing sha 14af4d7 - gate probe re-measured (…`

---

## 5. THE BAKE — **AND THE POINT OF `s223-D8` HELD**

### 5.1 Dry-run twice at `14af4d7`

```
$ bash apollo-spider/build-designer-pack.sh --dry-run --out-dir /var/tmp/dr1 --commit 14af4d76c2ea…
sha256: 3a7fe297140862b706f83c072e52be1a8c0af5145c6f8b5a516d198ce9f287b6
$ … --out-dir /var/tmp/dr2 …
sha256: 3a7fe297140862b706f83c072e52be1a8c0af5145c6f8b5a516d198ce9f287b6
$ cmp /var/tmp/dr1/…zip /var/tmp/dr2/…zip && echo BYTE-IDENTICAL
BYTE-IDENTICAL          19850657 bytes each
```

### 5.2 The word-independence proof, on the real artefact

Before the release, with the repo-side manifest forced back to `PROPOSED` (the exact experiment
the bake sub ran, which then gave two different shas):

```
$ …status = "PROPOSED — no ruling is keyed to v1.0.2 yet…"
$ bash apollo-spider/build-designer-pack.sh --dry-run --out-dir /var/tmp/dr3 --commit 14af4d76c2ea…
sha256: 3a7fe297140862b706f83c072e52be1a8c0af5145c6f8b5a516d198ce9f287b6      ← THE SAME
$ git checkout -- knowledge/_release/_pack_manifest.json                       # restored
```

| | before `s223-D8` (bake sub, measured) | after (this cut, measured) |
|---|---|---|
| manifest PROPOSED | `26eb33c3…` | **`3a7fe297…`** |
| manifest RATIFIED | `6787d87d…` | **`3a7fe297…`** |

### 5.3 `--release` into `dist/`

Tree cleaned first (a dry-run rewrites the go/no-go page), then:

```
$ bash apollo-spider/build-designer-pack.sh --release --commit 14af4d76c2ea…
  216 finding(s). ADVISORY — exiting 0.        ← VERSION arm 0 findings (was 1; total was 217)
pack:   apollo-spider/dist/Apollo-Spider-v1.0.2.zip
sha256: 3a7fe297140862b706f83c072e52be1a8c0af5145c6f8b5a516d198ce9f287b6
size:   19,850,657 B
```

> ## ✅ **RELEASED sha256 == DRY-RUN sha256 — `3a7fe297…`. The fence held.**

The advisory gate over the real baked stage: `COMMAND 16 · COUNTS 2 · PATH 198 · VERSION 0`.
(The COUNTS arm reads 2 here and 1 in §1.5 because the bake's stage also carries the *generated*
`README.md` with its typed `files:` figure. Pre-existing, advisory, out of scope.)

### 5.4 ⛔ ONE REFUSAL, AND ITS REPAIR — `--check` went RED

```
$ bash apollo-spider/build-designer-pack.sh --check apollo-spider/dist/Apollo-Spider-v1.0.2.zip --commit 14af4d76c2ea…
CHECK RED — 1 problem(s):
  pack README does not carry the manifest hash
```

**A true consequence of leg B, and the arm was wrong, not the pack.** `check_pack()` asserted the
README carried `manifest_hash(canonical(man))` — the sha of the **repo-side** manifest. After
`s223-D8` the README stamps the sha of the manifest **that ships**. Repaired so the arm reads
those bytes back out of the zip, and gained a second assertion in the same edit:

```python
packed = z.read(root + "/_MANIFEST.json")
packed_sha = hashlib.sha256(packed).hexdigest()
if packed_sha not in txt: …
if packed.decode("utf8") != packed_manifest_text(canonical(man)):
    fails.append("the shipped _MANIFEST.json is not the status-free derivation "
                 "of the repo-side manifest (s223-D8)")
```

This is **strictly stronger** than what it replaced: the old arm compared the README to a file
sitting *outside* the pack and would have passed a zip whose own `_MANIFEST.json` had been
swapped. The repo↔pack link is not lost — it is now asserted directly, as the derivation
identity. I judged this mechanical (the arm's stated intent is unchanged; only the object it
measures moved, and it moved because `s223-D8` moved it). Re-driven:

```
CHECK GREEN — apollo-spider/dist/Apollo-Spider-v1.0.2.zip matches the manifest at 14af4d76c2ea
$ python3 knowledge/_release/_gen_pack_manifest.py --selftest
selftest: 214 bites, 0 fail(s)
```

`knowledge/_release/_gen_pack_manifest.py` is **not** a shipped path, so the repair does not need
to be inside this zip.

### 5.5 The ledger seed — `s223-D5(3)`, in the #220 two-commit shape

`--seed` **measures the committed surface** (`git ls-tree -r <rev>`), so seeding before the zip
landed produced a false row — driven and observed:

```
$ python3 knowledge/_release/_gate_frozen_release.py --seed        # BEFORE the zip commit
  apollo-spider   version v1.0.2   2 file(s)  027ce796a98b         ← 2 files: no v1.0.2 zip
$ cp /var/tmp/ledger-before.json knowledge/_release/_frozen-releases.json   # restored, byte-identical
```

`s223-D2`'s "in the same commit" is satisfied the way #220 satisfied it — **verified, not
assumed**: `git rev-list --ancestry-path 9f58516..b0b49de` shows the v1.0.1 ledger seed is a
*descendant* of the v1.0.1 bake commit. Same order here:

```
e33ea1b   the zip + the --check repair + the re-folded page
a91b7e0   the ledger seed
$ python3 knowledge/_release/_gate_frozen_release.py --seed        # AFTER the zip commit
  apollo-spider   version v1.0.2   3 file(s)  d20213cf3d14
```

The row moves `content_sha256` `027ce796…` → `d20213cf…` **with** the version bump
`v1.0.1` → `v1.0.2` in that same commit — the legal act `s114-D4` describes, and the shape the
laundering arm exists to require.

### 5.6 The gates, driven

```
$ python3 knowledge/_release/_gate_frozen_release.py            # at a91b7e0, post-commit
frozen-release gate — 3 release(s) at a91b7e035812
  designer-skills-v1   version v1          6 file(s)  b83d048483b7
  designer-skills-v2   version v2        849 file(s)  e1d8019b97cc
  apollo-spider        version v1.0.2      3 file(s)  d20213cf3d14
PASS — 3 arm(s) asked, no frozen surface moved.                                   rc=0

$ python3 knowledge/_release/_gate_release_audit.py --manifest-check
PASS — … byte-identical to a fresh generation at 14af4d76c2ea
$ python3 knowledge/_release/_gate_release_audit.py --pack
SKIPPED — …v1.0.0.zip is FROZEN HISTORY …
SKIPPED — …v1.0.1.zip is FROZEN HISTORY …
PASS — apollo-spider/dist/Apollo-Spider-v1.0.2.zip matches the manifest at 14af4d76c2ea
```

`apollo-spider/dist/`'s history was never touched: v1.0.0 and v1.0.1 are byte-unchanged and the
gate says so.

---

## 6. THE COMMITS, AND CI

| sha | what |
|---|---|
| `14af4d7` | the s223-D8 pre-bake fix (both legs) |
| `bff12fe` | the release surface regenerated at `14af4d7` |
| `e33ea1b` | **Spider v1.0.2 BAKED** — the zip, the `--check` repair, the re-folded page |
| `a91b7e0` | the frozen-release ledger seed |

All pushed; `remote master == local a91b7e035812b427387bdb988ec1d491e8cd269b`, verified by the
commit script's own read-back.

### ⛔ CI — **COULD-NOT-RUN**

```
$ curl -s https://api.github.com/repos/daveasewen/UX-design/actions/runs?per_page=5
{ "message": "Not Found", "status": "404" }
```

The repo is private and this sandbox holds no GitHub credential, so the unauthenticated API
cannot see it. **404 is not a CI verdict and I am not reporting one.** The conductor owes the
read-back via Dave's Chrome.

---

## 7. UNPROVEN / OWED

- **⬛ THE STANDING UNPROVEN — Dave's fifteen-minute Copilot first-session** on his own machine.
  `s223-D7` names it the only real test; it is the `closes_when` on `W-259`. Everything in this
  report is machine evidence about the pack, not evidence that the pack *works for him*. What
  changed in its favour: step one of that session no longer sends him to a directory that does
  not exist.
- **⛔ CI — COULD-NOT-RUN** (§6).
- **⚠ OWED A WORD — the three `Memento — Gumdrop v1.0.0` literals** (§1.4). Not touched, not
  ruled. They also shipped in v1.0.1.
- **⚠ The brief's "45 baseline"** for `_gate_pack_docs.py` is not reproducible (§1.5); measured
  216 → 215 with the VERSION arm going 1 → 0.
- **Not attempted:** promoting the pack-docs gate to blocking, and surfacing its advisory
  findings on the go/no-go page. Both are ruling-shaped, both named by the bake sub, neither
  ruled.

---

## 8. REPLAY-THESE

```bash
cd <repo>

# LEG 1 — the sweep, over every path the manifest carries
python3 - <<'PY'
import json, os
m = json.load(open('knowledge/_release/_pack_manifest.json'))
paths = sorted({p for g in m['groups'] for p in g['paths']})
for p in paths:
    for i, line in enumerate(open(p, encoding='utf-8', errors='replace').read().splitlines(), 1):
        if 'v1.0.1' in line or 'v1.0.0' in line:
            print(f"{p}:{i}: {line.strip()[:180]}")
PY
grep -n "VERSION_RE" knowledge/_release/_gate_pack_docs.py      # the class the gate defines

# the gate, over a real staged tree
mkdir -p /var/tmp/dgate/Apollo-Spider-v1.0.2
python3 knowledge/_release/_gen_pack_manifest.py --stage /var/tmp/dgate/Apollo-Spider-v1.0.2 --commit 14af4d7
cp knowledge/_release/_pack_manifest.json /var/tmp/dgate/Apollo-Spider-v1.0.2/_MANIFEST.json
python3 knowledge/_release/_gate_pack_docs.py --stage /var/tmp/dgate/Apollo-Spider-v1.0.2 | grep -E "=== |ADVISORY"

# LEG 2 — the packed manifest is status-free, and the mutation is red
python3 knowledge/_release/_gen_pack_manifest.py --selftest                  # 214 bites, 0 fail(s)
sed -i 's/^PACKED_DROP_KEYS = ("status",)$/PACKED_DROP_KEYS = ()/' knowledge/_release/_gen_pack_manifest.py
python3 knowledge/_release/_gen_pack_manifest.py --selftest                  # 5 fail(s)
git checkout -- knowledge/_release/_gen_pack_manifest.py                     # ⚠ RESTORE
python3 knowledge/_release/_gen_pack_manifest.py --pack-copy /var/tmp/packed-man.json
python3 -c "import json;print('status' in json.load(open('/var/tmp/packed-man.json')))"   # False

# THE FENCE — dry-run == release, and PROPOSED == RATIFIED
bash apollo-spider/build-designer-pack.sh --dry-run --out-dir /var/tmp/dr1 --commit 14af4d7
sha256sum apollo-spider/dist/Apollo-Spider-v1.0.2.zip /var/tmp/dr1/Apollo-Spider-v1.0.2.zip
#   both 3a7fe297140862b706f83c072e52be1a8c0af5145c6f8b5a516d198ce9f287b6

# the released pack, and the frozen surfaces
bash apollo-spider/build-designer-pack.sh --check apollo-spider/dist/Apollo-Spider-v1.0.2.zip --commit 14af4d7
python3 knowledge/_release/_gate_frozen_release.py
python3 knowledge/_release/_gate_release_audit.py --manifest-check
python3 knowledge/_release/_gate_release_audit.py --pack
```

---

## 9. PITFALLS FOR WHOEVER PICKS THIS UP

- **⛔ NOTHING SURVIVES A TOOL-CALL BOUNDARY IN THIS SANDBOX.** I backgrounded the gate probe with
  `nohup` and polled it across calls; `pgrep -f "…--probe"` matched the *polling shell's own
  command line* and reported STILL RUNNING for **35 minutes** while the process had been dead
  since the first boundary. Run it inline: it takes **49 seconds**. A liveness check whose
  pattern matches the checker is not a liveness check.
- **`--seed` measures the COMMITTED surface**, so the bake is two commits: zip first, ledger
  second. Verified against #220's own order.
- **A dry-run rewrites the go/no-go page** (folding in the zip size and sha) and strips the review
  overlay — so it dirties the tree, and `--release` refuses on a dirty tree. Restore the page
  before `--release`; re-inject the overlay after it.
- **`--check`'s README arm is now about the PACKED manifest** (§5.4). Anything else that compares
  a shipped file to its repo-side twin should be looked at through the same lens.
- **The manifest's commit and the bake's commit must match**, and the release commit is therefore
  always a *later* commit than the one the pack was cut from. `--drift` will read one behind
  immediately after a bake; that is the shape, not a defect.
