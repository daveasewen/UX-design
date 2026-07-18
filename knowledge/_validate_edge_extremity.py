#!/usr/bin/env python3
"""_validate_edge_extremity.py — the reverse-text edge-extremity check ({#col26-020}).

ADVISORY (does not fail the build), following the {#dv-019} precedent: a perceptual rule
earns blocking status only after the library has been triaged against it.

THE RULE (thresholds set from Dave's observation 2026-07-18, specimen v1+v2 — not theory)
Where light/reverse text sits on a dark or saturated ground, legibility is degraded by the
EXTREMITY of the edge, not by insufficient contrast: the bright field blooms across the
boundary (halation/irradiation) and small text reads as though it vibrates. Adding contrast
makes it worse. Two levers by ground type, plus a size×weight floor:

  (a) COLOURED ground  -> saturation ceiling  <= 0.72
        Dave picked #B92F1E (0.72) as the first ladder step that reads clean; 0.78 / 0.84 /
        1.00 strain. This is the gate's number — the equivalent of dv-019's 135° hue leg.
  (b) NEUTRAL ground   -> use surface/digital-black (#1A1A1A, 17.4:1) not pure black
        (#000000, 21:1) WHERE REVERSE TEXT SITS ON IT. Pure black stays correct for borders,
        marks and rules carrying no reverse text — the substitution is conditional.
  (c) BOTH             -> minimum weight, which FALLS as size rises:
        <12px not permitted (off-ramp) · 12/14/16px Medium 500 · >=20px Light 300

DISTINCT FROM {#dv-019} — DO NOT MERGE. Vibrating boundaries needs TWO saturated
near-complementary colours at near-equal value; it scores white-on-red 0/3 legs and is right
to. Merging them would make dv-019 fire on pairs that do not shimmer while still missing
white-on-red. Verified 2026-07-18 against vibration() itself.

METHOD — same-rule pairing, as DEF-005 does for square exemption. A rule block that declares
BOTH a light `color` and a dark/saturated `background` is a reverse-text pair. Cross-rule
inheritance is NOT resolved (a static checker cannot); those are missed, not mis-reported.

Usage:  python3 knowledge/_validate_edge_extremity.py [file ...]
        python3 knowledge/_validate_edge_extremity.py --selftest
Exit 0 always (advisory). Wired into _build_all.py as an advisory step.
"""
import re, sys, os, glob, colorsys

SAT_CEILING = 0.72
PURE_BLACK = {"#000000", "#000"}
DIGITAL_BLACK = "#1A1A1A"
LIGHT_FG_LUM = 0.55          # a foreground this bright counts as "reverse text"
DARK_BG_LUM = 0.35           # a ground this dark counts as a dark ground
WEIGHT_FLOOR = [(12, 500), (20, 300)]   # <12 not permitted; 12-19 -> 500; >=20 -> 300

