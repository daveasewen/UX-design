# LANE EX3 — REPORT — explorer 1.19: the legend stays put, and INSPECT opens the record in a modal

#280 · 2026-09-17 · lane EX3 (Opus 5) · Dave's two sentences on 1.18 · **template + builder + one
regenerate**; no node id, edge type, file or fam KEY moved, and the default canvas is 1.18 to the md5.

## For Dave, in plain prose

**The legend does not move by itself any more.** You said it jumps from the side to the bottom when
you interact with it, and it did: since 1.16 the page recomputed where the legend belonged on *every*
redraw, so the moment a family chip made the graph wide, the legend threw itself from the right
column to the bottom strip while your hand was still on the chip. Now its place is yours. It is
chosen once when the page opens, and after that it stays there — a chip, a dig, a scrub, a search, a
fold, nothing moves it. Next to `HIDE LEGEND` there is a small `⇣ BOTTOM` / `⇥ SIDE` button, and that
is the only thing that moves it. The page remembers which you chose, so it opens there next time.

**Every row now has an `i`, and it opens the record.** A search hit, a neighbour in the dig panel, a
step of a path — each carries a small `i` at its right edge, and pressing `i` on the keyboard inspects
whatever you have dug. It opens a window over the page with three things: **the record** (every field
the graph stores for that node, written out as a list, not as JSON), **the relations** (grouped by
type and read back in the verbs' own words — *"s→t reads as: t must satisfy s"*), and **the file** —
the path the record was read from, with the file's own contents in the window.

**One honest limit, and the page says it out loud.** A browser will not let a page opened straight off
the disk read a file next to it. So when you open `notes/_KG-EXPLORER.html` by double-clicking it, the
File section names the path, gives you a copy button, and says *"this page is open from disk, so it
can name the file but not read it."* Serve the folder — any tiny web server — and the file itself is
right there in the window. Nothing is embedded in the page; it is fetched when you ask for it.

**The page still opens exactly as it did.** Force · 2D at the defaults, canvas md5
`716028a29c5a9832f014da5d34d7d141` — the same string lane LM recorded for 1.18 and lane LY for 1.17.

Pictures: `notes/_lanes/280/explorer-ux/shots/` — `kg-119-legend-side-{light,dark}.png`,
`kg-119-legend-bottom-{light,dark}.png`, `kg-119-modal-served-{light,dark}.png` (the file's contents
in the modal) and `kg-119-modal-file-{light,dark}.png` (the same modal from `file://`).

---

## 1. The legend's place

| | 1.16 – 1.18 | 1.19 |
|---|---|---|
| when the place is decided | **every `renderLegend()`** — a chip toggle, a dig, a search, a dimension switch, a fold | **at load, and at a layout or dimension switch only** |
| what decides it | `NEWFAM.some(f=>famOn[f]) \|\| LAYOUT!=='force'` — a *rule about the chips*, not about the picture | the shown extent's own shape, asked of `fit()`'s numbers |
| what the user can do | nothing; it moved under the hand | `⇥ side / ⇣ bottom` in the legend's bar, remembered in `localStorage` under `kg-legend` |
| after the user has chosen | — | the automatic choice never runs again, in any cell |

`fit()` is unchanged; it still reads `usable()` from wherever the legend actually is, so the graph is
fitted into the free rectangle the legend leaves in either place. The phone sheet is untouched: under
900 px the legend is still the bottom sheet, closed to one bar, and the place toggle is not offered.

**How "portrait or landscape" is decided, exactly.** The brief's rule is *side when the shown extent
is portrait, bottom when landscape*. That question is only meaningful against this stage (879 × 744 at
1280), so it is asked exactly: the extent is measured once — the live cell's own coordinates **and its
furniture**, through the same `extent()` that `fit()` uses — and then the free rectangle each of the
two places would leave is measured from the live DOM, and the place that shows the graph LARGER wins.
A side column leaves a tall narrow rectangle and a bottom strip a wide short one, so this *is* the
portrait/landscape rule, with the stage's own proportions in it. A near-square picture on a stage
wider than it is tall therefore counts as portrait, which is right: measured, side beats bottom there.

Two things fell out of asking it exactly rather than by the old chip rule:

* **The furniture counts.** In strata-2D the nodes span 1,207 × 759 — landscape — but the *bands* span
  1,207 × 2,523, because an empty band is still a band and `fit()` already fits the bands. The picture
  is portrait. 1.18 put the legend at the bottom there and fitted the stack at **k 0.1126**; 1.19 puts
  it at the side and fits it at **k 0.2208** — twice the picture.
* **1.18's blanket "every layout but force takes the strip" was the worse choice in four of the six
  cells.** Measured at 1280 × 800, `k` with the automatic place vs `k` after one click on the toggle:

| cell / flag | extent | automatic | k | the other place | k |
|---|---|---|---|---|---|
| (defaults) force-2D | 1207 × 1999 | side | **0.2787** | bottom | 0.1421 |
| `?dim=3d` | 654 × 2000 | side | **0.2399** | bottom | 0.1223 |
| `?fam=assets` | 8511 × 1999 | bottom | **0.0872** | side | 0.0400 |
| `?fam=assets,governance` | 10596 × 1999 | bottom | **0.0700** | side | 0.0321 |
| `?layout=strata` | 1207 × 2523 | side | **0.2208** | bottom | 0.1126 |
| `?layout=strata&dim=3d` | 1500 × 1240 | side | **0.1953** | bottom | 0.1631 |
| `?layout=shells` | 2720 × 2720 | side | **0.1250** | bottom | 0.1044 |
| `?layout=shells&dim=3d` | 2640 × 2640 | side | **0.1110** | bottom | 0.0927 |

In all eight the automatic place is the larger picture. The default (force-2D, legend at the side) is
what 1.16–1.18 already did, which is why the canvas is identical.

**Cost, declared.** `extent()` is lifted out of `fit()` verbatim — only the braces moved — so the two
ask the same question of the same numbers. `autoPlace()` toggles the legend's `strip` class twice to
measure both free rectangles from the live DOM; that is two forced reflows, and it happens at load and
at a layout/dimension switch, never in a frame.

## 2. INSPECT

**Where the affordance is.** `.hit` (search), `.rel[data-id]` (the dig panel's group rows) and
`.path .steps .pstep` (a step of the shortest path) each gained a `<button class="insp" data-insp>`.
One delegated listener, in the CAPTURE phase at `document`, handles all of them and stops the event,
so a row's `i` never also digs the row. `i` on the keyboard inspects the dug node (ignored while the
caret is in the search box or a modal is open). The panel's `declared, unresolved` rows get no button:
they name no node.

**What the modal shows.**

1. **The record.** Every field the embedded KG carries for the node, as a `<dl>`. The page's own
   runtime fields (`ox`, `tx`, `a`, `bd`, `_sx`…) are not part of the record and are left out; the six
   baked coordinate sets collapse to ONE row — `force 2D … · force 3D … · strata 2D … · strata 3D … ·
   shells 2D … · shells 3D …` — because they are data, not reading matter. `born`/`died` are shown as
   their snapshot's date. A component gives 7 rows, a rule 11, an `sc` 12.
2. **The relations**, grouped by storage type, each group carrying the verb badges from
   `knowledge/_kg_verbs.json` (s277-D11 — a reading map, storage untouched: `must · must`,
   `is · decided`, `unread`), the verb's own `direction` sentence, the `$splits` note where a type is
   split by its target's kind, the READ direction phrase per row, the edge's `note`, its `derived` and
   `ratified` tags, and a `chip off` badge where that family is not currently drawn. Declared nulls get
   their own group. Every neighbour row carries its own `i`, so the modal walks.
3. **The file.** The path the builder read the record from, plus the node's own declared `file` where
   it has one, each with a copy button; then the file itself.

**Where the paths come from** — two new BUILD-TIME blocks, 13 KB of the 4.06 MB page, and no file
contents (the size is a gate; nothing is embedded):

* `src` — `byType` (`component` → `knowledge/components/{slug}.meta.json`, `snippet` →
  `knowledge/snippets/{slug}`, `ruling`/`session` → `knowledge/_rulings.json`, and so on), `fileRoot`
  (a rule's `file` is under `knowledge/guidelines/`, an icon's under `knowledge/assets/icons/`, a
  logo's under `knowledge/`), `dirs` (`axe`/`guideline`/`principle`/`policy`/`standard` come from a
  DIRECTORY of files — the path is shown and nothing is fetched) and `byId`, the 55 `sc:` → rule-file
  joins only the builder can make. An `artefact` IS its path; an `evidence` node names its document
  and its anchor.
* `verbs` — the twelve verbs as `{of: type→verb(s), verbs: {force, reads}, splits, unread}`.

**The fetch, and its honest failure.** A `file://` page cannot fetch a sibling — the browser refuses
the scheme. That is a known outcome, not one worth discovering by making a request that only writes a
console error nobody can act on, so the modal says it straight and shows the path. Served, the fetch
is made for real: `.md` renders lightly (headings, lists, `code`, **bold**), `.json` is parsed and
pretty-printed, everything else is mono as stored, capped at 180,000 characters with the cap declared.
A 404 or a refusal lands in the same place with the reason named. **Declared deviation from the
brief:** the brief said *"try the fetch; if it fails…"*; from `file://` the doomed request is not made,
because making it is what puts an unactionable error in the console. Served, it is made for real and
the failure branch is proved by a real 404 (§4).

**The modal's manners.** Escape closes it and does NOT surface the dig (the page's own Escape handler
steps aside while the modal is open, and the modal's handler stops the event); a click on the veil
closes it; focus moves to `Close · esc` on open, is trapped by a Tab/Shift-Tab wrap while open, and
returns to whatever had it. Opening from a search row closes the search dropdown, so nothing hangs
over the page.

## 3. Gate — the default canvas is 1.18, to the md5

Fresh `browser.new_context`, light, 1280 × 800, page defaults, `file://`, both pages:

| | canvas md5 |
|---|---|
| 1.18 — git HEAD's shipped `notes/_KG-EXPLORER.html` (`94204dc`) | `716028a29c5a9832f014da5d34d7d141` |
| 1.19 | `716028a29c5a9832f014da5d34d7d141` |

`k` 0.2787 in both. The legend's bar is 5 px taller (the extra button) and the fit is unchanged.

**Identity of the data, stronger than a sim.** Lane LY's method re-implements the page's draw predicate
to prove the drawn sets match. Here that is unnecessary and a weaker statement than the one available:
the two pages' node records are **equal object for object** (4,630 of 4,630, every field including
`x, y, x3, y3, z3, y2, xf, yf, zf, xo, yo, xs, ys, zs, deg, born, died, view`), the edge list is
**identical element for element** (8,124), and `bands`, `plates`, `rings`, `shells`, `islands`,
`orphans`, `snaps` and `extra` are equal. The only difference in the embedded JSON is the two added
keys, `src` and `verbs`. Identical inputs through unchanged draw code cannot produce a different
drawn set, and the md5 above is the picture agreeing.

