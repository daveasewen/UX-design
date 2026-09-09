import json, os, glob, pathlib
from playwright.sync_api import sync_playwright

REPO = "/sessions/practical-ecstatic-johnson/mnt/UX-design"
PAGE = "file://" + REPO + "/notes/_PROPOSED-263.html"
SHOT = REPO + "/notes/_subreports/assets/2026-09-09-265-D-drive-proposed-263"
pathlib.Path(SHOT).mkdir(parents=True, exist_ok=True)
EXE = glob.glob(os.path.expanduser("/var/tmp/pw-browsers-265/chromium_headless_shell-*/chrome-linux/headless_shell"))[0]
R = {}
console = []

def snap(pg, name, full=True):
    p = SHOT + "/" + name + ".png"
    pg.screenshot(path=p, full_page=full)
    return p

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE)

    # ---- (e)(a)(b)(c) desktop light ----
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, color_scheme="light")
    pg = ctx.new_page()
    pg.on("console", lambda m: console.append(m.type + ": " + m.text))
    pg.on("pageerror", lambda e: console.append("pageerror: " + str(e)))
    pg.goto(PAGE); pg.wait_for_timeout(400)
    R["boot_tally"] = pg.inner_text("#tallyN")
    R["boot_sRuled"] = pg.inner_text("#sRuled")
    R["boot_localStorage"] = pg.evaluate("localStorage.getItem('apollo-proposed-263')")
    snap(pg, "01-boot-light-1280")

    # (c) export with nothing ruled
    pg.click("#exportBtn"); pg.wait_for_timeout(120)
    R["export_empty"] = pg.inner_text("#out")

    # (a) rule three rows + a note
    pg.click("#P-01 button.rb[data-v='ACCEPT']")
    pg.click("#P-02 button.rb[data-v='REJECT']")
    pg.click("#P-03 button.rb[data-v='LATER']")
    pg.fill("#P-01 input.note", "ink seat, confirmed")
    pg.wait_for_timeout(150)
    R["after3_tally"] = pg.inner_text("#tallyN")
    R["after3_sRuled"] = pg.inner_text("#sRuled")
    R["after3_ls"] = pg.evaluate("localStorage.getItem('apollo-proposed-263')")
    R["after3_aria_P01"] = pg.eval_on_selector_all(
        "#P-01 button.rb", "els=>els.map(e=>e.dataset.v+'='+e.getAttribute('aria-checked'))")
    R["after3_dataruled"] = pg.eval_on_selector_all(
        "article.card", "els=>els.map(e=>e.id+':'+e.getAttribute('data-ruled'))")
    pg.click("#exportBtn"); pg.wait_for_timeout(120)
    R["export_after3"] = pg.inner_text("#out")
    snap(pg, "02-three-ruled-export-light")

    # (a) reload — persistence
    pg.reload(); pg.wait_for_timeout(400)
    R["reload_tally"] = pg.inner_text("#tallyN")
    R["reload_sRuled"] = pg.inner_text("#sRuled")
    R["reload_aria_P01"] = pg.eval_on_selector_all(
        "#P-01 button.rb", "els=>els.map(e=>e.dataset.v+'='+e.getAttribute('aria-checked'))")
    R["reload_note_P01"] = pg.input_value("#P-01 input.note")
    R["reload_out_text"] = pg.inner_text("#out")
    snap(pg, "03-after-reload-light")

    # toggle-off behaviour + full 11 export
    pg.click("#P-01 button.rb[data-v='ACCEPT']"); pg.wait_for_timeout(100)
    R["unset_tally"] = pg.inner_text("#tallyN")
    pg.click("#P-01 button.rb[data-v='ACCEPT']"); pg.wait_for_timeout(100)
    for i in range(4, 12):
        pg.click("#P-%02d button.rb[data-v='ACCEPT']" % i)
    pg.wait_for_timeout(200)
    R["all11_tally"] = pg.inner_text("#tallyN")
    pg.click("#exportBtn"); pg.wait_for_timeout(120)
    R["export_all11"] = pg.inner_text("#out")
    snap(pg, "04-all-eleven-export-light")

    # decide-only toggle
    pg.check("#decide"); pg.wait_for_timeout(200)
    R["decide_bodyclass"] = pg.evaluate("document.body.className")
    R["decide_cbody_visible"] = pg.eval_on_selector("#P-01 .cbody", "e=>e.offsetHeight>0")
    snap(pg, "05-decide-only-light")
    pg.uncheck("#decide")

    # clear all
    pg.click("#clearBtn"); pg.wait_for_timeout(150)
    R["clear_tally"] = pg.inner_text("#tallyN")
    R["clear_out"] = pg.inner_text("#out")
    R["clear_ls"] = pg.evaluate("localStorage.getItem('apollo-proposed-263')")
    ctx.close()

    # ---- (d) 44px targets at <=760px ----
    for w in (760, 375):
        ctx = b.new_context(viewport={"width": w, "height": 900}, color_scheme="light")
        pg = ctx.new_page()
        pg.on("console", lambda m: console.append("[%d] " % w + m.type + ": " + m.text))
        pg.on("pageerror", lambda e: console.append("[%d] pageerror: " % w + str(e)))
        pg.goto(PAGE); pg.wait_for_timeout(400)
        R["boxes_%d" % w] = pg.evaluate("""() => {
          const out = {};
          const m = (sel) => Array.from(document.querySelectorAll(sel)).map(e=>{
            const r = e.getBoundingClientRect();
            return {t:(e.textContent||'').trim().slice(0,18), w:+r.width.toFixed(1), h:+r.height.toFixed(1)};
          });
          out.rb = m('article.card button.rb');
          out.bar = m('.bar button, .bar label.tog, .bar input#decide');
          out.note = m('input.note');
          out.scrollW = document.documentElement.scrollWidth;
          out.clientW = document.documentElement.clientWidth;
          return out;
        }""")
        snap(pg, "06-viewport-%d-light" % w)
        ctx.close()

    # ---- (f) dark, both viewports ----
    for w, tag in ((1280, "1280"), (375, "375")):
        ctx = b.new_context(viewport={"width": w, "height": 900}, color_scheme="dark")
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: console.append("[dark] pageerror: " + str(e)))
        pg.goto(PAGE); pg.wait_for_timeout(400)
        R["dark_%s_bg" % tag] = pg.evaluate(
            "getComputedStyle(document.body).backgroundColor + ' | ink ' + getComputedStyle(document.body).color")
        R["dark_%s_accent" % tag] = pg.evaluate(
            "getComputedStyle(document.querySelector('.eyebrow')).color")
        if w == 1280:
            pg.click("#P-01 button.rb[data-v='ACCEPT']"); pg.wait_for_timeout(150)
            R["dark_selected_border"] = pg.eval_on_selector(
                "#P-01 button.rb[data-v='ACCEPT']", "e=>getComputedStyle(e).borderColor")
            R["dark_attr_theme_bg"] = pg.evaluate(
                "document.documentElement.setAttribute('data-theme','dark'); getComputedStyle(document.body).backgroundColor")
        snap(pg, "07-dark-%s" % tag)
        ctx.close()

    b.close()

R["console"] = console
print(json.dumps(R, indent=1))
