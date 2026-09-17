#!/usr/bin/env python3
"""Build notes/_KG-EXPLORER.html — the component knowledge graph as an interactive explorer.

Reads (never writes) knowledge/components/*.meta.json, _nodes-pattern.json, _nodes-context.json
and knowledge/_rulings.json; lays the graph out deterministically (Fruchterman-Reingold in 2D
and 3D, seeded, numpy) and bakes data + positions into knowledge/_kg_explorer.template.html.

  python3 knowledge/_build_kg_explorer.py            # → notes/_KG-EXPLORER.html
  python3 knowledge/_build_kg_explorer.py OUT.html

Born #266 (2026-09-10). Zero runtime dependencies in the page; numpy at build time.
Islands (disconnected components) are laid on a ring around the giant component; isolated
registered nodes (degree 0) are listed in the page as orphans, not hidden.

v1.2 adds TWO ADDITIVE FAMILIES on top of the component graph, each behind its own chip:
  governance — every ruling in knowledge/_rulings.json (not only the 14 a meta points at),
               plus the sessions they were ruled in, the artefacts they govern and the
               evidence they cite. `mentions` edges are DERIVED (regex over `says`) and are
               drawn dashed; a verb near the mention is recorded as `proposedType` only —
               the edge type stays `mentions` until Dave ratifies it.
  guidelines  — the WCAG success criteria in knowledge/compliance/rules/*.json, the
               guidelines/principles above them, EN 301 549, the HSBC policy and the
               axe-core rules that can check them.
The base component graph is laid out FIRST and UNTOUCHED (same seed, same node set, same
edges as v1.1), so with both new chips off the page is v1.1 to the pixel; the two new
families are laid out separately and parked either side of it.
"""
import json, glob, os, re, sys, datetime, subprocess
VERSION = "1.24"  # 1.24 (#281 lane TV, Dave’s decisions export 11:58Z q3 = (a) and q5 = (a) + the chat, s281-D4 + s281-D5 — “The Explanation view — a ‘cited by a design’ chip beside the polarities” and “System · Governance · Theory — three one-word nouns, verb line under each”) THE THEORY VIEW. Two rulings, one version. s281-D4 ANSWERS THE QUESTION 1.21 HELD. The 14 authored `obeys` component→`ux:` lines had been carried and drawn by nothing at any chip setting since 1.21, because s277-D8 fixed Design governance at three provenances and a `ux:` target is none of them. They are not obligation — they are EXPLANATION: a component naming a principle is the designer CITING a reason, and a reason is read in the view where the principle lives. So they are drawn in the THIRD VIEW, under their own chip, `cited by a design`, beside the UX-principles chip; the builder’s `held` flag is replaced by `cited` and clears on all 14; and Design governance KEEPS ITS THREE PROVENANCES — no fourth sub-chip, s277-D8 not reopened. Force by grade is NOT ruled: these 14 are the hand-authored SEED of applicability and the later ruling is lane RO’s, once rule→principle lines exist. The chip is OFF by default like the rest of that view, so THE DEFAULT CANVAS DOES NOT MOVE — md5 identical, to the byte. Three page predicates carry it: `EON` asks a cited line for `famOn.uxcited` INSTEAD OF its storage family (the chip lives in the Theory box, so turning the HSBC `rule:` chip on is not the price of reading a reason), `recount()` gains the same gate so the header cannot disagree with the canvas, and the stroke is painted the Theory colour while the edge’s STORAGE family stays `guidelinerules`, untouched and still named in INSPECT. The designer’s own `$why` sentence now RIDES THE EDGE: the meta reader took `$note` only, so 168 authored sentences stopped at storage; they are carried in the edge’s own `why` field and read in INSPECT’s ↔ door under the designer’s own words. s281-D5 RENAMES THE TRIAD to SYSTEM · GOVERNANCE · THEORY, three one-word nouns with a verb line under each — what exists / the agent chooses here · what a design must or should do / the agent obeys here · why / the agent consults here. The Constitution keeps its name and is still NOT a view. LABELS ONLY, the s277-D8 clause: no fam KEY, node id or edge type moves, the band ids (`explain`/`design`/`system`) are untouched, and one `BAND_NAME` dict feeds the strata bands, the 3D plates, the 2D rings and the 3D shells so the rename lands once. NO node is added or removed and every baked coordinate set is byte-identical — nothing enters the layout, a flag and four strings change. **14 held lines → 0 held, 14 drawn; the `obeys-ux` orphan set 4 → 0 at every-chip-on.** · 1.23 (#281 lane FO, Dave's export 11:58Z q2 = (a), s281-D2 — “The guideline family owns it; the builder declares the tie instead of resolving it by read order.”) THE DOUBLE-NAMED FILE. A file can be named by TWO records — a ruling’s artefacts (a `governs` entry in `_rulings.json`) and the rule index (`_rule_nodes.json`) — and until now the node was minted by whichever pass ran FIRST. Governance is pass A and the rule family is pass C, so every double-named file became a CONSTITUTION node and pass C’s “never restate a node another family owns” skip dropped the second claim on the floor: the `definedIn` line from every rule inside those files could not be drawn unless the Constitution chip was on. 24 rule: dots were dark that way when lane OC counted them at 1.19; 1.21’s `obeys` wiring lit 13 of them from the other side, leaving 11 at 1.22. s281-D2 does not pick a winner by hand: a new LAST pass, F, runs after every family has spoken, DECLARES the tie on the node (`claimedBy`, both claimants, plus a `tie` sentence and the `fileKind` — all three readable in INSPECT’s record) and assigns the family from a KIND MAP, by what the file IS. `ARTEFACT_KIND` is general and is the only place a kind becomes a family: a `.md` under `knowledge/guidelines/` is a GUIDELINE FILE and belongs to `guidelinerules`; a `.py`/`.sh`/`.js` is a REPO TOOL and hangs off the ruling record in `governance`. A kind the map does not name is left where it stands, marked UNRESOLVED on the node and PRINTED — never decided quietly. 14 files are tied today: 5 guideline files re-homed governance → guidelinerules, 9 repo tools confirmed in governance, 0 of an undeclared kind. A ruling naming a re-homed file STILL draws its artefact line to it: the `governs` edge keeps its governance family and its target is unchanged, so the Constitution loses nothing. NO node is added or removed (4,725 both sides), no edge is invented and the edge multiset is identical; the base graph does not move at all. The BAKED COORDINATES of two families do move, and must: `place_extra` solves each family’s column on its own, so governance (−5) and guidelinerules (+5) are both new solutions of the same solver, and the strata/plates/rings/shells passes re-pack the Design-governance and Constitution bands, which also shifts the `guidelines` family’s DERIVED coordinates (its force `x/y/x3/y3/z3` are byte-identical). **11 dark rule: dots at every-chip-on → 0; 19 dark dots → 8, and the 8 that remain are s277-D7’s logo lockups, leaves by design.** · 1.22 (#281 lane PH, Dave's export 11:58Z q1 = (a), s281-D1 — “Yes — families enter as nodes, and both lines go on.”) PRINCIPLES GET A HOME. The 145 graded UX principles have been in the graph since 1.12 and 100 of them were dark at every chip setting: the only way to reach a principle was through a polarity, and the polarities reach 45. Every principle already knew its research family and the sources it was graded on — both facts sat as ATTRIBUTES on the node, where nothing can walk them. s281-D1 ratifies the two edge types `gen_kg_principles.py` had held behind flags since s275-D2 and switches them on: `inFamily` (145 lines, ux → the new `family:<id>` hub, 32 of them) and `evidencedBy` (134 lines, ux → `evidence:<url>`, 53 new evidence nodes; the 11 principles whose evidence field carries no URL keep a DECLARED NULL with the field's own prose in the note — never dropped, never guessed). The `family` attribute leaves the node as it becomes the edge, so the fact is carried once, not twice; `grade` stays a field (s237-D1). The `family:` node type takes its own type chip and its own plum token beside `--c-ux` and `--c-polarity` — 1.21's second fall-through, learnt: an edge with a family draws nothing when the dot at its end has no chip. ONE predicate moved. `EON` read the family off the TYPE map alone; it now reads the edge's own `fam` first and falls back to the type map, which is what `recount()`'s `famOK` has always done for the counts and what INSPECT's edge door has done since 1.21. It matters because `evidencedBy` is one storage type in TWO families — 1,254 governance lines (a ruling and its evidence) and 134 uxprinciples lines (a principle and its source) — and type-only, the header counted the second lot under the Explanation chip while the canvas drew them only under the Constitution. The change is a MEASURED no-op everywhere else: the only edges whose `fam` disagrees with `FAMILY[type]` are 11 declared nulls, and a null is drawn at no setting. `chipF` and the stroke colour follow the same reading so header, legend and canvas cannot disagree; the 11 nulls move from the wiring chip's count to the assets chip's, where s277-D4/D7 authored them. NO node id, edge type, file or fam KEY moves, `obeys` and its 14 `held` lines are NOT touched, and the Explanation chip still loads OFF. The baked coordinates DO move, for the first time in three versions, and they must: 85 new dots (32 family: + 53 evidence: ) and 279 new lines enter the force layout, so every node's x/y is a new solution of the same solver. **100 dark UX principles → 0; 108 dark dots → 8.** · 1.21 (#281 lane CM, Dave's export 11:02Z — `wire` on homeless-edges, shapes, intents, roles) THE CHIP MAP. Six authored edge types reached storage and stopped there: `answersIntent` 28, `hasDataShape` 26, `providesRole` 108, `yieldsTo` 45 (43 + 2 declared nulls), `defaultActive` 1 (a declared null) and `obeys` 168. Every one of them passed the validator, rode the force layout and was counted in the header's relations — and not one could be drawn, because the page decides what to draw from a type→family map (the template's `FAMILY`) and none of the six was a key in it: `EON` read `famOn[undefined]`, which is `undefined`, which is false. They were never suppressed; they were never addressed. This version gives each of them a family, and nothing else. The five SYSTEM-view types join `rules` — the base wiring chip they already sat beside, on by default — so the 23 shape:, 14 intent: and 12 role: dots light, and the 43 component→component `yieldsTo` lines (composition knowledge that had never once appeared) are drawn for the first time; `yieldsTo`'s 2 declared nulls and `defaultActive`'s 1 are carried and never drawn, the s270-D2 shape. `obeys` joins `guidelinerules` — the HSBC `rule:` sub-chip, because a component obeying a rule is the rule family's own line — and that chip loads OFF, so the 154 component→rule lines change no default. The 14 component→ux lines are HELD: the builder marks them `held:true` with the reason in the record, the page draws nothing for them and no chip can, and the legend says so in words. Where an obligation on a UX principle is drawn is Dave's word (the orphan plan's block 08, answered `ruling`), and a held line is the honest shape of a question that has not been answered — carried, counted, visible in INSPECT, drawn by nothing. No node id, edge type, file or fam KEY moves; no edge is invented; every baked coordinate set is byte-identical, because all six types were already in the layout pass — they were in the graph the whole time, only never on the stage. · 1.20 (#280 lane EX4, s280-D2 — Dave: "I want to see any artifact that exists here, including a render of the actual component snippet" · "no i want to inspect the edge or indeed the actual file") INSPECT OPENS THE ARTEFACT ITSELF. The modal's third section is no longer "the file, as text": it is THE ARTEFACT, rendered by its own kind, behind TABS. A component opens its meta record AND a RENDER tab — the renderedBy snippet live in a sandboxed iframe (sandbox="allow-same-origin", no scripts), its own stylesheet links re-pointed exactly the way gen_showroom.py re-points them for the showroom pane (a srcdoc document inherits the PARENT base URL, so ../canon/type.css becomes ../knowledge/canon/type.css from notes/), data-apollo-theme="mono" and the body's data-theme following the explorer's own light/dark toggle. A snippet renders and shows its source; a rule opens its GUIDELINE markdown with its own {#rule-id} row highlighted and scrolled to; a ruling and a session open their record out of _rulings.json; an icon or logo is DRAWN at 48 and 16 px on both grounds plus its SVG source; an artefact or an evidence node opens its filed markdown (anchor highlighted); an unknown kind still falls through to the raw file with its type, which is 1.19's behaviour kept. EVERY RELATION ROW gains a second door, ↔, which opens THE EDGE ITSELF — storage type, the verb (s277-D11) with this edge's own ends named in the sentence, the split, the family and whether its chip is on, the note, the provenance (authored/derived/ratified/at), where it is stored, born/gone, and the declaration itself when it is a declared null — with both ends as buttons into their own artefacts and a TRAIL of crumbs so the modal walks without closing. NOTHING is embedded: every byte is fetched from the served root, so the page is SERVED, not double-clicked — the repo ships knowledge/_serve_explorer.py (stdlib only, 127.0.0.1, read-only) and the file:// banner names that one command. No node id, edge type, file or fam KEY moves and the default canvas is 1.19 to the md5. · 1.19 (#280 lane EX3, Dave's two sentences on 1.18) (a) THE LEGEND DOES NOT MOVE BY ITSELF. Its place is STICKY — side or bottom — and it stays there until the user moves it with the new `⇥ side / ⇣ bottom` toggle in its own bar (remembered in localStorage under `kg-legend`, beside `kg-theme`). The initial place is computed ONCE at load and again only at a LAYOUT or DIMENSION switch: side when the shown extent is portrait, bottom when it is landscape. A family chip, a dig, a scrub or a search never move it (1.16..1.18 moved it on any chip that made the graph landscape — the jump Dave saw). fit() still measures usable() from wherever the legend is; the phone sheet is unchanged (b) INSPECT. Every node row in the aside — a search hit, a dig group's row, a step of the path — carries a small `i` button, and `i` on the keyboard inspects the dug node. It opens a MODAL over the page with the node's FULL stored record as a definition list (not raw JSON; the six baked coordinate sets collapse to one row), its edges grouped by type and READ with the verb's own wording from knowledge/_kg_verbs.json (s277-D11 — storage untouched), the declared nulls, and a FILE section naming the file the record was read from. The file is FETCHED AT RUNTIME, never embedded: served, its contents render in the modal (md lightly, json pretty, everything else mono); from file:// the fetch fails and the path is shown with a copy button and "open from the repo" — never a blank and never an error. Escape or a click outside closes it and focus is trapped while it is open. Two small BUILD-TIME blocks feed it — `src` (TYPE→path, the per-file sc: join, the per-family file roots) and `verbs` (the twelve verbs as a reading map) — and no node id, edge type, file or fam KEY moves. · 1.18 (#280 lane LM, s280-D1) THE LAYOUT MATRIX — three layouts (FORCE · STRATA · SHELLS) × two dimensions (2D · 3D) on one switch, six cells, force-2D the default and pixel-identical to 1.17. STRATA-3D is the sketch called FLOORS (three translucent plates in an exploded stack, the Constitution a fourth plate beside), SHELLS-2D the sketch called ORBITS (concentric rings, the Constitution an arc outside), SHELLS-3D the Fibonacci spheres with the Constitution as a plinth disc. Three new BUILD-TIME coordinate sets — `xf,yf,zf` / `xo,yo` / `xs,ys,zs` — and `plates`/`rings`/`shells` blocks in the data; `x`, `y`, `x3`, `y3`, `z3`, `y2` are NOT touched. 1.18a ships the strata-3D cell and the two-axis switch; 1.18b adds shells-2D; 1.18 completes the six. · 1.17 (#280 lane LY, s277-D8 rendered rather than ruled) THE STRATA LAYOUT — the three views laid out as three VISIBLE LAYERS, offered as a switch beside the force layout. Every node keeps the builder's `x` (so the columns and clusters below survive left-to-right) and gains a SECOND y, `y2`, packed inside its view's horizontal band by a light force at BUILD time (collide in y only, x frozen, plus a weak pull to the band centre); the bands run top to bottom EXPLANATION · DESIGN GOVERNANCE · SYSTEM, with THE CONSTITUTION as a fourth band below System — the bedrock, dimmed, drawn only when its chip is on. A node's band is its view under the fam→view map the page already carries (VIEWS): base nodes carry no `fam` and are SYSTEM. `x`, `y`, `x3`, `y3`, `z3` are NOT touched — the force layout is in the file byte for byte and the page opens in `force` unless the switch or `?layout=strata` says otherwise, so the shipped default is 1.16 to the pixel. The page gets a LAYOUT switch in the tool row, a `bands` block in the data (each band's name and its y0/y1), band tints + hairlines + left-edge labels painted under the graph, and cross-band edges drawn brighter than within-band ones — the crossings are the point of the picture. The switch SNAPS (no tween), so a never-driven screenshot is stable as soon as the page settles · 1.16 (#279 lane EX2, the EV fixes on 1.15 — template only, no reader, no layout change, no node/edge/fam key moved) (a) at phone width the legend is a BOTTOM SHEET closed by default to one bar — the graph gets the stage; open, the four view boxes come FIRST and the type rows scroll under them, capped at 62% of the stage so the graph never vanishes; the scrub row is three rows at 390 so its counts no longer clip (b) fit() measures the SHOWN extent on BOTH axes against the USABLE stage (the rectangle above the legend) — the assets column is fitted by width, the axis that binds, not by min(W,H), and a family chip toggle re-fits (c) the legend is COLLAPSIBLE at every width and the stage RESERVES its measured height: fit() and the dig centre in usable(), so no chip row sits on the base hub and no dug neighbour paints through a view box; folding the legend and pressing Fit gives the whole stage back (d) the "rulings a design cites" sub-chip counts the citation edges it GOVERNS under the family chips now (28 at defaults; 341 was a total that included 10 never-drawn nulls and 295 Constitution-only edges) and recount()/the scrub counts/the panel/the path honour the sub-chip, so the header agrees with the canvas when it is toggled; its label and its default are untouched (EV §9, Dave's question) · 1.15 (#279, s277-D8 + s277-D4) ONE GRAPH, THREE VIEWS BY FORCE — the chip bar is re-labelled into SYSTEM (what exists; the agent chooses: structure · usage · rendering · rules & wiring · assets) / DESIGN GOVERNANCE (what a design must or should do; the agent obeys: ONE obligation with THREE provenance sub-chips — WCAG sc: · HSBC rule: · rulings a design cites — each still its own chip, s275-D6) / EXPLANATION (why; the agent consults: UX principles + polarities), and THE CONSTITUTION — the ruling record, 593 rulings with their sessions, evidence and artefacts — named on the page as its own thing, NOT one of the three views. Storage untouched: no node id, edge type, file or fam KEY changes (RULE_FAM/UX_FAM/'governance'/'guidelines' stay; only labels move). A FIFTH additive family behind chip `assets`, OFF by default: the 688 icon:/iconGroup:/logo: nodes from knowledge/_icon_nodes.json + _logo_nodes.json (six edge types drawn — inGroup/activeVariantOf/usesIcon/usesLogo/defaultFor/ruledBy; every `t: null` carried as a declared null, never dropped, never drawn). The precedence ladder and the derived per-ruling scope are UNRATIFIED and are not drawn; the "rulings a design cites" sub-chip is AUTHORED citation only (governedBy from a meta, ruledBy from the asset files, a ruling's own `governs` naming a component) — no scope is derived. edges.obeys is still not drawn (the s276 declared gap, unchanged) · 1.14 (#277, s277-D1..D3) the four chart metas carry edges.obeys — chart-line 24, chart-pie 25, chart-bar 27, chart-donut 11 = 87 new entries, each with an authored `$why` grounded by grep in the live meta (corpus obeys 81 -> 168 across 10 metas); no new family and no new reader — the explorer still does not DRAW edges.obeys (the s276 declared gap, unchanged) · 1.13 (#276, s276-D1..D4) the 17 missing WCAG success criteria land in knowledge/compliance/rules/ (sc: nodes 38 -> 55) so the rules family's 19 declared `cites` nulls all resolve to real sc: nodes — 0 nulls left in _rule_nodes.json; the six authored metas carry edges.obeys (81 entries, 67 rule: + 14 ux:) · 1.12 (#275, s275-D1..D6) a FOURTH additive family behind its own chip: the 145 UX principles + 30 polarities from knowledge/_ux_principle_nodes.json (tensionWith/hasParty/touches/resolvedBy/challengedBy/explainedBy; 15 declared nulls carried, never dropped) · 1.11 (#274, s274-D7..D12) a THIRD additive family behind its own chip: the 470 guideline rules from knowledge/_rule_nodes.json (definedIn/cites/enforcedBy/flaggedBy; 19 declared nulls carried, never dropped) · 1.10 (#267, s267-D3) AUTHORED ruling→ruling edges from knowledge/_ruling_edges.json (solid; supersedesClause dotted), and the regex proposal loop no longer re-proposes a judged pair · … 1.7 halo dots above labels · 1.8 camera-plane ring (flattened the dig — reverted) · 1.9 the dig is a WORLD-SPACE SPHERE again (v1.6 geometry), sector labels ride the same sphere, occlusion mitigated by a <=12px screen-space nudge + occluded dots painted after the focus
from collections import defaultdict
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'knowledge')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'notes', '_KG-EXPLORER.html')

