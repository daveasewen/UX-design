#!/usr/bin/env python3
"""
_validate_a11y.py — accessibility enforcement gate for gated reference snippets.

Verification = enforcement (not a nudge). This gate fails the build when a snippet
regresses on a deterministic, statically-checkable WCAG criterion:

  FAIL (gating):
    * 2.3.3 / motion sensitivity — any snippet that animates (transition/animation/
      @keyframes) MUST carry a `prefers-reduced-motion: reduce` block. A canonical
      reference that animates with no reduced-motion escape hatch is a defect.

  WARN (reported, non-gating — needs a human/visual call):
    * 2.5.8 Target Size (Minimum, AA) — interactive controls (button / a[href] /
      [role=button|switch|tab|option]) whose CSS box is < 24×24px and which do NOT
      expand their hit area with a ::before/::after overlay. Decorative inner glyphs
      (.dot/.thumb/svg) are excluded; this only flags the focusable element itself.

Writes _A11Y-GATE.md and exits non-zero iff there is >=1 FAIL.
"""
import re, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")

MOTION = re.compile(r'transition\s*:|animation\s*:|@keyframes', re.I)
# selectors that denote the focusable control itself (not a decorative child)
CTRL = re.compile(r'(^|[\s,>])(button|a\.[\w-]+|\.x|\.close|\.clear|\.trigger|\.moves\s+button|\.handle|\.page|\.step)\b', re.I)
DECOR = re.compile(r'(svg|\.dot|\.thumb|\.bar\b|::before|::after)', re.I)

def css_blocks(s):
    for m in re.finditer(r'([.#][\w.\-:\s>+]+)\{([^}]*)\}', s):
        yield m.group(1).strip(), m.group(2)

def check(fp):
    s = open(fp).read()
    name = os.path.basename(fp).replace('.reference.html', '')
    fails, warns = [], []

    if MOTION.search(s) and 'prefers-reduced-motion' not in s:
        fails.append("animates but has no `prefers-reduced-motion: reduce` block (2.3.3)")

    has_expander = '::before' in s or '::after' in s
    for sel, body in css_blocks(s):
        if not CTRL.search(sel) or DECOR.search(sel):
            continue
        w = re.search(r'(?<![\w-])width\s*:\s*(\d+)px', body)
        h = re.search(r'(?<![\w-])height\s*:\s*(\d+)px', body)
        if w and h and int(w.group(1)) < 24 and int(h.group(1)) < 24:
            # does THIS selector have an explicit hit-area expander nearby?
            expanded = re.search(re.escape(sel) + r'\s*::(before|after)', s)
            if not expanded:
                warns.append(f"`{sel}` is {w.group(1)}×{h.group(1)}px (<24, 2.5.8) — add a ::before hit-area expander or enlarge")
    return name, fails, warns

def main():
    rows = [check(fp) for fp in sorted(glob.glob(os.path.join(SNIP, "*.reference.html")))]
    nfail = sum(len(f) for _, f, _ in rows)
    nwarn = sum(len(w) for _, _, w in rows)

    lines = ["# A11y gate — _validate_a11y.py", "",
             f"**{len(rows)} snippet(s)** · **{nfail} failure(s)** · **{nwarn} warning(s)**",
             "", "Gating: reduced-motion (2.3.3). Reported: target size (2.5.8).", ""]
    for name, fails, warns in rows:
        if not fails and not warns:
            continue
        lines.append(f"## {name}")
        for f in fails:
            lines.append(f"- 🔴 FAIL — {f}")
        for w in warns:
            lines.append(f"- 🟡 warn — {w}")
        lines.append("")
    if nfail == 0 and nwarn == 0:
        lines.append("_No issues._")
    open(os.path.join(HERE, "_A11Y-GATE.md"), "w").write("\n".join(lines) + "\n")

    print(f"a11y gate: {len(rows)} snippet(s), {nfail} failure(s), {nwarn} warning(s)")
    if nfail:
        for name, fails, _ in rows:
            for f in fails:
                print(f"  FAIL {name}: {f}")
    sys.exit(1 if nfail else 0)

if __name__ == "__main__":
    main()
