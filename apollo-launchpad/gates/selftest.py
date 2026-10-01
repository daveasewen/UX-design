#!/usr/bin/env python3
"""Launchpad step three — the gates' selftest, T3.1–T3.6 of the build spec
(notes/_lanes/312/C/SPEC-launchpad-day-one.md § 11). #313 lane C3.

  T3.1 differential: the in-memory gate gives the disk gate's verdict on every reference snippet —
       the a11y twin against _validate_a11y.check() (fails, warns, notes, every control and mark
       verdict), and the whole page layer against _validate_screen.py's own per-file steps run on the
       file; then the six planted pages of #304 R5 through both a11y gates
  T3.2 planted defects: R5's fourteen cases (two clean, twelve refused), each refusal BY NAME (the
       check id that must fail), plus the three new ones — S6 (a slot child that does not provide what
       the slot accepts, by provides and by tier), S9 (series outside the shape's arity, literal and
       through a binding), and motion judged per part (s305-D54) — and the deprecated-part check S7
       on a catalogue with one entry flipped (no deprecated part is published, so S7 needs a mutation)
  T3.3 the two worked-example surfaces (treasurer, operations analyst) pass the surface layer; the
       treasurer's stand-in page passes the page layer
  T3.4 timing: cold, then warm n=25 (median, max) for gate_surface, gate_surface+splice and gate_page;
       an audit hook counts file opens and mutations during the warm calls
  T3.5 one stdio round trip per tool through server.py, timed, and its verdict equal to the in-process one
  T3.6 the render leg: UNMEASURED in the cloud (no seat), with its price
Known misses (reported, not scored): the disk gate's own semantics the twin keeps on purpose.

Writes nothing under the repo (the page layer's one /dev/shm write per call is the gate's, declared).
Exit 1 when any scored test fails.
Run:  PYTHONDONTWRITEBYTECODE=1 python3 apollo-launchpad/gates/selftest.py [--json]
"""
import copy, json, os, statistics, subprocess, sys, time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gate_mem as G                                   # noqa: E402

FIX = os.path.join(HERE, "fixtures")
RESULTS, FAILED = {}, []


def say(ok, tid, line):
    print(("ok   " if ok else "FAIL ") + tid + "  " + line)
    if not ok:
        FAILED.append(tid)


def failed_ids(v):
    return [c["id"] for c in v["checks"] if c["result"] == "fail"]


# ------------------------------------------------------------------ audit hook (armed only around warm calls)
EVENTS, ARMED = [], [False]
WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC
MUTATING = {"os.remove", "os.rename", "os.mkdir", "os.rmdir", "os.truncate", "os.chmod", "os.symlink",
            "os.link", "os.utime", "shutil.copyfile", "shutil.rmtree", "shutil.move", "os.replace"}


def _hook(ev, args):
    if not ARMED[0]:
        return
    if ev == "open":
        path, mode, flags = (list(args) + [None, None, None])[:3]
        w = (isinstance(mode, str) and any(ch in mode for ch in "wax+")) or \
            (isinstance(flags, int) and bool(flags & WRITE_FLAGS))
        EVENTS.append(("write" if w else "read", str(path)))
    elif ev in MUTATING:
        EVENTS.append(("mutate:" + ev, str(args[:1])))


sys.addaudithook(_hook)


def audited(fn, n):
    del EVENTS[:]
    ARMED[0] = True
    ms = []
    try:
        for _ in range(n):
            t = time.perf_counter(); fn(); ms.append((time.perf_counter() - t) * 1000)
    finally:
        ARMED[0] = False
    ev = list(EVENTS)
    reads = sorted({shorten(p) for k, p in ev if k == "read"})
    writes = [(k, p) for k, p in ev if k != "read"]
    return ms, reads, writes


def shorten(p):
    return "/dev/shm/<page>" if "launchpad-gate-" in p else os.path.relpath(p, G.ROOT) if p.startswith(G.ROOT) else p


