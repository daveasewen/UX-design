#!/usr/bin/env python3
"""R5 / 5c — the deterministic when-evaluator over the metas' `when` predicates, to SPEC-when-evaluator.md.
Probe, not canon. Reads knowledge/ only; writes when-eval-results.json in this lane folder.
Run (seat, system python3): python3 notes/_lanes/304/R5/when_eval.py   [--selftest only runs the unit bites]
"""
import json, os, re, sys, glob, time

LANE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(LANE, "..", "..", "..", ".."))
K = os.path.join(ROOT, "knowledge")
ld = lambda p: json.load(open(p))
REG = ld(os.path.join(K, "when-fields.json"))
FIELDS = sorted(REG["fields"], key=len, reverse=True)
SHAPES = sorted(ld(os.path.join(K, "shapes.json"))["shapes"], key=len, reverse=True)
INTENTS = sorted(ld(os.path.join(K, "chart-intents.json"))["chart-intent"], key=len, reverse=True)
ROLES = ld(os.path.join(K, "roles.json"))["roles"]
OPS = ["spans", "in", "==", "!=", ">=", "<=", "≥", "≤", "=", "<", ">"]
NUM = re.compile(r"^\s*(-?\d+(?:\.\d+)?)")
RANGE = re.compile(r"^\s*(\d+)\s*[–\-]\s*(\d+)")

def norm(v):
    return re.sub(r"\s+", " ", str(v).strip().lower().replace("×", "x")).strip(" .,;:")

def load_metas():
    out = {}
    for f in sorted(glob.glob(os.path.join(K, "components", "*.meta.json"))):
        slug = os.path.basename(f)[:-10]
        if slug.startswith("EXAMPLE"):
            continue
        m = ld(f)
        if m.get("when"):
            out[slug] = m
    return out

# ------------------------------------------------------------------ parse
def split_clauses(gate):
    toks = re.split(r"\s+(AND|OR)\s+", gate.strip())
    return toks[0::2], toks[1::2]

def parse_clause(c):
    s = c.strip()
    for f in FIELDS:
        if not s.startswith(f):
            continue
        rest = s[len(f):]
        if rest and (rest[0].isalnum() or rest[0] in "._-"):
            continue                                 # a longer word that merely starts with the field name
        r = rest.strip()
        for op in OPS:
            if op.isalpha():
                if re.match(r"^%s\b" % op, r):
                    return {"field": f, "op": op, "raw": r[len(op):].strip(), "text": s}
            elif r.startswith(op):
                return {"field": f, "op": op, "raw": r[len(op):].strip(), "text": s}
        if RANGE.match(r):
            return {"field": f, "op": "range", "raw": r, "text": s}
        return {"field": f, "op": None, "raw": r, "text": s, "prose": True}
    return {"field": None, "text": s, "prose": True}

def parse_when(w):
    gate = w.split("—", 1)[0]
    clauses, joins = split_clauses(gate)
    parsed = [parse_clause(c) for c in clauses]
    # `answers spans A AND B`: fold the AND-joined bare addresses into the spans clause
    i = 0
    while i < len(parsed):
        p = parsed[i]
        if p.get("op") == "spans":
            addrs = [head_addr(p["raw"], INTENTS)]
            while i + 1 < len(parsed) and joins[i] == "AND" and head_addr(parsed[i + 1]["text"], INTENTS):
                addrs.append(head_addr(parsed[i + 1]["text"], INTENTS))
                del parsed[i + 1]; del joins[i]
            p["addrs"] = [a for a in addrs if a]
        i += 1
    return {"gate": gate.strip(), "clauses": parsed, "joins": joins}

def head_addr(raw, table):
    r = norm(raw)
    for a in table:
        if r.startswith(norm(a)):
            return a
    return None

# ------------------------------------------------------------------ evaluate (three-valued)
def val_num(x):
    if isinstance(x, (int, float)):
        return float(x)
    if norm(x) in ("none", "zero"):
        return 0.0
    m = NUM.match(str(x))
    return float(m.group(1)) if m else None

