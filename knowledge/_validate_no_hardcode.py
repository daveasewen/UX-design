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
# ⛔ #221 (from #220-L1 finding 12, MUTATION-PROVEN BLIND). The old pattern was
# `border(?:-(?:top|right|bottom|left|width))?` — six literal spellings, and it walked past
# every OTHER way CSS spells a border stroke. Measured on this tree before the change, all
# BLIND: `border-inline-width` · `border-block-start-width` · `border-top-width` ·
# `border-left-width` · `border-inline-start-width` · `border-block-width`. The plain PHYSICAL
# longhands were as invisible as the logical ones, which #220-L1 did not reach — so this hole
# was wider than the finding that opened it. The `SPACING` line directly above ALREADY carried
# the logical longhands, which is what made the omission a slip rather than a policy.
# ⚠ SCOPE, DELIBERATELY UNCHANGED: `outline-offset` stays out. This gate is spacing + radius +
# border-STROKE by its own docstring, and offset is the GEOMETRY axis Dave put on the other side
# of the line. Widening to it would be a scope change, not a repair.
BORDERW = (r'(?:border(?:-(?:top|right|bottom|left|inline|block|'
           r'inline-start|inline-end|block-start|block-end))?(?:-width)?|outline(?:-width)?)')
# ⛔ #221 — same class, the radius arm: `border-radius` alone could not see a single corner
# longhand. Physical (`border-top-left-radius`) and logical (`border-start-start-radius`) are
# both spellings of the same declaration and both walked through. MEASURED on the real
# population (11 icon-manifest pro-formas, 260 `style=""` attributes) BEFORE the change:
# widening all three patterns AND reading style attributes yields **0 new findings**, so this
# repair introduces no red. (`border-top-left-radius:0` carries no `px` and is not this gate's
# business; it is `_validate_radius.py`'s, where it IS a live question — see that file.)
RADIUS = r'(?:border(?:-(?:(?:top|bottom)-(?:left|right)|(?:start|end)-(?:start|end)))?-radius)'

CHECKS = [
    ("spacing", re.compile(r'(?<![-\w])(' + SPACING + r')\s*:\s*([^;{}]*\d+px[^;{}]*)')),
    ("radius",  re.compile(r'(?<![-\w])(' + RADIUS + r')\s*:\s*([^;{}]*\d+px[^;{}]*)')),
    ("border",  re.compile(r'(?<![-\w])(' + BORDERW + r')\s*:\s*([^;{}]*\d+px[^;{}]*)')),
]

def styles(html):
    """Every place a declaration can live in this artefact — `<style>` blocks AND `style=""`.

    ⛔ #221 (from #220-L1 finding 12). This used to read `<style>` blocks ONLY, so
    `<div style="padding:13px;border-radius:7px;border-width:5px">` put three hardcoded values
    through a BLOCKING gate green. DEF-004 exists because *"styling must be a token so MODES can
    override it"* — and a style attribute is the LEAST overridable place in CSS, so the one
    surface the gate could not see was the worst one to miss.
    ⚠ The extraction is not invented here: `_validate_compose.py:57` has read
    `style="([^"]*)"` for as long as it has existed. The fix is to use the reader the tree
    already had, in the gate that needed it.
    ⚠ REGEX, AND HONEST ABOUT IT: this reads double-quoted attributes, like its source. The
    class fix — reading the artefact in its CONSUMER'S grammar rather than with `re` at all
    [[no-gate-parses-the-artefact]] — is `_gate_inline_style_parse.py`, born ADVISORY at #221
    over this same population. It exists precisely because this line is still a pattern.
    """
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)
    attrs = re.findall(r'style="([^"]*)"', html)
    return "\n".join(blocks) + "\n" + "\n".join(a.strip().rstrip(";") + ";" for a in attrs)

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


