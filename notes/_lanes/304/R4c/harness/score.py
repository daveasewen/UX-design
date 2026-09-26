#!/usr/bin/env python3
"""score.py — the Apollo cold-run EVAL HARNESS (#304 lane R4c). Scores a generated page.

WHAT IT DOES
  Given the entry page of a generated build, it scores the four-part hand rubric of the
  #246/#258 cold-run series (visually rich · full · persistent · interactive, 0-3 each)
  MECHANICALLY where a measurement exists, plus: composed-vs-traced (structural and textual
  similarity to the pack's template snippets), component variety, charts used vs the
  prompt's ask, theme correctness (Common), a11y findings, the pack's own gates, and 4b's
  geometry / own-size gates when they exist (picked up BY PATH; absent = said so, never faked).
  Parts that stay JUDGMENT are listed on every scorecard for Dave's eye, unscored.

PHASES (each writes runs/<id>/<phase>.json; each fits one 180 s seat call)
  stage    copy the pack (zip or dir; default Spider v1.0.13) to $HOME/r4c/stage/<id>/pack,
           and either score the page IN PLACE (default) or, with --copy-out DIR, copy a cold
           run's output folder to stage/<id>/out beside the pack (so ../pack/… links resolve).
  static   no browser: root attrs, components, chart types, trace similarity, raw/leaked hex.
  gates    the PACK's own validators on the page: _validate_screen.py (receipt · compose ·
           composition · icons · a11y) and _validate_dataviz.check_file. Writes land in the
           per-run pack copy, never in the repo.
  render   browser (seat env): 1440x1000 light + dark, HSBC-face check, theme tokens, charts
           (rendered marks, legend, table, CLIPPED), native geometry signals, rendered a11y,
           errors; screenshots to runs/<id>/shots/. Linked local sub-pages probed light.
  drive    browser: persistence (state → reload → compare), nav views, every control family
           (bounded, deterministic order), tooltips, theme switch, dialogs/downloads.
  ext      4b's geometry and own-size gates, if found (see EXT_GATES below). exit 77 = absent.
  card     scorecard.json + scorecard.html from whatever phases exist (missing = 'not run').
  all      stage→card, skipping phases already on disk unless --force.
  compare  side-by-side page over several runs:  compare --runs a,b,c --out FILE.html
  selftest the harness's own test: planted-bad vs known-good fixtures must separate.

INVOCATION (browser phases need the seat env IN THE SAME CALL):
  cd "$HOME/mnt/Projects--UX-design" && export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; \\
    source knowledge/_render/seat_env.sh; \\
    python3 notes/_lanes/304/R4c/harness/score.py all --run-id X --page PATH [--profile ceo-common]

Every mechanical score is reproducible: same page + same pack + same phase command = same
number (drive order is fixed; timers fixed; no randomness). Scores carry their earning fact.
"""
import sys as _s; _s.dont_write_bytecode = True  # never litter the mount with __pycache__
import argparse, glob, hashlib, html as htmlmod, json, os, re, shutil, subprocess, sys, time, zipfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)                                   # notes/_lanes/304/R4c
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
RUNS = os.path.join(LANE, "runs")
SEAT = os.path.join(os.environ.get("HOME", "/tmp"), "r4c")
PACKS = os.path.join(SEAT, "packs")
STAGE = os.path.join(SEAT, "stage")
DEFAULT_PACK = os.path.join(REPO, "apollo-spider", "dist", "Apollo-Spider-v1.0.13.zip")
HARNESS_VERSION = "r4c-1.0"

# 4b's gates, looked up BY PATH in this order (first hit wins per kind). A gate is called
#   python3 <gate> <page.html> --json <out.json>
# 77 = could-not-ask. The verdict and 0-3 score are read from the gate's JSON ("verdict", "score"),
# as 4b's _validate_geometry.py writes them (it is ADVISORY and exits 0 whatever it finds); only a gate
# with no JSON verdict falls back to its exit code. Needs the seat env in the same call (it renders).
EXT_GATES = {
    "geometry": ["$R4C_GEOMETRY_GATE", "knowledge/_validate_geometry.py",
                 "notes/_lanes/304/R4b/**/_validate_geometry*.py", "notes/_lanes/304/R4b/**/*geometry*gate*.py"],
    "own_size": ["$R4C_OWNSIZE_GATE", "knowledge/_validate_own_size.py", "knowledge/_validate_own*.py",
                 "notes/_lanes/304/R4b/**/_validate_own_size*.py", "notes/_lanes/304/R4b/**/*own*size*.py"],
}

JUDGMENT = [
    "Taste: does the page look like Apollo at its best — hierarchy, rhythm, restraint (Dave's eye on the light/dark shots).",
    "Alignment and spacing that the geometry signals cannot name (optical alignment, crowding, the 'sloppiness class' of #288).",
    "Whether each chart is the RIGHT chart for its figure (form-to-question fit), not only present and rendered.",
    "Data believability: realistic entities, currencies, FX and magnitudes for a CEO audience.",
    "Whether the overview actually answers the three CEO questions, as read by a person, not by keyword.",
    "Whether each workflow (approve, acknowledge, service request) is plausible end to end, beyond 'the DOM changed'.",
    "Composed vs traced is MEASURED as similarity; whether the composition is GOOD composition is judgment.",
]

def jload(p, default=None):
    try:
        return json.load(open(p))
    except Exception:
        return default

def jdump(obj, p):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True, default=str)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def run_dir(rid):
    return os.path.join(RUNS, rid)

def meta_of(rid):
    m = jload(os.path.join(run_dir(rid), "meta.json"))
    if not m:
        sys.exit("run %s has no meta.json — run `stage` first" % rid)
    return m

# ----------------------------------------------------------------------------- stage
def unpack(pack):
    """Return the unzipped pack ROOT dir (cached under $HOME/r4c/packs/<zip stem>/)."""
    if os.path.isdir(pack):
        return os.path.abspath(pack)
    stem = os.path.splitext(os.path.basename(pack))[0]
    dest = os.path.join(PACKS, stem)
    marker = os.path.join(dest, ".sha256")
    zsha = sha256(pack)
    if not (os.path.exists(marker) and open(marker).read().strip() == zsha):
        shutil.rmtree(dest, ignore_errors=True)
        os.makedirs(dest)
        zipfile.ZipFile(pack).extractall(dest)
        open(marker, "w").write(zsha)
    tops = [d for d in os.listdir(dest) if os.path.isdir(os.path.join(dest, d))]
    return os.path.join(dest, tops[0]) if len(tops) == 1 else dest

