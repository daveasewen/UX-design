# `#245`-`L3` — the COMPOSITION EDGE (`s234-D4`): schema fragment, population proposal, derived dial, arithmetic gate, rename dry-run — built for Dave's eye, populating nothing

session: `#245` · 2026-09-03
window: lane L3 of the v1.0.6 brief (`notes/_briefs/2026-09-02-234-v106-brief.md` § L3) — one Fable sub, parallel to the other #245 lanes
sub index: `L3`
brief: `notes/_briefs/2026-09-02-234-v106-brief.md` (§ L3) — the lane brief itself was in-chat; no `notes/_briefs/` file was cut for it
tokens: `UNMEASURED — no message.usage at a sub's seat`. Shape for the conductor's ledger: ~45 tool calls;
four whole-file reads (the L2 report, the rB report, the v1.0.6 brief, the template meta), the L2 surface
read to line 200 + its section index, the live schema in two slices, the rails generator in four slices
(never whole — 4,366 lines), the snippet in five slices; the 68 KB surface was GENERATED and probed (16
theme × mode × width states), three PNGs looked at by eye; two playwright runs.

**I READ, first:** `_REVIEW-L2-behaviour-address-2026-09-02-v1.html` (structure, head, §01–02, nav/theme
script) · `notes/_subreports/2026-09-02-238-B-L2-behaviour-address.md` (whole) ·
`notes/_briefs/2026-09-02-234-v106-brief.md` § L3 (whole file) ·
`notes/_subreports/2026-09-02-234-rB-composition-rules.md` (whole, **including its REPLAY-THESE line**:
the Polaris and Carbon pages were NOT re-fetched — the gap-ladder and tile-group relations are taken from
rB's quoted text; the template meta's `$composesNote` / `$bentoGrammar` / `$awaitingDave` were read in
full; `canon.css` 1055–1135 was read via the snippet's byte-identical AUTO-BENTO copy at lines 306–385
plus `canon.css:536`; `_bento_edit_rails.json` was walked by key, not read whole) ·
`knowledge/_rulings.json` → `s234-D4` verbatim · `template-dashboard-bento.meta.json:154` verbatim ·
`notes/_subreports/_TEMPLATE.md`.

## VERDICT

