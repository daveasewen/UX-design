# `#234`-`rC` — the contract: exact retrieval + bounded flex

session: `#234` · 2026-09-02
window: quality-bar research, strand rC (three-sub fan-out)
sub index: `rC`
brief: `notes/_briefs/2026-09-02-234-quality-bar-research-brief.md`
tokens: `UNMEASURED — a sub cannot read its own message.usage from its seat; _checkin.py reports the
CONDUCTOR's window, not this sub's, so quoting it would be a wrong number rather than a missing one.`

## VERDICT

All four regions of the rC brief were DONE. The headline is that the diagnosis in the `#233` brief
is confirmed **and narrowed**: the pack's flex is not thin, it is *unaddressed*. 528 props are
declared across 135 metas and **every single enum prop carries its legal value set** — the
"variant, not invention" data already exists, machine-readable, complete on that axis. What does
not exist is any sentence in any of the six skills that tells the agent the data is there:
`slots`, `behaviour`, `behavior`, `javascript` and `receipt` each return **0 hits across all six
`SKILL.md` files**, and `props` returns 2. Behaviour is the sharper case. All 136 snippets carry a
`<script>` element and 100 carry an *executable* one, so the behaviour ships inside the artefact
the agent is already told to copy — but `behaviour` is schema-typed as `["object","array","string"]`
with the description "optional behavioural notes", appears in only 20 of 137 metas, holds three
different JSON types across those 20, and **never once addresses the script**. Both components that
failed Dave's cold test sit in the gap: `dropdown.meta.json` has no `behaviour` key and no `slots`
key at all; `chart-line.meta.json` has `slots` but no `behaviour` — its engine is described in
prose inside `motion.hover` and `responsive.rule`. Externally, four systems solve exactly this and
all four solve it the same way: behaviour travels as an **address beside the markup**, never as
prose about the markup (Code Connect `imports:` / `snippetImports`, Custom Elements Manifest module
`path` + typed `events`, Storybook manifest `import` + `snippet`). Enforcement of "variant, not
invention" splits into four distinct mechanisms in the wild — schema, prompt, curation-tag, and
test-loop — and Apollo has strong instruments for exactly one of them (gates) wired to a path a
generated page does not take: `_validate_screen.py`, the only gate that accepts a page, runs
compose / icon-source / a11y / state-contrast and asks nothing about provenance or behaviour.
Nothing here is ruled or recommended; the ruling-shaped questions are parked in their own section.

COUNTS: findings 16 · ruling-shaped 5 · UNPROVEN 4

## What was done

