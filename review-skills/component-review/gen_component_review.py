#!/usr/bin/env python3
"""
Component review gallery — every reviewed component shown in LIGHT and DARK side by side,
carefully labelled, in the Swiss review idiom. Optional DIFF mode compares two versions
(before/after) so iterative changes are obvious.

Each panel wraps the component's own reviewed snippet markup in its .cn-<slug> scope and
carries its own data-theme, so light and dark resolve correctly on one page against a single
canon.css (canon.css re-declares its aliases on [data-theme], so the theme can live on a div).

Usage
  # all reviewed components, light+dark, from a snippets dir:
  python3 gen_component_review.py --snippets knowledge/snippets --canon knowledge/canon/canon.css \
      --out component-review.html --subject "Canon components" --date 2026-07-14

  # a subset:
  python3 gen_component_review.py --only Button,Accordion,Modals ...

  # DIFF two versions (iterative review): before/ and after/ each a snippets dir:
  python3 gen_component_review.py --diff OLD_SNIPPETS NEW_SNIPPETS ...

Output is one self-contained HTML file (canon.css is INLINED so it shares with no setup).
"""
import os, re, glob, argparse, html as _html, hashlib

# ---------- snippet extraction (shared logic, adapted from gen_gallery.py) ----------

def slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")

def remove_div_by_class(html, cls):
    """Remove <div class="...cls...">...</div> with balanced nesting."""
    out, i = [], 0
    pat = re.compile(r'<div[^>]*class="[^"]*\b' + re.escape(cls) + r'\b[^"]*"[^>]*>')
    while True:
        m = pat.search(html, i)
        if not m: out.append(html[i:]); break
        out.append(html[i:m.start()])
        depth, j = 1, m.end()
        while j < len(html) and depth:
            nd = html.find("<div", j); cd = html.find("</div>", j)
            if cd == -1: break
            if nd != -1 and nd < cd: depth += 1; j = nd + 4
            else: depth -= 1; j = cd + 6
        i = j
    return "".join(out)

def extract_sprite(body):
    m = re.search(r'<svg[^>]*position:absolute[^>]*>.*?</svg>', body, re.S)
    if not m: return body, ""
    return body[:m.start()] + body[m.end():], m.group(0)

def load_snippet(path):
    """Return (body_without_sprite, sprite, symbol_ids)."""
    html = open(path).read()
    mb = re.search(r"<body[^>]*>(.*?)</body>", html, re.S)
    body = mb.group(1) if mb else html
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    body = remove_div_by_class(body, "demo-controls")
    body, sprite = extract_sprite(body)
    ids = set(re.findall(r'<symbol id="([^"]+)"', sprite))
    return body.strip(), sprite, ids

# ---------- id namespacing (so light & dark copies don't collide, sprite refs preserved) ----------

def namespace_ids(body, suffix, protected):
    """Suffix internal ids + their references with `suffix`; leave sprite ids (in `protected`) alone.
    Handles id / for / aria-controls / aria-labelledby / aria-describedby / aria-owns / list /
    href="#.." / xlink:href="#..". aria-* attrs may hold several space-separated ids."""
    def sfx(tok):
        return tok if tok in protected else tok + suffix

    # id="X"
    body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{sfx(m.group(1))}"', body)
    # single-id ref attributes
    for attr in ("for", "list"):
        body = re.sub(rf'\b{attr}="([^"]+)"', lambda m: f'{attr}="{sfx(m.group(1))}"', body)
    # #-prefixed refs (href/xlink:href) — only the fragment
    body = re.sub(r'(\bxlink:href|\bhref)="#([^"]+)"',
                  lambda m: f'{m.group(1)}="#{sfx(m.group(2))}"', body)
    # aria-* id-list attributes (space separated)
    for attr in ("aria-controls", "aria-labelledby", "aria-describedby", "aria-owns", "aria-activedescendant"):
        def repl(m):
            toks = m.group(1).split()
            return f'{attr}="' + " ".join(sfx(t) for t in toks) + '"'
        body = re.sub(rf'\b{attr}="([^"]+)"', repl, body)
    return body

# ---------- reveal script (interactive components shown in a representative state) ----------

