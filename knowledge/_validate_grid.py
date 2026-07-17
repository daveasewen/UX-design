#!/usr/bin/env python3
"""_validate_grid.py — the 4px-grid gate.

Forces every *layout* dimension to a 4px multiple. Grid-governed properties
(height, min/max-height, margin*, padding*, gap/row-gap/column-gap, top, bottom,
line-height, text-indent) must resolve to whole 4px multiples in px.

EXEMPT (not grid-governed): font-size, letter-spacing, border-width/border,
border-radius, outline*, box-shadow, transform, and anything inside @font-face.
Font glyph size is the type's business; the grid governs the boxes and the space
between them — which is exactly the vertical-stack rhythm the trimmed type needs.

Non-px units (em/rem/%/vh/ch/calc()) are skipped — they can't be checked statically;
keep layout values in px tokens so the grid is enforceable.

Usage:  python3 knowledge/_validate_grid.py knowledge/canon/type.css [more.css ...]
        python3 knowledge/_validate_grid.py --selftest
Exit non-zero on any violation (blocking). Wire into _build_all.py as DEF-005.
"""
import re, sys

GRID = 4
# Sanctioned subdivisions of the base unit for *spacing* (Dave 2026-07-17):
# 2px half-step is allowed. 1px quarter-step is NOT allowed as spacing — 1px is a
# hairline/border value, and border-width is already exempt below; allowing 1px here
# would let every integer pass and neuter the gate.
HALF_STEP = {2.0}
GRID_PROPS = {
    "height","min-height","max-height",
    "margin","margin-top","margin-bottom","margin-left","margin-right","margin-block","margin-inline",
    "padding","padding-top","padding-bottom","padding-left","padding-right","padding-block","padding-inline",
    "gap","row-gap","column-gap","top","bottom","text-indent",
    "line-height",  # unitless line-height is fine; px line-height must be on grid
}
PX = re.compile(r"(-?\d*\.?\d+)px")

def strip_font_face(css: str) -> str:
    # remove @font-face{...} blocks (base64 src, metrics) from the check
    return re.sub(r"@font-face\s*\{.*?\}", "", css, flags=re.S)

def check(css: str, name: str):
    css = strip_font_face(css)
    # drop comments
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    viol = []
    # walk declarations: prop : value ;
    for m in re.finditer(r"([\w-]+)\s*:\s*([^;{}]+)", css):
        prop, val = m.group(1).strip().lower(), m.group(2)
        if prop not in GRID_PROPS:
            continue
        if "calc(" in val or "var(" in val:
            continue  # can't resolve statically; assume token-governed
        for num in PX.findall(val):
            f = float(num)
            if abs(f % GRID) < 1e-6 or f in HALF_STEP:
                continue
            viol.append((prop, num + "px", f"{name}"))
    return viol

def run(paths):
    total = []
    for p in paths:
        try:
            css = open(p).read()
        except OSError as e:
            print(f"  ! cannot read {p}: {e}"); total.append((p,"",""))
            continue
        v = check(css, p)
        for prop, badval, where in v:
            print(f"  ✗ off-grid: {prop}: {badval}  ({where}) — not a {GRID}px multiple")
        total += v
    if total:
        print(f"\nGRID GATE FAIL — {len(total)} off-grid layout value(s).")
        return 1
    print(f"GRID GATE PASS — all layout dimensions on the {GRID}px grid.")
    return 0

def selftest():
    ok = ".a{min-height:20px;padding:8px 16px;gap:2px;line-height:24px;font-size:14px;letter-spacing:0.5px;border-radius:6px;}"
    bad = ".b{min-height:18px;padding:7px;}"  # 18, 7 off-grid; 2px half-step/radius/font-size exempt
    assert check(ok, "ok") == [], "clean case should pass (2px half-step + font-size/letter/radius exempt)"
    v = check(bad, "bad"); props = sorted(p for p,_,_ in v)
    assert props == ["min-height","padding"], v
    print("selftest OK — exempts font-size/letter-spacing/border-radius; catches off-grid height/padding.")
    return 0

import os
# Files that MUST be on-grid today (scanned when the gate runs with no args, e.g.
# as DEF-005 in _build_all.py). Grows as the retrofit (task #9) snaps canon.css +
# proforma tranches onto the grid; add them here once clean so regressions gate.
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TARGETS = [os.path.join(HERE, "canon", "type.css")]

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        sys.exit(selftest())
    if args:
        sys.exit(run(args))
    # no args → DEF-005 build mode: selftest, then gate the canonical on-grid set
    rc = selftest()
    rc = run([p for p in DEFAULT_TARGETS if os.path.exists(p)]) or rc
    sys.exit(rc)
