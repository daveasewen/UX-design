import glob, os, json, sys, math

sys.path.insert(0, "/sessions/upbeat-eager-thompson/mnt/outputs/_render-env/pylibs")
from playwright.sync_api import sync_playwright

ROOT = "/sessions/upbeat-eager-thompson/mnt/UX-design"
D = f"{ROOT}/reviews/_assets/type-css-180-specimen"
OUT = "/sessions/upbeat-eager-thompson/mnt/outputs"

shell = glob.glob(os.path.expanduser(
    "/sessions/upbeat-eager-thompson/mnt/outputs/_render-env/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell"))

def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)

def contrast(rgb1, rgb2):
    l1, l2 = luminance(rgb1), luminance(rgb2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def parse_rgb(s):
    # "rgb(17, 17, 17)" -> (17,17,17)
    nums = s[s.index("(")+1:s.index(")")].split(",")
    return tuple(float(n) for n in nums[:3])

results = {}

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=shell[0] if shell else None, headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])

    for width in (1180, 760):
        for name, fname in (("pane_a_today", "pane-a-today.html"), ("pane_b_declared", "pane-b-declared.html")):
            pg = b.new_page(viewport={"width": width, "height": 900})
            pg.goto(f"file://{D}/{fname}")
            pg.wait_for_timeout(300)
            fonts_ok = pg.evaluate("document.fonts.check('16px HSBC_MtUnivers_Latin')")
            bg = pg.evaluate("getComputedStyle(document.body).backgroundColor")
            col = pg.evaluate("getComputedStyle(document.body).color")
            # also read the account-card's own surface (should be IDENTICAL in both panes -- unaffected control)
            card_bg = pg.evaluate("getComputedStyle(document.querySelector('.account-card')).backgroundColor")
            key = f"{name}_{width}"
            results[key] = {
                "width": width, "fonts_ok": fonts_ok,
                "body_background": bg, "body_color": col, "card_background_control": card_bg,
            }
            shot = f"{OUT}/type180_{name}_{width}.png"
            pg.screenshot(path=shot, full_page=True)
            results[key]["screenshot"] = shot
            pg.close()

    b.close()

# numeric deltas + contrast, computed from the MEASURED values at 1180 (colour is viewport-independent, sanity check both widths agree)
a_bg = parse_rgb(results["pane_a_today_1180"]["body_background"])
b_bg = parse_rgb(results["pane_b_declared_1180"]["body_background"])
a_col = parse_rgb(results["pane_a_today_1180"]["body_color"])
b_col = parse_rgb(results["pane_b_declared_1180"]["body_color"])

a_bg_760 = parse_rgb(results["pane_a_today_760"]["body_background"])
b_bg_760 = parse_rgb(results["pane_b_declared_760"]["body_background"])

summary = {
    "pane_a_bg_measured": a_bg,
    "pane_b_bg_measured": b_bg,
    "widths_agree": (a_bg == a_bg_760) and (b_bg == b_bg_760),
    "delta_per_channel": [b_bg[i] - a_bg[i] for i in range(3)],
    "text_colour_a": a_col,
    "text_colour_b": b_col,
    "text_colour_identical_across_panes": a_col == b_col,
    "contrast_white_text_vs_pane_a": contrast(a_col, a_bg),
    "contrast_white_text_vs_pane_b": contrast(b_col, b_bg),
    "card_surface_control_identical": results["pane_a_today_1180"]["card_background_control"] == results["pane_b_declared_1180"]["card_background_control"],
}

results["_summary"] = summary

with open(f"{OUT}/type180_measure.json", "w") as f:
    json.dump(results, f, indent=2)

print(json.dumps(summary, indent=2))
print("FONTS OK:", all(v.get("fonts_ok") for k, v in results.items() if isinstance(v, dict) and "fonts_ok" in v))
