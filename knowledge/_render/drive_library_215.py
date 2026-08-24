#!/usr/bin/env python3
"""drive_library_215.py — the headless drive for showroom/index.html (Library v2, s215-D4/D5).

Run from the repo root with the render env exported (knowledge/_RUNBOOK-render-verify.md):
  python3 knowledge/_render/drive_library_215.py [showroom/index.html]
33 checks: tabs, search + aliases, cmd-K, status facet, thumbnails decoded, related links,
the #chrome=0 embed contract, the theme broadcast, and (added at the #215 Swiss restyle)
the three Swiss contract checks BB/CC/DD. Exits non-zero on any red.

⚠ TWO ASSERTIONS CHANGED AT THE #215 SWISS RESTYLE, both STYLING-COUPLED, neither weakened:
  A and M read #rc with inner_text, which returns the RENDERED text — the result line is now
  a Swiss caption with `text-transform:uppercase`, so the same string arrives as
  "135 OF 135 SHOWN". Both now compare `.lower()`; the exact count string is still asserted
  character for character. (Driven: before the change they went red, 28/30 — that red was the
  restyle showing up in the drive, not a functional break.)

DRIVEN RED 2026-08-22 (the check that proves the check): a single thumbnail path corrupted
in showroom/index.html took check Q from green to red, 29/30. Restored by regeneration.

WARNING - TWO POTHOLES BANKED HERE, 30s of timeout each, 2026-08-22:
  * page.click("body") at 1500x950 lands INSIDE the card gallery and opens a component.
    It is not a neutral click any more - press keys with keyboard.press instead.
  * the gallery is a nested scroller ~6000px deep and playwright's auto-scroll does not
    reach into it (the card resolves, then "element is not visible" forever). Narrow with
    the search box first, then click.

⛔ THREE TYPED CONSTANTS REMOVED 2026-08-24 (#218) — all three were ALREADY RED at this seat
before #218 touched anything, and each was red for the same reason: a fact about the library was
typed here instead of read from the library.
  · the REPO path was the absolute mount of the session that wrote this file, so the drive died
    with ERR_FILE_NOT_FOUND at every later seat. Derived from `__file__` now.
  · the ROW COUNT ("135 of 135 shown", and 135 again in checks I and O) predated #217's
    Foundations tier. Read from `showroom/index.json` now — the string is still asserted
    character for character, the number just is not typed.
  · the TIER LADDER was the five #215 tiers and #217 drew a sixth. Derived the way the page
    derives it: the tiers in LEVELS order that actually have a row.
And the screenshot path was a fixed `/var/tmp` file, which a foreign session already owned —
PermissionError AFTER all 33 checks ran, the whole drive lost to a shot. `LIB_SHOT` overrides it.
DRIVEN 2026-08-24 after the change: 33/33 green.

REPO HOME per s191-D2: the working copy lives at /var/tmp during a session; THIS is the
canonical copy. Copy it out, never retype it.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import sys, json, os
from playwright.sync_api import sync_playwright
# ⛔ #218 — DERIVED FROM THIS FILE, never typed. What was here was the absolute path of the
# SESSION THAT WROTE IT (`/sessions/sweet-blissful-albattani/mnt/UX-design`), so the drive could
# only ever run at that one seat and died with ERR_FILE_NOT_FOUND everywhere else — an instrument
# in the repo that no later session can re-drive is a claim, not an instrument (s191-D2's whole
# point). The mount name changes every session; the file's position in the tree does not.
REPO=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
URL="file://"+REPO+"/"+(sys.argv[1] if len(sys.argv)>1 else "showroom/index.html")
# ⛔ AND THE COUNT COMES FROM THE ARTEFACT. It was typed as "135 of 135 shown", so the check went
# red the moment the library gained a row — #218 added four and it did. The number the result line
# must print is the number of rows the index actually ships.
_IDX=os.path.join(REPO,"showroom","index.json")
_I=json.load(open(_IDX,encoding="utf-8")) if os.path.exists(_IDX) else {"components":[],"$levels":[]}
_N=len(_I["components"])
# ⛔ AND THE LADDER COMES FROM THE ARTEFACT TOO. It was typed as the five #215 tiers, so it went
# red the moment #217 filled the Foundations rung — a tier with members is DRAWN, and the check
# was asserting a word-set from before that. Derived here the way the page derives it: the tiers
# in LEVELS order that actually have a row. A drawn rung is now proof, not a surprise.
_LADDER=[lv["label"] for lv in _I.get("$levels",[])
         if any(c["level"]==lv["key"] for c in _I["components"])]
res=[]
def ck(n,g,w): res.append((g==w,n,g,w))
with sync_playwright() as p:
    b=p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--allow-file-access-from-files"])
    pg=b.new_page(viewport={"width":1500,"height":950})
    errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(700)
    ck("A · full count at load", pg.inner_text("#rc").lower(), "%d of %d shown"%(_N,_N))
    ck("B · Type tab is the default", pg.get_attribute("#tab-type","aria-selected"), "true")
    ck("C · Type tab draws the ruled ladder",
       pg.eval_on_selector_all("#tree-type summary","e=>e.map(x=>x.firstChild.textContent)"),
       _LADDER)
    ck("D · Pattern definition visible on Type tab",
       "assembly" in pg.inner_text("#tabnote-type") and pg.locator("#tabnote-type").is_visible(), True)
    ck("E · Usage tree hidden while Type is selected", pg.locator("#tree-usage").is_visible(), False)
    pg.click("#tab-usage"); pg.wait_for_timeout(250)
    ck("F · tab switch shows the Usage tree", pg.locator("#tree-usage").is_visible(), True)
    ck("G · tab switch hides the Type tree", pg.locator("#tree-type").is_visible(), False)
    ck("H · Usage groups are task groups",
       pg.eval_on_selector_all("#tree-usage summary","e=>e.map(x=>x.firstChild.textContent)"),
       ["Actions","Forms and input","Navigation","Feedback and status","Data display",
        "Content and media","Commerce and money","Structure and layout"])
    ck("I · every component appears exactly once in each tree",
       [pg.eval_on_selector_all("#tree-type a[data-slug]","e=>e.length"),
        pg.eval_on_selector_all("#tree-usage a[data-slug]","e=>e.length")], [_N,_N])
    pg.click("#tab-type"); pg.wait_for_timeout(200)
    # search + aliases
    pg.fill("#q","spinner"); pg.wait_for_timeout(250)
    vis=pg.eval_on_selector_all("#tree-type a[data-slug]:not([hidden])","e=>e.map(x=>x.dataset.slug)")
    ck("J · alias 'spinner' -> loading-indicator", vis, ["loading-indicator"])
    ck("K · matched alias is shown on the row",
       "spinner" in pg.eval_on_selector("#tree-type a[data-slug='loading-indicator'] .why","e=>e.textContent"), True)
    ck("L · the gallery filters with the search",
       pg.eval_on_selector_all(".card:not([hidden])","e=>e.map(x=>x.dataset.slug)"), ["loading-indicator"])
    pg.click("#qclear"); pg.wait_for_timeout(250)
    ck("M · clear restores", pg.inner_text("#rc").lower(), "%d of %d shown"%(_N,_N))
    # cmd-K
    pg.keyboard.press("Control+k"); pg.wait_for_timeout(150)
    ck("N · cmd/ctrl-K focuses the search box", pg.evaluate("document.activeElement.id"), "q")
    pg.keyboard.press("Escape")
    # status facet
    pg.click(".chip[data-status='beta']"); pg.wait_for_timeout(250)
    nb=int(pg.inner_text("#rc").split()[0])
    ck("O · status facet filters to beta only",
       (0<nb<_N, sorted(set(pg.eval_on_selector_all(".card:not([hidden]) .pill","e=>e.map(x=>x.dataset.status)")))),
       (True, ["beta"]))
    ck("P · the status facet filters INSIDE the tab too",
       pg.eval_on_selector_all("#tree-type a[data-slug]:not([hidden])","e=>e.length"), nb)
    pg.click("#reset"); pg.wait_for_timeout(250)
    # THUMBNAILS — every card image must actually have decoded
    pg.evaluate("()=>document.querySelectorAll('.card .shot').forEach(i=>i.loading='eager')")
    pg.wait_for_timeout(500)
    pg.evaluate("()=>{const g=document.getElementById('gallery'); g.scrollTop=g.scrollHeight;}")
    pg.wait_for_timeout(2500)
    bad=pg.evaluate("()=>Array.from(document.querySelectorAll('.card')).filter(c=>{const i=c.querySelector('img.shot'); return !i || !i.complete || i.naturalWidth===0;}).map(c=>c.dataset.slug)")
    ck("Q · every card thumbnail decoded (naturalWidth>0)", bad, [])
    ck("R · thumbnails are the small size", pg.evaluate("()=>{const i=document.querySelector('.card img.shot'); return [i.naturalWidth,i.naturalHeight];}"), [320,200])
    # related
    # narrow first, then click — the gallery is a nested scroller 6000px deep and
    # playwright's auto-scroll does not reach into it reliably
    pg.evaluate("()=>{document.getElementById('gallery').scrollTop=0;}")
    pg.fill("#q","dropdown"); pg.wait_for_timeout(400)
    pg.click(".card[data-slug='dropdown']"); pg.wait_for_timeout(1600)
    pg.fill("#q",""); pg.wait_for_timeout(200)
    rel=pg.eval_on_selector_all("#rel a","e=>e.map(x=>x.dataset.slug)")
    ck("S · related components surface on the open component", sorted(rel),
       ["cascader","combobox","multi-select","selection-controls"])
    ck("T · each related link carries a one-line disambiguation",
       all(len(t)>10 for t in pg.eval_on_selector_all("#rel a","e=>e.map(x=>x.title)")), True)
    pg.click("#rel a[data-slug='combobox']"); pg.wait_for_timeout(1500)
    ck("U · a related link opens that component", pg.inner_text("#now"), "Combobox")
    # embed contract still intact
    fr=pg.frame_locator("#vframe")
    ck("V · second bar hidden (chrome=0)", fr.locator("header").is_visible(), False)
    ck("W · review overlay GONE in the library view", fr.frame_locator("#f").locator("#rv-fab").count(), 0)
    ck("X · component mounted live", fr.frame_locator("#f").locator("body").count(), 1)
    for th in ["legacy","console","supercharge","mono"]:
        pg.click("#themes button[data-theme='%s']"%th); pg.wait_for_timeout(700)
        got=pg.frame_locator("#vframe").frame_locator("#f").locator("html").get_attribute("data-apollo-theme")
        ck("Y · theme reaches pane: %s"%th, got, th)
    pg.click("#all"); pg.wait_for_timeout(400)
    ck("Z · back to the gallery", pg.locator("#gallery").is_visible(), True)
    ck("AA · no page errors", errs, [])
    # ---- #215 SWISS RESTYLE, driven in the browser (computed styles, not source text) ----
    ck("BB · active tab is underlined in the accent #DA1A00 (two-red law s151-D1)",
       pg.evaluate("()=>getComputedStyle(document.getElementById('tab-type')).borderBottomColor"),
       "rgb(218, 26, 0)")
    ck("CC · Swiss: nothing in the chrome is rounded or shadowed",
       pg.evaluate("""()=>{const bad=[];
         document.querySelectorAll('.card,.chip,.pill,.btn,.seg,.seg button,#q,.cardgrid,header.app,nav.tree')
           .forEach(e=>{const c=getComputedStyle(e);
             if(parseFloat(c.borderTopLeftRadius)>0) bad.push(e.className+':radius');
             if(c.boxShadow!=='none') bad.push(e.className+':shadow');});
         return bad.slice(0,6);}"""), [])
    ck("DD · the label pattern draws a 20px accent dash before an uppercase eyebrow",
       pg.evaluate("""()=>{const l=document.querySelector('.gallery .label');
         const b=getComputedStyle(l,'::before'); const s=getComputedStyle(l);
         return [b.backgroundColor,b.width,s.textTransform,s.color];}"""),
       ["rgb(218, 26, 0)", "20px", "uppercase", "rgb(218, 26, 0)"])
    # ⛔ #218 — OVERRIDABLE, and it is the same shared-/var/tmp class as the mutant dirs. This was
    # a fixed /var/tmp path: the file already existed, owned by the session that first ran this,
    # and every later session died on PermissionError AFTER all 33 checks had run — the whole
    # drive lost to a screenshot. /var/tmp is shared; a fixed path in it is a foreign artefact
    # waiting to happen. Pass LIB_SHOT to put it somewhere this session owns.
    pg.screenshot(path=os.environ.get("LIB_SHOT", "/var/tmp/library-215-gallery.png"))
    b.close()
bad=[r for r in res if not r[0]]
for ok,n,g,w in res: print(("  ✅ " if ok else "  ❌ ")+n+("" if ok else "\n       got %r want %r"%(g,w)))
print("DRIVE: %d/%d green"%(len(res)-len(bad),len(res)))
sys.exit(1 if bad else 0)