Region 1 — repo grounding, in the brief's order. Read `apollo-spider/cold-start/DESIGN-CONTRACT.md`,
`apollo-spider/skills/generate-from-canon/SKILL.md`, `apollo-spider/skills/check-with-gates/SKILL.md`,
`notes/_briefs/2026-09-01-233-delegated-wrap-brief.md`, and three metas of my own choosing per the
brief — `knowledge/components/dropdown.meta.json` (component), `knowledge/components/chart-line.meta.json`
(chart), `knowledge/components/template-dashboard-bento.meta.json` (template). Added
`knowledge/components/meta.schema.json` (the field definitions the brief's schema question needs),
`knowledge/_BEHAVIOUR-GATE.md`, `knowledge/_CODE-CONNECT-PLACEMENT.md`, and docstring-only reads of
`_validate_behaviour.py`, `_validate_partials.py`, `_validate_wiring.py`, `_validate_compose.py`,
`_validate_screen.py`. Ran a root-key census over all 137 metas and a `<script>` census over all 136
snippets. `GOOD-MORNING.md` was NOT read. Nothing in the repo was written except this file.

Region 2 — web research: Custom Elements Manifest `schema.d.ts` (raw source), Figma Code Connect
HTML guide, Figma MCP server tools-and-prompts reference, Storybook MCP server overview, Storybook
manifests reference, plus search-level reads on Polaris/Shopify MCP and design-system MCP writing.

Regions 3 and 4 — the four brief outputs are Findings 7–9 (receipt shapes), 10–12 (behaviour
travel), 13–16 (enforcement), and the field-by-field table under Finding 16.

## Findings

**1 — The pack never names its own flex. MEASURED, and the naive probe lies.**
Probe, run in `apollo-spider/skills/`: `grep -ric "slots|behaviour|behavior|javascript|receipt"`
returns **0 for every one of those five words across all six skills**. `props` returns 2 hits
total. A naive `grep -ric "script"` returns 10 and is a **false probe** — the word `description` in
each skill's YAML front-matter contains the substring `script`. The true probe,
`grep -rinE "\bscripts?\b|\bJS\b|javascript"`, returns 6 lines: four in `check-with-gates/SKILL.md`
all meaning *Python gate script*, and two in `draft-a-new-pattern/SKILL.md` that push JS **away**:
line 39 "Motion in CSS, on the motion tokens — not computed in JS", line 40 "JS logic doesn't travel
to Figma." So the only two mentions of JavaScript in the whole pack tell the author to avoid it.

**2 — The flex is present and, on the enumerated axis, complete.**
Census over `knowledge/components/*.meta.json` (137 files, `EXAMPLE-button.meta.json` included):
`props` 135 · `variants` 124 · `slots` 34 · `behaviour` 20 · `tokens` 135 · `accessibility` 135 ·
`antiPatterns` 135 · `edges` 136 · `$composes` 12 · `$composesNote` 4. Deeper probe: **528 props
declared in total, and the count of `type:"enum"` props carrying no `values` array is 0.** Every
enumerated prop in the library states its legal set. 136 of 137 metas carry `edges.renderedBy`
pointing at `snippet:<Name>.reference.html` (the sole exception is `EXAMPLE-button.meta.json`).
The addressable spine for a retrieval contract is therefore already laid.
*(The brief's figures — 135/137 props, 124 variants, 34 slots, 20 behaviour — reproduce exactly;
my first `grep -l` pass said 125/22 because `grep` matches nested keys, and the JSON root-key
census is the true count. Naming the discrepancy rather than quietly adopting mine.)*

**3 — `behaviour` is the one load-bearing field with no shape.**
`knowledge/components/meta.schema.json:198`, quoted whole:
`"behaviour": { "description": "optional behavioural notes", "type": ["object", "array", "string"] },`
Compare the neighbouring `slots` (line 185–190), which is fully typed via `#/definitions/slotEntry`
with `accepts` closed to `tier`/`capability` by `additionalProperties:false` and `use` mandatory.
`slots` was ruled into a contract at `s140-D1`; `behaviour` never was. In the 20 files that carry
it, it holds **three different JSON types**: `dict` (`stepper`, `file-upload`), `str`
(`tab-bar`, `summary`), and per the schema `array` is legal too. `summary.meta.json`'s entire
behaviour value is the string `"Passive display list — no states."`

**4 — Both cold-test failures sit precisely in the hole.**
`dropdown.meta.json` — no `behaviour` key, no `slots` key. Its 6 props and 4 variants are declared;
nothing in the file mentions that the component has an engine. `chart-line.meta.json` — has `slots`
(`series`, `data`, both `$status: "ruled s140-D2"`), has no `behaviour`. Its engine is described in
prose in two other fields: `motion.hover` reads `"Interactive value POPOVER (dvTip — behaviour
partial)"` and `responsive.rule` reads `"...(behaviour partial): baked-fraction relayout
(data-fx/-fxs/-ys/-fx2/-x0...) ... JS-off falls back to the static answer: fixed 580×260 +
horizontal scroll."` That last clause is the exact symptom Dave's test produced. The file predicted
the failure in prose and no field carried the prediction anywhere a machine could act on it.
The `antiPatterns` array does carry `"Re-typing dv-behaviour locally (ADR-0015 — consume the
AUTO-BEHAVIOUR partial)"` — a "don't", with no matching "do" and no address.

**5 — The behaviour is already inside the artefact the agent is told to copy.**
Census over `knowledge/snippets/*.reference.html`: **136 of 136 carry a `<script>` element; 100
carry an executable one** (i.e. a `<script>` tag whose attributes do not include
`application/json` — the other 36 carry only the `#token-manifest` JSON block). `Dropdown.reference.html`
lines 178 onward hold the wiring Dave's agent re-authored: `function wire(dd)`, with
`trig.setAttribute('aria-expanded',...)`, arrow-key navigation and `Escape` handling. Rule 2 of
`generate-from-canon/SKILL.md` — *"Copy the snippet, don't re-draw it. Take markup and classes
from `knowledge/snippets/<Slug>.reference.html`"* — says **markup and classes**. An agent reading
that literally copies exactly what the sentence names.

**6 — There IS a behaviour gate, and it grades the wrong population for this purpose.**
`knowledge/_validate_behaviour.py` exists, is wired, and is green. Its docstring: *"This gate checks
every behaviour SOURCE registered in knowledge/component-types.json ($behaviour blocks), plus its
member snippets"* — size ≤16 KB, no polling, no network, exactly one rAF-debounced resize listener,
and on each member snippet "no external `<script src>`". `knowledge/_BEHAVIOUR-GATE.md` records
three sources (`dv-behaviour.js` 14174 bytes, `dv-legend.js` 15131, `dv-donut-sweep.js` 5511) and
`✓ PASS`. It grades the library's own JS budget. It does not, and does not claim to, ask whether a
*generated page* carries the behaviour it needs. The gate a generated page actually meets is
`_validate_screen.py`, whose docstring lists its four checks: `compose` · `icon-source` · `a11y` ·
`state-contrast (optional)`. Neither behaviour nor provenance appears. This is
[[instrument-without-a-consumer]] in the other direction: a real instrument, pointed elsewhere.

**7 — Receipt shape (a): Figma `get_code_connect_map` — the per-node mapping record.**
`https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/` : *"It returns an object
where each key is a Figma node ID (an instance in the current selection), and the value contains
metadata about the connected component, such as: `componentName` ... `source`: The location of the
component in your codebase (file path or URL). `snippet`, `snippetImports`, `snippetNestedFunctions`
... `version`: The source of the mapping ... `label`: The framework label."* Note the shape: the
receipt is keyed by a **stable identity**, and carries **where it came from**, **what was handed
over**, and **which version of the mapping produced it** — four fields, not prose.

**8 — Receipt shape (b): Figma's shader tools — content-addressed provenance.**
Same page, `get_shader_effect`: returns *"Name, Description, Version, Source file manifest
containing: filename, bytes, uri"*, and *"The version must be a 40-character commit SHA."* This is
the strictest form seen: the retrieved thing names its bytes and its commit. Apollo already mints a
sha256 in one place — `template-dashboard-bento.meta.json` `$cardinalRule` records *"every region
is a byte-identical SPLICE from a file already on disk, cut by an extractor and sha256-stamped in
the report's borrow ledger"* — but that ledger lives in a `#231` sub-report, not in the artefact.

**9 — Receipt shape (c): the Storybook components manifest entry.**
`https://storybook.js.org/docs/ai/manifests` — one entry is
`{ "id", "name", "path": "./src/components/Button/Button.stories.tsx", "stories": [{ "id", "name",
"snippet" }], "import": "import { Button } from \"@mealdrop/ui\";", "description", "reactDocgen": {
"props": {...} } }`, served at the fixed route `/manifests/components.json`. Two things Apollo does
not have: the entry carries the **import line** (the address of the runnable thing) and a
**snippet per story** (the exact string for each declared state). Storybook flags the schema
*"not yet stable and should not be considered a public API"* — quoted so the maturity is not
overstated.

**10 — Behaviour travel (a): Code Connect makes the script an explicit sibling field.**
`https://developers.figma.com/docs/code-connect/html` , Web Components example:
`imports: ['<script type="module" src="https://my.domain/js/ds-button.min.js">'],` — a declared
array beside `example`, and the same field surfaces in the retrieval result as `snippetImports`
(Finding 7). Behaviour is neither described nor inlined; it is **addressed**, and the address is
part of what retrieval returns.

**11 — Behaviour travel (b): Custom Elements Manifest types behaviour instead of narrating it.**
`https://raw.githubusercontent.com/webcomponents/custom-elements-manifest/main/schema.d.ts`. Every
declaration hangs off a `JavaScriptModule` whose `path` is documented as *"Path to the javascript
file needed to be imported."* The custom-element interface then declares four typed arrays where
Apollo has prose: `attributes?: Attribute[]` · `events?: Event[]` (*"The events that this element
fires"*) · `slots?: Slot[]` (*"The shadow dom content slots that this element accepts"*) ·
`cssParts` / `cssProperties` / `cssStates`, plus `demos?: Demo[]` where a `Demo` is
`{ description?, url, source? }`. `Event` is `{ name, summary?, description?, type: Type, ... }` —
a typed list, gate-readable, not a paragraph. **Apollo has `slots` at the same fidelity and has no
`events` analogue at all.**

**12 — Behaviour travel (c): the HTML idiom Apollo already uses is the sanctioned one.**
Same Code Connect page: *"Any JavaScript/TypeScript code accompanying the HTML code must be enclosed
in a `<script>` tag."* Its Web Components example ships the markup and a `<script>` with an
`addEventListener` in the same template string. That is byte-for-byte the shape of
`Dropdown.reference.html`. The difference is not the artefact — it is that Code Connect's retrieval
hands over `snippet` **and** `snippetImports` as one unit, where Apollo's instruction hands over
"markup and classes" and leaves the sibling `<script>` unmentioned.

**13 — Enforcement (i), by schema: variant restrictions and typed slot acceptance.**
Code Connect's `variant:` key registers a *separate mapping per legal variant* —
`figma.connect('https://...', { variant: { Type: 'Primary' }, example: () => html\`<ds-button-primary>\` })`,
with a sibling call for `Secondary` and `Danger`. An unregistered variant has no mapping and so
returns nothing to invent from. The docs also state for `figma.enum`: *"values are not normalized
... You always need to pass the exact literal values to the mapping object."* And for slots:
*"Only instances with their own Code Connect definitions are rendered. Other slot content,
including text, layers, and instances nested inside another instance, is omitted."* — i.e. a slot
child that is not in the system does not render. Apollo's `slotEntry` definition
(`meta.schema.json:60–77`) already closes `accepts` to `tier`/`capability` with
`additionalProperties:false`, which is the same family of mechanism at the schema level; it is
declared but, per the `s140-D1` note quoted at line 186, *"OPTIONAL at schema level (staging:
permit now, enforce by gate later)"*.

**14 — Enforcement (ii), by prompt: the published instruction text is blunt and specific.**
Storybook publishes the literal `AGENTS.md` text it expects teams to paste
(`https://storybook.js.org/docs/ai/mcp/overview`): *"**CRITICAL: Never hallucinate component
properties!** Before using ANY property on a component from a design system (including
common-sounding ones like `shadow`, etc.), you MUST use the MCP tools to check if the property is
actually documented for that component. ... Only use properties that are explicitly documented or
shown in example stories ... If a property isn't documented, do not assume properties based on
naming conventions or common patterns from other libraries. Check back with the user in these
cases."* Note the last clause: the fallback is **ask the human**, not "improvise" and not "flag a
gap silently". Figma's equivalent is the `create_design_system_rules` MCP prompt, described as *"A
prompt for creating a rule file that provide agents with the right context to translate designs into
high-quality, codebase-aware frontend code"*, with the instruction to *"make sure the result is
saved to the correct `rules/` or `instructions/` path"*. Apollo's `DESIGN-CONTRACT.md` rule 3 is the
same instrument and is arguably stronger prose — *"Never invent. No new component, variant, colour
or icon"* — but it names components, variants, colours and icons, and does not name props, slots or
behaviour.

**15 — Enforcement (iii), by curation: the retrieval SET is a declared subset.**
Storybook manifests: *"By default, all stories and independent docs pages have the `manifest` tag
applied, which means they will be included in the manifests"*, and a story is removed from the
agent's world with `tags: ['!manifest']`. The retrieval set is therefore an explicit, per-artefact
opt-out — the artefact itself declares whether an agent may see it. Apollo's nearest equivalent is
`$status` prose: `template-dashboard-bento.meta.json` carries *"⛔ NOT GATED, NOT RULED, NOT
REGISTERED - absent from CATEGORIES, MIGRATED_SNIPPETS, component-types.json and _rulings.json"*
while simultaneously being projected into `canon.css` and `showroom/` *"because gen_canon_components.py
and gen_showroom.py glob every snippet"*. So a PROPOSED artefact is fully retrievable and its
"do not use me yet" lives in a prose field no gate reads.

**16 — Enforcement (iv), by loop: the tester lives in the same server as the retriever.**
Storybook's MCP exposes three toolsets from one endpoint — docs (`list-all-documentation`,
`get-documentation`, `get-documentation-for-story`), development
(`get-storybook-story-instructions`, `preview-stories`, `get-changed-stories`), testing
(`run-story-tests`, which *"Runs tests for specific stories and returns results, including any
accessibility issues"*) — described as *"a self-healing loop that helps ensure the quality of the
generated UI without requiring you to intervene."* Apollo has the strongest half of this (39 gates
vs Storybook's axe-in-a-story) and splits it across a **second skill the agent must choose to
open**: `DESIGN-CONTRACT.md` rule 3 says *"Check before you show. Open
`skills/check-with-gates/SKILL.md` ... reading the file is not running it."*

**Field-by-field map onto the repo's meta schema as it stands** (the brief's output 4). This is a
correspondence table, not a proposal:

| external field | its job | Apollo's seat today | state |
|---|---|---|---|
| CEM `attributes[]` / SB `reactDocgen.props` | the legal knobs, typed, enumerated | `props[]` — 528 declared, 0 enums missing `values`, `binds` per `bindsShape` | **present and richer** (carries token binds) |
| CC `variant:` restriction | one registered mapping per legal variant | `variants[]` — 124 files; `{name, use}` only, no per-variant markup or selector | present as a **name list**, not a mapping |
| CEM `slots[]` | what may be injected, and what may not | `slots` + `slotEntry` (`accepts.tier`/`accepts.capability`, `use` mandatory) | **present and stricter**; 34/137 populated, enforcement staged to "later" |
| CEM `events[]` (typed array) | what the component emits | none | **absent** |
| CC `imports:` / MCP `snippetImports` | the address of the runnable behaviour | none; nearest is `antiPatterns` prose naming ADR-0015 | **absent** |
| CEM module `path` | where the JS lives | `provenance.code_path` (a *source* path, not a runtime import) + `edges.renderedBy` → snippet | partial, and points at the snippet, not the engine |
| SB `import` line | paste-ready runnable address | none | **absent** |
| SB `snippet` per story | the exact string per declared state | the snippet file, one per component, all variants in one page | present at component granularity, not per variant |
| MCP `componentName`/`source`/`version`/`label` | the retrieval receipt | none in a generated page; `provenance{source, figma_node, code_path}` is the *component's* provenance, not the *retrieval's* | **absent as a receipt** |
| shader `version` = 40-char SHA + `{filename, bytes, uri}` | content-addressed proof | sha256 borrow ledger exists once, in a `#231` sub-report | precedent exists, not a field |
| SB `manifest` tag / `!manifest` | is this in the retrieval set at all | `$status` prose (`PROPOSED`, `NOT GATED`) | **prose only** |
| CC "behaviour in the same `<script>`" | behaviour ships with markup | 136/136 snippets carry `<script>`, 100 executable | **present in the artefact, absent from the instruction** |
| `behaviour` field | describe behaviour | 20/137, three JSON types, `"optional behavioural notes"` | present, **untyped**, never an address |
| `$composes` / `$composesNote` | which components an organism is made of | 12 files carry `$composes`; 4 carry `$composesNote` explaining `relationships` is closed and has no seat for it | **named gap, deliberately not smuggled** |

