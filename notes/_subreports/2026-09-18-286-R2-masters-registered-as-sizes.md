# #286 lane R2 — the 40 masters are registered, as SIZES on the 8 existing nodes

**2026-09-18 · opus · predecessor `notes/_subreports/2026-09-18-286-R-masters-registered.md`
(lane R: nothing landed, and why) · evidence `notes/_lanes/286/R2/`**

⬛ **LANDED.** `knowledge/_logo_nodes.json` carries the 40 accepted masters as a `sizes` field on
the 8 lockup nodes. **Nodes 8 → 8. Edges 33 → 33, multiset identical. The 12 hand-authored
`governedBy` edges of s282-D5 are byte-identical after the run.** Nothing was lost in either
output file, and that is a parse, not a claim.

⚠ **Two `--land` invocations, not one, and the first was fully reverted.** The reason is §5 — a
SECOND hand-repair, in the *icon* file, that the brief did not name and that the first land ate.
The tree was restored byte-for-byte (sha proof below) before anything else happened.

---

## 1. Dave's word, and exactly what it settles

> *"okay size-on-the-existing-node"*

Appended verbatim to `notes/_lanes/286/DAVE-RULINGS-2026-09-18.md` with the question it answered —
**whether a master is its own node under its lockup, or a size field on the lockup's existing
node.** It refuses lane R's shapes 2 (40 `logo:<stem>-<h>` nodes) and 3 (a `logoMaster:` kind) and
rules shape 1.

⚠ **What he did NOT name: the field's key.** He named the location. `sizes` is this lane's reading
of the file's own vocabulary, and it is declared as such in the rulings file, not claimed as his:

- the node's other fields each carry **one** parsed value — `lockup`, `theme`, `colourMode`,
  `file` — and are singular;
- the generator's **collections** are plural — `nodes`, `edges`, `unresolved`, `fills`, `groups`;
- **five** masters hang on one node, so the collection is plural. `size` would be a lie about the
  count.

