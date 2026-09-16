# LANE EX — REPORT — the explorer 1.15: three views by force, the Constitution named, the `assets` chip OFF
#279 · 2026-09-16 · enacting `s277-D8` (relabel) + the explorer half of `s277-D4` (assets chip) · `s274-D11` / `s275-D6` apply · lane EX (Fable 5.1) · judgement lane: every choice below names the ruling sentence it rests on; every figure was RUN in a Chromium the sandbox did not have an hour ago.

**The one line.** `knowledge/_build_kg_explorer.py` → **v1.15** and `notes/_KG-EXPLORER.html` regenerated: the chip bar is four labelled boxes — SYSTEM · DESIGN GOVERNANCE (one obligation, three provenance sub-chips) · EXPLANATION · THE CONSTITUTION (its own box, not a view) — and a fifth additive family `assets` (688 nodes / 1,295 drawn edges + 30 declared nulls) sits in SYSTEM behind a chip that ships OFF. Storage untouched: no node id, edge type, file or fam KEY changed. With the assets chip off the canvas is 1.14 **to the pixel** once the family's ghost layer is set aside (md5-identical in light and dark), the shown/drawn sets and every base position are identical, and ONE header integer moved (declared nulls 105 → 90, §4). Gates: `_validate_kg.py` rc 0 · `_bite_kg_edge_proposal.py` green · `_compose_slice.py --selftest` 54/54 (bite 43 cross-checks `extract()+extract_extra()`) · lane ownership OK.

## 1. The view mapping — which fam goes where, and the D8 sentence each row rests on

Fam KEYS are storage (the landed files stamp `fam: "guidelinerules"` / `"uxprinciples"` / `"assets"`; `RULE_FAM`, `UX_FAM` unchanged); only the LABEL and the BOX are the page's.

| Box on the page | fam key (unchanged) | Label now | Rests on (s277-D8 `ruled`, verbatim) | Default |
|---|---|---|---|---|
| **SYSTEM** — "what exists — the agent chooses" | `structure` | Structure | "SYSTEM (what exists — the agent chooses here)" — what a component contains/composes IS what exists | on |
| SYSTEM | `usage` | Usage | same sentence — where a component is used is a fact of the system, not an obligation | on |
| SYSTEM | `render` | Rendering | same sentence — what renders a component exists | on |
| SYSTEM | `rules` (base wiring) | Rules & wiring | same sentence — `mustNotNeighbour` / `consumes` / `triggeredBy` / `drivesConsumer` are the component's OWN declared wiring; `governedBy` (also in this fam) is additionally gated by the design-governance sub-chip below, so the obligation reading of that one edge type is not lost | on |
| SYSTEM | `assets` (new) | Assets | brief §2 "Assets sits in SYSTEM"; D8's "what exists" — an icon or a logo exists, it obliges nothing | **off** (s277-D4 "behind an `assets` chip OFF by default") |
| **DESIGN GOVERNANCE** — "what a design must or should do — the agent obeys" · ONE obligation box, THREE provenance sub-chips | `guidelines` | WCAG sc: | "the 55 WCAG criteria … shown as ONE obligation with three provenance sub-chips" | off |
| DESIGN GOVERNANCE | `guidelinerules` | HSBC rule: | "the 470 HSBC rules … three provenance sub-chips" | off |
| DESIGN GOVERNANCE | *(no fam — a view sub-chip, key `designrulings`, page-only)* | rulings a design cites | "the design-scoped rulings shown as ONE obligation with three provenance sub-chips" AND "the derived per-ruling scope … UNRATIFIED". Since scope may not be derived, the sub-chip's membership is the AUTHORED citation only: `governedBy` (a meta names the ruling), `ruledBy` (the asset files name it, s277-D4), and a ruling's own `governs` list naming a component/snippet. It gates those 341 edges; it adds no node, no count, no scope. Each sub-chip is still its own chip (s275-D6). | on (it gates base edges that were on in 1.14) |
| **EXPLANATION** — "why — the agent consults" | `uxprinciples` | UX principles & polarities | "EXPLANATION (why — graded principles and polarities; the agent consults here; force is the edge's not the node's, so the 14 obeys→ux edges of s276-D3 stand)" | off |
| **THE CONSTITUTION** — "the ruling record — not a view" | `governance` | Rulings · sessions · evidence | "THE RULING RECORD — the 593 rulings with their evidence and sessions — IS NAMED THE CONSTITUTION … it is not one of the three views" | off |

