#!/usr/bin/env python3
"""#292 lane H — render design-system-map.html light + dark, and MEASURE it.

Run (one bash call — knowledge/_RUNBOOK-render-verify.md):

  cd <repo> && export TMPDIR=/dev/shm
  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/292/H/shoot.py

Writes: design-system-map.png (light, the deliverable)
        design-system-map-dark.png
        measured.json
"""
import json, os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = "file://" + os.path.join(HERE, "design-system-map.html")
SHELL = os.environ.get("RENDER_SHELL") or None

PROBE = r"""() => {
  const R = el => { const b = el.getBoundingClientRect();
    return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height)}; };
  const frame = document.querySelector('.frame');
  const tiles = [...document.querySelectorAll('.tile')].map(t => ({
    idx: t.querySelector('.idx').textContent.trim(),
    title: t.querySelector('h2').textContent.trim(),
    state: t.dataset.state,
    edge: t.dataset.edge,
    box: R(t),
    clipped: t.scrollHeight - t.clientHeight,
    cite: (t.querySelector('.src')||{}).textContent || null,
    badge: !!t.querySelector('.badge')
  }));
  const hub = document.querySelector('.hub');
  const cs = getComputedStyle(document.body);
  return {
    theme: document.documentElement.dataset.theme,
    bodyBg: cs.backgroundColor, bodyColor: cs.color,
    font: getComputedStyle(document.querySelector('.masthead h1')).fontFamily,
    frame: R(frame),
    gridCols: getComputedStyle(frame).gridTemplateColumns,
    gap: getComputedStyle(frame).gap,
    hub: R(hub),
    hubClipped: hub.scrollHeight - hub.clientHeight,
    ringWords: [...document.querySelectorAll('.ring span')].map(s=>s.textContent.trim()),
    tiles,
    have: tiles.filter(t=>t.state==='have').length,
    soon: tiles.filter(t=>t.state==='soon').length,
    pageHeight: document.documentElement.scrollHeight
  };
}"""

def main():
    errs, res = [], {}
    with sync_playwright() as p:
        kw = {"args": ["--no-sandbox"]}
        if SHELL:
            kw["executable_path"] = SHELL
        b = p.chromium.launch(**kw)
        try:
            for mode, out in (("light", "design-system-map.png"),
                              ("dark",  "design-system-map-dark.png")):
                pg = b.new_page(viewport={"width": 1440, "height": 1200},
                                device_scale_factor=2)
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.goto(PAGE, wait_until="networkidle")
                pg.evaluate("m => document.documentElement.dataset.theme = m", mode)
                pg.wait_for_timeout(250)
                res[mode] = pg.evaluate(PROBE)
                pg.screenshot(path=os.path.join(HERE, out), full_page=True)
                pg.close()
        finally:
            b.close()
    payload = {"page": PAGE, "viewport": "1440 @2x full_page",
               "pageErrors": errs, "measured": res}
    with open(os.path.join(HERE, "measured.json"), "w") as f:
        json.dump(payload, f, indent=1)
    for m in ("light", "dark"):
        r = res[m]
        print(m, "bg", r["bodyBg"], "h", r["pageHeight"],
              "have", r["have"], "soon", r["soon"],
              "clip", sum(t["clipped"] for t in r["tiles"]) + r["hubClipped"])
    print("errors:", errs)

if __name__ == "__main__":
    main()
