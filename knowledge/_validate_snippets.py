#!/usr/bin/env python3
"""Snippet gate — validate authored reference snippets against the canon.

For every knowledge/snippets/*.reference.html:
  1. TOKEN FIDELITY — each CSS var declared in the embedded #token-manifest must
     match its token's resolved value in BOTH light and dark (catches drift the
     moment the store changes and the snippet isn't updated).
  2. ARIA — every requiredAria string must be present in the markup.
  3. CONTRAST — every declared contrast pair must clear its threshold in both
     modes (text 4.5:1, ui/indicator 3:1).
  4. FOCUS — there must be a :focus-visible rule, and no outline:none without a
     visible replacement (box-shadow or a non-none outline).

This is the link that makes a snippet "gated": it cannot silently drift from the
meta + token stores. Exits non-zero on any failure so _build_all.py fails the build.
Writes knowledge/_SNIPPET-AUDIT.md.
"""
import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from _contrast_utils import contrast_ratio, is_sufficient_contrast

ROOT = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(ROOT, "snippets")
TOK = os.path.join(ROOT, "tokens")

sem = json.load(open(os.path.join(TOK, "semantic-colour.json")))


def resolve(token, mode):
    """tokens/active + 'dark' -> '#1D1D1D' (uppercased), or None."""
    n = sem
    for k in token.split("/"):
        n = n.get(k) if isinstance(n, dict) else None
        if n is None:
            return None
    m = n.get(mode)
    v = m.get("$value") if isinstance(m, dict) else m
    return v.upper() if isinstance(v, str) and v.startswith("#") else None


def theme_block(css, theme):
    m = re.search(r'\[data-theme="%s"\]\s*\{([^}]*)\}' % theme, css)
    return m.group(1) if m else ""


def var_value(block, var):
    m = re.search(re.escape(var) + r'\s*:\s*(#[0-9A-Fa-f]{6,8})', block)
    return m.group(1).upper() if m else None


def validate(path):
    html = open(path).read()
    name = os.path.basename(path)
    errors, warnings = [], []

    mm = re.search(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', html, re.S)
    if not mm:
        return [f"{name}: no #token-manifest block found"], []
    manifest = json.loads(mm.group(1))

    light, dark = theme_block(html, "light"), theme_block(html, "dark")
    if not light or not dark:
        errors.append(f"{name}: missing [data-theme=\"light\"] or [data-theme=\"dark\"] block")

    # 1. token fidelity (both modes)
    # driftAllow = { "--var": ["dark"], ..., "$reason": "..." } — an INTENTIONAL, documented deviation
    # (e.g. a broken/dangling token value worked around in the snippet pending a token-level fix). Such a
    # drift is recorded as a WARNING, not a build failure. Mirrors the contrast/dark-surface allow-lists.
    drift_allow = manifest.get("driftAllow", {})
    drift_reason = drift_allow.get("$reason", "intentional (see snippet comment)")
    for var, token in manifest.get("vars", {}).items():
        for mode, block in (("light", light), ("dark", dark)):
            declared = var_value(block, var)
            canon = resolve(token, mode)
            if canon is None:
                errors.append(f"{name}: token '{token}' not found in store")
            elif declared is None:
                errors.append(f"{name}: var {var} missing in {mode} block")
            elif declared != canon:
                if mode in drift_allow.get(var, []):
                    warnings.append(f"{name}: ALLOWED drift {var} ({mode}) = {declared} (token {token} = {canon}) — {drift_reason}")
                else:
                    errors.append(f"{name}: DRIFT {var} ({mode}) = {declared} but {token} = {canon}")

    # 2. ARIA
    for need in manifest.get("requiredAria", []):
        if need not in html:
            errors.append(f"{name}: required ARIA missing: {need}")

    # 3. contrast pairs
    for p in manifest.get("contrastPairs", []):
        ctx = p.get("context", "text")
        for mode in ("light", "dark"):
            fg, bg = resolve(p["fg"], mode), resolve(p["bg"], mode)
            if not fg or not bg:
                errors.append(f"{name}: contrast pair {p['fg']}/{p['bg']} unresolved ({mode})")
                continue
            r = contrast_ratio(fg, bg)
            if not is_sufficient_contrast(r, context=ctx):
                need = 4.5 if ctx == "text" else 3.0
                errors.append(f"{name}: CONTRAST {p['fg']} on {p['bg']} ({mode}) = {r}:1 < {need}:1")

    # 4. focus
    # Focus rules only apply to INTERACTIVE components; passive ones (e.g. Badge) are exempt.
    interactive = any(s in html for s in (
        "<button", "<a ", "<input", "<select", "<textarea",
        'role="button"', 'role="link"', 'role="option"', 'role="combobox"',
        'role="switch"', 'role="menuitem"', 'role="tab"', 'tabindex="0"'))
    if not interactive:
        return errors, warnings
    if ":focus-visible" not in html:
        errors.append(f"{name}: no :focus-visible rule (2.4.7)")
    bare = re.findall(r'outline\s*:\s*none', html)
    # a visible replacement = box-shadow, a non-none outline, or a :focus-visible-driven
    # visible change (transform/border/background/opacity) e.g. an animated underline.
    repl = (("box-shadow" in html)
            or re.search(r'outline\s*:\s*[^n;]', html)
            or re.search(r'focus-visible[^{}]*\{[^}]*(transform|scaleX|border|background|opacity)', html))
    if bare and not repl:
        errors.append(f"{name}: outline:none with no visible focus replacement (2.4.7)")

    return errors, warnings


snippets = sorted(glob.glob(os.path.join(SNIP, "*.reference.html")))
all_err, all_warn, lines = [], [], ["# Snippet gate — reference implementations vs canon", ""]

if not snippets:
    lines.append("_No snippets found in knowledge/snippets/._")
for path in snippets:
    errs, warns = validate(path)
    all_err += errs
    all_warn += warns
    status = "✅ PASS" if not errs else f"❌ {len(errs)} FAIL"
    lines.append(f"## {os.path.basename(path)} — {status}")
    for e in errs:
        lines.append(f"- ❌ {e}")
    for w in warns:
        lines.append(f"- 🟡 {w}")
    if not errs:
        lines.append("- token fidelity (light+dark), ARIA, contrast pairs, focus — all clean.")
    lines.append("")

open(os.path.join(ROOT, "_SNIPPET-AUDIT.md"), "w").write("\n".join(lines))

print(f"snippet gate: {len(snippets)} snippet(s), {len(all_err)} failure(s)")
for e in all_err:
    print("  ❌", e)
sys.exit(1 if all_err else 0)
