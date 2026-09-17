# `#281`-`PH` — principles get a home: `s281-D1` inscribed, 32 family nodes, 100 dark principles → 0

session: `#281` · 2026-09-17
window: lane PH — principles get a home
sub index: `PH`
brief: `notes/_lanes/281/principles-home/BRIEF.md`
tokens: `~165,000` — the difference between the remaining-budget counter reported to this lane at its
first tool call and at its last. `CLAIMED`, not `message.usage`: the seat does not hand
`message.usage` to a lane, so this is the closest honest reading available, and it is a budget
delta, which includes re-read context, not only new tokens.

## VERDICT

DONE, all four regions. `s281-D1` is inscribed in `knowledge/_rulings.json` by textual span —
**`git diff --numstat` reads `22  0`, zero deletions** — and it says what Dave said: the 32 research
families of the register enter the graph as `family:<id>` nodes in the `uxprinciples` family, and
`inFamily` and `evidencedBy`, held behind flags by `s275-D2` since #275, are ratified into the closed
vocabulary and switched on. The generator's own door landed them:
`gen_kg_principles.py --land --ratified s281-D1 --family-edges --evidence-edges` →
**32 family nodes · 145 `inFamily` edges · 134 `evidencedBy` edges + 11 declared nulls over 53 new
`evidence:` nodes**, every null carrying the register's own prose in its note, none dropped, none
guessed. Explorer **1.22** gives `family:` its type chip and its own plum token beside `--c-ux` and
`--c-polarity` — lane CM's second fall-through, learnt rather than repeated. The proof:
**108 dark dots → 8 at every-chip-on + Constitution, and the 100 dark UX principles → 0**; the 8 that
remain are exactly the logo lockups Dave answered `leaf`, and `dark_everywhere_by_type` reads
`{'ux': 100, 'logo': 8}` before and `{'logo': 8}` after. `_validate_kg.py` green, page errors `[]` in
all six shots, served.

Two things the brief did not predict and one it did. **It did:** the baked coordinates MOVE — 85 new
dots and 290 new lines enter the force layout, so every node's solution is new;
`md5 5233db6775b35040860600cc73416880` → `ae09dc26d0f16b6fb3fbd56504e3b118`, and that second md5 is
identical across two independent rebuilds, so the layout is deterministic, not drifting. **It did
not:** (1) `evidencedBy` is ONE storage type in TWO families now — 1,265 governance lines and 145
uxprinciples lines — and the page's draw predicate `EON` read the family off the TYPE map alone,
which would have counted the new lines under the Explanation chip while drawing them only under the
Constitution. `EON` now reads the edge's own `fam` first, which is what `recount()` has always done
for the counts and what INSPECT's edge door has done since 1.21; the change is a measured no-op for
every other edge in the graph (Finding 3). (2) `knowledge/_kg_explorer.template.html` is not in the
brief's Gates file list and had to be touched — the chip, the colour token and `EON` all live there
and Do-3 cannot be done without it. Declared, not smuggled: see the GATES section.

COUNTS: findings `7` · ruling-shaped `3` · UNPROVEN `3`

## What was done

1. **`s281-D1` inscribed** — `knowledge/_rulings.json`, by textual span, inserted between the last
   element's closing `}` and the array's `]` as ` ,` + the object, so not one existing byte moved:
   `git diff --numstat` reads `22  0`. Fields copied from `s275-D2`'s shape (`id`, `ruled`, `date`,
   `by`, `says`, `governs`, `evidence`, `status`). `says` carries the export reference
   (`2026-09-17T11:58:34.925Z`, `notes/_lanes/281/orphan-plan/DAVE-EXPORT-DECISIONS-2026-09-17.json`,
   q1 = (a), note empty, recommended (a), overruled false), the question verbatim and the option
   sentence verbatim: *"Yes — families enter as nodes, and both lines go on."* `ruled` names the
   `family:` node kind, the two edge types with their counts, that storage is otherwise untouched,
   that `obeys` and its `held` flag are not touched, and that the `s275-D2` hold — *"inFamily and
   evidencedBy stay OFF, behind flags"* — is lifted by this ruling and by nothing else in it.
   608 rulings, the file parses, `s281-D1` is last.
