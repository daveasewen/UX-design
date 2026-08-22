#!/usr/bin/env python3
"""Render-verify + drive knowledge/_fitness-test/bento-gallery-showcase-v1.html.

Homed in-repo per s191-D2 (a throwaway on a sub's outputs mount would have to be declared
NON-REPO; this one does not).

Follows _RUNBOOK-render-verify.md:
  - canvas width probe against TWO CONTROLS, never document.fonts.check() (which cannot fail)
  - env vars re-exported by the caller in EVERY bash call
  - chunked with --stage so no single call approaches the 45 s wall
  - the verdict prints BEFORE any teardown

It does three things a screenshot cannot:
  1. VAR RESOLUTION across 4 themes x light/dark -- every page-local custom property must resolve
     to a non-empty value, because a dangling var renders silent black and no gate sees it.
  2. DRIVES the lightbox by CLICKING the invoker button (not by calling showPopover()), so the
     command/commandfor attribute is what is under test, not the popover API.
  3. Measures the crop that object-fit:cover actually performs, so the aspect-ratio trade-off is a
     number rather than an impression.
"""
import glob, json, os, sys

REPO = "/sessions/busy-clever-rubin/mnt/UX-design"
PAGE = "file://" + REPO + "/knowledge/_fitness-test/bento-gallery-showcase-v1.html"
OUT = "/sessions/busy-clever-rubin/mnt/outputs"
THEMES = ["mono", "legacy", "console", "supercharge"]

LOCAL_VARS = ["--page", "--surface", "--surface-2", "--surface-3", "--line", "--line-2",
              "--ink", "--ink-2", "--focus", "--focus-w", "--radius", "--radius-ctl",
              "--gutter", "--margin", "--tap"]


def launch(p):
    sh = glob.glob(os.environ["PLAYWRIGHT_BROWSERS_PATH"] + "/chromium_headless_shell-*/chrome-linux/headless_shell")
    return p.chromium.launch(executable_path=sh[0], headless=True,
                             args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])