## RULING-SHAPED QUESTIONS

⛔ Per the brief, nothing here is recommended — the options are priced and left open. Dave rules.

1. **What identity does a retrieval receipt key on?** (a) the snippet filename (stable today, 136/136
   resolvable, but capitalisation is inconsistent between folders — the skill already warns *"Match
   the slug case-insensitively (glob it)"*); (b) the meta slug (the index key, but `EXAMPLE-button`
   has no `renderedBy`); (c) a content hash of the spliced region (the `#231` borrow-ledger
   precedent, and Figma's shader shape — strongest proof, highest mint cost, and it changes on every
   regen serial).
2. **Where does the behaviour ADDRESS live — beside markup, or in the meta?** (a) a `behaviour`
   field promoted from "optional notes" to a typed object with a `script`/`partial` address (schema
   change, touches 137 files' worth of authoring convention, and `behaviour` is currently absent
   from 117 of them); (b) a declared block inside the snippet itself, the way `#token-manifest`
   already works (no schema change, one generator, but a second home for a fact the meta arguably
   owns); (c) both, with one generated from the other.
3. **Is an `events` field wanted at all?** Every external manifest surveyed has one; Apollo has
   none. It is the field a developer receiving the page for wiring would read first. Cost: a new
   typed root key plus 137 authoring decisions, most of which will be empty.
