#!/usr/bin/env python3
"""Batch 2: Text/icon token contrast audit.

Check all text, icon, and label tokens in dark mode.
Do their dark values create sufficient contrast on a standard dark surface?

Standard dark surface: #1D1D1D (HSBC dark-mode/600 primitive)
Minimum contrast: 4.5:1 for text, 3:1 for icons/decorative

Flags: POOR_CONTRAST if dark value fails threshold.
Writes knowledge/_TEXT-CONTRAST-AUDIT.json + .md
"""
import json, os
from collections import defaultdict
import sys
sys.path.insert(0, os.path.dirname(__file__))
from _contrast_utils import hex_to_rgb, luminance, contrast_ratio, is_sufficient_contrast

ROOT = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.join(ROOT, "tokens")

DARK_SURFACE = "#1D1D1D"  # HSBC dark-mode/600

def leaves(node, path="", out=None):
    if out is None: out = {}
    if isinstance(node, dict):
        if any(k in node for k in ("$value", "light", "dark")):
            out[path] = node; return out
        for k, v in node.items():
            if k.startswith("$"): continue
            leaves(v, (path + "/" + k).strip("/") if path else k, out)
    return out

def mode_val(n, m):
    x = n.get(m)
    return (x.get("$value") or x.get("value")) if isinstance(x, dict) else x

def is_text_or_icon_token(token_name):
    """Classify if a token is text, icon, or label."""
    return any(x in token_name for x in ['text/', 'icon/', 'label'])

# Load tokens
sem = leaves(json.load(open(os.path.join(TOK, "semantic-colour.json"))))

# Find all text/icon tokens and check dark contrast on dark surface
text_audit = []
poor_contrast = defaultdict(list)

for token_name, node in sorted(sem.items()):
    if not is_text_or_icon_token(token_name):
        continue

    if "light" not in node or "dark" not in node:
        continue

    dark_val = mode_val(node, "dark")
    if not dark_val or not isinstance(dark_val, str) or not dark_val.startswith("#"):
        continue

    try:
        # Determine context (text needs stricter threshold than icon)
        context = 'text' if 'text' in token_name else 'ui'
        threshold = 4.5 if context == 'text' else 3.0

        ratio = contrast_ratio(dark_val, DARK_SURFACE)
        passes = is_sufficient_contrast(ratio, context=context)

        record = {
            "token": token_name,
            "dark_value": dark_val,
            "dark_surface": DARK_SURFACE,
            "contrast_ratio": ratio,
            "threshold": threshold,
            "context": context,
            "status": "OK" if passes else "POOR_CONTRAST"
        }
        text_audit.append(record)

        if not passes:
            poor_contrast[token_name].append(record)
    except Exception as e:
        print(f"Error processing {token_name}: {e}")

# Stats
ok_count = sum(1 for r in text_audit if r["status"] == "OK")
poor_count = len(poor_contrast)

# Write JSON
audit_json = {
    "$description": "Text/icon token dark-mode contrast audit. Checks if all text, icon, and label tokens' dark values create sufficient contrast on the standard dark surface (#1D1D1D). Text needs 4.5:1, icons/UI need 3:1. POOR_CONTRAST = fails the threshold.",
    "generated": "2026-06-19",
    "standard_dark_surface": DARK_SURFACE,
    "totals": {
        "text_icon_tokens": len(text_audit),
        "ok": ok_count,
        "poor_contrast": poor_count
    },
    "tokens": {r["token"]: r for r in text_audit}
}
json.dump(audit_json, open(os.path.join(ROOT, "_TEXT-CONTRAST-AUDIT.json"), "w"), indent=2, ensure_ascii=False)

# Write Markdown
lines = [
    "# Text/icon token dark-mode contrast audit",
    "",
    "> Checks if all text, icon, and label tokens' dark values create sufficient contrast on the standard dark surface (#1D1D1D, HSBC dark-mode/600). Text needs 4.5:1 (AA), icons/UI need 3:1 (AA).",
    "",
    f"**Coverage:** {ok_count}/{len(text_audit)} text/icon tokens pass · {poor_count} below threshold.",
    ""
]

if poor_count > 0:
    lines.extend([
        "## Poor contrast — requires fix",
        "",
        "| Token | Dark value | Contrast on #1D1D1D | Threshold | Context |",
        "|---|---|---|---|---|"
    ])
    for token_name in sorted(poor_contrast.keys()):
        r = poor_contrast[token_name][0]
        lines.append(f"| `{r['token']}` | `{r['dark_value']}` | **{r['contrast_ratio']}:1** | {r['threshold']}:1 | {r['context']} |")
    lines.append("")

lines.extend([
    "## All text/icon tokens",
    "",
    "| Token | Dark value | Contrast on #1D1D1D | Threshold | Status |",
    "|---|---|---|---|---|"
])
for r in text_audit:
    status = "❌ POOR" if r["status"] == "POOR_CONTRAST" else "✅ OK"
    lines.append(f"| `{r['token']}` | `{r['dark_value']}` | {r['contrast_ratio']}:1 | {r['threshold']}:1 | {status} |")

open(os.path.join(ROOT, "_TEXT-CONTRAST-AUDIT.md"), "w").write("\n".join(lines))

print(f"text/icon contrast audit: {ok_count}/{len(text_audit)} OK, {poor_count} poor contrast")
if poor_count > 0:
    print("Poor contrast tokens:")
    for token_name in sorted(poor_contrast.keys()):
        r = poor_contrast[token_name][0]
        print(f"  {token_name}: {r['contrast_ratio']}:1 (need {r['threshold']}:1, context={r['context']})")
