#!/usr/bin/env python3
"""#219 — transplant the DV-D16 wording-② region delta into _proforma/DataViz-interactive.html.

⚠ WHY THIS EXISTS AND WHY IT IS NOT A HAND-EDIT. `_review/_gen_dataviz_charts.py` is the owning
generator and the DV-D16 change is made THERE. But the committed artefact is AHEAD of its own
generator (measured #219: 11 CSS lines diverge, and the body line is 80,384 chars on disk against
the 73,242 the generator produces — the #72 scatter fit-hook work plus a later ink/type pass,
neither back-ported). A blind regenerate would DELETE ~7KB of committed body and flip the dark
page ground from #1A1A1A to pure #000000, so it is refused; the back-port itself carries type and
ink calls that are not a lane's to make.

So the region delta is TRANSPLANTED, and the transplant is PROVEN equal to the generator:

    python3 knowledge/_render/apply_dv_d16_region_219.py --selftest
        apply_region(generator output BEFORE the change) == generator output AFTER it, byte for
        byte. If that equality fails this script is wrong and must not be run.

    python3 knowledge/_render/apply_dv_d16_region_219.py --selftest --apply <file.html>
        run the selftest, then apply the same delta to <file.html>. Idempotent.

The two CSS blocks are LIFTED from the generator's own output, never retyped, so they cannot drift
from it. The per-rect emission is re-derived from the artefact's own `height` attributes — the
same contract `build_stacked()` follows — so it cannot drift from the data either.

⛔ This is a one-shot bridge for a stale artefact, NOT a second generator. It is retired the moment
`_proforma/DataViz-interactive.html` is reconciled with `_gen_dataviz_charts.py`.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import argparse, importlib.util, os, re, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(ROOT, "_review", "_gen_dataviz_charts.py")

TOKEN_ANCHOR = "    --ease:160ms cubic-bezier(.4,0,.2,1); --grow:760ms cubic-bezier(.22,.61,.36,1);\n"
CSS_ANCHOR = "  .dv-tip.on{opacity:1; transform:translateY(0);}\n"
STACK_MARK = "  /* ---- DV-D16 wording ② · the stacked float."


# ---------------------------------------------------------------- the generator, both ways
def _gen_module():
    spec = importlib.util.spec_from_file_location("_gdc_219", GEN)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def generator_output(with_stack):
    """The generator's page, WITH or WITHOUT the DV-D16 block — from the live generator, so the
    'before' side is never a stored copy that could rot."""
    m = _gen_module()
    tmp = tempfile.mkdtemp(prefix="dvd16-")
    m.OUT = tmp
    if not with_stack:
        m.stack_css = lambda n: ""
        m.build_stacked = _wording_one(m)
    m.main()
    html = open(os.path.join(tmp, "DataViz-interactive.html"), encoding="utf-8").read()
    if not with_stack:
        html = _drop_tokens(html)
    return html


def _drop_tokens(html):
    """Remove the three DV-D16 timing tokens, so the 'before' page is the pre-#219 one in full."""
    lines = html.splitlines(keepends=True)
    i = lines.index(TOKEN_ANCHOR) + 1
    j = i
    while not lines[j].startswith("    --draw:"):
        j += 1
    if j == i:
        raise SystemExit("SELFTEST: the generator emits no DV-D16 token block to remove")
    return "".join(lines[:i] + lines[j:])


def _wording_one(m):
    """The pre-#219 emission — SERIAL wording ①, reconstructed so the selftest's 'before' is the
    real thing. It exists here and NOWHERE else: the generator no longer knows how to write it."""
    original = m.build_stacked

    def build(cid, title, caption, cats, series, chevron_idx=None):
        html = original(cid, title, caption, cats, series, chevron_idx)
        n = len(series)
        seq = {}
        def swap(mt):
            t = mt.group(0)
            g = int(re.search(r'data-series-group="(\d+)"', t).group(1))
            x = re.search(r'\sx="([^"]*)"', t).group(1)
            seq.setdefault(x, 0)
            tf = "ease-in" if g == 1 else ("ease-out" if g == n else "linear")
            old = ('style="animation-delay:%dms; animation-duration:400ms; '
                   'animation-timing-function:%s"' % ((g - 1) * 420, tf))
            return re.sub(r'style="[^"]*"', old, t, count=1)
        return re.sub(r'<rect class="dv-series" data-grow="up" data-series-group="\d+" '
                      r'style="[^"]*"[^>]*>(?:<title>.*?</title>)?</rect>', swap, html, flags=re.S)
    return build