def cmd_stage(a):
    rid = a.run_id
    rd = run_dir(rid)
    os.makedirs(rd, exist_ok=True)
    pack = os.path.abspath(a.pack or DEFAULT_PACK)
    proot = unpack(pack)
    st = os.path.join(STAGE, rid)
    shutil.rmtree(st, ignore_errors=True)
    os.makedirs(st)
    shutil.copytree(proot, os.path.join(st, "pack"), symlinks=True)
    if a.copy_out:
        src = os.path.abspath(a.copy_out)
        shutil.copytree(src, os.path.join(st, "out"), symlinks=True,
                        ignore=shutil.ignore_patterns("pack", "Apollo-Spider-*", "*.zip", "node_modules"))
        entry = os.path.join(st, "out", os.path.relpath(os.path.abspath(a.page), src))
    else:
        entry = os.path.abspath(a.page)
    if not os.path.exists(entry):
        sys.exit("entry page not found: " + entry)
    m = {"run_id": rid, "label": a.label or rid, "kind": a.kind, "entry": entry,
         "page_source": os.path.abspath(a.page), "page_sha256": sha256(entry),
         "pack": pack, "pack_sha256": sha256(pack) if os.path.isfile(pack) else None,
         "pack_root_staged": os.path.join(st, "pack"), "stage": st,
         "profile": a.profile, "harness": HARNESS_VERSION, "staged_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    jdump(m, os.path.join(rd, "meta.json"))
    print("STAGED %s entry=%s pack=%s" % (rid, entry, os.path.basename(pack)))
    return m

# ----------------------------------------------------------------------------- static
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}

