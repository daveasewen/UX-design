#!/usr/bin/env python3
"""
_compose_slice.py — THE COMPOSE-TIME DOOR (third door on the retrieval spine).

A TASK goes in ("a payments dashboard screen with a stat card row, a filter bar and a
data table"); a CLOSED CONTEXT SLICE comes out: the components that provide the roles the
task needs, the BLOCKING rules first, the type composites, the icons, the tokens at TIER
grain, the anti-neighbours, and the ruling behind each item.

WHY IT EXISTS. The generate skill's step 1 today is "Query canon for the components each
screen needs (narrow context — just those nodes + their tokens)"
(skills/prototype-from-library/SKILL.md). There is no query surface for that sentence, so in
practice step 1 is READ THE METAS — 138 files, 3.0 MB, ~730K cl100k tokens if read whole, and
a judgement call about which to open made before anything has been retrieved. The two existing
doors answer different questions: `_consult.py` answers "what GOVERNS X?" over the rules/rulings
corpus, `_memento_search.py` answers "what did we DECIDE about X?" over the session archive.
Neither answers "what do I COMPOSE WITH?". This is that door, and it is a sibling of the other
two by construction: same two-stage posture (cheap refs first, `--fetch`-shaped detail behind
them), same lexicon-grows-on-miss maintenance model, same advisory tier at birth.

⛔ STATUS: PROPOSAL, ADVISORY, NOT WIRED. Nothing in the build calls this. It does not edit a
meta, a registry, a skill, a runbook or a gate. The one decision with weight — whether the
generate skill's step 1 switches to "ask the graph", advisory first or blocking — is Dave's
(notes/_PROPOSAL-compose-time-door-2026-09-14-v1.html).

CLOSED means: the slice says what it could NOT resolve, and why — `ref: null` + `$note`,
never an invention. Every item carries `why` (the edge / field / file that put it there) and
`blocking: true|false`.

RESOLUTION PATH (each hop names its source file):
  task sentence
    -> terms, expanded through knowledge/_consult-lexicon.json + ROLE_LEXICON below
    -> roles (knowledge/roles.json, 12 roles, s252-D1) and chart intents
       (knowledge/chart-intents.json, 5 words, ADR-0017 address set)
    -> components (knowledge/components/*.meta.json: name, provides, answers, shape, when,
       purpose, relationships.commonPatterns, edges.commonPattern/usedInContext)
    -> their edges (consumes / hasPart / composedOf / containedBy / family / groupsWith)
    -> rules (knowledge/guidelines/_rules-index.json — cited by id in the meta, plus the
       rule FILES routed by the component's own vocabulary; BLOCKING sorts first)
    -> type composites (knowledge/tokens/typography-composites.json)
    -> icons (knowledge/assets/icons/icons.manifest.json, via the component's snippet)
    -> tokens at TIER grain (semantic / component-type / foundation / primitive — the GROUP,
       never the 932 leaves)
    -> rulings (edges.governedBy -> knowledge/_rulings.json; plus _ruling_edges.json for what
       supersedes what)

USAGE
  python3 knowledge/_compose_slice.py "<task sentence>"            # JSON slice to stdout
  python3 knowledge/_compose_slice.py "<task>" --html out.html     # readable page
  python3 knowledge/_compose_slice.py "<task>" --out slice.json    # write the JSON
  python3 knowledge/_compose_slice.py "<task>" --explain           # one-screen text
  python3 knowledge/_compose_slice.py --selftest                   # 10 bites, exits 1 on miss

THE LEXICON — GROW ON MISS. ROLE_LEXICON below is hand-authored and deliberately seeded, not
exhaustive — the same maintenance model as knowledge/_consult-lexicon.json (see
_RUNBOOK-consult.md § The lexicon). A real task that misses gets ONE line added here.

LIMITS, DECLARED (do not read past them):
  - `provides` is authored on 24 of 138 metas today, so role -> component resolution leans on
    roles.json's provider lists (a MEMBERSHIP cross-check, per that file's own $description).
    Lane 1 of #270 (knowledge/gen_kg_roles_desk.py) puts role nodes in the graph; when it
    lands, ROLE_PROVIDERS_FROM_GRAPH below is the one function to re-point.
  - `_rules-index.json` carries no component tag. Rule attachment is therefore (a) exact,
    where a meta cites a rule id — 38 metas do — and (b) ROUTED, by rule-file, where the
    component's vocabulary matches. Routed rules are marked `confidence: "routed"` and never
    passed off as authored.
  - Icons are read off the component's own snippet; a component whose snippet names no icon
    resolves to nothing, which is stated, not filled in.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json, os, re, sys, glob, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
COMPONENTS = os.path.join(HERE, "components")
VERSION = "0.1"

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
# asker's word -> chart intent word in knowledge/chart-intents.json (the five-word fence).
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
# a rule attached this way is marked confidence:"routed", never authored.
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

# A COMPOSITE task word stands for several roles at once. These are INFERRED roles: the task
# did not name them, the lexicon did, and every role that arrives this way is flagged
# `inferred: true` in the slice so a reader can tell an inference from a request.
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


def load_graph(root=HERE):
    """Everything the door reads, loaded once. Returns a dict of raw stores."""
    metas = {}
    for f in sorted(glob.glob(os.path.join(root, "components", "*.meta.json"))):
        slug = os.path.basename(f)[:-10]
        if slug.startswith("EXAMPLE-"):
            continue
        m = _load(f)
        if isinstance(m, dict) and m.get("name"):
            m["$slug"] = slug
            m["$path"] = os.path.relpath(f, ROOT)
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
        "icons": _load(os.path.join(root, "assets", "icons", "icons.manifest.json")).get("groups", {}),
        "composites": _load(os.path.join(root, "tokens", "typography-composites.json")),
        "semantic_colour": _load(os.path.join(root, "tokens", "semantic-colour.json")),
        "component_types": _load(os.path.join(root, "component-types.json")).get("component-type", {}),
        "$root": root,
    }
    g["rules_by_id"] = {r["id"]: r for r in g["rules"] if isinstance(r, dict) and r.get("id")}
    g["token_tiers"] = _token_tier_map(g, root)
    return g


def _token_tier_map(g, root):
    """group name -> (tier, source file). TIER grain is the whole point: a slice names the
    token GROUP and its tier, never the leaves (932 of them at last count, #269 gaps proposal)."""
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


# ---------------------------------------------------------------- stage 1: the task sentence
def terms_of(task, lexicon):
    raw = re.findall(r"[a-z][a-z0-9-]+", task.lower())
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


def roles_of(task, terms, g):
    """task -> roles. Two legs: the hand lexicon (phrase match on the raw sentence) and a
    direct hit on a role slug or a provider slug."""
    low = " " + task.lower() + " "
    out = {}
    for role, words in ROLE_LEXICON.items():
        for w in words:
            if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
                out.setdefault(role, {"role": role, "why": 'ROLE_LEXICON["%s"] <- "%s"' % (role, w),
                                      "hits": []})
                out[role]["hits"].append(w)
    for word, roles in COMPOSITE_LEXICON.items():
        if re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", low):
            for role in roles:
                if role in out:
                    continue            # explicitly named beats inferred; keep the stronger why
                out[role] = {"role": role, "hits": [word], "inferred": True,
                             "why": 'COMPOSITE_LEXICON["%s"] -> %s (INFERRED — the task did not '
                                    'name this role)' % (word, role)}
    for role, spec in g["roles"].items():
        if role.replace("-", " ") in low or role in low:
            out.setdefault(role, {"role": role, "why": "roles.json role slug named in task", "hits": [role]})
        for p in spec.get("providers", []):
            slug = p.get("slug", "")
            if slug and re.search(r"(?<![a-z])" + re.escape(slug.lower().replace("-", " ")) + r"(?![a-z])", low):
                out.setdefault(role, {"role": role, "why": "roles.json provider %s named in task" % slug,
                                      "hits": [slug]})
    for r in out.values():
        spec = g["roles"].get(r["role"], {})
        r["definition"] = (spec.get("definition") or "")[:180]
        r["providers"] = [p.get("slug") for p in spec.get("providers", [])]
        r["blocking"] = False
    return list(out.values())


def intents_of(task, g):
    low = " " + task.lower() + " "
    out = []
    for intent, words in INTENT_LEXICON.items():
        for w in words:
            if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
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


def pick_components(task, terms, roles, intents, g, max_components=14, min_score=3.0):
    low = " " + task.lower() + " "
    role_slugs, role_rank = {}, {}
    for r in roles:
        for i, p in enumerate(r.get("providers", [])):
            role_slugs.setdefault(p, []).append(r["role"])
            # roles.json lists providers in ORDER, the first carrying `when: "default — ..."`.
            # That order is the tie-break, so a co-provider never wins on alphabet.
            role_rank[p] = min(role_rank.get(p, 99), i)
    for slug, m in g["metas"].items():                      # the authored half (24 metas)
        if m.get("provides"):
            for r in roles:
                if m["provides"] == r["role"]:
                    role_slugs.setdefault(slug, []).append(r["role"])
    scored = []
    for slug, m in g["metas"].items():
        blob = _meta_blob(m)
        score, whys = 0.0, []
        name = m.get("name", "").lower()
        if re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", low) or \
           re.search(r"(?<![a-z])" + re.escape(slug.replace("-", " ")) + r"(?![a-z])", low):
            score += 8
            whys.append("named in the task")
        else:
            # PARTIAL name match: "a filter bar" must reach Filter-toolbar-bar, which is in no
            # roles.json provider list today (a real gap — see `unresolved`). Two of the slug's
            # own words present in the task is the bar.
            words = [w for w in re.split(r"[-_ ]", slug.lower()) if len(w) > 2]
            hitw = [w for w in words if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low)]
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
        if intents and m.get("intent"):
            mi = m["intent"] if isinstance(m["intent"], list) else [m["intent"]]
            if any(i["intent"] in mi for i in intents):
                score += 4
                whys.append("meta.intent matches chart-intent " + "/".join(mi))
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
        named = "named in the task" in " ".join(whys)
        # chart-panel is the role whose provider is chosen by the INTENT WORD, not by the role
        # (roles.json, role 3: "gated by answers, not by the role"). No intent in the task means
        # the chart is NOT resolvable — say so, never pick one.
        if rl == ["chart-panel"] and not named:
            mi = m.get("intent") if isinstance(m.get("intent"), list) else [m.get("intent")]
            if not want_intents:
                if any(nn["what"] == "role:chart-panel" for nn in notes):
                    continue
                notes.append({"what": "role:chart-panel", "ref": None,
                              "$note": "the task asks for a chart but names no analytical intent "
                                       "(comparison / change-over-time / distribution / "
                                       "relationship / composition, knowledge/chart-intents.json). "
                                       "The chart cannot be chosen mechanically — ask, do not guess.",
                              "why": "chart-intents.json is the gate on this role"})
                want_intents = None       # report once
                continue
            if want_intents is None or not any(i in (mi or []) for i in want_intents):
                continue
        # ONE WINNER PER ROLE (roles.json: co-providers are SUBSTITUTES, and for page-frame only
        # one can win at all). The runners-up are kept as ALTERNATES — capped, because a slice
        # that hands back all 27 `input` providers is a catalogue, not a slice — except
        # chart-panel, where the intent word, not the role, picks the chart (roles.json, role 3).
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
        if len([c for c in chosen if not c["alternate"]]) >= max_components:
            break
    return chosen, notes


