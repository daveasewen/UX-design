#!/usr/bin/env python3
"""
Icon-source GATE — guards against invented icons (promoted from advisory 2026-06-24).

Why (Dave, 2026-06-22): an AI model building a snippet can hand-draw an SVG that *looks* like an
icon instead of using the real HSBC library glyph — a silent fidelity + maintenance defect. This
check extracts every inline SVG path from each snippet and matches the path data against the real
library in assets/icons/.

Each inline path is classified:
  • library  — byte-matches a library glyph (good; ideally via a <symbol> sprite + <use>).
  • bespoke  — inside an <svg data-bespoke="reason"> : a deliberately custom shape (control glyph
               like a checkbox tick, an animated/stateful mark, a focus ring). VERIFIED, not flagged.
  • UNKNOWN  — neither. Possibly invented → fix: use the library SVG, or, if genuinely custom,
               mark the <svg> with data-bespoke="why".

GATING: exits non-zero on any UNKNOWN (path that doesn't match the library, or a shape-only icon).
Shape-only icons — an <svg> built from <circle>/<rect>/<ellipse>/<polygon> with NO <path> to byte-match
(e.g. a 3-circle kebab) — are now flagged too (use the library glyph, or mark the <svg> data-bespoke).

Usage:  python3 _validate_icons.py [name-filter ...]      (default: all snippets)
"""
import os, re, glob, json

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")
ICONS = os.path.join(HERE, "assets", "icons")
MANIFEST = os.path.join(ICONS, "icons.manifest.json")
OUT = os.path.join(HERE, "_ICON-SOURCE-AUDIT.md")
SVGRE = re.compile(r'<svg\b[^>]*?>.*?</svg>', re.S)
DRE = re.compile(r'\bd="([^"]+)"')
SHAPERE = re.compile(r'<(?:circle|rect|ellipse|polygon|polyline)\b')  # shape-only icons (no <path> to byte-match)

def norm(d):
    return re.sub(r"\s+", " ", d.strip())

def build_library():
    lib = {}
    for f in glob.glob(os.path.join(ICONS, "**", "*.svg"), recursive=True):
        try:
            s = open(f, encoding="utf-8").read()
        except Exception:
            continue
        for d in DRE.findall(s):
            lib.setdefault(norm(d), os.path.relpath(f, HERE))
    return lib

def declared_icons(html):
    m = re.search(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return {}
    try:
        data = json.loads(m.group(1))
    except Exception:
        return {}
    return {k: v for k, v in data.get("icons", {}).items() if not k.startswith("$")}

def run(filters):
    lib = build_library()
    files = sorted(glob.glob(os.path.join(SNIP, "*.reference.html")))
    if filters:
        files = [f for f in files if any(x.lower() in os.path.basename(f).lower() for x in filters)]

    rows, detail, total_unknown, total_bespoke = [], [], 0, 0
    for f in files:
        name = os.path.basename(f).replace(".reference.html", "")
        html = open(f, encoding="utf-8").read()
        known, bespoke, unknown, ntot = 0, 0, [], 0
        for blk in SVGRE.findall(html):
            paths = DRE.findall(blk)
            ntot += len(paths)
            if "data-bespoke" in blk[:blk.find(">") + 1]:
                bespoke += len(paths)
                continue
            for d in paths:
                if norm(d) in lib:
                    known += 1
                else:
                    unknown.append(d)
            # circle/rect/ellipse/polygon-only icon: no <path> to byte-match → can't be verified.
            # An invented kebab/dots/shape icon would otherwise slip through. Flag unless data-bespoke.
            if not paths and SHAPERE.search(blk):
                ntot += 1
                unknown.append("(shape-only icon: " + re.sub(r"\s+", " ", blk)[:60] + "…)")
        total_unknown += len(unknown)
        total_bespoke += bespoke
        decl = declared_icons(html)

        if not ntot:
            status = "— no inline svg paths"
        elif not unknown:
            status = "✅ verified" + (f" · {bespoke} bespoke" if bespoke else "")
        else:
            status = f"⚠ {len(unknown)} UNKNOWN"
        rows.append((name, ntot, known, bespoke, len(unknown), "yes" if decl else "—", status))

        if unknown:
            detail.append(f"### {name} — {len(unknown)} UNKNOWN of {ntot} path(s)")
            for d in unknown[:12]:
                detail.append(f"- `d=\"{d[:70]}{'…' if len(d) > 70 else ''}\"`")
            detail.append("")

    L = ["# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)",
         "",
         "*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. "
         "**library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke=\"reason\">`, a "
         "deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither "
         "(possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons "
         "(`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*",
         "",
         f"**{total_unknown} UNKNOWN path(s)** across {len(files)} snippet(s) "
         f"({total_bespoke} verified-bespoke). Library glyphs indexed: {len(lib)}.",
         "",
         "| # | Snippet | paths | library | bespoke | UNKNOWN | declares | status |",
         "|---|---------|------:|--------:|--------:|--------:|:--------:|--------|"]
    for i, (name, n, k, bsp, u, dec, st) in enumerate(rows, 1):
        L.append(f"| {i} | {name} | {n} | {k} | {bsp} | {u} | {dec} | {st} |")
    L += ["", "## UNKNOWN detail", ""] + (detail or ["*(none — every inline path is library-matched or marked bespoke)*"])
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")

    print(f"icon-source audit → {os.path.relpath(OUT, HERE)}")
    print(f"{total_unknown} UNKNOWN, {total_bespoke} bespoke, across {len(files)} snippet(s); {len(lib)} library glyphs.")
    flagged = [r for r in rows if r[4]]
    if flagged:
        print("still UNKNOWN:")
        for name, n, k, bsp, u, dec, st in flagged:
            print(f"  {u:3d}  {name}")
    return total_unknown

if __name__ == "__main__":
    import sys
    # GATE (2026-06-24): exits non-zero on any UNKNOWN so _build_all.py fails the build.
    sys.exit(1 if run(sys.argv[1:]) else 0)
