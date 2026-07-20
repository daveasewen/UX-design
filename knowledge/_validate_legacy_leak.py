#!/usr/bin/env python3
"""Legacy-colour leakage gate — Apollo Mono surfaces may not resolve to a Legacy-only colour.

WHY THIS EXISTS (Dave, 2026-07-20): the Mono "Done" success button was rendering the Legacy
teal #00847F because it bound `rag/success`, whose primitive `color/green/600` literally holds
the teal. Dave: "how do we stop this leakage so we don't have to keep fixing such errors." This
is the gate-don't-patch answer: a build-blocking check so a Legacy-only colour landing in a Mono
component fails the build the moment it happens, instead of being hand-found later.

WHAT IT CHECKS: every token-manifest binding in a reference snippet (the Mono canon surface) is
resolved in BOTH modes; if a resolved hex is in LEGACY_ONLY_HEXES it's a leak. Known, un-fixable-
yet leaks are WAIVED with provenance (see WAIVERS) so the gate is honest — it blocks NEW leaks and
keeps the existing debt visible, rather than going red on debt we've already accounted for.

ANTI-FALSE-FIX PROVENANCE: the fix for a real leak is to rebind the Mono component onto the R-D14
token (rag/*-background / -glyph), NOT to add the leaking hex to LEGACY_ONLY exceptions and NOT to
delete the binding. A waiver is only legitimate when the correct R-D14 token does not yet exist in
both modes (see the success-glyph dark gap). Registry grows as each Legacy colour is ruled.
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(ROOT, "snippets")
TOK = os.path.join(ROOT, "tokens")

# ── Legacy-only colours: belong to Apollo Legacy alone; must never resolve inside a Mono surface.
#    Seeded with the RULED one (the success teal, Dave 2026-07-20 → R-D15: teal is Legacy's alone).
#    Add a hex here only once its Mono replacement is ruled AND present in both modes, so fixing the
#    leak is possible rather than just flagged. (error HSBC-red, warning #FFBB33, info navy are
#    identically drifted on their bare rag/* roles — pending their own rulings + R-D14 completion.)
LEGACY_ONLY_HEXES = {
    "#00847F": "Legacy success/status teal (R-D15: teal is Apollo Legacy's alone; Mono uses R-D14 green)",
}

# ── Waivers: (snippet_basename, css_var) → reason. Legitimate ONLY while the correct R-D14 token is
#    incomplete (a clean rebind is impossible until the replacement exists in both modes). Add one here
#    only with that justification; remove it the moment the component is rebound. NONE currently: the
#    success green set was completed (R-D18, Dave 2026-07-20), the bare rag/success role + tint rebased
#    off the teal, so the seven previously-waived components now resolve green with no edit needed.
WAIVERS = {}

_stores = [json.load(open(os.path.join(TOK, f))) for f in ("colour.json", "semantic-colour.json")]


def _node(path):
    for d in _stores:
        o = d
        ok = True
        for k in path.split("/"):
            if isinstance(o, dict) and k in o:
                o = o[k]
            else:
                ok = False
                break
        if ok and isinstance(o, dict):
            return o
    return None


def resolve(path, mode):
    n = _node(path)
    if n is None:
        return None
    # aliased token
    if "$alias" in n and "$value" not in n and mode not in n:
        a = n["$alias"]
        a = a.get(mode) if isinstance(a, dict) else a
        return resolve(a, mode)
    # flat $value (may be a scalar or a light/dark dict)
    if n.get("$value") is not None:
        v = n["$value"]
        return (v.get(mode) if isinstance(v, dict) else v)
    # nested light/dark value nodes
    if mode in n and isinstance(n[mode], dict) and "$value" in n[mode]:
        return n[mode]["$value"]
    # fall back through an alias if present
    if "$alias" in n:
        a = n["$alias"]
        a = a.get(mode) if isinstance(a, dict) else a
        return resolve(a, mode)
    return None


def main():
    leaks, waived = [], []
    for path in sorted(glob.glob(os.path.join(SNIP, "*.html"))):
        name = os.path.basename(path)
        html = open(path, encoding="utf-8").read()
        mm = re.search(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', html, re.S)
        if not mm:
            continue
        try:
            manifest = json.loads(mm.group(1))
        except json.JSONDecodeError:
            continue
        for var, token in manifest.get("vars", {}).items():
            for mode in ("light", "dark"):
                hexv = resolve(token, mode)
                if hexv and hexv.upper() in LEGACY_ONLY_HEXES:
                    reason = LEGACY_ONLY_HEXES[hexv.upper()]
                    if (name, var) in WAIVERS:
                        waived.append((name, var, token, mode, hexv, WAIVERS[(name, var)]))
                    else:
                        leaks.append((name, var, token, mode, hexv, reason))

    # audit report
    lines = ["# Legacy-colour leakage gate\n",
             f"**Registry:** {len(LEGACY_ONLY_HEXES)} Legacy-only hex(es) · "
             f"{len(leaks)} unwaived leak(s) · {len(waived)} waived (known debt).\n"]
    if leaks:
        lines.append("\n## ❌ Unwaived leaks (block the build)\n")
        for n_, v, t, m, h, r in leaks:
            lines.append(f"- {n_}: `{v}` → `{t}` resolves to **{h}** ({m}) — {r}\n")
    if waived:
        lines.append("\n## ⚠ Waived — known debt (rebind when the R-D14 token lands)\n")
        for n_, v, t, m, h, r in waived:
            lines.append(f"- {n_}: `{v}` → `{t}` = {h} ({m}) — WAIVED: {r}\n")
    open(os.path.join(ROOT, "_LEGACY-LEAK-GATE.md"), "w", encoding="utf-8").writelines(lines)

    print(f"legacy-leak gate: {len(leaks)} unwaived leak(s), {len(waived)} waived.")
    for n_, v, t, m, h, r in leaks:
        print(f"  ❌ {n_}: {v} -> {t} = {h} ({m})")
    if leaks:
        sys.exit(1)


if __name__ == "__main__":
    main()
