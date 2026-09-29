"""#309 lane C - run knowledge/_build_kg_explorer.py in steps that each fit the seat's ~170 s shell cap.
The builder is unchanged: this wrapper imports it and caches the results of its slow pure functions
(the force layouts and the placements) on disk, keyed by the call's inputs, so a run the cap kills
resumes where it stopped. Run it until it prints 'wrote'. Cache: outputs/309/C/kgcache (ignored)."""
import sys, os, time, pickle, hashlib, json
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
sys.argv = [sys.argv[0]] + sys.argv[1:]
import _build_kg_explorer as K
CACHE = os.path.join(ROOT, "outputs", "309", "C", "kgcache"); os.makedirs(CACHE, exist_ok=True)
def cached(name, fn, mutates=False):
    def w(*a, **kw):
        key = hashlib.sha256(pickle.dumps((name, a, kw))).hexdigest()[:24]
        p = os.path.join(CACHE, f"{name}-{key}.pkl")
        if os.path.exists(p):
            out, after = pickle.load(open(p, "rb"))
            if mutates:
                for i, v in enumerate(after):
                    if v is not None: a[i][:] = v
            return out
        t = time.time(); out = fn(*a, **kw)
        pickle.dump((out, [list(x) if isinstance(x, list) else None for x in a] if mutates else None), open(p, "wb"))
        print(f"  [{name}] {time.time()-t:.1f}s (cached)", flush=True)
        return out
    return w
K.layout = cached("layout", K.layout)
for f in ("place_extra", "floors", "orbits", "shells3d", "strata"):
    if hasattr(K, f): setattr(K, f, cached(f, getattr(K, f), mutates=True))
K.main()
