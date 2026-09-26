#!/usr/bin/env python3
"""R4a — rehearse the enactment of the drafts on a SCRATCH copy of knowledge/, and test them hard.
Nothing in the repo is written: the copy lives under $HOME/r4a-scratch/enact (rebuilt each run).
Run (seat): PYTHONDONTWRITEBYTECODE=1 python3 notes/_lanes/304/R4a/drafts/check_drafts.py
Writes: check-drafts-results.json (this folder). Exit 1 if any arm fails.
Arms: T1 textual meta patch (one field, rest byte-identical) · T2 meta.schema.json on every patched meta ·
T3 the resolver (_validate_roles_resolve.py) green before AND after · T4 each ruling entry through
_inscribe_ruling.py --dry-run · T5 the SUPERSESSIONS rows through role_defaults_219 · T6 R5's when-evaluator
on its 20 tests + new tests, with the drafts applied, and a no-regression check.
"""
import json, os, re, shutil, subprocess, sys, copy
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
SCR = os.path.join(os.path.expanduser("~"), "r4a-scratch", "enact")
res = {"arms": {}}
def arm(name, ok, **kw):
    res["arms"][name] = dict(ok=bool(ok), **kw); print("%-4s %s %s" % (name, "PASS" if ok else "FAIL", json.dumps(kw, ensure_ascii=False)[:300]))

# ---- scratch copy
if os.path.isdir(SCR): shutil.rmtree(SCR)
os.makedirs(SCR)
shutil.copytree(os.path.join(ROOT, "knowledge"), os.path.join(SCR, "knowledge"),
                ignore=shutil.ignore_patterns("assets", "_memento-index.json", "__pycache__", "photography*"))
os.makedirs(os.path.join(SCR, "notes", "_lanes", "304", "R5"))
shutil.copy(os.path.join(ROOT, "notes/_lanes/304/R5/when_eval.py"), os.path.join(SCR, "notes/_lanes/304/R5/"))
for rel in ("notes/_receipts/2026-08-25-219-role-defaults-exports.md", "notes/_DECIDE-304-when-rules-2026-09-26-v1.html",
            "notes/_lanes/303/WRAP-BRIEF.md"):
    os.makedirs(os.path.dirname(os.path.join(SCR, rel)), exist_ok=True); shutil.copy(os.path.join(ROOT, rel), os.path.join(SCR, rel))
import hashlib
def snap():
    out = {}
    for d, _, fs in os.walk(os.path.join(ROOT, "knowledge")):
        if "__pycache__" in d or "/assets" in d: continue
        for f in fs:
            fp = os.path.join(d, f)
            try: out[fp] = os.stat(fp).st_mtime_ns
            except OSError: pass
    return out
SNAP0 = snap()
K = os.path.join(SCR, "knowledge")
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
def run(cmd, cwd=SCR):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env, timeout=150)
    return r.returncode, (r.stdout + r.stderr)

W = json.load(open(os.path.join(HERE, "when-rules.proposed.json")))
O = json.load(open(os.path.join(HERE, "observations.proposed.json")))
RU = json.load(open(os.path.join(HERE, "rulings.proposed.json")))

# ---- T3a resolver BEFORE (its failure set on the untouched copy is the baseline; the six reds are the schema page's)
rc0, out0 = run([sys.executable, "knowledge/_validate_roles_resolve.py"])
FAIL0 = sorted(set(l.strip() for l in out0.splitlines() if ": FAIL [" in l))
arm("T3a", True, rc=rc0, baseline_fails=len(FAIL0), tail=out0.strip().splitlines()[-1:])

# ---- registry additions (when-fields.json, by addition)
wf_p = os.path.join(K, "when-fields.json")
wf = json.load(open(wf_p))
for k, v in W["registry_additions"].items():
    assert k not in wf["fields"], k
    wf["fields"][k] = v
json.dump(wf, open(wf_p, "w"), ensure_ascii=False, indent=1)

# ---- T1 textual patch of ONE field per meta
t1 = []
def jstr(s): return json.dumps(s, ensure_ascii=False)
for r in W["rows"]:
    if r["change"] == "KEEP": continue
    p = os.path.join(SCR, r["meta"]); raw = open(p, encoding="utf-8").read()
    before = json.load(open(p))
    if r["current"]:
        old = '"when": ' + jstr(r["current"])
        n = raw.count(old)
        if n != 1:  # the file may escape differently from json.dumps(ensure_ascii=False)
            t1.append((r["slug"], "current not found verbatim (%d)" % n)); continue
        new_raw = raw.replace(old, '"when": ' + jstr(r["proposed"]))
    elif re.search(r'"when":\s*""', raw):
        new_raw = re.sub(r'"when":\s*""', '"when": ' + jstr(r["proposed"]).replace("\\", "\\\\"), raw, count=1)
    else:  # insert after the "name" line, same indent
        m = re.search(r'^(\s*)"name":[^\n]*,\n', raw, re.M)
        new_raw = raw[:m.end()] + '%s"when": %s,\n' % (m.group(1), jstr(r["proposed"])) + raw[m.end():]
    after = json.loads(new_raw)
    diff = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    if diff != ["when"] or after["when"] != r["proposed"]:
        t1.append((r["slug"], "diff keys %s" % diff)); continue
    open(p, "w", encoding="utf-8").write(new_raw)
