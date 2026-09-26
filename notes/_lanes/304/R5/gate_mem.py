#!/usr/bin/env python3
"""R5 / 5b — a gate that runs IN MEMORY on one surface description. Probe, not canon.

  gate_surface(messages, catalogue, snippets) -> verdict dict, NO disk writes, NO reads once warm
    layer S (surface): every A2UI message validates against server_to_client.json with catalog.json
                       resolved to the Apollo catalogue; one root; ids unique; every child reference
                       resolves; no deprecated part (x-apollo.status) — all in memory.
    layer A (a11y):    the page string the surface stands for is put through check_text(), an
                       in-memory port of knowledge/_validate_a11y.check() (same engine: _a11y_target.analyse,
                       same tiers read off the module). The page string is made by a STAND-IN renderer that
                       splices the parts' reference snippets (the real renderer is PoC step 2).
Tests (all written to gate-mem-results.json in this lane folder, the only write, after the timed runs):
  T1 differential: check_text(open(f).read()) == _validate_a11y.check(f) on the 10 dashboard-part snippets,
     then on all 137 snippets (fails, warns, notes and every control/mark verdict identical).
  T2 planted defects: a clean surface must PASS; each planted defect must be REFUSED, and a mutation of the
     clean page by one change must flip the verdict.
  T3 timing: cold (build validator) and warm (median of 25) per surface; audit-hook proof of zero writes and
     zero file reads during the warm calls.
Run (seat): $HOME/.r5venv/bin/python notes/_lanes/304/R5/gate_mem.py
"""
import json, os, re, sys, time, statistics, copy

LANE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(LANE, "..", "..", "..", ".."))
K = os.path.join(ROOT, "knowledge")
sys.path.insert(0, K)
import _validate_a11y as disk                              # the disk gate (check(fp) reads a file)
from _a11y_target import analyse, unknown_roles            # the engine both share
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

# ------------------------------------------------------------------ layer A: the in-memory a11y gate
def check_text(s, name="<memory>"):
    """In-memory port of _validate_a11y.check(fp): identical body, the string replaces open(fp).read().
    Tiers are read off the disk module at call time so a ruled flip there flips here too."""
    fails, warns, notes = [], [], []
    if disk.MOTION.search(s) and 'prefers-reduced-motion' not in s:
        fails.append("animates but has no `prefers-reduced-motion: reduce` block (2.3.3)")
    root, _sheet, controls, marks = analyse(s)
    bad = unknown_roles(root)
    if bad:
        fails.append("CTRL vocabulary: unknown ARIA role(s) %s — this gate cannot classify "
                     "them as interactive or structural, so it cannot tell whether the "
                     "elements carrying them are in scope for 2.5.8. Add each to "
                     "INTERACTIVE_ROLES or NON_INTERACTIVE_ROLES in _a11y_target.py before "
                     "shipping (dv-vocab shape: fail loud, never let an unknown default to "
                     "skip)." % bad)
    for r in controls:
        who = "`%s`" % r.el.descr()
        if r.verdict == "fail":
            fails.append("%s — %s" % (who, r.detail))
        elif r.verdict == "warn":
            (fails if disk.CONTROL_TIER_44 == "fail" else warns).append("%s — %s" % (who, r.detail))
        elif r.verdict == "unmeasured":
            notes.append("%s — UNMEASURED: %s" % (who, r.detail))
        elif r.verdict == "exception":
            notes.append("%s — %s" % (who, r.detail))
    for r in marks:
        who = "`%s`" % r.el.descr()
        if r.verdict == "under":
            (fails if disk.MARK_TIER == "fail" else warns).append(
                "DATA MARK %s — %s (s116-D1: marks carry the 24 floor, not the 44 target)" % (who, r.detail))
        elif r.verdict == "unmeasured":
            notes.append("DATA MARK %s — UNMEASURED: %s" % (who, r.detail))
    return name, fails, warns, notes, controls, marks

def sig(row):
    n, f, w, no, c, m = row
    return (f, w, no, [(r.el.descr(), r.verdict, r.detail) for r in c], [(r.el.descr(), r.verdict, r.detail) for r in m])

