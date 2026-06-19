#!/usr/bin/env python3
"""Unified cross-reference index (Graphify-borrow #4) — per-component hub.

Joins the four authored/generated layers into ONE traversable record per component:
  - tokens            (from tokens/_blast-radius.json by_component)
  - god_nodes_touched (high-blast tokens this component shares — migration coupling)
  - wcag_sc           (from compliance/graph-index.json by_component)
  - guidelines        (curated topical map + global RAG docs that always apply)
  - anti_patterns     (from the meta, split asserted vs inferred/REVIEW)
  - relationships     (from the meta)
  - deprecated_bindings (from the meta tokenValidation.depricateUsage: token->rebind)

Writes:
  - knowledge/_XREF-INDEX.json  (machine: hub per component for multi-hop queries)
  - knowledge/_XREF-INDEX.md    (human: one table row per component + coverage notes)

Source of truth = the authored canon. This is a derived view; regenerate after
editing metas, tokens, the compliance KG, or the guideline map below:
  python3 knowledge/_build_xref_index.py
Depends on tokens/_blast-radius.json and compliance/graph-index.json being current
(run their generators first).
"""
import json, os, glob, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.join(ROOT, "components")
GUIDE = os.path.join(ROOT, "guidelines")

# --- guideline map: every guideline file that applies to a component ---
# GLOBAL apply to all interactive components (theming + a11y framework + foundations).
GLOBAL = ["accessibility.md", "digital-accessibility-standards.md", "colour-usage.md", "dark-mode.md", "focus-indicators.md"]
# TOPICAL is curated (gradeable, authored — not inferred). Keyed by component name.
TOPICAL = {
    "Accordion":        ["elevation.md", "contextual-help.md"],
    "Avatar":           ["imagery.md", "hexagon-masks.md", "typography-usage.md"],
    "Badge":            ["typography-usage.md"],
    "Breadcrumbs":      ["platform-web.md", "tone-of-voice.md"],
    "Button":           ["calls-to-action.md"],
    "Cards":            ["elevation.md", "imagery.md", "hexagon-masks.md", "icons.md"],
    "Countdown timer":  ["time-based-indicators.md"],
    "Divider":          ["elevation.md"],
    "Dropdown":         ["forms.md", "elevation.md", "icons.md"],
    "Headers":          ["typography-usage.md", "platform-web.md", "logos.md"],
    "Hero":             ["imagery.md", "hexagon-masks.md", "calls-to-action.md", "typography-usage.md"],
    "Input fields":     ["forms.md", "tone-of-voice.md"],
    "Links":            ["calls-to-action.md", "tone-of-voice.md"],
    "List items":       ["typography-usage.md", "icons.md"],
    "Loading indicator":["time-based-indicators.md"],
    "Modals":           ["elevation.md", "calls-to-action.md", "platform-app.md"],
    "Navigations":      ["platform-web.md", "platform-app.md", "icons.md"],
    "Notifications":    ["tone-of-voice.md", "cookie-notifications.md", "icons.md"],
    "Pagination":       ["platform-web.md", "horizontal-scroll.md"],
    "Progress tracker": ["time-based-indicators.md"],
    "Quick actions":    ["calls-to-action.md", "icons.md"],
    "Reorder":          ["icons.md"],
    "Search field":     ["forms.md", "icons.md"],
    "Selection controls":["forms.md"],
    "Slider":           ["forms.md"],
    "Status indicator": ["tone-of-voice.md", "time-based-indicators.md", "icons.md"],
    "Table":            ["horizontal-scroll.md", "typography-usage.md", "view-controls-sort.md"],
    "Tabs":             ["horizontal-scroll.md", "platform-web.md"],
    "Tags":             ["typography-usage.md"],
    "Tooltip":          ["contextual-help.md", "elevation.md"],
    "Video player":     ["time-based-indicators.md", "imagery.md"],
    "View options":     ["view-controls-sort.md", "calls-to-action.md"],
}

# --- load generated layers ---
blast = json.load(open(os.path.join(ROOT, "tokens", "_blast-radius.json")))
by_comp_tokens = blast["by_component"]
# god-nodes = tokens whose blast >= threshold (top tier of the ranking)
GOD_BLAST = 7
god_nodes = {r["token"] for r in blast["ranking"] if r["blast"] >= GOD_BLAST}

compl = json.load(open(os.path.join(ROOT, "compliance", "graph-index.json")))
by_comp_sc = compl["by_component"]

avail_guides = set(os.path.basename(p) for p in glob.glob(os.path.join(GUIDE, "*.md")))