def extract(K=K):
    nodes, edges = {}, []
    def add(id, label=None, **kw):
        n = nodes.setdefault(id, {'id': id, 'type': id.split(':')[0], 'label': label or id.split(':', 1)[1]})
        if label: n['label'] = label  # a component referenced before its own meta is read keeps the slug otherwise
        n.update({k: v for k, v in kw.items() if v})
    for f in ['_nodes-pattern.json', '_nodes-context.json']:
        fp = os.path.join(K, 'components', f)
        if not os.path.exists(fp): continue
        for n in json.load(open(fp)):
            add(n['id'], n.get('label'), sources=n.get('sources'), registered=True)
    rp = os.path.join(K, '_rulings.json')
    rul = {x['id']: x for x in json.load(open(rp)).get('rulings', []) if isinstance(x, dict)} if os.path.exists(rp) else {}
    for f in sorted(glob.glob(os.path.join(K, 'components', '*.meta.json'))):
        slug = os.path.basename(f)[:-10]
        if slug.startswith('EXAMPLE-'): continue  # the schema's worked example, not a component
        try: m = json.load(open(f))
        except Exception: continue
        if not isinstance(m, dict): continue
        cid = 'component:' + slug
        add(cid, m.get('name'), purpose=(m.get('purpose') or '')[:260], category=m.get('category'), interactive=m.get('interactive'))
        for et, lst in (m.get('edges') or {}).items():
            if et.startswith('$') or not isinstance(lst, list): continue
            for e in lst:
                if not isinstance(e, dict): continue
                ref = e.get('ref'); note = (e.get('$note') or e.get('note') or '')[:320]
                # #281 s281-D4 — the designer's own `$why` RIDES THE EDGE. It is authored in the
                # meta beside the ref (168 obeys entries carry one, and no entry carries both a
                # $why and a $note), and until now it stopped at storage: the reader took $note
                # only, so the sentence that says WHY a component cites a principle never reached
                # the page. It is carried in its OWN field, not folded into `note`, because it is
                # a different thing — a note annotates the link, a $why is the reason for it.
                why = (e.get('$why') or '')[:320]
                if not ref:
                    edges.append({'s': cid, 't': None, 'type': et, 'note': note,
                                  **({'why': why} if why else {})}); continue
                if ref.startswith('ruling:'):
                    r = rul.get(ref.split(':', 1)[1], {})
                    ruled = r.get('ruled') if isinstance(r.get('ruled'), str) and len(r.get('ruled')) < 8 else None
                    add(ref, ref.split(':', 1)[1], text=(r.get('says') or '')[:280], date=r.get('date'), ruled=ruled)
                else:
                    add(ref)
                edges.append({'s': cid, 't': ref, 'type': et, 'note': note,
                              **({'why': why} if why else {})})
    for n in nodes.values():
        if n['type'] == 'snippet': n['label'] = n['label'].replace('.reference.html', '')
    return list(nodes.values()), edges