class Tree(HTMLParser):
    """Flat, ordered element list — enough for shingles, classes, attrs, text. stdlib only."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.els, self.stack, self.texts = [], [], []
        self.skip = 0          # inside script/style/template
        self.svg = 0           # inside svg (children not tokenised)
        self.html_attrs, self.body_attrs = {}, {}
        self.styles, self.scripts_src, self.links = [], [], []
        self._cur_style = None
    def handle_starttag(self, tag, attrs):
        d = {k: (v or "") for k, v in attrs}
        if tag == "html": self.html_attrs = d
        if tag == "body": self.body_attrs = d
        if tag == "link" and "stylesheet" in d.get("rel", ""): self.links.append(d.get("href", ""))
        if tag == "script" and d.get("src"): self.scripts_src.append(d["src"])
        if tag in ("script", "style", "template"):
            if tag == "style": self._cur_style = []
            self.skip += 1
            if tag not in VOID: self.stack.append(tag)
            return
        if self.skip:
            if tag not in VOID: self.stack.append(tag)
            return
        if self.svg:
            if tag not in VOID: self.stack.append(tag)
            if tag == "svg": self.svg += 1
            return
        cls = sorted(c for c in d.get("class", "").split() if c)
        self.els.append({"tag": tag, "cls": cls, "attrs": d, "depth": len(self.stack)})
        if tag == "svg": self.svg += 1
        if tag not in VOID: self.stack.append(tag)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1] == tag: self.stack.pop()
        if tag == "svg" and self.svg: self.svg -= 1
    def handle_endtag(self, tag):
        if tag in VOID: return
        if tag in ("script", "style", "template") and self.skip:
            if tag == "style" and self._cur_style is not None:
                self.styles.append("".join(self._cur_style)); self._cur_style = None
            self.skip -= 1
        elif tag == "svg" and self.svg:
            self.svg -= 1
        # pop to the matching tag (tolerant of sloppy html)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag:
                del self.stack[i:]
                break
    def handle_data(self, data):
        if self._cur_style is not None:
            self._cur_style.append(data); return
        if self.skip or self.svg: return
        t = " ".join(data.split())
        if t: self.texts.append(t)

def parse(path):
    t = Tree()
    t.feed(open(path, encoding="utf-8", errors="replace").read())
    return t

def shingles(tree, k=5):
    toks = [e["tag"] + "." + ".".join(e["cls"]) for e in tree.els if e["tag"] not in ("html", "head", "meta", "link", "title")]
    return {tuple(toks[i:i + k]) for i in range(max(0, len(toks) - k + 1))}

def known_slugs(pack_root):
    css = open(os.path.join(pack_root, "knowledge", "canon", "canon.css"), encoding="utf-8", errors="replace").read()
    return sorted(set(re.findall(r"\.cn-([a-z0-9]+(?:-[a-z0-9]+)*)\b", css)))

_SIG = {}
def comp_signatures(pack_root):
    """slug -> classes canon scopes ONLY under that component (:where(.cn-<slug>) .x, x in no other scope).
    A component is present by signature when >=2 of its own classes are on the page (pages that splice a
    component's inner markup without the cn- scope wrapper still get counted)."""
    if pack_root in _SIG: return _SIG[pack_root]
    import collections
    css = open(os.path.join(pack_root, "knowledge", "canon", "canon.css"), encoding="utf-8", errors="replace").read()
    m = collections.defaultdict(set)
    for a_, b_ in re.findall(r":where\(\.cn-([a-z0-9-]+)\)\s*\.([a-zA-Z][\w-]*)", css): m[a_].add(b_)
    # templates re-scope their parts' classes (.cn-template-dashboard-bento .kpi-tile …), so a part's
    # uniqueness is counted over PART scopes only; a template is known by classes no other scope uses.
    tpl = {k for k in m if k.startswith("template-")}
    cnt_parts = collections.Counter(c for k, v in m.items() if k not in tpl for c in v)
    cnt_all = collections.Counter(c for v in m.values() for c in v)
    ok = lambda c: not c.startswith(("is-", "has-", "js-", "demo", "spec"))
    _SIG[pack_root] = {k: {c for c in v if ok(c) and (cnt_all[c] == 1 if k in tpl else cnt_parts[c] == 1)} for k, v in m.items()}
    return _SIG[pack_root]

def comps_in(trees, pack_root, slugs):
    sig = comp_signatures(pack_root)
    cls = set()
    for t in trees:
        for e in t.els: cls |= set(e["cls"])
    scoped = {c[3:] for c in cls if c.startswith("cn-") and c[3:] in slugs}
    by_sig = {k for k, v in sig.items() if len(v & cls) >= 2 or (k in cls and not k.startswith("template-"))}  # class named for the part
    return scoped, by_sig

def theme_hexes(pack_root):
    reg = jload(os.path.join(pack_root, "knowledge", "tokens", "themes", "_themes.json"), {}) or {}
    own = {}
    for tid, t in (reg.get("themes") or {}).items():
        for hx in (t.get("ownsHexes") or {}):
            if hx.startswith("#"): own[hx.upper()] = t.get("attr")
    return own

def local_pages(entry, tree):
    """Local .html files the entry links to (same folder tree), plus itself. Max 20."""
    base = os.path.dirname(entry)
    out = [entry]
    for e in tree.els:
        if e["tag"] != "a": continue
        href = e["attrs"].get("href", "").split("#")[0].split("?")[0]
        if not href or re.match(r"^[a-z]+:", href) or not href.lower().endswith((".html", ".htm")): continue
        p = os.path.normpath(os.path.join(base, htmlmod.unescape(href)))
        if os.path.exists(p) and p not in out and p.startswith(base):
            out.append(p)
    return out[:20]

TRACE_RULE = ("trace_index = 0.4*DOM shingle containment + 0.3*template text reuse + 0.3*template-only classes present; "
              ">=0.30 TRACED, >=0.15 PARTLY TRACED, else COMPOSED — calibrated on pages whose provenance the record states "
              "(7 bento-first splices read 0.334-0.561; 2 template-closed compositions read 0.041)")

def trace_roots(staged_root):
    roots = [("staged pack", staged_root)]
    try:
        ref = unpack(DEFAULT_PACK)
        if os.path.realpath(ref) != os.path.realpath(staged_root): roots.append(("v1.0.13 reference", ref))
    except Exception:
        pass
    return roots

def trace_against(trees, roots):
    pshing, pcls, ptext = set(), set(), []
    for t in trees:
        pshing |= shingles(t)
        for e in t.els: pcls |= set(e["cls"])
        ptext.append(" ".join(t.texts))
    ptext = " ".join(ptext)
    trace = []
    for label, pr in roots:
        tpl_dir = os.path.join(pr, "knowledge", "snippets")
        tpls = sorted(glob.glob(os.path.join(tpl_dir, "Template-*.reference.html")))
        others = [f for f in glob.glob(os.path.join(tpl_dir, "*.reference.html")) if f not in tpls]
        other_cls = set()
        for f in others:
            for cl in re.findall(r'class="([^"]*)"', open(f, encoding="utf-8", errors="replace").read()):
                other_cls |= set(cl.split())
        for f in tpls:
            tt = parse(f)
            ts = shingles(tt)
            inter = len(pshing & ts)
            containment = inter / len(pshing) if pshing else 0.0
            jacc = inter / len(pshing | ts) if (pshing | ts) else 0.0
            ttexts = sorted({x for x in tt.texts if len(x) >= 16})
            reused = [x for x in ttexts if x in ptext]
            text_reuse = len(reused) / len(ttexts) if ttexts else 0.0
            tcls = set()
            for e in tt.els: tcls |= set(e["cls"])
            uniq = sorted(c for c in tcls if c not in other_cls and not c.startswith(("cn-", "t-", "is-", "has-")))
            uniq_hit = [c for c in uniq if c in pcls]
            uniq_frac = len(uniq_hit) / len(uniq) if uniq else 0.0
            index = round(0.4 * containment + 0.3 * text_reuse + 0.3 * uniq_frac, 3)
            trace.append({"template": os.path.basename(f).replace(".reference.html", ""), "from": label,
                          "shingle_containment": round(containment, 3), "shingle_jaccard": round(jacc, 3),
                          "text_reuse": round(text_reuse, 3), "text_reused_n": len(reused), "text_strings_n": len(ttexts),
                          "text_reused_sample": reused[:6], "template_unique_classes_frac": round(uniq_frac, 3),
                          "template_unique_hit": uniq_hit[:12], "trace_index": index})
    trace.sort(key=lambda r: (-r["trace_index"], r["template"], r["from"]))
    top = trace[0] if trace else None
    verdict = "n/a"
    if top:
        verdict = "TRACED" if top["trace_index"] >= 0.30 else ("PARTLY TRACED" if top["trace_index"] >= 0.15 else "COMPOSED")
    return {"verdict": verdict, "top": top, "all": trace[:4]}

def cmd_static(a):
    m = meta_of(a.run_id)
    prof = jload(os.path.join(HERE, "profiles", m["profile"] + ".json"))
    pr = m["pack_root_staged"]
    slugs = set(known_slugs(pr))
    owners = theme_hexes(pr)
    entry_tree = parse(m["entry"])
    pages = local_pages(m["entry"], entry_tree)
    per = []
    comps, ctypes, charts_total, demo_markers = set(), {}, 0, 0
    hexes, leaks, alltext = [], [], []
    for p in pages:
        t = entry_tree if p == m["entry"] else parse(p)
        src = open(p, encoding="utf-8", errors="replace").read()
        c = set()
        for e in t.els:
            for cl in e["cls"]:
                if cl.startswith("cn-") and cl[3:] in slugs: c.add(cl[3:])
        comps |= c
        types = [e["attrs"].get("data-dv-type") for e in t.els if "dv" in e["cls"] and e["tag"] == "figure"]
        for ty in types: ctypes[ty] = ctypes.get(ty, 0) + 1
        charts_total += len(types)
        demo_markers += src.count("APOLLO-DEMO")
        css = "\n".join(t.styles) + "\n" + "\n".join(e["attrs"].get("style", "") for e in t.els)
        css_nc = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        hx = [h.upper() for h in re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", css_nc)]
        hexes += hx
        prof_attr = (prof.get("theme") or {}).get("attr")
        ok_attrs = {prof_attr} | set((prof.get("theme") or {}).get("aliases", [])) if prof_attr else None
        for h in hx:
            own = owners.get(h)
            if own and ok_attrs and own not in ok_attrs:
                leaks.append({"hex": h, "owned_by": own, "page": os.path.basename(p)})
        alltext.append(" ".join(t.texts))
        per.append({"page": os.path.relpath(p, os.path.dirname(m["entry"])), "components": sorted(c),
                    "chart_types": types, "html_attrs": t.html_attrs,
                    "body_theme_attrs": {k: v for k, v in t.body_attrs.items() if k in ("data-theme", "data-apollo-theme")},
                    "bytes": len(src.encode())})
    # ---- trace similarity against every template snippet (staged pack AND the v1.0.13 reference)
    trees = [entry_tree if p == m["entry"] else parse(p) for p in pages]
    scoped, by_sig = comps_in(trees, pr, slugs)
    comps = scoped | by_sig
    tr = trace_against(trees, trace_roots(pr))
    trace, top, verdict = tr["all"], tr["top"], tr["verdict"]
    # ---- prompt keyword coverage (text only; drive measures liveness)
    full_text = " ".join(alltext).lower()
    def hits(d):
        return {k: bool(re.search(v, full_text, re.I)) for k, v in (d or {}).items()}
    out = {
        "pages": per, "page_count": len(pages),
        "components": sorted(comps), "component_count": len(comps),
        "components_scoped": sorted(scoped), "components_by_signature_only": sorted(by_sig - scoped),
        "chart_types_static": ctypes, "charts_static": charts_total,
        "apollo_demo_markers": demo_markers,
        "raw_hex_in_authored_css": len(hexes), "raw_hex_sample": sorted(set(hexes))[:12],
        "theme_hex_leaks": leaks,
        "root": per[0]["html_attrs"] if per else {},
        "theme_on_body": [p["page"] for p in per if p["body_theme_attrs"]],
        "trace": {"verdict": verdict, "top": top, "all": trace[:4], "thresholds": TRACE_RULE},
        "keywords": {"kpis": hits(prof.get("kpis")), "questions": hits(prof.get("questions")),
                     "views_text": hits(prof.get("view_patterns"))},
        "stylesheets": per and entry_tree.links, "scripts": entry_tree.scripts_src,
    }
    jdump(out, os.path.join(run_dir(a.run_id), "static.json"))
    print("STATIC %s pages=%d comps=%d charts=%d trace=%s(%s %.3f) rawhex=%d leaks=%d" % (
        a.run_id, len(pages), len(comps), charts_total, verdict, top and top["template"], top and top["trace_index"] or 0,
        len(hexes), len(leaks)))
    return out

# ----------------------------------------------------------------------------- gates
def cmd_gates(a):
    m = meta_of(a.run_id)
    kn = os.path.join(m["pack_root_staged"], "knowledge")
    out = {"pack_gates_from": m["pack"], "screen": None, "dataviz": None}
    env = dict(os.environ, SCREEN_GATE_REBIND="1", PYTHONDONTWRITEBYTECODE="1")
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, os.path.join(kn, "_validate_screen.py"), m["entry"]],
                           cwd=kn, env=env, capture_output=True, text=True, timeout=100)
        txt = r.stdout + r.stderr
        lines = [ln for ln in txt.splitlines() if ln.startswith("- ")]
        out["screen"] = {"exit": r.returncode, "verdict": "PASS" if r.returncode == 0 else "FAIL",
                         "lines": lines[:40], "tail": txt.strip().splitlines()[-3:]}
    except Exception as e:
        out["screen"] = {"exit": None, "verdict": "COULD-NOT-ASK", "error": str(e)}
    code = ("import sys,json; sys.path.insert(0,%r); import _validate_dataviz as dv\n"
            "res, adv = dv.check_file(%r)\n"
            "print(json.dumps({'charts':len(res),'blocking':[[t,c,b] for t,c,B,A in res for b in B],"
            "'advisory':[[t,c,x] for t,c,B,A in res for x in A]+[['file','',x] for x in adv]}))") % (kn, m["entry"])
    try:
        r = subprocess.run([sys.executable, "-c", code], cwd=kn, env=env, capture_output=True, text=True, timeout=60)
        d = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 else None
        out["dataviz"] = d if d is not None else {"verdict": "COULD-NOT-ASK", "error": (r.stderr or "")[-600:]}
        if d is not None:
            out["dataviz"]["verdict"] = "FAIL" if d["blocking"] else "PASS"
            out["dataviz"]["blocking_n"] = len(d["blocking"]); out["dataviz"]["advisory_n"] = len(d["advisory"])
            out["dataviz"]["blocking"] = d["blocking"][:20]; out["dataviz"]["advisory"] = d["advisory"][:20]
    except Exception as e:
        out["dataviz"] = {"verdict": "COULD-NOT-ASK", "error": str(e)}
    out["seconds"] = round(time.time() - t0, 1)
    jdump(out, os.path.join(run_dir(a.run_id), "gates.json"))
    print("GATES %s screen=%s dataviz=%s (%ss)" % (a.run_id, out["screen"].get("verdict"),
          out["dataviz"].get("verdict"), out["seconds"]))
    return out