REVEAL_JS = r"""
  // reveal interactive components in a representative state for visual review (both themes)
  (function(){
    document.querySelectorAll('.cn-dropdown .menu').forEach(m=>m.setAttribute('data-open','true'));
    document.querySelectorAll('.cn-dropdown .trigger').forEach(t=>t.setAttribute('aria-expanded','true'));
    document.querySelectorAll('.cn-accordion').forEach(acc=>{
      const h=acc.querySelector('.head'); if(h){h.setAttribute('aria-expanded','true');
      const it=h.closest('.item')||acc; const p=it.querySelector('.panel'); if(p)p.style.maxHeight='260px';}});
    document.querySelectorAll('.cn-tabs .tablist').forEach(tl=>{const s=tl.querySelector('[aria-selected="true"]')||tl.querySelector('.tab');
      const ind=tl.querySelector('.indicator'); if(s&&ind){ind.style.left=s.offsetLeft+'px';ind.style.width=s.offsetWidth+'px';ind.style.opacity='1';}});
    document.querySelectorAll('.cn-modals .overlay').forEach(o=>{o.style.cssText+=';position:static;inset:auto;visibility:visible;opacity:1;padding:0;background:transparent;display:block;';
      const d=o.querySelector('.dialog'); if(d){d.style.transform='none';d.style.opacity='1';}});
    document.querySelectorAll('.cn-tooltip .tip').forEach(t=>{t.style.opacity='1';t.style.pointerEvents='auto';});
  })();
"""

# ---------- HTML assembly ----------

def pane(raw_body, ids, theme, cslug, label, ns):
    """Namespace this pane's copy uniquely (component slug + ns) so ids never collide with the
    sibling theme/version OR with an identically-named id in another component."""
    body = namespace_ids(raw_body, f"__{cslug}{ns}", ids)
    return (f'<div class="pane" data-tone="{theme}">'
            f'<div class="plabel">{label}</div>'
            f'<div class="canon frame" data-theme="{theme}">'
            f'<div class="cn-{cslug}">{body}</div>'
            f'</div></div>')

def build(components, canon_css, subject, date, diff=False):
    """components: list of dicts. Non-diff: {name,slug,body,sprite}. Diff: adds before/after bodies + changed flag."""
    # collect all sprite symbols once (union), shared across panes
    symbols = {}
    for c in components:
        for sp in c.get("sprites", []):
            for sm in re.finditer(r'<symbol id="([^"]+)".*?</symbol>', sp, re.S):
                symbols[sm.group(1)] = sm.group(0)
    sprite_block = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
                    + "".join(symbols.values()) + "</svg>") if symbols else ""

    rows = []
    for c in components:
        chip = ""
        if diff:
            chip = ('<span class="chip changed">Changed</span>' if c["changed"]
                    else ('<span class="chip new">New</span>' if c.get("new")
                    else ('<span class="chip gone">Removed</span>' if c.get("gone")
                    else '<span class="chip same">Unchanged</span>')))
        cls = "crow" + (" is-changed" if diff and (c["changed"] or c.get("new") or c.get("gone")) else "")
        head = f'<div class="clabel"><span class="cname">{_html.escape(c["name"])}</span>{chip}</div>'
        if not diff:
            panes = (pane(c["body_raw"], c["ids"], "light", c["slug"], "Light", "__L")
                     + pane(c["body_raw"], c["ids"], "dark", c["slug"], "Dark", "__D"))
            rows.append(f'<section class="{cls}">{head}<div class="panes two">{panes}</div></section>')
        else:
            # 2x2: rows = theme, cols = before/after
            def cell(bodykey, theme, lbl, ns):
                b = c.get(bodykey)
                if b is None:
                    return f'<div class="pane empty" data-tone="{theme}"><div class="plabel">{lbl}</div><div class="frame missing">— not present —</div></div>'
                return pane(b, c["ids"], theme, c["slug"], lbl, ns)
            grid = (cell("before", "light", "Before · Light", "__BL") + cell("after", "light", "After · Light", "__AL")
                    + cell("before", "dark", "Before · Dark", "__BD") + cell("after", "dark", "After · Dark", "__AD"))
            rows.append(f'<section class="{cls}">{head}<div class="panes four">{grid}</div></section>')

    changed_ctl = ('<label class="only"><input type="checkbox" id="onlyChanged"> Show changed only</label>'
                   if diff else '')
    title = ("Component review — <b>changes</b>" if diff else "Component review")

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Component review · {_html.escape(subject)}</title>
<style>
/* ---- inlined canon (drives the component appearance in each themed .frame) ---- */
{canon_css}
</style>
<style>
/* ---- Swiss review chrome (wraps the components; does not touch canon vars) ---- */
:root{{ --accent:#DB0011; --ink:#000; --paper:#fff; --g1:#F3F3F3; --g2:#EDEDED; --g3:#D7D8D6;
  --g6:#767676; --g7:#545454; --amber:#B7791F; --ok:#1a7a4a;
  --rvfont:"Univers Next","Helvetica Neue",Helvetica,Arial,sans-serif; }}
