#!/usr/bin/env python3
"""
Composition GATE — the tier above the per-component rubric (called for in the
payments-journey proof). Validates that a SCREEN composed from canon/canon.css
cannot silently drift from the gated components + tokens.

For canon/canon.css:
  1. VARS RESOLVE   — every var(--x) used has a matching --x definition
                      (runtime-set --pct/--row-h excepted; --demo-width is REFUSED, check 11).
  2. BRACES         — balanced (cheap structural sanity).
  3. TOKEN SPINE    — the AUTO-GENERATED token block regenerates byte-identically
                      from knowledge/tokens/*.json (the spine is generated, not
                      hand-copied → it cannot drift from the store).

For each composed screen (*.canon.html):
  4. NO ROGUE HEX   — the screen's own <style> and inline style="" carry no #hex
                      colour. All colour must arrive via canon classes / tokens.
  5. NO REDEFINES   — the screen does not locally redefine any .c-* class
                      (no per-screen component re-derivation = the drift vector).
  6. CLASSES RESOLVE — every .c-* class used in the markup is defined in canon.css
                      (a typo'd class silently renders unstyled).
  8. UNIQUE TITLE   — every composed screen carries a non-empty <title>, unique
                      across the *.canon.html set (aca-003, SC 2.4.2 — first thing
                      a speech-output user hears. RULED BLOCKING by Dave 2026-07-03,
                      sweep-batch ruling; scope = composed/canon screens only, so
                      showcase/fitness-test surfaces are exempt by scope — the known
                      cold-A/cold-B duplicate is a deliberate A/B pair outside scope).

  9. NO SIZED PART — s305-D57 half A (rule 3a of ADS-generate-from-canon: "the page arranges
                      parts; it never resizes them") made checkable, and s307-D75 (#307, Dave by
                      click 2026-09-28 21:17 BST, verbatim: "Rebuild the shared stylesheet" — "a
                      page places parts and never sizes them"). The page's own <style> rules and
                      inline style="" may not set font-size, height, min-height, padding(-*),
                      width, zoom or transform on a part: a rule whose SUBJECT (the last compound
                      of the selector) carries a `.c-*`/`.cn-*` class, or a class that canon.css
                      defines under a `.cn-*` scope the element on this page actually sits inside
                      (so the page's own `.sheet` is its own, while `.tpl-tabs .tabs` resizes the
                      Tabs part). Custom properties are not read here. A static approximation of
                      "a .cn-* scope or anything inside one", measured on the tree before it was
                      wired (report notes/_subreports/2026-10-01-311-A1-*).
                      LEGACY LEDGER: four older hand-composed fitness screens carried sizing
                      before the check existed; their counts are pinned below and may only SHRINK
                      (a new hit on them reds; a lower count is printed as a note to lower the pin).
 10. LINK, DON'T PASTE — s307-D74. `_validate_receipt.link_or_paste()` is called here and by
                      the receipt gate: a spliced kind=style region is STYLE-PASTED and a page with
                      no live <link rel=stylesheet> to canon.css is CANON-NOT-LINKED. One
                      definition, two readers — the two checks agree by construction.
 11. NO DEMO WIDTH IN CANON — s258-D3 / s307-D75: canon.css (comments stripped) reads no
                      `--demo-width`; a showroom width dial is never a part's default.

Exits non-zero on any failure. Writes knowledge/_COMPOSE-AUDIT.md.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, sys, glob, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(HERE, "canon", "canon.css")
GEN = os.path.join(HERE, "..")  # generator lives in outputs at runtime; spine check is optional
RUNTIME_VARS = {"--pct", "--row-h"}   # --demo-width left at s307-D75 (#311 A1): check 11 refuses it
# s258-D3 (#258): `--<component>-max` are PAGE-OWNED width vars (s210-D3) — the snippet gives a
# 100%/px fallback, the showroom harness sets them inside its APOLLO-DEMO fence (never projected
# into canon since #258), and a composed page may set them. Unresolved in canon.css BY DESIGN.
def _is_runtime(v): return v in RUNTIME_VARS or v.endswith("-max")

def inline_scope_vars():
    """Scan snippet + composed HTML for inline style="--x:..." definitions
    (per-instance scope vars set on markup, e.g. style="--sc:var(--data-series-1)").
    These are invisible to a CSS-only scan of canon.css and must be resolved
    with a distinct provenance, never silently merged into canon.css's own defs
    (ds-010 / #101 finding: --sc false positive)."""
    found = set()
    paths = glob.glob(os.path.join(HERE, "snippets", "*.html")) + \
            glob.glob(os.path.join(HERE, "_fitness-test", "*.canon.html")) + \
            glob.glob(os.path.join(HERE, "_proforma", "*.html")) + \
            glob.glob(os.path.join(HERE, "_review", "*.html"))
    for p in paths:
        html = open(p, encoding="utf-8", errors="replace").read()
        for style_attr in re.findall(r'style="([^"]*)"', html):
            found |= set(re.findall(r'(--[\w-]+)\s*:', style_attr))
    return found

_COMMENT = re.compile(r"/\*.*?\*/", re.S)

def strip_css_comments(css):
    """Remove /* ... */ blocks before any var() analysis.

    PARSE IN THE CONSUMER'S GRAMMAR (#122 ds-039): the browser never sees comment
    text, so a `var(--x)` written inside PROSE is not a reference and a `--x:` inside
    prose is not a definition. This gate read the raw bytes, so canon.css's own
    hazard note — "`fill:var(--undefined)` does not fall back to the previous value"
    (canon.css, projected verbatim from Template-report.reference.html) — was counted
    as an unresolved reference and reddened the gate on a sentence. Stripping comments
    is strictly MORE accurate in both directions: it also stops a definition that only
    exists in a comment from resolving a real dangling ref.
    """
    return _COMMENT.sub(" ", css)

def check_canon():
    css = open(CANON).read()
    fails = []
    notes = []
    code = strip_css_comments(css)
    defs = set(re.findall(r'(--[\w-]+)\s*:', code))
    refs = set(re.findall(r'var\((--[\w-]+)', code))
    # #267 lane N — PARSE IN THE CONSUMER'S GRAMMAR (same discipline as strip_css_comments).
    # `var(--x, 380px)` is NOT an unresolved reference: the browser substitutes the fallback,
    # so the declaration renders exactly as authored. Only a BARE `var(--x)` with no definition
    # renders nothing. Measured when canon.css was regenerated from the #261 snippets: the three
    # newly-projected page-owned dials --dg-vh (Data-grid, `var(--dg-vh, 380px)`) and --ftb-top
    # (Filter-toolbar-bar, `var(--ftb-top,0px)`) turned this gate red although both carry a real
    # default — the s258-D3 `-max` allowance above is the same family, keyed on a name suffix
    # instead of on the grammar. A ref is exempt only if EVERY occurrence carries a fallback;
    # one bare use anywhere still fails (that is how --slot stayed red and got fixed at source).
    bare_refs = set(re.findall(r'var\(\s*(--[\w-]+)\s*\)', code))
    with_fallback_only = refs - bare_refs
    inline_defs = inline_scope_vars()
    missing = sorted(r for r in refs if r not in defs and not _is_runtime(r)
                     and r not in with_fallback_only)  # s258-D3 + #267 fallback grammar
    # split out vars resolved via inline-scope (set on markup, not in CSS) —
    # report as a distinct provenance, don't fold them into "defs" or silently drop them
    # (#101 finding: --sc is set inline in snippets, e.g. style="--sc:var(--data-series-1)",
    # invisible to a CSS-only scan ⇒ was a false positive, not a real unresolved var)
    inline_resolved = sorted(r for r in missing if r in inline_defs)
    missing = sorted(r for r in missing if r not in inline_defs)
    if inline_resolved:
        notes.append(f"canon.css: {len(inline_resolved)} var(s) resolved via inline-scope (set in snippet markup, not CSS): {inline_resolved[:8]}")
    if missing:
        fails.append(f"canon.css: {len(missing)} unresolved var(): {missing[:8]}")
    if css.count("{") != css.count("}"):
        fails.append(f"canon.css: unbalanced braces {css.count('{')}/{css.count('}')}")
    demo_reads = re.findall(r'var\(\s*--demo-width\b[^)]*\)', code)
    if demo_reads:
        fails.append(f"canon.css: {len(demo_reads)} read(s) of the showroom width dial --demo-width "
                     f"(s258-D3, s307-D75: a part's width is a real default, never a demo dial): "
                     f"{sorted(set(demo_reads))[:4]}")
    if "AUTO-GENERATED TOKENS START" not in css:
        fails.append("canon.css: token spine markers missing")
    return fails, notes, len(defs), len(refs)

# ---------- 9. NO SIZED PART (s305-D57 half A, s307-D75) ----------
SIZING_PROPS = re.compile(r"^(font-size|height|min-height|width|zoom|transform|padding(?:-[a-z-]+)?)$")
# The four hand-composed fitness screens that sized parts before check 9 existed, measured at
# #311 A1 (2026-10-01) on the tree at 148fa6fc. May only SHRINK. Named hits: the A1 report.
# Shrunk at the A1 second seat (21/8/12/1 -> 2/4/8/1) when the parts' own inline data API
# (_part_inline_api: fill widths, skeleton bone widths, link font-sizes) stopped counting as sizing.
# #313 A6: canon-gallery's 2 -> out of the ledger. Dave kept the page ("Keep and regenerate", s313-D46), so
# gen_gallery.py now shows the modal by canon's own `.overlay.open` instead of sizing it; the regenerated page
# sizes no part, and a pin it does not need would let two sizing rules come back unseen.
SIZING_LEDGER = {
    "nio-dash-console-v1.canon.html": 4,
    "nio-dash-console-v2.canon.html": 8,
    "payments-journey.canon.html": 1,
}
_SCOPES = None

def _canon_class_scopes():
    """class -> set of `.cn-*` scopes canon.css defines it under (None = unscoped). Cached."""
    global _SCOPES
    if _SCOPES is None:
        code = strip_css_comments(open(CANON, encoding="utf-8").read())
        m = {}
        for mm in re.finditer(r"([^{}]+)\{", code):
            sel = mm.group(1).strip()
            if sel.startswith("@"):
                continue
            for one in sel.split(","):
                sc = set(re.findall(r"\.(cn-[\w-]+)", one)) or {None}
                for c in re.findall(r"\.([A-Za-z_][\w-]*)", one):
                    if not c.startswith("cn-"):
                        m.setdefault(c, set()).update(sc)
        _SCOPES = m
    return _SCOPES

def _decl_props(body):
    return [d.split(":", 1)[0].strip().lower() for d in body.split(";") if ":" in d]

_PART_API = None

def _part_inline_api():
    """{(cn-scope, class, prop)}: the inline sizing a part's OWN reference snippet writes on its
    own markup — Meter's `.meter-fill` width, Progress-bar's `.pb-fill` width, Skeleton-loader's
    `.bone` widths, Links' `.arrow` font-size. That inline value IS the part's data API (a splice
    copies it byte-for-byte), so the page writing it is USING the part, not sizing it. Without this
    set check 9 would red a faithful splice — the very link/paste disagreement s307-D74 closed
    (#311 A1, second seat: 161 inline sizing declarations across 41 snippet (class, prop) pairs,
    measured on the 137 snippets). Scoped by the part, so `.bone` width is licensed only inside a
    `.cn-*` whose snippet writes it. Cached."""
    global _PART_API
    if _PART_API is None:
        api = set()
        for f in glob.glob(os.path.join(HERE, "snippets", "*.reference.html")):
            scope = "cn-" + re.sub(r"[^a-z0-9]+", "-",
                                   os.path.basename(f)[:-len(".reference.html")].lower()).strip("-")
            try:
                h = open(f, encoding="utf-8").read()
            except OSError:
                continue
            h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
            h = re.sub(r"<(script|style)\b.*?</\1>", "", h, flags=re.S | re.I)
            for m in re.finditer(r"<\w+\b([^>]*)>", h):
                attrs = m.group(1)
                st = re.search(r'\bstyle="([^"]*)"', attrs)
                cl = re.search(r'\bclass="([^"]*)"', attrs)
                if not (st and cl):
                    continue
                for x in _decl_props(st.group(1)):
                    if SIZING_PROPS.match(x):
                        for c in cl.group(1).split():
                            api.add((scope, c, x))
        _PART_API = api
    return _PART_API

def sized_parts(html):
    """-> list of human-readable hits: the page sizing a part (check 9). Never raises."""
    from html.parser import HTMLParser
    scopes_by_class = _canon_class_scopes()
    void = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param",
            "source", "track", "wbr"}

    class _P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.stack, self.part, self.inline = [], set(), []
        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            cls = (a.get("class") or "").split()
            scopes = (set().union(*self.stack) if self.stack else set()) | \
                     {c for c in cls if c.startswith("cn-")}
            pc = [c for c in cls if c.startswith(("cn-", "c-")) or
                  bool((scopes_by_class.get(c, set()) - {None}) & scopes)]
            self.part.update(pc)
            st = a.get("style") or ""
            if st and pc:
                api = _part_inline_api()
                sz = [x for x in _decl_props(st) if SIZING_PROPS.match(x) and
                      not any((sc, c, x) in api for sc in scopes for c in cls)]
                if sz:
                    self.inline.append(f'<{tag} class="{" ".join(cls)[:48]}" style="{",".join(sz)}">')
            if tag not in void:
                self.stack.append(scopes)
        def handle_startendtag(self, tag, attrs):
            self.handle_starttag(tag, attrs)
            if tag not in void and self.stack:
                self.stack.pop()
        def handle_endtag(self, tag):
            if tag not in void and self.stack:
                self.stack.pop()

    nocom = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    p = _P()
    try:
        p.feed(re.sub(r"<(script|style)\b.*?</\1>", "", nocom, flags=re.S | re.I))
    except Exception:
        pass
    hits = []
    style = strip_css_comments("".join(re.findall(r"<style\b[^>]*>(.*?)</style>", nocom, re.S | re.I)))
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", style):
        sel = m.group(1).strip()
        if sel.startswith("@"):
            continue
        sz = [x for x in _decl_props(m.group(2)) if SIZING_PROPS.match(x)]
        if not sz:
            continue
        for one in sel.split(","):
            subj = re.split(r"[\s>+~]+", one.strip())[-1]
            why = sorted(c for c in re.findall(r"\.([A-Za-z_][\w-]*)", subj)
                         if c.startswith(("cn-", "c-")) or c in p.part)
            if why:
                flat = re.sub(r"\s+", " ", one.strip())[:70]
                hits.append(flat + " {" + ",".join(sz) + "}")
                break
    return hits + p.inline

