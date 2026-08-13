#!/usr/bin/env python3
"""_validate_type_composites.py — the type-composite gate (DEF-006).

Forces every component's text to be specified by a canon type COMPOSITE rather than
by raw font declarations. Sibling to _validate_grid.py (DEF-005): the grid gate snapped
DIMENSIONS, this one governs TEXT.

Dave 2026-07-17: "everything we produce should use these font rules … we need to hard
wire this."  Until a rule is gated, assume it will be broken.

THREE CHECKS (all blocking, component scope only)
  TYPE-001  every gated file pulls canon/type.css — either a <link> to it, or an inlined
            copy fenced by the sentinel markers (snippets are deliberately self-contained
            and portable, so inlining is the sanctioned form for them).
  TYPE-002  no raw font declarations in component-scope rules. Text is specified by a
            composite class: .t-cm-* (Component — single-line labels, cap-trim, 4px slot)
            or .t-ed-* (Editorial — wrapping prose, 4px line-heights).
            THE DECIDING RULE: single-line -> Component; wrapping -> Editorial. Multi-line
            Component text drifts off-grid (the N1 caveat), so wrapping text must be
            Editorial even when it looks like a label.
  TYPE-003  any surviving font-size/font-weight must be ON the canon ramp. Backstop for
            declarations that legitimately escape TYPE-002 (see EXEMPT).

SCOPE — component only (Dave ruling 2026-07-18)
  Demo-chrome selectors (.demo-controls and reference-page harness furniture) are NOT
  gated: that scaffolding never ships. Their raw declarations are COUNTED and reported as
  advisory, and the deferral is logged in _DS-IMPROVEMENTS.md so it is a known debt rather
  than a silent exemption. If chrome is ever brought into scope, drop CHROME_SEL.

EXEMPT
  - canon/type.css itself (it IS the source of truth — it must declare fonts).
  - the inlined type.css block inside a gated file, fenced by the sentinels.
  - @font-face blocks (glyph business, as in DEF-005).
  - custom-property DEFINITIONS (--font:…) on :root / [data-theme] — declaring a family
    token is fine; what's banned is components re-specifying size/weight/family per rule.
  - font-style, font-variant, font-feature-settings, font-smoothing (not ramp business).
  - font:inherit / font-family:inherit — inheriting is the desired behaviour.

Usage:  python3 knowledge/_validate_type_composites.py <file.html|file.css> [more ...]
        python3 knowledge/_validate_type_composites.py --selftest
        python3 knowledge/_validate_type_composites.py --inventory   # CSV of every fail
        python3 knowledge/_validate_type_composites.py               # DEF-006 build mode
Exit non-zero on any violation (blocking). Wired into _build_all.py as DEF-006.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re, sys, os, glob, csv

# ---- the canon ramp, read from type.css so this gate can never drift from the source ----
HERE = os.path.dirname(os.path.abspath(__file__))
TYPE_CSS = os.path.join(HERE, "canon", "type.css")

SENTINEL_OPEN = "APOLLO-TYPE-COMPOSITES"        # /* APOLLO-TYPE-COMPOSITES v1 — inlined from canon/type.css */
SENTINEL_CLOSE = "END-APOLLO-TYPE-COMPOSITES"   # /* END-APOLLO-TYPE-COMPOSITES */

# demo/harness scaffolding on reference pages — advisory, not gated (see SCOPE)
CHROME_SEL = re.compile(r"\.demo|\bdemo-|harness|\.dossier|\.swatch|\.spec-|#rv-|\.rv-", re.I)

FONT_PROPS = {"font", "font-size", "font-weight", "font-family"}
INHERITY = re.compile(r"^\s*(inherit|unset|initial|revert)\s*$", re.I)

BLOCK = re.compile(r"([^{}]*)\{([^{}]*)\}")
DECL = re.compile(r"([\w-]+)\s*:\s*([^;{}]+)")
PXSIZE = re.compile(r"(\d+\.?\d*)px")
NUMWEIGHT = re.compile(r"(?<![\w.-])([1-9]\d{2})(?![\w.%-])")


def canon_ramp():
    """Sizes + weights actually defined in canon/type.css. Never hardcode the ramp."""
    try:
        t = open(TYPE_CSS).read()
    except OSError:
        return {12, 14, 16, 20, 24, 28, 32, 40, 52}, {250, 300, 350, 400, 500}
    sizes = {float(x) for x in re.findall(r"font-size\s*:\s*(\d+\.?\d*)px", t)}
    weights = {int(x) for x in re.findall(r"font-weight\s*:\s*(\d+)", t)}
    return sizes, weights


SIZES, WEIGHTS = canon_ramp()


def strip_noise(css):
    css = re.sub(r"@font-face\s*\{.*?\}", "", css, flags=re.S)
    return css


def strip_inlined_composites(css):
    """Remove the fenced inlined type.css block — those declarations ARE the composites."""
    pat = re.compile(re.escape(SENTINEL_OPEN) + r".*?" + re.escape(SENTINEL_CLOSE), re.S)
    return pat.sub("", css)


def is_var_definition(prop):
    return prop.startswith("--")


def read_css(p):
    """CSS files: whole text. HTML: <style> blocks + inline style="" (never <script>)."""
    t = open(p).read()
    if not p.lower().endswith((".html", ".htm")):
        return t, t
    parts = re.findall(r"<style[^>]*>(.*?)</style>", t, flags=re.S | re.I)
    parts += ['._inl{%s}' % s for s in re.findall(r'style="([^"]*)"', t)]
    return "\n".join(parts), t


def links_type_css(raw, css):
    """TYPE-001 — a <link> to canon/type.css, or a sentinel-fenced inlined copy."""
    if re.search(r'<link[^>]+href=["\'][^"\']*type\.css', raw, re.I):
        return True
    return SENTINEL_OPEN in css and SENTINEL_CLOSE in css


def check(css, raw, name):
    """Returns (violations, chrome_count). violations = list of (code, sel, prop, val, name)."""
    css = strip_noise(css)
    body_css = strip_inlined_composites(css)
    body_css = re.sub(r"/\*.*?\*/", "", body_css, flags=re.S)
    viol, chrome = [], 0

    # TYPE-001 is scoped to HTML files ONLY (s166: Dave, 2026-08-13). A .css file has
    # no legal way to pull type.css — <link> is inert there, so the only way a
    # stylesheet ever "passed" was by an inert string in a comment (canon.css did
    # exactly that until #122 dropped it; the ratchet was blind until #164 revived
    # the build). A gate satisfied by MENTION is not a gate. CSS files remain fully
    # gated by TYPE-002/TYPE-003.
    if name.lower().endswith((".html", ".htm")) and not links_type_css(raw, css):
        viol.append(("TYPE-001", "(file)", "-", "does not pull canon/type.css", name))

    for bm in BLOCK.finditer(body_css):
        sel = " ".join(bm.group(1).split())[-90:]
        body = bm.group(2)
        is_chrome = bool(CHROME_SEL.search(sel))
        for m in DECL.finditer(body):
            prop, val = m.group(1).strip().lower(), m.group(2).strip()
            if prop not in FONT_PROPS or is_var_definition(prop):
                continue
            if INHERITY.match(val):
                continue
            if is_chrome:
                chrome += 1
                continue
            # TYPE-002 — a raw font declaration in component scope
            viol.append(("TYPE-002", sel, prop, val, name))
            # TYPE-003 — and is it even on the ramp?
            for s in PXSIZE.findall(val):
                if float(s) not in SIZES:
                    viol.append(("TYPE-003", sel, prop, s + "px (off-ramp)", name))
            if prop in ("font-weight", "font"):
                for w in NUMWEIGHT.findall(val):
                    if int(w) not in WEIGHTS:
                        viol.append(("TYPE-003", sel, prop, w + " (off-ramp weight)", name))
    return viol, chrome


def run(paths, inventory=False):
    total, chrome_total, files_ok = [], 0, 0
    for p in paths:
        if os.path.abspath(p) == os.path.abspath(TYPE_CSS):
            continue  # the source of truth declares fonts by definition
        try:
            css, raw = read_css(p)
        except OSError as e:
            print(f"  ! cannot read {p}: {e}")
            total.append(("READ", "-", "-", str(e), p))
            continue
        v, ch = check(css, raw, os.path.relpath(p))
        chrome_total += ch
        if not v:
            files_ok += 1
        total += v
        if not inventory:
            for code, sel, prop, val, where in v[:6]:
                print(f"  ✗ {code}  {prop}: {val}  [{sel}]  ({where})")
            if len(v) > 6:
                print(f"    … +{len(v)-6} more in {os.path.relpath(p)}")

    if inventory:
        w = csv.writer(sys.stdout)
        w.writerow(["code", "file", "selector", "property", "value"])
        for code, sel, prop, val, where in total:
            w.writerow([code, where, sel, prop, val])
        return 0

    n_files = len([p for p in paths if os.path.abspath(p) != os.path.abspath(TYPE_CSS)])
    print(f"\n  advisory — {chrome_total} raw font decl(s) in demo-chrome scope "
          f"(not gated; logged in _DS-IMPROVEMENTS.md)")
    if total:
        by = {}
        for code, *_ in total:
            by[code] = by.get(code, 0) + 1
        summary = " · ".join(f"{k} ×{v}" for k, v in sorted(by.items()))
        print(f"TYPE GATE FAIL — {len(total)} violation(s) across "
              f"{n_files - files_ok}/{n_files} file(s).  {summary}")
        return 1
    print(f"TYPE GATE PASS — all component text bound to canon composites ({n_files} file(s)).")
    return 0


def selftest():
    good = ("/* %s v1 */ .t-cm-label{font-size:16px;font-weight:400;} /* %s */\n"
            ".cn-btn .txt{color:#333;}" % (SENTINEL_OPEN, SENTINEL_CLOSE))
    v, _ = check(good, good, "good")
    assert v == [], f"clean composite-bound case should pass, got {v}"

    bad = "/* %s */.t-cm-label{font-size:16px;}/* %s */\n.cn-badge{font:700 13px/1 var(--font);}" % (
        SENTINEL_OPEN, SENTINEL_CLOSE)
    v, _ = check(bad, bad, "bad")
    codes = sorted({c for c, *_ in v})
    assert codes == ["TYPE-002", "TYPE-003"], f"expected raw+off-ramp, got {codes} / {v}"

    nolink = ".cn-x{color:red;}"
    v, _ = check(nolink, nolink, "nolink.html")
    assert v and v[0][0] == "TYPE-001", f"missing type.css must fail TYPE-001, got {v}"

    # s166 scope: a .css file CANNOT pull type.css (no legal form), so TYPE-001
    # must NOT fire on it — but TYPE-002/003 still must. Both directions asserted.
    v, _ = check(nolink, nolink, "nolink.css")
    assert not any(c == "TYPE-001" for c, *_ in v), f"TYPE-001 must not fire on .css, got {v}"
    cssraw = ".cn-badge{font:700 13px/1 var(--font);}"
    v, _ = check(cssraw, cssraw, "raw.css")
    assert any(c == "TYPE-002" for c, *_ in v), f".css must still fail TYPE-002, got {v}"

    ch = "/* %s */.t{font-size:16px;}/* %s */\n.demo-controls button{font-size:13px;}" % (
        SENTINEL_OPEN, SENTINEL_CLOSE)
    v, c = check(ch, ch, "chrome")
    assert v == [] and c == 1, f"chrome must be advisory-only, got viol={v} chrome={c}"

    var = "/* %s */.t{font-size:16px;}/* %s */\n:root{--font:Univers,sans-serif;}" % (
        SENTINEL_OPEN, SENTINEL_CLOSE)
    v, _ = check(var, var, "var")
    assert v == [], f"custom-property definitions are exempt, got {v}"

    print(f"selftest OK — ramp from type.css: sizes {sorted(SIZES)} weights {sorted(WEIGHTS)}; "
          "catches raw decls + off-ramp; exempts chrome/vars/inherit/sentinel block.")
    return 0


DEFAULT_TARGETS = (
    [os.path.join(HERE, "canon", "canon.css")]
    + sorted(glob.glob(os.path.join(HERE, "snippets", "*.html")))
    + sorted(glob.glob(os.path.join(HERE, "_proforma", "*.html")))
)

RATCHET_FILE = os.path.join(HERE, "_type_ratchet.json")


def run_ratchet(paths):
    """Tier (b) — SHRINK-ONLY RATCHET, ruled by Dave #119 (2026-08-07).

    Enforces today against any NEW violation; existing debt is DECLARED in
    _type_ratchet.json and may only shrink. Named risk (put to Dave, accepted):
    a baseline set to today's count has the shape of "a cap raised to clear its
    own gate" — the claimed difference is it may ONLY shrink and is carried as
    declared debt, never absorbed as a pass. The baseline was MEASURED at wiring,
    not copied from _HANDOFF-118 (whose 1,101 was a dated measurement).
    """
    import io, json
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        run(paths)
    finally:
        sys.stdout = real
    # count from the SUMMARY line only — per-violation ✗ lines truncate at 6/file
    count = _ratchet_count_from_summary(buf.getvalue())
    with open(RATCHET_FILE, encoding="utf-8") as f:
        state = json.load(f)
    base = state["baseline"]
    if count > base:
        print(f"TYPE RATCHET FAIL — {count} violation(s) > declared debt {base}. "
              f"{count - base} NEW violation(s); the ratchet only shrinks.")
        return 1
    if count < base:
        state["baseline"] = count
        state["shrunk"] = f"{base} -> {count} on {__import__('datetime').date.today()}"
        with open(RATCHET_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        print(f"TYPE RATCHET PASS — debt shrank {base} -> {count}; baseline ratcheted down.")
        return 0
    print(f"TYPE RATCHET PASS — declared debt holds at {base} (0 new). "
          f"This is DEBT, not a pass of the underlying gate.")
    return 0


def _ratchet_count_from_summary(text):
    import re as _re
    m = _re.search(r"TYPE GATE FAIL — (\d+) violation", text)
    return int(m.group(1)) if m else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        sys.exit(selftest())
    if args and args[0] == "--ratchet":
        sys.exit(run_ratchet([p for p in DEFAULT_TARGETS if os.path.exists(p)]))
    if args and args[0] == "--inventory":
        rest = args[1:] or [p for p in DEFAULT_TARGETS if os.path.exists(p)]
        sys.exit(run(rest, inventory=True))
    if args:
        sys.exit(run(args))
    rc = selftest()
    rc = run([p for p in DEFAULT_TARGETS if os.path.exists(p)]) or rc
    sys.exit(rc)
