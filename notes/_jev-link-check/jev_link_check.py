#!/usr/bin/env python3
"""jev_link_check.py — Jev as a HAND-RUN link checker on four edge types (s305-D55).

WHAT DAVE RULED. The #305 sitting, call 52, Sunday 2026-09-27, answer verbatim: "yes", to
"Adopt Jev as a hand-run link checker on four edge types (obeys, providesRole, answersIntent,
hasDataShape), with a two-band rule: below 0.2 comes to you as "this link looks wrong", above 0.8
is silent, the middle is ignored" — recommended as "A script under notes, never a gate, never in
the build, as your #294 ruling says." So:

  * FOUR EDGE TYPES ONLY: obeys · providesRole · answersIntent · hasDataShape. Any other type is
    REFUSED by name (#304 seat J measured the others as weak, pointless or coin-flip).
  * TWO BANDS: p < 0.2  -> listed for Dave as "this link looks wrong"
               p > 0.8  -> silent (counted, not listed)
               between  -> ignored (counted, not listed)
  * NEVER A GATE, NEVER IN THE BUILD (s294-D10, not amended). Nothing imports this file; it lives
    under notes/ so no build step, gate, wiring scan or pack manifest reaches it. It always exits 0
    when it ran, whatever it found — a flag is a suggestion Dave rules on, never a red.
  * NO CREDENTIAL IS A LOUD, NAMED STOP (exit 3): a hand-run tool that silently does nothing would
    read as "no links look wrong". It prints what is missing and where it looked, asks nothing and
    writes nothing.

HOW IT ASKS — THE #304 SEAT J QUESTION, UNCHANGED. The two-band thresholds were measured with one
question shape (notes/_lanes/304/J/run_edges.py + build_sample.py; report
notes/_subreports/2026-09-27-304-J-jev-edge-node-probe.md: on 50 edges every p < 0.2 was a fake and
every p > 0.8 was real, AUC 0.954). A band measured on one question does not transfer to another,
so the relation meanings, the Noul question and the node descriptions below are that probe's,
copied, not reworded. The authored `$why` is NOT sent (it would test whether Jev can read a
justification, not whether the link holds); it is printed beside a flag for Dave.

THE EDGE LIST is the KG explorer's own reader (`knowledge/_build_kg_explorer.py` extract() +
extract_extra()) — no second reader. Every call goes through `knowledge/_jev.py`, which appends its
receipt to `knowledge/_jev-receipts.jsonl` (the adapter's convention; the key is never printed).

OUTPUT (dated, under notes/_jev-link-check/):
  <date>-raw.jsonl        one line per edge asked: p, band, request id, latency — the RESUME file
  <date>-link-check.md    the list for Dave (p < 0.2), the counts of the other two bands, errors
A run that stops part-way (time, a refusal) is resumed by running it again the same day: edges
already in the raw file are not asked twice.

USAGE
  python3 notes/_jev-link-check/jev_link_check.py                 # the full sweep (~330 calls, ~2-3 min)
  python3 notes/_jev-link-check/jev_link_check.py --max 120       # at most 120 calls this run, then report
  python3 notes/_jev-link-check/jev_link_check.py --report        # rewrite the report from the raw file, no calls
  python3 notes/_jev-link-check/jev_link_check.py --env-file PATH # read the key from PATH instead of .env.local
  python3 notes/_jev-link-check/jev_link_check.py --date YYYY-MM-DD   # which dated files to write/resume
  python3 notes/_jev-link-check/jev_link_check.py --types obeys,hasDataShape  # a subset of the four (never another type)
EXIT  0 ran (flags or not) · 2 bad usage · 3 NO CREDENTIAL · 4 the API refused (auth) — named
"""
import json
import os
import sys
import time
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
K = os.path.join(REPO, "knowledge")
sys.path.insert(0, K)

TYPES = ("obeys", "providesRole", "answersIntent", "hasDataShape")   # s305-D55, the four
LOW, HIGH = 0.2, 0.8                                                  # s305-D55, the two bands

