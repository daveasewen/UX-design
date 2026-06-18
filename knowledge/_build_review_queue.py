#!/usr/bin/env python3
"""Confidence enum + review queue (Graphify-borrow #1).

Formalises the confidence vocabulary already used in prose across the metas into a
gradeable, discoverable surface — without mass-editing 32 files.

Confidence tiers (mirrors Graphify EXTRACTED / INFERRED / AMBIGUOUS):
  asserted  — observed directly from Figma or an authoritative doc. Default; NOT queued.
  inferred  — reasoned from context; stated as fact but not directly observed.
  review    — inferred AND flagged for human verification before treated as canon
              (authored marker: a string containing the token "REVIEW").

Classification (read from the authored strings, not re-inferred):
  contains "REVIEW"                         -> review
  else contains inferred|assumed|likely|tbc -> inferred
  else                                      -> asserted (not collected)

Categories (by JSON field path, so the queue can be filtered):
  anti-pattern | token-rebind | accessibility | other

Writes:
  - knowledge/_REVIEW-QUEUE.json  (machine: every non-asserted assertion w/ component, field, tier, category, text)
  - knowledge/_REVIEW-QUEUE.md    (human: worklist grouped by category, then component)
Regenerate after editing metas:  python3 knowledge/_build_review_queue.py
"""
import json, os, glob, re
from collections import Counter, defaultdict

ROOT = "/sessions/eloquent-cool-fermat/mnt/UX-design/knowledge"
COMP = os.path.join(ROOT, "components")

REVIEW_RE = re.compile(r"\bREVIEW\b")
INFER_RE = re.compile(r"\b(inferred|assumed|likely|presumably|tbc|to confirm)\b", re.I)

def tier(s):
    if REVIEW_RE.search(s):
        return "review"
    if INFER_RE.search(s):
        return "inferred"
    return "asserted"

def category(path):
    if "antiPatterns" in path:
        return "anti-pattern"
    if "rebind" in path or "blocker" in path or "depricateUsage" in path:
        return "token-rebind"
    if path.startswith("accessibility"):
        return "accessibility"
    return "other"

items = []
def walk(node, path, name, figma):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, (path + "." + k) if path else k, name, figma)
    elif isinstance(node, list):
        for v in node:
            walk(v, path, name, figma)
    elif isinstance(node, str):
        t = tier(node)
        if t != "asserted":
            items.append({
                "component": name, "field": path, "tier": t,
                "category": category(path), "text": node.strip(),
                "figma_node": figma,
            })

for f in sorted(glob.glob(os.path.join(COMP, "*.meta.json"))):
    b = os.path.basename(f)
    if b.startswith("EXAMPLE") or b == "meta.schema.json":
        continue
    d = json.load(open(f))
    walk(d, "", d.get("name", b), (d.get("provenance") or {}).get("figma_node"))

# --- rollups ---
by_tier = Counter(i["tier"] for i in items)
by_cat = Counter(i["category"] for i in items)
by_comp = Counter(i["component"] for i in items)
review_rebinds = [i for i in items if i["tier"] == "review" and i["category"] == "token-rebind"]

index = {
    "$description": "Review queue — every non-asserted assertion in the component metas, classified by confidence tier (review|inferred) and category. Formalises the in-prose 'REVIEW (inferred)' convention (Graphify-borrow #1). 'review' = human must verify before treating as canon; 'inferred' = reasoned, lower urgency. Derived view; regenerate via _build_review_queue.py after editing metas. See _CONFIDENCE.md for the vocabulary.",
    "generated": "2026-06-18",
    "tiers": {"asserted": "observed directly from Figma/authoritative doc (default, not listed)", "inferred": "reasoned from context, stated as fact but not observed", "review": "inferred AND flagged for human verification before canon"},
    "totals": {"items": len(items), "by_tier": dict(by_tier), "by_category": dict(by_cat),
               "components_with_items": len(by_comp), "review_token_rebinds": len(review_rebinds)},
    "items": items,
}
json.dump(index, open(os.path.join(ROOT, "_REVIEW-QUEUE.json"), "w"), indent=2, ensure_ascii=False)

# --- human worklist ---
def block(title, rows, note=None):
    L = [f"## {title} ({len(rows)})", ""]
    if note:
        L += [note, ""]
    if not rows:
        L += ["_None._", ""]
        return L
    by_c = defaultdict(list)
    for r in rows:
        by_c[r["component"]].append(r)
    for c in sorted(by_c):
        L.append(f"**{c}**")
        for r in by_c[c]:
            tag = "🔴" if r["tier"] == "review" else "🟡"
            txt = r["text"] if len(r["text"]) <= 240 else r["text"][:237] + "…"
            L.append(f"- {tag} `{r['field']}` — {txt}")
        L.append("")
    return L

L = []
L.append("# Review queue — confidence-tagged assertions")
L.append("")
L.append("> Every assertion in the component metas that is **not** directly observed canon. Formalises the in-prose confidence convention (Graphify-borrow #1). 🔴 **review** = verify before trusting; 🟡 **inferred** = reasoned, lower urgency. `asserted` items (the default) are not listed. Generated — regenerate after editing metas: `python3 knowledge/_build_review_queue.py`. Vocabulary in `_CONFIDENCE.md`; machine detail in `_REVIEW-QUEUE.json`.")
L.append("")
L.append(f"**Totals:** {len(items)} items across {len(by_comp)} components — "
         f"{by_tier.get('review',0)} 🔴 review, {by_tier.get('inferred',0)} 🟡 inferred. "
         f"By category: " + ", ".join(f"{k} {v}" for k, v in by_cat.most_common()) + ".")
L.append("")
L.append("Most-flagged components: " + ", ".join(f"{c} ({n})" for c, n in by_comp.most_common(8)) + ".")
L.append("")
L += block("Token-rebind — verify before the Sutherland migration", [i for i in items if i["category"] == "token-rebind"],
           "These gate the deprecated-token rebind: each names a best-guess replacement that must be confirmed against the real Sutherland values. Cross-ref `tokens/_manifests/depricate-replacement-map.json` and `_blast-radius.json`.")
L += block("Accessibility — verify in code/with the a11y team", [i for i in items if i["category"] == "accessibility"])
L += block("Anti-patterns — confirm or promote to asserted", [i for i in items if i["category"] == "anti-pattern"])
L += block("Other", [i for i in items if i["category"] == "other"])
open(os.path.join(ROOT, "_REVIEW-QUEUE.md"), "w").write("\n".join(L))

print(f"wrote _REVIEW-QUEUE.json + .md — {len(items)} items")
print("by tier:", dict(by_tier))
print("by category:", dict(by_cat))
print("review token-rebinds (migration-gating):", len(review_rebinds))
print("top components:", by_comp.most_common(6))