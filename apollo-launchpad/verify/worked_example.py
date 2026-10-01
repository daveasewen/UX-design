#!/usr/bin/env python3
"""Launchpad verifier — the worked example end to end (#313 lane CV; spec § 8, § 9, § 11).

One request in, one screen out, the reasons on record. For each of the worked example's two requests
(mock/requests.json: the treasurer and the operations analyst, "What needs my attention this morning?",
09:10 on month end) this runs the chain the proposal's `dashboard` tool names — choose → entitle → gate →
record — with the pieces steps one, three and four built:

  1. choose()                      chooser/choose.py (C4), on the catalogue in tree (C1)
  2. compose the surface           THIS FILE: a stand-in for the agent/host, A2UI v0.9.1 messages built
                                   from choose()'s tiles and mock/data.json (not a renderer, not E1)
  3. gate_surface(splice=True)     gates/gate_mem.py (C3): surface layer S1–S9, page layer P0–P4
  4. the same surface over stdio   gates/server.py (C3): verdict must equal the in-process one
  5. the record per screen         spec § 8, written to apollo-launchpad/records/ with --write

Each screen is composed twice: with its data inline (literal values), and with its data in the
surface's data model and the settings BOUND to it (A2UI's DataBinding, `{"path": ...}`) — the way a
host is meant to send data. The bound form is the one C3 found refused (catalogue `oneOf` matches a
binding twice); it is reported as BLOCKED, never as a pass or a fail of this chain.

Then the bad screens: the analyst's composed surface with one defect each, through the same gate.

Stdlib + the launchpad venv's jsonschema (the surface layer). Writes nothing unless --write.
Run:  PYTHONDONTWRITEBYTECODE=1 $VENV/bin/python apollo-launchpad/verify/worked_example.py [--write] [--json]
"""
import copy, hashlib, json, os, subprocess, sys, time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
LP = os.path.dirname(HERE)
ROOT = os.path.dirname(LP)
sys.path.insert(0, os.path.join(LP, "chooser"))
sys.path.insert(0, os.path.join(LP, "gates"))

import choose as CH          # noqa: E402  (C4)
import gate_mem as GM        # noqa: E402  (C3)

DATA = json.load(open(os.path.join(LP, "mock", "data.json"), encoding="utf-8"))
REQS = json.load(open(os.path.join(LP, "mock", "requests.json"), encoding="utf-8"))
RECORDS = os.path.join(LP, "records")
PROPOSAL_QUESTION = "What needs my attention this morning?"   # spec § 9, verbatim


def pascal(slug):
    return "".join(w[:1].upper() + w[1:] for w in slug.split("-"))


def money(v, cur="GBP"):
    return ("£" if cur == "GBP" else cur + " ") + "{:,.0f}".format(v)


# ------------------------------------------------------------------ step 2: compose
def tile_component(tile, item, bind):
    """One tile part from choose()'s tile row and the item's mock data. Returns (component, data-model
    entries). Only settings the catalogue entry carries are sent; what the entry cannot carry is listed."""
    cid, d = tile["item"], item.get("data") or {}
    c = {"id": cid, "component": tile["component"]}
    model, cannot = {}, []
    for k, v in (tile.get("settings") or {}).items():
        c[k] = v
    part = tile["part"]
    if part == "metric":
        c["state"] = "ready"
        if d.get("delta") is not None:
            c["delta"] = "up" if d["delta"] > 0 else ("down" if d["delta"] < 0 else "flat")
        cur = d.get("currency")
        fig = (lambda x: money(x, cur)) if cur else str
        dl = d.get("delta") or 0
        cannot.append("the figure itself (%s, %s%s %s): Metric has no setting for the number it shows"
                      % (fig(d["value"]), "+" if dl >= 0 else "-", fig(abs(dl)), d.get("period")))
    elif part == "status-indicator":
        c["variant"] = d.get("variant", "pending")
    elif part == "list-items":
        flags = tile.get("flags") or []
        rows = []
        for i, r in enumerate(d.get("records") or []):
            title = r.get("payee") or r.get("kind") or r.get("name") or r.get("id")
            row = {"title": title, "id": r.get("id")}
            if "amount" in r:
                row["value"] = money(r["amount"], r.get("currency", "GBP"))
            if i < len(flags):
                row["detail"] = {"within-limit": "within limit", "second-approver": "needs a second approver"}.get(
                    flags[i], flags[i])
            elif r.get("opened"):
                row["detail"] = "opened " + r["opened"][11:16]
            rows.append(row)
        if bind:
            model["/" + cid + "/items"] = rows
            c["items"] = {"path": "/" + cid + "/items"}
        else:
            c["items"] = rows
    elif part in ("chart-line", "chart-bar"):
        series = d.get("series") or []
        if part == "chart-line":
            c["series"] = len(series)
        data = {k: v for k, v in d.items() if k in ("series", "categories", "x", "unit_scale")}
        if bind:
            model["/" + cid + "/data"] = data
            c["data"] = {"path": "/" + cid + "/data"}
        else:
            c["data"] = data
    return c, model, cannot


