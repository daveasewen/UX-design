import glob, os, sys
sys.path.insert(0, "/sessions/upbeat-eager-thompson/mnt/outputs/_render-env/pylibs")
from playwright.sync_api import sync_playwright

ROOT = "/sessions/upbeat-eager-thompson/mnt/UX-design"
OUT = "/sessions/upbeat-eager-thompson/mnt/outputs"
DOC = f"{ROOT}/reviews/TYPE-CSS-180-SPECIMEN-2026-08-06-v1.html"

shell = glob.glob(os.path.expanduser(
    "/sessions/upbeat-eager-thompson/mnt/outputs/_render-env/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell"))

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=shell[0] if shell else None, headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
    pg = b.new_page(viewport={"width": 1600, "height": 1000})
    pg.goto(f"file://{DOC}")
    pg.wait_for_timeout(400)
    el = pg.locator("h2:has-text('760px')")
    el.scroll_into_view_if_needed()
    pg.wait_for_timeout(600)
    pg.screenshot(path=f"{OUT}/type180_760_scrolled.png", full_page=False)
    b.close()
print("done")
