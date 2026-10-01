#!/usr/bin/env python3
"""_validate_token_routers.py — do the THREE token routers send every namespace to the same store?
ADVISORY. Built #313 lane A5 under s307-D43 (W-307qk, the third of the three names the #219 segmented
report left: "a shared token router").

THE CLASS (#219 lane 1, finding 3): three hand-kept copies of one routing table decide which store a
token path is read from —
  canon/gen_theme_cascade.py::_store_for   (the canon theme cascade; base_value walks it)
  gen_snippet_tokens.py::resolve           (the snippet/canon literal projector)
  _validate_snippets.py::resolve           (the snippet gate)
Twice the copies disagreed and a well-minted token read as missing (`size/`, `padding/`, `alpha/`:
the ds-018 silent-lookup class, s121-D1). Nothing compared them.

THE SETTLEMENT (#313 A5, s307-D43 handed it to Claude): ONE table, ROUTES below, is the record of
which store owns which namespace; the three routers stay where they are tonight (two of them sit on
the canon write path that other lanes regenerate through) and this check DRIVES each of them on one
real token per namespace and says where they disagree with the table. A disagreement is a router
that would read a minted token as missing. Moving the three onto ROUTES is the follow-up; this file
is what will prove that move changed nothing.

HOW IT MEASURES (driven, not read): for every ROUTES row it finds a real leaf in the owning store,
walks it directly for the expected value, then asks each router for the same path in light mode.
AGREE = the router returns the same value (numbers compared as numbers, so '44px' == 44).
The gate's `resolve` cannot be imported (the module runs its gate at import), so its function is
compiled out of its own source with the stores it reads — the same function text, not a copy.

  python3 knowledge/_validate_token_routers.py             # the table, exit 0 (ADVISORY)
  python3 knowledge/_validate_token_routers.py --strict    # exit 1 on any disagreement
  python3 knowledge/_validate_token_routers.py --selftest  # control + planted mis-route, both directions
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import ast
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.join(ROOT, "tokens")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "canon"))
from _dtcg_load import load_legacy  # noqa: E402  the same read-site seam all three routers use
from _dtcg_units import px_number   # noqa: E402

# THE ONE TABLE. (namespace prefixes, store file relative to knowledge/tokens/). Order matters only
# in that the first matching row wins, as in every router; the last row is the fallback.
ROUTES = [
    (("color/",), "colour.json"),
    (("border-radius/", "border-width/", "breakpoint/", "layout/", "focus-ring/", "target/", "size/"),
     "layout.json"),
    (("padding/", "gap/"), "spacing.json"),
    (("motion/",), "motion.json"),
    (("component-type/",), "../component-types.json"),
    (("alpha/",), "opacity.json"),
    ((), "semantic-colour.json"),          # everything else
]


def store_for(path):
    for prefixes, store in ROUTES:
        if not prefixes or path.startswith(prefixes):
            return store
    raise AssertionError("ROUTES has no fallback row")


_STORES = {}


def _store(name):
    if name not in _STORES:
        p = os.path.join(TOK, name)
        _STORES[name] = (json.load(open(p, encoding="utf-8")) if name.startswith("..")
                         else load_legacy(p))
    return _STORES[name]


def _leaf_value(node, mode="light"):
    if isinstance(node, dict):
        if mode in node and isinstance(node[mode], dict) and "$value" in node[mode]:
            return node[mode]["$value"]
        if "$value" in node:
            return node["$value"]
    return None


def first_leaf(store, root_key):
    """-> (path, value) of the first real leaf under store[root_key], or None. Walks in file order."""
    def walk(node, path):
        v = _leaf_value(node)
        if v is not None and not isinstance(v, (dict, list)):
            return path, v
        if isinstance(node, dict):
            for k, child in node.items():
                if k.startswith("$") or k in ("light", "dark"):
                    continue
                got = walk(child, path + "/" + k)
                if got:
                    return got
        return None
    if root_key not in store:
        return None
    return walk(store[root_key], root_key)


def probes():
    """-> [(path, store, expected)] — one real token per prefix, found in the store ROUTES names."""
    out = []
    for prefixes, store in ROUTES:
        roots = [p.rstrip("/") for p in prefixes] or ["text"]
        for root in roots:
            got = first_leaf(_store(store), root)
            if got:
                out.append((got[0], store, got[1]))
    return out


def norm(v):
    if v is None:
        return None
    try:
        n = px_number(v)
        if isinstance(n, (int, float)):
            return float(n)
    except Exception:
        pass
    s = str(v).strip()
    try:
        return float(s)
    except ValueError:
        return s.upper()


# ------------------------------------------------------------------ the three routers, driven
def router_cascade():
    import gen_theme_cascade as c
    return lambda path, mode: c.base_value(path, mode)


def router_projector():
    import gen_snippet_tokens as g
    return lambda path, mode: g.resolve(path, mode)


def router_gate():
    """The snippet gate's own `resolve`, compiled from its source with the stores it reads."""
    src_path = os.path.join(ROOT, "_validate_snippets.py")
    tree = ast.parse(open(src_path, encoding="utf-8").read(), src_path)
    fn = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "resolve"]
    if len(fn) != 1:
        raise RuntimeError("_validate_snippets.py: expected exactly one top-level resolve(), found %d" % len(fn))
    env = {"px_number": px_number,
           "sem": _store("semantic-colour.json"), "layout": _store("layout.json"),
           "spacing": _store("spacing.json"), "motion_store": _store("motion.json"),
           "opacity_store": _store("opacity.json"), "ctypes_store": _store("../component-types.json")}
    exec(compile(ast.Module(body=fn, type_ignores=[]), src_path, "exec"), env)
    return env["resolve"]


