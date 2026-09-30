#!/usr/bin/env python3
"""
gen_provenance_receipt.py — the MINT half of the provenance receipt (s234-D6, s235-D1).

`_validate_receipt.py` is the check. This is the generator that makes a page checkable:
it SPLICES regions out of `knowledge/snippets/*.reference.html`, marks them in the page's
own bytes, and injects a `#provenance-receipt` JSON block BESIDE `#token-manifest` — never
inside it, exactly as `#token-manifest` sits beside nothing and owns its own id (the
precedent regex: `gen_component_partials.py:301`).

⛔ THE PREMISE IN THE BRIEF DID NOT SURVIVE THE PROBE, AND THE PROBE WINS.
The L1 brief says "whichever module today injects `#token-manifest` into snippets gains the
receipt injection beside it". **No module injects it.** Probes:
  `grep -rn 'type="application/json" id="token-manifest"' --include=*.py .` -> 6 hits, all
    test fixtures / selftest strings (`_tests/test_gates.py:375`, `_validate_binds_resolve.py:251`);
  `knowledge/gen_snippet_tokens.py:139-141` — the manifest is READ, and a snippet without one
    is returned as `{"warn": ["no #token-manifest"]}`, not repaired;
  `check-with-gates/SKILL.md` Route C tells a contributor to WRITE the manifest by hand.
137/137 snippets carry a hand-authored manifest. So the receipt could not be added "beside"
an injector that does not exist, and this is a NEW module — named in the repo's `gen_*`
grammar, sharing ONE parse with the gate. What the brief's clause actually protects is the
SHAPE (a sibling JSON block, not a new key inside the manifest), and that is honoured.

⛔ AND THE RECEIPT IS A PAGE-LEVEL ARTEFACT ANYWAY. `#token-manifest` belongs to a SNIPPET
(the var -> token bindings that snippet declares). A receipt belongs to a COMPOSED PAGE (what
was spliced INTO it, and from where). A snippet has no provenance to record — it is the
source. So the injection point is the page, and the consumer is `_validate_screen.py <path>`,
which is the one gate that takes a path (s234-D6).

--------------------------------------------------------------------------------- WHAT IT DOES

  --compose SPEC -o PAGE   build PAGE by splicing the regions SPEC names, then mint.
  --mint PAGE              (re-)mint the receipt from the APOLLO-SPLICE markers already in PAGE.
  --check PAGE             mint in memory and diff against what is on disk; non-zero if stale.
  --selftest               bite-test (ADR-0005 §5)

THE SPEC (JSON):
  {"title": "...", "pack": "1.0.5", "theme": "light",
   "regions": [
     {"snippet": "Stat-card", "select": ".stat-card", "kind": "markup", "props": {...}},
     {"snippet": "Stat-card", "kind": "style"},
     {"snippet": "Chart-line", "kind": "behaviour", "behaviour": "dv-behaviour"}
   ]}

`kind`:
  markup     the first element in the snippet's <body> carrying `select`, extracted by a
             BALANCED tag scan — the exact source bytes, opening tag to matching close.
  style      the snippet's <style> inner text, verbatim.
  behaviour  one whole `AUTO-BEHAVIOUR <name>` block, markers included, so the page inlines
             the behaviour the way a snippet does and `_validate_receipt.behaviour_loaded`
             can see it.

THE HASH IS NOT COMPUTED HERE. `_validate_receipt.region_bytes` / `.sha256_of` are imported.
One definition, two users — [[no-gate-parses-the-artefact]]: the mint and the check parse the
artefact with the SAME parser, so a drift between them is not expressible.

THE BEHAVIOUR ADDRESS IS READ, NEVER PROMOTED. For each markup region the generator looks for
an address in exactly two mechanical places, in order:
  1. `knowledge/component-types.json` `$behaviour/<name>.source` for a behaviour the SNIPPET
     carries an AUTO-BEHAVIOUR block for (a real, resolvable path — e.g. `canon/dv-behaviour.js`);
  2. nothing else.
`knowledge/components/<slug>.meta.json` `behaviour` is DELIBERATELY NOT read as an address:
`meta.schema.json:197` still types it as "optional behavioural notes" (object|array|string),
i.e. prose. Typing it is `s234-D5` and belongs to L2. Promoting prose to an address here would
mint a receipt that asserts something the meta never said. `script: null` + `$scriptNote` is
the honest form, and the gate reports NO-BEHAVIOUR-DECLARED for it.

`retrievalSet` is `null` with a `$retrievalSetNote`: rC Q4 is OPEN and is not this lane's.

Usage:
  python3 knowledge/gen_provenance_receipt.py --compose spec.json -o out.html
  python3 knowledge/gen_provenance_receipt.py --mint out.html
  python3 knowledge/gen_provenance_receipt.py --check out.html
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SNIP = os.path.join(HERE, "snippets")
sys.path.insert(0, HERE)
import _validate_receipt as VR          # ONE parse, shared with the gate

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
TAG_RE = re.compile(r"<(/?)([a-zA-Z][\w:-]*)([^>]*?)(/?)>", re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
STYLE_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S)
BODY_RE = re.compile(r"<body[^>]*>(.*)</body>", re.S)


def snippet_path(name):
    p = os.path.join(SNIP, name + ".reference.html")
    if not os.path.isfile(p):
        raise SystemExit("REFUSED: no snippet %s (looked at %s)" % (name, p))
    return p


def extract_element(html, select):
    """The first element in <body> matching `select` (".cls" or "#id"), returned as the EXACT
    source bytes from its opening `<` to the end of its matching close tag.

    Balanced scan over the tag stream, comments masked out so a commented-out copy can never
    be the match (the [[unmatched-grep-is-not-an-absence]] sibling: a MATCH inside a comment
    is not a presence either — `_htmlmask`'s lesson, applied at the same length so offsets
    hold). Void elements never open a level. Raises SystemExit with a NAMED reason rather
    than returning something plausible."""
    bm = BODY_RE.search(html)
    if not bm:
        raise SystemExit("REFUSED: snippet has no <body>")
    body, base = bm.group(1), bm.start(1)
    masked = COMMENT_RE.sub(lambda m: " " * len(m.group(0)), body)   # length-preserving

    if select.startswith("."):
        attr_re = re.compile(r'class="[^"]*(?<![\w-])%s(?![\w-])[^"]*"' % re.escape(select[1:]))
    elif select.startswith("#"):
        attr_re = re.compile(r'id="%s"' % re.escape(select[1:]))
    else:
        raise SystemExit("REFUSED: select must start with . or # — got %r" % select)

    for m in TAG_RE.finditer(masked):
        closing, tag, attrs, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if closing or not attr_re.search(attrs):
            continue
        if selfclose or tag in VOID:
            return body[m.start():m.end()], base + m.start()
        depth, pos = 1, m.end()
        for n in TAG_RE.finditer(masked, m.end()):
            t = n.group(2).lower()
            if t != tag:
                continue
            if n.group(1):
                depth -= 1
                if depth == 0:
                    return body[m.start():n.end()], base + m.start()
            elif not (n.group(4) or t in VOID):
                depth += 1
        raise SystemExit("REFUSED: %s opens and never closes in this snippet" % select)
    raise SystemExit("REFUSED: nothing in the snippet's live <body> matches %s" % select)


def extract_style(html):
    m = STYLE_RE.search(html)
    if not m:
        raise SystemExit("REFUSED: snippet has no <style> block")
    return m.group(1), m.start(1)


def extract_behaviour(html, name):
    """One whole AUTO-BEHAVIOUR block, MARKERS INCLUDED — the markers are what makes the
    behaviour findable by `_validate_receipt.behaviour_loaded` once it is in the page."""
    s = re.search(r'<!--\s*=====\s*AUTO-BEHAVIOUR\s+%s\s+START[^>]*=====\s*-->' % re.escape(name),
                  html)
    e = re.search(r'<!--\s*=====\s*AUTO-BEHAVIOUR\s+%s\s+END\s*=====\s*-->' % re.escape(name),
                  html)
    if not (s and e and e.start() > s.start()):
        raise SystemExit("REFUSED: snippet carries no AUTO-BEHAVIOUR %s block" % name)
    return html[s.start():e.end()], s.start()


_CT = None
def behaviour_address(snippet_html):
    """The behaviour address this snippet ACTUALLY carries, resolved mechanically:
    the AUTO-BEHAVIOUR names present in the snippet, looked up in component-types.json's
    $behaviour registry. Returns a repo-relative path or None. Never reads meta prose."""
    global _CT
    names = [m.group("name") for m in VR.AUTO_BEHAVIOUR_RE.finditer(snippet_html)]
    if not names:
        return None
    if _CT is None:
        _CT = json.load(open(os.path.join(HERE, "component-types.json"), encoding="utf-8"))
    reg = {}
    def walk(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == "$behaviour" and isinstance(v, dict):
                    for n, b in v.items():
                        if isinstance(b, dict) and b.get("source"):
                            reg[n] = "knowledge/" + b["source"]
                else:
                    walk(v)
    walk(_CT)
    for n in names:
        if n in reg:
            return reg[n]
    return None


def script_address(snippet_name, snippet_html):
    """#305 call 4 (Dave, 2026-09-27: "yes as recommended") — THE MINT FOLLOWS THE META.
    The meta is the ONE home of a component's facts (s234-D5) and `_validate_receipt` already reads
    it as the home and the receipt as a copy; so a region's `script` is COPIED from the meta's typed
    `behaviour.script` (all fourteen chart metas: knowledge/canon/dv-render.js, the core that draws,
    priced once per page by s260-D1). Before this, the mint took the FIRST registered AUTO-BEHAVIOUR
    name in the snippet's document order (dv-behaviour.js for every chart), so every chart region on
    a pack-minted page read FAIL:BEHAVIOUR-ADDRESS-DISAGREES (R4s2; cand2-r3 10/10 pages).
    Only a component whose meta carries NO typed behaviour falls back to the mechanical resolution
    below, which is the pre-s234-D5 reading and names what the snippet actually inlines.
    -> (address or None, "meta" | "snippet")"""
    mp = VR.meta_path_for(snippet_name or "")
    typed = VR.typed_behaviour(VR.load_meta(mp)) if mp else None
    if typed is not None:
        return typed.get("script"), "meta"
    return behaviour_address(snippet_html), "snippet"


def manifest_vars(html):
    m = re.search(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(1)).get("vars", {})
    except Exception:
        return {}


PAGE_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<!--
  GENERATED by knowledge/gen_provenance_receipt.py --compose %(spec)s
  Every region between APOLLO-SPLICE markers is a byte-identical cut from the file its
  marker names. Do not edit them here: edit the snippet and regenerate. The
  #provenance-receipt block below is minted from THESE bytes (s235-D1) and
  knowledge/_validate_receipt.py re-hashes them.
-->
<script type="application/json" id="token-manifest">%(manifest)s</script>
<style>
%(styles)s
</style>
</head>
<body data-theme="%(theme)s">
%(markup)s
%(behaviours)s
</body>
</html>
"""


