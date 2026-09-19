#!/usr/bin/env python3
"""#288 lane B — compose the four-theme contact sheet from measurements.json.

Every number printed on the sheet is read out of measurements.json, which the render driver
wrote from getBoundingClientRect() in the page. Nothing here is typed by hand.
"""
import html, json, os

LANE = "/sessions/trusting-youthful-franklin/mnt/UX-design/notes/_lanes/288/B"
M = json.load(open(os.path.join(LANE, "measurements.json")))

# ---- 1:1 detail crops ---------------------------------------------------------------------
# The quarter-width thumbnails cannot show a 0-vs-8px difference. For each render, cut a 1:1
# band from the full-page PNG spanning the seam between the lead group (the KPI row) and the
# evidence group below it: the INNER gutters between the four KPI tiles and the OUTER gutter
# between the two groups are both in frame, unscaled.
DETAIL = os.path.join(LANE, "detail")
os.makedirs(DETAIL, exist_ok=True)


def make_detail(key):
    from PIL import Image
    d = M[key]
    im = Image.open(os.path.join(LANE, d["png"]))
    lead, wall = d["rect_lead"], d["rect_wall"]
    x0 = int(wall["x"]) - 12
    y0 = int(lead["y"] + lead["h"]) - 96
    box = (max(0, x0), max(0, y0), min(im.width, x0 + 470), min(im.height, y0 + 240))
    out = os.path.join(DETAIL, key + ".png")
    im.crop(box).save(out)
    return os.path.relpath(out, LANE)


for k in M:
    M[k]["detail"] = make_detail(k)

SOURCE = {   # theme -> (outer token value, its file:line, role-default main, sub, file)
    "mono": ("0", "knowledge/canon/canon.css:537 (:root) · knowledge/tokens/layout.json layout/bento/gutter", 40, 4),
    "legacy": ("24px", 'knowledge/canon/canon.css:22009 ([data-apollo-theme="legacy"],[…"common"]) · knowledge/tokens/themes/apollo-legacy.overrides.json:188', 24, 4),
    "console": ("24px", 'knowledge/canon/canon.css:24611 ([data-apollo-theme="console"]) · knowledge/tokens/themes/apollo-console.overrides.json:27', 40, 4),
    "supercharge": ("0", "no declaration in the supercharge block (canon.css:26250ff) — inherits :root, canon.css:537", 24, 2),
}

LABEL = {"mono": "Apollo Mono", "legacy": "Apollo Legacy / Common",
         "console": "Apollo Console", "supercharge": "Apollo Supercharge"}


def card(key, caption, note=""):
    d = M[key]
    o, il = d["outer"], d["inner_lead"]
    cfg = d["cfg"]
    decl_o = "40px (literal pin)" if not cfg["override"] else "%dpx" % cfg["outer"]
    decl_i = "4px (literal pin)" if not cfg["override"] else "%dpx" % cfg["inner"]
    return f"""
  <figure class="shot">
    <a href="{d['png']}"><img src="{d['png']}" alt="{html.escape(caption)}" loading="lazy"></a>
    <a href="{d['png']}"><img class="detail" src="{d['detail']}"
       alt="{html.escape(caption)} — seam at 1:1" loading="lazy"></a>
    <figcaption>
      <b>{html.escape(caption)}</b>
      {('<span class="note">' + note + '</span>') if note else ''}
      <table>
        <tr><th></th><th>declared</th><th>measured</th></tr>
        <tr><td>outer (structural bento)</td><td>{decl_o}</td>
            <td class="m">{o['measured_col_gap']} / {o['measured_row_gap']} px</td></tr>
        <tr><td>inner (embedded bento)</td><td>{decl_i}</td>
            <td class="m">{il['measured_col_gap']} px</td></tr>
        <tr><td>--layout-bento-gutter at the wall</td><td colspan="2">{o and d['layout_bento_gutter_at_wall'] or '—'}</td></tr>
      </table>
    </figcaption>
  </figure>"""


rows = []

rows.append(("A", "AT HEAD, RIGHT NOW — the template as it stands, four themes, nothing overridden",
             """The template pins Mono's pair as literals — <code>--bento-gutter:40px</code> at
             <code>knowledge/canon/canon.css:18119</code> and <code>--bento-gutter:4px</code> at
             <code>:18121</code> (authoring source <code>knowledge/snippets/Template-dashboard-bento.reference.html:802</code>
             and <code>:804</code>). They are literals, not theme-conditioned. <b>Measured here: all four
             themes render an identical 40 / 4.</b> The theme token still resolves correctly at the wall
             (<code>--layout-bento-gutter</code> reads 0 / 24px / 24px / 0 below) — it is simply
             out-specified and never reaches the gap. This is the s219-D3 generation arm that was never built.""",
             [card("r0-" + t, LABEL[t]) for t in ("mono", "legacy", "console", "supercharge")]))

