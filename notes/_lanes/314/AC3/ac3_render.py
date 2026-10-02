"""#314 AC3 - seat renders for Dave's second look at the templates and the parts lane TP2 changed.
Real face (seat fontconfig), file:// only, no keyboard focus (nothing is focused or tabbed).
Run from the repo root at the seat after ensure_env + seat_env:
  python3 notes/_lanes/314/AC3/ac3_render.py templates|report|parts-after|parts-before [names...]
Writes JPEG (q80, <=1280 wide) to notes/_lanes/314/AC3/renders/ and facts to renders/_facts-<group>.json.
parts-before reads a 3c717370 copy at /tmp/ac3-before (git archive of snippets, canon, logos, icons)."""
import io, json, os, sys, time
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = os.getcwd(); HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "renders")
os.makedirs(OUT, exist_ok=True)
TEMPLATES = ["auth", "confirmation", "create-edit", "dashboard", "dashboard-bento", "detail", "empty", "error", "list-index", "report", "settings"]
PARTS = ["Page-header-lockup", "Summary", "Timeline", "Metric", "Form-layout", "Segmented-control", "Stepper", "Empty-state", "Action-bar", "Confirmation", "Anchor-nav", "Input-fields", "Dropdown"]
NOANIM = "*{transition:none!important;animation:none!important;caret-color:transparent!important}"
FACTS = """()=>{const b=document.body,cs=getComputedStyle(b);
 const ff=[...document.querySelectorAll('h1,h2,p,button,label')].slice(0,6).map(e=>getComputedStyle(e).fontFamily.split(',')[0]);
 return {w:document.documentElement.scrollWidth,h:document.documentElement.scrollHeight,font:ff,
  loaded:[...new Set([...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family))].slice(0,4),
  overflowX:document.documentElement.scrollWidth>window.innerWidth,
  zero:[...document.querySelectorAll('[class^="cn-"],[class*=" cn-"]')].filter(e=>{const r=e.getBoundingClientRect();return r.width===0||r.height===0}).length}}"""

def save(png, name):
    im = Image.open(io.BytesIO(png)).convert("RGB")
    if im.width > 1280:
        im = im.resize((1280, round(im.height * 1280 / im.width)))
    im.save(os.path.join(OUT, name + ".jpg"), "JPEG", quality=80, optimize=True)

def shot(pg, path, mode, w, name):
    pg.set_viewport_size({"width": w, "height": 900}); pg.goto("about:blank")
    pg.goto("file://" + path, wait_until="load"); pg.wait_for_timeout(500)
    pg.evaluate("(m)=>{document.body.setAttribute('data-theme',m);}", mode)
    pg.add_style_tag(content=NOANIM)
    try: pg.evaluate("()=>document.fonts.ready.then(()=>1)")
    except Exception: pass
    pg.evaluate("()=>{if(document.activeElement)document.activeElement.blur();window.scrollTo(0,0)}")
    pg.wait_for_timeout(250)
    f = pg.evaluate(FACTS)
    save(pg.screenshot(full_page=True), name)
    return f

def main(group, names):
    t0 = time.time(); facts = {}
    jobs = []
    if group == "templates":
        for t in (names or TEMPLATES):
            for m in ("light", "dark"):
                jobs.append((os.path.join(ROOT, "knowledge/snippets/Template-%s.reference.html" % t), m, 1280, "template-%s-after-%s-1280" % (t, m)))
    elif group == "report":
        for w in (1440, 1024, 768, 390):
            jobs.append((os.path.join(ROOT, "knowledge/snippets/Template-report.reference.html"), "light", w, "template-report-after-light-%d" % w))
    elif group in ("parts-after", "parts-before"):
        base = ROOT if group == "parts-after" else "/tmp/ac3-before"
        tag = group.split("-")[1]
        for p in (names or PARTS):
            for m in ("light", "dark"):
                jobs.append((os.path.join(base, "knowledge/snippets/%s.reference.html" % p), m, 1280, "part-%s-%s-%s" % (p.lower(), tag, m)))
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ["RENDER_SHELL"], args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1, reduced_motion="reduce")
        for path, m, w, name in jobs:
            try: facts[name] = shot(pg, path, m, w, name)
            except Exception as e: facts[name] = {"err": str(e)[:200]}
        b.close()
    fp = os.path.join(OUT, "_facts-%s.json" % group)
    old = json.load(open(fp)) if os.path.exists(fp) else {}
    old.update(facts); json.dump(old, open(fp, "w"), indent=1)
    for k, v in facts.items():
        print(k, v.get("err") or "w%s h%s ox%s zero%s font=%s" % (v["w"], v["h"], v["overflowX"], v["zero"], sorted(set(v["font"]))[:3]))
    print(len(facts), "shots", round(time.time() - t0), "s")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
