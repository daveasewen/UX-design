# LANE EX4 — REPORT — `s280-D2` inscribed, and explorer 1.20: INSPECT opens the ARTEFACT — the file, the render, the edge

#280 · 2026-09-17 · lane EX4 (Opus 5) · Dave's two sentences on 1.19 · **ruling + serve script +
template + builder + one regenerate**; no node id, edge type, file or fam KEY moved, and the template
is proved PICTURE-NEUTRAL against 1.19 to the md5.

## For Dave, in plain prose

**INSPECT now opens the thing, not a note about the thing.** You said you wanted to see any artefact
that exists here, including a render of the actual component snippet — so the modal's third section is
no longer "the file, as text". It is **the artefact**, opened the way its own kind wants to be opened,
behind small tabs. A component opens with **RENDER** already showing: the real snippet, running in the
window, with the same stylesheets the showroom gives it and following this page's light/dark. Beside
it are its snippet's source and its meta record. A snippet does the same. A rule opens its guideline's
markdown with **its own row highlighted and scrolled to**. A ruling opens its record — ruled, says,
governs, evidence. An icon or a logo is **drawn**, at 48 and at 16 px, on a light ground and a dark
one, with its SVG beside it. A session shows what was ruled in it; a filed report renders as the
document it is. Anything with no renderer yet still opens as the raw file, named by its type, so
"nothing built for this yet" never looks like "there is nothing here".

**And the lines are doors too.** Every relation row — in the side panel and inside the modal — now
carries a second small button, **↔**, next to the `i`. The `i` opens the node at the other end; the
**↔** opens *the relation itself*: its storage type, the verb that reads it with **these two ends
named in the sentence**, which family it belongs to and whether that family's chip is on, its note,
its provenance, where it is stored, when it was born — and, when it is one of the declared nulls, the
declaration itself, which is the only place in the system where you can read what a record *claims*
exists but does not. Both ends are buttons, so you walk: component → relation → the ruling at the
other end → that ruling's evidence, without the window ever closing. A **trail** across the top takes
you back a step at a time.

**One thing changes how you open it, and it is the only instruction in this report.** A page opened by
double-clicking it runs on `file://`, and a browser will not let a `file://` page read the file sitting
next to it — not the path, the *scheme*. So none of the above can work from the disk, ever. The repo
now ships a one-line server. From the repo root:

```
python3 knowledge/_serve_explorer.py
```

It prints a URL; open that. It is stdlib only, binds `127.0.0.1` alone, reads and never writes, and
opens no window of its own. Opened from the disk instead, the modal still names every artefact and now
names **that command** as the way to open it.

**What the picture does: nothing.** The template does not move a pixel — proved below by a 2×2, not
claimed: 1.20's template with 1.19's data reproduces 1.19's canvas md5 `716028a2…` exactly. The default
canvas *string* does change, and it changes for one reason: inscribing `s280-D2` (step 0 of this lane's
own brief) adds one ruling, one artefact and three evidence nodes to the Constitution, whose force
layout then re-settles; the Constitution is not drawn at the defaults but its edges are painted as the
faint ghost hatch, and that hatch is what moved. 1.19's template with 1.20's data gives the *same* new
string. The picture is the data's, and the data is your ruling.

Pictures: `notes/_lanes/280/explorer-artefacts/shots/` — `kg-120-component-render-{light,dark}.png`
(the Alert snippet rendering inside the modal), `kg-120-edge-{light,dark}.png`,
`kg-120-ruling-{light,dark}.png`, `kg-120-file-banner-{light,dark}.png` (the same modal from the disk,
naming the serve command), and the two control shots for the md5 gate.

---

## 0. The ruling, inscribed first and on its own