# ------------------------------------------------------------------ fixtures
def load(name):
    return json.load(open(os.path.join(FIX, name), encoding="utf-8"))


def comps(msgs):
    return msgs[1]["updateComponents"]["components"]


def with_comps(msgs, cs, extra=None):
    m = copy.deepcopy(msgs[:2])
    m[1]["updateComponents"]["components"] = cs
    return m + (extra or [])


def by_id(cs, i):
    return next(c for c in cs if c["id"] == i)


CANON_LINK = '<link rel="stylesheet" href="knowledge/canon/canon.css">'
MIN = "<!doctype html><html lang=\"en\"><head>" + CANON_LINK + "%s</head><body>%s</body></html>"
TINY = "<style>.probe-tiny{width:16px;height:16px;}</style>"


def main():
    t_cold = time.perf_counter()
    g = G.Gate()
    cold_build_ms = round((time.perf_counter() - t_cold) * 1000, 2)
    T = load("treasurer-surface.json")
    A = load("analyst-surface.json")
    t = time.perf_counter(); g.gate_surface(T); cold_first_surface = round((time.perf_counter() - t) * 1000, 2)
    t = time.perf_counter(); g.gate_page(g.splice(T)[0]); cold_first_page = round((time.perf_counter() - t) * 1000, 2)

    # ================================================================ T3.1
    snips = sorted(f for f in os.listdir(G.SNIPDIR) if f.endswith(".reference.html"))
    same_a11y, diff_a11y, same_page, diff_page, disk_red = 0, [], 0, [], 0
    for f in snips:
        p = os.path.join(G.SNIPDIR, f)
        s = open(p, encoding="utf-8").read()
        d = G.A11Y.check(p)
        m = G.a11y_text(s, f)
        if G.a11y_signature(d) == G.a11y_signature(m):
            same_a11y += 1
        else:
            diff_a11y.append(f)
        # the disk screen gate's own steps, on the FILE (as _validate_screen.main runs them, minus its writes)
        rl, rf = G.SCREEN.gate_receipt(p, False)
        cf = G.SCREEN.gate_compose(p)
        _cpl, cpf = G.SCREEN.gate_composition(s)
        icf = G.SCREEN.gate_icons(s)
        disk_fail = bool(rf or cf or cpf or icf or d[1])
        disk_red += disk_fail
        v = g.gate_page(s)
        mem = {c["id"]: c["result"] == "fail" for c in v["checks"]}
        disk = {"P0": bool(rf), "P1": bool(d[1]), "P2": bool(cpf), "P3": bool(icf), "P4": bool(cf)}
        if (v["verdict"] == "fail") == disk_fail and mem == disk:
            same_page += 1
        else:
            diff_page.append((f, disk, mem))
    RESULTS["T3.1"] = {"snippets": len(snips), "a11y_identical": same_a11y, "a11y_differ": diff_a11y,
                       "page_layer_identical": same_page, "page_layer_differ": diff_page[:5],
                       "disk_red_snippets": disk_red}
    say(same_a11y == len(snips), "T3.1a", "a11y twin = disk a11y gate on %d/%d reference snippets (fails, warns, notes, every verdict)"
        % (same_a11y, len(snips)))
    say(same_page == len(snips), "T3.1b", "page layer = disk screen gate's steps per check on %d/%d snippets (%d red on disk)"
        % (same_page, len(snips), disk_red))
    base_page = g.splice(T)[0]
    planted = {
        "R5-P1 clean 44px button": MIN % ("<style>.b{width:44px;height:44px;}</style>", '<button class="b">Approve</button>'),
        "R5-P2 16px button": MIN % (TINY, '<button class="probe-tiny">x</button>'),
        "R5-P3 spliced page + a 16px button": base_page.replace("</head>", TINY + "</head>").replace(
            "</body>", '<button class="probe-tiny">x</button></body>'),
        "R5-P4 animation, no reduced-motion block": MIN % (
            "<style>.s{animation:spin 1s infinite}@keyframes spin{to{transform:rotate(1turn)}}</style>", '<div class="s"></div>'),
        "R5-P5 unknown ARIA role": MIN % ("", '<div role="probe-made-up-role" tabindex="0">x</div>'),
        "R5-K3 too small, sized by padding only": MIN % ("<style>.p{padding:2px}</style>", '<button class="p">x</button>'),
    }
    t1b, fails_seen = {}, 0
    shm = "/dev/shm" if os.path.isdir("/dev/shm") else "/tmp"
    for k, pg in planted.items():
        fp = os.path.join(shm, "c3-selftest-planted.html")
        open(fp, "w", encoding="utf-8").write(pg)
        d = G.A11Y.check(fp)
        os.remove(fp)
        m = G.a11y_text(pg, os.path.basename(fp).replace(".reference.html", ""))
        t1b[k] = {"identical": G.a11y_signature(d) == G.a11y_signature(m), "disk_fails": len(d[1]), "memory_fails": len(m[1])}
        fails_seen += bool(d[1])
    RESULTS["T3.1c"] = t1b
    ok = all(x["identical"] for x in t1b.values())
    say(ok, "T3.1c", "six planted pages: %d/6 identical, %d of them FAIL on disk" % (
        sum(x["identical"] for x in t1b.values()), fails_seen))

    # ================================================================ T3.2
    clean = comps(T)
    cases = []

    def case(tid, label, expect_ids, run):
        v = run()
        got = failed_ids(v)
        if expect_ids:
            ok = v["verdict"] == "fail" and all(e in got for e in expect_ids)
        else:
            ok = v["verdict"] == "pass"
        reasons = [r for c in v["checks"] if c["id"] in (expect_ids or []) for r in c["reasons"]][:2]
        cases.append({"id": tid, "case": label, "expect": expect_ids or "pass", "failed": got, "ok": ok, "reasons": reasons})
        say(ok, "T3.2 " + tid, "%s -> %s %s" % (label, v["verdict"], ("refused by " + ",".join(got)) if got else ""))

    case("P0", "clean treasurer surface + stand-in page", [], lambda: g.gate_surface(T, splice=True))
    case("P1", "clean minimal page: one 44px button", [], lambda: g.gate_page(planted["R5-P1 clean 44px button"]))
    case("P2", "16px button (2.5.8 floor)", ["P1"], lambda: g.gate_page(planted["R5-P2 16px button"]))
    case("P3", "the real spliced page + one 16px button", ["P1"], lambda: g.gate_page(planted["R5-P3 spliced page + a 16px button"]))
    case("P4", "animation with no reduced-motion block", ["P1"], lambda: g.gate_page(planted["R5-P4 animation, no reduced-motion block"]))
    case("P5", "unknown ARIA role", ["P1"], lambda: g.gate_page(planted["R5-P5 unknown ARIA role"]))
    case("P6", "part not in the catalogue (Carousel)", ["S2"],
         lambda: g.gate_surface(with_comps(T, clean + [{"id": "x", "component": "Carousel"}])))
    case("P7", "required slot missing (frame without content)", ["S2"],
         lambda: g.gate_surface(with_comps(T, [{k: v for k, v in clean[0].items() if k != "content"}] + clean[1:])))
    case("P8", "child reference does not resolve", ["S5"],
         lambda: g.gate_surface(with_comps(T, [dict(clean[0], content="ghost")] + clean[1:])))
    case("P9", "no root", ["S3"],
         lambda: g.gate_surface(with_comps(T, [dict(c, id="top") if c["id"] == "root" else c for c in clean])))
    case("P10", "duplicate ids", ["S4"],
         lambda: g.gate_surface(with_comps(T, clean + [{"id": "cash", "component": "Metric"}])))
    case("P11", "deprecated part (ViewOptions: never published, so refused as unknown)", ["S2"],
         lambda: g.gate_surface(with_comps(T, clean + [{"id": "vo", "component": "ViewOptions"}])))
    case("P12", "unknown property on a part", ["S2"],
         lambda: g.gate_surface(with_comps(T, [dict(clean[0], probeUnknown=1)] + clean[1:])))
    case("P13", "state outside the part's states (Metric)", ["S2", "S8"],
         lambda: g.gate_surface(with_comps(T, [dict(c, state="probe-not-a-state") if c["id"] == "cash" else c for c in clean])))
    # ---- the new ones
    case("N1a", "S6: a wayfinding part (Navigations) as a tile of the wall", ["S6"],
         lambda: g.gate_surface(with_comps(T, [dict(c, tiles=["cash", "cutoff", "approvals", "nav"]) if c["id"] == "wall" else c
                                               for c in clean])))
    case("N1b", "S6: a pattern-tier part in a slot that accepts atoms and molecules (DataGrid.filters)", ["S6"],
         lambda: g.gate_surface(with_comps(T, clean[:3] + [
             {"id": "wall", "component": "TemplateDashboardBento", "tiles": ["grid"]},
             {"id": "grid", "component": "DataGrid", "columns": [{"key": "a"}], "filters": ["fbar"]},
             {"id": "fbar", "component": "ChartBar", "data": {"series": [{"name": "x", "values": [1]}]}}])))
    # s313-D41 (Dave, by click, 'Keep the four'): the wall accepts exactly these four kinds of tile; the gate
    # reads them from the catalogue, so pin the catalogue's list and refuse a fifth kind (a page title)
    four = ["headline-metric", "status-surface", "chart", "record-list"]
    acc = (g.props("TemplateDashboardBento").get("tiles", {}).get("x-apollo") or {}).get("accepts", {}).get("provides")
    say(acc == four, "T3.2 D41", "the wall's tiles slot accepts exactly the four kinds s313-D41 keeps: %s" % acc)
    case("D41", "a fifth kind (Headers, a page title) as a tile of the wall", ["S6"],
         lambda: g.gate_surface(with_comps(T, [dict(c, tiles=["cash", "cutoff", "approvals", "balance", "title2"])
                                               if c["id"] == "wall" else c for c in clean] +
                                           [{"id": "title2", "component": "Headers", "title": "A fifth tile", "subtitle": "x"}])))
    six = {"series": [{"name": "s%d" % i, "values": [1, 2]} for i in range(6)]}
    case("N2a", "S9: a line chart carrying six series (shape admits 1–5)", ["S9"],
         lambda: g.gate_surface(with_comps(T, [dict(c, data=six) if c["id"] == "balance" else c for c in clean])))
    case("N2b", "S9: a line chart whose series count is 6", ["S9"],
         lambda: g.gate_surface(with_comps(T, [dict(c, series=6) if c["id"] == "balance" else c for c in clean])))
    case("N2c", "S9 through a binding: data bound to a six-series value in the surface's data model", ["S9"],
         lambda: g.gate_surface(with_comps(T, [dict(c, data={"path": "/balance"}) if c["id"] == "balance" else c for c in clean],
                                           [{"version": "v0.9.1", "updateDataModel": {"surfaceId": "treasurer", "path": "/balance", "value": six}}])))
    animA = "<style>.pa{animation:spin 1s infinite}@keyframes spin{to{opacity:0}}@media (prefers-reduced-motion: reduce){.pa{animation:none}}</style><div class=\"pa\"></div>"
    animB = "<style>.pb{transition:opacity .2s}</style><div class=\"pb\"></div>"
    import _validate_receipt as VR
    two = MIN % ("", VR.splice_marker_start("Part-a#1", "knowledge/snippets/Part-a.reference.html", "markup") + animA +
                 VR.splice_marker_end("Part-a#1") + VR.splice_marker_start("Part-b#2", "knowledge/snippets/Part-b.reference.html", "markup") +
                 animB + VR.splice_marker_end("Part-b#2"))
    case("N3", "motion per part: two spliced parts, only one has a reduced-motion block, the other animates", ["P1"],
         lambda: g.gate_page(two))
    whole_string_green = G.A11Y.MOTION.search(two) is not None and G.A11Y.REDUCED in two
    say(whole_string_green and any("Part-b" in r for c in cases if c["id"] == "N3" for r in c["reasons"]),
        "T3.2 N3m", "mutation: the whole-string reading (pre-s305-D54) is green on N3's page (%s); the gate names part `Part-b`"
        % whole_string_green)
    # S7 needs a published deprecated part; none is published (the catalogue drops them), so flip one in memory
    cat2 = copy.deepcopy(g.cat)
    cat2["components"]["Metric"]["x-apollo"]["status"] = "deprecated"
    g2 = G.Gate(cat2)
    case("N4", "S7: a part whose entry says deprecated (catalogue mutated in memory)", ["S7"], lambda: g2.gate_surface(T))
    # ---- #313 lane C1F: a data setting takes a binding. C3's F2 found the catalogue typed it
    # oneOf[object, array, DataBinding], so a binding matched twice and was refused; the generator's object
    # branch now excludes `path`. A bound value passes; a malformed binding and a bare word stay refused.
    good = {"series": [{"name": "b", "values": [1, 2]}]}

    def bal(v):
        return with_comps(T, [dict(c, data=v) if c["id"] == "balance" else c for c in clean],
                          [{"version": "v0.9.1", "updateDataModel": {"surfaceId": "treasurer", "path": "/balance", "value": good}}])
    case("B1", "a data setting bound to the data model (A2UI DataBinding), well-formed", [],
         lambda: g.gate_surface(bal({"path": "/balance"})))
    case("B2", "a binding whose path is not a string", ["S1", "S2"], lambda: g.gate_surface(bal({"path": 5})))
    case("B3", "a binding carrying a stray key beside its path", ["S1", "S2"],
         lambda: g.gate_surface(bal({"path": "/balance", "probe": 1})))
    case("B4", "a data setting given a bare word", ["S1", "S2"], lambda: g.gate_surface(bal("x")))
    n2c = next(c for c in cases if c["id"] == "N2c")
    say(n2c["failed"] == ["S9"], "T3.2 N2c1", "the six-series binding is refused by S9 alone now the binding itself is legal "
        "(refused by %s)" % ",".join(n2c["failed"]))
    # bite: put back the pre-fix object branch (no `not path`) in memory and the well-formed binding is refused again
    cat3 = copy.deepcopy(g.cat)
    for br in cat3["components"]["ChartLine"]["allOf"][-1]["properties"]["data"]["oneOf"]:
        br.pop("not", None)
    v3 = G.Gate(cat3).gate_surface(bal({"path": "/balance"}))
    say(v3["verdict"] == "fail" and "S2" in failed_ids(v3), "T3.2 B1m",
        "mutation: the pre-fix oneOf (object branch admits a path) refuses B1's binding (%s, %s)" % (v3["verdict"], ",".join(failed_ids(v3))))
    RESULTS["T3.2"] = cases

    # known misses and found defects: reported, never scored
    known = []

    def note(tid, label, run, what):
        v = run()
        known.append({"id": tid, "case": label, "verdict": v["verdict"], "failed": failed_ids(v), "what": what})
        print("note " + tid + "  " + label + " -> " + v["verdict"] + (" (" + ",".join(failed_ids(v)) + ")" if failed_ids(v) else ""))
    note("K2", "animation + the phrase only inside a CSS comment",
         lambda: g.gate_page(MIN % ("<style>/* prefers-reduced-motion is handled elsewhere */.s{animation:spin 1s}"
                                    "@keyframes spin{to{opacity:0}}</style>", '<div class="s"></div>')),
         "the disk clause is a substring test; a comment that mentions the phrase satisfies it (R5 K2, kept)")
    note("K3", "a control too small but sized by padding only", lambda: g.gate_page(planted["R5-K3 too small, sized by padding only"]),
         "layout-determined boxes are UNMEASURED by the static gate; the render leg would see it (R5 K3, kept)")
    chart = g.snippets["ChartLine"][1]
    body = chart[chart.find("<body"):chart.rfind("</body>")]
    inl = MIN % ("", VR.splice_marker_start("Chart-line#c", "knowledge/snippets/Chart-line.reference.html", "markup") +
                 body[body.find(">") + 1:] + VR.splice_marker_end("Chart-line#c"))
    note("F1", "the Chart-line snippet's body spliced WITH its inlined behaviour script",
         lambda: g.gate_page(inl),
         "the motion regex reads script text: dv-render's comment 'turns it into a transition:' trips 2.3.3 for a part "
         "whose reduced-motion block lives in the snippet's <head>; the stand-in loads behaviour by address to avoid it")
    # F2 (a well-formed binding refused by the catalogue) was fixed in the generator at #313 lane C1F: scored as B1
    RESULTS["known"] = known

    # ================================================================ T3.3
    vt, va = g.gate_surface(T), g.gate_surface(A)
    vp = g.gate_page(g.splice(T)[0])
    RESULTS["T3.3"] = {"treasurer_surface": vt, "analyst_surface": va, "treasurer_page": vp}
    say(vt["verdict"] == "pass", "T3.3a", "treasurer surface (frame, wall, metric, status, list, line chart): %s; unmeasured: %s"
        % (vt["verdict"], [c["id"] for c in vt["checks"] if c["result"] == "unmeasured"]))
    say(va["verdict"] == "pass", "T3.3b", "operations-analyst surface (frame, wall, metric, status, list, bar chart): %s"
        % va["verdict"])
    say(vp["verdict"] == "pass", "T3.3c", "treasurer stand-in page, page layer: %s; unmeasured: %s"
        % (vp["verdict"], [c["id"] for c in vp["checks"] if c["result"] == "unmeasured"]))

    # ================================================================ T3.4
    ms_s, r_s, w_s = audited(lambda: g.gate_surface(T), 25)
    ms_x, r_x, w_x = audited(lambda: g.gate_surface(T, splice=True), 25)
    page = g.splice(T)[0]
    ms_p, r_p, w_p = audited(lambda: g.gate_page(page), 25)
    t4 = {"cold_ms": {"warm_up (catalogue, spec, snippets, icon library, compose memo)": cold_build_ms,
                      "first gate_surface": cold_first_surface, "first gate_page": cold_first_page},
          "page_bytes": len(page), "n": 25}
    for k, ms, r, w in (("gate_surface", ms_s, r_s, w_s), ("gate_surface+splice", ms_x, r_x, w_x), ("gate_page", ms_p, r_p, w_p)):
        t4[k] = {"median_ms": round(statistics.median(ms), 2), "max_ms": round(max(ms), 2),
                 "reads_distinct": r, "writes": len([x for x in w if x[0] == "write"]),
                 "events": sorted({k for k, _p in w}),
                 "mutations": len([x for x in w if x[0] != "write"]),
                 "writes_where": sorted({shorten(p) for _k, p in w})}
    RESULTS["T3.4"] = t4
    s0 = t4["gate_surface"]
    say(s0["writes"] == 0 and not s0["reads_distinct"] and s0["mutations"] == 0, "T3.4a",
        "gate_surface warm: median %.2f ms, max %.2f ms (n=25); %d writes, %d file reads"
        % (s0["median_ms"], s0["max_ms"], s0["writes"], len(s0["reads_distinct"])))
    p0 = t4["gate_page"]
    allowed = {"/dev/shm/<page>", "knowledge/canon/canon.css"}
    say(set(p0["writes_where"]) <= {"/dev/shm/<page>"} and set(p0["reads_distinct"]) <= allowed, "T3.4b",
        "gate_page warm: median %.2f ms, max %.2f ms; %d writes + %d removes, all at /dev/shm/<page>; reads %s"
        % (p0["median_ms"], p0["max_ms"], p0["writes"], p0["mutations"], p0["reads_distinct"]))
    x0 = t4["gate_surface+splice"]
    print("info T3.4c  gate_surface+splice warm: median %.2f ms, max %.2f ms; cold warm-up %.0f ms, first surface %.1f ms, first page %.1f ms"
          % (x0["median_ms"], x0["max_ms"], cold_build_ms, cold_first_surface, cold_first_page))

    # ================================================================ T3.5
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    t = time.perf_counter()
    pr = subprocess.Popen([sys.executable, os.path.join(HERE, "server.py")], stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    rt = {}

    def rpc(obj, key):
        a = time.perf_counter()
        pr.stdin.write(json.dumps(obj) + "\n"); pr.stdin.flush()
        if "id" not in obj:
            return None
        line = pr.stdout.readline()
        rt[key] = round((time.perf_counter() - a) * 1000, 2)
        return json.loads(line)
    init = rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "c3-selftest", "version": "0"}}}, "initialize (warms the gate)")
    rpc({"jsonrpc": "2.0", "method": "notifications/initialized"}, None)
    tl = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, "tools/list")
    cs = rpc({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "gate_surface", "arguments": {"surface": T}}}, "gate_surface")
    cs2 = rpc({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "gate_surface", "arguments": {
        "surface": with_comps(T, [dict(clean[0], content="ghost")] + clean[1:])}}}, "gate_surface (a refused surface)")
    cp = rpc({"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "gate_page", "arguments": {"html": page}}}, "gate_page")
    bad = rpc({"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "gate_page", "arguments": {"html": 3}}}, "gate_page (bad arguments)")
    pr.stdin.close(); pr.wait(timeout=30)
    rt["process, spawn to exit"] = round((time.perf_counter() - t) * 1000, 2)
    err = pr.stderr.read()
    names = [x["name"] for x in tl["result"]["tools"]]
    strip = lambda v: {k: v[k] for k in ("verdict", "checks", "catalogue")}
    ok = (init["result"]["serverInfo"]["name"] == "apollo-gates" and names == ["gate_surface", "gate_page"]
          and strip(cs["result"]["structuredContent"]) == strip(vt)
          and cs2["result"]["structuredContent"]["verdict"] == "fail" and "S5" in failed_ids(cs2["result"]["structuredContent"])
          and strip(cp["result"]["structuredContent"]) == strip(vp)
          and bad["result"]["isError"] is True)
    RESULTS["T3.5"] = {"round_trip_ms": rt, "tools": names, "stderr_bytes": len(err)}
    say(ok, "T3.5", "stdio: tools %s; verdicts equal the in-process ones; a refused surface fails S5; bad arguments are isError; "
        "round trips %s" % (names, json.dumps(rt)))

    # ================================================================ T3.6
    RESULTS["T3.6"] = {"render_leg": "UNMEASURED", "why": "cloud lane, no seat (the render leg needs ensure_env.sh + seat_env.sh "
                       "at Dave's seat)", "price": "one seat call: export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; "
                       "source knowledge/_render/seat_env.sh; time python3 knowledge/_validate_screen.py --render <one dashboard page>"}
    print("info T3.6  render leg UNMEASURED (cloud lane, no seat); price: " + RESULTS["T3.6"]["price"])

    print("\nCOUNTS: T3.1 a11y %d/%d, page layer %d/%d, planted %d/6 · T3.2 %d/%d refused or passed by name · T3.3 %s · "
          "T3.4 surface %.1f ms median · T3.5 %s · T3.6 UNMEASURED · failed: %s"
          % (same_a11y, len(snips), same_page, len(snips), sum(x["identical"] for x in t1b.values()),
             sum(c["ok"] for c in cases), len(cases),
             "/".join(x["verdict"] for x in (vt, va, vp)), s0["median_ms"], "ok" if "T3.5" not in FAILED else "FAIL",
             FAILED or "none"))
    if "--json" in sys.argv:
        print(json.dumps(RESULTS, indent=1, ensure_ascii=False, default=str))
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
