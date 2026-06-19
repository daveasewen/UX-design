#!/usr/bin/env python3
"""Derived-view generators over the knowledge graph (Graphify-inspired, no dependency).

Produces:
  - knowledge/tokens/_blast-radius.json  : token -> [components] reverse index + god-node ranking
  - knowledge/_GRAPH-REPORT.md           : health dashboard (god-nodes, groups, orphans, compliance, depricate)

Token usage is matched by scanning each component meta's `tokens` + `subComponents`
blocks for the exact store token paths (word-boundary safe), so only real tokens count
and prefixes (icon/default vs icon/default-reverse) don't double-match.
"""
import json, re, glob, os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOK = os.path.join(ROOT, "tokens")
COMP = os.path.join(ROOT, "components")

# --- token store: all defined leaf paths ---
store = {}
def walk(node, path=""):
    if isinstance(node, dict):
        if any(k in node for k in ("$value", "light", "scale-1", "dark")):
            store[path] = True
        for k, v in node.items():
            if k.startswith("$"):
                continue
            walk(v, (path + "/" + k).strip("/") if path else k)
for f in glob.glob(os.path.join(TOK, "*.json")):
    if os.path.basename(f).startswith("_"):
        continue
    try:
        walk(json.load(open(f)))
    except Exception:
        pass
store_paths = sorted(store, key=len, reverse=True)  # longest first

# --- scan component metas for token usage ---
tok_to_comps = defaultdict(set)
comp_to_toks = defaultdict(set)
comp_depricate = {}   # component -> count of (depricate) refs in tokens block
metas = []
for f in sorted(glob.glob(os.path.join(COMP, "*.meta.json"))):
    b = os.path.basename(f)
    if b.startswith("EXAMPLE"):
        continue
    d = json.load(open(f))
    name = d.get("name", b)
    metas.append(name)
    blob = json.dumps(d.get("tokens", {})) + json.dumps(d.get("subComponents", {})) + json.dumps(d.get("variants", []))
    for p in store_paths:
        if re.search(r"(?<![\w/-])" + re.escape(p) + r"(?![\w/-])", blob):
            tok_to_comps[p].add(name)
            comp_to_toks[name].add(p)
    dep = len(re.findall(r"\(depricate\)", blob))
    if dep:
        comp_depricate[name] = dep

# --- blast-radius index ---
ranking = sorted(tok_to_comps.items(), key=lambda kv: (-len(kv[1]), kv[0]))
blast = {
    "$description": "Token blast-radius index — which components reference each live token (god-nodes = highest blast radius). Generated from component meta `tokens` blocks vs the token store. Use before changing/rebinding a token to see what's affected. Conformance: derived view, regenerate after meta/token edits.",
    "generated": "2026-06-18",
    "totals": {"tokens_defined": len(store), "tokens_referenced": len(tok_to_comps), "components": len(metas)},
    "ranking": [{"token": t, "blast": len(c), "components": sorted(c)} for t, c in ranking],
    "by_component": {c: sorted(list(s)) for c, s in sorted(comp_to_toks.items())},
}
json.dump(blast, open(os.path.join(TOK, "_blast-radius.json"), "w"), indent=2, ensure_ascii=False)

# --- token group coverage ---
def group(p):
    return p.split("/")[0]
grp_comps = defaultdict(set)
for t, cs in tok_to_comps.items():
    grp_comps[group(t)] |= cs
grp_rank = sorted(grp_comps.items(), key=lambda kv: -len(kv[1]))

# --- orphans: defined leaf tokens never referenced by any component ---
referenced = set(tok_to_comps)
orphans = sorted(set(store) - referenced)
orphan_groups = Counter(group(p) for p in orphans)

# --- compliance rollup (from graph-index if present) ---
gi_path = os.path.join(ROOT, "compliance", "graph-index.json")
comp_rules = ""
if os.path.exists(gi_path):
    gi = json.load(open(gi_path))
    comp_rules = f"{gi['totals']['rules']} rules x {gi['totals']['components']} components ({gi['totals']['sc']} SCs)"

# --- write report ---
top = ranking[:15]
L = []
L.append("# Knowledge graph — health report")
L.append("")
L.append("> Generated derived view over `knowledge/` (Graphify-inspired; no external dependency). Regenerate after editing component metas or tokens: `python3 knowledge/tokens/_build_blast_radius.py`. Authored canon stays the source of truth; this is a generated dashboard.")
L.append("")
L.append(f"**Totals:** {len(metas)} components · {len(store)} tokens defined · {len(tok_to_comps)} tokens referenced by components · compliance: {comp_rules or 'n/a'}.")
L.append("")
L.append("## God-nodes — highest token blast radius")
L.append("")
L.append("Change one of these and the listed number of components is affected. Use before any token rebind/rename (esp. the Sutherland migration).")
L.append("")
L.append("| Token | Blast | Example components |")
L.append("|---|---|---|")
for t, c in top:
    ex = ", ".join(sorted(c)[:6]) + ("…" if len(c) > 6 else "")
    L.append(f"| `{t}` | {len(c)} | {ex} |")
L.append("")
L.append("## Token-group reach (components using each group)")
L.append("")
L.append("| Group | Components |")
L.append("|---|---|")
for g, c in grp_rank:
    L.append(f"| `{g}/` | {len(c)} |")
L.append("")
L.append("## Deprecated tokens still bound (migration worklist)")
L.append("")
if comp_depricate:
    L.append("Components whose `tokens` block still references a `(depricate)` token (count = mentions). See `tokens/_manifests/depricate-replacement-map.json` `$usage_audit` for the rebind targets and `_DESIGN-SYSTEM-GAPS.md` for blockers.")
    L.append("")
    L.append("| Component | (depricate) refs |")
    L.append("|---|---|")
    for c, n in sorted(comp_depricate.items(), key=lambda kv: -kv[1]):
        L.append(f"| {c} | {n} |")
else:
    L.append("None — all components migrated off deprecated tokens. 🎉")
L.append("")
L.append("## Orphans — defined tokens not referenced by any component meta")
L.append("")
L.append(f"{len(orphans)} of {len(store)} defined tokens are unreferenced at the component layer. **Expected** for primitives and scale steps (consumed via semantic aliases, not bound directly); worth scanning the *semantic* groups for genuinely-dead tokens. By group:")
L.append("")
L.append("| Group | Unreferenced |")
L.append("|---|---|")
for g, n in orphan_groups.most_common():
    L.append(f"| `{g}/` | {n} |")
L.append("")
L.append("> Method: token usage matched by scanning each meta's `tokens`/`subComponents`/`variants` blocks for exact store token paths (word-boundary safe). Misses any token referenced only in prose elsewhere; treat blast counts as a strong lower bound.")
L.append("")
open(os.path.join(ROOT, "_GRAPH-REPORT.md"), "w").write("\n".join(L))

print("wrote tokens/_blast-radius.json and _GRAPH-REPORT.md")
print(f"tokens defined={len(store)} referenced={len(tok_to_comps)} components={len(metas)}")
print("top god-nodes:", [(t, len(c)) for t, c in top[:8]])
print("depricate-still-bound components:", len(comp_depricate))
print("orphans:", len(orphans))
