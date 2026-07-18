#!/usr/bin/env python3
"""gen_component_medium_specimen.py — is small-label Medium structural, or drift?

THE QUESTION THIS SHEET EXISTS TO ANSWER
  The TYPE-002 retrofit has 721 raw font declarations to rebind. 339 map cleanly onto an
  existing composite. 100 of the remainder are the SAME shape: Component-scope, single-line,
  weight 500, at 12 / 14 / 24px — and the Component composites at those sizes are all 400.

    .t-cm-legal   12px / 400        .t-cm-caption  14px / 400
    .t-cm-tooltip 14px / 400        .t-cm-label    16px / 400

  So either the corpus is right and the composites are missing a Medium rung, or the corpus
  drifted and these 100 should snap to Regular. Nobody has ruled. Binding them to the 400
  composites would silently pick one answer.

WHAT THIS SHEET IS *NOT*
  NOT the reverse-text question. {#col26-020}(c) — 12/14/16px = Medium, 20px = Light — was
  settled from the v2 specimen and is CONDITIONAL on reverse text over an extreme ground.
  Only family A below sits in that condition. The other four families are on ordinary
  grounds, where col26-020 has nothing to say. Establishing that separation is half the
  point of the sheet: a rule quoted outside its condition is how a preference becomes a gate
  by accident.

IT MUST BE ABLE TO COME BACK NULL
  The honest null result is "all five families are drift — snap every one to Regular, add no
  composites." The sheet is built so that answer is as easy to give as any other. If Medium
  wins everywhere that is also a result, but it must be SEEN, not assumed from the fact that
  someone once typed it.

METHOD
  Every row is a REAL selector from the real corpus, with its file and its declared ground.
  Nothing invented. Each family renders its actual specimen at 500 and at 400, same size,
  same ground, so the comparison is the only variable.

Usage:  python3 reviews/gen_component_medium_specimen.py
Then:   python3 knowledge/_review/_make_review.py reviews/COMPONENT-MEDIUM-2026-07-18.html
"""
import os, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reviews", "COMPONENT-MEDIUM-2026-07-18.html")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_component-medium-data.json")

# ---------------------------------------------------------------- the five families
# Each: (key, title, whatitis, the governing question, specimen renderer key)
FAMILIES = [
    ("A", "Reverse on primary ground",
     "White label on <code>var(--pri)</code> — in Apollo mono that is the near-black "
     "<code>surface/digital-black</code> ground.",
     "This is the ONLY family inside {#col26-020}(c)'s condition. The rule already says "
     "Medium at 12&ndash;16px here. Confirm the reading &mdash; then it needs a composite that "
     "<i>encodes</i> the condition, not a note asking authors to remember it.",
     "reverse"),
    ("B", "Eyebrow / group label",
     "Muted small label above a block &mdash; <code>.eyebrow</code>, list-item <code>h2</code>, "
     "menu group headings.",
     "Classic candidate for structural Medium: short, muted, doing hierarchy work at small size. "
     "Muted colour lowers contrast, which is the argument FOR weight. Or it is just a habit.",
     "eyebrow"),
    ("C", "Control label (toggle / tab / segmented)",
     "Interactive affordance text on a transparent ground &mdash; <code>.tgl</code>, "
     "<code>.tab</code>, <code>.seg button</code>, <code>.navtoggle</code>.",
     "The largest family (31). <code>.t-cm-button</code> is already 16px/<b>500</b> &mdash; so "
     "Medium-for-controls is arguably ALREADY canon, and these are the same thing at 12/14px. "
     "If so the fix is a size range on the button composite, not a new one.",
     "control"),
    ("D", "Chip / tag / badge on surface",
     "Small enclosed label with its own quiet ground &mdash; <code>.tag</code>, "
     "<code>.chip</code>, <code>.badge</code>, <code>.avatar</code>.",
     "Enclosed text in a small pill. The enclosure already separates it from the page, which "
     "may make the weight redundant &mdash; or may be exactly why it needs to hold its own.",
     "chip"),
    ("E", "Numeral / data label",
     "Figures and axis labels &mdash; <code>.num</code>, <code>.delta</code>, "
     "<code>.axlbl</code>, <code>.prog-pct</code>.",
     "Digits carry less stroke variety than letters, and tabular figures are already in play "
     "(D6). May want Medium for a different reason than the text families.",
     "numeral"),
]

