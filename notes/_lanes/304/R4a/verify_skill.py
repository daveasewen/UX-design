#!/usr/bin/env python3
"""R4a — test the rewritten generate skill HARD against the candidate pack, as a cold agent holding only the pack.
Run (seat): PYTHONDONTWRITEBYTECODE=1 python3 notes/_lanes/304/R4a/verify_skill.py <candidate stage dir> [<v1.0.13 stage dir>]
Writes verify-skill-results.json beside itself. Exit 1 on any FAIL.
  C1  every path and command the skill names resolves in the candidate pack (globs must match >= 1 file)
  C2  the nailed lines: no splice / start-from-template instruction; step 1 calls the reader; templates are fenced
      as reference fixtures; rule 7a (the projections' pointer) and the bento question survive
  C3  every hard rule the old skill carried is still carried (anchor phrases, read from the OLD blob)
  C4  every ruling id the skill cites exists in the PACK's _rulings.json
  C5  the skill's reader and ASK commands RUN inside a copy of the pack with no repo on the path
  C6  pack-docs gate: no finding in the skill, and the finding delta against v1.0.13 is named
"""
import json, os, re, sys, glob, shutil, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
STAGE = os.path.abspath(sys.argv[1]); V13 = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None
SK = os.path.join(STAGE, "skills/generate-from-canon/SKILL.md")
text = open(SK, encoding="utf-8").read()
res, fails = {}, []
def arm(k, ok, **kw):
    res[k] = dict(ok=bool(ok), **kw); print("%-3s %s %s" % (k, "PASS" if ok else "FAIL", json.dumps(kw, ensure_ascii=False)[:600]))
    ok or fails.append(k)

# C1 — paths and commands
EXT = r"\.(py|json|html|css|js|md|png|svg|jsonl)"
cands = set()
for m in re.finditer(r"`([^`\n]+)`", text):
    t = m.group(1).strip()
    for tok in re.findall(r"(?:python3\s+)?([A-Za-z0-9_.<>*\-/]+%s|[A-Za-z0-9_\-]+/[A-Za-z0-9_.<>*\-/]*/)" % EXT, t):
        tok = tok[0] if isinstance(tok, tuple) else tok
        cands.add(tok)
for m in re.finditer(r"python3\s+(\S+\.py)", text):
    cands.add(m.group(1))
skip, miss, ok = [], [], []
for c in sorted(cands):
    if c.startswith(("path/to", "your-")) or "/" not in c and not c.endswith(".py"):
        skip.append(c); continue
    if c in ("seed.json", "seed-panel-2.json"): skip.append(c); continue
    if c.startswith("briefs/"): skip.append(c + "  (the designer's PROJECT folder, written by ADS-grill-me — not a pack path)"); continue
    if re.fullmatch(r"[a-z-]+/[a-z-]+/", c) and c.split("/")[0] not in ("knowledge", "showroom", "skills", "ci-template", "cold-start"): skip.append(c + "  (a token name, not a path)"); continue
    g = re.sub(r"<[^>]+>", "*", c)
    hits = glob.glob(os.path.join(STAGE, g)) or glob.glob(os.path.join(STAGE, "knowledge", g))
    if not hits and "*" in g:   # case-insensitive glob (the skill's own rule for slug/Slug)
        pat = re.compile(re.escape(g).replace(r"\*", ".*") + "$", re.I)
        hits = [p for p in glob.glob(os.path.join(STAGE, "**"), recursive=True) if pat.search(os.path.relpath(p, STAGE))]
    (ok if hits else miss).append(c)
arm("C1", not miss, resolved=len(ok), missing=miss, skipped_placeholders=skip)

# C2 — the nailed lines
proc = text[text.index("## Procedure"):]
step1 = proc[proc.index("1. **Seed"):proc.index("2. **Decide")]
checks = {
    "no 'splice' instruction": not re.search(r"\bsplice\b", text, re.I),
    "no 'edit it down'": "edit it down" not in text,
    "no 'start from knowledge/snippets/Template…'": not re.search(r"start\s+from\s+`?knowledge/snippets/Template", text),
    "step 1 (the first building step) calls the reader": "knowledge/_compose_slice.py" in step1,
    "templates fenced as reference fixtures": "reference fixture" in text and "never the starting point" in text.lower().replace("\n", " ") or "is never the starting point" in text,
    "rule 7a exists (projections point at it)": re.search(r"^7a\. \*\*Dashboards are bento-first", text, re.M) is not None,
    "bento question survives verbatim": "**dashboard bento — is that right?**" in text,
    "a skip is a yes (s230-D1 beat 2)": "A skip is a yes" in text,
}
arm("C2", all(checks.values()), checks=checks)

