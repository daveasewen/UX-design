#!/usr/bin/env python3
"""Query harness over the knowledge base — one entry point for multi-hop lookups.

Reads only the generated indexes (run _build_all.py first) and joins them so a
human or agent can ask the questions the graph was built to answer.

Usage:
  python3 knowledge/query.py "Tabs"          # full hub for a component
  python3 knowledge/query.py --token text/default   # components binding a token (blast)
  python3 knowledge/query.py --sc 2.4.11     # components owing an SC + the rule
  python3 knowledge/query.py --leaks         # dark-mode primitive leaks
  python3 knowledge/query.py --list          # list components
"""
import json, os, sys, argparse

ROOT = os.path.dirname(os.path.abspath(__file__))

def load(rel):
    p = os.path.join(ROOT, rel)
    return json.load(open(p)) if os.path.exists(p) else None

XREF = load("_XREF-INDEX.json") or {}
BLAST = load("tokens/_blast-radius.json") or {}
COMPL = load("compliance/graph-index.json") or {}
REVIEW = load("_REVIEW-QUEUE.json") or {}
DARK = load("_DARK-MODE-AUDIT.json") or {}

def need(idx, name):
    if not idx:
        sys.exit("missing generated index — run: python3 knowledge/_build_all.py")
    return idx

def rule_for(sc):
    f = os.path.join(ROOT, "compliance", "rules")
    for fn in os.listdir(f):
        if fn.startswith(f"wcag-{sc}-"):
            return json.load(open(os.path.join(f, fn)))
    return None

def resolve_name(q):
    comps = need(XREF, "xref").get("components", {})
    if q in comps:
        return q
    low = {k.lower(): k for k in comps}
    if q.lower() in low:
        return low[q.lower()]
    hits = [k for k in comps if q.lower() in k.lower()]
    if len(hits) == 1:
        return hits[0]
    if hits:
        sys.exit(f"ambiguous: {q!r} matches {hits}")
    sys.exit(f"unknown component {q!r}. --list to see all.")

def show_component(q):
    name = resolve_name(q)
    h = XREF["components"][name]
    dark = (DARK.get("components", {}) or {}).get(name, {})
    revs = [i for i in REVIEW.get("items", []) if i["component"] == name]
    print(f"\n=== {name} ({h.get('category')}) ===")
    print(f"figma: {h.get('figma_node')}")
    print(f"\nWCAG SCs ({len(h['wcag_sc'])}):")
    for sc in h["wcag_sc"]:
        r = rule_for(sc)
        if r:
            print(f"  {sc:8} {r['title']} [{r['level']}/{r['severity']}]")
        else:
            print(f"  {sc}")
    print(f"\nGuidelines ({len(h['guidelines'])}): " + ", ".join(g.replace('.md','') for g in h['guidelines']))
    print(f"\nTokens ({h['token_count']}) — god-nodes touched: " + (", ".join(h['god_nodes_touched']) or "none"))
    # blast coupling: other components sharing a god-node
    coupled = {}
    rank = {r["token"]: r["components"] for r in BLAST.get("ranking", [])}
    for g in h["god_nodes_touched"]:
        for c in rank.get(g, []):
            if c != name:
                coupled.setdefault(c, []).append(g)
    if coupled:
        top = sorted(coupled.items(), key=lambda kv: -len(kv[1]))[:6]
        print("  migration-coupled with: " + ", ".join(f"{c} ({len(g)})" for c, g in top))
    dm = dark.get("status")
    print(f"\nDark mode: {'🔴 LEAK — ' + ', '.join(dark.get('leaks', [])) if dm == 'LEAK' else '✅ clean' if dm else 'n/a'}")
    print(f"\nAnti-patterns ({len(h['anti_patterns']['asserted'])} asserted, {len(h['anti_patterns']['inferred_review'])} review):")
    for a in h["anti_patterns"]["asserted"]:
        print(f"  • {a}")
    for a in h["anti_patterns"]["inferred_review"]:
        print(f"  🔴 {a}")
    if h["deprecated_bindings"]:
        print(f"\nDeprecated bindings ({len(h['deprecated_bindings'])}):")
        for d in h["deprecated_bindings"]:
            print(f"  • {d['token']}  →  {d.get('rebind') or '(no target — REVIEW)'}")
    if revs:
        print(f"\nReview queue ({len(revs)}):")
        for r in revs:
            print(f"  {'🔴' if r['tier']=='review' else '🟡'} [{r['category']}] {r['field']}: {r['text'][:100]}")
    print()

def show_token(tok):
    rank = {r["token"]: r for r in need(BLAST, "blast").get("ranking", [])}
    r = rank.get(tok)
    if not r:
        sys.exit(f"token {tok!r} not referenced by any component (or not in store). See tokens/_blast-radius.json.")
    print(f"\n=== {tok} — blast {r['blast']} ===")
    for c in r["components"]:
        print(f"  • {c}")
    print()

def show_sc(sc):
    comps = need(COMPL, "compliance").get("by_sc", {}).get(sc)
    if not comps:
        sys.exit(f"SC {sc!r} not in the compliance graph. See compliance/graph-index.json by_sc.")
    r = rule_for(sc)
    if r:
        print(f"\n=== {sc} {r['title']} [{r['level']}/{r['severity']}] ===")
        print(f"check ({r['check']['type']}): {r['check']['description']}")
        if r['check'].get('threshold'):
            print(f"threshold: {r['check']['threshold']}")
        print(f"source: {r['sources']['wcag_url']}")
    print(f"\nApplies to ({len(comps)}):")
    for c in comps:
        print(f"  • {c}")
    print()

def show_leaks():
    d = need(DARK, "dark-mode")
    t = d["totals"]
    print(f"\n=== dark-mode leaks — {t['clean']}/{t['components']} clean ===")
    for tok, comps in d.get("leak_index", {}).items():
        print(f"  {tok}: {', '.join(comps)}")
    print()

def main():
    ap = argparse.ArgumentParser(description="Query the Apollo knowledge base.")
    ap.add_argument("component", nargs="?", help="component name (partial ok)")
    ap.add_argument("--token", help="show components binding a token")
    ap.add_argument("--sc", help="show components owing a WCAG SC + the rule")
    ap.add_argument("--leaks", action="store_true", help="dark-mode primitive leaks")
    ap.add_argument("--list", action="store_true", help="list components")
    a = ap.parse_args()
    if a.list:
        for c in sorted(need(XREF, "xref").get("components", {})):
            print(c)
    elif a.token:
        show_token(a.token)
    elif a.sc:
        show_sc(a.sc)
    elif a.leaks:
        show_leaks()
    elif a.component:
        show_component(a.component)
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
