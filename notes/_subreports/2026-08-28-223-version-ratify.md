# #223 FILED REPORT — the v1.0.2 version move + the per-cut ratify re-key

**Session** #223 · 2026-08-28 · **Model** Opus (build sub) · **Conductor** Fable seat
**Rulings enacted** `s223-D2` (the cut is v1.0.2, four homes, ledger re-seed) · `s223-D3` (ratify re-keyed per cut)
**Repo state at work** `HEAD = fe4994289442f2119fdb6f2b9d1514300cfb49f7`
**Files changed (3, uncommitted — this lane commits nothing)**
`apollo-spider/build-designer-pack.sh` · `knowledge/_release/_gen_pack_manifest.py` · `knowledge/_release/_gate_frozen_release.py`

---

## 0. THE HEADLINE, FOR THE CONDUCTOR

1. **Version moved to v1.0.2 in every live home** — plus a FIFTH home the brief did not name (a
   hand-moved selftest fixture) which would have gone red at the next selftest.
2. **The ratify re-key is DONE and DRIVEN.** v1.0.2 reads `PROPOSED`, v1.0.0 still reads
   `RATIFIED`, and a planted ruling flips it on. All three controls ran; nothing was UNPROVEN.
3. **⛔ I DID NOT LEAVE THE LEDGER RE-SEEDED, and this is a deviation from `s223-D2`'s letter.**
   I drove `--seed`, measured what it produces, and it produces a FALSE ROW: version `v1.0.2`
   over a surface holding **no v1.0.2 zip**. Worse, it makes the laundering arm go RED **at the
   bake**. I restored the ledger byte-identical to HEAD and left the re-seed for the bake commit,
   which is what #220 did. **This is a ruling-shaped question — §6, Q1. Dave or the conductor
   settles it, not me.**
4. Two smaller findings for the release plan: a stale prose line on the go/no-go page (§5-F2) and
   a stale generated `_pack_manifest.json` whose only fence is the commit-match arm (§5-F3).

---

## 1. RULED GROUND, QUOTED FROM THE STORE

Read from `knowledge/_rulings.json` (the store, not a paraphrase) before any edit.

**`s223-D2`**, `ruled`:

> THE CUT IS v1.0.2 - A PATCH ON THE PACK'S OWN PROMISE (WORKS OUT OF THE BOX), MOVED IN ALL FOUR
> HOMES IN ONE COMMIT WITH THE LEDGER RE-SEED, v1.0.1 STAYS FROZEN HISTORY

`says`, the operative sentence:

> The number moves in build-designer-pack.sh, _gen_pack_manifest.py VERSION and
> MEMENTO_CUT_VERSION, and the frozen-release ledger row, with the ledger re-seeded in the same
> commit so the laundering arm stays honest.

**`s223-D3`**, `ruled`:

> THE RATIFY CHECK IS RE-KEYED PER CUT: --release MUST REFUSE ON A v-NEXT MANIFEST UNTIL A RULING
> NAMING THAT SPECIFIC CUT IS IN THE STORE - THE HARD-CODED s219-D10 KEY (v1.0.0'S WORD, HONOURED
> FOREVER) IS RETIRED AS THE GATE

`says`, the operative sentence:

> Dave rules the fix: each cut requires his fresh word - a ruling naming this cut's version in the
> store - before the manifest may read RATIFIED. His fresh word for v1.0.2 itself is NOT this
> entry; it is given only after his eye on the release page, per the #222 plan item 11.

**Honoured:** I did not grant v1.0.2 its word. The machine now ASKS. `RATIFY_IDS` has no v1.0.2
row and must not get one until Dave rules.

---

## 2. PART 1 — THE VERSION MOVE

### 2.1 BEFORE — the four homes, quoted