# ----------------------------------------------------------------------------- ext (4b)
def find_ext(kind):
    for pat in EXT_GATES[kind]:
        if pat.startswith("$"):
            v = os.environ.get(pat[1:])
            if v and os.path.exists(v): return v
            continue
        hits = sorted(glob.glob(os.path.join(REPO, pat), recursive=True))
        hits = [h for h in hits if "/_tests/" not in h and "selftest" not in os.path.basename(h)]
        if hits: return hits[0]
    return None

def cmd_ext(a):
    m = meta_of(a.run_id)
    out = {}
    for kind in EXT_GATES:
        g = find_ext(kind)
        if not g:
            out[kind] = {"status": "ABSENT", "searched": EXT_GATES[kind]}
            continue
        jp = os.path.join(m["stage"], "ext-%s.out.json" % kind)   # seat-local: the mount refuses deletes
        if os.path.exists(jp): os.remove(jp)          # never read a previous run's verdict
        try:
            r = subprocess.run([sys.executable, g, m["entry"], "--json", jp], cwd=REPO,
                               capture_output=True, text=True, timeout=150)
            res = jload(jp)
            one = res[0] if isinstance(res, list) and res else (res.get("pages", [res])[0] if isinstance(res, dict) and isinstance(res.get("pages"), list) and res.get("pages") else res)
            verdict = (one or {}).get("verdict") if isinstance(one, dict) else None
            status = verdict or {0: "PASS", 1: "FINDINGS", 77: "COULD-NOT-ASK"}.get(r.returncode, "EXIT %d" % r.returncode)
            if r.returncode == 77: status = "COULD-NOT-ASK"
            out[kind] = {"status": status, "score": (one or {}).get("score") if isinstance(one, dict) else None,
                         "counts": (one or {}).get("counts") if isinstance(one, dict) else None,
                         "findings_n": len((one or {}).get("findings", [])) if isinstance(one, dict) else None,
                         "findings_sample": [{k: f.get(k) for k in ("clause", "severity", "width", "where", "measured", "expected")} for f in ((one or {}).get("findings") or [])[:12]] if isinstance(one, dict) else None,
                         "font_ok": (one or {}).get("font_ok") if isinstance(one, dict) else None,
                         "gate": os.path.relpath(g, REPO), "gate_sha256": sha256(g), "exit": r.returncode,
                         "stdout_tail": (r.stdout + r.stderr).strip().splitlines()[-8:]}
        except Exception as e:
            out[kind] = {"status": "ERROR", "gate": os.path.relpath(g, REPO), "error": str(e)}
    jdump(out, os.path.join(run_dir(a.run_id), "ext.json"))
    print("EXT %s %s" % (a.run_id, {k: v["status"] for k, v in out.items()}))
    return out

# ----------------------------------------------------------------------------- scoring
def band(x, cuts):
    """cuts = (c1, c2, c3) ascending; return 0..3."""
    return sum(1 for c in cuts if x >= c)