Chosen, and said: the `rules` base fam stays whole (splitting `governedBy` out would mint a new base fam key — the brief says fam keys do not change — and would break the chip-off identity); the obligation reading is carried by the sub-chip gate instead.

## 2. The Constitution placement — and where the non-design rulings sit

The `governance` family (every ruling in `knowledge/_rulings.json` — 604 today, 593 when D8 was ruled — with `session:` / `evidence:` / `artefact:` nodes and the 48 authored + 241 derived ruling→ruling edges) IS the Constitution. On the page it is the fourth box, drawn with a heavier left rule, headed **THE CONSTITUTION · the ruling record — not a view**, placed after the three views and outside them. The empty panel carries a section of the same name.

**Process, gauge and ritual rulings sit in the Constitution, with the design-scoped ones.** Rests on D8's sentence "THE RULING RECORD — the 593 rulings with their evidence and sessions — IS NAMED THE CONSTITUTION": the record is named as ONE thing, all 593, and the only instrument that would sort design from process — "the derived per-ruling scope on the page" — is "A2's proposal, UNRATIFIED by this ruling". So no ruling is sorted by scope; a ruling appears under DESIGN GOVERNANCE only through the authored citation edge the sub-chip gates (§1), and its node stays a Constitution node. The panel says so in one sentence. The precedence ladder is not drawn.

## 3. The assets family (s277-D4, the explorer half)

* Reader `asset_nodes()` — the `rule_nodes()` shape (`json.load` → `nodes`/`edges`, missing/unreadable file → `[], []`), over `_icon_nodes.json` + `_logo_nodes.json`; `ASSET_FAM='assets'` (free — re-checked: 0 hits in the 1.14 page or builder). Family E runs after A so the 8 `ruledBy` targets (governance `ruling:` nodes) resolve; `usesIcon`/`usesLogo` sources are base components.
* Six edge types drawn (`ASSET_DRAWN`): inGroup 666 · activeVariantOf 232 · usesIcon 371 · usesLogo 18 · defaultFor 0 · ruledBy 8 = **1,295**. Nulls **30** (defaultActive 15 · governedBy 10 · activeVariantOf 2 · defaultFor 2 · usesLogo 1): linked with `t: None` + the file's `$note`, so they are counted in the headline and listed in the node's "declared, unresolved" group exactly as the guideline-rules family's were. `defaultActive` and the logos' `governedBy` are DECLARED-NULL ONLY — no `FAMILY` entry, never drawn.
* Fifth column at `cx 3.4` (`place_extra`); `fit()` now measures the SHOWN extent and centres on it (the base branch keeps its constant, so the base fit is untouched).
* Page: `icon` / `iconGroup` / `logo` node chips + colours (teal / deep teal / slate; not a red — s151-D1 untouched), `READ` verbs for the six, a detail `<dl>` on icon (file · group · active · fill), logo (file · lockup · theme · colour) and iconGroup (manifest key · count) nodes.
* Payload: 2,920,919 B (1.14 rebuilt on today's tree) → 3,423,846 B, **+17.2 %** (lane IL's +12.3 % was nodes+edges only; the rest is the panel prose and the legend).

## 4. Chip-off proof — 1.14 to the pixel, with the two things that are not

Like-for-like: the 1.14 builder + template from `84658db` were run against TODAY's tree (`/tmp/old`, symlinked `knowledge/`) so the ruling store is the same in both pages. Driven in a fresh Chromium context per page (1280×800, `Fit` clicked), `/tmp/proof.py` · `/tmp/proof3.py`:

| Measure, assets chip off (page defaults) | 1.14 | 1.15 | identical |
|---|---|---|---|
| `SHOWN` node ids | 1050 | 1050 | **yes** (set equality) |
| `SHOWNE` edge keys | 1,642 | 1,642 | **yes** |
| drawn-edge set (the draw predicate, `NODEON(s)&&NODEON(t)&&EON(e)`) | — | — | **yes** |
| drawn-node set | — | — | **yes** |
| `x,y,x3,y3,z3,deg` of every base node | — | — | **yes** |
| `view` after Fit | `{0,0,k}` | `{0,0,k}` | **yes** |
| canvas `toDataURL` md5, as-is (light / dark) | `1b86d457…` / `6a7650c3…` | `be06c5e9…` / `0a2d54a9…` | no — see below |
| canvas md5 with the assets family spliced out of the runtime arrays (light / dark) | `1b86d457…` / `6a7650c3…` | `1b86d457…` / `6a7650c3…` | **yes, both** |
| header "declared, unresolved" | 105 | 90 | no — see below |

