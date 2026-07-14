#!/usr/bin/env python3
"""Indicator/accent token dark-mode contrast audit (fix #1b — resolved + gating).

Brand red, RAG status, and interactive-state tokens must stay visible in dark
mode. Each is tested against the worst-case (lightest) dark surface it can sit
on, resolved from the store. Mode-specific (*/on-light) tokens are excluded.
Allowlisted tokens are reported but do not gate.

GATES the build: exits non-zero if any non-allowlisted indicator is below 3:1
(WCAG 1.4.11 non-text contrast, AA).

Classifier note (2026-07-14): `is_indicator_token` was widened to include
BORDER tokens generally (e.g. `divider/border/subsection`, `form/border/default`),
not just brand/RAG/interactive-accent tokens. Reason: WCAG 1.4.11 explicitly
covers "the boundaries of user interface components" — a border IS a graphical
object this SC protects, not a surface fill. The prior classifier required one
of {primary, rag/, interactive, status} AND excluded anything containing
"border", which meant a token like `divider/border/subsection` could never be
picked up regardless — it's not brand/status-named, and even if it were, the
border exclusion would have caught it. That silently exempted every border
token in the store from this SC's audit. Fixed by adding a `border` keyword to
the positive match and dropping `border` from the surface-exclusion list
(surface exclusion now only covers actual fills: background/surface/tint).
This was found via the compliance-graph verification join (2026-07-14,
[[compliance-verified-by-edges]]) surfacing Divider as `1.4.11 not_covered`
despite binding proper light/dark-mode tokens.

Inactive-component exemption (2026-07-14, same pass): the first full run of the
widened classifier caught 19 tokens below 3:1, not just Divider's. 4 of those
were `*/disabled` tokens (`form/border/disabled`, `primary/border/disabled`,
`secondary/border/disabled`, `tertiary/border/disabled`). WCAG 1.4.11's own
normative text carves these out: "...have a contrast ratio of at least 3:1...
except for inactive components." So auditing disabled-state borders against
this SC was itself a bug in the widened classifier, not a real finding — fixed
by excluding any token containing "disabled" from this audit entirely.

The remaining 15 tokens (dividers, table/tabs/tooltip borders, active-state
form/primary borders, data-vis gridlines, and the generic border/strong +
border/subtle primitives) are left as genuine GATING failures per an explicit
decision (2026-07-14): rather than quietly narrowing the classifier further or
allowlisting them, the build stays red on these until each is either given a
real dark-mode value fix or its component's `applies_to` claim is reconsidered.
See `_INDICATOR-CONTRAST-AUDIT.md` for the live list and
`knowledge/compliance/README.md` for the tracking note.
"""
import json, os, sys
from collections import OrderedDict
sys.path.insert(0, os.path.dirname(__file__))
from _contrast_utils import (
    contrast_ratio, is_sufficient_contrast,
    load_dark_surfaces, resolve_dark_surface, standard_dark_surfaces,
    CONTRAST_ALLOWLIST,
)

ROOT = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.join(ROOT, "tokens")


def leaves(node, path="", out=None):
    if out is None:
        out = {}
    if isinstance(node, dict):
        if any(k in node for k in ("$value", "light", "dark")):
            out[path] = node
            return out
        for k, v in node.items():
            if k.startswith("$"):
                continue
            leaves(v, (path + "/" + k).strip("/") if path else k, out)
    return out


def mode_val(n, m):
    x = n.get(m)
    return (x.get("$value") or x.get("value")) if isinstance(x, dict) else x


def is_indicator_token(name):
    has = any(p in name for p in ["primary", "rag/", "interactive", "status", "border"])
    is_surface = any(x in name for x in ["background", "surface", "tint"])
    is_inactive = "disabled" in name  # WCAG 1.4.11 exempts inactive components, verbatim
    return has and not is_surface and not is_inactive


sem = leaves(json.load(open(os.path.join(TOK, "semantic-colour.json"))))
surfaces = load_dark_surfaces(sem)
DEFAULT_DARK, RAISED_DARK = standard_dark_surfaces(TOK)

audit, poor, skipped = [], [], []