⬛ **#75 is not touched.** The generator's own fence reads *"A NEW NODE KIND AND A NEW EDGE TYPE
ARE CLOSED-VOCABULARY CHANGES (#75)"*. A **field** on an existing node of an existing kind is
neither. `RATIFIES` is unchanged, no new ratifying id was asked for or invented, and the land ran
under the same `s277-D4` the file already records.

---

## 2. The generator diff

```
 knowledge/_icon_nodes.json                     | 147 ++++++---
 knowledge/_logo_nodes.json                     | 276 +++++++++++++++-
 knowledge/_state.json                          |  29 +-
 notes/_lanes/277/icons-propose/gen_kg_icons.py | 421 ++++++++++++++++++++++++-
 4 files changed, 810 insertions(+), 63 deletions(-)
```

### (a) the masters are READ — `logo_masters()`, new

`logo_stems()` is **deliberately left non-recursive** and now says why: making it recursive is
exactly how 40 `logo:<stem>-<h>` ids would be minted, which is the shape Dave refused. The masters
are read by a separate function that returns fields, not nodes:

```python
def logo_masters(corpus=None):
    """Reads `assets/logos/masters/*.svg` and returns (sizes, refused). …"""
    …
        sizes.setdefault(m.group("stem"), {})[m.group("h")] = {
            "file": rel, "width": w, "height": h,
            "sha256": hashlib.sha256(raw).hexdigest()}
```

Every figure is **measured**: `svg_box()` reads the root element's own `width=`/`height=` (the
masters carry raw pixels and no `viewBox`, by `_gen_masters.py`'s design), and the sha256 is of the
file's bytes. **Three refusal routes, each declared, never a silent drop** — a name that does not
parse, a master whose `<svg>` declares no numeric geometry, and one whose filename claims a height
its own bytes contradict. All three land in `unresolved` as ledger-only rows (`source: null`, type
`logo:` — the class the malformed lockup stem already uses), because a size is a field and a field
has no arrow to null.

### (b) the field is attached — `build()`, no node minted

```python
    masters, master_refused = ({}, []) if no_logos else logo_masters(corpus)
    for stem in sorted(masters):
        if stem not in logo_fields:
            unresolved.append({… "a master never mints the node it hangs on"})
            continue
        nodes[LOGO + stem]["sizes"] = {h: masters[stem][h] for h in sorted(masters[stem], key=int)}
```

The map is written onto a node `add()` already made, so `len(nodes)` is identical either side of
the block. New report keys: `masters_on_disk`, `masters_attached`, `masters_refused`,
`logos_with_sizes`, `master_size_steps`.

### (c) `--land` MERGES instead of clobbering — `merge_landed()` + `extend_verdict()`, new

Five rules, **all stated by provenance marker or by shape, none naming s282-D5, `governedBy`, a
rule id or any value this tree holds today**:

1. an edge marked `authored: "hand"` is kept verbatim;
2. a generated edge is dropped when a kept hand edge already speaks for the same `(source, type)` —
   this is what suppresses the 6 `t: null` stubs lane R predicted;
3. the `unresolved` rows for those same pairs go with them — a resolved null is not an open null;
4. the `edge_types` status line is kept from disk for any type a kept hand edge draws (the
   generated line for such a type says "never drawn", which would be false);
5. every **top-level key the generator does not produce** is carried over verbatim — this is what
   saves `$s282-D5`, with no code that knows its name.

Plus, added after §5's finding: **row-level fields**. In any top-level list of records both files
carry, a rebuilt row keeps every field the landed row has and the build does not produce. The
generator still wins on every field it does produce, so its own prose stays live; an identity that
is not unique on both sides is left alone and **counted**, never merged on a guess.

`extend_verdict()` finds any top-level dict carrying a `generatorVerdict` **string** — the shape
`notes/_lanes/282/logo-land/bind.py` composed — keeps that sentence (it is true of the run it
describes) and appends, after a marker, what THIS run did, from the merge's own receipt. The marker
makes it **idempotent**: a second land replaces its own clause instead of growing the string
(proved by bite 24, which lands twice and compares).

### (d) selftest: 22 → 24 bites, all green

```
python3 notes/_lanes/277/icons-propose/gen_kg_icons.py --selftest   →   SELFTEST PASS
```

- **bite 23** — the masters are fields, not nodes: no id ending in `-<digits>` exists, `logo` node
  count is unchanged, the `sizes` map is keyed by raw height, and **the sha256 is recomputed inside
  the bite from the exact bytes the fixture wrote**, so a generator that invented, copied or cached
  a digest goes red. All three refusals asserted by their own sentences.
- **bite 24** — merge-on-write: a hand edge, its `edge_types` line and a top-level block survive a
  regenerate; the null stub for the hand edge does **not** come back; the verdict records what was
  preserved; and a second land changes nothing further.

The mini corpus gained a `masters/` directory with 3 good masters and 3 that must be refused.

---

## 3. Dry run, then the land — and the structured JSON diff

**BEFORE** (= `HEAD`, verified: `git show HEAD:…` hashes match):

```
9409c60144e464922d127e051484446eae3693106e8d3b2b10ab6fbacdace072  knowledge/_logo_nodes.json
5bc419187774b1a4f9ed8df7d36cfc982db80fb33788a675ace8370ad87f6bc7  knowledge/_icon_nodes.json
```

**Dry run** (the default mode) into `notes/_lanes/286/R2/dryrun`, exit 0, stderr empty:

```
DRY RUN — 666 icon records · 10 groups · 8 logos  ->  684 nodes · 1321 edges
  nodes: {'iconGroup': 10, 'icon': 666, 'logo': 8}
```

and in its own `dry-run.json`: `masters_on_disk 40 · masters_attached 40 · masters_refused []
· master_size_steps [24, 28, 32, 36, 40] · logos_with_sizes` = all 8 stems. **684 nodes, the same
684 as before: 40 masters registered, 0 nodes added.** The live files were byte-identical after the
dry run.

**The land** (`--land --ratified s277-D4`), its own words:

```
LANDED — ratified s277-D4 · ['_icon_nodes.json', '_logo_nodes.json']
  masters: 40 of 40 attached as `sizes` fields on 8 existing logo node(s) at steps [24, 28, 32, 36, 40] — 0 nodes minted (Dave: size-on-the-existing-node)
  _icon_nodes.json: MERGED — kept 0 hand-authored edge(s) [], dropped 0 generated edge(s) and 0 unresolved row(s) they speak for, carried [], extended verdict in []
  _logo_nodes.json: MERGED — kept 12 hand-authored edge(s) ['governedBy'], dropped 6 generated edge(s) and 6 unresolved row(s) they speak for, carried ['$s282-D5'], extended verdict in ['$s282-D5']
```

### The structured diff of `_logo_nodes.json` (`notes/_lanes/286/R2/diff-logo.json`)

| | |
|---|---|
| node count | **8 → 8** |
| nodes added | **0** |
| nodes removed | **0** |
| node fields changed | `sizes` on all 8 nodes, **and nothing else on any node** |
| edge count | 33 → 33, **`edge_multiset_identical: true`**, 0 added, 0 removed |
| top-level keys added / removed | **0 / 0** |
| top-level keys changed | `$description`, `$s282-D5` (its `generatorVerdict`) — **and nothing else** |

That is exactly the brief's acceptable set: the new `sizes` field + the verdict, plus the
`$description` sentence the generator composes on every land (its text now records the
preservation instead of instructing a human to re-run `bind.py`).

A sample entry, the shape landed on every node:

```json
"24": {
  "file": "assets/logos/masters/hexagon-dark-colour-24.svg",
  "width": 48, "height": 24,
  "sha256": "6406f4d19efa80691ea078a53bb8abe5188bfd049e21d0cbbc7b13caca6c22a4"
}
```

---

## 4. The preserved-fields proof — parsed, not asserted

`notes/_lanes/286/R2/preserved-proof.txt`, verbatim:

```
governedBy DRAWN edges before/after: 12 / 12
all 12 byte-identical: True
all marked authored=hand after: True
targets after: ['rule:logo26-008', 'rule:logo26-009', 'rule:logo26-010']
ratified: s277-D4 | $s282-D5 present: True | keys equal: True
resolvedNulls preserved: True
edge_types.governedBy preserved verbatim: True
governedBy t:null stubs after: 0
unresolved rows before/after: 3 / 3
edge fields lost: []
node fields lost: []
top-level keys lost: []
sizes entries: 40 | verified against disk: 40 | bad: []
distinct heights: [24, 28, 32, 36, 40]
```

Each of the 40 size entries was re-opened from disk: the sha256 recomputed, the declared
`width=`/`height=` found in the file's own bytes, and the map key checked equal to the height.

The verdict now reads (the #282 sentence kept, this run's clause appended):

> *gen_kg_icons.py --land --ratified s277-D4 was RUN FIRST and did not pick the new rules up:
> governedBy is in NULL_ONLY_TYPES; the regen changed 6 `why` lines only … and drew 0 edges*
> **`|| MERGE-ON-WRITE (#286 lane R2):`** *the generator no longer clobbers: --land now READS the
> landed file and MERGES, keeping 12 hand-authored edge(s) (governedBy) verbatim, 0 row field(s)
> the build does not produce, suppressing the 6 generated edge(s) and 6 unresolved row(s) those
> edges speak for, keeping the edge_types status line(s) for governedBy, and carrying the 1
> top-level field(s) it does not generate ($s282-D5). Re-applying
> notes/_lanes/282/logo-land/bind.py after a regenerate is NO LONGER NEEDED — verified by this
> run's own before/after diff, not asserted.*

---

## 5. ⛔ THE SECOND FINDING — a hand repair in the ICON file, which the first land ate

The brief named one hand repair (`bind.py`, the logo file). **There is a second one**, and the
first `--land` of this lane destroyed it. The STOP condition was met, the tree was restored, and
the merge was widened before anything landed for keeps.

**What happened, in order, all measured:**

1. `--land` ran with merge-on-write as first written (edges + top-level keys only). The
   `_logo_nodes.json` diff was already clean (§3). The `_icon_nodes.json` diff was **not**:
   `ruled` rows lost a `flagged_as` sentence on **14 rows**.
2. `grep` on the generator: **`flagged_as` appears 0 times in `gen_kg_icons.py`**. It appears in
   `notes/_lanes/280/inscribe-active/_inscribe2.py` — **`bind.py`'s opposite number for the icon
   file**, a #280 hand-repair script. So those 14 sentences were hand state, and the run ate them.
3. ⇒ **Reverted.** `git checkout` was unavailable (another lane held `.git/index.lock`; the lock
   was left alone, not removed), so both files were restored from this lane's own pre-land copies
   and the restoration was **proved by sha** against `git show HEAD:` — `9409c601…` and
   `5bc41918…`, byte-identical to HEAD.
4. The merge was widened to row-level fields (§2c), and **rehearsed against a throwaway corpus of
   symlinks** — the live tree untouched and re-hashed to prove it — until the loss test came back
   empty.
5. Only then did the second `--land` run. **The live output is byte-identical to the rehearsal
   output** (`9240fdd0…` / `a486efda…` both sides), so the run is reproducible, not lucky.

**What the icon file's diff is now** (`notes/_lanes/286/R2/icon-residual-diff.txt`), all measured:

- **nothing lost**: `edge fields lost: []`, `node fields lost: []`, `ruled`/`unresolved` row fields
  lost `[]`, `top-level keys lost: []`. All 14 `flagged_as` sentences are present and **identical**;
  `ruled` is row-for-row identical.
- **additions**: 13 edges gain `$his_note` (Dave's own words, read from his exports — e.g.
  *"alert-active-2 is incorrectly labeled"*) and 10 gain `$his_flags`; these were absent from the
  landed file.
- **prose refreshed** by the current generator's own composition, on fields the generator produces:
  14 `$ruled` sentences, 1 `$open`, 1 `his_answer`, plus `$description`, `$ruled` and
  `edge_types.defaultActive`. ⚠ **The one to look at**: `his_answer` on `icon:jade-lifestyle` was
  written by `_inscribe2.py` and is now the generator's shorter sentence. **No fact moved** — both
  say he answered `open` and no twin is drawn — and **Dave's own words in `his_note` are
  byte-identical** (*"jade-lifestyle-active-2 - think is the most likely the correct icon"*).
  Because the generator produces that field itself, no generic rule can tell a hand version from a
  stale generated one; the merge lets the generator win on fields it writes. **Declared here rather
  than decided quietly.**

⬛ **Generalised, because it will happen again:** `_logo_nodes.json` and `_icon_nodes.json` have
each had a hand-repair script standing in for a generator that could not hold a ruling. Both are
now unnecessary **for edges and for row fields**; the `authored: "hand"` marker is the durable way
to keep something across a regenerate, and the landed `$description` now says so in the file
itself.

---

## 6. The consumer checks

Before and after, read-only, from `knowledge/_git_commit.sh`'s own list
(`notes/_lanes/286/R2/checks-before.txt` / `checks-after.txt`):

| check | before | after | |
|---|---|---|---|
| `gen_showroom.py --check` (s191-D1) — the showroom consumer | 0 | **0** | `137 page(s) + index in sync` |
| `_validate_polarities.py --check` (s238-D7) | 0 | **0** | `polarity gate GREEN` |
| `_build_graph_mention_map.py --check` | 0 | **0** | `current (102 of 102 node(s) mentioned)` |
| `_gate_doc_rows.py` | 0 | **0** | `PASS — every in-scope document has a store row` |
| `_validate_kg.py` | 0 | **0** | `OK — every ref parses+resolves …` |
| `_gen_chain.py --check` | **1** | **1** | ⚠ `_CHAIN.md is STALE` — **ALREADY RED at lane open**, before this lane wrote anything (lane R measured the same). Not caused here; `_gen_chain.py` is a generator and was not run. **The commit lane must run it and stage the result, or `_git_commit.sh` refuses at its chain gate.** |
| `_compose_slice.py --selftest` (the other `_logo_nodes.json` consumer) | **6 of 79 fail** | **6 of 79 fail** | ⚠ **identical six, before and after** — proved by re-running it with the pre-land files swapped in and the landed files restored by sha afterwards. They are bites 46/57/60/62/71/73 (`logos.md` has no `_scope.json` row; `logo26-001`/`va25-015`/`va25-016` ruleFacets overrides; the `restsOn` verb `$source`) — the #282/#281 residue, **not this lane's**. |

`gen_kg_icons.py --selftest`: **24 bites, SELFTEST PASS.**
`knowledge/_state.py --selftest`: **57 bites, all GREEN.**

### ⬛ OWED, not built

**`notes/_KG-EXPLORER.html` does not show the sizes.** Measured: `grep -c '"sizes"'` → **0**, and a
master's sha256 → **0**. The builder copies every node field it does not itself own
(`_build_kg_explorer.py`: `**{k: v for k, v in n.items() if k not in ('id','label','fam','type')}`)
and INSPECT renders a node's full stored record, so **the field will appear when the explorer is
next rebuilt** — and the baked coordinates will move, as every version note in that file says.
`_build_kg_explorer.py` offers **no `--check`**, so nothing goes red in the meantime and no gate is
being dodged. **Not built here: a rebuild is a generator run this lane was not sent to make.**

---

## 7. Row receipts

**`W-285lm` — CLOSED**, through `knowledge/_state.py`'s module API
(`notes/_lanes/286/R2/close_w285lm.py`, the shape of lane S's `close_w285sc.py`; `_state.json` was
never hand-edited). **`closes_when` is UNCHANGED** — no condition was invented or rewritten.

Both halves are met: the **eye** half at #285 (Dave accepted the regenerated masters on the 4×
contact sheet — the literal condition), and the **registration** the row was deliberately held open
for, which is now done and measured.

The writer's own words, verbatim:

```
PRE  check ok=True fails=0 notes=4
BEFORE state: open
BEFORE closes_when: Dave has looked at the 4x before/after contact sheet and either accepted the
regenerated masters by eye or named what still looks wrong
POST check ok=True fails=0
  NOTE: DECLARED DEBT: 14 item(s) carry no close condition (W-0b, W-01, W-02, W-03, W-04, W-05,
W-06, W-07, W-08, W-09, W-10, W-11, W-12, W-13). Frozen set size 19 — this number may only fall.
Each needs Dave's word, not an agent's guess.
  NOTE: real-input coverage: 1 item(s) carry a deadline, 0 carry an effort; on those items the
dashboard's PROXY is REPLACED. The rest of the 595 live item(s) are still scored by prose scan /
body length.
  NOTE: project split: apollo 550 · memento 152 (of 702 items). The values written at #172 are
DEFAULTS proposed for Dave's eye, not his ruling on each item.
  NOTE: home pointers: 684 resolve by ANCHOR (rot-proof), 18 are still `path:line` (UNVERIFIABLE by
content — the #168 rot class), 0 UNRESOLVABLE. Blocking = True (Dave's dial).
save() would reorder items: False
closes_when unchanged: True
SAVED
AFTER state: done | closes_when unchanged: True | closed_by len: 1406
counts: {"total": 702, "live": 595, "by_state": {"open": 595, "blocked": 0, "ruled": 0, "done": 87,
"dropped": 0, "parked": 20}, "by_owner": {"dave": 311, "claude": 284}, "unconditioned": 14,
"conditioned": 688}
```

⚠ **Concurrency, checked not assumed** (`notes/_lanes/286/R2/state-concurrency.txt`): against
`HEAD`, `_state.json` now differs by exactly **one added row, `W-286p` (another lane's, carried
through my `save()` untouched)** and **one changed row, `W-285lm` (mine: `state`, `closed_by`,
`links`)**. Nothing of another lane's was clobbered.

**This report's own row is `W-286rb`, NOT `W-286r` — and the deviation is deliberate.**
`W-286r` was already taken when this lane reached the store: it is **lane R's** row, home
`notes/_subreports/2026-09-18-286-R-masters-registered.md`, `closes_when` = *"Dave has ruled the
SHAPE of the master registration…"*. The doc-row gate counts a document rowed **only by a `home`
field** (`_gate_doc_rows.py:25`), so re-pointing that home would have **orphaned lane R's own
report**. `W-286r2` is refused by the store's id regex `^(?:W-[0-9]{1,3}[a-z]{0,2}|G[0-9]{1,2}[a-z]?)$`
— measured, by being refused — so the id is **`W-286rb`**, added through `_state.add()` with
`home` = this report (`notes/_lanes/286/R2/row_w286r.py`; `POST check ok=True fails=0`;
`_gate_doc_rows.py` PASS, `unrowed 0`, re-run after the write).

**`W-286r` (lane R's) was AMENDED, not moved.** Its body gained one paragraph recording that the
shape is now ruled and the registration landed, and its links gained this report and this lane's
folder. ⚠ **Its `closes_when` now reads as MET** — Dave ruled the shape, and the registration it
names is done — **but its `state` was left `open`**: it is not this lane's row and the commit lane
may be quoting it as it stands. **That close is the conductor's to make.**

---

## 8. ⛔ Ruling-shaped, left open for Dave

1. **The field's KEY NAME.** He ruled the location (`size-on-the-existing-node`); `sizes` is this
   lane's reading of the file's vocabulary, recorded as such in
   `notes/_lanes/286/DAVE-RULINGS-2026-09-18.md`. One word from him renames it; nothing else moves.
2. **`his_answer` on `icon:jade-lifestyle`** (§5): a hand-written sentence replaced by the
   generator's own on a field the generator owns. No fact moved and his own words are untouched,
   but the class — *"who owns a field both a human and the generator write?"* — is his to settle if
   he wants a rule rather than this lane's default (the generator wins on what it writes).
3. **The explorer rebuild** (§6): a rebuild moves every baked coordinate, as it has at every
   version since 1.22. That is a generator run and a judgement about when to spend it.

---

## Working files (all under `notes/_lanes/286/R2/`, none in /tmp)

```
before-_logo_nodes.json · before-_icon_nodes.json · before-hashes.txt   the pre-land tree (= HEAD)
dryrun/                                     the default-mode dry run (3 JSONs)
dryrun-stdout.txt · dryrun-stderr.txt       the generator's own words (stderr empty)
land-stdout.txt                             the FIRST land — the one that was reverted
rehearsal-stdout.txt · rehearsal-_*.json    the throwaway-corpus rehearsal, live tree untouched
land2-stdout.txt                            the land that stands, byte-identical to the rehearsal
jsondiff.py · diff-logo.json · diff-icon.json   the structured diff and its tool
preserved-proof.txt                         the 12 edges, the 40 sizes, the loss test
icon-residual-diff.txt                      §5's measurement, in full
checks-before.txt · checks-after.txt · compose-slice-BEFORE.txt
close_w285lm.py · state-writer-dryrun.txt · state-writer-output.txt · state-concurrency.txt
```

**Net effect on tracked files: `gen_kg_icons.py` (+421), `_logo_nodes.json`, `_icon_nodes.json`,
one row in `_state.json`, one line in the rulings file, and this report. Nothing committed —
a commit lane follows.**
