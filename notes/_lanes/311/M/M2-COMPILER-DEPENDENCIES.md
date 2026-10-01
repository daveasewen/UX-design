# M2 — What Apollo's build depends on: snippets, metas, tokens

Lane M2 of #311, Opus, read-only, run on Dave's seat on Thu 2026-10-01. Nothing in the repo was edited. All paths are relative to the repo root unless they start with `knowledge/`, in which case they are under `knowledge/`.

## Summary — the plain answer

Dave asked: "do we rely on the snippet for structure or with the py build it correctly regardless of the reference". Today Apollo relies on the snippets, and for more than structure. The Python build does not build a component from anything else. The snippets are the declared source of truth for three things: the CSS, the markup and most of the behaviour.

The CSS. `knowledge/canon/gen_canon_components.py` regenerates the component layer of `canon/canon.css` from `knowledge/snippets/*.reference.html` on every build (`_build_all.py:215-216`). Its docstring says it plainly (lines 3-7): "The snippets are the source of truth (they are the final reviewed components); canon regenerates from them". Measured today, that AUTO-COMPONENTS block is 1,728,813 of canon.css's 2,087,030 bytes (82.8%). The four-theme AUTO-THEMES block is another 256,389 bytes (12.3%), and `gen_theme_cascade.py:341-344` derives it from each snippet's `#token-manifest`. So about 95% of the shared stylesheet is downstream of the snippets. Only the token spine (34 KB, from tokens JSON), the bento block and the hand-written `.c-*` utilities are not.

The markup. No meta carries an anatomy or a template. Every route that puts a component on a page copies the snippet's markup. The compose runbook says to drop in "its scope class + the snippet's own markup" (`_RUNBOOK-compose-from-canon.md:46-48`). The receipt mint "SPLICES regions out of `knowledge/snippets/*.reference.html`" as exact source bytes (`gen_provenance_receipt.py:5-6, 45-46`). The Launchpad spec's planned renderer emits "the same classes the reference snippets use", and until it exists the stand-in is "R5's splice of reference snippets" (`notes/_lanes/312/C/SPEC-launchpad-day-one.md:62, 200`). The pack's own README calls `knowledge/snippets/` "the reviewed reference markup. This is what 'correct' looks like" (`apollo-spider/build-designer-pack.sh:461`).

The behaviour. 102 of 137 snippets carry executable script, 22,765 lines in all. About 16,750 of those lines are generated copies of the 17 shared `canon/*.js` files (AUTO-BEHAVIOUR blocks in 18 chart snippets). About 170 are fenced demo harness. That leaves roughly 5,800 lines of per-component behaviour that exist only inside snippets (the date picker, tabs, menus and so on). Metas point at them: for example, `date-picker.meta.json` has `behaviour.script: "knowledge/snippets/Date-picker.reference.html#script"`.

Dave's instinct is that the snippets are for viewing and the build should not depend on them. That is a reversal of the recorded design, not a tidy-up. ADR-0013 ruling 4 and `gen_component_partials.py:9-11` both say "Snippets stay self-contained and remain the source of truth". The reversal is buildable, but it needs three new sources that do not exist today: a per-component CSS source, a markup or anatomy template per component, and behaviour modules outside the snippets. The metas already hold about half of a framework-neutral spec (see §3). The tokens are close to DTCG but not quite there (see §5).

Count. About 90 code files read snippet files. My heuristic found 95 that pair a snippet path with a file read, and spot checks removed at least five that only mention snippets in a string. About 47 of the 90 are run directly by `_build_all.py` or `.github/workflows/gates.yml`. Seven of them write output that the product depends on. A further 13 files only mention snippets in comments or labels.

## 1 · Who reads the snippets, what they take, what they make

Method: I grepped the live tree (`knowledge/`, `canon/`, `designer-skills-v1/`, `.github/`, excluding `notes/`, `outputs/`, backups and archives) for `reference.html` or `snippets`, then kept the files where a snippet path appears together with glob/open/read_text/listdir/readFileSync. That gave 108 files that mention snippets and 95 that look like readers. Spot checks show these are only mentions: `gen_runbook_index.py:90` (prose), `gen_dashboard.py:141` (label), `_validate_queue_fresh.py:18` (probe fixture), `_validate_token_forks.py:77` (excludes snippets). Treat the count as roughly 90.