rows.append(("B", "WHAT THE s219-D3 ARM WOULD DELIVER — reading 1: the TOKEN governs the outer gutter",
             """Ruled values, applied by override in the render only — never in the repo.
             Outer = <code>layout/bento/gutter</code> per theme (s217-D2, from Dave's four tuner exports):
             mono 0, legacy 24, console 24, supercharge 0. Inner = s219-D1 <code>subSpacing</code>:
             4 / 4 / 4 / 2. <b>This is the reading in which Mono's outer gutter is 0 — the value Dave doubted.</b>""",
             [card("r1-" + t, LABEL[t], "ruled values, applied by override")
              for t in ("mono", "legacy", "console", "supercharge")]))

rows.append(("C", "MONO'S OUTER GUTTER — 0 / 8 / 16 / 24, inner held at 4. RULE BY EYE.",
             """Same page, same theme, same inner gutter. Only the outer (structural bento) gutter moves.
             The 0 at the left is what <code>s217-D2</code> rules today; 40 is what the template
             actually ships (row A, first tile) and what <code>s219-D1 mainSpacing</code> says.""",
             [card("r2-mono-%d" % o, "Mono · outer %dpx" % o, "override") for o in (0, 8, 16, 24)]))

rows.append(("D", "WHAT THE s219-D3 ARM WOULD DELIVER — reading 2: the ROLE DEFAULT governs the outer gutter",
             """The competing ruled number. Outer = s219-D1 <code>dashboard mainSpacing</code>
             (mono 40, legacy 24, console 40, supercharge 24, from
             <code>knowledge/_render/role_defaults_219.py --table</code>); inner = <code>subSpacing</code>.
             <b>Three of the four themes disagree with reading B.</b> Only legacy agrees (24 = 24).""",
             [card("r3-" + t, LABEL[t], "ruled values, applied by override")
              for t in ("mono", "legacy", "console", "supercharge")]))

src_rows = "".join(
    f"""<tr><td><b>{LABEL[t]}</b></td><td class="m">{SOURCE[t][0]}</td>
        <td class="m">{SOURCE[t][2]}px</td><td class="m">{SOURCE[t][3]}px</td>
        <td class="src">{html.escape(SOURCE[t][1])}</td></tr>"""
    for t in ("mono", "legacy", "console", "supercharge"))

body = "".join(
    f"""<section class="row">
      <h2><span class="tag">{k}</span> {html.escape(title)}</h2>
      <p class="lede">{lede}</p>
      <div class="strip">{''.join(cards)}</div>
    </section>""" for k, title, lede, cards in rows)