# ---------------------------------------------------------------- v1.2: governance + guidelines
MENTION_RX = re.compile(r's\d{2,3}-D\d+|ds-\d{3}|DV-D\d+|ADR-\d{4}(?:-A\d)?|T-D\d+|B-D\d+|GM-D\d+(?:-am)?')
VERB_STEMS = {'supersedes': 'supersed', 'retires': 'retir', 'narrows': 'narrow', 'refines': 'refin',
              'corrects': 'correct', 'enacts': 'enact', 'extends': 'extend', 'bounds': 'bound',
              'confirms': 'confirm', 'overrides': 'overrid'}
# #267 s267-D3 defect 1 (lane E, :81): the stem had a LEFT boundary only, so `enact` hit
# "enactment", `overrid` hit "override sets"/"overrides.json", `narrow` hit "NARROWEST",
# `correct` hit "correctly", `refin` hit "refinement". A right boundary + an explicit inflection
# set fixes those. LIMIT, declared: a regex has no part of speech — a bare infinitive
# ("supersede") is not matched, and a plural noun spelled like a verb ("the overrides") still is;
# only the file-extension form ("overrides.json") is excluded, by the lookahead.
VERB_RX = {k: re.compile(r'\b' + v + r'(?:s|es|d|ed|ing)?\b(?!\.[a-z])', re.I)
           for k, v in VERB_STEMS.items()}
RULING_EDGES = '_ruling_edges.json'


def ruling_edges(K=K):
    """The AUTHORED ruling->ruling edges ratified by s267-D3. Returns (edges, suppress_pairs)."""
    fp = os.path.join(K, RULING_EDGES)
    if not os.path.exists(fp): return [], set()
    try: d = json.load(open(fp))
    except Exception: return [], set()
    E = [e for e in d.get('edges', []) if isinstance(e, dict) and e.get('s') and e.get('t')]
    sup = set()
    for e in E:
        sup.add((e['s'], e['t']))
        fp2 = e.get('from_pair')
        if isinstance(fp2, list) and len(fp2) == 2: sup.add(tuple(fp2))
    plain = set()
    for p in d.get('ratified_plain_mentions', []):
        pr = p.get('pair') if isinstance(p, dict) else p
        if isinstance(pr, list) and len(pr) == 2: plain.add(tuple(pr))
    return E, (sup, plain)


# ---------------------------------------------------------------- #274 s274-D7..D12: the rule family
RULE_NODES = '_rule_nodes.json'
RULE_FAM = 'guidelinerules'   # NOT 'rules': that family key is taken by the base wiring chip

# ---------------------------------------------------------------- #281 s281-D2: THE DOUBLE-NAMED FILE
# One file can be named by TWO records — a ruling's artefacts (a `governs` entry in
# knowledge/_rulings.json) and the rule index (knowledge/_rule_nodes.json). Until 1.22 the node was
# minted by whichever pass ran FIRST: governance (pass A) runs before the rule family (pass C), and
# pass C's "never restate a node another family owns" skip then dropped the second claim on the
# floor. The file became a Constitution node, and the `definedIn` line from every rule inside it
# could not be drawn unless the Constitution chip was on.
#
# s281-D2 (Dave, 2026-09-17): the guideline family owns it; the builder DECLARES the tie instead of
# resolving it by read order. Both claimants are recorded on the node (`claimedBy`), and the family
# is assigned by WHAT THE FILE IS — never by pass order. A ruling naming it still draws its artefact
# line to it, because the `governs` edge keeps its own governance family and its target is unchanged.
#
# The kind map is the only place a file kind turns into a family. It is general: any future
# double-named file follows it, and a kind it does not name is REPORTED, not decided quietly.
ARTEFACT_KIND = (
    # (predicate on the path, family, the kind's name for the record)
    (lambda p: p.startswith('knowledge/guidelines/') and p.endswith('.md'), RULE_FAM, 'guideline file'),
    (lambda p: p.rsplit('.', 1)[-1] in ('py', 'sh', 'js', 'mjs'), 'governance', 'repo tool'),
)


def artefact_kind(node_id):
    """(family, kind name) for a double-named artefact, by file kind (s281-D2), or (None, None)
    for a kind this ruling does not name — the tie is still declared, the family is left where it
    was, and the builder prints it so the next ruling has something to rule on."""
    if not node_id.startswith('artefact:'): return None, None
    p = node_id.split(':', 1)[1].strip()
    for pred, fam, kind in ARTEFACT_KIND:
        if pred(p): return fam, kind
    return None, None


def rule_nodes(K=K):
    """The 470 tagged guideline rules landed by gen_kg_rules.py --land --ratified s274-D8
    (s274-D7 node kind, s274-D8 the four edge types, s274-D11 this reader). Returns (nodes, edges)."""
    fp = os.path.join(K, RULE_NODES)
    if not os.path.exists(fp): return [], []
    try: d = json.load(open(fp))
    except Exception: return [], []
    return d.get('nodes', []), d.get('edges', [])


# ------------------------------------------------- #275 s275-D1..D6: the UX-principle family
UX_NODES = '_ux_principle_nodes.json'
UX_FAM = 'uxprinciples'   # the landed file's own `family` key; free in FAMILY/FAMLABEL


def ux_principle_nodes(K=K):
    """The 145 ux:<id> principle nodes and 30 polarity:<id> nodes landed by
    gen_kg_principles.py --land --ratified s275-D2 (s275-D1 the twelve fields, s275-D2 the six
    edge types, s275-D3 the polarity node, s275-D6 this reader). Returns (nodes, edges)."""
    fp = os.path.join(K, UX_NODES)
    if not os.path.exists(fp): return [], []
    try: d = json.load(open(fp))
    except Exception: return [], []
    return d.get('nodes', []), d.get('edges', [])


# ------------------------------------------------- #279 s277-D4 (+ D5..D7): the assets family
ASSET_FILES = ('_icon_nodes.json', '_logo_nodes.json')
ASSET_FAM = 'assets'   # the landed files' own `family` key; free in FAMILY/FAMLABEL (lane IL checked; re-checked #279)
ASSET_DRAWN = ('inGroup', 'activeVariantOf', 'usesIcon', 'usesLogo', 'defaultFor', 'ruledBy')  # the six; defaultActive + governedBy are DECLARED-NULL ONLY


def asset_nodes(K=K):
    """The 688 icon:<slug> (666) / iconGroup:<slug> (10) / logo:<slug> (12) nodes landed by
    gen_kg_icons.py --land --ratified s277-D4 (f641242; the declared nulls in-file at 84658db).
    Same reader shape as rule_nodes(): a missing or unreadable file is [], []. Returns (nodes, edges)
    with the two files concatenated — icons first, logos second."""
    N, E = [], []
    for fn in ASSET_FILES:
        fp = os.path.join(K, fn)
        if not os.path.exists(fp): continue
        try: d = json.load(open(fp))
        except Exception: continue
        N += d.get('nodes', []); E += d.get('edges', [])
    return N, E
PRINCIPLE = {'1': 'perceivable', '2': 'operable', '3': 'understandable', '4': 'robust'}
POLICY_ID = 'policy:hsbc-digital-accessibility-framework'
STANDARD_ID = 'standard:en-301-549'
SESSION_RX = re.compile(r'^#(\d+)')  # "#81-D1" → session #81; anything with no leading #N has no session


def rulings(K=K):
    fp = os.path.join(K, '_rulings.json')
    if not os.path.exists(fp): return []
    try: d = json.load(open(fp))
    except Exception: return []
    return [x for x in d.get('rulings', []) if isinstance(x, dict) and x.get('id')]


def ruling_ids(K=K):
    return sorted({r['id'] for r in rulings(K)})


def sc_rules(K=K):
    out = []
    for f in sorted(glob.glob(os.path.join(K, 'compliance', 'rules', '*.json'))):
        try: r = json.load(open(f))
        except Exception: continue
        if isinstance(r, dict) and r.get('sc'): out.append(r)
    return out


def sc_ids(K=K):
    return sorted({r['sc'] for r in sc_rules(K)})


