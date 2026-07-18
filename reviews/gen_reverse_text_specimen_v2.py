#!/usr/bin/env python3
"""gen_reverse_text_specimen_v2.py — re-cut at the chosen chroma.

WHAT V1 SETTLED (Dave, 2026-07-18)
  Q1 ANSWERED — chroma is the driver, not lightness. The v1 §2 control pair sat at
  near-identical lightness (0.43 vs 0.42) and differed only in saturation (1.00 vs 0.72);
  Dave: "they are quite similar but these seems to dance the least. the bright red and
  the white text is instantly straining." The null result did NOT come back — the effect
  is real and does not fold into the contrast gate.
  Consequence: the earlier #A8000B ruling is SUPERSEDED. #A8000B is sat 1.00 — the same
  maximum chroma as the straining #DB0011, only darker — so it buys lightness contrast
  that was never the problem.

WHAT THIS SHEET IS FOR — the two variables v1 could not isolate
  §1  WEIGHT × SIZE at fixed chroma (sat 0.72). Answers Q2 (minimum weight) and
      Q3 (is there a size floor, i.e. is the rule a size×weight pair rather than a
      weight minimum).
  §2  The CHROMA LADDER at fixed weight/size. Answers the question the new rule needs
      in order to be gateable at all: WHERE does saturation stop mattering? dv-019 has
      its 135° hue leg because Dave observed the dance on a 146° pair; this rule needs
      the equivalent number for its saturation leg.

CONSTRAINTS (unchanged from v1)
  · Real palette values only, each carrying its $token path — nothing invented.
  · Real weights only: 400/500/700. No 600 (type25-004: licensed five are
    100/300/400/500/700; the OTF set ships no SemiBold, so 600 = faux-bold).

Usage:  python3 reviews/gen_reverse_text_specimen_v2.py
Then:   python3 knowledge/_review/_make_review.py reviews/REVERSE-TEXT-SPECIMEN-V2-2026-07-18.html
"""
import os, colorsys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reviews", "REVERSE-TEXT-SPECIMEN-V2-2026-07-18.html")

CHOSEN = ("#B92F1E", "data/delta/loss/light", "sat 0.72 — the chroma you picked")

# the ladder: real palette reds, descending saturation, for the threshold leg
LADDER = [
    ("#DB0011", "color/primary", 1.00, "CURRENT badge — you called this instantly straining"),
    ("#E31E22", "color/complimentary/red-1", 0.78, ""),
    ("#BA1110", "color/complimentary/red-2", 0.84, ""),
    ("#B92F1E", "data/delta/loss/light", 0.72, "YOUR PICK — danced least"),
    ("#CC4333", "data/delta/loss/dark", 0.60, "lowest-chroma red in the palette"),
]
WEIGHTS = [(400, "Regular"), (500, "Medium"), (700, "Bold")]
SIZES = [10, 12, 14, 16, 20]


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


def cw(h):
    return 1.05 / (lum(h) + 0.05)


def badge(bg, w, size, text="99+"):
    return (f'<span class="bdg" style="background:{bg};font-weight:{w};font-size:{size}px">'
            f"{text}</span>")


CSS = """<style>
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
.ask{width:120px;background:#fffdf5}
.pick{background:#f2f8f4}
.foot{color:var(--mut);font-size:12px;margin-top:40px;border-top:1px solid var(--line);padding-top:12px}
</style></head><body>"""


