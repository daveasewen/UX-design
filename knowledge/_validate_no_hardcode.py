#!/usr/bin/env python3
"""DEF-004 — no hardcoded STYLING in component CSS; everything is a token (mode-governed).

Dave 2026-07-15 (FOUNDATIONAL): "we shouldn't hard code any styling going forward, must be tokenised
and all the sibling libraries [Apollo mono/UI/SC] should be governed by modes ... very flexible and
future-proof." STYLING here = spacing (padding/margin/gap), border-radius, and border-STROKE width —
each must be a var() token, never a raw px, so a MODE can override it. Colour has its own hardcode
check (universal gate); motion has DEF-003.

NOT flagged (a separate axis, per Dave): geometry / component dimensions (width/height/font-size/
top/left), @media breakpoints, transparent borders (CSS-triangle shapes), and token DEFINITIONS
(`--name:value`, the source of truth). px allowed only inside a var() fallback (`var(--x, 8px)`).

Auto-discovers knowledge/_proforma/*.html (icon-manifest ones); writes _NO-HARDCODE-GATE.md; exits non-zero on any fail."""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROFORMA = os.path.join(HERE, "_proforma")

SPACING = r'(?:padding|margin|gap|row-gap|column-gap)(?:-(?:top|right|bottom|left|inline|block|inline-start|inline-end|block-start|block-end))?'
BORDERW = r'(?:border(?:-(?:top|right|bottom|left|width))?|outline(?:-width)?)'

CHECKS = [
    ("spacing", re.compile(r'(?<![-\w])(' + SPACING + r')\s*:\s*([^;{}]*\d+px[^;{}]*)')),
    ("radius",  re.compile(r'(?<![-\w])(border-radius)\s*:\s*([^;{}]*\d+px[^;{}]*)')),
    ("border",  re.compile(r'(?<![-\w])(' + BORDERW + r')\s*:\s*([^;{}]*\d+px[^;{}]*)')),
]

def styles(html):
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))

def check_file(path):
    css = styles(open(path).read())
    fails = []
    for kind, rx in CHECKS:
        for m in rx.finditer(css):
            prop, val = m.group(1), m.group(2).strip()
            # px only inside a var() fallback is fine
            if not re.search(r'\d+px', re.sub(r'var\([^)]*\)', '', val)):
                continue
            # geometry exception: transparent border = CSS-triangle / invisible shape, not a stroke
            if kind == "border" and "transparent" in val:
                continue
            fails.append("DEF-004 [%s]: `%s:%s` — raw px; use a token (--space-*, --bw-*, --radius*)" % (kind, prop, val))
    return fails

def main():
    files = sorted(f for f in glob.glob(os.path.join(PROFORMA, "*.html")) if 'id="icon-manifest"' in open(f).read())
    lines = ["# No-hardcode styling gate — DEF-004", "",
             "Styling (spacing / radius / border-stroke) must be a token so MODES (Apollo mono/UI/SC) can override it.",
             "Geometry/dimensions, @media breakpoints, transparent borders, and token definitions are a separate axis (not flagged).", ""]
    any_fail = False
    for p in files:
        name = os.path.relpath(p, HERE)
        fails = check_file(p)
        if fails:
            any_fail = True
        print("  [%s] %s" % ("PASS" if not fails else "FAIL", name))
        lines.append("## %s %s — %s" % ("✓" if not fails else "✗", name, "PASS" if not fails else "FAIL"))
        for f in fails:
            print("     -", f)
            lines.append("- ✗ " + f)
        lines.append("")
    lines += ["---", "Rule 15 in `_proforma/_PROFORMA-RULES.md`. Sibling companions: motion = DEF-003, colour = universal-gate hardcode check."]
    open(os.path.join(HERE, "_NO-HARDCODE-GATE.md"), "w").write("\n".join(lines) + "\n")
    if any_fail:
        print("\n❌ No-hardcode gate FAILED — styling is hardcoded; see knowledge/_NO-HARDCODE-GATE.md")
        return 1
    print("\n✅ No-hardcode gate passed (%d tranche file(s))." % len(files))
    return 0

if __name__ == "__main__":
    sys.exit(main())