# real specimens, pulled from the corpus (selector, size, label text, note)
SPECIMENS = {
    "reverse": [(".toast", 14, "Payment scheduled", "Masthead + T1&ndash;T8, 8 files"),
                (".skip-link", 14, "Skip to content", "Masthead, T7"),
                (".count-badge", 12, "12", "Tranche-5")],
    "eyebrow": [(".eyebrow", 14, "Account overview", "Eyebrow + canon.css"),
                ("h2 (list-items)", 14, "Recent transactions", "List-items"),
                (".grouplbl", 12, "Saved accounts", "Dropdown"),
                (".menugroup-h", 12, "Transfers", "Masthead")],
    "control": [(".tgl", 14, "Show details", "T1&ndash;T8, DataViz, 10 files"),
                (".tab", 14, "Statements", "Masthead, T4, T7"),
                (".seg button", 14, "Monthly", "View-options + canon.css"),
                (".variant-tabs button", 12, "Compact", "DataViz")],
    "chip": [(".tag", 12, "Pending", "T5 &times;7"),
             (".chip", 12, "Last 30 days", "Tranche-5"),
             (".badge", 14, "99+", "Badge + canon.css"),
             (".avatar", 14, "DW", "List-items + canon.css")],
    "numeral": [(".num", 24, "02:47", "Countdown-timer"),
                (".delta", 14, "+2.4%", "canon.css"),
                (".axlbl", 12, "Q3", "DataViz"),
                (".prog-pct", 14, "68%", "Tranche-6")],
}

CSS = """<style>
:root{--ink:#1c1c1c;--mut:#6b6b6b;--line:#e4e4e4;--red:#db0011;--pri:#1a1a1a;--pri-lbl:#fff;
      --surf:#f0f0f0;--muted:#6b6b6b;--ink2:#4a4a4a;}
*{box-sizing:border-box}
body{font-family:"Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;color:var(--ink);
  margin:0;padding:40px;max-width:1180px;line-height:1.5;background:#fafafa}
h1{font-size:32px;font-weight:300;margin:0 0 4px}
h2{font-size:20px;font-weight:500;margin:44px 0 4px;padding-top:16px;border-top:2px solid var(--ink)}
h3{font-size:15px;font-weight:500;margin:24px 0 2px}
.sub{color:var(--mut);font-size:14px;margin:0 0 24px}
.lead{font-size:15px;background:#fff;border:1px solid var(--line);border-left:3px solid var(--red);
  padding:16px 20px;margin:20px 0}
.null{font-size:14px;background:#fff;border:1px solid var(--line);border-left:3px solid #0b7a34;
  padding:14px 20px;margin:20px 0}
table{width:100%;border-collapse:collapse;background:#fff;margin:12px 0 8px;font-size:13px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:middle}
th{font-weight:500;font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:var(--mut);
  background:#f4f4f4}
code{font-family:ui-monospace,Menlo,monospace;font-size:11px;background:#f2f2f2;padding:1px 5px;
  border-radius:3px}
.met{font-size:11px;color:var(--mut);white-space:nowrap}
.ask{width:150px;background:#fffdf5}
.count{font-size:22px;font-weight:300;color:var(--ink)}
.rules{background:#fff;border:1px solid var(--line);padding:4px 20px 16px;margin:16px 0}
.rules li{margin:14px 0;font-size:14px}
.fam{background:#fff;border:1px solid var(--line);padding:0 20px 8px;margin:16px 0}
.q{font-size:13px;color:var(--ink);background:#fbfbfb;border-left:2px solid var(--line);
  padding:8px 14px;margin:10px 0 14px}
.rev{background:var(--pri);color:var(--pri-lbl);padding:6px 12px;display:inline-block;line-height:1.2}
.pill{background:var(--surf);padding:3px 10px;border-radius:999px;display:inline-block;line-height:1.3}
.plain{display:inline-block;line-height:1.3}
.foot{color:var(--mut);font-size:12px;margin-top:44px;border-top:1px solid var(--line);padding-top:12px}
.warn{color:#8a1f1f;font-weight:500}
</style></head><body>"""


