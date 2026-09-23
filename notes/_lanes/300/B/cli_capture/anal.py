import json, sys, gzip, tiktoken, collections
enc = tiktoken.get_encoding("cl100k_base")
def tk(s): return len(enc.encode(s, disallowed_special=()))
raw = open(sys.argv[1],'rb').read()
try: d = json.loads(raw)
except Exception: d = json.loads(gzip.decompress(raw))
print("model", d.get("model"), "keys", list(d.keys()))
sysb = d.get("system")
if isinstance(sysb, str): sysb=[{"type":"text","text":sysb}]
st = [tk(b.get("text","")) for b in sysb]
print("system blocks", len(sysb), st, "sum", sum(st))
tools = d.get("tools", [])
rows=[]
for t in tools:
    ser = json.dumps({k:v for k,v in t.items() if k in ("name","description","input_schema")})
    rows.append((t.get("name"), tk(ser), bool(t.get("defer_loading"))))
print("tools", len(tools), "sum cl100k", sum(r[1] for r in rows), "deferred-flagged", sum(1 for r in rows if r[2]), "tokens of non-deferred", sum(r[1] for r in rows if not r[2]))
for r in sorted(rows, key=lambda x:-x[1]): print(f"   {r[0]:40s} {r[1]:6d} {'DEFER' if r[2] else ''}")
msgs = d.get("messages", [])
mt = 0
for m in msgs:
    c = m["content"]
    if isinstance(c,str): mt += tk(c)
    else:
        for b in c:
            s = b.get("text") or json.dumps(b)
            mt += tk(s)
print("messages", len(msgs), "cl100k", mt)
for m in msgs:
    c = m["content"]
    if isinstance(c, list):
        for b in c:
            s = b.get("text") or ""
            print("   msgblock", m["role"], tk(s), repr(s[:100]))
