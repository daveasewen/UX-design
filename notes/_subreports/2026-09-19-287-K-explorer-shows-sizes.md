# #287 lane K — the explorer now SHOWS the masters, and the rebuild is done

**2026-09-19 · opus · predecessor `notes/_subreports/2026-09-18-286-R2-masters-registered-as-sizes.md`
(§6 "OWED, not built") · evidence `notes/_lanes/287/K/`**

⬛ **LANDED.** Dave: *"keep `sizes` and rebuild."* The key name is untouched, the explorer is rebuilt,
and the map is now read in three places instead of being one line of JSON nobody would open. **All 8
`logo:` nodes carry `sizes` with 5 keys each in the built page — 40 entries, byte-identical to
`knowledge/_logo_nodes.json`, parsed out of the page and compared, not eyeballed.** `_logo_nodes.json`
is 8 nodes / 33 edges either side — **this lane did not write to it at all.**

---

## 1. What was found first (§1 of the brief)

- `knowledge/_build_kg_explorer.py` bakes the graph into `knowledge/_kg_explorer.template.html`
  (`__KG__` → a `<script id="kg" type="application/json">` block, `__DATE__` → the version line) and
  writes **`notes/_KG-EXPLORER.html`** — `python3 knowledge/_build_kg_explorer.py` with no argument.
- **The logo nodes DO flow in**, through pass E (`asset_nodes()`, `ASSET_FILES =
  ('_icon_nodes.json', '_logo_nodes.json')`), and the pass copies **every field it does not own**:
  `**{k: v for k, v in n.items() if k not in ('id','label','fam','type')}`. So `sizes` was always
  going to ride into the bake — #286 lane R2 read this correctly.
- **But it would not have been READABLE.** INSPECT's record (`recDL`) sends every unclaimed field
  through `fmtVal()`, and `fmtVal` renders any object as `esc(JSON.stringify(v))` — the whole 40-entry
  map as ONE unbroken line, no link, no preview, the digests inline. The aside panel's `logo` head
  (`<dl class="sc">`: file · lockup · theme · colour) named nothing at all, and the artefact tabs for a
  logo were `DRAWN` + `SVG SOURCE`, both of the **parent** SVG — the masters had no door.
- `knowledge/_serve_explorer.py` is stdlib `SimpleHTTPRequestHandler` **rooted at the repo**, so a
  master under `knowledge/assets/logos/masters/` is fetchable by the same runtime `getText()` every
  other artefact uses. No new dependency, no new serving rule.

⬛ **No fenced generator is involved.** §4 of the brief does not fire: the field is visible through
the explorer's own builder, which is not on the fenced list (`gen_kg_rules.py`, `land_rests_on.py`,
`gen_kg_icons.py`, `_build_all.py` — **none was run**). `knowledge/_rulings.json` and
`notes/_RULINGS.html` were **not written**; the builder READS `_rulings.json`, which is all it has
ever done, and §4 below measures what that read cost.

## 2. The change — three reads, all in the template, one line in the builder

### (a) the aside panel names the masters without opening anything

`renderPanel`'s `logo` block gains a fifth row beside file/lockup/theme/colour:

```js
['masters', sh.length ? `<b>${sh.length}</b> · ${esc(sh.join(' · '))} px` : '— none registered']
```

→ **`MASTERS  5 · 24 · 28 · 32 · 36 · 40 px`**. A lockup with no map says so in words rather than
showing an empty row — the same shape the `icon` head uses for a missing group.

### (b) INSPECT's RECORD reads the map, one row per height

`recDL` intercepts the key before `fmtVal` can flatten it:

```js
if(k==='sizes'&&sizeHeights(n).length){rows+=`<dt>sizes · the masters</dt><dd>${sizesDL(n)}</dd>`;continue}
```

Each row is the height, the master's own path as a link, and the stored geometry + digest:

```html
<div class="szrow"><b>24px</b> <a href="../knowledge/assets/logos/masters/hexagon-dark-colour-24.svg"
 target="_blank" rel="noopener">assets/logos/masters/hexagon-dark-colour-24.svg</a>
 <small>48×24 · sha256 6406f4d19efa…</small></div>
```

⚠ **The heights sort NUMERICALLY.** The map's keys are strings, so the default sort would put `"4"`
after `"24"` the day a 4px step is ever registered — `sort((a,b)=>a-b)`, said once in `sizeHeights()`
and used by all three readers, so the ladder cannot lie in one place and be right in another.

The link is built the way every other declared file is: `REL` (`../`, the page lives in `notes/`) +
the builder's own `SRC.fileRoot[n.type]` (`knowledge/` for a logo) + the record's `file`. **No path is
hard-coded and no root is invented** — `masterPath()` reads the same block `declaredFile()` reads.

### (c) INSPECT gains a MASTERS tab, between DRAWN and SVG SOURCE

```js
if((t==='icon'||t==='logo')&&path)return sizeHeights(n).length?[svgTab(path),mastersTab(n),sourceTab(path,'SVG source')]
                                                               :[svgTab(path),sourceTab(path,'SVG source')];
```