def check_screen(path):
    html = open(path).read()
    css_defs = set(re.findall(r'\.((?:c|cn)-[\w-]+)', open(CANON).read()))
    fails = []
    style = "".join(re.findall(r'<style>(.*?)</style>', html, re.S))
    # 4. rogue hex in <style> or inline
    style_hex = re.findall(r'#[0-9A-Fa-f]{3,8}\b', style)
    inline_hex = re.findall(r'style="[^"]*?(#[0-9A-Fa-f]{3,8})', html)
    if style_hex:  fails.append(f"{len(style_hex)} hex colour(s) in <style>: {style_hex[:5]}")
    if inline_hex: fails.append(f"{len(inline_hex)} inline hex colour(s): {inline_hex[:5]}")
    # 5. local redefinition of canon classes (component or pattern)
    redefs = re.findall(r'\.((?:c|cn)-[\w-]+)\s*\{', style)
    if redefs: fails.append(f"redefines canon class(es): {sorted(set(redefs))[:5]}")
    # 6. used canon classes resolve (c-/cn- prefixed; inner snippet classes are scope-resolved)
    used = set()
    for attr in re.findall(r'class="([^"]+)"', html):
        used |= {c for c in attr.split() if c.startswith("c-") or c.startswith("cn-")}
    unresolved = sorted(used - css_defs)
    if unresolved: fails.append(f"used but undefined: {unresolved}")
    # 7. don't reinvent reviewed components. Native form controls must compose the canon
    #    Selection-controls component (grey->ink radio/checkbox), never a native/accent-color one.
    # 9. the page never sizes a part (s305-D57 half A, s307-D75)
    sized = sized_parts(html)
    base = os.path.basename(path)
    pinned = SIZING_LEDGER.get(base) if os.path.dirname(os.path.abspath(path)) == \
        os.path.join(HERE, "_fitness-test") else None
    if sized and (pinned is None or len(sized) > pinned):
        fails.append(f"sizes a part — {len(sized)} rule(s) set size on a part"
                     + (f" (ledger pins {pinned})" if pinned is not None else "")
                     + f" (s305-D57, s307-D75: a page places parts, never sizes them): {sized[:4]}")
    if pinned is not None and len(sized) < pinned:
        print(f"ℹ️ {base}: sizes {len(sized)} part rule(s), ledger pins {pinned} — lower the pin "
              f"in SIZING_LEDGER (it may only shrink)")
    # 10. link, don't paste (s307-D74) — the receipt gate's own function, one definition
    try:
        import _validate_receipt as _VR
        for code, msg in _VR.link_or_paste(html):
            fails.append(f"{code}: {msg}")
    except ImportError as e:
        fails.append(f"LINK-CHECK-UNAVAILABLE: {e}")
    if re.search(r'accent-color', html):
        fails.append("uses accent-color (native control styling) — compose .cn-selection-controls instead")
    ctrls = re.findall(r'<input[^>]*type="(radio|checkbox)"', html)
    if ctrls and ("cn-selection-controls" not in html or 'class="radio"' not in html and 'class="box"' not in html):
        fails.append(f"{len(ctrls)} native radio/checkbox not composed from .cn-selection-controls (.radio/.box)")
    return fails, len(used)

