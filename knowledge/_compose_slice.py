#!/usr/bin/env python3
"""
_compose_slice.py — THE READER: step 1 of generate-from-canon (the thin-slice SEED) and the
ASK door (the on-demand half). One contract, two halves — s277-D10 + s277-D13 under s278-D1.

WHAT IT IS NOW (#279 lane RD). Until #279 this file was a PROPOSAL nothing called. s277-D10
(Dave, 2026-09-16) made it STEP 1 OF GENERATE-FROM-CANON under the thin-slice contract below;
s277-D13 made ASK — the typed-question door for the 12 canonical designer questions — the same
lane; s278-D1 fixed the relationship: the slice is a SEED composed once at step 1, ASK is the
ON-DEMAND door that READS THE CONSTITUTION LIVE (knowledge/_rulings.json + the graph), so a
ruling inscribed after the seed was composed is answerable without recomposing. The consumer
(s274-D11: an instrument without a consumer is refused) is
designer-skills-v2/generate-from-canon/SKILL.md § Procedure step 1, which lands in the same
commit as this contract.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE THIN-SLICE CONTRACT (s277-D10) — the SEED half
═══════════════════════════════════════════════════════════════════════════════════════════════
IN  — build_slice(task=None, *, intent=None, shape=None, roles=None, components=None,
                  budget=None)
      task        the designer's sentence; roles/intents are DERIVED from it when the typed
                  inputs below are absent (ROLE_LEXICON / COMPOSITE_LEXICON / INTENT_LEXICON)
      intent      one or more chart-intent words — knowledge/chart-intents.json `chart-intent`
                  keys (comparison · change-over-time · distribution · relationship ·
                  composition · one-number · …)
      shape       a data shape string as authored on a meta's `shape` field (e.g.
                  "parts-of-whole", "categories × series"); matched against metas' `shape` and
                  the `hasDataShape` edge
      roles       role slugs — knowledge/roles.json `roles` keys (12, s252-D1)
      components  an OPTIONAL explicit component set (meta stems, e.g. ["button", "table"]);
                  forced into the slice with why "named by the caller"
      budget      an OPTIONAL cl100k token budget for the seed. Over budget the seed REDUCES by
                  declared steps (drop alternates, then drop routed obeys) and records each
                  step in `sized.reductions`; if still over it REFUSES loudly (SliceRefused),
                  never truncates silently.
OUT — a dict with exactly these CONTRACT FIELDS (plus $-prefixed metadata, `task`, `query`,
      `generated`). THE HOUSE RULE (s274-D7..D12 shape): every field either carries content or
      is `null` with a note in `$nulls[<field>]` — never absent, never silently empty.
      components  the chosen components, one winner per role plus capped alternates; each row
                  carries id · roles · when · snippet · consumes/hasPart/containedBy/family ·
                  score · alternate · why · blocking
      governs     the RULINGS over those components (Dave's law): (a) `edges.governedBy` on the
                  meta and (b) `_rulings.json` `governs[]` naming the meta path or its snippet —
                  the Q1 join, read LIVE at compose time. Rows: id · ruled (≤200) · date · by ·
                  status · via · over · blocking:true (Dave's `says` is one ASK Q6 away, not seeded)
      obeys       the guideline RULES + UX PRINCIPLES the components obey, in three declared
                  classes, BLOCKING first:
                    authored — `edges.obeys` on the meta (rule:/ux:, with the meta's own $why)
                    derived  — reached by a typed hop the meta did not author: the rule that
                               `flaggedBy` the component's own renderedBy snippet
                               (_rule_nodes.json), and a rule id CITED in the meta's prose but
                               not in edges.obeys
                    routed   — a BLOCKING rule whose FILE is routed by the component's
                               vocabulary (RULE_FILE_ROUTES) or the always-on screen set
                    routed-by-scope — (s277-D9, #279 lane SC) a BLOCKING rule whose FILE's
                               DECLARED SCOPE (knowledge/guidelines/_scope.json, 34 rows)
                               reaches the component: kind component (authored list) or
                               kind facet (the meta binds a token group / field / edge the
                               facet names). Inference by declared scope — never authored,
                               never vocabulary; a null-scope file routes nothing and an
                               exception row suppresses its rule. The non-BLOCKING reach
                               is ASK Q2's `routedByScope`.
                  Each row: id · class · destiny · blocking · file · text (≤280) · why
      mustNot     mustNotNeighbour from both homes (edges + relationships prose) and meta
                  `not-with`, INCLUDING the ref:null entries with their $note — a prohibition
                  is real even where the other end is not yet a node (51 of 70 today)
      tokens      TIER grain — the token GROUP and its tier (semantic / component-type /
                  foundation / primitive / composite), ≤4 example members and an honest count;
                  never the 932 leaves. Type composites ride here as tier "composite".
      assets      icons and logos from the RATIFIED node files knowledge/_icon_nodes.json +
                  _logo_nodes.json (s277-D4..D7, family `assets`): every `usesIcon` /
                  `usesLogo` edge whose source is a chosen component, plus that component's
                  declared-null asset edges. Photos: no node kind — declared, never invented.
      unresolved  everything the slice could NOT resolve, each `ref: null` + `$note` + `why`
      sized       tokens (cl100k, LABELLED estimator — ds-021) of the slice, per field, against
                  the metas it replaces and the whole library; `budget`, `within_budget`,
                  `reductions`

═══════════════════════════════════════════════════════════════════════════════════════════════
ASK (s277-D13) — the ON-DEMAND half
═══════════════════════════════════════════════════════════════════════════════════════════════
  ask(question, seed=None, budget=1000) → {q, verb, node, answer, declared, sized, live}
  python3 knowledge/_compose_slice.py --ask "what governs component:button?"

ASK reads the Constitution LIVE on every call: knowledge/_rulings.json is re-read, the metas'
edges are re-read, the ratified node files are re-read. The seed passed as `seed` is READ ONLY
(it lets ASK say whether the node was in the seed); ASK never mutates it — selftest bite proves
it byte-for-byte. The 12 canonical questions (notes/_lanes/277/kg-audit/A3-AUGMENT.md § 1.2)
map to 12 typed verbs, each with the node kind it takes and the edge types it walks:

  Q1  governs    component     ruling→component (`governs[]` via meta path / snippet) + edges.governedBy
  Q2  binds      rule|ux       component→rule (`edges.obeys`), reversed — which components obey it
  Q3  principle  rule          rule→ux — NO SUCH EDGE TYPE (A1 verdict UNANSWERABLE); answers the
                               rule's own destiny/grade and DECLARES the missing hop
  Q4  conflicts  component     the obeyed ux: principles that carry a `tensionWith` edge between
                               them (+ the polarity) — a 2-hop typed answer; DECLARES that no
                               rule→rule conflict type exists
  Q5  ruled      component|any what Dave ruled and WHEN: governs edges with `ruled` + `date`
  Q6  evidence   ruling        the ruling's `evidence[]` + its authored ruling→ruling edges
  Q7  answers    intent|shape  `answersIntent` / `hasDataShape` edges + meta `answers`/`shape`
  Q8  avoid      component     `mustNotNeighbour` incl. nulls + `not-with`
  Q9  tokens     component     the meta's tokens at group+tier, and the blast radius of each
                               group's members from tokens/_blast-radius.json (a DERIVED index
                               — no token: node kind exists; declared)
  Q10 usedIn     component     `commonPattern` / `usedInContext`
  Q11 wcag       component     sc→component `appliesTo` (compliance/rules applies_to by meta
                               name) + the sc: nodes CITED by the rules it obeys
  Q12 assets     component     `usesIcon` / `usesLogo` + declared nulls; photo: no node kind

Budget: the answer is measured with tiktoken cl100k; over `budget` (default 1,000) ASK REFUSES
LOUDLY (AskRefused, exit 3) naming the count — it never truncates silently. An unmappable
question is a legal refusal naming the FIRST obstacle (no verb · no node · node not in graph).

USAGE
  python3 knowledge/_compose_slice.py "<task sentence>"                     # JSON seed
  python3 knowledge/_compose_slice.py "<task>" --roles page-frame,record-list --intent comparison
  python3 knowledge/_compose_slice.py "<task>" --components button,table --budget 12000
  python3 knowledge/_compose_slice.py "<task>" --explain | --html out.html | --out seed.json
  python3 knowledge/_compose_slice.py --ask "which components does rule:ctkb-003 bind?"
  python3 knowledge/_compose_slice.py --ask "<q>" --budget 600 --seed seed.json
  python3 knowledge/_compose_slice.py --measure         # the s277-D10 claim, re-measured
  python3 knowledge/_compose_slice.py --measure-scope   # the s277-D9 reach figures (obeys / scope / either)
  python3 knowledge/_compose_slice.py --selftest        # named bites, exits 1 on miss

RESOLUTION PATH of the seed (each hop names its source file):
  task / typed inputs
    -> roles (knowledge/roles.json) and intents (knowledge/chart-intents.json)
    -> components (knowledge/components/*.meta.json: name, provides, answers, shape, when …)
    -> their edges (consumes / hasPart / composedOf / containedBy / family)
    -> governs (edges.governedBy + _rulings.json governs[]) · obeys (edges.obeys +
       _rule_nodes.json flaggedBy + _rules-index.json by file) · mustNot · tokens (tokens/*.json
       tiers + typography-composites.json) · assets (_icon_nodes.json / _logo_nodes.json)

THE LEXICON — GROW ON MISS. ROLE_LEXICON below is hand-authored and deliberately seeded, not
exhaustive — the same maintenance model as knowledge/_consult-lexicon.json. A real task that
misses gets ONE line added here.

LIMITS, DECLARED (do not read past them):
  - `provides` is authored on a minority of metas, so role -> component resolution leans on
    roles.json's provider lists AND the `providesRole` edges (108 today) — a MEMBERSHIP join.
  - `_rules-index.json` carries no component tag. The routed class is vocabulary, never passed
    off as authored; the derived class is a typed hop, never passed off as authored; the
    routed-by-scope class is a declared per-file scope (_scope.json), never passed off as either.
  - rule→ux has no edge type (Q3), rule→rule has no conflict type (Q4), token: has no node kind
    (Q9), photo has no node kind (Q12). ASK declares each; nothing here invents one.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json, os, re, sys, glob, html, datetime, copy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
COMPONENTS = os.path.join(HERE, "components")
VERSION = "1.0"   # 1.0 (#279, s277-D10/D13 under s278-D1) the contract + ASK; 0.1 (#270) the proposal
RULED_BY = ("s277-D10", "s277-D13", "s278-D1", "s277-D9")
CONTRACT_FIELDS = ("components", "governs", "obeys", "mustNot", "tokens", "assets", "unresolved", "sized")
ASK_BUDGET = 1000


class SliceRefused(Exception):
    """The seed cannot be handed over as asked. The message names the first obstacle."""


class AskRefused(Exception):
    """ASK cannot answer as asked. The message names the first obstacle."""


# ---------------------------------------------------------------- the hand-authored lexicon
# asker's word -> role slug in knowledge/roles.json. GROW ON MISS (see docstring).
ROLE_LEXICON = {
    "headline-metric": ["stat", "stat card", "kpi", "metric", "metrics", "figure", "big number",
                        "headline number", "tile", "scorecard"],
    "status-surface": ["status", "state", "health", "rag", "threshold", "badge", "traffic light"],
    "chart-panel": ["chart", "charts", "graph", "graphs", "plot", "visualisation", "visualization",
                    "trend", "series", "sparkline", "dataviz"],
    "record-list": ["table", "data table", "datatable", "grid", "rows", "records", "list",
                    "transactions", "transaction", "ledger", "line items", "timeline"],
    "page-frame": ["screen", "page", "dashboard", "app", "shell", "layout", "view"],
    "page-title": ["title", "heading", "header", "page title", "eyebrow"],
    "wayfinding": ["nav", "navigation", "sidebar", "tabs", "breadcrumb", "breadcrumbs",
                   "pagination", "menu", "wayfinding"],
    "action": ["button", "buttons", "action", "actions", "cta", "link", "links", "export",
               "download", "submit"],
    "arrangement": ["card", "cards", "grid", "band", "row", "columns", "bento", "accordion",
                    "carousel", "panel", "panels"],
    "feedback": ["alert", "notification", "toast", "banner", "empty state", "loading",
                 "skeleton", "progress", "error state", "confirmation"],
    "input": ["filter", "filters", "filtering", "search", "form", "field", "fields", "input",
              "dropdown", "select", "date picker", "date range", "picker", "toolbar",
              "filter bar", "controls"],
    "overlay": ["modal", "dialog", "drawer", "popover", "tooltip", "command palette"],
}
# asker's word -> chart intent word in knowledge/chart-intents.json.
INTENT_LEXICON = {
    "comparison": ["compare", "comparison", "ranking", "rank", "versus", "vs", "against target",
                   "by currency", "by category", "breakdown by"],
    "change-over-time": ["trend", "over time", "history", "historical", "monthly", "daily",
                         "growth", "time series", "movement"],
    "distribution": ["distribution", "spread", "histogram", "outliers", "variance", "range of"],
    "relationship": ["correlation", "relationship", "scatter", "against each other"],
    "composition": ["composition", "share", "split", "make-up", "percentage of total",
                    "proportion", "mix"],
}
# component vocabulary -> rule FILE in knowledge/guidelines/_rules-index.json. The routed leg:
# a rule attached this way is class "routed", never authored.
RULE_FILE_ROUTES = {
    "data-visualisation.md": ["chart", "graph", "series", "axis", "dataviz", "plot"],
    "data-visualisation-bar-charts.md": ["bar chart", "column chart", "bar graph"],
    "data-visualisation-line-charts.md": ["line chart", "area chart", "trend line"],
    "data-visualisation-pie-charts.md": ["pie", "donut", "doughnut"],
    "common-toolkit-buttons.md": ["button", "cta", "action"],
    "common-toolkit-links.md": ["link", "anchor"],
    "common-toolkit-notifications.md": ["alert", "notification", "toast", "banner"],
    "common-toolkit-tags-chips.md": ["tag", "chip", "badge", "filter"],
    "common-toolkit-foundations.md": ["toolkit", "foundation"],
    "typography-standards-2026.md": ["typography", "font", "label", "heading", "headline"],
    "typography-usage.md": ["typography", "label", "caption", "body copy"],
    "colour-standards-2026.md": ["colour", "color", "palette", "red", "amber", "green"],
    "colour-usage.md": ["colour", "color", "background", "fill"],
    "icons.md": ["icon", "glyph", "pictogram"],
    "pictograms.md": ["pictogram", "illustration"],
    "accessibility-visual-design.md": ["contrast", "colour", "focus", "visual"],
    "accessibility-interaction-design.md": ["interactive", "keyboard", "target", "hit area",
                                            "focus", "hover", "sort", "filter"],
    "accessibility-content-authoring.md": ["title", "heading", "link", "label", "table"],
    "accessibility-client-side-dev.md": ["aria", "role", "semantics", "live region"],
    "neurodiversity.md": ["motion", "animation", "density", "air", "cognitive"],
    "web-foundations.md": ["page", "screen", "responsive", "reflow", "breakpoint"],
    "copywriting.md": ["label", "copy", "text", "microcopy", "empty state"],
    "tone-of-voice.md": ["copy", "message", "tone"],
    "motion-standards.md": ["motion", "animation", "transition"],
    "naming.md": ["name", "label"],
    "visual-assets.md": ["image", "photo", "asset"],
}
# ALWAYS-ON rule files: a composed SCREEN is always subject to these, whatever it contains.
SCREEN_ALWAYS = ["accessibility-content-authoring.md", "web-foundations.md",
                 "accessibility-visual-design.md"]

# A COMPOSITE task word stands for several roles at once. These are INFERRED roles, flagged
# `inferred: true` so a reader can tell an inference from a request.
COMPOSITE_LEXICON = {
    "dashboard": ["page-frame", "wayfinding", "headline-metric", "chart-panel", "record-list",
                  "page-title"],
    "overview": ["page-frame", "headline-metric", "chart-panel", "page-title"],
    "report": ["page-title", "record-list", "chart-panel"],
}

STOP = set("""a an and are as at be build by can do for from get give has have her his in into is it
its make me my of on one or our page please put screen show that the their them then there they this
to up us use user users want was we what when where which who will with would you your need needs
some such all both each work works working element elements thing things real really just also""".split())


# ---------------------------------------------------------------- loaders (one per source file)
def _load(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default if default is not None else {}


def _read(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return ""


def load_graph(root=HERE):
    """Everything the SEED reads, loaded once. Returns a dict of raw stores."""
    metas = {}
    for f in sorted(glob.glob(os.path.join(root, "components", "*.meta.json"))):
        slug = os.path.basename(f)[:-10]
        if slug.startswith("EXAMPLE-"):
            continue
        m = _load(f)
        if isinstance(m, dict) and m.get("name"):
            m["$slug"] = slug
            m["$path"] = os.path.relpath(f, os.path.dirname(root))
            m["$bytes"] = os.path.getsize(f)
            metas[slug] = m
    g = {
        "metas": metas,
        "roles": _load(os.path.join(root, "roles.json")).get("roles", {}),
        "intents": _load(os.path.join(root, "chart-intents.json")).get("chart-intent", {}),
        "rules": _load(os.path.join(root, "guidelines", "_rules-index.json")).get("rules", []),
        "rulings": {r["id"]: r for r in _load(os.path.join(root, "_rulings.json")).get("rulings", [])
                    if isinstance(r, dict) and r.get("id")},
        "ruling_edges": _load(os.path.join(root, "_ruling_edges.json")).get("edges", []),
        "lexicon": _load(os.path.join(root, "_consult-lexicon.json")).get("synonyms", {}),
        "composites": _load(os.path.join(root, "tokens", "typography-composites.json")),
        "semantic_colour": _load(os.path.join(root, "tokens", "semantic-colour.json")),
        "component_types": _load(os.path.join(root, "component-types.json")).get("component-type", {}),
        "rule_nodes": _load(os.path.join(root, "_rule_nodes.json")),
        "ux_nodes": _load(os.path.join(root, "_ux_principle_nodes.json")),
        "icon_nodes": _load(os.path.join(root, "_icon_nodes.json")),
        "logo_nodes": _load(os.path.join(root, "_logo_nodes.json")),
        "scope": _load(os.path.join(root, "guidelines", "_scope.json")),   # s277-D9 (#279 lane SC)
        "$root": root,
    }
    g["rules_by_id"] = {r["id"]: r for r in g["rules"] if isinstance(r, dict) and r.get("id")}
    g["token_tiers"] = _token_tier_map(g, root)
    g["ux_by_id"] = {n["id"]: n for n in (g["ux_nodes"].get("nodes") or []) if n.get("id")}
    g["rule_node_by_id"] = {n["id"]: n for n in (g["rule_nodes"].get("nodes") or []) if n.get("id")}
    return g


def _token_tier_map(g, root):
    """group name -> (tier, source file). TIER grain is the whole point: a slice names the
    token GROUP and its tier, never the leaves (932 of them at last count)."""
    tiers = {}
    for grp in g["semantic_colour"]:
        if not grp.startswith("$"):
            tiers[grp] = ("semantic", "tokens/semantic-colour.json")
    for grp in g["component_types"]:
        if not grp.startswith("$"):
            tiers.setdefault(grp, ("component-type", "component-types.json"))
    for fn in ("spacing.json", "layout.json", "typography.json", "elevation.json", "motion.json",
               "opacity.json", "icon-scale.json"):
        d = _load(os.path.join(root, "tokens", fn))
        for grp in d:
            if not grp.startswith("$"):
                tiers.setdefault(grp, ("foundation", "tokens/" + fn))
    for grp in _load(os.path.join(root, "tokens", "colour.json")):
        if not grp.startswith("$"):
            tiers.setdefault(grp, ("primitive", "tokens/colour.json"))
    return tiers


# ---------------------------------------------------------------- the LIVE graph (ASK's substrate)
META_PATH_RX = re.compile(r"^knowledge/components/(.+)\.meta\.json$")
SNIP_RX = re.compile(r"([^/\s]+\.reference\.html)$")


def load_live(root=HERE):
    """The graph as the Constitution holds it NOW — re-read on every call, never cached across
    calls. Edges are {s, t, type, note, via, fam}; t is None for a declared null (carried,
    never dropped — s274-D10). The joins are the explorer's own (`_build_kg_explorer.extract`
    + `extract_extra`): a ruling's `governs[]` entry resolves to component:<stem> by meta path,
    or through the snippet's renderedBy owner; compliance `applies_to` matches the meta's own
    `name`. Selftest cross-checks the shared edge-type counts against the explorer when it is
    importable, so the two readers cannot drift silently."""
    g = load_graph(root)
    nodes, edges = {}, []

    def add(nid, **kw):
        n = nodes.setdefault(nid, {"id": nid, "type": nid.split(":")[0]})
        n.update({k: v for k, v in kw.items() if v not in (None, "", [], {})})
        return nid

    def link(s, t, ty, fam, note="", **kw):
        e = {"s": s, "t": t, "type": ty, "fam": fam, "note": (note or "")[:320]}
        e.update({k: v for k, v in kw.items() if v not in (None, "", [], {})})
        edges.append(e)
        return e

    snip_owner, name_to_id = {}, {}
    for slug, m in g["metas"].items():
        cid = add("component:" + slug, label=m.get("name"), purpose=(m.get("purpose") or "")[:200],
                  category=m.get("category"), provides=m.get("provides"), answers=m.get("answers"),
                  shape=m.get("shape"), meta=m["$path"])
        name_to_id.setdefault(m.get("name"), cid)
        for et, lst in (m.get("edges") or {}).items():
            if et.startswith("$") or not isinstance(lst, list):
                continue
            for e in lst:
                if not isinstance(e, dict):
                    continue
                ref = e.get("ref")
                note = e.get("$note") or e.get("note") or e.get("$why") or ""
                if ref:
                    add(ref)
                    if et == "renderedBy":
                        snip_owner.setdefault(ref, cid)
                link(cid, ref or None, et, "components", note=note)
    # governance — LIVE from _rulings.json
    for rid, r in g["rulings"].items():
        nid = add("ruling:" + rid, date=r.get("date"), by=r.get("by"), ruled=r.get("ruled"),
                  says=(r.get("says") or "")[:280], status=r.get("status"))
        for gv in (r.get("governs") or []):
            if not (isinstance(gv, str) and gv.strip()):
                continue
            gv = gv.strip()
            mm = META_PATH_RX.match(gv)
            if mm and ("component:" + mm.group(1)) in nodes:
                link(nid, "component:" + mm.group(1), "governs", "governance", note=gv, via="governs[] meta path")
                continue
            sm = SNIP_RX.search(gv)
            if sm and ("snippet:" + sm.group(1)) in snip_owner:
                link(nid, snip_owner["snippet:" + sm.group(1)], "governs", "governance", note=gv,
                     via="governs[] snippet -> renderedBy owner")
                continue
            link(nid, add("artefact:" + gv), "governs", "governance", note=gv, via="governs[] artefact")
        for ev in (r.get("evidence") or []):
            if isinstance(ev, str) and ev.strip():
                link(nid, add("evidence:" + ev.strip()[:200]), "evidencedBy", "governance", note=ev.strip()[:300])
    for e in g["ruling_edges"]:
        s, t = e.get("s"), e.get("t")
        if s in g["rulings"] and t in g["rulings"]:
            link("ruling:" + s, "ruling:" + t, e.get("type") or "relates", "governance",
                 note=" · ".join(str(x) for x in (e.get("evidence") or []))[:300], ratified=e.get("ratified"))
    # compliance — sc: nodes and appliesTo by the meta's own name
    for f in sorted(glob.glob(os.path.join(root, "compliance", "rules", "*.json"))):
        r = _load(f)
        if not isinstance(r, dict) or not r.get("sc"):
            continue
        sid = add("sc:" + r["sc"], label=("%s %s" % (r["sc"], r.get("title") or "")).strip(),
                  level=r.get("level"), severity=r.get("severity"),
                  check=((r.get("check") or {}).get("description") or "")[:200])
        for name in (r.get("applies_to") or []):
            cid = name_to_id.get(name)
            if cid:
                link(sid, cid, "appliesTo", "guidelines")
            else:
                link(sid, None, "appliesTo", "guidelines", note="applies_to '%s' matches no meta name" % name)
    # the three ratified families, read verbatim
    for store, fam in ((g["rule_nodes"], "rules"), (g["ux_nodes"], "uxprinciples"),
                       (g["icon_nodes"], "assets"), (g["logo_nodes"], "assets")):
        for n in (store.get("nodes") or []):
            if n.get("id"):
                add(n["id"], **{k: v for k, v in n.items() if k not in ("id", "type", "fam")})
        for e in (store.get("edges") or []):
            if e.get("s"):
                link(e["s"], e.get("t"), e.get("type"), fam,
                     note=e.get("$note") or e.get("note") or e.get("via") or e.get("mediatingVariable") or "",
                     **{k: v for k, v in e.items() if k in ("polarity", "ruling", "theme")})
    live = {
        "nodes": nodes, "edges": edges, "g": g,
        "read": {
            "rulings": len(g["rulings"]),
            "rulings_mtime": _mtime(os.path.join(root, "_rulings.json")),
            "metas": len(g["metas"]),
            "at": datetime.datetime.now().isoformat(timespec="seconds"),
        },
    }
    out_i, in_i = {}, {}
    for e in edges:
        out_i.setdefault(e["s"], []).append(e)
        if e["t"]:
            in_i.setdefault(e["t"], []).append(e)
    live["out"], live["in"] = out_i, in_i
    return live


def _mtime(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).isoformat(timespec="seconds")
    except Exception:
        return None


# ---------------------------------------------------------------- stage 1: the task sentence
def terms_of(task, lexicon):
    raw = re.findall(r"[a-z][a-z0-9-]+", (task or "").lower())
    terms, why = [], {}
    for w in raw:
        if w in STOP or len(w) < 3:
            continue
        base = w[:-1] if w.endswith("s") and len(w) > 4 and not w.endswith("ss") else w
        if base not in terms:
            terms.append(base)
            why[base] = "task"
        for syn in lexicon.get(w, []) if isinstance(lexicon.get(w), list) else \
                ([lexicon[w]] if isinstance(lexicon.get(w), str) else []):
            s = syn.lower()
            if s not in terms:
                terms.append(s)
                why[s] = "_consult-lexicon.json:" + w
    return terms, why


def _wb(word, low):
    return re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", low)


def roles_of(task, terms, g, typed_roles=None):
    """task -> roles. Three legs: the TYPED roles (contract input, wins), the hand lexicon
    (phrase match on the sentence) and a direct hit on a role slug or a provider slug."""
    low = " " + (task or "").lower() + " "
    out = {}
    for role in (typed_roles or []):
        if role in g["roles"]:
            out[role] = {"role": role, "why": "typed input: roles", "hits": [role]}
        else:
            out[role] = {"role": role, "why": "typed input: roles (NOT a roles.json role — declared)",
                         "hits": [role], "unknown": True}
    for role, words in ROLE_LEXICON.items():
        for w in words:
            if _wb(w, low):
                out.setdefault(role, {"role": role, "why": 'ROLE_LEXICON["%s"] <- "%s"' % (role, w),
                                      "hits": []})
                out[role]["hits"].append(w)
    for word, roles in COMPOSITE_LEXICON.items():
        if _wb(word, low):
            for role in roles:
                if role in out:
                    continue
                out[role] = {"role": role, "hits": [word], "inferred": True,
                             "why": 'COMPOSITE_LEXICON["%s"] -> %s (INFERRED — the task did not '
                                    'name this role)' % (word, role)}
    for role, spec in g["roles"].items():
        if role.replace("-", " ") in low or role in low:
            out.setdefault(role, {"role": role, "why": "roles.json role slug named in task", "hits": [role]})
        for p in spec.get("providers", []):
            slug = p.get("slug", "")
            if slug and _wb(slug.lower().replace("-", " "), low):
                out.setdefault(role, {"role": role, "why": "roles.json provider %s named in task" % slug,
                                      "hits": [slug]})
    for r in out.values():
        spec = g["roles"].get(r["role"], {})
        r["definition"] = (spec.get("definition") or "")[:180]
        r["providers"] = [p.get("slug") for p in spec.get("providers", [])]
        r["blocking"] = False
    return list(out.values())


def intents_of(task, g, typed_intents=None):
    low = " " + (task or "").lower() + " "
    out, seen = [], set()
    for i in (typed_intents or []):
        seen.add(i)
        out.append({"intent": i, "why": "typed input: intent" + ("" if i in g["intents"] else
                                                                  " (NOT a chart-intents.json word — declared)"),
                    "definition": (g["intents"].get(i, {}).get("definition") or "")[:160],
                    "blocking": False, "unknown": i not in g["intents"]})
    for intent, words in INTENT_LEXICON.items():
        if intent in seen:
            continue
        for w in words:
            if _wb(w, low):
                out.append({"intent": intent, "why": 'INTENT_LEXICON["%s"] <- "%s"' % (intent, w),
                            "definition": (g["intents"].get(intent, {}).get("definition") or "")[:160],
                            "blocking": False})
                break
    return out


# ---------------------------------------------------------------- stage 2: components
def _meta_blob(m):
    rel = m.get("relationships") or {}
    parts = [m.get("name", ""), m.get("$slug", ""), m.get("purpose", ""), m.get("category", ""),
             str(m.get("provides", "")), str(m.get("answers", "")), str(m.get("intent", "")),
             str(m.get("shape", "")), str(m.get("when", ""))]
    parts += [str(x) for x in rel.get("commonPatterns", [])]
    parts += [str(x) for x in rel.get("livesInside", [])]
    for et in ("commonPattern", "usedInContext"):
        for e in (m.get("edges") or {}).get(et, []) or []:
            if isinstance(e, dict) and e.get("ref"):
                parts.append(e["ref"].split(":", 1)[-1].replace("-", " "))
    return " ".join(parts).lower()


ALT_PER_ROLE = 2      # runners-up kept per role (the rest are named in `unresolved`, not dropped silently)
ALT_MIN_SCORE = 5.0   # a runner-up must have EVIDENCE, not just membership of the role


def _norm_shape(s):
    return re.sub(r"\s+", " ", str(s or "").replace("×", "x").replace("*", "x")).strip().lower()


def pick_components(task, terms, roles, intents, g, max_components=14, min_score=3.0,
                    shape=None, forced=None):
    low = " " + (task or "").lower() + " "
    role_slugs, role_rank = {}, {}
    for r in roles:
        for i, p in enumerate(r.get("providers", [])):
            role_slugs.setdefault(p, []).append(r["role"])
            role_rank[p] = min(role_rank.get(p, 99), i)
    for slug, m in g["metas"].items():                      # the authored half
        if m.get("provides"):
            for r in roles:
                if m["provides"] == r["role"]:
                    role_slugs.setdefault(slug, []).append(r["role"])
        for e in ((m.get("edges") or {}).get("providesRole") or []):   # the typed half (108 edges)
            if isinstance(e, dict) and e.get("ref"):
                rr = e["ref"].split(":", 1)[-1]
                if any(rr == r["role"] for r in roles):
                    role_slugs.setdefault(slug, []).append(rr)
    want_shape = _norm_shape(shape) if shape else None
    forced = set(forced or [])
    scored = []
    for slug, m in g["metas"].items():
        blob = _meta_blob(m)
        score, whys = 0.0, []
        name = m.get("name", "").lower()
        if slug in forced:
            score += 20
            whys.append("named by the caller (typed input: components)")
        if _wb(name, low) or _wb(slug.lower().replace("-", " "), low):
            score += 8
            whys.append("named in the task")
        else:
            words = [w for w in re.split(r"[-_ ]", slug.lower()) if len(w) > 2]
            hitw = [w for w in words if _wb(w, low)]
            if len(words) > 1 and len(hitw) >= min(2, len(words)):
                score += 4
                whys.append("slug words in the task: " + "+".join(hitw))
        if slug in role_slugs:
            rl = sorted(set(role_slugs[slug]))
            score += 5 + max(0.0, 1.5 - 0.2 * role_rank.get(slug, 99))
            whys.append("roles.json: provider #%d of %s" % (role_rank.get(slug, 99) + 1, "/".join(rl)))
        if m.get("provides") and any(m["provides"] == r["role"] for r in roles):
            score += 2
            whys.append("meta.provides = " + m["provides"])
        if intents and (m.get("intent") or m.get("answers")):
            mi = m.get("intent") or m.get("answers")
            mi = mi if isinstance(mi, list) else [mi]
            if any(i["intent"] in mi for i in intents):
                score += 4
                whys.append("meta.answers/intent matches chart-intent " + "/".join(mi))
        if want_shape and m.get("shape") and _norm_shape(m["shape"]) == want_shape:
            score += 6
            whys.append("meta.shape == typed shape")
        hit = [t for t in terms if len(t) > 3 and re.search(r"(?<![a-z])" + re.escape(t), blob)]
        if hit:
            score += min(3.0, 0.5 * len(hit))
            whys.append("meta text matches: " + ", ".join(hit[:6]))
        if score >= min_score:
            scored.append((score, slug, whys))
    scored.sort(key=lambda x: (-x[0], x[1]))
    chosen, seen_role, alts, notes = [], {}, {}, []
    want_intents = {i["intent"] for i in intents}
    for score, slug, whys in scored:
        m = g["metas"][slug]
        rl = sorted(set(role_slugs.get(slug, [])))
        named = "named in the task" in " ".join(whys) or slug in forced
        # chart-panel is chosen by the INTENT WORD, not by the role (roles.json, role 3).
        if rl == ["chart-panel"] and not named:
            mi = m.get("intent") or m.get("answers")
            mi = mi if isinstance(mi, list) else [mi]
            if not want_intents:
                if any(nn["what"] == "role:chart-panel" for nn in notes):
                    continue
                notes.append({"what": "role:chart-panel", "ref": None,
                              "$note": "the task asks for a chart but names no analytical intent "
                                       "(knowledge/chart-intents.json). The chart cannot be chosen "
                                       "mechanically — ask, do not guess.",
                              "why": "chart-intents.json is the gate on this role"})
                want_intents = None
                continue
            if want_intents is None or not any(i in (mi or []) for i in want_intents):
                continue
        primary = rl[0] if rl else None
        if primary and primary in seen_role and not named and primary != "chart-panel":
            if alts.get(primary, 0) >= ALT_PER_ROLE or score < ALT_MIN_SCORE:
                continue
            alts[primary] = alts.get(primary, 0) + 1
            chosen.append(_component_row(m, score, whys, rl, g, alternate=seen_role[primary]))
            continue
        if primary:
            seen_role[primary] = slug
        chosen.append(_component_row(m, score, whys, rl, g, alternate=None))
        if len([c for c in chosen if not c["alternate"]]) >= max_components and not forced - {c["id"].split(":", 1)[1] for c in chosen}:
            break
    for slug in sorted(forced):
        if slug not in g["metas"]:
            notes.append({"what": "component:" + slug, "ref": None,
                          "$note": "named by the caller but has no meta in knowledge/components/",
                          "why": "typed input: components"})
    return chosen, notes


def _component_row(m, score, whys, roles, g, alternate=None):
    ed = m.get("edges") or {}

    def refs(et):
        return [e["ref"] for e in (ed.get(et, []) or []) if isinstance(e, dict) and e.get("ref")]
    return {
        "id": "component:" + m["$slug"],
        "name": m.get("name"),
        "category": m.get("category"),
        "provides": m.get("provides"),
        "roles": roles,
        "answers": m.get("answers"),
        "shape": m.get("shape"),
        "when": (m.get("when") or "")[:320] or None,
        "purpose": (m.get("purpose") or "")[:240],
        "meta": m["$path"],
        "snippet": (refs("renderedBy") or [None])[0],
        "consumes": refs("consumes"),
        "hasPart": refs("hasPart") + refs("composedOf"),
        "containedBy": refs("containedBy"),
        "family": refs("family"),
        "not-with": m.get("not-with") or [],
        "with": m.get("with") or [],
        "score": round(score, 2),
        "alternate": alternate,
        "why": "; ".join(whys),
        "blocking": False,
    }


def expand_required(chosen, g):
    """A component's `consumes` / `hasPart` atoms are REQUIRED, so they join the slice with the
    edge that pulled them in as their `why`."""
    have = {c["id"] for c in chosen}
    added = []
    for c in list(chosen):
        if c["alternate"]:
            continue
        for et in ("consumes", "hasPart"):
            for ref in c[et]:
                if ref in have or not ref.startswith("component:"):
                    continue
                slug = ref.split(":", 1)[1]
                m = g["metas"].get(slug)
                if not m:
                    added.append({"id": ref, "name": None, "why": "edges.%s from %s" % (et, c["id"]),
                                  "ref": None, "$note": "edge target has no meta in knowledge/components/",
                                  "blocking": False})
                    continue
                row = _component_row(m, 0.0, ["required by %s (edges.%s)" % (c["id"], et)],
                                     sorted({m.get("provides")}) if m.get("provides") else [], g)
                row["required_by"] = c["id"]
                have.add(ref)
                added.append(row)
    return [a for a in added if "meta" in a], [a for a in added if "meta" not in a]


def _meta_of(c, g):
    return g["metas"].get(c["id"].split(":", 1)[1]) if c.get("id") else None


# ---------------------------------------------------------------- stage 3: governs (rulings, LIVE)
def governs_for(chosen, g):
    """Dave's law over the chosen components — two legs, both named on the row.
    (a) edges.governedBy on the meta; (b) _rulings.json governs[] naming the meta path or its
    renderedBy snippet (the same join the explorer draws)."""
    out = {}
    by_meta, by_snip = {}, {}
    for c in chosen:
        m = _meta_of(c, g)
        if not m:
            continue
        by_meta[m["$path"]] = c["id"]
        if c.get("snippet"):
            by_snip[c["snippet"].split(":", 1)[-1]] = c["id"]
        for e in ((m.get("edges") or {}).get("governedBy") or []):
            if isinstance(e, dict) and e.get("ref"):
                rid = e["ref"].split(":", 1)[-1]
                row = out.setdefault(rid, _ruling_row(rid, g))
                row["via"].append("edges.governedBy on %s" % os.path.basename(m["$path"]))
                row["over"].add(c["id"])
    for rid, r in g["rulings"].items():
        for gv in (r.get("governs") or []):
            if not isinstance(gv, str):
                continue
            gv = gv.strip()
            cid = by_meta.get(gv)
            if not cid:
                sm = SNIP_RX.search(gv)
                cid = by_snip.get(sm.group(1)) if sm else None
            if cid:
                row = out.setdefault(rid, _ruling_row(rid, g))
                row["via"].append("_rulings.json governs[] -> %s" % gv)
                row["over"].add(cid)
    rows = []
    for row in out.values():
        row["via"] = "; ".join(sorted(set(row["via"])))[:400]
        row["over"] = sorted(row["over"])
        rows.append(row)
    rows.sort(key=lambda r: (r.get("date") or "", r["id"]), reverse=True)
    return rows


def _ruling_row(rid, g):
    r = g["rulings"].get(rid)
    return {"id": rid, "ref": "ruling:" + rid if r else None,
            "ruled": (str((r or {}).get("ruled") or "")[:200]) or None,
            "date": (r or {}).get("date"), "by": (r or {}).get("by"),
            "status": (r or {}).get("status"),
            "$note": None if r else "ruling id cited by a meta but absent from knowledge/_rulings.json",
            "via": [], "over": set(), "blocking": True}


# ---------------------------------------------------------------- declared scope (s277-D9): file -> components
# knowledge/guidelines/_scope.json — one hand-authored row per guideline file: kind component|facet|null,
# facets, authored components, exceptions, and the $source sentence of the file it rests on. The join
# is the file's own `$joinRule`; nothing here reads prose (s277-D5, s274-D12). A rule reached this way is
# class "routed-by-scope" — inference by declared scope — never "authored" and never "routed" (vocabulary).
def _meta_token_groups(m, g):
    """The token GROUPS a meta's `tokens` block binds — the same TOKEN_PATH_RX walk tokens_for uses."""
    groups = set()

    def walk(v):
        if isinstance(v, dict):
            for k, x in v.items():
                yield k
                yield from walk(x)
        elif isinstance(v, list):
            for x in v:
                yield from walk(x)
        else:
            yield str(v)
    for v in walk(m.get("tokens")):
        for path in TOKEN_PATH_RX.findall(v.lower()):
            grp = path.split("/")[0]
            if grp in g["token_tiers"]:
                groups.add(grp)
    return groups


