#!/usr/bin/env python3
"""Pro-forma GLYPH-PRESENCE gate (DEF-002) — enforces _PROFORMA-RULES.md rule 12: a glyph
must read against its own surface in EVERY state, never bound to a token equal (or
near-equal) to its surface. This is the recurring bug tracked as DEF-002 in
knowledge/_PROFORMA-DEFECTS.md (the checkbox-tick bug: fill="currentColor" resolved to
--ink sitting on the --pri near-black fill — dark-on-dark, invisible).

Mirrors the idiom of _validate_proforma.py: auto-discover knowledge/_proforma/*.html files
that carry an #icon-manifest, check each, print per-file PASS/FAIL (with every painted
pair's light/dark ratios + the min), write knowledge/_GLYPH-PRESENCE-GATE.md, sys.exit(1)
if any fail.

FLOOR = 1.3:1 (rule 12 "~1.3"). Uses knowledge/_contrast_utils.py's contrast_ratio().

Algorithm per file:
  1. Parse BOTH [data-theme="light"]{...} and [data-theme="dark"]{...} blocks -> token->hex
     maps (only opaque 6-digit hex; 8-digit/alpha and `transparent` are skipped).
  2. In the COMPONENT <style> (theme blocks stripped first), find every rule that sets a
     NON-transparent background/background-color:var(--Y) AND a glyph colour
     color:var(--X) (or fill:var(--X)) in the SAME declaration block — a painted
     glyph/ink-on-surface pair (svgs use currentColor = the box's `color`).
  3. For each pair, for each theme where both --X and --Y resolve to a hex, compute
     contrast_ratio(). If ratio < 1.3 in EITHER theme -> FAIL.
  4. Report every pair + its light/dark ratios + the min. A tranche with no painted glyph
     pair -> PASS.
"""
import re, os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROFORMA_DIR = os.path.join(HERE, "_proforma")
sys.path.insert(0, HERE)
from _contrast_utils import contrast_ratio

FLOOR = 1.3

RULE_RE = re.compile(r'([^{}]+)\{([^}]*)\}', re.S)
TOKEN_RE = re.compile(r'--([\w-]+)\s*:\s*([^;]+);')
HEX_RE = re.compile(r'^#[0-9A-Fa-f]{6}$')

# property boundary: not preceded by a word char or hyphen, so "background-color" never
# matches as a bare "color" property.
BG_RE = re.compile(r'(?<![\w-])background(?:-color)?\s*:\s*var\(--([\w-]+)')
COLOR_RE = re.compile(r'(?<![\w-])color\s*:\s*var\(--([\w-]+)')
FILL_RE = re.compile(r'(?<![\w-])fill\s*:\s*var\(--([\w-]+)')

def parse_theme_tokens(css_or_html):
    """Return (light_map, dark_map): token(no --) -> UPPERCASE hex, opaque 6-digit only."""
    def one(theme):
        m = re.search(r'\[data-theme="%s"\]\s*\{([^}]*)\}' % theme, css_or_html, re.S)
        if not m:
            return {}
        out = {}
        for name, val in TOKEN_RE.findall(m.group(1)):
            val = val.strip()
            if HEX_RE.match(val):
                out[name] = val.upper()
        return out
    return one("light"), one("dark")

def parse_rules(css):
    out = []
    for m in RULE_RE.finditer(css):
        sel_group, decl = m.group(1), m.group(2)
        out.append((sel_group.strip(), decl.strip()))
    return out

def find_painted_pairs(css):
    """Return dict (bg_token, glyph_token) -> list of representative selectors."""
    pairs = {}
    for sel, decl in parse_rules(css):
        bgm = BG_RE.search(decl)
        if not bgm:
            continue
        glm = COLOR_RE.search(decl) or FILL_RE.search(decl)
        if not glm:
            continue
        bg_tok, gl_tok = bgm.group(1), glm.group(1)
        pairs.setdefault((bg_tok, gl_tok), []).append(sel)
    return pairs