# ------------------------------------------------------------------ layer S: the surface
SPEC = os.path.join(LANE, "a2ui-v0.9.1")
ld = lambda p: json.load(open(p))
CATALOG_URI = "https://a2ui.org/specification/v0_9/catalog.json"

def build_validator(cat):
    ct = ld(os.path.join(SPEC, "json_common_types.json")); s2c = ld(os.path.join(SPEC, "json_server_to_client.json"))
    res = lambda d: Resource.from_contents(d, default_specification=DRAFT202012)
    reg = Registry().with_resources([(ct["$id"], res(ct)), (s2c["$id"], res(s2c)), (CATALOG_URI, res(cat))])
    return Draft202012Validator({"$ref": s2c["$id"]}, registry=reg)

_PV = {}
def PART_V(V, name):
    if name not in _PV:
        _PV[name] = Draft202012Validator({"$ref": CATALOG_URI + "#/components/" + name}, registry=V._registry if hasattr(V, "_registry") else V.registry)
    return _PV[name]

STYLE = re.compile(r"<style\b[^>]*>.*?</style>", re.S | re.I)
BODY = re.compile(r"<body\b[^>]*>(.*)</body>", re.S | re.I)

def stand_in_render(components, cat, snippets):
    """NOT a renderer: splices each part's reference snippet (styles + body) in surface order."""
    styles, bodies, missing = [], [], []
    for c in components:
        x = cat["x-apollo"].get(c.get("component"), {})
        sn = (x.get("snippet") or "").split(":", 1)[-1]
        s = snippets.get(sn)
        if s is None:
            missing.append(c.get("component")); continue
        styles += STYLE.findall(s)
        b = BODY.search(s)
        bodies.append('<section data-part="%s">%s</section>' % (c.get("id"), b.group(1) if b else ""))
    return "<!doctype html><html><head>%s</head><body>%s</body></html>" % ("".join(styles), "".join(bodies)), missing

def gate_surface(messages, cat, V, snippets, page=None):
    """messages: list of A2UI v0.9.1 dicts. page: an explicit page string (else the stand-in splice)."""
    t = time.perf_counter()
    refusals = []
    comps = []
    for i, msg in enumerate(messages):
        for e in V.iter_errors(msg):
            refusals.append("S1 schema msg[%d] %s: %s" % (i, "/".join(map(str, e.absolute_path)) or "(root)", e.message[:140]))
        comps += (msg.get("updateComponents") or {}).get("components") or []
    # S1b: the discriminator emulated — each part against its own entry, for a READABLE reason
    # (A2UI's anyComponent is a oneOf; a oneOf failure names the whole instance, not the fault)
    for c in comps:
        name = c.get("component")
        if name not in cat["components"]:
            refusals.append("S1b %s: part %r is not in catalogue %s" % (c.get("id"), name, cat["catalogId"]))
            continue
        for e in PART_V(V, name).iter_errors(c):
            refusals.append("S1b %s (%s) %s: %s" % (c.get("id"), name, "/".join(map(str, e.absolute_path)) or "(root)", e.message[:140]))
    ids = [c.get("id") for c in comps]
    if "root" not in ids:
        refusals.append("S2 no component with id 'root'")
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        refusals.append("S3 duplicate ids %s" % dup)
    known = set(ids)
    for c in comps:
        for k, v in c.items():
            if k in ("id", "component"):
                continue
            prop = ((cat["components"].get(c.get("component")) or {}).get("allOf") or [{}])[-1].get("properties", {}).get(k, {})
            ref = prop.get("$ref", "")
            refs = [v] if ref.endswith("ComponentId") and isinstance(v, str) else (v if ref.endswith("ChildList") and isinstance(v, list) else [])
            for r in refs:
                if r not in known:
                    refusals.append("S4 %s.%s -> %r does not resolve" % (c.get("id"), k, r))
        st = (cat["x-apollo"].get(c.get("component")) or {}).get("status")
        if st == "deprecated":
            refusals.append("S5 %s uses deprecated part %s" % (c.get("id"), c.get("component")))
    if page is None:
        page, missing = stand_in_render(comps, cat, snippets)
        if missing:
            refusals.append("S6 no reference snippet for %s" % missing)
    _n, af, aw, an, _c, _m = check_text(page, "surface")
    for f in af:
        refusals.append("A a11y FAIL: " + f[:200])
    return {"verdict": "REFUSE" if refusals else "PASS", "refusals": refusals, "a11y_warns": len(aw),
            "a11y_notes": len(an), "page_bytes": len(page), "ms": round((time.perf_counter() - t) * 1000, 2)}

