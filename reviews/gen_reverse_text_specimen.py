#!/usr/bin/env python3
"""gen_reverse_text_specimen.py — the reverse-text-on-chroma specimen sheet.

WHY THIS SHEET EXISTS
Dave observed the badge count "dancing" after the type retrofit collapsed it from
700 -> 500. Running the pair through OUR OWN stored rule — vibration() in
_validate_dataviz.py, the {#dv-019} vibrating-boundaries rule quantified from the
Tuts+ article on 2026-07-16 — scores it 0/3 legs, correctly:

    white on #DB0011   value-ratio 5.22 · hue-sep  5° · min-sat 0.00  -> 0/3 low
    red vs rag success value-ratio 1.15 · hue-sep 178° · min-sat 1.00 -> 3/3 HIGH

dv-019 needs TWO saturated near-complementary colours at near-equal value. White has
zero saturation and the value ratio is 5.22. So this is a SIBLING phenomenon, not the
same one: light low-stroke type on a high-chroma ground (halation/irradiation — the
bright field bleeding across a high-chroma edge), which no current gate can see:
  · contrast gates  — pass at 5.22:1, and would pass at ANY weight
  · vibration()     — 0/3, and scoped to adjacent series-fill pairs in DataViz only
  · type gates      — no concept of weight relative to its surface

PURPOSE: derive thresholds from what Dave can SEE dance, exactly as dv-019's 135° leg
was set because he observed the dance on a 146° pair. Nothing here is a proposal to
promote — it is an instrument for capturing an observation.

CONSTRAINTS HONOURED
  · Real palette values only — every ground carries its $token path (Dave: "we can't
    invent anything"). No derived or invented reds.
  · Real weights only — 400/500/700. There is NO 600 in the licensed portfolio
    (type25-004: five weights, store 100/300/400/500/700; the OTF set has no SemiBold
    file). A 600 would be browser-synthesised faux-bold.

Usage:  python3 reviews/gen_reverse_text_specimen.py    # from repo root
Then:   python3 knowledge/_review/_make_review.py reviews/REVERSE-TEXT-SPECIMEN-2026-07-18.html
"""
import os, colorsys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reviews", "REVERSE-TEXT-SPECIMEN-2026-07-18.html")

# ground, $token path, note — REAL palette values only
GROUNDS = [
    ("#DB0011", "color/primary · primary/background/default", "CURRENT badge fill"),
    ("#E31E22", "color/complimentary/red-1", "lighter, still max chroma"),
    ("#BA1110", "color/complimentary/red-2 · primary/background/hover", ""),
    ("#A8000B", "color/red/600 · rag/error light", "PROPOSED — the new RAG red"),
    ("#730014", "color/complimentary/red-3", "darkest full-chroma red in the palette"),
    ("#B92F1E", "data/delta/loss/light", "CONTROL — see §2"),
]
WEIGHTS = [(400, "Regular"), (500, "Medium"), (700, "Bold")]
SIZES = [12, 14, 16]


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


def badge(bg, w, size, text):
    return (f'<span class="bdg" style="background:{bg};font-weight:{w};font-size:{size}px">'
            f'{text}</span>')


