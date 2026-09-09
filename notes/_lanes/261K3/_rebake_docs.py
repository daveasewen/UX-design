#!/usr/bin/env python3
"""#261 K3 — re-bake the four DOCS blobs on the K review page.

The page shipped at K2 embedded each snippet RAW, so its <link href="../canon/type.css"> resolved
against notes/_lanes/ and 404'd inside every srcdoc: all three columns were rendering UNSTYLED
(one ERR_FILE_NOT_FOUND in the console, four squashed together). Since Dave is judging the TYPE
lock-up, that is fatal. Bake each doc the way gen_showroom.py bakes a standalone: type.css inlined
plus gen_theme_cascade.snippet_theme_css(), so the four [data-apollo-theme] slots resolve too.
Idempotent: re-running replaces the blobs from the same sources.
"""
import base64, json, os, re, subprocess, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "knowledge" / "canon"))
import gen_theme_cascade as gtc

TYPE = (REPO / "knowledge/canon/type.css").read_text(encoding="utf-8")
PAGE = REPO / "notes/_lanes/261-K-kpi-tile-review.html"
SNIP = "knowledge/snippets/Kpi-tile.reference.html"

def bake(src):
    mv = json.loads(re.search(r'id="token-manifest">\s*(\{.*?\})\s*</script>', src, re.S).group(1))["vars"]
    css = gtc.snippet_theme_css(mv, "kpi-tile")
    d = src.replace('<link rel="stylesheet" href="../canon/type.css">',
                    "<style>\n" + TYPE + "\n</style>\n<style>\n" + css + "\n</style>")
    assert '<link rel="stylesheet" href="../canon/type.css">' not in d, "type.css link survived the bake"
    d = d.replace("body{margin:0; padding:2.25rem;", "body{margin:0; padding:24px;")
    return base64.b64encode(d.encode("utf-8")).decode("ascii")

def at(rev):
    return subprocess.check_output(["git", "-C", str(REPO), "show", f"{rev}:{SNIP}"]).decode("utf-8")

DOCS = {
    "old": at("7647aaf"),                       # #203, the layout Dave prefers
    "nw":  at("c8dd830^"),                      # #261 K, before Dave's first review
    "k2":  at("c8dd830"),                       # #261 K2, first review enacted
    "k3":  (REPO / SNIP).read_text(encoding="utf-8"),      # working tree = #261 K3
}
blob = "  var DOCS = { " + ", ".join(f'{k}: "{bake(v)}"' for k, v in DOCS.items()) + " };"
lines = PAGE.read_text().split("\n")
hit = [i for i, l in enumerate(lines) if l.strip().startswith("var DOCS = {")]
assert len(hit) == 1
lines[hit[0]] = blob
PAGE.write_text("\n".join(lines))
print("re-baked", ", ".join(DOCS), "->", len(blob), "bytes")