# ---------------------------------------------------------------- the transplant
def blocks(after_txt):
    """The two pure-insert blocks, lifted from the generator's AFTER output."""
    lines = after_txt.splitlines(keepends=True)
    i = lines.index(TOKEN_ANCHOR)
    j = i + 1
    while not lines[j].startswith("    --draw:"):
        j += 1
    tokens = "".join(lines[i + 1:j])
    k = next(n for n, l in enumerate(lines) if l.startswith(STACK_MARK))
    m, depth = k, 0
    while True:
        if "@media" in lines[m]:
            depth = 1
        if depth and lines[m].rstrip("\n") == "  }":
            m += 1
            break
        m += 1
    stack = "".join(lines[k:m])
    if not tokens.strip() or not stack.strip():
        raise SystemExit("TRANSPLANT: an empty block was lifted — the generator's shape changed")
    return tokens, stack


def apply_region(html, tokens, stack):
    if STACK_MARK in html:
        return html                                             # idempotent
    for name, anchor in (("token", TOKEN_ANCHOR), ("css", CSS_ANCHOR)):
        if anchor not in html:
            raise SystemExit("TRANSPLANT: the %s anchor is not in this file" % name)
    html = html.replace(TOKEN_ANCHOR, TOKEN_ANCHOR + tokens, 1)
    html = html.replace(CSS_ANCHOR, CSS_ANCHOR + "\n" + stack, 1)

    fm = re.search(r'<figure class="dv" data-dv-type="stacked".*?</figure>', html, re.S)
    if not fm:
        raise SystemExit("TRANSPLANT: no figure[data-dv-type=\"stacked\"] in this file")
    fig = fm.group(0)
    rects = re.findall(r'<rect class="dv-series" data-grow="up" data-series-group="\d+" '
                       r'style="[^"]*"[^>]*>(?:<title>.*?</title>)?</rect>', fig, re.S)
    if len(rects) < 3:
        raise SystemExit("TRANSPLANT: only %d stacked rects — the rewrite would be vacuous" % len(rects))
    below, out = {}, fig
    for t in rects:
        x = re.search(r'\sx="([^"]*)"', t).group(1)
        g = int(re.search(r'data-series-group="(\d+)"', t).group(1))
        h = float(re.search(r'\sheight="([^"]*)"', t).group(1))
        col = below.setdefault(x, [])
        if g != len(col) + 1:
            raise SystemExit("TRANSPLANT: column x=%s: series-group %d arrived at depth %d — the "
                             "document order is not bottom-first and --b would be wrong"
                             % (x, g, len(col) + 1))
        bvars = "".join("--b%d:%.1fpx; " % (i + 1, hb) for i, hb in enumerate(col))
        new = re.sub(r'style="[^"]*"', 'style="%s--self:var(--dvf%d)"' % (bvars, g), t, count=1)
        out = out.replace(t, new, 1)
        col.append(h)
    return html.replace(fig, out, 1)


# ---------------------------------------------------------------- driver
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true",
                    help="prove the transplant equals the generator, byte for byte")
    ap.add_argument("--apply", nargs="*", default=[], help="files to transplant into")
    a = ap.parse_args()
    after = generator_output(with_stack=True)
    tokens, stack = blocks(after)

    if a.selftest or a.apply:
        before = generator_output(with_stack=False)
        if STACK_MARK in before:
            raise SystemExit("SELFTEST: the 'before' page already carries the block — vacuous")
        got = apply_region(before, tokens, stack)
        if got != after:
            for i, (p, q) in enumerate(zip(got.splitlines(), after.splitlines())):
                if p != q:
                    raise SystemExit("SELFTEST RED at line %d\n  transplant: %s\n  generator : %s"
                                     % (i + 1, p[:220], q[:220]))
            raise SystemExit("SELFTEST RED: %d bytes vs %d" % (len(got), len(after)))
        print("SELFTEST GREEN — transplant output is byte-identical to the generator's (%d bytes)"
              % len(after))
    if not a.selftest and not a.apply:
        raise SystemExit("nothing to do — pass --selftest and/or --apply <file>")
    for path in a.apply:
        src = open(path, encoding="utf-8").read()
        new = apply_region(src, tokens, stack)
        if new == src:
            print("unchanged (already applied):", path)
            continue
        open(path, "w", encoding="utf-8").write(new)
        print("applied region ->", path)


if __name__ == "__main__":
    main()
