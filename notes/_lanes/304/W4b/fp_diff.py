"""W4b: diff the old and new sweeps — every finding the NEW gate adds or drops, by page."""
import json, re, sys, collections
corpus = sys.argv[1]
L = lambda w: {j["page"]: j for j in map(json.loads, open("fp/%s-%s.jsonl" % (w, corpus)))}
old, new = L("old"), L("new")
key = lambda f: (f["clause"], f["where"])
added, dropped = collections.Counter(), collections.Counter()
rows = []
for p in sorted(new):
    o = collections.Counter(key(f) for f in old.get(p, {}).get("findings", []))
    n = collections.Counter(key(f) for f in new[p].get("findings", []))
    a, d = n - o, o - n
    for k, c in a.items(): added[k[0]] += c; rows.append(("+", p, k[0], k[1][:90], next(f["measured"][:90] for f in new[p]["findings"] if key(f) == k)))
    for k, c in d.items(): dropped[k[0]] += c; rows.append(("-", p, k[0], k[1][:90], ""))
print("pages old=%d new=%d errors new=%d font_ok new=%s" % (len(old), len(new), sum(1 for j in new.values() if "error" in j), all(j.get("font_ok") for j in new.values() if "error" not in j)))
print("findings old=%d new=%d" % (sum(len(j.get("findings", [])) for j in old.values()), sum(len(j.get("findings", [])) for j in new.values())))
print("ADDED by clause", dict(added)); print("DROPPED by clause", dict(dropped))
for r in rows: print(" ".join(r))
