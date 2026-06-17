#!/usr/bin/env python3
"""
HSBC logo exporter — 12 logo variants from the Foundations › Logos page (node 29:1009)
of the "Gaps and edits" branch, as SVG.

Run with a Figma personal access token (file_content:read scope):
    export FIGMA_TOKEN=figd_xxxx
    python3 _export-logos.py
(Token read from env only — don't commit it.)
"""
import os, re, json, urllib.request, urllib.parse

FK = "Cgbtrmfp15ruNFkIAClpkI"
OUT = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.environ.get("FIGMA_TOKEN")

NAMES = {
    "29:941": "hexagon-light-colour",   "29:954": "hexagon-light-mono",
    "960:26531": "hexagon-dark-colour", "960:26563": "hexagon-dark-mono",
    "29:962": "masterbrand-light-colour", "960:26499": "masterbrand-light-mono",
    "29:978": "masterbrand-dark-colour",  "29:994": "masterbrand-dark-mono",
    "2384:92762": "masterbrand-identifier-light-colour", "2384:92778": "masterbrand-identifier-light-mono",
    "2384:92925": "masterbrand-identifier-dark-colour",  "2384:92910": "masterbrand-identifier-dark-mono",
}

def clean(s):
    s = re.sub(r'<rect[^>]*fill="#E5E5E5"[^>]*/>\s*', '', s)
    s = re.sub(r'<path d="M-?\d{3,}[^"]*"\s*fill="white"\s*/>\s*', '', s)
    return s.strip()

def api(p):
    r = urllib.request.Request("https://api.figma.com" + p, headers={"X-Figma-Token": TOKEN})
    return json.load(urllib.request.urlopen(r, timeout=30))

def main():
    if not TOKEN:
        raise SystemExit("Set FIGMA_TOKEN (file_content:read scope).")
    ids = ",".join(NAMES)
    imgs = api(f"/v1/images/{FK}?ids={urllib.parse.quote(ids)}&format=svg").get("images", {})
    for nid, nm in NAMES.items():
        u = imgs.get(nid)
        if not u:
            print("  !! no url", nm); continue
        data = urllib.request.urlopen(u, timeout=30).read().decode("utf-8")
        open(os.path.join(OUT, nm + ".svg"), "w").write(clean(data) + "\n")
        print("  wrote", nm + ".svg")
    print("Done.")

if __name__ == "__main__":
    main()
