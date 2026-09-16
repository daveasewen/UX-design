# LANE LY — REPORT — explorer 1.17: the graph laid out as three visible layers, one option on a page
#280 · 2026-09-16 · lane LY (Opus 5) · **this lane renders, it does not rule** — the page asks Dave one question and the switch defaults to 1.16's behaviour until he answers it.

## For Dave, in plain prose

You said the last round did not look like three layers — that relabelling and grouping the chips
was not what you expected. So this round changes the layout, not the labels. The explorer now has a
second way of standing the graph up, called **strata**: one stage, three horizontal bands top to
bottom — **Explanation**, then **Design governance**, then **System** — with **The Constitution** as
a fourth band beneath System, the bedrock, dimmed, and drawn only when its chip is on. Each band has
its name at its left edge in the band's own colour, a hairline at its boundaries, and a 4% tint, so
the layers read as layers before a single node is read.

Nothing moved sideways. Every node keeps the exact x the force layout gave it, so the clusters and
the family columns are exactly where they were; all that changed is the vertical, where each node is
now packed inside its own view's band by a light force. Lines that cross a band boundary are drawn
brighter and a touch heavier than lines that stay inside a layer, because the crossings are what the
picture is for — with the Constitution switched on you get a thick red bundle running from the
ruling record up into the components that cite it.

**The default is unchanged.** The page still opens in the old force layout, pixel for pixel: the
canvas of 1.16 and the canvas of 1.17-in-force are identical at the page defaults (§4). Strata is a
switch in the tool row, `LAYOUT: force · strata`, and `?layout=strata` in the URL. The one question
on the option page is whether it should stay a switch or become the default.

**The page for you:** `notes/_lanes/280/layout/OPTION-strata-2026-09-16.html` — the two layouts side
by side in light and dark, strata with the assets layer on, strata with the Constitution on, all
four layers at once, the band table, and one radio with a note field and an export button.

## 1. What was built

| Where | What |
|---|---|
| `knowledge/_build_kg_explorer.py` | `strata()` + `pack_y()` — every node gains **`view`** (its band, from the fam→view map the page already carries in `VIEWS`) and **`y2`** (its y inside that band). `x`, `y`, `x3`, `y3`, `z3` are not touched. The four bands and their y-bounds are written into the data as `bands`. VERSION → **1.17**. |
| `knowledge/_kg_explorer.template.html` | `LAYOUT` (`force` default, `?layout=strata` or the tool-row switch), `BY(n)` and a one-word change to `base()` so the 2D layout reads whichever y-set is live; `drawBands()`; strata's edge weighting; `fit()` fits the band stack in strata; the legend takes the bottom strip in strata; `?fam=…` to switch family chips on before the first paint, so a layer can be photographed never-driven. |
| `notes/_KG-EXPLORER.html` | regenerated the module's own way — `python3 knowledge/_build_kg_explorer.py`. |
| `notes/_lanes/280/layout/` | `shots.py` (the screenshots + the band gate), `drive_strata.py` (the interaction gate), `_build_option.py` → `OPTION-strata-2026-09-16.html`, `shots/` (10 PNG + `shots.json` + `drive.json`). |

**The band rule, stated plainly.** A node's band is its view: `structure`/`usage`/`render`/`rules`/
`assets` → System, `guidelines`/`guidelinerules` → Design governance, `uxprinciples` → Explanation,
`governance` → The Constitution. Base nodes carry no `fam` and are **System** — including the
`ruling:` nodes a component meta points at directly, which are part of the base graph and stay in
the base's band. That is the map the page already had; this lane did not invent a second one.

**How the packing works.** x is frozen. Within a band, y is relaxed for 140 iterations under two
forces — collide (two nodes closer than 2r are pushed apart along y by exactly the distance their
frozen dx still owes) and a weak pull to the band centre (`y *= 0.992` per iteration). The collide
radius is calibrated per band, twice, so the pack fills the band instead of over- or under-flowing
it, and a final scale guarantees the invariant the gate tests: no node leaves its own band.