**Not identical, declared, with size:**
1. **The ghost layer.** Since v1.2 the page paints every OFF family at alpha 0.04 (edges) / 0.05 (nodes) — that is how 1.14 shows the governance and guideline families with their chips off, and 1.12 showed the UX family. The assets family gets the same ghost, and 398 of its edges reach base nodes, so the as-is canvas differs by those faint lines. Removing the family from the runtime arrays makes the two canvases md5-identical in both themes — so the difference is exactly the ghost and nothing else. Size: one alpha-0.04 layer; the alternative (no ghost for assets alone) would make one family behave unlike the other four. Not taken.
2. **One header integer.** `UNRES` was chip-blind: 1.14 read 105 with every family chip off because the 15 UX nulls were counted regardless (the guideline-rules nulls were 0 after 1.13). The page's own stated rule (template: "counts follow the FAMILY chips only") now applies to nulls too: 90 with every chip off (the base's own), 120 with assets on, 135 with everything on. Size: one `<span>` in the header; the alternative (add 30 chip-blind → 135 at chip-off) also breaks 1.14's number and keeps the inconsistency.

Everything else on the page that differs from 1.14 is the brief's own ask: the legend (relabelled, boxed, compacted 30 → 24 px chips so four boxes fit where three rows sat), the hint (moved under the tools because the legend now spans the stage), and the empty-panel prose.

## 5. Counts — every chip on = base + 4 families + 688 / 1,325

| | nodes | drawn edges | declared nulls |
|---|---|---|---|
| base (live) | 1,050 | 1,552 | 90 |
| governance (the Constitution) | 2,155 | 3,255 | 0 |
| guidelines (WCAG sc:) | 142 | 1,120 | 0 |
| guidelinerules (HSBC rule:) | 400 | 634 | 0 |
| uxprinciples (Explanation) | 171 | 96 | 15 |
| **assets** | **688** | **1,295** | **30** |
| every chip on (header) | **4,606** = 3,918 + 688 | **8,087** relations = 6,762 + 1,325 (drawn + nulls) | 135 |

Builder totals: nodes 4,618 (3,930 + 688, dead nodes included), edges 8,125 (6,800 + 1,325). Assets chip alone on: 1,738 nodes · 2,959 relations (the 8 `ruledBy` edges count only when the Constitution chip is also on — both ends must be shown, the `hasParty` precedent) · 22 edge types · 120 declared nulls. `LIVEE` chip count for assets reads 1,300 = 1,295 drawn + 5 nulls whose type is a drawn type (the UX chip's 111 = 96 + 15 is the same arithmetic).

## 6. Screenshots — `notes/_lanes/279/explorer/shots/` (never-driven: fresh `browser.new_context` per shot, `color_scheme` emulated, `Object.keys(localStorage) == ['kg-theme']` asserted — the page writes only its own theme key on load; `shots.json` carries the header and chip readings of each)

`kg-115-light-1280-assets-off.png` · `kg-115-light-1280-assets-on.png` · `kg-115-light-1280-assets-all.png` (every chip) · `kg-115-light-390-assets-off.png` · `kg-115-light-390-assets-on.png` · `kg-115-dark-1280-assets-off.png` · `kg-115-dark-1280-assets-on.png` · `kg-115-dark-390-assets-off.png` · `kg-115-dark-390-assets-on.png` · `kg-115-light-1280-focus-logo-masterbrand-dark-colour.png` (a logo node dug: 8 `usesLogo` with their `via`, the detail `<dl>`).

Chromium: the memory recipe's `playwright install chromium` fails here on `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` (Node's TLS, not the CDN — `curl` reaches it), and `/sessions` was at 100 % disk. Done instead: `curl` the headless-shell zip to `/tmp/pw/chromium_headless_shell-1243/`, `touch INSTALLATION_COMPLETE`, `libXdamage.so.1` from `ports.ubuntu.com` (apt has no lists here) into `/tmp/lib`, run with `PLAYWRIGHT_BROWSERS_PATH=/tmp/pw LD_LIBRARY_PATH=/tmp/lib`. `ldd … | grep "not found"` → 0. Worth a memory-note amendment; not this lane's file.

## 7. Gates — every line