def extract_extra(base_nodes, base_edges, K=K):
    """The two new families. Returns (nodes, edges, report). Never touches the base graph."""
    base = {n['id'] for n in base_nodes}
    comp_slugs = {n['id'].split(':', 1)[1] for n in base_nodes if n['type'] == 'component'}
    snip_ids = {n['id'] for n in base_nodes if n['type'] == 'snippet'}
    # applies_to names are matched against the meta's OWN `name` field, read from the meta files —
    # NOT against the node label (a node first created by another component's ref keeps the slug as
    # its label, so labels are not a reliable index) and NOT fuzzily. A miss is reported, not guessed.
    comp_by_name = {}
    for f in sorted(glob.glob(os.path.join(K, 'components', '*.meta.json'))):
        slug = os.path.basename(f)[:-10]
        if slug.startswith('EXAMPLE-') or ('component:' + slug) not in base: continue
        try: m = json.load(open(f))
        except Exception: continue
        if isinstance(m, dict) and m.get('name'): comp_by_name.setdefault(m['name'], 'component:' + slug)
    snip_to_comp = {}
    for e in base_edges:
        if e.get('t') and e['t'].startswith('snippet:') and e['s'].startswith('component:'):
            snip_to_comp.setdefault(e['t'], e['s'])

    nodes, edges = {}, []
    rep = defaultdict(int); rep['unmatched_applies_to'] = []; rep['proposed'] = defaultdict(int)
    rep['authored_by_type'] = defaultdict(int)
    rep['tied_rehomed'] = []; rep['tied_kind_unknown'] = []; rep['tied_confirmed'] = []
    # s281-D2: every family that NAMES a node records its claim here, whether or not it got to mint
    # it. Pass F below reads this and declares the ties. Recording a claim never creates a node.
    claims = defaultdict(set)

    def add(id, label, fam, **kw):
        n = nodes.setdefault(id, {'id': id, 'type': id.split(':')[0], 'label': label, 'fam': fam})
        n.update({k: v for k, v in kw.items() if v not in (None, '', [], {})})
        return id

    def link(s, t, ty, fam, **kw):
        e = {'s': s, 't': t, 'type': ty, 'note': kw.pop('note', ''), 'fam': fam, 'authored': kw.pop('authored', True)}
        e.update({k: v for k, v in kw.items() if v not in (None, '', [], {})})
        edges.append(e); return e

    def gov_target(entry):
        m = re.match(r'^knowledge/components/(.+)\.meta\.json$', entry.strip())
        if m and m.group(1) in comp_slugs:
            rep['governs_to_component'] += 1; return 'component:' + m.group(1)
        m = re.search(r'([^/\s]+\.reference\.html)$', entry.strip())
        if m:
            sid = 'snippet:' + m.group(1)
            if sid in snip_to_comp:
                rep['governs_to_component'] += 1; return snip_to_comp[sid]
            if sid in snip_ids:
                rep['governs_to_component'] += 1; return sid
        rep['governs_to_artefact'] += 1
        aid = 'artefact:' + entry.strip()
        claims[aid].add('governance')          # s281-D2: the ruling record's claim on this file
        return add(aid, entry.strip(), 'governance')

    # ---- A. governance
    R = rulings(K)
    rid_set = {r['id'] for r in R}
    for r in R:
        rid = 'ruling:' + r['id']
        if rid in base:  # already a base node (a meta points at it) — leave it in the base family
            nodes.pop(rid, None)
        else:
            add(rid, r['id'], 'governance', text=(r.get('says') or '')[:280], date=r.get('date'),
                ruled=r.get('ruled'), by=r.get('by'), status=(r.get('status') or '')[:180])
        for g in (r.get('governs') or []):
            if isinstance(g, str) and g.strip(): link(rid, gov_target(g), 'governs', 'governance', note=g.strip()[:200])
        for ev in (r.get('evidence') or []):
            if not (isinstance(ev, str) and ev.strip()): continue
            eid = add('evidence:' + ev.strip(), ev.strip()[:110], 'governance', full=ev.strip()[:300])
            link(rid, eid, 'evidencedBy', 'governance')
        m = SESSION_RX.match(str(r.get('ruled') or ''))
        if m:
            sid = add('session:' + m.group(1), '#' + m.group(1), 'governance')
            link(rid, sid, 'ruledIn', 'governance', note=str(r['ruled'])[:60])
    # ---- A2. AUTHORED ruling -> ruling edges (s267-D3, #267). Solid, never re-proposed below.
    AUTH, supsets = ruling_edges(K)
    SUPPRESS, PLAIN = (supsets if supsets else (set(), set()))
    for e in AUTH:
        if e['s'] not in rid_set or e['t'] not in rid_set:
            rep['authored_ruling_edges_skipped'] += 1; continue
        ev = ' · '.join(str(x) for x in (e.get('evidence') or []))
        link('ruling:' + e['s'], 'ruling:' + e['t'], e['type'], 'governance',
             authored=True, derived=False, ratified=e.get('ratified'),
             note=((e.get('ratified') or '') + ' · ' + ev).strip(' ·')[:300])
        rep['authored_ruling_edges'] += 1
        rep['authored_by_type'][e['type']] += 1

    # mentions — DERIVED, dashed, unratified
    seen = set()
    for r in R:
        says = r.get('says') or ''
        ms = [m for m in MENTION_RX.finditer(says)]
        for i, m in enumerate(ms):
            t = m.group(0)
            if t not in rid_set or t == r['id'] or (r['id'], t) in seen: continue
            seen.add((r['id'], t))
            pair = (r['id'], t)
            if pair in SUPPRESS:  # an AUTHORED edge already carries this pair — no citation, no proposal
                rep['mentions_suppressed_authored'] += 1; continue
            # defect 2 (:188): the +-80 window must not cross a NEIGHBOURING mention id — a list
            # ("s122-D1, s123-D1, s131-D1") used to hand one verb to every id in it.
            lo = ms[i - 1].end() if i else 0
            hi = ms[i + 1].start() if i + 1 < len(ms) else len(says)
            a, b = max(lo, m.start() - 80), min(hi, m.end() + 80)
            win = says[a:b]
            hit = None
            for k, rx in VERB_RX.items():
                mm = rx.search(win)
                if mm and (hit is None or mm.start() < hit[1]): hit = (k, mm.start())
            proposed = hit[0] if hit else None
            # defect 3 (:191): no direction test. Simplest honest version — if the verb reads AFTER
            # the mention ("<t> supersedes this"), the subject is t, so the proposal runs t -> s.
            # LIMIT, declared: passive voice and parenthetical citation ("CORRECTED BY ... (see X)")
            # still read s -> t, and a third ruling named as the actor is not detected at all.
            pdir = None
            if proposed:
                if a + hit[1] >= m.end(): pdir = 't->s'
                else: pdir = 's->t'
            if pair in PLAIN:  # ratified as a PLAIN citation by s267-D3 — cite, never re-propose
                proposed = pdir = None
                rep['mentions_ratified_plain'] += 1
            if proposed: rep['proposed'][proposed] += 1; rep['proposed_total'] += 1
            link('ruling:' + r['id'], 'ruling:' + t, 'mentions', 'governance', authored=False,
                 derived=True, proposedType=proposed, proposedDir=pdir, at=m.start(),
                 note=(('proposed ' + proposed + (' (' + pdir + ')' if pdir else '') + ' · ')
                       if proposed else '') + win.strip()[:200])
            rep['mentions'] += 1

    # ---- B. guidelines
    gi = {}
    gip = os.path.join(K, 'compliance', 'graph-index.json')
    if os.path.exists(gip):
        try: gi = json.load(open(gip))
        except Exception: gi = {}
    verif = ((gi.get('verification') or {}).get('by_sc') or {})
    for r in sc_rules(K):
        sc = r['sc']; g = '.'.join(sc.split('.')[:2]); p = PRINCIPLE.get(sc.split('.')[0], 'perceivable')
        src = r.get('sources') or {}; chk = r.get('check') or {}
        axe = [a for a in (r.get('external_automatable_refs') or []) if isinstance(a, dict) and a.get('rule_id')]
        v = verif.get(sc)
        scid = add('sc:' + sc, f"{sc} {r.get('title', '')}".strip(), 'guidelines',
                   level=r.get('level'), severity=r.get('severity'), checkType=chk.get('type'),
                   checkDesc=(chk.get('description') or '')[:260], threshold=chk.get('threshold'),
                   verified=bool(v), axeCount=len(axe), enClause=src.get('en301549_clause'),
                   policy=(src.get('internal_policy_ref') or '')[:300], wcagUrl=src.get('wcag_url'),
                   versions=r.get('wcag_versions'))
        gid = add('guideline:' + g, g, 'guidelines')
        pid = add('principle:' + p, p, 'guidelines')
        link(scid, gid, 'under', 'guidelines'); link(gid, pid, 'under', 'guidelines')
        for name in (r.get('applies_to') or []):
            cid = comp_by_name.get(name)
            if cid: link(scid, cid, 'appliesTo', 'guidelines'); rep['applies_to_matched'] += 1
            else:
                rep['applies_to_unmatched'] += 1
                if name not in rep['unmatched_applies_to']: rep['unmatched_applies_to'].append(name)
        if src.get('en301549_clause'):
            add(STANDARD_ID, 'EN 301 549', 'guidelines')
            link(scid, STANDARD_ID, 'enClause', 'guidelines', note=src['en301549_clause'])
        if src.get('internal_policy_ref'):
            add(POLICY_ID, 'HSBC digital accessibility framework', 'guidelines')
            link(scid, POLICY_ID, 'boundBy', 'guidelines', note=src['internal_policy_ref'][:200])
        for a in axe:
            aid = add('axe:' + a['rule_id'], a['rule_id'], 'guidelines', url=a.get('url'),
                      version=a.get('source_version'), text=(a.get('description') or '')[:220])
            link(scid, aid, 'checkedBy', 'guidelines', note=(a.get('description') or '')[:200])
        if v and v.get('script'):
            for part in [x.strip() for x in str(v['script']).split('+') if x.strip()]:
                aid = 'artefact:' + part
                claims[aid].add('guidelines')   # s281-D2: the WCAG family's claim (a verification script)
                if aid not in nodes: add(aid, part, 'guidelines')
                link(scid, aid, 'verifiedBy', 'guidelines',
                     note=f"{v.get('mechanism', '')[:180]}".strip() or v.get('artifact', ''))
                rep['verifiedBy'] += 1

    # ---- C. rules (#274, s274-D7..D12) — AUTHORED by knowledge/gen_kg_rules.py, read verbatim.
    RN, RE = rule_nodes(K)
    for n in RN:
        claims[n['id']].add(RULE_FAM)                            # s281-D2: the claim is recorded even when the node is not minted here
        if n['id'] in base or n['id'] in nodes: continue   # never restate a node another family owns
        add(n['id'], n.get('label') or n['id'], RULE_FAM,
            **{k: v for k, v in n.items() if k not in ('id', 'label', 'fam', 'type')})
        rep['rule_nodes'] += 1
    known_r = base | set(nodes)
    for e in RE:
        if e['s'] not in known_r: rep['rule_edges_skipped'] += 1; continue
        if e.get('t') is None:   # s274-D10: a declared null is carried, never dropped
            link(e['s'], None, e['type'], RULE_FAM, note=e.get('note', '')); rep['rule_edges_null'] += 1
        elif e['t'] in known_r:
            link(e['s'], e['t'], e['type'], RULE_FAM, note=e.get('note', '')); rep['rule_edges'] += 1
        else: rep['rule_edges_skipped'] += 1

    # ---- D. UX principles + polarities (#275, s275-D1..D6) — AUTHORED by
    # knowledge/gen_kg_principles.py, read verbatim. Runs after A so the `hasParty` edges that
    # point at a ruling: node find it.
    UN, UE = ux_principle_nodes(K)
    for n in UN:
        claims[n['id']].add(UX_FAM)                            # s281-D2: the claim is recorded even when the node is not minted here
        if n['id'] in base or n['id'] in nodes: continue   # never restate a node another family owns
        add(n['id'], n.get('label') or n['id'], UX_FAM,
            **{k: v for k, v in n.items() if k not in ('id', 'label', 'fam', 'type')})
        rep['ux_nodes'] += 1
    known_u = base | set(nodes)
    for e in UE:
        if e['s'] not in known_u: rep['ux_edges_skipped'] += 1; continue
        if e.get('t') is None:   # s275-D2: an unresolvable target is ref:null with a note
            link(e['s'], None, e['type'], UX_FAM, note=e.get('note', '')); rep['ux_edges_null'] += 1
        elif e['t'] in known_u:
            link(e['s'], e['t'], e['type'], UX_FAM, note=e.get('note', '')); rep['ux_edges'] += 1
        else: rep['ux_edges_skipped'] += 1

    # ---- E. assets (#279, s277-D4..D7) — AUTHORED by gen_kg_icons.py, read verbatim. Runs after A
    # so the 8 `ruledBy` edges that point at a ruling: node find it; usesIcon/usesLogo sources are
    # base component: nodes. A `t: null` edge is a declared null (s277-D6 defaultActive, s277-D7
    # governedBy, the two active orphans, the rail usesLogo): COUNTED, shown in the panel's
    # "declared, unresolved" group, never drawn and never dropped.
    AN, AE = asset_nodes(K)
    for n in AN:
        claims[n['id']].add(ASSET_FAM)                            # s281-D2: the claim is recorded even when the node is not minted here
        if n['id'] in base or n['id'] in nodes: continue   # never restate a node another family owns
        add(n['id'], n.get('label') or n['id'], ASSET_FAM,
            **{k: v for k, v in n.items() if k not in ('id', 'label', 'fam', 'type')})
        rep['asset_nodes'] += 1
    known_a = base | set(nodes)
    for e in AE:
        if e['s'] not in known_a: rep['asset_edges_skipped'] += 1; continue
        note = (e.get('$note') or e.get('note') or e.get('via') or '')[:320]
        if e.get('t') is None:
            link(e['s'], None, e['type'], ASSET_FAM, note=note); rep['asset_edges_null'] += 1
        elif e['t'] in known_a and e['type'] in ASSET_DRAWN:
            link(e['s'], e['t'], e['type'], ASSET_FAM, note=note, theme=e.get('theme'), ruling=e.get('ruling'))
            rep['asset_edges'] += 1
        else: rep['asset_edges_skipped'] += 1

    # ---- F. THE DOUBLE-NAMED FILE (#281, s281-D2). Runs LAST, after every family has spoken, so
    # the claims are complete however the passes are ordered. It adds no node, removes no node,
    # invents no edge and moves no edge: it writes `claimedBy` on the node and, where the kind map
    # names the kind, sets the node's `fam` to the family the FILE belongs to. A base node is left
    # alone — the base graph owns what it owns (the 1.11/1.12/1.15 rule, unchanged).
    for nid in sorted(claims):
        cl = claims[nid]
        if len(cl) < 2 or nid in base or nid not in nodes: continue
        rep['tied'] += 1
        n = nodes[nid]
        n['claimedBy'] = sorted(cl)
        want, kind = artefact_kind(nid)
        if want is None:
            n['tie'] = ('named by ' + ' and '.join(sorted(cl))
                        + '; no file kind is declared for it, so the family is UNRESOLVED and stands where it was (s281-D2)')
            rep['tied_kind_unknown'].append(nid); continue
        n['fileKind'] = kind
        n['tie'] = ('named by ' + ' and '.join(sorted(cl)) + '; it is a ' + kind
                    + ', so the ' + want + ' family owns it — assigned by what the file is, not by pass order (s281-D2)')
        if n['fam'] != want:
            rep['tied_rehomed'].append(f"{nid} ({kind}): {n['fam']} → {want}")
            n['fam'] = want
        else:
            rep['tied_confirmed'].append(f"{nid} ({kind}): {want}")

    # keep only edges whose two ends exist somewhere (base or new)
    known = base | set(nodes)
    edges = [e for e in edges if e['s'] in known and (e['t'] is None or e['t'] in known)]  # s274-D10: `e['t'] is None or` keeps declared nulls
    rep['nodes'] = len(nodes); rep['edges'] = len(edges)
    rep['unmatched_applies_to'] = sorted(rep['unmatched_applies_to'])
    rep['proposed'] = dict(rep['proposed'])
    rep['authored_by_type'] = dict(rep['authored_by_type'])
    return list(nodes.values()), edges, dict(rep)