def component_facets(g):
    """component slug -> {facet: [binding evidence, ...]} under _scope.json's `facets[*].binds`."""
    if "$component_facets" in g:
        return g["$component_facets"]
    facets = (g["scope"] or {}).get("facets") or {}
    asset_edges = {}
    for store in ("icon_nodes", "logo_nodes"):
        for e in (g[store].get("edges") or []):
            if e.get("t") and str(e.get("s", "")).startswith("component:"):
                asset_edges.setdefault(e["s"][len("component:"):], set()).add(e["type"])
    out = {}
    for slug, m in g["metas"].items():
        groups = _meta_token_groups(m, g)
        edges = {et for et, es in (m.get("edges") or {}).items() if es and not et.startswith("$")} | asset_edges.get(slug, set())
        mine = {}
        for f, spec in facets.items():
            b = spec.get("binds") or {}
            ev = ["tokens %s/*" % grp for grp in b.get("tokenGroups") or [] if grp in groups]
            ev += ["meta.%s" % fld for fld in b.get("metaFields") or [] if m.get(fld)]
            ev += ["edge %s" % et for et in b.get("edges") or [] if et in edges]
            if ev:
                mine[f] = ev
        out[slug] = mine
    g["$component_facets"] = out
    return out


def scope_reach(g):
    """file -> {kind, components: {slug: why}, exceptions: set(rule ids), facets, row}. Cached on g."""
    if "$scope_reach" in g:
        return g["$scope_reach"]
    cf = component_facets(g)
    out = {}
    for row in (g["scope"] or {}).get("rows") or []:
        reach, kind = {}, row.get("kind")
        for c in row.get("components") or []:
            if c in g["metas"]:
                reach[c] = "authored on the %s row of _scope.json" % row["file"]
        if kind == "facet":
            for slug, mine in cf.items():
                hits = [f for f in row.get("facets") or [] if f in mine]
                if hits and slug not in reach:
                    reach[slug] = "facet %s <- %s" % ("/".join(hits), "; ".join(mine[hits[0]][:2]))
        out[row["file"]] = {"kind": kind, "components": reach,
                            "exceptions": {e["rule"] for e in row.get("exceptions") or [] if e.get("rule")},
                            "facets": list(row.get("facets") or []), "row": row}
    g["$scope_reach"] = out
    return out