## 4. Gate — driven, twice (`shots/drive-file.json`, `shots/drive-served.json`)

Each run: a fresh context, 1280, light; the legend measured after every move; then INSPECT from each
of the three row kinds.

**The legend stays put.** `load → chip:assets → chip:governance → chip:uxprinciples → dig
(component:button) → scrub −12 days → scrub home → search "button"` — the legend's bounding rect is
**(419, 116, 440, 543) at all eight steps**, in both runs. Then `⇥/⇣` → **side → bottom, the rect
moves**. Then a reload in the SAME context → **place `bottom`, `localStorage` `['kg-legend',
'kg-theme']`**. Then a chip toggle after the reload → rect unchanged; then a layout switch → the
chosen place kept.

**INSPECT.** Opened from a search row, a dig row, a path row and the `i` key; each time three sections,
the record rows, the edge groups, the File section, focus inside the modal. Closed by Escape in all
three cases and by a click on the veil; the dig underneath survived (`focus` still `component:button`).

| probe | served: File section | `file://`: File section |
|---|---|---|
| search row → `component:button` | `knowledge/components/button.meta.json`, **18,737 chars rendered** | the path + copy button + the disk sentence |
| dig row → `component:badge` | `knowledge/components/badge.meta.json`, **6,565 chars** | same |
| path step → `component:button` | 18,737 chars | same |
| `i` key on the dug node | 18,737 chars | same |
| a `rule:` node (a markdown record) | `knowledge/_rule_nodes.json` + `knowledge/guidelines/accessibility-content-authoring.md`, **7,482 chars rendered as markdown** | both paths, both copy buttons |
| an `axe:` node (a directory) | *"a directory of files, not one — there is nothing single to fetch"* | same |
| **a real 404** (a rule's `file` pointed at a name that does not exist) | *"the file could not be read (the server answered 404) — open it from the repo; the path is above."* | n/a |

**Page errors `[]` in both runs, and console errors `[]` from `file://`.** The served run's only console
line is the 404 the driver itself asks for.

## 5. Gate — the modal is the same in all six cells and both themes (`shots/cells.json`)

Twelve fresh contexts, the cell chosen by URL flag, the modal opened by a real click on a dig row:
**3 sections, 7 record rows, 21 edge rows, 16 verb badges, closes on Escape, page errors `[]`,
console `[]`, `localStorage == ['kg-theme']` in every one.** At 390 × 844: the legend is still the
closed bottom sheet at `(12, 425, 366, 24)` reading `1050 nodes · 1,642 relations · 16 edge types`, the
place toggle is **not** offered, and the modal opens full-width (374 px) with the same three sections.

## 6. Screenshots — `notes/_lanes/280/explorer-ux/shots/` (`shots.json` carries each one's measurements)

Eight at 1280 × 800, each in a fresh `browser.new_context`, colour scheme emulated, page errors `[]`
and `Object.keys(localStorage)` recorded — `['kg-theme']` for the six never-driven ones,
`['kg-legend','kg-theme']` for the two the toggle was clicked in (which is the point of those two).
Plus `kg-118-control-light.png`, the 1.18 control for §3.

What I saw, by eye. **legend-side** — the page as it opens: the red hub down the left, the legend the
right column, and its bar now reads `HIDE LEGEND ▾ · ⇣ BOTTOM · 1050 nodes · 1,642 relations · 16 edge
types`; the hint under the graph has gained its third line, *"any row's **i** — or the i key — opens
its record"*. **legend-bottom** — one click later, the legend is the bottom strip (the 1.15/1.18 place,
views in a row, type rows beneath), its button now offering `⇥ SIDE`, and the graph re-fitted above it;
dark reads as well as light. **modal-served** — Badge's record over the page, the FILE heading, the
path with `COPY PATH`, *"the record the builder read this node from"*, and `badge.meta.json` itself
pretty-printed below it; behind the modal you can see the `i` down the right edge of every panel row.
**modal-file** — the same modal from the disk, the relations reading *"s→t reads as: t must satisfy s
— sc s applies to component t (appliesTo); component s must obey BLOCKING rule t (obeys, branch)…"*
under `governs`, and the File section naming the path and saying it cannot read it.

