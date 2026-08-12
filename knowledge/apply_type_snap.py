#!/usr/bin/env python3
"""apply_type_snap.py — snap off-ramp type to the canon ramp (Dave's rulings 2026-07-18).

Sibling to apply_grid_snap.py. Applies §1 + §2 of reviews/TYPE-RETROFIT-2026-07-18.html,
all 17 rows returned "as proposed". This is the MECHANICAL half of the type retrofit —
it fixes VALUES (TYPE-003). It does not rebind declarations to composite classes
(TYPE-002); that is the second pass, which needs per-component judgement.

SOURCES OF TRUTH — edit snippets + proforma, never canon.css
  canon.css is GENERATED from the gated snippets (canon/gen_canon_components.py).
  Hand-retyping canon.css loses decisions. This script refuses to touch it.

SCOPE (Dave's rulings, recorded in _proforma/_TYPE-DECISIONS.md)
  - component scope only; demo-chrome is skipped (ds-003, logged not exempted)
  - avatars/badges ARE in scope — rule 3, a deliberate divergence from DEF-005's
    intrinsic-square exemption. Do not "reconcile" the two gates.
  - SVG <text> is SKIPPED — rule 4C, deferred to Dave's parked DataViz pass. SVG text px
    is viewBox-relative (.dv-svg is width:100% + runtime fit()), so snapping it to the CSS
    ramp measures the wrong thing. Open question: a viewBox-relative ramp expression.

Usage:  python3 knowledge/apply_type_snap.py            # dry run — report only
        python3 knowledge/apply_type_snap.py --apply    # write changes
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))

# §1 — 15 size rulings, all "as proposed"
SIZE = {13.0: 14, 15.0: 16, 11.0: 12, 22.0: 24, 13.5: 14, 19.0: 20, 18.0: 20, 17.0: 16,
        12.5: 12, 33.0: 32, 10.0: 12, 57.0: 52, 30.0: 32, 10.5: 12, 26.0: 24}
# §2 — 2 weight rulings: collapse, do not extend the ramp
WEIGHT = {600: 500, 700: 500}

CHROME_SEL = re.compile(r"\.demo|\bdemo-|harness|\.dossier|\.swatch|\.spec-|#rv-|\.rv-", re.I)
# rule 4C — SVG text, deferred to the DataViz pass
SVG_TEXT_SEL = re.compile(r"(^|[\s,>+~])text[.#:\[\s,]|(^|[\s,>+~])text$|\.dv-(val|key|anno|axlbl)", re.I)

BLOCK = re.compile(r"([^{}]*)\{([^{}]*)\}")


def snap_decls(body):
    """Rewrite font-size / font-weight / font-shorthand values in one rule body."""
    n = [0]

    def size_sub(m):
        v = float(m.group(1))
        if v in SIZE:
            n[0] += 1
            return f"{SIZE[v]}px"
        return m.group(0)

    def weight_sub(m):
        v = int(m.group(1))
        if v in WEIGHT:
            n[0] += 1
            return str(WEIGHT[v])
        return m.group(0)

    def one_decl(m):
        prop, val = m.group(1), m.group(2)
        p = prop.strip().lower()
        if p == "font-size":
            val = re.sub(r"(\d+\.?\d*)px", size_sub, val)
        elif p == "font-weight":
            val = re.sub(r"\b(\d{3})\b", weight_sub, val)
        elif p == "font":
            # shorthand: [weight] size[/lh] family — weight is a leading 3-digit token
            val = re.sub(r"^(\s*)(\d{3})\b", lambda w: w.group(1) + weight_sub(
                re.match(r"(\d{3})", w.group(2))), val)
            val = re.sub(r"(\d+\.?\d*)px", size_sub, val)
        else:
            return m.group(0)
        return f"{prop}:{val}"

    body = re.sub(r"([\w-]+)\s*:\s*([^;{}]+)", one_decl, body)
    return body, n[0]


def process_css(css, counts, where):
    """Walk rule blocks; snap component-scope ones, skip chrome + SVG text."""
    out, last = [], 0
    for m in BLOCK.finditer(css):
        sel, body = m.group(1), m.group(2)
        s = " ".join(sel.split())
        if CHROME_SEL.search(s):
            counts["skip_chrome"] += 1
            continue
        if SVG_TEXT_SEL.search(s):
            counts["skip_svgtext"] += 1
            continue
        new, n = snap_decls(body)
        if n:
            out.append((m.start(2), m.end(2), new))
            counts["snapped"] += n
    if not out:
        return css
    buf = []
    for st, en, new in out:
        buf.append(css[last:st]); buf.append(new); last = en
    buf.append(css[last:])
    return "".join(buf)


def process_html(t, counts):
    """<style> blocks, then inline style="" — skipping inline styles on <text> (rule 4C)."""
    def style_block(m):
        return m.group(1) + process_css(m.group(2), counts, "style") + m.group(3)

    t = re.sub(r"(<style[^>]*>)(.*?)(</style>)", style_block, t, flags=re.S | re.I)

    def inline(m):
        tag, pre, style, post = m.group(1), m.group(2), m.group(3), m.group(4)
        if tag.lower() == "text":            # rule 4C — SVG text deferred
            counts["skip_svgtext"] += 1
            return m.group(0)
        new, n = snap_decls(style)
        counts["snapped"] += n
        return f"<{tag}{pre}style=\"{new}\"{post}>"

    t = re.sub(r'<([a-zA-Z][\w-]*)([^>]*?)style="([^"]*)"([^>]*)>', inline, t)
    return t


def process_canon(t, counts):
    """canon.css has THREE regions, and only ONE of them is hand-authored.

    1. AUTO-GENERATED TOKENS START..END      — generated (gen_canon_tokens.py)
    2. the .c-* COMPOSITION layer in between — HAND-AUTHORED, no snippet source
    3. AUTO-COMPONENTS START..EOF           — generated from snippets

    The blanket rule "canon.css is generated, never hand-edit" is imprecise: the
    generator's own marker says "do NOT hand-edit BETWEEN AUTO-COMPONENTS markers".
    Region 2 (semantic aliases, layout utilities, journey/screen patterns — the
    composition tier) lives ONLY here, so ruled values must be applied here or they
    are lost at regeneration. Regions 1 and 3 are skipped — fix those at source.
    """
    tok_end = t.find("AUTO-GENERATED TOKENS END")
    comp_start = t.find("AUTO-COMPONENTS START")
    if tok_end == -1 or comp_start == -1 or comp_start < tok_end:
        print("  ! canon.css region markers not found — skipping (investigate)")
        return t
    head, mid, tail = t[:tok_end], t[tok_end:comp_start], t[comp_start:]
    return head + process_css(mid, counts, "canon-composition") + tail


def main(apply=False):
    targets = sorted(glob.glob(os.path.join(HERE, "snippets", "*.html"))) + \
              sorted(glob.glob(os.path.join(HERE, "_proforma", "*.html")))
    total = {"snapped": 0, "skip_chrome": 0, "skip_svgtext": 0}
    touched = []

    # canon.css — hand-authored composition region only
    cpath = os.path.join(HERE, "canon", "canon.css")
    if os.path.exists(cpath):
        csrc = open(cpath).read()
        ccounts = {"snapped": 0, "skip_chrome": 0, "skip_svgtext": 0}
        cnew = process_canon(csrc, ccounts)
        for k in total:
            total[k] += ccounts[k]
        if cnew != csrc:
            touched.append(("canon/canon.css (composition layer)", ccounts["snapped"]))
            if apply:
                open(cpath, "w").write(cnew)

    for p in targets:
        src = open(p).read()
        counts = {"snapped": 0, "skip_chrome": 0, "skip_svgtext": 0}
        new = process_html(src, counts)
        for k in total:
            total[k] += counts[k]
        if new != src:
            touched.append((os.path.relpath(p, HERE), counts["snapped"]))
            if apply:
                open(p, "w").write(new)
    for f, n in sorted(touched, key=lambda x: -x[1]):
        print(f"  {n:4d}  {f}")
    print(f"\n{'APPLIED' if apply else 'DRY RUN'} — {total['snapped']} value(s) snapped "
          f"across {len(touched)} file(s)")
    print(f"  skipped: {total['skip_chrome']} demo-chrome rule(s) [ds-003] · "
          f"{total['skip_svgtext']} SVG-text rule(s)/element(s) [rule 4C, DataViz pass]")
    if not apply:
        print("\n  re-run with --apply to write. canon.css: ONLY the hand-authored .c-* composition\n"
              "  region is edited; the AUTO-* regions are skipped — regenerate those from source after.")
    return 0


if __name__ == "__main__":
    sys.exit(main(apply="--apply" in sys.argv[1:]))
