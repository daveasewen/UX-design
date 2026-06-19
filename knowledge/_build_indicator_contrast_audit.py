#!/usr/bin/env python3
"""Batch 3: Indicator/accent token contrast audit.

Check brand red, RAG status indicators, and interactive state tokens in dark mode.
Do their dark values create sufficient contrast on a standard dark surface?

Standard dark surface: #1D1D1D (HSBC dark-mode/600 primitive)
Minimum contrast: 3:1 (UI component threshold for indicators)

These are intentional/accent colours, but still need to be visible in dark mode.

Flags: POOR_CONTRAST if dark value fails threshold.
Writes knowledge/_INDICATOR-CONTRAST-AUDIT.json + .md
"""
import json, os
from collections import defaultdict
import sys
sys.path.insert(0, os.path.dirname(__file__))
from _contrast_utils import contrast_ratio, is_sufficient_contrast

ROOT = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.join(ROOT, "tokens")

DARK_SURFACE = "#1D1D1D"

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

def is_indicator_token(token_name):
    """Classify if a token is an indicator/accent/status colour (not a surface)."""
    patterns = ['primary', 'rag/', 'interactive', 'status']
    has_pattern = any(p in token_name for p in patterns)
    # Exclude background/surface/border tokens (they're not indicators)
    is_surface = any(x in token_name for x in ['background', 'surface', 'border', 'tint'])
    return has_pattern and not is_surface

# Load tokens
sem = leaves(json.load(open(os.path.join(TOK, "semantic-colour.json"))))

# Find all indicator tokens and check dark contrast
indicator_audit = []
poor_contrast = defaultdict(list)

for token_name, node in sorted(sem.items()):
    if not is_indicator_token(token_name):
        continue

    if "light" not in node or "dark" not in node:
        continue

    dark_val = mode_val(node, "dark")
    if not dark_val or not isinstance(dark_val, str) or not dark_val.startswith("#"):
        continue

    try:
        ratio = contrast_ratio(dark_val, DARK_SURFACE)
        passes = is_sufficient_contrast(ratio, context='ui')

        record = {
            "token": token_name,
            "dark_value": dark_val,
            "dark_surface": DARK_SURFACE,
            "contrast_ratio": ratio,
            "threshold": 3.0,
            "status": "OK" if passes else "POOR_CONTRAST"
        }
        indicator_audit.append(record)

        if not passes:
            poor_contrast[token_name].append(record)
    except Exception as e:
        print(f"Error processing {token_name}: {e}")

# Stats
ok_count = sum(1 for r in indicator_audit if r["status"] == "OK")
poor_count = len(poor_contrast)

# Write JSON
audit_json = {
    "$description": "Indicator/accent token dark-mode contrast audit. Checks if brand red, RAG status, and interactive state tokens' dark values create sufficient contrast (3:1) on the standard dark surface (#1D1D1D). POOR_CONTRAST = fails the threshold.",
    "generated": "2026-06-19",
    "standard_dark_surface": DARK_SURFACE,
    "minimum_contrast": 3.0,
    "totals": {
        "indicator_tokens": len(indicator_audit),
        "ok": ok_count,
        "poor_contrast": poor_count
    },
    "tokens": {r["token"]: r for r in indicator_audit}
}
json.dump(audit_json, open(os.path.join(ROOT, "_INDICATOR-CONTRAST-AUDIT.json"), "w"), indent=2, ensure_ascii=False)

# Write Markdown
lines = [
    "# Indicator/accent token dark-mode contrast audit",
    "",
    "> Checks if brand red, RAG status, and interactive state tokens' dark values create sufficient contrast on the standard dark surface (#1D1D1D). Minimum threshold: 3:1 (UI component).",
    "",
    f"**Coverage:** {ok_count}/{len(indicator_audit)} indicator tokens pass · {poor_count} below threshold.",
    ""
]

if poor_count > 0:
    lines.extend([
        "## Poor contrast — requires fix",
        "",
        "| Token | Dark value | Contrast on #1D1D1D | Threshold |",
        "|---|---|---|---|"
    ])
    for token_name in sorted(poor_contrast.keys()):
        r = poor_contrast[token_name][0]
        lines.append(f"| `{r['token']}` | `{r['dark_value']}` | **{r['contrast_ratio']}:1** | {r['threshold']}:1 |")
    lines.append("")

lines.extend([
    "## All indicator/accent tokens",
    "",
    "| Token | Dark value | Contrast on #1D1D1D | Status |",
    "|---|---|---|---|"
])
for r in indicator_audit:
    status = "❌ POOR" if r["status"] == "POOR_CONTRAST" else "✅ OK"
    lines.append(f"| `{r['token']}` | `{r['dark_value']}` | {r['contrast_ratio']}:1 | {status} |")

open(os.path.join(ROOT, "_INDICATOR-CONTRAST-AUDIT.md"), "w").write("\n".join(lines))

print(f"indicator/accent contrast audit: {ok_count}/{len(indicator_audit)} OK, {poor_count} poor contrast")
if poor_count > 0:
    print("Poor contrast tokens:")
    for token_name in sorted(poor_contrast.keys()):
        r = poor_contrast[token_name][0]
        print(f"  {token_name}: {r['contrast_ratio']}:1 (need {r['threshold']}:1)")