2. **The edges landed** through the generator's own door, never by hand:
   `python3 knowledge/gen_kg_principles.py --land --ratified s281-D1 --family-edges --evidence-edges`
   → `knowledge/_ux_principle_nodes.json`, 260 nodes / 401 edges (Finding 1 for the split).
3. **Explorer 1.22** — `knowledge/_kg_explorer.template.html`: `family` joins `TYPES2` (the chip),
   `--c-family` joins all three palette blocks, `inFamily:'uxprinciples'` joins `FAMILY`,
   `inFamily:['is in research family','is the research family of']` joins `READ`, and `EFAM` is
   introduced and used in `EON`, `chipF`, `DRGOV`, the stroke colour and the two aside group headers
   (Findings 3 and 4). `knowledge/_build_kg_explorer.py`: `VERSION` → `1.22` with the note in the
   house style, and `family` joins `SRC_BY_TYPE` so INSPECT names the file a family hub was read from.
   `notes/_KG-EXPLORER.html` rebuilt: 4,635 → 4,725 nodes, 8,130 → 8,429 edges.
4. **Proved** — the census re-run at three chip settings, the coordinate md5s, six never-driven
   1280×800 light shots of force-2D, a driven INSPECT pass on both new edge types, `_validate_kg.py`.
   All below.

Files changed: `knowledge/_rulings.json` (span insert, `22  0`) · `knowledge/_ux_principle_nodes.json`
(regenerated by the generator) · `knowledge/_kg_explorer.template.html` ·
`knowledge/_build_kg_explorer.py` · `notes/_KG-EXPLORER.html` (rebuilt) ·
`notes/_lanes/281/principles-home/*` · this report.
`knowledge/gen_kg_principles.py` was **not** edited — it was RUN; its flags already existed and were
waiting on exactly this ruling id. `knowledge/_kg_verbs.json` was **not** edited (Finding 5, and
ruling-shaped question 1). `obeys`, its 14 `held` lines and the `held` flag were **not** touched —
`held (drawn at no setting): 14 · {'obeys': 14}` before and after, same four targets.

## Findings

1. **What landed, counted off the file, not the banner.** `knowledge/_ux_principle_nodes.json`,
   `ratified: "s281-D1"`:
   nodes `{'ux': 145, 'evidence': 53, 'family': 32, 'polarity': 30}` = 260;
   edges `inFamily 145 (0 null) · evidencedBy 134 + 11 null · hasParty 53 + 15 null · tensionWith 22 ·
   touches 9 · resolvedBy 7 · challengedBy 4 · explainedBy 1` = 401, 26 declared nulls.
   The 11 `evidencedBy` nulls are the principles whose `evidence` field carries no URL; each keeps
   the field's own prose, e.g. `ux:pr-von-restorff` → *"PRIMARY NOT FETCHED. Secondary receipt:
   lawsofux.com/ (fetched) 'the one that differs from the rest is most likely to be remembered'"*.
   That is RP-2 option (a) and `s275-D2`'s own rule, unchanged. The file's diff is `2263  147`, and
   the 147 deletions are **exactly** `145 × "family"` + the `$description` and `ratified` header lines
   (`git diff -U0 … | grep '^-' | sed 's/:.*//' | sort | uniq -c` → `145 "family" · 1 "ratified" ·
   1 "$description"`). The fact moved from the attribute to the edge and is carried once, not twice.
   `grade` stayed a field, per `s237-D1`.
