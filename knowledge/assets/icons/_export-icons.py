#!/usr/bin/env python3
"""
HSBC Common Toolkit — icon catalogue exporter (REST batch).

Enumerates every icon on the Figma "Export board", batch-exports them as SVG via
the Figma REST /v1/images endpoint, cleans Figma's artboard artefacts, rewrites
monochrome (neutral-fill) icons to currentColor so they inherit the icon/* colour
tokens, and writes icons.manifest.json.

PREREQUISITES
  - A Figma personal access token with the **file_content:read** scope.
    (Figma → Settings → Security → Personal access tokens → File content: Read-only)
  - Run it with the token in the environment — do NOT paste the token into a file:
        export FIGMA_TOKEN=figd_xxxxxxxx
        python3 _export-icons.py
  - Stays on the "Gaps and edits" branch (branch key used as file key).

OUTPUT
  knowledge/assets/icons/<group-slug>/<icon-slug>.svg
  knowledge/assets/icons/icons.manifest.json
"""
import os, re, json, sys, time, collections, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

FILE_KEY = "Cgbtrmfp15ruNFkIAClpkI"          # "Gaps and edits" branch key
EXPORT_BOARD = "13244:4171"                    # Export board node
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.environ.get("FIGMA_TOKEN")

# Neutral primitives (from colour.json brand greys) — single-fill icons using one
# of these are treated as monochrome and rewritten to currentColor.
NEUTRALS = {"#F3F3F3", "#EDEDED", "#D7D8D6", "#B7B7B7", "#9B9B9B",
            "#767676", "#545454", "#333333", "#000000"}
WHITE = {"#FFFFFF", "#FFF", "WHITE"}

def api(path):
    req = urllib.request.Request("https://api.figma.com" + path,
                                 headers={"X-Figma-Token": TOKEN})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def slug(s):
    s = s.strip().lower().replace("/", "-").replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "icon"

def walk_groups(node, groups):
    """Collect icons grouped by 'Export Group -> X' frames."""
    name = node.get("name", "")
    if name.startswith("Export Group"):
        grp = name.split("->")[-1].strip()
        icons = [{"id": c["id"], "name": c.get("name", "").strip()}
                 for c in node.get("children", []) if c.get("name")]
        groups[grp] = icons
        return
    for c in node.get("children", []):
        walk_groups(c, groups)

def clean_svg(s):
    s = re.sub(r'<rect[^>]*fill="#E5E5E5"[^>]*/>\s*', '', s)
    s = re.sub(r'<path d="M-?\d{2,}[^"]*"\s*fill="white"\s*/>\s*', '', s)
    s = re.sub(r'<g id="Export board">\s*', '', s)
    s = re.sub(r'<g id="Export Group[^"]*">\s*', '', s)
    opens, closes = len(re.findall(r'<g\b', s)), len(re.findall(r'</g>', s))
    for _ in range(closes - opens):
        s = re.sub(r'\s*</g>\s*</svg>', '</svg>', s, count=1)
    return s.strip()

def apply_currentcolor(s):
    """If the icon is a single neutral fill, swap to currentColor. Returns (svg, mode, fills)."""
    fills = [f.upper() for f in re.findall(r'fill="(#[0-9A-Fa-f]{3,8})"', s)]
    non_white = [f for f in fills if f not in WHITE]
    distinct = set(non_white)
    if len(distinct) == 1 and next(iter(distinct)) in NEUTRALS:
        s = re.sub(r'fill="#[0-9A-Fa-f]{3,8}"',
                   lambda m: 'fill="currentColor"' if m.group(0)[6:-1].upper() not in WHITE else m.group(0),
                   s)
        return s, "currentColor", sorted(distinct)
    return s, "baked", sorted(distinct)

def fetch(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return r.read().decode("utf-8")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(0.5 * (i + 1))

def main():
    if not TOKEN:
        sys.exit("Set FIGMA_TOKEN env var (token needs file_content:read scope).")
    print("Enumerating icons from Export board...")
    tree = api(f"/v1/files/{FILE_KEY}/nodes?ids={urllib.parse.quote(EXPORT_BOARD)}")
    board = tree["nodes"][EXPORT_BOARD]["document"]
    groups = {}
    walk_groups(board, groups)
    total = sum(len(v) for v in groups.values())
    print(f"  {len(groups)} groups, {total} icons")

    # id -> (group, name); assign collision-free slugs per group (lossless)
    idmap = {ic["id"]: (grp, ic["name"]) for grp, ics in groups.items() for ic in ics}
    ids = list(idmap)
    seen = collections.defaultdict(set)
    plan = {}
    for nid, (grp, name) in idmap.items():
        gslug, base = slug(grp), slug(name)
        s, i = base, 2
        while s in seen[gslug]:
            s = f"{base}-{i}"; i += 1
        seen[gslug].add(s)
        plan[nid] = (grp, name, gslug, s)

    # batch image export (chunk to keep URLs sane)
    urls = {}
    CHUNK = 200
    for i in range(0, len(ids), CHUNK):
        chunk = ids[i:i+CHUNK]
        print(f"  requesting SVG urls {i+1}-{i+len(chunk)}...")
        res = api(f"/v1/images/{FILE_KEY}?ids={urllib.parse.quote(','.join(chunk))}&format=svg")
        urls.update(res.get("images", {}))
        time.sleep(0.3)

    manifest = {"$source": f"Figma {FILE_KEY} Export board {EXPORT_BOARD}",
                "$generated": time.strftime("%Y-%m-%d"), "groups": {}}

    def process(item):
        nid, (grp, name, gslug, islug) = item
        url = urls.get(nid)
        if not url:
            return ("miss", name, nid)
        gdir = os.path.join(OUT_DIR, gslug)
        os.makedirs(gdir, exist_ok=True)
        path = os.path.join(gdir, islug + ".svg")
        try:
            svg_text, mode, fills = apply_currentcolor(clean_svg(fetch(url)))
            with open(path, "w") as f:
                f.write(svg_text + "\n")
        except Exception as e:
            return ("err", name, f"{type(e).__name__}")
        return ("ok", grp, {"name": name, "slug": islug, "file": f"{gslug}/{islug}.svg",
                            "active": name.lower().endswith("active"),
                            "fillMode": mode, "fills": fills})

    print(f"Downloading {len(idmap)} SVGs (parallel)...")
    misses = 0
    with ThreadPoolExecutor(max_workers=32) as ex:
        for res in ex.map(process, list(plan.items())):
            if res[0] == "ok":
                manifest["groups"].setdefault(res[1], []).append(res[2])
            else:
                misses += 1; print("  !! no url:", res[1], res[2])
    for g in manifest["groups"]:
        manifest["groups"][g].sort(key=lambda x: x["slug"])
    manifest["$counts"] = {g: len(v) for g, v in manifest["groups"].items()}
    manifest["$total"] = sum(len(v) for v in manifest["groups"].values())
    print(f"  misses: {misses}")
    with open(os.path.join(OUT_DIR, "icons.manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Done. {total} icons → {OUT_DIR}")

if __name__ == "__main__":
    main()
