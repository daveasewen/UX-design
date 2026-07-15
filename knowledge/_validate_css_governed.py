#!/usr/bin/env python3
"""DEF-003 — motion/styling is CSS + TOKEN governed, NOT JS-driven.

Dave 2026-07-15: "as little JS as possible; CSS and tokens should govern everything —
motion, spacing, etc." The library must be PORTABLE (and transferable to Figma, where
tokens map to variables but JS logic does not). This gate flags the `sizeScale` class of
anti-pattern: JS that computes element scale, sets the --hs/--ps motion vars, or assigns
transform:scale. JS for genuine BEHAVIOUR (open/close, validation) and data-driven values
(a progress bar's width, a ring's offset) is fine — only motion-in-JS is flagged.

Auto-discovers knowledge/_proforma/*.html; writes _CSS-GOVERNED-GATE.md; exits non-zero on any fail."""
import re, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROFORMA = os.path.join(HERE, "_proforma")

PATTERNS = [
    (r'\bsizeScale\b', "JS sizeScale() helper computing button motion"),
    (r"""setProperty\(\s*['"]--hs['"]""", "JS setting the --hs motion variable"),
    (r"""setProperty\(\s*['"]--ps['"]""", "JS setting the --ps motion variable"),
    (r"""\.style\.transform\s*=\s*['"][^'"]*scale""", "JS assigning a transform:scale (motion belongs in CSS)"),
]

def script_text(html):
    # behaviour scripts only — skip the JSON icon-manifest block
    return "\n".join(re.findall(r"<script(?![^>]*application/json)[^>]*>(.*?)</script>", html, re.S))

def check_file(path):
    js = script_text(open(path).read())
    fails = []
    for pat, msg in PATTERNS:
        if re.search(pat, js):
            fails.append("DEF-003: %s — move it to CSS scale-factor tokens (--btn-grow/--btn-press, --ib-grow/--ib-press)" % msg)
    return fails

def main():
    files = sorted(f for f in glob.glob(os.path.join(PROFORMA, "*.html")) if 'id="icon-manifest"' in open(f).read())
    lines = ["# CSS-governed motion gate — DEF-003", ""]
    any_fail = False
    for p in files:
        name = os.path.relpath(p, HERE)
        fails = check_file(p)
        status = "PASS" if not fails else "FAIL"
        if fails:
            any_fail = True
        print("  [%s] %s" % (status, name))
        lines.append("## %s %s — %s" % ("✓" if not fails else "✗", name, status))
        for f in fails:
            print("     -", f)
            lines.append("- ✗ " + f)
        lines.append("")
    lines += ["---", "Rule: motion/spacing/styling is CSS + token governed; JS is behaviour-only (portability + Figma transfer)."]
    open(os.path.join(HERE, "_CSS-GOVERNED-GATE.md"), "w").write("\n".join(lines) + "\n")
    if any_fail:
        print("\n❌ CSS-governed gate FAILED — styling is JS-driven; see knowledge/_CSS-GOVERNED-GATE.md")
        return 1
    print("\n✅ CSS-governed gate passed (%d tranche file(s))." % len(files))
    return 0

if __name__ == "__main__":
    sys.exit(main())
