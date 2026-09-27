"""Seat 304-W5b build. Copies the house CSS (both style blocks) and Dave's decisions overlay from the
Apollo-MCP v2 proposal page, changes only the overlay's page id/title/path, the section skip (only the
Friday context box keeps a section box, labelled Context) and nothing else; adds this seat's small CSS block;
writes notes/_SITTING-304-tuesday-2026-09-29-v1.html. Run from the repo root."""
import os
ROOT = os.getcwd()
HERE = os.path.join(ROOT, 'notes/_lanes/304/W5b')
HOUSE = os.path.join(ROOT, 'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html')
OUT = 'notes/_SITTING-304-tuesday-2026-09-29-v1.html'

def rep(s, a, b):
    assert s.count(a) == 1, a[:70]
    return s.replace(a, b)

house = open(HOUSE, encoding='utf-8').read()
i = house.index('<style>'); j = house.index('</style>', i) + 8
k = house.index('<style>', j); l = house.index('</style>', k) + 8
CSS = house[i:j] + '\n' + house[k:l]
m = house.index("<!-- ===== DAVE'S DECISIONS"); n = house.index('</script>', m) + 9
ov = house[m:n]
ov = rep(ov, "page:'proposal-apollo-mcp-v2', title:'Apollo-MCP, proposal v2', path:'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'",
         "page:'sitting-304-tuesday-v1', title:'The sitting, Tuesday 29 September 2026', path:'%s'" % OUT)
ov = rep(ov, "copied from the story proposal v2 (#289) at #304", "copied from the Apollo-MCP proposal v2 (#304 lane M) by seat W5b")
ov = rep(ov, "skip:function(el){ return el.id==='tech' || el.id==='sources'; }", "skip:function(el){ return el.id!=='friday'; }")
ov = rep(ov, "kind:'Section', fallbackNum:'.label'", "kind:'Context'")

ADD = """<style>
/* W5b sitting-page additions */
ol.decide{list-style:none;padding:0;margin:0}
.beats li>div{min-width:0}
.rec{font-size:19px;font-weight:300;line-height:1.5;margin:var(--s1) 0 var(--s2);max-width:40em;border-left:2px solid var(--black);padding-left:var(--s2)}
.rec b,.beats .rec b{display:inline;font-weight:500;font-size:inherit;line-height:inherit;margin:0}
.beats li>div>b{font-size:22px;line-height:1.3;max-width:30em}
.why{font-size:15px;color:var(--grey-8);max-width:44em;margin:0 0 var(--s2)}
.more{font-size:13px;color:var(--grey-7);max-width:44em;margin:var(--s1) 0 0}
.more a{color:var(--grey-8)}
.more code{font-family:ui-monospace,Menlo,monospace;font-size:12px;background:var(--grey-1);padding:.1em .35em}
section.grey .more code{background:var(--white)}
.spec{margin:var(--s2) 0 0}
.spec img{display:block;width:100%;height:auto;border:1px solid var(--grey-2);background:var(--white)}
.spec figcaption{font-size:12px;color:var(--grey-6);line-height:1.5;margin-top:6px}
.specs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--s3);margin-top:var(--s2)}
.specs.three{grid-template-columns:repeat(3,minmax(0,1fr))}
.specs.one{grid-template-columns:1fr;gap:var(--s2)}
.specs .spec{margin:0}
.spec.badge img{max-width:380px}
.crop{height:360px;overflow:hidden;border:1px solid var(--grey-2);background:var(--white)}
.crop img{border:0}
.clash{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:var(--grey-3);border:1px solid var(--grey-3);margin:var(--s2) 0}
.clash>div{background:var(--white);padding:var(--s2) var(--s3)}
.clash .hd{font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:500;line-height:1.5;margin:0 0 var(--s1)}
.clash .hd.now{color:var(--grey-6)}.clash .hd.his{color:var(--accent)}
.clash p{font-size:15px;color:var(--grey-8);margin:0}
.stats.four{grid-template-columns:repeat(4,1fr)}
.one{margin-top:var(--s5);padding:var(--s4);background:var(--black);color:var(--white)}
.one .label{color:var(--white)}.one .label::before{background:var(--white)}
.one .line{color:var(--white)}.one .line b{font-weight:500}
.slot{margin-top:var(--s4);border:1px dashed var(--grey-6);padding:var(--s3);max-width:60em}
.slot p{margin:0;font-size:15px;color:var(--grey-8)}
.cols.two-up .hd{margin-bottom:var(--s1)}
.moved li b{display:inline}
.tech code{overflow-wrap:anywhere}
.dd-host:empty{display:none}
@media(max-width:820px){
  .specs,.specs.three,.clash{grid-template-columns:1fr}
  .rec{font-size:17px}
  .stats.four{grid-template-columns:1fr 1fr}
  .crop{height:240px}
  .one{padding:var(--s3)}
}
</style>"""

src = open(os.path.join(HERE, 'page.src.html'), encoding='utf-8').read()
src = rep(src, '<!--CSS-->', CSS)
src = rep(src, '<!--ADD-->', ADD)
src = rep(src, '<!--OVERLAY-->', ov)
assert '<!--' not in src.replace('<!-- ====', '').replace("<!-- ===== DAVE'S", ''), 'placeholder left'
open(os.path.join(ROOT, OUT), 'w', encoding='utf-8').write(src)
print('wrote', OUT, len(src), 'bytes')
