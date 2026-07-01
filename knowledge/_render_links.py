#!/usr/bin/env python3
"""One-off visual-check render for the Links fitness-test (session-specific)."""
import os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "file://" + os.path.join(HERE, "_fitness-test", "links-responsive.html")
OUT = "/sessions/magical-practical-einstein/mnt/outputs"

# (filename, viewport_width, theme, related_narrow)
SHOTS = [
    ("links-wide-light.png",   900, "light", False),
    ("links-wide-dark.png",    900, "dark",  False),
    ("links-narrow-light.png", 900, "light", True),
    ("links-320-light.png",    320, "light", False),
    ("links-320-dark.png",     320, "dark",  False),
]

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    for fn, vw, theme, narrow in SHOTS:
        pg = b.new_page(viewport={"width": vw, "height": 900}, device_scale_factor=2)
        pg.goto(SRC)
        pg.evaluate(f"document.body.setAttribute('data-theme','{theme}')")
        if narrow:
            pg.evaluate("document.getElementById('related').style.setProperty('--demo-width','320px')")
        pg.wait_for_timeout(200)
        overflow = pg.evaluate(
            "Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)")
        pg.screenshot(path=os.path.join(OUT, fn), full_page=True)
        print(f"{fn:24} vw={vw:<4} theme={theme:<5} narrow={narrow!s:<5} h-overflow={overflow}px")
    b.close()
print("done")