# ── KNOWN-ANSWER TEST (#221) ──────────────────────────────────────────────────────────────
# ⛔ WHY THIS DID NOT EXIST UNTIL NOW, WHICH IS THE REAL FINDING. #220-L1 counted 26
# BLOCKING-routed scripts with no known-answer test that actually runs; it planted defects in
# two of them and BOTH turned out to be blind. This was one of the two. A gate with no bite is
# not a gate that might be blind — it is a gate whose blindness nobody can be told about.
# ⚠ EVERY CASE IS A PAIR, BOTH DIRECTIONS DRIVEN [[mutation-tests-the-clause-not-the-feature]]:
# the FIRES list plants the defect and demands a finding; the SILENT list is the discrimination
# control and demands none. A gate that fires on everything is as useless as one that fires on
# nothing, and only the second list can tell them apart.
# ⚠ WRITES NOTHING. `main()` rewrites the tracked `_NO-HARDCODE-GATE.md`; this arm returns
# before it, so the selftest cannot be the #158 write-by-default door in a new place.
FIRES = [
    # (name, artefact fragment, how many findings at minimum) — #220-L1 finding 12's own mutants first
    ("B1 control — plain border-width in <style> (the shape that ALWAYS fired)",
     "<style>.l1probe{border-width:3px}</style>", 1),
    ("B2 — logical border-inline-width (L1 mutant, was BLIND)",
     "<style>.l1probe{border-inline-width:3px}</style>", 1),
    ("B3 — logical border-block-start-width (L1 mutant, was BLIND)",
     "<style>.l1probe{border-block-start-width:3px}</style>", 1),
    ("B4 — three hardcodes in ONE style attribute (L1 mutant, the gate could not see attributes AT ALL)",
     '<div style="padding:13px;border-radius:7px;border-width:5px">x</div>', 3),
    # found by #221's own replay — the PHYSICAL longhands were blind too, which L1 did not reach
    ("B5 — physical border-top-width (#221 replay, was BLIND)",
     "<style>.l1probe{border-top-width:3px}</style>", 1),
    ("B6 — physical corner radius longhand (#221 replay, was BLIND)",
     "<style>.l1probe{border-top-left-radius:7px}</style>", 1),
    ("B7 — logical corner radius longhand (#221 replay, was BLIND)",
     "<style>.l1probe{border-start-start-radius:7px}</style>", 1),
    ("B8 — a hardcode in an attribute on a SVG element, no <style> block in the file at all",
     '<svg><rect style="margin-inline-start:9px"/></svg>', 1),
]
SILENT = [
    ("C1 — the token route, which is the whole point of DEF-004",
     "<style>.ok{border-width:var(--bw-1);padding:var(--space-2)}</style>"),
    ("C2 — px inside a var() fallback is allowed by the docstring",
     "<style>.ok{padding:var(--space-2, 8px);border-inline-width:var(--bw-1, 1px)}</style>"),
    ("C3 — a token DEFINITION is the source of truth, not a hardcode",
     "<style>:root{--border-inline-width:3px;--border-top-left-radius:7px;--padding-x:13px}</style>"),
    # ⚠ THIS CONTROL BIT ITS AUTHOR FIRST. Its first draft carried a real
    # `border-inline-width:3px` beside the transparent border and the gate flagged it — correctly.
    # The fixture was wrong, not the gate, and it is recorded because a control that "fails" is
    # the moment you find out which of the two you are actually testing.
    ("C4 — a transparent border is a CSS-triangle shape, not a stroke",
     "<style>.ok{border:3px solid transparent;border-inline-start:2px solid transparent}</style>"),
    ("C5 — geometry / dimensions are the OTHER axis, expressly not flagged",
     "<style>.ok{width:13px;height:4px;top:8px;font-size:12px;outline-offset:3px}</style>"),
    ("C6 — a @media breakpoint is not styling",
     "<style>@media (min-width: 720px){.ok{color:red}}</style>"),
    ("C7 — a style attribute carrying only a token",
     '<div style="color:var(--text-primary);padding:var(--space-2)">x</div>'),
    # the discrimination control with TEETH: it carries px, so a sloppier widening (anything
    # starting `border-`, or a reach into shadows) would light it up. box-shadow is neither a
    # stroke nor spacing nor radius, and must stay out.
    ("C8 — the widened border pattern must not swallow border-COLOUR, border-STYLE or box-shadow",
     "<style>.ok{border-block-start-color:#0af;border-inline-style:solid;box-shadow:0 0 0 3px #0af}</style>"),
]


def selftest():
    import tempfile
    fails = []
    def run(fragment):
        d = tempfile.mkdtemp(prefix="nohardcode-selftest-")   # ⚠ scratch, never the repo
        p = os.path.join(d, "probe.html")
        open(p, "w").write("<html><body>%s</body></html>" % fragment)
        try:
            return check_file(p)
        finally:
            os.remove(p); os.rmdir(d)
    for name, frag, least in FIRES:
        got = run(frag)
        if len(got) < least:
            fails.append("PLANTED DEFECT NOT CAUGHT — %s (wanted >=%d finding(s), got %d: %s)"
                         % (name, least, len(got), got))
    for name, frag in SILENT:
        got = run(frag)
        if got:
            fails.append("CLEAN INPUT FLAGGED — %s (got %d finding(s): %s)" % (name, len(got), got))
    return fails


def main():
    if "--selftest" in sys.argv:
        f = selftest()
        print("no-hardcode gate selftest — %d planted defect(s) must fire, %d clean input(s) must not"
              % (len(FIRES), len(SILENT)))
        if f:
            print("❌ _validate_no_hardcode SELFTEST FAIL:")
            for x in f:
                print("   X " + x)
            return 1
        print("✅ selftest OK — %d bite(s), both directions driven; nothing written." % (len(FIRES) + len(SILENT)))
        return 0

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