def _component_row(m, score, whys, roles, g, alternate=None):
    ed = m.get("edges") or {}

    def refs(et):
        out = []
        for e in ed.get(et, []) or []:
            if isinstance(e, dict) and e.get("ref"):
                out.append(e["ref"])
        return out
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
        "alternate": alternate,          # non-null => a co-provider held in reserve, not the pick
        "why": "; ".join(whys),
        "blocking": False,
    }


def expand_required(chosen, g):
    """A component's `consumes` / `hasPart` atoms are REQUIRED — the page cannot be composed
    without them — so they join the slice with the edge that pulled them in as their `why`."""
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


# ---------------------------------------------------------------- stage 3: rules
RULE_ID_RX = re.compile(r"\b[a-z]{2,6}\d{0,2}-\d{3}\b")


def rules_for(chosen, g, task):
    """Two legs, both named. (a) EXACT: a rule id cited in the component's own meta.
    (b) ROUTED: a rule FILE routed by the component's vocabulary (RULE_FILE_ROUTES) or by the
    always-on screen set. BLOCKING sorts first, always — that is the whole ordering contract."""
    out = {}
    low = (" " + task.lower() + " ") + " ".join(
        (c.get("purpose") or "") + " " + (c.get("name") or "") + " " + (c.get("category") or "")
        for c in chosen).lower()
    for c in chosen:
        mp = os.path.join(ROOT, c["meta"]) if c.get("meta") else None
        if not mp or not os.path.exists(mp):
            continue
        txt = open(mp, encoding="utf-8", errors="replace").read()
        for rid in set(RULE_ID_RX.findall(txt)):
            r = g["rules_by_id"].get(rid)
            if not r:
                continue
            row = out.setdefault(rid, _rule_row(r))
            row["why"].append("cited in " + os.path.basename(c["meta"]))
            row["confidence"] = "authored"
    files = set(SCREEN_ALWAYS)
    route_why = {f: "always-on for a composed screen" for f in SCREEN_ALWAYS}
    for fn, words in RULE_FILE_ROUTES.items():
        for w in words:
            if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
                files.add(fn)
                route_why.setdefault(fn, 'routed by vocabulary "%s" (RULE_FILE_ROUTES)' % w)
                break
    for r in g["rules"]:
        if r.get("file") in files and r.get("destiny") == "BLOCKING":
            row = out.setdefault(r["id"], _rule_row(r))
            if row.get("confidence") != "authored":
                row["confidence"] = "routed"
            row["why"].append(route_why[r["file"]])
    rows = list(out.values())
    for row in rows:
        row["why"] = "; ".join(sorted(set(row["why"])))
    # THE ORDERING CONTRACT — blocking first, then REVIEW, then the rest; stable by id inside.
    order = {"BLOCKING": 0, "REVIEW": 1, "ADVISORY": 2, "TASTE": 3}
    rows.sort(key=lambda r: (order.get(r["destiny"], 9), 0 if r["confidence"] == "authored" else 1,
                             r["id"]))
    return rows


