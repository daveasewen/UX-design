#!/usr/bin/env python3
"""Snippet gate — validate authored reference snippets against the canon.

For every knowledge/snippets/*.reference.html:
  1. TOKEN FIDELITY — each CSS var declared in the embedded #token-manifest must
     match its token's resolved value in BOTH light and dark (catches drift the
     moment the store changes and the snippet isn't updated).
  2. ARIA — every requiredAria string must be present in the markup.
  3. CONTRAST — every declared contrast pair must clear its threshold in both
     modes (text 4.5:1, ui/indicator 3:1).
  4. ALL-CAPS — no text-transform:uppercase anywhere, no multi-word ALL-CAPS runs
     in visible text (acronym runs exempt). PROMOTED from advisory → blocking by
     Dave ruling 2026-07-02 (ADR-0005 §5; brand source: type26-019 — the 2026
     standard bans uppercase outside acronyms brand-wide, dyslexia rationale).
     Bite-tested in _tests/test_gates.py. Advisory continues to sweep non-gated
     surfaces (_fitness-test) for the same class.
  5. FOCUS — there must be a :focus-visible rule, and no outline:none without a
     visible replacement (box-shadow or a non-none outline).
  6. TYPOGRAPHY — no italics (font-style or <i>/<em>), no text-shadow, no raw
     brand-red hex on the color property (red text arrives only via the
     rag/error role token or a CTA role). RULED STRAIGHT TO BLOCKING by Dave
     2026-07-02 (type25-020; overrides advisory-first — all three families had
     zero canon occurrences, evidence pre-computed). Bite-tested in
     _tests/test_gates.py.
  7. COPY-LINT — nam-001 (HSBC never possessive: no "HSBC's" in copy),
     avd-006 (alt/aria-label never opens with "Image of…"/"Picture of…"/
     "Link to…"-class element-type prefixes), aca-004 (no bare
     "click here"-class link text — SC 2.4.4). RULED STRAIGHT TO BLOCKING by
     Dave 2026-07-03 (sweep-batch ruling; all three exact-match + pre-swept to
     zero canon signals, type25-020 precedent). The avd-006 ROLE-SUFFIX half
     (aria-label ending "… button"/"… link") had 4 live canon signals at
     ruling time (Cards "Example link") so it enters at ADVISORY tier instead
     (_validate_advisory.py check G) — fix at the Cards revisit, promote after.
     Bite-tested in _tests/test_gates.py.

This is the link that makes a snippet "gated": it cannot silently drift from the
meta + token stores. Exits non-zero on any failure so _build_all.py fails the build.
Writes knowledge/_SNIPPET-AUDIT.md.
"""
import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from _contrast_utils import contrast_ratio, is_sufficient_contrast
from _dtcg_units import px_number             # s141-D1 (A) unit-strip seam

ROOT = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(ROOT, "snippets")
TOK = os.path.join(ROOT, "tokens")

sem = json.load(open(os.path.join(TOK, "semantic-colour.json")))
layout = json.load(open(os.path.join(TOK, "layout.json")))
motion_store = json.load(open(os.path.join(TOK, "motion.json")))
opacity_store = json.load(open(os.path.join(TOK, "opacity.json")))  # #99-D1 alpha/* primitives
ctypes_store = json.load(open(os.path.join(ROOT, "component-types.json")))  # ADR-0013 registry

# Brand exemption (type26-019): uppercase is allowed for acronyms only. Runs made
# ENTIRELY of these pass; anything else in a 2+ word caps run is a gate failure.
ACRONYMS = {
    "HSBC", "UK", "AA", "AAA", "AT", "ARIA", "WCAG", "RAG", "SME", "API",
    "PDF", "URL", "CTA", "OK", "IBAN", "BIC", "OTP", "KYC", "FX",
    "GBP", "USD", "EUR", "HKD", "CNY", "AED", "ATM", "ID",
}

