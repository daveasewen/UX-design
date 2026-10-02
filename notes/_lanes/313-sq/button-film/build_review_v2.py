#!/usr/bin/env python3
"""Build REVIEW-v1.html: cut A and cut B side by side, every key frame with its words, films linked."""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cuts = {c: json.load(open(os.path.join(HERE, f'stills-{c}', 'keys.json'))) for c in ('a-v2', 'b')}

LBL = {'a-v2': 'Cut A · version 2 · your script', 'b': 'Cut B · version 1 · unchanged'}
def col(c, title, sub):
    k = cuts[c]
    rows = []
    for i, f in enumerate(k['keys']):
        w = html.escape(f['words']) or '&nbsp;'
        rows.append(f'<figure><span class="n">{i + 1:02d}</span><img src="{f["file"]}" alt="" loading="lazy">'
                    f'<figcaption>{w}<em>{f["t"]:.1f} s</em></figcaption></figure>')
    return (f'<section><header><p class="k">{LBL[c]}</p><h2>{title}</h2><p class="s">{sub}</p>'
            f'<p class="m">{k["duration"]:.0f} s · {len(k["keys"])} frames · '
            f'<a href="button-film-{c}.html">play the film ↗</a></p></header>{"".join(rows)}</section>')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Button film · two cuts</title>
<style>
@font-face{{font-family:U;font-weight:300;src:local("HSBC_MtUnivers_Latin Light"),local("Univers Next for HSBC Light")}}
:root{{--ink:#0C0C0C;--g:#767676;--rule:#E2E2E2;--red:#DA1A00}}
*{{box-sizing:border-box}}body{{margin:0;background:#fff;color:var(--ink);font:300 16px/1.45 "Univers Next for HSBC",U,Helvetica,Arial,sans-serif}}
.top{{padding:48px 40px 32px;border-bottom:1px solid var(--ink)}}
.top p{{margin:0}}.k{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--g)}}
h1{{font-weight:400;font-size:44px;line-height:1.05;margin:10px 0 14px}}h1 i{{font-style:normal;color:var(--red)}}
.lede{{max-width:62ch;color:#333}}
main{{display:grid;grid-template-columns:1fr 1fr;gap:0}}
section{{padding:28px 40px 60px}}section+section{{border-left:1px solid var(--rule)}}
header{{position:sticky;top:0;background:#fff;padding:12px 0 16px;border-bottom:1px solid var(--rule);margin-bottom:20px;z-index:1}}
h2{{font-weight:400;font-size:24px;margin:4px 0}}.s{{color:#333;margin:0 0 6px}}.m{{font-size:13px;color:var(--g);margin:0}}
a{{color:var(--ink)}}
figure{{margin:0 0 22px;position:relative}}img{{width:100%;display:block;border:1px solid var(--rule)}}
.n{{position:absolute;left:8px;top:6px;font-size:12px;color:var(--g)}}
figcaption{{font-size:14px;margin-top:6px;display:flex;justify-content:space-between;gap:12px}}
figcaption em{{font-style:normal;color:var(--g);white-space:nowrap}}
@media (max-width:900px){{main{{grid-template-columns:1fr}}section+section{{border-left:0;border-top:1px solid var(--ink)}}section{{padding:24px 16px}}.top{{padding:32px 16px}}}}
</style></head><body>
<div class="top"><p class="k">Apollo · film B · 313-sq · review v2</p>
<h1>It started with a single button<i>.</i></h1>
<p class="lede">Version 2 of cut A from your script, beside cut B as it was. Both open on a real button that is pressed and becomes the red dot, and every idea opens out of the dot and folds back into it. Words on screen in Univers. Play either film with sound; the arrow keys step through the beats.</p></div>
<main>{col('a-v2', 'Your edit of the script', 'The red dot becomes part of every subject. The colour beat is the full Supercharge palette. Everything resolves back into the button. Scrub bar and comments in the film.')}
{col('b', 'The single words', 'Colour. Words. Shape. State. Reason. Judgement. Then the one place makes room for what matters: the user, their needs, your empathy, your craft.')}</main>
</body></html>'''
open(os.path.join(HERE, 'REVIEW-v2.html'), 'w', encoding='utf-8').write(page)
print('REVIEW-v2.html', len(page), 'bytes')