def _rule_row(r):
    return {"id": r["id"], "destiny": r.get("destiny"), "blocking": r.get("destiny") == "BLOCKING",
            "file": r.get("file"), "rule": r.get("rule", "")[:400], "confidence": "routed",
            "why": []}


# ---------------------------------------------------------------- stage 4: anti-neighbours
def anti_neighbours(chosen, g):
    """mustNotNeighbour, from BOTH homes — edges.mustNotNeighbour (typed, 70 across the library)
    and relationships.mustNotNeighbour (prose). A null ref is SURFACED, never dropped: the
    prohibition is real even where the other end is not yet a node."""
    ids = {c["id"] for c in chosen}
    out = []
    for c in chosen:
        mp = os.path.join(ROOT, c["meta"]) if c.get("meta") else None
        if not mp or not os.path.exists(mp):
            continue
        m = _load(mp)
        for e in ((m.get("edges") or {}).get("mustNotNeighbour") or []):
            if not isinstance(e, dict):
                continue
            ref = e.get("ref")
            out.append({"from": c["id"], "to": ref, "ref": ref,
                        "$note": (e.get("$note") or e.get("note") or "") or None,
                        "in_slice": bool(ref) and ref in ids,
                        "why": "edges.mustNotNeighbour on " + os.path.basename(c["meta"]),
                        "blocking": True})
        for txt in ((m.get("relationships") or {}).get("mustNotNeighbour") or []):
            out.append({"from": c["id"], "to": None, "ref": None, "$note": str(txt),
                        "in_slice": False,
                        "why": "relationships.mustNotNeighbour on " + os.path.basename(c["meta"]),
                        "blocking": True})
        for nw in (c.get("not-with") or []):
            ref = nw if isinstance(nw, str) else (nw.get("ref") if isinstance(nw, dict) else None)
            out.append({"from": c["id"], "to": ref, "ref": ref,
                        "$note": (nw.get("$note") if isinstance(nw, dict) else None),
                        "in_slice": bool(ref) and ref in ids,
                        "why": "meta.not-with on " + os.path.basename(c["meta"]),
                        "blocking": True})
    out.sort(key=lambda r: (not r["in_slice"], r["from"], str(r["to"])))
    return out