# type25-020 (blocking 2026-07-02): brand + complementary reds that may never be
# typed raw onto the color property. HSBC Red, Deep Red, rag/error light, and the
# retired Complementary Reds (legacy-asset drift guard). The sanctioned routes for
# red text are the rag/error role token (var(--error)) and CTA-role styling.
RED_HEXES = {"DB0011", "9B0000", "A8000B", "E31E22", "BA1110", "730014"}

# check 7 (blocking 2026-07-03): copy-lint pattern lists.
# avd-006 — alt/aria-label must describe PURPOSE, never announce the element type.
BANNED_ALT_PREFIX = re.compile(
    r'^\s*(image of|picture of|photo of|graphic of|icon of|link to)\b', re.I)
# aca-004 — bare link labels that describe the MECHANISM, not the target
# (normalised: tags stripped, whitespace collapsed, trailing punctuation dropped,
# lowercased). The uniqueness half of CA-4 (repeat labels on one screen) is
# screen-scope and stays with the composition layer.
BARE_LINK_TEXT = {
    "click here", "here", "click", "more", "read more", "learn more",
    "see more", "find out more", "this link", "link", "go",
}


def resolve(token, mode):
    """tokens/active + 'dark' -> '#1D1D1D' (uppercased), or None. Layout-namespace
    paths (border-radius/* …, Phase-0 shape de-hardcode) resolve from layout.json
    to a CSS-formatted string ('0' / '8px') so snippets can bind radius via manifest.
    motion/* + component-type/* (ADR-0013) resolve to UNITLESS number strings —
    the scale-factor namespace (matches gen_snippet_tokens._fmt)."""
    if token.startswith(("border-radius/", "border-width/", "focus-ring/", "layout/", "breakpoint/", "target/")):
        n = layout
        for k in token.split("/"):
            n = n.get(k) if isinstance(n, dict) else None
            if n is None:
                return None
        m = n.get(mode) if isinstance(n.get(mode), dict) else n
        v = m.get("$value") if isinstance(m, dict) else None
        v = px_number(v)   # s141-D1 (A) unit-strip seam: "0px" -> 0, then as before
        if isinstance(v, (int, float)):
            return "0" if v == 0 else f"{v}px"
        return str(v) if v is not None else None
    if token.startswith("alpha/"):
        # #99-D1 opacity primitives — UNITLESS number strings, mode-less (same both themes).
        n = opacity_store
        for k in token.split("/"):
            n = n.get(k) if isinstance(n, dict) else None
            if n is None:
                return None
        v = n.get("$value") if isinstance(n, dict) else None
        return str(v) if isinstance(v, (int, float)) else None
    if token.startswith(("motion/", "component-type/")):
        n = motion_store if token.startswith("motion/") else ctypes_store
        for k in token.split("/"):
            n = n.get(k) if isinstance(n, dict) else None
            if n is None:
                return None
        m = n.get(mode) if isinstance(n.get(mode), dict) else n
        v = m.get("$value") if isinstance(m, dict) else None
        if isinstance(v, (int, float)):
            return str(v)                      # scale factors are unitless
        return str(v) if v is not None else None
    n = sem
    for k in token.split("/"):
        n = n.get(k) if isinstance(n, dict) else None
        if n is None:
            return None
    m = n.get(mode)
    if m is None and "$value" in n:
        m = n                       # modeless semantic leaf (e.g. DV-D07 data/*/alpha slots)
    v = m.get("$value") if isinstance(m, dict) else m
    if isinstance(v, (int, float)):
        return str(v)               # unitless factor (alpha) — matches gen_snippet_tokens._fmt
    return v.upper() if isinstance(v, str) and v.startswith("#") else None


def theme_block(css, theme):
    m = re.search(r'\[data-theme="%s"\]\s*\{([^}]*)\}' % theme, css)
    return m.group(1) if m else ""