def score(rid):
    m = meta_of(rid)
    rd = run_dir(rid)
    prof = jload(os.path.join(HERE, "profiles", m["profile"] + ".json"))
    st, gt, rn, dr, ex = (jload(os.path.join(rd, n + ".json"), None) for n in ("static", "gates", "render", "drive", "ext"))
    S = {"dimensions": {}, "sections": {}, "missing_phases": [n for n, v in
         (("static", st), ("gates", gt), ("render", rn), ("drive", dr), ("ext", ex)) if v is None]}
    ent = (rn or {}).get("entry", {})
    light = ent.get("light") or {}
    subs = (rn or {}).get("subpages", [])
    # ---------- charts (rendered, over entry + subpages)
    charts = list(light.get("charts", []))
    for sp in subs: charts += sp.get("charts", [])
    rendered = [c for c in charts if c.get("marks", 0) > 0 and c.get("w", 0) > 20 and c.get("h", 0) > 20]
    clipped = [c for c in charts if c.get("clipped")]
    rtypes = sorted({c.get("type") for c in rendered if c.get("type")})
    with_legend = sum(1 for c in rendered if c.get("legend"))
    with_table = sum(1 for c in rendered if c.get("table"))
    tips = (dr or {}).get("tooltips", {})
    pack_types = prof["charts"]["pack_types"]
    slugs_known = set(known_slugs(m["pack_root_staged"]))
    comp_set = set((st or {}).get("components", []))
    for R_ in [light] + subs:
        comp_set |= {c[3:] for c in (R_.get("components_rendered") or []) if c[3:] in slugs_known}
    if os.path.exists(os.path.join(rd, "dom-light.html")):
        sc_, bs_ = comps_in([parse(os.path.join(rd, "dom-light.html"))], m["pack_root_staged"], slugs_known)
        comp_set |= sc_ | bs_
    templates_seen = sorted(c for c in comp_set if c.startswith("template-"))
    comp_set = {c for c in comp_set if not c.startswith("template-")}   # a template is a composition, not a part
    comps = len(comp_set)
    chart_slugs = sorted(c for c in comp_set if c.startswith("chart-"))
    # ---------- visually rich
    if st and rn:
        v = 0
        if prof["charts"].get("liberal"):
            # the CEO prompt asks to be LIBERAL with data visualisation: chart count and variety carry the score
            if comps >= 4 or len(rendered) >= 1: v = 1
            if comps >= 8 and len(rtypes) >= 3 and len(rendered) >= 4: v = 2
            if comps >= 12 and len(rtypes) >= 5 and len(rendered) >= 8 and not clipped: v = 3
            rule = "LIBERAL-DATAVIZ prompt · 1: >=4 components or >=1 rendered chart · 2: >=8 comps, >=3 chart types, >=4 charts · 3: >=12 comps, >=5 types, >=8 charts, 0 clipped"
        else:
            # the #246/#258 hand rubric: component breadth + charts that actually render
            if comps >= 4 or len(rendered) >= 1: v = 1
            if comps >= 8 and len(rendered) >= 1: v = 2
            if comps >= 12 and len(rendered) >= 1 and not clipped: v = 3
            rule = "hand-rubric equivalent · 1: >=4 components or >=1 rendered chart · 2: >=8 comps and a rendered chart · 3: >=12 comps, a rendered chart, 0 clipped"
        fact = "%d distinct Apollo components; %d charts rendered with marks (%d types: %s); %d clipped" % (
            comps, len(rendered), len(rtypes), ", ".join(rtypes) or "none", len(clipped))
        S["dimensions"]["visually_rich"] = {"score": v, "fact": fact, "rule": rule}
    # ---------- full
    if st and rn and dr:
        views_asked = len(prof.get("views", []))
        views_live = (dr.get("views") or {}).get("live_distinct", 0)
        kp = (st.get("keywords") or {}).get("kpis", {})
        qs = (st.get("keywords") or {}).get("questions", {})
        rows = max([light.get("max_table_rows", 0)] + [sp.get("max_table_rows", 0) for sp in subs])
        pager = light.get("pager", False) or any(sp.get("pager") for sp in subs)
        series = max([c.get("table_rows", 0) for c in charts] + [0])
        parts = []
        if views_asked: parts.append(("views live %d/%d" % (min(views_live, views_asked), views_asked), min(views_live, views_asked) / views_asked))
        else: parts.append(("views live %d (no list asked)" % views_live, min(1.0, views_live / 3)))
        if kp: parts.append(("KPI words %d/%d" % (sum(kp.values()), len(kp)), sum(kp.values()) / len(kp)))
        if qs: parts.append(("question words %d/%d" % (sum(qs.values()), len(qs)), sum(qs.values()) / len(qs)))
        parts.append(("largest record set %d rows%s" % (rows, " + pager" if pager else ""), 1.0 if rows >= prof["records"]["min_rows"] or (pager and rows >= 8) else rows / prof["records"]["min_rows"]))
        if prof.get("series_days"): parts.append(("longest chart series %d points" % series, min(1.0, series / prof["series_days"])))
        f = sum(p[1] for p in parts) / len(parts)
        S["dimensions"]["full"] = {"score": band(f, (0.3, 0.6, 0.85)), "fact": "; ".join(p[0] for p in parts) + " → coverage %.2f" % f,
            "rule": "mean of the coverage parts: >=0.30 → 1, >=0.60 → 2, >=0.85 → 3"}
    # ---------- persistent
    if dr:
        pe = dr.get("persistence", {})
        fam = pe.get("families", {})
        kept = [k for k, v in fam.items() if v.get("persisted")]
        tried = [k for k, v in fam.items() if v.get("changed")]
        S["dimensions"]["persistent"] = {"score": min(3, len(kept)),
            "fact": "survived reload: %s (of changed: %s; storage keys %d; url after %s)" % (
                ", ".join(kept) or "none", ", ".join(tried) or "none", pe.get("storage_keys", 0), pe.get("url_after", "")),
            "rule": "count of families {nav/view, filter, theme, sort, search} whose changed state survived a reload, capped at 3"}
    # ---------- interactive
    if dr:
        c = dr.get("controls", {})
        driven, live = c.get("driven", 0), c.get("live", 0)
        fam_live = sorted(k for k, v in (c.get("families") or {}).items() if v.get("live", 0) > 0)
        fam_dead = sorted(k for k, v in (c.get("families") or {}).items() if v.get("live", 0) == 0)
        ratio = live / driven if driven else 0.0
        errs = len(dr.get("pageerrors", [])) + len(light.get("pageerrors", []))
        v = 0
        if ratio >= 0.3 or len(fam_live) >= 2: v = 1
        if ratio >= 0.6 and len(fam_live) >= 5: v = 2
        if ratio >= 0.85 and len(fam_live) >= 8 and errs == 0: v = 3
        S["dimensions"]["interactive"] = {"score": v,
            "fact": "%d/%d driven controls changed the page (%.0f%%); live families %d: %s; dead: %s; page errors %d" % (
                live, driven, 100 * ratio, len(fam_live), ", ".join(fam_live) or "none", ", ".join(fam_dead) or "none", errs),
            "rule": "1: >=30% live or >=2 families · 2: >=60% and >=5 families · 3: >=85%, >=8 families, 0 page errors"}
    # ---------- sections (not in the four-part total)
    if st:
        tr = st["trace"]
        ctv = {"verdict": tr["verdict"], "top": tr["top"], "thresholds": tr["thresholds"], "measured_on": "page source"}
        dom = os.path.join(rd, "dom-light.html")
        if os.path.exists(dom):
            rt = trace_against([parse(dom)], trace_roots(m["pack_root_staged"]))
            ctv["rendered_dom"] = {"verdict": rt["verdict"], "top": rt["top"]}
            if rt["top"] and tr["top"] and rt["top"]["trace_index"] > tr["top"]["trace_index"]:
                ctv.update({"verdict": rt["verdict"], "top": rt["top"], "measured_on": "rendered DOM (higher than source)"})
        S["sections"]["composed_vs_traced"] = ctv
        S["sections"]["components"] = {"count": comps, "list": sorted(comp_set), "chart_components": chart_slugs,
                                       "templates_recognised": templates_seen, "static_count": st.get("component_count"), "rendered_only": sorted(comp_set - set(st.get("components", []))),
                                       "pages": st["page_count"], "apollo_demo_markers": st["apollo_demo_markers"]}
    S["sections"]["charts_vs_ask"] = {
        "rendered": len(rendered), "declared_static": (st or {}).get("charts_static"), "types_rendered": rtypes,
        "pack_types_available": len(pack_types), "types_used_frac": round(len(rtypes) / len(pack_types), 2) if pack_types else None,
        "on_overview": sum(1 for c in (light.get("charts") or []) if c.get("marks", 0) > 0),
        "min_overview_asked": prof["charts"]["min_charts_overview"], "liberal_asked": prof["charts"]["liberal"],
        "with_legend": with_legend, "with_table": with_table, "clipped": [{k: c.get(k) for k in ("id", "type", "clip_by", "clip_px", "page")} for c in clipped],
        "tooltips": tips, "subpages_with_charts": sum(1 for sp in subs if any(c.get("marks", 0) for c in sp.get("charts", [])))}
    th = {"asked": prof["theme"]["attr"]}
    if st:
        root = st.get("root", {})
        th.update({"root_class_canon": "canon" in root.get("class", "").split(), "data_apollo_theme": root.get("data-apollo-theme"),
                   "data_theme": root.get("data-theme"), "theme_attrs_on_body": st.get("theme_on_body"),
                   "raw_hex_in_authored_css": st.get("raw_hex_in_authored_css"), "leaked_hexes": st.get("theme_hex_leaks")})
    if rn:
        th["rendered_tokens"] = light.get("theme_tokens")
        th["vars_changed_by_theme_attr"] = light.get("theme_vars_changed")
    if dr:
        th["switch"] = dr.get("theme_switch")
    checks = []
    if prof["theme"]["attr"]:
        ok_attrs = [prof["theme"]["attr"]] + prof["theme"]["aliases"]
        checks.append(("root carries data-apollo-theme=%s" % prof["theme"]["attr"], th.get("data_apollo_theme") in ok_attrs))
        checks.append(("root carries class canon", bool(th.get("root_class_canon"))))
        checks.append(("theme attrs not on <body>", not th.get("theme_attrs_on_body")))
        if rn:
            want = prof["theme"].get("tokens_light", {})
            got = th.get("rendered_tokens") or {}
            checks.append(("Common tokens resolve (%s)" % ", ".join("%s=%s" % kv for kv in want.items()),
                           all((got.get(k) or "").strip().upper() == v.upper() for k, v in want.items())))
        checks.append(("no hex owned by another theme", not th.get("leaked_hexes")))
        if prof["theme"].get("switch_required") and dr:
            sw = th.get("switch") or {}
            checks.append(("light/dark switch flips the theme, on <html>", bool(sw.get("flips")) and bool(sw.get("on_html"))))
    th["checks"] = [{"check": c, "ok": ok} for c, ok in checks]
    th["verdict"] = "n/a (profile asks no theme)" if not checks else ("PASS" if all(ok for _, ok in checks) else "FAIL")
    S["sections"]["theme"] = th
    if rn:
        S["sections"]["a11y"] = {"rendered": light.get("a11y"), "pack_gate_line": next((ln for ln in ((gt or {}).get("screen") or {}).get("lines", []) if ln.startswith("- a11y")), None)}
        S["sections"]["geometry_native"] = light.get("geometry")
        S["sections"]["render"] = {"hsbc_face": light.get("font"), "h_overflow_px": light.get("h_overflow"),
                                   "pageerrors_light": light.get("pageerrors"), "console_errors_light": light.get("console_errors"),
                                   "clipped_elements": light.get("clipped_elements"), "shots": (rn or {}).get("shots"),
                                   "subpages_probed": len(subs), "subpages_not_reached": (rn or {}).get("subpages_not_reached", [])}
    if gt:
        S["sections"]["pack_gates"] = {"screen": {k: gt["screen"].get(k) for k in ("verdict", "exit", "lines")},
                                       "dataviz": {k: (gt.get("dataviz") or {}).get(k) for k in ("verdict", "charts", "blocking_n", "advisory_n", "blocking")}}
    S["sections"]["geometry_4b"] = ex or {"status": "NOT RUN"}
    dims = S["dimensions"]
    S["total"] = sum(d["score"] for d in dims.values()) if len(dims) == 4 else None
    geo = (ex or {}).get("geometry") or {}
    S["geometry_score"] = geo.get("score") if isinstance(geo.get("score"), int) else None
    S["total_with_geometry"] = (S["total"] + S["geometry_score"]) if (S["total"] is not None and S["geometry_score"] is not None) else None
    S["judgment"] = JUDGMENT
    S["meta"] = m
    S["reproduce"] = ["python3 notes/_lanes/304/R4c/harness/score.py %s --run-id %s" % (p, rid) for p in ("static", "gates", "render", "drive", "ext", "card")]
    return S

