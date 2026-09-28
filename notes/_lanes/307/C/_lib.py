"""#307 lane C — shared render helpers. House path: run inside ONE bash call after
`export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh`.
Pages are opened with page.goto('file://...') — never set_content."""
import os, json, math, pathlib
from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[4]
OUT = pathlib.Path(__file__).resolve().parent / "shots"
OUT.mkdir(exist_ok=True)

def launch(p):
    return p.chromium.launch(executable_path=os.environ["RENDER_SHELL"], args=["--allow-file-access-from-files"])

def url(rel, frag=""):
    return "file://" + str(REPO / rel) + (("#" + frag) if frag else "")

def wait_images(page_or_frame, timeout=15000):
    page_or_frame.evaluate("""() => { document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading='eager'); }""")
    page_or_frame.wait_for_function("""() => Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)""", timeout=timeout)

def fonts_ready(page_or_frame):
    page_or_frame.evaluate("() => document.fonts ? document.fonts.ready.then(()=>true) : true")

def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(rgb):
    r, g, b = [srgb_to_lin(x) for x in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def Lstar(rgb):
    y = lum(rgb)
    return 116 * (y ** (1 / 3)) - 16 if y > 216 / 24389 else y * 24389 / 27

def parse_rgb(s):
    import re
    m = re.findall(r"[\d.]+", s)
    return tuple(int(float(x)) for x in m[:3])

def hexof(rgb):
    return "#%02X%02X%02X" % tuple(rgb)

def save_json(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=1))
