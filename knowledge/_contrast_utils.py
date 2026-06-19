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
      context (str): 'text' (4.5:1), 'large_text' (3:1), 'ui' (3:1)

    Returns:
      bool: True if meets threshold
    """
    if context == 'text':
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