## 2. `git diff --numstat` on the two source files

```
86  2  knowledge/_build_kg_explorer.py
57  4  knowledge/_kg_explorer.template.html
```
(against `5cc3ecd`, HEAD at lane start; one added/one deleted line of each is the VERSION or a
comment line.)

## 3. The 1.16 control, and a finding that is not mine

`knowledge/_rulings.json` and `knowledge/_icon_nodes.json` both moved **during** this lane —
`_rulings.json` gained `s279-D1` since the shipped 1.16 was built, and **#280 lane IN inscribed
Dave's nine `defaultActive` answers into `_icon_nodes.json` at 20:14**, turning nine declared nulls
into resolved (undrawn) edges. Either would make a naive "1.16 file vs 1.17 file" diff read as if
this lane had moved things. So the control is a **like-for-like rebuild**: HEAD's builder
(`git show HEAD:knowledge/_build_kg_explorer.py`, byte-identical to the one that built the shipped
1.16) run against **today's** data, with only its ROOT redirected. That control is what §4 compares
against. Nothing was stashed and nothing in `knowledge/` was edited to produce it.

## 4. Gate — EX2 §3's method, re-implemented, 1.16 control vs 1.17

`sim.py` re-implements `famOK` / `NODEON` / `EON` / `DRON` / `DR` / `DRGOV` / `recount` / the draw
predicate in Python over the two pages' embedded `KG` JSON.

| chips | nodes | relations | edge types | nulls | DR chip | drawn-node set | drawn-edge set | x,y of every drawn node | x3,y3,z3,deg |
|---|---|---|---|---|---|---|---|---|---|
| page defaults | 1050 = 1050 | 1,642 = 1,642 | 16 = 16 | 90 = 90 | 28 = 28 | 1001, same set | 1,175, same set | **0 moved** | **0 moved** |
| + assets | 1738 = 1738 | 2,950 = 2,950 | 22 = 22 | 111 = 111 | 28 = 28 | 1689, same set | 2,462, same set | **0 moved** | **0 moved** |
| + Constitution | 3210 = 3210 | 4,903 = 4,903 | 31 = 31 | 90 = 90 | 323 = 323 | 3161, same set | 4,425, same set | **0 moved** | **0 moved** |
| every chip on | 4611 = 4611 | 8,084 = 8,084 | 53 = 53 | 126 = 126 | 331 = 331 | 4562, same set | 7,528, same set | **0 moved** | **0 moved** |

The same run against the **shipped** 1.16 page (copied from HEAD before any build) is also identical
at page defaults and with assets on — it differs only with the Constitution on, by the `s279-D1`
ruling and the four nodes that came with it, which is §3's finding, not this lane's.

**Canvas identity.** Stronger than the data gate: the 1.16 control page and the 1.17 page, both at
page defaults, both light, both 1280×800, in fresh contexts — `cv.toDataURL()` md5
**`cd4dc2198d…` = `cd4dc2198d…`**, the same pixels. The shipped default of 1.17 is 1.16.

## 5. Gate — the band invariant, and everything else still working

`drive_strata.py`, two fresh contexts:

* **Never driven**, `?layout=strata`: of **4,623** nodes, **0** have no band, **0** sit at a y other
  than their own `y2`, and **0** lie outside their band's `[y0, y1]`. The same check runs inside
  every strata screenshot context (`shots.json` → `outOfBand`): **0** in all seven.
* **Driven**: opens as `force` → switch → strata (invariant holds) → the legend is the bottom strip
  → dig **Button** (62 relations, 10 sectors, panel renders) → Escape (invariant holds) → scrub 12
  days back (`871 nodes · 1,137 relations · 78 unresolved`) and home (`1050 · 1,552 · 88`) → the
  Constitution chip on (header `3210 nodes · 4,903 relations · 31 edge types · 137 components · 90
  declared, unresolved`; its band appears at y `942.4…1702.4`; invariant holds) → off → search
  "button" → fly → dig → Escape → switch back to force, where **every node is back at its `oy`**
  and the legend is back in its 1.16 place. **Page errors `[]`.**

