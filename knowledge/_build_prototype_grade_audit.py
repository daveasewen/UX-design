#!/usr/bin/env python3
"""
_build_prototype_grade_audit.py — advisory (non-gating) scorer.

Scores each reference snippet against the prototype-grade rubric (the "Tabs-bar
standard" — see _RUBRIC-prototype-grade.md) using measurable signals in the HTML.
Output: _PROTOTYPE-GRADE-AUDIT.md, ranked ascending (lowest = most work), with a
★ PRIORITY flag for the payments-journey components. Does NOT gate the build.
Dims 7 (geometry) & 9 (edge states) are manual and not auto-scored.
"""
import os, re, glob, json

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")
COMP = os.path.join(HERE, "components")

PRIORITY = {  # components the payments-journey demo needs first
    "Cards", "List-items", "Table", "Button", "Input-fields", "Status-indicator",
    "Notifications", "Modals", "Tags", "Links", "Progress-tracker", "Selection-controls",
}

ROUND_EXEMPT = {"Badge", "Avatar"}  # the ONLY two components allowed round corners (brand convention)

DIMS = ["token-faithful", "dual-theme", "states", "focus-visible",
        "reduced-motion", "AT(aria+kbd)", "behaviour", "square-corners", "responsive"]

def score(name, s, interactive=True):
    d = {}
    d["token-faithful"] = 1 if "token-manifest" in s else 0
    d["dual-theme"]     = 1 if 'data-theme="dark"' in s else 0
    states = sum(1 for pat in [r":hover", r":active", r":focus-visible",
                               r"\[disabled\]|:disabled",
                               r"aria-(selected|checked|expanded|current)"]
                 if re.search(pat, s))
    d["states"]         = 1 if states >= 4 else (0.5 if states >= 2 else 0)
    d["focus-visible"]  = 1 if ":focus-visible" in s else 0
    d["reduced-motion"] = 1 if "prefers-reduced-motion" in s else (
        0.5 if re.search(r"transition:|@keyframes|animation:", s) else 0)
    if interactive:
        d["AT(aria+kbd)"] = 1 if ("role=" in s and "aria-" in s and re.search(r"keydown|keyup", s)) else (
            0.5 if ("role=" in s and "aria-" in s) else 0)
    else:
        # PASSIVE atom (meta interactive:false) — keyboard is N/A by design (decided 2026-06-22, option A).
        # Full credit for being exposed to AT via announce/role/label; 0 if it exposes nothing (still
        # catches a badly-built passive component, e.g. a status indicator with no aria-live).
        d["AT(aria+kbd)"] = 1 if re.search(r"aria-live|role=|aria-label", s) else 0
    d["behaviour"]      = 1 if "addEventListener" in s else 0
    if name in ROUND_EXEMPT:
        d["square-corners"] = 1                  # Badge/Avatar are sanctioned round — exempt
    else:
        radius_bad = bool(re.search(r"border-radius:\s*[1-9]", s)) and "round" not in s.lower()
        d["square-corners"] = 1 if ("border-radius:0" in s.replace(" ", "") and not radius_bad) else 0
    # responsive = real width adaptation only (NOT the prefers-reduced-motion media query)
    d["responsive"]     = 1 if re.search(r"ResizeObserver|matchMedia|container-type|@container|@media[^{}]*(?:min-width|max-width)", s) else 0
    return d, sum(d.values())

rows = []
for f in sorted(glob.glob(os.path.join(SNIP, "*.reference.html"))):
    name = os.path.basename(f).replace(".reference.html", "")
    mp = os.path.join(COMP, name.lower() + ".meta.json")
    interactive = True
    if os.path.exists(mp):
        try: interactive = json.load(open(mp, encoding="utf-8")).get("interactive", True)
        except Exception: pass
    d, total = score(name, open(f, encoding="utf-8").read(), interactive)
    rows.append((name, total, d))

MAX = len(DIMS)
rows.sort(key=lambda r: (r[1], r[0]))

def cell(v): return "✅" if v == 1 else ("🟡" if v == 0.5 else "—")

out = ["# Prototype-grade audit — snippets vs the Tabs-bar standard",
       f"*Advisory (non-gating). {len(rows)} snippets scored on {MAX} measurable signals. "
       f"Lowest first = most refinement needed. ★ = payments-journey priority. "
       f"Dims 7 (geometry) & 9 (edge states) are manual, not scored here.*\n",
       "| # | Component | Score | " + " | ".join(DIMS) + " |",
       "|---|---|---|" + "|".join(["---"] * MAX) + "|"]
for i, (name, total, d) in enumerate(rows, 1):
    star = "★ " if name in PRIORITY else ""
    out.append(f"| {i} | {star}{name} | {total:.1f}/{MAX} | " + " | ".join(cell(d[k]) for k in DIMS) + " |")

avg = sum(r[1] for r in rows) / len(rows)
ex = next((r for r in rows if r[0] == "Tabs"), None)
out.append(f"\n**Average {avg:.1f}/{MAX}** · exemplar Tabs {ex[1]:.1f}/{MAX}." if ex else "")
pr = sorted((r for r in rows if r[0] in PRIORITY), key=lambda r: r[1])
out.append(f"\n## ★ Payments-journey priority — refine these first ({len(pr)})")
for name, total, _ in pr:
    out.append(f"- **{name}** — {total:.1f}/{MAX}")

report = "\n".join(out) + "\n"
open(os.path.join(HERE, "_PROTOTYPE-GRADE-AUDIT.md"), "w", encoding="utf-8").write(report)
print(report)