FONT_PROBE = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return c.measureText('Handgloves 12345').width; };
  return { target: m('HSBC_MtUnivers_Latin'),
           uf: m('"Univers Next HSBC"'),
           ctrl_dejavu: m('"DejaVu Sans"'),
           ctrl_missing: m('"NoSuchFaceAnywhere"') };
}"""

VAR_PROBE = """(names) => {
  const el = document.querySelector('.bgx');
  const cs = getComputedStyle(el);
  const out = {};
  for (const n of names) out[n] = cs.getPropertyValue(n).trim();
  // also the three things a dangling var would blank
  const tile = document.querySelector('.bx-tile');
  const ts = getComputedStyle(tile);
  out['$body-bg'] = getComputedStyle(document.body).backgroundColor;
  out['$body-ink'] = getComputedStyle(document.body).color;
  out['$tile-bg'] = ts.backgroundColor;
  out['$tile-border'] = ts.borderTopColor;
  out['$tile-radius'] = ts.borderTopLeftRadius;
  return out;
}"""


def stage_probe(pg):
    """Numeric assertions. Returns (ok, report)."""
    rep, ok = [], True

    f = pg.evaluate(FONT_PROBE)
    font_ok = (round(f["target"], 2) == round(f["uf"], 2)
               and abs(f["target"] - f["ctrl_dejavu"]) > 1
               and abs(f["target"] - f["ctrl_missing"]) > 1)
    ok &= font_ok
    rep.append("FONT   %s target=%.2f uf=%.2f dejavu=%.2f missing=%.2f"
               % ("PASS" if font_ok else "FAIL", f["target"], f["uf"], f["ctrl_dejavu"], f["ctrl_missing"]))

    # capability badges, measured
    caps = pg.evaluate("""() => ({
        command: 'command' in HTMLButtonElement.prototype,
        popover: HTMLElement.prototype.hasOwnProperty('popover'),
        masonry: CSS.supports('grid-template-rows','masonry')})""")
    rep.append("CAPS   command=%s popover=%s nativeMasonry=%s" % (caps["command"], caps["popover"], caps["masonry"]))
    ok &= caps["command"] and caps["popover"]

    # var resolution across 4 themes x light/dark
    for th in THEMES:
        for mode in ("light", "dark"):
            pg.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);"
                        "document.documentElement.setAttribute('data-theme',m);}", [th, mode])
            pg.wait_for_timeout(90)
            v = pg.evaluate(VAR_PROBE, LOCAL_VARS)
            empty = [k for k in LOCAL_VARS if not v[k]]
            same = v["$body-bg"] == v["$tile-bg"]
            flat_ink = v["$body-ink"] == v["$body-bg"]
            bad = bool(empty) or flat_ink
            ok &= not bad
            rep.append("VARS   %-11s %-5s %s empty=%s bodybg=%s tilebg=%s%s border=%s r=%s ink=%s"
                       % (th, mode, "PASS" if not bad else "FAIL", empty or "none",
                          v["$body-bg"], v["$tile-bg"], "  <-- SAME AS PAGE" if same else "",
                          v["$tile-border"], v["$tile-radius"], v["$body-ink"]))

    pg.evaluate("()=>{document.documentElement.setAttribute('data-apollo-theme','mono');"
                "document.documentElement.setAttribute('data-theme','light');}")

    # DRIVE the lightbox via the invoker button -- the clause under test is command/commandfor
    lb = pg.locator("#lb-3")
    before = pg.evaluate("()=>document.getElementById('lb-3').matches(':popover-open')")
    pg.locator('button[commandfor="lb-3"]').first.click()
    pg.wait_for_timeout(280)
    during = pg.evaluate("()=>document.getElementById('lb-3').matches(':popover-open')")
    pg.locator('#lb-3 button[command="hide-popover"]').click()
    pg.wait_for_timeout(280)
    after = pg.evaluate("()=>document.getElementById('lb-3').matches(':popover-open')")
    lb_ok = (before is False and during is True and after is False)
    ok &= lb_ok
    rep.append("LIGHTBOX %s closed=%s -> opened-by-command=%s -> closed-by-command=%s"
               % ("PASS" if lb_ok else "FAIL", before, during, after))

    # negative control: a button whose commandfor points nowhere must NOT open anything
    ctrl = pg.evaluate("""() => {
      const b = document.createElement('button');
      b.setAttribute('command','show-popover'); b.setAttribute('commandfor','lb-does-not-exist');
      document.body.appendChild(b); b.click();
      const n = document.querySelectorAll(':popover-open').length; b.remove(); return n; }""")
    ok &= (ctrl == 0)
    rep.append("NEGCTRL %s dangling commandfor opened %d popover(s) (expect 0)"
               % ("PASS" if ctrl == 0 else "FAIL", ctrl))

    # object-fit:cover crop, measured -- the aspect-ratio trade-off as a number
    pg.evaluate("()=>{const g=document.getElementById('glMain');g.setAttribute('data-mode','grid');"
                "g.setAttribute('data-aspect','1/1');g.style.setProperty('--gl-ar','1/1');}")
    pg.wait_for_timeout(200)
    crop = pg.evaluate("""() => {
      const out = [];
      for (const sel of ['lb-3','lb-8','lb-9']) {}
      document.querySelectorAll('#glMain .gl-img').forEach((im,i) => {
        const r = im.getBoundingClientRect();
        const nat = im.naturalWidth / im.naturalHeight;
        const box = r.width / r.height;
        const visible = nat > box ? (box/nat) : (nat/box);
        out.push({n:i+1, alt:im.alt, nat:+nat.toFixed(3), box:+box.toFixed(3),
                  kept:+(visible*100).toFixed(1)});
      });
      return out; }""")
    worst = min(crop, key=lambda c: c["kept"])
    rep.append("CROP@1:1 worst=%s keeps %.1f%% of the frame; median kept=%.1f%%"
               % (worst["alt"], worst["kept"],
                  sorted(c["kept"] for c in crop)[len(crop)//2]))
    rep.append("CROP@1:1 detail=" + json.dumps(crop))

    # horizontal overflow, both modes, at this viewport
    for mode in ("masonry", "grid"):
        pg.evaluate("(m)=>document.getElementById('glMain').setAttribute('data-mode',m)", mode)
        pg.wait_for_timeout(150)
        ov = pg.evaluate("()=>document.documentElement.scrollWidth - document.documentElement.clientWidth")
        ok &= (ov <= 0)
        rep.append("OVERFLOW %s %-8s horizontal overflow = %dpx" % ("PASS" if ov <= 0 else "FAIL", mode, ov))

    return ok, rep


def shoot(pg, name, theme, mode, width, actions=None, clip_sel=None):
    """Theme and mode are set by CLICKING the real controls, not by setting the attribute.
    Driving the thing is the point: an attribute poke would leave the chrome's aria-pressed
    state stale and the screenshot would misreport which theme it is showing."""
    pg.set_viewport_size({"width": width, "height": 1100})
    pg.locator('#rvTheme button[data-v="%s"]' % theme).click()
    pg.locator('#rvDark button[data-v="%s"]' % mode).click()
    pg.wait_for_timeout(120)
    if actions:
        actions(pg)
    pg.wait_for_timeout(450)
    if clip_sel:
        el = pg.locator(clip_sel).first
        el.scroll_into_view_if_needed()
        pg.wait_for_timeout(250)
    pg.screenshot(path=os.path.join(OUT, name + ".png"))
    return name


def main():
    from playwright.sync_api import sync_playwright
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": 1400, "height": 1100})
        pg.goto(PAGE)
        pg.wait_for_timeout(900)

        if stage in ("probe", "all"):
            ok, rep = stage_probe(pg)
            print("\n".join(rep))
            print("\nVERDICT: " + ("ALL NUMERIC CHECKS PASS" if ok else "*** SOMETHING FAILED ***"))

        if stage in ("shots-a", "all"):
            for th in THEMES:
                shoot(pg, "bg-%s-light-bento" % th, th, "light", 1400, clip_sel="#bxGrid")

        if stage in ("shots-b", "all"):
            shoot(pg, "bg-mono-dark-bento", "mono", "dark", 1400, clip_sel="#bxGrid")
            shoot(pg, "bg-supercharge-dark-gallery", "supercharge", "dark", 1400,
                  actions=lambda q: q.evaluate("()=>document.getElementById('glMain').setAttribute('data-mode','masonry')"),
                  clip_sel="#glMain")
            shoot(pg, "bg-mono-light-gallery-grid-1x1", "mono", "light", 1400,
                  actions=lambda q: q.evaluate("()=>{const g=document.getElementById('glMain');"
                                               "g.setAttribute('data-mode','grid');g.setAttribute('data-aspect','1/1');"
                                               "g.style.setProperty('--gl-ar','1/1');}"),
                  clip_sel="#glMain")

        if stage in ("shots-c", "all"):
            # narrow: BOTH a narrow viewport and the stage-width harness
            shoot(pg, "bg-narrow-420-viewport", "console", "light", 420, clip_sel="#bxGrid")
            def stage380(q):
                q.set_viewport_size({"width": 1400, "height": 1100})
                q.evaluate("()=>{const s=document.getElementById('stage');"
                           "s.style.setProperty('--rv-stage-w','380px');s.setAttribute('data-framed','yes');}")
            shoot(pg, "bg-stage380-harness", "legacy", "light", 1400, actions=stage380, clip_sel="#bxGrid")
            # lightbox OPEN, driven by the command attribute
            def openlb(q):
                q.evaluate("()=>{const s=document.getElementById('stage');"
                           "s.style.removeProperty('--rv-stage-w');s.setAttribute('data-framed','no');}")
                q.locator('button[commandfor="lb-9"]').first.click()
            shoot(pg, "bg-lightbox-open-portrait", "mono", "light", 1400, actions=openlb)
            def openlb2(q):
                q.keyboard.press("Escape")
                q.wait_for_timeout(200)
                q.locator('button[commandfor="lb-8"]').first.click()
            shoot(pg, "bg-lightbox-open-dark-console", "console", "dark", 1400, actions=openlb2)

        print("SHOTS: " + " ".join(sorted(os.path.basename(f) for f in glob.glob(OUT + "/bg-*.png"))))
        b.close()


if __name__ == "__main__":
    main()
