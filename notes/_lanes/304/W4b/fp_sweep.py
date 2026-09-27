"""W4b: false-positive sweep — the OLD (R4b) and NEW (W4b) geometry gates on one corpus slice at 1440.
usage: python3 fp_sweep.py {old|new} {snippets|showroom} START END   → appends to fp/<which>-<corpus>.jsonl
Resumable: pages already in the jsonl are skipped. Nothing else is written."""
import glob, importlib.machinery, json, os, sys, time
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "knowledge"))
which, corpus, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
if which == "old":
    G = importlib.machinery.SourceFileLoader("geo_old", os.path.join(os.path.dirname(__file__), "_validate_geometry.pre-W4b.py.txt")).load_module()
else:
    import _validate_geometry as G
pages = sorted(glob.glob(os.path.join(REPO, "knowledge/snippets/*.reference.html"))) if corpus == "snippets" else \
        sorted(p for p in glob.glob(os.path.join(REPO, "showroom/*.html")))
out = os.path.join(os.path.dirname(__file__), "fp", "%s-%s.jsonl" % (which, corpus))
done = set()
if os.path.exists(out):
    done = {json.loads(l)["page"] for l in open(out) if l.strip()}
t0 = time.time()
with G.Harness() as h, open(out, "a") as fh:
    for p in pages[a:b]:
        rel = os.path.relpath(p, REPO)
        if rel in done: continue
        if time.time() - t0 > 150: print("budget"); break
        try:
            r = G.run_pages(h, [p], [1440], (), G.spacing_stops(), quiet=True)[0]
            fh.write(json.dumps({"page": rel, "font_ok": r["font_ok"], "findings": [{k: f.get(k) for k in ("clause", "where", "measured")} for f in r["findings"]]}) + "\n")
        except Exception as e:
            fh.write(json.dumps({"page": rel, "error": str(e)[:200]}) + "\n")
        fh.flush()
print("done", which, corpus, a, b, round(time.time() - t0))