# ---------------------------------------------------------------- stage 5: type, icons, tokens
TOKEN_PATH_RX = re.compile(r"\b([a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:/[a-z0-9][a-z0-9-]*){1,3})\b")


def type_composites(chosen, g):
    comp = g["composites"]
    out = []
    names = []
    for grp in ("editorial", "component"):
        for k in (comp.get(grp) or {}):
            if not k.startswith("$"):
                names.append((grp, k))
    blob = " ".join((c.get("purpose") or "") + " " + (c.get("name") or "") for c in chosen).lower()
    metatext = ""
    for c in chosen:
        mp = os.path.join(ROOT, c["meta"]) if c.get("meta") else None
        if mp and os.path.exists(mp):
            metatext += open(mp, encoding="utf-8", errors="replace").read().lower()
    for grp, k in names:
        hits = []
        if re.search(r"(?<![a-z])" + re.escape(k) + r"(?![a-z-])", blob):
            hits.append("component purpose names it")
        if re.search(r"typography[-/]composites?/" + re.escape(grp) + "/" + re.escape(k), metatext) or \
           re.search(r'"' + re.escape(k) + r'"\s*:', metatext) and grp == "component":
            hits.append("named in a selected meta")
        if not hits:
            continue
        spec = (comp.get(grp) or {}).get(k) or {}
        ext = ((spec.get("$extensions") or {}).get("com.apollo.sds") or {})
        out.append({"path": "typography-composites/%s/%s" % (grp, k), "tier": "composite",
                    "weight": ext.get("weight"), "trim": ext.get("trim"),
                    "descender-guard": ext.get("descender-guard"),
                    "why": "; ".join(hits), "blocking": False})
    return out


def icons_for(chosen, g):
    by_file = {}
    for grp, items in (g["icons"] or {}).items():
        for it in items:
            by_file[it.get("file", "")] = dict(it, group=grp)
    out, unresolved = [], []
    for c in chosen:
        snip = c.get("snippet")
        if not snip:
            continue
        p = os.path.join(HERE, "snippets", snip.split(":", 1)[-1])
        if not os.path.exists(p):
            continue
        txt = open(p, encoding="utf-8", errors="replace").read()
        hits = set(re.findall(r"icons/([a-z0-9][a-z0-9/-]*\.svg)", txt))
        hits |= {d + ".svg" for d in re.findall(r'data-icon="([a-z0-9][a-z0-9/-]*)"', txt)}
        for m in hits:
            rec = by_file.get(m)
            if rec:
                out.append({"slug": rec.get("slug"), "file": "assets/icons/" + m,
                            "group": rec.get("group"), "active": rec.get("active"),
                            "why": "used by %s (%s)" % (c["id"], snip), "blocking": False})
            else:
                unresolved.append({"what": "icon " + m, "ref": None,
                                   "$note": "referenced by %s but not in assets/icons/icons.manifest.json"
                                            % snip, "why": "snippet scan"})
    seen, dedup = set(), []
    for i in out:
        if i["file"] in seen:
            continue
        seen.add(i["file"])
        dedup.append(i)
    return sorted(dedup, key=lambda i: i["file"]), unresolved