# ----------------------------------------------------------------------------- card
CSS = """
:root{--ink:#1a1a1a;--mute:#5c5c5c;--rule:#d7d8d6;--bg:#fff;--soft:#f3f3f3;--ok:#0a7a44;--bad:#b3261e;--warn:#8a5a00}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--ink:#eee;--mute:#aaa;--rule:#444;--bg:#141414;--soft:#1f1f1f;--ok:#5fcf93;--bad:#ff8a80;--warn:#e0b050}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 "Univers Next for HSBC","Helvetica Neue",Arial,sans-serif}
main{max-width:1240px;margin:0 auto;padding:40px 16px 80px}h1{font-size:34px;line-height:1.1;margin:0 0 8px;font-weight:500}
h2{font-size:13px;letter-spacing:.08em;text-transform:uppercase;margin:40px 0 12px;border-top:2px solid var(--ink);padding-top:10px}
.sub{color:var(--mute);margin:0 0 24px}.grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule)}
.cell{background:var(--bg);padding:16px}.big{font-size:48px;line-height:1;font-weight:300}.lab{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute)}
.fact{font-size:13px;color:var(--mute);margin-top:8px}table{border-collapse:collapse;width:100%;font-size:13px}td,th{text-align:left;padding:6px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-weight:500;color:var(--mute)}.ok{color:var(--ok)}.bad{color:var(--bad)}.warn{color:var(--warn)}.shots{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.shots img{width:100%;border:1px solid var(--rule)}code{font-size:12px}ul{padding-left:18px}.tag{display:inline-block;padding:2px 8px;border:1px solid currentColor;font-size:12px}
.scroll{overflow-x:auto}@media (max-width:720px){.grid4{grid-template-columns:1fr 1fr}.shots{grid-template-columns:1fr}}
"""

def esc(x):
    return htmlmod.escape(str(x))

def okcls(b):
    return "ok" if b else "bad"

