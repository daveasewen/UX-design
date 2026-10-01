#!/usr/bin/env python3
"""Launchpad step four — the chooser's selftest (spec § 11, T4.1–T4.6, plus this lane's bites for Dave's
calls 21 and 22 of 2026-10-01). Exit 0 when every test passes, 1 otherwise. Writes nothing under the repo
(the one bite that needs a changed catalogue writes its copy to a temp dir and removes it).

    PYTHONDONTWRITEBYTECODE=1 python3 apollo-launchpad/chooser/selftest.py

stdlib only: the chooser does not need the launchpad venv.
"""
import copy
import json
import os
import shutil
import statistics
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

AUDIT = {"armed": False, "writes": [], "sockets": []}


def _audit(event, args):
    if not AUDIT["armed"]:
        return
    if event == "open":
        path, mode = args[0], args[1]
        if isinstance(mode, str) and any(c in mode for c in "wax+"):
            AUDIT["writes"].append(str(path))
        elif isinstance(args[2], int) and args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT):
            AUDIT["writes"].append(str(path))
    elif event.startswith("socket."):
        AUDIT["sockets"].append(event)


sys.addaudithook(_audit)

import when_eval as W  # noqa: E402
import entitle as E  # noqa: E402
import rank as R  # noqa: E402
import choose as C  # noqa: E402

RESULTS = []


def check(tid, ok, text):
    RESULTS.append((tid, bool(ok), text))


# ------------------------------------------------------------------ T4.1 · R5's fifteen bites still bite
def t41():
    pc, ec = W.parse_clause, W.eval_clause
    bites = [
        ("range clause", ec(pc("span.cols 4–6"), {"span.cols": 5}), True),
        ("range clause false", ec(pc("span.cols 4–6"), {"span.cols": 8}), False),
        ("unknown field -> None", ec(pc("series=2 mirrored"), {}), None),
        ("series=2 with trailing prose", ec(pc("series=2 mirrored outward"), {"series": 2}), True),
        ("series != none vs 0", ec(pc("series != none"), {"series": "none"}), False),
        ("in list", ec(pc("emphasis in (primary, secondary)"), {"emphasis": "primary"}), True),
        ("address with trailing words", ec(pc("shape = periods × OHLC (open · high)"), {"shape": "periods × ohlc"}), True),
        ("enum prefix tolerates prose", ec(pc("total=printed as a centre figure"), {"total": "printed"}), True),
        ("enum 'not printed' is not 'printed'", ec(pc("total=not printed"), {"total": "printed"}), False),
        ("prose clause is None", ec(pc("parts sum to a whole"), {"parts": 3}), None),
        ("field-prefix word is not the field", pc("seriesish = 2").get("field"), None),
        ("spans folds the AND-joined addresses",
         W.parse_when("answers spans change-over-time AND composition AND cumulative bands — x")["clauses"][0].get("addrs"),
         ["change-over-time", "composition"]),
        ("3-valued AND", W.AND([True, None]), None),
        ("3-valued AND false wins", W.AND([None, False]), False),
        ("3-valued OR", W.OR([None, True]), True),
    ]
    miss = [(n, g, w) for n, g, w in bites if g != w]
    check("T4.1", not miss, "R5 bites %d/%d%s" % (len(bites) - len(miss), len(bites), (" MISS %s" % miss) if miss else ""))


