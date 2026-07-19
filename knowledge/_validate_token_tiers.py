#!/usr/bin/env python3
"""Token-tier gate — enforces the three-tier stack (_STANDARDS.md §1).

Primitive (color/*) -> Semantic (intent) -> Component (component-scoped). The `$alias` per mode is the
source of truth; the `$value` is a build-resolved cache. This gate enforces:

  1. CONSISTENCY (all aliased tokens): $value == resolve($alias) along the chain, per mode. A drifted
     cache is a defect. STRICT for the migrated three-tier set; ADVISORY (report only) for the rest of
     the store until it migrates (so legacy two-tier tokens don't block the build prematurely).
  2. TIER DISCIPLINE (migrated set): a component-tier token references a SEMANTIC token, never a
     primitive; a semantic-tier token references a PRIMITIVE. This is the "components never touch
     primitives" rule (Dave, 2026-07-19).

The migrated set grows as tokens move onto proper tiers; add them to MIGRATED below. Writes
_TOKEN-TIER-AUDIT.md. Exits non-zero on any STRICT failure.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
COL = json.load(open(os.path.join(ROOT, "tokens", "colour.json")))
SEM = json.load(open(os.path.join(ROOT, "tokens", "semantic-colour.json")))

# --- the three-tier migrated set (STRICT). Grow this as the store migrates. ---
SEMANTIC_ELEVATION = ["surface/raised", "surface/subtle", "surface/raised-hover"]
COMPONENTS_ON_SEMANTIC = {
    "tertiary/background/default": "surface/raised",
    "tertiary/background/hover": "surface/raised-hover",
    "tabs/background": "surface/raised",
    "tabs/overflow-background": "surface/raised",
    "tabs/hover": "surface/raised-hover",
    "table/header/background": "surface/subtle",
    "table/column/background": "surface/subtle",
    "scrollbar/background": "surface/subtle",
    "form/background/hover": "surface/raised-hover",
}
MIGRATED = set(SEMANTIC_ELEVATION) | set(COMPONENTS_ON_SEMANTIC)


def node_at(path):
    store = COL if path.startswith("color/") else SEM
    n = store
    for k in path.split("/"):
        if not isinstance(n, dict) or k not in n:
            return None
        n = n[k]
    return n


def resolve(path, mode):
    """Follow $alias chain / mode leaves to a final hex. None if unresolvable."""
    seen = set()
    while True:
        if path in seen:
            return None                      # cycle
        seen.add(path)
        n = node_at(path)
        if n is None:
            return None
        # primitive leaf (no mode)
        if "$value" in n and "light" not in n and "dark" not in n:
            return str(n["$value"]).upper()
        # mode token: prefer following the alias (source of truth), else the cached value
        al = n.get("$alias") if isinstance(n.get("$alias"), dict) else {}
        if al.get(mode):
            path = al[mode]
            continue
        m = n.get(mode)
        if isinstance(m, dict) and "$value" in m:
            return str(m["$value"]).upper()
        return None


def is_aliased(n):
    return isinstance(n, dict) and isinstance(n.get("$alias"), dict) and ("light" in n or "dark" in n)


def walk(node, path, hits):
    if not isinstance(node, dict):
        return
    if is_aliased(node):
        hits.append(("/".join(path), node))
        return
    for k, v in node.items():
        if not k.startswith("$"):
            walk(v, path + [k], hits)


strict_fail, advisory = [], []
hits = []
walk(SEM, [], hits)

for path, n in hits:
    al = n["$alias"]
    strict = path in MIGRATED
    # 1. consistency
    for mode in ("light", "dark"):
        if not (isinstance(n.get(mode), dict) and "$value" in n[mode]) or not al.get(mode):
            continue
        want = resolve(al[mode], mode)
        got = str(n[mode]["$value"]).upper()
        if want is None:
            (strict_fail if strict else advisory).append(f"{path} ({mode}): alias '{al[mode]}' does not resolve")
        elif want != got:
            (strict_fail if strict else advisory).append(f"{path} ({mode}): $value {got} != resolve({al[mode]}) {want}")
    # 2. tier discipline (migrated only)
    if strict:
        for mode in ("light", "dark"):
            tgt = al.get(mode)
            if not tgt:
                continue
            if path in COMPONENTS_ON_SEMANTIC:
                if tgt.startswith("color/"):
                    strict_fail.append(f"{path} ({mode}): component references a PRIMITIVE '{tgt}' — must reference a semantic token")
                elif tgt != COMPONENTS_ON_SEMANTIC[path]:
                    strict_fail.append(f"{path} ({mode}): expected semantic '{COMPONENTS_ON_SEMANTIC[path]}', found '{tgt}'")
            elif path in SEMANTIC_ELEVATION and not tgt.startswith("color/"):
                strict_fail.append(f"{path} ({mode}): semantic token must reference a PRIMITIVE, found '{tgt}'")

# primitives exist
for p in ("color/mono/raise-1", "color/mono/raise-2", "color/mono/raise-3"):
    if node_at(p) is None:
        strict_fail.append(f"missing elevation primitive {p}")

lines = ["# Token-tier gate (_STANDARDS.md §1)", "",
         f"**Result:** {len(strict_fail)} strict failure(s) · {len(advisory)} advisory (legacy, not gated).",
         f"Migrated three-tier set: {len(MIGRATED)} token(s).", ""]
if strict_fail:
    lines += ["## ❌ STRICT failures (block the build)", ""] + [f"- {x}" for x in strict_fail] + [""]
if advisory:
    lines += ["## Advisory — legacy tokens (consistency, not yet gated)", ""] + [f"- {x}" for x in advisory[:60]] + [""]
open(os.path.join(ROOT, "_TOKEN-TIER-AUDIT.md"), "w").write("\n".join(lines))

print(f"token-tier gate: {len(strict_fail)} strict failure(s), {len(advisory)} advisory.")
for x in strict_fail:
    print(f"  ❌ {x}")
sys.exit(1 if strict_fail else 0)
