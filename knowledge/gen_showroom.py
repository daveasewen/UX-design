#!/usr/bin/env python3
"""
gen_showroom.py — the generated, browsable component library (RULED, Dave 2026-07-21).

One separate file per component + one master categorised index (showroom/), assembled
FROM the canon (snippets + tokens + the theme cascade stay the gated source) so it
cannot rot. reviews/ is demoted to scratch; THIS is the human-navigable library.

Each component page is the UNIVERSAL REVIEW HARNESS (build-out Phase 0), ONE BAR
(#98-D1, Dave 2026-08-05 — controls consolidated, snippet sources are pure canon):
  * title · details · theme seg (all four [data-apollo-theme] slots, ADR-0011;
    Console/Supercharge render as Mono where their override sets are empty, labelled)
  * light/dark TOGGLE driving ONE pane (replaces the side-by-side spread)
  * responsive width slider · ↻ Replay (disabled where the snippet has no
    `dv-animate` motion idiom) · Open ↗ (theme × mode baked into a standalone doc)
  * the snippet's own live variant/state spread inside the pane

Mechanism: the reference snippet document is embedded VERBATIM (base64) with TWO
generated additions — (1) the per-snippet theme CSS from gen_theme_cascade.snippet_theme_css()
(the [data-apollo-theme] re-projection of its own manifest vars); (2) the REVIEW OVERLAY
(single source of truth: _review/_review-overlay.html, same block _make_review.py injects)
so every pane — and every Open-↗ standalone doc — carries comment pins + export-to-prompt.
rv-file points at the CLEAN snippet source (edits land there, then regenerate). The overlay
rides the PANES only; index.html carries none (Dave, 2026-07-22). Panes render in
same-origin srcdoc iframes; the chrome sets html[data-apollo-theme] + body[data-theme].

Deterministic (no timestamps) so `--check` can verify the showroom regenerates
byte-identically — wired into _build_all.py like every other generated surface.

Usage:
  python3 knowledge/gen_showroom.py            # write showroom/
  python3 knowledge/gen_showroom.py --check    # verify in sync (build gate)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import base64, glob, html as htmlmod, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNIP = os.path.join(HERE, "snippets")
OUTD = os.path.join(ROOT, "showroom")
sys.path.insert(0, os.path.join(HERE, "canon"))
import gen_theme_cascade as cascade

MANIFEST_RE = re.compile(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', re.S)
OVERLAY_PATH = os.path.join(HERE, "_review", "_review-overlay.html")
OVERLAY_MARK = "<!-- APOLLO-REVIEW-OVERLAY -->"

# ---------------------------------------------------------------------------
# URL REBASE + GATE (2026-07-27) — the srcdoc base-URL trap.
#
# The payload is the snippet VERBATIM, and it is handed to the pane iframe via
# `srcdoc`. A srcdoc document has NO URL of its own: per spec it inherits the
# base URL of the PARENT document — i.e. `showroom/<Component>.html`. So every
# relative URL inside the snippet silently re-resolves one directory tree away.
#
# OBSERVED 2026-07-27 (render, computed styles): all 49 snippets carrying
# `<link rel="stylesheet" href="../canon/type.css">` resolved it to
# `<repo>/canon/type.css` — a path that does not exist — so type.css 404'd in
# EVERY showroom pane and every `.t-cm-*` composite + selector binding in it was
# inert. Chart legend labels measured 16px/400 against the canon 12px/500; the
# Reset button was the only correct one in the pane because its snippet CSS
# hard-codes `font-size:12px`. The failure is SILENT — a 404 stylesheet renders
# as "type looks a bit off", never as an error.
#
# ⚠ ANTI-FALSE-FIX: do NOT "simplify" this to injecting `<base href=...>`. A
# <base> element also re-bases FRAGMENT-only URLs, which would break every inline
# icon-sprite reference (`<use href="#ic-*">`) in the library — trading a type
# outage for an icon outage. Rewriting the URLs themselves is the narrow fix.
#
# The GATE is the second half and the part that matters: a rebased URL whose
# target does not exist FAILS THE BUILD. That gates the condition (a payload URL
# the harness cannot resolve), not this one instance of it.
# ---------------------------------------------------------------------------
URL_ATTR_RE = re.compile(r'\b(href|src)="([^"]+)"')
SKIP_URL_RE = re.compile(r'^(#|/|data:|https?:|mailto:|tel:|//)')

def rebase_payload_urls(payload, snippet_path):
    """Re-point the snippet's relative URLs so they resolve from showroom/.

    Returns (payload, [(original, rebased)]). Raises SystemExit on a rebased
    URL whose target is missing — the build gate."""
    src_dir = os.path.dirname(os.path.abspath(snippet_path))
    rewrites, missing = [], []

    def sub(m):
        attr, url = m.group(1), m.group(2)
        if SKIP_URL_RE.match(url):
            return m.group(0)
        path = re.split(r'[?#]', url, 1)[0]
        suffix = url[len(path):]                     # keep ?query / #fragment intact
        target = os.path.normpath(os.path.join(src_dir, path))
        if not os.path.exists(target):
            missing.append((url, target))
            return m.group(0)
        rebased = os.path.relpath(target, OUTD).replace(os.sep, "/") + suffix
        if rebased == url:
            return m.group(0)
        rewrites.append((url, rebased))
        return '%s="%s"' % (attr, rebased)

    out = URL_ATTR_RE.sub(sub, payload)
    if missing:
        print("gen_showroom GATE — payload URL does not resolve in %s:"
              % os.path.basename(snippet_path))
        for url, target in missing:
            print("   %-40s -> %s (MISSING)" % (url, target))
        print("   A relative URL in a snippet must point at a real file: the showroom\n"
              "   pane re-resolves it against showroom/ (srcdoc inherits the parent base URL).")
        sys.exit(1)
    return out, rewrites

def overlay_block(label, rv_file):
    """The review overlay + its rv-* meta, exactly as _make_review.py stamps it.
    rv-file names the CLEAN snippet source so exported prompts route edits there."""
    with open(OVERLAY_PATH) as fh:
        overlay = fh.read()
    return ('<meta name="rv-doc" content="%s">\n<meta name="rv-file" content="%s">\n%s\n%s'
            % (htmlmod.escape(label, quote=True), rv_file, OVERLAY_MARK, overlay))

# ---------------------------------------------------------------- catalogue
# slug -> category (editable judgment map; unlisted slugs land in 'More').
CATEGORIES = [
    ("Actions",           ["button", "icon-button", "action-bar", "quick-actions", "links"]),
    ("Forms and input",   ["input-fields", "search-field", "selection-controls", "slider",
                           "dropdown", "reorder", "view-options", "segmented-control",
                           # Phase-2 wave 1 (worker A + Account-selector from B's lane)
                           # + wave 2 A-continuation (registered by the CONDUCTOR from receipts —
                           # workers never edit this file):
                           "form-layout", "amount-input", "textarea", "secure-entry",
                           "account-selector", "date-picker", "date-range-picker",
                           "time-picker", "file-upload", "stepper",
                           # Wave 3b, #203 (conductor-registered):
                           "combobox", "multi-select", "tags-input"]),
    ("Navigation",        ["navigations", "breadcrumbs", "pagination", "tabs", "tab-bar",
                           # Wave 3b, #203 (conductor-registered):
                           "command-palette", "sidebar-nav", "anchor-nav"]),
    ("Feedback and status", ["notifications", "status-indicator", "badge", "loading-indicator",
                           "progress-tracker", "tooltip", "confirmation", "modals",
                           "countdown-timer",
                           # Phase-2 wave 1 (worker B — an Overlays split is queued for Dave):
                           "alert", "toast", "banner", "skeleton-loader", "empty-state",
                           "drawer", "popover", "modal-lightbox"]),
    ("Data and content",  ["table", "cards", "list-items", "account-card", "amount-display",
                           "summary", "accordion",
                           # Phase-2 wave 1 (worker B) + wave 2 (worker C):
                           "stat-card", "data-grid",
                           # Wave 3b, #203 (conductor-registered):
                           "kpi-tile", "timeline", "avatar-group"]),
    ("Identity and display", ["avatar", "tags", "eyebrow", "headers", "hero", "divider",
                           "video-player"]),
    # Phase-2 wave 2 (worker D's lane; bucket cut by the conductor — provisional-agent
    # pending Dave's dataviz sign-off):
    ("Charts",            ["chart-bar", "chart-line", "chart-donut", "chart-sparkline",
                           # chart-expansion programme, prove-one-then-wave exemplar (2026-07-22):
                           "chart-scatter",
                           # chart-revisit wave, net-new bar+line-overlay combo (2026-07-24):
                           "chart-combo",
                           # chart wave 2 (2026-08-05, #95 — 3 Sonnet lanes, conductor-registered):
                           "chart-butterfly-h", "chart-butterfly-v", "chart-histogram",
                           "chart-boxplot", "chart-bullet", "chart-candlestick",
                           "chart-pie", "chart-stacked-area"]),
]
CAT_OF = {slug: cat for cat, slugs in CATEGORIES for slug in slugs}

def slug_of(fname):
    return re.sub(r'[^a-z0-9]+', '-',
                  os.path.basename(fname).replace('.reference.html', '').lower()).strip('-')

def label_of(slug):
    return slug.replace("-", " ").capitalize()

# ---------------------------------------------------------------- chrome CSS/JS
CHROME_CSS = """
  :root{--ink:#1A1A1A; --page:#FAFAFA; --line:#E1E1E1; --mid:#808080; --dark:#1A1A1A;}
  *{box-sizing:border-box;}
  body{margin:0; font-family:"Univers Next for HSBC","Helvetica Neue",Arial,Helvetica,sans-serif;
    background:var(--page); color:var(--ink); -webkit-font-smoothing:antialiased;}
  header{display:flex; gap:16px; align-items:center; flex-wrap:wrap; padding:16px 24px;
    background:#FFFFFF; border-bottom:1px solid var(--line); position:sticky; top:0; z-index:5;}
  header h1{font-size:18px; font-weight:500; margin:0 16px 0 0;}
  header>button{font:inherit; font-size:13px; padding:8px 14px; border:1px solid var(--line);
    background:#FFFFFF; color:var(--ink); cursor:pointer;}
  header>button:hover:not(:disabled){border-color:var(--ink);}
  header>button:disabled{color:var(--mid); cursor:default; opacity:.5;}
  header>button:focus-visible{outline:2px solid #305A85; outline-offset:2px;}
  .seg{display:inline-flex; border:1px solid var(--ink);}
  .seg button{font:inherit; font-size:13px; padding:8px 14px; border:0; background:transparent;
    color:var(--ink); cursor:pointer; border-right:1px solid var(--line);}
  .seg button:last-child{border-right:0;}
  .seg button[aria-pressed="true"]{background:var(--ink); color:#FFFFFF;}
  .seg button:focus-visible{outline:2px solid #305A85; outline-offset:2px;}
  .note{font-size:12px; color:var(--mid);}
  .wctl{display:flex; gap:8px; align-items:center; font-size:13px;}
  .wctl input[type=range]{width:180px; accent-color:var(--ink);}
  main{padding:24px;}
  .frame{border:1px solid var(--line); background:#FFFFFF; overflow:auto; resize:vertical; height:82vh;}
  .frame.dark{background:var(--dark);}
  .frame iframe{display:block; width:100%; height:100%; border:0; margin:0 auto;}
"""

PAGE_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__LABEL__ · Apollo showroom</title>
<style>__CSS__</style>
</head>
<body>
<header>
  <h1>__LABEL__</h1>
  <span class="note" id="meta">__META__</span>
  <div class="seg" id="themes" role="group" aria-label="Theme">__THEME_BTNS__</div>
  <div class="seg" id="modes" role="group" aria-label="Light or dark">
    <button data-mode="light" aria-pressed="true">Light</button>
    <button data-mode="dark" aria-pressed="false">Dark</button>
  </div>
  <div class="wctl"><label for="w">Width</label>
    <input id="w" type="range" min="320" max="1600" step="20" value="1600">
    <span id="wv">full</span></div>
  <button id="replay" type="button"__REPLAY_ATTR__>↻ Replay</button>
  <button id="open" type="button">Open ↗</button>
  <span class="note" id="themenote"></span>
</header>
<main>
  <div class="frame light" id="frame"><iframe id="f" title="__LABEL__"></iframe></div>
</main>
<script id="payload" type="application/octet-stream">__B64__</script>
<script>
(function(){
  var THEMES=__THEMES_JSON__;                       // [{attr,label,hits,note}]
  var b64=document.getElementById('payload').textContent.trim();
  var src=new TextDecoder().decode(Uint8Array.from(atob(b64),function(c){return c.charCodeAt(0)}));
  var f=document.getElementById('f'), frameBox=document.getElementById('frame');
  var state={theme:'mono',mode:'light',w:null};

  function hash(){ var h={}; location.hash.replace(/^#/,'').split('&').forEach(function(kv){
      var p=kv.split('='); if(p[0]) h[p[0]]=decodeURIComponent(p[1]||''); }); return h; }
  function setHash(){ var parts=['theme='+state.theme,'m='+state.mode];
    if(state.w) parts.push('w='+state.w);
    history.replaceState(null,'','#'+parts.join('&')); }

  function apply(){
    try{
      var d=f.contentDocument; if(!d||!d.documentElement) return;
      d.documentElement.setAttribute('data-apollo-theme',state.theme);
      if(d.body) d.body.setAttribute('data-theme',state.mode);
    }catch(e){}
    frameBox.className='frame '+state.mode;
    var t=THEMES.find(function(x){return x.attr===state.theme});
    document.getElementById('themenote').textContent=t&&t.note?t.note:'';
    document.querySelectorAll('#themes button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.theme===state.theme)); });
    document.querySelectorAll('#modes button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.mode===state.mode)); });
    setHash(); }

  f.addEventListener('load',apply);
  f.srcdoc=src;

  document.getElementById('themes').addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    state.theme=b.dataset.theme; apply();
  });
  document.getElementById('modes').addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    state.mode=b.dataset.mode; apply();
  });

  var w=document.getElementById('w'), wv=document.getElementById('wv');
  function setW(){ var full=(+w.value>=1600); state.w=full?null:+w.value;
    f.style.width=full?'100%':w.value+'px';
    wv.textContent=full?'full':w.value+'px'; setHash(); }
  w.addEventListener('input',setW);

  document.getElementById('replay').addEventListener('click',function(){
    try{
      var d=f.contentDocument; if(!d) return;
      d.querySelectorAll('.dv-animate, figure.dv').forEach(function(el){
        el.classList.remove('dv-animate'); void el.offsetWidth; el.classList.add('dv-animate'); });
      // second idiom (ds-029): direct `animation:` + @keyframes, no dv-animate class
      // to toggle — restart per-element by forcing the animation off then back on.
      d.querySelectorAll('*').forEach(function(el){
        var cs = d.defaultView.getComputedStyle(el);
        if (cs.animationName && cs.animationName !== 'none') {
          var prev = el.style.animation;
          // getBoundingClientRect(), not offsetWidth: offsetWidth is undefined on
          // SVGElement (HTMLElement-only per CSSOM View), so on a bare <svg> the
          // reflow never flushed and the none->prev toggle silently no-opped.
          // getBoundingClientRect() is defined on Element and forces layout for
          // both HTML and SVG.
          el.style.animation = 'none'; void el.getBoundingClientRect(); el.style.animation = prev || '';
        }
      });
    }catch(e){}
  });

  document.getElementById('open').addEventListener('click',function(){
    var doc=src.replace(/(<body[^>]*data-theme=")[a-z]+(")/,'$1'+state.mode+'$2')
               .replace(/<html/,'<html data-apollo-theme="'+state.theme+'" ');
    window.open(URL.createObjectURL(new Blob([doc],{type:'text/html'})));
  });

  function initFromHash(){ var h=hash();
    if(h.theme&&THEMES.some(function(t){return t.attr===h.theme})) state.theme=h.theme;
    if(h.m==='light'||h.m==='dark') state.mode=h.m;
    if(h.w){ w.value=h.w; setW(); }
    apply(); }
  window.addEventListener('hashchange',initFromHash);
  initFromHash();
})();
</script>
</body>
</html>
"""

INDEX_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Apollo component library · showroom</title>
<style>__CSS__
  .count{display:inline-flex; align-items:baseline; gap:8px; font-size:13px; color:var(--mid);}
  .count strong{font-size:40px; font-weight:300; line-height:1; color:var(--ink);
    font-variant-numeric:tabular-nums; letter-spacing:-1px;}
  .shell{display:grid; grid-template-columns:260px 1fr; min-height:calc(100vh - 57px);}
  nav.tree{border-right:1px solid var(--line); background:#FFFFFF; padding:12px 0 24px;
    overflow-y:auto; position:sticky; top:57px; height:calc(100vh - 57px);}
  nav.tree details{border-bottom:1px solid var(--line);}
  nav.tree summary{font-size:13px; font-weight:500; color:var(--ink); padding:10px 16px;
    cursor:pointer; list-style:none; display:flex; align-items:baseline; gap:8px;}
  nav.tree summary::-webkit-details-marker{display:none;}
  nav.tree summary::before{content:"▸"; font-size:10px; color:var(--mid); transition:transform 140ms;}
  nav.tree details[open] summary::before{transform:rotate(90deg);}
  nav.tree summary .c{margin-left:auto; font-size:11px; color:var(--mid);
    font-variant-numeric:tabular-nums;}
  nav.tree a{display:block; font-size:13px; color:var(--ink); text-decoration:none;
    padding:6px 16px 6px 34px; border-left:2px solid transparent;}
  nav.tree a:hover{background:var(--wash, #F4F4F4);}
  nav.tree a[aria-current="true"]{border-left-color:var(--ink); font-weight:500;
    background:var(--wash, #F4F4F4);}
  main.view{min-width:0; display:flex; flex-direction:column;}
  .view iframe{display:none; border:0; width:100%; flex:1;}
  .view.on iframe{display:block;}
  .view.on .intro{display:none;}
  .intro{padding:24px 24px 0; max-width:820px;}
  .intro p{font-size:14px; color:var(--mid); line-height:1.5; margin:4px 0 0;}
  @media (max-width:760px){
    .shell{grid-template-columns:1fr; align-content:start;}
    nav.tree{position:static; height:auto; max-height:40vh;}
  }
</style>
</head>
<body>
<header>
  <h1>Apollo component library</h1>
  <span class="count" aria-label="__COUNT__ components"><strong>__COUNT__</strong> components</span>
  <span class="note">Every control lives on the component page's one bar (#98-D1).</span>
</header>
<div class="shell">
<nav class="tree" aria-label="Components">
__SECTIONS__
</nav>
<main class="view" id="view">
  <div class="intro">
    <p>Generated from the gated canon (snippets + tokens + theme cascade) — regenerate with
    <code>python3 knowledge/gen_showroom.py</code>; never hand-edit. Each page: ONE bar
    (title · details · theme · light/dark · width · replay · open) over the component's
    full live variant spread. Snippet sources are pure canon — no demo controls (#98-D1).</p>
    <p>Pick a component from the tree to preview it here.</p>
  </div>
  <iframe id="vframe" title="Component preview"></iframe>
</main>
</div>
<script>
(function(){
  var current=null;
  var view=document.getElementById('view'), frame=document.getElementById('vframe');
  function pageURL(slug){ return slug+'.html'; }
  function setHash(){ location.hash=current?('c='+current):''; }
  function show(slug){
    current=slug;
    view.classList.add('on');
    frame.src=pageURL(slug);
    document.querySelectorAll('nav.tree a').forEach(function(a){
      var on=(a.dataset.slug===slug);
      a.setAttribute('aria-current', String(on));
      if(on){ var d=a.closest('details'); if(d) d.open=true; }
    });
  }
  document.querySelector('nav.tree').addEventListener('click',function(e){
    var a=e.target.closest('a[data-slug]'); if(!a) return;
    e.preventDefault(); show(a.dataset.slug); setHash();
  });
  function initFromHash(){
    var h={}; location.hash.replace(/^#/,'').split('&').forEach(function(p){
      var kv=p.split('='); if(kv[0]) h[kv[0]]=kv[1]; });
    if(h.c && document.querySelector('nav.tree a[data-slug="'+h.c+'"]')) show(h.c);
  }
  window.addEventListener('hashchange',initFromHash);
  initFromHash();
})();
</script>
</body>
</html>
"""

# ---------------------------------------------------------------- generation
def theme_meta(themes, manifest_vars):
    """Per-page theme metadata: hits = how many of this component's vars the theme
    re-binds; note = what actually renders."""
    out = []
    for t in themes:
        hits = len(cascade.component_overrides(manifest_vars, t))
        if t["status"] == "base":
            note = ""
        elif not t["overrides"]:
            note = t["label"] + " has an empty override set — renders as Mono."
        elif hits == 0:
            note = t["label"] + " overrides nothing this component binds — renders as Mono."
        else:
            note = t["label"] + ": " + str(hits) + " var(s) re-bound."
        out.append({"attr": t["attr"], "label": t["label"], "hits": hits, "note": note})
    return out

def theme_buttons(themes):
    return "".join(
        '<button data-theme="%s" aria-pressed="%s">%s</button>'
        % (t["attr"], "true" if t["attr"] == "mono" else "false",
           htmlmod.escape(t["label"].replace("Apollo ", "")))
        for t in themes)

def build_pages():
    """-> {relpath: content} for the whole showroom."""
    themes = cascade.load_themes()
    btns = theme_buttons(themes)
    files, cards = {}, {}
    for f in sorted(glob.glob(os.path.join(SNIP, "*.reference.html"))):
        src = open(f).read()
        mm = MANIFEST_RE.search(src)
        varmap = json.loads(mm.group(1)).get("vars", {}) if mm else {}
        slug = slug_of(f)
        theme_css = cascade.snippet_theme_css(varmap, slug)   # slug -> s158 guards parity
        payload, _rewrites = rebase_payload_urls(src, f)   # srcdoc base-URL trap — see the block above
        inject = ("\n<style id=\"apollo-theme-cascade\">\n/* generated by gen_showroom.py from "
                  "tokens/themes/*.json — the [data-apollo-theme] re-projection of this "
                  "snippet's manifest vars */\n" + theme_css + "\n</style>\n"
                  + "\n<!-- generated by gen_showroom.py: review overlay in every pane "
                  + "(source of truth: knowledge/_review/_review-overlay.html) -->\n"
                  + overlay_block(label_of(slug), "knowledge/snippets/" + os.path.basename(f))
                  + "\n")
        if "</body>" in payload:
            payload = payload.replace("</body>", inject + "</body>", 1)
        else:
            payload += inject
        b64 = base64.b64encode(payload.encode("utf-8")).decode("ascii")
        meta = theme_meta(themes, varmap)
        legacy_hits = next((m["hits"] for m in meta if m["attr"] == "legacy"), 0)
        meta_line = "%d token(s) · Legacy re-binds %d" % (len(varmap), legacy_hits)
        # Replay lives in the ONE bar (#98-D1); DISABLED where the snippet has no
        # motion idiom — the bar states inapplicability, never hides it.
        # Two recognised idioms (ds-029): (1) the `dv-animate` class-toggle idiom,
        # (2) direct `animation:` properties driven by @keyframes in the snippet
        # (e.g. Confirmation.reference.html), which is ratified and NOT migrated
        # to dv-animate for tooling's sake.
        has_dv_animate = "dv-animate" in src
        has_direct_keyframes = ("@keyframes" in src
                                 and re.search(r"animation\s*:\s*[a-zA-Z]", src) is not None)
        has_motion = has_dv_animate or has_direct_keyframes
        page = (PAGE_TMPL
                .replace("__LABEL__", htmlmod.escape(label_of(slug)))
                .replace("__CSS__", CHROME_CSS)
                .replace("__THEME_BTNS__", btns)
                .replace("__THEMES_JSON__", json.dumps(meta))
                .replace("__META__", htmlmod.escape(meta_line))
                .replace("__REPLAY_ATTR__",
                         "" if has_motion else ' disabled title="No motion in this component"')
                .replace("__B64__", b64))
        files[slug + ".html"] = page
        cards[slug] = {"label": label_of(slug),
                       "cat": CAT_OF.get(slug, "More"),
                       "meta": meta_line}
    # index
    sections = []
    cats = [c for c, _ in CATEGORIES] + (["More"] if any(v["cat"] == "More" for v in cards.values()) else [])
    for cat in cats:
        slugs = sorted(s for s, v in cards.items() if v["cat"] == cat)
        if not slugs:
            continue
        links = "".join(
            '<a data-slug="%s" href="%s.html" aria-current="false" title="%s">%s</a>'
            % (s, s, htmlmod.escape(cards[s]["meta"], quote=True),
               htmlmod.escape(cards[s]["label"]))
            for s in slugs)
        sections.append('<details open><summary>%s<span class="c">%d</span></summary>%s</details>'
                        % (htmlmod.escape(cat), len(slugs), links))
    files["index.html"] = (INDEX_TMPL
                           .replace("__CSS__", CHROME_CSS)
                           .replace("__THEME_BTNS__", btns)
                           .replace("__COUNT__", str(len(cards)))
                           .replace("__SECTIONS__", "\n".join(sections)))
    return files

def selftest():
    """Bites for the URL rebase + gate (2026-07-27). Every gate ships one."""
    import tempfile
    fails = []
    ran = []          # ★ the count is COMPUTED, never a literal — the {17} class, swept #39.
                      # ⚠ Two of this selftest's checks are try/except gates, NOT bite() calls,
                      # so counting bite() alone would UNDER-report 6 as 4. They register here.
    def bite(name, got, want):
        ran.append(name)
        if got != want:
            fails.append("%s\n     got:  %r\n     want: %r" % (name, got, want))

    fake = os.path.join(SNIP, "_selftest.reference.html")   # never written; path only

    out, rw = rebase_payload_urls('<link rel="stylesheet" href="../canon/type.css">', fake)
    bite("1 · the real case — type.css rebased for showroom/",
         out, '<link rel="stylesheet" href="../knowledge/canon/type.css">')

    out, _ = rebase_payload_urls('<use href="#ic-help"></use><a href="#top">x</a>', fake)
    bite("2 · fragment-only URLs are NOT rebased (the <base> trap: icon sprites)",
         out, '<use href="#ic-help"></use><a href="#top">x</a>')

    out, _ = rebase_payload_urls(
        '<img src="data:image/png;base64,AAA"><a href="https://x.test/a">x</a><i href="/abs">y</i>', fake)
    bite("3 · data:/https:/root-absolute URLs are left alone",
         out, '<img src="data:image/png;base64,AAA"><a href="https://x.test/a">x</a><i href="/abs">y</i>')

    # 4 · NOT idempotent, and that is the safe direction: the input is always a raw
    # snippet (URLs relative to knowledge/snippets/). Feeding it an already-rebased
    # payload must FAIL LOUD rather than quietly walk the path up another level.
    ran.append("4 · double-rebase fails loud")
    try:
        rebase_payload_urls('<link href="../knowledge/canon/type.css">', fake)
        fails.append("4 · a double-rebase must exit non-zero — it did not")
    except SystemExit as e:
        if e.code != 1:
            fails.append("4 · double-rebase exited %r, expected 1" % e.code)

    ran.append("5 · missing-target gate fires")
    with tempfile.TemporaryDirectory():                      # bite 5 — the GATE fires
        try:
            rebase_payload_urls('<link href="../canon/does-not-exist.css">', fake)
            fails.append("5 · a MISSING target must exit non-zero — it did not")
        except SystemExit as e:
            if e.code != 1:
                fails.append("5 · gate exited %r, expected 1" % e.code)

    out, _ = rebase_payload_urls('<link href="../canon/type.css?v=2#x">', fake)
    bite("5b · query/fragment suffixes survive the existence check",
         out, '<link href="../knowledge/canon/type.css?v=2#x">')

    # 6 · #98-D1 ONE-BAR contract, pinned on the templates themselves: no back-CTA,
    # no per-pane bars, ONE iframe, replay + open IN the bar; index carries no viewbar.
    bite("6 · page template has no Library back-CTA (#98-D1)",
         'class="back"' in PAGE_TMPL or "← Library" in PAGE_TMPL, False)
    bite("6b · ONE pane — a single iframe in the page template",
         PAGE_TMPL.count("<iframe"), 1)
    bite("6c · replay + open live in the ONE bar",
         'id="replay"' in PAGE_TMPL and 'id="open"' in PAGE_TMPL, True)
    bite("6d · index has no duplicate viewbar",
         "viewbar" in INDEX_TMPL, False)
    bite("6e · index has no theme seg — controls live on the page bar only (#98)",
         'id="themes"' in INDEX_TMPL, False)

    if fails:
        print("gen_showroom --selftest: %d BITE(S) FAILED" % len(fails))
        for f in fails:
            print("  ❌ " + f)
        sys.exit(1)
    print("gen_showroom --selftest OK — %d bites (rebase · fragments · absolutes · "
          "double-rebase fails loud · missing-target gate · query suffix · "
          "#98-D1 one-bar contract ×4)." % len(ran))

def main():
    if "--selftest" in sys.argv:
        return selftest()
    files = build_pages()
    check = "--check" in sys.argv
    stale = []
    for rel, content in sorted(files.items()):
        path = os.path.join(OUTD, rel)
        cur = open(path).read() if os.path.exists(path) else None
        if cur != content:
            stale.append(rel)
            if not check:
                os.makedirs(OUTD, exist_ok=True)
                open(path, "w").write(content)
    # prune orphans (a renamed/removed snippet must not leave a rotting page)
    orphans = [os.path.basename(p) for p in glob.glob(os.path.join(OUTD, "*.html"))
               if os.path.basename(p) not in files]
    if not check:
        for o in orphans:
            os.remove(os.path.join(OUTD, o))
    if check:
        if stale or orphans:
            print("gen_showroom --check: OUT OF SYNC — stale: %s orphaned: %s\n"
                  "Run: python3 knowledge/gen_showroom.py" % (stale[:6], orphans[:6]))
            sys.exit(1)
        print("gen_showroom --check OK — %d page(s) + index in sync." % (len(files) - 1))
        return
    print("gen_showroom: %d page(s) + index -> showroom/ (%d written, %d orphan(s) pruned)"
          % (len(files) - 1, len(stale), len(orphans)))

if __name__ == "__main__":
    main()
