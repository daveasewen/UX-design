#!/usr/bin/env python3
"""Candlestick four-state compare doc generator — #100 eyeball ①.

Emits reviews/CANDLESTICK-FOURSTATE-2026-08-05-v1.html:
  Variant A — two-state canon (#96-D1 ①): hollow = close>=open (gain stroke), filled = close<open (loss).
  Variant B — four-state (Dave's table, #100): colour = close vs PRIOR close, fill = close vs open.
Same seeded 40-session dataset in both. Canon frame 580×260, plot 46→568 / 14→230.
Deterministic: seed pinned. Asserts run in-script (fail loud, named).
"""
import random, json, sys, os

random.seed(103)  # session #100

N = 40
# ── data: intraday-style walk (cf. Dave's SPY screenshot — trend + chop) ──
sessions = []
prev_close = 100.0
# choppier profile (cf. Dave's SPY reference): down open, rally, dip, rally, stall
drift = [-0.5]*6 + [0.85]*10 + [-0.7]*7 + [0.9]*11 + [-0.15]*6
for i in range(N):
    o = prev_close + random.uniform(-1.3, 1.3)   # gap opens — the source of the divergent 4-states
    c = o + drift[i] + random.uniform(-1.8, 1.8)
    hi = max(o, c) + random.uniform(0.1, 1.1)
    lo = min(o, c) - random.uniform(0.1, 1.1)
    sessions.append(dict(o=round(o,2), h=round(hi,2), l=round(lo,2), c=round(c,2),
                         pc=round(prev_close,2)))
    prev_close = c

lo_all = min(s['l'] for s in sessions); hi_all = max(s['h'] for s in sessions)
# nice domain
import math
dmin = math.floor(lo_all/5)*5; dmax = math.ceil(hi_all/5)*5
PL, PR, PT, PB = 46, 568, 14, 230
def Y(v): return PB - (v-dmin)*(PB-PT)/(dmax-dmin)
step = (PR-PL)/N
bw = round(step*0.62, 1)          # body width ≈ 8.1 at N=40
def X(i): return PL + step*(i+0.5)

def classify2(s):  # canon: vs open
    return 'up' if s['c'] >= s['o'] else 'down'
def classify4(s):
    col = 'gain' if s['c'] > s['pc'] else 'loss'
    fill = 'hollow' if s['c'] > s['o'] else 'filled'
    return col, fill

def candles(mode):
    out = []
    for i, s in enumerate(sessions):
        x = X(i); bx = round(x-bw/2,1)
        fx = (i+0.5)/N          # fractional centre — dv-fit contract (data-fx on the group)
        by = round(min(Y(s['o']), Y(s['c'])),1)
        bh = round(max(abs(Y(s['o'])-Y(s['c'])), 1.2),1)
        wick = f'<line class="dv-wick" x1="{x:.1f}" y1="{Y(s["h"]):.1f}" x2="{x:.1f}" y2="{Y(s["l"]):.1f}"></line>'
        if mode == 2:
            cls = 'dv-up' if classify2(s)=='up' else 'dv-down'
        else:
            col, fill = classify4(s)
            cls = f'dv4-{col}-{fill}'
        lab = (f"Session {i+1}: open {s['o']}, high {s['h']}, low {s['l']}, close {s['c']}"
               + (f", prior close {s['pc']}" if mode==4 else ""))
        body = (f'<rect class="dv-body {cls}" x="{bx}" y="{by}" width="{bw}" height="{bh}" '
                f'tabindex="0" role="img" aria-label="{lab}" data-tip="{lab}"></rect>')
        out.append(f'<g class="dv-candle" data-fx="{fx:.4f}" data-x0="{x:.1f}">{wick}{body}</g>')
    return '\n        '.join(out)

def gridlines():
    out = []
    ticks = range(dmin, dmax+1, 5)
    for v in ticks:
        y = Y(v)
        out.append(f'<line class="dv-grid" data-fx="0" data-fx2="1" x1="{PL}" y1="{y:.1f}" x2="{PR}" y2="{y:.1f}"/>'
                   f'<text class="dv-axis t-cm-chart-value" x="38" y="{y+3:.1f}" text-anchor="end">{v}</text>')
    out.append(f'<line class="dv-axisline" data-fx="0" data-fx2="1" x1="{PL}" y1="{PB}" x2="{PR}" y2="{PB}"/>')
    return '\n        '.join(out)

