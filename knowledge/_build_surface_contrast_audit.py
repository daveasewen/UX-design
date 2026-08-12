#!/usr/bin/env python3
"""Text/icon token dark-mode contrast audit (fix #1b — resolved-surface + gating).

For every text/icon/label token, compute its dark-mode contrast against the
REAL worst-case dark surface it sits on (resolved from the token store), not a
single hardcoded surface. Mode-specific tokens (e.g. */on-light) are excluded
rather than false-flagged. Tokens in CONTRAST_ALLOWLIST (disabled states) are
reported but do not fail the build.

GATES the build: exits non-zero if any non-allowlisted token is below threshold.
Text needs 4.5:1 (WCAG 1.4.3 AA); icons/UI need 3:1 (1.4.11).
Writes knowledge/_TEXT-CONTRAST-AUDIT.json + .md
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
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


def is_text_or_icon_token(name):
    return any(x in name for x in ["text/", "icon/", "label"])


sem = leaves(json.load(open(os.path.join(TOK, "semantic-colour.json"))))
surfaces = load_dark_surfaces(sem)
DEFAULT_DARK, RAISED_DARK = standard_dark_surfaces(TOK)

audit, poor, skipped = [], [], []

for name, node in sorted(sem.items()):
    if not is_text_or_icon_token(name):
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

    context = "text" if "text" in name else "ui"
    threshold = 4.5 if context == "text" else 3.0
    ratio = contrast_ratio(dark_val, surface)
    passes = is_sufficient_contrast(ratio, context=context)
    allowlisted = name in CONTRAST_ALLOWLIST

    rec = {
        "token": name, "dark_value": dark_val,
        "surface": surface, "surface_label": label,
        "contrast_ratio": ratio, "threshold": threshold, "context": context,
        "status": "OK" if passes else ("ALLOWED" if allowlisted else "POOR_CONTRAST"),
        "allowlist_reason": CONTRAST_ALLOWLIST.get(name) if (allowlisted and not passes) else None,
    }
    audit.append(rec)
    if not passes and not allowlisted:
        poor.append(rec)

ok_count = sum(1 for r in audit if r["status"] == "OK")
allowed = [r for r in audit if r["status"] == "ALLOWED"]

audit_json = {
    "$description": "Text/icon dark-mode contrast audit. Each token is tested against the worst-case (lightest) dark surface it can sit on, resolved from the store (page default + raised island, or its own group's surfaces). on-light tokens are excluded (light-only). Allowlisted disabled-state tokens are reported but do not gate. POOR_CONTRAST (non-allowlisted, below threshold) FAILS the build.",
    "generated": "2026-06-19",
    "default_dark_surface": DEFAULT_DARK,
    "raised_dark_surface": RAISED_DARK,
    "totals": {
        "text_icon_tokens": len(audit), "ok": ok_count,
        "allowed_exceptions": len(allowed), "poor_contrast": len(poor),
        "skipped_light_only": len(skipped),
    },
    "poor_contrast": poor,
    "allowed_exceptions": allowed,
    "skipped_light_only": skipped,
    "tokens": OrderedDict((r["token"], r) for r in audit),
}
json.dump(audit_json, open(os.path.join(ROOT, "_TEXT-CONTRAST-AUDIT.json"), "w"), indent=2, ensure_ascii=False)

L = [
    "# Text/icon token dark-mode contrast audit",
    "",
    f"> Each text/icon token is tested against the **worst-case (lightest) dark surface it can sit on**, resolved from the store — page default `{DEFAULT_DARK}` + raised island `{RAISED_DARK}`, or the token's own group surfaces. `on-light` tokens are excluded (light-only). Disabled-state tokens are allowlisted (reported, not gated). Text needs 4.5:1, icons/UI need 3:1.",
    "",
    f"**Result:** {ok_count} pass · {len(allowed)} allowed exception(s) · **{len(poor)} gating failure(s)** · {len(skipped)} skipped (light-only).",
    "",
]
if poor:
    L += ["## ❌ Gating failures — these FAIL the build", "",
          "| Token | Dark value | Surface | Contrast | Need | Context |",
          "|---|---|---|---|---|---|"]
    for r in poor:
        L.append(f"| `{r['token']}` | `{r['dark_value']}` | `{r['surface']}` ({r['surface_label']}) | **{r['contrast_ratio']}:1** | {r['threshold']}:1 | {r['context']} |")
    L.append("")
if allowed:
    L += ["## Allowed exceptions (reported, not gated)", "",
          "| Token | Dark value | Surface | Contrast | Reason |",
          "|---|---|---|---|---|"]
    for r in allowed:
        L.append(f"| `{r['token']}` | `{r['dark_value']}` | `{r['surface']}` | {r['contrast_ratio']}:1 | {r['allowlist_reason']} |")
    L.append("")
if skipped:
    L += ["## Skipped — light-mode-only tokens", "",
          "| Token | Reason |", "|---|---|"]
    for r in skipped:
        L.append(f"| `{r['token']}` | {r['reason']} |")
    L.append("")
L += ["## All audited text/icon tokens", "",
      "| Token | Dark value | Surface | Contrast | Status |", "|---|---|---|---|---|"]
for r in audit:
    badge = {"OK": "✅ OK", "ALLOWED": "🟡 ALLOWED", "POOR_CONTRAST": "❌ POOR"}[r["status"]]
    L.append(f"| `{r['token']}` | `{r['dark_value']}` | `{r['surface']}` | {r['contrast_ratio']}:1 | {badge} |")
open(os.path.join(ROOT, "_TEXT-CONTRAST-AUDIT.md"), "w").write("\n".join(L))

print(f"text/icon contrast audit: {ok_count} OK, {len(allowed)} allowed, {len(poor)} GATING FAIL, {len(skipped)} skipped(light-only)")
for r in poor:
    print(f"  ❌ {r['token']}: {r['contrast_ratio']}:1 on {r['surface']} (need {r['threshold']}:1, {r['context']})")
sys.exit(1 if poor else 0)
