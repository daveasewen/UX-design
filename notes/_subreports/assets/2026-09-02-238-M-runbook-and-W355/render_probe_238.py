#!/usr/bin/env python3
"""#238 lane M — render ONE page at ONE viewport/theme with the CANVAS font probe (never fonts.check).

Usage (after `source knowledge/_render/seat_env.sh` in the SAME bash call):
    python3 render_probe_238.py <page.html> <out.png> <width> <height> <light|dark> <probe.json> [crop.png] [crop_h]

What it asserts, in order, and prints as JSON BEFORE the browser closes (verdict before cleanup):
  seat        — from $RENDER_SEAT (seat_env.sh) and from the page path itself
  theme       — documentElement[data-theme] must equal the requested theme (the page seeds it from
                prefers-color-scheme, which we emulate; a toggle-only page would need the attribute set)
  layout      — scrollWidth == clientWidth at the viewport (lane T finding 12 regression check)
  fonts       — canvas widths of one string in the TARGET face and in CONTROLS. The runbook's rule:
                the target must differ from BOTH a real different face and a nonexistent face, and both
                HSBC aliases must land on the target number. `document.fonts.check` is recorded but NOT
                used as evidence (it returned true in both the broken and working conf at #138).
  page face   — which installed face the page's own body stack resolved to, identified by width match
                against named candidates (closes lane T's "which face" UNPROVEN at this seat).
  reflow      — one throwaway full_page shot first (#217 pothole), then the real capture; the document
                height is re-measured after and the run REFUSES if it moved.
"""
import glob, json, os, sys, time

from playwright.sync_api import sync_playwright

PROBE_STRING = "Handgloves 12345"
PROBE_PX = 40
CANDIDATES = [  # name → what it is
    ("HSBC_MtUnivers_Latin", "target: the real HSBC cut"),
    ("Univers Next HSBC", "alias (type.css --uf) → must equal target"),
    ("Univers Next for HSBC", "alias (snippet --font) → must equal target"),
    ("DejaVu Sans", "control: a real different face"),
    ("Nimbus Sans", "candidate for Helvetica (fc metric alias)"),
    ("Liberation Sans", "candidate for Arial (fc metric alias)"),
    ("NoSuchFace-238", "control: nonexistent face → default fallback"),
    ("sans-serif", "generic default"),
    ("Helvetica Neue", "page body family #1, alone"),
    ("Helvetica", "page body family #2, alone"),
    ("Arial", "page body family #3, alone"),
    ('"Helvetica Neue",Helvetica,Arial,sans-serif', "the page's own body stack"),
]

JS_MEASURE = """
(args) => {
  const c = document.createElement('canvas').getContext('2d');
  const out = {};
  for (const fam of args.fams) {
    c.font = args.px + 'px ' + (fam.startsWith('"') || fam === 'sans-serif' ? fam : JSON.stringify(fam));
    out[fam] = Math.round(c.measureText(args.s).width * 100) / 100;
  }
  return out;
}
"""


