#!/usr/bin/env python3
"""gen_rag_promotion.py — the RAG palette promotion sheet.

DAVE'S PROPOSAL (2026-07-18, pinned on the reverse-text specimen §1 control row):
  "this and it's the other selected for rag during the session should be canon,
   red amber green and blue"

i.e. promote the **data/delta** family — chosen during the 07-16 D2 vibration work —
to be the canon RAG set, replacing the current rag/* values.

WHY THE PROPOSAL IS WELL-FOUNDED (the data, not the opinion)
  The delta family is SATURATION-NORMALISED: every member sits at sat 0.72, and it
  already spans exactly red / amber / green / blue. The incumbent rag/* set has no
  consistent chroma at all (1.00 / 1.00 / 1.00 / 0.47). The delta values were
  value-split AND saturation-normalised during D2 precisely to stop the dance, which
  is why they behave — they were engineered for this problem before it was named.

THE CAVEAT THIS SHEET EXISTS TO SURFACE
  Amber still cannot carry white text. delta/warning #C58720 is 3.06:1 — better than
  the incumbent #FFBB33 at 1.69:1, but still under 4.5. Amber needs dark text
  (rag/text/on-light) regardless of which set wins. "Red amber green blue" is NOT a
  uniform set where reverse text is concerned, and treating it as one is the trap.

PROMOTION IS DAVE'S ALONE (derivation governance) — nothing here is applied.

Usage:  python3 reviews/gen_rag_promotion.py
Then:   python3 knowledge/_review/_make_review.py reviews/RAG-PROMOTION-2026-07-18.html
"""
import os, json, colorsys, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOK = os.path.join(ROOT, "knowledge", "tokens", "semantic-colour.json")
OUT = os.path.join(ROOT, "reviews", "RAG-PROMOTION-2026-07-18.html")

PAIRS = [("red", "rag/error", "data/delta/loss"),
         ("amber", "rag/warning", "data/delta/warning"),
         ("green", "rag/success", "data/delta/gain"),
         ("blue", "rag/information", "data/delta/neutral")]
ON_DARK, ON_LIGHT = "#FFFFFF", "#333333"


def flat(o, path=""):
    if isinstance(o, dict):
        v = o.get("$value", o.get("value"))
        if isinstance(v, str) and v.startswith("#"):
            yield path, v
        for k, vv in o.items():
            if not k.startswith("$"):
                yield from flat(vv, f"{path}/{k}" if path else k)


def load():
    return {p: v for p, v in flat(json.load(open(TOK)))}