# ---- the #304 seat J question, verbatim (notes/_lanes/304/J/run_edges.py) -------------------
MEAN = {
    "obeys": "The source component is designed to follow the target rule or principle: the target constrains or shapes how this component looks or behaves.",
    "providesRole": "The source component can fill the target role: when a page slot asks for this role, this component is a suitable thing to put there.",
    "answersIntent": "The source component answers the target intent: it is a suitable way to show someone the question the intent describes.",
    "hasDataShape": "The source component takes data of the target shape: the shape describes the data this component is fed and draws.",
}
QUESTION = (
    "Does the relation described in `relation.meaning` genuinely hold from `source` to `target`, judged from what each of them is?",
    "The relation holds: given what the source is and what the target says, a design-system expert would accept this link as correct.",
    "The relation does not hold or is a stretch: the target is about something else, fits a different kind of component, or the two do not relate in the stated way.",
)


def die(code, msg):
    print(msg, file=sys.stderr)
    sys.exit(code)


def args(argv):
    a = {"max": None, "report": False, "env": None, "date": date.today().isoformat(), "types": TYPES}
    it = iter(argv)
    for x in it:
        if x == "--max":
            a["max"] = int(next(it, "0") or 0)
        elif x == "--report":
            a["report"] = True
        elif x == "--env-file":
            a["env"] = next(it, None)
        elif x == "--date":
            a["date"] = next(it, a["date"])
        elif x == "--types":
            want = [t for t in next(it, "").split(",") if t]
            bad = [t for t in want if t not in TYPES]
            a["types"] = tuple(t for t in TYPES if t in want)
            if bad or not want:
                die(2, "REFUSED — edge type(s) %s are not in the ruled four (%s). s305-D55 adopts Jev "
                       "on these four only." % (", ".join(bad), ", ".join(TYPES)))
        elif x in ("-h", "--help"):
            print(__doc__); sys.exit(0)
        else:
            die(2, "unknown argument %r (see --help)" % x)
    return a


def edges_and_describer():
    """The explorer's own edge list, filtered to the four, plus the #304 J node describer."""
    saved = sys.argv
    sys.argv = ["x", "/dev/null"]                       # the builder reads its OUT path at import
    try:
        import _build_kg_explorer as B
    finally:
        sys.argv = saved
    n, e = B.extract()
    r = B.extract_extra(n, e)
    N = {x["id"]: x for x in n}
    N.update({x["id"]: x for x in r[0]})
    seen, E = set(), []
    for x in e + r[1]:
        if x.get("type") in TYPES and x.get("t"):
            key = (x["s"], x["type"], x["t"])
            if key not in seen:
                seen.add(key)
                E.append(x)
    rules = {x["id"]: x for x in json.load(open(os.path.join(K, "_rule_nodes.json")))["nodes"]
             if x["id"].startswith("rule:")}
    roles = json.load(open(os.path.join(K, "roles.json")))["roles"]
    intents = json.load(open(os.path.join(K, "chart-intents.json")))["chart-intent"]
    shapes = json.load(open(os.path.join(K, "shapes.json")))["shapes"]
    UX = {x["id"]: x for x in json.load(open(os.path.join(K, "_ux_principle_nodes.json")))["nodes"]}

    def desc(nid):                                      # notes/_lanes/304/J/build_sample.py desc()
        kind, key = nid.split(":", 1)
        x = N.get(nid, {})
        if kind == "component":
            return {"kind": "UI component", "name": x.get("label"), "purpose": x.get("purpose", "")}
        if kind == "rule":
            return {"kind": "design-system rule", "id": key, "text": (rules.get(nid, {}).get("text") or "")[:700]}
        if kind == "ux":
            return {"kind": "UX principle", "name": key.replace("pr-", "").replace("-", " "),
                    "statement": UX.get(nid, {}).get("statement", "")}
        if kind == "role":
            ro = roles.get(key, {})
            return {"kind": "layout role (a job a slot asks a component to do)", "name": key,
                    "definition": ro.get("definition", "")}
        if kind == "intent":
            it = intents.get(key, {})
            return {"kind": "chart intent (the question a chart answers)", "name": key,
                    "definition": it.get("definition", ""), "not_for": it.get("notFor", "")}
        if kind == "shape":
            s = shapes.get(key, {})
            return {"kind": "data shape (what data a component takes)", "name": key,
                    "definition": s.get("definition", "")}
        return {"kind": kind, "name": key}

    return E, desc, N