def card_html(S, rid):
    m = S["meta"]; d = S["dimensions"]; sec = S["sections"]
    out = ["<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
           "<title>Scorecard %s</title><style>%s</style></head><body><main>" % (esc(rid), CSS)]
    out.append("<p class='lab'>Apollo eval harness %s · #304 R4c · profile %s</p>" % (HARNESS_VERSION, esc(m["profile"])))
    out.append("<h1>%s</h1><p class='sub'>%s · page <code>%s</code> · pack <code>%s</code></p>" % (
        esc(m["label"]), esc(m["kind"]), esc(os.path.relpath(m["page_source"], REPO) if m["page_source"].startswith(REPO) else m["page_source"]), esc(os.path.basename(m["pack"]))))
    tot = S.get("total")
    out.append("<p><span class='tag'>mechanical total %s / 12</span> <span class='tag'>geometry (4b) %s / 3</span> %s</p>" % (esc(tot if tot is not None else "incomplete"), esc(S.get("geometry_score") if S.get("geometry_score") is not None else "not scored"),
               ("<span class='warn'>phases missing: %s</span>" % esc(", ".join(S["missing_phases"]))) if S["missing_phases"] else ""))
    out.append("<h2>The four-part rubric, measured</h2><div class='grid4'>")
    for k, lab in (("visually_rich", "Visually rich"), ("full", "Full"), ("persistent", "Persistent"), ("interactive", "Interactive")):
        x = d.get(k)
        out.append("<div class='cell'><div class='lab'>%s</div><div class='big'>%s</div><div class='fact'>%s</div><div class='fact'><em>%s</em></div></div>" % (
            lab, esc(x["score"]) if x else "–", esc(x["fact"]) if x else "not run", esc(x["rule"]) if x else ""))
    out.append("</div>")
    ct = sec.get("composed_vs_traced")
    if ct:
        t = ct["top"] or {}
        out.append("<h2>Composed or traced</h2><p><span class='tag %s'>%s</span> nearest template <b>%s</b>, trace index %s</p>" % (
            "ok" if ct["verdict"] == "COMPOSED" else "bad", esc(ct["verdict"]), esc(t.get("template")), esc(t.get("trace_index"))))
        out.append("<table><tr><th>DOM shingle containment</th><th>template text reused</th><th>template-only classes present</th></tr><tr><td>%s</td><td>%s (%s of %s strings)</td><td>%s %s</td></tr></table><p class='fact'>%s</p>" % (
            esc(t.get("shingle_containment")), esc(t.get("text_reuse")), esc(t.get("text_reused_n")), esc(t.get("text_strings_n")),
            esc(t.get("template_unique_classes_frac")), esc(", ".join(t.get("template_unique_hit", [])[:8])), esc(ct["thresholds"])))
    th = sec.get("theme")
    if th:
        out.append("<h2>Theme — asked: %s</h2><p><span class='tag %s'>%s</span></p><table>" % (esc(th.get("asked")), okcls(th["verdict"] != "FAIL"), esc(th["verdict"])))
        for c in th.get("checks", []):
            out.append("<tr><td>%s</td><td class='%s'>%s</td></tr>" % (esc(c["check"]), okcls(c["ok"]), "yes" if c["ok"] else "NO"))
        out.append("<tr><td>root</td><td><code>class=%s data-apollo-theme=%s data-theme=%s</code></td></tr>" % (
            esc(th.get("root_class_canon")), esc(th.get("data_apollo_theme")), esc(th.get("data_theme"))))
        out.append("<tr><td>raw hex in authored CSS</td><td>%s</td></tr></table>" % esc(th.get("raw_hex_in_authored_css")))
    ch = sec.get("charts_vs_ask")
    if ch:
        out.append("<h2>Charts against the ask</h2><table>")
        for k in ("rendered", "declared_static", "on_overview", "min_overview_asked", "types_rendered", "pack_types_available", "types_used_frac", "with_legend", "with_table", "subpages_with_charts"):
            out.append("<tr><td>%s</td><td>%s</td></tr>" % (esc(k.replace("_", " ")), esc(ch.get(k))))
        out.append("<tr><td>clipped charts</td><td class='%s'>%s</td></tr>" % (okcls(not ch["clipped"]), esc(ch["clipped"] or "none")))
        out.append("<tr><td>tooltips on hover</td><td>%s</td></tr></table>" % esc(ch.get("tooltips")))
    comp = sec.get("components")
    if comp:
        out.append("<h2>Component variety — %s distinct</h2><p>%s</p><p class='fact'>pages scored: %s · APOLLO-DEMO markers copied: %s</p>" % (
            esc(comp["count"]), esc(", ".join(comp["list"])), esc(comp["pages"]), esc(comp["apollo_demo_markers"])))
    g4 = sec.get("geometry_4b") or {}
    out.append("<h2>Geometry and own size (4b's gates)</h2><table>")
    for k in ("geometry", "own_size"):
        x = g4.get(k) or {"status": g4.get("status", "NOT RUN")}
        out.append("<tr><td>%s</td><td>%s</td><td>score %s · findings %s</td><td><code>%s</code></td></tr>" % (esc(k), esc(x.get("status")), esc(x.get("score")), esc(x.get("findings_n")), esc(x.get("gate", ""))))
        for f in (x.get("findings_sample") or [])[:8]:
            out.append("<tr><td></td><td colspan='3' class='fact'>%s %s @%s — %s</td></tr>" % (esc(f.get("clause")), esc(f.get("severity")), esc(f.get("width")), esc(str(f.get("where"))[:120])))
    out.append("</table>")
    gn = sec.get("geometry_native")
    if gn:
        out.append("<p class='fact'>Harness-native geometry signals (advisory, NOT 4b's score): %s</p>" % esc(json.dumps(gn.get("summary", gn))[:900]))
    a = sec.get("a11y")
    if a:
        out.append("<h2>Accessibility findings</h2><p>%s</p><p class='fact'>pack gate: %s</p>" % (esc(json.dumps((a.get("rendered") or {}).get("summary"))), esc(a.get("pack_gate_line"))))
    pg = sec.get("pack_gates")
    if pg:
        out.append("<h2>The pack's own gates</h2><table><tr><td>screen gate</td><td>%s</td></tr><tr><td>dataviz gate</td><td>%s</td></tr></table><ul>%s</ul>" % (
            esc(pg["screen"].get("verdict")), esc(pg["dataviz"]), "".join("<li><code>%s</code></li>" % esc(l) for l in (pg["screen"].get("lines") or [])[:14])))
    r = sec.get("render")
    if r:
        out.append("<h2>Render</h2><p class='fact'>HSBC face: %s · horizontal overflow: %s px · page errors: %s · console errors: %s · clipped elements: %s · sub-pages probed: %s</p>" % (
            esc(r.get("hsbc_face")), esc(r.get("h_overflow_px")), esc(len(r.get("pageerrors_light") or [])), esc(len(r.get("console_errors_light") or [])),
            esc((r.get("clipped_elements") or {}).get("count") if isinstance(r.get("clipped_elements"), dict) else r.get("clipped_elements")), esc(r.get("subpages_probed"))))
        shots = r.get("shots") or {}
        if shots:
            out.append("<div class='shots'>%s</div>" % "".join("<figure style='margin:0'><img alt='%s render' src='%s'><figcaption class='fact'>%s</figcaption></figure>" % (esc(k), esc(v), esc(k)) for k, v in sorted(shots.items())))
    out.append("<h2>Left to judgment — for Dave's eye, not scored</h2><ul>%s</ul>" % "".join("<li>%s</li>" % esc(j) for j in S["judgment"]))
    out.append("<h2>Reproduce</h2><pre style='white-space:pre-wrap;font-size:12px'>%s</pre>" % esc("\n".join(S["reproduce"])))
    out.append("<p class='fact'>page sha256 %s · pack sha256 %s</p></main></body></html>" % (esc(m["page_sha256"]), esc(m.get("pack_sha256"))))
    return "\n".join(out)

def cmd_card(a):
    S = score(a.run_id)
    rd = run_dir(a.run_id)
    jdump(S, os.path.join(rd, "scorecard.json"))
    open(os.path.join(rd, "scorecard.html"), "w").write(card_html(S, a.run_id))
    d = S["dimensions"]
    print("CARD %s  rich=%s full=%s persistent=%s interactive=%s total=%s geo=%s  trace=%s theme=%s clipped=%s" % (
        a.run_id, *(d.get(k, {}).get("score", "-") for k in ("visually_rich", "full", "persistent", "interactive")), S["total"], S["geometry_score"],
        (S["sections"].get("composed_vs_traced") or {}).get("verdict"), S["sections"]["theme"]["verdict"],
        len(S["sections"]["charts_vs_ask"]["clipped"])))
    return S