def rule_reach(g):
    """rule id -> {"obeys": set(slugs), "scope": set(slugs)} — the two paths, kept apart (s277-D9)."""
    obeys = {}
    for slug, m in g["metas"].items():
        for e in ((m.get("edges") or {}).get("obeys") or []):
            ref = e.get("ref") if isinstance(e, dict) else None
            if ref and ref.startswith("rule:"):
                obeys.setdefault(ref[5:], set()).add(slug)
    sr = scope_reach(g)
    out = {}
    for r in g["rules"]:
        rid = r["id"]
        f = sr.get(r.get("file"))
        sc = set(f["components"]) if f and f["kind"] in ("component", "facet") and rid not in f["exceptions"] else set()
        out[rid] = {"obeys": obeys.get(rid, set()), "scope": sc}
    return out


def measure_scope(root=HERE):
    """The s277-D9 figures, re-run: how many rules reach >=1 component by obeys, by scope, by either."""
    g = load_graph(root)
    rr = rule_reach(g)
    rules = g["rules"]
    blocking = [r["id"] for r in rules if r.get("destiny") == "BLOCKING"]

    def fig(ids):
        ob = {i for i in ids if rr[i]["obeys"]}
        sc = {i for i in ids if rr[i]["scope"]}
        return {"total": len(ids), "reach_by_obeys": len(ob), "reach_by_scope": len(sc),
                "reach_by_either": len(ob | sc), "reach_by_none": len(ids) - len(ob | sc),
                "scope_only": len(sc - ob), "obeys_only": len(ob - sc), "both": len(ob & sc)}
    sr = scope_reach(g)
    cf = component_facets(g)
    return {
        "command": "python3 knowledge/_compose_slice.py --measure-scope",
        "before_obeys_only": {"rules_no_component": len(rules) - fig([r["id"] for r in rules])["reach_by_obeys"],
                              "blocking_no_component": len(blocking) - fig(blocking)["reach_by_obeys"]},
        "rules": fig([r["id"] for r in rules]),
        "blocking": fig(blocking),
        "files": {f: {"kind": d["kind"], "components": len(d["components"]), "exceptions": len(d["exceptions"]),
                      "rules": len([r for r in rules if r.get("file") == f])} for f, d in sr.items()},
        "byKind": (g["scope"] or {}).get("byKind"),
        "facets": {f: {"covers": v.get("covers"), "components_binding": sum(1 for m in cf.values() if f in m)}
                   for f, v in ((g["scope"] or {}).get("facets") or {}).items()},
    }


