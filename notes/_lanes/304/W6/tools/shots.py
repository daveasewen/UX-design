"""shots.py <outdir> — W6: before/after element shots of the first chart figures on cand2-r1 and r3 overview, 1440, reduced motion AND no-preference."""
import os, sys
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
H = os.path.expanduser('~')
sides = {'head': H + '/f5st/f5', 'w6': H + '/w6st'}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for side, root in sides.items():
        for r in ('c2r1', 'c2r3'):
            for rm in ('reduce', 'no-preference'):
                for attempt in range(8):   # HEAD under reduced motion: keep the first MISFIT load (the bug), else the last
                    pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion=rm)
                    pg.goto('file://' + root + '/' + r + '/out/index.html'); pg.wait_for_timeout(1500)
                    bad = pg.evaluate("""() => [...document.querySelectorAll('svg.dv-fit')].map(s => s.viewBox.baseVal.width + '/' + Math.round(s.getBoundingClientRect().width)).join(' ')""")
                    if not (side == 'head' and rm == 'reduce') or any(x.split('/')[0] != x.split('/')[1] for x in bad.split()) or attempt == 7: break
                    pg.close()
                figs = pg.query_selector_all('figure.dv:has(svg.dv-fit)')
                f = figs[0]; f.scroll_into_view_if_needed()
                fn = f'{out}/{r}-overview-chart1-{side}-{"rm" if rm == "reduce" else "motion"}.png'
                f.screenshot(path=fn); print(fn.split('/')[-1], bad)
                pg.close()
    b.close()