def tokens_for(chosen, g):
    """TIER grain: the GROUP and its tier, with up to 4 example members and an honest count.
    Never the leaves — 932 token leaves is the thing this door exists not to hand anybody."""
    groups = {}
    unresolved = []
    for c in chosen:
        mp = os.path.join(ROOT, c["meta"]) if c.get("meta") else None
        if not mp or not os.path.exists(mp):
            continue
        m = _load(mp)
        vals = []
        tk = m.get("tokens")
        if isinstance(tk, dict):
            vals = [str(v) for v in tk.values()] + list(tk.keys())
        elif isinstance(tk, list):
            vals = [str(v) for v in tk]
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
                row["why"].add("tokens on " + os.path.basename(c["meta"]))
    for grp, row in groups.items():
        row["count"] = len(row["members"])
        row["members"] = sorted(row["members"])[:4]
        row["why"] = "; ".join(sorted(row["why"])[:3])
    order = {"semantic": 0, "component-type": 1, "foundation": 2, "primitive": 3}
    return sorted(groups.values(), key=lambda r: (order.get(r["tier"], 9), r["group"])), unresolved


# ---------------------------------------------------------------- stage 6: rulings
def rulings_for(chosen, g):
    out = {}
    for c in chosen:
        mp = os.path.join(ROOT, c["meta"]) if c.get("meta") else None
        if not mp or not os.path.exists(mp):
            continue
        m = _load(mp)
        for e in ((m.get("edges") or {}).get("governedBy") or []):
            if not isinstance(e, dict) or not e.get("ref"):
                continue
            rid = e["ref"].split(":", 1)[-1]
            r = g["rulings"].get(rid)
            row = out.setdefault(rid, {"id": rid, "says": (r or {}).get("says", "")[:300] or None,
                                       "date": (r or {}).get("date"), "by": (r or {}).get("by"),
                                       "ref": "ruling:" + rid if r else None,
                                       "why": [], "blocking": True})
            row["why"].append("edges.governedBy on " + os.path.basename(c["meta"]))
            if not r:
                row["$note"] = "ruling id cited by a meta but absent from knowledge/_rulings.json"
    ids = set(out)
    for e in g["ruling_edges"]:
        s, t = e.get("s") or e.get("from"), e.get("t") or e.get("to")
        for a, b in ((s, t), (t, s)):
            if isinstance(a, str) and a.split(":")[-1] in ids and isinstance(b, str):
                rid = a.split(":")[-1]
                out[rid].setdefault("related", []).append({"type": e.get("type"), "other": b})
    for row in out.values():
        row["why"] = "; ".join(sorted(set(row["why"])))
    return sorted(out.values(), key=lambda r: r["id"])


# ---------------------------------------------------------------- the slice
def unresolved_report(task, roles, chosen, g, extra):
    out = list(extra)
    covered = set()
    for c in chosen:
        covered |= set(c.get("roles") or [])
        if c.get("provides"):
            covered.add(c["provides"])
    for r in roles:
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
                                 "roles.json provider list, so its ROLE is unknown today "
                                 "(lane 1 of #270 puts role nodes in the graph)",
                        "why": "meta has no provides field"})
        if not c.get("when") and c.get("alternate"):
            out.append({"what": c["id"], "ref": None,
                        "$note": "held as an alternate co-provider of %s but carries no `when` "
                                 "predicate, so the choice between them is not mechanical "
                                 "(s251-D5)" % (c["alternate"],),
                        "why": "meta has no when field"})
    seen, dedup = set(), []
    for u in out:
        k = (str(u.get("what")), (u.get("$note") or "")[:80])
        if k in seen:
            continue
        seen.add(k)
        dedup.append(u)
    return dedup


def build_slice(task, root=HERE, graph=None, max_components=14):
    g = graph or load_graph(root)
    terms, term_why = terms_of(task, g["lexicon"])
    roles = roles_of(task, terms, g)
    intents = intents_of(task, g)
    chosen, pick_notes = pick_components(task, terms, roles, intents, g,
                                         max_components=max_components)
    required, dangling = expand_required(chosen, g)
    chosen = chosen + required
    primary = [c for c in chosen if not c.get("alternate")]
    rules = rules_for(primary, g, task)
    anti = anti_neighbours(primary, g)
    comps = type_composites(primary, g)
    icons, icon_unres = icons_for(primary, g)
    toks, tok_unres = tokens_for(primary, g)
    ruls = rulings_for(primary, g)
    unres = unresolved_report(task, roles, chosen, g,
                              pick_notes + icon_unres + tok_unres +
                              [dict(d, what=d["id"]) for d in dangling])
    slice_ = {
        "$tool": "_compose_slice.py v%s — the compose-time door (#270 lane 2). ADVISORY, not wired."
                 % VERSION,
        "$closed": "Every item names the edge/field/file that put it there (`why`) and whether it "
                   "BLOCKS. What could not be resolved is in `unresolved` with ref:null — never "
                   "invented.",
        "task": task,
        "generated": datetime.date.today().isoformat(),
        "query": {"terms": terms, "roles": roles, "intents": intents},
        "components": chosen,
        "rules": rules,
        "antiNeighbours": anti,
        "typeComposites": comps,
        "icons": icons,
        "tokens": toks,
        "rulings": ruls,
        "unresolved": unres,
    }
    slice_["measure"] = measure(slice_, g)
    return slice_