def table_rows():
    r = []
    for i, s in enumerate(sessions):
        col, fill = classify4(s)
        r.append(f'<tr><th scope="row">S{i+1}</th><td>{s["o"]}</td><td>{s["h"]}</td>'
                 f'<td>{s["l"]}</td><td>{s["c"]}</td><td>{s["pc"]}</td>'
                 f'<td class="tag-{col}">{col}</td><td>{fill}</td></tr>')
    return '\n          '.join(r)

# ── asserts (fail loud, named) ──
c2 = [classify2(s) for s in sessions]
c4 = [classify4(s) for s in sessions]
n_up = c2.count('up'); n_down = c2.count('down')
from collections import Counter
c4c = Counter(c4)
assert n_up + n_down == N, "ASSERT-count2: 2-state classes don't sum to N"
assert sum(c4c.values()) == N, "ASSERT-count4: 4-state classes don't sum to N"
assert len(c4c) == 4 and min(c4c.values()) >= 4, \
    f"ASSERT-spread4: every 4-state needs >=4 examples for the eyeball, got {dict(c4c)}"
n_diverge = sum(1 for s in sessions
                if ('gain' if s['c'] > s['pc'] else 'loss') != ('gain' if s['c'] >= s['o'] else 'loss'))
assert n_diverge >= 8, f"ASSERT-diverge: only {n_diverge}/40 candles differ between variants — spread too weak to judge"
assert all(s['l'] <= min(s['o'],s['c']) and s['h'] >= max(s['o'],s['c']) for s in sessions), "ASSERT-ohlc: wick bounds violated"
assert abs(Y(dmin) - PB) < 1e-9 and abs(Y(dmax) - PT) < 1e-9, "ASSERT-scale: domain endpoints off plot frame"

svg2 = candles(2); svg4 = candles(4); grid = gridlines(); rows = table_rows()

