#!/usr/bin/env python3
"""One-off visual-check render for the Button responsive fitness-test.
Session-specific (headless Chromium via Playwright). Not part of _build_all.py."""
import os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "file://" + os.path.join(HERE, "_fitness-test", "button-responsive.html")
OUT = "/sessions/magical-practical-einstein/mnt/outputs"

# (filename, viewport_width, theme, narrow_container)
SHOTS = [
    ("btn-wide-light.png",   900, "light", False),
    ("btn-wide-dark.png",    900, "dark",  False),
    ("btn-narrow-light.png", 900, "light", True),
    ("btn-narrow-dark.png",  900, "dark",  True),
    ("btn-320-light.png",    320, "light", False),  # true viewport reflow (WCAG 1.4.10)
]

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    for fn, vw, theme, narrow in SHOTS:
        pg = b.new_page(viewport={"width": vw, "height": 800}, device_scale_factor=2)
        pg.goto(SRC)
        pg.evaluate(f"document.body.setAttribute('data-theme','{theme}')")
        if narrow:
            pg.evaluate("document.body.classList.add('narrow')")
        pg.wait_for_timeout(250)
        # report any horizontal overflow (the real responsive failure mode)
        overflow = pg.evaluate(
            "Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth)")
        pg.screenshot(path=os.path.join(OUT, fn), full_page=True)
        print(f"{fn:22} vw={vw:<4} theme={theme:<5} narrow={narrow!s:<5} h-overflow={overflow}px")
    b.close()
print("done")