def compose(choice, bind=False):
    """A2UI v0.9.1 messages for one screen: frame (shell + title + nav) holding the wall holding the tiles."""
    sid = choice["role"]
    cat_id = choice["catalogue"]["id"]
    comps = [
        {"id": "root", "component": pascal(choice["frame"]["shell"]), "brand": "title", "primaryNav": "nav",
         "content": "wall"},
        {"id": "title", "component": "Headers", "title": choice.get("question") or PROPOSAL_QUESTION,
         "subtitle": "Month end · " + (choice.get("asked_at") or "")[11:16]},
        {"id": "nav", "component": "Navigations"},
        {"id": "wall", "component": pascal(choice["frame"]["wall"]), "tiles": [t["item"] for t in choice["tiles"]]},
    ]
    model, cannot = {}, []
    for t in choice["tiles"]:
        c, m, cn = tile_component(t, DATA["items"][t["item"]], bind)
        comps.append(c); model.update(m); cannot += [t["item"] + ": " + x for x in cn]
    msgs = [{"version": "v0.9.1", "createSurface": {"surfaceId": sid, "catalogId": cat_id}},
            {"version": "v0.9.1", "updateComponents": {"surfaceId": sid, "components": comps}}]
    for path, value in model.items():
        msgs.append({"version": "v0.9.1", "updateDataModel": {"surfaceId": sid, "path": path, "value": value}})
    return msgs, cannot


