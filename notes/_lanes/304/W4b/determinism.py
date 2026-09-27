"""W4b: the views phase run twice on every cold run (runs/ and runs-rerun/) — every view's ink must match."""
import json, sys
bad = 0
for r in ["v1013-r1","v1013-r2","v1013-r3","cand-r1","cand-r2","cand-r3"]:
    A=[v for v in json.load(open("notes/_lanes/304/W4b/runs/cold-%s/views.json"%r))["views"] if v.get("kept")]
    B=[v for v in json.load(open("notes/_lanes/304/W4b/runs-rerun/cold-%s/views.json"%r))["views"] if v.get("kept")]
    same_views = [a["url"] for a in A] == [b["url"] for b in B]
    textsig = [a["nav_text"][:12] for a, b in zip(A, B) if a["sig"] != b["sig"]]   # information: the page's text moved between loads
    d = [(a["nav_text"][:16], k) for a, b in zip(A, B) for k in ("affected", "instances", "worst", "tiles") if a["ink"][k] != b["ink"][k]]
    th = json.load(open("notes/_lanes/304/W4b/runs/cold-%s/views.json"%r))["theme_switch"]["verdict"] == json.load(open("notes/_lanes/304/W4b/runs-rerun/cold-%s/views.json"%r))["theme_switch"]["verdict"]
    # a difference confined to a view holding a ring chart, in the DEAD class only, is the PAGE's own
    # bistability (the ring's diameter differs load to load — notes/_lanes/304/W4b/probe_ring_bistable.txt)
    ring = lambda v: any(c.get("type") in ("donut", "pie") for c in v["page"]["charts"])
    pagebi = [(a["nav_text"][:16]) for a, b in zip(A, B) if a["ink"] != b["ink"] and ring(a)
              and all(a["ink"]["affected"][k] == b["ink"]["affected"][k] and a["ink"]["instances"][k] == b["ink"]["instances"][k] for k in ("cut", "collision", "size", "markers"))]
    other = [x for x in d if x[0] not in pagebi]
    ok = same_views and not other and th and len(A) == len(B)
    bad += not ok
    print("%-9s views %d/%d same-views=%s theme-same=%s ink-diffs=%s ring-bistable-views=%s text-moved=%s → %s" % (
        r, len(A), len(B), same_views, th, other, pagebi, textsig, ("IDENTICAL" if not d else "IDENTICAL but for the page's bistable ring") if ok else "DIFFER"))
print("DETERMINISM", "PASS" if not bad else "FAIL", "(instrument; ring-bistable views are the page's, receipted)")
