#!/usr/bin/env python3
"""#261 lane F — build the self-contained OLD vs NEW review page.

Both documents are baked the way gen_showroom.py bakes an Open-↗ standalone doc: the snippet
bytes, type.css inlined, plus gen_theme_cascade.snippet_theme_css() so the four
[data-apollo-theme] slots actually resolve. Embedded base64 -> iframe srcdoc, so the page is
one file with no external reference.
"""
import os, sys, re, json, base64, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "knowledge", "canon"))
import gen_theme_cascade as gtc

TYPE = open(os.path.join(REPO, "knowledge", "canon", "type.css"), encoding="utf-8").read()
NEW = open(os.path.join(REPO, "knowledge", "snippets", "Filter-toolbar-bar.reference.html"), encoding="utf-8").read()
OLD = subprocess.check_output(["git", "-C", REPO, "show",
                              "HEAD:knowledge/snippets/Filter-toolbar-bar.reference.html"]).decode("utf-8")

def bake(src):
    mv = json.loads(re.search(r'id="token-manifest">\s*(\{.*?\})\s*</script>', src, re.S).group(1))["vars"]
    css = gtc.snippet_theme_css(mv, "filter-toolbar-bar")
    d = src.replace('<link rel="stylesheet" href="../canon/type.css">',
                    "<style>\n" + TYPE + "\n</style>\n<style>\n" + css + "\n</style>")
    d = d.replace("body{margin:0; padding:2.5rem;", "body{margin:0; padding:24px;")
    return base64.b64encode(d.encode("utf-8")).decode("ascii")

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Filter/toolbar bar — #261 lane F review</title>
<style>
  :root{--ink:#1A1A1A;--page:#FAFAFA;--paper:#FFFFFF;--line:#E1E1E1;--mid:#808080;--red:#DA1A00;--grid:24px;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--page);color:var(--ink);
    font:400 15px/22px "Univers Next for HSBC","Helvetica Neue",Arial,Helvetica,sans-serif;
    -webkit-font-smoothing:antialiased;}
  .wrap{max-width:1440px;margin:0 auto;padding:0 32px 96px;}
  header.masthead{border-bottom:2px solid var(--ink);padding:40px 0 16px;margin-bottom:32px;}
  .kicker{font-size:12px;letter-spacing:.06em;color:var(--mid);margin:0 0 12px;}
  h1{font-size:44px;line-height:48px;font-weight:300;margin:0 0 12px;max-width:22ch;}
  .lede{font-size:17px;line-height:26px;max-width:64ch;margin:0;}
  h2{font-size:13px;font-weight:500;letter-spacing:.06em;color:var(--mid);
     border-top:1px solid var(--ink);padding-top:8px;margin:56px 0 20px;}
  h3{font-size:20px;font-weight:400;margin:0 0 6px;}
  p{margin:0 0 12px;max-width:70ch;}
  .cols{display:grid;grid-template-columns:repeat(12,1fr);gap:24px;}
  .c4{grid-column:span 4}.c6{grid-column:span 6}.c8{grid-column:span 8}.c12{grid-column:span 12}
  @media(max-width:900px){.c4,.c6,.c8{grid-column:span 12}}
  .card{background:var(--paper);border:1px solid var(--line);padding:20px;}
  .card h3{margin-bottom:8px}
  .card p{font-size:14px;line-height:21px;color:#333;margin:0}
  table.spec{width:100%;border-collapse:collapse;font-size:14px;background:var(--paper);}
  table.spec th,table.spec td{text-align:left;vertical-align:top;padding:8px 12px;border-bottom:1px solid var(--line);}
  table.spec th{background:#F0F0F0;font-weight:500;white-space:nowrap;}
  table.spec code{font:400 12.5px/18px ui-monospace,SFMono-Regular,Menlo,monospace;}
  .bar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;background:var(--paper);
       border:1px solid var(--line);padding:12px;margin-bottom:0;position:sticky;top:0;z-index:5;}
  .bar .lab{font-size:12px;color:var(--mid);margin-right:4px;}
  .seg{display:inline-flex;border:1px solid var(--ink);}
  .seg button{font:inherit;font-size:13px;padding:6px 12px;border:0;background:transparent;
    color:var(--ink);cursor:pointer;min-height:32px;}
  .seg button[aria-pressed="true"]{background:var(--ink);color:#fff;}
  .seg button:focus-visible{outline:2px solid #305A85;outline-offset:-2px;}
  input[type=range]{width:220px;}
  .frames{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--line);border-top:0;}
  @media(max-width:1100px){.frames{grid-template-columns:1fr}}
  .frame{background:var(--paper);min-width:0;}
  .frame+.frame{border-left:1px solid var(--line);}
  .frame .cap{display:flex;gap:8px;align-items:baseline;padding:10px 12px;border-bottom:1px solid var(--line);
    font-size:12px;color:var(--mid);}
  .frame .cap b{font-size:13px;font-weight:500;color:var(--ink);}
  .frame iframe{display:block;width:100%;height:1560px;border:0;background:#fff;}
  .note{font-size:13px;color:var(--mid);margin-top:8px;}
  ul.tight{margin:0 0 12px 18px;padding:0;font-size:14px;line-height:21px;}
  ul.tight li{margin-bottom:6px;}
  .flag{color:var(--red);}
</style></head><body>
<div class="wrap">
<header class="masthead">
  <p class="kicker">Apollo · session #261 · lane F · design pass · PROPOSED, not ruled</p>
  <h1>Filter/toolbar bar</h1>
  <p class="lede">Dave's third nominated dashboard element, rebuilt as the thing that actually drives a
  dashboard. Old and new are side by side below, live, in all four themes and both modes — the same
  bytes the gates read, not a picture of them.</p>
</header>

<h2>What changed</h2>
<div class="cols">
  <div class="c4 card"><h3>It drives something</h3><p>The bar now publishes a documented event and
  attribute contract — <code>apollo:filter-change</code> out, <code>data-apollo-result-state</code>
  back — and the demo consumer under it re-queries 24 seeded transactions on every change. Written
  under s258-D1, which removed the no-JS rule.</p></div>
  <div class="c4 card"><h3>It has states</h3><p>Five, on one attribute: no filters, filtered,
  loading, zero results, error. Loading holds the count's position instead of blanking it; error
  shows an em-dash rather than a stale number dressed as a fresh one.</p></div>
  <div class="c4 card"><h3>It has an anatomy</h3><p>Search, add-filter menu, date-range trigger,
  applied-filter chips with a <code>+N more</code> overflow, results count, clear all, and
  right-aligned export and density. Every one composed from a gated atom; nothing re-drawn.</p></div>
</div>
<div class="cols" style="margin-top:24px">
  <div class="c6 card"><h3>It never lies about the answer</h3><p>The bar does not set its own state
  from the request it just made. It reads the consumer's <code>data-apollo-result-state</code> and
  moves to match. A driver that reports success because it dispatched an event is the defect the
  read-back leg exists to close.</p></div>
  <div class="c6 card"><h3>The date range hands off</h3><p>Presets resolve in the bar.
  <b>Custom range…</b> delegates to <code>date-range-picker</code>, which owns the calendar. Copying
  half of that component's body in here would be exactly the re-draw the Layer-2 rule forbids.</p></div>
</div>

<h2>Old and new — live, four themes, two modes</h2>
<p class="note">The frames are the real documents. Theme sets <code>html[data-apollo-theme]</code>,
mode sets <code>body[data-theme]</code>, width narrows the frame so the container queries fire.</p>
<div class="bar">
  <span class="lab">Theme</span>
  <span class="seg" id="segTheme">
    <button type="button" data-v="mono" aria-pressed="true">Mono</button>
    <button type="button" data-v="legacy" aria-pressed="false">Legacy</button>
    <button type="button" data-v="console" aria-pressed="false">Console</button>
    <button type="button" data-v="supercharge" aria-pressed="false">Supercharge</button>
  </span>
  <span class="lab">Mode</span>
  <span class="seg" id="segMode">
    <button type="button" data-v="light" aria-pressed="true">Light</button>
    <button type="button" data-v="dark" aria-pressed="false">Dark</button>
  </span>
  <span class="lab">Width</span>
  <input type="range" id="w" min="320" max="1440" value="1440" step="8" aria-label="Frame width">
  <span class="lab" id="wlab">full</span>
</div>
<div class="frames">
  <div class="frame"><p class="cap"><b>Before</b> — #210 wave-5 composition, at HEAD</p>
    <iframe id="fOld" title="Filter toolbar bar, before"></iframe></div>
  <div class="frame"><p class="cap"><b>After</b> — #261 design pass</p>
    <iframe id="fNew" title="Filter toolbar bar, after"></iframe></div>
</div>

<h2>The wiring contract</h2>
<table class="spec">
  <tr><th>Marker</th><td><code>data-apollo-filter-bar</code> on the driver ·
    <code>data-apollo-filter-target="&lt;selector&gt;"</code> optional ·
    <code>data-apollo-filter-consumer</code> on anything that renders a result set</td></tr>
  <tr><th>Emits</th><td><code>apollo:filter-change</code> {query, filters[{key,facet,value,label}],
    range{preset,days,label}, view, density} · <code>apollo:filter-clear</code> {} ·
    <code>apollo:filter-export</code> {format}. All bubble.</td></tr>
  <tr><th>Writes</th><td><code>data-apollo-view</code> and <code>data-apollo-density</code> onto the
    consumer — a CSS-only consumer responds with no script at all</td></tr>
  <tr><th>Reads back</th><td><code>data-apollo-result-count</code> ·
    <code>data-apollo-result-total</code> · <code>data-apollo-result-state</code> =
    ok | loading | empty | error</td></tr>
  <tr><th>Budget</th><td>No network, no <code>setInterval</code>, no external script. One
    rAF-debounced resize listener. 14,145 code-only bytes of 16,384 (ADR-0015).</td></tr>
</table>

<h2>The five states, and what each one refuses to do</h2>
<table class="spec">
  <tr><th>no filters</th><td>Total count plus a "No filters applied" hint. No chip row, no clear-all
    — a clear-all with nothing to clear is furniture.</td></tr>
  <tr><th>filtered</th><td><code>N of M</code>, the chip row with a <code>+N more</code> disclosure
    past three, and clear-all.</td></tr>
  <tr><th>loading</th><td>A skeleton where the count sits, so the row does not jump, plus the words
    "Updating results" through <code>role=status</code>/<code>aria-live=polite</code>. The controls
    are <b>never disabled</b> — a filter you cannot change while it runs is a trap.</td></tr>
  <tr><th>zero results</th><td><code>0 of M</code> and the chips that produced the zero, so the user
    can see what to remove, plus a message and a clear-all action.</td></tr>
  <tr><th>error</th><td>An em-dash where the count would be, and a block carrying an error triangle,
    a title and a sentence saying nothing was changed. Colour is the third channel, never the only
    one — the declaration is measured at the browser, not asserted.</td></tr>
</table>

<h2>Receipts</h2>
<table class="spec">
  <tr><th>snippet gate</th><td>137 snippets, 0 failures</td></tr>
  <tr><th>behaviour gate</th><td>OK — 14,145 code-only bytes of 16,384 per source; one rAF-debounced resize listener</td></tr>
  <tr><th>type composites</th><td>PASS — no raw font declaration in component scope</td></tr>
  <tr><th>icon source</th><td>0 UNKNOWN, 17 bespoke (the neutral selection tick, ×17 instances)</td></tr>
  <tr><th>grid</th><td>PASS — every layout dimension on the 4px grid</td></tr>
  <tr><th>coverage</th><td>137 metas / 137 snippets, 0 failures</td></tr>
  <tr><th>hit area (driven, Chromium)</th><td>1440 / 680 / 375px — 144 targets measured,
    <b>0 BREACH-FLOOR</b>; every seat at or above the 24px dial-down floor</td></tr>
  <tr><th>state contrast (driven)</th><td>0 carrier failures — the numerals declare
    <code>label</code> (the minus sign), the error block declares <code>symbol label</code></td></tr>
  <tr><th>render</th><td>4 themes × 2 modes shot in headless Chromium at the real face
    (canvas probe 346.88 vs 301.07)</td></tr>
</table>

<h2>Two defects the render caught that no static gate would have</h2>
<ul class="tight">
  <li><span class="flag">Chips shrunk to a single letter.</span> With <code>flex:0 1 auto</code> and
  no floor, the chip group was squeezed by its neighbours to about ten pixels and every chip
  rendered as one clipped character. The group now declares a 200px floor, and the two-rows-to-one
  collapse is a consequence of both groups fitting at their floors rather than a claim about width.</li>
  <li><span class="flag">Three views painted at once.</span> <code>[hidden]</code> is specificity
  (0,1,0) and lost to <code>.ftb-msg{display:flex}</code>, <code>.demo-cards{display:grid}</code>
  and the table — so the empty message, the error message and both views rendered together while
  <code>hidden</code> told assistive tech they were gone. The remedy rule is now in the file.</li>
</ul>
</div>
<script>
  var OLD="__OLD__", NEW="__NEW__";
  var state={theme:"mono",mode:"light"};
  function decode(b){return new TextDecoder().decode(Uint8Array.from(atob(b),function(c){return c.charCodeAt(0)}));}
  function doc(b){
    var s=decode(b);
    if(state.theme!=="mono") s=s.replace('<html lang="en">','<html lang="en" data-apollo-theme="'+state.theme+'">');
    return s.replace('<body data-theme="light">','<body data-theme="'+state.mode+'">');
  }
  function paint(){
    document.getElementById("fOld").srcdoc=doc(OLD);
    document.getElementById("fNew").srcdoc=doc(NEW);
  }
  function wire(id,key){
    var g=document.getElementById(id);
    g.querySelectorAll("button").forEach(function(b){
      b.addEventListener("click",function(){
        g.querySelectorAll("button").forEach(function(x){x.setAttribute("aria-pressed",String(x===b));});
        state[key]=b.dataset.v; paint();
      });
    });
  }
  wire("segTheme","theme"); wire("segMode","mode");
  /* the slider is a plain px dial, 320 to 1440; 1440 means "let the frame have the column" */
  var w=document.getElementById("w"), wl=document.getElementById("wlab");
  w.min=320; w.max=1440; w.step=8; w.value=1440;
  w.addEventListener("input",function(){
    document.querySelectorAll(".frame iframe").forEach(function(f){
      f.style.width = (+w.value>=1440? "100%" : w.value+"px");
    });
    wl.textContent = (+w.value>=1440? "full" : w.value+"px");
  });
  paint();
</script>
</body></html>"""

out = PAGE.replace("__OLD__", bake(OLD)).replace("__NEW__", bake(NEW))
path = os.path.join(HERE, "261-F-filter-toolbar-review.html")
open(path, "w", encoding="utf-8").write(out)
print("wrote", path, len(out), "bytes")
