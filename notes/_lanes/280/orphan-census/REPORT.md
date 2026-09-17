# #280 lane OC — THE ORPHAN CENSUS — REPORT

provenance: 280 · 2026-09-17 · lane OC (Opus sub) · MEASURING lane — nothing was wired
page: `notes/_lanes/280/orphan-census/ORPHANS-2026-09-17.html`
measured on: explorer **v1.19**, graph generated 2026-09-17, builder commit `94204dc` (the live
`notes/_KG-EXPLORER.html` as lane EX3 had it at 07:47Z; re-run `_census.py` if it moves again)

## The headline

**157 of the 4,618 nodes on the stage have no line that any chip can draw — four causes account
for every one of them, and the largest is the 100 UX principles of the pink cloud, 99 of which
have no edge of any kind in storage.**

At the page's own defaults it is 160 of 1,050; with every family chip on, 181 of 2,451; with the
Constitution too, 157 of 4,618. The middle number is the biggest because switching a family on
brings its own dark dots with it — the UX family arrives carrying 99 of them.

## The ten sets, one line each — what, why, what it costs

1. **The pink cloud — 100 of 145 UX principles, dark at all three settings.** A principle gets a
   line only when a polarity names it; 99 of the dark ones have no edge of any kind in storage.
   *Cause: the source never emitted it* — the principle generator can already write two more edge
   kinds (a principle's research family, 145 carry the field across 32 families; and its graded
   sources, 145 carry those) and both were held off when the family landed. **Cost: one question
   to Dave, then one lane** — the generator is written, the lane lands and proves it.
2. **94 base `rule:` nodes dark at the page defaults, and only there.** Every one lights the
   moment the HSBC rule: chip goes on, because the line that holds them belongs to that family.
   *Cause: a chip that loads off — not an orphan.* **Cost: free**, or one question if the default
   should change.
3. **23 `shape:` nodes, dark at every setting**, with 26 `hasDataShape` lines behind them.
   *Cause: no edge type reaches the page* — the chip map has no family for that type. **Cost:
   shares one lane with 4, 5 and 9.**
4. **14 `intent:` nodes, dark at every setting**, with 28 `answersIntent` lines behind them. Same
   cause. **Same lane.**
5. **12 `role:` nodes, dark at every setting**, with 108 `providesRole` lines — the heaviest
   single undrawn edge type in the graph. Same cause. **Same lane.**
6. **24 `rule:` nodes that stay dark with every chip on and need the Constitution to show a
   line.** Their one edge is a `definedIn` pointing at three guideline files the builder filed in
   the governance family, because a ruling named the file among its artefacts first:
   data-visualisation.md (15 rules), accessibility-interaction-design.md (6), naming.md (3).
   *Cause: the relation has no declared home.* **Cost: one question — which family owns a file
   two records both name — then a short lane.**
7. **8 `logo:` lockups whose only edge is a declared-null `governedBy`.** *Cause: a leaf by
   design* — `s277-D7` put them on the stage visibly unbound on purpose and parked a separate
   logo review. **Cost: free to declare; the review is its own piece of work.**
8. **The 4 principles a design actually cites.** 10 component metas carry `obeys`; 14 of those
   168 lines land on a principle and `s277-D8` said they stand. Not one is drawn: `obeys` has no
   family in the chip map, and unlike 3–5 it is an obligation, so it belongs in DESIGN
   GOVERNANCE, which `s277-D8` fixed at three provenances. **Cost: one question, then a small lane.**
9. **376 authored lines across 6 edge types that no chip can turn on** — `obeys` 168,
   `providesRole` 108, `yieldsTo` 45, `answersIntent` 28, `hasDataShape` 26, `defaultActive` 1
   (a declared null). They orphan 49 nodes between them and hide 43 component→component
   `yieldsTo` lines that orphan nobody. **Cost: one lane for the System-view ones; only the
   obligation edge in 8 needs a word first.**
10. **The Explanation view rests on one hinge.** All 30 polarities are wired and between them
    reach 45 of the 145 principles; no component, no rule and no ruling reaches a principle at
    all. Not an orphan set — the reason there is one. **Cost: none separate. It is set 1 seen
    from the other side.**

## The four causes, and what each one is worth

| cause | sets | nodes | price |
|---|---|---|---|
| (a) no edge type reaches the page — the chip map has no family for it | 3 · 4 · 5 · 8 · 9 | 49 | one lane for the System-view types; one question for the obligation edge |
| (b) the source never emitted the edge | 1 · 10 | 100 | one question, then one lane |
| (c) the relation has no declared home | 6 | 24 (0 at the Constitution setting) | one question, then a short lane |
| (d) a leaf by design, or a chip that is simply off | 2 · 7 | 8 permanent, 94 default-only | free to declare |

## Method

`_census.py` reads the graph out of the embedded `<script id="kg">` in the live
`notes/_KG-EXPLORER.html` and the chip vocabulary — the `FAMILY` edge-type→family map, the
`famOn` defaults and `FAMLABEL` — out of `knowledge/_kg_explorer.template.html`, parsed, never
retyped. It then re-implements the page's own three predicates: a node is shown when its family
chip is on (every type chip is on in all three settings), an edge is DRAWN when its family chip
is on, the design-rulings sub-chip allows it, its target resolves, and both ends are shown. A
node is degree-zero when no drawn edge touches it; it is *null-only* when it is degree-zero and
carries at least one declared null. Every number on the page comes out of `facts.json`; none is
typed into the copy.

The ghost line the page paints at alpha 0.04 for an edge into a switched-off family is **not**
counted as drawn — it is a halo, not a relation, and lane LM's finding 1 is the precedent.

## Gates

- Page errors `[]` and zero console errors in two never-driven contexts (1280 light, 390 light)
  and in the driven pass. `Object.keys(localStorage)` empty in all three.
- No horizontal scroll at 390px (`scrollWidth` 390 = `innerWidth`).
- 10 blocks · 10 radio groups · 30 options · 10 note fields · 0 pre-checked.
- Export proved by driving: `{exportedAt, page, answers:{<set>:{choice, note}}}`, 10 answers, the
  note carried verbatim. `clipboard.writeText`'s rejection is swallowed (lane LS finding 3).
- Screenshots: `shots/orphans-1280-light-top.png`, `shots/orphans-1280-light-set01.png`,
  never driven, via `knowledge/_render/seat_env.sh`.

## Declared

- **Nothing under `knowledge/` was written.** The lane read the explorer, the template,
  `_rulings.json` and `_ux_principle_nodes.json`, and wrote only inside its own folder plus the
  `W-280oc` row in `_state.json` through `_state.add()`.
- **The graph moved under this lane.** Lane EX3 rebuilt `notes/_KG-EXPLORER.html` from v1.18 to
  v1.19 mid-lane. Both readings were taken; the families, the storage and all 157 figures are
  identical across them, and the page cites v1.19. A later EX3 rebuild means re-running
  `_census.py` — it is a pure read, and it rewrites the page from the live file.
- **No ruling ids appear in the page's body copy** (they are in this report, which is for the
  record, not for him).
- The `s277-D12` tokens question is untouched by this census: no token node is in the graph, so
  none of them can be an orphan yet.
