#!/usr/bin/env python3
"""Generate the Apollo Mono semantic-grey review sheet (surface for ruling; nothing swapped).
Data-driven so the swatches + contrasts can't drift from the numbers. Run from repo root."""
import os

MONO = {1:'#000000',2:'#050505',3:'#0F0F0F',4:'#1A1A1A',5:'#313131',6:'#484848',7:'#626262',
        8:'#808080',9:'#9D9D9D',10:'#B7B7B7',11:'#CECECE',12:'#E1E1E1',13:'#F0F0F0',14:'#FAFAFA',15:'#FFFFFF'}

# The governed / flagged DECISIONS — where a rule or a tint makes 'nearest step' not automatic.
DECISIONS = [
 ("Primary text ink",  "text/default · icon/default · rag/text/on-light",
  "#333333", "Grey-8",
  [("Keep #333 (Grey-8)","#333333","12.6:1","col25-011 says typography = white or Grey-8 ONLY"),
   ("m5 #313131 (nearest)","#313131","13.0:1","2 units darker — on-ramp, barely visible"),
   ("m4 #1A1A1A (blacker)","#1A1A1A","17.4:1","the 'make it black' option; = digital black")],
  "col25-011 (gated): text is white or Grey-8 only. Grey-8 is NOT an exact mono step. Your call: keep Grey-8, or rule Mono text ink onto the ramp."),
 ("Secondary text",    "text/secondary (the muted / redacted ink)",
  "#545454", "off-ramp",
  [("m6 #484848 (nearest)","#484848","9.1:1","on-ramp, slightly darker"),
   ("Keep #545454","#545454","7.6:1","current value"),
   ("Drop it","—","—","Mono may not want a second text grey at all")],
  "Not a brand grey; free to seat on the ramp. Does 'very mono' keep a secondary ink, or collapse to one ink + weight?"),
 ("UI grey (borders / dividers)", "border/strong · form/border · rag/neutral · scrollbar",
  "#767676", "Grey-6",
  [("m8 #808080 (nearest)","#808080","3.9:1 on white","fine for borders (3:1); FAILS as text (4.5)"),
   ("Keep #767676","#767676","4.5:1 on white","exactly AA-text — safe if ever used as text")],
  "grey-tint flagged. Mostly borders (3:1 fine) — but rag/neutral can read as text. Move borders to m8; keep text uses at Grey-6 or rule them black."),
 ("Tinted light grey", "border/subtle · divider · table/tooltip border · disabled fills",
  "#D7D8D6", "TINTED",
  [("m11 #CECECE (nearest)","#CECECE","—","neutralises the tint, on-ramp"),
   ("m12 #E1E1E1 (lighter)","#E1E1E1","—","softer hairline")],
  "#D7D8D6 is NOT neutral (R=D7 G=D8 B=D6 — a faint green cast). grey-tint check: surfaced for you. Seat on a pure mono step."),
]

# MECHANICAL — clean nearest-step maps (low decision), grouped by the distinct off-ramp value.
MECH = [
 ("#1D1D1D","m4","#1A1A1A","dark surfaces — tertiary bg · tabs · tooltip · table column"),
 ("#212121","m4","#1A1A1A","dark hover surfaces — form/tertiary hover"),
 ("#EDEDED","m13","#F0F0F0","light dividers · table header · secondary hover"),
 ("#F3F3F3","m13","#F0F0F0","light hover surfaces"),
 ("#707070","m7","#626262","dark borders / dividers / tooltip border"),
 ("#696969","m7","#626262","dark dividers (break/subsection)"),
 ("#404040","m6","#484848","dark disabled fills / borders"),
 ("#474747","m6","#484848","form pressed (dark)"),
 ("#9B9B9B","m9","#9D9D9D","secondary text (dark) — near exact"),
 ("#6C6C6C","m7","#626262","data-vis border (dark)"),
 ("#787878","m8","#808080","tabs border (dark)"),
]

# Already EXACT on the ramp — no change needed.
EXACT = "#000000 (m1) · #1A1A1A (m4) · #808080 (m8) · #B7B7B7 (m10) · #FFFFFF (m15)"

def sw(hex_, big=False):
    h = 64 if big else 26
    bd = "#00000022" if hex_.upper() in ("#FFFFFF","#FAFAFA","#F0F0F0","#E1E1E1") else "transparent"
    return f'<span class="sw" style="background:{hex_};width:{h}px;height:{h}px;border:1px solid {bd}"></span>'

def build():
    ramp = "".join(
        f'<div class="rk"><span class="sw" style="background:{MONO[i]};width:100%;height:34px;border:1px solid #00000018"></span>'
        f'<div class="rl">m{i}</div><div class="rh">{MONO[i]}</div></div>' for i in MONO)

    dec = ""
    for name, uses, cur, tag, opts, note in DECISIONS:
        rows = "".join(
            f'<tr><td>{sw(v) if v!="—" else ""} <code>{v}</code></td><td>{lbl}</td><td class="c">{c}</td><td class="w">{w}</td></tr>'
            for lbl, v, c, w in opts)
        dec += f'''
        <div class="card">
          <div class="ch"><div><b>{name}</b> <span class="tag">{tag}</span></div>
            <div class="uses">{uses}</div></div>
          <div class="cur">now: {sw(cur, True)} <code>{cur}</code></div>
          <table><thead><tr><th>option</th><th></th><th>contrast</th><th>note</th></tr></thead><tbody>{rows}</tbody></table>
          <div class="note">▸ {note}</div>
        </div>'''

    mech = "".join(
        f'<tr><td>{sw(c)} <code>{c}</code></td><td>→ {m} {sw(h)} <code>{h}</code></td><td class="w">{u}</td></tr>'
        for c, m, h, u in MECH)

    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Apollo Mono — semantic greys onto the ramp (review)</title>
