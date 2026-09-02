# `#234`-`rB` — the designer's composition rules: what mature systems write down, and what they leave to taste

session: `#234` · 2026-09-02
window: quality-bar research, strand rB
sub index: `rB`
brief: `notes/_briefs/2026-09-02-234-quality-bar-research-brief.md`
tokens: `UNMEASURED` — a sub cannot read `message.usage` from its own seat; no `_checkin.py` run was
authorised by the brief (read-only lane, and the probe file is not this sub's to write). Effort band
by the `s168-D2` ladder: **S–M** — 2 repo passes, 6 web searches, 4 full page fetches.

## VERDICT

Both regions of the strand were **DONE**. The headline is that mature systems DO write composition
down, but they write it in a shape the Apollo pack has no seat for: **not "here is a good layout",
but "here is the spacing/nesting/containment RELATION that must hold between a parent and its
children"** — Polaris states it as a strictly-decreasing gap ladder by nesting depth, Carbon as a
same-height/same-width contract inside a tile group plus three named layout models, GOV.UK as a
one-thing-per-page rule with a research-gated exception, Material as three canonical layouts with
fixed/flexible pane roles. Ten of those relations restate as machine-checkable conditions and are
listed below with the check named; four more are honestly eye-only and are marked as such. The
WHEN-TO-GROUP question has a clean answer from the sources: **nobody groups by content type**
(KPI/chart/rail are not categories anywhere) — they group by *shared decision*, and then constrain
the group so its members are uniform. That is the opposite of what the pack's `tpl-group-kpi` /
`-chart` / `-rail` vocabulary implies, and it is the single most consequential finding here. On
tile/row sizing I found four distinct published models and I report them without ranking: Dave's
floated ladder stays floated, and canon already ships a **two-model hybrid** (fixed rows at the top
level, `minmax(unit,1fr)` floor inside a nested bento) that the brief's framing did not anticipate.
The one absence worth naming: **no mature system publishes a bento rule at all** — the bento
literature is entirely industry blogs, and I label it as such rather than dress it as a standard.

COUNTS: findings `15` · ruling-shaped `5` · UNPROVEN `3`

*(the UNPROVEN/CLAIMED section carries 4 items — 3 UNPROVEN plus 1 CLAIMED; the parsed count is the
UNPROVEN term only.)*

## What was done

**Region 1 — repo grounding (read-only, in the brief's order).**
`apollo-spider/cold-start/DESIGN-CONTRACT.md` · `apollo-spider/skills/generate-from-canon/SKILL.md` ·
`apollo-spider/skills/check-with-gates/SKILL.md` · three meta files —
`knowledge/components/dropdown.meta.json` (component),
`knowledge/components/chart-line.meta.json` (chart),
`knowledge/components/template-dashboard-bento.meta.json` (template) ·
`notes/_briefs/2026-09-01-233-delegated-wrap-brief.md`. `GOOD-MORNING.md` was NOT read.
Beyond the named set, and because the strand is composition: `knowledge/_render/_bento_edit_rails.json`
(structure walked, not read whole), `knowledge/canon/canon.css` §AUTO-BENTO (lines 1055–1135),
`knowledge/snippets/Template-dashboard-bento.reference.html` (the three `tpl-group-*` rules and the
three group `<section>`s), `knowledge/guidelines/_rules-index.json` (470 rules, filtered), and the
gate roster by filename only (42 `_validate_*.py`; none was run).

**Region 2 — web research.** 6 searches, 4 full fetches (Carbon tile usage; Carbon v10 dashboards;
Polaris card-layout pattern; NN/g common region; GOV.UK question pages). One fetch failed
(`m3.material.io/foundations/designing/flow` — JS-only shell, no content served); Material findings
therefore rest on search-result text and are labelled CLAIMED, not quoted.

Nothing was written except this file. No git operations. No gate was run.

## Findings

Every finding carries its probe. Findings marked **OPINION** have no primary probe and are my
reading, not a source's word.

---

**1. Polaris states grouping as a MONOTONIC GAP LADDER, and that is arithmetic, not taste.**
Probe — <https://polaris-react.shopify.com/patterns/card-layout>, quoted: *"It's the difference
between the gap sizes that creates the effect of grouping and hierarchy. Elements with tighter gaps
are perceived as more related than those with a looser gap."* and, on padding: *"The general rule is
that the deeper an element is nested, the smaller its padding is."* The page then names the whole
ladder concretely — `space-100` (tightest, innermost groups), `space-200` (blocks inside card
sections), `space-300` (form layout items — *"By increasing the gap size, content blocks can be more
readily perceived as unified, discrete items"*), `space-400` (loosest, between card sections; *"The
gap size is the same as the card padding"*). This is the most directly transplantable rule found:
it is a relation over a *stop set*, and Apollo already has the stop set (`{1,2,4,16,24,40}`,
`s219-D1(4)`, `knowledge/_render/_bento_edit_rails.json` → `rail.spacing_stops`).

**2. Polaris also states the ANTI-rule — a flat ladder is a defect, not a style.**
Same page, the two "Don't" captions: *"Use a flat hierarchy for content that should have different
spatial relationships"* and *"Use a flat hierarchy that causes section titles to float with equal
space to sections above and below."* A parent gap equal to its child gap is therefore a *named
failure* in a mature system — which makes "all gaps equal at two adjacent nesting levels" a
legitimate gate condition rather than an aesthetic opinion.

**3. Carbon constrains the GROUP, not the page: members of a tile group must match.**
Probe — <https://carbondesignsystem.com/components/tile/usage/>: *"Tile groups are helpful when
aligning tiles that have a strong relationship. Tile groups usually flow horizontally from left to
right and have hierarchical importance"*; and the Do/Don't pair: *"Do match the tile variants in
groups. Do not mix different variants of tiles in groups."* The grouping test in Carbon is
**relationship strength + equal hierarchical importance**, and the enforcement is **uniformity of
member type**. Note what is absent: no content-type taxonomy, no "KPIs go here".

**4. Carbon publishes THREE named tile-layout models, and they are about height/width variance.**
Same page, quoted: *"In a standard layout, tiles are the same in height and width as all other tiles
in the group. In a vertical masonry layout, tiles can vary in height, but are consistent in width.
In a horizontal masonry layout, tiles can vary in width; different rows of tiles may vary in height,
but tiles within a row should be consistent in height."* Plus the sizing rule: *"Tile height varies
depending on the content placed within it while using spacing tokens and following aspect ratios.
The minimum tile height is a 2:1 aspect ratio."* Carbon's model is therefore **content-sized height
with an aspect-ratio FLOOR, and uniformity enforced per row** — the row, not the wall, is the unit
of consistency.

**5. Carbon's dashboard guidance is ordering + budget, not layout.**
Probe — <https://v10.carbondesignsystem.com/data-visualization/dashboards/>: *"Prioritize data by
importance, then create a clear visual hierarchy. The most important data should have the highest
contrast and occupy the largest area."* · *"Place the most important at the top of the page and
follow the F-pattern"* · *"Limit the number of metrics"* · *"All charts should use the same layout
and spacing, and have legends in the same position relative to the charting area."* Only the last of
these is mechanically checkable; the first three are eye/product decisions. Carbon itself flags the
page: *"This guidance is a work in progress."*

**6. NN/g: a container OVERPOWERS proximity — so containment and spacing are not interchangeable.**
Probe — <https://www.nngroup.com/articles/common-region/>: *"Creating a clear boundary is a strong
visual cue that can overpower other grouping principles such as proximity or similarity"*, and the
definition: *"items within a boundary are perceived as a group and assumed to share some common
characteristic or functionality."* Consequence for a bento: a group's *surface* is a grouping claim
of the strongest kind. This is exactly the failure the #233 test hit — a local override
(`cn-table` on stat-cards) that stripped the Trade/Accounts group's surface silently un-grouped it
(probe: `notes/_briefs/2026-09-01-233-delegated-wrap-brief.md:41-44`).

**7. NN/g also names the OVERUSE failure — borders where whitespace would do, and false floors.**
Same page: *"When possible, using whitespace alone to create clear groupings reduces the visual
complexity of a design"* · *"segmenting a page into distinct sections can create false floors, and
may prevent users from scrolling down the page because they think they've hit the end. This issue is
especially common when borders extend the full width of the screen."* This is the published
counter-pressure to "group everything", and it is why a WHEN-to-group rule needs a *stop* condition
as well as a start condition.

**8. GOV.UK is the only source that rules on WHEN A PAGE BECOMES A FLOW, and it gates the exception
on research, not on taste.** Probe — <https://design-system.service.gov.uk/patterns/question-pages/>:
*"Asking just one question per question page helps users understand what you're asking them to do"* ·
*"Sometimes it makes sense to group a number of related questions on the same page. User research
will tell you when you can group pages together."* · *"If you need to ask for multiple related things
on a page, use a statement as the heading."* · *"Do not use the same page heading across multiple
pages."* The structural minimum is stated as a list — *"Question pages must include a: back link,
page heading, continue button"* — which is the shape of a machine-checkable page contract.

**9. Material's composition unit is a PANE with a declared size ROLE, not a tile.**
CLAIMED (search-result text; the m3 page is a JS-only shell and could not be quoted —
<https://m3.material.io/foundations/layout/canonical-examples/overview>): three canonical layouts
(list-detail, supporting pane, feed), each with compact/medium/expanded configurations; in
list-detail *the list should have a fixed width while the detail pane is flexible*. The transferable
idea is that **one member of a pair is declared fixed and the other declared flexible** — the
relation is authored, not left to content.

**10. Atlassian says the same thing as Polaris in one line, and adds size as a hierarchy signal.**
CLAIMED (search-result text, <https://atlassian.design/foundations/spacing>): hierarchy is ranked by
element size, and *varying the amount of whitespace around an element can be used to group elements
together or separate them*; spacing is built on an 8px base unit. Second-hand; not quoted from the
page body.

**11. NO mature design system publishes a bento or bento-grouping rule. Probe named, run twice.**
Probe A — open search `"bento grid" layout design guidance rules grouping tile sizes 2026`: every
result was an industry blog (orbix.studio, studiomeyer.io, digitalheroes, brainy.ink). Probe B —
the same query restricted to `carbondesignsystem.com, polaris-react.shopify.com, m3.material.io,
atlassian.design, design-system.service.gov.uk, designsystem.digital.gov`: **zero bento pages
returned**; the engine fell back to those systems' grid/spacing pages. Per
[[unmatched-grep-is-not-an-absence]] this is not proof of absence, but two probes agreeing is the
honest reading: the bento genre has no published standard, and Apollo's `s217`–`s220` bento canon is
ahead of the field rather than behind it. The blog corpus does converge on two claims worth naming
as **OPINION, blog-sourced, no primary standard**: (a) tile size encodes importance — *"the bigger
the tile, the more important the data inside it"*; (b) the common failure is *"sizing cells to fill
the canvas instead of sizing cells to fit what they hold"*
(<https://www.orbix.studio/blogs/bento-grid-dashboard-design-aesthetics>).

**12. The repo already carries composition rules — as ADVISORY prose that no gate reads.**
Probes: `knowledge/guidelines/accessibility-interaction-design.md:23` — *"ID-9 — group elements that
belong together (proximity): labels close to controls; form errors close to their fields; too much
whitespace confuses… responsive reflow must keep related content directly AFTER the section it
relates to"*; `knowledge/guidelines/neurodiversity.md:30` — *"Separate sections clearly: ≥20px
whitespace between sections"*; `knowledge/guidelines/accessibility-content-authoring.md:18-20` —
*"CA-2 — content order must be logical (SC 1.3.2 A)… [ADVISORY — composition-layer rule; DOM order =
reading order in canon, keep it that way when composing]"*. The index counts 470 rules split
ADVISORY 321 / BLOCKING 59 / REVIEW 34 / TASTE 56 (`knowledge/guidelines/_rules-index.json`,
`byDestiny`). Probe for the consumer: `grep -ln '_rules-index' knowledge/_validate_*.py` → **no
match**. So the composition rules exist, are already destiny-tagged, and **have no gate**. That is
[[instrument-without-a-consumer]] in its mirror form — a rule set without an instrument.

**13. The bento DIAL VOCABULARY has no seat for grouping. Measured.**
Probe: `grep -c 'group' knowledge/_render/_bento_edit_rails.json` → **0**. `grep -n
'row.unit\|row_unit\|rowUnit\|row-height'` on the same file → **0 matches**. The ten dials it does
carry are `spacing · mainSpacing · subSpacing · keylines · mode · edge · rounding · bentoBg · capBg`
plus the page rail — every one of them a *surface or spacing* dial. Meanwhile the grouping
vocabulary lives only in one snippet as three hardcoded classes:
`knowledge/snippets/Template-dashboard-bento.reference.html:737-739` —
`.c-bento.tpl-group-kpi{--bento-row-unit:196px;}` / `tpl-group-chart{380px}` /
`tpl-group-rail{184px}`, re-projected into `knowledge/canon/canon.css:17230-17232`. **The rails file
is the file the SKILL tells the agent to read** (`generate-from-canon/SKILL.md` rule 7: *"For bento,
grids and the layout dials, read one file"*), and grouping is not in it. An agent that obeys rule 7
literally cannot find a grouping rule — which is the mechanism behind the #233 "grouped by taste"
symptom, not a lapse of attention.

**14. The template meta file states the gap in its own words, and names it as Dave's.**
Probes, `knowledge/components/template-dashboard-bento.meta.json`: line 12 — *"HOW MANY groups a
dashboard has, and what belongs in each, is a product decision and is Dave's"*; and the
`$composesNote` (line 168) — *"`relationships` is a CLOSED shape in meta.schema.json (livesInside ·
mustNotNeighbour · commonPatterns · triggeredBy) and has no seat for 'the components this organism is
assembled from'. ⬛ THAT IS A REAL GAP FOR LAYER 2… composition is the defining edge of a template,
and the graph cannot currently express it."* Two different gaps sit here and they should not be
conflated: **(a)** the schema cannot express *what a template is made of* (`$composes` is a
workaround); **(b)** nothing anywhere expresses *when two things belong in the same group*. Only (a)
is written down as a gap.

**15. The graph CAN already express one composition rule, and one chart uses it.**
Probe: `knowledge/components/chart-line.meta.json` → `relationships.mustNotNeighbour` = *"A second
chart re-using these series colours for DIFFERENT data in the same journey (dv-014)"*; and
`knowledge/components/template-dashboard-bento.meta.json:90-93` — *"A second dashboard template on
the same page - a page has one overview"*. `mustNotNeighbour` is a **negative composition edge that
already exists and is already populated**. There is no positive counterpart (`shouldNeighbour` /
`groupsWith`), and `dropdown.meta.json`'s `mustNotNeighbour` is `[]` — most components leave it
empty.

---

## THE TEN CANDIDATE RULES, AS CHECKABLE CONDITIONS

Each is stated as a condition a page either satisfies or does not. "Gate could see" names the probe
an instrument would run; "eye only" names the residue that no instrument can settle. Nothing here is
proposed for adoption — the brief's DO-NOT-RULE stands.

| # | Rule, as a condition | What a gate could see | What only Dave's eye sees |
|---|---|---|---|
| **C1** | **Gaps strictly decrease with nesting depth.** For any container and its child container, `gap(child) < gap(parent)`; never equal. (Polaris, F1/F2) | Parse the composed HTML + resolved custom properties; walk the container tree; compare the resolved gap at each level. Both values are already tokens from `{1,2,4,16,24,40}`, so this is integer comparison, not measurement. Fails LOUD on `40/40` or `4/4`. | Whether the *chosen* rung is right — 40-over-4 vs 24-over-4 is a rhythm judgement, not a violation. |
| **C2** | **A group's members are uniform in kind.** Every direct child tile of one group is the same component type (or an explicitly declared mixed group). (Carbon: *"Do not mix different variants of tiles in groups"*) | Read the child tiles' scope classes (`.kpi-tile`, `.stat-card`, `.dv`) and assert one class per group, or an explicit `data-mixed="reason"` marker in the `data-bespoke` idiom canon already uses. | Whether a mixed group is *justified* — Carbon allows the case to exist, it just wants it deliberate. |
| **C3** | **Every group carries a name.** Each grouping container has an accessible name (`aria-label` / `aria-labelledby`) and, where visible, a heading in the right rank. (Carbon tile-group hierarchy + the template's own a11y block) | Assert `aria-label`-or-`labelledby` on every `.c-bento` that is itself a tile; assert heading rank monotonicity `h1 → h2 → h3` with no skips. The snippet already passes this (`aria-label="This month"` / `"Spending analysis"` / `"Position"`, lines 840/901/946). | Whether the name is a *good* one — "Position" vs "Your balances" is copy, not structure. |
| **C4** | **DOM order equals visual order.** No composed screen reorders content visually away from source order (no `order:`, no `grid-row-start` that inverts, no `flex-direction:*-reverse` on a content container). (WCAG 1.3.2; repo `aca-002`: *"DOM order = reading order in canon, keep it that way when composing"*) | Static: grep the screen's own `<style>` for `order:` / `*-reverse` / explicit `grid-area` placement. Rendered: compare DOM order against bounding-box top-then-left order under `--render`. | Whether an intentional reorder is the right call at one band. |
| **C5** | **Containment is not doubled.** A group that paints a surface does not also carry a keyline, and vice versa — one grouping signal per boundary. (NN/g F6/F7: containment overpowers proximity; borders "added in an abundance of caution" cause clutter) | Resolve the group's background against its parent's; if they differ AND a border/keyline is set, flag. Directly checkable against `bentoBg` + `keylines` in the rails, which already rules keylines OFF on every dashboard (`s219-D2(4)`). | Whether one signal reads *strongly enough* at that theme's contrast — the #231 `$awaitingDave` dark-ground collision (1.00:1) is exactly this, and it is already his. |
| **C6** | **A grouping surface never resolves to its parent's colour.** The group ground and the wall ground must differ by a stated minimum, or the group is not a group. (NN/g common region; the repo's own measured collision) | Resolve both grounds per theme × mode and compare — the repo already has the machinery (`_validate_dark_surfaces.py`, and the meta file records the measurement as *"byte-identical: 1.00:1"*). | The minimum itself (ΔL\*, or a ratio) is a value, and values are Dave's. |
| **C7** | **Section separation meets the whitespace floor.** ≥20px between sibling sections. (repo `neuro-003`, `knowledge/guidelines/neurodiversity.md:30`) | Resolve the outer gap; assert ≥20. Cheap, and already expressible on the ruled stop set (24 and 40 pass; 16 fails). | Whether 24 or 40 — see C1. |
| **C8** | **Related content stays adjacent through every band.** At each responsive band, a group's members remain contiguous; nothing is "dumped at page bottom". (repo `aid-004`/ID-9: *"responsive reflow must keep related content directly AFTER the section it relates to"*) | Render at each compiled band (1100/820/520 container px) and assert each group's children are contiguous in visual order. Needs the browser three — a `COULD-NOT-ASK` where playwright is absent, which the pack already reports honestly. | Whether the resulting single-column *order* is the right priority order. |
| **C9** | **Span vocabulary is legal at every band.** No tile takes a span that leaves an orphan column at a compiled band. (the template's own anti-pattern: *"Do not invent a span. Only 6 and 3 are square at every compiled band… A `data-c="2"` tile leaves one column empty at the 3-column band, and no gate sees it"*) | Enumerate `data-c` values against the compiled column counts and flag any that do not divide. This is arithmetic and the meta file states that **no gate sees it today**. | Nothing — this one is fully mechanical, and its absence is a hole rather than a judgement. |
| **C10** | **Metric budget declared.** A dashboard states how many primary metrics it carries, and the number is inside a declared band. (Carbon: *"Limit the number of metrics"*) | Count KPI-class tiles; compare to a declared ceiling. Trivially checkable — but **the ceiling is a value nobody has ruled**, so today the gate could only report the count, not judge it. | The ceiling itself. Secondary sources attribute "5–7" to NN/g; I could not reach a primary NN/g page saying so (see UNPROVEN). |

**Eye-only, and honestly so** — these came up in the sources and I list them separately rather than
dressing them as conditions, because a rule that sounds checkable but isn't wastes the next lane:
**(E1)** *"The most important data should have the highest contrast and occupy the largest area"*
(Carbon) — importance is not in the markup. **(E2)** F-pattern placement (Carbon) — reading-order
priority is a product decision. **(E3)** "Does this group read as one thing?" — the perceptual
question C5/C6 only approximate. **(E4)** Whether a tile's spare space is *"sometimes desirable"*
padding or a dead band — Dave's own words at #233, and the reason three renders are owed.

## WHAT A WHEN-TO-GROUP RULE WOULD SAY FOR A KPI/CHART/RAIL BENTO

Reading the sources back rather than inventing: **no mature system groups by content type.** Carbon
groups by *"strong relationship"* and *"similar hierarchical importance"*; Polaris groups by *"content
that shares purpose"* and *"similar concepts and actions grouped together in cards"*; GOV.UK groups
questions that are *"closely related"*, with research as the arbiter. In every case the grouping
criterion is a **shared reason for looking**, and the *uniformity* (same variant, same tile height,
same chart layout) is the **consequence** of having grouped, not the cause.

That inverts the pack's current vocabulary. `tpl-group-kpi` / `tpl-group-chart` / `tpl-group-rail`
name three *content types*, so an agent reading the class names infers "put the KPIs together
because they are KPIs". A source-faithful rule would instead read, in shape:

> A group exists when its members answer **one question** the user came with, and every member of a
> group is the same kind of thing at the same level of importance. If members differ in kind, they
> are two groups. If a would-be group has one member, it is not a group — it is a module. A group
> gets exactly one containment signal (surface **or** keyline, never both) and one accessible name,
> and its members stay contiguous at every band.

Note what that rule does NOT settle, and must not pretend to: **how many groups a dashboard has and
what belongs in each** is already written down as Dave's
(`template-dashboard-bento.meta.json:12`). The rule above is a *shape* constraint; the
*membership* is product. The three drawn groups are also explicitly a demonstration, not a canon —
same file, line 12: *"Three sub-bentos are drawn… because three is the smallest number that shows a
full-width group AND a side-by-side pair."*

Two further conditions fall out of the sources and belong in any such rule:
- **A stop condition.** NN/g's false-floor and clutter warnings mean "group harder" is not
  monotonically better. The published counter-rule is: if proximity alone already reads, do not add
  a boundary.
- **A one-member carve-out.** The chart group in the shipped snippet holds exactly one module
  (`Template-dashboard-bento.reference.html:901-907`). Under Carbon's framing that is a tile, not a
  tile group. Whether Apollo wants the wrapper anyway — for the row-unit seat it carries — is a
  question, not a defect, and it is listed below.

## ROW-HEIGHT AND TILE-SIZING: WHAT OTHERS DO — REPORT ONLY

⛔ **No recommendation is made here.** Dave's ladder is FLOATED (`#233`, his words: *"not saying
this is correct"*), three renders are owed, and this section exists so those renders can be framed
against what exists elsewhere.

**Four published models, and one hybrid already in canon:**

1. **Fixed unit (uniform).** Carbon's *standard* layout: *"tiles are the same in height and width as
   all other tiles in the group."* Simplest, and the only model under which a span vocabulary is
   fully legible. Apollo measured the same thing independently at `#217` (intrinsic rows kill the
   span vocabulary — recorded in `canon.css:1089-1090`: *"⚠ FIXED rows. With intrinsic rows the
   tallest content sizes every row and the span vocabulary renders invisible (MEASURED #217,
   Foundations photography bento)"*).
2. **Content-sized with a FLOOR.** Carbon's tile sizing: *"Tile height varies depending on the
   content placed within it… The minimum tile height is a 2:1 aspect ratio."* The floor is expressed
   as an **aspect ratio**, not a pixel unit — worth noting, because an aspect-ratio floor is
   width-responsive where a px floor is not.
3. **Per-row uniformity (masonry).** Carbon's two masonry layouts: vertical masonry varies height at
   constant width; horizontal masonry allows *"different rows of tiles may vary in height, but tiles
   within a row should be consistent in height."* The consistency unit is the **row**, not the wall.
4. **Declared fixed/flexible roles per pane.** Material's list-detail: one pane declared fixed-width,
   the other flexible (CLAIMED — search text, page not quotable). The sizing is an authored property
   of the *slot*, not of the content.
5. **The hybrid canon already ships.** `knowledge/canon/canon.css` — a top-level bento grid uses
   `grid-auto-rows:var(--bento-row-unit)` (line 1091, fixed), while a **nested** bento uses
   `grid-auto-rows:minmax(var(--bento-row-unit),1fr)` (line 1124) with the comment
   *"`minmax(<unit>,1fr)` keeps the row unit as the FLOOR — the fixed-row discipline that makes the
   span vocabulary visible is untouched, rows only grow when the parent has already stretched the
   container past its content."* Concretely, in the shipped dashboard the outer wall sets
   `--bento-row-unit:auto` (`canon.css:17225`) while the three groups set literals 196px / 380px /
   184px (`canon.css:17230-17232`). **So "fixed vs floor" is not an open choice between two futures —
   both are already in the file, at different levels, and one of them is already `auto`.** Any
   render matrix that shows "fixed" and "floor" as alternatives should say which *level* it is
   varying, or it will compare two things that both already ship.

**One blog-sourced idea, labelled OPINION:** the bento corpus treats tile size as an *encoding* —
bigger tile = more important — which would make the row unit a semantic choice rather than a layout
one. No standards body says this. (<https://www.orbix.studio/blogs/bento-grid-dashboard-design-aesthetics>)

## RULING-SHAPED QUESTIONS

⛔ Per the brief's DO-NOT-RULE, these carry **no recommendation** — the template's "recommend (x)"
clause is overridden for this lane. Options are priced; the pick is Dave's.

1. **Does grouping become a DIAL, a RULE, or an EDGE?** (a) a dial in
   `_bento_edit_rails.json` — one file, the file the skill already sends the agent to, but the rails
   file is GENERATED (`$do_not_edit`, `gen_bento_matrix_217.py --rails`) so this is a generator
   change; (b) a rule in `generate-from-canon/SKILL.md` beside rule 7a — cheapest, but prose an
   agent can skim, which is the #233 failure mode repeating; (c) a positive edge in the meta schema
   (`groupsWith` / `sharesGroupWith`) beside the existing `mustNotNeighbour` — most durable and
   gate-able, but a **schema change**, which `template-dashboard-bento.meta.json:154` already records
   as Dave's.
2. **Is `tpl-group-kpi/-chart/-rail` kept as content-type names, or re-cut as role names?** The
   sources group by shared question, not by content type (see the WHEN-TO-GROUP section). Renaming
   touches one snippet, canon's projection and any downstream copy; keeping costs nothing today but
   keeps teaching the agent the taxonomy that produced the taste-grouping.
3. **Is a one-member group legal?** The shipped chart group has one module. Carbon's framing says
   that is a tile, not a group; Apollo's construction needs the wrapper for the row-unit seat. Option
   (a) legal, documented as a deliberate carve-out; (b) illegal, and the row unit moves to the tile.
4. **Which of C1–C10 is worth an instrument at all?** C9 (span legality) is pure arithmetic and the
   meta file already states no gate sees it. C1 (gap ladder) is integer comparison on a ruled stop
   set. Both are cheap; neither is ruled, and "which gate first" is expressly outside this lane.
5. **Do the 470 destiny-tagged guideline rules get a consumer?** `grep -ln '_rules-index'
   knowledge/_validate_*.py` returns nothing: 59 BLOCKING rules sit in an index no gate reads. Wiring
   even a subset is a build lane with a real price; leaving it is a standing
   [[instrument-without-a-consumer]].

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** the "5–7 primary metrics" ceiling in **C10**. Every source stating it is a secondary
  blog attributing it to NN/g; no primary NN/g page was reached that says it. Price to prove: 1–2
  targeted fetches of NN/g dashboard articles (~4–6K tk), or drop the number and let C10 report the
  count only.
- **CLAIMED (not re-read from the artefact):** all Material Design 3 findings (F9) and the Atlassian
  spacing findings (F10). `m3.material.io/foundations/designing/flow` returned *"This website
  requires JavaScript"* with no body; the canonical-layouts and Atlassian claims rest on
  search-result text, not quoted page bodies. Re-read costs a browser-backed fetch (~5K tk plus the
  render dependency the pack already documents).
- **UNPROVEN:** that C1–C10 would actually **bite** on the #233 output. Nothing here was run against
  the failing artefact — the proving zip is recorded as VANISHED in memory, and this lane is
  read-only besides. Price to prove: regenerate a page and drive each candidate condition over it
  (one render lane, ~15–25K tk). Until then every "a gate could see" is a design claim, not a
  measurement — [[mutation-tests-the-clause-not-the-feature]] applies: none of these clauses has been
  driven.
- **UNPROVEN:** the absence in F11 ("no mature system publishes a bento rule"). Two probes agree, but
  a search engine is not an index of a documentation site. Price to prove properly: site-search each
  of the six systems directly (~6 fetches, ~10K tk).

## Evidence

No evidence files: every claim above quotes its probe inline — a URL with the quoted sentence, or a
repo path with a line number. The `assets/` folder for this report was not created, deliberately: an
empty asset directory reads as evidence that evaporated.

## WHAT APPLIES TO A FACTORY

A codebase-shaped rule says "here is the right layout". A factory cannot use that, because the
factory does not know the content. What transfers is the shape mature systems actually publish: a
**relation that must hold between a parent and its children**, stated over a vocabulary the system
already owns. Polaris does not say "use 16px"; it says the inner gap is smaller than the outer one,
always. Apollo already has the vocabulary — six ruled spacing stops, a role set, a span set, a
theme set — so the missing layer is not values, it is *relations over those values*. That is the
form a composition rule should take here, and it is why grouping keeps escaping the meta schema:
the schema describes components one at a time, and every rule in this report is about a **pair**.
Second: uniformity is a consequence of grouping, never its cause — a factory that groups by content
type will produce the #233 output every time, because the agent has been handed the wrong criterion.
Third: the factory's real quality bar is the one Carbon states in one line — *"all charts should use
the same layout and spacing"* — because sameness across a page is the only thing a generator is
inherently better at than a person, and the only composition property that is cheap to check.
Finally: every rule here has a stop condition. A factory that only knows how to add structure
produces a page of boxes; NN/g's false floors are what that looks like from the user's side.

REPLAY-THESE: `https://polaris-react.shopify.com/patterns/card-layout` (~7,000 tk — the gap ladder in full, the one directly transplantable rule) · `https://carbondesignsystem.com/components/tile/usage/` (~5,000 tk — the three layout models + the tile-group contract) · `knowledge/components/template-dashboard-bento.meta.json` (~5,000 tk — `$composesNote`, `$bentoGrammar`, `$awaitingDave`) · `knowledge/canon/canon.css` lines 1055–1135 + 17225–17232 (~1,200 tk — the fixed/floor hybrid as it actually ships) · `knowledge/_render/_bento_edit_rails.json` (~10,000 tk — only if the grouping-as-a-dial option in question 1 is live)