*{{box-sizing:border-box;}}
.rv, .rv *{{}}
body{{margin:0;font-family:var(--rvfont);color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased;}}
.nav{{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:24px;background:var(--paper);
  border-bottom:1px solid var(--g2);height:56px;padding:0 32px;}}
.nav .brand{{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;display:flex;align-items:center;gap:8px;}}
.nav .brand::before{{content:"";width:20px;height:1px;background:var(--accent);}}
.nav .spacer{{flex:1;}}
.nav .only{{font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--g6);display:flex;align-items:center;gap:6px;cursor:pointer;}}
.head{{max-width:1200px;margin:0 auto;padding:40px 32px 8px;}}
.label{{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);display:flex;align-items:center;gap:8px;margin:0 0 12px;}}
.label::before{{content:"";width:20px;height:1px;background:var(--accent);}}
h1{{font-size:32px;line-height:1.14;font-weight:300;margin:0 0 24px;}} h1 b{{font-weight:600;}}
.wrap{{max-width:1200px;margin:0 auto;padding:0 32px 64px;}}
.crow{{border-top:1px solid var(--g2);padding:28px 0;}}
.crow:last-child{{border-bottom:1px solid var(--g2);}}
.clabel{{display:flex;align-items:baseline;gap:12px;margin:0 0 16px;}}
.cname{{font-size:18px;font-weight:600;}}
.chip{{display:inline-block;font-size:11px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;padding:2px 8px;border:1px solid var(--g3);color:var(--g7);}}
.chip.changed{{border-color:var(--accent);color:var(--accent);}}
.chip.new{{border-color:var(--ok);color:var(--ok);}}
.chip.gone{{border-color:var(--g6);color:var(--g6);}}
.chip.same{{border-color:var(--g3);color:var(--g6);}}
.panes{{display:grid;gap:16px;}}
.panes.two{{grid-template-columns:1fr 1fr;}}
.panes.four{{grid-template-columns:1fr 1fr;}}
@media(max-width:820px){{.panes.two,.panes.four{{grid-template-columns:1fr;}}}}
.pane{{border:1px solid var(--g2);}}
.plabel{{font-size:11px;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);
  padding:8px 12px;border-bottom:1px solid var(--g2);background:var(--g1);display:flex;justify-content:space-between;}}
.pane[data-tone="dark"] .plabel::after{{content:"◑";}} .pane[data-tone="light"] .plabel::after{{content:"◐";}}
.frame{{padding:24px;background:var(--page);color:var(--text);font-family:var(--font);min-height:80px;}}
.frame.missing{{color:var(--g6);font-style:italic;display:flex;align-items:center;min-height:80px;}}
.foot{{max-width:1200px;margin:0 auto;padding:32px;border-top:1px solid var(--g2);font-size:13px;color:var(--g6);}}
body.only-changed .crow:not(.is-changed){{display:none;}}
</style></head>
<body>
<nav class="nav">
  <span class="brand">Component review</span>
  <span class="spacer"></span>
  {changed_ctl}
</nav>
<div class="head">
  <p class="label">Component review · {_html.escape(subject)} · {_html.escape(date)}</p>
  <h1>{title} — <b>{_html.escape(subject)}</b></h1>
