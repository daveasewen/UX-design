import glob, os, sys, json
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
    pg = b.new_page(viewport={"width": 1600, "height": 1400})
    pg.goto(f"file://{DOC}")
    pg.wait_for_timeout(500)

    frames = pg.frames
    print("TOTAL FRAMES (incl. main):", len(frames))
    report = []
    for fr in frames:
        if fr == pg.main_frame:
            continue
        url = fr.url
        try:
            bg = fr.evaluate("getComputedStyle(document.body).backgroundColor")
            fonts_ok = fr.evaluate("document.fonts.check('16px HSBC_MtUnivers_Latin')")
        except Exception as e:
            bg = f"ERROR: {e}"
            fonts_ok = None
        report.append({"frame_url": url, "body_bg": bg, "fonts_ok": fonts_ok})

    for r in report:
        print(r)

    # top-of-page + full-page screenshots for visual confirmation
    pg.screenshot(path=f"{OUT}/type180_outer_viewport.png", full_page=False)
    pg.screenshot(path=f"{OUT}/type180_outer_full.png", full_page=True)

    with open(f"{OUT}/type180_outer_frames.json", "w") as f:
        json.dump(report, f, indent=2)

    b.close()

print("DONE")