```
$ grep -n "v1\.0\.1" --include=*.py --include=*.sh --include=*.json  (live code homes only)
./apollo-spider/build-designer-pack.sh:38:VERSION="v1.0.1"
./knowledge/_release/_gen_pack_manifest.py:107:VERSION = "v1.0.1"                     # Spider's own lineage starts here; v1/v2 stay frozen
./knowledge/_release/_gen_pack_manifest.py:109:MEMENTO_CUT_VERSION = "v1.0.1"
./knowledge/_release/_gate_frozen_release.py:115:    ("apollo-spider", ["apollo-spider/dist/"], "v1.0.1",
./knowledge/_release/_frozen-releases.json:36:      "version": "v1.0.1"
```

**⚠ THE GATE PATH IS NOT WHERE THE BRIEF SAID IT WAS.** The brief named
`knowledge/_gate_frozen_release.py`; the file is at **`knowledge/_release/_gate_frozen_release.py`**.
`wc -l knowledge/_gate_frozen_release.py` → `No such file or directory`. Found by `find`.

**⚠ HOME 4 IS TWO PLACES, NOT ONE.** The ledger row's `version` field is **not typed into the
JSON** — `seed()` reads it from the `SURFACES` literal in the gate file:

```python
row = dict(id=rid, version=version, surface=list(prefixes), ...)
```

so `_frozen-releases.json:36` is an OUTPUT. The editable home is the gate's `SURFACES` literal.
The gate's own #220 comment says so in as many words:

> `seed()` takes a row's `version` from HERE, not from the zip's filename

### 2.2 THE FIFTH HOME — found, and it would have gone red

`_gen_pack_manifest.py:2733` is a selftest bite whose expected value is a **hand-moved fixture**
pinned to `MEMENTO_CUT_VERSION`:

```python
    bite("naming/memento-cut-is-named", (MEMENTO_CUT_NAME, MEMENTO_CUT_VERSION),
         ("Memento — Gumdrop", "v1.0.1"),
```

Its own comment states the discipline: *"Moved v1.0.0 -> v1.0.1 at the #220 bake, in the same edit
as MEMENTO_CUT_VERSION itself."* Moving `MEMENTO_CUT_VERSION` without moving this literal turns
the generator's 195-bite selftest red. Moved, and the comment extended (not replaced):

```python
    # Moved v1.0.0 -> v1.0.1 at the #220 bake, and v1.0.1 -> v1.0.2 at #223 (s223-D2), each
    # time in the same edit as MEMENTO_CUT_VERSION itself.
```

### 2.3 AFTER — quoted

```
$ grep -n 'VERSION="v1.0.2"' apollo-spider/build-designer-pack.sh
38:VERSION="v1.0.2"

$ grep -n '^VERSION = \|^MEMENTO_CUT_VERSION = ' knowledge/_release/_gen_pack_manifest.py
107:VERSION = "v1.0.2"                     # Spider's own lineage starts here; v1/v2 stay frozen
109:MEMENTO_CUT_VERSION = "v1.0.2"

$ grep -n '"apollo-spider", \["apollo-spider/dist/"\]' knowledge/_release/_gate_frozen_release.py
112:    ("apollo-spider", ["apollo-spider/dist/"], "v1.0.2",
```

`_frozen-releases.json` still reads `v1.0.1` **deliberately** — see §3.

### 2.4 Parse + import proofs

```
$ bash -n apollo-spider/build-designer-pack.sh
build-designer-pack.sh: parses clean

$ python3 -c "<exec_module _gen_pack_manifest.py>"
import: clean
VERSION            = v1.0.2
MEMENTO_CUT_VERSION= v1.0.2
RATIFY_IDS         = {'v1.0.0': 's219-D10'}

$ python3 knowledge/_release/_gen_pack_manifest.py --selftest
selftest: 195 bites, 0 fail(s)          exit=0

$ python3 knowledge/_release/_gate_frozen_release.py --selftest
selftest: 14 bites, 0 fail(s)
```

---

## 3. THE FROZEN-RELEASE GATE — VERDICT ON ALL ARMS, AND THE RE-SEED DECISION

### 3.1 Baseline, before any edit