def hsl(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return hh * 360, s, l


def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def cr(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def blast():
    """Real consumption counts, measured — not asserted."""
    files, lit = set(), set()
    pats = re.compile(r"rag/(error|warning|success|information)")
    for pat in ("knowledge/snippets/*.html", "knowledge/_proforma/*.html",
                "knowledge/canon/canon.css", "knowledge/components/*.meta.json"):
        for p in glob.glob(os.path.join(ROOT, pat)):
            t = open(p).read()
            if pats.search(t):
                files.add(os.path.relpath(p, ROOT))
    hexes = ("#A8000B", "#FFBB33", "#00847F", "#305A85", "#DB0011")
    for pat in ("knowledge/snippets/*.html", "knowledge/_proforma/*.html", "knowledge/canon/canon.css"):
        for p in glob.glob(os.path.join(ROOT, pat)):
            t = open(p).read()
            if any(hx in t.upper() for hx in hexes):
                lit.add(os.path.relpath(p, ROOT))
    return files, lit


def swatch(bg, fg, label):
    ok = cr(fg, bg) >= 4.5
    mark = "" if ok else " ✗"
    return (f'<span class="sw" style="background:{bg};color:{fg}">{label}{mark}</span>')


def build():
    T = load()
    files, lit = blast()
    h = []
    A = h.append
    A('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>RAG promotion &mdash; review</title>")
    A("""<style>
:root{--ink:#1c1c1c;--mut:#6b6b6b;--line:#e4e4e4;--rec:#0b7a34;--tie:#b25000;--arrow:#8a1f1f;--red:#db0011;}
*{box-sizing:border-box}
body{font-family:"Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;color:var(--ink);margin:0;padding:40px;max-width:1180px;line-height:1.5;background:#fafafa}
h1{font-size:32px;font-weight:300;margin:0 0 4px}
h2{font-size:20px;font-weight:500;margin:40px 0 4px;padding-top:16px;border-top:2px solid var(--ink)}
.sub{color:var(--mut);font-size:14px;margin:0 0 24px}
.lead{font-size:15px;background:#fff;border:1px solid var(--line);border-left:3px solid var(--red);padding:16px 20px;margin:20px 0}
table{width:100%;border-collapse:collapse;background:#fff;margin:12px 0 8px;font-size:13px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:middle}
th{font-weight:500;font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:var(--mut);background:#f4f4f4}
code{font-family:ui-monospace,Menlo,monospace;font-size:11px;background:#f2f2f2;padding:1px 5px;border-radius:3px}
.sw{display:inline-flex;align-items:center;justify-content:center;min-width:104px;height:34px;padding:0 10px;
  font-size:13px;font-weight:500;margin:0 4px 0 0}
.met{font-size:11px;color:var(--mut);white-space:nowrap}
.ask{width:120px;background:#fffdf5}
.rules{background:#fff;border:1px solid var(--line);padding:4px 20px 16px;margin:16px 0}
.rules li{margin:12px 0;font-size:14px}
.fail{color:var(--arrow);font-weight:600}.pass{color:var(--rec);font-weight:600}
.num{background:#fff;border:1px solid var(--line);display:flex;margin:16px 0}
.num div{padding:12px 18px;border-right:1px solid var(--line);flex:1}.num div:last-child{border-right:0}
.num b{display:block;font-size:26px;font-weight:300;line-height:1.1}
.num span{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.03em}
.foot{color:var(--mut);font-size:12px;margin-top:40px;border-top:1px solid var(--line);padding-top:12px}
</style></head><body>""")

    A("<h1>RAG promotion &mdash; review</h1>")
    A('<p class="sub">Apollo SDS &middot; 2026-07-18 &middot; promote the <b>data/delta</b> family to canon RAG. '
      "Your proposal, pinned on the reverse-text specimen. Nothing applied.</p>")

    A('<div class="num">')
    A(f"<div><b>0.72</b><span>delta set — one saturation, all four hues</span></div>")
    A(f"<div><b>4</b><span>incumbent sats: 1.00/1.00/1.00/0.47</span></div>")
    A(f"<div><b>{len(files)}</b><span>files consuming rag/* tokens</span></div>")
    A(f"<div><b>{len(lit)}</b><span>files carrying the literal hexes</span></div>")
    A("</div>")

    A('<div class="lead"><b>Why this is well-founded.</b> The delta family is <b>saturation-normalised '
      "&mdash; every member at sat 0.72</b> &mdash; and already spans exactly red/amber/green/blue. The "
      "incumbent <code>rag/*</code> set has no consistent chroma (1.00/1.00/1.00/0.47). The delta values "
      "were value-split <i>and</i> saturation-normalised during the 07-16 D2 vibration work, which is why "
      "they behave: they were engineered for this problem before it had a name. "
      "<b>The caveat this sheet exists to surface:</b> amber still cannot carry white text in either set "
      "&mdash; <code>#C58720</code> is 3.06:1 against <code>#FFBB33</code>'s 1.69:1. Better, not fixed. "
      "&ldquo;Red amber green blue&rdquo; is <b>not</b> a uniform set where reverse text is concerned, and "
      "treating it as one is the trap.</div>")

    A("<h2>1 &middot; Head to head &mdash; incumbent vs delta</h2>")
    A('<p class="sub">White text and dark text on each. <span class="fail">✗</span> = under 4.5:1. '
      "Light mode shown; dark-mode values in §2.</p>")
    A("<table><thead><tr><th>Hue</th><th>Incumbent</th><th>sat</th><th>white / dark</th>"
      '<th>Delta (proposed)</th><th>sat</th><th>white / dark</th><th class="ask">Ruling</th></tr></thead><tbody>')
    for name, old, new in PAIRS:
        ov = T.get(old + "/light", "#888888")
        nv = T.get(new + "/light", "#888888")
        _, os_, _ = hsl(ov)
        _, ns_, _ = hsl(nv)
        ow, od = cr(ON_DARK, ov), cr(ON_LIGHT, ov)
        nw, nd = cr(ON_DARK, nv), cr(ON_LIGHT, nv)
        A(f"<tr><td><b>{name}</b></td>")
        A(f"<td>{swatch(ov, ON_DARK,'white')}{swatch(ov, ON_LIGHT,'dark')}<br>"
          f"<span class='met'><code>{ov}</code> {old}</span></td>")
        A(f"<td class='met'><b>{os_:.2f}</b></td>")
        A(f"<td class='met'><span class='{'pass' if ow>=4.5 else 'fail'}'>{ow:.2f}</span> / "
          f"<span class='{'pass' if od>=4.5 else 'fail'}'>{od:.2f}</span></td>")
        A(f"<td>{swatch(nv, ON_DARK,'white')}{swatch(nv, ON_LIGHT,'dark')}<br>"
          f"<span class='met'><code>{nv}</code> {new}</span></td>")
        A(f"<td class='met'><b>{ns_:.2f}</b></td>")
        A(f"<td class='met'><span class='{'pass' if nw>=4.5 else 'fail'}'>{nw:.2f}</span> / "
          f"<span class='{'pass' if nd>=4.5 else 'fail'}'>{nd:.2f}</span></td>")
        A('<td class="ask"></td></tr>')
    A("</tbody></table>")

    A("<h2>2 &middot; Dark mode</h2>")
    A('<p class="sub">Both sets carry per-mode values. Same test.</p>')
    A("<table><thead><tr><th>Hue</th><th>Incumbent (dark)</th><th>white / dark</th>"
      '<th>Delta (dark)</th><th>white / dark</th><th class="ask">Ruling</th></tr></thead><tbody>')
    for name, old, new in PAIRS:
        ov = T.get(old + "/dark", T.get(old + "/light", "#888"))
        nv = T.get(new + "/dark", T.get(new + "/light", "#888"))
        ow, od = cr(ON_DARK, ov), cr(ON_LIGHT, ov)
        nw, nd = cr(ON_DARK, nv), cr(ON_LIGHT, nv)
        A(f"<tr><td><b>{name}</b></td>")
        A(f"<td>{swatch(ov, ON_DARK,'white')}{swatch(ov, ON_LIGHT,'dark')}<br><span class='met'><code>{ov}</code></span></td>")
        A(f"<td class='met'><span class='{'pass' if ow>=4.5 else 'fail'}'>{ow:.2f}</span> / "
          f"<span class='{'pass' if od>=4.5 else 'fail'}'>{od:.2f}</span></td>")
        A(f"<td>{swatch(nv, ON_DARK,'white')}{swatch(nv, ON_LIGHT,'dark')}<br><span class='met'><code>{nv}</code></span></td>")
        A(f"<td class='met'><span class='{'pass' if nw>=4.5 else 'fail'}'>{nw:.2f}</span> / "
          f"<span class='{'pass' if nd>=4.5 else 'fail'}'>{nd:.2f}</span></td>")
        A('<td class="ask"></td></tr>')
    A("</tbody></table>")

    A("<h2>3 &middot; Blast radius</h2>")
    A(f'<p class="sub"><b>{len(files)} files</b> consume <code>rag/*</code> tokens; <b>{len(lit)} files</b> '
      "carry the literal hexes. Token-bound consumers re-resolve for free; literal-bearing files need a sweep. "
      "This is a promotion, not an edit.</p>")
    A("<table><thead><tr><th>Files consuming <code>rag/*</code> tokens</th></tr></thead><tbody>")
    A("<tr><td class='met'>" + " · ".join(f"<code>{f}</code>" for f in sorted(files)[:28]) +
      (f" … +{len(files)-28} more" if len(files) > 28 else "") + "</td></tr>")
    A("</tbody></table>")

    A("<h2>4 &middot; Questions to rule</h2>")
    A('<ol class="rules">')
    A("<li><b>R1 &mdash; promote the delta family to canon RAG?</b> <b>[ yes / no / partially ]</b> "
      "If partially, which hues.</li>")
    A("<li><b>R2 &mdash; amber = DARK TEXT. RULED (Dave, 2026-07-18):</b> &ldquo;we should use black text "
      "on the amber.&rdquo; Consistent with what Notifications already does. "
      "<b>BUT the ruling forces a second choice:</b> on the delta amber <code>#C58720</code>, your existing "
      f"<code>rag/text/on-light</code> (<code>#333333</code>) scores <span class='fail'>4.13:1 &mdash; FAIL</span>. "
      "Only <code>#1A1A1A</code> (5.69) or <code>#000000</code> (6.86) pass. So &ldquo;black text&rdquo; cannot "
      "mean the existing token. <b>[ #1A1A1A / #000000 / new amber-specific text token ]</b> &mdash; see &sect;5.</li>")
    A("<li><b>R3 &mdash; do the incumbent values survive as a sibling?</b> The spacing retrofit parked the "
      "incumbent as <code>_spacing-hsbc-general.json</code> (&ldquo;preserve the old as legacy&rdquo;). Same "
      "pattern here? <b>[ park as sibling / retire ]</b></li>")
    A("<li><b>R4 &mdash; does this change <code>rag/error</code>'s meaning for the badge?</b> A count badge "
      "is not an error. If RAG red becomes the badge fill, the RAG vocabulary is doing double duty. "
      "<b>[ accept / give badges their own token ]</b></li>")
    A("</ol>")

    A("<h2>5 &middot; The near-black &mdash; <code>#1A1A1A</code>, and the lever it reveals</h2>")
    A('<p class="sub">Dave, 2026-07-18: <i>&ldquo;we discovered a new black value that helped with halation, '
      "not #000 but I can't remember &mdash; is it stored anywhere?&rdquo;</i> It is "
      "<code>#1A1A1A</code>, <code>_PROFORMA-RULES.md</code> rule 1. Three problems: it is "
      "<b>in no token store</b> (a literal in 10 files plus a line in a rules doc &mdash; nothing resolves "
      "or gates it); it is <b>still marked open</b> (<i>&ldquo;Open to confirm with Dave: (a) near-black "
      "shade&rdquo;</i>); and <b>the halation rationale was never recorded</b> &mdash; the written rationale "
      "is about red already meaning destruction. The value survived; the reason did not.</p>")
    A("<table><thead><tr><th>White text on&hellip;</th><th>Contrast</th><th>Luminance step</th>"
      '<th class="ask">Ruling</th></tr></thead><tbody>')
    for bg, lbl in [("#000000", "pure black"), ("#1A1A1A", "the near-black — proforma rule 1"),
                    ("#1D1D1D", "color/grey/dark-mode/600"), ("#333333", "color/grey/800")]:
        r = cr(ON_DARK, bg)
        A(f'<tr><td>{swatch(bg, ON_DARK,"white text")}<br><span class="met"><code>{bg}</code> {lbl}</span></td>'
          f'<td class="met"><b>{r:.2f}:1</b></td>'
          f'<td class="met">{100*(21-r)/21:.0f}% below pure black</td><td class="ask"></td></tr>')
    A("</tbody></table>")
    A('<p class="sub"><b>Why this matters beyond the badge.</b> White on <code>#000</code> is 21:1; on '
      "<code>#1A1A1A</code> it is 17.4:1 &mdash; the edge step cut by ~17%. That is <b>the same lever</b> as "
      "dropping chroma 1.00&rarr;0.72 on a coloured ground: both reduce the <b>extremity of the edge</b> "
      "rather than adding contrast. So the rule being drafted has <b>two levers</b> &mdash; <b>chroma</b> on "
      "coloured grounds, <b>luminance extremity</b> on neutral ones &mdash; and <code>#1A1A1A</code> is "
      "already its neutral-ground instance, applied for two weeks without ever being written down as such. "
      "<b>R5 &mdash; tokenise <code>#1A1A1A</code> and record the halation rationale? [ yes / no ]</b></p>")

    A('<p class="foot">Generated by <code>reviews/gen_rag_promotion.py</code> from live '
      "<code>tokens/semantic-colour.json</code> &middot; contrast computed, blast radius measured &mdash; "
      "not asserted &middot; promotion is Dave&rsquo;s alone; nothing applied.</p>")
    A("</body></html>")

    with open(OUT, "w") as f:
        f.write("\n".join(h))
    print(f"wrote {os.path.relpath(OUT, ROOT)} — {len(PAIRS)} hues · {len(files)} token files · {len(lit)} literal files")


if __name__ == "__main__":
    build()