def compose(spec_path, out_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    styles, markup, behaviours = [], [], []
    vars_union = {}
    for i, r in enumerate(spec["regions"], 1):
        name = r["snippet"]
        src_rel = os.path.relpath(snippet_path(name), REPO)
        html = open(snippet_path(name), encoding="utf-8").read()
        vars_union.update(manifest_vars(html))
        kind = r.get("kind", "markup")
        if kind == "markup":
            text, _off = extract_element(html, r["select"])
        elif kind == "style":
            text, _off = extract_style(html)
            # s258-D3: APOLLO-DEMO fenced CSS is showroom harness, never spliced - the same span
            # gen_canon_components.py drops from canon (#309 D: Metric's style carries one).
            text = re.sub(r"/\* ===== APOLLO-DEMO[^\n]*?START.*?APOLLO-DEMO[^\n]*?END ===== \*/", "",
                          text, flags=re.S)
        elif kind == "behaviour":
            text, _off = extract_behaviour(html, r["behaviour"])
        else:
            raise SystemExit("REFUSED: unknown kind %r" % kind)
        region = r.get("region") or "%s#%d" % (name, i)
        block = "%s\n%s\n%s" % (VR.splice_marker_start(region, src_rel, kind), text,
                                VR.splice_marker_end(region))
        (styles if kind == "style" else behaviours if kind == "behaviour" else markup).append(block)
    page = PAGE_TMPL % {
        "title": spec.get("title", "Composed page"),
        "spec": os.path.relpath(spec_path, REPO),
        "manifest": json.dumps({"vars": vars_union}, indent=1),
        "styles": "\n".join(styles),
        "markup": "\n".join(markup),
        "behaviours": "\n".join(behaviours),
        "theme": spec.get("theme", "light"),
    }
    page = mint(page, spec, out_path)
    open(out_path, "w", encoding="utf-8").write(page)
    return page


def mint(page, spec, out_path):
    """Build the receipt from the page's OWN marked regions and splice it in beside
    #token-manifest. Idempotent: an existing receipt block is REPLACED, not appended."""
    props_by_region = {}
    if spec:
        for i, r in enumerate(spec.get("regions", []), 1):
            rid = r.get("region") or "%s#%d" % (r["snippet"], i)
            props_by_region[rid] = r
    else:
        # --mint / --check on a page with no spec in hand: the READER fields (variant, props,
        # select, behaviour) are carried forward from the receipt already in the page. Dropping
        # them would make `--check` report RECEIPT-STALE for a page whose bytes never moved —
        # a re-mint that changes the receipt is a change, and a check that reds on its own
        # forgetting is the [[a-crash-is-not-a-fail]] class in the other direction.
        old, _err = VR.parse_receipt(page)
        for r in (old or {}).get("regions", []):
            if isinstance(r, dict) and r.get("region"):
                props_by_region[r["region"]] = r
        if old and not (spec or {}).get("pack"):
            spec = {"pack": old.get("pack")}
    regions = []
    for rid in VR.marked_regions(page):
        text, _span = VR.region_bytes(page, rid)
        if text is None:
            raise SystemExit("REFUSED: region %s has a START marker and no END marker" % rid)
        attrs = ""
        for mm in VR.SPLICE_START_RE.finditer(page):
            if mm.group("region") == rid:
                attrs = mm.group("attrs"); break
        ms = re.search(r"source=(\S+)", attrs)
        mk = re.search(r"kind=(\w+)", attrs)
        source = ms.group(1) if ms else None
        kind = mk.group(1) if mk else None
        spec_r = props_by_region.get(rid, {})
        script, script_from = None, None
        snip_name = spec_r.get("snippet") or (
            os.path.basename(source).replace(".reference.html", "") if source else None)
        if kind == "markup" and source:
            sp = os.path.join(REPO, source)
            if os.path.isfile(sp):
                script, script_from = script_address(snip_name, open(sp, encoding="utf-8").read())
        entry = {
            "region": rid,
            "snippet": snip_name,
            "kind": kind,
            "source": source,
            # FOR THE READER, per s235-D1 ("filename/slug/pack may ride along … the gate
            # COMPARES on the hash"). `select`/`behaviour` let the gate re-cut the region
            # from `source` to name the byte that moved — a HINT after the verdict is
            # already settled by the hash, never an input to it.
            "select": spec_r.get("select"),
            "behaviour": spec_r.get("behaviour"),
            "hash": VR.sha256_of(text),
            "bytes": len(text.encode("utf-8")),
            "variant": spec_r.get("variant"),
            "props": spec_r.get("props"),
            "script": script,
        }
        if script is None and script_from == "meta":
            entry["$scriptNote"] = ("the meta's typed `behaviour.script` is null: the component "
                                    "declares it carries no script (s234-D5), and the receipt copies that.")
        elif script is None:
            entry["$scriptNote"] = ("no ADDRESS exists to declare: the snippet carries no "
                                    "AUTO-BEHAVIOUR block, and meta `behaviour` is untyped "
                                    "prose (meta.schema.json:197). Typing it is s234-D5 (L2).")
        regions.append(entry)
    receipt = {
        "$schema": VR.SCHEMA,
        "pack": (spec or {}).get("pack") or "UNDECLARED",
        "generator": "knowledge/gen_provenance_receipt.py",
        "retrievalSet": None,
        "$retrievalSetNote": ("rC Q4 — the retrieval-set membership marker — is OPEN. null "
                              "is the honest value; the gate reports it UNPROVEN rather than "
                              "letting a green imply it was checked."),
        "$key": ("sha256 of the page's OWN region bytes (s235-D1). Valid against `pack` only: "
                 "the hash moves on every regen serial."),
        "regions": regions,
    }
    block = '<script type="application/json" id="%s">\n%s\n</script>' % (
        VR.RECEIPT_ID, json.dumps(receipt, indent=1))
    if VR.RECEIPT_RE.search(page):
        return VR.RECEIPT_RE.sub(lambda m: block, page, count=1)
    anchor = re.search(r'<script[^>]*id="token-manifest"[^>]*>.*?</script>', page, re.S)
    if anchor:                       # BESIDE the manifest, never inside it
        return page[:anchor.end()] + "\n" + block + page[anchor.end():]
    return page.replace("</head>", block + "\n</head>", 1)


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--compose" in argv:
        spec = argv[argv.index("--compose") + 1]
        if "-o" not in argv:
            print("REFUSED: --compose needs -o <out.html>"); return 2
        out = argv[argv.index("-o") + 1]
        compose(spec, out)
        print("wrote %s" % out)
        return 0
    if "--mint" in argv or "--check" in argv:
        checking = "--check" in argv
        p = argv[argv.index("--check" if checking else "--mint") + 1]
        if not os.path.isfile(p):
            print("REFUSED: not a file — %s" % p); return 2
        cur = open(p, encoding="utf-8").read()
        new = mint(cur, None, p)
        if checking:
            same = (new == cur)
            print(("PASS — receipt in sync with the page's bytes" if same else
                   "FAIL:RECEIPT-STALE — the page's regions no longer mint this receipt"))
            return 0 if same else 1
        open(p, "w", encoding="utf-8").write(new)
        print("minted receipt into %s" % p)
        return 0
    print("REFUSED: one of --compose / --mint / --check / --selftest is required")
    return 2


def selftest():
    """ADR-0005 §5. Drives the REAL extractor on a REAL snippet, then proves the minted
    receipt is one the REAL gate accepts, and that a one-byte edit reds it."""
    import tempfile
    ok = True
    d = tempfile.mkdtemp()
    spec = {"title": "selftest", "pack": "selftest", "regions": [
        {"snippet": "Metric", "select": ".metric", "kind": "markup"},
        {"snippet": "Metric", "kind": "style"}]}
    sp = os.path.join(d, "spec.json")
    json.dump(spec, open(sp, "w"))
    out = os.path.join(d, "page.html")
    compose(sp, out)
    page = open(out, encoding="utf-8").read()

    # A — the spliced markup is byte-identical to the snippet's own bytes
    snip = open(snippet_path("Metric"), encoding="utf-8").read()  # s309-D3: the stat card moved to Metric
    want, _ = extract_element(snip, ".metric")
    got, _ = VR.region_bytes(page, "Metric#1")
    a = (got.strip() == want.strip()) and want in snip
    ok &= a; print(("  ✅ " if a else "  ❌ ") + "A  splice is byte-identical to the snippet")

    # B — the real gate passes the generated page
    lines, fails, unproven = VR.check(out)
    b = not fails
    ok &= b; print(("  ✅ " if b else "  ❌ ") + "B  gate PASSes the minted page -> " +
                   (",".join(fails) or "PASS"))

    # C — one byte inside a region reds it
    mut = page.replace("Net cash flow", "Net cash flowe", 1)
    mp = os.path.join(d, "mut.html")
    open(mp, "w", encoding="utf-8").write(mut)
    _l, mf, _u = VR.check(mp)
    c = "HASH-MISMATCH" in mf
    ok &= c; print(("  ✅ " if c else "  ❌ ") + "C  one-byte mutation -> " + (",".join(mf) or "PASS"))

    # D — --check sees a stale receipt
    dsame = (mint(mut, None, mp) != mut)
    ok &= dsame; print(("  ✅ " if dsame else "  ❌ ") + "D  --check detects the stale receipt")

    # E — an unreachable selector REFUSES loudly, it does not return something plausible
    try:
        extract_element(snip, ".no-such-class-anywhere")
        e = False
    except SystemExit:
        e = True
    ok &= e; print(("  ✅ " if e else "  ❌ ") + "E  missing selector REFUSES, never guesses")

    # F — #305 call 4: a chart region's minted `script` is the META's (dv-render.js), and the real
    #     gate reads no BEHAVIOUR-ADDRESS-DISAGREES on it. The old reading (first AUTO-BEHAVIOUR name)
    #     would have minted dv-behaviour.js here.
    spec2 = {"title": "selftest-chart", "pack": "selftest", "regions": [
        {"snippet": "Chart-line", "select": ".dv", "kind": "markup"}]}
    sp2 = os.path.join(d, "spec2.json"); json.dump(spec2, open(sp2, "w"))
    out2 = os.path.join(d, "chart.html")
    try:
        compose(sp2, out2)
        rc2, _e = VR.parse_receipt(open(out2, encoding="utf-8").read())
        got_s = [r.get("script") for r in (rc2 or {}).get("regions", []) if r.get("kind") == "markup"]
        meta_s = VR.typed_behaviour(VR.load_meta(VR.meta_path_for("Chart-line")))["script"]
        _l2, f2, _u2 = VR.check(out2)
        f = got_s == [meta_s] and "BEHAVIOUR-ADDRESS-DISAGREES" not in f2
        detail = "script %s (meta %s) · gate %s" % (got_s, meta_s, ",".join(f2) or "PASS")
    except SystemExit as e:
        f, detail = False, "compose refused: %s" % e
    ok &= f; print(("  ✅ " if f else "  ❌ ") + "F  chart region's script is the meta's -> " + detail)

    print("SELFTEST: " + ("PASS ✅" if ok else "FAIL ❌"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