def band(p):
    if p is None:
        return "error"
    return "looks-wrong" if p < LOW else "silent" if p > HIGH else "ignored"


def read_raw(path):
    done = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                done[(r["s"], r["type"], r["t"])] = r
    return done


def report(a, E, N, raw_path, md_path, run_note):
    done = read_raw(raw_path)
    total = len(E)
    rows = [done[k] for k in ((x["s"], x["type"], x["t"]) for x in E) if k in done]
    asked = [r for r in rows if r.get("p") is not None]
    errs = [r for r in rows if r.get("p") is None]
    flags = sorted((r for r in asked if r["p"] < LOW), key=lambda r: r["p"])
    silent = sum(1 for r in asked if r["p"] > HIGH)
    ignored = len(asked) - len(flags) - silent
    pending = total - len(rows)
    by = {t: [r for r in asked if r["type"] == t] for t in TYPES}
    why = {(x["s"], x["type"], x["t"]): (x.get("why") or x.get("note") or "") for x in E}
    lab = lambda nid: (N.get(nid, {}).get("label") or nid)
    L = []
    A = L.append
    A("# Jev link check — %s" % a["date"])
    A("")
    A("provenance: hand-run by `notes/_jev-link-check/jev_link_check.py` under `s305-D55` (Dave, #305 sitting call 52, \"yes\") · "
      "ADVISORY, never a gate, never in the build (`s294-D10`) · raw answers `%s` · receipts `knowledge/_jev-receipts.jsonl`"
      % os.path.relpath(raw_path, REPO))
    A("")
    A("**%d of %d links asked** (obeys, providesRole, answersIntent, hasDataShape)%s. "
      "**%d look wrong** (p < %.1f, listed below for you to rule) · %d silent (p > %.1f) · %d ignored (the middle) · %d error(s)."
      % (len(asked), total, "" if not pending else " — **%d NOT YET ASKED**, run it again today to finish" % pending,
         len(flags), LOW, silent, HIGH, ignored, len(errs)))
    A("")
    A("The bands were measured on 50 edges at #304 (seat J): every link under 0.2 was a fake, every link over 0.8 was real. "
      "That is n = 50 on one day — a flag is a suggestion, and the graph changes only by your word.")
    A("")
    A("## This link looks wrong (p < %.1f)" % LOW)
    A("")
    if not flags:
        A("None.")
    else:
        A("| # | link | p | the designer's reason on the edge |")
        A("|---|---|---|---|")
        for i, r in enumerate(flags, 1):
            A("| %d | `%s` —%s→ `%s` (%s → %s) | %.2f | %s |" % (
                i, r["s"], r["type"], r["t"], lab(r["s"]), lab(r["t"]), r["p"],
                (why.get((r["s"], r["type"], r["t"])) or "—").replace("|", "/").replace("\n", " ")[:300]))
    A("")
    A("## Counts by edge type")
    A("")
    A("| type | links | asked | looks wrong | silent | ignored |")
    A("|---|---|---|---|---|---|")
    for t in TYPES:
        rs = by[t]
        A("| %s | %d | %d | %d | %d | %d |" % (t, sum(1 for x in E if x["type"] == t), len(rs),
            sum(1 for r in rs if r["p"] < LOW), sum(1 for r in rs if r["p"] > HIGH),
            sum(1 for r in rs if LOW <= r["p"] <= HIGH)))
    if errs:
        A("")
        A("## Errors (not asked successfully; run again to retry)")
        A("")
        for r in errs:
            A("- `%s` —%s→ `%s`: %s" % (r["s"], r["type"], r["t"], r.get("error", "")[:200]))
    lat = sorted(r["latency_ms"] for r in asked if r.get("latency_ms"))
    if lat:
        A("")
        A("Latency median %.0f ms (range %.0f–%.0f) over %d call(s). %s" % (
            lat[len(lat) // 2], lat[0], lat[-1], len(lat), run_note))
    open(md_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return len(asked), total, len(flags), silent, ignored, len(errs), pending


def main(argv):
    a = args(argv)
    import _jev as J
    if a["env"]:
        J.ENV_FILE = os.path.abspath(a["env"])          # load_env() reads the module global at call time
    raw_path = os.path.join(HERE, "%s-raw.jsonl" % a["date"])
    md_path = os.path.join(HERE, "%s-link-check.md" % a["date"])
    where = os.path.relpath(J.ENV_FILE, REPO) if J.ENV_FILE.startswith(REPO) else J.ENV_FILE
    if not a["report"] and not J.available():
        die(3, "JEV LINK CHECK STOPPED — NO CREDENTIAL. TYPESAFE_API_KEY is not set (looked in %s and in the "
               "process environment), or it is the template placeholder. This hand-run check asks TypeSafe's Jev "
               "one question per link and cannot run without a key. Nothing was asked and nothing was written. "
               "Put the key in .env.local at the repo root (gitignored) and run it again." % where)
    E, desc, N = edges_and_describer()
    E = [x for x in E if x["type"] in a["types"]]
    note = ""
    if not a["report"]:
        done = read_raw(raw_path)
        todo = [x for x in E if (x["s"], x["type"], x["t"]) not in done or done[(x["s"], x["type"], x["t"])].get("p") is None]
        if a["max"] is not None:
            todo = todo[:a["max"]]
        q = J.noul(QUESTION[0], true=QUESTION[1], false=QUESTION[2])
        t0, n = time.time(), 0
        with open(raw_path, "a", encoding="utf-8") as fh:
            for x in todo:
                state = {"relation": {"name": x["type"], "meaning": MEAN[x["type"]]},
                         "source": desc(x["s"]), "target": desc(x["t"])}
                row = {"s": x["s"], "type": x["type"], "t": x["t"]}
                try:
                    r = J.ask(state, {"holds": q}, note="s305-D55 link check %s %s %s -> %s" % (a["date"], x["type"], x["s"], x["t"]))
                    ans = r["answers"]["holds"]
                    p = ans.get("noul", ans.get("probability"))
                    row.update(p=p, band=band(p), latency_ms=r["_latency_ms"], request_id=r["_request_id"], model=r.get("model"))
                except J.JevUnavailable as ex:
                    die(3, "JEV LINK CHECK STOPPED — NO CREDENTIAL: %s" % ex)
                except J.JevError as ex:
                    if getattr(ex, "error_type", None) in ("authentication_error", "permission_error") or ex.status in (401, 403):
                        die(4, "JEV LINK CHECK STOPPED — TypeSafe REFUSED THE CREDENTIAL (HTTP %s, %s). "
                               "The key in .env.local is present but not accepted." % (ex.status, getattr(ex, "error_type", None)))
                    row.update(p=None, band="error", error="%s: HTTP %s %s" % (type(ex).__name__, ex.status, getattr(ex, "error_type", "")))
                except Exception as ex:                      # a network fault is an error row, never a crash
                    row.update(p=None, band="error", error="%s: %s" % (type(ex).__name__, str(ex)[:160]))
                row["asked"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                fh.flush()
                n += 1
        note = "This run: %d call(s) in %.0f s." % (n, time.time() - t0)
    asked, total, flags, silent, ignored, errs, pending = report(a, E, N, raw_path, md_path, note)
    print("jev link check %s: %d/%d asked · %d look wrong · %d silent · %d ignored · %d error(s)%s -> %s"
          % (a["date"], asked, total, flags, silent, ignored, errs,
             (" · %d pending (run again)" % pending) if pending else "", os.path.relpath(md_path, REPO)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
