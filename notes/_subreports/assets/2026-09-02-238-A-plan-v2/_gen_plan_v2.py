#!/usr/bin/env python3
"""_gen_plan_v2.py — #238 lane A. GENERATES `_PLAN-designers-brain-2026-09-02-v2.html` from
`plan-v2.template.html` (same folder) + `knowledge/_rulings.json`, so that every ruled text the
plan quotes is copied from the store by machine and never retyped (s234-D1 generation, never
copy; the brief's DO-NOT-RULE: "No re-wording of any `ruled` text").

Placeholders in the template:
  {{RULED:<id>}}                the store's `ruled` text, HTML-escaped, verbatim
  {{DATE:<id>}} {{BY:<id>}}     the store's `date` / `by`
  {{SAYS-FRAG:<id>|<fragment>}} renders <fragment>, REFUSES unless it is a substring of `says`
  {{RULINGS-TOTAL}}             len(rulings) in the store at generation time
  {{S238-COUNT}}                how many ids start with s238
  {{OPEN-COUNT}}                number of <tr class="open"> rows in the template (counted, not typed)
  {{BYTES:<repo-relative path>}} os.path.getsize at generation time
  {{GENERATED-AT}}              UTC clock

Usage:
  python3 _gen_plan_v2.py            # generate (refuses if any placeholder cannot resolve)
  python3 _gen_plan_v2.py --check    # re-read the OUTPUT and verify every quoted ruling is verbatim,
                                     # and classify every 'tension' hit (path / id / quote / footnote)
Exit codes: 0 ok · 2 refusal (named).
"""
import datetime as _dt
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
STORE = os.path.join(REPO, "knowledge", "_rulings.json")
TEMPLATE = os.path.join(HERE, "plan-v2.template.html")
OUT = os.environ.get("PLAN_V2_OUT") or os.path.join(REPO, "_PLAN-designers-brain-2026-09-02-v2.html")
# PLAN_V2_OUT exists so the --check can be driven against a MUTATED copy (self-test); generation
# in the repo never sets it.

PH = re.compile(r"\{\{([A-Z0-9-]+)(?::([^}|]+?))?(?:\|([^}]+?))?\}\}")


def refuse(msg):
    print("REFUSED: " + msg)
    sys.exit(2)


def load_store():
    d = json.load(open(STORE, encoding="utf-8"))
    rows = d["rulings"]
    return {e["id"]: e for e in rows}, len(rows)


def generate():
    store, total = load_store()
    tpl = open(TEMPLATE, encoding="utf-8").read()
    open_count = len(re.findall(r'<tr class="open"', tpl))
    used = []

    def sub(m):
        kind, arg, frag = m.group(1), m.group(2), m.group(3)
        if kind == "RULED":
            if arg not in store:
                refuse(f"ruling id not in store: {arg}")
            used.append(arg)
            return html.escape(store[arg]["ruled"], quote=False)
        if kind == "DATE":
            return html.escape(store[arg]["date"])
        if kind == "BY":
            return html.escape(store[arg]["by"])
        if kind == "SAYS-FRAG":
            if arg not in store:
                refuse(f"ruling id not in store: {arg}")
            if frag not in store[arg]["says"]:
                refuse(f"SAYS-FRAG not a substring of {arg}.says: {frag!r}")
            return html.escape(frag, quote=False)
        if kind == "RULINGS-TOTAL":
            return str(total)
        if kind == "S238-COUNT":
            return str(sum(1 for k in store if k.startswith("s238")))
        if kind == "OPEN-COUNT":
            return str(open_count)
        if kind == "BYTES":
            p = os.path.join(REPO, arg)
            if not os.path.exists(p):
                refuse(f"BYTES path missing: {arg}")
            return f"{os.path.getsize(p):,}"
        if kind == "GENERATED-AT":
            return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        refuse(f"unknown placeholder {m.group(0)}")

    out = PH.sub(sub, tpl)
    left = PH.findall(out)
    if left:
        refuse(f"unresolved placeholders remain: {left[:5]}")
    open(OUT, "w", encoding="utf-8").write(out)
    print(f"GENERATED {os.path.relpath(OUT, REPO)}  bytes={len(out.encode('utf-8')):,}  "
          f"rulings quoted={len(used)} distinct={len(set(used))}  open rows={open_count}  store={total}")
    return 0


