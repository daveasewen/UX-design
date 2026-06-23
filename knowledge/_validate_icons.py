#!/usr/bin/env python3
"""
Icon-source check (ADVISORY) — guards against invented icons.

Why (Dave, 2026-06-22): an AI model building a snippet can hand-draw an SVG that *looks* like
an icon instead of using the real HSBC library glyph. That's a silent fidelity + maintenance
defect. This check extracts every inline SVG path from each snippet and compares the path data
against the real library in assets/icons/. Anything that doesn't match is flagged UNKNOWN
(possibly invented) for human review.

UNKNOWN means "not byte-matched to a library glyph" — it is EITHER an invented icon (fix: use
the library SVG, ideally via a <symbol> sprite + <use>, and declare it in the snippet
token-manifest 'icons' block) OR a legitimately bespoke/decorative shape (focus ring, a custom
mark). Advisory, non-gating: it surfaces, a human decides.

Usage:  python3 _validate_icons.py [name-filter ...]      (default: all snippets)
"""
import os, re, glob, json

HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = os.path.join(HERE, "snippets")
ICONS = os.path.join(HERE, "assets", "icons")
MANIFEST = os.path.join(ICONS, "icons.manifest.json")
OUT = os.path.join(HERE, "_ICON-SOURCE-AUDIT.md")

def norm(d):
    return re.sub(r"\s+", " ", d.strip())

def build_library():
    """normalized path-d -> library file (relative)."""
    lib = {}
    for f in glob.glob(os.path.join(ICONS, "**", "*.svg"), recursive=True):
        try:
            s = open(f, encoding="utf-8").read()
        except Exception:
            continue
        for d in re.findall(r'\bd="([^"]+)"', s):
            lib.setdefault(norm(d), os.path.relpath(f, HERE))
    return lib

def manifest_files():
    try:
        m = json.load(open(MANIFEST, encoding="utf-8"))
    except Exception:
        return set()
    files = set()
    for items in m.get("groups", {}).values():
        for it in items:
            if it.get("file"):
                files.add(it["file"])
    return files

def declared_icons(html):
    """parse the token-manifest 'icons' block, if present."""
    m = re.search(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return {}
    try:
        data = json.loads(m.group(1))
    except Exception:
        return {}
    icons = data.get("icons", {})
    return {k: v for k, v in icons.items() if not k.startswith("$")}

def run(filters):
    lib = build_library()
    mfiles = manifest_files()
    files = sorted(glob.glob(os.path.join(SNIP, "*.reference.html")))
    if filters:
        files = [f for f in files if any(x.lower() in os.path.basename(f).lower() for x in filters)]

    rows, detail = [], []
    total_unknown = 0
    for f in files:
        name = os.path.basename(f).replace(".reference.html", "")
        html = open(f, encoding="utf-8").read()
        ds = re.findall(r'\bd="([^"]+)"', html)
        known, unknown = 0, []
        for d in ds:
            if norm(d) in lib:
                known += 1
            else:
                unknown.append(d)
        total_unknown += len(unknown)

        # manifest 'icons' declaration cross-check
        decl = declared_icons(html)
        decl_notes = []
        for slug, fileref in decl.items():
            ok = fileref in mfiles or os.path.exists(os.path.join(ICONS, fileref.split("/", 0)[0])) or any(fileref.endswith(mf.split("/")[-1]) for mf in mfiles)
            decl_notes.append(f"{slug}→{fileref} {'✓' if (fileref in mfiles) else '?'}")

        status = "✅ all paths trace to the library" if not unknown else f"⚠ {len(unknown)} UNKNOWN path(s)"
        if not ds:
            status = "— no inline svg paths"
        rows.append((name, len(ds), known, len(unknown), "yes" if decl else "—", status))

        if unknown:
            detail.append(f"### {name} — {len(unknown)} UNKNOWN of {len(ds)} path(s)")
            if decl:
                detail.append(f"*declares icons:* {', '.join(decl_notes)}")
            for d in unknown[:12]:
                detail.append(f"- `d=\"{d[:70]}{'…' if len(d) > 70 else ''}\"`")
            detail.append("")

    # write report
    L = ["# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)",
         "",
         "*ADVISORY (non-gating). Each snippet's inline `<svg>` path data is matched byte-for-byte against the "
         "library. UNKNOWN = not matched — EITHER an invented icon (use the library SVG, ideally a `<symbol>` "
         "sprite + `<use>`, and declare it in the token-manifest `icons` block) OR a legitimately bespoke/"
         "decorative shape (focus ring, custom mark). A human decides.*",
         "",
         f"**{total_unknown} UNKNOWN path(s) across {len(files)} snippet(s).** Library glyphs indexed: {len(lib)}.",
         "",
         "| # | Snippet | paths | library | UNKNOWN | declares icons | status |",
         "|---|---------|------:|--------:|--------:|:--------------:|--------|"]
    for i, (name, n, k, u, dec, st) in enumerate(rows, 1):
        L.append(f"| {i} | {name} | {n} | {k} | {u} | {dec} | {st} |")
    L += ["", "## UNKNOWN detail", ""] + (detail or ["*(none — every inline path traces to the library)*"])
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")

    print(f"icon-source audit → {os.path.relpath(OUT, HERE)}")
    print(f"{total_unknown} UNKNOWN path(s) across {len(files)} snippet(s); {len(lib)} library glyphs indexed.")
    flagged = [r for r in rows if r[3]]
    if flagged:
        print("snippets with UNKNOWN paths:")
        for name, n, k, u, dec, st in flagged:
            print(f"  {u:3d}  {name}")
    return total_unknown

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])
