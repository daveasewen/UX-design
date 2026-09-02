#!/usr/bin/env python3
"""#238-P — INDEPENDENT READERS over the same artefacts (a green from one instrument is a claim).

1. jsonschema (the library, draft-7 semantics) reads knowledge/brain/schema/polarity.schema.json:
   metaschema-valid; the 30 real nodes pass; ten structural mutants are refused — the same
   mutants _validate_polarities.py --selftest drives. (The library ignores the house keyword
   `maxWords` — declared in x-vocabulary — and knows nothing of R1 resolution; those are the
   gate's own and are NOT cross-checked here.)
2. a recount straight from the FROZEN R1 rows + register (never from the generated files):
   cross-side principle↔principle edges, rows with edges, obligation rows — compared with
   knowledge/brain/_generated/polarity-edges.json and polarity-status.json, and with 237-T's
   tension-sort.json buckets.
3. byte receipts: principles.json == principle-register.json; sha256 of every file this lane wrote.
Read-only.
"""
import copy
import hashlib
import itertools
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
R1 = os.path.join(REPO, "notes/_subreports/assets/2026-09-02-236-R1-principles-survey")
T = os.path.join(REPO, "notes/_subreports/assets/2026-09-02-237-T-tensions-schema")
BRAIN = os.path.join(REPO, "knowledge/brain")


def load(p):
    return json.load(open(p, encoding="utf-8"))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


ok = True
# ---- 1 · jsonschema ------------------------------------------------------------------------
try:
    from jsonschema import Draft7Validator
    schema = load(os.path.join(BRAIN, "schema/polarity.schema.json"))
    Draft7Validator.check_schema(schema)
    V = Draft7Validator(schema)
    nodes = load(os.path.join(BRAIN, "polarities.json"))["polarities"]
    errs = [(n["id"], e.message) for n in nodes for e in V.iter_errors(n)]
    print("1. jsonschema: schema metaschema-valid ·", "30 real nodes: 0 errors" if not errs else errs)
    cases = {
        "untyped link": lambda n: n["links"].append({"ref": "s116-D1"}),
        "fifth type": lambda n: n["links"].append({"type": "relatedTo", "ref": "s116-D1"}),
        "judgement field": lambda n: n.__setitem__("how_it_resolves", "x"),
        "typed status": lambda n: n.__setitem__("status", "open"),
        "1 party": lambda n: n.__setitem__("parties", n["parties"][:1]),
        "role side_d": lambda n: n["parties"][0].__setitem__("role", "side_d"),
        "unicode id": lambda n: n.__setitem__("id", "pl-0１"),
        "party extra key": lambda n: n["parties"][0].__setitem__("why", "x"),
        "sources missing": lambda n: n.__delitem__("sources"),
        "non-ascii ref": lambda n: n["parties"].append({"ref": "pr-jаkobs", "role": "side_b"}),
    }
    agree = 0
    for name, fn in cases.items():
        n = copy.deepcopy(nodes[0]); fn(n)
        e = [x.message for x in V.iter_errors(n)]
        agree += bool(e)
        print(f"   {name:16s} refused: {'YES' if e else 'NO '}  {e[0][:64] if e else ''}")
    print(f"   independent reader refuses {agree}/{len(cases)} structural mutants")
    ok &= (not errs) and agree == len(cases)
except ImportError:
    print("1. jsonschema: NOT INSTALLED here — cross-check UNASKED (declared)")

# ---- 2 · recount from the frozen rows -------------------------------------------------------
t = load(os.path.join(R1, "tensions.json"))["tensions"]
G = {p["id"]: p["grade"] for p in load(os.path.join(R1, "principle-register.json"))["principles"]}
PR = re.compile(r"\bpr-[a-z0-9][a-z0-9-]*")
fix = {"pr-info-scent": "pr-information-scent", "pr-two-red-law": None}
edges = 0; rows_with = 0; obl = set()
for row in t:
    sides = []
    for k in ("side_a", "side_b", "side_c"):
        s = row.get(k)
        if not s:
            continue
        ids = [fix.get(i, i) for i in PR.findall(s)]
        ids = [i for i in ids if i and i in G]
        sides.append(ids)
        if any(G[i] == "L" for i in ids):
            obl.add(row["id"])
    n = sum(len(sides[a]) * len(sides[b]) for a, b in itertools.combinations(range(len(sides)), 2))
    edges += n; rows_with += 1 if n else 0
st = load(os.path.join(BRAIN, "_generated/polarity-status.json"))
ed = load(os.path.join(BRAIN, "_generated/polarity-edges.json"))
ts = load(os.path.join(T, "tension-sort.json"))
g_obl = sorted(r["r1_id"] for r in st["rows"] if r["status_derived"] == "settled-by-obligation")
g_res = sorted(r["r1_id"] for r in st["rows"] if r["status_derived"] == "resolved")
t_obl = sorted(r["id"] for r in ts["rows"] if r["bucket"] == "settled-by-obligation")
t_res = sorted(r["id"] for r in ts["rows"] if r["bucket"] == "resolved-here")
print(f"2. recount from R1: edges {edges} · rows with edges {rows_with} · obligation rows {sorted(obl)}")
print(f"   generated       : edges {ed['counts']['edges']} · rows with edges {ed['counts']['polarities_with_edges']} · "
      f"status {st['counts']}")
print(f"   obligation rows: generated == recount == 237-T: {g_obl == sorted(obl) == t_obl}")
print(f"   resolved rows  : generated {g_res} · 237-T {t_res} · delta {sorted(set(g_res) - set(t_res))} "
      f"(tn-22: resolvedBy s217-D8 from apollo_touch, T finding 2)")
ok &= edges == ed["counts"]["edges"] and rows_with == ed["counts"]["polarities_with_edges"]
ok &= g_obl == sorted(obl) == t_obl and set(g_res) - set(t_res) == {"tn-22"}

# ---- 3 · byte receipts -----------------------------------------------------------------------
same = sha(os.path.join(R1, "principle-register.json")) == sha(os.path.join(BRAIN, "principles.json"))
print(f"3. principles.json byte-identical to principle-register.json: {same} "
      f"(sha256 {sha(os.path.join(BRAIN, 'principles.json'))[:16]}…)")
ok &= same
print(f"   source tensions.json sha256 {sha(os.path.join(R1, 'tensions.json'))}")
print(f"   $migration.sha256 in polarities.json matches: "
      f"{load(os.path.join(BRAIN, 'polarities.json'))['$migration']['sha256'] == sha(os.path.join(R1, 'tensions.json'))}")
for rel in ("knowledge/_validate_polarities.py", "knowledge/brain/principles.json", "knowledge/brain/polarities.json",
            "knowledge/brain/stubs.json", "knowledge/brain/schema/polarity.schema.json",
            "knowledge/brain/_generated/polarity-status.json", "knowledge/brain/_generated/polarity-edges.json",
            "knowledge/brain/_generated/defaults-declaration.txt"):
    print(f"   {sha(os.path.join(REPO, rel))}  {rel}")
print("\n✓ independent readers agree" if ok else "\n✗ an independent reader DISAGREES — read above")
sys.exit(0 if ok else 1)
