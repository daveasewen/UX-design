#!/usr/bin/env python3
"""#292 / P4 — render deck v13 and MEASURE the new map card (10A).

Self-contained at this seat: it generates its own fontconfig farm in $TMPDIR
(the stored outputs/_render-env-23x farms are foreign-seat symlinks and resolve
0/10 here — the runbook's eighth stratum), finds the playwright headless shell,
and never trusts a stored absolute path by name.

Writes into notes/_lanes/292/P4/:
  s10.png          slide 10, the card BEFORE the insertion point
  s10map.png       slide 10A, the NEW card
  s11.png          slide 11, the card AFTER it (the ask) — unchanged
  s10map-dark.png  the new card under prefers-color-scheme: dark
  contact.png      all 13 cards in one strip, so the count is visible
  measured.json    counts, index, page errors, clipping

Run (one bash call):
  cd <repo> && export TMPDIR=/dev/shm
  python3 notes/_lanes/292/P4/shoot.py
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
V12 = os.path.join(ROOT, "notes", "_DEMO-SLIDES-apollo-2026-09-20-v12.html")
V13 = os.path.join(ROOT, "notes", "_DEMO-SLIDES-apollo-2026-09-21-v13.html")

# ---------------------------------------------------------------- font farm
def seat_fonts():
    """Per-seat fontconfig, generated in THIS call. Returns (conf, faces)."""
    tmp = os.environ.get("TMPDIR", "/tmp")
    d = os.path.join(tmp, "p4-fonts")
    cache = os.path.join(d, "cache")
    os.makedirs(cache, exist_ok=True)
    ttf = os.path.join(ROOT, "knowledge", "assets", "fonts", "_desktop", "TTF")
    faces = [f for f in glob.glob(os.path.join(ttf, "*.ttf")) if os.path.exists(f)]
    conf = os.path.join(d, "fonts.conf")
    with open(conf, "w") as f:
        f.write("<?xml version='1.0'?><!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>\n"
                "<fontconfig><cachedir>%s</cachedir><dir>%s</dir>"
                "<include ignore_missing='yes'>/etc/fonts/conf.d</include>"
                "<dir>/usr/share/fonts</dir></fontconfig>\n" % (cache, ttf))
    return conf, len(faces)


def shell_path():
    pats = [os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/"
                               "chrome-headless-shell-linux-*/chrome-headless-shell"),
            os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome")]
    for p in pats:
        hits = sorted(glob.glob(p))
        if hits:
            return hits[-1]
    return None


CONF, FACES = seat_fonts()
os.environ["FONTCONFIG_FILE"] = CONF
syslib = os.path.join(ROOT, "outputs", "syslibs", "usr", "lib", "aarch64-linux-gnu")
os.environ["LD_LIBRARY_PATH"] = syslib + ":" + os.environ.get("LD_LIBRARY_PATH", "")

from playwright.sync_api import sync_playwright  # noqa: E402

SHELL = shell_path()
if not SHELL:
    sys.exit("SHOOT: FAIL no headless shell found under ~/.cache/ms-playwright")

# ------------------------------------------------------------------- probe
PROBE = r"""() => {
  const o = {};
  const S = [...document.querySelectorAll('section.slide')];
  o.sectionSlideBlocks = S.length;
  o.slideIds = S.map(s => s.id);
  o.pagenums = S.map(s => { const p = s.querySelector('.pagenum'); return p ? p.textContent.trim() : null; });
  o.numberedSlides = o.pagenums.filter(Boolean).length;
  o.newIndex0 = o.slideIds.indexOf('s10map');
  o.newIndex1 = o.newIndex0 + 1;

  const sec = document.getElementById('s10map');
  const R = el => { const b = el.getBoundingClientRect();
    return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1)}; };
  const sr = sec.getBoundingClientRect();
  const inner = sec.querySelector('.inner').getBoundingClientRect();
  o.card = {slide: R(sec), inner: R(sec.querySelector('.inner'))};

  // 1 · does the CARD clip? (scroll overflow of the section itself)
  o.cardScrollOverY = Math.max(0, sec.scrollHeight - Math.ceil(sr.height));
  o.cardScrollOverX = Math.max(0, sec.scrollWidth  - Math.ceil(sr.width));
  o.innerOutsideCardPx = +Math.max(0, sr.top - inner.top, inner.bottom - sr.bottom).toFixed(1);

  // 2 · does any CONTENT spill past its tile's content box?
  //     overflow is `visible` everywhere in this card by design, so a spill is
  //     geometric, not a scrollHeight: last child's ink vs the padding box.
  const spill = [];
  [...sec.querySelectorAll('.dsm > *')].forEach(t => {
    const cs = getComputedStyle(t), b = t.getBoundingClientRect();
    const padT=parseFloat(cs.paddingTop), padB=parseFloat(cs.paddingBottom);
    const padL=parseFloat(cs.paddingLeft), padR=parseFloat(cs.paddingRight);
    const boxT=b.top+padT, boxB=b.bottom-padB, boxL=b.left+padL, boxR=b.right-padR;
    let over = {bottom:0, top:0, left:0, right:0};
    [...t.children].forEach(c => {
      if (c.classList.contains('tick')) return;           // the tick IS the edge
      const walk = el => {
        const r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return;
        over.bottom = Math.max(over.bottom, r.bottom - boxB);
        over.top    = Math.max(over.top,    boxT - r.top);
        over.left   = Math.max(over.left,   boxL - r.left);
        over.right  = Math.max(over.right,  r.right - boxR);
        [...el.children].forEach(walk);
      };
      walk(c);
    });
    const worst = Math.max(over.bottom, over.top, over.left, over.right);
    spill.push({cls: t.className.toString().slice(0,24),
                box: {w:+b.width.toFixed(1), h:+b.height.toFixed(1)},
                overPx: +worst.toFixed(1),
                scrollOver: Math.max(0, t.scrollHeight - t.clientHeight)});
  });
  o.tiles = spill;
  o.tileCount = spill.length;
  o.maxTileSpillPx = +Math.max(...spill.map(t => t.overPx)).toFixed(1);
  o.clippedPx = Math.max(0, o.cardScrollOverY, o.cardScrollOverX,
                         o.innerOutsideCardPx, o.maxTileSpillPx);

  // 3 · no ink under the ticks, and the grid is 4x4
  const g = getComputedStyle(sec.querySelector('.dsm'));
  o.grid = {cols: g.gridTemplateColumns.split(' ').length,
            rows: g.gridTemplateRows.split(' ').length, gap: g.gap};
  o.hub = R(sec.querySelector('.hub'));
  o.states = [...sec.querySelectorAll('.tile')].map(t => t.dataset.state);
  o.soonCount = o.states.filter(s => s === 'soon').length;
  o.srcCount = sec.querySelectorAll('.src').length;
  o.badgeCount = sec.querySelectorAll('.badge').length;
  o.pagenum = sec.querySelector('.pagenum').textContent.trim();
  o.headline = sec.querySelector('h2').textContent.trim();
  // font actually resolved for the card
  o.cardFont = getComputedStyle(sec.querySelector('h2')).fontFamily;
  const c = document.createElement('canvas').getContext('2d');
  o.faceProbe = {};
  ['"Univers Next"','HSBC_MtUnivers_Latin','"Helvetica Neue"','nonexistent-xyz'].forEach(f => {
    c.font = '40px ' + f; o.faceProbe[f] = +c.measureText('Handgloves 12345').width.toFixed(2);
  });
  return o;
}"""


def count_file(path):
    src = open(path, encoding="utf-8").read()
    return {"lines": src.count("\n"),
            "section_class_slide_occurrences": src.count('<section class="slide'),
            "pagenum_blocks": src.count('class="pagenum"')}


def main():
    out = {"v12": count_file(V12), "v13": count_file(V13),
           "shell": SHELL, "fontFaces": FACES, "fontconfig": CONF}
    errs = {"light": [], "dark": []}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=SHELL, args=["--no-sandbox"])
        for mode in ("light", "dark"):
            pg = b.new_page(viewport={"width": 1440, "height": 900},
                            device_scale_factor=2, color_scheme=mode)
            pg.on("pageerror", lambda e, m=mode: errs[m].append(str(e)))
            pg.on("console", lambda msg, m=mode: errs[m].append("console:" + msg.text)
                  if msg.type == "error" else None)
            pg.goto("file://" + V13, wait_until="load")
            pg.wait_for_timeout(3200)
            pg.eval_on_selector("#s10map", "e => e.scrollIntoView()")
            pg.wait_for_timeout(1600)
            out["measured_" + mode] = pg.evaluate(PROBE)
            if mode == "light":
                for sid in ("s10", "s10map", "s11"):
                    pg.eval_on_selector("#" + sid, "e => e.scrollIntoView()")
                    pg.wait_for_timeout(1400)
                    pg.locator("#" + sid).screenshot(path=os.path.join(HERE, sid + ".png"))
                # contact strip — every card, small, in order
                ids = out["measured_light"]["slideIds"]
                for i, sid in enumerate(ids):
                    pg.eval_on_selector("#" + sid, "e => e.scrollIntoView()")
                    pg.wait_for_timeout(700)
                    pg.locator("#" + sid).screenshot(
                        path=os.path.join(HERE, "_c%02d.png" % i))
            else:
                pg.locator("#s10map").screenshot(path=os.path.join(HERE, "s10map-dark.png"))
            pg.close()
        b.close()
    out["pageErrors"] = errs
    out["pageErrorCount"] = len(errs["light"]) + len(errs["dark"])

    # contact strip, 4 across
    try:
        from PIL import Image
        tiles = sorted(glob.glob(os.path.join(HERE, "_c*.png")))
        ims = [Image.open(t) for t in tiles]
        tw, th = 360, 225
        ims = [im.resize((tw, th)) for im in ims]
        cols, pad = 4, 10
        rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols*tw + (cols+1)*pad, rows*th + (rows+1)*pad), (100, 100, 100))
        for i, im in enumerate(ims):
            r, c = divmod(i, cols)
            sheet.paste(im, (pad + c*(tw+pad), pad + r*(th+pad)))
        sheet.save(os.path.join(HERE, "contact.png"))
        out["contact"] = {"cards": len(ims), "cols": cols, "rows": rows}
        for t in tiles:
            os.remove(t)
    except Exception as e:
        print("CONTACT STRIP NOT WRITTEN: %s" % e, file=sys.stderr)

    with open(os.path.join(HERE, "measured.json"), "w") as f:
        json.dump(out, f, indent=1)
    slim = {k: v for k, v in out.items() if not k.startswith("measured_")}
    slim["light"] = {k: v for k, v in out["measured_light"].items() if k != "tiles"}
    slim["dark_clippedPx"] = out["measured_dark"]["clippedPx"]
    slim["light_worst_tiles"] = sorted(out["measured_light"]["tiles"],
                                       key=lambda t: -t["overPx"])[:4]
    print(json.dumps(slim, indent=1))


if __name__ == "__main__":
    main()
