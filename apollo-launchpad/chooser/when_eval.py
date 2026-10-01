#!/usr/bin/env python3
"""Launchpad step four (the chooser) — the deterministic when-evaluator.

Grown from the R5 probe's `notes/_lanes/304/R5/when_eval.py` to its six-step spec
(`notes/_lanes/304/R5/SPEC-when-evaluator.md`), with what was ruled since:
  * variant B is the rule (s305-D22): a part's own `answers` and `shape` are claims beside its when-rule;
  * data-grid's `needs` is a registered when-field (s305-D23);
  * chart-line's two clauses are in its meta (s305-D21);
  * the chart role is `chart`, not `chart-panel` (s308-D41).

Three-valued clauses (True / False / None = unknown). A part is out only when its gate is False (open
world: unknown does not exclude). Rank by true claims, then `priority`, then slug.

Same input, same output: no clock, no network, no model, no Jev. Reads knowledge/ and the catalogue only;
writes nothing. Run with PYTHONDONTWRITEBYTECODE=1.
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
K = os.path.join(ROOT, "knowledge")
CATALOGUE = os.path.join(ROOT, "apollo-launchpad", "catalogue", "out", "catalogue-dashboard.json")


def _ld(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


REG = _ld(os.path.join(K, "when-fields.json"))
FIELDS = sorted(REG["fields"], key=len, reverse=True)
SHAPES = sorted(_ld(os.path.join(K, "shapes.json"))["shapes"], key=len, reverse=True)
INTENTS = sorted(_ld(os.path.join(K, "chart-intents.json"))["chart-intent"], key=len, reverse=True)
ROLES = _ld(os.path.join(K, "roles.json"))["roles"]
OPS = ["spans", "in", "==", "!=", ">=", "<=", "≥", "≤", "=", "<", ">"]
NUM = re.compile(r"^\s*(-?\d+(?:\.\d+)?)")
RANGE = re.compile(r"^\s*(\d+)\s*[–\-]\s*(\d+)")


def norm(v):
    return re.sub(r"\s+", " ", str(v).strip().lower().replace("×", "x")).strip(" .,;:")


# ------------------------------------------------------------------ the parts, from either source
def _part(m, slug):
    return {"slug": slug, "when": m.get("when"), "answers": m.get("answers"), "shape": m.get("shape"),
            "priority": m.get("priority") or 0, "provides": m.get("provides"), "edges": m.get("edges") or {}}


def parts_from_metas():
    """Every real meta that carries a `when` (the W table's pool, as R5 had it)."""
    out = {}
    for f in sorted(glob.glob(os.path.join(K, "components", "*.meta.json"))):
        slug = os.path.basename(f)[:-len(".meta.json")]
        if slug.startswith("EXAMPLE"):
            continue
        m = _ld(f)
        if m.get("when"):
            out[slug] = _part(m, slug)
    return out


def load_catalogue(path=CATALOGUE):
    return _ld(path)


def parts_from_catalogue(cat):
    """The published parts, read from the catalogue (the API), keyed by slug. The when-rule is the entry's
    gate half; `answers`, `shape`, `priority`, `provides` are the entry's x-apollo copies of the meta."""
    out = {}
    for name, e in sorted(cat["components"].items()):
        xa = e.get("x-apollo") or {}
        slug = xa.get("slug")
        if not slug:
            continue
        w = (xa.get("when") or {}).get("gate")
        out[slug] = {"slug": slug, "component": name, "when": w, "answers": xa.get("answers"),
                     "shape": xa.get("shape"), "priority": xa.get("priority") or 0,
                     "provides": xa.get("provides"), "proposal": bool(xa.get("proposal")),
                     "aliases": xa.get("aliases") or [], "settings": xa.get("settings") or [],
                     "slots": xa.get("slots") or {}, "edges": {}}
    return out


def alias_readings():
    """aliasOf readings from the alias metas (stat-card 'without trend', kpi-tile 'with trend')."""
    out = {}
    for f in sorted(glob.glob(os.path.join(K, "components", "*.meta.json"))):
        m = _ld(f)
        a = m.get("aliasOf")
        if isinstance(a, dict) and a.get("component"):
            out[os.path.basename(f)[:-len(".meta.json")]] = {
                "owner": a["component"].split(":", 1)[-1], "reading": a.get("reading")}
    return out


# ------------------------------------------------------------------ parse
def split_clauses(gate):
    toks = re.split(r"\s+(AND|OR)\s+", gate.strip())
    return toks[0::2], toks[1::2]


def head_addr(raw, table):
    r = norm(raw)
    for a in table:
        if r.startswith(norm(a)):
            return a
    return None


def parse_clause(c):
    s = c.strip()
    for f in FIELDS:
        if not s.startswith(f):
            continue
        rest = s[len(f):]
        if rest and (rest[0].isalnum() or rest[0] in "._-"):
            continue  # a longer word that merely starts with the field name
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
    i = 0
    while i < len(parsed):  # `answers spans A AND B`: fold the AND-joined bare addresses into the spans clause
        p = parsed[i]
        if p.get("op") == "spans":
            addrs = [head_addr(p["raw"], INTENTS)]
            while i + 1 < len(parsed) and joins[i] == "AND" and head_addr(parsed[i + 1]["text"], INTENTS):
                addrs.append(head_addr(parsed[i + 1]["text"], INTENTS))
                del parsed[i + 1]
                del joins[i]
            p["addrs"] = [a for a in addrs if a]
        i += 1
    return {"gate": gate.strip(), "clauses": parsed, "joins": joins}


# ------------------------------------------------------------------ evaluate (three-valued)
def val_num(x):
    if isinstance(x, (int, float)) and not isinstance(x, bool):
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
        have = cv if isinstance(cv, list) else [cv]
        return any(norm(h) in opts for h in have)
    if op == "range":
        a, b = map(float, RANGE.match(raw).groups())
        x = val_num(cv)
        return None if x is None else a <= x <= b
    if kind == "address":
        target = head_addr(raw, SHAPES if f == "shape" else INTENTS) or raw
        have = cv if isinstance(cv, list) else [cv]
        eq = any(norm(h) == norm(target) for h in have)
        return eq if op in ("=", "==") else (not eq if op == "!=" else None)
    rm = RANGE.match(raw)
    if rm and op in ("=", "=="):
        a, b = map(float, rm.groups())
        x = val_num(cv)
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
    groups, cur = [], ([vals[0]] if vals else [])
    for j, op in enumerate(pw["joins"]):
        if op == "AND":
            cur.append(vals[j + 1])
        else:
            groups.append(cur)
            cur = [vals[j + 1]]
    if cur:
        groups.append(cur)
    return (OR([AND(g) for g in groups]) if groups else None), vals


def implicit_vals(part, ctx):
    """Variant B (s305-D22): the part's own `answers` / `shape` read as extra AND claims."""
    out = []
    if "shape" in ctx and part.get("shape"):
        out.append(("shape = " + part["shape"] + " [the part's own shape]", norm(ctx["shape"]) == norm(part["shape"])))
    if "answers" in ctx and part.get("answers"):
        have = part["answers"] if isinstance(part["answers"], list) else [part["answers"]]
        want = ctx["answers"] if isinstance(ctx["answers"], list) else [ctx["answers"]]
        out.append(("answers = " + "/".join(have) + " [the part's own question]", all(w in have for w in want)))
    return out


def providers(role, parts):
    """Parts that provide a roles.json slug: the role's providers list, `provides`, or a providesRole edge."""
    out = set()
    rr = ROLES.get(role) or {}
    for p in rr.get("providers", []):
        out.add(p.get("slug") if isinstance(p, dict) else p)
    for slug, m in parts.items():
        if m.get("provides") == role:
            out.add(slug)
        for e in ((m.get("edges") or {}).get("providesRole") or []):
            if isinstance(e, dict) and (e.get("ref") or "").split(":", 1)[-1] == role:
                out.add(slug)
    return {s for s in out if s in parts}


_PARSED = {}


def evaluate(ctx, parts, pool=None, implicit=True):
    """Every candidate in `pool` (default: all `parts` with a when-rule), evaluated against `ctx`.
    Returns {pick, eligible: [row…] in rank order, excluded: [row…]}; each row carries its clause verdicts."""
    pool = sorted(pool if pool is not None else parts)
    rows = []
    for slug in pool:
        part = parts[slug]
        if not part.get("when"):
            rows.append({"slug": slug, "result": False, "trues": 0, "priority": part.get("priority") or 0,
                         "clauses": [], "reasons": [], "why": "no when-rule, so no gate can pick it"})
            continue
        key = (slug, part["when"])
        pw = _PARSED.get(key)
        if pw is None:
            pw = _PARSED[key] = parse_when(part["when"])
        res, vals = eval_gate(pw, ctx)
        clauses = [(p["text"], v) for p, v in zip(pw["clauses"], vals)]
        if implicit:
            iv = implicit_vals(part, ctx)
            clauses += iv
            if iv:
                res = AND([res] + [v for _, v in iv])
        trues = sum(1 for _, v in clauses if v is True)
        row = {"slug": slug, "result": res, "trues": trues, "priority": part.get("priority") or 0,
               "clauses": clauses, "reasons": [t for t, v in clauses if v is True]}
        if res is False:
            row["why"] = "gate false: " + "; ".join(t for t, v in clauses if v is False)
        rows.append(row)
    elig = [r for r in rows if r["result"] is not False]
    elig.sort(key=lambda r: (-r["trues"], -r["priority"], r["slug"]))
    return {"pick": elig[0]["slug"] if elig else None, "eligible": elig,
            "excluded": [r for r in rows if r["result"] is False]}
