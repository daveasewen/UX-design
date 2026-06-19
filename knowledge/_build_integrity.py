#!/usr/bin/env python3
"""Knowledge-base integrity lint — the CI gate.

Checks that the hand-authored canon hangs together:
  1. SCHEMA      every components/*.meta.json validates against meta.schema.json
  2. SC          every accessibility.relatedSC entry is a known WCAG 2.2 SC
  3. REBIND      every tokenValidation rebind target resolves to a real store token
                 (REVIEW/"no equivalent" markers are allowed and counted, not failed)
  4. GUIDELINE   every guideline referenced (xref TOPICAL map + literal guidelines/*.md
                 in metas) exists on disk
  5. TOKENS      best-effort: token-path-looking strings in each meta's `tokens` block
                 resolve to the store (WARNING only — tokens are stored in prose)

Writes knowledge/_INTEGRITY-REPORT.md and exits non-zero if any ERROR-level check fails
(so it can gate a build). Run standalone or via _build_all.py.
"""
import json, os, glob, re, sys
from collections import defaultdict
import jsonschema

ROOT = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.join(ROOT, "components")
TOK = os.path.join(ROOT, "tokens")
GUIDE = os.path.join(ROOT, "guidelines")

# known WCAG 2.2 SCs we maintain rules for (mirror of build_compliance_kg.py M keys, + a few common AAs)
KNOWN_SC = {
 "1.1.1","1.2.2","1.2.5","1.3.1","1.3.2","1.3.5","1.4.1","1.4.3","1.4.4","1.4.10","1.4.11","1.4.13",
 "2.1.1","2.1.2","2.2.1","2.2.2","2.3.3","2.4.1","2.4.3","2.4.4","2.4.5","2.4.6","2.4.7","2.4.8",
 "2.4.11","2.5.7","2.5.8","3.3.1","3.3.2","4.1.2","4.1.3"}
SCRE = re.compile(r"^(\d+\.\d+\.\d+)")

errors, warnings, info = [], [], []
def err(c, m): errors.append((c, m))
def warn(c, m): warnings.append((c, m))

# --- token store leaf paths ---
store = set()
def walk_store(node, path=""):
    if isinstance(node, dict):
        if any(k in node for k in ("$value", "light", "scale-1", "dark")):
            store.add(path)
        for k, v in node.items():
            if k.startswith("$"): continue
            walk_store(v, (path + "/" + k).strip("/") if path else k)
for f in glob.glob(os.path.join(TOK, "*.json")):
    if os.path.basename(f).startswith(("_", "EXAMPLE")): continue
    try: walk_store(json.load(open(f)))
    except Exception as e: err("tokens", f"{os.path.basename(f)} not parseable: {e}")
store_groups = {p.split("/")[0] for p in store}

# --- schema ---
schema = json.load(open(os.path.join(COMP, "meta.schema.json")))
# base_uri="" so the local "#/definitions/..." $ref resolves by JSON pointer
# (the schema's non-URL $id must not be used as a base URI).
_resolver = jsonschema.RefResolver(base_uri="", referrer=schema)
validator = jsonschema.Draft7Validator(schema, resolver=_resolver)
avail_guides = {os.path.basename(p) for p in glob.glob(os.path.join(GUIDE, "*.md"))}

TOKPATH = re.compile(r"\b([a-z][a-z0-9-]*(?:/[a-z0-9*-]+){1,4})\b")
metas = sorted(f for f in glob.glob(os.path.join(COMP, "*.meta.json"))
               if not os.path.basename(f).startswith("EXAMPLE") and os.path.basename(f) != "meta.schema.json")