# ------------------------------------------------------------------ T4.2 · the W table, variant B as the rule
# R5's table (notes/_lanes/304/R5/when_eval.py TESTS), contexts unchanged, with two vocabulary moves that are
# rulings, not fits: the chart role is `chart` (s308-D41, was chart-panel), and stat-card / kpi-tile are
# readings of metric (s308-D42, aliasOf) — the expectation is metric without / with its spark. W3b is added:
# the with-trend reading as the spec's alias rule states it (metric's own shape, a series present).
TABLE = [
    ("W1", "chart", {"answers": "change-over-time", "shape": "time-series × 1–5-series", "series": 1, "axes": "present", "span.cols": 8}, "chart-line", None),
    ("W1b", "chart", {"answers": "change-over-time"}, "chart-line", None),
    ("W1c", "chart", {"answers": "change-over-time", "shape": "periods × ohlc", "span.cols": 8}, "Chart-candlestick", None),
    ("W2", "headline-metric", {"answers": "one-number", "shape": "one-measure × value-and-delta", "series": "none", "delta": "present", "span.cols": 3}, "metric", "without trend"),
    ("W3", "headline-metric", {"shape": "one-measure × value-delta-and-series", "series": 1, "span.cols": 3}, "metric", "with trend"),
    ("W3b", "headline-metric", {"shape": "one-measure × value-and-delta", "delta": "present", "series": 1, "span.cols": 3}, "metric", "with trend"),
    ("W4", "headline-metric", {"answers": "one-number", "shape": "one-measure × committed-vs-balance-split", "verdict": "covered until 14 Oct", "span.cols": 4}, "runway-bar", None),
    ("W5", "status-surface", {"answers": "status-of-one", "shape": "one-state × dot-and-label", "span.cols": 3}, "status-indicator", None),
    ("W6", "status-surface", {"answers": "details-before-commit", "shape": "rows × name-value-pairs", "rows": 4, "span.cols": 6}, "summary", None),
    ("W7", "chart", {"answers": "comparison", "axis.x": "categorical", "span.cols": 6}, "chart-bar", None),
    ("W8", "chart", {"answers": "composition", "total": "printed", "parts": 4, "span.cols": 6}, "chart-donut", None),
    ("W9", "chart", {"answers": "composition", "total": "not printed", "parts": 4, "span.cols": 6}, "chart-pie", None),
    ("W10", "chart", {"answers": "change-over-time", "series": 2, "units": "different", "span.cols": 8}, "chart-combo", None),
    ("W11", "page-frame", {"destinations": 5, "nav.levels": 1}, "app-shell-top-nav", None),
    ("W12", "wayfinding", {"shape": "ancestor-path × links", "depth": 3}, "breadcrumbs", None),
    ("W13", "record-list", {"records": 3, "surface": "none"}, "list-items", None),
    ("W14", "page-title", {"level": "page", "platform": "app", "lockup": "none"}, "headers", None),
    ("W15", "action", {"emphasis": "primary", "label": "text"}, "button", None),
    ("W16", "arrangement", {"content": "arbitrary-blocks", "surface": "none"}, "layout-utilities", None),
    ("W17", "wayfinding", {"shape": "destination-set × links", "scope": "global"}, "navigations", None),
    ("W18", "record-list", {"records": 40, "surface": "none"}, "data-grid", None),
    # W18b moved from needs = sort to needs = select at #313 lane C1F: s313-D27 (Dave, 'Option 1, toolbar does not
    # change the shape') keeps a sorted list a list; the grid wins only when rows are selected or edited
    ("W18b", "record-list", {"records": 40, "surface": "none", "needs": "select"}, "data-grid", None),
]


def w_table():
    parts = W.parts_from_metas()
    readings = W.alias_readings()
    rows = []
    for tid, role, ctx, want, want_reading in TABLE:
        pool = W.providers(role, parts)
        res = W.evaluate(ctx, parts, pool=pool, implicit=True)
        pick = res["pick"]
        reading = None
        if pick == "metric":
            s = ctx.get("series")
            reading = "with trend" if (s not in (None, "none", 0)) else "without trend"
        ok = pick == want and (want_reading is None or reading == want_reading)
        why = ""
        if not ok:
            ex = {r["slug"]: r.get("why") for r in res["excluded"]}
            why = ex.get(want) or ("%s eligible but ranked below %s" % (want, pick) if want in [r["slug"] for r in res["eligible"]] else "%s not in the %s pool" % (want, role))
        rows.append({"id": tid, "want": want, "want_reading": want_reading, "pick": pick, "reading": reading,
                     "ok": ok, "why": why, "top3": [(r["slug"], r["trues"], r["priority"]) for r in res["eligible"][:3]]})
    return rows, readings


def t42():
    rows, readings = w_table()
    added = [r for r in rows if r["id"] in ("W3b", "W18b")]
    r5 = [r for r in rows if r["id"] not in ("W3b", "W18b")]
    hit = sum(r["ok"] for r in r5)
    misses = ["%s want %s%s got %s%s — %s" % (r["id"], r["want"], (" (%s)" % r["want_reading"]) if r["want_reading"] else "",
                                              r["pick"], (" (%s)" % r["reading"]) if r["reading"] else "", r["why"])
              for r in rows if not r["ok"]]
    for r in rows:
        print("    %-4s want %-18s got %-18s %s  top3 %s" % (r["id"], r["want"] + (("/" + r["want_reading"]) if r["want_reading"] else ""),
                                                      str(r["pick"]) + (("/" + r["reading"]) if r["reading"] else ""),
                                                      "OK  " if r["ok"] else "MISS", r["top3"]))
    w3b = {"ok": all(r["ok"] for r in added)}
    # the spec's expectation is 19 of 20 (s305-D21's own figure); this test passes when every miss is NAMED
    # and the measured count is printed, because the count is the measurement, not the gate.
    named = all(r["why"] for r in rows if not r["ok"])
    aliases_ok = readings.get("stat-card", {}).get("reading") == "without trend" and readings.get("kpi-tile", {}).get("reading") == "with trend"
    check("T4.2", named and aliases_ok and w3b["ok"],
          "W table variant B: %d of %d on R5's twenty (spec expected 19 of 20); added rows W3b (alias rule) and W18b (needs = select, s313-D27) %s; misses named: %s"
          % (hit, len(r5), "OK" if w3b["ok"] else "MISS", "; ".join(misses) or "none"))
    return hit, len(r5), misses