# --- build hub per component ---
hubs = {}
warn_missing_guides = set()
for f in sorted(glob.glob(os.path.join(COMP, "*.meta.json"))):
    b = os.path.basename(f)
    if b.startswith("EXAMPLE") or b == "meta.schema.json":
        continue
    d = json.load(open(f))
    name = d.get("name", b)

    # guidelines: global + topical, only those that actually exist on disk
    guides = []
    for g in GLOBAL + TOPICAL.get(name, []):
        if g in avail_guides and g not in guides:
            guides.append(g)
        elif g not in avail_guides:
            warn_missing_guides.add(g)

    # anti-patterns split
    aps = d.get("antiPatterns", []) or []
    asserted = [a for a in aps if not a.strip().upper().startswith("REVIEW")]
    inferred = [a for a in aps if a.strip().upper().startswith("REVIEW")]

    # deprecated bindings: token -> rebind target
    tv = d.get("tokenValidation")
    du = tv.get("depricateUsage") if isinstance(tv, dict) else None
    dep = du.get("tokens") if isinstance(du, dict) else None
    dep = dep if isinstance(dep, list) else []
    dep_map = []
    for t in dep:
        if isinstance(t, dict):
            dep_map.append({"token": t.get("token"), "rebind": t.get("rebind"), "usedBy": t.get("usedBy")})
        else:
            dep_map.append({"token": str(t), "rebind": None, "usedBy": None})

    toks = by_comp_tokens.get(name, [])
    hubs[name] = {
        "name": name,
        "category": d.get("category"),
        "figma_node": (d.get("provenance") or {}).get("figma_node"),
        "tokens": toks,
        "token_count": len(toks),
        "god_nodes_touched": sorted([t for t in toks if t in god_nodes]),
        "wcag_sc": by_comp_sc.get(name, []),
        "guidelines": guides,
        "anti_patterns": {"asserted": asserted, "inferred_review": inferred},
        "deprecated_bindings": dep_map,
        "deprecated_count": len(dep_map),
    }

index = {
    "$description": "Unified cross-reference index — one hub per component joining tokens, god-nodes touched, WCAG SCs, guideline docs, anti-patterns (asserted vs inferred), relationships and deprecated bindings. Enables multi-hop queries (component->tokens->other components; component->SC->sibling components; component->guideline). Derived view over the authored canon + the two generated indexes; regenerate via _build_xref_index.py. god_nodes_touched = tokens with blast>=%d." % GOD_BLAST,
    "generated": "2026-06-18",
    "guideline_map_note": "guidelines = GLOBAL (apply to all) + TOPICAL (curated per component). Authored, not inferred.",
    "global_guidelines": GLOBAL,
    "totals": {
        "components": len(hubs),
        "with_deprecated_bindings": sum(1 for h in hubs.values() if h["deprecated_count"]),
        "god_node_count": len(god_nodes),
    },
    "components": hubs,
}
json.dump(index, open(os.path.join(ROOT, "_XREF-INDEX.json"), "w"), indent=2, ensure_ascii=False)

# --- human-readable overview ---
L = []
L.append("# Cross-reference index — component hubs")
L.append("")
L.append("> One traversable record per component joining **tokens · god-nodes · WCAG SCs · guidelines · anti-patterns · deprecated bindings**. Generated derived view over the canon (Graphify-borrow #4); regenerate after editing metas/tokens/compliance KG/the guideline map: `python3 knowledge/_build_xref_index.py`. Machine-readable detail in `_XREF-INDEX.json`.")
L.append("")
L.append(f"**Totals:** {len(hubs)} components · {index['totals']['with_deprecated_bindings']} with deprecated bindings · {len(god_nodes)} god-nodes (blast≥{GOD_BLAST}).")
L.append("")
L.append(f"**Global guidelines (apply to every component):** {', '.join(g.replace('.md','') for g in GLOBAL)}.")
L.append("")
L.append("| Component | Cat | #Tok | God-nodes touched | WCAG SCs | Topical guidelines | Dep. |")
L.append("|---|---|---|---|---|---|---|")
for name in sorted(hubs):
    h = hubs[name]
    gn = ", ".join("/".join(t.split("/")[-2:]) for t in h["god_nodes_touched"][:4]) + ("…" if len(h["god_nodes_touched"]) > 4 else "")
    topical = ", ".join(g.replace(".md", "") for g in h["guidelines"] if g not in GLOBAL)
    scs = ", ".join(h["wcag_sc"])
    L.append(f"| {name} | {h['category'][:3] if h['category'] else ''} | {h['token_count']} | {gn or '—'} | {scs or '—'} | {topical or '—'} | {h['deprecated_count'] or ''} |")
L.append("")
L.append("## How to traverse")
L.append("")
L.append("- **Component → everything:** `_XREF-INDEX.json` `components[\"Modals\"]` → its tokens, SCs, guideline docs, anti-patterns, deprecated bindings in one read.")
L.append("- **Token → sibling components (blast):** `tokens/_blast-radius.json` `ranking` (or `by_component` reverse).")
L.append("- **SC → sibling components:** `compliance/graph-index.json` `by_sc`.")
L.append("- **Migration coupling:** components sharing a `god_nodes_touched` entry move together — rebind/test them as a set.")
L.append("")
L.append("> `god_nodes_touched` lists only the high-blast tokens (blast≥%d) a component binds — the ones whose change ripples widely. Full token list per component is in the JSON." % GOD_BLAST)
L.append("")
open(os.path.join(ROOT, "_XREF-INDEX.md"), "w").write("\n".join(L))

print(f"wrote _XREF-INDEX.json + _XREF-INDEX.md for {len(hubs)} components")
print("with deprecated bindings:", index["totals"]["with_deprecated_bindings"])
print("god-nodes (blast>=%d):" % GOD_BLAST, sorted(god_nodes))
if warn_missing_guides:
    print("WARN: mapped guidelines not found on disk:", sorted(warn_missing_guides))
# spot rollup: components per topical guideline
gcount = defaultdict(int)
for h in hubs.values():
    for g in h["guidelines"]:
        if g not in GLOBAL:
            gcount[g] += 1
print("topical guideline reach:", dict(sorted(gcount.items(), key=lambda kv: -kv[1])))