# ------------------------------------------------------------------ audit hook: prove no writes / reads
EVENTS = []
ARMED = [False]
WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC
MUTATING = {"os.remove", "os.rename", "os.mkdir", "os.rmdir", "os.truncate", "os.chmod", "os.symlink",
            "os.link", "os.utime", "shutil.copyfile", "shutil.rmtree", "shutil.move", "os.replace"}
def hook(ev, args):
    if not ARMED[0]:
        return
    if ev == "open":
        path, mode, flags = (list(args) + [None, None, None])[:3]
        w = (isinstance(mode, str) and any(ch in mode for ch in "wax+")) or (isinstance(flags, int) and flags & WRITE_FLAGS)
        EVENTS.append(("write" if w else "read", str(path)))
    elif ev in MUTATING:
        EVENTS.append(("mutate:" + ev, str(args[:1])))
sys.addaudithook(hook)

# ------------------------------------------------------------------ fixtures
def U(components):
    return [{"version": "v0.9.1", "createSurface": {"surfaceId": "probe", "catalogId": CAT["catalogId"]}},
            {"version": "v0.9.1", "updateComponents": {"surfaceId": "probe", "components": components}}]

if __name__ == "__main__":
    out = {"$run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    CAT = ld(os.path.join(LANE, "catalogue-dashboard.json"))
    SNIPDIR = os.path.join(K, "snippets")
    # ---- T1 differential ----
    dash_snips = sorted({(x.get("snippet") or "").split(":", 1)[-1] for x in CAT["x-apollo"].values() if x.get("snippet")})
    ten = [s for s in dash_snips if os.path.exists(os.path.join(SNIPDIR, s))][:10]
    allf = sorted(f for f in os.listdir(SNIPDIR) if f.endswith(".reference.html"))
    def diff(files):
        same, differ, td, tm = 0, [], 0.0, 0.0
        for f in files:
            p = os.path.join(SNIPDIR, f)
            a = time.perf_counter(); d = disk.check(p); td += time.perf_counter() - a
            s = open(p).read()
            a = time.perf_counter(); m = check_text(s, f); tm += time.perf_counter() - a
            if sig(d) == sig(m):
                same += 1
            else:
                differ.append(f)
            
        return {"files": len(files), "identical": same, "differ": differ, "disk_s": round(td, 3), "memory_s": round(tm, 3)}
    out["T1_ten"] = dict(diff(ten), list=ten, verdicts={f: ("FAIL" if disk.check(os.path.join(SNIPDIR, f))[1] else "PASS") for f in ten})
    out["T1_all"] = diff(allf)
    print("T1 ten:", out["T1_ten"]["identical"], "/", out["T1_ten"]["files"], "| all:", out["T1_all"]["identical"], "/", out["T1_all"]["files"], out["T1_all"]["differ"])

    # ---- the surface + planted defects ----
    t = time.perf_counter(); V = build_validator(CAT); cold_build = time.perf_counter() - t
    need = {(x.get("snippet") or "").split(":", 1)[-1] for x in CAT["x-apollo"].values()}
    SN = {s: open(os.path.join(SNIPDIR, s)).read() for s in need if s and os.path.exists(os.path.join(SNIPDIR, s))}
    clean = [
        {"id": "root", "component": "AppShellTopNav", "brand": "brand", "primaryNav": "nav", "trail": "crumbs", "content": "kpi", "utilityActions": "act"},
        {"id": "brand", "component": "Headers", "variant": CAT["components"]["Headers"]["allOf"][-1]["properties"]["variant"]["enum"][0]},
        {"id": "nav", "component": "Navigations"},
        {"id": "crumbs", "component": "Breadcrumbs"},
        {"id": "kpi", "component": "KpiTile", "state": "ready"},
        {"id": "act", "component": "Button"},
    ]
    TINY = "<style>.probe-tiny{width:16px;height:16px;}</style>"
    MIN = "<!doctype html><html><head>%s</head><body>%s</body></html>"
    cases = []
    def case(name, msgs, expect, page=None, why=""):
        r = gate_surface(msgs, CAT, V, SN, page=page)
        cases.append({"case": name, "expect": expect, "got": r["verdict"], "ok": r["verdict"] == expect,
                      "refusals": [x for x in r["refusals"] if not x.startswith("S1 ")][:4] + [x[:160] for x in r["refusals"] if x.startswith("S1 ")][:1], "ms": r["ms"], "why": why})
    case("P0 clean dashboard surface (6 parts, stand-in splice)", U(clean), "PASS")
    case("P1 clean minimal page string: one 44px button", U(clean), "PASS",
         page=MIN % ("<style>.b{width:44px;height:44px;}</style>", '<button class="b">Approve</button>'))
    case("P2 planted: 16px button (2.5.8 floor)", U(clean), "REFUSE",
         page=MIN % (TINY, '<button class="probe-tiny">x</button>'), why="mutation of P1: one size change")
    base_page, _ = stand_in_render(clean, CAT, SN)
    case("P3 planted into the real spliced page: + a 16px button", U(clean), "REFUSE",
         page=base_page.replace("</head>", TINY + "</head>").replace("</body>", '<button class="probe-tiny">x</button></body>'),
         why="mutation of P0's page by one added control")
    case("P4 planted: animation with no reduced-motion block", U(clean), "REFUSE",
         page=MIN % ("<style>.s{animation:spin 1s infinite}@keyframes spin{to{transform:rotate(1turn)}}</style>", '<div class="s"></div>'))
    case("P5 planted: unknown ARIA role", U(clean), "REFUSE",
         page=MIN % ("", '<div role="probe-made-up-role" tabindex="0">x</div>'))
    case("P6 surface: part not in the catalogue", U(clean + [{"id": "x", "component": "Carousel"}]), "REFUSE")
    case("P7 surface: required slot missing (AppShellTopNav without content)",
         U([dict(clean[0], content=None) if False else {k: v for k, v in clean[0].items() if k != "content"}] + clean[1:]), "REFUSE")
    case("P8 surface: child reference does not resolve", U([dict(clean[0], content="ghost")] + clean[1:]), "REFUSE",
         why="schema cannot see this: ids are plain strings; the structural layer must")
    case("P9 surface: no root", U([dict(c, id=("top" if c["id"] == "root" else c["id"])) for c in clean]), "REFUSE")
    case("P10 surface: duplicate ids", U(clean + [{"id": "kpi", "component": "StatCard"}]), "REFUSE")
    case("P11 surface: deprecated part (ViewOptions)", U(clean + [{"id": "vo", "component": "ViewOptions"}]), "REFUSE")
    case("P12 surface: unknown property on a part", U([dict(clean[0], probeUnknown=1)] + clean[1:]), "REFUSE")
    case("P13 surface: enum value outside the meta's values", U(clean[:4] + [dict(clean[4], state="probe-not-a-state")] + clean[5:]), "REFUSE")
    # known misses — the disk gate's own semantics, which the port preserves on purpose
    case("K1 KNOWN MISS: animation planted into a page whose other part already has a reduced-motion block", U(clean), "REFUSE",
         page=base_page.replace("</head>", "<style>.probe-anim{animation:spin 1s infinite}@keyframes spin{to{opacity:0}}</style></head>"),
         why="the 2.3.3 clause is a whole-string substring test: one block anywhere in the page satisfies it")
    case("K2 KNOWN MISS: animation + the phrase only inside a comment", U(clean), "REFUSE",
         page=MIN % ("<style>/* prefers-reduced-motion is handled elsewhere */.s{animation:spin 1s}@keyframes spin{to{opacity:0}}</style>", '<div class="s"></div>'),
         why="same clause: a comment mentioning the phrase satisfies it")
    case("K3 KNOWN MISS: a control that is too small but sized only by padding", U(clean), "REFUSE",
         page=MIN % ("<style>.p{padding:2px}</style>", '<button class="p">x</button>'),
         why="layout-determined boxes are UNMEASURED by design (static gate); the render leg would see it")
    out["T2_cases"] = cases
    # ---- T1b differential on FAILING inputs: every snippet passes the disk gate, so T1 alone cannot see a
    # dropped fail clause. The planted pages go through BOTH gates (the test harness, not the gate, writes
    # them to /dev/shm for the disk gate to read; nothing is written in the repo).
    planted = {"P1": MIN % ("<style>.b{width:44px;height:44px;}</style>", '<button class="b">Approve</button>'),
               "P2": MIN % (TINY, '<button class="probe-tiny">x</button>'),
               "P3": base_page.replace("</head>", TINY + "</head>").replace("</body>", '<button class="probe-tiny">x</button></body>'),
               "P4": MIN % ("<style>.s{animation:spin 1s infinite}@keyframes spin{to{transform:rotate(1turn)}}</style>", '<div class="s"></div>'),
               "P5": MIN % ("", '<div role="probe-made-up-role" tabindex="0">x</div>'),
               "K3": MIN % ("<style>.p{padding:2px}</style>", '<button class="p">x</button>')}
    t1b = {}
    for k, pg in planted.items():
        fp = "/dev/shm/r5-planted-%s.html" % k
        open(fp, "w").write(pg)
        d = disk.check(fp); m = check_text(pg, os.path.basename(fp).replace(".reference.html", ""))
        t1b[k] = {"identical": sig(d) == sig(m), "disk_fails": len(d[1]), "memory_fails": len(m[1])}
        os.remove(fp)
    out["T1b_planted_differential"] = t1b
    print("T1b planted differential:", t1b)
    for c in cases:
        print(("ok  " if c["ok"] else "MISS"), c["case"], "->", c["got"], c["refusals"][:1])

    # ---- T3 timing + audit ----
    del EVENTS[:]
    ARMED[0] = True
    warm = [gate_surface(U(clean), CAT, V, SN)["ms"] for _ in range(25)]
    ARMED[0] = False
    ev_warm = list(EVENTS)
    del EVENTS[:]
    ARMED[0] = True
    t = time.perf_counter(); V2 = build_validator(CAT); cold = gate_surface(U(clean), CAT, V2, SN); cold_total = (time.perf_counter() - t) * 1000
    ARMED[0] = False
    ev_cold = list(EVENTS)
    a11y_only = []
    for _ in range(25):
        a = time.perf_counter(); check_text(base_page); a11y_only.append((time.perf_counter() - a) * 1000)
    out["T3"] = {"warm_ms_median": round(statistics.median(warm), 2), "warm_ms_max": round(max(warm), 2), "n": 25,
                 "cold_ms_incl_validator_build": round(cold_total, 2), "validator_build_ms_first": round(cold_build * 1000, 2),
                 "a11y_only_ms_median": round(statistics.median(a11y_only), 2), "page_bytes": len(base_page),
                 "warm_events": {"writes": [e for e in ev_warm if e[0] != "read"], "reads": len([e for e in ev_warm if e[0] == "read"])},
                 "cold_events": {"writes": [e for e in ev_cold if e[0] != "read"], "reads": sorted({e[1] for e in ev_cold if e[0] == "read"})[:20]}}
    print("T3", json.dumps({k: v for k, v in out["T3"].items() if k not in ("cold_events",)}), "cold reads:", len(out["T3"]["cold_events"]["reads"]), "cold writes:", out["T3"]["cold_events"]["writes"])
    json.dump(out, open(os.path.join(LANE, "gate-mem-results.json"), "w"), indent=1, ensure_ascii=False)