```
$ python3 knowledge/_release/_gate_frozen_release.py --check
frozen-release gate — 3 release(s) at fe4994289442
  designer-skills-v1   version v1          6 file(s)  b83d048483b7
  designer-skills-v2   version v2        849 file(s)  e1d8019b97cc
  apollo-spider        version v1.0.1      2 file(s)  027ce796a98b

PASS — 3 arm(s) asked, no frozen surface moved.
exit=0
```

**3 arms asked** = arm 1 surface + arm 2 working tree + arm 3 laundering. No COULD-NOT-ASK
refusal — the parent commit and its ledger blob are both reachable in this checkout.

### 3.2 After the version move, ledger un-seeded — FINAL STATE OF THE TREE

```
$ python3 knowledge/_release/_gate_frozen_release.py --check
frozen-release gate — 3 release(s) at fe4994289442
  designer-skills-v1   version v1          6 file(s)  b83d048483b7
  designer-skills-v2   version v2        849 file(s)  e1d8019b97cc
  apollo-spider        version v1.0.1      2 file(s)  027ce796a98b

PASS — 3 arm(s) asked, no frozen surface moved.
exit=0
```

**Arm-by-arm verdict on the final tree:**

| arm | verdict | why |
|---|---|---|
| 1 · surface (blocking) | **PASS** | `apollo-spider/dist/` is untouched; measured sha `027ce796a98b` = recorded sha. |
| 2 · working tree (blocking) | **PASS** | my three edited files are `build-designer-pack.sh` and two files under `knowledge/_release/` — **none is under a frozen prefix** (`designer-skills-v1/`, `designer-skills-v2/`, `apollo-spider/dist/`). |
| 3 · laundering (blocking) | **PASS** | the ledger blob is byte-identical to the parent's, so no row's `content_sha256` moved. |

### 3.3 ⛔ THE RE-SEED — DRIVEN, MEASURED, THEN DELIBERATELY NOT LEFT IN PLACE

I ran `--seed` and captured what it produces:

```
$ python3 knowledge/_release/_gate_frozen_release.py --seed
seeded knowledge/_release/_frozen-releases.json at fe4994289442
  designer-skills-v1   version v1          6 file(s)  b83d048483b7
  designer-skills-v2   version v2        849 file(s)  e1d8019b97cc
  apollo-spider        version v1.0.2      2 file(s)  027ce796a98b

⚠ If a frozen surface MOVED, bump that row's `version` in this same commit — the laundering arm is what checks you did.
```

The row it writes:

```json
{
  "id": "apollo-spider",
  "version": "v1.0.2",
  "baseline_commit": "fe4994289442f2119fdb6f2b9d1514300cfb49f7",
  "files": 2,
  "content_sha256": "027ce796a98b2ee65efceb7de39a236df8b3db061a6d39e03452723802ec6528"
}
```

**Two things are wrong with keeping that, and both are measured, not believed.**

**(a) It is a FALSE RECORD.** `files: 2`, and the two are:

```
$ git ls-tree -r --name-only HEAD -- apollo-spider/dist/
apollo-spider/dist/Apollo-Spider-v1.0.0.zip
apollo-spider/dist/Apollo-Spider-v1.0.1.zip
```

The row would assert *"the frozen surface recorded at v1.0.2"* over a surface containing **no
v1.0.2 artefact**. The ledger's own `_README` says every field here is MEASURED, never claimed —
this row would be a claim wearing a measurement's clothes.

**(b) IT GUARANTEES A RED AT THE BAKE.** The laundering arm keys on exactly this:

```python
        moved = old.get("content_sha256") != row.get("content_sha256")
        if moved and old.get("version") == row.get("version"):
```

Projected, with real values:

| commit | ledger version | content_sha | arm 3 |
|---|---|---|---|
| parent (HEAD `fe49942`) | v1.0.1 | `027ce796…` | — |
| **if I re-seed now** | v1.0.2 | `027ce796…` (unmoved) | green (`moved`=False) |
| **the bake commit** (adds `Apollo-Spider-v1.0.2.zip`) | v1.0.2 (**unchanged**) | **moves** | **🔴 RE-RECORDED WITHOUT A VERSION BUMP** |

