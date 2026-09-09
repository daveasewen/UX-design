#!/usr/bin/env python3
"""#261 Ft2 — drive the footer review page in Chromium and shoot the full-width pane.

goto file://… only (knowledge/_RUNBOOK-render-verify.md); executable_path=$RENDER_SHELL.
"""
import os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = "file://" + os.path.join(HERE, "261-Ft-footer-review.html")
CASES = [("fw1440", 1440, 1000, "261-Ft2-footer-1440.png"),
         ("fw1920", 1920, 1000, "261-Ft2-footer-1920.png"),
         ("fw0375", 375, 900, "261-Ft2-footer-375.png")]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for cid, w, h, out in CASES:
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg.goto(PAGE, wait_until="load")
        pg.wait_for_timeout(400)
        # the sticky control bar is review chrome; unstick it so it
        # does not paint over the specimen in an element screenshot
        pg.add_style_tag(content=".ctl{position:static !important;}")
        el = pg.query_selector("#" + cid)
        assert el is not None, "missing case " + cid
        box = el.bounding_box()
        ft = pg.query_selector("#%s footer.ft" % cid)
        fb = ft.bounding_box()
        el.screenshot(path=os.path.join(HERE, out))
        print("%s  case_w=%.0f footer_w=%.0f footer_h=%.0f -> %s"
              % (cid, box["width"], fb["width"], fb["height"], out))
        pg.close()
    b.close()
