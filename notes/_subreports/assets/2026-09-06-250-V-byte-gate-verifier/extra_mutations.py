#!/usr/bin/env python3
"""VERIFIER's OWN mutations — the two the builder did NOT run. In-memory only."""
import importlib.util, json, os
spec = importlib.util.spec_from_file_location("vb", "knowledge/_validate_behaviour.py")
vb = importlib.util.module_from_spec(spec); spec.loader.exec_module(vb)

reg = json.load(open("knowledge/component-types.json"))
behs = reg["component-type"]["dataviz"]["$behaviour"]
mem  = {m: v for m, v in reg["component-type"]["dataviz"]["$members"].items() if not m.startswith("$")}
consumes = {m: list((v or {}).get("consumes") or []) for m, v in mem.items()}
srcs, names = [], []
for b, v in behs.items():
    names.append(b); srcs.append(open(os.path.join("knowledge", v["source"])).read())

# ---- V-MUT-1: page-budget clause ALONE. Pad legend + donut-sweep with REAL CODE so that
# EVERY source stays under MAX_BYTES (16384) but Chart-donut's page crosses PAGE_BYTES (34816).
# This is the clause "splitting a source does not buy headroom", never bitten on live data.
print("=== V-MUT-1 page-clause-only (every source GREEN, worst member page RED) — expect RED ===")
mut = list(srcs)
for i, nm in enumerate(names):
    if nm in ("dv-legend", "dv-donut-sweep"):
        mut[i] = srcs[i] + "\n" + vb.CODE_PAD(8000)
src_fails = []
for js, nm in zip(mut, names):
    f, raw, code = vb.check_source(js, nm)
    print("   source %-16s code-only %6d  cap %d  %s" % (nm, code, vb.MAX_BYTES, "RED" if f else "green"))
    src_fails += f
gf, worst, per = vb.check_group(mut, "dataviz (page budget)", names, consumes)
print("   worst member page = %d  cap %d" % (worst, vb.PAGE_BYTES))
print("   per-source fails: %d  |  group fails: %s" % (len(src_fails), gf or "NONE"))
v1 = "RED" if gf else "GREEN"
print("   expected RED · got %s — %s\n" % (v1, "OK" if v1 == "RED" else "*** GATE MISSED IT ***"))

# ---- V-MUT-2: MINIFIED source, zero comments, exactly cap+1 code bytes. Boundary test:
# no comment credit available, so an off-by-one would show here and nowhere else.
print("=== V-MUT-2 minified, no comments, exactly MAX_BYTES+1 code bytes — expect RED ===")
for delta, expect in ((1, "RED"), (0, "GREEN")):
    body = "var z=0;" + "z+=1;" * 4000
    body = body[: vb.MAX_BYTES + delta - 1] + ";"
    raw, code = vb.measure(body)
    assert code == vb.MAX_BYTES + delta, (code, vb.MAX_BYTES + delta)
    f = vb.check_source(body, "MIN")[0]
    got = "RED" if f else "GREEN"
    print("   code-only %6d (= cap%+d) · comments 0 · got %-5s expected %-5s — %s"
          % (code, delta, got, expect, "OK" if got == expect else "*** WRONG ***"))
