#!/usr/bin/env python3
"""Dark-mode coverage audit — which components theme correctly in dark mode.

The store splits colour into two kinds:
  - semantic tokens (semantic-colour.json) carry BOTH a `light` and a `dark` value
    -> binding these is dark-mode-safe.
  - primitives (colour.json: color/*, grey/*, etc.) are single-valued, no modes
    -> binding one DIRECTLY in a component leaks: it cannot re-theme in dark mode.
    This is exactly the P3 finding (Tabs selected-indicator bound to color/primary
    instead of a semantic tabs/* token).

This audit classifies every colour token each component binds (from the blast-radius
reverse index) and reports:
  - LEAK   : component binds a raw primitive directly (real defect — fix before dark mode)
  - flat   : component binds a semantic token whose dark == light (often intentional —
             reverse text, RAG status, brand red — but listed for a human to confirm)
  - clean  : all colour bindings are dark-adapted semantics

Writes knowledge/_DARK-MODE-AUDIT.json + _DARK-MODE-AUDIT.md.
Depends on tokens/_blast-radius.json (run _build_blast_radius.py first; _build_all.py
does this in order). Regenerate: python3 knowledge/_build_dark_mode_audit.py
"""
import json, os, glob
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.join(ROOT, "tokens")
COMP = os.path.join(ROOT, "components")

def leaves(node, path="", out=None):
    if out is None: out = {}
    if isinstance(node, dict):
        if any(k in node for k in ("$value", "light", "dark", "scale-1")):
            out[path] = node; return out
        for k, v in node.items():
            if k.startswith("$"): continue
            leaves(v, (path + "/" + k).strip("/") if path else k, out)
    return out

def mode_val(n, m):
    x = n.get(m)
    return (x.get("$value") or x.get("value")) if isinstance(x, dict) else x

sem = leaves(json.load(open(os.path.join(TOK, "semantic-colour.json"))))
prim = set(leaves(json.load(open(os.path.join(TOK, "colour.json")))))
semantic = set(sem)
flat = {p for p, n in sem.items() if "light" in n and "dark" in n and mode_val(n, "light") == mode_val(n, "dark")}
colour_tokens = prim | semantic  # everything colour-ish; used to ignore non-colour tokens

blast = json.load(open(os.path.join(TOK, "_blast-radius.json")))
by_comp = blast["by_component"]

# self-declared primitive bindings (corroboration)
selfflag = {}
for f in glob.glob(os.path.join(COMP, "*.meta.json")):
    b = os.path.basename(f)
    if b.startswith("EXAMPLE") or b == "meta.schema.json": continue
    d = json.load(open(f))
    tv = d.get("tokenValidation")
    if isinstance(tv, dict) and ("primitiveBinding" in tv or "newTokenSeen" in tv):
        selfflag[d.get("name")] = tv.get("primitiveBinding") or tv.get("newTokenSeen")

rows = {}
leak_to_comps = defaultdict(list)
for name, toks in by_comp.items():
    bound_colour = [t for t in toks if t in colour_tokens]
    leaks = sorted(t for t in bound_colour if t in prim and t not in semantic)
    flats = sorted(t for t in bound_colour if t in flat)
    for t in leaks:
        leak_to_comps[t].append(name)
    rows[name] = {
        "status": "LEAK" if leaks else "clean",
        "leaks": leaks, "flat_semantics": flats,
        "colour_token_count": len(bound_colour),
        "self_flagged": selfflag.get(name),
    }

clean = [n for n, r in rows.items() if r["status"] == "clean"]
leaking = sorted([n for n, r in rows.items() if r["status"] == "LEAK"])

audit = {
    "$description": "Dark-mode coverage audit. LEAK = component binds a raw colour primitive directly (no dark value -> cannot re-theme). flat_semantics = semantic tokens whose dark==light (often intentional, listed for confirmation). Derived from tokens/_blast-radius.json + the colour stores. Regenerate via _build_dark_mode_audit.py.",
    "generated": "2026-06-18",
    "totals": {
        "components": len(rows), "clean": len(clean), "leaking": len(leaking),
        "semantic_colour_tokens": len(semantic), "flat_semantics": len(flat), "primitives": len(prim),
    },
    "leak_index": {t: sorted(c) for t, c in sorted(leak_to_comps.items(), key=lambda kv: -len(kv[1]))},
    "components": dict(sorted(rows.items())),
}
json.dump(audit, open(os.path.join(ROOT, "_DARK-MODE-AUDIT.json"), "w"), indent=2, ensure_ascii=False)

L = ["# Dark-mode coverage audit", "",
     "> Which components re-theme correctly in dark mode. **LEAK** = binds a raw colour *primitive* directly (single-valued, no dark variant — a real defect; the P3 family). *flat* = binds a semantic token whose dark value equals its light value (frequently intentional — reverse text, RAG, brand red — confirm per case). Derived view over the colour stores + blast-radius; regenerate: `python3 knowledge/_build_dark_mode_audit.py`. Detail in `_DARK-MODE-AUDIT.json`.", ""]
L.append(f"**Coverage:** {len(clean)}/{len(rows)} components clean · {len(leaking)} leak a primitive. "
         f"Store: {len(semantic)} semantic colour tokens (light+dark), {len(flat)} flat (dark==light), {len(prim)} primitives.")
L.append("")
L.append("## Primitive leaks — fix before dark mode")
L.append("")
L.append("Each raw primitive bound directly, and the components binding it. Rebind to a semantic token that carries a dark value (see `_DESIGN-SYSTEM-GAPS.md` / `_REVIEW-QUEUE.md` token-rebind section).")
L.append("")
if leak_to_comps:
    L.append("| Primitive | Components | Note |")
    L.append("|---|---|---|")
    notes = {"color/primary": "brand red #db0011 — for Tabs the indicator should be a semantic tabs/active (P3); for links/badges confirm dark-mode brand red"}
    for t, comps in sorted(leak_to_comps.items(), key=lambda kv: -len(kv[1])):
        L.append(f"| `{t}` | {', '.join(sorted(comps))} | {notes.get(t,'')} |")
else:
    L.append("_No primitive leaks._")
L.append("")
L.append("## Per-component")
L.append("")
L.append("| Component | Status | Primitive leaks | Flat semantics (confirm) |")
L.append("|---|---|---|---|")
for name in sorted(rows):
    r = rows[name]
    badge = "🔴 LEAK" if r["status"] == "LEAK" else "✅ clean"
    flats = ", ".join(f"`{t}`" for t in r["flat_semantics"][:5]) + ("…" if len(r["flat_semantics"]) > 5 else "")
    leaks = ", ".join(f"`{t}`" for t in r["leaks"]) or "—"
    L.append(f"| {name} | {badge} | {leaks} | {flats or '—'} |")
L.append("")
L.append("> *flat* tokens are not necessarily wrong — `icon/default-reverse`, `text/reverse`, `rag/*` and brand reds are designed to read the same on their fixed surfaces in both modes. They're listed so a reviewer can confirm none is an unthemed surface that *should* darken (e.g. check `tertiary/background/*`).")
L.append("")
open(os.path.join(ROOT, "_DARK-MODE-AUDIT.md"), "w").write("\n".join(L))

print(f"dark-mode audit: {len(clean)}/{len(rows)} clean, {len(leaking)} leaking")
print("leaks by primitive:", {t: len(c) for t, c in sorted(leak_to_comps.items(), key=lambda kv: -len(kv[1]))})
print("leaking components:", leaking)