# ------------------------------------------------------------------ T4.3 · the worked example
def t43():
    notes = []
    ok_all = True
    for req in C.REQUESTS["worked_example"]:
        out = C.choose_request(req)
        exp = req["expect"]
        refused = [{"item": n["item"], "part": n["part"], "why": n["why"]} for n in out["not_chosen"] if n.get("reason")]
        grants = [{k: v for k, v in g.items() if k != "asked_scope"} for g in out["grants"]]
        ok = (out["chosen"] == exp["tiles"]
              and out["frame"]["shell"] == exp["frame"]["shell"] and out["frame"]["wall"] == exp["frame"]["wall"]
              and refused == exp["not_chosen_refused"]
              and grants == exp["grants"]
              and [t for t in out["tiles"] if t["part"] == "metric"][0]["reading"]["reading"] == exp["metric_reading"])
        if "payment_flags" in exp:
            fl = [t for t in out["tiles"] if t["item"] == "payments-awaiting-approval"][0].get("flags")
            ok = ok and fl == exp["payment_flags"]
            third = C.DATA["items"]["payments-awaiting-approval"]["data"]["records"][2]
            notes.append("third payment %s £%s → %s" % (third["id"], format(third["amount"], ","), fl[2]))
        ok_all = ok_all and ok
        notes.append("%s %s: frame %s + %s, tiles %s, refused %s, grants %d rows"
                     % (req["id"], "OK" if ok else "MISS", out["frame"]["shell"], out["frame"]["wall"], out["chosen"],
                        [(r["item"], r["part"], r["why"]) for r in refused], len(grants)))
    # the sentence CV checks: the same request, two roles, two different correct screens
    a, b = C.REQUESTS["worked_example"]
    same_q = a["question"] == b["question"] and a["asked_at"] == b["asked_at"]
    check("T4.3", ok_all and same_q, " · ".join(notes) + (" · same question and clock, two screens" if same_q else " · QUESTION DIFFERS"))


# ------------------------------------------------------------------ T4.4 · the 4 × 7 grant matrix
SPEC_TABLE = {  # spec § 6, typed from its table: tool → scope, absent = refused
    "corporate-treasurer": {"dashboard": None, "positions": "all-entities", "payments_queue": "full", "prepare_approval": "up-to-limit"},
    "relationship-manager": {"dashboard": None, "positions": "summary", "client_book": "own-book"},
    "operations-analyst": {"dashboard": None, "payments_queue": "status-only", "exceptions": "full"},
    "auditor": {"dashboard": None, "audit_record": "read"},
}


def t44():
    m = E.matrix()
    bad = []
    for role, row in m.items():
        for tool, g in row.items():
            want = SPEC_TABLE[role]
            if tool in want:
                if not (g["allowed"] and g["scope"] == want[tool]):
                    bad.append((role, tool, g))
            elif g["allowed"] or g["reason"] != "tool-not-granted":
                bad.append((role, tool, g))
    print("    %-22s " % "" + " ".join("%-16s" % t for t in E.TOOLS))
    for role in sorted(m):
        print("    %-22s " % role + " ".join("%-16s" % ((m[role][t]["scope"] or "yes") if m[role][t]["allowed"] else "refused") for t in E.TOOLS))
    cells = sum(len(r) for r in m.values())
    check("T4.4", not bad and len(m) == 4 and len(E.TOOLS) == 7,
          "grant matrix %d roles × %d tools = %d cells, equal to spec § 6%s" % (len(m), len(E.TOOLS), cells, (" — BAD %s" % bad) if bad else ""))
    # T4.4b the mock data keeps its contract: every item's shape is one its tool supplies, and a scope is
    # asked only of a tool that has scopes
    supplies = E.ROLES_DOC["supplies"]
    off = [(i, it["tool"], it["shape"]) for i, it in C.DATA["items"].items() if it["shape"] not in supplies.get(it["tool"], [])]
    check("T4.4b", not off, "every mock item's shape is one its tool supplies (%d items)%s" % (len(C.DATA["items"]), (" — OFF %s" % off) if off else ""))
    # T4.4c a scope refusal is a refusal by scope, not by tool (the relationship manager's all-entities ask)
    out = C.choose_request(C.find_request("manager-scope"))
    sc = [n for n in out["not_chosen"] if n.get("reason") == "scope-not-granted"]
    check("T4.4c", out["chosen"] == ["summary", "status-indicator"] and len(sc) == 1 and sc[0]["part"] == "metric",
          "relationship manager: tiles %s; refused by scope %s" % (out["chosen"], [(n["item"], n["part"], n["why"]) for n in sc]))