# ------------------------------------------------------------------ step 4: stdio
def stdio_round_trip(calls):
    """Spawn gates/server.py, initialize, then one tools/call per (name, args). Returns verdicts, timings."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.Popen([sys.executable, os.path.join(LP, "gates", "server.py")], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, env=env, cwd=ROOT)

    def rpc(i, method, params):
        t = time.perf_counter()
        p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": i, "method": method, "params": params}) + "\n")
        p.stdin.flush()
        r = json.loads(p.stdout.readline())
        return r, round((time.perf_counter() - t) * 1000, 2)
    out, times = [], {}
    _r, times["initialize"] = rpc(0, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                                    "clientInfo": {"name": "cv", "version": "0"}})
    for n, (name, args) in enumerate(calls, 1):
        r, ms = rpc(n, "tools/call", {"name": name, "arguments": args})
        times["call %d" % n] = ms
        res = r.get("result") or {}
        out.append((res.get("isError"), res.get("structuredContent")))
    p.stdin.close(); p.wait(timeout=30)
    return out, times


# ------------------------------------------------------------------ step 5: the record
def rulings_of(entry):
    r = ((entry or {}).get("x-apollo") or {}).get("rulings") or {}
    out = []
    for k in ("governs", "obeysAuthored", "obeysDerived"):
        out += r.get(k) or []
    return out


def record(choice, msgs, verdict, gate):
    surface_bytes = json.dumps(msgs, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    sh = hashlib.sha256(surface_bytes).hexdigest()
    comps = GM.Gate.components_of(msgs)
    parts, rulings = [], set()
    for c in comps:
        e = gate.entry(c["component"]) or {}
        xa = e.get("x-apollo") or {}
        parts.append({"id": c["id"], "component": c["component"], "slug": xa.get("slug"),
                      "proposal": bool(xa.get("proposal")), "provides": xa.get("provides")})
        rulings.update(rulings_of(e))
    cat = choice["catalogue"]
    return {
        "screen_id": "%s-%s-%s" % (choice["asked_at"], choice["role"], sh[:8]),
        "asked_at": choice["asked_at"], "question": choice["question"], "role": choice["role"],
        "catalogue": {"id": cat.get("id"), "version": cat.get("version"), "sha256": cat.get("sha256"),
                      "metas_sha": cat.get("metas_sha")},
        "parts": parts,
        "rulings_obeyed": sorted(rulings),
        "entitlement": [{"tool": g["tool"], "scope": g.get("scope"), "allowed": g["allowed"],
                         "reason": g.get("reason")} for g in choice["grants"]],
        # spec § 7/§ 8: refusals AND gate-false parts; choose() keeps the second per tile under `excluded`
        "not_chosen": [{"part": n["part"], "why": n["why"], "item": n.get("item")} for n in choice["not_chosen"]] +
                      [{"part": x["part"], "why": x["why"], "item": t["item"]}
                       for t in choice["tiles"] for x in (t.get("excluded") or [])],
        "gate": verdict,
        "ranker": choice["ranker"],
        "host": "none",
        "surface_sha256": sh,
        "surface": msgs,
    }


# ------------------------------------------------------------------ the bad screens
def bad_screens(msgs, line_msgs):
    """One defect each, on a copy of a composed surface. (label, expected check ids, messages)."""
    def comps_of(m):
        return m[1]["updateComponents"]["components"]
    out = []
    m = copy.deepcopy(msgs); cs = comps_of(m)
    cs.append({"id": "trail", "component": "Breadcrumbs"}); next(c for c in cs if c["id"] == "wall")["tiles"].append("trail")
    out.append(("a fifth kind of tile: a breadcrumb trail on the wall (s313-D41 keeps four)", {"S6"}, m))
    m = copy.deepcopy(line_msgs); cs = comps_of(m)
    ch = next(c for c in cs if c["component"] == "ChartLine")
    ch["data"]["series"] = ch["data"]["series"] * 6; ch["series"] = 6
    out.append(("the treasurer's line chart carrying six series (time-series × 1–5-series)", {"S9"}, m))
    m = copy.deepcopy(msgs); cs = comps_of(m)
    next(c for c in cs if c["id"] == "wall")["tiles"].append("ghost")
    out.append(("the wall names a tile that is not on the screen", {"S5"}, m))
    m = copy.deepcopy(msgs); cs = comps_of(m)
    next(c for c in cs if c["component"] == "Metric")["state"] = "celebrating"
    out.append(("the metric in a state it does not have", {"S8"}, m))
    m = copy.deepcopy(msgs); cs = comps_of(m)
    root = next(c for c in cs if c["id"] == "root"); del root["content"]
    out.append(("the frame with no page in it (required slot missing)", {"S1", "S2"}, m))
    return out


# ------------------------------------------------------------------ main
def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="write the two records under apollo-launchpad/records/")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    lines, fails, figures = [], 0, {}

    def say(ok, tag, text):
        nonlocal fails
        mark = {True: "ok  ", False: "FAIL", None: "info", "blocked": "BLKD"}[ok]
        if ok is False:
            fails += 1
        lines.append("%s %-6s %s" % (mark, tag, text))

    t = time.perf_counter()
    gate = GM.gate()
    figures["warm_ms"] = round((time.perf_counter() - t) * 1000, 1)
    say(None, "V0", "gate warm %.0f ms on catalogue %s sha256 %s… metas_sha %s" % (
        figures["warm_ms"], gate.cat_id["version"], (gate.cat_id["sha256"] or "")[:12],
        ((gate.cat.get("x-apollo") or {}).get("catalogue") or {}).get("metas_sha")))

    screens, records = {}, {}
    for req in REQS["worked_example"]:
        rid = req["id"]
        if req.get("question") != PROPOSAL_QUESTION:
            say(False, "V1", "%s: question is not the proposal's verbatim" % rid)
        t = time.perf_counter()
        choice = CH.choose_request(req)
        ms_choose = round((time.perf_counter() - t) * 1000, 2)
        exp = req.get("expect") or {}
        tiles = [x["part"] for x in choice["tiles"]]
        ok = tiles == exp.get("tiles") and choice["frame"]["shell"] == exp["frame"]["shell"] \
            and choice["frame"]["wall"] == exp["frame"]["wall"]
        say(ok, "V1", "%s choose(): frame %s + %s, tiles %s, not chosen %s (%.2f ms)" % (
            rid, choice["frame"]["shell"], choice["frame"]["wall"], tiles,
            [(n["part"], n["why"]) for n in choice["not_chosen"]], ms_choose))
        # every tile carries its reasons, every grant row is on the choice
        say(all(x.get("reasons") for x in choice["tiles"]), "V1r", "%s every tile carries its reasons (%s)" % (
            rid, ", ".join("%s %d" % (x["part"], len(x["reasons"])) for x in choice["tiles"])))

        msgs, cannot = compose(choice, bind=False)
        t = time.perf_counter()
        v = gate.gate_surface(msgs, splice=True)
        ms_gate = round((time.perf_counter() - t) * 1000, 2)
        bad = [(c["id"], c["reasons"][:2]) for c in v["checks"] if c["result"] == "fail"]
        unm = [c["id"] for c in v["checks"] if c["result"] == "unmeasured"]
        say(v["verdict"] == "pass", "V2", "%s composed surface (data inline) + stand-in page: %s in %.0f ms; "
            "unmeasured %s%s" % (rid, v["verdict"], ms_gate, unm, ("; fails " + json.dumps(bad, ensure_ascii=False)) if bad else ""))
        for x in cannot:
            say(None, "V2c", "%s cannot carry %s" % (rid, x))

        mb, _ = compose(choice, bind=True)
        vb = gate.gate_surface(mb, splice=False)
        badb = [c["id"] for c in vb["checks"] if c["result"] == "fail"]
        n_bound = sum(1 for m in mb if "updateDataModel" in m)
        if vb["verdict"] == "pass":
            say(True, "V3", "%s the same screen with its data BOUND (%d bindings): pass — the catalogue takes "
                "bound data" % (rid, n_bound))
        else:
            s2 = next((c for c in vb["checks"] if c["id"] == "S2"), None) or {}
            why = " | ".join(r for r in (s2.get("reasons") or [])[:2])
            say("blocked", "V3", "%s the same screen with its data BOUND (%d bindings): refused by %s — %s"
                % (rid, n_bound, badb, why[:200]))
        screens[rid] = (choice, msgs, v)
        records[rid] = record(choice, msgs, v, gate)

    # two roles, one question, one clock, two different correct screens, the reasons on record (spec § 9)
    tc, ac = screens["treasurer-0910"][0], screens["analyst-0910"][0]
    same_q = tc["question"] == ac["question"] and tc["asked_at"] == ac["asked_at"]
    diff = [x["part"] for x in tc["tiles"]] != [x["part"] for x in ac["tiles"]]
    an_refused = [(n["part"], n["why"]) for n in ac["not_chosen"]]
    say(same_q and diff and ("metric", "positions refused for this role") in an_refused, "V4",
        "same question and clock, two roles, two screens; the analyst's record names the cash position "
        "refused: %s" % an_refused)
    tr = records["treasurer-0910"]
    flags = next(x.get("flags") for x in tc["tiles"] if x["part"] == "list-items")
    say(flags == ["within-limit", "within-limit", "second-approver"], "V4b",
        "treasurer's third payment flagged second-approver, never prepared: %s" % flags)
    grants_ok = all(r["entitlement"] == [{"tool": g["tool"], "scope": g["scope"], "allowed": g["allowed"],
                                          "reason": g.get("reason")} for g in (req.get("expect") or {}).get("grants", [])]
                    for r, req in ((records[q["id"]], q) for q in REQS["worked_example"]))
    say(grants_ok, "V4c", "each record's entitlement rows equal the request's expected grants row for row")

    # the record per screen (spec § 8)
    keys = ["screen_id", "asked_at", "question", "role", "catalogue", "parts", "rulings_obeyed", "entitlement",
            "not_chosen", "gate", "ranker", "host", "surface_sha256", "surface"]
    for rid, r in records.items():
        miss = [k for k in keys if k not in r]
        props = [p["slug"] for p in r["parts"] if p["proposal"]]
        say(not miss and r["ranker"]["switch"] == "off", "V5", "%s record %s: %d parts (proposals named: %s), "
            "%d rulings obeyed, gate %s%s" % (rid, r["screen_id"], len(r["parts"]), props, len(r["rulings_obeyed"]),
                                              r["gate"]["verdict"], (" MISSING " + str(miss)) if miss else ""))
        # replay: the record's surface gives the same surface verdict again
        rv = gate.gate_surface(r["surface"], splice=True)
        same = [(c["id"], c["result"]) for c in rv["checks"]] == [(c["id"], c["result"]) for c in r["gate"]["checks"]]
        say(same, "V5r", "%s replay from the record: same verdict, check by check" % rid)

    # the same surfaces over stdio (C3's server)
    calls = [("gate_surface", {"surface": screens[q][1], "splice": True}) for q in ("treasurer-0910", "analyst-0910")]
    res, times = stdio_round_trip(calls)
    eq = all((not err) and sc and [(c["id"], c["result"]) for c in sc["checks"]] ==
             [(c["id"], c["result"]) for c in screens[q][2]["checks"]]
             for (err, sc), q in zip(res, ("treasurer-0910", "analyst-0910")))
    say(eq, "V6", "over stdio (apollo-gates): both verdicts equal the in-process ones; round trips %s"
        % json.dumps(times))

    # bad screens through the gate
    base = screens["analyst-0910"][1]
    m6 = copy.deepcopy(base); bar = next(c for c in m6[1]["updateComponents"]["components"] if c["component"] == "ChartBar")
    bar["data"]["series"] = bar["data"]["series"] * 6
    v6 = gate.gate_surface(m6)
    s9 = next((c for c in v6["checks"] if c["id"] == "S9"), {})
    say(None, "V7i", "the analyst's bar chart carrying six series: %s (S9 %s: categories × series states no count)"
        % (v6["verdict"], s9.get("result")))
    for label, want, m in bad_screens(base, screens["treasurer-0910"][1]):
        v = gate.gate_surface(m, splice=False)
        got = {c["id"] for c in v["checks"] if c["result"] == "fail"}
        say(v["verdict"] == "fail" and want <= got, "V7", "bad screen — %s: %s, refused by %s (want %s)" % (
            label, v["verdict"], sorted(got), sorted(want)))
    # a whole bad page through gate_page: the analyst's stand-in page with one 16px control spliced in
    page, _ = gate.splice(base)
    small = page.replace("</body>", '<button style="width:16px;height:16px" aria-label="x">x</button></body>')
    v = gate.gate_page(small)
    got = sorted(c["id"] for c in v["checks"] if c["result"] == "fail")
    say(v["verdict"] == "fail" and "P1" in got, "V7p", "bad page — the analyst's stand-in page plus a 16px "
        "button: %s, refused by %s" % (v["verdict"], got))

    # the surface names its catalogue; does the gate hold it to the one it gates against? (record pins by both)
    mc = copy.deepcopy(screens["treasurer-0910"][1])
    mc[0]["createSurface"]["catalogId"] = "https://example.invalid/another-catalogue/v9/catalog.json"
    vc = gate.gate_surface(mc)
    say(None, "V8", "a surface that names ANOTHER catalogue (%s): %s — the gate %s the surface's catalogId "
        "against its own (%s)" % (mc[0]["createSurface"]["catalogId"], vc["verdict"],
                                  "does not compare" if vc["verdict"] == "pass" else "compares", gate.cat_id["id"]))

    if a.write:
        os.makedirs(RECORDS, exist_ok=True)
        for r in records.values():
            p = os.path.join(RECORDS, r["screen_id"].replace(":", "") + ".json")
            with open(p, "w", encoding="utf-8") as f:
                f.write(json.dumps(r, indent=2, ensure_ascii=False) + "\n")
            say(None, "W", "wrote " + os.path.relpath(p, ROOT))

    print("\n".join(lines))
    print("worked example — %s, %d failed" % ("GREEN" if not fails else "RED", fails))
    if a.json:
        print(json.dumps({"records": records}, ensure_ascii=False)[:2000])
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
