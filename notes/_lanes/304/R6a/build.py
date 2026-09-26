"""Seat 304-R6a build. For each of the three decision pages: copies the house CSS (both style blocks)
and Dave's decisions overlay from the Apollo-MCP v2 proposal page (built by notes/_lanes/304/M/build_v2.py),
changes only the overlay's page id/title/path and its targets (one box per question, keyed on the h2;
no per-section boxes), adds this seat's small CSS block, and writes notes/_DECIDE-304-*.html.
Run from the repo root."""
import os
ROOT = os.getcwd()
HERE = os.path.join(ROOT, 'notes/_lanes/304/R6a')
HOUSE = os.path.join(ROOT, 'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html')

def rep(s, a, b):
    assert s.count(a) == 1, a[:70]
    return s.replace(a, b)

house = open(HOUSE, encoding='utf-8').read()
i = house.index('<style>'); j = house.index('</style>', i) + 8
k = house.index('<style>', j); l = house.index('</style>', k) + 8
CSS = house[i:j] + '\n' + house[k:l]
m = house.index("<!-- ===== DAVE'S DECISIONS"); n = house.index('</script>', m) + 9
OVERLAY0 = house[m:n]

ADD = """<style>
/* R6a decision-page additions */
section.q .wrap>.label{margin-bottom:var(--s2)}
ol.decide{list-style:none;padding:0;margin:0}
ol.decide>li>div>h2{max-width:24em}
.rec{font-size:19px;font-weight:300;line-height:1.5;margin:0 0 var(--s3);max-width:40em;border-left:2px solid var(--black);padding-left:var(--s2)}
.rec b{font-weight:500}
.lead{font-size:16px;color:var(--grey-8);max-width:44em}
.opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:var(--grey-3);border:1px solid var(--grey-3);margin-top:var(--s3)}
.opts.three{grid-template-columns:repeat(3,minmax(0,1fr))}
.opt{background:var(--white);padding:var(--s3);min-width:0}
.opt .k{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-6);font-weight:500;line-height:1.5;margin-bottom:var(--s1)}
.opt.pick{box-shadow:inset 0 3px 0 var(--black)}
.opt.pick .k{color:var(--accent)}
.opt h3{font-size:19px;margin:0 0 var(--s1)}
.opt p{font-size:15px;color:var(--grey-8);margin:0 0 var(--s1);line-height:1.55}
.opt p.for{margin-top:var(--s2);padding-top:var(--s1);border-top:1px solid var(--grey-2);color:var(--black)}
.spec{margin:var(--s2) 0 0}
.spec img{display:block;width:100%;height:auto;border:1px solid var(--grey-2);background:var(--white)}
.spec figcaption{font-size:12px;color:var(--grey-6);line-height:1.5;margin-top:6px}
.specs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--s3);margin-top:var(--s3)}
.specs.three{grid-template-columns:repeat(3,minmax(0,1fr))}
.specs .spec{margin:0}
pre.code{font-family:ui-monospace,Menlo,monospace;font-size:12px;line-height:1.55;background:var(--grey-1);color:var(--grey-8);padding:var(--s2);margin:var(--s1) 0 0;white-space:pre-wrap;overflow-wrap:anywhere}
section.grey pre.code{background:var(--white)}
.est{font-size:12px;color:var(--grey-6);letter-spacing:.04em}
.stats.four{grid-template-columns:repeat(4,1fr)}
.order{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--grey-3);border:1px solid var(--grey-3);margin-top:var(--s3)}
.order>div{background:var(--white);padding:var(--s3)}
.order .k{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-6);font-weight:500;line-height:1.5;margin-bottom:var(--s1)}
.order .n{font-size:40px;font-weight:200;line-height:1.1;color:var(--grey-6);display:block}
.order h3{font-size:19px;margin:var(--s1) 0}
.order p{font-size:15px;color:var(--grey-8);margin:0 0 var(--s1)}
.order .parked{background:var(--grey-1)}
.clash{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--s3);margin-top:var(--s3)}
.clash .spec{margin:0}
.clash .hd{font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:500;line-height:1.5;margin-bottom:var(--s1)}
.clash .hd.now{color:var(--grey-6)}.clash .hd.his{color:var(--accent)}
.clash p{font-size:15px;color:var(--grey-8);margin:var(--s1) 0 0}
.mini{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--grey-3);border:1px solid var(--grey-3);margin-top:var(--s3)}
.mini>div{background:var(--white);padding:var(--s2) var(--s3)}
.mini .hd{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-6);font-weight:500;line-height:1.5;margin-bottom:var(--s1)}
.mini ul{list-style:none;margin:0;padding:0}
.mini li{font-size:14px;line-height:1.5;padding:4px 0;border-top:1px solid var(--grey-2)}
.mini li:first-child{border-top:0}
td.rc{color:var(--black)}
footer .dd-box{flex-basis:100%}
@media(max-width:820px){
  .opts,.opts.three,.specs,.specs.three,.order,.clash,.mini{grid-template-columns:1fr}
  .opt,.order>div{padding:var(--s2)}
  .rec{font-size:17px}
  .stats.four{grid-template-columns:1fr 1fr}
}
</style>"""

PAGES = [
  ('schema', 'decide-304-schema-v1', 'Decision page: the schema and the shape of a part, v1', 'notes/_DECIDE-304-schema-2026-09-26-v1.html'),
  ('delivery', 'decide-304-delivery-shape-v1', 'Decision page: the delivery shape, v1', 'notes/_DECIDE-304-delivery-shape-2026-09-26-v1.html'),
  ('when', 'decide-304-when-rules-v1', 'Decision page: the when-rules and your three observations, v1', 'notes/_DECIDE-304-when-rules-2026-09-26-v1.html'),
]
for key, pid, title, path in PAGES:
    ov = OVERLAY0
    ov = rep(ov, "page:'proposal-apollo-mcp-v2', title:'Apollo-MCP, proposal v2', path:'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'",
             "page:'%s', title:'%s', path:'%s'" % (pid, title, path))
    ov = rep(ov, "copied from the story proposal v2 (#289) at #304", "copied from the Apollo-MCP proposal v2 (#304 lane M) by seat R6a")
    ov = rep(ov, "skip:function(el){ return el.id==='tech' || el.id==='sources'; }", "skip:function(el){ return true; }")
    ov = rep(ov, "{ sel:'.decide > li', kind:'Decision', title:'b', host:'div', prefix:'decision', count:true }",
             "{ sel:'.decide > li', kind:'Decision', title:'h2', host:'div', prefix:'decision', count:true }")
    src = open(os.path.join(HERE, 'page-%s.src.html' % key), encoding='utf-8').read()
    src = rep(src, '<!--CSS-->', CSS + '\n' + ADD)
    src = rep(src, '<!--OVERLAY-->', ov)
    out = os.path.join(ROOT, path)
    open(out, 'w', encoding='utf-8').write(src)
    print('wrote', path, len(src), 'bytes')
