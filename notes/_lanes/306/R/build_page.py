#!/usr/bin/env python3
"""306 R: build notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html.
Chrome (tokens, light/dark, back button, chips, decisions bar, Copy-as-text) is copied from
notes/_CHECK-306-parked-superseded-2026-09-28-v1.html via _chrome.css and the same script shape.
Figures come from wraptimes.py, dupgroup.py and prose_size.py in this folder."""
import os, json, html
os.chdir(os.path.expanduser("~/mnt/Projects--UX-design"))
CSS = open("notes/_lanes/306/R/_chrome.css").read()
EXTRA = r"""
.tally a:first-child b{color:inherit}
.q{margin:0 0 1.25rem;padding:0 0 0 16px;border-left:3px solid var(--accent);font-size:19px;line-height:1.45;font-weight:300}
.q small{display:block;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-top:4px}
.tw{width:100%;overflow-x:auto;margin:1rem 0 0}
table.t{width:100%;border-collapse:collapse;font-size:15px;font-variant-numeric:tabular-nums}
table.t th,table.t td{text-align:left;padding:.55rem .6rem .55rem 0;border-top:1px solid var(--rule);vertical-align:top}
table.t th{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);font-weight:500}
table.t td.n,table.t th.n{text-align:right;white-space:nowrap}
table.t tr.tot td{font-weight:500;border-top:2px solid var(--ink)}
table.t tr.sub td{color:var(--ink-2);font-size:14px}
.note{font-size:14px;color:var(--ink-2);max-width:44em;margin:.9rem 0 0}
.note .k{margin-right:4px}
ol.dup{list-style:none;margin:1rem 0 0;padding:0}
ol.dup li{display:grid;grid-template-columns:64px 1fr;gap:1rem;padding:.8rem 0;border-top:1px solid var(--rule)}
ol.dup .c{font-size:34px;font-weight:200;line-height:1}
ol.dup .c small{display:block;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-top:4px;line-height:1.3}
ol.dup .f{font-weight:500;margin:0 0 2px}
ol.dup .w{margin:0;font-size:14px;color:var(--ink-2)}
ol.dup .g{color:var(--ok)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:2rem;margin-top:1.5rem}
.card{border-top:2px solid var(--ink);padding-top:.8rem}
.card h3{font-size:18px;font-weight:500;margin:0 0 .4rem}
.card p,.card li{color:var(--ink-2);font-size:15px}
.card ul{margin:.3rem 0 0;padding-left:1.1rem}
code{font-family:"SFMono-Regular",Menlo,Consolas,monospace;font-size:.86em;background:var(--wash);padding:1px 4px;word-break:break-word}
section.grey code{background:var(--ground)}
figure{margin:1.5rem 0 0}
figure svg{width:100%;max-width:760px;height:auto;display:block}
figcaption{font-size:14px;color:var(--ink-2);margin-top:.6rem;max-width:44em}
svg text{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif}
.s-ink{fill:var(--ink)} .s-ink2{fill:var(--ink-2)} .s-ink3{fill:var(--ink-3)} .s-wait{fill:var(--rule)} .s-acc{fill:var(--accent)}
.s-txt{fill:var(--ink)} .s-dim{fill:var(--ink-2)} .s-acct{fill:var(--accent)}
.s-line{stroke:var(--ink-3);stroke-width:1} .s-mark{stroke:var(--accent);stroke-width:2;stroke-dasharray:4 3}
.s-idle{fill:none;stroke:var(--ink-3);stroke-width:1;stroke-dasharray:3 3}
ol.ph{list-style:none;margin:1rem 0 0;padding:0;counter-reset:p}
ol.ph li{counter-increment:p;display:grid;grid-template-columns:56px 1fr;gap:1rem;padding:1rem 0;border-top:1px solid var(--rule)}
ol.ph li::before{content:counter(p);font-size:32px;font-weight:200;line-height:1.1;color:var(--ink-3)}
ol.ph b{display:block;font-weight:500;margin-bottom:2px}
ol.ph p{margin:0 0 .3rem;color:var(--ink-2);font-size:15px}
ol.ph .k{margin-right:4px}
.rec{display:inline-block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0 0 .5rem}
.why{font-size:14px;color:var(--ink-2);margin:.5rem 0 0!important}
.ref{font-size:12px;color:var(--ink-3);margin:.3rem 0 0!important}
@media(max-width:820px){.cols{grid-template-columns:1fr;gap:1.25rem}ol.dup li{grid-template-columns:48px 1fr}ol.dup .c{font-size:28px}table.t{font-size:13px}table.t th,table.t td{padding:.45rem .35rem .45rem 0}.q{font-size:17px}ol.ph li{grid-template-columns:36px 1fr}ol.ph li::before{font-size:26px}}
"""
dup = json.load(open("notes/_lanes/306/R/dupgroup.json"))
NICE = {"GM banner":"banner","LS delta":"delta","W report":"wrap report","handoff 156":"handoff","old-handoff addenda":"old handoffs","memory note":"memory note",
        "state rows":"state rows","summary bullets":"summary","commit messages":"commit messages","carries":"carries","dossier":"dossier","narrative":"narrative","sign-off register":"sign-off list"}
FACTNAME = {
 "v1.0.14 cut":"The release cut (v1.0.14)",
 "rulings total 699":"The rulings total (699)",
 "newest ruling s305-D61":"The newest ruling's id",
 "headline 'he took the sitting'":"The session headline",
 "boot ceiling breach 131,130":"The boot-ceiling breach figure",
 "next beat: 102 parked questions":"Next session's first beat",
 "fill at wrap 450,794":"The window fill at the wrap",
 "his words 'set in ink'":"Your words: “set in ink”",
 "HEAD at open cd16f7ec":"The commit the wrap started from",
 "40 enacted / 20 ruled":"Rulings built vs. ruled (40 / 20)",
 "date split line":"The date-split line",
 "12 carries struck":"Carried items struck (12)",
 "CI verdict 154 of 154 / 69 pass":"The CI verdict",
 "wrap sha 81bce363":"The wrap commit's id",
 "his words 'okay go for it'":"Your words: “okay go for it”",
}
rows=[r for r in dup if r[0] in FACTNAME]
dup_html=[]
for fact,h,g,occ,hl,gl in rows:
    where=", ".join(NICE.get(x,x) for x in hl)
    gen=(' <span class="g">+ generated: '+", ".join("chain" if "CHAIN" in x else "titles" for x in gl)+'</span>') if gl else ""
    dup_html.append(f'<li><div class="c">{h}<small>hand-written</small></div><div><p class="f">{html.escape(FACTNAME[fact])}</p><p class="w">{html.escape(where)}.{gen} <span class="k">{occ} mentions</span></p></div></li>')
BODY = open("notes/_lanes/306/R/page_body.html").read().replace("%%DUP%%","\n".join(dup_html))
SCRIPT = open("notes/_lanes/306/R/page_script.js").read()
out = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
       '<title>Wrap redesign</title>\n<style>'+CSS+EXTRA+'</style></head>\n'+BODY+'\n<script>\n'+SCRIPT+'\n</script>\n</body></html>\n')
p="notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html"
open(p,"w").write(out); print(p, len(out), "bytes ·", len(rows), "duplicate rows")