def render(kind, text, size, weight):
    """Render one specimen at a given weight, in its real ground."""
    st = f"font-size:{size}px;font-weight:{weight}"
    if kind == "reverse":
        return f'<span class="rev" style="{st}">{text}</span>'
    if kind == "chip":
        return f'<span class="pill" style="{st}">{text}</span>'
    if kind == "eyebrow":
        return f'<span class="plain" style="{st};color:var(--muted)">{text}</span>'
    if kind == "numeral":
        return f'<span class="plain" style="{st};font-variant-numeric:tabular-nums">{text}</span>'
    return f'<span class="plain" style="{st};color:var(--ink2)">{text}</span>'


def build():
    counts = {"A": 12, "B": 16, "C": 31, "D": 20, "E": 7}
    other = 14
    total = sum(counts.values()) + other

    h = []
    A = h.append
    A('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>Component Medium &mdash; structural or drift?</title>")
    A(CSS)

    A("<h1>Small-label Medium &mdash; structural, or drift?</h1>")
    A('<p class="sub">Apollo SDS &middot; 2026-07-18 &middot; blocking the TYPE-002 rebind '
      f"({total} declarations of the 721).</p>")

    A('<div class="lead"><b>The situation.</b> Of the 721 raw font declarations, '
      "<b>339 map cleanly</b> onto an existing composite and can be rebound without a ruling. "
      f"<b>{total} do not</b>, and they are all the same shape: Component scope, single-line, "
      "<b>weight 500</b>, at 12&nbsp;/&nbsp;14&nbsp;/&nbsp;24px. The Component composites at those "
      "sizes are all <b>400</b> &mdash; <code>.t-cm-legal</code> 12/400, <code>.t-cm-caption</code> "
      "and <code>.t-cm-tooltip</code> 14/400.<br><br>"
      "So either the corpus is right and the composite ladder is missing a Medium rung, or the "
      "corpus drifted and these should snap to Regular. <b>Binding them to the 400 composites "
      "would answer the question silently, in the direction nobody chose.</b></div>")

    A('<div class="null"><b>This sheet can come back null &mdash; and that is a real outcome.</b> '
      'If every family below reads fine at Regular, the answer is "drift: snap all '
      f'{total} to Regular, add no composites" and the ladder stays at eleven. '
      "Medium winning everywhere is equally valid, but it has to be <i>seen</i> here, not "
      "inherited from the fact that someone once typed 500.</div>")

    A('<div class="lead"><b class="warn">What this sheet is NOT.</b> It is not the reverse-text '
      "question. <code>{#col26-020}(c)</code> &mdash; 12/14/16px&nbsp;=&nbsp;Medium, "
      "20px&nbsp;=&nbsp;Light &mdash; was settled from the v2 specimen and is <b>conditional on "
      "reverse text over an extreme ground</b>. Only <b>family A</b> sits in that condition. "
      "The other four are on ordinary grounds where col26-020 has nothing to say. "
      "Keeping that separation visible is half the point: a rule quoted outside its condition is "
      "how a preference becomes a gate by accident.</div>")

    # ---- §1 the shape
    A("<h2>1 &middot; The shape of the 100</h2>")
    A('<p class="sub">Every row is real &mdash; selector, size and declared ground taken from the '
      "corpus, not composed for the sheet.</p>")
    A("<table><thead><tr><th>Family</th><th>What it is</th><th>Decls</th><th>Sizes</th>"
      "<th>Ground</th><th>In col26-020?</th></tr></thead><tbody>")
    shape = [
        ("A &middot; Reverse on primary", "toast, skip-link, count-badge", 12, "12, 14",
         "<code>var(--pri)</code> near-black", "<b>YES</b> &mdash; the only one"),
        ("B &middot; Eyebrow / group label", "eyebrow, list h2, group headings", 16, "12, 14",
         "inherited page", "no"),
        ("C &middot; Control label", "toggle, tab, segmented, nav", 31, "12, 14",
         "transparent", "no"),
        ("D &middot; Chip / tag / badge", "tag, chip, badge, avatar", 20, "12, 14",
         "<code>var(--surf)</code> quiet", "no"),
        ("E &middot; Numeral / data label", "num, delta, axis label, pct", 7, "12, 14, 24",
         "inherited page", "no"),
        ("&mdash; &middot; Unclassified", "13 one-off selectors, no family yet", other, "14, 24",
         "inherited page", "no"),
    ]
    for fam, what, n, sizes, ground, gov in shape:
        A(f"<tr><td><b>{fam}</b></td><td class='met'>{what}</td>"
          f"<td class='count'>{n}</td><td class='met'>{sizes}</td>"
          f"<td class='met'>{ground}</td><td class='met'>{gov}</td></tr>")
    A("</tbody></table>")

    # ---- §2 the eyeball
    A("<h2>2 &middot; Medium vs Regular, family by family</h2>")
    A('<p class="sub">Same specimen, same size, same ground &mdash; weight is the only variable. '
      "<b>Mark which column holds.</b> If Regular is fine, say so; that is the null result and it "
      "retires a composite request.</p>")

    for key, title, whatis, question, spec in FAMILIES:
        A('<div class="fam">')
        A(f"<h3>{key} &middot; {title}</h3>")
        A(f'<p class="sub" style="margin-bottom:8px">{whatis}</p>')
        A(f'<div class="q">{question}</div>')
        A("<table><thead><tr><th>Selector</th><th>Size</th>"
          "<th>500 &middot; Medium <span class='met'>(as authored)</span></th>"
          "<th>400 &middot; Regular <span class='met'>(as the composite says)</span></th>"
          "<th>Where</th><th class='ask'>Which holds?</th></tr></thead><tbody>")
        for sel, size, text, where in SPECIMENS[spec]:
            A(f"<tr><td><code>{sel}</code></td><td class='met'>{size}px</td>")
            A(f"<td>{render(spec, text, size, 500)}</td>")
            A(f"<td>{render(spec, text, size, 400)}</td>")
            A(f"<td class='met'>{where}</td><td class='ask'></td></tr>")
        A("</tbody></table>")
        A("</div>")

    # ---- §3 rulings
    A("<h2>3 &middot; To rule</h2>")
    A('<ol class="rules">')
    A("<li><b>R1 &mdash; per family, is Medium structural?</b> Five answers from &sect;2. "
      "Each <i>structural</i> answer costs a composite; each <i>drift</i> answer costs nothing "
      "and snaps to Regular. <b>[ per family: structural / drift ]</b></li>")
    A("<li><b>R2 &mdash; if family C is structural, is it really a new composite?</b> "
      "<code>.t-cm-button</code> is already 16px/<b>500</b>. Controls at 12/14px may be the same "
      "role at a smaller size, in which case the fix is <b>extending the button composite down "
      "the ramp</b> rather than adding <code>.t-cm-control-sm</code>. Cheaper, and it keeps the "
      "ladder honest about roles. <b>[ extend button / new composite ]</b></li>")
    A("<li><b>R3 &mdash; naming, if any composite is added.</b> The Editorial set already uses "
      "<code>.em</code> as its emphasis modifier. A Component equivalent could be "
      "<code>.t-cm-caption.em</code> rather than a parallel <code>-strong</code> family &mdash; "
      "one mechanism instead of two. R1 in <code>_TYPE-DECISIONS</code> left Component naming "
      "open for exactly this. <b>[ .em modifier / -strong family / other ]</b></li>")
    A("<li><b>R4 &mdash; Q5, carried forward from specimen v2 and still open.</b> Scope of the "
      "reverse-text rule: badges only, or every light-on-chroma surface (RAG banners, primary "
      "buttons, pressed states, tags)? Family A is the population it would bite. "
      "<b>[ library-wide / badges only ]</b></li>")
    A("<li><b>R5 &mdash; the two DataViz strays.</b> Independent of the above, both breaking "
      "existing rules: an <b>11px</b> size (below the 12px floor set in specimen v2) and a "
      "<b>font-weight 600</b> (<code>type25-004</code> &mdash; not a licensed weight, no OTF ships, "
      "so it renders as browser faux-bold). Confirm both snap to 12px / 500. "
      "<b>[ confirm / handle separately ]</b></li>")
    A("</ol>")

    A('<p class="foot">Generated by <code>reviews/gen_component_medium_specimen.py</code> '
      "&middot; every selector, size and ground taken from the live corpus &middot; licensed "
      "weights only &middot; <b>judge on YOUR screen with the real webfont</b> &mdash; the sandbox "
      "has no Univers, so these render in a fallback face and the weight difference will read "
      "differently here than it does for you. Nothing promoted; promotion is yours alone.</p>")
    A("</body></html>")

    with open(OUT, "w") as f:
        f.write("\n".join(h))
    print(f"wrote {os.path.relpath(OUT, ROOT)} — {len(FAMILIES)} families, "
          f"{sum(len(v) for v in SPECIMENS.values())} specimens, 5 rulings")


if __name__ == "__main__":
    build()