schema_ok = 0
for f in metas:
    name = os.path.basename(f)
    d = json.load(open(f))
    cname = d.get("name", name)
    # 1. schema
    errs = sorted(validator.iter_errors(d), key=lambda e: e.path)
    if errs:
        for e in errs[:8]:
            loc = "/".join(str(x) for x in e.path) or "(root)"
            err(cname, f"schema: {loc}: {e.message[:120]}")
    else:
        schema_ok += 1
    # 2. SCs
    for sc in (d.get("accessibility") or {}).get("relatedSC") or []:
        m = SCRE.match(sc.strip())
        if not m: err(cname, f"relatedSC not a SC number: {sc!r}")
        elif m.group(1) not in KNOWN_SC: err(cname, f"relatedSC unknown to compliance lookup: {m.group(1)}")
    # 3. rebind targets
    tv = d.get("tokenValidation")
    du = tv.get("depricateUsage") if isinstance(tv, dict) else None
    rows = du.get("tokens") if isinstance(du, dict) else None
    for r in (rows or []):
        if not isinstance(r, dict): continue
        rb = r.get("rebind")
        if not rb or not isinstance(rb, str): continue
        if re.search(r"\bREVIEW\b|no live|no clean|NO live|no equivalent", rb): continue  # flagged, not a clean target
        cands = [c for c in TOKPATH.findall(rb) if c.split("/")[0] in store_groups]
        if cands and not any(c.rstrip("/*") in store or c in store for c in cands):
            warn(cname, f"rebind target unresolved: {rb!r} (tok {r.get('token','?')[:40]})")
    # 4. guideline literals in meta
    for g in re.findall(r"guidelines/([a-z0-9-]+\.md)", json.dumps(d)):
        if g not in avail_guides: err(cname, f"references missing guideline: {g}")
    # 5. token paths in tokens block (best-effort, WARNING)
    tb = d.get("tokens", {})
    for v in (tb.values() if isinstance(tb, dict) else []):
        if not isinstance(v, str): continue
        for cand in TOKPATH.findall(v):
            top = cand.split("/")[0]
            if top not in store_groups: continue
            if "*" in cand or "depricate" in cand: continue
            if cand in store: continue
            # allow parent-path references (e.g. tertiary/background) that have children in store
            if any(p.startswith(cand + "/") for p in store): continue
            warn(cname, f"token path may not resolve: {cand!r}")

# --- cross-check: xref TOPICAL guideline map points only at real files ---
xref = os.path.join(ROOT, "_XREF-INDEX.json")
if os.path.exists(xref):
    xj = json.load(open(xref))
    for cname, h in xj.get("components", {}).items():
        for g in h.get("guidelines", []):
            if g not in avail_guides: err(cname, f"xref guideline missing on disk: {g}")

# --- report ---
L = ["# Knowledge-base integrity report", "",
     "> CI gate over the authored canon. **ERROR** = the graph is inconsistent (fix before relying on it); **WARNING** = best-effort / probably fine but worth a look. Regenerate: `python3 knowledge/_build_integrity.py` (exits non-zero on any ERROR).", ""]
L.append(f"**Result:** {'PASS ✅' if not errors else 'FAIL ❌'} — {len(errors)} errors, {len(warnings)} warnings. "
         f"Schema: {schema_ok}/{len(metas)} metas valid. Token store: {len(store)} leaf tokens, groups {len(store_groups)}.")
L.append("")
def section(title, rows, none="None."):
    out = [f"## {title} ({len(rows)})", ""]
    if not rows: out += [f"_{none}_", ""]; return out
    by = defaultdict(list)
    for c, m in rows: by[c].append(m)
    for c in sorted(by):
        out.append(f"**{c}**")
        for m in by[c]: out.append(f"- {m}")
        out.append("")
    return out
L += section("Errors", errors, "No errors — the canon is internally consistent. 🎉")
L += section("Warnings (best-effort)", warnings)
open(os.path.join(ROOT, "_INTEGRITY-REPORT.md"), "w").write("\n".join(L))

print(f"integrity: {'PASS' if not errors else 'FAIL'} — {len(errors)} errors, {len(warnings)} warnings")
print(f"schema valid: {schema_ok}/{len(metas)}")
if errors:
    print("first errors:")
    for c, m in errors[:12]: print(f"  [{c}] {m}")
sys.exit(1 if errors else 0)