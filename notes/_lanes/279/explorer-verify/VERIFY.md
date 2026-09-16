# LANE EV — VERIFY — explorer 1.15 (lane EX, commit `2c6b640` + report `e7ff7b9`)
#279 · 2026-09-16 · verifying s277-D8 (three views, the Constitution named) + the explorer half of s277-D4 (assets chip OFF) · lane EV (Fable 5.1) · read-only on the tree; nothing committed. Every number below was re-derived against the LIVE tree and the SHIPPED page, never copied from EX's report.

## VERDICT: GREEN WITH FIXES

Storage is untouched, the chip-off identity holds, every count re-derives, the gates are green, EX stayed inside its paths. The fixes are three page-level things a designer sees on sight (§5) and one ruling-shaped question (§9) that EX's third provenance sub-chip raises rather than settles. None of them is a reason to pull the commit.

## 1. Storage untouched — YES for EX's commit

* `git diff 84658db 2c6b640 --stat -- knowledge/` → 5 files: `_build_kg_explorer.py` (54), `_kg_explorer.template.html` (98), `_state.json` (38), **and** `_compose_slice.py` (268), `guidelines/_scope.json` (1247). The last two are lane SC's, landed at `9e7a158` which sits between the two shas — the range crosses SC. **EX's own commit** (`git diff --numstat 2c6b640^ 2c6b640`) touches exactly `_build_kg_explorer.py` 52/2 · `_kg_explorer.template.html` 78/20 · `_state.json` 19/0 (the W-279ex row only) under `knowledge/` — nothing else.
* Fam KEYS before/after (grep `_FAM =` at both shas): `RULE_FAM='guidelinerules'`, `UX_FAM='uxprinciples'` unchanged; `ASSET_FAM='assets'` added (the landed files' own key). `place_extra` tuple gains `(ASSET_FAM, 3.4)` only; the four existing `cx` values unchanged.
* No node id or edge type changed: the builder diff is purely additive (a new reader `asset_nodes()`, a new block E in `extract_extra`, three new `extra` keys, one print). No node/edge file under `knowledge/` is in EX's diff.

## 2. View mapping — graded row by row against D8's words

| Row | Grade | Why |
|---|---|---|
| `structure` → SYSTEM | honest | "what exists — the agent chooses" |
| `usage` → SYSTEM | honest | same |
| `render` → SYSTEM | honest | same |
| `rules` (base wiring, incl. `governedBy`) → SYSTEM | **stretched** | `mustNotNeighbour`/`consumes`/`triggeredBy`/`drivesConsumer` are wiring, fine. But `governedBy` is a component saying "this ruling binds me" — that is D8's "what a design must do", not "what exists". EX keeps it in SYSTEM because the fam KEY may not split (true) and covers the obligation reading with the sub-chip. Declared, defensible, not what the sentence says. |
| `assets` → SYSTEM | honest | brief §2 + "what exists"; an icon obliges nothing |
| `guidelines` → WCAG sc: | honest | "the 55 WCAG criteria" |
| `guidelinerules` → HSBC rule: | honest | "the 470 HSBC rules" |
| `designrulings` sub-chip (page-only) | **stretched** | D8's third provenance is "the design-scoped rulings" — a set of ruling NODES named beside two other node sets (55 criteria, 470 rules). EX's chip contains no nodes: it is an EDGE gate over authored citations (`governedBy` · `ruledBy` · `governs→component/snippet`). It exists because D8 also says the per-ruling scope is UNRATIFIED, so the node set cannot be derived. The chip therefore enacts a sentence D8 half-blocks. See §9. |
| `uxprinciples` → EXPLANATION | honest | "why — graded principles and polarities; the agent consults" |
| `governance` → THE CONSTITUTION, own box | honest | "IS NAMED THE CONSTITUTION … it is not one of the three views" |

**Is the `designrulings` gate "storage untouched, chips and labels change", or a base-graph behaviour change?** Both, and the second part is the honest description. Storage: untouched (nothing in `knowledge/` node or edge files moves). Page: a NEW gate `EON(e)` now sits in the draw predicate, `applyFocus` and the depth-2 walk, so a base-family edge can be hidden by a chip outside its own family — 1.14 had no cross-family gate. At page defaults (sub-chip ON) the draw is identical to 1.14 (§3). When Dave clicks it OFF with the base chips only, **28** base `governedBy` edges leave the canvas and the focus dig — the header does not move (`recount()` ignores `EON`), so the counts and the drawing disagree in that state. D8 said "the explorer's chips and fam labels do [change]" — a new chip is within that; a chip that reaches into the base draw is more than a relabel. It is declared in EX's report; it was not asked for by D8.

**The chip's number.** It reads **341** = 295 `governs→component/snippet` (Constitution family — visible only with THAT chip on) + 28 base `governedBy` + 8 asset `ruledBy` + 10 asset `governedBy` **nulls that are never drawn**. So at the page's defaults a chip labelled 341 governs 28 drawn edges; 10 of its 341 can never draw. A designer would call the number wrong on sight.

**Process / gauge / ritual rulings in the Constitution box, with the design-scoped ones — does D8 support it?** Yes, on its face: "THE RULING RECORD — the 593 rulings … IS NAMED THE CONSTITUTION" names the whole record as one thing and forbids the only sorting instrument ("derived per-ruling scope … UNRATIFIED"). The cost EX does not say out loud: under this reading NO ruling node ever appears inside DESIGN GOVERNANCE — the "design-scoped rulings shown as ONE obligation" clause is enacted as edges only. That is the residue for Dave (§9).

## 3. Chip-off identity — reproduced, my own code, at the data level

Both pages rebuilt by me from the shipped shas into `/tmp/ev/` (symlinked `knowledge/`, today's tree; `84658db` builder+template → `114.html` 2,920,919 B; `2c6b640` → `115.html` 3,423,832 B). The shipped `notes/_KG-EXPLORER.html` equals my 1.15 build byte-for-byte except the git-sha stamp (`commit: a39d4cd` — my scratch has no git). The page's own predicates (`famOK`, `NODEON`, `EON`, `recount`, the draw loop's `NODEON(s)&&NODEON(t)&&EON(e)`, `alive` at the last snapshot) were re-implemented in Python over the embedded `KG` JSON (`/tmp/ev/sim.py`), defaults = base four chips on, every family off, `designrulings` on:

| Measure, chips at page default | 1.14 | 1.15 | identical |
|---|---|---|---|
| SHOWN nodes | 1050 | 1050 | yes |
| SHOWNE relations | 1,642 | 1,642 | yes |
| edge types | 16 | 16 | yes |
| drawn-edge set (s,t,type) | 1,175 | 1,175 | yes (set equality) |
| drawn-node set | 1050 | 1050 | yes |
| `x,y,x3,y3,z3,deg` of every base node (1,062 incl. dead) | — | — | yes |
| header "declared, unresolved" | **105** | **90** | no |

**105 → 90: a correction, not a defect.** Nulls by family are the same in both pages: base 90 · governance 0 · guidelines 0 · guidelinerules 0 · uxprinciples 15 (1.15 adds assets 30). 1.14 summed nulls chip-blind, so the 15 UX nulls counted with the UX chip OFF while the same chip's nodes and relations did not — the one header integer that ignored the chips. 1.15 filters nulls through `famOK` like the other four integers: 90 / 120 (assets on) / 135 (all on). The template's own stated rule ("counts follow the FAMILY chips only") now holds for all five integers. Correction.

**Canvas md5 not reproduced** — the Chromium EX built (`/tmp/pw` headless-shell) is gone from disk; `/sessions` is at 99 % and the brief forbids a download; the Browser pane refuses `file://`. So EX's ghost-layer claim (as-is canvases differ only by the assets family's alpha-0.04 ghost) rests on its report; what I can say from the data is that the ghost has 398 asset edges reaching base nodes to paint, and that with the family removed nothing else in the draw inputs differs (§3 table). The ghost is consistent with the four other families' behaviour since v1.2 — not a defect.

## 4. Counts with every chip on — re-derived

From the live node files via the shipped builder's `extract()+extract_extra()` (my 1.15 build) and my own predicate code over the page's `KG`: base 1,050 / 1,552 / 90 · governance 2,155 / 3,255 / 0 · guidelines 142 / 1,120 / 0 · guidelinerules 400 / 634 / 0 · uxprinciples 171 / 96 / 15 · **assets 688 / 1,295 / 30** (inGroup 666 · usesIcon 371 · activeVariantOf 232 · usesLogo 18 · ruledBy 8 · defaultFor 0; nulls defaultActive 15 · governedBy 10 · activeVariantOf 2 · defaultFor 2 · usesLogo 1). Every chip on: **4,606 nodes · 8,087 relations · 53 edge types · 135 declared nulls** (= 3,918+688 / 6,762+1,325). Builder totals 4,618 / 8,125 (12 dead base nodes, 38 dead edges). Assets alone: 1,738 / 2,959 / 22 / 120. All equal to EX's §5 and to the header in `kg-115-light-1280-assets-all.png` (4606 · 8,087 · 53 · 137 · 135).

## 5. The ten screenshots, by eye

Legible at 1280: the four boxes read as SYSTEM · DESIGN GOVERNANCE (dashed inner box "one obligation · three provenances") · EXPLANATION · THE CONSTITUTION — the last with a heavier left rule, after the three, visibly its own thing. Light and dark both fine; asset colours (teal/slate) are not a red. Header integers match §4 in every shot. What a designer would call wrong on sight:

1. **390 is not broken any more, but it is not usable either.** The stage is full-width now (1.14 had it at ~48 px — EX's `look-114-390.png`, seen), but the legend stack fills the entire 55vh stage in all four phone shots: the graph is a red smear behind the chip rows, and DESIGN GOVERNANCE / EXPLANATION / THE CONSTITUTION are below the legend's own scroll fold — so at 390 the Constitution is NOT visible without scrolling the legend, and the scrub row's counts run off the right edge ("1,552" clipped). The chips work; the canvas does not.
2. **Assets-on fit crops the base cluster** (`light-1280-assets-on`, `dark-1280-assets-on`): the base hub sits at x≈100–190 with nodes bleeding off the left edge at x=0, while the assets column ends at x≈790 with ~90 px of empty stage to its right and the whole graph in a band 150 px tall. The new `fit()` centres on the shown extent but the wide-family constant + the 0.12·H lift leave the picture left-heavy. Same in the all-chips shot: a horizontal band across the middle third, legend on top of its lower edge.
3. **The legend sits on the graph at 1280 too.** With 24 px chips and four boxes the legend now reaches y≈475 of an 800 px stage; the base hub's lower third is under it in every 1280 shot, and in the focus shot the dug neighbour "App shell — multi-column" and a sector label ("USESLOGO · 8") are painted through the DESIGN GOVERNANCE box. Not new in kind (1.14's three rows also overlapped), worse in degree.
4. Small: "RULINGS A DESIGN CITES 341" reads as a live count of something the eye cannot find (28 drawn at defaults, §2). The empty-panel headline "Every one declared by a component, none invented" now heads 1,738 / 4,606 nodes, most of which no component declared (pre-existing wording, wrong-er now).

## 6. "Inherited phone grid fixed in passing"

Broken in 1.14: yes — EX's own 1.14 screenshot at 390 (`outputs/look-114-390.png`) shows the stage as a ~48 px strip with the aside beside it, and the mechanism is in the 1.14 CSS: `.app{grid-template-columns:1fr}` under 900 px while `header{grid-column:1/3}` spans two columns, forcing an implicit second column. I could not re-measure in a browser (none on disk, none allowed). The fix: `header{grid-column:1}` inside the media query, plus in the same block `.search input` 180→150, `.brand span{display:none}`, `.tools{gap:4px}`, a scrolling legend (`max-height:calc(100% - 140px);overflow:auto`), column-wise view boxes, `.hint{display:none}`. Confined to the template (and therefore the generated page): the builder diff has no CSS. The 1.15 phone shots confirm the stage is full-width. It is more than "one declaration" — seven — and it produces §5.1.

## 7. Gates

* `python3 knowledge/_validate_kg.py` → rc **0**, "OK — every ref parses+resolves …".
* `git diff HEAD -- knowledge/_validate_lane_ownership.py` → **0** lines; `git diff 84658db 2c6b640 --stat -- knowledge/_validate_lane_ownership.py` → empty; last touched `8053591` (#276).
* `git diff --numstat 2c6b640^ 2c6b640` = EX's §9 list exactly (`_CHAIN.md` 2/2 · builder 52/2 · template 78/20 · `_state.json` 19/0 · `_KG-EXPLORER.html` 80/22 · `_REHEARSAL-LOG.jsonl` 2/0 · BRIEF 19 · REPORT 99 · `shots.json` 83 · subreport 99 · 10 png). `2c6b640^` is `a39d4cd`, the sha EX diffed against. `e7ff7b9`: REPORT +18, subreport +18, `_REHEARSAL-LOG.jsonl` +1 — the report-only follow-up.
* Live tree at verify time: `git status --short` = `M knowledge/_graph-mark-observations.jsonl` · `M notes/_dream/_GRADE-DECISIONS.jsonl` · `?? notes/_lanes/279/active-review/` — the two pre-dirty files and another lane's dir; nothing of EX's uncommitted. Live builder/template == `2c6b640` (diff empty).

## 8. Outside its paths?

No. `_CHAIN.md` (+1 item, the store row) and `notes/_REHEARSAL-LOG.jsonl` (the commit script's session witness) are the commit script's own writes, declared. `_state.json` adds one row, `W-279ex`. Lane SC's files — `knowledge/_compose_slice.py`, `knowledge/guidelines/`, `knowledge/guidelines/_scope.json` — are absent from EX's diff. EX did not stage `_graph-mark-observations.jsonl` or `_GRADE-DECISIONS.jsonl`.

## 9. Judgement

Yes, the `designrulings` gate is a ruling-shaped question for Dave: D8 names "the design-scoped rulings" as the third of three provenances inside the one obligation, and in the same breath leaves the only way of knowing which rulings are design-scoped unratified, so EX built a third sub-chip that holds no rulings at all — only the authored edges by which a design cites one — and put every ruling node, design-scoped or not, in the Constitution. The two options in plain prose: (a) accept EX's reading — the third provenance IS "the rulings a design cites", an edge chip with no ruling nodes of its own, ON by default; then fix its count to the drawn edges it actually governs and say on the chip that it is citations, not rulings; or (b) say the third provenance is a set of RULING nodes and cannot be drawn until a per-ruling scope is ratified — remove the sub-chip, ship DESIGN GOVERNANCE with two provenances and a visible "third: pending s277 scope ruling" slot, and rule the scope (A2's proposal or another) in its own lane. Either way the base draw should not answer to a chip outside its family until Dave has said which it is.

## Verifier's own residue
* Two 3 MB scratch pages (`114.html`, `115.html`) landed in this session's outputs folder while trying to open them in the Browser pane; the pane refused `file://` and the folder refuses `rm` — harmless, not in the tree.
* Not run: canvas md5s, the 390 measurement of 1.14 (browser gone). Said where it matters (§3, §6).
