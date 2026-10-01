#!/usr/bin/env python3
"""Launchpad step three — the gates as a service: one screen IN MEMORY in, one verdict out.
(#313 lane C3, grown from the #304 R5 probe notes/_lanes/304/R5/gate_mem.py, to the build spec
notes/_lanes/312/C/SPEC-launchpad-day-one.md § 7.)

  Gate(catalogue_path=None)            warm-up: reads the catalogue, the two A2UI spec files and the
                                       reference snippets the catalogue names, ONCE
  .gate_surface(messages, splice=False) the surface layer S1–S9 on A2UI v0.9.1 messages; with
                                       splice=True the page layer also runs on the stand-in page
  .gate_page(html)                     the page layer P0–P4 on a page string
  .splice(messages)                    the stand-in page (NOT a renderer: step two is emitter E1, s311-D9)

The verdict object (spec § 7):
  {"verdict": "pass"|"fail",
   "checks": [{"id", "name", "result": "pass"|"fail"|"unmeasured"|"n/a", "reasons": [...]}],
   "timing_ms": {"surface", "page", "total"},
   "catalogue": {"id", "version", "sha256"}}
Only a "fail" fails the verdict; "unmeasured" is said, never rounded to a pass or a fail.

Surface layer (A2UI messages against OUR catalogue):
  S1 each message valid against server_to_client.json with catalog.json resolved to ours
  S2 each part valid against its own entry (readable reasons; A2UI's anyComponent is a oneOf)
  S3 one root (an id "root")          S4 ids unique          S5 every child reference resolves
  S6 a slot's children provide what the slot's x-apollo.accepts asks (the check A2UI cannot make):
     `provides` against the child's provides role, `tier` against the child's level — decisive;
     `capability` "anything" passes; a capability equal to the child's slug passes (by name); any
     other capability is UNMEASURED: no registry says which parts offer which capability
  S7 no deprecated part (x-apollo.status)
  S8 a `state` value inside the entry's x-apollo.states list, where the entry carries one
  S9 a data setting's value fits its data shape's arity (a `time-series × 1–5-series` with six
     series fails); a binding is resolved through the surface's own updateDataModel messages
Page layer (the static checks of knowledge/_validate_screen.py, called on the string):
  P0 provenance receipt (_validate_screen.gate_receipt, non-strict: NO-RECEIPT is UNMEASURED)
  P1 a11y — the in-memory twin of _validate_a11y.check(): the module's own motion_fails() (per
     part, s305-D54), its own analyse()/unknown_roles() engine and its own tiers, read at call time
  P2 composition (_validate_screen.gate_composition: C9 blocks; C1/C7/C8/C4 advisory)
  P3 icon source (_validate_screen.gate_icons on the markup; the icon library is read once, at warm-up)
  P4 compose (_validate_screen.gate_compose)
P0 and P4 take a PATH today, so gate_page writes the page ONCE to /dev/shm (or $TMPDIR), reads it
through those two, and removes it — the one declared write (spec § 7; the split that would end it
is a check_text() in each, named in the report). The render leg (state-contrast, geometry, own size)
is not run here (the brief defers it).

Needs jsonschema >= 4.18 with `referencing` (apollo-launchpad/requirements.txt) for the surface
layer; the page layer is the repo's own stdlib modules. Run with PYTHONDONTWRITEBYTECODE=1.
"""
import copy, functools, json, os, re, sys, tempfile, time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
LP = os.path.dirname(HERE)
ROOT = os.path.dirname(LP)
K = os.path.join(ROOT, "knowledge")
SNIPDIR = os.path.join(K, "snippets")
SPEC = os.path.join(LP, "catalogue", "a2ui-v0.9.1")
CATALOGUE = os.path.join(LP, "catalogue", "out", "catalogue-dashboard.json")
CATALOG_URI = "https://a2ui.org/specification/v0_9/catalog.json"   # what server_to_client's "catalog.json" resolves to
if K not in sys.path:
    sys.path.insert(0, K)

import _validate_a11y as A11Y                 # noqa: E402 - the disk a11y gate: its functions and tiers
import _validate_screen as SCREEN             # noqa: E402 - the composed-screen gate: its string steps
from _a11y_target import analyse, unknown_roles   # noqa: E402 - the engine both share