# ---------------------------------------------------------------- the headline number
def _tok(text):
    try:
        import tiktoken
        return len(tiktoken.get_encoding("cl100k_base").encode(text))
    except Exception:
        return max(1, len(text) // 4)          # declared fallback, never presented as measured


def measure(slice_, g):
    body = json.dumps({k: v for k, v in slice_.items() if k != "measure"}, ensure_ascii=False)
    slice_tokens = _tok(body)
    metas = [c["meta"] for c in slice_["components"] if c.get("meta")]
    read_today = 0
    for p in metas:
        fp = os.path.join(ROOT, p)
        if os.path.exists(fp):
            read_today += _tok(open(fp, encoding="utf-8", errors="replace").read())
    whole = 0
    for slug, m in g["metas"].items():
        whole += _tok(open(os.path.join(ROOT, m["$path"]), encoding="utf-8", errors="replace").read())
    try:
        import tiktoken  # noqa: F401
        unit = "cl100k (tiktoken) — a LABELLED ESTIMATOR, never a unit a cap is stated in (ds-021)"
    except Exception:
        unit = "chars/4 FALLBACK — tiktoken absent; NOT a measurement (ds-021)"
    return {
        "unit": unit,
        "slice_tokens": slice_tokens,
        "metas_in_slice": len(metas),
        "metas_in_slice_tokens": read_today,
        "ratio_vs_selected_metas": round(read_today / slice_tokens, 2) if slice_tokens else None,
        "library_metas": len(g["metas"]),
        "library_metas_tokens": whole,
        "ratio_vs_whole_library": round(whole / slice_tokens, 2) if slice_tokens else None,
    }


# ---------------------------------------------------------------- renderers
def explain(s):
    L = []
    m = s["measure"]
    L.append("TASK  " + s["task"])
    L.append("ROLES " + ", ".join(r["role"] for r in s["query"]["roles"]) or "(none)")
    if s["query"]["intents"]:
        L.append("INTENT " + ", ".join(i["intent"] for i in s["query"]["intents"]))
    L.append("")
    L.append("COMPONENTS (%d, %d alternates)" %
             (len([c for c in s["components"] if not c.get("alternate")]),
              len([c for c in s["components"] if c.get("alternate")])))
    for c in s["components"]:
        L.append("  %-34s %-16s %s%s" % (c["id"], "/".join(c.get("roles") or []) or "-",
                                         c["why"][:70], "  [ALT]" if c.get("alternate") else ""))
    nb = len([r for r in s["rules"] if r["blocking"]])
    L.append("")
    L.append("RULES %d (%d BLOCKING, first)" % (len(s["rules"]), nb))
    for r in s["rules"][:12]:
        L.append("  %-11s %-9s %s" % (r["id"], r["destiny"], r["rule"][:78]))
    L.append("")
    L.append("ANTI-NEIGHBOURS %d" % len(s["antiNeighbours"]))
    for a in s["antiNeighbours"][:8]:
        L.append("  %s  x  %s   %s" % (a["from"], a["to"] or "(ref:null)", (a["$note"] or "")[:60]))
    L.append("")
    L.append("TOKENS (tier grain) " + ", ".join("%s[%s:%d]" % (t["group"], t["tier"], t["count"])
                                                for t in s["tokens"]))
    L.append("TYPE " + ", ".join(t["path"] for t in s["typeComposites"]) or "(none)")
    L.append("ICONS %d   RULINGS %s" % (len(s["icons"]), ", ".join(r["id"] for r in s["rulings"]) or "-"))
    L.append("")
    L.append("UNRESOLVED %d" % len(s["unresolved"]))
    for u in s["unresolved"][:8]:
        L.append("  %-28s %s" % (u["what"], (u["$note"] or "")[:80]))
    L.append("")
    L.append("MEASURE  slice %d tok  vs  %d tok of the %d metas it replaces  = %sx  "
             "(whole library %d tok = %sx)" %
             (m["slice_tokens"], m["metas_in_slice_tokens"], m["metas_in_slice"],
              m["ratio_vs_selected_metas"], m["library_metas_tokens"], m["ratio_vs_whole_library"]))
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
    m = s["measure"]
    P = ["<title>Compose slice — %s</title>" % e(s["task"][:60]), "<style>%s</style>" % CSS,
         '<div class="wrap">', "<h1>%s</h1>" % e(s["task"]),
         '<p class="muted mono">%s · generated %s</p>' % (e(s["$tool"]), s["generated"])]
    P.append('<div class="grid">')
    for k, v in (("slice", m["slice_tokens"]), ("metas it replaces", m["metas_in_slice_tokens"]),
                 ("ratio", str(m["ratio_vs_selected_metas"]) + "x"),
                 ("vs whole library", str(m["ratio_vs_whole_library"]) + "x")):
        P.append('<div><div class="k">%s</div><div class="big">%s</div></div>' % (e(k), e(str(v))))
    P.append("</div>")
    P.append('<div class="note">Unit: %s</div>' % e(m["unit"]))

    P.append("<h2>Query</h2><p>roles: <span class='b'>%s</span> · intents: %s</p>" % (
        e(", ".join(r["role"] for r in s["query"]["roles"]) or "none"),
        e(", ".join(i["intent"] for i in s["query"]["intents"]) or "none")))

    P.append("<h2>Components</h2><table><tr><th>component</th><th>role</th><th>when</th><th>why</th></tr>")
    for c in s["components"]:
        P.append("<tr><td class='mono'>%s%s</td><td>%s</td><td class='muted'>%s</td><td class='muted'>%s</td></tr>"
                 % (e(c["id"]), " <span class='b'>ALT</span>" if c.get("alternate") else "",
                    e("/".join(c.get("roles") or []) or "—"), e((c.get("when") or "—")[:150]),
                    e(c.get("why", "")[:160])))
    P.append("</table>")

    P.append("<h2>Rules — blocking first</h2><table><tr><th>id</th><th>destiny</th><th>rule</th><th>why</th></tr>")
    for r in s["rules"]:
        P.append("<tr><td class='mono %s'>%s</td><td>%s</td><td>%s</td><td class='muted'>%s</td></tr>"
                 % ("b" if r["blocking"] else "", e(r["id"]), e(r["destiny"] or ""),
                    e(r["rule"][:220]), e(r["why"][:110])))
    P.append("</table>")

    P.append("<h2>Anti-neighbours</h2><table><tr><th>from</th><th>must not neighbour</th><th>note</th></tr>")
    for a in s["antiNeighbours"]:
        P.append("<tr><td class='mono'>%s</td><td class='mono b'>%s</td><td class='muted'>%s</td></tr>"
                 % (e(a["from"]), e(a["to"] or "ref:null"), e((a["$note"] or "")[:200])))
    P.append("</table>")

    P.append("<h2>Tokens — tier grain</h2><table><tr><th>group</th><th>tier</th><th>members</th><th>count</th></tr>")
    for t in s["tokens"]:
        P.append("<tr><td class='mono'>%s/*</td><td>%s</td><td class='mono muted'>%s</td><td>%d</td></tr>"
                 % (e(t["group"]), e(t["tier"]), e(", ".join(t["members"])), t["count"]))
    P.append("</table>")

    P.append("<h2>Type composites</h2><p class='mono'>%s</p>" %
             e(", ".join(t["path"] for t in s["typeComposites"]) or "none resolved"))
    P.append("<h2>Icons (%d)</h2><p class='mono muted'>%s</p>" %
             (len(s["icons"]), e(", ".join(i["slug"] or i["file"] for i in s["icons"]) or "none")))

    P.append("<h2>Rulings behind the slice</h2><table><tr><th>id</th><th>says</th><th>why</th></tr>")
    for r in s["rulings"]:
        P.append("<tr><td class='mono b'>%s</td><td>%s</td><td class='muted'>%s</td></tr>"
                 % (e(r["id"]), e(r.get("says") or r.get("$note") or ""), e(r["why"][:110])))
    P.append("</table>")

    P.append("<h2>Not resolvable today</h2><table><tr><th>what</th><th>ref</th><th>note</th></tr>")
    for u in s["unresolved"]:
        P.append("<tr><td class='mono'>%s</td><td class='mono'>null</td><td class='muted'>%s</td></tr>"
                 % (e(str(u["what"])), e((u.get("$note") or "")[:240])))
    P.append("</table></div>")
    return "\n".join(P)


# ---------------------------------------------------------------- selftest
TASK_A = "a payments dashboard screen with a stat card row, a filter bar and a data table"
TASK_B = "build me a financial dashboard for corporate international banking. Please make the all the interactive elements work such as filtering and navigation."
TASK_C = "a liquidity overview comparing balances by currency over time with a chart panel and a stat card row"


def selftest():
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
    bite("1 the worked task resolves the table", "component:table" in ids, ids[:6])
    bite("2 the worked task resolves a headline-metric provider",
         any("headline-metric" in (c.get("roles") or []) for c in s["components"]),
         [c["roles"] for c in s["components"]][:8])
    bite("3 every slice item carries a why + blocking flag",
         all(("why" in c and "blocking" in c) for c in s["components"]) and
         all(("why" in r and "blocking" in r) for r in s["rules"]))

    # 4 — THE ORDERING CONTRACT, mutation-tested: the slice must sort BLOCKING first even when
    # the rule store hands them back last. Mutate the input order, re-run the sorter, re-check.
    g2 = dict(g)
    g2["rules"] = sorted(g["rules"], key=lambda r: (r.get("destiny") != "TASTE", r["id"]))
    g2["rules_by_id"] = {r["id"]: r for r in g2["rules"]}
    prim = [c for c in s["components"] if not c.get("alternate")]
    mut = rules_for(prim, g2, TASK_A)
    dest = [r["destiny"] for r in mut]
    first_non = next((i for i, d in enumerate(dest) if d != "BLOCKING"), len(dest))
    bite("4 MUTATION: blocking still sorts first after the store order is inverted",
         "BLOCKING" in dest and "BLOCKING" not in dest[first_non:], dest[:14])
    bite("5 the blocking set is non-empty and matches the index's own destiny field",
         all(g["rules_by_id"][r["id"]]["destiny"] == "BLOCKING"
             for r in s["rules"] if r["blocking"]) and any(r["blocking"] for r in s["rules"]))

    # 6 — anti-neighbour surfaced, mutation-tested both ways.
    bite("6 an anti-neighbour pair is surfaced for the worked task",
         len(s["antiNeighbours"]) > 0 and all(a["blocking"] for a in s["antiNeighbours"]),
         len(s["antiNeighbours"]))
    victim = next((c for c in prim if c["meta"] and
                   ((_load(os.path.join(ROOT, c["meta"])).get("edges") or {}).get("mustNotNeighbour"))), None)
    if victim:
        before = [a for a in s["antiNeighbours"] if a["from"] == victim["id"]]
        stripped = [c for c in prim if c["id"] != victim["id"]]
        after = [a for a in anti_neighbours(stripped, g) if a["from"] == victim["id"]]
        bite("7 MUTATION: drop the component carrying it and the pair disappears",
             len(before) > 0 and len(after) == 0, (len(before), len(after)))
    else:
        bite("7 MUTATION: drop the component carrying it and the pair disappears", False,
             "no selected component carries edges.mustNotNeighbour")

    bite("8 tokens are at TIER grain, never leaves",
         all(t.get("tier") in ("semantic", "component-type", "foundation", "primitive")
             and len(t["members"]) <= 4 for t in s["tokens"]) and len(s["tokens"]) > 0,
         [(t["group"], t["tier"]) for t in s["tokens"]])

    sc = build_slice(TASK_C, graph=g)
    bite("9 a chart task resolves through chart-intents, not by chart name",
         any(i["intent"] in ("comparison", "change-over-time") for i in sc["query"]["intents"]) and
         any((c.get("provides") == "chart-panel") for c in sc["components"]),
         [i["intent"] for i in sc["query"]["intents"]])

    bite("10 unresolved is honest — every entry carries ref:null and a note",
         all(u.get("ref", None) is None and u.get("$note") for u in s["unresolved"]),
         s["unresolved"][:2])

    sb = build_slice(TASK_B, graph=g)
    bite("11 the real demo prompt resolves a page-frame and a record-list",
         any("page-frame" in (c.get("roles") or []) for c in sb["components"]) and
         any("record-list" in (c.get("roles") or []) for c in sb["components"]),
         [(c["id"], c["roles"]) for c in sb["components"]][:8])
    bite("12 the slice is smaller than the metas it replaces",
         s["measure"]["ratio_vs_selected_metas"] and s["measure"]["ratio_vs_selected_metas"] > 1,
         s["measure"])

    print("\n%d bites, %d failed" % (n, len(fails)))
    return 1 if fails else 0


# ---------------------------------------------------------------- cli
def main(argv):
    args = [a for a in argv[1:]]
    if "--selftest" in args:
        return selftest()
    task = next((a for a in args if not a.startswith("--")), None)
    if not task:
        print(__doc__.split("USAGE")[1].split("THE LEXICON")[0])
        return 2
    maxc = 14
    if "--max" in args:
        maxc = int(args[args.index("--max") + 1])
    s = build_slice(task, max_components=maxc)
    if "--explain" in args:
        print(explain(s))
    out = None
    if "--out" in args:
        out = args[args.index("--out") + 1]
        open(out, "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, indent=1))
        print("wrote %s" % out, file=sys.stderr)
    if "--html" in args:
        i = args.index("--html")
        hp = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith("--") else "slice.html"
        open(hp, "w", encoding="utf-8").write(to_html(s))
        print("wrote %s" % hp, file=sys.stderr)
    if not out and "--explain" not in args and "--html" not in args:
        print(json.dumps(s, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