def build():
    h = []
    A = h.append
    A('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>Reverse text on chroma &mdash; specimen v2</title>")
    A(CSS)

    A("<h1>Reverse text on chroma &mdash; specimen v2</h1>")
    A('<p class="sub">Apollo SDS &middot; 2026-07-18 &middot; re-cut at the chroma you chose. '
      "Two variables left: <b>weight&times;size</b> (&sect;1) and <b>where saturation stops mattering</b> (&sect;2).</p>")

    A('<div class="lead"><b>What v1 settled.</b> Your two control rows sat at near-identical lightness '
      "(0.43 vs 0.42) and differed only in saturation (1.00 vs 0.72), and you saw a difference &mdash; so "
      "<b>chroma is the driver, not lightness</b>. The effect is real and does not fold into the contrast "
      "gate. That also <b>supersedes the earlier <code>#A8000B</code> ruling</b>: <code>#A8000B</code> is "
      "sat&nbsp;1.00, the same maximum chroma as the red you called straining &mdash; it only adds lightness "
      "contrast, which was never the problem. "
      "<b>&sect;2 is the one that makes the rule gateable</b>: without a saturation number there is nothing "
      "to check, the way <code>dv-019</code> would be unenforceable without its 135&deg;.</div>")

    # ---- §1 weight × size at fixed chroma
    bg, tok, note = CHOSEN
    hd, s, l = hsl(bg)
    A("<h2>1 &middot; Weight &times; size at your chosen chroma</h2>")
    A(f'<p class="sub">Ground fixed at <code>{bg}</code> &middot; <span class="met">{tok} &middot; '
      f"sat {s:.2f} &middot; light {l:.2f} &middot; {cw(bg):.2f}:1 on white</span>. "
      "<b>Q2 &mdash; mark the lightest weight that holds. Q3 &mdash; mark the smallest size that holds.</b> "
      "If the answer differs by size, the rule is a size&times;weight pair, not a weight minimum.</p>")
    A("<table><thead><tr><th>Size</th>")
    for w, n in WEIGHTS:
        A(f"<th>{w} &middot; {n}</th>")
    A('<th class="ask">Holds from</th></tr></thead><tbody>')
    for sz in SIZES:
        A(f"<tr><td><b>{sz}px</b></td>")
        for w, _ in WEIGHTS:
            A("<td>" + badge(bg, w, sz, "3") + badge(bg, w, sz, "99+") + "</td>")
        A('<td class="ask"></td></tr>')
    A("</tbody></table>")

    # ---- §2 chroma ladder
    A("<h2>2 &middot; The chroma ladder &mdash; where does saturation stop mattering?</h2>")
    A('<p class="sub">Fixed at <b>14px / weight 500</b> (the current badge spec) so only the ground varies. '
      "Ordered by saturation. <b>Mark the first row that reads clean</b> &mdash; that saturation becomes the "
      "rule's threshold, the way 135&deg; became <code>dv-019</code>'s hue leg because you saw the dance on a "
      "146&deg; pair.</p>")
    A("<table><thead><tr><th>Ground</th><th>sat</th><th>light</th><th>on white</th>"
      '<th>14px / 500</th><th>14px / 700</th><th class="ask">Reads clean?</th></tr></thead><tbody>')
    for bg2, tok2, _s, note2 in sorted(LADDER, key=lambda x: -hsl(x[0])[1]):
        hd2, s2, l2 = hsl(bg2)
        cls = ' class="pick"' if "YOUR PICK" in note2 else ""
        A(f"<tr{cls}><td><code>{bg2}</code><br><span class='met'>{tok2}</span>"
          + (f"<br><b style='font-size:11px'>{note2}</b>" if note2 else "") + "</td>")
        A(f"<td class='met'><b>{s2:.2f}</b></td><td class='met'>{l2:.2f}</td>"
          f"<td class='met'>{cw(bg2):.2f}:1</td>")
        A("<td>" + badge(bg2, 500, 14, "3") + badge(bg2, 500, 14, "99+") + "</td>")
        A("<td>" + badge(bg2, 700, 14, "3") + badge(bg2, 700, 14, "99+") + "</td>")
        A('<td class="ask"></td></tr>')
    A("</tbody></table>")

    A("<h2>3 &middot; Still to rule</h2>")
    A('<ol class="rules">')
    A("<li><b>Q2 &mdash; minimum weight.</b> From &sect;1. Candidates <b>500</b> or <b>700</b> only. "
      "The badge was 700 before the retrofit collapsed it. <b>[ 500 / 700 ]</b></li>")
    A("<li><b>Q3 &mdash; size floor.</b> Is there a size below which no weight rescues it? "
      "<b>[ pin the size, or: no floor ]</b></li>")
    A("<li><b>Q-new &mdash; the saturation threshold.</b> From &sect;2, the number the gate will actually "
      "test. Without it there is no rule, only a preference. <b>[ pin a saturation ]</b></li>")
    A("<li><b>Q5 &mdash; scope.</b> Badges are the visible case; this applies to every light-on-chroma "
      "surface &mdash; solid RAG banners, primary buttons, pressed states, tags. "
      "<b>[ library-wide / badges only ]</b></li>")
    A("</ol>")

    A('<p class="foot">Generated by <code>reviews/gen_reverse_text_specimen_v2.py</code> &middot; '
      "real palette values with token paths &middot; licensed weights only (no 600) &middot; "
      "judge on YOUR screen with the real webfont &mdash; the sandbox has no Univers. Nothing promoted.</p>")
    A("</body></html>")

    with open(OUT, "w") as f:
        f.write("\n".join(h))
    print(f"wrote {os.path.relpath(OUT, ROOT)} — §1 {len(SIZES)}×{len(WEIGHTS)} · §2 ladder {len(LADDER)}")


if __name__ == "__main__":
    build()