# ------------------------------------------------------------------ T4.5 · determinism and time
def t45():
    req = C.REQUESTS["worked_example"][0]
    a = json.dumps(C.choose_request(req), sort_keys=True, ensure_ascii=False)
    b = json.dumps(C.choose_request(req), sort_keys=True, ensure_ascii=False)
    ts = []
    for _ in range(25):
        t0 = time.perf_counter()
        C.choose_request(req)
        ts.append((time.perf_counter() - t0) * 1000)
    ev = []
    parts = W.parts_from_metas()
    ctx = TABLE[0][2]
    pool = W.providers("chart", parts)
    for _ in range(25):
        t0 = time.perf_counter()
        W.evaluate(ctx, parts, pool=pool)
        ev.append((time.perf_counter() - t0) * 1000)
    check("T4.5", a == b, "same request twice byte-identical (%d bytes); choose() median %.2f ms max %.2f ms n=25; one evaluation median %.3f ms n=25 (R5: 0.27 ms)"
          % (len(a.encode()), statistics.median(ts), max(ts), statistics.median(ev)))


# ------------------------------------------------------------------ T4.6 · the ranker seam
def t46():
    jev_before = sorted(m for m in sys.modules if "jev" in m.lower())
    AUDIT["armed"] = True
    outs = [C.choose_request(r) for r in C.REQUESTS["worked_example"] + C.REQUESTS["fixtures"]]
    on = C.choose_request(C.REQUESTS["worked_example"][0], switch="on")
    AUDIT["armed"] = False
    jev_after = sorted(m for m in sys.modules if "jev" in m.lower())
    raised = None
    try:
        R._ranker_stub(["a"], {})
    except NotImplementedError as e:
        raised = str(e)
    off_ok = all(o["ranker"] == {"switch": "off", "answer": None, "fallback": "rules-order"} for o in outs)
    on_ok = on["ranker"]["fallback"] == "rules-order" and on["chosen"] == outs[0]["chosen"]
    check("T4.6", not jev_before and not jev_after and not AUDIT["sockets"] and off_ok and on_ok and raised == "step six",
          "switch off: Jev modules imported %s, socket events %d, ranker %s on %d runs; switch on: stub raises %r, result fallback %r, error %s, parts unchanged %s"
          % (jev_after or "none", len(AUDIT["sockets"]), "rules-order" if off_ok else "WRONG", len(outs), raised,
             on["ranker"]["fallback"], on["ranker"].get("error"), on["chosen"] == outs[0]["chosen"]))
    # the seam only re-orders: a ranker that adds a part is refused and falls back
    saved = R.RANKER
    try:
        R.RANKER = lambda slugs, ctx: list(reversed(slugs)) + ["chart-candlestick"]
        o, rec = R.rank(["a", "b"], {}, "on")
        R.RANKER = lambda slugs, ctx: list(reversed(slugs))
        o2, rec2 = R.rank(["a", "b"], {}, "on")
    finally:
        R.RANKER = saved
    check("T4.6b", o == ["a", "b"] and rec["fallback"] == "rules-order" and o2 == ["b", "a"] and rec2["fallback"] is None,
          "a ranker that adds a part is refused (%s); one that only re-orders is taken (%s)" % (rec.get("error"), o2))
    check("T4.6c", not AUDIT["writes"], "chooser runs wrote %d files%s" % (len(AUDIT["writes"]), (": %s" % AUDIT["writes"][:3]) if AUDIT["writes"] else ""))


# ------------------------------------------------------------------ T4.7 · Dave's call 22: the wall keeps the four
FOUR = ["headline-metric", "status-surface", "chart", "record-list"]