def eval_clause(p, ctx):
    if p.get("prose") or not p.get("field"):
        return None
    f, op, raw = p["field"], p["op"], p["raw"]
    if f not in ctx:
        return None
    cv = ctx[f]
    kind = REG["fields"][f].get("kind")
    if op == "spans":
        have = cv if isinstance(cv, list) else [cv]
        return all(a in have for a in p.get("addrs", []))
    if op == "in":
        m = re.match(r"^\(([^)]*)\)", raw)
        opts = [norm(x) for x in (m.group(1).split(",") if m else [raw])]
        return norm(cv) in opts
    if op == "range":
        a, b = map(float, RANGE.match(raw).groups()); x = val_num(cv)
        return None if x is None else a <= x <= b
    if kind == "address":
        target = head_addr(raw, SHAPES if f == "shape" else INTENTS) or raw
        have = cv if isinstance(cv, list) else [cv]
        eq = any(norm(h) == norm(target) for h in have)
        return eq if op in ("=", "==") else (not eq if op == "!=" else None)
    rm = RANGE.match(raw)
    if rm and op in ("=", "=="):
        a, b = map(float, rm.groups()); x = val_num(cv)
        return None if x is None else a <= x <= b
    xn, vn = val_num(cv), val_num(raw)
    if op in (">=", "≥", "<=", "≤", "<", ">") or (xn is not None and vn is not None and kind in ("count", "number")):
        if xn is None or vn is None:
            return None
        return {">=": xn >= vn, "≥": xn >= vn, "<=": xn <= vn, "≤": xn <= vn, "<": xn < vn, ">": xn > vn,
                "=": xn == vn, "==": xn == vn, "!=": xn != vn}[op]
    c, v = norm(cv), norm(raw)
    eq = (c == v) or v.startswith(c + " ") or v.startswith(c + ",")
    if op in ("=", "=="):
        return eq
    if op == "!=":
        return not eq
    return None

def AND(vs):
    return False if any(v is False for v in vs) else (True if all(v is True for v in vs) else None)

def OR(vs):
    return True if any(v is True for v in vs) else (False if all(v is False for v in vs) else None)

def eval_gate(pw, ctx):
    vals = [eval_clause(p, ctx) for p in pw["clauses"]]
    groups, cur = [], [vals[0]] if vals else []
    for j, op in enumerate(pw["joins"]):
        if op == "AND":
            cur.append(vals[j + 1])
        else:
            groups.append(cur); cur = [vals[j + 1]]
    if cur:
        groups.append(cur)
    return OR([AND(g) for g in groups]) if groups else None, vals

def providers(role, metas):
    out = set()
    rr = ROLES.get(role) or {}
    for p in rr.get("providers", []):
        out.add(p.get("slug") if isinstance(p, dict) else p)
    for slug, m in metas.items():
        if m.get("provides") == role:
            out.add(slug)
        for e in ((m.get("edges") or {}).get("providesRole") or []):
            if isinstance(e, dict) and (e.get("ref") or "").split(":", 1)[-1] == role:
                out.add(slug)
    return out

PARSED = {}
def implicit_vals(m, ctx):
    """VARIANT B only: the meta's own `answers` / `shape` fields read as extra AND claims."""
    out = []
    if "shape" in ctx and m.get("shape"):
        out.append(("[meta.shape] " + m["shape"], norm(ctx["shape"]) == norm(m["shape"])))
    if "answers" in ctx and m.get("answers"):
        have = m["answers"] if isinstance(m["answers"], list) else [m["answers"]]
        want = ctx["answers"] if isinstance(ctx["answers"], list) else [ctx["answers"]]
        out.append(("[meta.answers] " + "/".join(have), all(w in have for w in want)))
    return out

def choose(ctx, role=None, metas=None, implicit=False):
    metas = metas or METAS
    pool = sorted(metas) if not role else sorted(s for s in providers(role, metas) if s in metas)
    rows = []
    for slug in pool:
        pw = PARSED.setdefault(slug, parse_when(metas[slug]["when"]))
        res, vals = eval_gate(pw, ctx)
        clauses = [(p["text"][:70], v) for p, v in zip(pw["clauses"], vals)]
        if implicit:
            iv = implicit_vals(metas[slug], ctx)
            clauses += iv
            res = AND([res] + [v for _, v in iv]) if iv else res
            vals = vals + [v for _, v in iv]
        trues = sum(1 for v in vals if v is True)
        rows.append({"slug": slug, "result": res, "trues": trues, "priority": metas[slug].get("priority") or 0,
                     "clauses": clauses})
    elig = [r for r in rows if r["result"] is not False]
    elig.sort(key=lambda r: (-r["trues"], -r["priority"], r["slug"]))
    return {"pick": elig[0]["slug"] if elig else None, "eligible": [(r["slug"], r["trues"], r["priority"]) for r in elig],
            "excluded": [r["slug"] for r in rows if r["result"] is False], "rows": rows}

