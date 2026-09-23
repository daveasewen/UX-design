#!/usr/bin/env python3
"""shoot_p.py — lane P (#300) render driver for the boot-diet plan page.
Run at the seat, in ONE bash call, after the env:
  export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh
  python3 notes/_lanes/300/P/shoot_p.py <page.html> <outdir>
Shoots desktop (1280) and phone (390) full-page PNGs via goto(file://) — never set_content.
Also prints layout facts: page scroll width vs viewport (horizontal overflow), and any
in-segment chart label hidden by the fit check."""
import os, sys
from playwright.sync_api import sync_playwright

src = os.path.abspath(sys.argv[1]); out = sys.argv[2]
os.makedirs(out, exist_ok=True)
shell = os.environ.get("RENDER_SHELL")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=shell, headless=True,
                          args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
    for name, w, h in (("desktop", 1280, 900), ("phone", 390, 844), ("desktop-open", 1280, 900)):
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg.goto("file://" + src)
        pg.wait_for_timeout(600)
        if name.endswith("-open"):
            pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
            pg.wait_for_timeout(200)
        facts = pg.evaluate("""() => {
          const de = document.documentElement;
          const hidden = [...document.querySelectorAll('.seg .t')].filter(t => getComputedStyle(t).visibility==='hidden').map(t => t.textContent);
          const wide = [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > de.clientWidth + 1 && !e.closest('.tablewrap') && getComputedStyle(e).position!=='fixed').slice(0,8).map(e => e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().right));
          return {scrollW: de.scrollWidth, clientW: de.clientWidth, height: de.scrollHeight, hiddenLabels: hidden, overflowing: wide};
        }""")
        print(name, facts)
        pg.screenshot(path=os.path.join(out, f"plan-{name}.png"), full_page=True)
        pg.close()
    b.close()
print("SHOT", out)
