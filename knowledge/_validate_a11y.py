#!/usr/bin/env python3
"""
_validate_a11y.py — accessibility enforcement gate for gated reference snippets.

Verification = enforcement (not a nudge). This gate fails the build when a snippet
regresses on a deterministic, statically-checkable WCAG criterion:

  FAIL (gating):
    * 2.3.3 / motion sensitivity — any snippet that animates (transition/animation/
      @keyframes) MUST carry a `prefers-reduced-motion: reduce` block. A canonical
      reference that animates with no reduced-motion escape hatch is a defect.

    * 2.5.8 Target Size (Minimum, AA) — interactive controls (button / a[href] /
      [role=button|switch|tab|option]) with a declared CSS box under 24px in EITHER
      dimension and no ::before/::after hit-area expander for that selector.
      PROMOTED from warn tier by the aid-009 ruling (Dave, 2026-07-03): 24 is the
      hard floor. (Was AND-semantics <24×24; EITHER-dimension is the SC's reading.)

  WARN (reported, non-gating — needs a human/visual call):
    * target size < 44 — the HSBC DEFAULT is 44×44 (ID-26 + axs-003 "existing 44×44
      guidance takes priority"; 24 is the exception tier, not the goal). Advisory
      per the same aid-009 ruling: signal 24–43, promotion only with the exception
      outs (spacing/equivalent/inline/UA/essential) modelled. Decorative inner
      glyphs (.dot/.thumb/svg) are excluded; only the focusable element flags.

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

    for sel, body in css_blocks(s):
        if not CTRL.search(sel) or DECOR.search(sel):
            continue
        w = re.search(r'(?<![\w-])width\s*:\s*(\d+)px', body)
        h = re.search(r'(?<![\w-])height\s*:\s*(\d+)px', body)
        if not (w and h):
            continue
        wv, hv = int(w.group(1)), int(h.group(1))
        # an explicit hit-area expander for THIS selector exempts both tiers
        # (static CSS can't size the expander; the render axis owns that check)
        if re.search(re.escape(sel) + r'\s*::(before|after)', s):
            continue
        if min(wv, hv) < 24:
            fails.append(f"`{sel}` is {wv}×{hv}px (<24 floor, 2.5.8) — add a ::before hit-area expander or enlarge (aid-009)")
        elif min(wv, hv) < 44:
            warns.append(f"`{sel}` is {wv}×{hv}px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out")
    return name, fails, warns

def main():
    rows = [check(fp) for fp in sorted(glob.glob(os.path.join(SNIP, "*.reference.html")))]
    nfail = sum(len(f) for _, f, _ in rows)
    nwarn = sum(len(w) for _, _, w in rows)

    lines = ["# A11y gate — _validate_a11y.py", "",
             f"**{len(rows)} snippet(s)** · **{nfail} failure(s)** · **{nwarn} warning(s)**",
             "", "Gating: reduced-motion (2.3.3) · target size <24 floor (2.5.8, aid-009 ruling 2026-07-03). "
             "Reported: target size 24–43 vs the 44×44 HSBC default (aid-009).", "",
             "Library bar (aqa-003, ruled 2026-07-03): the canon is LIBRARY-GRADE — guideline "
             "and recommendation tiers bind it, not just standards.", ""]
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
