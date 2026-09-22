# #297 lane R - SKETCH renders: the review's proposals applied as CSS/DOM injected AT RENDER TIME ONLY.
# The deck file is never written. Usage: python3 sketch_render.py <deck.html> <outdir> [WxH]
import os, sys, time, json
from playwright.sync_api import sync_playwright
deck = os.path.abspath(sys.argv[1]); out = os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
W, H = [int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else '1440x900').split('x')]
BLOCK = ("window.addEventListener('pointermove', function(e){ e.stopImmediatePropagation(); }, {capture:true});"
         "window.addEventListener('mousemove', function(e){ e.stopImmediatePropagation(); }, {capture:true});")
CSS = r"""
/* 8 - the rail gutter */
.slide{padding-left:max(6vw,232px)!important}
#s10map{padding-left:max(6vw,232px)!important}
/* 10 - balanced headlines; 11 - three headline sizes */
h2{text-wrap:balance}
#s5x h2{font-size:40px!important;max-width:24em!important}
#s10map h2{font-size:40px!important}
/* 1 - the loop (04) */
#s5x .steps li{border:1px solid var(--g3)!important}
#s5x .steps li.k4,#s5x .steps li.k5{border-top:2px solid var(--accent)!important}
#s5x .sh,#s5x .blk .sh,#s5x .red .sh{background:none!important;color:#111!important;font-size:12px!important;font-weight:500!important;letter-spacing:.14em!important;
  border-bottom:1px solid var(--g3);padding:12px 14px 10px!important;min-height:calc(2 * 16.8px + 22px)!important}
#s5x .sh .n{color:var(--g6);margin-right:.6em}
#s5x .steps li+li::before{border-top:1px solid #111!important;top:27px!important}
#s5x .steps li+li::after{border-left:6px solid #111!important;border-top:4px solid transparent!important;border-bottom:4px solid transparent!important;top:24px!important;left:-7px!important}
#s5x .regen{border-width:1.5px!important}
#s5x .st{font-style:normal!important;color:var(--g6)}
#s5x .sb{font-size:16px!important}
/* 4 - the five causes (06) */
#s4p .c5 > div{border-top:1px solid var(--g3);padding-top:16px!important}
#s4p .c5 .ix{color:var(--g6)!important}
#s4p .c5 h3{font-size:18px!important;line-height:1.3!important}
#s4p .c5 div p:last-child{font-size:16px!important}
/* 2 - the three problems (11) */
#s6b .wb-h span{background:none!important;color:#111!important;font-size:12px!important;font-weight:500!important;letter-spacing:.14em!important;padding:0 0 10px!important;min-width:0!important}
#s6b .wb-h.sp span{color:var(--accent)!important}
#s6b .wb-bus path{stroke:#111!important;stroke-width:1!important}
#s6b .wb-g{border:1px solid var(--g3)!important;border-top:2px solid #111!important}
#s6b .wb-g.sp{border-top-color:var(--accent)!important}
#s6b .wb-g.sp .gl,#s6b .wb-g.qu .gl{display:none}
#s6b .wb-g.all .gl{color:var(--g6)!important;font-size:12px!important}
#s6b .wb-g li{font-size:16px!important}
/* 5 - the three elements (12) */
#s10 .grid5 .ix{color:var(--g6)!important}
#s10 .grid4{border-left-color:var(--g3)!important}
#s10 .grid4>div{border-right-color:var(--g3)!important;border-bottom-color:var(--g3)!important}
/* 3 - the map (13) */
#s10map .tile .src{display:none!important}
#s10map .tile .idx{font-size:12px!important;font-weight:500!important;color:var(--g6)!important}
#s10map .tile h3{font-size:16px!important;font-weight:600!important}
#s10map .tile .d{font-size:13px!important;line-height:1.4!important}
#s10map .tile[data-state="soon"]{background:var(--white)!important;outline:1px dashed var(--g5);outline-offset:-5px}
#s10map .tile[data-state="soon"] .ink-block{opacity:1!important}
#s10map .tile[data-state="soon"] h3{color:var(--g6)!important}
#s10map .badge{font-family:var(--font)!important;font-size:11px!important;font-weight:500!important;letter-spacing:.14em!important;border:0!important;padding:0!important;color:var(--g6)!important;background:none!important}
"""
DOM = r"""() => {
  // 1 - 04 headers: '1 · Intake' -> '01' (grey) + 'Intake'
  document.querySelectorAll('#s5x .sh').forEach(e => { const m = e.textContent.match(/^(\d)\s*·\s*(.*)$/); if (m) e.innerHTML = '<span class="n">0' + m[1] + '</span>' + m[2]; });
  // 12 - 07 weight: light set-up, bold point
  const h7 = document.querySelector('#s6 h2'); if (h7) h7.innerHTML = 'The first improvement: <b>the catalogue went from 36 to&nbsp;137.</b>';
  // 2 - 11 labels and the tick
  const all = document.querySelector('#s6b .wb-g.all .gl'); if (all) all.textContent = 'Shared by all three';
  const done = document.querySelector('#s6b .done'); const lib = document.querySelector('#s6b .wb-g.all li');
  if (done && lib) { done.textContent = 'Addressed first'; done.style.margin = '6px 0 0'; lib.appendChild(done); }
  // 4 - 06: one title block height so the five descriptions start on one line
  const hs = [...document.querySelectorAll('#s4p .c5 h3')]; const mx = Math.max(...hs.map(h => h.getBoundingClientRect().height)); hs.forEach(h => h.style.minHeight = mx + 'px');
  // 3 - 13: sentence case + plain words
  const tc = {'Brand Standards':'Brand standards','User Research & Insights':'User research & insights','Design Patterns':'Design patterns','Tone of Voice':'Tone of voice',
    'Accessibility Standards':'Accessibility standards','Governance & Operations':'Governance & operations','Data & Insights':'Data & insights','Design Tokens':'Design tokens',
    'Content Guidelines':'Content guidelines','UX Principles':'UX principles','CX Principles':'CX principles','UX Components':'UX components'};
  document.querySelectorAll('#s10map .tile h3').forEach(h => { if (tc[h.textContent]) h.textContent = tc[h.textContent]; });
  document.querySelectorAll('#s10map .tile .d').forEach(d => { d.textContent = d.textContent.replace('Every ruling inscribed with its receipt.', 'Every decision recorded, with its evidence.').replace('Governed components, each with a meta and a build.', 'Governed components, each documented and built in code.'); });
  return true;
}"""
want = ['s5x','s4p','s6','s7b','s6b','s10','s10map','s12','s3']
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'], args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
    pg.add_init_script(BLOCK)
    pg.goto('file://' + deck, wait_until='load'); time.sleep(3.0)
    pg.add_style_tag(content=CSS); pg.evaluate(DOM); time.sleep(0.5)
    pg.evaluate("() => { const hs = [...document.querySelectorAll('#s4p .c5 h3')]; hs.forEach(h => h.style.minHeight = ''); const mx = Math.max(...hs.map(h => h.getBoundingClientRect().height)); hs.forEach(h => h.style.minHeight = mx + 'px'); }")
    order = pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s => s.id)")
    facts = {}
    for i, sid in enumerate(order):
        if sid not in want: continue
        pg.evaluate('n => window.deckGo(n)', i); time.sleep(1.8)
        pg.evaluate('() => { window.brSet && window.brSet(0,0); window.shlSet && window.shlSet(0,0); if (window.calSetTime){ window.calSetTime(0); window.calStill(); } }'); time.sleep(0.3)
        facts[sid] = pg.evaluate("""(sid) => { const s = document.getElementById(sid); const t = document.querySelector('#chrail .cr-ch.is-cur .cr-t'); const i = s.querySelector('.inner');
           const h = s.querySelector('h2, h1'); return {inner_x: i ? i.getBoundingClientRect().x : null, rail_r: t ? t.getBoundingClientRect().right : null, h2_h: h ? h.getBoundingClientRect().height : null}; }""", sid)
        pg.screenshot(path=os.path.join(out, 'P%02d-%s.png' % (i + 1, sid)))
    b.close()
json.dump(facts, open(os.path.join(out, '_sketch_facts.json'), 'w'), indent=1)
print('sketch renders', len(facts), json.dumps(facts))