Grouped by what they produce:

| group | files (examples, with line) | what is extracted | what is produced |
|---|---|---|---|
| A. Generate canon FROM snippets (product) | `canon/gen_canon_components.py:422` (glob), `:337` (harvest `<style>`), `:348` (`#token-manifest`); `canon/gen_theme_cascade.py:341-344`; `canon/gen_bento_role_vars.py:61` | the whole `<style>` verbatim (comments, states, @media, @keyframes); manifest var→token map; driftAllow per-mode values plus reasons; `:root` non-colour vars; the header carries requiredAria, knownFindings and contrastPairs | `canon/canon.css` AUTO-COMPONENTS (82.8%) and AUTO-THEMES (12.3%) |
| B. Write INTO snippets (snippets as both target and hub) | `gen_snippet_tokens.py:236` (tokens JSON → snippet `[data-theme]` blocks via the manifest); `gen_component_partials.py:561` (AUTO-PARTIAL CSS, AUTO-BEHAVIOUR JS, AUTO-MARKUP HTML from atom snippets or `canon/*.js` into member snippets; AUTO-MARKUP is in 13 snippets); `gen_token_ramp.py` (AUTO-TOKENS); `apply_type_bind.py:102`, `apply_type_snap.py:153` | manifests, PARTIAL source blocks, markup source blocks | the snippets themselves, which group A then reads |
| C. Compose and receipt (screens) | `gen_provenance_receipt.py:259, 335` (splice); `_validate_compose.py:77, 194` (inline scope vars; the "part's own data API": 161 inline sizing declarations over 41 pairs, read from snippets); `_validate_receipt.py` (fixtures plus region hashes) | exact markup bytes by balanced tag scan; AUTO-BEHAVIOUR blocks; inline `style="--x"` usage | composed `.canon.html` pages and their provenance receipts |
| D. Showroom and gallery (viewing) | `gen_showroom.py:458` (whole snippet into srcdoc plus theme cascade from the manifest); `gen_gallery.py:51`; `_render/gen_library_214.py:616` | the whole file | showroom, gallery, library pages |
| E. Knowledge graph and provenance | `gen_kg_edges.py:165` (renderedBy index); `gen_kg_rules.py:151`; `gen_kg_sources.py:90, 237` (copies the snippets dir); `gen_kg_roles_desk.py`; `_build_kg_explorer.py`; `compliance/_build_verification_edges.py:146`; `_validate_kg.py:88, 223` | filenames and stems; some text | KG edges (`renderedBy` is on 138 metas), explorer, compliance edges |
| F. Release and pack | `_release/_gen_pack_manifest.py:669-671` ("Reference markup" group); `designer-skills-v1/build-designer-kb.sh` | file list | the designer pack ships the snippets as engine canon |
| G. Gates on the snippets themselves | about 35 `_validate_*.py`, for example `_validate_snippets.py:351` (token fidelity), `_validate_a11y.py:180`, `_validate_hit_area.py:612`, `_validate_state_contrast.py:603`, `_validate_radius.py:46`, `_validate_icons.py:120`, `_validate_partials.py:83`, `_validate_dataviz.py:1094`, `_validate_own_size.py:109`, `_validate_descender_computed.py:144` | CSS, markup, aria, rendered geometry | pass/fail reports and audits (`_SNIPPET-AUDIT.md` and others) |
| H. Probes, audits, one-off verifiers | 18 in `_render/verify_*`; 5 in `_probe_registry/`; `_build_states_probe.py:93`, `_build_sutherland_fixtures.py:30`, `_build_prototype_grade_audit.py:79`, `_detect_retrieval.py:387`, `gen_itinerary_status.py:416` | various | advisory reports, mostly historical |

Seven files make output the product depends on: in group A, `gen_canon_components` and `gen_theme_cascade`; in group B, `gen_snippet_tokens`, `gen_component_partials` and `gen_token_ramp`; in group C, `gen_provenance_receipt`; in group D, `gen_showroom`. Everything else checks, indexes or reports.