# ---------------------------------------------------------------- stage 4: obeys (authored / derived / routed)
RULE_ID_RX = re.compile(r"\b[a-z]{2,6}\d{0,2}-\d{3}\b")
DESTINY_ORDER = {"BLOCKING": 0, "REVIEW": 1, "ADVISORY": 2, "TASTE": 3}


def obeys_for(chosen, g, task):
    """Three declared classes, BLOCKING first, authored before derived before routed inside a
    destiny. authored = edges.obeys (rule:/ux:) with the meta's own $why; derived = a typed hop
    the meta did not author (rule flaggedBy the component's snippet; a rule id cited in prose
    but not in edges.obeys); routed = a BLOCKING rule whose FILE the vocabulary routes."""
    out = {}
    flagged = {}
    for e in (g["rule_nodes"].get("edges") or []):
        if e.get("type") == "flaggedBy" and e.get("s") and e.get("t"):
            flagged.setdefault(e["s"], []).append(e)
    low = (" " + (task or "").lower() + " ") + " ".join(
        (c.get("purpose") or "") + " " + (c.get("name") or "") + " " + (c.get("category") or "")
        for c in chosen).lower()
    for c in chosen:
        m = _meta_of(c, g)
        if not m:
            continue
        base = os.path.basename(m["$path"])
        authored = set()
        for e in ((m.get("edges") or {}).get("obeys") or []):
            if not (isinstance(e, dict) and e.get("ref")):
                continue
            ref = e["ref"]
            authored.add(ref)
            row = out.setdefault(ref, _obeys_row(ref, g))
            row["class"] = "authored"
            row["why"].append("edges.obeys on %s%s" % (base, (" — " + (e.get("$why") or "")[:160]) if e.get("$why") else ""))
        txt = _read(os.path.join(os.path.dirname(g["$root"]), m["$path"]))
        for rid in sorted(set(RULE_ID_RX.findall(txt))):
            ref = "rule:" + rid
            if rid not in g["rules_by_id"] or ref in authored:
                continue
            row = out.setdefault(ref, _obeys_row(ref, g))
            if row["class"] != "authored":
                row["class"] = "derived"
            row["why"].append("rule id cited in the prose of %s (not in edges.obeys)" % base)
        if c.get("snippet"):
            for e in flagged.get(c["snippet"], []):
                ref = e["t"]
                row = out.setdefault(ref, _obeys_row(ref, g))
                if row["class"] != "authored":
                    row["class"] = "derived"
                row["why"].append("_rule_nodes.json flaggedBy: %s -> %s" % (c["snippet"], ref))
    files = set(SCREEN_ALWAYS)
    route_why = {f: "always-on for a composed screen" for f in SCREEN_ALWAYS}
    for fn, words in RULE_FILE_ROUTES.items():
        for w in words:
            if _wb(w, low):
                files.add(fn)
                route_why.setdefault(fn, 'routed by vocabulary "%s" (RULE_FILE_ROUTES)' % w)
                break
    for r in g["rules"]:
        if r.get("file") in files and r.get("destiny") == "BLOCKING":
            ref = "rule:" + r["id"]
            row = out.setdefault(ref, _obeys_row(ref, g))
            if row["class"] is None:
                row["class"] = "routed"
            row["why"].append(route_why[r["file"]])
    # routed-by-scope (s277-D9): a BLOCKING rule whose FILE's declared scope reaches a chosen component —
    # kind component (authored list) or kind facet (the meta binds a token group / field / edge the facet
    # names). A null-scope file routes nothing; an exception row suppresses its rule. Distinct from
    # "routed" (vocabulary) and never passed off as authored. The non-BLOCKING reach is ASK Q2's.
    sr = scope_reach(g)
    slugs = {c["id"][len("component:"):] for c in chosen if c["id"].startswith("component:")}
    for fn, d in sr.items():
        if d["kind"] not in ("component", "facet"):
            continue
        hit = [sl for sl in slugs if sl in d["components"]]
        if not hit:
            continue
        for r in g["rules"]:
            if r.get("file") != fn or r.get("destiny") != "BLOCKING" or r["id"] in d["exceptions"]:
                continue
            ref = "rule:" + r["id"]
            row = out.setdefault(ref, _obeys_row(ref, g))
            if row["class"] is None:
                row["class"] = "routed-by-scope"
            row["why"].append("routed-by-scope: %s scope kind=%s reaches %s (%s)" % (
                fn, d["kind"], ", ".join(sorted(hit)[:3]), d["components"][sorted(hit)[0]][:90]))
    rows = list(out.values())
    for row in rows:
        row["why"] = "; ".join(sorted(set(row["why"])))[:600]
    corder = {"authored": 0, "derived": 1, "routed": 2, "routed-by-scope": 3}
    rows.sort(key=lambda r: (DESTINY_ORDER.get(r["destiny"], 9), corder.get(r["class"], 9), r["id"]))
    return rows


def _obeys_row(ref, g):
    kind, rid = ref.split(":", 1)
    if kind == "rule":
        r = g["rules_by_id"].get(rid)
        return {"id": ref, "class": None, "destiny": (r or {}).get("destiny"),
                "blocking": (r or {}).get("destiny") == "BLOCKING", "file": (r or {}).get("file"),
                "text": ((r or {}).get("rule") or "")[:280] or None,
                "$note": None if r else "rule id not in knowledge/guidelines/_rules-index.json",
                "ref": ref if r else None, "why": []}
    if kind == "ux":
        n = g["ux_by_id"].get(ref)
        return {"id": ref, "class": None, "destiny": ("grade " + n["grade"]) if n and n.get("grade") else None,
                "blocking": False, "file": "_ux_principle_nodes.json",
                "text": ((n or {}).get("statement") or "")[:400] or None,
                "$note": None if n else "ux id not in knowledge/_ux_principle_nodes.json",
                "ref": ref if n else None, "why": []}
    return {"id": ref, "class": None, "destiny": None, "blocking": False, "file": None, "text": None,
            "$note": "obeys target of unknown kind '%s'" % kind, "ref": None, "why": []}


# ---------------------------------------------------------------- stage 5: must-not (incl. nulls)
def must_not_for(chosen, g):
    """mustNotNeighbour from BOTH homes — edges (typed) and relationships (prose) — plus
    meta not-with. A null ref is SURFACED, never dropped."""
    ids = {c["id"] for c in chosen}
    out = []
    for c in chosen:
        m = _meta_of(c, g)
        if not m:
            continue
        base = os.path.basename(m["$path"])
        for e in ((m.get("edges") or {}).get("mustNotNeighbour") or []):
            if not isinstance(e, dict):
                continue
            ref = e.get("ref")
            out.append({"from": c["id"], "to": ref, "ref": ref,
                        "$note": (e.get("$note") or e.get("note") or "") or None,
                        "in_slice": bool(ref) and ref in ids,
                        "why": "edges.mustNotNeighbour on " + base, "blocking": True})
        for txt in ((m.get("relationships") or {}).get("mustNotNeighbour") or []):
            out.append({"from": c["id"], "to": None, "ref": None, "$note": str(txt), "in_slice": False,
                        "why": "relationships.mustNotNeighbour on " + base, "blocking": True})
        for nw in (c.get("not-with") or []):
            ref = nw if isinstance(nw, str) else (nw.get("ref") if isinstance(nw, dict) else None)
            out.append({"from": c["id"], "to": ref, "ref": ref,
                        "$note": (nw.get("$note") if isinstance(nw, dict) else None),
                        "in_slice": bool(ref) and ref in ids,
                        "why": "meta.not-with on " + base, "blocking": True})
    for r in out:
        if r["ref"] is None and not r["$note"]:
            r["$note"] = "declared null with no note in the meta — surfaced, not dropped"
    out.sort(key=lambda r: (not r["in_slice"], r["from"], str(r["to"])))
    return out


# ---------------------------------------------------------------- stage 6: tokens (group + tier)
TOKEN_PATH_RX = re.compile(r"\b([a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:/[a-z0-9][a-z0-9-]*){1,3})\b")


def tokens_for(chosen, g):
    """TIER grain: the GROUP and its tier, ≤4 example members and an honest count. Type
    composites ride as tier "composite". Never the leaves."""
    groups = {}
    for c in chosen:
        m = _meta_of(c, g)
        if not m:
            continue
        base = os.path.basename(m["$path"])
        tk = m.get("tokens")
        vals = ([str(v) for v in tk.values()] + list(tk.keys())) if isinstance(tk, dict) else \
               ([str(v) for v in tk] if isinstance(tk, list) else [])
        for v in vals:
            for path in TOKEN_PATH_RX.findall(v.lower()):
                grp = path.split("/")[0]
                tier = g["token_tiers"].get(grp)
                if not tier:
                    continue
                row = groups.setdefault(grp, {"group": grp, "tier": tier[0], "source": tier[1],
                                              "members": [], "why": set(), "blocking": False})
                if path not in row["members"]:
                    row["members"].append(path)
                row["why"].add("tokens on " + base)
    # type composites at group grain (tier "composite")
    comp = g["composites"]
    blob = " ".join((c.get("purpose") or "") + " " + (c.get("name") or "") for c in chosen).lower()
    metatext = "".join(_read(os.path.join(os.path.dirname(g["$root"]), (_meta_of(c, g) or {}).get("$path", "")))
                       for c in chosen if _meta_of(c, g)).lower()
    for grp in ("editorial", "component"):
        for k in (comp.get(grp) or {}):
            if k.startswith("$"):
                continue
            hits = []
            if re.search(r"(?<![a-z])" + re.escape(k) + r"(?![a-z-])", blob):
                hits.append("component purpose names it")
            if re.search(r"typography[-/]composites?/" + re.escape(grp) + "/" + re.escape(k), metatext) or \
               (re.search(r'"' + re.escape(k) + r'"\s*:', metatext) and grp == "component"):
                hits.append("named in a selected meta")
            if not hits:
                continue
            gname = "typography-composites/" + grp
            row = groups.setdefault(gname, {"group": gname, "tier": "composite",
                                            "source": "tokens/typography-composites.json",
                                            "members": [], "why": set(), "blocking": False})
            if k not in row["members"]:
                row["members"].append(k)
            row["why"].add("; ".join(hits))
    for grp, row in groups.items():
        row["count"] = len(row["members"])
        row["members"] = sorted(row["members"])[:4]
        row["why"] = "; ".join(sorted(row["why"])[:3])
    order = {"semantic": 0, "component-type": 1, "foundation": 2, "primitive": 3, "composite": 4}
    return sorted(groups.values(), key=lambda r: (order.get(r["tier"], 9), r["group"]))


# ---------------------------------------------------------------- stage 7: assets (icons + logos)
def assets_for(chosen, g):
    """From the RATIFIED node files (s277-D4..D7): every usesIcon / usesLogo edge whose source
    is a chosen component, and every declared-null asset edge on those components. Returns
    (rows, unresolved). Photo has no node kind — the caller declares it."""
    ids = {c["id"] for c in chosen}
    nodes = {}
    for store in (g["icon_nodes"], g["logo_nodes"]):
        for n in (store.get("nodes") or []):
            if n.get("id"):
                nodes[n["id"]] = n
    out, unres, seen = [], [], set()
    for store in (g["icon_nodes"], g["logo_nodes"]):
        for e in (store.get("edges") or []):
            if e.get("s") not in ids or e.get("type") not in ("usesIcon", "usesLogo"):
                continue
            if e.get("t") is None:
                unres.append({"what": "%s from %s" % (e["type"], e["s"]), "ref": None,
                              "$note": e.get("$note") or "declared null in the ratified asset file",
                              "why": "_icon_nodes.json / _logo_nodes.json"})
                continue
            key = (e["s"], e["t"])
            if key in seen:
                continue
            seen.add(key)
            n = nodes.get(e["t"], {})
            out.append({"id": e["t"], "kind": e["t"].split(":")[0], "file": n.get("file"),
                        "group": n.get("group"), "active": n.get("active"),
                        "lockup": n.get("lockup"), "theme": n.get("theme"),
                        "used_by": e["s"], "edge": e["type"],
                        "via": "byte-match (s277-D5)" if e["type"] == "usesIcon" else "src= path (s277-D5)",
                        "blocking": False})
    out.sort(key=lambda r: (r["kind"], r["id"], r["used_by"]))
    if not g["icon_nodes"].get("nodes"):
        unres.append({"what": "assets", "ref": None,
                      "$note": "knowledge/_icon_nodes.json absent or empty — the assets field cannot be read",
                      "why": "s277-D4 node file"})
    return out, unres


# ---------------------------------------------------------------- unresolved + the seed
def unresolved_report(task, roles, chosen, g, extra):
    out = list(extra)
    covered = set()
    for c in chosen:
        covered |= set(c.get("roles") or [])
        if c.get("provides"):
            covered.add(c["provides"])
    for r in roles:
        if r.get("unknown"):
            out.append({"what": "role:" + r["role"], "ref": None,
                        "$note": "typed role is not one of the 12 in knowledge/roles.json",
                        "why": "typed input: roles"})
            continue
        if r["role"] not in covered:
            out.append({"what": "role:" + r["role"], "ref": None,
                        "$note": "the task asks for this role (%s) and no component in the slice "
                                 "provides it" % r["why"], "why": "roles.json"})
    in_slice = {c["id"].split(":", 1)[1] for c in chosen}
    for r in roles:
        spec = g["roles"].get(r["role"], {})
        held = [p.get("slug") for p in spec.get("providers", []) if p.get("slug") not in in_slice]
        if held:
            out.append({"what": "co-providers of role:" + r["role"], "ref": None,
                        "$note": "%d further provider(s) exist and are NOT in the slice (%s). Their "
                                 "`when` predicates decide, and they are not all authored today "
                                 "(s251-D5) — so the choice is a judgement, not a lookup."
                                 % (len(held), ", ".join(held[:8])),
                        "why": "roles.json providers vs slice"})
    for c in chosen:
        if not c.get("roles") and not c.get("provides"):
            out.append({"what": c["id"], "ref": None,
                        "$note": "in the slice by text match; it declares no `provides` and is in no "
                                 "roles.json provider list, so its ROLE is unknown today",
                        "why": "meta has no provides field"})
        if not c.get("when") and c.get("alternate"):
            out.append({"what": c["id"], "ref": None,
                        "$note": "held as an alternate co-provider of %s but carries no `when` "
                                 "predicate, so the choice between them is not mechanical "
                                 "(s251-D5)" % (c["alternate"],),
                        "why": "meta has no when field"})
    out.append({"what": "photo", "ref": None,
                "$note": "no photo/photography node kind exists in the graph — the assets field carries "
                         "icons and logos only (s277-D4); photography is chosen by eye against "
                         "knowledge/assets/, never invented here",
                "why": "assets_for — declared limit"})
    seen, dedup = set(), []
    for u in out:
        k = (str(u.get("what")), (u.get("$note") or "")[:80])
        if k in seen:
            continue
        seen.add(k)
        dedup.append(u)
    return dedup


