#!/usr/bin/env python3
"""_validate_descender_clip.py — the descender-clip gate (ds-005).

WHY THIS EXISTS
---------------
The canon leading-trim strategy applies `text-box-trim:trim-both; text-box-edge:cap alphabetic`
to label elements. `cap alphabetic` trims the box to the cap-height…baseline span — which is
exactly what optically centres a label against an adjacent icon/dot. BUT when that same label
ALSO truncates (`overflow:hidden` + `text-overflow:ellipsis`), the descender (g/y/p/q) sits
*below* the alphabetic baseline — outside the trimmed box — and is CLIPPED. Render-confirmed
2026-07-19: "Savings" renders "Savin*q*s" on the Masthead dropdown title.

THE RULE (universal, so nobody has to remember the decision tree):
  Every rule that TRUNCATES a text label (`text-overflow:ellipsis`) must ALSO carry the
  descender-safe override on the same selector — `text-box-edge:text text` (full glyph box,
  keeps the ellipsis, descenders survive) OR `overflow:visible` (short atoms; no ellipsis).
  Applying `text-box-edge:text text` to a label that isn't trimmed is a harmless no-op
  (text-box-edge does nothing without text-box-trim), so the rule is safe everywhere.

`text-overflow:ellipsis` is the high-precision signal for "visible truncating text label":
sr-only patterns use `clip:rect(...)` not ellipsis; layout containers (.note/.track/.player/
.panel/avatar) use `overflow:hidden` WITHOUT ellipsis. So this gate has no known false positives.

Ruling: ds-005 decision-tree extension (knowledge/_DS-IMPROVEMENTS.md), Dave 2026-07-19
("do it right — gate it, keep cap alphabetic as the default").

⚠️ TO A FUTURE SESSION — the scattered `text-box-edge:text text` overrides on truncating
labels are NOT a bug and NOT a stray inconsistency to "clean up". They ARE the ds-005 fix; each
one prevents a real, render-confirmed descender clip. Removing one is the exact regression this
gate exists to catch — the build will go red and point you straight back here. Do not design a
"fix". CONSULT first (`python3 knowledge/_consult.py "descender clip"`).

Usage:  python3 knowledge/_validate_descender_clip.py <file.css|file.html> [more ...]
        python3 knowledge/_validate_descender_clip.py --selftest
        python3 knowledge/_validate_descender_clip.py         # build mode: gate DEFAULT_TARGETS
Exit non-zero on any un-overridden truncating label (blocking). Wired into _build_all.py.
"""
import re, sys, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))

RULE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
ELLIPSIS = re.compile(r"text-overflow\s*:\s*ellipsis", re.I)
OVR_TEXTBOX = re.compile(r"text-box-edge\s*:\s*text\s+text", re.I)
OVR_VISIBLE = re.compile(r"overflow\s*:\s*visible", re.I)


def _norm(sel: str) -> str:
    """Normalise one selector for comparison: collapse whitespace, strip."""
    return re.sub(r"\s+", " ", sel).strip()


def _selectors(sel_group: str):
    """Split a comma selector list into normalised parts."""
    return [_norm(s) for s in sel_group.split(",") if _norm(s)]


def read_css(path: str) -> str:
    """CSS from a .css file, or the concatenated <style> blocks of an .html file.
    Inline style="" attributes are intentionally NOT scanned — the override is a
    companion class rule, which an inline style cannot carry."""
    with open(path, encoding="utf-8") as f:
        t = f.read()
    if not path.endswith((".css",)):
        t = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", t, flags=re.S | re.I))
    # Strip CSS comments so they can't glue onto the following selector.
    return re.sub(r"/\*.*?\*/", "", t, flags=re.S)


def check(css: str, where: str):
    """Return a list of (selector, where) for truncating labels lacking the override."""
    # Pass 1 — collect every selector that HAS a descender-safe override anywhere in the file.
    covered = set()
    for m in RULE.finditer(css):
        body = m.group(2)
        if OVR_TEXTBOX.search(body) or OVR_VISIBLE.search(body):
            for s in _selectors(m.group(1)):
                covered.add(s)
    # Pass 2 — every truncating rule must have all its selectors covered.
    viol = []
    for m in RULE.finditer(css):
        sel_group, body = m.group(1), m.group(2)
        if not ELLIPSIS.search(body):
            continue
        # a rule that truncates AND carries its own override is fine
        if OVR_TEXTBOX.search(body) or OVR_VISIBLE.search(body):
            continue
        for s in _selectors(sel_group):
            if s not in covered:
                viol.append((s, where))
    return viol


def run(paths):
    total = []
    for p in paths:
        try:
            css = read_css(p)
        except OSError as e:
            print(f"  ! cannot read {p}: {e}"); total.append(("<unreadable>", p)); continue
        v = check(css, os.path.relpath(p))
        for sel, where in v:
            print(f"  ✗ truncating label without descender-safe override: "
                  f"`{sel}` ({where}) — add `{sel}{{text-box-edge:text text;}}` (ds-005)")
        total += v
    if total:
        print(f"\nDESCENDER-CLIP GATE FAIL — {len(total)} truncating label(s) will clip descenders "
              f"(g/y/p/q). Add `text-box-edge:text text` to each. See knowledge/_DS-IMPROVEMENTS.md ds-005.")
        return 1
    print(f"DESCENDER-CLIP GATE PASS — every truncating label is descender-safe ({len(paths)} file(s)).")
    return 0


def selftest():
    clips = ".a{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}"
    fixed = clips + "\n.a{text-box-edge:text text;}"
    fixed_inline = ".b{overflow:hidden;text-overflow:ellipsis;text-box-edge:text text;}"
    fixed_group = (".c .x{overflow:hidden;text-overflow:ellipsis;}\n"
                   ".d .y{overflow:hidden;text-overflow:ellipsis;}\n"
                   ".c .x, .d .y{text-box-edge:text text;}")
    visible_ok = ".e{text-overflow:ellipsis;overflow:visible;}"
    container = ".note{overflow:hidden;padding:12px;}"        # no ellipsis -> not a label -> ignored
    sronly = ".sr{overflow:hidden;white-space:nowrap;clip:rect(0 0 0 0);}"  # no ellipsis -> ignored
    assert [s for s, _ in check(clips, "t")] == [".a"], check(clips, "t")
    assert check(fixed, "t") == [], "companion override should pass"
    assert check(fixed_inline, "t") == [], "same-rule override should pass"
    assert check(fixed_group, "t") == [], f"comma-group override should cover both, got {check(fixed_group,'t')}"
    assert check(visible_ok, "t") == [], "overflow:visible is a valid override"
    assert check(container, "t") == [], "non-ellipsis container must be ignored"
    assert check(sronly, "t") == [], "sr-only (clip:rect, no ellipsis) must be ignored"
    print("selftest OK — flags un-overridden ellipsis labels; accepts text-text / overflow-visible / "
          "same-rule / comma-group overrides; ignores containers + sr-only.")
    return 0


# Files whose truncating labels MUST be descender-safe today (build mode).
DEFAULT_TARGETS = (
    [os.path.join(HERE, "canon", "type.css"),
     os.path.join(HERE, "canon", "canon.css")]
    + sorted(glob.glob(os.path.join(HERE, "snippets", "*.html")))
    + sorted(glob.glob(os.path.join(HERE, "_proforma", "*.html")))
)

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        sys.exit(selftest())
    if args:
        sys.exit(run(args))
    rc = selftest()
    rc = run([p for p in DEFAULT_TARGETS if os.path.exists(p)]) or rc
    sys.exit(rc)