ROUTERS = [("cascade  canon/gen_theme_cascade.py", router_cascade),
           ("projector gen_snippet_tokens.py", router_projector),
           ("gate     _validate_snippets.py", router_gate)]


def ask(fn, path):
    try:
        return norm(fn(path, "light")), ""
    except Exception as exc:              # a mis-route surfaces as KeyError / TypeError
        return None, "%s: %s" % (type(exc).__name__, str(exc)[:60])


def run(routers=None, quiet=False):
    routers = routers or [(n, f()) for n, f in ROUTERS]
    rows, bad = [], []
    for path, store, expected in probes():
        want = norm(expected)
        cells = []
        for name, fn in routers:
            got, err = ask(fn, path)
            ok = got == want
            cells.append((name, ok, got, err))
            if not ok:
                bad.append((path, store, name, want, got, err))
        rows.append((path, store, want, cells))
    if not quiet:
        print("token routers vs the one table (ROUTES) — %d namespace probe(s) x %d router(s), light mode"
              % (len(rows), len(routers)))
        for path, store, want, cells in rows:
            marks = " ".join("%s" % ("ok " if ok else "XX ") for _n, ok, _g, _e in cells)
            print("  %-46s -> %-26s %s" % (path, store, marks))
        print("  columns: " + " · ".join(n.split()[0] for n, _ in routers))
        for path, store, name, want, got, err in bad:
            print("  ⚠ %s reads %s as %r (the table's store %s holds %r)%s"
                  % (name.split()[0], path, got, store, want, ("  — " + err) if err else ""))
        print("%s — %d disagreement(s). ADVISORY (W-307qk): a disagreement is a router that would read a "
              "minted token as missing." % ("AGREE" if not bad else "DISAGREE", len(bad)))
    return rows, bad


def _selftest():
    ok, n = True, [0]

    def bite(label, good, detail=""):
        nonlocal ok
        n[0] += 1
        print("  [%d] %-66s %s%s" % (n[0], label, "PASS" if good else "FAIL", ("  — " + detail) if detail else ""))
        ok = ok and good

    pr = probes()
    roots = {p.split("/")[0] for p, _s, _v in pr}
    bite("every ROUTES row finds a real token to probe", {"color", "size", "padding", "alpha", "motion",
         "component-type", "text"} <= roots, ",".join(sorted(roots)))

    def table_router(path, mode):          # CONTROL: a router that IS the table must agree everywhere
        node = _store(store_for(path))
        for k in path.split("/"):
            node = node[k]
        return _leaf_value(node, mode)
    _rows, bad = run([("control", table_router)], quiet=True)
    bite("control: a router built from ROUTES agrees on every probe", not bad, "%d disagreement(s)" % len(bad))

    def misroute(path, mode):              # MUTANT: forget size/ (the #219 defect, re-planted)
        if path.startswith("size/"):
            node = _store("semantic-colour.json")
            for k in path.split("/"):
                node = node[k]
            return _leaf_value(node, mode)
        return table_router(path, mode)
    _rows, bad = run([("mutant", misroute)], quiet=True)
    bite("mutant: a router that forgets size/ is named on the size/ probe, and only there",
         bool(bad) and all(b[0].startswith("size/") for b in bad), ",".join(b[0] for b in bad))

    gate = router_gate()
    bite("the gate's resolve compiles from its own source and answers a probe",
         ask(gate, "border-radius/" + first_leaf(_store("layout.json"), "border-radius")[0].split("/", 1)[1])[0]
         is not None)
    print("\n%s (%d bites)" % ("✅ selftest PASS" if ok else "❌ selftest FAIL", n[0]))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    _rows, _bad = run()
    sys.exit(1 if (_bad and "--strict" in sys.argv) else 0)