`s280-D2` — THE EXPLORER IS THE FRONT DOOR TO THE WHOLE SYSTEM. Inscribed by
`knowledge/_inscribe_ruling.py`, dry-run then `--write`: a **textual span of 1,724 bytes at offset
832,378**, file 832,383 → 834,107 B, rulings **606 → 607**, *reconstruction proof PASSED (all other
bytes identical)*. `notes/_RULINGS.html` re-rendered by `_render_rulings.py` (607 rulings, 156
sessions, 1,051,552 B) and `--check` reports **FRESH**. `governs`:
`_kg_explorer.template.html`, `_build_kg_explorer.py`, `_serve_explorer.py`. `says` carries both of
Dave's sentences verbatim. Its own commit, `9e04796`, nothing else in it.

## 1. `knowledge/_serve_explorer.py`

Stdlib only; no dependency, no download, no browser opened. `python3 knowledge/_serve_explorer.py`
serves the **repo root** (the parent of `knowledge/`) on a port the OS says is free, binds
`127.0.0.1` alone, answers `GET`/`HEAD` and refuses `POST`/`PUT`/`DELETE` with **405**, sends
`Cache-Control: no-store` so a rebuilt page is never read out of a stale cache, and prints the
explorer's URL and what it is for. `--port N` pins a port; `--print-url-only` prints the URL and
serves nothing (for a driver that starts its own server). If `notes/_KG-EXPLORER.html` is not built it
says so and names the builder, rc 2. Verified by hand: page **200**, `knowledge/canon/type.css`
**200**, `POST /` **405**.

## 2. The artefact section, by kind

The modal is now **record · artefact · relations** (the artefact moved above the relations, because it
is the thing you came for). The section keeps 1.19's path lines with their copy buttons and adds tabs:

| node kind | tabs | what opens |
|---|---|---|
| `component` | **Render** · Snippet source · The meta record | the `renderedBy` snippet live, then its source, then `knowledge/components/{slug}.meta.json` |
| `snippet` | **Render** · Source | the same render, and the file |
| `rule` | **In the guideline** · Where | the guideline `.md` rendered, the `{#rule-id}` block highlighted and scrolled into view |
| `ruling` | The ruling | that one entry out of `_rulings.json` as a definition list (id · ruled · date · by · says · governs · evidence · status) |
| `session` | What was ruled | every ruling whose `ruled` is `#N`, or whose id is `sN-…` |
| `icon` · `logo` | **Drawn** · SVG source | the SVG at 48 and 16 px, on `#FAFAFA` and on `#1A1A1A` (the marks are `currentColor`, so the ink is the ground's) |
| `evidence` | The document | the document it quotes, with its anchor's block highlighted |
| `artefact`, anything else with a path | The file | 1.19's renderer — md lightly, json pretty, everything else mono |
| a directory kind (`axe`, `guideline`, `principle`, `policy`, `standard`) | — | "a directory of files, not one — there is nothing single to fetch" (1.19, unchanged) |

**How the render is made, and why it is the showroom's render and not a lookalike.** The snippet is
fetched as text and handed to a `srcdoc` iframe — which is exactly what `showroom/<slug>.html` does.
A `srcdoc` document has no URL of its own and inherits the **parent's** base URL, so `gen_showroom.py`
rewrites every relative `href`/`src` in the payload before handing it over (`../canon/type.css` →
`../knowledge/canon/type.css`, because the showroom page is one directory deep). `notes/` is one
directory deep too, so the explorer performs **the same rewrite**, and it is the same narrow fix for
the same reason: the anti-false-fix note about `<base href>` breaking every `<use href="#ic-*">` icon
sprite is carried into the template verbatim. Then `html[data-apollo-theme="mono"]` and the body's
`data-theme` are set, the second from the explorer's own theme toggle, and the toggle re-renders any
open frame.

**Nothing is embedded.** Not one byte of any artefact is in the page; every tab fetches from the served
root when it is opened, and a fetch that starts before you move on drops itself.

## 3. Edge inspect, and the trail

Every `.rel` row in the panel, every `.erow` in the modal, and every declared null in both, carries
`↔`. One delegated capture-phase listener handles it, ahead of the node `i` and ahead of the row's own
dig, so pressing it never also digs. The edge modal shows:

* **the two ends**, each a button into its own artefact — or, for a declared null, `nothing · ref:
  null` with the declaration's own words underneath;
* **the record**: storage type · the verb badges (s277-D11) · *this* relation read with both ends
  named · the verb's own direction sentence · the `$splits` note where the type is split by its
  target's kind · the family and a `chip off` note when it is not currently drawn · the note · the
  provenance (`authored` / `derived` / `ratified …` / `at …`) · where the edge is stored · born/gone ·
  and the evidence path when the far end is an `evidence` node.

A **trail** of crumbs sits under the modal's head as soon as you are two steps in; a crumb truncates
the trail and re-opens that step without pushing a new one. The modal never closes while you walk.

## 4. Gate — the template is picture-neutral, proved by a 2×2

Fresh `browser.new_context`, light, 1280 × 800, page defaults, `file://`, `cv.toDataURL()` md5:

| | canvas md5 |
|---|---|
| 1.19 template + 1.19 data (git HEAD's shipped page, `5e3ba3b`) | `716028a29c5a9832f014da5d34d7d141` |
| **1.20 template + 1.19 data** (the same page's data spliced into the new template) | **`716028a29c5a9832f014da5d34d7d141`** |
| 1.19 template + 1.20 data | `30b2ccf32cd31a37807dbc8a7c566e7d` |
| 1.20 template + 1.20 data (shipped) | `30b2ccf32cd31a37807dbc8a7c566e7d` |

Deterministic: the md5 repeats across reloads in fresh contexts (119 twice, 120 three times, same
string each). So **the template contributes nothing to the picture and the data contributes all of
it**, in both directions.

**Why the data moved, exactly.** `s280-D2` adds 5 nodes (`ruling:s280-D2`,
`artefact:knowledge/_serve_explorer.py` and 3 evidence nodes) and 6 edges, all in the `governance`
family, and the build's force pass then re-settles that family: **2,167 governance nodes moved, and 0
base nodes moved** — every base node is byte-equal, id for id, including `deg` and every one of the six
coordinate sets. At the defaults the drawn sets are *identical*: 1,050 nodes and 1,642 edges, node for
node and edge for edge, with the same `x, y, deg, r, a` on every one, and `k` 0.278656, `view.x`
−652.347, `view.y` 6.6395 in both. The picture still differs because `draw()` paints **every** edge,
not only the shown ones — an edge whose family chip is off is drawn at alpha 0.04, the faint hatch
behind the hub — so the 2,167 re-settled Constitution nodes move that ghost layer. Max channel delta
255, 108,669 of 653,976 pixels non-zero, and by eye the two pictures are the same graph with a
different faint weave behind it.

**Declared deviation from the brief.** The brief asked for "default canvas md5 identical to 1.19". It
is not, and it *cannot* be: the same brief's step 0 required inscribing `s280-D2` before the build, and
inscribing any ruling re-settles the Constitution's layout. The gate that survives — and the stronger
statement — is the 2×2 above: the 1.20 template is identical to 1.19 on identical data. The same
applies to "node/edge object identity as EX3 proved": identity holds for every base node and every
drawn node and edge; the 5 nodes and 6 edges the ruling adds are the whole difference, listed by id
above.

## 5. Gate — driven on a SERVED page (`shots/drive-served.json`)

`python3 knowledge/_serve_explorer.py --port 8757`, killed after. Fresh context, 1280 × 900, light,
every modal opened by a real click on a real search row's `i` (never by calling `openInspect`).

| probe | tabs offered | tab open | what the pane holds |
|---|---|---|---|
| `component:alert` | Render · Snippet source · The meta record | **Render** | **1 iframe** |
| … its Snippet source | — | Snippet source | **24,045 chars** |
| … its meta record | — | The meta record | **9,799 chars** (`alert.meta.json`, pretty) |
| `snippet:Alert.reference.html` | Render · Source | **Render** | 1 iframe |
| `rule:aca-001` | In the guideline · Where | In the guideline | **7,482 chars**, `#mdhit` **present** |
| `ruling:s280-D2` | The ruling | The ruling | **1,607 chars** — the record just inscribed |
| `icon:accessibility` | Drawn · SVG source | Drawn | **4 cells** (48 light, 16 light, 48 dark, 16 dark) |
| `artefact:knowledge/_serve_explorer.py` | The file | The file | **4,599 chars** |
| an EDGE from a panel row (`containedBy`) | — | — | **2 ends**, the record |
| an EDGE from inside a node's modal (`appliesTo`) | — | — | 2 ends, the record |

**THE RENDER PROOF, and what it is not.** `document.fonts.check` is not evidence and was not used —
a face can be installed while the stylesheet 404s, which is precisely the silent failure
`gen_showroom.py`'s rebase gate exists to kill. The frame is asked, from the parent, for a **computed
style that only `type.css` can produce**:

```
theme light · data-apollo-theme mono · sandbox "allow-same-origin"
root <svg> in body · 83 elements in the frame's body
link href ../knowledge/canon/type.css   (rebased from ../canon/type.css)
styleSheets: http://127.0.0.1:8757/knowledge/canon/type.css : 57 rules  ·  inline : 37 rules
.t-ed-body  →  line-height 24px        (type.css declares 24px; without the sheet it is `normal`)
```

The dark run gives the same with `theme dark`. **Page errors `[]`, console errors `[]`.**

**The walk.** From a panel `↔` (`containedBy`, Alert → Cards) → a click on an end opened Alert's own
artefact with its Render tab live → **1 crumb** → the crumb returned to the `containedBy` edge, and
`#insp` stayed `on` through all of it. Escape closed it.

## 6. Gate — `file://`, never driven (`shots/drive-file.json`)

Same script, same clicks, page opened from the disk. Every modal opens; the record and the relations
are there; **the artefact section is the banner and the banner names the command**:

> *"this page is open from disk (`file://`), so it can name the artefact but not open it — a browser
> will not let a `file://` page read the file next to it. **Serve the repo** and everything here opens:
> from the repo root run `python3 knowledge/_serve_explorer.py`, then follow the URL it prints."*

**Page errors `[]`, console errors `[]`.** Edge inspect works from the disk too — an edge is a record
the page already carries, so it needs no fetch. The doomed fetch is still never attempted (1.19's rule,
kept): a known outcome is declared, not discovered by writing an unactionable console error.

## 7. Screenshots — `notes/_lanes/280/explorer-artefacts/shots/`

Ten PNG at 1280 (800 for the two controls, 900 for the modal shots), each in a fresh context, colour
scheme emulated, `localStorage` `['kg-theme']` and page errors `[]` on every one (`shots.json` carries
each one's measurements, including the frame's theme and its `.t-ed-body` line-height).

What I saw by eye. **component-render** — the Alert component's four callouts (error, warning, success,
information) sitting inside the modal in their real type and their real colours, under the line *"the
snippet itself, rendered the way the showroom renders it"*, with `RENDER · SNIPPET SOURCE · THE META
RECORD` above them and the relations section visible below. Dark reads as well as light and the
snippet follows the page. **edge** — `RELATION · containedBy · Alert —containedBy→ Cards`, the two ends
as boxes with their types under them, and the record beneath: *"s→t reads as: s contains t / is built
from / drives / hands off to t; containedBy runs the other way — t contains s"*, family `structure`,
stored in `knowledge/components/alert.meta.json`, born 2026-08-08. **ruling** — `s280-D2`'s record,
`says` carrying both of Dave's sentences. **file-banner** — the same component modal from the disk,
with the serve command in the banner where the tabs would be.

## 8. Gates run

* `node --check` on the template's extracted script before every build.
* `python3 knowledge/_validate_kg.py` → rc **0**.
* `python3 knowledge/_validate_lane_ownership.py` → "LANE OWNERSHIP: OK … (this is #280)".
* `notes/_KG-EXPLORER.html` regenerated ONLY by `python3 knowledge/_build_kg_explorer.py`.
  4,056,963 B → **4,081,945 B** (+24,982 B, all template — CSS and script). No artefact contents are
  embedded; the `src` and `verbs` build-time blocks are 1.19's, unchanged.
* Disk: `/sessions` at 99% throughout. Nothing downloaded, `knowledge/` never copied; Chromium from
  `knowledge/_render/seat_env.sh` only. Scratch lived in `/sessions/…/mnt/outputs/ex4/` (the 1.19
  control page, the two spliced hybrids and the extracted template script) and is removed at the end.
  The served runs used `_serve_explorer.py` on scratch ports 8741 and 8752–8757, each killed after.

## 9. Not done, or done differently, with size

1. **The default canvas md5 differs from 1.19** — §4, declared, with the 2×2 that isolates the cause to
   the ruling the brief's own step 0 required. Nothing to fix; the alternative would be not inscribing.
2. **The snippet's own scripts are cut out of the render, not merely blocked.** The frame is
   `sandbox="allow-same-origin"` without `allow-scripts` — same-origin is kept so the page and a driver
   can read the frame's computed styles, which is what makes the type proof possible. Left in place,
   each blocked script wrote a console error per render (6 of them, measured), so the `<script>` blocks
   are stripped from the payload before it is handed over. **Consequence, stated plainly:** a snippet
   whose *content* is produced by script — the animated data-visualisation snippets are the candidates
   — will render its static markup, not its scripted result. Allowing scripts would mean dropping
   `allow-same-origin` (they cannot both be set without defeating the sandbox), which would cost the
   type proof. ~10 lines to add a "run its scripts" button that swaps the sandbox and declares the
   trade, if Dave wants the animated ones live.
3. **`guideline:` nodes are WCAG guideline NUMBERS** (`guideline:1.1`), not the markdown guidelines.
   They have no file of their own and fall in 1.19's directory-kind branch. The guideline markdown IS
   opened — through the `rule:` nodes that live in it, with the rule's own row highlighted. There is no
   "token group" node type in the graph at all (the nearest is `iconGroup`, which has no file); both
   are declared OUT rather than faked.
4. **107 of the 470 `rule:` nodes carry no `file`** (`rule:ctkb-002` is one) because the node was
   created by another record's reference before its own was read, and `add()` keeps the first label.
   Those fall back to `_rule_nodes.json` — correct but unhelpful, and capped at 180,000 chars. A
   build-time join would fix it for all of them (~6 lines in `src_block`).
5. **A ruling's tab parses the whole 834 KB `_rulings.json` to find one entry.** It is one fetch, it
   is not cached between opens, and it takes about a second. A build-time `{id: byteOffset}` map would
   make it a range request (~15 lines); not done, because a second is not a defect yet.
6. **The markdown renderer is still 1.19's light one** — headings, lists, `code`, `**bold**`,
   paragraphs, now block-wrapped so one block can be marked. No tables, no links, no nested lists.
7. **No deep link.** There is still no `?inspect=<id>` / `?edge=<k>` flag, so a modal cannot be
   photographed never-driven. ~6 lines if a never-driven shot of one is ever wanted.
8. **The provenance row reads `—` on the edges that carry no provenance keys at all** (the base
   families store none). Shown rather than hidden, so the absence is visible.

## 10. Shipped

* `9e04796` — **`s280-D2`** inscribed, on its own, with `notes/_RULINGS.html` re-rendered.
* (this lane's second commit) — explorer **1.20**: `knowledge/_serve_explorer.py`, the template's
  artefact section with its tabs and its four renderers, edge inspect and the trail, the builder's
  VERSION, the regenerated page, this report, its `_subreports` copy, `shots/` (10 PNG + `shots.json`
  + `drive-served.json` + `drive-file.json`), the driver and the shot script, and the store row
  **W-280ea**. `_validate_kg.py` rc 0; `_validate_lane_ownership.py` "LANE OWNERSHIP: OK". Nothing
  pushed.
