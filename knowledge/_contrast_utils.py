#!/usr/bin/env python3
"""WCAG contrast ratio calculation and token context mapping.

Batch 1 (Foundations) for comprehensive contrast-aware audit.

Functions:
  - hex_to_rgb(hex_str) → (r, g, b) 0-1 range
  - luminance(r, g, b) → relative luminance (0-1)
  - contrast_ratio(lum1, lum2) → WCAG AA ratio (float)
  - is_sufficient_contrast(ratio, context) → bool (4.5:1 for text, 3:1 for UI)
  - token_context(token_name) → str ('text', 'surface', 'indicator', 'unknown')

Test harness validates against known good/bad pairs from Tabs fitness test.
"""

def hex_to_rgb(hex_str):
    """Convert #RRGGBB to (r, g, b) with values 0-1."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex: {hex_str}")
    r = int(hex_str[0:2], 16) / 255.0
    g = int(hex_str[2:4], 16) / 255.0
    b = int(hex_str[4:6], 16) / 255.0
    return (r, g, b)

def luminance(r, g, b):
    """Relative luminance per WCAG 2.1 formula.

    Each channel: if <= 0.03928 → / 12.92, else → ((+0.055)/1.055)^2.4
    L = 0.2126*R + 0.7152*G + 0.0722*B
    """
    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    R = channel(r)
    G = channel(g)
    B = channel(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B

def contrast_ratio(hex1, hex2):
    """WCAG contrast ratio between two colours.

    Ratio = (L1 + 0.05) / (L2 + 0.05), where L1 >= L2.
    Returns float, rounded to 2 decimals.
    """
    r1, g1, b1 = hex_to_rgb(hex1)
    r2, g2, b2 = hex_to_rgb(hex2)

    l1 = luminance(r1, g1, b1)
    l2 = luminance(r2, g2, b2)

    # Lighter color first
    if l1 < l2:
        l1, l2 = l2, l1

    return round((l1 + 0.05) / (l2 + 0.05), 2)

def is_sufficient_contrast(ratio, context='text'):
    """Check if contrast ratio meets WCAG AA threshold.

    Args:
      ratio (float): contrast ratio (e.g., from contrast_ratio())
      context (str): 'text' (4.5:1), 'icon' (4.5:1 — brand icon-015, PROMOTED
        blocking 2026-07-02, Dave: "icons alone should have the small-text
        equivalent contrast at least"; pictograms/RAG indicators stay 'ui'/3:1),
        'large_text' (3:1), 'ui' (3:1)

    Returns:
      bool: True if meets threshold
    """
    if context in ('text', 'icon'):
        return ratio >= 4.5
    elif context in ('large_text', 'ui', 'indicator'):
        return ratio >= 3.0
    else:
        return ratio >= 4.5  # default to strictest

def token_context(token_name):
    """Classify a token by its intended use.

    Returns 'text', 'surface', 'indicator', 'decorative', or 'unknown'.
    """
    if any(x in token_name for x in ['text', 'label', 'copy']):
        return 'text'
    elif any(x in token_name for x in ['background', 'surface', 'border']):
        return 'surface'
    elif any(x in token_name for x in ['icon', 'indicator', 'active', 'primary', 'rag']):
        return 'indicator'
    elif any(x in token_name for x in ['disabled', 'decorative']):
        return 'decorative'
    else:
        return 'unknown'


# --- Surface resolution + audit policy (fix #1b completion, 2026-06-19) --------
# Replaces the old "assume one hardcoded #1D1D1D surface" model. A text/icon
# token is now judged against the WORST-CASE (lightest) dark surface it can
# actually sit on, and mode-specific tokens are excluded rather than false-flagged.

# Tokens intentionally exempt from the dark-mode contrast GATE, with reasons.
# These are reported but do NOT fail the build. Everything else below threshold does.
CONTRAST_ALLOWLIST = {
    "text/disabled":          "Disabled text — exempt from WCAG 1.4.3 (inactive UI component).",
    "tertiary/text/disabled": "Disabled text — exempt from WCAG 1.4.3 (inactive UI component).",
    "icon/disabled":          "Disabled icon — exempt from WCAG 1.4.3/1.4.11 (inactive component).",
    "tertiary/icon/disabled": "Disabled icon — exempt from WCAG 1.4.3/1.4.11 (inactive component).",
}

# Pairs FORBIDDEN BY RULING — not exemptions from contrast, but pairings that are
# not allowed to occur at all, so auditing them is auditing a non-existent state.
# Keyed token-prefix -> {surface-token: written reason}. Scope deliberately narrow:
# a pair lands here only when a recorded ruling forbids the combination, with the
# ledger reference in the reason. (Mechanism added 2026-07-18 with the R-D4 token
# promotion — the amber role token was the first fill the surface-resolver ever
# paired with the universal white RAG text.)
RULED_PAIR_EXCLUSIONS = {
    "rag/text": {
        "rag/warning-background":
            "R-D3 rule 1 (2026-07-18, _RAG-DECISIONS.md): amber ALWAYS carries black "
            "ink (#1A1A1A — 9.16:1); white RAG text on amber is forbidden by ruling, so "
            "this pair cannot occur. The amber-rules gate (owed) enforces the ruling "
            "itself; this entry only stops the audit testing a state the ruling forbids.",
    },
}

def _excluded_surfaces(token_name):
    for prefix, pairs in RULED_PAIR_EXCLUSIONS.items():
        if token_name.startswith(prefix):
            return pairs
    return {}

def is_light_only(token_name):
    """Tokens designed for light surfaces only (e.g. */on-light) are not used in
    dark mode, so judging them against a dark surface is a false positive."""
    return "on-light" in token_name

def _leaf_dark_hex(node):
    d = node.get("dark") if isinstance(node, dict) else None
    v = (d.get("$value") if isinstance(d, dict) else d)
    return v.upper() if isinstance(v, str) and v.startswith("#") else None

def load_dark_surfaces(sem_leaves):
    """Map every surface/background token -> its dark hex, to resolve the real
    surface a text/icon token sits on instead of assuming one."""
    out = {}
    for name, node in sem_leaves.items():
        if any(x in name for x in ("background", "surface")) and "tint" not in name:
            hx = _leaf_dark_hex(node)
            if hx:
                out[name] = hx
    return out

def _group_prefix(token_name):
    """'tertiary/text/disabled' -> 'tertiary'; 'text/default' -> '' (global)."""
    for marker in ("/text/", "/icon/", "/label"):
        if marker in token_name:
            return token_name.split(marker)[0]
    return ""

def resolve_dark_surface(token_name, surfaces, default_dark, raised_dark):
    """Return (surface_hex, label) — the worst-case (lightest) dark surface this
    token must stay legible on — or (None, reason) to skip.

    - on-light tokens: skip (light-mode only).
    - grouped tokens (tertiary/text/*): lightest dark surface within that group.
    - generic text/icon: lightest of the page default and the raised island,
      since a token can sit on either. Lightest = highest luminance = hardest
      for light text → the conservative choice (no false negatives).
    """
    if is_light_only(token_name):
        return (None, "light-mode-only (on-light); excluded from dark audit")
    if "on-inverse" in token_name:
        return (None, "sits on an inverting surface (secondary/pressed buttons), not the page; validated per-component via snippet contrast pairs")
    grp = _group_prefix(token_name)
    excluded = _excluded_surfaces(token_name)
    candidates = [hx for nm, hx in surfaces.items()
                  if grp and nm.startswith(grp + "/") and nm not in excluded]
    if not candidates:
        candidates = [default_dark, raised_dark]
    worst = max(candidates, key=lambda h: luminance(*hex_to_rgb(h)))
    return (worst, grp if grp else "page/raised")

def standard_dark_surfaces(tok_dir):
    """Resolve the two standard dark surfaces from the stores (not hardcoded):
    page default = semantic background/default dark; raised island = primitive
    grey dark-mode/600. Returns (default_dark, raised_dark)."""
    import json, os
    def leaves(node, path="", out=None):
        if out is None: out = {}
        if isinstance(node, dict):
            v = node.get("$value")
            if isinstance(v, str) and v.startswith("#"):
                out[path] = v.upper()
            for k, sub in node.items():
                if not k.startswith("$"):
                    leaves(sub, (path + "/" + k).strip("/") if path else k, out)
        return out
    default_dark = "#000000"
    try:
        sem = json.load(open(os.path.join(tok_dir, "semantic-colour.json")))
        default_dark = sem["background"]["default"]["dark"]["$value"].upper()
    except Exception:
        pass
    prims = leaves(json.load(open(os.path.join(tok_dir, "colour.json"))))
    raised = next((hx for p, hx in prims.items() if p.endswith("dark-mode/600")), "#1D1D1D")
    return default_dark, raised


if __name__ == '__main__':
    # Batch 1 validation harness: known good/bad pairs from Tabs fitness test
    print("=== Contrast Calculator — Validation Harness ===\n")

    test_cases = [
        # (label, fg_hex, bg_hex, context, expected_pass)
        ("Tabs label light mode (good)", "#333333", "#FFFFFF", "text", True),
        ("Tabs label dark mode Route A (good)", "#a9a9ad", "#161617", "text", True),
        ("Tabs label dark mode Route B (broken)", "#FFFFFF", "#FFFFFF", "text", False),
        ("Tabs indicator light (good)", "#DB0011", "#FFFFFF", "ui", True),
        ("Tabs indicator dark Route A (good)", "#DB0011", "#161617", "ui", True),
        ("Tabs indicator dark Route B (broken)", "#FFFFFF", "#FFFFFF", "ui", False),
        ("Text on light surface (good)", "#333333", "#FFFFFF", "text", True),
        ("Text on dark surface (good)", "#FFFFFF", "#1D1D1D", "text", True),
        ("Grey text on white (minimal)", "#767676", "#FFFFFF", "text", True),  # 4.48:1
        ("Grey text on white (too low)", "#B7B7B7", "#FFFFFF", "text", False),  # 2.85:1
    ]

    passed = 0
    failed = 0

    for label, fg, bg, context, expected in test_cases:
        ratio = contrast_ratio(fg, bg)
        actual = is_sufficient_contrast(ratio, context)
        status = "✓" if actual == expected else "✗"

        if actual == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {label}")
        print(f"   {fg} on {bg} → {ratio}:1 ({context}) — {'PASS' if actual else 'FAIL'}")

    print(f"\nResults: {passed} passed, {failed} failed")
    if failed == 0:
        print("✓ All validation cases passed. Ready for Batch 2.")
    else:
        print("✗ Some cases failed. Check the contrast function.")