def check_file(path):
    html = open(path).read()
    fails, warns = [], []

    sm = re.search(r"<style>(.*?)</style>", html, re.S)
    if not sm:
        return (["no <style> block found — not a pro-forma surface?"], warns, [])
    full_css = sm.group(1)
    full_css = re.sub(r'/\*.*?\*/', '', full_css, flags=re.S)

    light_map, dark_map = parse_theme_tokens(full_css)

    # component css = theme blocks stripped
    css = re.sub(r'\[data-theme="(light|dark)"\]\s*\{[^}]*\}', '', full_css)

    pairs = find_painted_pairs(css)
    pair_reports = []
    for (bg_tok, gl_tok), selectors in sorted(pairs.items()):
        light_ratio = None
        dark_ratio = None
        if bg_tok in light_map and gl_tok in light_map:
            light_ratio = contrast_ratio(light_map[gl_tok], light_map[bg_tok])
        if bg_tok in dark_map and gl_tok in dark_map:
            dark_ratio = contrast_ratio(dark_map[gl_tok], dark_map[bg_tok])
        ratios = [r for r in (light_ratio, dark_ratio) if r is not None]
        min_ratio = min(ratios) if ratios else None
        rep_sel = re.sub(r'\s+', ' ', selectors[0]).strip()
        if len(rep_sel) > 90:
            rep_sel = rep_sel[:87] + "..."
        pair_reports.append({
            "bg": bg_tok, "glyph": gl_tok, "selector": rep_sel, "count": len(selectors),
            "light": light_ratio, "dark": dark_ratio, "min": min_ratio,
        })
        if light_ratio is not None and light_ratio < FLOOR:
            fails.append(
                "DEF-002: color:var(--%s) on background:var(--%s) = %s:1 in LIGHT (< %s floor) — %s"
                % (gl_tok, bg_tok, light_ratio, FLOOR, rep_sel))
        if dark_ratio is not None and dark_ratio < FLOOR:
            fails.append(
                "DEF-002: color:var(--%s) on background:var(--%s) = %s:1 in DARK (< %s floor) — %s"
                % (gl_tok, bg_tok, dark_ratio, FLOOR, rep_sel))
        if light_ratio is None and dark_ratio is None:
            warns.append(
                "pair --%s on --%s never resolves to opaque hex in either theme (skipped) — %s"
                % (gl_tok, bg_tok, rep_sel))

    return (fails, warns, pair_reports)

def main():
    files = sorted(f for f in glob.glob(os.path.join(PROFORMA_DIR, "*.html"))
                   if 'id="icon-manifest"' in open(f).read())
    lines = ["# Pro-forma glyph-presence gate (DEF-002) — report", "",
             "Enforces rule 12: a painted glyph/ink-on-surface pair (rule setting both a non-transparent",
             "`background:var(--Y)` and `color:var(--X)`/`fill:var(--X)` in the same declaration block)",
             "must read at >= %s:1 in BOTH themes. Computed via `_contrast_utils.contrast_ratio`." % FLOOR,
             ""]
    if not files:
        lines.append("No pro-forma tranche files found (nothing to gate). PASS.")
        open(os.path.join(HERE, "_GLYPH-PRESENCE-GATE.md"), "w").write("\n".join(lines) + "\n")
        print("glyph-presence gate: no tranche files found — PASS")
        return 0
    any_fail = False
    for path in files:
        name = os.path.relpath(path, HERE)
        fails, warns, pair_reports = check_file(path)
        status = "PASS" if not fails else "FAIL"
        if fails:
            any_fail = True
        print(f"  [{status}] {name}  ({len(pair_reports)} painted pair(s))")
        lines.append(f"## {'✓' if not fails else '✗'} {name} — {status}")
        if not pair_reports:
            print("     (no painted glyph/ink-on-surface pairs found)")
            lines.append("- no painted glyph/ink-on-surface pairs found")
        for pr in pair_reports:
            l = "n/a" if pr["light"] is None else f'{pr["light"]}:1'
            d = "n/a" if pr["dark"] is None else f'{pr["dark"]}:1'
            mn = "n/a" if pr["min"] is None else f'{pr["min"]}:1'
            msg = (f'  --{pr["glyph"]} on --{pr["bg"]}  light={l}  dark={d}  min={mn}'
                   f'  ({pr["count"]}x, e.g. {pr["selector"]})')
            print(" " + msg)
            lines.append(f"- {msg}")
        for w in warns:
            lines.append(f"- ⚠ {w}")
        for f in fails:
            print("     -", f)
            lines.append(f"- ✗ {f}")
        lines.append("")
    lines.append("---")
    lines.append("Floor: %s:1 (rule 12 \"~1.3\"). Below floor in either theme = FAIL (DEF-002)." % FLOOR)
    open(os.path.join(HERE, "_GLYPH-PRESENCE-GATE.md"), "w").write("\n".join(lines) + "\n")
    if any_fail:
        print("\n❌ pro-forma glyph-presence gate FAILED (DEF-002) — see knowledge/_GLYPH-PRESENCE-GATE.md")
        return 1
    print(f"\n✅ pro-forma glyph-presence gate passed ({len(files)} tranche file(s)).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