# ------------------------------------------------------------------ the reader, for comparison
def reader_pick(t):
    sys.path.insert(0, K)
    import _compose_slice as R
    global _G
    try:
        _G
    except NameError:
        _G = R.load_graph(K)
    kw = {"roles": [t["role"]]}
    if t["ctx"].get("answers") and not isinstance(t["ctx"]["answers"], list):
        kw["intent"] = [t["ctx"]["answers"]]
    if t["ctx"].get("shape"):
        kw["shape"] = t["ctx"]["shape"]
    s = R.build_slice(t.get("task"), graph=_G, **kw)
    rows = [c for c in s["components"] if not c.get("alternate") and t["role"] in (c.get("roles") or [])]
    return (rows[0]["id"].split(":", 1)[1] if rows else None), [c["id"].split(":", 1)[1] for c in rows]

# ------------------------------------------------------------------ the test table (expectations written BEFORE the run,
# from each meta's own `when` text and the proposal's worked example; this lane's reading, not a ruling)
TESTS = [
 {"id": "W1", "why": "REQUIRED: treasury cash balance over 30 days (G1's candlestick case), shape stated",
  "task": "treasury cash position trend over the last 30 days", "role": "chart-panel",
  "ctx": {"answers": "change-over-time", "shape": "time-series × 1–5-series", "series": 1, "axes": "present", "span.cols": 8}, "expect": "chart-line"},
 {"id": "W1b", "why": "REQUIRED variant: the same question with only the intent known (no shape, no series)",
  "task": "treasury cash position over time", "role": "chart-panel", "ctx": {"answers": "change-over-time"}, "expect": "chart-line"},
 {"id": "W1c", "why": "positive control: a real OHLC question must still reach the candlestick",
  "task": "FX rate open high low close per day", "role": "chart-panel",
  "ctx": {"answers": "change-over-time", "shape": "periods × ohlc", "span.cols": 8}, "expect": "Chart-candlestick"},
 {"id": "W2", "why": "cash position today with change since yesterday, no series", "role": "headline-metric",
  "task": "cash position today", "ctx": {"answers": "one-number", "shape": "one-measure × value-and-delta", "series": "none", "delta": "present", "span.cols": 3}, "expect": "stat-card"},
 {"id": "W3", "why": "the same figure with a 30-day series to show", "role": "headline-metric",
  "task": "cash position with trend", "ctx": {"shape": "one-measure × value-delta-and-series", "series": 1, "span.cols": 3}, "expect": "kpi-tile"},
 {"id": "W4", "why": "balance vs scheduled payments, verdict with a date", "role": "headline-metric",
  "task": "cash runway", "ctx": {"answers": "one-number", "shape": "one-measure × committed-vs-balance-split", "verdict": "covered until 14 Oct", "span.cols": 4}, "expect": "runway-bar"},
 {"id": "W5", "why": "cut-off in 2 hours, one state", "role": "status-surface",
  "task": "payments cut-off status", "ctx": {"answers": "status-of-one", "shape": "one-state × dot-and-label", "span.cols": 3}, "expect": "status-indicator"},
 {"id": "W6", "why": "balances per account as name/value rows", "role": "status-surface",
  "task": "account balances summary", "ctx": {"answers": "details-before-commit", "shape": "rows × name-value-pairs", "rows": 4, "span.cols": 6}, "expect": "summary"},
 {"id": "W7", "why": "region's queue by stage (operations analyst)", "role": "chart-panel",
  "task": "payments queue by stage", "ctx": {"answers": "comparison", "axis.x": "categorical", "span.cols": 6}, "expect": "chart-bar"},
 {"id": "W8", "why": "balance by currency, total printed in the centre", "role": "chart-panel",
  "task": "balance split by currency", "ctx": {"answers": "composition", "total": "printed", "parts": 4, "span.cols": 6}, "expect": "chart-donut"},
 {"id": "W9", "why": "same split, no total printed", "role": "chart-panel",
  "task": "balance split by currency", "ctx": {"answers": "composition", "total": "not printed", "parts": 4, "span.cols": 6}, "expect": "chart-pie"},
 {"id": "W10", "why": "inflows vs balance, two units, one x", "role": "chart-panel",
  "task": "inflow volume and balance over time", "ctx": {"answers": "change-over-time", "series": 2, "units": "different", "span.cols": 8}, "expect": "chart-combo"},
 {"id": "W11", "why": "the dashboard's frame", "role": "page-frame",
  "task": "treasury dashboard", "ctx": {"destinations": 5, "nav.levels": 1}, "expect": "app-shell-top-nav"},
 {"id": "W12", "why": "where am I, three levels deep", "role": "wayfinding",
  "task": "breadcrumb trail", "ctx": {"shape": "ancestor-path × links", "depth": 3}, "expect": "breadcrumbs"},
 {"id": "W13", "why": "3 payments awaiting approval, each read across its row", "role": "record-list",
  "task": "payments awaiting approval list", "ctx": {"records": 3, "surface": "none"}, "expect": "list-items"},
 {"id": "W14", "why": "page title, app, no lockup", "role": "page-title",
  "task": "page title", "ctx": {"level": "page", "platform": "app", "lockup": "none"}, "expect": "headers"},
 {"id": "W15", "why": "the primary action, a text label", "role": "action",
  "task": "approve button", "ctx": {"emphasis": "primary", "label": "text"}, "expect": "button"},
 {"id": "W16", "why": "arrange the tiles, paint nothing", "role": "arrangement",
  "task": "tile layout", "ctx": {"content": "arbitrary-blocks", "surface": "none"}, "expect": "layout-utilities"},
 {"id": "W17", "why": "global navigation", "role": "wayfinding",
  "task": "main navigation", "ctx": {"shape": "destination-set × links", "scope": "global"}, "expect": "navigations"},
 {"id": "W18", "why": "payments to approve that must be sorted and filtered (data-grid carries no when)", "role": "record-list",
  "task": "sortable filterable payments grid", "ctx": {"records": 40, "surface": "none"}, "expect": "data-grid",
  "expect_note": "EXPECTED MISS: data-grid has no `when`, so no gate can pick it"},
]