## 6. The bands, as built

| Band | Nodes | y from | y to |
|---|---|---|---|
| Explanation | 171 | −1702.4 | −942.4 |
| Design governance | 542 | −820.8 | −60.8 |
| System | 1750 | 60.8 | 820.8 |
| The Constitution | 2160 | 942.4 | 1702.4 |

(Node counts include the dead nodes the scrub can show; the drawn counts are §4's.)

## 7. Screenshots — `notes/_lanes/280/layout/shots/`

Ten PNG at 1280×800, each in a **fresh `browser.new_context`**, colour scheme emulated, the layer
selected by **URL flag** rather than by a click, `Object.keys(localStorage) == ['kg-theme']` and
page errors `[]` in every one; `shots.json` carries each shot's fit scale, header line, canvas md5,
band check and byte size. `kg-116-force-{light,dark}` · `kg-117-strata-{light,dark}` ·
`kg-117-strata-assets-{light,dark}` · `kg-117-strata-const-{light,dark}` ·
`kg-117-strata-all-light` · `kg-117-force-light` (the identity control).

What I saw, by eye. **Strata at page defaults** — three bands fill the stage, EXPLANATION and DESIGN
GOVERNANCE empty (their chips are off, which is the truth and reads as it), SYSTEM carrying the red
component hub; the legend is the bottom strip so the stack gets the full width. **Strata with the
Constitution** — the fourth band appears below System with its own dimmed tint, the ruling cloud
sits in it, and a heavy red bundle of citation edges runs up across the boundary into the
components. That bundle is the picture the ruling asked for. **Every layer on** — four bands, the
UX plum at the top, the green rule column and the amber SCs in the middle, the red base and the teal
assets in System, the black ruling cloud at the bottom, and every cross-layer line legible.
**Dark** — the tints hold; the band labels stay readable.

## 8. Not done, or done differently, with size

1. **The switch snaps, it does not tween.** Positions are set straight to the new set and the stage
   re-fits. A tween would fit mid-flight and make a screenshot non-deterministic. ~10 lines to add a
   tween that fits on settle, if it is wanted.
2. **The ghost layer is dropped in strata.** 1.16 draws an edge to a switched-off family at alpha
   0.04 — a faint halo round the hub in force, but across a stack of bands it is a long diagonal
   smear over every layer that reads as traffic which is not in fact drawn. In strata those edges
   fall below the draw threshold. In force they are untouched.
3. **The wide-band gap from EX2 §7.1 is still there** and now shows as horizontal emptiness in the
   all-layers picture: the off families still hold their slots on the x axis, and this lane keeps
   the builder's x by brief. That fix is still the runtime column-packing lane EX2 sized.
4. **3D is force only.** `?layout=strata` with the 3D button pressed shows the 3D cloud; the bands
   are a 2D idea and are not painted there. Declared, not hidden.
5. **Equal band heights.** Explanation (171 nodes) gets the same 760 world units as System (1,750),
   so its band is sparse. Sizing bands to their content is ~6 lines in `strata()` if Dave prefers it.

## 9. Gates run

* `node --check` on the template's script, before every build (it caught one `//` comment that would
  have swallowed the rest of the `renderLegend` line — the exact trap EX2 §6 recorded).
* `python3 knowledge/_validate_kg.py` and `python3 knowledge/_validate_lane_ownership.py` — results
  appended below with the shipped sha.
* Disk: `/sessions` was at 99% throughout. Nothing was downloaded; scratch lived under
  `/sessions/…/outputs/ly/` and is removed at the end. One mistake is recorded honestly: a
  `cp -r knowledge` into that scratch dir put 2.9 GB on the mount for about four minutes before it
  was deleted; the control build was then done without any copy.