def date_extra(xnodes, xedges, hist, ndays):
    """born/died for the new families. Rulings and SCs get REAL born dates from the history
    snapshots; every other new node (session/artefact/evidence/guideline/principle/policy/
    standard/axe) inherits the earliest born of the ruling or SC that introduced it, and every
    new EDGE takes born = the later of its two endpoints. That is an APPROXIMATION: the day a
    ruling first names an artefact is not separately recorded, so the edge is dated by its ends."""
    days = sorted(hist)
    born, died = {}, {}
    for key, pref in (('rulings', 'ruling:'), ('scs', 'sc:')):
        for i, d in enumerate(days):
            present = set(hist[d].get(key) or [])
            for x in present:
                born.setdefault(pref + x, i); died[pref + x] = None
            for k in list(born):
                if not k.startswith(pref): continue
                if k.split(':', 1)[1] not in present and died.get(k) is None and born[k] < i: died[k] = i
    byid = {n['id']: n for n in xnodes}
    for n in xnodes:
        if n['id'] in born: n['born'] = born[n['id']]; n['died'] = died.get(n['id'])
    # inherit: seed from ruling/sc ends of each edge
    for _ in range(2):
        for e in xedges:
            for a, b in ((e['s'], e['t']), (e['t'], e['s'])):
                na, nb = byid.get(a), byid.get(b)
                if nb is None or 'born' not in (na or {}): continue
                if 'born' not in nb or nb['born'] > na['born']: nb['born'] = na['born']; nb.setdefault('died', None)
    for n in xnodes:
        n.setdefault('born', max(0, ndays - 1)); n.setdefault('died', None)
    def bo(i):
        n = byid.get(i)
        return (n['born'], n.get('died')) if n else (0, None)
    for e in xedges:
        bs, ds = bo(e['s']); bt, dt = bo(e['t'])
        e['born'] = max(bs, bt)
        dd = [x for x in (ds, dt) if x is not None]
        e['died'] = min(dd) if dd else None


def place_extra(xnodes, xedges, base_extent):
    """Lay the two new families out on their own and park them either side of the base graph,
    so no base position moves. Governance left, guidelines right."""
    if not xnodes: return
    idx = {n['id']: i for i, n in enumerate(xnodes)}
    # s274-D11 · s275-D6 · s277-D4: assets is the FIFTH column, outermost right — the page's fit()
    # now measures the shown extent instead of assuming four columns, so the base fit is untouched.
    for fam, cx in (('governance', -1.0), ('guidelines', 1.0), (RULE_FAM, 2.2), (UX_FAM, -2.2), (ASSET_FAM, 3.4)):
        grp = [n for n in xnodes if n['fam'] == fam]
        if not grp: continue
        loc = {n['id']: i for i, n in enumerate(grp)}
        E = np.array([[loc[e['s']], loc[e['t']]] for e in xedges if e['s'] in loc and e['t'] in loc] or [[0, 0]])
        for dim in (2, 3):
            P = fr(len(grp), E, dim, 34.0 if dim == 2 else 46.0, 240 if dim == 2 else 160, 400, 1266 + dim)
            mx = np.abs(P).max() or 1
            P = P / mx * (base_extent * 0.82)
            for n, i in zip(grp, range(len(grp))):
                v = [round(float(P[i, j]), 1) for j in range(dim)]
                if dim == 2:
                    n['x'] = v[0] + cx * base_extent * 2.05; n['y'] = v[1]
                else:
                    n['x3'] = v[0] + cx * base_extent * 2.05; n['y3'] = v[1]; n['z3'] = v[2]
    del idx


# ---------------------------------------------------------------- #280 s277-D8: the STRATA layout
# ONE GRAPH, THREE VIEWS — laid out as three visible LAYERS. This computes a SECOND y per node,
# `y2`, and touches nothing else: `x`, `y`, `x3`, `y3`, `z3` stay exactly as the force layout left
# them, so the page's default layout is unchanged and the 1.16 file is still in here byte for byte.
# A node's band is its VIEW, read off the same fam→view map the page carries in VIEWS: base nodes
# carry no `fam` and are SYSTEM (what exists), and that includes the handful of ruling: nodes a
# component meta points at directly — they are in the base graph, so they stay in the base's band.
VIEW_OF_FAM = {None: 'system', 'guidelines': 'design', RULE_FAM: 'design',
               UX_FAM: 'explain', ASSET_FAM: 'system', 'governance': 'constitution'}
BAND_ORDER = ['explain', 'design', 'system', 'constitution']  # top → bottom; the Constitution is the bedrock
# #281 s281-D5 — THE TRIAD IS SYSTEM · GOVERNANCE · THEORY. Three one-word nouns with a verb line
# under each (choose · obey · consult), which is the option Dave took in the chat his q5 note asked
# for. LABELS ONLY: the band IDS (`explain`, `design`, `system`, `constitution`), the fam keys they
# are computed from and every node id and edge type are untouched — the s277-D8 clause. These four
# strings feed all four furniture sets (bands, plates, rings, shells), so the rename lands once.
BAND_NAME = {'explain': 'Theory', 'design': 'Governance',
             'system': 'System', 'constitution': 'The Constitution'}


