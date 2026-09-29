# #308 lane O — design-system ontologies research (read-only)

Asked: Dave, Tue 2026-09-29 08:43 BST — "I also want some research around design system ontologies, this might help our edge definitions".
Output: notes/_RESEARCH-308-design-system-ontologies-2026-09-29-v1.html (self-contained, no external scripts; answers stay in localStorage, "Copy my answers" gives plain text).

COUNTS: edge types found 65 (11,412 edges, 5,901 nodes, explorer extract at 2026-09-29T07:53Z) · sources read 28 · recommendations 9

## Headline
No published design-system ontology worth adopting was found (searched; empty is not proof of absence). The general standards (OWL, SKOS, SHACL, Dublin Core, Backstage, Wikidata, PROV-O) all define each relation ONCE — ends, opposite, shape, count, reason, maker — and a separate check reads that. Apollo has a closed vocabulary, typed ends by prefix, declared nulls, force (must/should/is ≈ SHACL violation/warning/info) and n-ary polarity nodes, but no per-type definition: it is spread over meta.schema.json, _kg_verbs.json, _build_kg_explorer.py and _validate_kg.py, and the gate checks resolution, not kind.

## Measured (repo, 2026-09-29)
- Reason on edge: obeys 168/168, restsOn 75/75; no other type (2 of 65). Named $why / why / evidence / $note.
- governedBy: component→ruling 28, logo→rule 12 (two relations, one word). 18 of 28 mirrored by governs.
- containedBy 88 vs hasPart 14 comp→comp: 0 mirrored.
- Self-loops 22: family 9, mustNotNeighbour 7, hasPart 4, groupsWith 2. Containment 2-cycle: carousel↔cards.
- Repeated (type,s,t) pairs 29 (governs 14, under 11, hasPart 4), 60 extra copies.
- `authored` flag absent on 1,648 edges (incl. all hand-written obeys); true on 835 generated bindsToken.
- _decision-graph.json: 172 edges, 9 types, spelled differently from _ruling_edges.json's 10.
- inFamily (145) read by no verb and not in `unread` (already noted in _kg_verbs.json $drift).
- _validate_kg.py: grep for domain|range|inverse|symmetric|irreflex|self-loop|cycle → nothing.

## Recommendations (Dave rules: take / change / leave)
1. One edge register — every type defined once (word, verb, from, to, opposite, shape, count, reason rule, maker, outside term).
2. Check both ends of every edge against its row (SHACL-style closed world, advisory first); move the 12 logo→rule lines to obeys.
3. Store one direction, read the other (governs over governedBy, containedBy over hasPart); one-off agreement check first.
4. Declare shape (self / loop / both-ways / chains); move the 22 self-lines to the fields they mean (count, field, slot/null).
5. One reason field `why`, required per type on hand-made judgement edges; 40-char floor kept.
6. One maker field on every edge: hand / generated (script) / ratified (ruling) — replaces `authored`.
7. Keep Apollo's words; add nearest outside term graded exact/close/loose (SKOS mapping grades). No RDF move.
8. Fold the two ruling-to-ruling vocabularies into one; conflicts-with the one gap (Kruchten; 8 old lines).
9. Four gaps the standards show: token→token alias with loop check (DTCG); provides-capability (Backstage pairs); a theme to point at for defaults; component→ARIA role.

## Not done
No commit, no git, no memory writes. The "first run would print" list is an inference from measurement, not a gate run. Fit grades in the word map are judgement.

## Round 2 — Dave's challenge, 08:48 BST: "there are many defined online ubuntu comes to mind too"

Output: notes/_RESEARCH-308-design-system-ontologies-2026-09-29-v2.html (v1 untouched). New section 02 "catalogue of published ontologies"; corrected headline; items 4, 7, 9 changed.

COUNTS (round 2): named candidates searched 25 · real published vocabularies with relations 3 (Canonical ds:/dt:/anatomy, Adobe Spectrum CTR, Open UI component schema) · recommendations 9 (items 4, 7, 9 changed; 9 gains e)