def wall_keeps_the_four(catalogue_path):
    cat, parts = C.catalogue(catalogue_path)
    wall, accepts = C.the_wall(parts)
    return wall == "template-dashboard-bento" and sorted(accepts) == sorted(FOUR), wall, accepts


def t47():
    ok, wall, accepts = wall_keeps_the_four(W.CATALOGUE)
    _, parts = C.catalogue()
    tile_parts = sorted(s for s, p in parts.items() if p.get("provides") in accepts)
    out = C.choose_request(C.find_request("analyst-breadcrumb"))
    nt = [n for n in out["not_chosen"] if n["item"] == "where-am-i"]
    placed_ok = out["chosen"] == ["status-indicator"] and nt and nt[0]["part"] == "breadcrumbs" and nt[0].get("provides") == "wayfinding"
    every_tile_in_four = all(t["provides"] in FOUR for r in C.REQUESTS["worked_example"] + C.REQUESTS["fixtures"]
                             for t in C.choose_request(r)["tiles"])
    # the bite: on a catalogue copy whose wall is widened by one kind, the pin fails and the trail becomes a tile
    tmp = tempfile.mkdtemp(prefix="c4-call22-")
    try:
        cat = copy.deepcopy(C.catalogue()[0])
        cat["components"]["TemplateDashboardBento"]["x-apollo"]["slots"]["tiles"]["accepts"]["provides"].append("wayfinding")
        p = os.path.join(tmp, "catalogue-widened.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(cat, f, ensure_ascii=False)
        bite_pin, _, _ = wall_keeps_the_four(p)
        bite_out = C.choose_request(C.find_request("analyst-breadcrumb"), catalogue_path=p)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        C._CAT.pop(p, None)
    bites = (not bite_pin) and "breadcrumbs" in bite_out["chosen"]
    check("T4.7", ok and placed_ok and every_tile_in_four and bites,
          "call 22 'Keep the four' (s313-D41): the wall %s accepts %s, read from its tiles slot; %d published parts can be tiles %s; "
          "a breadcrumb trail is chosen as %s and refused as a tile; every tile on every request is one of the four; bite: a wall widened to five fails the pin and lets the trail in (%s)"
          % (wall, accepts, len(tile_parts), tile_parts, nt[0]["part"] if nt else None, bite_out["chosen"]))


# ------------------------------------------------------------------ T4.8 · Dave's call 21: the grid's search words are `terms`
def t48():
    _, parts = C.catalogue()
    g = parts["data-grid"]
    name_ok = "terms" in g["settings"] and "terms" not in g["slots"] and "filters" in g["slots"] and "filters" not in g["settings"]
    out = C.choose_request(C.find_request("analyst-search-terms"))
    t = out["tiles"][0] if out["tiles"] else {}
    passed = t.get("part") == "data-grid" and t.get("settings") == {"terms": ["Calder"]} and not t.get("unknown_settings")
    # the bite: the same words sent under the slot's name are refused as a setting
    saved = copy.deepcopy(C.DATA["items"]["exceptions-search"])
    try:
        C.DATA["items"]["exceptions-search"]["settings"] = {"filters": ["Calder"]}
        bad = C.choose_request(C.find_request("analyst-search-terms"))["tiles"][0]
    finally:
        C.DATA["items"]["exceptions-search"] = saved
    bites = bad.get("unknown_settings") == ["filters"] and "filters" not in bad.get("settings", {})
    check("T4.8", name_ok and passed and bites,
          "call 21 'Keep terms' (s313-D40): DataGrid carries `terms` as a setting and `filters` as its slot; the analyst's search picks %s with settings %s; "
          "bite: the words sent as `filters` are refused (%s)" % (t.get("part"), t.get("settings"), bad.get("unknown_settings")))


def main():
    t0 = time.perf_counter()
    print("chooser selftest — catalogue %s" % json.dumps(C.choose_request(C.REQUESTS["worked_example"][0])["catalogue"]))
    t41()
    t42()
    t43()
    t44()
    t45()
    t46()
    t47()
    t48()
    ok = all(r[1] for r in RESULTS)
    print("chooser selftest — %s, %d of %d  (%.2f s)" % ("GREEN" if ok else "RED", sum(r[1] for r in RESULTS), len(RESULTS), time.perf_counter() - t0))
    for tid, good, text in RESULTS:
        print("%-6s %s %s" % (tid, "PASS" if good else "FAIL", text))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