def var_value(block, var, hexonly=True):
    """Declared value of --var in a theme block. hexonly=True (default) keeps the
    original colour-token behaviour; hexonly=False captures any literal value
    (used when the token's canon value is non-hex, e.g. a radius)."""
    m = re.search(re.escape(var) + r'\s*:\s*(#[0-9A-Fa-f]{6,8})', block)
    if m:
        return m.group(1).upper()
    if not hexonly:
        m = re.search(re.escape(var) + r'\s*:\s*([^;]+);', block)
        return m.group(1).strip() if m else None
    return None


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
            canon = resolve(token, mode)
            declared = var_value(block, var,
                                 hexonly=(canon is None or str(canon).startswith("#")))
            if canon is None:
                errors.append(f"{name}: token '{token}' not found in store")
            elif declared is None:
                errors.append(f"{name}: var {var} missing in {mode} block")
            elif declared != canon:
                if mode in drift_allow.get(var, []):
                    warnings.append(f"{name}: ALLOWED drift {var} ({mode}) = {declared} (token {token} = {canon}) — {drift_reason}")
                else:
                    errors.append(f"{name}: DRIFT {var} ({mode}) = {declared} but {token} = {canon}")

    # 2. ARIA — search OUTSIDE the manifest block. A bare declared string (e.g.
    #    "aria-expanded") otherwise matches its own declaration in the manifest
    #    JSON and the check can never fail. (Found by _tests/test_gates.py,
    #    2026-07-02 — the self-test's first real catch.)
    html_sans_manifest = html.replace(mm.group(0), "", 1)
    for need in manifest.get("requiredAria", []):
        if need not in html_sans_manifest:
            errors.append(f"{name}: required ARIA missing: {need}")

    # 3. contrast pairs
    for p in manifest.get("contrastPairs", []):
        ctx = p.get("context", "text")
        # icon-015 PROMOTED blocking 2026-07-02 (Dave: "icons alone should have the
        # small-text equivalent contrast at least"): declared pairs whose fg is an
        # icon/* token are held to 4.5:1 regardless of the declared 'ui' context.
        # Pictograms + RAG graphic indicators (rag/*) stay at 3:1 (roundel policy).
        if p["fg"].startswith("icon/"):
            ctx = "icon"
        for mode in ("light", "dark"):
            fg, bg = resolve(p["fg"], mode), resolve(p["bg"], mode)
            if not fg or not bg:
                errors.append(f"{name}: contrast pair {p['fg']}/{p['bg']} unresolved ({mode})")
                continue
            r = contrast_ratio(fg, bg)
            if not is_sufficient_contrast(r, context=ctx):
                need = 4.5 if ctx in ("text", "icon") else 3.0
                tag = " (icon-015, promoted 2026-07-02)" if ctx == "icon" else ""
                errors.append(f"{name}: CONTRAST {p['fg']} on {p['bg']} ({mode}) = {r}:1 < {need}:1{tag}")

    # 4. ALL-CAPS (PROMOTED advisory → blocking, Dave ruling 2026-07-02; type26-019.
    #    Runs BEFORE the interactive early-return so passive components are covered too.)
    for _ in re.finditer(r'text-transform\s*:\s*uppercase', html, re.I):
        errors.append(f"{name}: ALL-CAPS text-transform:uppercase — banned canon-wide (type26-019, promoted 2026-07-02)")
    vis = re.sub(r'<script.*?</script>', ' ', html, flags=re.S | re.I)
    vis = re.sub(r'<style.*?</style>', ' ', vis, flags=re.S | re.I)
    vis = re.sub(r'<!--.*?-->', ' ', vis, flags=re.S)
    vis = re.sub(r'<[^>]+>', ' ', vis)
    for run in sorted(set(re.findall(r'\b[A-Z]{2,}(?: [A-Z]{2,})+\b', vis))):  # sorted: deterministic (dream-pass v2 P2, 2026-07-26)
        if all(w in ACRONYMS for w in run.split()):
            continue  # acronym-only runs are the brand exemption (type26-019)
        errors.append(f"{name}: ALL-CAPS text run \"{run}\" — banned outside acronyms (type26-019, promoted 2026-07-02)")

    # 6. TYPOGRAPHY (type25-020 — RULED STRAIGHT TO BLOCKING, Dave 2026-07-02.
    #    Brand sources: no-italics + no-text-shadow (2025+2026 typography standards),
    #    red type only for CTA/toolkit roles (col26-016 + type25 red-type rule).
    #    color:var(--error) stays legal — that IS the sanctioned rag/error role route;
    #    this bans the ROLE BYPASS (raw red hex typed onto text).
    #    Runs before the interactive early-return so passive components are covered.)
    for _ in re.finditer(r'font-style\s*:\s*italic', html, re.I):
        errors.append(f"{name}: ITALICS font-style:italic — banned canon-wide (type25-020, blocking 2026-07-02)")
    for m in re.finditer(r'<(i|em)\b', html, re.I):
        errors.append(f"{name}: ITALICS <{m.group(1)}> tag — banned canon-wide (type25-020, blocking 2026-07-02)")
    for _ in re.finditer(r'text-shadow\s*:', html, re.I):
        errors.append(f"{name}: TEXT-SHADOW — banned canon-wide (type25-020, blocking 2026-07-02)")
    for m in re.finditer(r'(?<![-\w])color\s*:\s*#([0-9A-Fa-f]{6})', html):
        if m.group(1).upper() in RED_HEXES:
            errors.append(f"{name}: RED TEXT color:#{m.group(1)} — raw brand red on text; "
                          f"red type only via the rag/error role token or a CTA role "
                          f"(type25-020/col26-016, blocking 2026-07-02)")

    # 7. COPY-LINT (nam-001 + avd-006-prefix + aca-004 — RULED STRAIGHT TO
    #    BLOCKING by Dave 2026-07-03. Overrides advisory-first: exact-match
    #    checks, pre-swept to zero canon signals (type25-020 precedent).
    #    Runs before the interactive early-return so passive components'
    #    alt text is covered too.)
    #    nam-001 — HSBC never possessive with a product/service name: applies
    #    to visible text AND accessible-name attributes.
    attr_copy = re.findall(
        r'\b(?:alt|aria-label|title|placeholder)\s*=\s*"([^"]*)"', html, re.I)
    for surface, t in [("visible text", vis)] + [("attribute copy", a) for a in attr_copy]:
        if re.search(r"\bHSBC[’']s\b", t):
            errors.append(f"{name}: POSSESSIVE \"HSBC's\" in {surface} — brand/product "
                          f"names never take the possessive (nam-001, blocking 2026-07-03)")
    #    avd-006 — alt/aria-label describes purpose, never the element type.
    for m in re.finditer(r'\b(alt|aria-label)\s*=\s*"([^"]*)"', html, re.I):
        if BANNED_ALT_PREFIX.match(m.group(2)):
            errors.append(f"{name}: ALT PREFIX {m.group(1)}=\"{m.group(2)}\" — announce "
                          f"purpose, not element type (avd-006, blocking 2026-07-03)")
    #    aca-004 — link text must describe the target (SC 2.4.4).
    for m in re.finditer(r'<a\b[^>]*>(.*?)</a>', html, re.S | re.I):
        txt = re.sub(r'<[^>]+>', ' ', m.group(1))
        txt = re.sub(r'\s+', ' ', txt).strip().strip('.…!').lower()
        if txt in BARE_LINK_TEXT:
            errors.append(f"{name}: BARE LINK text \"{txt}\" — link text describes the "
                          f"target, not the mechanism (aca-004, blocking 2026-07-03)")

    # 5. focus
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
        lines.append("- token fidelity (light+dark), ARIA, contrast pairs, all-caps, typography, copy-lint, focus — all clean.")
    lines.append("")

open(os.path.join(ROOT, "_SNIPPET-AUDIT.md"), "w").write("\n".join(lines))

print(f"snippet gate: {len(snippets)} snippet(s), {len(all_err)} failure(s)")
for e in all_err:
    print("  ❌", e)
sys.exit(1 if all_err else 0)
