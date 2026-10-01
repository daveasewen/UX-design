"""#312 lane L3 — pictures for the cohort-one review page, and the page's own render check.

shots : one small light-theme picture per drafted part, cut from its reference snippet at the draft's own
        root `$sel` (knowledge/components/<id>.meta.json → anatomy.$sel), with the flyout/panel/tip opened
        where the tree names it. Written to notes/_lanes/312/L/img/<id>.png at 2x.
page  : renders notes/_REVIEW-312-L-cohort-one-trees-2026-10-01-v1.html at 1440 and 390, writes
        img/check-1440.png and img/check-390.png, and prints side-scroll, image-load and Copy-as-text facts.

Usage (at the seat, after seat_env.sh; executable_path=$RENDER_SHELL; or in the cloud with no RENDER_SHELL):
  python3 notes/_lanes/312/L/render_312L.py shots|page
"""
import os, sys, json
from playwright.sync_api import sync_playwright

R = os.getcwd()
OUT = "notes/_lanes/312/L/img"
os.makedirs(OUT, exist_ok=True)
PAGE = "notes/_REVIEW-312-L-cohort-one-trees-2026-10-01-v1.html"
IDS = "button tabs table date-picker metric split-button accordion slider selection-controls input-fields dropdown modals tooltip pagination notifications".split()
SNIP = {"button": "Button", "tabs": "Tabs", "table": "Table", "date-picker": "Date-picker", "metric": "Metric",
        "split-button": "Split-button", "accordion": "Accordion", "slider": "Slider",
        "selection-controls": "Selection-controls", "input-fields": "Input-fields", "dropdown": "Dropdown",
        "modals": "Modals", "tooltip": "Tooltip", "pagination": "Pagination", "notifications": "Notifications"}

# The drafts' root selectors as read in the cloud worktree (L2's uncommitted metas); used when the seat's meta
# does not carry `anatomy` yet (the 20:00 commit may land after this render).
ROOTS = {
 "button": "body > div.row > button.btn.primary",
 "tabs": "body > div.tabs",
 "table": "body > div.wrap > div.scroll",
 "date-picker": "body > div.dp",
 "metric": "body > div.board > div.metric",
 "split-button": "body > div.row > div.split-btn.primary",
 "accordion": "body > div.acc",
 "slider": "body > div.field",
 "selection-controls": "body > div.sc",
 "input-fields": "body > div.field",
 "dropdown": "body > div.row > div > div.dd",
 "modals": "body > div.overlay",
 "tooltip": "body > div.row > span.lbl > span.tip-wrap",
 "pagination": "body > nav.pg",
 "notifications": "body > div.nwrap > div.note.tint.err"
}

# Per part: what to open before the shot (JS), which extra boxes join the root's box, and an optional
# override of the box to shoot (the modal's root is the full-viewport overlay; the dialog is the picture).
PREP = {
    "date-picker": dict(js="document.querySelector('.dp .tail-btn').click()", extra=[".dp .dp-panel.is-open"]),
    "split-button": dict(js="document.querySelector('.split-btn .sb-caret').click()", extra=[".split-btn .sb-menu[data-open='true']"]),
    "dropdown": dict(js="document.querySelector('.dd .trigger').click()", extra=[".dd .menu"]),
    "modals": dict(js="document.getElementById('open').click()", shoot=".overlay .dialog", wait=500),
    "tooltip": dict(hover=".tip-wrap .trigger", shoot="body > div.row > span.lbl", extra=[".tip.show"]),
    "accordion": dict(js="(function(){var h=document.querySelectorAll('.acc .head');if(h[0]&&h[0].getAttribute('aria-expanded')!=='true')h[0].click();})()"),
}
# A second picture for the family root: the switch rows, which Dave's word names.
SECOND = {"selection-controls": ("selection-controls-switch", ".sc .field:has(input[role='switch'])")}

UNION = """(sels)=>{let b=null;let root=null;
  for(const s of sels){let els;
    if(s.startsWith('body > ')){root=document.querySelector(s);els=root?[root]:[];}
    else els=[...(root||document).querySelectorAll(s)];
    for(const e of els){const r=e.getBoundingClientRect();
      if(r.width===0&&r.height===0)continue;const x=r.left+scrollX,y=r.top+scrollY,x2=x+r.width,y2=y+r.height;
      b=b?[Math.min(b[0],x),Math.min(b[1],y),Math.max(b[2],x2),Math.max(b[3],y2)]:[x,y,x2,y2];}}
  return b;}"""