def main():
    if len(sys.argv) < 7:
        sys.exit(__doc__)
    src, out, w, h, theme, probe_out = sys.argv[1:7]
    crop_out = sys.argv[7] if len(sys.argv) > 7 else None
    crop_h = int(sys.argv[8]) if len(sys.argv) > 8 else 1000
    w, h = int(w), int(h)
    shell = os.environ.get("RENDER_SHELL") or (glob.glob(os.path.join(
        os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
        "chromium_headless_shell-*/chrome-linux/headless_shell")) or [None])[0]
    if not shell or not os.access(shell, os.X_OK):
        sys.exit("REFUSED: no executable headless_shell — source seat_env.sh first")

    verdict = {"seat_env": os.environ.get("RENDER_SEAT"), "page": os.path.abspath(src),
               "seat_from_path": os.path.abspath(src).split("/")[2] if os.path.abspath(src).startswith("/sessions/") else None,
               "viewport": [w, h], "theme_requested": theme, "shell": shell,
               "fontconfig_file": os.environ.get("FONTCONFIG_FILE"), "checks": {}, "ok": False}
    t0 = time.time()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell, headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=theme)
        pg = ctx.new_page()
        pg.goto("file://" + os.path.abspath(src))       # never set_content() — drops linked css (#29)
        pg.wait_for_timeout(1200)                         # let CSS entry motion settle
        pg.add_style_tag(content="*{transition:none !important;animation:none !important}")  # settle rule (07-27)
        pg.wait_for_timeout(200)

        got_theme = pg.evaluate("document.documentElement.getAttribute('data-theme')")
        verdict["checks"]["theme"] = {"got": got_theme, "ok": got_theme == theme}

        lay = pg.evaluate("({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,"
                          " sh: document.documentElement.scrollHeight, bg: getComputedStyle(document.body).backgroundColor,"
                          " ink: getComputedStyle(document.body).color, body_ff: getComputedStyle(document.body).fontFamily})")
        verdict["checks"]["layout"] = {"scrollWidth": lay["sw"], "clientWidth": lay["cw"], "ok": lay["sw"] == lay["cw"]}
        verdict["checks"]["body"] = {"background": lay["bg"], "color": lay["ink"], "font_family": lay["body_ff"]}

        fams = [c[0] for c in CANDIDATES]
        widths = pg.evaluate(JS_MEASURE, {"fams": fams, "s": PROBE_STRING, "px": PROBE_PX})
        tgt, dj, none = widths["HSBC_MtUnivers_Latin"], widths["DejaVu Sans"], widths["NoSuchFace-238"]
        a1, a2 = widths["Univers Next HSBC"], widths["Univers Next for HSBC"]
        fonts_ok = (tgt != dj) and (tgt != none) and (a1 == tgt) and (a2 == tgt)
        verdict["checks"]["fonts"] = {
            "probe": f"{PROBE_PX}px '{PROBE_STRING}' canvas measureText",
            "widths": {k: {"px": widths[k], "is": d} for k, d in CANDIDATES},
            "rule": "target != DejaVu && target != nonexistent && both aliases == target",
            "fonts_check_recorded_not_used": pg.evaluate("document.fonts.check('16px HSBC_MtUnivers_Latin')"),
            "ok": fonts_ok}
        # identify the page's own body face by width match against named candidates
        stack_w = widths['"Helvetica Neue",Helvetica,Arial,sans-serif']
        named = {"DejaVu Sans": dj, "Nimbus Sans": widths["Nimbus Sans"], "Liberation Sans": widths["Liberation Sans"],
                 "HSBC_MtUnivers_Latin": tgt}
        matches = [n for n, v in named.items() if v == stack_w]
        verdict["checks"]["page_face"] = {"stack_width": stack_w, "matches": matches,
                                          "identified": matches[0] if len(matches) == 1 else None,
                                          "note": "width-identity against installed candidates; a tie is reported, never guessed"}

        # #217: the first full_page shot reflows — throwaway first, then measure, capture, re-measure.
        pg.screenshot(path=out, full_page=True)
        h1 = pg.evaluate("document.documentElement.scrollHeight")
        pg.screenshot(path=out, full_page=True)
        h2 = pg.evaluate("document.documentElement.scrollHeight")
        verdict["checks"]["reflow"] = {"height_before": h1, "height_after": h2, "ok": h1 == h2}
        if crop_out:
            pg.screenshot(path=crop_out, full_page=True, clip={"x": 0, "y": 0, "width": w, "height": min(crop_h, h2)})
        verdict["png"] = {"path": os.path.abspath(out), "bytes": os.path.getsize(out)}
        verdict["ok"] = all(v.get("ok", True) for v in verdict["checks"].values())
        verdict["seconds"] = round(time.time() - t0, 1)
        print(json.dumps(verdict, indent=1))                 # verdict BEFORE cleanup
        with open(probe_out, "w") as f:
            json.dump(verdict, f, indent=1)
        b.close()
    print("RENDER", "OK" if verdict["ok"] else "FAIL", out)
    sys.exit(0 if verdict["ok"] else 1)


if __name__ == "__main__":
    main()