def pack_y(xs, r, band_h, seed, iters=140, win=26):
    """Pack n nodes into a band by relaxing y ONLY — x is frozen, so the left-to-right order the
    force layout produced survives. Two forces: collide (two nodes closer than 2r are pushed apart
    along y, by exactly the y-distance their frozen dx still owes) and a weak pull to the band's
    centre. Neighbours are taken in x order inside a window, which is exact enough because a pair
    further than `win` apart in x order is further than 2r apart in x for any band we build."""
    n = len(xs)
    if n == 0: return np.zeros(0)
    rng = np.random.default_rng(seed)
    o = np.argsort(xs, kind='stable')
    X = xs[o]
    y = rng.uniform(-0.5, 0.5, n) * band_h
    d2 = (2.0 * r) ** 2
    for _ in range(iters):
        for off in range(1, min(win, n)):
            dx = X[off:] - X[:-off]
            need2 = d2 - dx * dx
            m = need2 > 0
            if not m.any(): continue
            a = np.nonzero(m)[0]
            b = a + off
            need = np.sqrt(need2[m])
            dy = y[b] - y[a]
            k = need - np.abs(dy)
            sel = k > 0
            if not sel.any(): continue
            a, b = a[sel], b[sel]
            s = np.sign(dy[sel]); s[s == 0] = 1.0
            push = k[sel] * 0.5 * s
            np.add.at(y, b, push)
            np.add.at(y, a, -push)
        y *= 0.992   # the weak y-centre pull
    out = np.empty(n); out[o] = y
    return out


def strata(nodes, band_h=760.0, gap_frac=0.16):
    """Give every node `view` and `y2`. Returns the band list for the page (name + y0/y1)."""
    for n in nodes:
        n['view'] = VIEW_OF_FAM.get(n.get('fam'), 'system')
    step = band_h * (1.0 + gap_frac)
    centres = {v: (i - (len(BAND_ORDER) - 1) / 2.0) * step for i, v in enumerate(BAND_ORDER)}
    bands = []
    for bi, v in enumerate(BAND_ORDER):
        grp = [n for n in nodes if n['view'] == v]
        cy = centres[v]
        bands.append({'id': v, 'name': BAND_NAME[v], 'y0': round(cy - band_h / 2, 1),
                      'y1': round(cy + band_h / 2, 1), 'n': len(grp)})
        if not grp: continue
        xs = np.array([float(n['x']) for n in grp])
        span = max(1.0, float(xs.max() - xs.min()))
        r = float(np.sqrt(max(1.0, band_h * span / (4.0 * len(grp)))))  # first guess at the collide radius
        y = pack_y(xs, r, band_h, 1280 + bi)
        for _ in range(2):   # calibrate the radius so the pack fills the band instead of over/under-flowing it
            h = float(y.max() - y.min()) or 1.0
            if abs(h - band_h) / band_h < 0.08: break
            r *= float(np.sqrt(band_h / h))
            y = pack_y(xs, r, band_h, 1280 + bi)
        mx = float(np.abs(y).max()) or 1.0
        y = y * min(1.0, (band_h / 2.0) / mx)   # the guarantee: no node leaves its own band
        for n, v2 in zip(grp, y):
            n['y2'] = round(float(v2) + cy, 1)
    return bands


# ---------------------------------------------------------------- #280 s280-D1: the LAYOUT MATRIX
# THREE LAYOUTS × TWO DIMENSIONS = SIX CELLS. FORCE (as built) · STRATA (bands) · SHELLS (concentric),
# each in 2D and 3D. This adds THREE MORE coordinate sets and touches nothing that exists:
#   floors()  → `xf,yf,zf`  STRATA-3D — three translucent plates in an exploded stack, each carrying
#                           its view's own force x,y laid flat on it; the Constitution a fourth plate
#                           BESIDE the stack (LS sketch 3).
#   orbits()  → `xo,yo`     SHELLS-2D — concentric rings, the angle taken from the node's own force
#                           position so neighbours stay neighbours; the Constitution an arc outside
#                           the rings (LS sketch 4).
#   shells3d()→ `xs,ys,zs`  SHELLS-3D — Fibonacci placement on a sphere per view, radius by view, the
#                           Constitution a flat plinth disc under them (LS sketch 2).
# `x`, `y`, `x3`, `y3`, `z3` and `y2` are NOT touched, so force-2D is 1.17 to the pixel and strata-2D
# is 1.17's strata to the pixel. Two honest deviations are lane LS's findings, kept on purpose:
# (1) the 2D force layout parks whole families in far-off columns, so the flat placements use
# PERCENTILE RANK rather than a min–max squash — left is still left, only the spacing is given up;
# (2) the 3D force directions are clumped, so a straight projection onto a sphere gives a blot —
# hence Fibonacci placement handed out in the order of each node's own longitude, which keeps the
# ordering and gives up the spacing. Both are one line to reverse.
PLATE_ORDER = ['explain', 'design', 'system']      # top → bottom in the exploded stack
RING_ORDER = ['system', 'design', 'explain']       # core → outermost ring


def prank(v):
    """Percentile rank in [-0.5, 0.5], stable. LS's flattening: order survives, spacing does not."""
    v = np.asarray(v, dtype=float)
    if len(v) == 0: return v
    o = np.argsort(v, kind='stable'); r = np.empty(len(v)); r[o] = np.arange(len(v), dtype=float)
    return r / max(1.0, len(v) - 1.0) - 0.5


def floors(nodes, plate=1500.0, gap=620.0, aside=1.30):
    """STRATA-3D. Returns the plate list (each plate's centre, its half-width and its height)."""
    plates = []
    for i, v in enumerate(PLATE_ORDER + ['constitution']):
        grp = [n for n in nodes if n['view'] == v]
        if v == 'constitution':
            cy = gap * 0.5; cx = plate * aside          # BESIDE the building, not under it
        else:
            cy = (i - (len(PLATE_ORDER) - 1) / 2.0) * gap; cx = 0.0
        plates.append({'id': v, 'name': BAND_NAME[v], 'y': round(cy, 1), 'cx': round(cx, 1),
                       'half': round(plate / 2.0, 1), 'n': len(grp)})
        if not grp: continue
        px = prank([n['x'] for n in grp]) * plate + cx
        pz = prank([n['y'] for n in grp]) * plate
        for n, a, b in zip(grp, px, pz):
            n['xf'] = round(float(a), 1); n['yf'] = round(float(cy), 1); n['zf'] = round(float(b), 1)
    return plates


def _ring_place(grp, ang, r0, r1, a0, a1):
    """Lay a group into an annulus sector, keeping the cyclic order of `ang` and equalising its
    spacing. Sub-rings are chosen so the angular and the radial spacing come out about equal."""
    n = len(grp)
    span = a1 - a0
    rmid = (r0 + r1) / 2.0
    rows = max(1, int(round(np.sqrt(max(1.0, n * (r1 - r0) / max(1.0, span * rmid))))))
    cols = int(np.ceil(n / rows))
    order = np.argsort(np.asarray(ang), kind='stable')
    out = []
    for k, i in enumerate(order):
        row, col = k % rows, k // rows
        a = a0 + span * ((col + 0.5) / cols)
        r = r0 + (r1 - r0) * ((row + 0.5) / rows)
        out.append((i, r, a))
    return out, rows


def orbits(nodes):
    """SHELLS-2D (the orbits). Returns the ring list — each ring's radii and, for the Constitution,
    its angular sector. A node's angle comes from its own force position, so neighbours stay near."""
    GEO = {'system': (140.0, 560.0, -np.pi, np.pi), 'design': (760.0, 1040.0, -np.pi, np.pi),
           'explain': (1180.0, 1360.0, -np.pi, np.pi),
           'constitution': (1560.0, 2180.0, np.pi * 0.12, np.pi * 1.28)}  # an ARC outside the rings
    rings = []
    for v in RING_ORDER + ['constitution']:
        r0, r1, a0, a1 = GEO[v]
        grp = [n for n in nodes if n['view'] == v]
        rings.append({'id': v, 'name': BAND_NAME[v], 'r0': r0, 'r1': r1,
                      'a0': round(float(a0), 4), 'a1': round(float(a1), 4), 'n': len(grp)})
        if not grp: continue
        ang = [float(np.arctan2(n['y'], n['x'])) for n in grp]
        placed, rows = _ring_place(grp, ang, r0, r1, a0, a1)
        rings[-1]['rows'] = rows
        for i, r, a in placed:
            grp[i]['xo'] = round(float(np.cos(a) * r), 1); grp[i]['yo'] = round(float(np.sin(a) * r), 1)
    return rings


def shells3d(nodes):
    """SHELLS-3D. Fibonacci placement on each view's sphere, the index handed out in the order of the
    node's own longitude in the 3D force layout; the Constitution a flat plinth disc beneath them."""
    R = {'system': 620.0, 'design': 1000.0, 'explain': 1320.0}
    PLINTH_Y, PLINTH_R = 1560.0, 1560.0
    shells = []
    ga = np.pi * (3.0 - np.sqrt(5.0))
    for v in RING_ORDER:
        grp = [n for n in nodes if n['view'] == v]
        shells.append({'id': v, 'name': BAND_NAME[v], 'r': R[v], 'n': len(grp)})
        if not grp: continue
        lon = [float(np.arctan2(n.get('z3', 0.0), n.get('x3', 0.0))) for n in grp]
        order = np.argsort(np.asarray(lon), kind='stable')
        m = len(grp)
        for k, i in enumerate(order):
            y = 1.0 - 2.0 * (k + 0.5) / m          # cos(latitude), evenly spaced
            rr = np.sqrt(max(0.0, 1.0 - y * y)); th = ga * k
            n = grp[i]
            n['xs'] = round(float(np.cos(th) * rr * R[v]), 1)
            n['ys'] = round(float(y * R[v]), 1)
            n['zs'] = round(float(np.sin(th) * rr * R[v]), 1)
    grp = [n for n in nodes if n['view'] == 'constitution']
    shells.append({'id': 'constitution', 'name': BAND_NAME['constitution'], 'plinthY': PLINTH_Y,
                   'r': PLINTH_R, 'n': len(grp)})
    if grp:
        lon = [float(np.arctan2(n.get('z3', 0.0), n.get('x3', 0.0))) for n in grp]
        order = np.argsort(np.asarray(lon), kind='stable'); m = len(grp)
        for k, i in enumerate(order):       # a sunflower disc — the ground the shells stand on
            r = PLINTH_R * np.sqrt((k + 0.5) / m); th = ga * k
            n = grp[i]
            n['xs'] = round(float(np.cos(th) * r), 1); n['ys'] = PLINTH_Y
            n['zs'] = round(float(np.sin(th) * r), 1)
    return shells