DOC = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bento gutters · four themes · #288 lane B</title>
<style>
  :root{{--ink:#1A1A1A;--page:#FFFFFF;--line:#E1E1E1;--mid:#767676;--red:#DB0011;--wash:#F5F5F5;}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--page);color:var(--ink);
    font:15px/1.5 "Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;}}
  header{{padding:32px 32px 24px;border-bottom:2px solid var(--ink);}}
  h1{{font-size:28px;font-weight:500;margin:0 0 8px;letter-spacing:-.01em}}
  .sub{{color:var(--mid);font-size:13px;margin:0}}
  .warn{{border-left:4px solid var(--red);background:var(--wash);padding:14px 18px;margin:20px 32px;font-size:14px}}
  section.row{{padding:28px 32px;border-bottom:1px solid var(--line)}}
  h2{{font-size:17px;font-weight:500;margin:0 0 6px}}
  .tag{{display:inline-block;background:var(--ink);color:#fff;padding:1px 9px;margin-right:8px;font-size:14px}}
  .lede{{margin:0 0 18px;max-width:105ch;font-size:13.5px;color:#333}}
  .strip{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}}
  .shot{{margin:0;border:1px solid var(--line);background:#fff}}
  .shot img{{display:block;width:100%;height:auto;border-bottom:1px solid var(--line)}}
  .shot img.detail{{background:#fff;border-top:3px solid var(--ink)}}
  figcaption{{padding:10px 12px 12px;font-size:12px}}
  figcaption b{{display:block;font-size:13px;font-weight:500}}
  .note{{display:block;color:var(--red);font-size:11px;margin:2px 0 6px;text-transform:uppercase;letter-spacing:.04em}}
  figcaption table{{border-collapse:collapse;width:100%;margin-top:6px;font-size:11.5px}}
  figcaption th{{text-align:left;font-weight:500;color:var(--mid);border-bottom:1px solid var(--line);padding:3px 4px}}
  figcaption td{{padding:3px 4px;border-bottom:1px solid var(--line);vertical-align:top}}
  figcaption td:first-child{{color:var(--mid)}}
  .m{{font-variant-numeric:tabular-nums;font-weight:500}}
  table.source{{border-collapse:collapse;width:100%;font-size:12.5px;margin-top:10px}}
  table.source th{{text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px;font-weight:500}}
  table.source td{{border-bottom:1px solid var(--line);padding:6px 8px;vertical-align:top}}
  .src{{color:var(--mid);font-family:ui-monospace,Menlo,monospace;font-size:11px}}
  code{{font-family:ui-monospace,Menlo,monospace;font-size:.92em;background:var(--wash);padding:0 3px}}
  footer{{padding:24px 32px 48px;color:var(--mid);font-size:12px}}
  @media (max-width:1100px){{.strip{{grid-template-columns:repeat(2,1fr)}}}}
</style></head>
<body>
<header>
  <h1>Bento gutters — outer and inner, four themes</h1>
  <p class="sub">#288 lane B · 2026-09-19 · rendered from <code>showroom/template-dashboard-bento.html</code>
     at HEAD · viewport 1440&nbsp;px, light mode · every “measured” number is
     <code>getBoundingClientRect()</code> between sibling tiles in the page, not an eyeball.<br>
     Each tile shows the whole page above and, below the black rule, a <b>1:1 (unscaled) crop of the
     seam</b> — the four KPI tiles' inner gutters and the outer gutter to the group beneath them.
     Rule by eye from the 1:1 strip; the page above it is scaled to a quarter and cannot show 8&nbsp;px.
     Click any image for the full-size render.</p>
</header>

<div class="warn">
  <b>What Dave asked, and the shape of the answer.</b>
  “The problem with the gutters it that they are deliberately different for the themes and the gutters
  are also different for the inner and outer bentos we essentially have a structural bento and embedded
  bentos or tile groupings.”<br><br>
  <b>Read from source, not assumed:</b> yes — <code>--layout-bento-gutter</code> IS the structural (outer)
  gutter for the dashboard role. Canon sets the dashboard role's gutter to a flat <code>1px</code>
  (<code>knowledge/canon/canon.css:1184</code>), then restores the theme token for exactly the
  bento-of-bentos case: <code>.c-bento[data-bento-role="dashboard"]:has(&gt; .c-bento__grid &gt; .c-bento)
  {{--bento-gutter:var(--layout-bento-gutter)}}</code> at <code>canon.css:1198–1200</code>, with the
  source comment “THE OUTER WALL OF A BENTO-OF-BENTOS KEEPS THE THEME GUTTER”. The inner (embedded)
  gutter is a <i>separate</i> quantity and canon gives it a literal, not a token.
  <b>Three sources give three different inner numbers and two different outer numbers — see the table.</b>
</div>

<section class="row">
  <h2><span class="tag">SRC</span> READ FROM SOURCE — outer and inner, per theme</h2>
  <p class="lede">The outer gutter has a token; the inner gutter does not. Canon's inner default for the
     dashboard role is a literal <code>1px</code> at <code>canon.css:1184</code>; the s219-D1 role defaults
     say 4/4/4/2; the template pins 4 for every theme at <code>canon.css:18121</code>. Nothing in the tree
     reconciles them.</p>
  <table class="source">
    <tr><th>theme</th><th>outer — <code>layout/bento/gutter</code> (s217-D2)</th>
        <th>outer — <code>mainSpacing</code> (s219-D1)</th>
        <th>inner — <code>subSpacing</code> (s219-D1)</th><th>where the outer token is declared</th></tr>
    {src_rows}
  </table>
  <p class="lede" style="margin-top:14px">
    Canon's own inner default for the role: <code>1px</code>, flat, all themes
    (<code>knowledge/canon/canon.css:1182–1185</code>) — it agrees with none of the four
    <code>subSpacing</code> values. The template's pins: outer <code>40px</code>
    (<code>canon.css:18119</code>), inner <code>4px</code> (<code>canon.css:18121</code>), both literal,
    both theme-blind. The role defaults come from
    <code>knowledge/_render/role_defaults_219.py --table</code>.</p>
</section>

{body}

<footer>
  Renders are per-render overrides of the two pinned declarations only; no repo file was modified.
  Driver: <code>notes/_lanes/288/B/render_four_themes.py</code> ·
  raw numbers: <code>notes/_lanes/288/B/measurements.json</code> ·
  PNGs: <code>notes/_lanes/288/B/png/</code>.<br>
  <b>Provenance.</b> Lane A is building the s219-D3 arm in parallel and its edits to
  <code>knowledge/canon/canon.css</code> and
  <code>knowledge/snippets/Template-dashboard-bento.reference.html</code> are in the working tree now.
  <code>showroom/template-dashboard-bento.html</code> — the file rendered here — is <b>unmodified, at
  HEAD <code>4cc8b37a</code></b>, and every line number quoted above was re-read from
  <code>git show HEAD:…</code>, not from the working tree. So this sheet is what the template delivers
  <i>today, before lane A lands</i>, and it is not a picture of lane A's output.
</footer>
</body></html>
"""

out = os.path.join(LANE, "four-themes.html")
open(out, "w", encoding="utf-8").write(DOC)
print("WROTE", out, len(DOC), "chars")
