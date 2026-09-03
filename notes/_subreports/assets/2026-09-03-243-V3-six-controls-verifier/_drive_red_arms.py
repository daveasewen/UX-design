"""V3 — drive the five new RED shapes and the six GREEN shapes via the CLI against a fresh brain copy; print every refusal line."""
import json, os, re, shutil, subprocess, sys, tempfile
M = "/sessions/awesome-festive-hamilton/v3/mirror"
VAL = os.path.join(M, "knowledge/_validate_polarities.py")
BRAIN = os.path.join(M, "knowledge/brain")
ROOT = tempfile.mkdtemp(prefix="v3-")
def fresh(s):
    d = os.path.join(ROOT, s); shutil.copytree(BRAIN, d); return d
def jmut(p, fn):
    o = json.loads(open(p).read()); fn(o); open(p, "w").write(json.dumps(o, indent=1, ensure_ascii=False) + "\n")
def run(args):
    r = subprocess.run([sys.executable, VAL] + args, capture_output=True, text=True, cwd=M); return r.returncode, r.stdout + r.stderr
def show(label, rc, out):
    lines = [l for l in out.splitlines() if "REFUSED" in l or "✓" in l and "GREEN" in l]
    nm = sorted(set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)", out)))
    print(f"--- {label}: rc={rc} names={nm}")
    for l in lines: print("    " + l.strip()[:230])
def add(d, entry):
    ep = os.path.join(ROOT, "e.json"); json.dump(entry, open(ep, "w")); return run(["--add-polarity", ep, "--write", "--brain", d])
P = [{"ref": "pr-fitts", "role": "side_a"}, {"ref": "pr-hick", "role": "side_b"}]
NEW31 = {"id": "pl-31", "parties": P, "mediating_variable": "target count", "links": [], "sources": [{"path": "notes/nowhere.json", "id": "tn-31"}]}
GOOD = {"id": "pl-90", "parties": P, "mediating_variable": "target count", "links": [], "sources": [{"path": "selftest", "id": "x"}]}
GOOD_SEED = dict({k: v for k, v in GOOD.items() if k != "sources"}, **{"$seed": "s240-D3"})
ALLSTUB = {"id": "pl-40", "parties": [{"ref": "st-brand-palette", "role": "side_a"}, {"ref": "st-consistency-of-investment-across-a-journey", "role": "side_b"}], "mediating_variable": "x", "links": [], "sources": [{"path": "x", "id": "y"}]}
d = fresh("100L"); jmut(d + "/polarities.json", lambda o: o["polarities"].append(NEW31)); show("100 LITERAL --write", *run(["--write", "--brain", d]))
d = fresh("235L"); jmut(d + "/stubs.json", lambda o: o["stubs"].append({"id": "st-orphan-phrase", "phrase": "an orphan phrase"})); show("235 LITERAL --check", *run(["--check", "--brain", d]))
d = fresh("248L"); jmut(d + "/polarities.json", lambda o: o["polarities"].append(ALLSTUB)); show("248 LITERAL --write", *run(["--write", "--brain", d]))
d = fresh("321L"); jmut(d + "/polarities.json", lambda o: o.__setitem__("polarities", [])); show("321 LITERAL add_entry --write", *add(d, GOOD_SEED))
d = fresh("326L"); o = json.load(open(d + "/polarities.json")); open(d + "/polarities.json", "w").write(json.dumps(o, indent=2, ensure_ascii=False) + "\n"); show("326 LITERAL add_entry --write", *add(d, GOOD))
# is 235 LEGAL's phrase inside ONE field of the register?
reg = json.load(open(os.path.join(M, "notes/_subreports/assets/2026-09-02-236-R1-principles-survey/tensions.json")))["tensions"]
ph = "tn-01 pr-jakobs-law (work like"
print("235 LEGAL phrase in any single field of any row:", any(ph in v for r in reg for v in r.values() if isinstance(v, str)))
print("235 LEGAL phrase in raw file bytes:", ph in open(os.path.join(M, "notes/_subreports/assets/2026-09-02-236-R1-principles-survey/tensions.json")).read())
shutil.rmtree(ROOT)
