"""Render up-is-bad.html to a PNG beside it at 1440, at the seat, and print each tile's measured inks.
Run: export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh;
python3 notes/_lanes/309/G/render_up_is_bad.py"""
import os, sys
from playwright.sync_api import sync_playwright
here = os.path.dirname(os.path.abspath(__file__))
name = sys.argv[1] if len(sys.argv) > 1 else "up-is-bad"
src = os.path.join(here, name + ".html"); out = os.path.join(here, name + ".png")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    pg = b.new_page(viewport={"width": 1440, "height": 800}, device_scale_factor=2)
    pg.goto("file://" + src); pg.wait_for_timeout(300)
    info = pg.evaluate("""() => [...document.querySelectorAll('.cn-metric .metric')].map(e => {
        const g = e.querySelector('.metric-delta .glyph'), s = e.querySelector('.dv-series');
        return {mode: e.closest('[data-theme]').dataset.theme, bad: e.classList.contains('up-is-bad'),
                delta: e.querySelector('.metric-delta').className.replace('metric-delta ',''),
                glyph: getComputedStyle(g).color, glyphOpacity: getComputedStyle(g).opacity,
                spark: s ? getComputedStyle(s).stroke : null};
    })""")
    for i in info: print(i)
    pg.screenshot(path=out, full_page=True)
    b.close()
print("wrote", out)