CHECK_NAMES = {
    "S1": "message valid against A2UI v0.9.1 with our catalogue",
    "S2": "each part valid against its own entry",
    "S3": "one root",
    "S4": "ids unique",
    "S5": "child references resolve",
    "S6": "slot children provide what the slot accepts",
    "S7": "no deprecated part",
    "S8": "state inside the part's states",
    "S9": "data fits its shape's arity",
    "P0": "provenance receipt",
    "P1": "accessibility (2.3.3 per part, 2.5.8, ARIA vocabulary)",
    "P2": "composition (C9 span legality)",
    "P3": "icon source",
    "P4": "compose (canon classes, no hex, link not paste, page never sizes a part)",
}


# ------------------------------------------------------------------ P1: the in-memory a11y twin
def a11y_text(s, name="<memory>"):
    """_validate_a11y.check(fp) with the string in place of open(fp).read(). Every clause is the disk
    module's own function or tier, read at call time, so a ruled change there changes this too; the
    body below is the disk check's loop, line for line (T3.1 holds them equal on every snippet)."""
    fails, warns, notes = [], [], []
    fails.extend(A11Y.motion_fails(s))
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
            (fails if A11Y.CONTROL_TIER_44 == "fail" else warns).append("%s — %s" % (who, r.detail))
        elif r.verdict == "unmeasured":
            notes.append("%s — UNMEASURED: %s" % (who, r.detail))
        elif r.verdict == "exception":
            notes.append("%s — %s" % (who, r.detail))
    for r in marks:
        who = "`%s`" % r.el.descr()
        if r.verdict == "under":
            (fails if A11Y.MARK_TIER == "fail" else warns).append(
                "DATA MARK %s — %s (s116-D1: marks carry the 24 floor, not the 44 target)" % (who, r.detail))
        elif r.verdict == "unmeasured":
            notes.append("DATA MARK %s — UNMEASURED: %s" % (who, r.detail))
    return name, fails, warns, notes, controls, marks


def a11y_signature(row):
    """What T3.1 compares between the disk gate and the twin: fails, warns, notes, every verdict."""
    _n, f, w, no, c, m = row
    return (f, w, no, [(r.el.descr(), r.verdict, r.detail) for r in c],
            [(r.el.descr(), r.verdict, r.detail) for r in m])


# ------------------------------------------------------------------ S9: a shape's arity, from its name
SERIES_RANGE = re.compile(r"(\d+)\s*[–-]\s*(\d+)-series")

def shape_arity(shape):
    """(lo, hi) series a shape admits, read off the shape's own name in knowledge/shapes.json's grammar
    (`<x-dimension> × <mark>`): `1–5-series` -> (1, 5), `single-series…` -> (1, 1), `two-series…` -> (2, 2).
    None when the name states no series count (the shape is then not arity-checked: S9 says n/a)."""
    if not shape:
        return None
    m = SERIES_RANGE.search(shape)
    if m:
        return int(m.group(1)), int(m.group(2))
    if "single-series" in shape:
        return 1, 1
    if "two-series" in shape:
        return 2, 2
    return None


def series_count(v):
    """How many series a literal data value carries, or None when its form says nothing countable.
    [C3's reading, no ruling] a number is the count itself (ChartLine's `series` is a DynamicNumber);
    an object's `series` list is counted; a list of objects each carrying `values` or `points` is
    counted, one series per object."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, dict) and isinstance(v.get("series"), list):
        return len(v["series"])
    if isinstance(v, list) and v and all(isinstance(x, dict) and ("values" in x or "points" in x) for x in v):
        return len(v)
    return None


def pointer_get(doc, path):
    """JSON-pointer lookup in the surface's data model; (found, value)."""
    if path in ("", "/"):
        return True, doc
    cur = doc
    for tok in path.lstrip("/").split("/"):
        tok = tok.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, dict) and tok in cur:
            cur = cur[tok]
        elif isinstance(cur, list) and tok.isdigit() and int(tok) < len(cur):
            cur = cur[int(tok)]
        else:
            return False, None
    return True, cur