The birth clause cannot save it — it fires only when the parent recording is
`_EMPTY_SURFACE_SHA`, and `027ce796…` is not empty. The gate's own selftest proves this shape is
red and it is currently green: bite `laundering/bites` — *"re-seeding a moved surface without
bumping the version must stay RED"*.

**Leaving the re-seed for the bake commit makes arm 3 go GREEN instead:** parent v1.0.1/`027c…`
→ bake commit v1.0.2/new sha = a content move **with** a version bump, which is the legal act
`s114-D4` describes. This is precisely what #220 did, recorded in the gate at line 108–113:

> Moved with the bake, in the same commit as the content, exactly as the _README says.

**So I restored the ledger and verified it byte-identical to HEAD:**

```
$ git diff --stat -- knowledge/_release/_frozen-releases.json
(empty — byte-identical to HEAD)
```

I did **not** use `git checkout` (forbidden); I restored from a copy taken before the seed.

**The `SURFACES` literal is already moved to `v1.0.2`, so the bake's single `--seed` will produce
the correct row with no further edit.** The re-seed is now a one-command step in the bake, §7.

**DECLARED:** `s223-D2` says *"with the ledger re-seeded in the same commit"*. If the commit it
means is the BAKE commit, the tree is already correct and nothing is owed. If it means THIS
commit, I have deviated, on the measured ground above, and §6-Q1 puts it to Dave. I did not force
an arm to pass and I did not silently reinterpret his ruling.

---

## 4. PART 2 — THE PER-CUT RATIFY RE-KEY

### 4.1 What was there

```python
RATIFY_ID = "s219-D10"

def ratification_status():
    ...
    for r in rl:
        if r.get("id") == RATIFY_ID and r.get("status") == "ruled":
            return ("RATIFIED — %s, Dave's word 'bake' (2026-08-26); "
                    "s219-D4(2) satisfied by the store, not by prose" % RATIFY_ID)
    return "PROPOSED — awaiting Dave's word (s219-D4(2): release = his word)"
```

The lookup never mentions the version. `s219-D10` is `ruled` and permanent, so **every** future
manifest inherited it.

### 4.2 What is there now — EXPLICIT MAPPING, per the brief's preference

```python
RATIFY_IDS = {
    "v1.0.0": "s219-D10",   # #219, Dave's word 'bake' (2026-08-26)
}

RULINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_rulings.json")


def ratify_id(version=None):
    """The ruling id that ratifies THIS cut — None if no ruling has been keyed to it yet."""
    return RATIFY_IDS.get(VERSION if version is None else version)


def ratification_status(store_path=None, version=None):
    v = VERSION if version is None else version
    p = RULINGS_PATH if store_path is None else store_path
    data = json.load(open(p))
    rl = data if isinstance(data, list) else data.get("rulings", data.get("entries"))
    if rl is None:
        raise SystemExit(...)                      # ← LOUD failure preserved, and preserved FIRST
    want = ratify_id(v)
    if want is None:
        return ("PROPOSED — no ruling is keyed to %s yet (s223-D3: ...)" % v)
    for r in rl:
        if r.get("id") == want and r.get("status") == "ruled":
            return ("RATIFIED — %s names %s in the store; "
                    "s219-D4(2) satisfied by the store, not by prose" % (want, v))
    return ("PROPOSED — %s is keyed to ruling %s, which is not 'ruled' in the store ..." % (v, want))
```

**Design notes, each deliberate:**