def check():
    store, total = load_store()
    tpl = open(TEMPLATE, encoding="utf-8").read()
    out = open(OUT, encoding="utf-8").read()
    ids = re.findall(r"\{\{RULED:([^}]+)\}\}", tpl)
    bad = [i for i in ids if html.escape(store[i]["ruled"], quote=False) not in out]
    print(f"quoted rulings: {len(ids)} ({len(set(ids))} distinct) — verbatim in output: {len(ids) - len(bad)}/{len(ids)}")
    if bad:
        refuse(f"ruled text NOT verbatim in output for: {bad}")
    # the rename probe: every 'tension' on the page must be a path, an id, a quoted store text,
    # a register/store title, or the footnote itself — never v2 prose.
    text = re.sub(r"<style>.*?</style>", "", out, flags=re.S)
    hits = [(m.start(), m.group(0)) for m in re.finditer(r"tension", text, re.I)]
    classes = {"path": 0, "quoted-store-text": 0, "quoted-report-text": 0, "footnote": 0, "store-title": 0, "prose": 0}
    prose = []
    store_blobs = [html.escape(e["ruled"], quote=False) for e in store.values()] + \
                  [html.escape(e.get("says", ""), quote=False) for e in store.values()]
    for pos, w in hits:
        ctx = text[max(0, pos - 160): pos + 160]
        line = text[text.rfind("\n", 0, pos) + 1: text.find("\n", pos)]
        # a path: the hit sits inside a filename token (no whitespace between the hit and a '.json' / '.md' / '.html' / '-brief')
        tok_start = max(text.rfind(" ", 0, pos), text.rfind(">", 0, pos), text.rfind("\n", 0, pos)) + 1
        tok_end = min(x for x in (text.find(" ", pos), text.find("<", pos), text.find("\n", pos), len(text)) if x != -1)
        token = text[tok_start:tok_end]
        if re.search(r"(\.json|\.md|\.html|-brief|_derive_sort|T-tensions)", token):
            classes["path"] += 1
        elif 'class="rt"' in text[max(0, pos - 3000):pos] and "</p>" not in text[text.rfind('class="rt"', 0, pos):pos]:
            classes["quoted-store-text"] += 1
        elif '<q class="rq">' in text[max(0, pos - 200):pos] and "</q>" not in text[text.rfind('<q class="rq">', 0, pos):pos]:
            classes["quoted-report-text"] += 1
        elif "fn-polarity" in text[max(0, pos - 400):pos + 50]:
            classes["footnote"] += 1
        elif re.search(r"W-3\d\d", line) or "store-title" in ctx:
            classes["store-title"] += 1
        elif any(w in blob and re.sub(r"\s+", " ", line.strip())[:60] in re.sub(r"\s+", " ", blob) for blob in store_blobs):
            classes["quoted-store-text"] += 1
        else:
            classes["prose"] += 1
            prose.append(line.strip()[:140])
    print("'tension' hits on the page (style block excluded):", len(hits), classes)
    if prose:
        print("PROSE HITS (must be zero):")
        for p in prose:
            print("   ", p)
        refuse("the rename is incomplete — 'tension' survives in v2 prose")
    # counts
    open_rows = len(re.findall(r'<tr class="open"', out))
    print(f"open rows counted on the page: {open_rows}")
    print("CHECK OK")
    return 0


if __name__ == "__main__":
    sys.exit(check() if "--check" in sys.argv else generate())