Corrected headline: v1 was WRONG. Canonical (Ubuntu's publisher) publishes an OWL "Design System Ontology" (ds:, v3.0.0, ds.canonical.com, LGPL-3.0) with a dt: token ontology and an anatomy DSL checked by SHACL shapes — announced on Ubuntu Discourse 2025-10-22 (Adrian Villa), now in github.com/canonical/pragma-core/packages/semantics (repo created 2026-09-28 from archived canonical/design-system). Read ontology.ttl in full.

- Its relations: inheritsFrom↔specializedBy, variantOf↔hasVariant, hasSubcomponent↔parentComponent, hasModifier↔modifierFamily (declared inverses); tier/library/implementsBlock functional; hasTokenBinding → reified TokenBinding (symbol, anatomy path, rank); dt:aliasOf (functional), refersTo, tokenType, coordinate/resolvesBy/otherwise, contains (transitive); anatomy Edge → Relation (cardinality, slotName). decisionLog is a string; no reasons on edges; no rules/rulings/principles/WCAG.
- Maps onto ~11 of Apollo's 65 types (judgement): family, partial, hasPart, containedBy, composedOf, activeVariantOf, renderedBy, bindsToken, setIn, acceptsCapability, capturedFrom. None of the governance half.
- Spectrum Design Data (1.0.0-draft): JSON Schema + numbered graph rules; Component/Token Relationship scoped by component/part/property/options/state; lifecycle introduced/deprecatedIn/replacedBy/plannedRemoval.
- Open UI: component JSON Schema with openUIName (cross-system name), anatomy, concepts.
- Checked and not a relation vocabulary / not established: Vanilla (CSS), CAMELEON/MBUI (WG Note 2014, levels + transformations), UsiXML (relations not on W3C wiki), IFML (containment + flows), schema.org WebPageElement, W3C UI Spec Schema CG (closed May 2026, no output), Figma, Tokens Studio, Style Dictionary, Theo (archived), Material DSP (archived), GOV.UK params yaml, ODS-Terms (2018 stub), montology / design-ontology-harness / design-token-context-model. Carbon, Polaris, Atlassian: no public relation schema found — searched, not established.

Effect on the nine: MAP, don't adopt. Items 1–3 confirmed by Canonical in practice. Item 4: part-names become a subcomponent kind (Canonical). Item 7: outside column points first at Canonical ds:/dt: or Spectrum, then SKOS/DC/PROV; add Open UI name per component. Item 9: a) = dt:aliasOf; c) leans to a theme NODE (Canonical coordinates, Tokens Studio); new e) replaced-by lifecycle on components and tokens (Spectrum, DTCG $deprecated).

Lesson for the record: v1 searched by topic and rounded an empty search to an absence; v2 searched by name and found it in minutes.

## Round 3: cards, tiles and containers (Dave, 17:07 BST)

Dave's question, verbatim: "i think we have to create a definition for cards and tiles, this might help as a differentiator, in the case of a bento one of it's 'tiles' could contain a carousel, it's tricky as a card is a container and a carousel can sit in a container, is the question about the hierarchy of containers or clear definitions for different types. we need to work this out, is there a standard nomenclature for this?"

Output: notes/_RESEARCH-308-cards-tiles-containers-2026-09-29-v1.html. It has the rv-back link after `<body>`, and its decision bar copies under the header "Session 308 · cards and tiles · answers".

COUNTS (round 3): 17 systems and specs read · 5 calls.

Headline: no standard nomenclature exists. "Card" is broadly settled: content about one thing, usually one of a set. It appears in 12 of the 27 systems in Open UI's data, and Carbon has none. "Tile" is not settled. It means four different things:
- Carbon: any container.
- Canonical: a surfaced box for unlike content, the one used in dashboards and bento layouts.
- Atlassian: a 16–48 px square holding one asset.
- Material 1: a grid cell holding a picture.

The conductor's premise mostly holds, with one correction. The line that fits Apollo best is Canonical's, from card.ttl and tile.ttl in pragma-core:
- A card is one of a set of like records. It is not a surface; its border bounds it.
- A tile holds one-off content, with a surface. Canonical's own example: a lone "Total users" number goes in a tile.

Apollo's #274 ruling already matches the card half: a record is a card when its container draws a border around each record. Definitions come first, and the hierarchy falls out of the accept rules.

Apollo collisions (measured over the 142 metas):
- "Tile" has four meanings: the KPI tile component; the stat card ("the dashboard tile for one headline number"); a bento cell; and the app tile in logos.md.
- "Card" has four meanings: the Cards container; the stat card metric; the account card record; and the payment card, meaning the plastic.
- The stat card and the KPI tile are one object, split only by whether a series is present. The KPI tile meta cites the ruling that says so. This is the #202 "switch" class again.
- "Panel" is used for the chart-panel role and as a word for a box. Outside Apollo it means a region at the side of the screen.
- Cards and carousel are both providers of the arrangement role.
- containedBy has no accepts check.

Proposed definitions (proposals only, not rulings):
- Five kinds: layout, holder, record, block and part.
- Bento: accepts two or more tiles.
- Tile: accepts exactly one block, carousel or layout; never a tile directly inside a tile.
- Carousel: its slides each hold one record or image block, all of the same kind.
- Card: accepts its parts only; its content accepts atom- or molecule-sized blocks; it always has peers.
- Card grid: accepts two or more records of the same kind.
- Panel: a region of the screen frame only.
- Container becomes an umbrella word in the register, and surface becomes a property (ground, border or none).

Enforcement: add accepts-by-kind to the containedBy row of the edge register. Each meta declares its kind, and each slot's accepts names kinds. The check refuses any containedBy line the parent does not accept (NOT-ACCEPTED, TOO-MANY, MIXED-SLOTS, and LONE-CARD as a warning). Tonight's pair ruling, "a carousel holds cards", then becomes something the check derives.

Calls, each with a recommendation:
1. Canonical's line between card and tile.
2. Check containment by kind through accepts, advisory first.
3. Container as the umbrella word, surface as a property, panel as a frame region; rename the chart-panel role to chart.
4. Merge the stat card and KPI tile into one Metric block, with the trend as an optional slot and the old names kept as aliases.
5. Write in all four nesting limits: three refuse and the lone-card limit warns.

Nothing is committed and nothing in the tree was changed.