- **The store read happens BEFORE the key lookup.** A malformed store still dies loud even for a
  cut with no key — otherwise the re-key would have quietly traded a real `SystemExit` for a
  cheerful `PROPOSED`. The old contract (*"Fails LOUD on a malformed store; a missing entry is
  not an error, it is PROPOSED"*) survives intact.
- **Three outcomes, not two.** *no key* / *key present but not `ruled`* / *ratified* now say
  different things, so a future reader can tell "nobody has ruled" from "the ruling is not ruled".
- **`store_path`/`version` are optional seams** added so the mutation control (§4.5) could run
  without going near the real store. Zero call sites changed behaviour.
- **`RULINGS_PATH` uses `abspath`** — the old line used bare `__file__`, which is cwd-fragile.
- **The `s219-D4(2)` provenance comment is UPDATED, NOT DELETED.** Every original sentence is
  still there; `s223-D3`'s paragraph is added beneath it, and it names the retired constant
  `RATIFY_ID = "s219-D10"` so a grep for the old name still lands on the explanation.
- **Why mapping, not text-match** — recorded in the comment, because it is the load-bearing
  reason: `s223-D3`'s own body contains the string `v1.0.2` while explicitly *withholding* the
  word. A substring hunt across `says` fields would have ratified v1.0.2 off the very ruling that
  refuses to ratify it. *A gate that cannot tell a mention from a mandate is not a gate.*
- `_gen_pack_manifest.py:1865` used `RATIFY_ID` in the go/no-go page prose; now `ratify_id()`.
  That branch runs only under `status_word() == "RATIFIED"`, which implies the key exists.

```
$ grep -rn "RATIFY_ID\b" --include=*.py --include=*.sh .   (excluding RATIFY_IDS)
./knowledge/_release/_gen_pack_manifest.py:569:# `RATIFY_ID = "s219-D10"`, which is Dave's word for v1.0.0 and for nothing else. Because the
```
Only the explanatory comment remains. No live reference to the retired constant.

### 4.3 NEGATIVE PROOF — v1.0.2 does NOT read RATIFIED (driven)

```
NEGATIVE (this cut, v1.0.2):
  status_word()        -> PROPOSED
  ratification_status()-> PROPOSED — no ruling is keyed to v1.0.2 yet (s223-D3: the ratify check is re-keyed PER CUT). s219-D4(2): release = his word, and this cut has not had it.
  ratify_id()          -> None
```

**And the refusal itself is DRIVEN, not quoted.** The build script's fence is:

```bash
ratified() {
  python3 - "$MANIFEST" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
sys.exit(0 if str(m.get("status", "")).upper().startswith("RATIFIED") else 1)
PY
}
```
```bash
  if [ "$MODE" = release ]; then
    require_clean
    ratified || die "the manifest's status is not RATIFIED. s219-D4(2): the exact cut is a
         proposed manifest for Dave's eye BEFORE the bake — release is his word, not the
         script's. Show him reviews/RELEASE-SPIDER-*.html, then set the status."
```

I fed that exact predicate a **throwaway** manifest carrying the new v1.0.2 status string:

```
$ python3 - /tmp/_throwaway_manifest.json   # the same 4 lines as ratified(), verbatim
ratified() exit code = 1 -> would DIE (--release refuses)
```

**The refusal is PROVEN at the predicate level.** What is **UNPROVEN-UNTIL-BAKE-STAGE** is the
full `bash build-designer-pack.sh --release --commit <sha>` invocation: `require_clean` runs
BEFORE `ratified`, the tree is dirty, so an end-to-end drive today would die on the dirty-tree
arm and prove nothing about ratification — *[[refusal-names-the-first-obstacle]]*. I did not dirty
the record by claiming it.

### 4.4 POSITIVE CONTROL — v1.0.0's history is preserved

```
POSITIVE CONTROL (v1.0.0 history):
  ratify_id("v1.0.0")  -> s219-D10
  status               -> RATIFIED — s219-D10 names v1.0.0 in the store; s219-D4(2) satisfied by the store, not by prose
```

Read from the **real** store. `s219-D10` remains the valid key for v1.0.0, honoured forever, as
`s223-D3` requires.

### 4.5 MUTATION CONTROL — RATIFIED flips ON, and the real store was never touched

The real `_rulings.json` was deep-copied in memory, a fake row appended to the **copy** only, and
`ratification_status(store_path=…)` pointed at the copy:

```
copy written to /sessions/nice-dreamy-johnson/tmp/tmpa6bcdi1j/_rulings_COPY.json
real store still 270 rows; copy has 271

A. copy + NO mapping row for v1.0.2 -> PROPOSED
B. copy + mapping row, fake entry ruled -> RATIFIED — sFAKE-D1 names v1.0.2 in the store; s219-D4(2) satisfied by the store, not by prose
   status_word against copy -> RATIFIED
C. REAL store + mapping row, no such id ->  PROPOSED — v1.0.2 is keyed to ruling sFAKE-D1, which is not 'ruled' in the store (s219-D4(2): release = his word)

real _rulings.json on disk unchanged: True
```

**The control RAN — it is not COULD-NOT-RUN.** Three arms, and C is the bonus one: it proves the
check bites on a *dangling* key too, so a mapping row added ahead of the ruling cannot ratify
anything. The mapping mutation was **in-memory on the module object only**; nothing on disk
gained a v1.0.2 row. `knowledge/_rulings.json` was never opened for writing at any point in this
lane.

---

## 5. FINDINGS — things the brief did not name

**F1 · The gate lives at `knowledge/_release/_gate_frozen_release.py`, not `knowledge/`.**
The brief's path does not exist. *[[premise-ages-faster-than-rule]]* — worth correcting in the
release plan before another sub is sent to the wrong file.

**F2 · The go/no-go page's RATIFIED lede is typed prose, and it is v1.0.0's.**
`_gen_pack_manifest.py:1864` still reads:

```python
        A('<p class="lede">#219 · 2026-08-26 · ratified by %s — Dave’s word, in the store. '
```

The `%s` is now derived, but `#219 · 2026-08-26` is hard-typed. When Dave ratifies v1.0.2 the page
will print *his* id under *v1.0.0's* session and date. Same class as #220's `Apollo-Spider-v1.0.0/`
defect. **Left alone: rewriting the ratification page's wording brushes DO-NOT-RULE.** Priced:
~10 min to derive session+date from the keyed ruling's own record.

**F3 · The committed `_pack_manifest.json` is stale, and only ONE fence stands between it and a
waved-through bake.**

```
manifest version: v1.0.1
manifest status : RATIFIED — s219-D10, Dave's word 'bake' (2026-08-26); ...
manifest commit field: 789f4331242ef7bca6d7bfd8d0f1765bafff6e4f
HEAD                 : fe4994289442f2119fdb6f2b9d1514300cfb49f7
```

`ratified()` reads this file, and the `--release` path checks it **before** anything regenerates
it. What saves it is the commit-match arm immediately above:

```bash
  MAN_COMMIT="$(python3 -c '...["commit"]' "$MANIFEST")"
  [ "$MAN_COMMIT" = "$COMMIT" ] \
    || die "the manifest was generated at ${MAN_COMMIT:0:12}, you asked to bake ${COMMIT:0:12}."
```

`789f4331 ≠ fe499428`, so any bake at a current sha is forced through `--manifest` first, and that
regeneration carries `VERSION = v1.0.2` and `PROPOSED`. **The hole is closed, but by an arm that
was not designed for it.** I did **not** regenerate the manifest: a working-tree regen is
throwaway, the real one is generated at the landing sha. Flagged so the bake sequence does not
skip the `--manifest` step.

**F4 · The ledger row's `note` is now slightly stale.** It reads *"v1.0.0 stays beside v1.0.1 and
the row's version names the newest"* while the row's version will be v1.0.2. Cosmetic, inside the
gate, and the brief forbids gate edits beyond the version literal — so **untouched, declared**.

**F5 · Tension noted, not resolved by me.** The brief says *"FORBIDDEN: … touching … any gate
other than reading"*, and Part 1(4) requires moving the ledger row, whose only editable source is
a literal inside that gate. I made the **one-token** change (`"v1.0.1"` → `"v1.0.2"` in `SURFACES`)
and nothing else in that file. Coverage, prefixes and arms are untouched, so DO-NOT-RULE ("any
change to what the frozen-release gate covers") is intact.

---

## 6. RULING-SHAPED QUESTIONS

**Q1 (blocking the commit) · Which commit carries the ledger re-seed?**
`s223-D2` says *"re-seeded in the same commit"*. Measured (§3.3), re-seeding in the **bump** commit
writes a row naming a version whose zip does not exist, and makes the laundering arm RED at the
bake. Re-seeding in the **bake** commit is #220's precedent and is green.
 (a) **Re-seed at the bake** — my recommendation; tree is already in this shape; zero further edits.
 (b) **Re-seed now** — one command (§7); accepts a false row now and a red arm at the bake.
 (c) **Squash bump+bake into one commit** — satisfies `s223-D2` literally and stays green, but
 gives up the separate reviewable version-bump commit.

**Q2 (later, Dave's own) · The v1.0.2 ratification.** `RATIFY_IDS` deliberately has no v1.0.2 row.
When Dave gives the word after his eye on the release page, the inscription lands the ruling and
**one line** is added: `"v1.0.2": "<his ruling id>",`. Not mine to write, and not written.

**Q3 · Is the mapping the permanent shape?** It is a ledger that grows one row per cut — v1.0.0's
row must never move. Confirm that reading; the alternative (drop old rows) would silently unratify
history.

---

## 7. REPLAY-THESE

Every command below was run from the repo root and its output is quoted above.

```bash
# the four homes, after
grep -n 'VERSION="v1.0.2"' apollo-spider/build-designer-pack.sh
grep -n '^VERSION = \|^MEMENTO_CUT_VERSION = ' knowledge/_release/_gen_pack_manifest.py
grep -n '"apollo-spider", \["apollo-spider/dist/"\]' knowledge/_release/_gate_frozen_release.py
grep -n '"version": "v1.0' knowledge/_release/_frozen-releases.json      # still v1.0.1 — see §3.3

# parse + import + selftests
bash -n apollo-spider/build-designer-pack.sh
python3 knowledge/_release/_gen_pack_manifest.py --selftest               # 195 bites, 0 fail(s)
python3 knowledge/_release/_gate_frozen_release.py --selftest             # 14 bites, 0 fail(s)

# the frozen-release gate, all three arms
python3 knowledge/_release/_gate_frozen_release.py --check                # PASS — 3 arm(s) asked

# ratify: negative, positive, and the flip
python3 -c "import importlib.util,sys
spec=importlib.util.spec_from_file_location('gpm','knowledge/_release/_gen_pack_manifest.py')
m=importlib.util.module_from_spec(spec); sys.modules['gpm']=m; spec.loader.exec_module(m)
print('v1.0.2 ->', m.status_word(), '|', m.ratify_id())
print('v1.0.0 ->', m.ratification_status(version='v1.0.0'))"

# ⛔ ONLY IF Q1 answers (b): the re-seed. Run it at the BAKE commit under answer (a).
# python3 knowledge/_release/_gate_frozen_release.py --seed
```

**NOT run, and why:**
- `bash apollo-spider/build-designer-pack.sh --release --commit <sha>` end-to-end —
  **UNPROVEN-UNTIL-BAKE-STAGE**: `require_clean` precedes `ratified`, the tree is dirty, so the
  drive would prove the dirty-tree arm, not the ratification arm. The predicate itself WAS driven
  (§4.3).
- `--manifest` regeneration — throwaway from a dirty working tree; the real manifest is generated
  at the landing sha. See F3.

---

## 8. FENCES HONOURED

- `knowledge/_rulings.json` — **never opened for writing.** Proven: `real _rulings.json on disk
  unchanged: True`. The mutation control used an in-memory deep copy written to a tmpdir.
  (It shows as `M` in `git status` — that is the conductor's own `s223-D2`/`s223-D3` inscription
  from earlier today, not this lane.)
- `apollo-spider/dist/` — untouched. Arm 2 (working tree, untracked included) is green, which is
  machine proof, not my word.
- No `git commit`, `git add`, or `git checkout`. The ledger restore used a plain file copy.
- No gate modified beyond the single version literal `SURFACES` requires (F5).
- No new memory hooks.
- No reformatting: `git diff --stat` = `build-designer-pack.sh | 2 +-`,
  `_gate_frozen_release.py | 2 +-`, `_gen_pack_manifest.py | 55 +++--` (the ratify block plus its
  provenance comment).