def selftest():
    bites = []
    def b(name, got, want):
        bites.append((name, got == want, got, want))
    b("range clause", eval_clause(parse_clause("span.cols 4–6"), {"span.cols": 5}), True)
    b("range clause false", eval_clause(parse_clause("span.cols 4–6"), {"span.cols": 8}), False)
    b("unknown field -> None", eval_clause(parse_clause("series=2 mirrored"), {}), None)
    b("series=2 with trailing prose", eval_clause(parse_clause("series=2 mirrored outward"), {"series": 2}), True)
    b("series != none vs 0", eval_clause(parse_clause("series != none"), {"series": "none"}), False)
    b("in list", eval_clause(parse_clause("emphasis in (primary, secondary)"), {"emphasis": "primary"}), True)
    b("address with trailing words", eval_clause(parse_clause("shape = periods × OHLC (open · high)"), {"shape": "periods × ohlc"}), True)
    b("enum prefix tolerates prose", eval_clause(parse_clause("total=printed as a centre figure"), {"total": "printed"}), True)
    b("enum 'not printed' is not 'printed'", eval_clause(parse_clause("total=not printed"), {"total": "printed"}), False)
    b("prose clause is None", eval_clause(parse_clause("parts sum to a whole"), {"parts": 3}), None)
    b("field-prefix word is not the field", parse_clause("seriesish = 2").get("field"), None)
    pw = parse_when("answers spans change-over-time AND composition AND cumulative bands — x")
    b("spans folds the AND-joined addresses", pw["clauses"][0].get("addrs"), ["change-over-time", "composition"])
    b("3-valued AND", AND([True, None]), None)
    b("3-valued AND false wins", AND([None, False]), False)
    b("3-valued OR", OR([None, True]), True)
    return bites

