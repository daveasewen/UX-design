#!/usr/bin/env python3
"""gen_tracking_contact_sheet.py — tracking variations, contact sheet, CUT BY ROLE.

v2 — RECUT after Dave's correction, 2026-07-18
  Dave: "we have editorial and component styles to take into account. I don't [think] there
  is any impact on short labeling to reading speed … this isn't just about reading speed,
  it's about halation and blooming, so we may have different rules for the text roles."

  He is right, and v1 contained a category error I should have caught. v1 cut the ladders by
  SIZE and GROUND. It should have cut by ROLE first, because the two composite sets answer to
  different physics:

    EDITORIAL  = continuous reading. Fixations, saccades, word-skipping, word-shape cues.
                 This is what every reading-speed study measures.
    COMPONENT  = short labels. RECOGNISED, not read. One or two words, often enclosed, often
                 reversed on a coloured or near-black ground. Nobody saccades through
                 "Pending approval".

  TWO CONSEQUENCES, and the second inverts a v1 recommendation:
    1. The reading-speed evidence ("do not widen — it slows fast readers") governs EDITORIAL
       ONLY. In v1 I used it to argue against opening tracking on component labels. It was
       never in scope there.
    2. The CROWDING literature — Zorzi, the dyslexia work — is about LETTER IDENTIFICATION,
       which is precisely what recognising a short label is. So crowding relief matters MORE
       for Component than for Editorial. v1 filed it under the wrong tier of the system.
       Component tracking therefore has a STRONGER case than v1 gave it, not a weaker one,
       and L3's "low confidence" was low for the wrong reason.

  Halation compounds this: the reversed-on-chroma surfaces are almost all Component
  (badges, toasts, tags, count-badges). So the two phenomena that actually bear on tracking
  — bloom and crowding — both land on Component, and the one phenomenon that argues for
  restraint — reading speed — lands on Editorial.

STRUCTURE
  Part A — EDITORIAL ladders. Governed by reading-speed + optical sizing.
  Part B — COMPONENT ladders. Governed by crowding + halation. Reading-speed evidence is
           explicitly OUT OF SCOPE and the sheet says so.

Usage:  python3 reviews/gen_tracking_contact_sheet.py
Then:   python3 knowledge/_review/_make_review.py reviews/TRACKING-CONTACT-2026-07-18.html
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reviews", "TRACKING-CONTACT-2026-07-18.html")

BLACK = "#1A1A1A"   # surface/digital-black
CHROMA = "#B92F1E"  # data/delta/loss/light — sat 0.72, Dave's pick


def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def cr(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)



FONT_DIR = os.path.join(ROOT, "knowledge", "assets", "fonts", "_desktop", "TTF")
FONT_WEIGHTS = {"Th": 300, "Lt": 350, "Rg": 400, "Md": 500, "Bd": 700}


def embed_fonts():
    """v3: embed the REAL licensed face as base64 woff2.

    Retires the caveat carried by every previous sheet ("sandbox has no Univers, judge on
    your screen"). The Latin desktop TTFs have been in the repo since 2024-03; the earlier
    _TYPE-DECISIONS blocker saying otherwise was stale. Subset to woff2 keeps the whole
    family under ~300KB base64, so the sheet stays a single portable file.
    """
    import base64, io
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return "", False
    faces = []
    for suffix, css_weight in FONT_WEIGHTS.items():
        path = os.path.join(FONT_DIR, f"HSBC_MtUnivers_Latin-{suffix}.ttf")
        if not os.path.exists(path):
            return "", False
        try:
            f = TTFont(path)
            f.flavor = "woff2"
            buf = io.BytesIO()
            f.save(buf)
            b64 = base64.b64encode(buf.getvalue()).decode()
        except Exception:
            return "", False
        faces.append(
            "@font-face{font-family:'UniversReal';font-style:normal;font-weight:%d;"
            "src:url(data:font/woff2;base64,%s) format('woff2');font-display:block}"
            % (css_weight, b64))
    return "<style>" + "".join(faces) + "</style>", True


EDITORIAL = [
    dict(key="E1", title="Editorial display &mdash; <code>.t-ed-display-2</code> / 40px",
         sub="Continuous-reading tier, display size. Optical sizing: at display sizes the gaps "
             "grow faster than the strokes and the line drifts apart.",
         text="Your money, working harder", size=40, ground="#FFFFFF", ink="#1A1A1A", weight=300,
         steps=["0", "-0.005em", "-0.01em", "-0.015em", "-0.02em", "-0.025em", "-0.03em"],
         rec=4,
         why="<code>&minus;0.02em</code>. Brand {#type26-016} gives &minus;15 to &minus;30 for Latin "
             "headlines; this is its midpoint. Optical sizing is SETTLED and medium-independent. "
             "Midpoint rather than the &minus;0.03 extreme because the brand range was written for "
             "print, where ink spread closes gaps that a screen does not. <b>Strengthened by the "
             "font measurements:</b> Univers is a relatively LOOSE face (SB/stem 0.90 vs ~0.75 for "
             "the Helvetica lineage), so it drifts apart at display size more than a tighter face "
             "would &mdash; which is exactly what this tightening is for.",
         tier="SETTLED direction &middot; brand number &middot; MEASURED support"),

    dict(key="E2", title="Editorial body &mdash; <code>.t-ed-body</code> / 16px",
         sub="The tier every reading-speed study actually measures. Wrapping prose, read "
             "continuously.",
         text="Your payment of &pound;240.00 has been scheduled for 21 July and will leave your "
              "account overnight.",
         size=16, ground="#FFFFFF", ink="#1A1A1A", weight=400,
         steps=["-0.01em", "-0.005em", "0", "+0.005em", "+0.01em", "+0.015em"],
         rec=2,
         why="<b>Change nothing.</b> Reading speed peaks at a face's designed spacing and falls off "
             "both ways; widening cuts word-skipping and slows fast readers. This is the one place "
             "on the sheet where that evidence is fully in scope, and it says leave it alone. "
             "Brand's &minus;5/&minus;10 body leg is print practice for ink spread. "
             "<b>The null result, and the highest-confidence call here.</b>",
         tier="CONTESTED evidence, correctly scoped &rarr; do no harm"),
]

COMPONENT = [
    dict(key="C1", title="Component label, ordinary ground &mdash; <code>.t-cm-legal</code> / 12px",
         sub="Short label on white. Recognised, not read &mdash; so crowding and glyph "
             "discrimination govern, and reading-speed evidence does not apply.",
         text="Pending approval", size=12, ground="#FFFFFF", ink="#1A1A1A", weight=500,
         steps=["0", "+0.005em", "+0.01em", "+0.015em", "+0.02em", "+0.025em"],
         rec=1,
         why="<code>+0.005em</code> &mdash; <b>revised DOWN from v2's <code>+0.01em</code> on the "
             "font measurements.</b> This recommendation has now moved twice, in both directions, "
             "and the round trip is the useful part: v1 said +0.005 for the wrong reason "
             "(reading-speed evidence that was out of scope), v2 raised it to +0.01 on correctly-"
             "scoped crowding, and the font file then showed <b>Univers is already looser than "
             "Arial</b> (15.6% vs 12.4% of x-height). Crowding relief still applies &mdash; but it "
             "starts from a baseline with more air than I assumed, so the smallest step is the "
             "honest one. <b>Lowest-confidence cell on the sheet.</b>",
         tier="CROWDING (scoped) &middot; tempered by MEASURED baseline looseness"),

    dict(key="C2", title="Component label, reverse on <code>surface/digital-black</code> / 14px",
         sub="Where bloom starts. Reversed letterforms scatter light across the boundary and read "
             "tighter than they are.",
         text="Payment scheduled", size=14, ground=BLACK, ink="#FFFFFF", weight=500,
         steps=["0", "+0.005em", "+0.01em", "+0.015em", "+0.02em", "+0.025em"],
         rec=3,
         why="<code>+0.015em</code> &mdash; <b>a step wider than the ordinary-ground label at C1</b>, "
             "because two effects stack here: crowding (as C1) plus bloom closing the apparent gaps "
             "further. <b>Now with measured backing:</b> these specify Medium, which sits at "
             "SB/stem <b>0.64</b> &mdash; tight-side for this family &mdash; so the stack is "
             "crowding + relative tightness + bloom. If C1 and C2 want the same number, bloom adds "
             "nothing and the rule is simpler. <b>The comparison between these two strips is the "
             "real experiment.</b>",
         tier="CROWDING + PRACTITIONER bloom &middot; screen-specific mechanism"),

    dict(key="C3", title="Component label, reverse on chroma &mdash; 14px on <code>#B92F1E</code>",
         sub="Your badge, at the sat-0.72 ground you picked and the weight col26-020(c) mandates.",
         text="Payment scheduled", size=14, ground=CHROMA, ink="#FFFFFF", weight=500,
         steps=["0", "+0.005em", "+0.01em", "+0.015em", "+0.02em", "+0.025em"],
         rec=3,
         why="<code>+0.015em</code>, same as C2. If chroma and neutral grounds want the SAME "
             "opening, tracking is one leg covering all reverse Component text &mdash; cheap to "
             "state, cheap to gate. If chroma wants more, the rule branches by ground, mirroring "
             "col26-020's existing two-lever split.",
         tier="Tests whether the tracking lever is ground-dependent"),

    dict(key="C4", title="Component figure &mdash; <code>.t-cm-figure-2</code> / 40px",
         sub="The other end of the Component set. Large numerals &mdash; D6: &quot;we use large "
             "figures for some components&quot;. Still recognised, not read.",
         text="&pound;24,580.00", size=40, ground="#FFFFFF", ink="#1A1A1A", weight=300,
         steps=["-0.02em", "-0.015em", "-0.01em", "-0.005em", "0", "+0.005em"],
         rec=2,
         why="<code>&minus;0.01em</code>. <b>The Component set spans the full ramp, so it needs both "
             "directions</b> &mdash; open at 12px, tighten at 40px. Less tightening than editorial "
             "display (E1) because tabular figures are uniform-width by construction and tighten "
             "less gracefully; digits also carry less shape variety, so gap loss costs more. "
             "<b>This ladder did not exist in v1 at all</b> &mdash; a gap your point exposed.",
         tier="SETTLED optical sizing &middot; tabular-figure caveat is my inference"),

    dict(key="C5", title="Text luminance &mdash; the other bloom lever / 14px",
         sub="Not tracking. The literature's remedy at source: dim the ink off pure white. "
             "Tracking fixed at 0 so only luminance varies.",
         text="Payment scheduled", size=14, ground=BLACK, ink=None, weight=500,
         inks=["#FFFFFF", "#F5F5F5", "#EBEBEB", "#E0E0E0", "#D4D4D4"],
         rec=2,
         why="<code>#EBEBEB</code> on digital-black &mdash; still <b>14.60:1</b>, so it costs "
             "almost nothing. <b>But the arithmetic exposes an asymmetry:</b> on the chroma ground "
             "the same lever runs out immediately &mdash; <code>#E0E0E0</code> is 4.56:1 and "
             "<code>#D4D4D4</code> already FAILS at 4.06:1. So text-dimming is a <b>neutral-ground "
             "lever only</b>, which mirrors col26-020's existing chroma/luminance split rather than "
             "cutting across it. That symmetry is the argument for adopting it.",
         tier="PRACTITIONER &middot; contrast headroom computed from real token values"),

    dict(key="C6", title="The weight question &mdash; 14px label, tracking fixed at 0",
         sub="NEW in v3, from the font measurements. Sidebearings barely move across the family "
             "(92&rarr;68) while stems grow sevenfold (20&rarr;146), so SB/stem collapses "
             "4.60&rarr;0.46. Same label, same size, same tracking &mdash; only weight varies.",
         text="Payment scheduled", size=14, ground=BLACK, ink="#FFFFFF",
         weights_ladder=[(300, "Thin &middot; 2.12"), (350, "Light &middot; 1.38"),
                         (400, "Regular &middot; 0.90"), (500, "Medium &middot; 0.64"),
                         (700, "Bold &middot; 0.46")],
         rec=3,
         why="<b>No tracking recommendation &mdash; this ladder asks a question the others assume "
             "away.</b> Every rule we have treats tracking as a function of size and role. The "
             "measurements say the largest single effect in this family is <b>weight</b>: Bold "
             "leaves under half a stem of air, Thin over two stems. If the heavier cells here look "
             "visibly tighter to you at identical tracking, <b>tracking has to carry a weight term "
             "as well</b>, and every recommendation on this sheet is under-specified. Medium is "
             "marked only because col26-020(c) mandates it here, not because I am recommending it.",
         tier="MEASURED &middot; the open question, not an answer"),
]

CSS = """<style>
:root{--ink:#1c1c1c;--mut:#6b6b6b;--line:#e4e4e4;--red:#db0011;--rec:#0b7a34;--ed:#3b5f8a;
      --cm:#8a1f1f;}
*{box-sizing:border-box}
body{font-family:'UniversReal',"Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;color:var(--ink);
  margin:0;padding:40px;max-width:1240px;line-height:1.5;background:#fafafa}
h1{font-size:32px;font-weight:300;margin:0 0 4px}
h2{font-size:19px;font-weight:500;margin:0 0 2px}
h3{font-size:22px;font-weight:300;margin:0 0 4px}
.sub{color:var(--mut);font-size:14px;margin:0 0 22px}
.lead{font-size:15px;background:#fff;border:1px solid var(--line);border-left:3px solid var(--red);
  padding:16px 20px;margin:20px 0}
.caveat{font-size:14px;background:#fff;border:1px solid var(--line);border-left:3px solid #b25000;
  padding:14px 20px;margin:20px 0}
.ok{font-size:14px;background:#fff;border:1px solid var(--line);border-left:3px solid var(--rec);
  padding:14px 20px;margin:20px 0}
.part{margin:44px 0 0;padding:18px 22px;background:#fff;border:1px solid var(--line)}
.part.ed{border-left:4px solid var(--ed)}
.part.cm{border-left:4px solid var(--cm)}
.plabel{font-size:11px;letter-spacing:.06em;font-weight:500;color:#fff;padding:3px 10px;
  display:inline-block;margin-bottom:10px}
.plabel.ed{background:var(--ed)}.plabel.cm{background:var(--cm)}
.governs{font-size:13.5px;background:#fbfbfb;border-left:2px solid var(--line);padding:10px 14px;
  margin:10px 0 0}
.sheet{background:#fff;border:1px solid var(--line);padding:20px 22px 8px;margin:16px 0}
.head{display:flex;align-items:baseline;gap:12px;margin-bottom:2px}
.key{font-size:12px;font-weight:500;color:#fff;background:var(--ink);padding:3px 9px}
.lsub{color:var(--mut);font-size:13px;margin:6px 0 16px}
.strip{display:flex;flex-wrap:wrap;border:1px solid var(--line);border-right:0;border-bottom:0;
  margin-bottom:14px}
.cell{flex:1 1 155px;min-width:155px;border-right:1px solid var(--line);
  border-bottom:1px solid var(--line)}
.cap{font-size:11px;color:var(--mut);padding:6px 10px;background:#f7f7f7;
  border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}
.cell.is-rec .cap{background:var(--rec);color:#fff;font-weight:500}
.frame{padding:18px 12px;display:flex;align-items:center;justify-content:center;min-height:82px;
  overflow:hidden;text-align:center}
.recflag{font-size:9px;letter-spacing:.05em;background:#fff;color:var(--rec);padding:1px 5px;
  font-weight:500}
.why{font-size:13.5px;background:#fbfbfb;border-left:2px solid var(--rec);padding:10px 14px;
  margin:0 0 10px}
.tier{font-size:10.5px;letter-spacing:.04em;color:var(--mut);margin:0 0 14px}
.ask{background:#fffdf5;border:1px solid var(--line);padding:9px 14px;font-size:12.5px;
  color:var(--mut);margin:0 0 6px}
code{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;background:#f2f2f2;padding:1px 5px;
  border-radius:3px}
.summary{width:100%;border-collapse:collapse;background:#fff;margin:14px 0;font-size:13px}
.summary th,.summary td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line)}
.summary th{font-weight:500;font-size:11px;letter-spacing:.04em;color:var(--mut);background:#f4f4f4}
.chg{color:var(--cm);font-weight:500}
.foot{color:var(--mut);font-size:12px;margin-top:44px;border-top:1px solid var(--line);
  padding-top:12px}
</style></head><body>"""


def cell(text, size, ground, ink, track, weight, is_rec, label, extra=""):
    st = (f"font-size:{size}px;font-weight:{weight};letter-spacing:{track};"
          f"color:{ink};line-height:1.35")
    return (f'<div class="cell{" is-rec" if is_rec else ""}">'
            f'<div class="cap"><span>{label}</span>'
            f'{"<span class=recflag>PICK</span>" if is_rec else f"<span>{extra}</span>"}</div>'
            f'<div class="frame" style="background:{ground}">'
            f'<span style="{st}">{text}</span></div></div>')


def strip(L, A):
    A('<div class="sheet">')
    A(f'<div class="head"><span class="key">{L["key"]}</span><h2>{L["title"]}</h2></div>')
    A(f'<p class="lsub">{L["sub"]}</p>')
    A('<div class="strip">')
    wt = L.get("weight", 400)
    if L.get("weights_ladder"):
        for i, (w, lbl) in enumerate(L["weights_ladder"]):
            A(cell(L["text"], L["size"], L["ground"], L["ink"], "0", w,
                   i == L["rec"], lbl))
        pick = "no change &mdash; this one is a question"
        A("</div>")
        A(f'<p class="why"><b>{pick}. </b>{L["why"]}</p>')
        A(f'<p class="tier">RESTS ON: {L["tier"]}</p>')
        A('<p class="ask">Do the heavier cells read tighter at identical tracking?</p>')
        A("</div>")
        return
    if L.get("inks"):
        for i, ink in enumerate(L["inks"]):
            A(cell(L["text"], L["size"], L["ground"], ink, "0", wt,
                   i == L["rec"], ink, f"{cr(ink, L['ground']):.1f}:1"))
        pick = L["inks"][L["rec"]]
    else:
        for i, step in enumerate(L["steps"]):
            A(cell(L["text"], L["size"], L["ground"], L["ink"], step, wt,
                   i == L["rec"], step))
        pick = L["steps"][L["rec"]]
    A("</div>")
    A(f'<p class="why"><b>Recommend {pick} &mdash; </b>{L["why"]}</p>')
    A(f'<p class="tier">RESTS ON: {L["tier"]}</p>')
    A('<p class="ask">Your pick, or a note if none of them hold:</p>')
    A("</div>")


def build():
    h = []
    A = h.append
    A('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>Tracking &mdash; contact sheet, cut by role</title>")
    fontcss, real = embed_fonts()
    A(fontcss)
    A(CSS)

    A("<h1>Tracking &mdash; contact sheet</h1>")
    A('<p class="sub">Apollo SDS &middot; 2026-07-18 &middot; <b>v2, recut by role</b> &mdash; '
      "Editorial and Component governed separately.</p>")

    A('<div class="lead"><b>Why this was recut.</b> Dave: <i>&quot;we have editorial and component '
      "styles to take into account &hellip; I don&#39;t [think] there is any impact on short "
      "labeling to reading speed &hellip; this isn&#39;t just about reading speed, it&#39;s about "
      "halation and blooming, so we may have different rules for the text roles.&quot;</i><br><br>"
      "<b>Correct, and v1 had a category error.</b> It cut the ladders by size and ground. It "
      "should have cut by role, because the two sets answer to different physics: "
      "<b>Editorial</b> is read continuously &mdash; fixations, saccades, word-skipping. "
      "<b>Component</b> is recognised, not read. Nobody saccades through "
      "&quot;Pending&nbsp;approval&quot;.</div>")

    A('<div class="lead"><b>Two consequences &mdash; and the second reverses a v1 recommendation.</b>'
      "<br><br><b>1.</b> The reading-speed evidence (&quot;do not widen&quot;) governs "
      "<b>Editorial only</b>. In v1 I used it to argue against opening tracking on component "
      "labels, where it was never in scope.<br><br>"
      "<b>2.</b> The <b>crowding</b> literature &mdash; Zorzi, the dyslexia work &mdash; is about "
      "<b>letter identification</b>, which is exactly what recognising a short label is. Crowding "
      "relief therefore matters <b>more</b> for Component than for Editorial. I had it filed under "
      "the wrong tier. <b>Component tracking has a stronger case than v1 gave it, not a weaker "
      "one</b>, and C1 moves from <code>+0.005em</code> to <code>+0.01em</code> as a result.<br><br>"
      "Halation compounds it: the reversed-on-chroma surfaces are almost all Component &mdash; "
      "badges, toasts, tags. <b>Both phenomena that argue for opening tracking land on Component; "
      "the one that argues for restraint lands on Editorial.</b></div>")

    if real:
        A('<div class="ok"><b>&#10003; Rendering in the real face.</b> The licensed Latin desktop '
          "set has been in the repo since 2024-03 &mdash; the <code>_TYPE-DECISIONS</code> blocker "
          "saying otherwise was stale. All five weights are now embedded in this file as base64 "
          "woff2, so <b>you are looking at actual Univers, not a fallback</b>, and so am I. "
          "<b>The caveat carried by every previous sheet is retired.</b> The recommendations below "
          "are still reasoning rather than observation &mdash; but for the first time the specimens "
          "are honest.</div>")
    else:
        A('<div class="caveat"><b>Font embedding failed</b> &mdash; falling back. Judge on your '
          "screen with Univers installed.</div>")

    # ---- Part A
    A('<div class="part ed">')
    A('<span class="plabel ed">PART A &middot; EDITORIAL</span>')
    A("<h3>Continuous reading &mdash; prose that wraps</h3>")
    A('<p class="governs"><b>Governed by:</b> reading-speed evidence (CONTESTED &mdash; peaks at '
      "designed spacing, falls off both ways) and optical sizing (SETTLED). "
      "<b>Halation is largely out of scope</b> &mdash; editorial text rarely sits reversed on "
      "chroma. This is the restraint half of the system.</p>")
    A("</div>")
    for L in EDITORIAL:
        strip(L, A)

    # ---- Part B
    A('<div class="part cm">')
    A('<span class="plabel cm">PART B &middot; COMPONENT</span>')
    A("<h3>Short labels &mdash; recognised, not read</h3>")
    A('<p class="governs"><b>Governed by:</b> crowding / letter identification, and halation on '
      "reversed grounds. <b>Reading-speed evidence is explicitly OUT OF SCOPE here</b> &mdash; it "
      "measures continuous reading, which is not what happens to a two-word label. This is the "
      "half where the case for opening tracking is real.</p>")
    A("</div>")
    for L in COMPONENT:
        strip(L, A)

    # ---- summary
    A('<div class="sheet">')
    A('<div class="head"><span class="key">&Sigma;</span><h2>All seven, and what changed from v1'
      "</h2></div>")
    A("<table class='summary'><thead><tr><th>Role</th><th>Context</th><th>Recommend</th>"
      "<th>vs v1</th><th>Confidence</th></tr></thead><tbody>")
    rows = [
        ("Editorial", "Display 40px", "<code>&minus;0.02em</code>", "unchanged", "Medium-high"),
        ("Editorial", "Body 16px", "<b>no change</b>", "unchanged &mdash; now correctly scoped",
         "<b>High</b>"),
        ("Component", "Label 12px, ordinary", "<code>+0.005em</code>",
         "<span class='chg'>LOWERED &mdash; moved twice</span>", "<b>Low</b>"),
        ("Component", "Label 14px, reverse neutral", "<code>+0.015em</code>",
         "<span class='chg'>RAISED from +0.01em</span>", "Medium"),
        ("Component", "Label 14px, reverse chroma", "<code>+0.015em</code>",
         "<span class='chg'>RAISED from +0.01em</span>", "Medium"),
        ("Component", "Figure 40px", "<code>&minus;0.01em</code>",
         "<span class='chg'>NEW &mdash; absent from v1</span>", "Low-medium"),
        ("Both", "Text luminance, neutral only", "<code>#EBEBEB</code>", "unchanged", "Medium"),
        ("Component", "Weight term", "<b>open question</b>",
         "<span class='chg'>NEW &mdash; C6</span>", "&mdash;"),
    ]
    for role, ctx, rec, delta, conf in rows:
        A(f"<tr><td><b>{role}</b></td><td>{ctx}</td><td>{rec}</td><td>{delta}</td>"
          f"<td>{conf}</td></tr>")
    A("</tbody></table>")
    A('<p class="why"><b>The shape, if it survives you.</b> Not one ramp but <b>two, running in '
      "opposite directions</b>. Editorial holds near zero and tightens only at display &mdash; "
      "restraint, because continuous reading punishes interference. Component opens at label sizes "
      "and tightens only at figure sizes &mdash; because recognition rewards separation and bloom "
      "steals it back. <b>That is a genuinely different rule per role, which is what you "
      "suspected.</b> It also fits the architecture already ruled in D2/D3: two composite sets, "
      "shared primitives, governed separately.</p>")
    A('<p class="why"><b>What it would cost.</b> Tracking becomes a property ON the composites &mdash; '
      "eleven Component and nine Editorial &mdash; rather than a token ramp indexed by size, because "
      "the same 40px wants <code>&minus;0.02em</code> in Editorial and <code>&minus;0.01em</code> in "
      "Component. <b>Size alone cannot express this rule.</b> That is the strongest argument on the "
      "sheet for the role split being real rather than tidy.</p>")
    A("</div>")

    A('<p class="foot">Generated by <code>reviews/gen_tracking_contact_sheet.py</code> (v2, recut '
      "by role) &middot; contrast figures computed from real token values &middot; evidence tiers "
      "carried from <code>TRACKING-DOSSIER-2026-07-18</code> &middot; <b>recommendations are "
      "hypotheses, not defaults; nothing is promoted</b> &mdash; promotion is Dave&#39;s alone "
      "&middot; rendered in a fallback face; judge on your screen with Univers.</p>")
    A("</body></html>")

    with open(OUT, "w") as f:
        f.write("\n".join(h))
    n = sum(len(L.get("inks") or L.get("weights_ladder") or L["steps"])
            for L in EDITORIAL + COMPONENT)
    print(f"wrote {os.path.relpath(OUT, ROOT)} — {len(EDITORIAL)} editorial + "
          f"{len(COMPONENT)} component ladders, {n} cells")


if __name__ == "__main__":
    build()