def fr(n, Es, dim, k, IT, R0, seed):
    rng = np.random.default_rng(seed)
    pos = rng.normal(size=(n, dim)); pos /= np.linalg.norm(pos, axis=1, keepdims=True); pos *= rng.uniform(0.2, 1, (n, 1)) * R0
    for it in range(IT):
        dd = pos[:, None, :] - pos[None, :, :]; dist = np.sqrt((dd ** 2).sum(-1)) + 1e-6
        fo = np.minimum(k * k / dist, k * 6); np.fill_diagonal(fo, 0)
        disp = ((fo / dist)[..., None] * dd).sum(1)
        if len(Es):
            ed = pos[Es[:, 0]] - pos[Es[:, 1]]; el = np.sqrt((ed ** 2).sum(-1)) + 1e-6
            att = (el * el / k)[:, None] * ed / el[:, None]
            np.add.at(disp, Es[:, 0], -att); np.add.at(disp, Es[:, 1], att)
        disp -= pos * 0.012
        t = max(1.0, k * 1.2 * (1 - it / IT)); l = np.sqrt((disp ** 2).sum(-1))[:, None] + 1e-6
        pos += disp / l * np.minimum(l, t)
    return pos - pos.mean(0)

def layout(nodes, edges, dim):
    ids = [n['id'] for n in nodes]; idx = {k: i for i, k in enumerate(ids)}; N = len(ids)
    E = np.array([[idx[e['s']], idx[e['t']]] for e in edges if e['t']])
    par = list(range(N))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in E: par[f(a)] = f(b)
    comp = defaultdict(list)
    for i in range(N): comp[f(i)].append(i)
    cs = sorted(comp.values(), key=len, reverse=True)
    def sub_edges(c):
        loc = {g: i for i, g in enumerate(c)}
        return np.array([[loc[a], loc[b]] for a, b in E if a in loc and b in loc]) if len(c) > 1 else np.zeros((0, 2), int)
    giant = cs[0]; P = fr(len(giant), sub_edges(giant), dim, 42.0 if dim == 2 else 60.0, 600 if dim == 2 else 350, 600, 266)
    R = np.sqrt((P ** 2).sum(-1)); Rmax = np.percentile(R, 99) * 1.05; P = np.clip(P, -Rmax, Rmax)
    pos = np.zeros((N, dim))
    for g, i in zip(giant, range(len(giant))): pos[g] = P[i]
    isl = [c for c in cs[1:] if len(c) > 1]; ring = Rmax + 140; a0 = 0; tot = sum(len(c) + 2 for c in isl) or 1
    for c in isl:
        span = 2 * np.pi * (len(c) + 2) / tot; a = a0 + span / 2; a0 += span
        sub = fr(len(c), sub_edges(c), dim, 30.0, 200, 30, len(c))
        centre = np.zeros(dim); centre[0] = np.cos(a) * ring; centre[1] = np.sin(a) * ring
        for g, i in zip(c, range(len(c))): pos[g] = sub[i] + centre
    orphans = [c[0] for c in cs[1:] if len(c) == 1]
    for j, g in enumerate(orphans):  # orphans: a short arc at the top, so they are seen
        a = -np.pi / 2 + (j - (len(orphans) - 1) / 2) * 0.12
        pos[g] = 0; pos[g][0] = np.cos(a) * (ring + 90); pos[g][1] = np.sin(a) * (ring + 90)
    pos /= np.abs(pos).max(); pos *= 1000
    return pos, cs, orphans

# ---------------------------------------------------------------- #281 lane CM: the obeys SPLIT
# `edges.obeys` holds two readings in one list — "the rules this component obeys and the laws it
# rests on" (meta.schema.json, s276-D3), and _kg_verbs.json's $splits says so: `must`/`should` when
# the target is a rule:, `rests-on` when it is a ux:. The chip map now gives the type ONE family
# (the HSBC rule: sub-chip, where the 154 component→rule lines belong). The 14 component→ux lines
# were the other branch, and #281 lane CM marked them HELD — carried, readable, drawn by nothing —
# because where an obligation on a UX principle is drawn was Dave's word and nobody had said it.
#
# #281 s281-D4 SAYS IT. Dave's decisions export, q3 = (a): "The Explanation view — a 'cited by a
# design' chip beside the polarities". The 14 lines are EXPLANATION, not obligation: a component
# naming a principle is the designer CITING a reason, and the reason is read in the view where the
# principle lives. Governance stays at THREE provenances — s277-D8 is not reopened and no fourth
# sub-chip is added — and force by grade is NOT ruled here: these 14 are the hand-authored SEED of
# applicability, and whether a high-graded principle carries force is a later ruling, once lane RO's
# rule→principle lines exist. So the flag changes from `held` (drawn by nothing, at any setting) to
# `cited` (drawn under its own chip in the Theory view, OFF by default like the rest of that view).
# The HELD machinery is left standing, unused: it is the right shape for the next question nobody
# has answered, and this ruling answers only this one.
HELD_WHY = ('held pending a ruling: a line whose drawn home has not been ruled — carried in the '
            'data and readable in INSPECT, drawn by no chip at any setting')
CITED_WHY = ('cited by a design: an authored `obeys` from a component to a UX principle. It is '
             'EXPLANATION, not obligation (s281-D4) — the designer citing the reason a rule exists '
             '— so it is drawn in the THEORY view under its own chip, beside the polarities, and '
             'Governance stays at the three provenances s277-D8 fixed. Its storage family is '
             'untouched; force by grade is not ruled by s281-D4.')


def cite_obeys_ux(edges):
    """#281 s281-D4 — mark every obeys edge whose target is a ux: principle as a DESIGN'S CITATION.

    Replaces lane CM's `hold_obeys_ux`: the same 14 edges, the same predicate, a different verdict.
    `held` is not written by this pass any more, so the flag clears on every one of them and the
    legend's held row goes with it. Returns the count."""
    n = 0
    for e in edges:
        if e.get('type') == 'obeys' and str(e.get('t') or '').startswith('ux:'):
            e.pop('held', None); e.pop('heldWhy', None)
            e['cited'] = True
            e['citedWhy'] = CITED_WHY
            n += 1
    return n


def with_history(nodes, edges):
    hp = os.path.join(K, '_kg_history.json')
    if not os.path.exists(hp): return nodes, edges, []
    hist = json.load(open(hp)); days = sorted(hist)
    byid = {n['id']: n for n in nodes}; ekey = lambda e: f"{e['s']}|{e['t']}|{e['type']}"
    ekeys = {ekey(e) for e in edges if e['t']}
    born_n, died_n, born_e, died_e = {}, {}, {}, {}
    for i, d in enumerate(days):
        for nid in hist[d]['nodes']: born_n.setdefault(nid, i); died_n[nid] = None
        for k in hist[d]['edges']: born_e.setdefault(k, i); died_e[k] = None
        # anything born earlier and absent today died today (first absence after presence)
        pn, pe = set(hist[d]['nodes']), set(hist[d]['edges'])
        for nid in list(born_n):
            if nid not in pn and died_n.get(nid) is None and born_n[nid] < i: died_n[nid] = i
        for k in list(born_e):
            if k not in pe and died_e.get(k) is None and born_e[k] < i: died_e[k] = i
    # dead nodes/edges join the graph so the scrub can show them
    for nid, b in born_n.items():
        if nid not in byid:
            n = {'id': nid, 'type': nid.split(':')[0], 'label': nid.split(':', 1)[1].replace('.reference.html', ''), 'dead': True}
            nodes.append(n); byid[nid] = n
    for k, b in born_e.items():
        if k not in ekeys:
            s_, t_, ty = k.split('|'); edges.append({'s': s_, 't': t_, 'type': ty, 'note': '', 'dead': True})
    for n in nodes:
        n['born'] = born_n.get(n['id'], len(days) - 1); n['died'] = died_n.get(n['id'])
    for e in edges:
        if e['t']: e['born'] = born_e.get(ekey(e), len(days) - 1); e['died'] = died_e.get(ekey(e))
    snaps = [{'date': d, 'commit': hist[d]['commit'], 'nodes': len(hist[d]['nodes']), 'edges': len(hist[d]['edges']), 'unresolved': hist[d]['unresolved']} for d in days]
    return nodes, edges, snaps

# ---------------------------------------------------------------- #280 v1.19: what INSPECT needs
# The modal shows the node's own stored record, its edges READ with the verb's wording, and the FILE
# the record was read from. Two tiny blocks are baked for it — a TYPE→path map and the verb map —
# never file CONTENTS: the page fetches the file at runtime (and says so when it cannot).
SRC_BY_TYPE = {
    'component': 'knowledge/components/{slug}.meta.json',
    'snippet':   'knowledge/snippets/{slug}',
    'pattern':   'knowledge/components/_nodes-pattern.json',
    'context':   'knowledge/components/_nodes-context.json',
    'ruling':    'knowledge/_rulings.json',
    'session':   'knowledge/_rulings.json',
    'rule':      'knowledge/' + RULE_NODES,
    'ux':        'knowledge/' + UX_NODES,
    'polarity':  'knowledge/' + UX_NODES,
    # #281 s281-D1 — the research-family hub is landed in the same file as the principles it holds.
    # The `evidence:` nodes of the same file are deliberately NOT given a path here: an entry would
    # claim every evidence: node lives in it, and 900 of the 953 are the Constitution's own filed
    # artefacts. A ux: evidence node's label IS its URL, which is the receipt; the modal falls
    # through to the node's own record, as it did for all 900 before this version.
    'family':    'knowledge/' + UX_NODES,
    'icon':      'knowledge/_icon_nodes.json',
    'iconGroup': 'knowledge/_icon_nodes.json',
    'logo':      'knowledge/_logo_nodes.json',
}
# a node's own declared `file` is relative to its family's own root, not to the repo root
SRC_FILE_ROOT = {'rule': 'knowledge/guidelines/', 'icon': 'knowledge/assets/icons/', 'logo': 'knowledge/'}
# these come from a DIRECTORY of files, not from one: the path is shown, never fetched
SRC_DIRS = ['axe', 'guideline', 'principle', 'policy', 'standard']


def src_block(nodes, K=K):
    """TYPE→path (and the sc: per-file join the builder alone knows). Paths are repo-root-relative."""
    have = {n['id'] for n in nodes}
    byId = {}
    for f in sorted(glob.glob(os.path.join(K, 'compliance', 'rules', '*.json'))):
        try: r = json.load(open(f))
        except Exception: continue
        if isinstance(r, dict) and r.get('sc') and ('sc:' + r['sc']) in have:
            byId['sc:' + r['sc']] = 'knowledge/compliance/rules/' + os.path.basename(f)
    return {'byType': SRC_BY_TYPE, 'fileRoot': SRC_FILE_ROOT, 'dirs': SRC_DIRS, 'byId': byId,
            'dir': 'knowledge/compliance/rules/'}


