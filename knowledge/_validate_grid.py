#!/usr/bin/env python3
"""_validate_grid.py — the 4px-grid gate (DEF-005).

Forces every *layout* dimension to a 4px multiple. Grid-governed properties
(height, min/max-height, margin*, padding*, gap/row-gap/column-gap, top, bottom,
line-height, text-indent) must resolve to whole 4px multiples in px.

Sanctioned grid = 4n + 2px half-step (Dave 2026-07-17). 1px = hairline/border only.

EXEMPT (not grid rhythm):
  - font-size, letter-spacing, border-width/border, border-radius, outline*,
    box-shadow, transform, and anything inside @font-face (glyph/hairline business).
  - 1px & 3px hairlines (dividers, focus rings, optical offsets) — Dave rule 2.
  - negative values (overlap / pull offsets — positioning, not rhythm).
  - a height that EQUALS a width in the same rule = an intrinsic square size
    (icon / avatar / spinner / media), governed by icon-scale, not layout — like
    font-size. Snapping only the height would distort the aspect ratio.

Non-px units (em/rem/%/vh/ch/calc()/var()) are skipped — can't be checked statically;
keep layout values in px tokens so the grid is enforceable.

Usage:  python3 knowledge/_validate_grid.py <file.css|file.html> [more ...]
        python3 knowledge/_validate_grid.py --selftest
        python3 knowledge/_validate_grid.py            # DEF-005 build mode: gate DEFAULT_TARGETS
Exit non-zero on any violation (blocking). Wired into _build_all.py as DEF-005.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re, sys, os, glob

GRID = 4
HALF_STEP = {2.0}          # 2px half-step allowed for spacing
HAIRLINE = {1.0, 3.0}      # 1/3px hairline/optical — exempt (rule 2)
HEIGHTS = {"height", "min-height", "max-height"}
GRID_PROPS = {
    "height","min-height","max-height",
    "margin","margin-top","margin-bottom","margin-left","margin-right","margin-block","margin-inline",
    "padding","padding-top","padding-bottom","padding-left","padding-right","padding-block","padding-inline",
    "gap","row-gap","column-gap","top","bottom","text-indent",
    "line-height",  # unitless line-height is fine; px line-height must be on grid
}
PX = re.compile(r"(-?\d*\.?\d+)px")
BLOCK = re.compile(r"([^{}]*)\{([^{}]*)\}")
DECL = re.compile(r"([\w-]+)\s*:\s*([^;{}]+)")

def strip_font_face(css: str) -> str:
    return re.sub(r"@font-face\s*\{.*?\}", "", css, flags=re.S)

def _scan_body(body, name, viol):
    """Check one rule body's declarations, exempting squares/hairlines/negatives."""
    widths = set()
    for wm in re.finditer(r"(?:min-|max-)?width\s*:\s*([^;{}]+)", body):
        for x in PX.findall(wm.group(1)):
            widths.add(float(x))
    for m in DECL.finditer(body):
        prop, val = m.group(1).strip().lower(), m.group(2)
        if prop not in GRID_PROPS or "calc(" in val or "var(" in val:
            continue
        for num in PX.findall(val):
            f = float(num)
            if abs(f % GRID) < 1e-6 or f in HALF_STEP:
                continue
            if abs(f) in HAIRLINE or f < 0:
                continue
            if prop in HEIGHTS and f in widths:
                continue  # intrinsic square size
            viol.append((prop, num + "px", name))

def check(css: str, name: str):
    css = strip_font_face(css)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    viol = []
    for bm in BLOCK.finditer(css):
        _scan_body(bm.group(2), name, viol)
    return viol

def read_css(p):
    """CSS files: whole text. HTML: <style> blocks + inline style="" only (never <script>)."""
    t = open(p).read()
    if not p.lower().endswith((".html", ".htm")):
        return t
    parts = re.findall(r"<style[^>]*>(.*?)</style>", t, flags=re.S | re.I)
    # inline styles as pseudo-rules so _scan_body sees them (fast: no brace backtracking)
    parts += ["._inl{%s}" % s for s in re.findall(r'style="([^"]*)"', t)]
    return "\n".join(parts)

def run(paths):
    total = []
    for p in paths:
        try:
            css = read_css(p)
        except OSError as e:
            print(f"  ! cannot read {p}: {e}"); total.append((p, "", "")); continue
        v = check(css, os.path.relpath(p))
        for prop, badval, where in v:
            print(f"  ✗ off-grid: {prop}: {badval}  ({where}) — not a {GRID}px multiple")
        total += v
    if total:
        print(f"\nGRID GATE FAIL — {len(total)} off-grid layout value(s).")
        return 1
    print(f"GRID GATE PASS — all layout dimensions on the {GRID}px grid ({len(paths)} file(s)).")
    return 0

def selftest():
    ok = ".a{min-height:20px;padding:8px 16px;gap:2px;line-height:24px;font-size:14px;letter-spacing:0.5px;border-radius:6px;}"
    bad = ".b{min-height:18px;padding:7px;}"
    sq = ".i{width:22px;height:22px;} .d{height:1px;} .n{margin:-6px;}"  # square/hairline/negative all exempt
    assert check(ok, "ok") == [], "clean case should pass"
    v = check(bad, "bad"); props = sorted(p for p, _, _ in v)
    assert props == ["min-height", "padding"], v
    assert check(sq, "sq") == [], f"square/hairline/negative must be exempt, got {check(sq,'sq')}"
    print("selftest OK — exempts font-size/letter/radius + hairline(1/3)/negative/square; catches off-grid height/padding.")
    return 0

HERE = os.path.dirname(os.path.abspath(__file__))
# Files that MUST be on-grid today (scanned in DEF-005 build mode). Grew 2026-07-17
# after the retrofit snapped the library + the arrow asset was retired.
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