def pointer_set(doc, path, value):
    if path in (None, "", "/"):
        return value if isinstance(value, dict) else {"": value}
    cur = doc
    toks = [t.replace("~1", "/").replace("~0", "~") for t in path.lstrip("/").split("/")]
    for t in toks[:-1]:
        cur = cur.setdefault(t, {}) if isinstance(cur, dict) else cur
    if isinstance(cur, dict):
        cur[toks[-1]] = value
    return doc


AUTO_BEHAVIOUR_BLOCK = re.compile(
    r"<!--\s*=====\s*AUTO-BEHAVIOUR\s+(\S+)\s+START[^>]*=====\s*-->.*?"
    r"<!--\s*=====\s*AUTO-BEHAVIOUR\s+\1\s+END\s*=====\s*-->", re.S)


# ------------------------------------------------------------------ the gate
class Gate:
    def __init__(self, catalogue=None):
        """Warm-up: every file the gate will ever read on the surface layer is read here."""
        t = time.perf_counter()
        if isinstance(catalogue, dict):
            self.cat = catalogue
        else:
            self.cat = json.load(open(catalogue or CATALOGUE, encoding="utf-8"))
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012
        ld = lambda p: json.load(open(os.path.join(SPEC, p), encoding="utf-8"))
        ct, s2c = ld("json_common_types.json"), ld("json_server_to_client.json")
        res = lambda d: Resource.from_contents(d, default_specification=DRAFT202012)
        self.registry = Registry().with_resources(
            [(ct["$id"], res(ct)), (s2c["$id"], res(s2c)), (CATALOG_URI, res(self.cat))])
        self.V = Draft202012Validator({"$ref": s2c["$id"]}, registry=self.registry)
        self._DV = Draft202012Validator
        self._pv = {}
        meta = (self.cat.get("x-apollo") or {}).get("catalogue") or {}
        self.cat_id = {"id": self.cat.get("catalogId"), "version": meta.get("version"), "sha256": meta.get("sha256")}
        # the reference snippets the catalogue names, read once (the stand-in splice reads them from memory)
        self.snippets = {}
        for name, e in self.cat["components"].items():
            sn = ((e.get("x-apollo") or {}).get("snippet") or "").split(":", 1)[-1]
            p = os.path.join(SNIPDIR, sn)
            if sn and os.path.exists(p):
                self.snippets[name] = (sn, open(p, encoding="utf-8").read())
        # the icon library: _validate_screen.gate_icons rebuilds it from ~700 files on every call; the
        # service reads it once and keeps it (a process-local memo of the module's own builder)
        icons = SCREEN.icons
        if not getattr(icons.build_library, "_launchpad_memo", False):
            memo = functools.lru_cache(maxsize=1)(icons.build_library)
            memo._launchpad_memo = True
            icons.build_library = memo
        icons.build_library()
        # the compose gate memoises the canon class scopes and the parts' inline API at module level on
        # its first call (~7.7 s cold in the cloud clone); build them here so no screen pays for it
        import importlib
        comp = importlib.import_module("_validate_compose")
        comp._canon_class_scopes(); comp._part_inline_api()
        self.warm_ms = round((time.perf_counter() - t) * 1000, 2)

    # -------------------------------------------------------------- helpers
    def entry(self, name):
        return self.cat["components"].get(name)

    def props(self, name):
        e = self.entry(name) or {}
        return ((e.get("allOf") or [{}])[-1]).get("properties", {})

    def xa(self, name):
        return (self.entry(name) or {}).get("x-apollo") or {}

    def part_validator(self, name):
        if name not in self._pv:
            self._pv[name] = self._DV({"$ref": CATALOG_URI + "#/components/" + name}, registry=self.registry)
        return self._pv[name]

    @staticmethod
    def components_of(messages):
        comps = []
        for m in messages or []:
            comps += ((m or {}).get("updateComponents") or {}).get("components") or []
        return comps

    @staticmethod
    def data_model_of(messages):
        dm = {}
        for m in messages or []:
            u = (m or {}).get("updateDataModel")
            if isinstance(u, dict) and "value" in u:
                dm = pointer_set(dm, u.get("path"), copy.deepcopy(u["value"]))
        return dm

    def slot_children(self, c):
        """[(slot name, accepts, [child ids])] for one component, from its entry's slot properties."""
        out = []
        for k, sch in self.props(c.get("component")).items():
            xs = sch.get("x-apollo") or {}
            if not xs.get("slot") or k not in c:
                continue
            v = c[k]
            ids = [v] if isinstance(v, str) else (v if isinstance(v, list) else
                  ([v["componentId"]] if isinstance(v, dict) and isinstance(v.get("componentId"), str) else []))
            out.append((k, xs.get("accepts") or {}, [i for i in ids if isinstance(i, str)]))
        return out

    # -------------------------------------------------------------- the surface layer
    def surface_checks(self, messages):
        R = {k: [] for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9")}
        U = {k: [] for k in R}          # unmeasured reasons
        NA = set()
        for i, msg in enumerate(messages or []):
            for e in self.V.iter_errors(msg):
                R["S1"].append("message %d at %s: %s" % (i, "/".join(map(str, e.absolute_path)) or "(root)", e.message[:160]))
        comps = self.components_of(messages)
        if not comps:
            R["S1"].append("no updateComponents message carries a component")
        for c in comps:
            name = c.get("component")
            if self.entry(name) is None:
                R["S2"].append("%s: part %r is not in catalogue %s" % (c.get("id"), name, self.cat_id["version"]))
                continue
            for e in self.part_validator(name).iter_errors(c):
                R["S2"].append("%s (%s) at %s: %s" % (c.get("id"), name, "/".join(map(str, e.absolute_path)) or "(root)", e.message[:160]))
        ids = [c.get("id") for c in comps]
        if "root" not in ids:
            R["S3"].append("no component has the id 'root'")
        dup = sorted({str(i) for i in ids if ids.count(i) > 1})
        if dup:
            R["S4"].append("duplicate ids: %s" % ", ".join(dup))
        byid = {c.get("id"): c for c in comps}
        dm = self.data_model_of(messages)
        slot_seen = False
        for c in comps:
            name = c.get("component")
            if self.entry(name) is None:
                continue
            for slot, accepts, kids in self.slot_children(c):
                slot_seen = True
                for kid in kids:
                    if kid not in byid:
                        R["S5"].append("%s.%s -> %r does not resolve to any component on the surface" % (c.get("id"), slot, kid))
                        continue
                    kc = byid[kid]; kname = kc.get("component"); kx = self.xa(kname)
                    if self.entry(kname) is None:
                        continue                                  # S2 has said so
                    where = "%s.%s -> %s (%s)" % (c.get("id"), slot, kid, kx.get("slug") or kname)
                    if accepts.get("provides"):
                        if kx.get("provides") not in accepts["provides"]:
                            R["S6"].append("%s provides %r; the slot accepts only %s" % (
                                where, kx.get("provides"), " / ".join(accepts["provides"])))
                    if accepts.get("tier"):
                        if kx.get("level") not in accepts["tier"]:
                            R["S6"].append("%s is tier %r; the slot accepts tier %s" % (
                                where, kx.get("level"), " / ".join(accepts["tier"])))
                    cap = accepts.get("capability") or []
                    if cap and "anything" not in cap and kx.get("slug") not in cap:
                        U["S6"].append("%s: the slot asks for capability %s and no registry says which parts "
                                       "offer it" % (where, " / ".join(cap)))
            # S5 — a reference held by a non-slot ComponentId/ChildList property (none in this catalogue
            # today, but A2UI allows it) resolves too
            for k, sch in self.props(name).items():
                if (sch.get("x-apollo") or {}).get("slot") or k not in c:
                    continue
                ref = sch.get("$ref", "")
                v = c[k]
                refs = [v] if ref.endswith("ComponentId") and isinstance(v, str) else \
                       (v if ref.endswith("ChildList") and isinstance(v, list) else [])
                for r in refs:
                    if r not in byid:
                        R["S5"].append("%s.%s -> %r does not resolve" % (c.get("id"), k, r))
            x = self.xa(name)
            if x.get("status") == "deprecated":
                R["S7"].append("%s uses the deprecated part %s" % (c.get("id"), x.get("slug") or name))
            states = (x.get("states") or {}).get("states") if isinstance(x.get("states"), dict) else None
            if isinstance(states, list) and "state" in c:
                if isinstance(c["state"], str) and c["state"] not in states:
                    R["S8"].append("%s (%s) state %r is not one of the part's states %s" % (
                        c.get("id"), x.get("slug") or name, c["state"], ", ".join(states)))
            for k, sch in self.props(name).items():
                xs = sch.get("x-apollo") or {}
                if not xs.get("data") or k not in c:
                    continue
                ar = shape_arity(xs.get("shape"))
                if ar is None:
                    continue
                v = c[k]
                if isinstance(v, dict) and set(v) == {"path"}:
                    found, v = pointer_get(dm, v["path"])
                    if not found:
                        U["S9"].append("%s.%s is bound to %s, which no updateDataModel on this surface sets" % (
                            c.get("id"), k, c[k]["path"]))
                        continue
                n = series_count(v)
                if n is None:
                    U["S9"].append("%s.%s: the value's form says no series count" % (c.get("id"), k))
                elif not (ar[0] <= n <= ar[1]):
                    R["S9"].append("%s (%s).%s carries %d series; its shape %s admits %d–%d" % (
                        c.get("id"), x.get("slug") or name, k, n, xs.get("shape"), ar[0], ar[1]))
        if not slot_seen:
            NA.add("S6")
        if not any("state" in c for c in comps):
            NA.add("S8")
        out = []
        for k in R:
            res = "fail" if R[k] else ("unmeasured" if U[k] else ("n/a" if k in NA else "pass"))
            out.append({"id": k, "name": CHECK_NAMES[k], "result": res, "reasons": R[k] + U[k]})
        return out

    # -------------------------------------------------------------- the page layer
    def page_checks(self, html):
        out = []
        # P1 — in memory
        _n, af, aw, an, _c, _m = a11y_text(html, "page")
        out.append({"id": "P1", "name": CHECK_NAMES["P1"], "result": "fail" if af else "pass",
                    "reasons": af + ["warn: " + w for w in aw]})
        # P2 — in memory
        cl, blocking = SCREEN.gate_composition(html)
        res = "fail" if blocking else ("n/a" if any("composition: n/a" in l for l in cl) else
                                       ("unmeasured" if any("UNPROVEN" in l for l in cl) else "pass"))
        out.append({"id": "P2", "name": CHECK_NAMES["P2"], "result": res, "reasons": [l.strip() for l in cl]})
        # P3 — in memory (the library memoised at warm-up)
        icf = SCREEN.gate_icons(html)
        out.append({"id": "P3", "name": CHECK_NAMES["P3"], "result": "fail" if icf else "pass", "reasons": icf})
        # P0 + P4 take a path: the one declared write
        d = "/dev/shm" if os.path.isdir("/dev/shm") and os.access("/dev/shm", os.W_OK) else tempfile.gettempdir()
        fd, fp = tempfile.mkstemp(prefix="launchpad-gate-", suffix=".html", dir=d)
        try:
            os.close(fd)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(html)
            rl, rf = SCREEN.gate_receipt(fp, False)
            res = "fail" if rf else ("unmeasured" if any("UNPROVEN" in l for l in rl) else "pass")
            out.insert(0, {"id": "P0", "name": CHECK_NAMES["P0"], "result": res,
                           "reasons": [l.strip().replace(fp, "<page>") for l in rl]})
            cf = SCREEN.gate_compose(fp)
            out.append({"id": "P4", "name": CHECK_NAMES["P4"], "result": "fail" if cf else "pass",
                        "reasons": [str(x).replace(fp, "<page>") for x in cf]})
        finally:
            try:
                os.remove(fp)
            except OSError:
                pass
        return out

    # -------------------------------------------------------------- the stand-in page
    def splice(self, messages):
        """NOT a renderer (emitter E1 is, s311-D9): the page a surface stands for, made by splicing each
        part's reference-snippet MARKUP in tree order (depth first from root, then any part the tree does
        not reach), each in its own APOLLO-SPLICE markup region named by the snippet it came from, so the
        a11y clause judges it per part (s305-D54). canon.css is LINKED, never pasted (s307-D74); a
        snippet's inlined behaviour (an AUTO-BEHAVIOUR block, the copy of knowledge/canon/<name>.js
        gen_component_partials.py injects) is loaded by its address once per page instead, the way the
        receipt grammar addresses behaviour; the snippets' showroom fences (APOLLO-DEMO, s258-D3) are
        dropped. Returns (html, missing parts)."""
        import _validate_receipt as VR
        comps = self.components_of(messages)
        byid = {c.get("id"): c for c in comps}
        order, seen = [], set()

        def walk(i):
            if i in seen or i not in byid:
                return
            seen.add(i); order.append(byid[i])
            for _s, _a, kids in self.slot_children(byid[i]):
                for k in kids:
                    walk(k)
        walk("root")
        for c in comps:
            if c.get("id") not in seen:
                seen.add(c.get("id")); order.append(c)
        body, missing, behaviours = [], [], []
        for c in order:
            name = c.get("component")
            got = self.snippets.get(name)
            if not got:
                missing.append(name); continue
            sn, html = got
            m = re.search(r"<body\b[^>]*>(.*)</body>", html, re.S | re.I)
            inner = m.group(1) if m else html
            for a, b in reversed(VR.demo_fenced_spans(inner)):
                inner = inner[:a] + inner[b:]

            def link_behaviour(mb):
                if mb.group(1) not in behaviours:
                    behaviours.append(mb.group(1))
                return ""
            inner = AUTO_BEHAVIOUR_BLOCK.sub(link_behaviour, inner)
            region = "%s#%s" % (sn.split(".")[0], c.get("id"))
            body.append(VR.splice_marker_start(region, "knowledge/snippets/" + sn, "markup") + inner +
                        VR.splice_marker_end(region))
        scripts = "".join('<script src="knowledge/canon/%s.js"></script>' % b for b in behaviours)
        page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>surface</title>'
                '<link rel="stylesheet" href="knowledge/canon/canon.css"></head><body>%s%s</body></html>'
                % ("\n".join(body), scripts))
        return page, missing

    # -------------------------------------------------------------- the two tools
    def _verdict(self, checks, ts, tp, t0):
        return {"verdict": "fail" if any(c["result"] == "fail" for c in checks) else "pass",
                "checks": checks,
                "timing_ms": {"surface": ts, "page": tp, "total": round((time.perf_counter() - t0) * 1000, 2)},
                "catalogue": dict(self.cat_id)}

    def gate_surface(self, messages, splice=False):
        t0 = time.perf_counter()
        checks = self.surface_checks(messages)
        ts = round((time.perf_counter() - t0) * 1000, 2)
        tp = None
        if splice:
            t1 = time.perf_counter()
            page, missing = self.splice(messages)
            pc = self.page_checks(page)
            if missing:
                pc.insert(0, {"id": "P-", "name": "stand-in page", "result": "unmeasured",
                              "reasons": ["no reference snippet for %s" % ", ".join(map(str, missing))]})
            checks += pc
            tp = round((time.perf_counter() - t1) * 1000, 2)
        return self._verdict(checks, ts, tp, t0)

    def gate_page(self, html):
        t0 = time.perf_counter()
        checks = self.page_checks(html)
        tp = round((time.perf_counter() - t0) * 1000, 2)
        return self._verdict(checks, None, tp, t0)


_GATE = [None]

def gate():
    """The process's one warm gate."""
    if _GATE[0] is None:
        _GATE[0] = Gate()
    return _GATE[0]


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Gate one A2UI surface (a JSON list of messages) or one page.")
    ap.add_argument("file", help="a .json surface (list of A2UI messages) or an .html page; - for stdin JSON")
    ap.add_argument("--splice", action="store_true", help="also run the page layer on the stand-in page")
    a = ap.parse_args()
    raw = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    if a.file.endswith((".html", ".htm")):
        v = gate().gate_page(raw)
    else:
        v = gate().gate_surface(json.loads(raw), splice=a.splice)
    print(json.dumps(v, indent=1, ensure_ascii=False))
    sys.exit(0 if v["verdict"] == "pass" else 1)