def main():
    report = ["# Composition gate audit\n"]
    ok = True
    cfails, cnotes, ndef, nref = check_canon()
    report.append(f"## canon.css\n- defs {ndef}, var() refs {nref}")
    if cfails:
        ok = False
        for f in cfails: report.append(f"- ❌ {f}")
    else:
        report.append("- ✅ vars resolve, braces balanced, spine markers present")
    for n in cnotes:
        report.append(f"- ℹ️ {n}")
    screens = sorted(glob.glob(os.path.join(HERE, "_fitness-test", "*.canon.html")))
    report.append(f"\n## composed screens ({len(screens)})")
    for s in screens:
        fails, nused = check_screen(s)
        name = os.path.basename(s)
        if fails:
            ok = False
            report.append(f"- ❌ {name} ({nused} canon classes): " + "; ".join(fails))
        else:
            _pin = SIZING_LEDGER.get(name)
            report.append(f"- ✅ {name} — {nused} canon classes, 0 rogue hex, 0 redefines, all resolve, "
                          f"canon.css linked, nothing pasted, "
                          + (f"sized parts within the legacy pin {_pin}" if _pin else "0 sized parts"))
    # 8. unique <title> across the composed set (aca-003, blocking 2026-07-03)
    report.append(f"\n## screen titles (aca-003)")
    titles = {}
    tfails = 0
    for s in screens:
        name = os.path.basename(s)
        m = re.search(r'<title>(.*?)</title>', open(s).read(), re.S)
        t = m.group(1).strip() if m else ""
        if not t:
            ok = False; tfails += 1
            report.append(f"- ❌ {name}: missing/empty <title> (aca-003, SC 2.4.2)")
        elif t in titles:
            ok = False; tfails += 1
            report.append(f"- ❌ {name}: duplicate <title> \"{t}\" — also {titles[t]} (aca-003, SC 2.4.2)")
        else:
            titles[t] = name
    if not tfails:
        report.append(f"- ✅ {len(screens)} screen(s), every <title> present + unique")
    open(os.path.join(HERE, "_COMPOSE-AUDIT.md"), "w").write("\n".join(report) + "\n")
    print("\n".join(report))
    print("\nRESULT:", "PASS ✅" if ok else "FAIL ❌")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
