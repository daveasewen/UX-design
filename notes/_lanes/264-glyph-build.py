#!/usr/bin/env python3
"""#264 — sidebar glyph options page. Generated; do not hand-edit. Every glyph is the library file, inlined."""
import re, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
ICONS = R/'knowledge/assets/icons'
def sym(slug, sid):
    s = (ICONS/f'{slug}.svg').read_text()
    inner = re.sub(r'^.*?<svg[^>]*>', '', s, flags=re.S).replace('</svg>', '').strip()
    return f'<symbol id="{sid}" viewBox="0 0 18 18">{inner}</symbol>'
pairs = {
 'data-chart':'products-and-services/data-chart','data-chart-active':'products-and-services/data-chart-active',
 'insight':'products-and-services/insight','insight-active':'products-and-services/insight-active',
 'dashboard':'media/dashboard','dashboard-active':'media/dashboard-active',
 'balance-transfer':'products-and-services/balance-transfer','transfer':'products-and-services/transfer','transfer-active':'products-and-services/transfer-active',
 'account':'products-and-services/account','account-active':'products-and-services/account-active',
}
symbols = '\n'.join(sym(p, k) for k, p in pairs.items())

def row(label, line, fill, current=False, cls=''):
    cur = ' aria-current="page"' if current else ''
    return (f'<a class="nv-item {cls}" href="#"{cur}><span class="nv-ic" aria-hidden="true">'
            f'<svg class="ic-line" viewBox="0 0 18 18"><use href="#{line}"/></svg>'
            f'<svg class="ic-fill" viewBox="0 0 18 18"><use href="#{fill}"/></svg></span>'
            f'<span class="nv-label">{label}</span></a>')

def panel(theme, label, line, fill):
    return (f'<div class="sn" data-theme="{theme}">'
            f'<span class="sn-group-label">Insight</span>{row(label,line,fill)}{row(label,line,fill,True)}</div>')

