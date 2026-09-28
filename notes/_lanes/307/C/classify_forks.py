"""Item 5 — re-run the #221 lane-B triage rule on TODAY's forks (read-only).
Input: forks-strict-now.json, written by `knowledge/_validate_token_forks.py --strict --json <this dir>`
(ledger md5 checked unchanged either side). Rule, verbatim from notes/_subreports/2026-08-27-221-laneB.md §9:
  A  = one side a raw #hex, the other var(...), same name        (token bypass)
  A2 = two raw hexes, channel distance <= 60                     (near-miss drift)
  B  = not a hex pair (geometry / motion)   C = two raw hexes, distance > 60   D = var vs var
Distance = |dR|+|dG|+|dB| (reproduces #221's 239 for #f6604c v #a8000b)."""
import json, re, pathlib
here = pathlib.Path(__file__).parent
d = json.load(open(here / "forks-strict-now.json"))
led = json.load(open(here.parents[3] / "knowledge/_TOKEN-FORK-LEDGER.json"))
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
def dist(a, b):
    a, b = a.lstrip('#'), b.lstrip('#')
    return sum(abs(int(a[i:i+2], 16) - int(b[i:i+2], 16)) for i in (0, 2, 4))
def ishex(s): return bool(HEX.match(s.strip()))
decl = led.get("declared_forks", {})   # keyed by property name
out = []
for f in d["forks"]:
    a, b = f["a"], f["b"]; da, db = a["declared"].strip(), b["declared"].strip()
    ra, rb = a.get("resolved") or "", b.get("resolved") or ""
    if ishex(da) and ishex(db):
        dd = dist(da, db); bucket = "A2" if dd <= 60 else "C"
    elif (ishex(da) and da.startswith('#') and db.startswith('var(')) or (ishex(db) and da.startswith('var(')):
        bucket = "A"; dd = dist(ra, rb) if ishex(ra) and ishex(rb) else None
    elif da.startswith('var(') and db.startswith('var('):
        bucket = "D"; dd = dist(ra, rb) if ishex(ra) and ishex(rb) else None
    else:
        bucket = "B"; dd = None
    lr = decl.get(f["prop"])
    out.append({"bucket": bucket, "prop": f["prop"], "theme": f["theme"], "mode": f["mode"],
                "a": a["file_line"], "a_sel": a["selector"], "a_val": ra or da,
                "b": b["file_line"], "b_sel": b["selector"], "b_val": rb or db, "dist": dd,
                "ledger": (lr or {}).get("status", "NOT IN LEDGER")[:40]})
json.dump(out, open(here / "shots/5-forks-classified.json", "w"), indent=1)
from collections import Counter
print(Counter(o["bucket"] for o in out), len(out))
for o in out:
    if o["bucket"] in ("A", "A2"):
        print(o["bucket"], o["prop"], o["theme"], o["mode"], o["a_val"], "v", o["b_val"], o["dist"], "|", o["b_sel"][:50], "|", (o["ledger"] or "")[:70])
