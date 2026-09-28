#!/usr/bin/env python3
"""305 B6 — the accepted when-rules (loose-ends page 4c, Dave 2026-09-28, each "Accept") written into their metas.
Wording: R4a's drafts, verbatim (notes/_lanes/304/R4a/drafts/when-rules.proposed.json, `proposed`), gate + prose
(the drafting lane's machine form). Only the four rows B5 measured as new/changed and not already in the metas:
button, filter-toolbar-bar, footer, template-dashboard-bento. NOT list-items, NOT app-shell-top-nav (Dave: "Change").
Plus `layout.grammar` added to knowledge/when-fields.json by addition (s273-D4), R4a's registry_additions.
Idempotent; writes through jspan.py so each file changes only in the lines meant. Run from the repo root:
  python3 notes/_lanes/305/B6/work/apply_rules.py [--dry]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import jspan as J
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
K = os.path.join(ROOT, "knowledge"); C = os.path.join(K, "components")
DRY = "--dry" in sys.argv
DRAFT = json.load(open(os.path.join(ROOT, "notes/_lanes/304/R4a/drafts/when-rules.proposed.json")))
ROWS = {r["slug"]: r for r in DRAFT["rows"]}
TAKE = ["button", "filter-toolbar-bar", "footer", "template-dashboard-bento"]
log = []

def edit(path, fn):
    raw = open(path, encoding="utf-8").read()
    new = fn(raw); json.loads(new)
    rel = os.path.relpath(path, ROOT)
    if new != raw:
        log.append("CHANGED " + rel)
        if not DRY: open(path, "w", encoding="utf-8").write(new)
    else:
        log.append("same    " + rel)

def rule(slug):
    r = ROWS[slug]
    def fn(raw):
        m = json.loads(raw); cur = m.get("when")
        if cur == r["proposed"]:
            return raw
        if r["current"] is None:
            assert cur is None, (slug, cur)
            return J.insert_after_key(raw, [], "name", "when", r["proposed"])   # no `provides`: after `name`, the template-* precedent
        assert cur == r["current"], (slug, "meta moved since the draft")
        return J.replace_string(raw, ["when"], r["proposed"])
    return fn

def when_fields(raw):
    have = json.loads(raw)["fields"]
    k = "layout.grammar"
    if k in have:
        return raw
    d = DRAFT["registry_additions"][k]
    anchor = '    "options": { "definition": "how many choices one selection offers", "kind": "count", "example": "options >= 5" }'
    assert raw.count(anchor) == 1
    add = ",\n    %s: { \"definition\": %s, \"kind\": %s, \"example\": %s }" % (
        json.dumps(k), json.dumps(d["definition"], ensure_ascii=False), json.dumps(d["kind"]), json.dumps(d["example"], ensure_ascii=False))
    return raw.replace(anchor, anchor + add, 1)

for s in TAKE:
    edit(os.path.join(C, s + ".meta.json"), rule(s))
edit(os.path.join(K, "when-fields.json"), when_fields)
print("\n".join(log))