HEX = re.compile(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b")
BLOCK = re.compile(r"([^{}]*)\{([^{}]*)\}")
DECL = re.compile(r"([\w-]+)\s*:\s*([^;{}]+)")
CHROME = re.compile(r"\.demo|\bdemo-|harness|\.dossier|#rv-|\.rv-", re.I)


def norm(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h.upper()


def rgb(h):
    h = norm(h).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hsl(h):
    r, g, b = rgb(h)
    hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return hh * 360, s, l


def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    r, g, b = rgb(h)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def min_weight_for(size):
    if size < 12:
        return None                      # not permitted at all
    return 500 if size < 20 else 300


VARDEF = re.compile(r"(--[\w-]+)\s*:\s*(#[0-9A-Fa-f]{3,8})\b")
VARUSE = re.compile(r"var\(\s*(--[\w-]+)")


def var_map(css, theme="light"):
    """Resolve --x:#hex definitions so var() references can be checked.

    WITHOUT THIS THE GATE IS A LIAR. The snippets declare `background:var(--surface)`
    rather than a literal, so a checker that skips var() reports CLEAN on the very badge
    that motivated the rule. That is the declared-pairs blind spot that let Cards score
    9/9 with real failures (2026-06-22) — do not remove this.

    Light-mode definitions win: later blocks override, but a [data-theme="dark"] block
    must not overwrite the light value, so dark-scoped defs are collected separately.
    """
    light, dark = {}, {}
    for m in BLOCK.finditer(css):
        sel, body = m.group(1), m.group(2)
        target = dark if 'data-theme="dark"' in sel or "data-theme='dark'" in sel else light
        for v in VARDEF.finditer(body):
            target[v.group(1)] = norm(v.group(2)[:7])
    return dark if theme == "dark" else light


def resolve(val, vmap):
    """Return the first hex in val, following one level of var() indirection."""
    hx = HEX.findall(val)
    if hx:
        return norm(hx[0])
    u = VARUSE.search(val)
    if u and u.group(1) in vmap:
        return vmap[u.group(1)]
    return None


def check(css, name, theme="light"):
    """Return list of (code, selector, detail)."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    vmap = var_map(css, theme)
    out = []
    for m in BLOCK.finditer(css):
        sel = " ".join(m.group(1).split())[-80:]
        body = m.group(2)
        if CHROME.search(sel):
            continue
        fg = bgc = None
        size = weight = None
        for d in DECL.finditer(body):
            p, v = d.group(1).strip().lower(), d.group(2)
            if p.startswith("--"):
                continue                       # a definition, not a usage
            if p == "color":
                fg = resolve(v, vmap) or fg
            elif p in ("background", "background-color"):
                bgc = resolve(v, vmap) or bgc
            elif p == "font-size":
                s = re.search(r"(\d+\.?\d*)px", v)
                if s:
                    size = float(s.group(1))
            elif p == "font-weight":
                w = re.search(r"\b(\d{3})\b", v)
                if w:
                    weight = int(w.group(1))
            elif p == "font":
                w = re.match(r"\s*(\d{3})\b", v)
                if w:
                    weight = int(w.group(1))
                s = re.search(r"(\d+\.?\d*)px", v)
                if s:
                    size = float(s.group(1))
        if not (fg and bgc):
            continue
        if lum(fg) < LIGHT_FG_LUM:        # not reverse text
            continue
        _, sat, _l = hsl(bgc)
        is_dark = lum(bgc) <= DARK_BG_LUM

        # threshold is stated to 2dp (Dave picked "sat 0.72"), so compare at 2dp —
        # #B92F1E computes to 0.7200000…1 and must NOT trip its own ceiling.
        if sat > 0.05 and round(sat, 2) > SAT_CEILING:
            out.append(("EDGE-CHROMA", sel,
                        f"ground {bgc} sat {sat:.2f} > {SAT_CEILING} ceiling"))
        if sat <= 0.05 and bgc in PURE_BLACK:
            out.append(("EDGE-BLACK", sel,
                        f"pure black ground carrying reverse text — use "
                        f"surface/digital-black {DIGITAL_BLACK}"))
        if is_dark or round(sat, 2) > SAT_CEILING:
            if size is not None:
                floor = min_weight_for(size)
                if floor is None:
                    out.append(("EDGE-SIZE", sel,
                                f"{size:g}px reverse text — below the 12px floor, not permitted"))
                elif weight is not None and weight < floor:
                    out.append(("EDGE-WEIGHT", sel,
                                f"{size:g}px @ weight {weight} — floor is {floor} at this size"))
    return out


def read_css(p):
    t = open(p).read()
    if not p.lower().endswith((".html", ".htm")):
        return t
    parts = re.findall(r"<style[^>]*>(.*?)</style>", t, flags=re.S | re.I)
    parts += ["._inl{%s}" % s for s in re.findall(r'style="([^"]*)"', t)]
    return "\n".join(parts)


def run(paths):
    total = []
    for p in paths:
        try:
            v = check(read_css(p), os.path.relpath(p))
        except OSError:
            continue
        for code, sel, detail in v[:4]:
            print(f"  ~ {code}  {detail}  [{sel}]  ({os.path.relpath(p)})")
        if len(v) > 4:
            print(f"    … +{len(v)-4} more in {os.path.relpath(p)}")
        total += v
    if total:
        by = {}
        for c, *_ in total:
            by[c] = by.get(c, 0) + 1
        print(f"\nEDGE-EXTREMITY (advisory, {{#col26-020}}) — {len(total)} finding(s): "
              + " · ".join(f"{k} ×{v}" for k, v in sorted(by.items())))
        print("  advisory only — perceptual rule, blocking status after triage (dv-019 precedent)")
    else:
        print(f"EDGE-EXTREMITY (advisory) — clean across {len(paths)} file(s).")
    return 0


def selftest():
    bad_chroma = ".b{color:#FFFFFF;background:#DB0011;font-size:14px;font-weight:500;}"
    v = check(bad_chroma, "t")
    assert any(c == "EDGE-CHROMA" for c, *_ in v), v

    ok_chroma = ".b{color:#FFFFFF;background:#B92F1E;font-size:14px;font-weight:500;}"
    assert check(ok_chroma, "t") == [], check(ok_chroma, "t")

    pure = ".b{color:#FFFFFF;background:#000000;font-size:14px;font-weight:500;}"
    assert any(c == "EDGE-BLACK" for c, *_ in check(pure, "t")), check(pure, "t")

    dblack = ".b{color:#FFFFFF;background:#1A1A1A;font-size:14px;font-weight:500;}"
    assert check(dblack, "t") == [], check(dblack, "t")

    light_w = ".b{color:#FFFFFF;background:#1A1A1A;font-size:14px;font-weight:400;}"
    assert any(c == "EDGE-WEIGHT" for c, *_ in check(light_w, "t")), check(light_w, "t")

    big = ".b{color:#FFFFFF;background:#1A1A1A;font-size:20px;font-weight:300;}"
    assert check(big, "t") == [], "Light is permitted at 20px"

    tiny = ".b{color:#FFFFFF;background:#1A1A1A;font-size:10px;font-weight:500;}"
    assert any(c == "EDGE-SIZE" for c, *_ in check(tiny, "t")), check(tiny, "t")

    darktext = ".b{color:#333333;background:#FFBB33;font-size:14px;font-weight:500;}"
    assert check(darktext, "t") == [], "dark text on light ground is not reverse text"

    print(f"selftest OK — sat ceiling {SAT_CEILING} · pure-black substitution · "
          "weight floor 500@12-16 / 300@20+ / none <12 · dark-on-light ignored.")
    return 0


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TARGETS = (
    [os.path.join(HERE, "canon", "canon.css")]
    + sorted(glob.glob(os.path.join(HERE, "snippets", "*.html")))
    + sorted(glob.glob(os.path.join(HERE, "_proforma", "*.html")))
)

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        sys.exit(selftest())
    if args:
        sys.exit(run(args))
    selftest()
    run([p for p in DEFAULT_TARGETS if os.path.exists(p)])
    sys.exit(0)