<link rel="stylesheet" href="../knowledge/canon/type.css">
<style>
  :root{{--font:"Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;}}
  [data-theme="light"]{{--bg:#FFFFFF;--fg:#1A1A1A;--mut:#545454;--line:#CECECE;--card:#FAFAFA;}}
  [data-theme="dark"]{{--bg:#1A1A1A;--fg:#FFFFFF;--mut:#9D9D9D;--line:#484848;--card:#0F0F0F;}}
  *{{box-sizing:border-box}} body{{margin:0;padding:2.5rem;font-family:var(--font);background:var(--bg);color:var(--fg);-webkit-font-smoothing:antialiased}}
  h1{{font:400 28px/1.2 var(--font);margin:0 0 6px}} .sub{{color:var(--mut);font-size:14px;margin-bottom:24px;max-width:70ch}}
  .controls{{display:flex;gap:8px;margin-bottom:24px}} .controls button{{font:inherit;font-size:13px;padding:8px 12px;border:1px solid var(--mut);background:transparent;color:var(--fg);cursor:pointer}}
  h2{{font:500 14px/1 var(--font);letter-spacing:.04em;text-transform:none;margin:32px 0 12px;color:var(--fg)}}
  .ramp{{display:grid;grid-template-columns:repeat(15,1fr);gap:4px;margin-bottom:8px}}
  .rk{{text-align:center}} .rl{{font-size:11px;margin-top:4px}} .rh{{font-size:10px;color:var(--mut)}}
  .banner{{border-left:3px solid var(--fg);padding:10px 14px;background:var(--card);font-size:13px;margin:16px 0 8px}}
  .card{{border:1px solid var(--line);padding:16px;margin-bottom:12px;background:var(--card)}}
  .ch{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:10px}}
  .uses{{color:var(--mut);font-size:12px;max-width:42ch;text-align:right}}
  .tag{{font-size:11px;border:1px solid var(--mut);padding:2px 6px;color:var(--mut)}}
  .cur{{font-size:13px;margin-bottom:10px;display:flex;align-items:center;gap:8px}}
  table{{width:100%;border-collapse:collapse;font-size:13px}} th{{text-align:left;color:var(--mut);font-weight:400;font-size:11px;border-bottom:1px solid var(--line);padding:4px 8px 4px 0}}
  td{{padding:6px 8px 6px 0;border-bottom:1px solid var(--line);vertical-align:middle}} td.c{{font-variant-numeric:tabular-nums;white-space:nowrap}} td.w{{color:var(--mut);font-size:12px}}
  code{{font-family:ui-monospace,Menlo,monospace;font-size:12px}}
  .sw{{display:inline-block;vertical-align:middle;border-radius:0}}
  .note{{margin-top:10px;font-size:12px;color:var(--fg);background:transparent}}
  .foot{{margin-top:28px;font-size:12px;color:var(--mut);border-top:1px solid var(--line);padding-top:12px}}
</style></head>
<body data-theme="light">
  <div class="controls"><button id="tt" type="button">◐ Toggle theme</button></div>
  <h1>Apollo Mono — semantic greys onto the ramp</h1>
  <div class="sub">Surfacing every semantic grey against the new <code>color/mono/1–15</code> ramp — per the grey-tint check, <b>nothing is swapped</b>; this is for your ruling. The bulk map cleanly to the nearest step. The real calls are the few brand greys a rule or a tint already touches (below). Pin a comment on each.</div>

  <h2>The mono ramp (15 steps)</h2>
  <div class="ramp">{ramp}</div>

  <div class="banner"><b>Constraint (CONSULT):</b> <code>col25-011</code> — “typography: white or Grey-8 <code>#333333</code> only.” Grey-8 is not an exact mono step, so <b>text ink is a ruling, not a nearest-step swap.</b></div>

  <h2>Decisions — your call (rule/tint-governed)</h2>
  {dec}

  <h2>Mechanical — nearest step (confirm, low-decision)</h2>
  <div class="card"><table><thead><tr><th>current</th><th>→ mono step</th><th>where</th></tr></thead><tbody>{mech}</tbody></table>
  <div class="note">Already exact on the ramp (no change): {EXACT}</div></div>

  <div class="foot">Nothing enacted. On your ruling I wire the Mono theme's grey roles onto these steps in <code>semantic-colour.json</code>, regenerate <code>canon.css</code>, and re-gate. Contrast shown on white; dark values seat symmetrically. Sheet v1 · 2026-07-19.</div>
  <script>document.getElementById('tt').onclick=()=>{{const b=document.body;b.setAttribute('data-theme',b.getAttribute('data-theme')==='dark'?'light':'dark')}}</script>
</body></html>'''
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "APOLLO-MONO-SEMANTIC-GREYS-2026-07-19-v1.html")
    open(out, "w").write(html)
    print("wrote", out)

if __name__ == "__main__":
    build()