## 7. Gates run

* `node --check` on the template's script before every build (five times).
* `python3 knowledge/_validate_kg.py` → rc **0**.
* `python3 knowledge/_validate_lane_ownership.py` → "LANE OWNERSHIP: OK … (this is #280)".
* `notes/_KG-EXPLORER.html` regenerated ONLY by `python3 knowledge/_build_kg_explorer.py`.
  4,020,981 B → **4,056,963 B** (+35,982 B: the `src` + `verbs` blocks are 13,012 B of it, the rest is
  the template's own new CSS and script). No file contents are embedded.
* Disk: `/sessions` at 99% throughout. Nothing downloaded, `knowledge/` never copied; Chromium from
  `knowledge/_render/seat_env.sh` only. Scratch lived in `/sessions/…/mnt/outputs/ex3/` (the 1.18
  control page + the extracted template script) and is removed at the end. The served runs used
  `python3 -m http.server` on scratch ports 8731–8736, bound to 127.0.0.1, killed after each.

## 8. Not done, or done differently, with size

1. **The `file://` fetch is not attempted** (§2, declared). ~2 lines to attempt it anyway, at the cost
   of an unactionable console error per inspect.
2. **The record's coordinates are one row, not six.** A reader who wants the raw six has them in the
   page's JSON; the modal is for reading.
3. **The relations list is NOT gated by the chips.** The modal is the record, so it lists every edge
   the node has and marks the families whose chip is off with a `chip off` badge, rather than hiding
   them the way the dig panel does. If Dave would rather it matched the panel, that is one predicate.
4. **The markdown rendering is light** — headings, lists, `code`, **bold**, paragraphs. No tables, no
   links, no nested lists; a table renders as its pipe-separated source lines. ~15 lines each if wanted.
5. **A node with no stored path shows none.** `role:`, `intent:` and `shape:` nodes are created by
   another component's `ref` and have no record file of their own; their File section says so. Giving
   them their referring meta's path is a join the builder could make (~10 lines).
6. **The modal does not deep-link.** There is no `?inspect=<id>` flag, so a modal cannot be
   photographed never-driven the way a cell can. ~4 lines plus a gate if a shot of it is ever wanted
   without a click.
7. **The legend's automatic place is not recomputed on a window resize.** Resizing the window re-fits
   the graph but leaves the legend where it is — which is the sticky rule, and is what Dave asked for;
   noted because it is the one moment where "the picture changed shape" and the place does not follow.

## 9. Shipped

The sha is appended below.
