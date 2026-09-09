#!/usr/bin/env python3
"""#261 K3 — rhythm + arrow-colour driver (lane fragment; not a gate).

Measures label->value->delta offsetTop deltas on the ORIGINAL (git 7647aaf, dumped to
/tmp/orig-kpi.html) and on the working Kpi-tile snippet, and reads the resolved delta-arrow
colour across 4 themes x 2 modes. goto file:// only (RUNBOOK-render-verify).
"""
import json, os, sys, pathlib

for extra in ("/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu",
              "/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/x86_64-linux-gnu"):
    if os.path.isdir(extra):
        os.environ["LD_LIBRARY_PATH"] = extra + ":" + os.environ.get("LD_LIBRARY_PATH", "")
from playwright.sync_api import sync_playwright

ARGS = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--force-color-profile=srgb"]
ROOT = pathlib.Path("/sessions/zen-funny-hawking/mnt/UX-design")
CUR = ROOT / "knowledge/snippets/Kpi-tile.reference.html"
# the original (git 7647aaf) is staged under a dir with a ../canon sibling so its
# <link href="../canon/type.css"> resolves — otherwise it renders UNSTYLED and the
# comparison is meaningless (this bit me once at #261 K3).
ORIG = pathlib.Path("/sessions/zen-funny-hawking/tmp/k3orig/snippets/orig.html")

RHYTHM = """(sel) => {
  const out = [];
  for (const t of document.querySelectorAll(sel.tile)) {
    const lbl = t.querySelector(sel.lbl), val = t.querySelector(sel.val),
          del = t.querySelector(sel.del);
    if (!lbl || !val || !del) continue;
    const L = lbl.getBoundingClientRect(), V = val.getBoundingClientRect(),
          D = del.getBoundingClientRect();
    out.push({name: (t.getAttribute('aria-label')||'').split(',')[0],
              compact: t.classList.contains('compact'),
              lbl_to_val: +(V.top - L.top).toFixed(2),
              val_to_del: +(D.top - V.top).toFixed(2),
              lbl_h: +L.height.toFixed(2), val_h: +V.height.toFixed(2)});
  }
  return out;
}"""

ARROW = """() => {
  const out = {};
  for (const k of ['up','down']) {
    const el = document.querySelector('.kpi-delta.'+k+' .glyph');
    out[k] = el ? getComputedStyle(el).color : null;
  }
  const sp = document.querySelector('.spark-inline[data-trend="up"] .dv-series');
  out.spark_up = sp ? getComputedStyle(sp).stroke : null;
  const sd = document.querySelector('.spark-inline[data-trend="down"] .dv-series');
  out.spark_down = sd ? getComputedStyle(sd).stroke : null;
  return out;
}"""


def main():
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=ARGS)
        pg = b.new_page(viewport={"width": 1280, "height": 1600})

        pg.goto(ORIG.as_uri()); pg.wait_for_timeout(250)
        res["original"] = pg.evaluate(RHYTHM, {"tile": ".kpi-tile", "lbl": ".lbl16",
                                               "val": ".amt", "del": ".delta"})
        pg.goto(CUR.as_uri()); pg.wait_for_timeout(250)
        res["k3"] = pg.evaluate(RHYTHM, {"tile": ".kpi-tile", "lbl": ".kpi-lbl",
                                         "val": ".kpi-val", "del": ".kpi-delta"})

        res["arrows"] = {}
        for theme in ["mono", "legacy", "console", "supercharge"]:
            for mode in ["light", "dark"]:
                pg.evaluate("""([t,m]) => {
                  if (t === 'mono') document.documentElement.removeAttribute('data-apollo-theme');
                  else document.documentElement.setAttribute('data-apollo-theme', t);
                  document.body.setAttribute('data-theme', m);
                }""", [theme, mode])
                pg.wait_for_timeout(60)
                res["arrows"][f"{theme}/{mode}"] = pg.evaluate(ARROW)
        b.close()

    # PAIR the tiles by name and report the worst |delta| — the 1px acceptance test.
    o = {r["name"]: r for r in res["original"]}
    worst = 0.0
    rows = []
    for r in res["k3"]:
        m = o.get(r["name"])
        if not m:
            continue
        d1 = round(r["lbl_to_val"] - m["lbl_to_val"], 2)
        d2 = round(r["val_to_del"] - m["val_to_del"], 2)
        # The .compact VARIANT is a #261 addition with its own 12px padding / 4px gap; the
        # original had no compact tile, so it is reported but NOT held to the 1px test.
        if not r["compact"]:
            worst = max(worst, abs(d1), abs(d2))
        rows.append((r["name"], "compact" if r["compact"] else "default",
                     m["lbl_to_val"], r["lbl_to_val"], d1,
                     m["val_to_del"], r["val_to_del"], d2))
    res["paired"] = rows
    res["worst_abs_delta_px"] = worst
    res["verdict"] = "PASS <=1px" if worst <= 1.0 else "FAIL"
    print(json.dumps(res, indent=1))
    sys.exit(0 if worst <= 1.0 else 1)


if __name__ == "__main__":
    main()
