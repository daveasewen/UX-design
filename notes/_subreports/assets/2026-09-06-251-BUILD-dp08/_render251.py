"""#251 BUILD lane — render the CANON template (never the outputs copy) and drive the anchor.

Adapted from outputs/w2-debt/dp08/_probe251.py (the #251 premise probe): same measurement
JS, three differences, all because canon is not the probe's page — canon has no tab panels
(`#p1` does not exist in it), its rail card is titled "Balances", not "Balances by entity",
and its strip class is `.tpl-strip`, not `.dp08-strip`. Writes only into this assets dir.
"""
import json, sys
from playwright.sync_api import sync_playwright

PAGE = '/sessions/bold-focused-hopper/mnt/UX-design/knowledge/snippets/Template-dashboard-bento.reference.html'
OUT = '/sessions/bold-focused-hopper/mnt/UX-design/notes/_subreports/assets/2026-09-06-251-BUILD-dp08'

PROBE = r"""()=>{
const r=e=>{if(!e)return null;const b=e.getBoundingClientRect();return {x:+(b.left).toFixed(1),y:+(b.top+window.scrollY).toFixed(1),w:+b.width.toFixed(1),h:+b.height.toFixed(1)}};
const names=['--success','--warning','--error','--info','--up','--down','--spark-up','--spark-down','--success-tint','--warning-tint','--error-tint','--info-tint'];
const probe=document.createElement('span'); document.body.appendChild(probe);
const rag={}; for(const n of names){probe.style.color=`var(${n})`; const v=getComputedStyle(probe).color; if(v&&v!=='rgba(0, 0, 0, 0)') rag[v]=n;}
probe.remove();
const isRag=v=>v&&rag[v]!==undefined;
const lead=document.querySelector('.tpl-group-lead');
const grid=lead?lead.querySelector(':scope>.c-bento__grid'):null;
const tiles=lead?[...lead.querySelectorAll(':scope>.c-bento__grid>.kpi-tile')]:[];
const gcs=grid?getComputedStyle(grid):null;
const boxes=tiles.map(t=>({label:t.getAttribute('aria-label'),...r(t)}));
const rows={}; boxes.forEach(b=>{const k=Math.round(b.y); (rows[k]=rows[k]||[]).push(b);});
const rowKeys=Object.keys(rows).map(Number).sort((a,b)=>a-b);
const ws=boxes.map(b=>b.w);
const maxWDiff=ws.length?+(Math.max(...ws)-Math.min(...ws)).toFixed(2):null;
let lastRowVoid=null, gap=null;
if(grid&&rowKeys.length){
  const gb=grid.getBoundingClientRect();
  const pad=parseFloat(gcs.paddingLeft)+parseFloat(gcs.paddingRight);
  gap=parseFloat(gcs.columnGap)||0;
  const last=rows[rowKeys[rowKeys.length-1]].slice().sort((a,b)=>a.x-b.x);
  const used=last.reduce((s,b)=>s+b.w,0)+gap*(last.length-1);
  lastRowVoid=+((gb.width-pad)-used).toFixed(1);
}
const ev=document.querySelector('.tpl-group-evidence'); const svg=ev?ev.querySelector('svg'):null;
const ctx=document.querySelector('.tpl-group-context');
const cards=ctx?[...ctx.querySelectorAll(':scope>.c-bento__grid>.c-bento__tile')]:[];
const cardInfo=cards.map(c=>{const h=c.querySelector('h3'); return {title:h?h.textContent.trim():'(none)',...r(c)};});
const ctxGrid=ctx?ctx.querySelector(':scope>.c-bento__grid'):null;
const na=document.getElementById('dp08-na');
const bal=cards.find(c=>c!==na);
const strip=document.querySelector('.tpl-strip')||null;
const chip=document.querySelector('[data-dp08-anchor]');
const sig=[]; for(const e of document.querySelectorAll('.tpl-page *, .tpl-header *, .sh-masthead *')){
  const b=e.getBoundingClientRect(); if(b.width===0||b.height===0) continue; const top=b.top+window.scrollY; if(top>=900) continue;
  const s=getComputedStyle(e); const hits=[];
  if(isRag(s.backgroundColor)) hits.push('bg:'+rag[s.backgroundColor]);
  if(isRag(s.color) && e.childNodes.length && [...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())) hits.push('color:'+rag[s.color]);
  if(e instanceof SVGElement){ if(isRag(s.fill)&&s.fill!=='none') hits.push('fill:'+rag[s.fill]); if(isRag(s.stroke)&&s.stroke!=='none') hits.push('stroke:'+rag[s.stroke]); }
  if(hits.length){ const car=e.closest('.status, .kpi-tile')||e; sig.push({el:e.tagName.toLowerCase()+'.'+[...e.classList].join('.'),y:+top.toFixed(0),hits,carrier:(car.getAttribute('aria-label')||car.innerText||'').replace(/\s+/g,' ').slice(0,44)}); }
}
const carriers=[...new Set(sig.map(s=>s.carrier))];
const txt=document.body.innerText;
return {
 leadGridCols: gcs?gcs.gridTemplateColumns:null,
 colsNow: grid?getComputedStyle(grid).getPropertyValue('--bento-cols-now').trim():null,
 tiles: boxes, tileRows: rowKeys.length, rowSizes: rowKeys.map(k=>rows[k].length),
 maxTileWidthDiff: maxWDiff, columnGap: gap, lastRowVoid: lastRowVoid,
 first_chart_y: svg?r(svg).y:null,
 ctxGridCols: ctxGrid?getComputedStyle(ctxGrid).gridTemplateColumns:null,
 railCards: cardInfo,
 needs_attention: r(na), balances: r(bal), strip: r(strip),
 chip_href: chip?chip.getAttribute('href'):null,
 na_id: na?na.id:null, na_target_attr: na?na.hasAttribute('data-dp08-target'):null,
 repeats: {'Awaiting approval': (txt.match(/Awaiting approval/g)||[]).length,
           '14 payments': (txt.match(/14 payments/g)||[]).length,
           '5 need you': (txt.match(/5 need you/g)||[]).length,
           'N of M': (txt.match(/\d+ of \d+ need you/g)||[]).length,
           'Undrawn facilities': (txt.match(/Undrawn facilities/g)||[]).length},
 signals_above_fold:{elements:sig.length,carriers:carriers.length,carrier_list:carriers},
 page_h: document.documentElement.scrollHeight};
}"""

