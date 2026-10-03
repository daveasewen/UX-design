#!/usr/bin/env python3
"""Lane PR #316 render driver: pending roundel + footer, light and dark. Usage: render_pr.py <tag>"""
import os, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
OUT = os.path.dirname(os.path.abspath(__file__))
tag = sys.argv[1]
shell = os.environ.get('RENDER_SHELL')
T = 'file://' + ROOT + '/knowledge/snippets/Template-confirmation.reference.html'
N = 'file://' + ROOT + '/knowledge/snippets/Notifications.reference.html'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=shell, headless=True, args=["--no-sandbox","--disable-gpu"])
    pg = b.new_page(viewport={"width": 1280, "height": 1000}, device_scale_factor=2)
    for mode in ("light", "dark"):
        pg.goto(T); pg.evaluate("m=>document.body.setAttribute('data-theme',m)", mode)
        pg.wait_for_timeout(1500)
        print('fonts', pg.evaluate("document.fonts.check('16px \"Univers Next for HSBC\"')"))
        pend = pg.locator('#cf-b-title').locator('xpath=ancestor::div[contains(@class,"confirm")][1]')
        pend.scroll_into_view_if_needed(); pg.wait_for_timeout(400)
        bb = pend.bounding_box()
        pg.screenshot(path=f"{OUT}/{tag}-pending-{mode}.png", clip={"x":bb["x"],"y":bb["y"],"width":bb["width"],"height":min(bb["height"],320)})
        roundel = pg.locator('#cf-b-title').locator('xpath=preceding-sibling::*[1]')
        rb = roundel.bounding_box()
        pg.screenshot(path=f"{OUT}/{tag}-roundel-{mode}.png", clip={"x":rb["x"]-12,"y":rb["y"]-12,"width":rb["width"]+24,"height":rb["height"]+24})
        fill = roundel.evaluate("e=>getComputedStyle(e.querySelector('.disc')).fill")
        foot = pg.locator('footer').last
        foot.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        fb = foot.bounding_box()
        pg.screenshot(path=f"{OUT}/{tag}-footer-{mode}.png", clip={"x":0,"y":max(fb["y"]-80,0),"width":1280,"height":fb["height"]+80})
        fbg = foot.evaluate("e=>{const f=e.querySelector('.ft')||e; return getComputedStyle(f).backgroundColor}")
        page_bg = pg.evaluate("getComputedStyle(document.body).backgroundColor")
        print(mode, 'disc fill', fill, '| footer bg', fbg, '| page bg', page_bg)
        if tag != 'before':
            pg.goto('file://' + OUT + '/compare.html'); pg.evaluate("m=>document.body.setAttribute('data-theme',m)", mode); pg.wait_for_timeout(800)
            pg.screenshot(path=f"{OUT}/{tag}-compare-amber-{mode}.png", full_page=True)
            print(mode, 'notification icon colour', pg.locator('.note.tint.warn .ic').evaluate("e=>getComputedStyle(e).color"),
                  '| inline icon', pg.locator('.inline.warn .ic').evaluate("e=>getComputedStyle(e).color"),
                  '| pending disc', pg.locator('#pend .disc').evaluate("e=>getComputedStyle(e).fill"),
                  '| marks', pg.locator('.note.tint.warn').evaluate("e=>getComputedStyle(e).getPropertyValue('--mark')"), pg.locator('#pend svg').evaluate("e=>getComputedStyle(e).getPropertyValue('--mark')"))
    b.close()