NULL_NOTES = {
    "components": "no component resolved — the task named no role, intent, shape or component the lexicon knows; grow the lexicon on this miss",
    "governs": "no ruling names any chosen component (edges.governedBy on the metas and _rulings.json governs[] both empty for this set)",
    "obeys": "no rule or principle attaches — no edges.obeys, no cited rule id, no flaggedBy snippet, and the vocabulary routed no BLOCKING file",
    "mustNot": "no chosen component carries mustNotNeighbour (edges or prose) or not-with — nothing is prohibited by the metas, which is a statement, not an absence",
    "tokens": "no chosen meta carries a `tokens` block whose paths resolve to a known tier",
    "assets": "no usesIcon / usesLogo edge in _icon_nodes.json / _logo_nodes.json has a chosen component as its source — the components draw no library glyph and no lockup",
    "unresolved": "nothing was left unresolved",
}


def _finish_fields(s):
    """THE HOUSE RULE: every contract field is content or `null` + a note in $nulls."""
    s.setdefault("$nulls", {})
    for f in CONTRACT_FIELDS:
        if f == "sized":
            continue
        v = s.get(f)
        if not v:
            s[f] = None
            s["$nulls"][f] = NULL_NOTES[f]
        else:
            s["$nulls"].pop(f, None)
    return s


def build_slice(task=None, root=HERE, graph=None, max_components=14, *, intent=None, shape=None,
                roles=None, components=None, budget=None):
    """The SEED — composed once at step 1 (s278-D1). See the module docstring for the contract."""
    if not task and not (intent or shape or roles or components):
        raise SliceRefused("nothing to compose from: give a task sentence or at least one typed "
                           "input (intent / shape / roles / components)")
    g = graph or load_graph(root)
    if isinstance(intent, str):
        intent = [intent]
    if isinstance(roles, str):
        roles = [roles]
    if isinstance(components, str):
        components = [components]
    terms, term_why = terms_of(task or "", g["lexicon"])
    rls = roles_of(task or "", terms, g, typed_roles=roles)
    ints = intents_of(task or "", g, typed_intents=intent)
    chosen, pick_notes = pick_components(task or "", terms, rls, ints, g, max_components=max_components,
                                         shape=shape, forced=components)
    required, dangling = expand_required(chosen, g)
    chosen = chosen + required
    primary = [c for c in chosen if not c.get("alternate")]
    gov = governs_for(primary, g)
    ob = obeys_for(primary, g, task or "")
    mn = must_not_for(primary, g)
    toks = tokens_for(primary, g)
    assets, asset_unres = assets_for(primary, g)
    unres = unresolved_report(task or "", rls, chosen, g,
                              pick_notes + asset_unres + [dict(d, what=d["id"]) for d in dangling])
    if shape and not any("meta.shape == typed shape" in c["why"] for c in chosen):
        unres.append({"what": "shape:" + str(shape), "ref": None,
                      "$note": "no meta's `shape` field equals the typed shape — declared, not approximated",
                      "why": "typed input: shape"})
    s = {
        "$tool": "_compose_slice.py v%s — the reader: step 1 of generate-from-canon (%s)" % (VERSION, "/".join(RULED_BY)),
        "$contract": "SEED (s278-D1): composed once; the session works from it. Fields: %s. Every field is "
                     "content or null + $nulls[field]. ASK (--ask) is the on-demand door and reads live."
                     % ", ".join(CONTRACT_FIELDS),
        "task": task,
        "generated": datetime.date.today().isoformat(),
        "query": {"terms": terms, "roles": rls, "intents": ints, "shape": shape,
                  "components": sorted(components or []), "budget": budget},
        "components": chosen,
        "governs": gov,
        "obeys": ob,
        "mustNot": mn,
        "tokens": toks,
        "assets": assets,
        "unresolved": unres,
    }
    _finish_fields(s)
    s["sized"] = sized(s, g, budget=budget)
    if budget and not s["sized"]["within_budget"]:
        _reduce(s, g, budget)
    return s


def _reduce(s, g, budget):
    """Declared reductions, in order; refuse loudly if they are not enough."""
    steps = []
    if s["components"]:
        alts = [c for c in s["components"] if c.get("alternate")]
        if alts:
            s["components"] = [c for c in s["components"] if not c.get("alternate")]
            s["unresolved"] = (s["unresolved"] or []) + [
                {"what": c["id"], "ref": None, "$note": "alternate dropped to meet the budget (%d); it was a "
                 "co-provider of %s" % (budget, c["alternate"]), "why": "sized.reductions"} for c in alts]
            steps.append("dropped %d alternate component(s)" % len(alts))
            _finish_fields(s)
            s["sized"] = sized(s, g, budget=budget, reductions=steps)
            if s["sized"]["within_budget"]:
                return s
    if s["obeys"]:
        byscope = [r for r in s["obeys"] if r["class"] == "routed-by-scope"]
        if byscope:
            s["obeys"] = [r for r in s["obeys"] if r["class"] != "routed-by-scope"]
            s["unresolved"] = (s["unresolved"] or []) + [
                {"what": "obeys:routed-by-scope", "ref": None,
                 "$note": "%d routed-by-scope BLOCKING rule(s) dropped to meet the budget (%d): %s — they still bind; "
                          "ask for them with --ask" % (len(byscope), budget, ", ".join(r["id"] for r in byscope[:12])),
                 "why": "sized.reductions"}]
            steps.append("dropped %d routed-by-scope obeys row(s)" % len(byscope))
            _finish_fields(s)
            s["sized"] = sized(s, g, budget=budget, reductions=steps)
            if s["sized"]["within_budget"]:
                return s
        routed = [r for r in s["obeys"] if r["class"] == "routed"]
        if routed:
            s["obeys"] = [r for r in s["obeys"] if r["class"] != "routed"]
            s["unresolved"] = (s["unresolved"] or []) + [
                {"what": "obeys:routed", "ref": None,
                 "$note": "%d routed BLOCKING rule(s) dropped to meet the budget (%d): %s — they still bind; "
                          "ask for them with --ask" % (len(routed), budget, ", ".join(r["id"] for r in routed[:12])),
                 "why": "sized.reductions"}]
            steps.append("dropped %d routed obeys row(s)" % len(routed))
            _finish_fields(s)
            s["sized"] = sized(s, g, budget=budget, reductions=steps)
            if s["sized"]["within_budget"]:
                return s
    raise SliceRefused("seed is %d cl100k tokens against a budget of %d after %s — refused, not truncated; "
                       "raise the budget or narrow the task"
                       % (s["sized"]["slice_tokens"], budget, "; ".join(steps) or "no reduction available"))