</div>
<div class="wrap">
  {sprite_block}
  {"".join(rows)}
</div>
<footer class="foot">Component review · generated by the component-review skill · light + dark shown together{' · changed items flagged' if diff else ''}.</footer>
<script>
{REVEAL_JS}
(function(){{
  var cb=document.getElementById('onlyChanged');
  if(cb) cb.addEventListener('change',function(){{document.body.classList.toggle('only-changed',cb.checked);}});
}})();
</script>
</body></html>"""

# ---------- component gathering ----------

CURATED_ORDER = ["Button","List-items","Cards","Headers","Navigations","Notifications","Modals","Input-fields",
 "Progress-tracker","Badge","Links","Tags","Status-indicator","Avatar","Divider","Table","Tabs",
 "Selection-controls","Search-field","Breadcrumbs","Pagination","Accordion","Tooltip","Quick-actions",
 "Dropdown","Hero","Slider","Reorder","Countdown-timer","View-options","Video-player","Loading-indicator"]

def names_in(d):
    return sorted(os.path.basename(p).replace(".reference.html","") for p in glob.glob(os.path.join(d,"*.reference.html")))

def ordered(names):
    return [n for n in CURATED_ORDER if n in names] + [n for n in names if n not in CURATED_ORDER]

def gather_single(snip_dir, only):
    names = names_in(snip_dir)
    if only: names = [n for n in names if n in only]
    comps=[]
    for nm in ordered(names):
        body, sprite, ids = load_snippet(os.path.join(snip_dir, nm+".reference.html"))
        comps.append({"name":nm, "slug":slug(nm), "body_raw":body, "ids":ids, "sprites":[sprite]})
    return comps

def content_hash(body):
    norm = re.sub(r"\s+"," ", body).strip()
    return hashlib.sha1(norm.encode()).hexdigest()

def gather_diff(old_dir, new_dir, only):
    old_n, new_n = names_in(old_dir), names_in(new_dir)
    alln = ordered(sorted(set(old_n)|set(new_n)))
    if only: alln = [n for n in alln if n in only]
    comps=[]
    for nm in alln:
        rec={"name":nm,"slug":slug(nm),"sprites":[],"before":None,"after":None,"ids":set(),
             "changed":False,"new":False,"gone":False}
        hb=ha=None
        if nm in old_n:
            b,sp,ids=load_snippet(os.path.join(old_dir,nm+".reference.html")); rec["before"]=b; rec["sprites"].append(sp); rec["ids"]|=ids; hb=content_hash(b)
        if nm in new_n:
            b,sp,ids=load_snippet(os.path.join(new_dir,nm+".reference.html")); rec["after"]=b; rec["sprites"].append(sp); rec["ids"]|=ids; ha=content_hash(b)
        rec["new"]  = (hb is None and ha is not None)
        rec["gone"] = (ha is None and hb is not None)
        rec["changed"] = (hb is not None and ha is not None and hb!=ha)
        comps.append(rec)
    return comps

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--snippets", default="knowledge/snippets")
    ap.add_argument("--canon", default="knowledge/canon/canon.css")
    ap.add_argument("--out", default="component-review.html")
    ap.add_argument("--subject", default="Canon components")
    ap.add_argument("--date", default="")
    ap.add_argument("--only", default="")
    ap.add_argument("--diff", nargs=2, metavar=("OLD","NEW"), default=None)
    a=ap.parse_args()
    only=set(x.strip() for x in a.only.split(",") if x.strip()) or None
    canon_css=open(a.canon).read()
    if a.diff:
        comps=gather_diff(a.diff[0], a.diff[1], only)
        doc=build(comps, canon_css, a.subject, a.date, diff=True)
        changed=sum(1 for c in comps if c["changed"] or c["new"] or c["gone"])
        print(f"diff review: {len(comps)} components, {changed} changed/new/removed -> {a.out}")
    else:
        comps=gather_single(a.snippets, only)
        doc=build(comps, canon_css, a.subject, a.date, diff=False)
        print(f"review: {len(comps)} components (light+dark) -> {a.out}")
    open(a.out,"w").write(doc)

if __name__=="__main__":
    main()
