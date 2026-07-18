#!/usr/bin/env python3
"""gen_type_retrofit.py — build the TYPE RETROFIT review doc from the gate's own inventory.

Sibling to the 4px-grid retrofit review (2026-07-17). Reads the live inventory emitted by
_validate_type_composites.py --inventory so the doc can never drift from the gate.

Usage:  python3 reviews/gen_type_retrofit.py            # run from repo root
Output: reviews/TYPE-RETROFIT-2026-07-18.html  (then run _make_review.py on it)

Nothing here APPLIES a change — every row is a proposal for Dave's ruling.
"""
import csv, io, os, re, subprocess, sys
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "knowledge", "_validate_type_composites.py")
OUT = os.path.join(ROOT, "reviews", "TYPE-RETROFIT-2026-07-18.html")

RAMP = [12, 14, 16, 20, 24, 28, 32, 40, 52]
WEIGHTS = [250, 300, 350, 400, 500]

# per-size proposal: (target, kind, note).  kind: rec = clean nearest | tie = equidistant
SIZE_CALLS = {
    13.0:   (14, "tie",  "Between 12 and 14. Overwhelmingly labels and captions — 14 keeps label legibility; 12 is the denser read."),
    15.0:   (16, "tie",  "Between 14 and 16. Mostly body and button text — 16 is <code>.t-cm-label</code> / <code>.t-ed-body</code>."),
    11.0:   (12, "rec",  "12 is the floor of the ramp; there is no step below it."),
    22.0:   (24, "tie",  "Between 20 and 24. Mixed: card <code>h3</code> reads as heading-3 (24); <code>.avatar.lg</code> is intrinsic scale — see rule 3."),
    13.5:   (14, "rec",  "Sub-pixel size — almost certainly unintended. Snaps clean."),
    19.0:   (20, "rec",  "All ten are the same selector (<code>.h h2</code>) — one ruling clears the row."),
    18.0:   (20, "tie",  "Between 16 and 20. <code>.av-lg</code> is intrinsic scale (rule 3); the header/hero text is heading-4 territory (20)."),
    17.0:   (16, "rec",  "Nearest step is 16. These are summary-total and drawer titles — emphasis should come from weight, not a +1px bump."),
    12.5:   (12, "rec",  "Sub-pixel — snaps clean to the ramp floor."),
    33.0:   (32, "rec",  "Clean: <code>.t-ed-heading-1</code>."),
    10.0:   (12, "rec",  "Below the ramp floor. Note 10px fails the accessibility floor anyway."),
    57.0:   (52, "rec",  "Clean: <code>.t-ed-display-1</code>."),
    30.0:   (32, "tie",  "Between 28 and 32. Account-card balance is a figure — <code>.t-cm-heading</code> (32) or <code>.t-ed-heading-2</code> (28)."),
    10.5:   (12, "rec",  "Sub-pixel, below the floor."),
    26.0:   (24, "tie",  "Between 24 and 28. Single occurrence: <code>.c-stat-cell__value</code>."),
}
WEIGHT_CALLS = {
    600: (500, "There is <b>no 600 composite</b>. 500 is the canon emphasis weight (the <code>.em</code> step). Alternative: extend the ramp with a 600 — but that widens the vocabulary."),
    700: (500, "There is <b>no 700 composite</b> either. Same call as 600."),
}


def inventory():
    out = subprocess.run([sys.executable, GATE, "--inventory"], capture_output=True, text=True).stdout
    return list(csv.DictReader(io.StringIO(out)))