**All six brief deliverables DONE as PROPOSALS; nothing live was written; the gate bites on six
mutants and, driven on the real artefact, found a defect by refusing.** (1) `groupsWith` is a one-line,
by-addition fragment beside `mustNotNeighbour` at `meta.schema.json:216` in the `#/definitions/edge`
form; 136/136 live metas validate against the live AND the proposed schema, the 6 proposal-applied metas
validate against the proposed schema and are RED against the live one (so the change is required, not
decorative); 6 planted mutants red, 3 controls green. (2) The population is 8 edges across 6 meta files
(the template + 5 member components), 4 with a resolved `ref`, **4 `ref:null`** each naming what Dave
must settle; every `$note` carries the artefact line it was measured at. (3) `rails_from_edge.py`
imports the live generator's own `edit_rails()` and derives a `grouping` dial from the proposed edges —
the live rails file and the generator hash identically before and after, and `--rails --out <tmp>` still
equals the file on disk. (4) `check_composition.py` (C9 span legality + C1 gap ladder, arithmetic read
off the artefact's own CSS) has a 10-arm selftest, 0 failed; on the real snippet it returns **UNPROVEN,
exit 77** because the snippet never declares its base column count — and the render probe shows the
consequence: **at 1440 the KPI board stacks 4×1 where the snippet's own comment says 2×2** (finding 5).
(5) The rename is a grep-before of 27 files / 234 occurrences with a dry-run plan; nothing renamed;
the floated words collide with nothing. (6) Rule 7b is drafted on the surface only.
`_REVIEW-L3-composition-edge-2026-09-03-v1.html` (68,723 B, repo root, GENERATED from the lane's files)
inlines `type.css` verbatim, has zero external refs, and renders 16/16 states (4 themes × light/dark ×
1440/390) with `scrollWidth == clientWidth` and `console_errors []`.

**Two things the conductor must not skim.** (a) Finding 5 is not this lane's to fix (a live snippet edit
+ the ordered regen serial) but it is a real defect in the file rule 7a tells every agent to splice, and
both `template-dashboard-bento.meta.json` `$tokenGaps` and the #231 report's FINDING 4 state the
opposite of what the file contains. (b) The derivation from the graph yields 3 components but the
artefact draws 3 groups that are NOT those 3 — the module-level `stat-card` self-edge and the
content-level `summary ↔ status-indicator` edge describe ONE drawn group, and a graph without a group
identity cannot say so. That is question 7 and it decides which level the edge lives at.

COUNTS: findings `12` · ruling-shaped `7` · UNPROVEN `4`

## What was done

**Probe first (brief's precondition).** `grep -rn groupsWith knowledge/components/ | wc -l` → **0**
(also 0 in `meta.schema.json`). Confirmed before any file was written.

**Region 1 — the schema fragment.** `knowledge/_tmp/l3-245/apply_schema.py` — text surgery on ONE anchor
(the `mustNotNeighbour` line inside `edges.properties`), refuses unless found exactly once,
`Draft7Validator.check_schema` before writing. Wrote `groupsWith.schema.fragment.json`,
`meta.schema.proposed.json`, `meta.schema.proposed.diff` (**+1 / −0 lines**, anchor at live line 216).
Live schema sha256 `ad04fcc16e4d98c9…` before and after. The shape: `"groupsWith": {type: array, items:
{$ref: "#/definitions/edge"}, description: …}` — the closed `{ref: <node-id>|null, $note}` form every
other edge uses. ⛔ `knowledge/components/meta.schema.json` untouched (line 154 quoted on the surface:
*"if Dave wants a first-class `layer` field for the Layer-2 artefact class, that is a SCHEMA change and
is his, not a worker lane's."*).

**Region 2 — the population PROPOSAL.** `build_population.py` measures the groups off the REAL snippet
(comments stripped, `<main>` only): 3 `<section class="… tpl-group-*">`, 7 tiles, shared question = each
section's `aria-label` ("This month" · "Spending analysis" · "Position"). Proposed edges
(`population-proposal.json`):

| meta file | `groupsWith.ref` | why |
|---|---|---|
| `kpi-tile` | `component:kpi-tile` | 4 Kpi-tiles, one question — a SELF-edge (uniform in kind, rB C2) |
| `stat-card` | `component:stat-card` | 2 Stat-card modules in "Position" |
| `chart-bar` | `null` | one-member group — rB Q3, Dave's |
| `summary` | `component:status-indicator` | content level of "Position" |
| `status-indicator` | `component:summary` | the mirror |
| `template-dashboard-bento` | `null` ×3 | one per drawn group; a GROUP is not a node in the grammar |

`schema-arms.txt`: live 136/136 (LIVE) · 136/136 (PROPOSED) · applied 6/6 GREEN (PROPOSED) · 6/6 RED
(LIVE) · 4/4 refs resolve to an existing meta · mutants M1–M6 red · controls K1–K3 green · **13 arms, 0
red**. `EXAMPLE-button.meta.json` is the 137th file and is RED against the LIVE schema on its own
(`tokenValidation` required) — pre-existing, excluded exactly as L2's `schema_arms.py` excluded it.
⛔ No `knowledge/components/*.meta.json` written (`git status --short knowledge/components` → empty).

**Region 3 — the grouping dial, dry run.** `rails_from_edge.py` imports `gen_bento_matrix_217`
(untouched — sha256 `b06b7929…` before and after), applies the proposal IN MEMORY over the live metas,
derives groups as connected components of the `groupsWith` graph over the template's `$composes`
members, and writes `_bento_edit_rails.proposed.json` (42,896 B): the live `edit_rails()` dict + ONE
dial `dials.grouping` (`kind: derived`, `control: none`, `groups` ×3, `unresolved` ×4 by name,
`role_names.status: FLOATED`) + `grouping` appended to `types.dashboard.dials`. Proof
(`rails-from-edge.txt`): live rails sha256 `e55922e0…` before = after · generator default path ==
disk (byte-identical) · `--rails --out <sandbox tmp>` == disk · proposed minus the addition == live
generation. **The generator was not touched, so no new flag exists; the dry run IS the proposal for
what `--rails-from-edge` would emit.**

**Region 4 — the gate.** `check_composition.py <artefact>` / `--selftest`. Reads bands and span clamps
off the artefact's `@container` blocks; resolves each `.c-bento`'s `--bento-gutter` by matching the
page's own rules against the page's own DOM (class/attribute/`:has(> .a > .b)` compounds, ancestor
chain, specificity-ranked, unsupported selectors SKIPPED and counted). Exit 0 green · 1 red · 77
UNPROVEN. `drive-real-artefact.txt`: C9 4 grids / 10 tiles at 3 bands (≤1100=3, ≤820=2, ≤520=1) all
whole rows; C1 wall 40px ← `.tpl-page .c-bento.tpl-wall[…]:has(> .c-bento__grid > .c-bento)`, groups
4px ← `.tpl-page .c-bento.tpl-group[…]`, 3 nested pairs, 4 < 40 ✓; **UNPROVEN: base band — the artefact
never declares `--layout-bento-columns:<n>`**. `selftest-check-composition.txt`: **10 arms, 0 failed** —
R (real artefact → 77), K0 (fixture with the literal → 0), M1 data-c 3→2 (C9), M2 3→6 (C9 row-sum,
base band only), M3 group gap 4→40 EQUAL (C1), M4 wall 40→4 (C1), M5 4→5 off-stop (C1), M6 inverted
ladder on stops (C1), K1/K2 controls. ⛔ Registered in no gate list.

**Region 5 — the rename, dry run.** `rename_dryrun.py` → `rename-grep-before.txt` (every file, per-name
counts, classified) + `rename-plan.json` (would_edit 1 · would_regenerate 2 · never_touch 21 ·
conductor_by_addition 3 · steps_if_ruled 5). ⛔ Nothing renamed.

**Region 6 — rule 7b.** Drafted on the surface §08 and in finding 11 below. ⛔ No `SKILL.md` edited.

**The surface.** `build_review.py` → `_REVIEW-L3-composition-edge-2026-09-03-v1.html` (sha256
`2755b6e898e653ff…`). Sections: 00 flag/header · 01 answer + stats · 02 the edge (fragment · diff ·
arms) · 03 the population (schematic · measured groups · the 8) · 04 the dial (proof · excerpt) · 05 the
gate (probe table · drive · selftest) · **06 ruling-shaped questions (7, options priced, one
recommendation each)** · 07 rename · 08 rule 7b · 09 consequences (8 cards, owners). Themes: the canon's
own `[data-apollo-theme]` + `[data-theme]` on `<html>`, per-theme grounds/inks READ via
`gen_bento_matrix_217.resolve_token` (`theme-tokens.json`); two-red law `#DA1A00` on white, `#F6604C`
else. `render-review.json`: 16 states, overflow 0, console errors 0.

**Row.** `knowledge/_REVIEW-SIGNOFF.md` — one row appended at the tail, AWAITING Dave.

### FILES TOUCHED (for the reconcile)

| path | state |
|---|---|
| `_REVIEW-L3-composition-edge-2026-09-03-v1.html` | NEW — generated, 68,723 B |
| `knowledge/_REVIEW-SIGNOFF.md` | one row appended |
| `knowledge/_tmp/l3-245/` (36 files) | NEW — scratch: scripts, proposals, transcripts, PNGs |
| `notes/_subreports/2026-09-03-245-L3-composition-edge.md` + `assets/…/` (28 files) | NEW — this report + evidence |

⛔ Not touched: `knowledge/components/meta.schema.json` · every `knowledge/components/*.meta.json` ·
`knowledge/_render/gen_bento_matrix_217.py` · `knowledge/_render/_bento_edit_rails.json` ·
`knowledge/snippets/Template-dashboard-bento.reference.html` · `knowledge/canon/*` · every `SKILL.md` ·
every gate list · `_build_all.py` (not run) · memory · git (no commit).

## Findings

**1 — THE EDGE DOES NOT EXIST TODAY, ANYWHERE.** Probe: `grep -rn groupsWith knowledge/components/` →
0 lines; `grep -c groupsWith knowledge/components/meta.schema.json` → 0. `mustNotNeighbour` (the
negative twin) is populated on 3 of the 6 files in scope (`stat-card`, `chart-bar`,
`template-dashboard-bento`).

**2 — THE CHANGE IS REQUIRED, NOT DECORATIVE.** `edges` is `additionalProperties:false`
(`meta.schema.json:211`), so a `groupsWith` key on any live meta today is RED. Probe: `schema-arms.txt`
arm C — 6/6 proposal-applied metas RED against the LIVE schema, 6/6 GREEN against the PROPOSED.

**3 — THE ARTEFACT DRAWS 3 GROUPS / 7 TILES / 5 MEMBER COMPONENTS, AT TWO LEVELS.** Probe:
`population-proposal.json` → `groups_measured`: "This month" (`data-c=6`, 4 × `kpi-tile` at 3),
"Spending analysis" (3, 1 × `stat-card` at 6 carrying `chart-bar` ×1), "Position" (3, 2 × `stat-card` at
6 carrying `summary` ×1 + `status-indicator` ×3). The MODULE (`kpi-tile`, `stat-card`) is what the bento
places; `chart-bar`, `summary`, `status-indicator` ride inside a module.

**4 — THE GRAPH DERIVES 3 COMPONENTS THAT ARE NOT THE 3 DRAWN GROUPS.** Probe: `rails-from-edge.txt` →
`derived groups: 3 (component:kpi-tile; component:stat-card; component:status-indicator +
component:summary)`. The second and third are ONE drawn group ("Position") at module and content
level. Without a group identity in the node grammar the derivation cannot merge them; with edges at
one level only it would not need to. → question 7.

**5 — ⛔ THE SNIPPET NEVER DECLARES ITS COLUMN COUNT OR PACKING, AND ITS META SAYS IT DOES.** Probes:
`grep -c -- '--layout-bento-columns\s*:' knowledge/snippets/Template-dashboard-bento.reference.html` →
**0**; same for `--layout-bento-packing\s*:` → **0**; the only occurrences are the reads at lines 309 /
313 (`--bento-columns: var(--layout-bento-columns)` etc.). `template-dashboard-bento.meta.json`
`$tokenGaps[0]`: *"The value is declared as a literal 6 with this note"* — it is not; #231 report
FINDING 4: *"Both are declared as literals in the file with the reason attached"* — they are not.
Consequence, MEASURED (`render-probe.json`, playwright `file://`, the seat's runbook recipe): at 1440 as
shipped, `--bento-cols-now` and `--layout-bento-columns` resolve EMPTY, `grid-auto-flow` is `row` (not
`row dense`), the wall shows 6 tracks that are **implicit** (created by the span-6 tile) and **the KPI
board stacks 4×1 — four tiles at 1376 × 196** — where the snippet's own comment (line 838) says *"2x2 at
six columns"*. With `--layout-bento-columns:6` declared in both theme blocks (fixture, sandbox scratch
only): `--bento-cols-now=6`, KPI board 2×2 at 686 × 196. Under the bands (≤1100) both behave alike
because each band rewrites `--bento-cols-now`. The canon projection is unaffected (`canon.css:536`
declares `--layout-bento-columns: 6` at root), which is why the #231 four-theme renders — taken from
the projected block — did not show it. **Owner: a repair lane (snippet edit + ordered serial); not
Dave's, not this lane's.** Price: two literals (or the `_unitless()` one-liner #231 priced) + the
serial, ~2K tokens.

**6 — THE GATE REFUSED RATHER THAN ASSUME 6, AND THAT IS WHAT FOUND FINDING 5.** Probe:
`drive-real-artefact.txt` last line — `check_composition: UNPROVEN … unproven 1`, exit 77. A gate that
defaulted the base column count to 6 would have gone green on the as-shipped artefact.

**7 — ONE MUTANT ONLY BITES AT THE BASE BAND.** M2 (a KPI tile 3→6: 3+3+3+6 = 15, not a multiple of 6)
is legal at 3/2/1 columns after clamping, so on the as-shipped artefact it cannot be caught. Probe: the
selftest drives M1–M6 on the FIXTURE (literal declared) and the real artefact separately (arm R). Until
finding 5 is repaired, C9's whole-row clause is blind at the widest band on this snippet.

**8 — C1 RESOLVES 40 / 4 / 4 / 4 FROM THE PAGE'S OWN RULES.** Probe: `drive-real-artefact.txt` — wall
40px via the (0,6,0) `:has()` rule, groups 4px via the (0,4,0) rule; 7 `--bento-gutter` rules in the
`<style>`, 3 nested pairs compared, all strictly decreasing, all on the stop set. Matches the meta's
`$bentoGrammar.mainSpacing/subSpacing` (40 / 4) — read, not assumed.

**9 — THE RENAME REACHES 27 FILES / 234 OCCURRENCES, OF WHICH 1 IS SOURCE AND 2 ARE GENERATED.**
Probe: `rename-grep-before.txt` — kpi 144 · chart 42 · rail 48. Source:
`knowledge/snippets/Template-dashboard-bento.reference.html` (6). Generated: `knowledge/canon/canon.css`
(3), `knowledge/_memento-index.json` (29). `_CARRIES.md` carries 23 `tpl-group-kpi` (conductor state).
The rest are history/rulings/review pages/scratch. Floated `-lead/-evidence/-context`: 0 collisions
outside this lane's scratch. `showroom/` carries none of the three names (0 files).

**10 — THE RAILS GENERATOR'S DEFAULT PATH IS BYTE-IDENTICAL TO DISK, BEFORE AND AFTER.** Probe:
`rails-from-edge.txt` — rails sha256 `e55922e004e7237a…` unchanged, generator `b06b792951c40fb7…`
unchanged, `rails_json() == open(RAILS_PATH).read()` True, CLI `--rails --out <tmp>` == disk True.
(A failed first run left `knowledge/_tmp/l3-245/_rails.live-cli.json` — the mount refuses `os.remove`;
overwritten with a 302 B note saying so.)

**11 — RULE 7b, PROPOSED TEXT (not written into any SKILL.md):**

```
7b. **Grouping comes from the graph, not from the class name.** Whether two modules share
    a group is a fact stored ONCE, as an `edges.groupsWith` entry in the member's
    `knowledge/components/<slug>.meta.json` (the positive twin of `mustNotNeighbour`). The
    rails' `grouping` dial and this rule are DERIVED from it and never restate it. A group is
    members that answer ONE question the user came with — never "the KPIs, because they are
    KPIs"; its members are uniform in kind, carry one accessible name and one containment
    signal, and stay contiguous at every band. Read the edge before you draw a `<section>`;
    where the edge is `ref:null` the grouping is undecided and is a Gap, not a guess. HOW MANY
    groups a screen has, and what belongs in each, is the designer's product decision — never
    yours (template-dashboard-bento.meta.json:12).
```

**12 — THREE OF THE FOUR DARK LEGS ARE BYTE-IDENTICAL IN THE STORE.** Probe: `theme-tokens.json` —
mono/legacy/console dark all resolve `--background-default #1A1A1A · --text-default #FFFFFF ·
--border-subtle #808080 · --surface-subtle #1F1F1F`; only supercharge differs (`#2A2621` / `#524842` /
ink `#F7F6F4`). Hence two of the review PNGs (`mono-dark`, `console-dark`) are the same 97,243 B. Not a
defect of this page; named so nobody thinks the switcher is broken. Supercharge LIGHT ground is
`#F7F6F4`, not white, so it takes `#F6604C` under the two-red law's literal reading (on-white / else).

## RULING-SHAPED QUESTIONS

⛔ Five of these are on Dave's do-not-rule list (the words · the schema change · one-member legality ·
the 470 rules · the row-height model). They are put back as questions; the recommendation the brief
asks for is a recommendation, not a ruling, and Q6 deliberately recommends no pick.

1. **The three role WORDS.** (a) `-lead` / `-evidence` / `-context` — floated; 0 collisions; (b) keep
   `-kpi/-chart/-rail` — free today, keeps teaching the content-type taxonomy that produced the #233
   grouping; (c) other words — same price as (a). Price of (a)/(c): 1 source file (6 occurrences), 2
   regenerated files, the ordered serial. **Recommend (a)**, on rB's finding that no mature system
   groups by content type.
2. **The schema change itself.** (a) apply the fragment as proposed — `groupsWith` in the closed
   `{ref,$note}` form, +1 line at `meta.schema.json:216`, 136/136 live metas already pass; (b) widen the
   edge form with a `group`/`role` field — carries the shared question as data but re-opens the closed
   form for all 12 edge types; (c) do not add it — grouping stays a class name in one snippet.
   **Recommend (a)**; the shared question rides in `$note` until Q7 settles the grammar.
3. **One-member group legality (rB Q3).** (a) legal, a declared carve-out — the edge stays `ref:null`
   with the reason, the wrapper keeps its row-unit seat; (b) illegal — row unit moves to the tile, the
   `<section>` goes, C2/C3 read the module. **Recommend (a)**: nothing changes in the snippet; (b) is a
   snippet edit + serial and touches the row-height model (L4's, Dave's).
4. **Which composition condition gets an INSTRUMENT (rB Q4).** `check_composition.py` bites (10 arms, 0
   failed) and is registered nowhere. (a) ADVISORY in `_validate_screen.py`'s chain; (b) BLOCKING for C9
   (no eye-only residue) + advisory C1; (c) leave unregistered. **Recommend (b)** — and note it already
   refuses honestly (exit 77) where the artefact does not declare its columns.
5. **Wiring the 470 destiny-tagged guideline rules (rB Q5).** `grep -ln '_rules-index'
   knowledge/_validate_*.py` → nothing. (a) not now, carried; (b) a subset — the composition-class rules
   (`ID-9`, `neuro-003`, `CA-2`) as C7/C8/C4 arms of this same gate, ~3 arms, ~2K tokens; (c) all 59
   BLOCKING, a build lane. **Recommend (b)**.
6. **The row-height model.** (a) fixed at every level; (b) the canon hybrid as shipped (fixed wall,
   `minmax(unit,1fr)` floor inside a group); (c) content-sized with an aspect-ratio floor (Carbon).
   **Recommend NO PICK here** — L4's renders (`reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html`) are the
   surface for this; the grouping edge names members, not heights, and is indifferent to the model.
7. **Which LEVEL carries the edge, and does a group need an identity?** Finding 4: the derivation yields
   `stat-card` and `summary + status-indicator` as two components for one drawn group; 4 of 8 proposed
   edges are `ref:null` because a group is not a node. (a) module level only — edges on `kpi-tile` and
   `stat-card`, content edges dropped (6 edges), groups derive cleanly, "Summary beside Status-indicator"
   is lost; (b) both levels as proposed — 8 edges, a consumer must know two edges can name one group;
   (c) add `group:<slug>` to the node-id grammar — every edge resolves, the template's 3 `ref:null`
   become refs; a grammar change touching `#/definitions/edge`'s pattern and `gen_kg_edges.py`.
   **Recommend (a) now, (c) when the grammar is next opened**: the module IS the component the bento
   places, and rule 7b reads the tile's meta.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: the regen serial and the gate roster with the schema fragment applied.** Nothing live was
  changed, so nothing was regenerated; `_build_all.py` is forbidden to a sub and was not run. What IS
  established: 136/136 live metas pass the proposed schema in memory. Price: the conductor's ordered
  serial at apply time (L2's fragment queues for the same act — one sitting, two hunks).
- **UNPROVEN: that the canon-projected `.cn-template-dashboard-bento` is free of finding 5.**
  `canon.css:536` declares the literal at root, so the projection *should* column correctly; it was not
  rendered here. Price: one render of the showroom/projection page, ~1K tokens.
- **UNPROVEN: that `check_composition.py`'s CSS matcher generalises past this artefact.** Driven on one
  real snippet + 9 derived arms. Selectors it cannot match are skipped and counted, never guessed, so a
  page whose gutter arrives only through such a rule reads UNRESOLVED (77), not green. Price: drive it
  on `Template-dashboard.reference.html` and one generated dashboard page, ~2K tokens.
- **UNPROVEN: the one-member-group and level questions have a "right" shape** — the 4 `ref:null` edges
  are declared gaps, and the proposal deliberately carries both levels so Dave can see the ambiguity
  rather than have it resolved for him. Price: his word on Q3 and Q7; then ~500 tokens to re-cut the
  proposal file.
- **CLAIMED — none.** Every figure above is from a probe in this window: `schema-arms.txt`,
  `population-proposal.json`, `rails-from-edge.txt`, `drive-real-artefact.txt`,
  `selftest-check-composition.txt`, `render-probe.json`, `rename-grep-before.txt`, `render-review.json`,
  `theme-tokens.json`. The rB relations (gap ladder, tile-group uniformity) are quoted from rB's report,
  not re-fetched — that is the declared skip of its REPLAY-THESE web items.

## PITFALLS (consequences replayed)

| # | what could go wrong | owner |
|---|---|---|
| 1 | Finding 5 is repaired by someone "fixing the meta text" instead of the snippet — the file would still stack 4×1 | repair lane: fix the FILE, then the meta reads true |
| 2 | The fragment is applied without L2's in the same sitting — two schema hunks, two serials | conductor |
| 3 | A consumer reads `ref:null` as "no group" and goes green on the undecided | whoever writes the consumer |
| 4 | The rename is run with `sed -i` across the repo and rewrites rulings/history | the plan says: 1 file, then regen; never history |
| 5 | The dial is hand-added to `_bento_edit_rails.json` — the R6d selftest goes RED (hand edit ≠ fresh generation) | generator flag first, then `--rails` |
| 6 | L4's render scripts carry the three old class names; a rename before L4 reconciles breaks its drive | conductor at reconcile |
| 7 | `check_composition` registered BLOCKING before finding 5 is repaired → every run is exit 77 on the one artefact it exists for | Dave (Q4) · repair lane first |

## Evidence

`notes/_subreports/assets/2026-09-03-245-L3-composition-edge/` (28 files, 718,724 B)

| file | proves |
|---|---|
| `apply_schema.py` → `groupsWith.schema.fragment.json` · `meta.schema.proposed.json` · `meta.schema.proposed.diff` | deliverable 1 — the fragment, the applied copy, the +1/−0 diff; live schema untouched |
| `build_population.py` → `population-proposal.json` · `schema-arms.txt` | deliverable 2 — the 8 edges with measured lines; 136/136 · 6/6 · 6/6-RED-under-live · 6 mutants · 3 controls |
| `rails_from_edge.py` → `_bento_edit_rails.proposed.json` · `rails-from-edge.txt` | deliverable 3 — the derived dial; hashes before/after; CLI == disk |
| `check_composition.py` → `drive-real-artefact.txt` · `selftest-check-composition.txt` | deliverable 4 — the real drive (UNPROVEN 77) and 10 arms / 6 mutants |
| `render_probe.py` → `render-probe.json` · `render-probe.txt` · `render-as-shipped-1440.png` (120,213 B) · `render-fixture-cols6-1440.png` (105,351 B) | finding 5 — the 4×1 vs 2×2 measurement and the two full-page renders |
| `rename_dryrun.py` → `rename-grep-before.txt` · `rename-plan.json` | deliverable 5 — 27 files / 234 occurrences classified; the dry-run plan |
| `build_review.py` · `theme-tokens.json` · `render_review.py` → `render-review.json` · `review-mono-light-1440.png` · `review-console-dark-gate.png` · `review-mono-light-390.png` | the surface's generator and its 16-state render proof (overflow 0, console errors 0) |

**Declared skips (in `knowledge/_tmp/l3-245/` only, not copied):** `render-standalone-1440.png` and
`render-fixed-cols-1440.png` (120,213 B + 105,351 B — the first probe run, byte-identical in content to
the two copied) · `review-mono-dark-1440.png` (97,243 B) · `review-console-dark-1440.png` (97,243 B,
identical to mono-dark, finding 12) · `review-supercharge-light-1440.png` (104,619 B) ·
`review-console-dark-population.png` (129,800 B) · `review-console-dark-questions.png` (126,315 B) ·
`_rails.live-cli.json` (302 B note). Total skipped 780,895 B.

REPLAY-THESE: `_REVIEW-L3-composition-edge-2026-09-03-v1.html` §05 "The gate" and §06 "Ruling-shaped questions" (~2,500 tk) · finding 5 above + `render-probe.txt` (~500 tk — the defect and its measurement) · `population-proposal.json` → `proposals` block (~1,200 tk — the 8 edges with their `$note`s) · `rails-from-edge.txt` (~400 tk — the byte-identical proof) · `drive-real-artefact.txt` (~500 tk — what C9/C1 read off the real page)