arm("T1", not t1, patched=sum(1 for r in W["rows"] if r["change"] != "KEEP"), problems=t1)

# ---- T2 schema
try:
    import jsonschema
    sch = json.load(open(os.path.join(K, "components/meta.schema.json")))
    bad = []
    for r in W["rows"]:
        if r["change"] == "KEEP": continue
        errs = sorted(jsonschema.Draft7Validator(sch).iter_errors(json.load(open(os.path.join(SCR, r["meta"])))), key=str)
        base = sorted(jsonschema.Draft7Validator(sch).iter_errors(json.load(open(os.path.join(ROOT, r["meta"])))), key=str)
        if len(errs) > len(base): bad.append((r["slug"], len(base), len(errs), [e.message[:120] for e in errs][:2]))
    arm("T2", not bad, note="no patched meta gains a schema error (pre-existing errors are the schema page's)", problems=bad)
except ImportError:
    arm("T2", False, note="jsonschema not importable at this seat")

# ---- T3b resolver AFTER (check 10 when-fields-known reads the new names)
rc1, out1 = run([sys.executable, "knowledge/_validate_roles_resolve.py"])
FAIL1 = sorted(set(l.strip() for l in out1.splitlines() if ": FAIL [" in l))
new = [l for l in FAIL1 if l not in FAIL0]
known = [l for l in out1.splitlines() if "when-fields-known" in l or "when-fields" in l][:4]
arm("T3b", not new and "RESULT" in out1, rc=rc1, fails_after=len(FAIL1), new_fails=new, when_field_lines=known,
    tail=out1.strip().splitlines()[-1:])

# ---- T4 rulings dry-run
t4 = []
for i, e in enumerate(RU["entries"], 1):
    ent = copy.deepcopy(e)
    ent["id"] = "s999-D%d" % i; ent["date"] = "2026-09-29"
    ent["says"] = ent["says"].replace("{{TUESDAY_WORD}}", "— and on the decision page: \"yes\"")
    ent["evidence"] = [x for x in ent["evidence"] if not x.startswith("{{")] + ["chat #305 — Dave's word on the decision page"]
    ent["ruled"] = ent["ruled"].replace("{{ID_A}}", ent["id"])
    ep = os.path.join(SCR, "entry-%d.json" % i); json.dump(ent, open(ep, "w"), ensure_ascii=False, indent=1)
    rc, out = run([sys.executable, "knowledge/_inscribe_ruling.py", "--entry", ep, "--dry-run"])
    t4.append((ent["id"], rc, " | ".join(l.strip() for l in out.strip().splitlines()[-3:])[:300]))
arm("T4", all(rc == 0 for _, rc, _ in t4), results=t4)

# ---- T5 SUPERSESSIONS through role_defaults_219 (textual append before the list's closing bracket)
rp = os.path.join(K, "_render/role_defaults_219.py"); src = open(rp, encoding="utf-8").read()
i = src.index("SUPERSESSIONS = ["); j = src.index("\n]\n", i)
rows = ["    " + json.dumps({k: (v.replace("{{ID_A}}", "s999-D1") if isinstance(v, str) else v) for k, v in row.items()},
                           ensure_ascii=False) + "," for row in O["A_bento_ground"]["supersessions_append"]]
open(rp, "w", encoding="utf-8").write(src[:j] + "\n" + "\n".join(rows) + src[j:])
code = ("import sys; sys.path.insert(0,'knowledge/_render'); import role_defaults_219 as d; "
        "import json; print(json.dumps({t:{k:d.DEFAULTS['dashboard'][t][k] for k in ('pageBg','bentoBg')} for t in d.DEFAULTS['dashboard']}))")
rc, out = run([sys.executable, "-c", code])
got = json.loads(out.strip().splitlines()[-1]) if rc == 0 else {}
ok5 = rc == 0 and all(v == {"pageBg": "white", "bentoBg": "grey"} for v in got.values()) and len(got) == 4
rcs, outs = run([sys.executable, "knowledge/_render/role_defaults_219.py", "--selftest"])
arm("T5", ok5 and rcs == 0, dashboard_defaults=got, selftest_rc=rcs, selftest_tail=outs.strip().splitlines()[-1:] if outs.strip() else [])