if __name__ == "__main__":
    METAS = load_metas()
    bites = selftest()
    print("selftest: %d/%d" % (sum(1 for x in bites if x[1]), len(bites)))
    for x in bites:
        if not x[1]:
            print("  BITE MISS", x)
    if "--selftest" in sys.argv:
        sys.exit(0 if all(x[1] for x in bites) else 1)
    # parse coverage over the 39
    cov = {"metas_with_when": len(METAS), "clauses": 0, "field_claims": 0, "prose": 0, "field_without_op": 0, "by_field": {}}
    per = {}
    for slug, m in METAS.items():
        pw = parse_when(m["when"]); PARSED[slug] = pw
        fc = [p for p in pw["clauses"] if p.get("field") and not p.get("prose")]
        cov["clauses"] += len(pw["clauses"]); cov["field_claims"] += len(fc)
        cov["prose"] += sum(1 for p in pw["clauses"] if p.get("prose"))
        cov["field_without_op"] += sum(1 for p in pw["clauses"] if p.get("field") and p.get("prose"))
        for p in fc:
            cov["by_field"][p["field"]] = cov["by_field"].get(p["field"], 0) + 1
        per[slug] = {"field_claims": len(fc), "prose": len(pw["clauses"]) - len(fc)}
    cov["metas_with_zero_field_claims"] = sorted(s for s, v in per.items() if v["field_claims"] == 0)
    print("coverage:", json.dumps({k: v for k, v in cov.items() if k != "by_field"}))
    results = []
    t0 = time.perf_counter()
    for t in TESTS:
        a = time.perf_counter(); r = choose(t["ctx"], t["role"]); ms = (time.perf_counter() - a) * 1000
        rb = choose(t["ctx"], t["role"], implicit=True)
        a = time.perf_counter(); rp, rall = reader_pick(t); rms = (time.perf_counter() - a) * 1000
        row = {"id": t["id"], "why": t["why"], "role": t["role"], "ctx": t["ctx"], "expect": t["expect"],
               "evaluator": r["pick"], "evaluator_ok": r["pick"] == t["expect"], "eligible": r["eligible"][:6],
               "variantB": rb["pick"], "variantB_ok": rb["pick"] == t["expect"], "variantB_eligible": rb["eligible"][:6],
               "excluded": r["excluded"], "reader": rp, "reader_primaries_for_role": rall,
               "agree_with_reader": r["pick"] == rp, "ms": round(ms, 2), "reader_ms": round(rms, 1),
               "note": t.get("expect_note", "")}
        results.append(row)
        print("%-4s exp %-18s A %-18s %s B %-18s %s | reader %-18s %s | reader primaries %s" % (
            t["id"], t["expect"], r["pick"], "OK " if row["evaluator_ok"] else "MISS", rb["pick"], "OK " if row["variantB_ok"] else "MISS", rp, "=" if row["agree_with_reader"] else "!=", rall[:5]))
    summ = {"tests": len(results), "evaluator_matches_expectation": sum(r["evaluator_ok"] for r in results),
            "reader_matches_expectation": sum(r["reader"] == r["expect"] for r in results),
            "evaluator_agrees_with_reader": sum(r["agree_with_reader"] for r in results),
            "variantB_matches_expectation": sum(r["variantB_ok"] for r in results),
            "variantB_agrees_with_reader": sum(r["variantB"] == r["reader"] for r in results),
            "evaluator_ms_median": sorted(r["ms"] for r in results)[len(results) // 2],
            "reader_ms_median": sorted(r["reader_ms"] for r in results)[len(results) // 2]}
    print("summary:", json.dumps(summ))
    json.dump({"$run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "selftest": [(n, ok) for n, ok, *_ in bites],
               "coverage": cov, "per_meta": per, "summary": summ, "results": results,
               "rows_W1": choose(TESTS[0]["ctx"], TESTS[0]["role"])["rows"], "rows_W1b": choose(TESTS[1]["ctx"], TESTS[1]["role"])["rows"]},
              open(os.path.join(LANE, "when-eval-results.json"), "w"), indent=1, ensure_ascii=False)
