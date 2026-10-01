"""#313 A5 — s313-D42 / W-307ye: does the Tabs part fill its container?
Run at the seat after the canon regen:
  export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh
  python3 notes/_lanes/313/A5/tabs_probe.py
PASS when .tabs == host width in both hosts (1200 and 360) and --tabs-w reads 100%.
The panel keeps its 52ch reading width (s313-D42's page: 'The panel's text keeps its reading width')."""
import os, json, sys
from playwright.sync_api import sync_playwright
here = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL") or None)
    pg = b.new_page(viewport={"width": 1440, "height": 400})
    pg.goto("file://" + os.path.join(here, "tabs_probe.html"))
    r = pg.evaluate("""()=>{const w=id=>document.getElementById(id).getBoundingClientRect().width;
      return {host:w('host'), tabs:w('t'), panel:w('p'), host2:w('host2'), tabs2:w('t2'),
              tabsW:getComputedStyle(document.getElementById('t')).getPropertyValue('--tabs-w').trim()}}""")
    pg.screenshot(path=os.path.join(here, "tabs_probe-1440.png"))
    b.close()
ok = r["tabs"] == r["host"] and r["tabs2"] == r["host2"] and r["tabsW"] == "100%"
print(json.dumps(r)); print("PASS — Tabs fills its container" if ok else "FAIL — Tabs does not fill its container")
sys.exit(0 if ok else 1)
