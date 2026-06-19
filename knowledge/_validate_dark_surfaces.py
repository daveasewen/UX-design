#!/usr/bin/env python3
"""Dark surface/border flatness gate.

Closes the coverage gap the text/icon + indicator contrast audits left: those
check FOREGROUND tokens, not the surfaces and borders themselves. This catches
the defect class we hit on form/* and the 24-token sweep — a surface, background,
border, or divider token that resolves to a flat #FFFFFF in dark mode (it lost
its theming and renders as a white block, hiding content).

Policy:
  - FAIL on any background/surface/border/divider token whose dark value is
    #FFFFFF while its light value isn't (the defect).
  - EXEMPT tokens that carry a `$darkNote` annotation (intentional inversions,
    e.g. a secondary button that inverts to white on dark) — the annotation is
    the explicit, reviewable allowlist.
  - SKIP `*/on-light` (light-context only) and `*reverse` tokens.

Gates the build (exits non-zero on any failure). Writes _DARK-SURFACE-AUDIT.md.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sem = json.load(open(os.path.join(ROOT, "tokens", "semantic-colour.json")))

CATS = ("background", "surface", "border", "divider")
fails, allowed = [], []


def mval(node, mode):
    m = node.get(mode)
    return m.get("$value") if isinstance(m, dict) else m


def walk(node, p=""):
    if not isinstance(node, dict):
        return
    if "light" in node and "dark" in node and isinstance(node.get("light"), dict):
        name = p.strip("/")
        if any(c in name for c in CATS) and "reverse" not in name and "on-light" not in name:
            l, dk = mval(node, "light"), mval(node, "dark")
            if isinstance(dk, str) and dk.upper() == "#FFFFFF" and isinstance(l, str) and l.upper() != "#FFFFFF":
                if node.get("$darkNote"):
                    allowed.append((name, node["$darkNote"]))
                else:
                    fails.append((name, l))
    for k, v in node.items():
        if not k.startswith("$"):
            walk(v, p + "/" + k)


walk(sem)

lines = ["# Dark surface/border flatness gate", "",
         "> Surface/background/border/divider tokens must not resolve to a flat `#FFFFFF` in dark "
         "(a white block hiding content). Intentional inversions are exempt via a `$darkNote` annotation.",
         "",
         f"**Result:** {len(fails)} failure(s) · {len(allowed)} annotated exception(s).", ""]
if fails:
    lines += ["## ❌ Flat-white in dark — these FAIL the build", "", "| Token | Light value |", "|---|---|"]
    lines += [f"| `{n}` | `{l}` |" for n, l in fails]
    lines.append("")
if allowed:
    lines += ["## Annotated intentional inversions (allowed)", "", "| Token | Why |", "|---|---|"]
    lines += [f"| `{n}` | {note} |" for n, note in allowed]
    lines.append("")
open(os.path.join(ROOT, "_DARK-SURFACE-AUDIT.md"), "w").write("\n".join(lines))

print(f"dark-surface gate: {len(fails)} flat-white failure(s), {len(allowed)} annotated exception(s)")
for n, l in fails:
    print(f"  ❌ {n}: dark=#FFFFFF (light={l}) — add a dark value or a $darkNote if intentional")
sys.exit(1 if fails else 0)