ISOLATE = """(s)=>{const r=document.querySelector(s);if(!r)return;for(const e of document.body.querySelectorAll('*')){
  if(e===r||r.contains(e)||e.contains(r))continue;e.style.visibility='hidden';}}"""

def launch(p):
    ex = os.environ.get("RENDER_SHELL")
    return p.chromium.launch(executable_path=ex) if ex else p.chromium.launch()

def shot(pg, sels, path, pad=14, top=8):
    b = pg.evaluate(UNION, sels)
    if not b:
        return None
    x, y, x2, y2 = b
    clip = {"x": max(0, x - pad), "y": max(0, y - top), "width": (x2 - x) + 2 * pad, "height": (y2 - y) + top + pad}
    pg.screenshot(path=path, clip=clip, full_page=True)
    return clip

def shots():
    facts = {}
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": 1100, "height": 900}, device_scale_factor=2)
        for i in IDS:
            meta = json.load(open(f"knowledge/components/{i}.meta.json"))
            root = meta.get("anatomy", {}).get("$sel") or ROOTS[i]
            pg.goto(f"file://{R}/knowledge/snippets/{SNIP[i]}.reference.html")
            pg.wait_for_timeout(350)
            pg.evaluate("document.body.setAttribute('data-theme','light')")
            cfg = PREP.get(i, {})
            if cfg.get("hover"):
                pg.hover(cfg["hover"])
            if cfg.get("js"):
                pg.evaluate(cfg["js"])
            pg.wait_for_timeout(cfg.get("wait", 250))
            sels = ([cfg["shoot"]] if cfg.get("shoot") else [root]) + cfg.get("extra", [])
            # hide everything that is neither the pictured element, inside it, nor an ancestor of it
            pg.evaluate(ISOLATE, sels[0])
            # the root `$sel` is a path from body; the first match is the drafted instance
            first = pg.evaluate("(s)=>!!document.querySelector(s)", root)
            clip = shot(pg, sels, f"{OUT}/{i}.png")
            facts[i] = {"root": root, "root_found": first, "sels": sels, "clip": clip}
            print(i, "root found" if first else "ROOT MISSING", clip)
            if i in SECOND:
                name, sel = SECOND[i]
                c2 = shot(pg, [sel], f"{OUT}/{name}.png")
                facts[name] = {"sels": [sel], "clip": c2}
                print(name, c2)
        b.close()
    json.dump(facts, open(f"{OUT}/facts-shots.json", "w"), indent=1)

CHECK = """()=>{const imgs=[...document.images];
  return {scrollWidth:document.documentElement.scrollWidth, clientWidth:document.documentElement.clientWidth,
    images:imgs.length, broken:imgs.filter(i=>!(i.complete&&i.naturalWidth>0)).map(i=>i.getAttribute('src')),
    calls:document.querySelectorAll('.call').length, chips:document.querySelectorAll('.chip').length,
    wide:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>document.documentElement.clientWidth+1).slice(0,8).map(e=>e.tagName.toLowerCase()+'.'+String(e.className).split(' ')[0])};}"""

def page():
    facts = {}
    with sync_playwright() as p:
        b = launch(p)
        for w in (1440, 390):
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto(f"file://{R}/{PAGE}")
            pg.wait_for_timeout(800)
            f = pg.evaluate(CHECK)
            # Copy as text must return every call: answer one, read the text, then clear the trial answer
            f["text_lines"] = pg.evaluate("()=>window.__reviewText().split('\\n').length")
            f["text_has_every_call"] = pg.evaluate("""()=>{const t=window.__reviewText();
              return [...document.querySelectorAll('.call')].every(c=>c.dataset.id==='page'? t.indexOf('Note on the page')>=0 : t.indexOf(c.dataset.q)>=0);}""")
            f["side_scroll"] = f["scrollWidth"] - f["clientWidth"]
            pg.screenshot(path=f"{OUT}/check-{w}.png", full_page=True)
            facts[w] = f
            print(w, json.dumps(f))
            pg.close()
        b.close()
    json.dump(facts, open(f"{OUT}/facts-page.json", "w"), indent=1)

if __name__ == "__main__":
    {"shots": shots, "page": page}[sys.argv[1]]()