The build is a loop through the snippets: tokens JSON → `gen_snippet_tokens` → snippet theme blocks → `gen_canon_components` → canon.css. Hand-written snippet manifests sit in the middle. `gen_provenance_receipt.py:12-20` records that 137 of 137 manifests are hand-authored and no module injects them.

## 2 · Where the HTML structure of a composed screen comes from

The markup is copied from snippets and finished by hand. It is not generated from metas.

1. The designer skill (`designer-skills-v2/generate-from-canon/SKILL.md:45-47`) says to open the meta and "the snippet it names (`components[].snippet`)", and that canon.css and type.css "are what you LINK, not what you read". Step 4 (lines 73-75) says "React (wire the real components) preferred, or plain HTML/CSS using the canon classes". No React components exist in the repo: one stray `runs/dryrun-001-action-row/prototype/ActionRow.tsx`, no `customElements.define` in any component. "React preferred" therefore has nothing to wire to.
2. The seed reader `_compose_slice.py` does not open snippets. It hands back each chosen component's snippet name (from the meta's `renderedBy`) along with rulings, rules and tokens. Structure is not in what it returns.
3. The compose runbook (`_RUNBOOK-compose-from-canon.md:46-62`) says "Drop in each component as its scope class + the snippet's own markup". Do not copy `APOLLO-DEMO` fences (51 snippets carry them; `_validate_receipt.py` step 3b refuses them as `FAIL:DEMO-CHROME-COPIED`).
4. The mint `gen_provenance_receipt.py --compose SPEC` splices "the first element in the snippet's `<body>` carrying `select` … the exact source bytes" (lines 45-46) and hashes them into the receipt.
5. "Link, don't paste" (s307-D74, enacted overnight by #311 A1, commit 50159e7a; `notes/_subreports/2026-10-01-311-A1-shared-stylesheet-link-dont-paste.md`) changed the CSS half only. A page must link canon.css and must not paste a part's `<style>` (`_validate_receipt.link_or_paste`, shared with `_validate_compose` check 10). Markup is still spliced from snippets. Check 9 now forbids a page from sizing a part, and its exemption list (the "part API") is itself read from the snippets.

So for markup, the agent copies a snippet or the mint splices one. The layout around the parts (`.c-stack-*`, grid, page frame) is hand-written by the composing agent.

## 3 · What the metas carry toward a framework-neutral spec

Coverage over all 139 metas (counted today):

| spec element | field | coverage | quality |
|---|---|---|---|
| props with types | `props[]` | 135 metas, 594 props | every prop has name and type (enum 221, string 121, boolean 108, number 52, array 44, table/component/slot/object/date …); 393 have a default, 239 have enum values; 47 `binds`, 32 `bindsData`. No `required` flag. |
| variants | `variants[]` | 125 | name plus prose `use`; overlaps with enum props |
| slots | `slots{}` (+ `accepts` by tier/capability/kind) | 20 | typed `accepts` (s140-D1, `meta.schema.json:190`) |
| three-axis model (s136-D1) | props / variants / slots | full on about 20, partial on the rest | |
| role | `provides` + edge `providesRole` | 107 | 12-role vocabulary |
| `when` | `when` | 45 | gate half is parseable, rest is prose |
| aria contract | `accessibility` | 135 | relatedSC on 135; keyboard 56, role 55, focus 54, states 23, announcements 15. Mostly prose. |
| tokens consumed | `tokens{}` | 135, 1,013 entries | 239 are pure token paths, 727 are prose strings (130 with a hex inside), 47 objects. Not machine-bindable as it stands; the snippet's `#token-manifest` is the real binding. |
| containment | `edges.containedBy` 47, `composedOf` 1, `$composes` 13, `subComponents` 5 | sparse | no `hasPart` edge on any meta |
| state machine | `stateModel` | 27 | a list of states plus prose; no transitions |
| behaviour address | `behaviour.script` | 33 typed (18 point into a snippet, 15 into `canon/*.js`); 7 null | `behaviour.events` (24) lists DOM listeners (blur, click, keydown), not events the component emits |
| anatomy / markup tree | none | 0 | absent; `meta.schema.json` has no anatomy or template field |
| emitted events / outputs (onChange etc.) | none | 0 | absent |
| content model (what text or children go where) | `ownText` on 57 props, slots | partial | no element-level map |
| code names per framework | `codeBindings` | 4 (table, list-items, cards, status-indicator) | all `sutherland-react: unverified` |

Five sampled components (yes = present, — = absent):

| | props typed | variants | slots | stateModel | aria | behaviour | when | provides | containment | anatomy |
|---|---|---|---|---|---|---|---|---|---|---|
| button | yes (enum type…) | yes | — | — | yes (role, keyboard, focus) | — | yes | action | — | — |
| tabs | yes (tabState enum) | — | — | — | yes (tablist/tab/tabpanel) | — (motion only) | — | wayfinding | containedBy cards; subComponents (Figma nodes) | — |
| table | yes (headerType…) | — | — | — | yes (th scope) | — (`interactive: false`) | — | record-list | subComponents (header, sub-header…) | — |
| date-picker | yes (value DD/MM/YYYY…) | yes (closed/open) | — | — | yes (dialog, grid) | script in the snippet; 5 DOM events | — | input | containedBy form-layout | — |
| metric | yes (size enum…) | yes | yes (spark accepts trend-series) | yes (ready/loading/empty/error/stale) | yes (group + aria-label) | — | yes | headline-metric | — | — (dimensions only) |

The metas are a good contract for what a component is, when to use it, what it takes and what it must not do. They are not yet a spec a generator could render from. They lack the anatomy tree, the states and transitions as data, emitted events, and token bindings as references. Those all live in the snippet today: the markup, the `<style>` state selectors, the script, and the `#token-manifest`.

## 4 · Behaviour and states

Behaviour lives in three places. First, the 17 shared `canon/*.js` files (3,156 lines: dv-render and its chart renderers, dv-legend, dv-behaviour, dv-donut-sweep, dp08-anchor). These are injected into 18 member snippets as AUTO-BEHAVIOUR blocks by `gen_component_partials.py` under `component-types.json` `$behaviour` (lines 495-533), and spliced whole into composed pages by the mint (`gen_provenance_receipt.py:53, 160-164`). Second, about 5,800 lines of per-component script hand-written inline in snippets, with no other home. Third, about 170 lines of demo harness inside APOLLO-DEMO fences. canon.css carries no behaviour. A composed page gets JS only by inlining a snippet's block.

States are expressed as CSS in the snippet's `<style>`, which then flows into canon:

- pseudo-classes (`:hover`, `:active`, `:focus-visible`, `:disabled`, `:checked`, `:invalid`): 1,556 uses in 122 snippets
- `.is-*` / `.has-*` classes: 502 in 75
- `[aria-*]` attribute selectors: 209 in 59
- `[data-state…]` selectors: 17 in 13
- bare `.selected`/`.open`/`.loading` classes: 16 in 9

Markup carries 4,174 `aria-*` attributes across the snippets. The meta's `stateModel` (27 metas) names states but does not drive them. So the state machine is implicit in CSS selectors plus script, per snippet.

## 5 · Tokens: how far from W3C DTCG

Over 940 tokens in the live files (`tokens/*.json`, themes and palettes, excluding `*-pre-s141` and `_*` parked files):

- Already DTCG-shaped: `$value`, `$type` and `$description` everywhere. `$type` values are color 743, dimension 96, number 70, typography 20, duration 6, cubicBezier 4, fontFamily 1. `EXAMPLE-tokens.json` declares "DTCG / W3C Design Tokens format".
- Gap 1, aliases: there are no DTCG `{group.token}` references at all. Semantic tokens store the resolved hex, and the alias sits beside it in a non-standard `$alias` (`semantic-colour.json`: `background/default/light {$value:"#FFFFFF"}`, `$alias:{light:"color/neutral/15", dark:"surface/digital-black"}`, written as slash paths).
- Gap 2, modes: light and dark are encoded as leaf path segments (`…/hover/light`). DTCG has no modes in its core format; its Resolver/modifier work handles them differently. Themes are separate `*.overrides.json` files plus `_themes.json` (ADR-0011).
- Gap 3, non-standard `$` keys on tokens: `$note` 67, `$contrast` 50, `$alias` 24, `$confidence` 8, `$label` 6, and others. Under DTCG these belong in `$extensions`.
- Gap 4, value syntax: dimensions are strings like `"16px"` (101). Recent DTCG drafts use `{value, unit}` objects, and colours an object with a colour space; hex strings were the older form. 78 bare numbers.

Converting is a mechanical transform: alias recovery from `$alias`, modes into a resolver or a set per mode, extra keys moved into `$extensions`, and value objects. I estimate one generator, with no information lost.

Generators that emit CSS from tokens: `canon/gen_canon_tokens.py` (tokens JSON → canon.css AUTO-GENERATED TOKENS; var name is the path with the mode leaf dropped; light goes to `:root`, dark to `[data-theme="dark"]`, lines 2-11); `gen_snippet_tokens.py` (tokens → each snippet's theme blocks via its manifest); `canon/gen_theme_cascade.py` (themes JSON + snippet manifests → `[data-apollo-theme]` layer); `gen_token_ramp.py` (canon TOKENS sets → AUTO-TOKENS in snippets and proformas). Also `gen_kg_tokens.py` and `gen_radius_derive.py`.

## 6 · Prior record on multi-framework output

Not absent; recorded as intent, never built.

- ADR-0008 (`docs/decisions/ADR-0008-canonical-core-and-adapters.md`, accepted by Dave 2026-07-20) decides that Apollo is the canonical core and that consumers ("Sutherland React, the Common Toolkit, and others later") are reached "by machine-runnable adapters, not hand-ports" (lines 39-43). Every divergence must be "expressible as an automated transform" (lines 45-50). `gen_component_partials.py:11-12` puts runtime class-sharing "at the ADR-0008 adapter boundary".
- `knowledge/_RUNBOOK-onboard-code-library.md` uses a hub-and-spoke model: the Figma node is the hub and `codeBindings.<lib-id>` holds each library's own names. It names `web-components` as an example library id (line 27). Only 4 metas carry a spoke, all `unverified`.
- Launchpad (s305-D45 route B, an A2UI catalogue over MCP): the catalogue is generated from metas (`SPEC-launchpad-day-one.md:84-95`; props become settings, slots become ComponentId, `x-apollo.accepts`). The renderer (step two, "a stretch nothing depends on") would grow from `canon/dv-render.js` and output canon markup with the snippets' classes (line 200). No launchpad directory exists on disk yet. The C1 catalogue is not built.
- The designer skill promises "React (preferred)" with nothing to wire to.
- `_memento_search.py` for "React", "web components", "framework-neutral" and "Angular" returned only loose archive hits (`_GM-ARCHIVE.md:527, 869`; `GOOD-MORNING.md:277`) and no ruling on multi-framework output. The ADR and the runbook above are the record.

## What changing the dependency would take

This is analysis, not a ruling. To make the snippets view-only, three sources must move out of them. The order follows the size of what moves.

1. CSS source. Per-component CSS files, for example `components/<slug>.css`, become what `gen_canon_components` reads. The snippet then links canon.css like any page. Today no snippet links canon.css (0 of 137, `gen_bento_role_vars.py:64`). The 82.8% block would not change in content. Only its origin moves. The manifests move to the meta, which also fixes the 727 prose token entries.
2. Markup. Add an `anatomy` or `template` to each meta (element tree, slots, aria, state attributes). The snippet, the receipt mint and the Launchpad renderer then all render from it. This is the large new piece of work, with 137 to author or extract. They could be extracted from today's snippets once, then reviewed.
3. Behaviour. The roughly 5,800 inline lines move into `canon/*.js`-style modules with a declared event surface (emitted events, not DOM listeners). `behaviour.script` then points at a module instead of `#script` in a snippet (18 metas today).

With those three in place, the snippet becomes generated output (spec + CSS + module → showroom view). Group G gates would keep working, because they read generated snippets. React or web-component adapters would then have a neutral spec to compile from, which is what ADR-0008 already asks for.