DRIVE = r"""()=>{
const chip=document.querySelector('[data-dp08-anchor]');
const before={y:window.scrollY,active:document.activeElement?(document.activeElement.id||document.activeElement.tagName):null,hash:location.hash};
chip.click();
return {before:before};
}"""

AFTER = r"""()=>{
const na=document.getElementById('dp08-na');
const b=na.getBoundingClientRect();
return {y:Math.round(window.scrollY),
        active:document.activeElement?(document.activeElement.id||document.activeElement.tagName):null,
        hash:location.hash,
        tabindex:na.getAttribute('tabindex'),
        arrivedClass:na.classList.contains('is-dp08-arrived'),
        naVisibleInViewport:(b.top<window.innerHeight&&b.bottom>0),
        naTopInViewport:Math.round(b.top),
        mainStillVisible:!!document.querySelector('#tplMain') && getComputedStyle(document.querySelector('#tplMain')).display!=='none',
        panelsOnPage:document.querySelectorAll('[role="tabpanel"]').length};
}"""


def main():
    jobs = [dict(key=f"{w}-{t}", w=w, theme=t) for w in (1440, 1100, 820) for t in ("light", "dark")]
    res, errs = {}, {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--no-sandbox'])
        for job in jobs:
            key = job['key']
            pg = b.new_page(viewport={'width': job['w'], 'height': 900})
            seen = []
            pg.on("pageerror", lambda e: seen.append(str(e)))
            pg.on("console", lambda m: seen.append("console:" + m.text) if m.type == "error" else None)
            pg.goto(f"file://{PAGE}")
            if job['theme'] == 'dark':
                pg.evaluate("()=>{document.documentElement.setAttribute('data-theme','dark');document.body.setAttribute('data-theme','dark');}")
            pg.wait_for_timeout(500)
            d = pg.evaluate(PROBE)
            res[key], errs[key] = d, list(seen)
            print('==', key, '| --bento-cols-now', d['colsNow'], '| cols', d['leadGridCols'])
            for t in d['tiles']:
                print('   tile', t['label'], {k: t[k] for k in ('x', 'y', 'w', 'h')})
            print('  rows', d['tileRows'], d['rowSizes'], '| maxWdiff', d['maxTileWidthDiff'],
                  '| gap', d['columnGap'], '| lastRowVoid', d['lastRowVoid'])
            print('  ctxCols', d['ctxGridCols'])
            for c in d['railCards']:
                print('   card', repr(c['title']), {k: c[k] for k in ('x', 'y', 'w', 'h')})
            print('  NA', d['needs_attention'], '| strip', d['strip'], '| chip_href', d['chip_href'],
                  '| na_id', d['na_id'], d['na_target_attr'])
            print('  first_chart_y', d['first_chart_y'], '| page_h', d['page_h'],
                  '| signals', d['signals_above_fold']['elements'], '/', d['signals_above_fold']['carriers'],
                  d['signals_above_fold']['carrier_list'])
            print('  repeats', d['repeats'], '| pageerrors', len(seen), seen[:3])
            pg.close()

        # --- drive the anchor at 1440, normal motion then reduced motion
        drive = {}
        for mode in ("normal", "reduce"):
            ctx = b.new_context(viewport={'width': 1440, 'height': 900},
                                reduced_motion=("reduce" if mode == "reduce" else "no-preference"))
            pg = ctx.new_page()
            seen = []
            pg.on("pageerror", lambda e: seen.append(str(e)))
            pg.goto(f"file://{PAGE}")
            pg.wait_for_timeout(400)
            before = pg.evaluate(DRIVE)['before']
            pg.wait_for_timeout(1200)
            after = pg.evaluate(AFTER)
            drive[mode] = {"before": before, "after": after, "pageerrors": seen}
            print('==DRIVE', mode, 'BEFORE', before)
            print('           AFTER ', after, '| errors', len(seen))
            ctx.close()
        b.close()
    json.dump({"render": res, "errors": errs, "drive": drive}, open(f"{OUT}/render251.json", "w"), indent=1)


if __name__ == '__main__':
    main()