# ----------------------------------------------------------------------------- compare
def cmd_compare(a):
    ids = [x for x in a.runs.split(",") if x]
    cards = [(i, jload(os.path.join(run_dir(i), "scorecard.json"))) for i in ids]
    cards = [(i, c) for i, c in cards if c]
    outp = os.path.abspath(a.out)
    rows = [("kind", lambda c: c["meta"]["kind"]), ("profile", lambda c: c["meta"]["profile"]),
            ("pack", lambda c: os.path.basename(c["meta"]["pack"])),
            ("visually rich", lambda c: c["dimensions"].get("visually_rich", {}).get("score", "–")),
            ("full", lambda c: c["dimensions"].get("full", {}).get("score", "–")),
            ("persistent", lambda c: c["dimensions"].get("persistent", {}).get("score", "–")),
            ("interactive", lambda c: c["dimensions"].get("interactive", {}).get("score", "–")),
            ("mechanical total /12", lambda c: c.get("total")),
            ("geometry score (4b) /3", lambda c: c.get("geometry_score")),
            ("composed or traced", lambda c: "%s (%s)" % ((c["sections"].get("composed_vs_traced") or {}).get("verdict"), ((c["sections"].get("composed_vs_traced") or {}).get("top") or {}).get("trace_index"))),
            ("theme", lambda c: c["sections"]["theme"]["verdict"]),
            ("components", lambda c: (c["sections"].get("components") or {}).get("count")),
            ("charts rendered", lambda c: c["sections"]["charts_vs_ask"]["rendered"]),
            ("chart types", lambda c: len(c["sections"]["charts_vs_ask"]["types_rendered"])),
            ("clipped charts", lambda c: len(c["sections"]["charts_vs_ask"]["clipped"])),
            ("pack screen gate", lambda c: ((c["sections"].get("pack_gates") or {}).get("screen") or {}).get("verdict")),
            ("dataviz gate blocking", lambda c: ((c["sections"].get("pack_gates") or {}).get("dataviz") or {}).get("blocking_n")),
            ("a11y unnamed controls", lambda c: (((c["sections"].get("a11y") or {}).get("rendered") or {}).get("summary") or {}).get("unnamed_controls")),
            ("a11y small targets", lambda c: (((c["sections"].get("a11y") or {}).get("rendered") or {}).get("summary") or {}).get("small_targets")),
            ("geometry (4b)", lambda c: (c["sections"].get("geometry_4b") or {}).get("geometry", {}).get("status", "NOT RUN")),
            ("own size (4b)", lambda c: (c["sections"].get("geometry_4b") or {}).get("own_size", {}).get("status", "NOT RUN"))]
    h = ["<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Cold runs side by side</title><style>%s</style></head><body><main>" % CSS]
    h.append("<p class='lab'>Apollo eval harness %s · #304 R4c</p><h1>%s</h1><p class='sub'>%d runs. Every number links back to its scorecard; every scorecard says how to reproduce it.</p>" % (HARNESS_VERSION, esc(a.title or "Cold runs, side by side"), len(cards)))
    h.append("<div class='scroll'><table><tr><th></th>%s</tr>" % "".join("<th><a href='%s'>%s</a></th>" % (esc(os.path.relpath(os.path.join(run_dir(i), "scorecard.html"), os.path.dirname(outp))), esc(c["meta"]["label"])) for i, c in cards))
    for lab, f in rows:
        vals = []
        for i, c in cards:
            try: vals.append(f(c))
            except Exception: vals.append("–")
        h.append("<tr><td>%s</td>%s</tr>" % (esc(lab), "".join("<td>%s</td>" % esc(v) for v in vals)))
    h.append("</table></div><h2>Light renders</h2><div class='shots' style='grid-template-columns:repeat(%d,1fr)'>" % max(1, min(4, len(cards))))
    for i, c in cards:
        shot = ((c["sections"].get("render") or {}).get("shots") or {}).get("light-1440")
        if shot:
            h.append("<figure style='margin:0'><img alt='%s' src='%s'><figcaption class='fact'>%s</figcaption></figure>" % (
                esc(c["meta"]["label"]), esc(os.path.relpath(os.path.join(run_dir(i), shot), os.path.dirname(outp))), esc(c["meta"]["label"])))
    h.append("</div><h2>Left to judgment</h2><ul>%s</ul></main></body></html>" % "".join("<li>%s</li>" % esc(j) for j in JUDGMENT))
    open(outp, "w").write("\n".join(h))
    jdump({i: {"total": c.get("total"), "dims": {k: v["score"] for k, v in c["dimensions"].items()}} for i, c in cards}, os.path.splitext(outp)[0] + ".json")
    print("COMPARE %d runs → %s" % (len(cards), outp))

# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("phase", choices=["stage", "static", "gates", "render", "drive", "ext", "card", "all", "compare", "selftest"])
    ap.add_argument("--run-id"); ap.add_argument("--page"); ap.add_argument("--pack")
    ap.add_argument("--copy-out", help="a cold run's output folder, copied beside the pack in the stage")
    ap.add_argument("--profile", default="ceo-common"); ap.add_argument("--label"); ap.add_argument("--kind", default="cold run")
    ap.add_argument("--runs"); ap.add_argument("--out"); ap.add_argument("--title")
    ap.add_argument("--force", action="store_true"); ap.add_argument("--budget", type=float, default=150.0)
    a = ap.parse_args()
    if a.phase == "stage": return cmd_stage(a)
    if a.phase == "static": return cmd_static(a)
    if a.phase == "gates": return cmd_gates(a)
    if a.phase == "ext": return cmd_ext(a)
    if a.phase == "card": return cmd_card(a)
    if a.phase == "compare": return cmd_compare(a)
    if a.phase in ("render", "drive"):
        sys.path.insert(0, HERE); import browser
        return browser.run(a.phase, a.run_id, a.budget)
    if a.phase == "selftest":
        sys.path.insert(0, HERE); import selftest
        return selftest.main()
    if a.phase == "all":
        rd = run_dir(a.run_id)
        t0 = time.time()
        if a.force or not os.path.exists(os.path.join(rd, "meta.json")): cmd_stage(a)
        for ph, fn in (("static", cmd_static), ("gates", cmd_gates)):
            if a.force or not os.path.exists(os.path.join(rd, ph + ".json")): fn(a)
        sys.path.insert(0, HERE); import browser
        for ph in ("render", "drive"):
            left = 170 - (time.time() - t0)
            if not (a.force or not os.path.exists(os.path.join(rd, ph + ".json"))): continue
            if left < 45:
                print("ALL: stopping before %s (%.0fs left in this call) — run it in the next call" % (ph, left)); break
            browser.run(ph, a.run_id, min(a.budget, left - 15))
        if os.path.exists(os.path.join(rd, "drive.json")) and not os.path.exists(os.path.join(rd, "ext.json")) and time.time() - t0 < 120:
            cmd_ext(a)
        return cmd_card(a)

if __name__ == "__main__":
    main()