for name, node in sorted(sem.items()):
    if not is_indicator_token(name):
        continue
    if "light" not in node or "dark" not in node:
        continue
    dark_val = mode_val(node, "dark")
    if not (isinstance(dark_val, str) and dark_val.startswith("#")):
        continue

    surface, label = resolve_dark_surface(name, surfaces, DEFAULT_DARK, RAISED_DARK)
    if surface is None:
        skipped.append({"token": name, "dark_value": dark_val, "reason": label})
        continue

    ratio = contrast_ratio(dark_val, surface)
    passes = is_sufficient_contrast(ratio, context="ui")
    allowlisted = name in CONTRAST_ALLOWLIST

    rec = {
        "token": name, "dark_value": dark_val,
        "surface": surface, "surface_label": label,
        "contrast_ratio": ratio, "threshold": 3.0,
        "status": "OK" if passes else ("ALLOWED" if allowlisted else "POOR_CONTRAST"),
        "allowlist_reason": CONTRAST_ALLOWLIST.get(name) if (allowlisted and not passes) else None,
    }
    audit.append(rec)
    if not passes and not allowlisted:
        poor.append(rec)

ok_count = sum(1 for r in audit if r["status"] == "OK")
allowed = [r for r in audit if r["status"] == "ALLOWED"]

audit_json = {
    "$description": "Indicator/accent dark-mode contrast audit. Brand red, RAG status, interactive-state, AND border tokens (widened 2026-07-14 — WCAG 1.4.11 explicitly covers UI-component boundaries, not just accent fills) tested at 3:1 (WCAG 1.4.11) against the worst-case (lightest) dark surface resolved from the store. on-light tokens excluded (light-only). Disabled/inactive-state tokens excluded per WCAG 1.4.11's own text ('except for inactive components'). Allowlisted tokens reported, not gated. POOR_CONTRAST FAILS the build — as of 2026-07-14, 15 border tokens genuinely fail and are being tracked as real gaps, not allowlisted away.",
    "generated": "2026-06-19",
    "default_dark_surface": DEFAULT_DARK,
    "raised_dark_surface": RAISED_DARK,
    "minimum_contrast": 3.0,
    "totals": {
        "indicator_tokens": len(audit), "ok": ok_count,
        "allowed_exceptions": len(allowed), "poor_contrast": len(poor),
        "skipped_light_only": len(skipped),
    },
    "poor_contrast": poor,
    "allowed_exceptions": allowed,
    "skipped_light_only": skipped,
    "tokens": OrderedDict((r["token"], r) for r in audit),
}
json.dump(audit_json, open(os.path.join(ROOT, "_INDICATOR-CONTRAST-AUDIT.json"), "w"), indent=2, ensure_ascii=False)

L = [
    "# Indicator/accent token dark-mode contrast audit",
    "",
    f"> Brand red, RAG status, interactive-state, and border tokens tested at **3:1** (WCAG 1.4.11) against the worst-case (lightest) dark surface resolved from the store — page default `{DEFAULT_DARK}` + raised island `{RAISED_DARK}`. `on-light` tokens excluded (light-only). Border tokens included since 2026-07-14 (1.4.11 explicitly covers UI-component boundaries). `*/disabled` tokens excluded — WCAG 1.4.11 itself exempts inactive components.",
    "",
    f"**Result:** {ok_count} pass · {len(allowed)} allowed exception(s) · **{len(poor)} gating failure(s)** · {len(skipped)} skipped (light-only).",
    "",
]
if poor:
    L += ["## ❌ Gating failures — these FAIL the build", "",
          "| Token | Dark value | Surface | Contrast | Need |",
          "|---|---|---|---|---|"]
    for r in poor:
        L.append(f"| `{r['token']}` | `{r['dark_value']}` | `{r['surface']}` ({r['surface_label']}) | **{r['contrast_ratio']}:1** | {r['threshold']}:1 |")
    L.append("")
if skipped:
    L += ["## Skipped — light-mode-only tokens", "", "| Token | Reason |", "|---|---|"]
    for r in skipped:
        L.append(f"| `{r['token']}` | {r['reason']} |")
    L.append("")
L += ["## All audited indicator/accent tokens", "",
      "| Token | Dark value | Surface | Contrast | Status |", "|---|---|---|---|---|"]
for r in audit:
    badge = {"OK": "✅ OK", "ALLOWED": "🟡 ALLOWED", "POOR_CONTRAST": "❌ POOR"}[r["status"]]
    L.append(f"| `{r['token']}` | `{r['dark_value']}` | `{r['surface']}` | {r['contrast_ratio']}:1 | {badge} |")
open(os.path.join(ROOT, "_INDICATOR-CONTRAST-AUDIT.md"), "w").write("\n".join(L))

print(f"indicator/accent contrast audit: {ok_count} OK, {len(allowed)} allowed, {len(poor)} GATING FAIL, {len(skipped)} skipped(light-only)")
for r in poor:
    print(f"  ❌ {r['token']}: {r['contrast_ratio']}:1 on {r['surface']} (need {r['threshold']}:1)")
sys.exit(1 if poor else 0)