def short(f):
    return (f.split("/")[-1].replace(".reference.html", "")
             .replace("-interactive.html", "").replace(".css", ""))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build():
    rows = inventory()
    t1 = [r for r in rows if r["code"] == "TYPE-001"]
    t2 = [r for r in rows if r["code"] == "TYPE-002"]
    t3 = [r for r in rows if r["code"] == "TYPE-003"]

    sizes, weights = defaultdict(list), defaultdict(list)
    for r in t3:
        m = re.match(r"([\d.]+)px", r["value"])
        (sizes[float(m.group(1))] if m else weights[int(r["value"].split()[0])]).append(r)

    inl = sum(1 for r in rows if r["selector"] == "._inl")
    t2_files = Counter(short(r["file"]) for r in t2)

    h = []
    A = h.append
    A('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>Type retrofit &mdash; review</title>")
    A("""<style>
:root{--ink:#1c1c1c;--mut:#6b6b6b;--line:#e4e4e4;--bg:#fff;--rec:#0b7a34;--tie:#b25000;--arrow:#8a1f1f;--exempt:#3a5bd9;--red:#db0011;}
*{box-sizing:border-box}
body{font-family:"Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;color:var(--ink);margin:0;padding:40px;max-width:1040px;line-height:1.5;background:#fafafa}
h1{font-size:32px;font-weight:300;margin:0 0 4px}
h2{font-size:20px;font-weight:500;margin:40px 0 4px;padding-top:16px;border-top:2px solid var(--ink)}
.sub{color:var(--mut);font-size:14px;margin:0 0 24px}
.lead{font-size:15px;background:#fff;border:1px solid var(--line);border-left:3px solid var(--red);padding:16px 20px;margin:20px 0}
table{width:100%;border-collapse:collapse;background:#fff;margin:12px 0 8px;font-size:13px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:500;font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:var(--mut);background:#f4f4f4}
td:last-child{width:120px;color:var(--mut)}
code{font-family:ui-monospace,Menlo,monospace;font-size:12px;background:#f2f2f2;padding:1px 5px;border-radius:3px}
.rec{color:var(--rec);font-weight:600} .tie{color:var(--tie);font-weight:600}
.tieflag{color:var(--tie);font-size:11px;font-weight:600} .arrow{color:var(--arrow);font-weight:600;font-size:12px}
.exempt{color:var(--exempt);font-weight:600}
.rules{background:#fff;border:1px solid var(--line);padding:4px 20px 16px;margin:16px 0}
.rules li{margin:12px 0;font-size:14px} .rules b{font-weight:600}
.num{background:#fff;border:1px solid var(--line);display:flex;gap:0;margin:16px 0}
.num div{padding:12px 18px;border-right:1px solid var(--line);flex:1}
.num div:last-child{border-right:0}
.num b{display:block;font-size:26px;font-weight:300;line-height:1.1}
.num span{font-size:11px;color:var(--mut);letter-spacing:.03em;text-transform:uppercase}
.foot{color:var(--mut);font-size:12px;margin-top:40px;border-top:1px solid var(--line);padding-top:12px}
</style></head><body>""")

    A("<h1>Type retrofit &mdash; review</h1>")
    A('<p class="sub">Apollo SDS &middot; queue&nbsp;#2 &middot; 2026-07-18 &middot; sibling to the 4px-grid retrofit. '
      "The grid retrofit snapped <b>dimensions</b>; this one governs <b>text</b>. "
      "Pin a comment on any row to rule; the four global rules resolve most of it.</p>")

    A('<div class="num">')
    A(f'<div><b>{len(t2)}</b><span>raw font decls to rebind</span></div>')
    A(f'<div><b>{len(t1)}</b><span>files not pulling type.css</span></div>')
    A(f'<div><b>{len(t3)}</b><span>off-ramp values</span></div>')
    A(f'<div><b>{len(SIZE_CALLS)+len(WEIGHT_CALLS)}</b><span>distinct rulings needed</span></div>')
    A("</div>")

    A('<div class="lead"><b>Read me first.</b> Type was promoted to canon on 07-17, but the library was '
      "never rebound to it: <b>0 of 50</b> component files reference a composite. This doc asks for "
      f"<b>{len(SIZE_CALLS)+len(WEIGHT_CALLS)} rulings</b>, not {len(t3)} &mdash; the off-ramp values collapse to "
      "15 distinct sizes and 2 weights. Rule the four global rules first, then override per row where design "
      "intent differs. <b>canon.css is generated</b> &mdash; every fix lands in the source snippet, then regenerate. "
      "Nothing is applied yet.</div>")

    A("<h2>Global rules &mdash; rule these once</h2>")
    A('<ol class="rules">')
    A("<li><b>Rule 1 &mdash; tie direction.</b> Where a size sits exactly between two ramp steps (13, 15, 18, 22, 26, 30) "
      "snap: <b>[ &nbsp;up&nbsp; ] &nbsp;[ &nbsp;down&nbsp; ] &nbsp;[ &nbsp;up for text, down for dense UI&nbsp; ]</b>. "
      '<i>Recommended: up for text, down for dense UI.</i> &nbsp;<span class="tieflag">&larr; pin your pick</span></li>')
    A("<li><b>Rule 2 &mdash; weights 600 and 700 have no composite.</b> "
      f"<b>{len(weights.get(600,[]))}</b> declarations use 600 and <b>{len(weights.get(700,[]))}</b> use 700; "
      "the ramp stops at 500. Either <b>collapse both to 500</b> (recommended &mdash; 500 is the canon emphasis step, "
      "and a narrower vocabulary is the point) or <b>extend type.css with a 600</b>. "
      '<b>[ collapse / extend ]</b> <span class="tieflag">&larr; this is the biggest single call in the doc</span></li>')
    A("<li><b>Rule 3 &mdash; intrinsic scale is not text.</b> Avatar initials, badge counts and similar set "
      "<code>font-size</code> to scale a glyph inside a fixed box &mdash; the size is driven by the box, not the type "
      "ramp. DEF-005 already carves out the equivalent case (a height equal to a width = intrinsic square size). "
      "Propose the same carve-out here: <b>exempt, governed by icon/avatar scale</b>. "
      "<b>[ exempt / gate them anyway ]</b></li>")
    A(f"<li><b>Rule 4 &mdash; inline <code>style=\"\"</code> attributes.</b> <b>{inl}</b> violations come from inline "
      "styles, which cannot take a composite class without a markup change. "
      "<b>[ promote to classes / accept as a documented exception ]</b></li>")
    A("</ol>")

    A("<h2>1 &middot; Off-ramp sizes &mdash; 15 rulings</h2>")
    A('<p class="sub">Grouped by value. Fix in the source snippet, then regenerate canon.css.</p>')
    A("<table><thead><tr><th>Value</th><th>N</th><th>Files (&times;count)</th><th>Proposed</th><th>Why</th><th>Your ruling</th></tr></thead><tbody>")
    for s in sorted(sizes, key=lambda x: -len(sizes[x])):
        rs = sizes[s]
        tgt, kind, note = SIZE_CALLS.get(s, (min(RAMP, key=lambda r: abs(r - s)), "rec", ""))
        fc = Counter(short(r["file"]) for r in rs)
        flist = ", ".join(f"{f}&times;{c}" for f, c in fc.most_common(6))
        if len(fc) > 6:
            flist += f" &hellip; +{len(fc)-6}"
        flag = ' <span class="tieflag">TIE &mdash; needs direction</span>' if kind == "tie" else ""
        A(f'<tr><td><b>{s:g}px</b></td><td>{len(rs)}</td><td>{flist}</td>'
          f'<td><span class="{kind}">&rarr; {tgt}px</span>{flag}</td><td>{note}</td><td></td></tr>')
    A("</tbody></table>")

    A("<h2>2 &middot; Off-ramp weights &mdash; 2 rulings</h2>")
    A('<p class="sub">See rule 2. These have no composite to bind to at all &mdash; the ramp does not contain them.</p>')
    A("<table><thead><tr><th>Value</th><th>N</th><th>Files (&times;count)</th><th>Proposed</th><th>Why</th><th>Your ruling</th></tr></thead><tbody>")
    for w in sorted(weights, key=lambda x: -len(weights[x])):
        rs = weights[w]
        tgt, note = WEIGHT_CALLS[w]
        fc = Counter(short(r["file"]) for r in rs)
        flist = ", ".join(f"{f}&times;{c}" for f, c in fc.most_common(6))
        if len(fc) > 6:
            flist += f" &hellip; +{len(fc)-6}"
        A(f'<tr><td><b>{w}</b></td><td>{len(rs)}</td><td>{flist}</td>'
          f'<td><span class="tie">&rarr; {tgt}</span> <span class="tieflag">no composite exists</span></td>'
          f"<td>{note}</td><td></td></tr>")
    A("</tbody></table>")

    A("<h2>3 &middot; Rebinding load &mdash; where the work sits</h2>")
    A('<p class="sub">TYPE-002: every raw font declaration in component scope, to be replaced by a composite class. '
      "No ruling needed per row &mdash; this is the mechanical sweep, shown so the scale is visible. "
      "The deciding rule: <b>single-line &rarr; Component (<code>.t-cm-*</code>); wrapping &rarr; Editorial "
      "(<code>.t-ed-*</code>)</b>. Multi-line Component text drifts off-grid (the N1 caveat).</p>")
    A("<table><thead><tr><th>File</th><th>Raw font decls</th><th>Pulls type.css?</th></tr></thead><tbody>")
    t1f = {short(r["file"]) for r in t1}
    NO = '<span class="arrow">no</span>'
    YES = '<span class="rec">yes</span>'
    for f, c in t2_files.most_common():
        A(f"<tr><td><code>{esc(f)}</code></td><td>{c}</td>"
          f"<td>{NO if f in t1f else YES}</td></tr>")
    A("</tbody></table>")

    A("<h2>4 &middot; Out of scope (logged, not gated)</h2>")
    A('<p class="sub">Demo-chrome &mdash; <code>.demo-controls</code> and reference-page harness furniture. '
      "Your ruling 2026-07-18: gate component scope now, log the chrome as a known deferral rather than a "
      "silent exemption. Recorded in <code>knowledge/_DS-IMPROVEMENTS.md</code>.</p>")

    A(f'<p class="foot">Generated by <code>reviews/gen_type_retrofit.py</code> from the live output of '
      f"<code>_validate_type_composites.py --inventory</code> &middot; ramp read from <code>canon/type.css</code> "
      f"({', '.join(str(r) for r in RAMP)}px; weights {', '.join(str(w) for w in WEIGHTS)}) &middot; "
      "nothing applied yet &mdash; this is a proposal for your sign-off.</p>")
    A("</body></html>")

    with open(OUT, "w") as fh:
        fh.write("\n".join(h))
    print(f"wrote {os.path.relpath(OUT, ROOT)}  "
          f"({len(t2)} rebinds · {len(t3)} off-ramp · {len(SIZE_CALLS)+len(WEIGHT_CALLS)} rulings)")


if __name__ == "__main__":
    build()
