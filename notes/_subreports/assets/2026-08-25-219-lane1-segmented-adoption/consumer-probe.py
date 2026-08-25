#!/usr/bin/env python3
"""One-off consumer probe (#219 lane 1, NON-REPO: /var/tmp/s219l1/consumers.py — declared per
s191-D2; the durable instrument is knowledge/_render/verify_segmented_219.py).

For every shipped page that consumes the CANON .cn-segmented-control block, render it twice —
once against canon.css at HEAD, once against the working tree's — and diff the resolved geometry
of every .seg. A consumer "still renders" only if its numbers did not move.
"""
import glob, json, os, sys, shutil
ROOT = "/sessions/pensive-cool-galileo/mnt/UX-design"
OLD = "/var/tmp/s219l1/old"
PAGES = sorted(set(
    p for p in glob.glob(ROOT + "/showroom/*.html")
      + glob.glob(ROOT + "/knowledge/_fitness-test/*.canon.html")
    if "cn-segmented-control" in open(p, errors="ignore").read()))

MEASURE = """() => {
  const out = [];
  document.querySelectorAll('.cn-segmented-control .seg').forEach((s,i) => {
    const cs = getComputedStyle(s);
    const b = s.querySelector('button');
    out.push({i, cls: s.className,
              h: cs.height, w: cs.width, pad: cs.paddingTop,
              r: cs.borderTopLeftRadius,
              bh: b ? getComputedStyle(b).height : null,
              bp: b ? getComputedStyle(b).paddingLeft : null});
  });
  return out;
}"""

def shell():
    r = os.environ["PLAYWRIGHT_BROWSERS_PATH"]
    return glob.glob(os.path.join(r, "chromium_headless_shell-*/chrome-linux/headless_shell"))[0]

from playwright.sync_api import sync_playwright
def run(pages, swap):
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell(), headless=True,
                              args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu"])
        pg = b.new_page(viewport={"width":1280,"height":900})
        for f in pages:
            pg.goto("file://" + f + "#theme=console&m=light")
            pg.wait_for_timeout(500)
            res[f] = pg.evaluate(MEASURE)
        b.close()
    return res

live = os.path.join(ROOT, "knowledge/canon/canon.css")
bak = "/var/tmp/s219l1/canon-live.css"
after = run(PAGES, False)
shutil.copy(live, bak)
shutil.copy(os.path.join(OLD, "canon.css"), live)
try:
    before = run(PAGES, True)
finally:
    shutil.copy(bak, live)          # ALWAYS restore, even on a crash

moved, same, radius_gained = [], 0, []
for f in PAGES:
    for a, bb in zip(after[f], before[f]):
        key = os.path.relpath(f, ROOT) + " " + a["cls"]
        geom_a = (a["h"], a["w"], a["pad"], a["bh"], a["bp"])
        geom_b = (bb["h"], bb["w"], bb["pad"], bb["bh"], bb["bp"])
        if geom_a != geom_b:
            moved.append((key, geom_b, geom_a))
        else:
            same += 1
        if a["r"] != bb["r"]:
            radius_gained.append((key, bb["r"], a["r"]))
print("pages measured: %d" % len(PAGES))
for f in PAGES: print("  " + os.path.relpath(f, ROOT) + "  (%d .seg)" % len(after[f]))
print("\nGEOMETRY UNCHANGED on %d .seg element(s)" % same)
if moved:
    print("MOVED — %d:" % len(moved))
    for k, b_, a_ in moved: print("  x %s\n      before %r\n      after  %r" % (k, b_, a_))
else:
    print("MOVED — none. No consumer pixel moved.")
print("\nRADIUS GAINED (console) on %d element(s):" % len(radius_gained))
for k, b_, a_ in radius_gained: print("  + %-58s %s -> %s" % (k, b_, a_))
sys.exit(1 if moved else 0)