def build():
    h = []
    A = h.append
    A('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>Reverse text on chroma &mdash; specimen</title>")
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
.bdg{display:inline-flex;align-items:center;justify-content:center;min-width:24px;height:24px;padding:0 8px;
  border-radius:999px;color:#fff;line-height:1;margin:0 4px 0 0;vertical-align:middle}
.rules{background:#fff;border:1px solid var(--line);padding:4px 20px 16px;margin:16px 0}
.rules li{margin:12px 0;font-size:14px}
.met{font-size:11px;color:var(--mut);white-space:nowrap}
.ask{width:130px;background:#fffdf5}
.foot{color:var(--mut);font-size:12px;margin-top:40px;border-top:1px solid var(--line);padding-top:12px}
.ctrl{background:#fffdf5}
.no6{color:var(--arrow);font-weight:600}
</style></head><body>""")

    A("<h1>Reverse text on chroma &mdash; specimen</h1>")
    A('<p class="sub">Apollo SDS &middot; 2026-07-18 &middot; instrument for setting a threshold, not a proposal. '
      "Mark the cell where the dancing <b>stops</b> in each row.</p>")

    A('<div class="lead"><b>Read me first.</b> This is <b>not</b> the vibrating-boundaries rule. '
      "Your <code>{#dv-019}</code> rule &mdash; quantified from the Tuts+ article on 07-16 &mdash; needs "
      "<b>two saturated near-complementary colours at near-equal value</b>. Run through "
      "<code>vibration()</code>, white-on-red scores <b>0 of 3 legs</b> (value-ratio 5.22, hue-sep 5&deg;, "
      "min-sat 0.00) while a real chart pair scores 3/3. The function is right; the badge is a "
      "<b>sibling effect</b> &mdash; light, low-stroke type on a high-chroma ground. "
      "<b>No current gate can see it:</b> contrast gates pass it at any weight, "
      "<code>vibration()</code> scores it low and only looks at DataViz series fills, and the type gates "
      "have no concept of weight relative to surface. "
      "<b>Every ground below is a real palette value with its token path. No 600 column &mdash; "
      "600 does not exist in the licensed portfolio (<code>type25-004</code>).</b></div>")

    A("<h2>1 &middot; The grid &mdash; ground &times; weight, at three sizes</h2>")
    A('<p class="sub">Each cell shows 12/14/16px. Contrast is white-on-ground; all pass 4.5:1, so this is '
      "purely a legibility judgement. <b>Mark the first weight in each row where it stops dancing.</b></p>")
    A("<table><thead><tr><th>Ground</th><th>Chroma / value</th>")
    for w, n in WEIGHTS:
        A(f"<th>{w} &middot; {n}</th>")
    A('<th class="ask">Stops dancing at</th></tr></thead><tbody>')
    for bg, tok, note in GROUNDS:
        hd, s, l = hsl(bg)
        c = cr("#FFFFFF", bg)
        cls = ' class="ctrl"' if "CONTROL" in note else ""
        A(f"<tr{cls}><td><code>{bg}</code><br><span class='met'>{tok}</span>"
          + (f"<br><b style='font-size:11px'>{note}</b>" if note else "") + "</td>")
        A(f"<td class='met'>sat <b>{s:.2f}</b><br>light <b>{l:.2f}</b><br>{c:.2f}:1</td>")
        for w, _ in WEIGHTS:
            cell = "".join(badge(bg, w, sz, t) for sz, t in zip(SIZES, ["3", "99+", "12"]))
            A(f"<td>{cell}</td>")
        A('<td class="ask"></td></tr>')
    A("</tbody></table>")

    A("<h2>2 &middot; Isolating the variable &mdash; is it chroma or is it darkness?</h2>")
    A('<p class="sub">The two rows below sit at <b>almost identical lightness</b> but very different '
      "saturation. If the dance stops on the lower-saturation ground at the same weight, the driver is "
      "<b>chroma</b>. If both behave the same, the driver is <b>lightness</b> (i.e. plain contrast) and "
      "this whole rule collapses into the existing contrast gate &mdash; which would be a useful null result.</p>")
    A("<table><thead><tr><th>Ground</th><th>sat</th><th>light</th><th>contrast</th>")
    for w, n in WEIGHTS:
        A(f"<th>{w}</th>")
    A('<th class="ask">Which dances more?</th></tr></thead><tbody>')
    for bg, tok, note in [g for g in GROUNDS if g[0] in ("#DB0011", "#B92F1E")]:
        hd, s, l = hsl(bg)
        A(f"<tr><td><code>{bg}</code><br><span class='met'>{tok}</span></td>"
          f"<td class='met'><b>{s:.2f}</b></td><td class='met'><b>{l:.2f}</b></td>"
          f"<td class='met'>{cr('#FFFFFF',bg):.2f}:1</td>")
        for w, _ in WEIGHTS:
            A("<td>" + "".join(badge(bg, w, sz, t) for sz, t in zip(SIZES, ["3", "99+", "12"])) + "</td>")
        A('<td class="ask"></td></tr>')
    A("</tbody></table>")

    A("<h2>3 &middot; Questions to rule</h2>")
    A('<ol class="rules">')
    A("<li><b>Q1 &mdash; is there a rule here at all?</b> If §2 shows lightness rather than chroma is the "
      "driver, the honest outcome is <b>no new rule</b>: raise the contrast floor for small reverse text and "
      "stop. <b>[ new rule / fold into contrast / no rule ]</b></li>")
    A("<li><b>Q2 &mdash; the minimum weight for small reverse text on chroma.</b> From §1, the first weight "
      "that holds. Candidates are <b>500</b> or <b>700</b> only. Note the badge was <b>700</b> before the "
      "retrofit collapsed it. <b>[ 500 / 700 / size-dependent ]</b></li>")
    A("<li><b>Q3 &mdash; does a size floor come with it?</b> If 12px dances at every weight but 16px never "
      "does, the rule is a <b>size&times;weight pair</b>, not a weight minimum. <b>[ pin the sizes ]</b></li>")
    A("<li><b>Q4 &mdash; the badge fill.</b> You ruled <code>#A8000B</code>. Worth confirming against §1: it "
      "may be that the weight alone fixes it and the fill can stay <code>#DB0011</code>, which avoids "
      "<code>rag/error</code> doing duty as a neutral count colour. <b>[ confirm A8000B / revert to DB0011 ]</b></li>")
    A("<li><b>Q5 &mdash; scope.</b> Badges are the visible case, but this applies to every light-on-chroma "
      "surface: solid RAG notification banners, primary buttons, pressed states, tags. "
      "<b>[ library-wide / badges only ]</b></li>")
    A("</ol>")

    A("<h2>4 &middot; What this sheet deliberately does not test</h2>")
    A('<p class="sub"><b class="no6">No 600 weight.</b> <code>type25-004</code> licenses five weights '
      "(store 100/300/400/500/700) and the OTF set ships no SemiBold file, so a 600 would be "
      "browser-synthesised faux-bold &mdash; unpredictable and off-brand. "
      "<b>Weights 250/300/350</b> are also excluded: they exist in the files but are far too light for "
      "reverse text at these sizes, which is the whole point of the finding. "
      "<b>Dark mode</b> is not shown &mdash; <code>type.css</code> already steps weights up under "
      "<code>[data-theme=dark]</code>; the gap is that the step-up is keyed to <b>theme</b>, not to the "
      "<b>local surface</b>, which is why a white-on-red badge in light mode gets nothing.</p>")

    A('<p class="foot">Generated by <code>reviews/gen_reverse_text_specimen.py</code> &middot; grounds are real '
      "palette values with token paths (nothing invented) &middot; weights limited to the licensed set &middot; "
      "renders in-browser, so judge it on YOUR screen with the real webfont &mdash; the sandbox has no Univers "
      "and would mislead. Nothing here is promoted.</p>")
    A("</body></html>")

    with open(OUT, "w") as f:
        f.write("\n".join(h))
    print(f"wrote {os.path.relpath(OUT, ROOT)} — {len(GROUNDS)} grounds × {len(WEIGHTS)} weights × {len(SIZES)} sizes")


if __name__ == "__main__":
    build()