# C3 — every hard rule of the OLD skill still carried
old = subprocess.run(["git", "--no-optional-locks", "show", "HEAD:apollo-spider/skills/generate-from-canon/SKILL.md"],
                     cwd=ROOT, capture_output=True, text=True).stdout
ANCHORS = ["Only what exists", "Gaps", "APOLLO-DEMO", "FAIL:DEMO-CHROME-COPIED", "NOTE:AUTHORED-JS", "FAIL:BEHAVIOUR-NOT-LOADED",
           "#behaviour-manifest", "Bind every visual value to a token", "Type via composites", ".t-cm-", ".t-ed-",
           "mono", "common", "console", "supercharge", "s227-D8", "_themes.json", "#DA1A00", "#F6604C", "mark only",
           "White-on-error does not exist", "_bento_edit_rails.json", "{1, 2, 4, 16, 24, 40}", "dashboard bento — is that right?",
           "A skip is a yes", "Template-dashboard.reference.html", "groupsWith", "ref:null", "tpl-group-lead",
           "_validate_composition.py", "knowledge/assets/icons/", "data-bespoke", "masterbrand-light-colour.svg",
           "masterbrand-dark-colour.svg", "antiPatterns", "mustNotNeighbour", "default / hover / pressed / focus / disabled / loading / error",
           "Sentence case", "Carry provenance", "const DATA", "s258-D2", "Every control does something visible",
           "closest('[data-action]')", "State survives a reload", "localStorage", "Zero uncaught JS errors", "footer",
           ".cn-chart-bar", "dispatchEvent(new Event('resize'))", "briefs/*-grill.md", "ADS-grill-me", "which theme",
           "mono makes every radius zero", "data-apollo-theme", "data-theme", "data-mode" , "_RUNBOOK-compose-from-canon.md",
           "_validate_screen.py", "gen_provenance_receipt.py --mint", "_validate_receipt.py", "FAIL:NO-RECEIPT",
           "not driven: no browser in this session", "behaviour manifest", "ADS-draft-a-new-pattern", "ADS-check-with-gates"]
lost = [a for a in ANCHORS if a in old and a not in text]
not_in_old = [a for a in ANCHORS if a not in old]
arm("C3", not lost, carried=len(ANCHORS) - len(lost) - len(not_in_old), lost=lost, anchors_not_in_old=not_in_old)

# C4 — ruling ids cited exist in the PACK
ids = sorted(set(re.findall(r"`(s\d{3}-D\d+)`", text) + re.findall(r"\b(s\d{3}-D\d+)\b", text)))
R = {r["id"] for r in json.load(open(os.path.join(STAGE, "knowledge/_rulings.json")))["rulings"]}
arm("C4", all(i in R for i in ids), cited=ids, missing=[i for i in ids if i not in R])

# C5 — run the skill's own reader commands inside a COPY of the pack (no repo anywhere on the path)
tmp = tempfile.mkdtemp(prefix="r4a-coldpack-", dir="/dev/shm")
try:
    shutil.copytree(os.path.join(STAGE, "knowledge"), os.path.join(tmp, "knowledge"),
                    ignore=shutil.ignore_patterns("assets", "photography*"))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH="")
    cmds = [["knowledge/_compose_slice.py", "Build an overview dashboard for a group treasurer: cash, liquidity, "
             "payments awaiting approval", "--out", "seed.json", "--explain"],
            ["knowledge/_compose_slice.py", "one panel's question", "--intent", "change-over-time", "--shape",
             "time-series × 1–5-series", "--out", "seed-panel-2.json"],
            ["knowledge/_compose_slice.py", "--ask", "what governs component:data-grid?", "--seed", "seed.json"],
            ["knowledge/_compose_slice.py", "--ask", "which components answer change-over-time?"],
            ["knowledge/_compose_slice.py", "--ask", "what must component:drawer not sit next to?"],
            ["knowledge/_compose_slice.py", "--help"]]
    out5 = []
    for c in cmds:
        r = subprocess.run([sys.executable] + c, cwd=tmp, capture_output=True, text=True, env=env, timeout=120)
        out5.append({"cmd": " ".join(c[1:3])[:60], "rc": r.returncode,
                     "repo_path_leak": ROOT in (r.stdout + r.stderr)})
    seed = json.load(open(os.path.join(tmp, "seed.json")))
    tmpl = [c["id"] for c in seed.get("components", []) if "template" in c["id"]]
    arm("C5", all(o["rc"] == 0 and not o["repo_path_leak"] for o in out5), runs=out5,
        seed_components=len(seed.get("components") or []), seed_governs=len(seed.get("governs") or []),
        seed_obeys=len(seed.get("obeys") or []), seed_names_templates=tmpl,
        live_rulings=json.loads(subprocess.run([sys.executable] + cmds[3], cwd=tmp, capture_output=True, text=True, env=env).stdout)["live"]["rulings"])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# C7 — what the skill DESCRIBES exists in the pack: the seed contract, the bento grammar, the chart engine