`mastersTab()` is `svgTab()`'s shape, five times: each master **fetched at runtime** (never embedded —
the s280-D2 rule), stripped of `<?xml?>` and any `<script>` exactly as DRAWN strips them, and drawn
**at its own declared width×height** — not at a nominal 48/16, because the whole point of a per-size
master is that it is cut for that size. The ground is the lockup's **own `theme`** (`dark` → the dark
cell, else light), since a `-dark-` master on a white ground would be a lie about the asset. Each cell
links its own file and prints `24px · 48×24`. Every fetch carries the modal's `inspSeq` guard, so a
pane that has been navigated away from drops itself; a master that cannot be read leaves **`—`** in its
own cell and the other four still draw. The tab **appears only on a node that has the map**, so the
666 icons and the 10 icon groups are untouched.

CSS: 7 lines, all `var()` tokens already in the file (`--ink`, `--ink-2`, `--ink-3`, `--mono`), reusing
the DRAWN tab's `.icells`/`.icell`/`.box.lt`/`.box.dk` cells with one `auto-fit` override so five cells
wrap instead of the fixed four. **No new dependency, no new colour, no new font.**

### (d) the builder: `VERSION = "1.26"` → `"1.27"`, with its own version note

One line changed (the version string plus its changelog clause, the file's own convention since 1.7).
**No reader, no pass, no map, no coordinate code is touched** — the builder did not need to change,
and did not.

## 3. Verification — parsed, not asserted

`notes/_lanes/287/K/verify.py` re-opens BOTH built pages, `json.load`s the `<script id="kg">` block out
of each and compares against `knowledge/_logo_nodes.json` on disk. Its output verbatim
(`verify-out.txt`):

```
version 1.26 -> 1.27
logo nodes before/after: 8 8 | source file: 8
all 8 logo nodes carry sizes with 5 keys, identical to _logo_nodes.json: True
heights: ['24', '28', '32', '36', '40']
sizes entries total: 40
sizes present in BEFORE build: 0
master files missing on disk: []
nodes total before/after: 4809 4820 | edges: 8630 8648
nodes with moved baked coordinates: 2256

FILE _logo_nodes.json: nodes 8 | edges 33
file edge types: {'usesLogo': 19, 'defaultFor': 2, 'governedBy': 12}
file edges with t null: 3
file edges not present in build: []
BEFORE logo-touching edges 32 {'usesLogo': 18, 'defaultFor': 2, 'governedBy': 12} nulls 2
AFTER  logo-touching edges 32 {'usesLogo': 18, 'defaultFor': 2, 'governedBy': 12} nulls 2
```

| the brief's check | result |
|---|---|
| `sizes` in the output for all 8 logo nodes, 5 keys each | ⬛ **8/8, 40 entries, every value byte-equal to the source record** (key, file, width, height, sha256) |
| logo node count 8 | ⬛ **8 → 8** |
| logo edge count 33 | ⬛ **33 in the file, and all 33 are in the built page** (`file edges not present in build: []`), multiset identical before and after |
| `_validate_kg.py` | ⬛ **exit 0** — *"OK — every ref parses+resolves, every null carries a note, every meta has provenance, edges match schema, `gen_kg_edges.py` is idempotent-clean"* (139 metas, 90 declared nulls, 82 ruled verdicts) |

⚠ **On "33": the built page's *logo-touching* count is 32, and that is not a loss.** The 33rd is the
rail's `usesLogo` **declared null** (s277-D7) — its source is a `component:`, its target is `null`, so
it touches no `logo:` node by definition and a filter on logo endpoints cannot see it. Counted the
other way — every `(s, t, type)` triple in the file looked up in the built edge list — **nothing is
missing**, which is the line printed above.

**The JavaScript parses.** Every inline `<script>` of the built page extracted and run through
`node --check`: **OK** (114,026 bytes, 1 block). The three new functions were then executed for real
in node against the page's own baked data with only `esc`/`SRC`/`REL` stubbed
(`notes/_lanes/287/K/smoke.mjs`, output in `smoke-out.txt`): heights come back
`['24','28','32','36','40']` in order and the five `<a href>`s resolve to paths that exist on disk.

## 4. ⚠ The baked coordinates moved, and NOT because of this version

2,256 nodes have new x/y, and the graph grew by **11 nodes / 18 edges** between the two builds. **None
of it is this lane's**, and the diff says whose it is:

```
nodes added by rebuild: ruling:s282-D6, ruling:s283-D1, ruling:s287-D1, ruling:s287-D2,
  evidence:notes/_lanes/283/DAVE-RULINGS-2026-09-18.md, evidence:notes/_lanes/286/DAVE-RULINGS-2026-09-18.md,
  evidence:notes/_lanes/287/DAVE-RULINGS-2026-09-19.md,
  evidence:notes/_subreports/2026-09-18-286-R2-masters-registered-as-sizes.md,
  artefact:knowledge/_seam.py, artefact:knowledge/_standing.md, artefact:knowledge/assets/logos/_gen_masters.py
nodes removed: []
```

⬛ These are **the Constitution growing under the build's feet**: the standing 1.26 page was built
2026-09-18 09:40, and `knowledge/_rulings.json` has been written since by another lane of this
session (it is `M` in `git status` and this lane is fenced from it — **it was read, never written**).
A rebuild reads the tree as it stands; the force layout is a function of the nodes and edges it is
given, so every coordinate is a new solution of the same solver. **`sizes` adds a field and a field is
not in the layout** — the move is the corpus's, not the field's. The version note in
`_build_kg_explorer.py` says exactly this rather than claiming a byte-identical canvas it could not
have. Nothing was removed; no id moved.

⬛ The four new rulings ride into the built page as ordinary Constitution nodes, which is the same
thing that would happen at any rebuild. **If the commit lane wants the explorer to carry only
committed rulings, it should rebuild after `_rulings.json` lands** — one command, same output shape.

## 5. Every path touched

```
 knowledge/_build_kg_explorer.py      |  2 +-      VERSION 1.26 → 1.27 + its changelog clause
 knowledge/_kg_explorer.template.html | 43 ++++--   the three reads + 7 lines of CSS
 notes/_KG-EXPLORER.html              | 47 ++++--   the rebuild (the KG data block is one line, so
                                                    the data change folds into the line count)
 3 files changed, 85 insertions(+), 7 deletions(-)
 knowledge/_state.json                |            one row ADDED, W-287k (see below)
```

**The store row is `W-287k`**, written through `_state.py`'s module API
(`notes/_lanes/287/K/row_w287k.py`, the shape of #286 R2's `row_w286r.py`) — **`_state.json` was never
hand-edited**. `PRE check ok=True fails=0` → `POST check ok=True fails=0`. Concurrency checked, not
assumed: against `HEAD`, `_state.json` differs by **exactly one added row (`W-287k`), 0 removed, 0
changed** — nothing of another lane's was touched. `_gate_doc_rows.py` re-run after the write: **PASS,
`unrowed 0`**.

⬛ **For the conductor, not decided here:** `W-286rb`'s `closes_when` asks for Dave to accept
**`sizes` as the field name** — and today he said *"keep `sizes`"*. Half of that condition is met by
his own word. It is **lane R2's row, left `open`**; the close is the conductor's to make.

Plus this report and the lane folder `notes/_lanes/287/K/` (untracked):

```
before-_KG-EXPLORER.html (+ .gz) · before-hashes.txt   the standing 1.26 page and its sha
build-stdout.txt · build-stderr.txt (EMPTY)            the builder's own words, exit 0
verify.py · verify-out.txt                             §3, the parse
smoke.mjs · smoke-out.txt                              the three functions run in node on real data
row_w287k.py · row-out.txt                             the store row, through the module API
```

⚠ **`before-_KG-EXPLORER.html` is 4.3 MB.** A `.gz` (807 KB) was written beside it, but **the sandbox
refused to delete the plain copy** (`Operation not permitted` on `unlink` under the mounted repo).
**The commit lane should drop the uncompressed `before-_KG-EXPLORER.html` rather than commit 4.3 MB of
a file the repo already has in its history.** Declared, not hidden.

## 6. How to look at it

```
python3 knowledge/_serve_explorer.py        # from the repo root; follow the URL it prints
```

Then, on the page: turn the **ASSETS** chip on (it loads OFF, unchanged), search **`hexagon`** or
**`masterbrand`**, and press the row's **`i`**.

1. the aside now says **`MASTERS  5 · 24 · 28 · 32 · 36 · 40 px`** under colour;
2. the modal's **RECORD** lists the five heights, each a link to its own master SVG with its
   width×height and digest;
3. the modal's third tab, **MASTERS**, draws all five at their true heights on the lockup's own ground.

⚠ **It must be SERVED.** Opened by double-click (`file://`) the fetches cannot run, the MASTERS cells
show `—` and the banner says so — 1.20's rule, unchanged. The **record rows and the aside row work
from `file://` regardless**, because they read the baked record and never fetch: the field is visible
either way, the drawings are the part that needs the server.

## 7. Refused / not done

- **No commit** — a separate lane commits. Nothing was staged.
- **`gen_kg_rules.py`, `land_rests_on.py`, `gen_kg_icons.py`, `_build_all.py` — not run.** Not needed:
  the field was already in `_logo_nodes.json` and the explorer's own builder is what shows it.
- **`knowledge/_rulings.json` and `notes/_RULINGS.html` — not written.** `_rulings.json` was read by
  the builder, as every build of this page has read it; see §4.
- **`_logo_nodes.json` — not written.** The key name `sizes` stands exactly as #286 lane R2 landed it,
  which is what Dave ruled today.
- **`_build_kg_explorer.py` has no `--check`** (#286 R2 measured the same), so there is no gate to run
  for this file beyond `_validate_kg.py`, which is green.