def verb_block(K=K):
    """THE TWELVE VERBS (s277-D11) as a reading map the page can apply: storage type → verb(s),
    each verb with its force word and its own direction sentence. Storage is untouched."""
    fp = os.path.join(K, '_kg_verbs.json')
    if not os.path.exists(fp): return {}
    try: d = json.load(open(fp))
    except Exception: return {}
    of, verbs = defaultdict(list), {}
    for name, v in d.items():
        if name.startswith('$') or name == 'unread' or not isinstance(v, dict): continue
        if not isinstance(v.get('reads'), list): continue
        verbs[name] = {'force': v.get('force') or name, 'reads': (v.get('direction') or '')[:400]}
        for t in v['reads']:
            if name not in of[t]: of[t].append(name)
    unread = {t: (u.get('$note') or '')[:240] for t, u in (d.get('unread') or {}).items() if isinstance(u, dict)}
    splits = {}
    for t, s in (d.get('$splits') or {}).items():
        if isinstance(s, dict) and isinstance(s.get('branches'), dict):
            splits[t] = {'by': (s.get('by') or '')[:200], 'branches': s['branches']}
    return {'of': dict(of), 'verbs': verbs, 'unread': unread, 'splits': splits}


def main():
    nodes, edges = extract()
    nodes, edges, snaps = with_history(nodes, edges)
    # #281 s281-D4 — the obeys→ux branch, DRAWN now, in the Theory view under its own chip. Runs
    # after with_history() so the dead edges of the scrub carry the flag too (lane CM's placement,
    # kept). `held` is what this pass used to write and writes no longer: the count is 0 by
    # construction, and it is still reported so the page's held row is a measured absence.
    cited = cite_obeys_ux(edges)
    held = sum(1 for e in edges if e.get('held'))
    base_nodes, base_edges = list(nodes), list(edges)
    p2, cs, orphans = layout(nodes, edges, 2)
    p3, _, _ = layout(nodes, edges, 3)
    deg = defaultdict(int)
    for e in edges:
        if e['t']: deg[e['s']] += 1; deg[e['t']] += 1
    for i, n in enumerate(nodes):
        n['x'], n['y'] = round(float(p2[i, 0]), 1), round(float(p2[i, 1]), 1)
        n['x3'], n['y3'], n['z3'] = (round(float(v), 1) for v in p3[i])
        n['deg'] = deg[n['id']]
    # islands + orphans are a LIVE finding: recompute on today's graph, dead edges excluded
    live_nodes = [n for n in nodes if not n.get('dead')]
    live_edges = [e for e in edges if e['t'] and not e.get('dead') and e.get('died') is None]
    _, cs_live, orph_live = layout(live_nodes, live_edges, 2) if live_nodes else (None, [], [])
    islands = [[live_nodes[i]['id'] for i in c] for c in cs_live[1:] if len(c) > 1]
    orphans = [live_nodes[i]['id'] for i in orph_live]
    # ---- v1.2: the two additive families, laid out AFTER (and beside) the untouched base graph
    xnodes, xedges, rep = extract_extra(base_nodes, base_edges)
    hp = os.path.join(K, '_kg_history.json')
    hist = json.load(open(hp)) if os.path.exists(hp) else {}
    date_extra(xnodes, xedges, hist, len(snaps) or 1)
    place_extra(xnodes, xedges, 1000.0)
    xdeg = defaultdict(int)
    for e in xedges: xdeg[e['s']] += 1; xdeg[e['t']] += 1
    for n in xnodes: n['deg'] = xdeg[n['id']]
    nodes = nodes + xnodes; edges = edges + xedges
    # #280 — the second coordinate set. Runs LAST, over the finished node list, and writes only
    # `view` and `y2`; every position the force layout wrote is already final and is left alone.
    bands = strata(nodes)
    # #280 s280-D1 — the LAYOUT MATRIX's second cell: STRATA-3D (the sketch called FLOORS). Runs after
    # strata() because it reads each node's `view`, and writes only `xf,yf,zf`.
    plates = floors(nodes)
    # ... and its third cell: SHELLS-2D (the sketch called ORBITS). Writes only `xo,yo`.
    rings = orbits(nodes)
    # ... and its sixth: SHELLS-3D. Writes only `xs,ys,zs`.
    shells = shells3d(nodes)
    sha = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    data = {'generated': datetime.date.today().isoformat(), 'version': VERSION, 'commit': sha, 'nodes': nodes, 'edges': edges,
            'islands': islands, 'orphans': orphans, 'snaps': snaps, 'bands': bands, 'plates': plates, 'rings': rings, 'shells': shells,
            'src': src_block(nodes), 'verbs': verb_block(),
            'extra': {'nodes': len(xnodes), 'edges': len(xedges),
                      'rulings': sum(1 for n in nodes if n['type'] == 'ruling'),
                      'sc': sum(1 for n in nodes if n['type'] == 'sc'),
                      'derived': sum(1 for e in xedges if e.get('derived')),
                      'assets': rep.get('asset_nodes', 0), 'assetEdges': rep.get('asset_edges', 0),
                      'assetNulls': rep.get('asset_edges_null', 0),
                      'proposed': rep.get('proposed', {}),
                      # #281 lane CM — the held branch, named in the data so the page can say it.
                      # #281 s281-D4 — it is empty now, and the CITED branch is named beside it.
                      'held': held, 'heldType': 'obeys', 'heldTo': 'ux', 'heldWhy': HELD_WHY,
                      'cited': cited, 'citedType': 'obeys', 'citedTo': 'ux',
                      'citedWhy': CITED_WHY}}
    tpl = open(os.path.join(K, '_kg_explorer.template.html')).read()
    html = tpl.replace('__KG__', json.dumps(data, separators=(',', ':')).replace('</script', '<\\/script')).replace('__DATE__', f"v{VERSION} · {data['generated']} · {sha}")
    open(OUT, 'w').write(html)
    print(f"wrote {OUT} · v{VERSION} · snaps {len(snaps)} · nodes {len(nodes)} · edges {len(edges)} · islands {len(islands)} · orphans {len(orphans)} · {os.path.getsize(OUT):,} B")
    lb = [n for n in base_nodes if not n.get('dead') and n.get('died') is None]
    print(f"  base (live): {len(lb)} nodes / {len([e for e in base_edges if e['t'] and not e.get('dead') and e.get('died') is None])} relations"
          f" / {sum(1 for n in lb if n['type'] == 'component')} components")
    print(f"  extra: {rep['nodes']} nodes / {rep['edges']} edges · mentions {rep.get('mentions', 0)} derived"
          f" · governs→component {rep.get('governs_to_component', 0)} / →artefact {rep.get('governs_to_artefact', 0)}"
          f" · appliesTo matched {rep.get('applies_to_matched', 0)} unmatched {rep.get('applies_to_unmatched', 0)}"
          f" · verifiedBy {rep.get('verifiedBy', 0)}")
    print(f"  proposedType: {rep.get('proposed', {})} · PROPOSED TOTAL {rep.get('proposed_total', 0)}"
          f" (pairs already judged by s267-D3: {rep.get('mentions_suppressed_authored', 0)} suppressed as authored,"
          f" {rep.get('mentions_ratified_plain', 0)} ratified plain mentions)")
    print(f"  authored ruling→ruling edges (s267-D3): {rep.get('authored_ruling_edges', 0)}"
          f" {rep.get('authored_by_type', {})}"
          + (f" · SKIPPED (unknown ruling id) {rep['authored_ruling_edges_skipped']}" if rep.get('authored_ruling_edges_skipped') else ''))
    print(f"  rules family (s274-D7..D12, ratified s274-D8): {rep.get('rule_nodes', 0)} new nodes"
          f" / {rep.get('rule_edges', 0)} edges + {rep.get('rule_edges_null', 0)} declared nulls"
          + (f" · SKIPPED {rep['rule_edges_skipped']}" if rep.get('rule_edges_skipped') else ''))
    print(f"  UX-principle family (s275-D1..D6, ratified s275-D2): {rep.get('ux_nodes', 0)} new nodes"
          f" / {rep.get('ux_edges', 0)} edges + {rep.get('ux_edges_null', 0)} declared nulls"
          + (f" · SKIPPED {rep['ux_edges_skipped']}" if rep.get('ux_edges_skipped') else ''))
    print(f"  assets family (s277-D4..D7, ratified s277-D4; chip OFF by default): {rep.get('asset_nodes', 0)} new nodes"
          f" / {rep.get('asset_edges', 0)} edges + {rep.get('asset_edges_null', 0)} declared nulls"
          + (f" · SKIPPED {rep['asset_edges_skipped']}" if rep.get('asset_edges_skipped') else ''))
    print("  strata bands (#280, s277-D8 rendered): " + " · ".join(
        f"{b['name']} {b['n']} @ {b['y0']}…{b['y1']}" for b in bands))
    print("  strata-3D plates (#280, s280-D1): " + " · ".join(
        f"{p['name']} {p['n']} @ y {p['y']} cx {p['cx']} ±{p['half']}" for p in plates))
    print("  shells-2D rings (#280, s280-D1): " + " · ".join(
        f"{r['name']} {r['n']} @ r {r['r0']}…{r['r1']}"
        + (f" arc {round(r['a0'],2)}…{round(r['a1'],2)}" if r['id'] == 'constitution' else '')
        + f" ×{r.get('rows', 0)} rings" for r in rings))
    print("  shells-3D (#280, s280-D1): " + " · ".join(
        f"{h['name']} {h['n']} @ " + (f"plinth y {h['plinthY']} r {h['r']}" if h.get('plinthY') is not None
                                      else f"sphere r {h['r']}") for h in shells))
    ec = defaultdict(int)
    for e in edges:
        if not e.get('dead') and e.get('died') is None: ec[e['type']] += 1
    print("  chip map (#281, s281 lane CM): rules += " + " · ".join(
        f"{t} {ec[t]}" for t in ('answersIntent', 'hasDataShape', 'providesRole', 'yieldsTo', 'defaultActive'))
        + f" · guidelinerules += obeys {ec['obeys'] - cited} · CITED obeys→ux {cited}"
        + f" (s281-D4: drawn in THEORY under its own chip, off by default)"
        + f" · HELD {held} (drawn by nothing)")
    print(f"  double-named files (#281, s281-D2): {rep.get('tied', 0)} tied"
          f" · re-homed {len(rep.get('tied_rehomed') or [])} · already right {len(rep.get('tied_confirmed') or [])}"
          f" · kind not declared {len(rep.get('tied_kind_unknown') or [])}")
    for line in (rep.get('tied_rehomed') or []): print(f"      re-homed  {line}")
    for line in (rep.get('tied_confirmed') or []): print(f"      confirmed {line}")
    for line in (rep.get('tied_kind_unknown') or []): print(f"      UNRESOLVED KIND {line}")
    if rep.get('unmatched_applies_to'): print(f"  UNMATCHED applies_to names: {rep['unmatched_applies_to']}")

if __name__ == '__main__':
    main()
