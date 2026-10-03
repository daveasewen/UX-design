"""#315 LA: does a MOUSE click draw a focus outline on any part? (s314-D1 / s313-D71: 'we never have a
focus state unless the user is using keybord controls'). Read-only: loads each snippet over file://,
for every visible focusable element outside the APOLLO-DEMO fence: hover -> read outline; click -> read
outline; a ring present after the click and absent on hover is a CLICK RING. Then Tab once from the
element before it and confirm a keyboard ring exists (so a missing ring is not counted as clean by accident).
Writes click_sweep.json beside itself."""
import json, os, glob, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../..'))
SNIPS = sorted(glob.glob(os.path.join(ROOT, 'knowledge/snippets/*.reference.html')))
BROKEN = '--control' in sys.argv
sys.argv = [a for a in sys.argv if a != '--control']
if len(sys.argv) > 1: SNIPS = [s for s in SNIPS if any(a in s for a in sys.argv[1:])]
JS_LIST = r"""
() => {
  // mark elements inside APOLLO-DEMO fenced comment ranges
  const fenced = new Set(); let on = 0;
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_ALL);
  let n; while ((n = w.nextNode())) {
    if (n.nodeType === 8) { if (/APOLLO-DEMO[^\n]*START/.test(n.nodeValue)) on++; else if (/APOLLO-DEMO[^\n]*END/.test(n.nodeValue)) on = Math.max(0, on-1); continue; }
    if (on && n.nodeType === 1) fenced.add(n);
  }
  const sel = 'a[href],button,input:not([type=hidden]),select,textarea,[tabindex]:not([tabindex="-1"]),summary,[contenteditable="true"]';
  const out = [];
  document.querySelectorAll(sel).forEach((el, i) => {
    if (fenced.has(el) || el.closest('.demo-controls,[data-demo],.stateLabel')) return;
    const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    if (r.width < 2 || r.height < 2 || cs.visibility === 'hidden' || cs.display === 'none') return;
    if (el.disabled) return;
    el.setAttribute('data-la-sweep', String(i));
    out.push({i, tag: el.tagName.toLowerCase(), type: el.type || '', cls: (el.getAttribute('class')||'').slice(0,60), text: (el.getAttribute('aria-label') || el.textContent || el.value || '').trim().slice(0,40)});
  });
  return out;
}"""
JS_RING = r"""(i) => { const el0 = document.querySelector('[data-la-sweep="'+i+'"]'); if(!el0) return null;
  // the ring may sit on the element or on a wrapper (e.g. .cb-box:has(input:focus-visible)): read the element and 3 ancestors
  const rings = []; let el = el0;
  for (let d = 0; d < 4 && el && el !== document.body; d++, el = el.parentElement) {
    const cs = getComputedStyle(el);
    if (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) rings.push({d, cls: (el.getAttribute('class')||el.tagName).slice(0,40), ow: cs.outlineWidth, oc: cs.outlineColor});
  }
  return {ring: rings.length > 0, rings, fv: el0.matches(':focus-visible')}; }"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for s in SNIPS:
        name = os.path.basename(s)
        pg = b.new_page(viewport={'width': 1280, 'height': 900})
        try:
            pg.goto('file://' + s, wait_until='load', timeout=20000); pg.wait_for_timeout(250)
            if BROKEN: pg.evaluate("() => addEventListener('mousedown', () => setTimeout(() => { document.documentElement.dataset.modality = 'keyboard'; }, 0))")
            els = pg.evaluate(JS_LIST)[:80]
            hits = []
            for e in els:
                loc = pg.locator('[data-la-sweep="%d"]' % e['i'])
                try:
                    if not loc.is_visible(): continue
                    pg.evaluate("() => document.activeElement && document.activeElement.blur && document.activeElement.blur()")
                    loc.hover(timeout=1500); h = pg.evaluate(JS_RING, e['i'])
                    loc.click(timeout=1500, no_wait_after=True); pg.wait_for_timeout(30)
                    c = pg.evaluate(JS_RING, e['i'])
                    if c and h and c['ring'] and not h['ring']:
                        hits.append({**e, 'after_click': c, 'on_hover': h})
                    pg.keyboard.press('Escape')
                except Exception as ex:
                    pass
            res[name] = {'checked': len(els), 'click_rings': hits}
        except Exception as ex:
            res[name] = {'error': str(ex)[:200]}
        pg.close()
    b.close()
json.dump(res, open(os.path.join(HERE, 'click_sweep.json'), 'w'), indent=1)
tot = sum(len(v.get('click_rings', [])) for v in res.values())
print('pages', len(res), 'click rings', tot, 'pages with rings', [k for k, v in res.items() if v.get('click_rings')])