4. **Does the retrieval SET need a machine-readable membership marker?** `template-dashboard-bento`
   is PROPOSED, unregistered, and fully retrievable — its "not yet" lives in `$status` prose.
   Storybook solves this with one tag. Apollo could (a) leave it prose, (b) add a boolean/enum root
   key, (c) drive it off the existing registration files (`component-types.json`, `CATEGORIES`)
   which already disagree with what the globbing generators publish.
5. **Does "copy the snippet" get re-worded, or does a new rule sit beside it?** Rule 2 currently
   reads *"Take markup and classes from ..."*. Widening that sentence is a one-line edit with a
   large blast radius (it is quoted in `DESIGN-CONTRACT.md`, the SKILL, and the #233 diagnosis);
   adding a rule 2a leaves the ruled sentence intact per [[header-wins-over-audit]].

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** that adding a behaviour address to the meta or snippet would have changed Dave's
  cold-test outcome. The causal claim in `#233` ("reverting to the snippet's script fixed it") is
  the conductor's, chat-sourced, and I did not re-drive it. Price to prove: one cold agent run
  against a v1.0.5 pack plus one against a pack with the address present, ~2 sessions, and it needs
  a fresh agent (a warm one has already read this report's findings).
- **UNPROVEN:** whether the shipped pack's `knowledge/components/` copies are byte-identical to the
  repo's. `build-designer-pack.sh` line 376 documents *"`knowledge/components/` — one contract per
  component: props, variants, token bindings"* and the census above is repo-side; `dist/` holds
  v1.0.0–v1.0.4 zips only, and the v1.0.5 proving zip is recorded as VANISHED in memory. Price:
  unzip one release and re-run the root-key census, ~3K tokens.
- **UNPROVEN:** that `_validate_screen.py` asks nothing about behaviour or provenance. I read its
  docstring and its four named checks, and read `_validate_compose.py`'s docstring for the delegated
  half; I did not read either body in full and did not run them (the brief's read-only rule and
  "list, do not run"). Price to prove: ~6K tokens to read both bodies, or one run against a page.
- **UNPROVEN:** the maturity of the external shapes. Storybook's manifests and MCP are marked
  preview and React-only (*"this manifest schema is not yet stable and should not be considered a
  public API"*), and Figma's framework-specific Code Connect parsers carry *"Framework-specific
  parsers will no longer receive updates or support. Template files are now the only actively
  maintained way of using Code Connect."* The HTML `imports:` shape I quote is therefore from a page
  Figma itself labels legacy. Price to prove the current shape: read the Template API page, ~5K.
- **CLAIMED (not re-read from the artefact):** the `#233` symptom detail — `Dropdown.reference.html:178`,
  the "22 `data-fx*` geometry attrs" in Dave's output, and the local `--bento-row-unit` overrides.
  I re-read `Dropdown.reference.html` around line 178 and confirm an executable wiring script is
  there; the other two are from the `#233` brief and Dave's output file, which I do not hold.
  Re-read cost: the output file is not in the repo — it would have to come from Dave.

## Evidence

No evidence files: every claim above quotes its probe inline — repo path plus line or quoted
string, or source URL plus the quoted sentence. The two census probes are reproducible in one
command each: a JSON root-key count over `knowledge/components/*.meta.json`, and a
`<script>`-attribute count over `knowledge/snippets/*.reference.html`.

## WHAT APPLIES TO A FACTORY

A factory that generates pages, not a codebase, inherits three of the four external mechanisms
cleanly and one badly. The **address** transfers exactly: a factory can hand over markup and the
runnable thing as one unit, because both are files it already owns — Code Connect proves an HTML
system can do this without a build step. The **receipt** transfers, and is cheaper here than in a
codebase: a generated page is a single artefact, so its provenance can be a block inside it, the
way `#token-manifest` already is, rather than a database. The **curation tag** transfers and is
arguably more urgent for a factory, because a factory's output looks finished whether or not the
parts were ratified — a PROPOSED template renders as beautifully as a canon one. What transfers
badly is the **self-healing test loop**: a codebase's tests are cheap and local, and a factory's
strongest checks are exactly the ones that need a browser and refuse (exit 77) more often than they
fail. The factory equivalent is not "run the tests until green" but "the retrieval and the check are
the same step" — the agent cannot receive a component without also receiving what proves it. The
last transferable point is smaller and harder: every external system makes its contract *the thing
the agent fetches*, never a document the agent is trusted to have read. Apollo's contract is
currently prose the agent must open, and 0 of 6 skills mention the fields that carry the flex.

REPLAY-THESE: `knowledge/components/meta.schema.json` lines 60–77 and 185–198 — the `slotEntry`
definition beside the untyped `behaviour` line, side by side (~1.5K tk) · `knowledge/components/dropdown.meta.json`
(~2K tk) · `knowledge/_validate_behaviour.py` docstring, lines 1–26 (~0.6K tk) · the Finding 16
field-by-field table above (~1.2K tk) · `apollo-spider/skills/generate-from-canon/SKILL.md` rule 2
and step 2, verbatim (~0.4K tk)