fig = lambda fid, title, body, note: f'''
  <figure class="dv" role="group" aria-labelledby="{fid}-h">
    <figcaption id="{fid}-h" class="sr-only">{title}</figcaption>
    <div class="dv-head"><h3 class="dv-title t-cm-section-label">{title}</h3></div>
    <p class="t-cm-legal vnote">{note}</p>
    <div class="dv-stage"><div class="dv-chart-area">
      <svg class="dv-svg dv-fit" data-pl="{PL}" data-pr="12" data-h="260" viewBox="0 0 580 260" role="group" aria-label="{title}. 40 sessions, domain {dmin} to {dmax}.">
        {grid}
        {body}
      </svg>
    </div></div>
  </figure>'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Candlestick — two-state canon vs four-state variant (#100 review)</title>
<link rel="stylesheet" href="../knowledge/canon/type.css">
<style>
  :root{{ --font:"Univers Next for HSBC","Helvetica Neue",Arial,Helvetica,sans-serif; --ease:160ms cubic-bezier(.4,0,.2,1); }}
  [data-theme="light"]{{ --page:#FFFFFF; --ink:#1A1A1A; --baseline:#1A1A1A; --line:#E1E1E1;
    --data-delta-gain:#16864E; --data-delta-loss:#B92F1E;
    --data-axis:#626262; --axis-alpha:var(--alpha-60,.6); --data-grid:#626262; --grid-alpha:.1; }}
  [data-theme="dark"]{{ --page:#1A1A1A; --ink:#FFFFFF; --baseline:#FFFFFF; --line:#808080;
    --data-delta-gain:#1AA05C; --data-delta-loss:#CC4333;
    --data-axis:#9D9D9D; --axis-alpha:var(--alpha-60,.6); --data-grid:#9D9D9D; --grid-alpha:.16; }}
  *{{box-sizing:border-box}} body{{margin:0;padding:2.25rem;font-family:var(--font);background:var(--page);
    color:var(--ink);-webkit-font-smoothing:antialiased;transition:background var(--ease),color var(--ease);}}
  h1{{font-size:18px;font-weight:500;margin:0 0 .5rem}} h2{{font-size:14px;opacity:.6;margin:1.75rem 0 .7rem;font-weight:500}}
  .sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-4px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}
  .vnote{{opacity:.6;max-width:72ch;margin:.2rem 0 .8rem}}
  figure.dv{{margin:0 0 2.5rem}} .dv-head{{margin:0 0 4px}} .dv-title{{margin:0}}
  .dv-stage{{overflow-x:auto;padding-bottom:4px}} .dv-chart-area{{width:100%}}
  .dv-svg{{display:block;width:100%;height:260px;overflow:visible}}
  .dv-grid{{stroke:var(--data-grid);stroke-opacity:var(--grid-alpha);stroke-width:1}}
  .dv-axisline{{stroke:var(--baseline);stroke-width:1}}
  text.dv-axis{{fill:var(--data-axis);opacity:var(--axis-alpha)}}
  .dv-wick{{stroke:var(--ink);stroke-opacity:var(--alpha-60,.6);stroke-width:1}}
  /* Variant A — two-state canon (#96-D1 ①) */
  .dv-body.dv-up{{fill:var(--page);stroke:var(--data-delta-gain);stroke-width:1.5}}
  .dv-body.dv-down{{fill:var(--data-delta-loss);stroke:var(--data-delta-loss);stroke-width:1.5}}
  /* Variant B — four-state: colour = vs prior close · fill = vs open */
  .dv4-gain-hollow{{fill:var(--page);stroke:var(--data-delta-gain);stroke-width:1.5}}
  .dv4-gain-filled{{fill:var(--data-delta-gain);stroke:var(--data-delta-gain);stroke-width:1.5}}
  .dv4-loss-hollow{{fill:var(--page);stroke:var(--data-delta-loss);stroke-width:1.5}}
  .dv4-loss-filled{{fill:var(--data-delta-loss);stroke:var(--data-delta-loss);stroke-width:1.5}}
  .dv-body[tabindex]:focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}
  .themebtn{{position:fixed;top:16px;right:16px;height:32px;background:transparent;border:1px solid var(--line);
    color:var(--ink);padding:0 12px;cursor:pointer;font-family:var(--font)}}
  .themebtn:hover{{border-color:var(--ink)}}
  table.dv-table{{border-collapse:collapse;color:var(--ink)}}
  table.dv-table caption{{text-align:left;opacity:.6;margin-bottom:8px}}
  table.dv-table th,table.dv-table td{{border:1px solid var(--line);padding:3px 10px;text-align:right}}
  table.dv-table th[scope="row"]{{text-align:left;font-weight:500}}
  table.dv-table thead th{{opacity:.6;font-weight:500}}
  td.tag-gain{{color:var(--data-delta-gain)}} td.tag-loss{{color:var(--data-delta-loss)}}
  .keygrid{{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;align-items:center;max-width:60ch;margin:0 0 1.5rem}}
  .keyswatch{{width:14px;height:20px;display:inline-block}}
  details summary{{cursor:pointer;opacity:.7;margin:.5rem 0}}
  .dv-tip{{position:fixed;z-index:9;background:var(--page);color:var(--ink);border:1px solid var(--line);
    box-shadow:0 0 16px #00000033;padding:8px 12px;pointer-events:none;opacity:0;transition:opacity var(--ease)}}
  .dv-tip.on{{opacity:1}}
</style>
</head>
<body data-theme="light">
<button type="button" class="themebtn t-cm-chart-label" onclick="document.body.dataset.theme=document.body.dataset.theme==='light'?'dark':'light'">Theme</button>
<h1>Candlestick — density + hollow/filled encoding, decision spread (#100)</h1>
<p class="t-cm-legal vnote">Same seeded 40-session dataset in both specimens, canon 580×260 frame.
Variant A is today's canon (#96-D1 ①). Variant B spends the fill channel on a second axis
(close vs prior close = colour · close vs open = fill) — the real-chart convention from your reference;
the OHLC table below becomes the accessibility fallback. Rule by eye; tooltips carry full OHLC.</p>

{fig("va", "Variant A — two-state (close vs open)", svg2, "Hollow always = gain token, filled always = loss token: shape and colour agree, greyscale-safe.")}

{fig("vb", "Variant B — four-state (colour vs prior close, fill vs open)", svg4, "A hollow candle can be a loss vs yesterday; shape no longer mirrors colour — richer, but not greyscale-safe.")}

<h2>Key — the four states (Dave's table, verbatim semantics in Apollo tokens)</h2>
<div class="keygrid t-cm-legal">
  <span class="keyswatch" style="background:var(--data-delta-gain)"></span><span>Gain filled — close &gt; prior close, close &lt; open</span>
  <span class="keyswatch" style="background:var(--page);border:1.5px solid var(--data-delta-gain)"></span><span>Gain hollow — close &gt; prior close, close &gt; open</span>
  <span class="keyswatch" style="background:var(--data-delta-loss)"></span><span>Loss filled — close &lt; open and &lt; prior close</span>
  <span class="keyswatch" style="background:var(--page);border:1.5px solid var(--data-delta-loss)"></span><span>Loss hollow — close &gt; open but &lt; prior close</span>
</div>

<details open>
  <summary class="t-cm-chart-label">OHLC data table — the accessibility fallback ({N} sessions)</summary>
  <table class="dv-table t-cm-legal">
    <caption>Share price OHLC + prior close, 40 sessions. State columns show the four-state classification.</caption>
    <thead><tr><th scope="col">Session</th><th scope="col">Open</th><th scope="col">High</th><th scope="col">Low</th>
      <th scope="col">Close</th><th scope="col">Prior close</th><th scope="col">vs prior</th><th scope="col">Body</th></tr></thead>
    <tbody>
          {rows}
    </tbody>
  </table>
</details>

<script>
(function(){{var t=document.createElement('div');t.className='dv-tip t-cm-chart-value';document.body.appendChild(t);
document.addEventListener('pointermove',function(e){{var el=e.target.closest&&e.target.closest('[data-tip]');
if(el){{t.textContent=el.getAttribute('data-tip');t.classList.add('on');
var r=t.getBoundingClientRect(),x=e.clientX+14,y=e.clientY+14;
if(x+r.width>innerWidth-8)x-=r.width+28;if(y+r.height>innerHeight-8)y-=r.height+28;
t.style.left=x+'px';t.style.top=y+'px';}}else{{t.classList.remove('on');}}}});
document.addEventListener('focusin',function(e){{var el=e.target.closest&&e.target.closest('[data-tip]');
if(!el)return;var b=el.getBoundingClientRect();t.textContent=el.getAttribute('data-tip');t.classList.add('on');
t.style.left=(b.left+b.width/2)+'px';t.style.top=(b.top-40)+'px';}});
document.addEventListener('focusout',function(){{t.classList.remove('on');}});}})();

/* dv-fit reflow — ported from canon dv-behaviour (ADR-0015): horizontal positions relayout
   to container width; height + text NEVER scale (DV-D02). Body width scales with plot. */
(function(){{
  function fitOne(svg){{
    try{{
      var PL=parseFloat(svg.getAttribute('data-pl')||'46'),PR=parseFloat(svg.getAttribute('data-pr')||'12');
      var H=parseFloat(svg.getAttribute('data-h')||'260');
      var W=Math.round(svg.getBoundingClientRect().width); if(!W)return;
      var plotW=W-PL-PR; if(plotW<90)plotW=90;
      svg.setAttribute('viewBox','0 0 '+W+' '+H);
      var X=function(f){{return PL+parseFloat(f)*plotW;}};
      var bw=Math.max(3,Math.min(16,plotW/{N}*0.62));   /* body width tracks density */
      var els=svg.querySelectorAll('[data-fx]');
      for(var i=0;i<els.length;i++){{
        var el=els[i],x=X(el.getAttribute('data-fx')),tag=el.tagName.toLowerCase();
        if(tag==='line'){{el.setAttribute('x1',x.toFixed(1));
          var f2=el.getAttribute('data-fx2'); if(f2!==null)el.setAttribute('x2',X(f2).toFixed(1));}}
        else if(tag==='g'){{
          var x0=parseFloat(el.getAttribute('data-x0')||'0');
          el.setAttribute('transform','translate('+(x-x0).toFixed(1)+',0)');
          var r=el.querySelector('rect.dv-body');
          if(r)r.setAttribute('width',bw.toFixed(1)),r.setAttribute('x',(x0-bw/2).toFixed(1));
        }}
      }}
    }}catch(e){{}}
  }}
  function fitAll(){{var s=document.querySelectorAll('svg.dv-fit');for(var i=0;i<s.length;i++)fitOne(s[i]);}}
  var raf; window.addEventListener('resize',function(){{cancelAnimationFrame(raf);raf=requestAnimationFrame(fitAll);}});
  fitAll();
}})();
</script>
<!-- GENERATED by reviews/gen_candlestick_fourstate.py (seed 100). Classification counts:
     2-state up={n_up} down={n_down} · 4-state {json.dumps(dict(("-".join(k), v) for k,v in c4c.items()))} -->
</body>
</html>'''

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CANDLESTICK-FOURSTATE-2026-08-05-v1.html')
with open(out, 'w') as f: f.write(html)
print(f"WROTE {out}")
print(f"domain {dmin}->{dmax} · step {step:.2f}px · body {bw}px")
print(f"2-state: up={n_up} down={n_down} · 4-state: {dict(('-'.join(k), v) for k,v in c4c.items())}")
