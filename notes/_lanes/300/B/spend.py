import json, sys
p = sys.argv[1]
seen = {}; order = []
for l in open(p):
    d = json.loads(l)
    if d.get("type") != "assistant": continue
    m = d["message"]; mid = m.get("id"); u = m.get("usage", {})
    real = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
    if mid not in seen: order.append(mid)
    seen[mid] = (real, u.get("output_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("input_tokens", 0))
vals = [seen[k] for k in order]
print("assistant messages", len(vals))
print("boot fill (msg 1)", vals[0][0], "| last fill", vals[-1][0], "| peak fill", max(v[0] for v in vals))
print("sum output", sum(v[1] for v in vals), "| sum cache_creation", sum(v[2] for v in vals), "| sum cache_read", sum(v[3] for v in vals), "| sum uncached input", sum(v[4] for v in vals))
print("cumulative processed input (sum of fills)", sum(v[0] for v in vals))