seed_keys = ["components", "governs", "obeys", "mustNot", "tokens", "assets", "unresolved", "sized", "$nulls"]
tmp = tempfile.mkdtemp(prefix="r4a-coldpack-", dir="/dev/shm")
try:
    shutil.copytree(os.path.join(STAGE, "knowledge"), os.path.join(tmp, "knowledge"), ignore=shutil.ignore_patterns("assets", "photography*"))
    subprocess.run([sys.executable, "knowledge/_compose_slice.py", "Build an overview dashboard", "--out", "seed.json"],
                   cwd=tmp, capture_output=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), timeout=120)
    seed = json.load(open(os.path.join(tmp, "seed.json")))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
row_keys = ["id", "when", "snippet", "meta", "why", "alternate"]
css = open(os.path.join(STAGE, "knowledge/canon/canon.css"), encoding="utf-8").read()
grammar = {sel: (sel in css) for sel in [".cn-template-dashboard-bento", ".tpl-page", ".tpl-wall", ".tpl-group",
           ".c-bento__grid", ".c-bento__tile", '[data-bento-role="dashboard"]', "--bento-dashboard-main", "--bento-dashboard-sub"]}
tm = json.load(open(os.path.join(STAGE, "knowledge/components/template-dashboard-bento.meta.json")))
line = open(os.path.join(STAGE, "knowledge/snippets/Chart-line.reference.html"), encoding="utf-8").read()
c7 = {"seed has every field the skill names": all(k in seed for k in seed_keys),
      "component rows carry id/when/snippet/meta/why/alternate": all(all(k in c for k in row_keys) for c in seed["components"]),
      "bento grammar classes in pack canon.css": all(grammar.values()),
      "template meta carries $bentoGrammar": "$bentoGrammar" in tm,
      "chart snippet carries the engine (dvRender)": "function dvRender(" in line,
      "dv-render.js ships": os.path.exists(os.path.join(STAGE, "knowledge/canon/dv-render.js")),
      "grill-me + check-with-gates skills ship": all(os.path.exists(os.path.join(STAGE, "skills", k, "SKILL.md")) for k in ("grill-me", "check-with-gates", "draft-a-new-pattern")),
      "copilot index points at this skill": "skills/generate-from-canon/SKILL.md" in open(os.path.join(STAGE, ".github/copilot-instructions.md"), encoding="utf-8").read()}
arm("C7", all(c7.values()), checks=c7, missing_seed_keys=[k for k in seed_keys if k not in seed], grammar=grammar)

# C6 — pack-docs gate: nothing in the skill; delta vs v1.0.13 named
sys.path.insert(0, os.path.join(ROOT, "knowledge/_release")); sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _gate_pack_docs as PD
fc, _ = PD.audit(STAGE, pack_version="1.0.14")
in_skill = [f for f in fc if f[1].startswith("skills/generate-from-canon")]
delta = None
if V13:
    f13, _ = PD.audit(V13, pack_version="1.0.13")
    k = lambda f: (f[0], f[1], f[2]); s13 = {k(f) for f in f13}; sc = {k(f) for f in fc}
    delta = {"v1.0.13": len(f13), "candidate": len(fc), "new": sorted(sc - s13), "gone": sorted(s13 - sc)}
arm("C6", not in_skill, findings_in_skill=in_skill, delta=delta)

json.dump({"stage": STAGE, "results": res}, open(os.path.join(HERE, "verify-skill-results.json"), "w"), ensure_ascii=False, indent=1)
print("VERDICT:", "PASS" if not fails else "FAIL " + ",".join(fails))
sys.exit(1 if fails else 0)