2. **The evidence targets land on `evidence:`, a node type that ALREADY HAS A CHIP — and the
   `family:` targets land on one that did not.** Measured, not assumed:
   `ALLTYPES.includes('evidence')` was already `true` (it is in `TYPES2` since v1.1 — the
   Constitution's 900 filed artefacts) and `ALLTYPES.includes('family')` was `false`. So the 53 new
   evidence dots needed no chip and the 32 family hubs needed one, plus a `--c-family` token: a type
   with no `--c-` token paints transparent, and a type with no chip is not drawn at all whatever its
   edges say — lane CM's Finding 2, the defect the brief told this lane not to repeat. Both are in
   now (`type_chips` gained exactly `{'family'}`), and the after census reads
   `node types with no chip at all: NONE` · `homeless edge types: NONE`.
   **The `evidence:` prefix now means two things, and that is Dave's ruling, not an accident.** The
   generator's own docstring flagged it (the #202 vocabulary-collision class): 900 governance
   `evidence:` nodes are repo paths (`evidence:notes/_MEMENTO-DECISIONS.md#…`), the 53 new ones are
   bibliographic URLs (`evidence:https://api.crossref.org/works/10.1037/h0055392`), and **0 of the 53
   match a live one** — measured, `len(live & new) == 0`. They are told apart by their `fam`
   (`governance` vs `uxprinciples`), which is what gates the chip, and by their label, which is the
   receipt itself. Nothing else in the graph changed meaning.
3. **The defect the brief did not name: `evidencedBy` is one type in two families, and `EON` read the
   type.** `const EON=e=>famOn[FAMILY[e.type]]&&…` — `FAMILY.evidencedBy` is `'governance'` and has
   been since v1.2. The 134 new ux→evidence lines carry `fam:'uxprinciples'` on the edge.
   `recount()`'s `SHOWNE` filter is `famOK(e)`, which reads `e.fam`; INSPECT's edge door has read
   `e.fam||FAMILY[e.type]` since 1.21. So the header would have counted the new lines under the
   Explanation chip while the canvas drew them only under the Constitution — the exact
   header-disagrees-with-canvas class 1.16 and 1.21 each had to fix once. `EON` now reads
   `EFAM(e)=e.fam||FAMILY[e.type]`. **MEASURED no-op everywhere else:** across the whole live graph
   the only edges whose `fam` disagrees with `FAMILY[type]` are **11 declared nulls** — 10 asset
   `governedBy` and 1 `defaultActive`, `fam:'assets'`, all `t: null` (probe: the divergence scan in
   `inspect.json`'s `picked.divergent`, and the same scan run against HEAD's page before any change)
   — and a null is drawn at no setting, ever. `chipF`, `DRGOV` and the stroke colour follow the same
   reading so the three cannot disagree; the one visible consequence is that those 11 nulls move from
   the wiring chip's count to the assets chip's, **where `s277-D4`/`s277-D7` authored them**. That is
   a correction of the same kind as lane CM's `EFAMFILE` fix, not a side effect.
4. **A fourth place still read the type map, and the driven pass caught it.** The aside's edge-group
   header takes `fam=FAMILY[t]` and prints `chip off` when `famOn[fam]` is false. First driven pass,
   Explanation chip ON, `ux:pr-fitts`: the `evidencedBy` group's header read
   `evidencedByis · decided1chip off` — while the canvas was drawing that very line. Fixed
   (`fam=EFAM(g[0].e)`; a node's edges of one type share one family) and re-driven: the header now
   reads `evidencedByis · decided1`, no `chip off`. Both strings are in `inspect.json`, scraped out
   of the rendered modal. The rebuild after this fix produced the **same** coordinate md5 and the
   **same** three canvas md5s — it is an aside change, and the pixels prove it.
5. **`inFamily` has no verb, and the page says `unread` with no note.** Driven, `ux:pr-fitts`'s
   groups: `inFamilyunread1`. Lane CM could report that all six of its types already had a verb;
   this one genuinely does not — `knowledge/_kg_verbs.json` has no `inFamily` entry and no `unread`
   note for it, so the badge's title falls back to the generic *"no verb reads this storage type"*.
   The neighbouring `family` EDGE type (component→component, structure family, untouched by this
   lane) reads through *is-a*, which is plainly the same force. Not fixed here: the verbs file is
   `s277-D11`'s and is named in neither `s281-D1`'s `governs` nor the brief's Gates. Ruling-shaped
   question 1. The reading itself is not missing — `READ.inFamily` gives the door and the row their
   sentence, scraped: *"pr-fitts is in research family fam-classic-hci"*.
6. **`evidencedBy`'s verb sentence is now wrong for half its edges.** Scraped from the ux edge door:
   verb `is · decided`, and the verb's own sentence begins *"the ruling end is the decider…"*. On a
   ux→evidence line there is no ruling end. The mechanism to fix it exists and is already used for
   `obeys` (`$splits` in `_kg_verbs.json`, branch by destiny). Same file, same reason as Finding 5 —
   ruling-shaped question 1.
7. **The INSPECT doors read correctly otherwise**, every string scraped from the rendered modal
   (`notes/_lanes/281/principles-home/inspect.json`, page errors `[]`):
   `inFamily` → title `pr-fitts —inFamily→ fam-classic-hci`, read *"pr-fitts is in research family
   fam-classic-hci"*, family `uxprinciples`, provenance *"authored — written in the record itself"*,
   stored in `knowledge/_ux_principle_nodes.json`.
   `evidencedBy` (ux, resolved) → read *"pr-fitts is evidenced by https://api.crossref.org/works/10.1037/h0055392"*,
   family `uxprinciples`, stored in `knowledge/_ux_principle_nodes.json`.
   `evidencedBy` (ux, declared null) → read *"pr-von-restorff is evidenced by — nothing: a declared
   null"* with the register's prose as the note.
   `evidencedBy` (governance, the control) → family `governance`, stored in
   `knowledge/_rulings.json · knowledge/_ruling_edges.json` — unchanged, which is the point of taking
   it.
   A family hub opened directly (`family:fam-laws-of-ux`) shows one group, `inFamilyunread26` — the
   26 Laws-of-UX principles now hanging off their shelf, which is the walk Dave's question asked for.

## The census, before and after

`notes/_lanes/281/principles-home/_recensus.py` — lane CM's copy of lane OC's `measure()`, with one
line tightened: `eon` reads `e.fam || FAMILY[type]`, matching v1.22's own predicate. Same two parsed
readers (the embedded `<script id="kg">`, and `FAMILY`/`famOn`/`TYPES`/`TYPES2` out of the shipped
template), same three settings, same three predicates. The "before" row is HEAD's page **and** HEAD's
template (`_recensus.py`'s third argument), taken before a byte changed.

| setting | visible | dark before | dark after | drawn before | drawn after |
|---|---|---|---|---|---|
| page defaults | 1,050 | 111 | **111** | 1,384 | **1,384** |
| every chip on | 2,451 → 2,536 | 119 | **19** | 4,570 | **4,849** |
| every chip on + Constitution | 4,623 → 4,713 | **108** | **8** | 7,957 | **8,245** |

`dark_everywhere_by_type`: `{'ux': 100, 'logo': 8}` → **`{'logo': 8}`**. The 8 that remain are set 7,
the logo lockups Dave answered `leaf` — not this lane's.
The dot sets this lane owns, degree > 0 at "every chip on": `ux` 145/145 lit (was 45/145) ·
`family` 32/32 · `evidence` (uxprinciples) 53/53. `polarity` 30/30, unchanged.
The **page defaults row does not move at all** — the Explanation chip loads OFF, so the page still
opens as v1.1 plus nothing: 1,050 nodes / 1,642 relations / 21 edge types / 90 declared-unresolved,
before and after, read off the rendered header in both shot sets.

## Coordinates and canvases — the layout MOVED, as the brief said it would

`notes/_lanes/281/principles-home/_coords.py` (lane CM's, unchanged) over all fourteen baked
coordinate sets (`x,y,x3,y3,z3,y2,xf,yf,zf,xo,yo,xs,ys,zs`) plus `plates/rings/shells/bands`:

- before (HEAD's page, `git show HEAD:notes/_KG-EXPLORER.html`): **`5233db6775b35040860600cc73416880`**, 4,635 nodes / 8,130 edges
- after: **`ae09dc26d0f16b6fb3fbd56504e3b118`**, 4,725 nodes / 8,429 edges

It had to move: 85 new dots (32 `family:` + 53 `evidence:`) and 290 new lines enter the same solver,
so every node's x/y is a new solution. The +90 nodes and +299 edges are 85/290 from the landing plus
the ruling record's own citizen — `s281-D1` becomes a `ruling:` node with its `governs` artefacts and
`evidence`, which is what inscribing a ruling has always done. **The after md5 is identical across
two independent rebuilds** (before and after the Finding-4 aside fix), so the layout is deterministic
and this is a move, not a drift.

Canvas md5s, 1280×800 light, force-2D, never driven, served:

| shot | before | after |
|---|---|---|
| page defaults | `6f56320dac575852e127507fee2f0a3f` | `651ba37711ff6b3bb4868622ab0eb41c` |
| `?fam=uxprinciples` | `415d09a73b25e0d2f4335fe60ebe75f5` | `f51a0cb6b5490c6ec073f221ed3c47e5` |
| every chip + Constitution | `28f297ff55e976e76fcb3a999eb2bae5` | `c1229e778c1e7f8bc9e6571e86ed5e8f` |

The single most useful number in that table's neighbourhood: at **`?fam=uxprinciples` alone** — the
Explanation chip and nothing else — the page's own dark count goes **207 → 107**. That is the 100,
lit by the Explanation view on its own, without the Constitution, which is what Dave's "a designer
can walk from Laws of UX to its twenty-six principles" asks for. Header at that setting: 1,221 →
1,306 nodes, 1,734 → 2,024 relations, 27 → 28 edge types.
Page errors `[]` and `Object.keys(localStorage) === ['kg-theme']` in all six shots, before and after —
`kg-theme` is `applyTheme()`'s, written at load since v1.16, not this lane's.

## GATES — one file touched that the brief's list does not name

The brief's Gates name `knowledge/_rulings.json`, `knowledge/_ux_principle_nodes.json`,
`knowledge/_build_kg_explorer.py`, `notes/_KG-EXPLORER.html`, the lane folder and the report.
**`knowledge/_kg_explorer.template.html` is not among them, and this lane changed it** (33 added,
10 removed). It had to: the type chip, the `--c-family` token, the `FAMILY` map, the `READ` map and
`EON` all live in the template — `_build_kg_explorer.py` holds the DATA and the VERSION, the template
holds the PAGE — so Do-3 ("the `family:` node type gets a type chip") is not executable without it,
and lane CM's chip work was in the same file for the same reason. It is named in `s281-D1`'s
`governs`. Declared here rather than done quietly; if the conductor reads that gate strictly, this is
the line to challenge.

Everything else held: no `git stash`, no `gen_kg_edges.py`, no `_build_all.py`, nothing downloaded,
no lock `rm`'d and none was created (`.git/_orphan-locks/` holds 60 entries, the same 60 it held at this lane's first `ls`; `.git/*.lock` is empty), scratch under
`/sessions/nifty-exciting-cerf/mnt/outputs/ph/` only.

## RULING-SHAPED QUESTIONS

1. **`inFamily` has no verb and `evidencedBy`'s verb now lies to half its edges — does
   `knowledge/_kg_verbs.json` get a reading for each?** (Findings 5, 6.) The file is `s277-D11`'s and
   is in neither this ruling's `governs` nor the brief's Gates, so this lane did not touch it.
   Options: (a) `inFamily` joins ***is-a*** (where the `family` edge type already reads) and
   `evidencedBy` gains a `$splits` branch by family — governance keeps *"the ruling end is the
   decider"*, `uxprinciples` reads *"principle s was graded on source t"*; the `obeys` split is the
   precedent and the mechanism is already built. (b) Give each an `unread` note saying why, which is
   a declared gap rather than a reading. (c) Leave both silent. Recommend **(a)**: the force is
   plainly *is-a* for one and plainly not *decided* for the other, and a reading map that misreads is
   worse than one with a declared hole. Price: two entries and one `$splits` block, about twenty
   lines, no rebuild of the layout.
2. **Should the Explanation chip still load OFF?** It does, so the default page is byte-for-byte the
   same picture it was — except the coordinates, which moved. 100 principles that were unreachable
   are now one chip away, but only if you find the chip. Options: (a) as shipped, OFF — the page opens
   as v1.1 and Dave adds a layer, which is `s277-D4`'s standing shape for every additive family;
   (b) ON, because after this ruling the Explanation view is the one view that is finally complete.
   Recommend **(a)**: the default is a standing decision across five families and this lane is not the
   place to reopen it.
3. **The 14 held `obeys`→`ux:` lines are still held — and this ruling moved the ground under lane
   CM's question.** CM asked where an obligation on a UX principle is drawn, with `s277-D8`'s three
   provenances as the obstacle. `s281-D1` has now put 85 new dots into the Explanation view and given
   `evidencedBy` a second family, which makes CM's option (b) — draw them in Explanation, where the
   `ux:` node lives — cheaper than it was when CM priced it, because `EON` now reads an edge's own
   `fam` and those 14 lines could carry one without a new chip. Not decided here, and not touched:
   the flag, the count and the four targets are identical before and after. Recommend the conductor
   re-put CM's question with this price attached.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** the page at **390px** with the new `family` chip. The legend gained one chip row; at
  390 it is a bottom sheet capped at 62% of the stage with `overflow:auto`, so nothing is lost, only
  scrolled — but no 390 shot was taken. Price to prove: one render pass, ~2 min,
  `shots.py` with `width=390,height=844`.
- **UNPROVEN:** the **dark** colour scheme, including the new `--c-family:#F4C2DF` against `#0C0C0C`.
  Every shot in this lane is `color_scheme='light'`, as the brief asked. Price: the same pass with
  `color_scheme='dark'`.
- **UNPROVEN:** the other five cells of the layout matrix (`force-3d`, `strata-2d/3d`,
  `shells-2d/3d`). Their coordinates are in the md5 above and have moved with everything else, so
  their pictures have certainly changed; no shot was taken of them. The brief asked for force-2D.
  Price: `shots.py` with CM's six-cell `CELLS` list, ~4 min.
- **CLAIMED:** the token figure in the header — see the note there. The seat does not hand
  `message.usage` to a lane.
- **DECLARED, not a defect:** the node and edge totals grew by 90 and 299, not by 85 and 290. The
  difference is `s281-D1` itself entering the graph as a `ruling:` node with its `governs` artefacts
  and its `evidence` — inscribing a ruling has always done that, and the count is the proof the
  inscription landed.

## Evidence

`notes/_lanes/281/principles-home/` —
- `_recensus.py` · `facts-before.json` · `facts-after.json` — the census table above, both rows,
  with `watch` blocks for `ux`, `family`, `evidence`, `polarity` at all three settings.
- `_coords.py` · `coords-before.json` · `coords-after.json` — the fourteen baked coordinate sets for
  all 4,635 / 4,725 nodes; the two md5s above. `coords-before.json` is taken from
  `git show HEAD:notes/_KG-EXPLORER.html`, not from a copy left lying in the tree.
- `shots.py` · `shots/shots-before.json` · `shots/shots-after.json` · `shots/*.png` — six
  never-driven 1280×800 light shots (defaults, `?fam=uxprinciples`, every chip + Constitution;
  before and after), served by `knowledge/_serve_explorer.py` on 127.0.0.1, the cell and the chips
  chosen by URL flag and never by a click. Each records the canvas md5, the header strip, drawn
  edges by family and by type, dark dots by type, page errors and `localStorage`.
- `drive.py` · `inspect.json` — the driven INSPECT pass: both new edge types through `openEdge`, a
  resolved line, a declared null and the governance control; `ux:pr-fitts` and `family:fam-laws-of-ux`
  through `openInspect`. Every string scraped from the rendered modal. Page errors `[]`.

REPLAY-THESE: `notes/_lanes/281/principles-home/facts-before.json` + `facts-after.json` (~1.5k tk) ·
`notes/_lanes/281/principles-home/inspect.json` (~2k tk) ·
`notes/_lanes/281/principles-home/shots/shots-after.json` (~1.5k tk)