def option(idx, title, line, fill, label, note, rec=False):
    tag = '<span class="tag">Recommended</span>' if rec else ''
    return f'''
<section class="option">
  <div class="opt-head"><span class="idx">{idx}</span><div><h3>{title}{tag}</h3><p class="meta">line <code>{line}</code> · current <code>{fill}</code></p></div></div>
  <div class="panels">{panel('light',label,line,fill)}{panel('dark',label,line,fill)}</div>
  <p class="note">{note}</p>
</section>'''

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>#264 · Sidebar glyph options</title>
<style>
:root{{--accent:#DB0011;--g1:#F3F3F3;--g2:#EDEDED;--g3:#D7D8D6;--g6:#767676;--g8:#333333;--s2:1rem;--s3:1.5rem;--s4:2rem;--s5:3rem;--s6:4rem}}
*{{box-sizing:border-box}} body{{margin:0;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;color:#000;background:#fff;font-size:16px;line-height:1.7}}
.wrap{{max-width:1100px;margin:0 auto;padding:0 var(--s4)}}
header{{padding:var(--s5) 0 var(--s4);border-bottom:1px solid var(--g2)}}
.label{{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);display:flex;align-items:center;gap:8px;margin:0 0 var(--s2)}}
.label::before{{content:'';width:20px;height:1px;background:var(--accent)}}
h1{{font-size:34px;font-weight:400;line-height:1.15;margin:0 0 var(--s2);letter-spacing:-.01em}}
h2{{font-size:19px;font-weight:500;margin:0 0 var(--s2)}}
h3{{font-size:19px;font-weight:500;margin:0;display:flex;align-items:center;gap:12px}}
p{{margin:0 0 var(--s2)}} .lede{{max-width:64ch}}
.finding{{display:grid;grid-template-columns:1fr 2fr;gap:var(--s6);padding:var(--s5) 0;border-bottom:1px solid var(--g2)}}
.finding .big{{font-size:57px;font-weight:200;line-height:1;color:var(--g8)}}
.finding .cap{{font-size:12px;color:var(--g6);letter-spacing:.08em;text-transform:uppercase}}
table{{border-collapse:collapse;width:100%;font-size:14px;margin:var(--s2) 0}} th,td{{text-align:left;padding:8px 12px 8px 0;border-bottom:1px solid var(--g2);vertical-align:top}} th{{font-weight:500;color:var(--g6);font-size:12px;letter-spacing:.08em;text-transform:uppercase}}
.bad{{color:var(--accent)}} code{{font-family:Menlo,monospace;font-size:13px}}
.option{{padding:var(--s4) 0;border-bottom:1px solid var(--g2)}}
.opt-head{{display:flex;gap:var(--s3);align-items:flex-start;margin-bottom:var(--s3)}}
.idx{{font-size:43px;font-weight:200;line-height:1;color:var(--g3);min-width:56px}}
.meta{{font-size:14px;color:var(--g6);margin:4px 0 0}}
.tag{{font-size:11px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);border-bottom:1px solid var(--accent);padding-bottom:1px}}
.panels{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--g2);margin:0 0 var(--s2)}}
.note{{max-width:70ch;font-size:15px;margin:0}}
/* sidebar family — verbatim token set + shared item block, Sidebar-nav.reference.html */
.sn{{--nav-row:44px;padding:8px 0 16px;width:100%}}
.sn[data-theme=light]{{--nav-surface:#FFFFFF;--nav-text:#1A1A1A;--nav-muted:#1A1A1A;--nav-icon:#1A1A1A;--nav-indicator:#DB0011;background:var(--nav-surface)}}
.sn[data-theme=dark]{{--nav-surface:#1F1F1F;--nav-text:#FFFFFF;--nav-muted:#FFFFFF;--nav-icon:#FFFFFF;--nav-indicator:#DB0011;background:var(--nav-surface)}}
.sn-group-label{{display:block;padding:8px 16px;color:var(--nav-muted);opacity:.72;font-size:12px;letter-spacing:.06em;text-transform:uppercase}}
.nv-item{{display:flex;align-items:center;gap:12px;min-height:var(--nav-row);padding:0 16px;color:var(--nav-text);text-decoration:none;font-size:16px}}
.nv-ic{{flex:none;display:inline-flex;width:18px;height:18px;color:var(--nav-icon)}} .nv-ic svg{{width:18px;height:18px;fill:currentColor}}
.nv-ic .ic-fill{{display:none}} .nv-item[aria-current=page] .ic-line{{display:none}} .nv-item[aria-current=page] .ic-fill{{display:block}}
.nv-item[aria-current=page]{{box-shadow:inset 3px 0 0 var(--nav-indicator)}} .nv-item[aria-current=page] .nv-label{{font-weight:500}}
.pair{{display:inline-flex;gap:6px;align-items:center;vertical-align:middle}} .pair svg{{width:18px;height:18px;fill:#1A1A1A}}
footer{{padding:var(--s4) 0 var(--s6);font-size:14px;color:var(--g6)}}
</style></head><body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">{symbols}</svg>
<div class="wrap">
<header>
  <p class="label">#264 · Sidebar-nav · glyph review</p>
  <h1>The sidebar's glyphs are all library assets. Two rows pair a line glyph with the wrong filled twin.</h1>
  <p class="lede">The carry called the <code>chart</code> glyph "hand-baked". It is not — every one of the twelve symbols in <code>Sidebar-nav.reference.html</code> is byte-identical to a file in <code>icons.manifest.json</code>. What is wrong is the <em>pairing</em>: <code>s262-D3</code> says the current row shows the line glyph's <code>-active</code> twin, and on two rows the twin is a different icon.</p>
</header>

<section class="finding">
  <div><div class="big">2<span style="font-size:19px;color:var(--g6)"> of 6</span></div><div class="cap">rows mis-twinned</div></div>
  <div>
  <table><tr><th>Row</th><th>Line glyph (rest)</th><th>Filled glyph (current)</th><th>Library twin that exists</th></tr>
  <tr><td>Spending</td><td><span class="pair"><svg viewBox="0 0 18 18"><use href="#data-chart"/></svg> <code>data-chart</code></span></td><td class="bad"><span class="pair"><svg viewBox="0 0 18 18"><use href="#insight-active"/></svg> <code>insight-active</code></span></td><td><span class="pair"><svg viewBox="0 0 18 18"><use href="#data-chart-active"/></svg> <code>data-chart-active</code></span></td></tr>
  <tr><td>Transfers</td><td><span class="pair"><svg viewBox="0 0 18 18"><use href="#balance-transfer"/></svg> <code>balance-transfer</code></span></td><td class="bad"><span class="pair"><svg viewBox="0 0 18 18"><use href="#transfer-active"/></svg> <code>transfer-active</code></span></td><td><span class="pair"><svg viewBox="0 0 18 18"><use href="#transfer"/></svg> <code>transfer</code> (line) — <code>balance-transfer</code> has no twin</span></td></tr>
  <tr><td>Home · Accounts · Cards · Settings</td><td colspan="3">correct twins, no change</td></tr>
  </table>
  <p>So the question is not "promote a pair into the library". Both pairs already exist. The question is which pair each row wears — and that is a naming choice, yours.</p>
  </div>
</section>

<h2 style="padding-top:var(--s5)">Spending — three pairs the library offers</h2>
{option('A','Data chart', 'data-chart','data-chart-active','Spending','Keeps the glyph the row has today at rest; only the current state changes, to the pie chart’s own filled twin. The row reads the same in both states. Smallest change: one <code>href</code>.', rec=True)}
{option('B','Insight', 'insight','insight-active','Spending','Keeps the filled bulb the row shows today when current, and gives it the matching line bulb at rest. It agrees with the group label "Insight", but the row is labelled "Spending" — a bulb is a weak sign for spending, and the bulb is also what the Tab-bar uses for its "Insights" item, so the two would collide.')}
{option('C','Dashboard', 'dashboard','dashboard-active','Spending','A gauge. Reads as "overview" rather than "spending"; offered because it is the third analytics-shaped pair in the library, not because it fits better than A.')}

<h2 style="padding-top:var(--s5)">Transfers — the same defect, one honest pair</h2>
{option('D','Transfer', 'transfer','transfer-active','Transfers','The library’s own line/fill pair. Today the row rests on <code>balance-transfer</code> (arrows over a coin, no twin exists) and goes current on <code>transfer-active</code> (arrows in a disc) — the shape changes on selection. This pair holds the shape.', rec=True)}
{option('E','As built', 'balance-transfer','transfer-active','Transfers','What ships today, shown so the shape change is visible side by side.')}

<section style="padding:var(--s4) 0">
  <h2>What no gate sees</h2>
  <p class="note">Nothing checks that a snippet's <code>-a</code> symbol is the manifest twin of its line symbol. <code>_validate_icons.py</code> resolves each glyph to a library file (its 5 UNKNOWN Legend reds are that arm working) but never asks whether the two glyphs on one row are the same asset in two states. A twin-check is a small arm — one lookup per row, red on a cross-family pair — and it would have caught both of these at #262. Ruling-shaped, separate from the pair choice above.</p>
</section>
<footer>Generated by <code>notes/_lanes/264-glyph-build.py</code> · every glyph inlined from <code>knowledge/assets/icons/</code> · sidebar tokens and item block copied verbatim from <code>Sidebar-nav.reference.html</code> · 2026-09-09 #264</footer>
</div></body></html>'''
out = R/'notes/_REVIEW-264-sidebar-glyph.html'
out.write_text(html); print(out, len(html))
