#!/usr/bin/env python3
"""render.py — THE CANONICAL HOME of the sandbox HTML→PNG screenshot script (s191-D2, #191).

Why this file exists IN THE REPO: the runbook (`knowledge/_RUNBOOK-render-verify.md` §6) had
sessions retype this into `/tmp/render.py` each time — and the sandbox is WIPED every session,
so the script existed nowhere permanent. The memory grader then (correctly) reported the memory
hook naming `render.py` as STALE forever, because no such file existed anywhere in UX-design.
Dave ruled #191: home the script here; the sandbox COPIES it, never retypes it.

Usage (in-sandbox, after the runbook's env staging — read the runbook, this is the payload only):
    python3 knowledge/_render/render.py <page.html> <out.png> [width] [height]

Font assertion uses the canvas-probe discipline where needed — see the runbook; the plain
`document.fonts.check` here is the 2026-07-23 proven shape and the runbook governs when it lies.
"""
import glob
import os
import sys

from playwright.sync_api import sync_playwright


def render(src: str, out: str, width: int = 1180, height: int = 1400) -> None:
    shell = glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell"))
    with sync_playwright() as p:
        b = p.chromium.launch(
            executable_path=shell[0] if shell else None, headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": width, "height": height})
        pg.goto("file://" + os.path.abspath(src))   # ⛔ never set_content() — drops type.css (#29)
        pg.wait_for_timeout(1200)                   # let CSS entry motion settle
        assert pg.evaluate("document.fonts.check('16px HSBC_MtUnivers_Latin')"), \
            "font NOT loaded — a screenshot without the real font verifies nothing"
        pg.screenshot(path=out, full_page=True)
        b.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    render(sys.argv[1], sys.argv[2],
           int(sys.argv[3]) if len(sys.argv) > 3 else 1180,
           int(sys.argv[4]) if len(sys.argv) > 4 else 1400)
