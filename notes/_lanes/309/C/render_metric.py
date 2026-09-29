"""Render notes/_lanes/309/C/metric-with-without-trend.html to a PNG beside it, at 1440 px, at the seat.
Run: export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh;
python3 notes/_lanes/309/C/render_metric.py"""
import os
from playwright.sync_api import sync_playwright
here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "metric-with-without-trend.html")
out = os.path.join(here, "metric-with-without-trend.png")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    pg = b.new_page(viewport={"width": 1440, "height": 560}, device_scale_factor=1)
    pg.goto("file://" + src)
    pg.wait_for_timeout(300)
    info = pg.evaluate("""() => [...document.querySelectorAll('.cn-metric .metric')].map(e => {
        const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
        return {w: Math.round(r.width), h: Math.round(r.height), bg: cs.backgroundColor, pad: cs.padding,
                border: cs.borderTopWidth + ' ' + cs.borderTopColor, spark: !!e.querySelector('.metric-spark'),
                glyph: getComputedStyle(e.querySelector('.metric-delta .glyph')).color};
    })""")
    for i in info: print(i)
    pg.screenshot(path=out, full_page=True)
    b.close()
print("wrote", out)