# ---------------------------------------------------------------- the headline number
def _tok(text):
    try:
        import tiktoken
        return len(tiktoken.get_encoding("cl100k_base").encode(text))
    except Exception:
        return max(1, len(text) // 4)          # declared fallback, never presented as measured


def _unit():
    try:
        import tiktoken  # noqa: F401
        return "cl100k (tiktoken) — a LABELLED ESTIMATOR, never a unit a cap is stated in (ds-021)"
    except Exception:
        return "chars/4 FALLBACK — tiktoken absent; NOT a measurement (ds-021)"


def _body(s):
    return json.dumps({k: v for k, v in s.items() if k != "sized"}, ensure_ascii=False)


def sized(s, g, budget=None, reductions=None):
    body = _body(s)
    n = _tok(body)
    metas = [c["meta"] for c in (s["components"] or []) if c.get("meta")]
    read_today = sum(_tok(_read(os.path.join(os.path.dirname(g["$root"]), p))) for p in metas)
    whole = sum(_tok(_read(os.path.join(os.path.dirname(g["$root"]), m["$path"]))) for m in g["metas"].values())
    per = {f: _tok(json.dumps(s.get(f), ensure_ascii=False)) for f in CONTRACT_FIELDS if f != "sized"}
    return {
        "unit": _unit(),
        "slice_tokens": n,
        "per_field": per,
        "budget": budget,
        "within_budget": (n <= budget) if budget else True,
        "reductions": reductions or [],
        "metas_in_slice": len(metas),
        "metas_in_slice_tokens": read_today,
        "ratio_vs_selected_metas": round(read_today / n, 2) if n else None,
        "library_metas": len(g["metas"]),
        "library_metas_tokens": whole,
        "ratio_vs_whole_library": round(whole / n, 2) if n else None,
    }


def measure_claim(root=HERE, task=None):
    """The s277-D10 claim re-measured on the live tree: the seed vs the metas it replaces vs what
    step 1 read before the wiring (every meta + canon.css + type.css). Prints the commands."""
    task = task or TASK_A
    g = load_graph(root)
    s = build_slice(task, graph=g)
    canon = _tok(_read(os.path.join(root, "canon", "canon.css")))
    tcss = _tok(_read(os.path.join(root, "canon", "type.css")))
    m = s["sized"]
    return {
        "task": task,
        "unit": m["unit"],
        "seed_tokens": m["slice_tokens"],
        "per_field": m["per_field"],
        "metas_in_seed": m["metas_in_slice"],
        "metas_in_seed_tokens": m["metas_in_slice_tokens"],
        "ratio_vs_selected_metas": m["ratio_vs_selected_metas"],
        "library_metas": m["library_metas"],
        "library_metas_tokens": m["library_metas_tokens"],
        "canon_css_tokens": canon,
        "type_css_tokens": tcss,
        "step1_before_wiring_tokens": m["library_metas_tokens"] + canon + tcss,
        "ratio_vs_step1_before_wiring": round((m["library_metas_tokens"] + canon + tcss) / m["slice_tokens"], 2),
        "command": 'python3 knowledge/_compose_slice.py --measure',
    }


# ---------------------------------------------------------------- ASK — the on-demand door
QUESTIONS = [
    # (q, verb, node kinds it takes, edge types it walks, the canonical wording)
    ("Q1", "governs", ("component",), ("governs", "governedBy"), "what governs this component?"),
    ("Q2", "binds", ("rule", "ux"), ("obeys",), "which components does this rule bind?"),
    ("Q3", "principle", ("rule",), (), "what principle underlies this rule, and its grade?"),
    ("Q4", "conflicts", ("component",), ("obeys", "tensionWith"), "which rules conflict for this component?"),
    ("Q5", "ruled", ("component", "any"), ("governs", "governedBy"), "what did Dave rule about this, and when?"),
    ("Q6", "evidence", ("ruling",), ("evidencedBy",), "what evidence supports that ruling?"),
    ("Q7", "answers", ("intent", "shape"), ("answersIntent", "hasDataShape"), "which components answer this intent / shape?"),
    ("Q8", "avoid", ("component",), ("mustNotNeighbour",), "what must this component not sit next to?"),
    ("Q9", "tokens", ("component",), (), "what tokens does it consume; what breaks if I change one?"),
    ("Q10", "usedIn", ("component",), ("commonPattern", "usedInContext"), "which pattern / context is it used in?"),
    ("Q11", "wcag", ("component",), ("appliesTo", "cites"), "what is the WCAG / accessible-name obligation?"),
    ("Q12", "assets", ("component",), ("usesIcon", "usesLogo"), "what icon / logo / photo may I use here?"),
]
VERB_RX = [
    ("evidence", r"\bevidence\b|\bsupports? (that|this|the) ruling\b"),
    ("conflicts", r"\bconflict"),
    ("binds", r"\bbind|\bwhich components (does|do) (this |the )?(rule|principle)|\bobey(s|ed)? (this|the) rule\b"),
    ("principle", r"\bprinciple\b|\bgrade\b|\bunderlies\b"),
    ("ruled", r"\bwhat did dave rule\b|\bruled?\b.*\bwhen\b|\bwhen (did|was)\b.*\brul"),
    ("governs", r"\bgovern"),
    ("answers", r"\banswer|\bwhich components? (answer|for|give)|\bintent\b|\bshape\b"),
    ("avoid", r"\bnot sit next to\b|\bnot neighbou?r|\bmust ?not\b|\bavoid\b|\bnext to\b"),
    ("tokens", r"\btokens?\b|\bbreaks? if i change\b|\bblast"),
    ("usedIn", r"\bpattern\b|\bcontext\b|\bused in\b|\bwhere is (it|this) used\b"),
    ("wcag", r"\bwcag\b|\baccessible[- ]name\b|\bsuccess criteri|\bobligation|\ba11y\b|\baccessibilit"),
    ("assets", r"\bicon|\blogo|\bphoto|\bglyph|\basset"),
]
NODE_RX = re.compile(r"\b(component|rule|ux|ruling|sc|intent|shape|snippet|pattern|context|icon|logo):([A-Za-z0-9][A-Za-z0-9._/\-]*)")
RULING_ID_RX = re.compile(r"\b(s\d{2,3}-D\d+(?:-am)?|ds-\d{3}|ADR-\d{4}(?:-A\d)?|DV-D\d+|T-D\d+|B-D\d+|GM-D\d+)\b")
SC_RX = re.compile(r"\b(\d\.\d{1,2}\.\d{1,2})\b")


def _map_question(q, live):
    """question text -> (verb, node id). Raises AskRefused naming the FIRST obstacle."""
    low = " " + q.lower().strip() + " "
    verb = None
    for v, rx in VERB_RX:
        if re.search(rx, low):
            verb = v
            break
    if not verb:
        raise AskRefused("unmappable question — no verb: none of the 12 canonical questions' words "
                         "(%s) appear in %r" % ("/".join(v for v, _ in VERB_RX), q))
    node = None
    m = NODE_RX.search(q)
    if m:
        node = "%s:%s" % (m.group(1), m.group(2).rstrip("?.,"))
    if not node:
        m = RULING_ID_RX.search(q)
        if m:
            node = "ruling:" + m.group(1)
    if not node:
        m = re.search(r"\b([a-z]{2,6}\d{0,2}-\d{3})\b", low)
        if m and ("rule:" + m.group(1)) in live["nodes"]:
            node = "rule:" + m.group(1)
    if not node and verb == "wcag":
        m = SC_RX.search(q)
        if m and ("sc:" + m.group(1)) in live["nodes"]:
            node = "sc:" + m.group(1)
    if not node and verb == "answers":
        g = live["g"]
        for i in sorted(g["intents"], key=len, reverse=True):
            if _wb(i, low):
                node = "intent:" + i
                break
        if not node:
            for slug, mm in g["metas"].items():
                if mm.get("shape") and _norm_shape(mm["shape"]) in _norm_shape(low):
                    node = "shape:" + _norm_shape(mm["shape"])
                    break
    if not node:
        # a component named in plain words — longest name/slug match wins
        g = live["g"]
        best = None
        for slug, mm in g["metas"].items():
            for cand in (mm.get("name", "").lower(), slug.lower().replace("-", " "), slug.lower()):
                if len(cand) >= 3 and _wb(cand, low) and (best is None or len(cand) > len(best[0])):
                    best = (cand, "component:" + slug)
        if best:
            node = best[1]
    if not node:
        raise AskRefused("unmappable question — verb %r found but no node: name one as kind:id "
                         "(component:button, rule:ctkb-003, ruling:s277-D10, sc:1.4.3, intent:comparison) "
                         "or by its meta name" % verb)
    if node not in live["nodes"] and not node.startswith("shape:"):
        raise AskRefused("node %s is not in the live graph (%d nodes read at %s)"
                         % (node, len(live["nodes"]), live["read"]["at"]))
    qrow = next(r for r in QUESTIONS if r[1] == verb)
    kinds = qrow[2]
    if "any" not in kinds and node.split(":")[0] not in kinds:
        raise AskRefused("%s (%s) takes a %s node, not %s" % (qrow[0], verb, "/".join(kinds), node))
    return qrow, node


def _e(e, live, side="t"):
    other = e[side]
    n = live["nodes"].get(other or "", {})
    row = {"type": e["type"], side: other,
           "label": (n.get("label") or n.get("says") or n.get("text") or "")[:90] or None}
    if e.get("note") and e["note"][:140] != row["label"]:
        row["note"] = e["note"][:140]
    if e.get("via"):
        row["via"] = e["via"][:60]
    if other is None:
        row["ref"] = None
        row["$note"] = e.get("note") or "declared null"
    return row


def ask(question, seed=None, budget=ASK_BUDGET, root=HERE, live=None):
    """The on-demand door. Reads LIVE; never mutates `seed`; refuses over budget."""
    live = live or load_live(root)
    qrow, node = _map_question(question, live)
    q, verb = qrow[0], qrow[1]
    out_e = live["out"].get(node, [])
    in_e = live["in"].get(node, [])
    nd = live["nodes"].get(node, {"id": node})
    ans, declared = {}, []
    g = live["g"]
    if verb == "governs":
        rows = [_e(e, live, "s") for e in in_e if e["type"] == "governs"]
        for r in rows:
            rn = live["nodes"].get(r["s"], {})
            r.pop("label", None)
            r.update({"date": rn.get("date"), "ruled": (rn.get("ruled") or "")[:120] or None})
        rows += [_e(e, live) for e in out_e if e["type"] == "governedBy"]
        ans["rulings"] = sorted(rows, key=lambda r: (r.get("date") or "", str(r.get("s") or r.get("t"))), reverse=True)
        if not rows:
            declared.append("no ruling names %s — governs[] in _rulings.json and edges.governedBy both empty" % node)
    elif verb == "binds":
        rows = [_e(e, live, "s") for e in in_e if e["type"] == "obeys"]
        ans["components"] = sorted(rows, key=lambda r: r["s"])
        if not rows:
            declared.append("no meta carries edges.obeys -> %s" % node)
        if node.startswith("rule:"):   # the declared-scope path (s277-D9), kept apart from obeys
            rn = g["rules_by_id"].get(node[5:]) or {}
            d = scope_reach(g).get(rn.get("file"))
            if d and d["kind"] in ("component", "facet") and node[5:] not in d["exceptions"] and d["components"]:
                ans["routedByScope"] = {"file": rn.get("file"), "kind": d["kind"], "facets": d["facets"],
                                        "count": len(d["components"]), "components": sorted(d["components"])}
            elif d and node[5:] in d["exceptions"]:
                declared.append("%s is an exception row on %s's scope — routed-by-scope does not fire" % (node, rn.get("file")))
            elif d and d["kind"] is None:
                declared.append("%s has a DECLARED NULL scope (%s) — routed-by-scope does not fire" % (rn.get("file"), (d["row"].get("$note") or "")[:120]))
            elif d:
                declared.append("%s's scope reaches no component today (%s)" % (rn.get("file"), "/".join(d["facets"])))
    elif verb == "principle":
        ans["rule"] = {"id": node, "destiny": nd.get("destinyFull") or nd.get("destiny"),
                       "file": nd.get("file"), "text": (nd.get("text") or "")[:240]}
        ans["cites"] = [_e(e, live) for e in out_e if e["type"] == "cites"]
        declared.append("rule -> ux principle: NO SUCH EDGE TYPE in the graph (A1 verdict UNANSWERABLE, "
                        "s274-D12 keeps rule->component out too); the grade above is the rule's own destiny, "
                        "not a principle's grade")
    elif verb == "conflicts":
        obeyed = [e["t"] for e in out_e if e["type"] == "obeys" and e["t"]]
        ux = [t for t in obeyed if t.startswith("ux:")]
        pairs = []
        for e in live["edges"]:
            if e["type"] == "tensionWith" and e["s"] in ux and e["t"] in ux:
                pairs.append({"a": e["s"], "b": e["t"], "polarity": e.get("polarity"), "note": e["note"][:200]})
        ans["obeys"] = obeyed
        ans["tensions"] = pairs
        if not pairs:
            declared.append("no tensionWith edge joins two principles %s obeys (%d obeyed, %d ux:)"
                            % (node, len(obeyed), len(ux)))
        declared.append("no rule->rule conflict edge type exists — conflict between guideline RULES is stated nowhere in the graph")
    elif verb == "ruled":
        rows = []
        for e in in_e:
            if e["type"] == "governs":
                rn = live["nodes"].get(e["s"], {})
                rows.append({"ruling": e["s"], "date": rn.get("date"), "by": rn.get("by"),
                             "ruled": (rn.get("ruled") or "")[:160] or None, "via": e.get("via")})
        for e in out_e:
            if e["type"] == "governedBy":
                rn = live["nodes"].get(e["t"], {})
                rows.append({"ruling": e["t"], "date": rn.get("date"), "by": rn.get("by"),
                             "ruled": (rn.get("ruled") or "")[:160] or None, "via": "edges.governedBy"})
        seen, dedup = set(), []
        for r in sorted(rows, key=lambda r: (r.get("date") or "", r["ruling"]), reverse=True):
            if r["ruling"] in seen:
                continue
            seen.add(r["ruling"])
            dedup.append(r)
        ans["rulings"] = dedup
        if not dedup:
            declared.append("nothing ruled names %s" % node)
    elif verb == "evidence":
        ans["ruling"] = {"id": node, "date": nd.get("date"), "by": nd.get("by"), "status": nd.get("status"),
                         "ruled": (nd.get("ruled") or "")[:200] or None}
        ans["evidence"] = [e["note"][:240] or e["t"] for e in out_e if e["type"] == "evidencedBy"]
        ans["ruling_edges"] = [_e(e, live) for e in out_e if e["type"] not in ("evidencedBy", "governs")] + \
                              [_e(e, live, "s") for e in in_e if e["s"].startswith("ruling:")]
        if not ans["evidence"]:
            declared.append("%s carries no evidence[]" % node)
    elif verb == "answers":
        et = "answersIntent" if node.startswith("intent:") else "hasDataShape"
        rows = [_e(e, live, "s") for e in in_e if e["type"] == et]
        # the meta fields, for the intents/shapes the edge layer has not reached
        val = node.split(":", 1)[1]
        for slug, m in g["metas"].items():
            cid = "component:" + slug
            if any(r["s"] == cid for r in rows):
                continue
            fld = m.get("answers") if node.startswith("intent:") else m.get("shape")
            fl = fld if isinstance(fld, list) else [fld]
            if any(_norm_shape(x) == _norm_shape(val) for x in fl if x):
                rows.append({"type": "meta." + ("answers" if node.startswith("intent:") else "shape"),
                             "s": cid, "label": m.get("name"), "note": "field on the meta, no typed edge"})
        ans["components"] = sorted(rows, key=lambda r: r["s"])
        if not rows:
            declared.append("no component answers %s by edge or by field" % node)
    elif verb == "avoid":
        rows = [_e(e, live) for e in out_e if e["type"] == "mustNotNeighbour"]
        m = g["metas"].get(node.split(":", 1)[1], {})
        for txt in ((m.get("relationships") or {}).get("mustNotNeighbour") or []):
            rows.append({"type": "relationships.mustNotNeighbour", "t": None, "ref": None, "$note": str(txt)[:200]})
        ans["mustNot"] = rows
        ans["nulls"] = sum(1 for r in rows if r.get("t") is None)
        if not rows:
            declared.append("%s carries no mustNotNeighbour (edges or prose) — nothing is prohibited by its meta" % node)
    elif verb == "tokens":
        row = {"id": node, "name": nd.get("label"), "meta": nd.get("meta")}
        toks = tokens_for([row], g)
        ans["groups"] = [{k: t[k] for k in ("group", "tier", "count", "members")} for t in toks]
        br = _load(os.path.join(root, "tokens", "_blast-radius.json"))
        rank = {r["token"]: r for r in (br.get("ranking") or []) if isinstance(r, dict)}
        blast = []
        for t in toks:
            for mbr in t["members"]:
                r = rank.get(mbr)
                if r:
                    blast.append({"token": mbr, "components": r.get("blast"), "sample": (r.get("components") or [])[:3]})
        blast.sort(key=lambda b: -(b["components"] or 0))
        ans["blast_radius"] = blast[:8]
        if len(blast) > 8:
            declared.append("blast radius shown for the 8 widest of %d indexed members; the rest are in tokens/_blast-radius.json" % len(blast))
        declared.append("no token: node kind exists — groups come from the meta's tokens block at tier grain; "
                        "blast radius is tokens/_blast-radius.json (a DERIVED index, generated %s)" % br.get("generated"))
        if not toks:
            declared.append("%s carries no tokens block that resolves to a tier" % node)
    elif verb == "usedIn":
        rows = [_e(e, live) for e in out_e if e["type"] in ("commonPattern", "usedInContext")]
        ans["patterns"] = [r for r in rows if r["type"] == "commonPattern"]
        ans["contexts"] = [r for r in rows if r["type"] == "usedInContext"]
        if not rows:
            declared.append("%s carries no commonPattern / usedInContext edge" % node)
    elif verb == "wcag":
        if node.startswith("sc:"):
            ans["sc"] = {k: nd.get(k) for k in ("id", "label", "level", "severity", "check")}
            ans["appliesTo"] = [_e(e, live) for e in out_e if e["type"] == "appliesTo"]
        else:
            direct = [_e(e, live, "s") for e in in_e if e["type"] == "appliesTo"]
            for r in direct:
                sn = live["nodes"].get(r["s"], {})
                r.update({"level": sn.get("level"), "severity": sn.get("severity"), "check": (sn.get("check") or "")[:120]})
            cited = []
            for e in out_e:
                if e["type"] == "obeys" and e["t"] and e["t"].startswith("rule:"):
                    for e2 in live["out"].get(e["t"], []):
                        if e2["type"] == "cites" and e2["t"]:
                            cited.append({"sc": e2["t"], "via": e["t"], "label": live["nodes"].get(e2["t"], {}).get("label")})
            ans["appliesTo"] = direct
            ans["citedByObeyedRules"] = cited
            if not direct and not cited:
                declared.append("no sc: node applies to %s by compliance applies_to, and no rule it obeys cites one" % node)
            declared.append("accessible-name obligation is carried by the sc: check text, not by a typed edge of its own")
    elif verb == "assets":
        rows = [_e(e, live) for e in out_e if e["type"] in ("usesIcon", "usesLogo")]
        for r in rows:
            an = live["nodes"].get(r.get("t") or "", {})
            r.update({"file": an.get("file"), "group": an.get("group"), "active": an.get("active")})
        ans["icons"] = [r for r in rows if r["type"] == "usesIcon"]
        ans["logos"] = [r for r in rows if r["type"] == "usesLogo"]
        ans["nulls"] = [r for r in rows if r.get("t") is None]
        if not rows:
            declared.append("%s draws no library icon and no lockup by the geometry byte-match (s277-D5)" % node)
        declared.append("photo: no node kind — chosen by eye against knowledge/assets/, never here")
    result = {
        "q": q, "verb": verb, "question": question, "node": node,
        "in_seed": _in_seed(seed, node),
        "answer": ans, "declared": declared,
        "live": live["read"],
    }
    n = _tok(json.dumps(result, ensure_ascii=False))
    result["sized"] = {"tokens": n, "budget": budget, "unit": _unit()}
    if n > budget:
        raise AskRefused("answer to %s for %s is %d cl100k tokens, over the budget of %d — refused, not "
                         "truncated; raise --budget or ask a narrower question" % (q, node, n, budget))
    return result


def _in_seed(seed, node):
    if not isinstance(seed, dict):
        return None
    ids = {c["id"] for c in (seed.get("components") or [])}
    ids |= {"ruling:" + r["id"] for r in (seed.get("governs") or [])}
    ids |= {r["id"] for r in (seed.get("obeys") or [])}
    ids |= {a["id"] for a in (seed.get("assets") or [])}
    return node in ids


# ---------------------------------------------------------------- renderers
def explain(s):
    L = []
    m = s["sized"]
    L.append("TASK  " + str(s["task"]))
    L.append("ROLES " + (", ".join(r["role"] for r in s["query"]["roles"]) or "(none)"))
    if s["query"]["intents"]:
        L.append("INTENT " + ", ".join(i["intent"] for i in s["query"]["intents"]))
    L.append("")
    comps = s["components"] or []
    L.append("COMPONENTS (%d, %d alternates)" % (len([c for c in comps if not c.get("alternate")]),
                                                 len([c for c in comps if c.get("alternate")])))
    for c in comps:
        L.append("  %-34s %-16s %s%s" % (c["id"], "/".join(c.get("roles") or []) or "-",
                                         c["why"][:70], "  [ALT]" if c.get("alternate") else ""))
    L.append("")
    L.append("GOVERNS %d ruling(s)" % len(s["governs"] or []))
    for r in (s["governs"] or [])[:10]:
        L.append("  %-12s %-10s %s" % (r["id"], r.get("date") or "-", (r.get("ruled") or r.get("says") or "")[:70]))
    ob = s["obeys"] or []
    L.append("")
    L.append("OBEYS %d (%d BLOCKING, first; %d authored / %d derived / %d routed / %d routed-by-scope)" % (
        len(ob), len([r for r in ob if r["blocking"]]), len([r for r in ob if r["class"] == "authored"]),
        len([r for r in ob if r["class"] == "derived"]), len([r for r in ob if r["class"] == "routed"]),
        len([r for r in ob if r["class"] == "routed-by-scope"])))
    for r in ob[:12]:
        L.append("  %-16s %-9s %-8s %s" % (r["id"], r["destiny"] or "-", r["class"], (r["text"] or "")[:60]))
    L.append("")
    mn = s["mustNot"] or []
    L.append("MUST-NOT %d (%d ref:null)" % (len(mn), len([a for a in mn if a["ref"] is None])))
    for a in mn[:8]:
        L.append("  %s  x  %s   %s" % (a["from"], a["to"] or "(ref:null)", (a["$note"] or "")[:60]))
    L.append("")
    L.append("TOKENS (group+tier) " + ", ".join("%s[%s:%d]" % (t["group"], t["tier"], t["count"]) for t in (s["tokens"] or [])))
    L.append("ASSETS %d   (%s)" % (len(s["assets"] or []), ", ".join(sorted({a["id"] for a in (s["assets"] or [])})[:8])))
    L.append("")
    L.append("UNRESOLVED %d" % len(s["unresolved"] or []))
    for u in (s["unresolved"] or [])[:8]:
        L.append("  %-28s %s" % (u["what"], (u["$note"] or "")[:80]))
    if s.get("$nulls"):
        L.append("NULL FIELDS " + "; ".join("%s: %s" % (k, v[:60]) for k, v in s["$nulls"].items()))
    L.append("")
    L.append("SIZED  seed %d tok  vs  %d tok of the %d metas it replaces  = %sx  (whole library %d tok = %sx)%s" %
             (m["slice_tokens"], m["metas_in_slice_tokens"], m["metas_in_slice"], m["ratio_vs_selected_metas"],
              m["library_metas_tokens"], m["ratio_vs_whole_library"],
              ("  budget %d %s" % (m["budget"], "OK" if m["within_budget"] else "OVER")) if m["budget"] else ""))
    L.append("UNIT " + m["unit"])
    return "\n".join(L)


CSS = """*{box-sizing:border-box}html{color-scheme:light dark}
body{margin:0;background:var(--bg);color:var(--fg);font-family:"Univers Next","Univers","Helvetica Neue",Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6}
:root{--accent:#DA1A00;--bg:#fff;--fg:#000;--panel:#F3F3F3;--rule:#EDEDED;--rule-2:#D7D8D6;--muted:#767676}
@media (prefers-color-scheme:dark){:root{--accent:#F6604C;--bg:#0E0E0E;--fg:#fff;--panel:#1A1A1A;--rule:#2A2A2A;--rule-2:#3A3A3A;--muted:#A8A8A8}}
.wrap{max-width:1180px;margin:0 auto;padding:0 2rem}
h1{font-size:44px;font-weight:300;line-height:1.05;margin:3rem 0 1rem}
h2{font-size:13px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:3rem 0 1rem;display:flex;gap:.5rem;align-items:center}
h2::before{content:'';width:20px;height:1px;background:var(--accent)}
table{width:100%;border-collapse:collapse;font-size:13px;line-height:1.5;margin-bottom:1rem}
th{text-align:left;font-size:11px;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);border-bottom:1px solid var(--rule-2);padding:0 .8rem .5rem 0;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:.5rem .8rem .5rem 0;vertical-align:top}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12px}
.b{color:var(--accent);font-weight:500}
.muted{color:var(--muted)}
.k{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.big{font-size:56px;font-weight:200;line-height:1}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:2rem;margin:1rem 0 2rem}
.note{background:var(--panel);border-left:2px solid var(--accent);padding:.75rem 1rem;font-size:13px;margin:1rem 0}
@media(max-width:700px){.wrap{padding:0 1rem}table{font-size:12px}}"""


def to_html(s):
    e = html.escape
    m = s["sized"]
    P = ["<title>Seed — %s</title>" % e(str(s["task"])[:60]), "<style>%s</style>" % CSS,
         '<div class="wrap">', "<h1>%s</h1>" % e(str(s["task"])),
         '<p class="muted mono">%s · generated %s</p>' % (e(s["$tool"]), s["generated"])]
    P.append('<div class="grid">')
    for k, v in (("seed", m["slice_tokens"]), ("metas it replaces", m["metas_in_slice_tokens"]),
                 ("ratio", str(m["ratio_vs_selected_metas"]) + "x"),
                 ("vs whole library", str(m["ratio_vs_whole_library"]) + "x")):
        P.append('<div><div class="k">%s</div><div class="big">%s</div></div>' % (e(k), e(str(v))))
    P.append("</div>")
    P.append('<div class="note">Unit: %s</div>' % e(m["unit"]))

    def table(title, cols, rows, cell):
        P.append("<h2>%s</h2>" % e(title))
        if not rows:
            P.append('<p class="muted">null — %s</p>' % e(s.get("$nulls", {}).get(title.split(" ")[0].lower(), "empty")))
            return
        P.append("<table><tr>" + "".join("<th>%s</th>" % e(c) for c in cols) + "</tr>")
        for r in rows:
            P.append("<tr>" + "".join("<td class='%s'>%s</td>" % (cls, e(str(v))) for cls, v in cell(r)) + "</tr>")
        P.append("</table>")

    table("components", ["component", "role", "when", "why"], s["components"] or [],
          lambda c: [("mono", c["id"] + (" ALT" if c.get("alternate") else "")), ("", "/".join(c.get("roles") or []) or "—"),
                     ("muted", (c.get("when") or "—")[:150]), ("muted", c.get("why", "")[:160])])
    table("governs — rulings, newest first", ["id", "date", "ruled", "via"], s["governs"] or [],
          lambda r: [("mono b", r["id"]), ("", r.get("date") or "—"), ("", (r.get("ruled") or r.get("says") or "")[:220]), ("muted", r["via"][:120])])
    table("obeys — blocking first", ["id", "class", "destiny", "text", "why"], s["obeys"] or [],
          lambda r: [("mono " + ("b" if r["blocking"] else ""), r["id"]), ("", r["class"]), ("", r["destiny"] or ""),
                     ("", (r["text"] or "")[:200]), ("muted", r["why"][:110])])
    table("mustNot — incl. nulls", ["from", "must not neighbour", "note"], s["mustNot"] or [],
          lambda a: [("mono", a["from"]), ("mono b", a["to"] or "ref:null"), ("muted", (a["$note"] or "")[:200])])
    table("tokens — group + tier", ["group", "tier", "members", "count"], s["tokens"] or [],
          lambda t: [("mono", t["group"] + "/*"), ("", t["tier"]), ("mono muted", ", ".join(t["members"])), ("", t["count"])])
    table("assets", ["asset", "file", "used by", "edge"], s["assets"] or [],
          lambda a: [("mono", a["id"]), ("mono muted", a.get("file") or ""), ("mono", a["used_by"]), ("", a["edge"])])
    table("unresolved", ["what", "ref", "note"], s["unresolved"] or [],
          lambda u: [("mono", str(u["what"])), ("mono", "null"), ("muted", (u.get("$note") or "")[:240])])
    P.append("</div>")
    return "\n".join(P)


# ---------------------------------------------------------------- selftest
TASK_A = "a payments dashboard screen with a stat card row, a filter bar and a data table"
TASK_B = "build me a financial dashboard for corporate international banking. Please make the all the interactive elements work such as filtering and navigation."
TASK_C = "a liquidity overview comparing balances by currency over time with a chart panel and a stat card row"

ASK_12 = [
    "what governs component:button?",
    "which components does rule:ctkb-003 bind?",
    "what principle underlies rule:ctkb-002, and its grade?",
    "which rules conflict for component:button?",
    "what did Dave rule about component:table, and when?",
    "what evidence supports ruling:s277-D10?",
    "which components answer intent:comparison?",
    "what must component:toast not sit next to?",
    "what tokens does component:button consume; what breaks if I change one?",
    "which pattern / context is component:button used in?",
    "what is the WCAG / accessible-name obligation for component:button?",
    "what icon / logo / photo may I use in component:app-shell-doormat?",
]


def selftest():
    import tempfile, shutil
    fails, n = [], 0
    g = load_graph()

    def bite(name, cond, detail=""):
        nonlocal n
        n += 1
        if cond:
            print("  ok   %d. %s" % (n, name))
        else:
            print("  FAIL %d. %s  %s" % (n, name, detail))
            fails.append(name)

    s = build_slice(TASK_A, graph=g)
    ids = [c["id"] for c in s["components"]]
    prim = [c for c in s["components"] if not c.get("alternate")]
    # — the contract
    bite("CONTRACT: every out field is present on the seed",
         all(f in s for f in CONTRACT_FIELDS), [f for f in CONTRACT_FIELDS if f not in s])
    bite("CONTRACT: a null field carries a note in $nulls (mutation: empty a field, re-finish)",
         (lambda t: t["assets"] is None and bool(t["$nulls"].get("assets")))(_finish_fields(dict(s, assets=[]))))
    empty = build_slice(components=["no-such-component-zz"], graph=g)
    bite("CONTRACT: an empty resolution yields null fields + notes, never absent fields",
         all(f in empty for f in CONTRACT_FIELDS) and empty["components"] is None and
         bool(empty["$nulls"].get("components")) and any(u["what"] == "component:no-such-component-zz" for u in empty["unresolved"]),
         empty.get("$nulls"))
    bite("CONTRACT: typed inputs — roles + intent + components compose without a task sentence",
         (lambda t: any(c["id"] == "component:button" for c in t["components"]) and
          any(r["role"] == "record-list" for r in t["query"]["roles"]))(
             build_slice(roles=["record-list"], intent="comparison", components=["button"], graph=g)))
    bite("CONTRACT: typed shape matches a meta.shape and is declared when it does not",
         any("meta.shape == typed shape" in c["why"] for c in build_slice(shape="parts-of-whole", graph=g)["components"]) and
         any(str(u["what"]).startswith("shape:") for u in build_slice(shape="no-such × shape", roles=["action"], graph=g)["unresolved"]))
    bite("CONTRACT: unknown typed input refused loudly (no task, no typed input)",
         (lambda: (_ for _ in ()).throw(SliceRefused) if False else True)() and _raises(SliceRefused, build_slice, None, graph=g))
    # — the old proposal's bites, carried
    bite("the worked task resolves the table", "component:table" in ids, ids[:6])
    bite("the worked task resolves a headline-metric provider",
         any("headline-metric" in (c.get("roles") or []) for c in s["components"]))
    bite("every slice row carries why + blocking",
         all(("why" in c and "blocking" in c) for c in s["components"]) and
         all(("why" in r and "blocking" in r) for r in s["obeys"]) and all("blocking" in r for r in s["governs"]))
    g2 = dict(g)
    g2["rules"] = sorted(g["rules"], key=lambda r: (r.get("destiny") != "TASTE", r["id"]))
    g2["rules_by_id"] = {r["id"]: r for r in g2["rules"]}
    dest = [r["destiny"] for r in obeys_for(prim, g2, TASK_A) if r["id"].startswith("rule:")]
    first_non = next((i for i, d in enumerate(dest) if d != "BLOCKING"), len(dest))
    bite("MUTATION: blocking still sorts first after the store order is inverted",
         "BLOCKING" in dest and "BLOCKING" not in dest[first_non:], dest[:14])
    bite("obeys carries all three classes on the worked task, each named (+ routed-by-scope since s277-D9)",
         {r["class"] for r in s["obeys"]} >= {"authored", "routed"} and all(r["class"] in ("authored", "derived", "routed", "routed-by-scope") for r in s["obeys"]),
         {r["class"] for r in s["obeys"]})
    bite("governs is LIVE: a ruling that names a chosen meta in governs[] is on the seed",
         any("_rulings.json governs[]" in r["via"] for r in s["governs"]), [r["via"][:60] for r in s["governs"]][:3])
    bite("mustNot is surfaced and carries the nulls with notes",
         len(s["mustNot"]) > 0 and all(a["blocking"] for a in s["mustNot"]) and
         all(a["$note"] for a in s["mustNot"] if a["ref"] is None))
    victim = next((c for c in prim if ((_meta_of(c, g) or {}).get("edges") or {}).get("mustNotNeighbour")), None)
    before = [a for a in s["mustNot"] if victim and a["from"] == victim["id"]]
    after = [a for a in must_not_for([c for c in prim if victim and c["id"] != victim["id"]], g) if victim and a["from"] == victim["id"]]
    bite("MUTATION: drop the component carrying a must-not and the pair disappears",
         victim is not None and len(before) > 0 and len(after) == 0, (len(before), len(after)))
    bite("tokens are at GROUP+TIER grain, never leaves",
         all(t.get("tier") in ("semantic", "component-type", "foundation", "primitive", "composite")
             and len(t["members"]) <= 4 for t in s["tokens"]) and len(s["tokens"]) > 0)
    sa = build_slice("a doormat footer with the masterbrand logo and an accordion", graph=g)
    bite("assets reads the ratified icon/logo node files (a logo-bearing task carries a logo: row)",
         any(a["kind"] == "logo" for a in (sa["assets"] or [])) or any(a["kind"] == "icon" for a in (sa["assets"] or [])),
         (sa["assets"] or [])[:2] or sa["$nulls"].get("assets"))
    sc = build_slice(TASK_C, graph=g)
    bite("a chart task resolves through chart-intents, not by chart name",
         any(i["intent"] in ("comparison", "change-over-time") for i in sc["query"]["intents"]) and
         any((c.get("provides") == "chart-panel") for c in sc["components"]))
    bite("unresolved is honest — every entry carries ref:null and a note",
         all(u.get("ref", None) is None and u.get("$note") for u in s["unresolved"]))
    sb = build_slice(TASK_B, graph=g)
    bite("the real demo prompt resolves a page-frame and a record-list",
         any("page-frame" in (c.get("roles") or []) for c in sb["components"]) and
         any("record-list" in (c.get("roles") or []) for c in sb["components"]))
    bite("sized: the seed is smaller than the metas it replaces, per-field counts present",
         s["sized"]["ratio_vs_selected_metas"] > 1 and set(s["sized"]["per_field"]) == set(CONTRACT_FIELDS) - {"sized"})
    # — budget
    tight = s["sized"]["slice_tokens"] - 1
    bite("BUDGET: an over-budget seed reduces by declared steps or refuses loudly — never silently",
         (lambda r: (isinstance(r, dict) and r["sized"]["within_budget"] and r["sized"]["reductions"]) or isinstance(r, SliceRefused))(
             _try(build_slice, TASK_A, graph=g, budget=tight)))
    bite("BUDGET: an impossible budget is a SliceRefused naming the count",
         (lambda r: isinstance(r, SliceRefused) and "refused" in str(r))(_try(build_slice, TASK_A, graph=g, budget=50)))
    # — ASK
    live = load_live()
    counts = {}
    for i, q in enumerate(ASK_12, 1):
        r = _try(ask, q, seed=s, live=live)
        ok = isinstance(r, dict) and r["sized"]["tokens"] <= ASK_BUDGET and r["q"] == "Q%d" % i
        counts[q] = r["sized"]["tokens"] if isinstance(r, dict) else str(r)
        bite("ASK Q%-2d ≤1K and mapped to its verb: %s" % (i, q[:58]), ok, counts[q])
    bite("ASK refuses over budget loudly (budget 40)",
         (lambda r: isinstance(r, AskRefused) and "over the budget" in str(r))(_try(ask, ASK_12[0], live=live, budget=40)))
    bite("ASK refuses an unmappable question naming the first obstacle",
         (lambda r: isinstance(r, AskRefused) and "no verb" in str(r))(_try(ask, "how are you today?", live=live)))
    bite("ASK refuses a node not in the live graph",
         (lambda r: isinstance(r, AskRefused) and "not in the live graph" in str(r))(_try(ask, "what governs component:zz-none?", live=live)))
    r4 = _try(ask, ASK_12[3], live=live)
    bite("ASK: Q4 on the LIVE tree declares when no tensionWith pair joins two obeyed principles (measured, not assumed)",
         isinstance(r4, dict) and (r4["answer"]["tensions"] or any("no tensionWith" in d for d in r4["declared"])))
    # — seed unchanged by ASK; ASK sees a ruling inscribed AFTER the seed (scratch copy, never live)
    snap = json.dumps(s, sort_keys=True)
    tmp = tempfile.mkdtemp(prefix="compose-slice-selftest-")
    try:
        k2 = os.path.join(tmp, "knowledge")
        os.makedirs(os.path.join(k2, "components"))
        for f in glob.glob(os.path.join(HERE, "components", "*.json")):
            shutil.copy(f, os.path.join(k2, "components"))
        for f in ("_rulings.json", "_ruling_edges.json", "roles.json", "chart-intents.json", "_consult-lexicon.json",
                  "component-types.json", "_rule_nodes.json", "_ux_principle_nodes.json", "_icon_nodes.json", "_logo_nodes.json"):
            if os.path.exists(os.path.join(HERE, f)):
                shutil.copy(os.path.join(HERE, f), k2)
        for d in ("guidelines", "tokens", "compliance"):
            shutil.copytree(os.path.join(HERE, d), os.path.join(k2, d), ignore=shutil.ignore_patterns("__pycache__", "_raw", "_manifests"))
        rj = _load(os.path.join(k2, "_rulings.json"))
        planted = {"id": "s999-D1", "ruled": "PLANTED AFTER THE SEED — selftest only, scratch copy", "date": "2099-01-01",
                   "by": "selftest", "says": "planted", "governs": ["knowledge/components/button.meta.json"],
                   "evidence": ["_compose_slice.py --selftest"], "status": "ruled"}
        rj["rulings"].append(planted)
        json.dump(rj, open(os.path.join(k2, "_rulings.json"), "w"))
        uj = _load(os.path.join(k2, "_ux_principle_nodes.json"))
        uj["edges"].append({"s": "ux:pr-fitts", "t": "ux:pr-hick", "type": "tensionWith", "fam": "uxprinciples",
                            "polarity": "pl-selftest", "mediatingVariable": "PLANTED — selftest only, scratch copy"})
        json.dump(uj, open(os.path.join(k2, "_ux_principle_nodes.json"), "w"))
        live2 = load_live(k2)
        r4b = _try(ask, "which rules conflict for component:button?", live=live2)
        bite("ASK: Q4's 2-hop walk finds a tensionWith pair between two obeyed principles (planted in the scratch copy)",
             isinstance(r4b, dict) and any(p["polarity"] == "pl-selftest" for p in r4b["answer"]["tensions"]),
             r4b if not isinstance(r4b, dict) else r4b["answer"].get("tensions"))
        r = ask("what governs component:button?", seed=s, live=live2)
        bite("LIVE: ASK sees a ruling inscribed AFTER the seed (planted in a scratch copy of _rulings.json)",
             any(x.get("s") == "ruling:s999-D1" for x in r["answer"]["rulings"]) and
             not any(x["id"] == "s999-D1" for x in (s["governs"] or [])),
             [x.get("s") for x in r["answer"]["rulings"]][:4])
        bite("LIVE: the live file was NOT touched by the plant",
             "s999-D1" not in _read(os.path.join(HERE, "_rulings.json")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    bite("SEED unchanged by ASK — byte-identical after 14 asks", json.dumps(s, sort_keys=True) == snap)
    # — cross-check the live reader against the explorer's own extract, when importable
    try:
        sys.path.insert(0, HERE)
        import importlib
        argv = sys.argv
        sys.argv = [argv[0]]
        try:
            bk = importlib.import_module("_build_kg_explorer")
        finally:
            sys.argv = argv
        bn, be = bk.extract()
        xn, xe, _ = bk.extract_extra(bn, be)
        from collections import Counter
        theirs = Counter(e["type"] for e in be + xe if e["type"] in ("governs", "obeys", "appliesTo", "definedIn", "cites", "flaggedBy", "tensionWith", "mustNotNeighbour"))
        mine = Counter(e["type"] for e in live["edges"] if e["type"] in theirs)
        bite("LIVE reader agrees with _build_kg_explorer.extract()+extract_extra() on shared edge-type counts",
             mine == theirs, {k: (mine[k], theirs[k]) for k in theirs if mine[k] != theirs[k]})
    except Exception as ex:  # numpy absent in a pack — declared, not failed
        print("  skip cross-check vs _build_kg_explorer (%s: %s)" % (type(ex).__name__, str(ex)[:80]))
    # — declared scope (s277-D9, #279 lane SC): knowledge/guidelines/_scope.json + routed-by-scope
    sc = g["scope"] or {}
    rows = {r["file"]: r for r in sc.get("rows") or []}
    rule_files = {r["file"] for r in g["rules"]}
    bite("SCOPE: every guideline file carrying rules in _rules-index.json has a row — kind component|facet, or a DECLARED null with a $note",
         rule_files == set(rows) and all((r["kind"] in ("component", "facet")) or (r["kind"] is None and r.get("$note")) for r in rows.values()),
         {"missing": sorted(rule_files - set(rows)), "extra": sorted(set(rows) - rule_files)})

    def _collapse(t):
        return re.sub(r"\s+", " ", t)
    src_ok = {f: r["$source"] in _collapse(_read(os.path.join(HERE, "guidelines", f))) for f, r in rows.items()}
    bite("SCOPE: every $source is a real substring of its LIVE file (whitespace-collapsed) — %d/%d" % (sum(src_ok.values()), len(src_ok)),
         all(src_ok.values()) and all(rows[f]["$source"] for f in rows), [f for f, ok in src_ok.items() if not ok])
    bite("SCOPE: a mutated $source (one word changed) FAILS the same check — the bite can bite",
         not (rows["naming.md"]["$source"].replace("UI copy", "UX copy") in _collapse(_read(os.path.join(HERE, "guidelines", "naming.md")))))
    facets = sc.get("facets") or {}
    fbad = [f for f, v in facets.items() for gname in (v.get("binds") or {}).get("tokenGroups") or [] if gname not in g["token_tiers"]]
    rbad = [(f, x) for f, r in rows.items() for x in r["facets"] if x not in facets] + \
           [(f, x) for f, r in rows.items() for x in r["tokenGroups"] if x not in g["token_tiers"]] + \
           [(f, x) for f, r in rows.items() for x in r["components"] if x not in g["metas"]] + \
           [(f, e["rule"]) for f, r in rows.items() for e in r["exceptions"] if e["rule"] not in {x["id"] for x in g["rules"] if x["file"] == f}]
    bite("SCOPE: every token group / facet / component / exception named exists (groups in the tier map, facets in the closed set, components as metas, exceptions as rules OF THAT FILE)",
         not fbad and not rbad, (fbad + rbad)[:6])
    sr = scope_reach(g)
    nulls = [f for f, r in rows.items() if r["kind"] is None]
    everything = build_slice(components=sorted(g["metas"]), graph=g, max_components=200)
    by_scope = [r for r in (everything["obeys"] or []) if r["class"] == "routed-by-scope"]
    bite("SCOPE: routed-by-scope never fires on a file with a null scope (all %d metas forced in; %d null files: %s; %d routed-by-scope rows)"
         % (len(g["metas"]), len(nulls), ", ".join(nulls), len(by_scope)),
         nulls and by_scope and not any(r["file"] in nulls for r in by_scope) and all(sr[f]["components"] == {} for f in nulls),
         sorted({r["file"] for r in by_scope if r["file"] in nulls}))
    bite("SCOPE: routed-by-scope is never passed off as authored / routed — a row keeps its stronger class when both paths reach it",
         not any("edges.obeys" in r["why"] or "RULE_FILE_ROUTES" in r["why"] or "always-on" in r["why"] for r in by_scope) and
         all("routed-by-scope:" in r["why"] for r in by_scope))
    # MUTATION: plant an exception on a scratch copy of the scope and the rule vanishes from routed-by-scope
    victim = by_scope[0] if by_scope else None
    g3 = dict(g)
    g3.pop("$scope_reach", None)
    g3["scope"] = copy.deepcopy(sc)
    for r in g3["scope"]["rows"]:
        if victim and r["file"] == victim["file"]:
            r["exceptions"].append({"rule": victim["id"][5:], "why": "PLANTED — selftest only, scratch copy"})
    e3 = build_slice(components=sorted(g["metas"]), graph=g3, max_components=200)
    bite("MUTATION: a planted exception row (scratch copy, on %s) suppresses its rule from routed-by-scope; the live file is untouched" % (victim and victim["file"]),
         victim is not None and not any(r["id"] == victim["id"] for r in (e3["obeys"] or [])) and
         "PLANTED" not in _read(os.path.join(HERE, "guidelines", "_scope.json")),
         victim and victim["id"])
    # MUTATION: flip a facet row to null and its rules vanish too
    g4 = dict(g)
    g4.pop("$scope_reach", None)
    g4["scope"] = copy.deepcopy(sc)
    vf = victim and victim["file"]
    for r in g4["scope"]["rows"]:
        if r["file"] == vf:
            r.update(kind=None, facets=[], components=[], **{"$note": "PLANTED null"})
    e4 = build_slice(components=sorted(g["metas"]), graph=g4, max_components=200)
    bite("MUTATION: a row flipped to null (scratch copy, %s) routes nothing — its rows leave routed-by-scope" % vf,
         vf and any(r["file"] == vf for r in by_scope) and not any(r["file"] == vf and r["class"] == "routed-by-scope" for r in (e4["obeys"] or [])))
    ms = measure_scope()
    bite("SCOPE measure: the two paths sum (scope_only + obeys_only + both == reach_by_either) for all rules and for BLOCKING",
         all(ms[k]["scope_only"] + ms[k]["obeys_only"] + ms[k]["both"] == ms[k]["reach_by_either"] for k in ("rules", "blocking")) and
         ms["rules"]["reach_by_either"] >= ms["rules"]["reach_by_obeys"], {k: ms[k] for k in ("rules", "blocking")})
    r2 = ask("which components does rule:copy-012 bind?", live=live)
    bite("ASK Q2 carries the declared-scope path apart from obeys (rule:copy-012 -> copywriting.md facet copy, %d components, %d tokens)"
         % ((r2["answer"].get("routedByScope") or {}).get("count", 0), r2["sized"]["tokens"]),
         (r2["answer"].get("routedByScope") or {}).get("kind") == "facet" and r2["answer"]["components"] == [] and r2["sized"]["tokens"] <= ASK_BUDGET)
    r3 = ask("which components does rule:axf-002 bind?", live=live)
    bite("ASK Q2 on a null-scope file DECLARES the null instead of routing (rule:axf-002)",
         "routedByScope" not in r3["answer"] and any("DECLARED NULL" in d for d in r3["declared"]))
    print("\n%d bites, %d failed" % (n, len(fails)))
    print("ASK token counts: " + json.dumps(counts))
    return 1 if fails else 0


def _try(fn, *a, **kw):
    try:
        return fn(*a, **kw)
    except Exception as ex:
        return ex


def _raises(exc, fn, *a, **kw):
    return isinstance(_try(fn, *a, **kw), exc)


# ---------------------------------------------------------------- cli
def _opt(args, flag, default=None):
    if flag in args:
        i = args.index(flag)
        if i + 1 < len(args) and not args[i + 1].startswith("--"):
            return args[i + 1]
    return default


def main(argv):
    args = list(argv[1:])
    if "--selftest" in args:
        return selftest()
    if "--measure-scope" in args:
        print(json.dumps(measure_scope(), ensure_ascii=False, indent=1))
        return 0
    if "--measure" in args:
        print(json.dumps(measure_claim(task=_opt(args, "--task")), ensure_ascii=False, indent=1))
        return 0
    if "--ask" in args:
        q = _opt(args, "--ask")
        if not q:
            print("--ask needs a question", file=sys.stderr)
            return 2
        seed = _load(_opt(args, "--seed")) if _opt(args, "--seed") else None
        try:
            r = ask(q, seed=seed, budget=int(_opt(args, "--budget", ASK_BUDGET)))
        except AskRefused as ex:
            print("REFUSED (ask): %s" % ex, file=sys.stderr)
            return 3
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    task = next((a for a in args if not a.startswith("--") and (args.index(a) == 0 or not args[args.index(a) - 1].startswith("--") or args[args.index(a) - 1] in ("--explain", "--selftest"))), None)
    typed = {
        "intent": (_opt(args, "--intent") or "").split(",") if _opt(args, "--intent") else None,
        "roles": (_opt(args, "--roles") or "").split(",") if _opt(args, "--roles") else None,
        "components": (_opt(args, "--components") or "").split(",") if _opt(args, "--components") else None,
        "shape": _opt(args, "--shape"),
        "budget": int(_opt(args, "--budget")) if _opt(args, "--budget") else None,
    }
    if not task and not any(typed.values()):
        print(__doc__.split("USAGE")[1].split("RESOLUTION PATH")[0])
        return 2
    try:
        s = build_slice(task, max_components=int(_opt(args, "--max", 14)), **typed)
    except SliceRefused as ex:
        print("REFUSED (seed): %s" % ex, file=sys.stderr)
        return 3
    if "--explain" in args:
        print(explain(s))
    out = _opt(args, "--out")
    if out:
        open(out, "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, indent=1))
        print("wrote %s" % out, file=sys.stderr)
    if "--html" in args:
        hp = _opt(args, "--html", "slice.html")
        open(hp, "w", encoding="utf-8").write(to_html(s))
        print("wrote %s" % hp, file=sys.stderr)
    if not out and "--explain" not in args and "--html" not in args:
        print(json.dumps(s, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