# ---- T6 the when-evaluator (R5) on the patched scratch metas
sys.path.insert(0, os.path.join(SCR, "notes/_lanes/304/R5"))
import when_eval as WE        # K resolves to the scratch knowledge/ (ROOT is 4 levels up from the copy)
assert os.path.samefile(WE.K, K), WE.K
base = {"W1": "chart-line"}
metas = WE.load_metas()
NEW_TESTS = [
    {"id": "N1", "role": "record-list", "ctx": {"records": 120, "needs": "sort"}, "expect": "data-grid"},
    {"id": "N2", "role": "record-list", "ctx": {"records": 3, "needs": "none"}, "expect": "list-items"},
    {"id": "N3", "role": "overlay", "ctx": {"interrupts": "required"}, "expect": "modals"},
    {"id": "N4", "role": "overlay", "ctx": {"interrupts": "none", "actions": 3}, "expect_excluded": "modals"},
    {"id": "N5", "role": "action", "ctx": {"emphasis": "primary", "label": "text", "actions": 3, "interrupts": "none"}, "expect": "split-button"},
    {"id": "N6", "role": "action", "ctx": {"emphasis": "primary", "label": "text", "actions": 1}, "expect": "button"},
    {"id": "W18n", "role": "record-list", "ctx": {"records": 40, "surface": "none", "needs": "sort"}, "expect": "data-grid"},
    {"id": "N7", "role": "input", "ctx": {"options": 8, "interrupts": "none"}, "expect": "dropdown"},
]
rows6 = []
for t in WE.TESTS + NEW_TESTS:
    for variant in (False, True):
        WE.PARSED.clear()
        r = WE.choose(t["ctx"], t.get("role"), metas=metas, implicit=variant)
        if "expect_excluded" in t:
            ok = t["expect_excluded"] in r["excluded"]
        else:
            ok = r["pick"] == t["expect"]
        rows6.append({"id": t["id"], "variant": "B" if variant else "A", "pick": r["pick"],
                      "expect": t.get("expect") or ("excluded: " + t["expect_excluded"]), "ok": ok})
def score(v, ids): return sum(1 for x in rows6 if x["variant"] == v and x["ok"] and x["id"] in ids)
w_ids = [t["id"] for t in WE.TESTS]; n_ids = [t["id"] for t in NEW_TESTS]
# baseline: R5's own results file (variant A 17/20, B 18/20) — recomputed here on the UNPATCHED metas for a like-for-like
WE.PARSED.clear(); m0 = {}
for f in sorted(os.listdir(os.path.join(ROOT, "knowledge/components"))):
    if f.endswith(".meta.json") and not f.startswith("EXAMPLE"):
        mm = json.load(open(os.path.join(ROOT, "knowledge/components", f)))
        if mm.get("when"): m0[f[:-10]] = mm
reg = []
base_ok = {}
for t in WE.TESTS:
    for variant in (False, True):
        WE.PARSED.clear(); r0 = WE.choose(t["ctx"], t.get("role"), metas=m0, implicit=variant)
        base_ok[(t["id"], variant)] = r0["pick"] == t["expect"]
for x in rows6:
    if x["id"] in w_ids and base_ok[(x["id"], x["variant"] == "B")] and not x["ok"]:
        reg.append(x)
res["T6_rows"] = rows6
arm("T6", not reg and score("A", n_ids) == len(n_ids),
    R5_tests_A="%d/%d (unpatched %d)" % (score("A", w_ids), len(w_ids), sum(v for (i, b), v in base_ok.items() if not b)),
    R5_tests_B="%d/%d (unpatched %d)" % (score("B", w_ids), len(w_ids), sum(v for (i, b), v in base_ok.items() if b)),
    new_tests_A="%d/%d" % (score("A", n_ids), len(n_ids)), new_tests_B="%d/%d" % (score("B", n_ids), len(n_ids)),
    regressions=reg, misses=[(x["id"], x["variant"], x["pick"], x["expect"]) for x in rows6 if not x["ok"]])

# ---- T7 nothing under knowledge/ moved while this ran (the scratch is the only thing written)
SNAP1 = snap()
moved = sorted(os.path.relpath(p, ROOT) for p in set(SNAP0) | set(SNAP1) if SNAP0.get(p) != SNAP1.get(p))
arm("T7", not moved, moved=moved[:10])

json.dump(res, open(os.path.join(HERE, "check-drafts-results.json"), "w"), ensure_ascii=False, indent=1)
sys.exit(0 if all(a["ok"] for a in res["arms"].values()) else 1)