* `python3 knowledge/_validate_kg.py` → rc **0** — "OK — every ref parses+resolves, every null carries a note, every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4 resolutions input was consumed."
* The explorer's own selftest: there is no `--selftest` in `_build_kg_explorer.py`; the two instruments that drive its real objects were run — `python3 knowledge/_bite_kg_edge_proposal.py` → "BITE PASSED — all cases green" rc 0; `python3 knowledge/_compose_slice.py --selftest` → **54 bites, 0 failed** (bite 43 "LIVE reader agrees with _build_kg_explorer.extract()+extract_extra() on shared edge-type counts" — ok). The template's script was also `node --check`ed after every edit (one `)` typo caught and fixed before any screenshot).
* `python3 knowledge/_validate_lane_ownership.py` → "LANE OWNERSHIP: OK — no staged path under another session's lane (this is #279)"; `git diff HEAD -- knowledge/_validate_lane_ownership.py` → 0 lines.
* Counts with every chip on = base + 4 families + 688 / 1,325 → §5, measured in the page.
* `git status` before staging: `M` my three files + `notes/_dream/_GRADE-DECISIONS.jsonl` (pre-dirty, left) + `knowledge/_graph-mark-observations.jsonl` (an instrument append the commit script declares; not mine, not staged) + `??` the two #279 lane dirs. Lane SC's paths (`_compose_slice.py`, `knowledge/guidelines/`, the rules index) untouched by me — `git diff --numstat` §9 names only my paths.
* Page errors in every driven context: `[]`.

## 8. Not done, with size

1. **`edges.obeys` still not drawn** — brief §4. D8 does not force it: "force is the edge's not the node's, so the 14 obeys→ux edges of s276-D3 stand" is a statement about the edges' standing, not an instruction to draw them, and D8's storage clause says the explorer's chips and labels change, not its readers. Left declared (v1.14 note, unchanged). Size if wanted: one reader over the 10 metas' `edges.obeys` (168 entries) + a `FAMILY` entry under DESIGN GOVERNANCE — a lane, because the chip's placement (obligation vs explanation, since half the refs are `ux:`) is a ruling-shaped question.
2. **Lane SC's row W-279sc** names "whether the explorer draws the 'inference by declared scope' chip from `scope_reach()`" as Dave's. Not in this brief; not drawn. Size: one reader over `knowledge/guidelines/_scope.json` + one chip; it would be a fourth provenance under DESIGN GOVERNANCE, which D8 fixed at three — so it is a ruling first.
3. **The mobile grid was broken before this lane** (`header{grid-column:1/3}` made an implicit second column under the one-column phone grid, so the stage was 48 px wide at 390 in 1.14 — measured in both pages). Fixed with one declaration (`header{grid-column:1}`) plus a scrolling legend at phone width, because the brief asked for 390 screenshots that mean something. Declared here because it is a base-page change, not a chip-off pixel of the canvas (the canvas identity in §4 is at 1280).
4. The s277-D6 reading question lane IL declared (31 `activeVariantOf` edges on the 15 multi-active bases) is unchanged — this lane draws what the files carry.

## 9. Shipped sha and `git diff --numstat` from it

Pre-commit numstat against `a39d4cd` (HEAD when this report was written; lane SC's last commit): `52 2 knowledge/_build_kg_explorer.py` · `78 20 knowledge/_kg_explorer.template.html` · `80 22 notes/_KG-EXPLORER.html` + this report, its `_subreports` copy, the `shots/` directory and the `_state.json` row. The shipped sha is appended below by the follow-up report-only commit, the W-279rd / W-279sc way.


Shipped: **`2c6b640`** — `#279 lane EX: explorer 1.15 — three views by force, the Constitution named, assets chip OFF — s277-D8 + D4` (this paragraph rides in the follow-up report-only commit). Staged by explicit path (the 9 named + `notes/_REHEARSAL-LOG.jsonl`, auto-staged by the commit script's own session witness; `_CHAIN.md` regenerated because the store row made the chain gate refuse). NOT staged, deliberately: `knowledge/_graph-mark-observations.jsonl` (an instrument append, not mine) and `notes/_dream/_GRADE-DECISIONS.jsonl` (per brief). `_state.check()` reports the same PRE-EXISTING failure lane SC saw, `W-278wr: missing required field(s) links` — not this row.

`git diff --numstat a39d4cd 2c6b640` (binary .png rows omitted):

```
2	2	_CHAIN.md
52	2	knowledge/_build_kg_explorer.py
78	20	knowledge/_kg_explorer.template.html
19	0	knowledge/_state.json
80	22	notes/_KG-EXPLORER.html
2	0	notes/_REHEARSAL-LOG.jsonl
19	0	notes/_lanes/279/explorer/BRIEF.md
99	0	notes/_lanes/279/explorer/REPORT.md
83	0	notes/_lanes/279/explorer/shots/shots.json
99	0	notes/_subreports/2026-09-16-279-EX-explorer.md
```
