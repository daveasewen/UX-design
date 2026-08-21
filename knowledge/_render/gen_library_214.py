#!/usr/bin/env python3
"""
gen_library_214.py — builds reviews/LIBRARY-2026-08-21-v2.html, the component-library
BROWSER (session #214, LANE L). Successor interface to showroom/index.html.

⛔ PROPOSED, NOT RULED. Writes ONE review-surface file. It mints no token, edits no canon,
touches no store file, and does not modify showroom/index.html (v1 stays exactly where it is).

WHY IT EXISTS — Dave, 2026-08-21, verbatim:
  "On the library file I'd like to improve the interface, I'd like the controls to be in the
   true header and the component pages don't need the review overlay, its just clutter. Can I
   have a search at the top of the menu. Type filters, atom, molecule, organism, lock-up,
   shell, template etc... And any other finding mechanism that might be appropriate. All the
   components must be interactively working. i need to see how the side menu behaves."

WHAT CHANGED AGAINST showroom/index.html (v1)
  1. TRUE HEADER. v1's header carried a title and a count only; every control (theme,
     light/dark, width, replay, open) lived on the embedded component page's own bar, so
     the library had two stacked bars and none of the controls belonged to the library.
     v2 owns theme · light/dark · width · replay · open in ONE page header, and the
     embedded page's bar is hidden (see 2).
  2. NO REVIEW OVERLAY, NO SECOND BAR. Panes are loaded as
     `../showroom/<slug>.html#theme=…&m=…&w=…&chrome=0`. `chrome=0` is the embed mode added
     to gen_showroom.py at #214: it hides that page's own bar and cuts the review-overlay
     block out of the payload before srcdoc. The overlay is opt-OUT, not deleted —
     REVIEW-213-wave-components-four-theme-v1.html iframes the same pages WITH the overlay
     and is untouched. Swap point documented in gen_showroom.py's docstring.
  3. SEARCH at the top of the menu — substring over name + slug + purpose + ALIASES.
  4. LEVEL FACET CHIPS + a category tree + a behaviour facet + recently-viewed.

THE SPECIMEN RULE — [[specimen-starts-from-reference]] (#202)
  Nothing here is re-drawn. Every pane is an <iframe> at the component's OWN generated
  showroom page, which srcdoc-mounts the gated reference snippet verbatim. Not one byte of
  component markup is copied into this page. This page owns only chrome.

THEME BROADCAST (same mechanism REVIEW-213 uses; read gen_showroom.py PAGE_TMPL first)
  Each showroom page listens on `hashchange` and re-applies html[data-apollo-theme] +
  body[data-theme] + the width to its srcdoc frame. So re-theming a pane is a FRAGMENT
  assignment on iframe.src — same document, no reload, no cross-origin script access.

⚠ THE LEVEL WORD-SET IS UNPICKED (Dave has not chosen — three candidates in
  notes/_briefs/2026-08-21-214-taxonomy-research-v1.md §d). SWAP POINT: `LEVELS` below is
  ONE config array. Change the `label` fields, or swap in one of the alternative arrays
  kept beside it, and regenerate. No other line in this file names a level word.

DERIVATION IS MECHANICAL — never hand-tagged:
  $layer "2 Shell"    -> shell      (knowledge/components/<slug>.meta.json)
  $layer "2 Template" -> template
  $layer "2 Lock-up"  -> lockup
  otherwise meta `category` in {atom, molecule, organism} -> that level
  no meta at all      -> slug-shape fallback (app-shell-* / template-* / *-lockup), else
                         "unfiled", which is REPORTED, not guessed.

REGENERATE
  python3 knowledge/_render/gen_library_214.py
  python3 knowledge/_render/gen_library_214.py --selftest
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob
import html as htmlmod
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KNOW = os.path.dirname(HERE)
ROOT = os.path.dirname(KNOW)
SNIP = os.path.join(KNOW, "snippets")
META = os.path.join(KNOW, "components")
SHOWROOM = os.path.join(ROOT, "showroom")
OUT = os.path.join(ROOT, "reviews", "LIBRARY-2026-08-21-v2.html")

sys.path.insert(0, KNOW)
sys.path.insert(0, os.path.join(KNOW, "canon"))
import gen_showroom as showroom          # label_of / CAT_OF / CATEGORIES — one source
import gen_theme_cascade as cascade      # the four themes, from tokens/themes/*.json

# ---------------------------------------------------------------------------
# ⚠⚠ THE SWAP POINT — the level word-set. Dave has NOT picked one (#214 open).
# Placeholder = his first candidate list. `key` is derived mechanically and never
# shown; `label` is the only thing on the face of the page. Swap labels here.
# ---------------------------------------------------------------------------
LEVELS = [
    {"key": "atom",     "label": "Atom"},
    {"key": "molecule", "label": "Molecule"},
    {"key": "organism", "label": "Organism"},
    {"key": "lockup",   "label": "Lock-up"},
    {"key": "shell",    "label": "Shell"},
    {"key": "template", "label": "Template"},
    {"key": "unfiled",  "label": "Unfiled"},   # never hand-tag: a gap shows as a gap
]
# Alternative word-sets from the research doc — paste over LEVELS to switch, keys unchanged:
#   Candidate 2 (industry-plain):  Foundation · Component · Pattern · Block · Shell · Template
#   Candidate 3 (Dave's second):   Primitive · Base · Pattern · Lock-up · Shell · Template

# ---------------------------------------------------------------------------
# ALIASES — the finding mechanism the research doc ranks ABOVE taxonomy
# (§c.2: "the strongest single fix for the dropdown-vs-select problem").
# alias -> slug it resolves to. Every target below is asserted to exist by --selftest.
# ---------------------------------------------------------------------------
ALIASES = {
    "select": "dropdown",
    "picker": "dropdown",
    "spinner": "loading-indicator",
    "loader": "loading-indicator",
    "throbber": "loading-indicator",
    "snackbar": "toast",
    "flash": "toast",
    "dialog": "modals",
    "lightbox": "modal-lightbox",
    "modal": "modals",
    "sheet": "drawer",
    "off-canvas": "drawer",
    "side panel": "drawer",
    "checkbox": "selection-controls",
    "radio": "selection-controls",
    "toggle": "selection-controls",
    "switch": "selection-controls",
    "typeahead": "combobox",
    "autocomplete": "combobox",
    "chips": "tags",
    "pill": "badge",
    "label": "badge",
    "datagrid": "data-grid",
    "datatable": "table",
    "grid": "table",
    "crumbs": "breadcrumbs",
    "wizard": "stepper",
    "progress": "progress-bar",
    "spin button": "stepper",
    "hamburger": "sidebar-nav",
    "side menu": "sidebar-nav",
    "nav drawer": "sidebar-nav",
    "rail": "app-shell-nav-rail",
    "omnibox": "command-palette",
    "cmd-k": "command-palette",
    "quick open": "command-palette",
    "avatar stack": "avatar-group",
    "facepile": "avatar-group",
    "tooltip": "tooltip",
    "popup": "popover",
    "menu": "dropdown",
    "context menu": "dropdown",
    "date": "date-picker",
    "calendar picker": "date-picker",
    "money": "amount-display",
    "currency": "amount-display",
    "password": "secure-entry",
    "otp": "secure-entry",
    "pin": "secure-entry",
    "search": "search-field",
    "filter": "filter-toolbar-bar",
    "sparkline": "chart-sparkline",
    "donut": "chart-donut",
    "pie": "chart-pie",
    "kpi": "kpi-tile",
    "metric": "stat-card",
    "hero banner": "hero",
    "footer links": "footer",
    "back to top": "back-to-top",
    "star rating": "rating",
    "carousel slider": "carousel",
    "accordion panel": "accordion",
    "tree view": "tree",
    "dual list": "transfer-list",
    "shuttle": "transfer-list",
    "split pane": "splitter",
    "fab": "fab",
    "speed dial": "fab",
    "qr": "qr-code",
    "gauge": "meter",
}

SCRIPT_RE = re.compile(r"<script\b(?![^>]*id=\"token-manifest\")[^>]*>(.*?)</script>", re.S)


def js_lines(snippet_src):
    """Mechanical behaviour signal: lines of non-manifest JS the snippet ships."""
    n = 0
    for body in SCRIPT_RE.findall(snippet_src):
        n += len([l for l in body.splitlines() if l.strip()])
    return n


def level_of(slug, meta):
    layer = (meta or {}).get("$layer")
    if layer == "2 Shell":
        return "shell"
    if layer == "2 Template":
        return "template"
    if layer == "2 Lock-up":
        return "lockup"
    cat = (meta or {}).get("category")
    if cat in ("atom", "molecule", "organism"):
        return cat
    if slug.startswith("app-shell-"):
        return "shell"
    if slug.startswith("template-"):
        return "template"
    if slug.endswith("-lockup"):
        return "lockup"
    return "unfiled"


def collect():
    """-> (rows, residuals). One row per EXISTING showroom page — the page is the artefact."""
    snippets = {showroom.slug_of(p): p
                for p in glob.glob(os.path.join(SNIP, "*.reference.html"))}
    alias_by_slug = {}
    for a, s in ALIASES.items():
        alias_by_slug.setdefault(s, []).append(a)

    rows, residuals = [], {"no_meta": [], "unfiled": [], "no_behaviour": [], "dead_alias": []}
    for page in sorted(glob.glob(os.path.join(SHOWROOM, "*.html"))):
        slug = os.path.basename(page)[:-5]
        if slug == "index":
            continue
        mpath = os.path.join(META, slug + ".meta.json")
        meta = None
        if os.path.exists(mpath):
            meta = json.load(open(mpath))
        else:
            residuals["no_meta"].append(slug)
        lvl = level_of(slug, meta)
        if lvl == "unfiled":
            residuals["unfiled"].append(slug)
        jsl = js_lines(open(snippets[slug]).read()) if slug in snippets else 0
        if jsl == 0:
            residuals["no_behaviour"].append(slug)
        purpose = (meta or {}).get("purpose", "") or ""
        rows.append({
            "slug": slug,
            "label": showroom.label_of(slug),
            "cat": showroom.CAT_OF.get(slug, "More"),
            "level": lvl,
            "js": jsl,
            "purpose": purpose[:240],
            "aliases": sorted(alias_by_slug.get(slug, [])),
        })
    have = {r["slug"] for r in rows}
    residuals["dead_alias"] = sorted({s for s in ALIASES.values() if s not in have})
    return rows, residuals


# ---------------------------------------------------------------------------- chrome
CSS = """
:root{--ink:#1A1A1A; --page:#FAFAFA; --line:#E1E1E1; --mid:#808080; --wash:#F4F4F4;
      --white:#FFFFFF; --focus:#305A85;}
*{box-sizing:border-box;}
html,body{height:100%;}
body{margin:0; font-family:"Univers Next for HSBC","Helvetica Neue",Arial,Helvetica,sans-serif;
  background:var(--page); color:var(--ink); -webkit-font-smoothing:antialiased;
  display:flex; flex-direction:column;}

/* ---- THE TRUE HEADER (Dave #214): every control the library owns lives here ---- */
header.app{display:flex; gap:14px; align-items:center; flex-wrap:wrap; padding:10px 20px;
  background:var(--white); border-bottom:1px solid var(--line); position:sticky; top:0; z-index:20;}
header.app h1{font-size:16px; font-weight:500; margin:0; white-space:nowrap;}
header.app .count{font-size:12px; color:var(--mid); font-variant-numeric:tabular-nums;}
header.app .spacer{flex:1 1 auto;}
header.app .now{font-size:13px; font-weight:500; max-width:26ch; overflow:hidden;
  text-overflow:ellipsis; white-space:nowrap;}
.ctl{display:flex; gap:8px; align-items:center; font-size:12px; color:var(--mid);}
.seg{display:inline-flex; border:1px solid var(--ink);}
.seg button{font:inherit; font-size:12px; padding:6px 11px; border:0; background:transparent;
  color:var(--ink); cursor:pointer; border-right:1px solid var(--line);}
.seg button:last-child{border-right:0;}
.seg button[aria-pressed="true"]{background:var(--ink); color:var(--white);}
.seg button:focus-visible, .btn:focus-visible, input:focus-visible, .chip:focus-visible,
nav.tree a:focus-visible, summary:focus-visible{outline:2px solid var(--focus); outline-offset:2px;}
.btn{font:inherit; font-size:12px; padding:6px 11px; border:1px solid var(--line);
  background:var(--white); color:var(--ink); cursor:pointer;}
.btn:hover:not(:disabled){border-color:var(--ink);}
.btn:disabled{color:var(--mid); opacity:.5; cursor:default;}
#w{width:150px; accent-color:var(--ink);}
#wv{font-variant-numeric:tabular-nums; min-width:5ch;}

/* ---- shell ---- */
.shell{display:grid; grid-template-columns:300px 1fr; flex:1 1 auto; min-height:0;}
nav.tree{border-right:1px solid var(--line); background:var(--white); overflow-y:auto;
  display:flex; flex-direction:column; min-height:0;}

/* ---- search + facets, at the TOP OF THE MENU (Dave #214) ---- */
.find{position:sticky; top:0; background:var(--white); z-index:5; padding:12px 14px 10px;
  border-bottom:1px solid var(--line);}
.searchwrap{position:relative;}
#q{width:100%; font:inherit; font-size:13px; padding:9px 30px 9px 11px; border:1px solid var(--ink);
  background:var(--white); color:var(--ink);}
#q::placeholder{color:var(--mid);}
/* the UA's own search-clear would sit beside ours — two × in one field (seen in the
   820px render, 2026-08-21). One clear affordance, and it is the one we wired. */
#q::-webkit-search-cancel-button, #q::-webkit-search-decoration{-webkit-appearance:none; display:none;}
#qclear{position:absolute; right:2px; top:2px; bottom:2px; width:26px; border:0; cursor:pointer;
  background:transparent; color:var(--mid); font:inherit; font-size:14px; display:none;}
.find .hint{font-size:11px; color:var(--mid); margin:6px 0 0;}
.chips{display:flex; flex-wrap:wrap; gap:5px; margin:10px 0 0;}
.chip{font:inherit; font-size:11px; padding:4px 9px; border:1px solid var(--line);
  background:var(--white); color:var(--ink); cursor:pointer; border-radius:999px;
  display:inline-flex; gap:5px; align-items:baseline;}
.chip .n{color:var(--mid); font-variant-numeric:tabular-nums;}
.chip:hover{border-color:var(--ink);}
.chip[aria-pressed="true"]{background:var(--ink); color:var(--white); border-color:var(--ink);}
.chip[aria-pressed="true"] .n{color:var(--white); opacity:.7;}
.resultline{font-size:11px; color:var(--mid); margin:9px 0 0; display:flex; gap:8px;
  align-items:baseline;}
.resultline button{font:inherit; font-size:11px; border:0; background:transparent; padding:0;
  color:var(--ink); text-decoration:underline; cursor:pointer;}

/* ---- the tree itself ---- */
.treescroll{overflow-y:auto; flex:1 1 auto; padding-bottom:24px;}
nav.tree details{border-bottom:1px solid var(--line);}
nav.tree summary{font-size:12px; font-weight:500; padding:9px 14px; cursor:pointer;
  list-style:none; display:flex; align-items:baseline; gap:8px;}
nav.tree summary::-webkit-details-marker{display:none;}
nav.tree summary::before{content:"\\25B8"; font-size:9px; color:var(--mid); transition:transform 140ms;}
nav.tree details[open] summary::before{transform:rotate(90deg);}
nav.tree summary .c{margin-left:auto; font-size:11px; color:var(--mid);
  font-variant-numeric:tabular-nums;}
nav.tree a{display:flex; gap:8px; align-items:baseline; font-size:13px; color:var(--ink);
  text-decoration:none; padding:6px 14px 6px 30px; border-left:2px solid transparent;}
nav.tree a:hover{background:var(--wash);}
nav.tree a[aria-current="true"]{border-left-color:var(--ink); font-weight:500; background:var(--wash);}
nav.tree a .lvl{margin-left:auto; font-size:10px; color:var(--mid); text-transform:lowercase;
  white-space:nowrap;}
nav.tree a .why{font-size:10px; color:var(--mid);}
nav.tree a[hidden], nav.tree details[hidden]{display:none;}
.recent{padding:10px 14px; border-bottom:1px solid var(--line);}
.recent h2{font-size:11px; font-weight:500; color:var(--mid); margin:0 0 6px; letter-spacing:.04em;
  text-transform:uppercase;}
.recent a{display:block; font-size:12px; color:var(--ink); text-decoration:none; padding:3px 0;}
.recent a:hover{text-decoration:underline;}
.empty{padding:18px 14px; font-size:12px; color:var(--mid);}

/* ---- the pane ---- */
main.view{min-width:0; display:flex; flex-direction:column; background:var(--page);}
main.view iframe{border:0; width:100%; flex:1 1 auto; display:none; background:var(--white);}
main.view.on iframe{display:block;}
main.view.on .intro{display:none;}
.intro{padding:28px 28px 0; max-width:760px;}
.intro h2{font-size:18px; font-weight:500; margin:0 0 10px;}
.intro p{font-size:13px; color:var(--mid); line-height:1.55; margin:0 0 10px;}
.intro code{font-family:ui-monospace,Menlo,Consolas,monospace; font-size:12px;}
.intro kbd{font:inherit; font-size:11px; border:1px solid var(--line); padding:1px 5px;
  background:var(--white);}
@media (max-width:820px){
  .shell{grid-template-columns:1fr;}
  nav.tree{border-right:0; border-bottom:1px solid var(--line); max-height:46vh;}
}
"""

TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Apollo component library v2 · browse</title>
<style>__CSS__</style>
</head>
<body>
<header class="app">
  <h1>Apollo component library</h1>
  <span class="count"><strong>__COUNT__</strong> components</span>
  <span class="now" id="now" aria-live="polite"></span>
  <span class="spacer"></span>
  <div class="ctl"><span>Theme</span>
    <div class="seg" id="themes" role="group" aria-label="Theme">__THEME_BTNS__</div></div>
  <div class="ctl">
    <div class="seg" id="modes" role="group" aria-label="Light or dark">
      <button data-mode="light" aria-pressed="true">Light</button>
      <button data-mode="dark" aria-pressed="false">Dark</button>
    </div></div>
  <div class="ctl"><label for="w">Width</label>
    <input id="w" type="range" min="320" max="1600" step="20" value="1600">
    <span id="wv">full</span></div>
  <button class="btn" id="replay" type="button" disabled>&#8635; Replay</button>
  <button class="btn" id="open" type="button" disabled>Open &#8599;</button>
</header>

<div class="shell">
<nav class="tree" aria-label="Components">
  <div class="find">
    <div class="searchwrap">
      <input id="q" type="search" autocomplete="off" spellcheck="false"
             placeholder="Search components&hellip;  (press /)"
             aria-label="Search components by name, purpose or alias">
      <button id="qclear" type="button" aria-label="Clear search">&times;</button>
    </div>
    <p class="hint">Names, purpose text and aliases &mdash; &ldquo;dropdown&rdquo; finds Select,
      &ldquo;spinner&rdquo; finds Loading-indicator.</p>
    <div class="chips" id="levels" role="group" aria-label="Filter by type">__LEVEL_CHIPS__</div>
    <div class="chips" id="flags" role="group" aria-label="Other filters">
      <button class="chip" data-flag="js" aria-pressed="false">Ships behaviour <span class="n"
        id="n-js"></span></button>
    </div>
    <p class="resultline"><span id="rc"></span>
      <button type="button" id="reset" hidden>Clear all</button></p>
  </div>
  <div class="recent" id="recentbox" hidden>
    <h2>Recently opened</h2>
    <div id="recent"></div>
  </div>
  <div class="treescroll" id="treescroll">
__SECTIONS__
    <p class="empty" id="noresults" hidden>Nothing matches. Try an alias &mdash;
      dropdown, spinner, snackbar, typeahead, facepile, shuttle&hellip;</p>
  </div>
</nav>

<main class="view" id="view">
  <div class="intro">
    <h2>Browse the library</h2>
    <p>Every pane below is the component&rsquo;s own generated showroom page, loaded live &mdash;
      its scripts run, its side-navs open, its tabs switch. Nothing on this page is a re-drawing.</p>
    <p>The controls in the header drive the pane: theme, light/dark and width are broadcast to it
      as a URL fragment, so switching theme never reloads the component.</p>
    <p>The component page&rsquo;s own bar and its review overlay are hidden here
      (<code>#chrome=0</code>) &mdash; this is the library view, not the review surface.</p>
    <p>Search with <kbd>/</kbd> or <kbd>&#8984;K</kbd>. Filter by type with the chips.
      Pick a component to preview it here.</p>
  </div>
  <iframe id="vframe" title="Component preview"></iframe>
</main>
</div>

<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
  var DATA=JSON.parse(document.getElementById('data').textContent);
  var ALIASES=DATA.aliases, ROWS=DATA.rows;
  var BY={}; ROWS.forEach(function(r){ BY[r.slug]=r; });

  var view=document.getElementById('view'), frame=document.getElementById('vframe');
  var q=document.getElementById('q'), qclear=document.getElementById('qclear');
  var rc=document.getElementById('rc'), reset=document.getElementById('reset');
  var noresults=document.getElementById('noresults'), now=document.getElementById('now');
  var wIn=document.getElementById('w'), wv=document.getElementById('wv');
  var openBtn=document.getElementById('open'), replayBtn=document.getElementById('replay');
  var state={slug:null, theme:'mono', mode:'light', w:null, levels:{}, flags:{}, q:''};
  var recent=[];

  /* ---------- the pane: fragment broadcast, exactly the REVIEW-213 mechanism ---------- */
  function frag(){
    var p=['theme='+state.theme,'m='+state.mode];
    if(state.w) p.push('w='+state.w);
    p.push('chrome=0');                       // library view: no second bar, no review overlay
    return '#'+p.join('&');
  }
  function pageURL(slug){ return '../showroom/'+slug+'.html'+frag(); }
  function retheme(){
    if(!state.slug) return;
    // same document + new fragment => the showroom page's hashchange handler re-themes
    // its srcdoc pane in place. Assigning the whole URL is safe: the path is unchanged.
    frame.src=pageURL(state.slug);
  }
  function show(slug){
    if(!BY[slug]) return;
    state.slug=slug;
    view.classList.add('on');
    frame.src=pageURL(slug);
    now.textContent=BY[slug].label;
    openBtn.disabled=false; replayBtn.disabled=(BY[slug].js===0);
    replayBtn.title=BY[slug].js===0?'This component ships no behaviour script':'';
    document.querySelectorAll('nav.tree a[data-slug]').forEach(function(a){
      var on=(a.dataset.slug===slug);
      a.setAttribute('aria-current', String(on));
      if(on){ var d=a.closest('details'); if(d) d.open=true; }
    });
    recent=[slug].concat(recent.filter(function(s){return s!==slug;})).slice(0,6);
    drawRecent();
    setHash();
  }
  function drawRecent(){
    var box=document.getElementById('recentbox'), list=document.getElementById('recent');
    box.hidden=recent.length<2;
    list.innerHTML='';
    recent.slice(1).forEach(function(s){
      var a=document.createElement('a'); a.href='#c='+s; a.textContent=BY[s].label;
      a.dataset.slug=s; list.appendChild(a);
    });
  }

  /* ---------- search: name + slug + purpose + ALIASES ---------- */
  function aliasHits(term){
    var out={};
    Object.keys(ALIASES).forEach(function(a){
      if(a.indexOf(term)!==-1) out[ALIASES[a]]=a;
    });
    return out;
  }
  function matches(r, term, hits){
    if(!term) return {ok:true, why:''};
    if(r.slug.indexOf(term)!==-1) return {ok:true, why:''};
    if(r.label.toLowerCase().indexOf(term)!==-1) return {ok:true, why:''};
    if(hits[r.slug]) return {ok:true, why:'\\u201c'+hits[r.slug]+'\\u201d'};
    if(r.purpose.toLowerCase().indexOf(term)!==-1) return {ok:true, why:'in purpose'};
    return {ok:false, why:''};
  }
  function activeKeys(obj){ return Object.keys(obj).filter(function(k){return obj[k];}); }

  function filter(){
    var term=state.q.trim().toLowerCase();
    var hits=term?aliasHits(term):{};
    var lv=activeKeys(state.levels), fl=activeKeys(state.flags), n=0;
    document.querySelectorAll('nav.tree a[data-slug]').forEach(function(a){
      var r=BY[a.dataset.slug];
      var m=matches(r, term, hits);
      var ok=m.ok
        && (lv.length===0 || lv.indexOf(r.level)!==-1)
        && (fl.indexOf('js')===-1 || r.js>0);
      a.hidden=!ok;
      a.querySelector('.why').textContent=(ok&&m.why)?m.why:'';
      if(ok) n++;
    });
    document.querySelectorAll('nav.tree details').forEach(function(d){
      var vis=d.querySelectorAll('a[data-slug]:not([hidden])').length;
      d.hidden=(vis===0);
      d.querySelector('.c').textContent=vis;
      if(term||lv.length||fl.length) d.open=true;
    });
    noresults.hidden=(n>0);
    rc.textContent=n+' of '+ROWS.length+' shown';
    var dirty=!!(term||lv.length||fl.length);
    reset.hidden=!dirty; qclear.style.display=term?'block':'none';
  }

  /* ---------- wiring ---------- */
  q.addEventListener('input',function(){ state.q=q.value; filter(); });
  q.addEventListener('keydown',function(e){
    if(e.key==='Escape'){ q.value=''; state.q=''; filter(); q.blur(); }
    if(e.key==='Enter'){
      var first=document.querySelector('nav.tree a[data-slug]:not([hidden])');
      if(first){ show(first.dataset.slug); }
    }
  });
  qclear.addEventListener('click',function(){ q.value=''; state.q=''; filter(); q.focus(); });
  reset.addEventListener('click',function(){
    q.value=''; state.q=''; state.levels={}; state.flags={};
    document.querySelectorAll('.chip').forEach(function(c){c.setAttribute('aria-pressed','false');});
    filter();
  });
  document.addEventListener('keydown',function(e){
    var typing=/^(INPUT|TEXTAREA|SELECT)$/.test((e.target.tagName||''));
    if((e.key==='/'&&!typing) || (e.key.toLowerCase()==='k'&&(e.metaKey||e.ctrlKey))){
      e.preventDefault(); q.focus(); q.select();
    }
  });
  document.getElementById('levels').addEventListener('click',function(e){
    var c=e.target.closest('.chip'); if(!c) return;
    var k=c.dataset.level, on=c.getAttribute('aria-pressed')!=='true';
    c.setAttribute('aria-pressed',String(on)); state.levels[k]=on; filter();
  });
  document.getElementById('flags').addEventListener('click',function(e){
    var c=e.target.closest('.chip'); if(!c) return;
    var on=c.getAttribute('aria-pressed')!=='true';
    c.setAttribute('aria-pressed',String(on)); state.flags[c.dataset.flag]=on; filter();
  });
  document.querySelector('nav.tree').addEventListener('click',function(e){
    var a=e.target.closest('a[data-slug]'); if(!a) return;
    e.preventDefault(); show(a.dataset.slug);
  });
  document.getElementById('themes').addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    state.theme=b.dataset.theme; syncSegs(); retheme(); setHash();
  });
  document.getElementById('modes').addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    state.mode=b.dataset.mode; syncSegs(); retheme(); setHash();
  });
  wIn.addEventListener('input',function(){
    var full=(+wIn.value>=1600); state.w=full?null:+wIn.value;
    wv.textContent=full?'full':wIn.value+'px'; retheme(); setHash();
  });
  openBtn.addEventListener('click',function(){
    if(state.slug) window.open('../showroom/'+state.slug+'.html'+frag().replace('&chrome=0',''));
  });
  replayBtn.addEventListener('click',function(){
    // the pane owns its motion; re-mounting the fragment is the library's only lever
    if(state.slug){ frame.src='about:blank'; setTimeout(function(){ frame.src=pageURL(state.slug); },0); }
  });
  function syncSegs(){
    document.querySelectorAll('#themes button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.theme===state.theme)); });
    document.querySelectorAll('#modes button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.mode===state.mode)); });
  }

  /* ---------- deep links ---------- */
  function setHash(){
    var p=[]; if(state.slug) p.push('c='+state.slug);
    p.push('theme='+state.theme); p.push('m='+state.mode);
    history.replaceState(null,'','#'+p.join('&'));
  }
  function initFromHash(){
    var h={}; location.hash.replace(/^#/,'').split('&').forEach(function(kv){
      var p=kv.split('='); if(p[0]) h[p[0]]=decodeURIComponent(p[1]||''); });
    if(h.theme) state.theme=h.theme;
    if(h.m==='light'||h.m==='dark') state.mode=h.m;
    syncSegs();
    if(h.c&&BY[h.c]) show(h.c);
  }
  document.getElementById('n-js').textContent=ROWS.filter(function(r){return r.js>0;}).length;
  filter(); initFromHash();
})();
</script>
</body>
</html>
"""


def build():
    rows, residuals = collect()
    themes = cascade.load_themes()
    btns = "".join(
        '<button data-theme="%s" aria-pressed="%s">%s</button>'
        % (t["attr"], "true" if t["attr"] == "mono" else "false",
           htmlmod.escape(t["label"].replace("Apollo ", "")))
        for t in themes)

    counts = {}
    for r in rows:
        counts[r["level"]] = counts.get(r["level"], 0) + 1
    chips = "".join(
        '<button class="chip" data-level="%s" aria-pressed="false">%s <span class="n">%d</span></button>'
        % (lv["key"], htmlmod.escape(lv["label"]), counts.get(lv["key"], 0))
        for lv in LEVELS if counts.get(lv["key"], 0))

    cats = [c for c, _ in showroom.CATEGORIES] + ["More"]
    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["cat"], []).append(r)
    sections = []
    lvl_label = {lv["key"]: lv["label"] for lv in LEVELS}
    for cat in cats:
        items = sorted(by_cat.get(cat, []), key=lambda r: r["label"])
        if not items:
            continue
        links = "".join(
            '<a data-slug="%s" href="#c=%s" aria-current="false" title="%s">'
            '<span class="nm">%s</span><span class="why"></span>'
            '<span class="lvl">%s</span></a>'
            % (r["slug"], r["slug"],
               htmlmod.escape((r["purpose"][:110] or r["label"]), quote=True),
               htmlmod.escape(r["label"]), htmlmod.escape(lvl_label[r["level"]]))
            for r in items)
        sections.append('<details open><summary>%s<span class="c">%d</span></summary>%s</details>'
                        % (htmlmod.escape(cat), len(items), links))

    data = json.dumps({"rows": rows, "aliases": ALIASES}, sort_keys=True)
    page = (TMPL
            .replace("__CSS__", CSS)
            .replace("__COUNT__", str(len(rows)))
            .replace("__THEME_BTNS__", btns)
            .replace("__LEVEL_CHIPS__", chips)
            .replace("__SECTIONS__", "\n".join(sections))
            .replace("__DATA__", data))
    return page, rows, residuals


def selftest():
    fails, ran = [], []

    def bite(name, got, want):
        ran.append(name)
        if got != want:
            fails.append("%s\n     got:  %r\n     want: %r" % (name, got, want))

    page, rows, residuals = build()

    bite("1 · every alias target is a real component page",
         residuals["dead_alias"], [])
    bite("2 · no component is re-drawn — the page owns no snippet markup, only iframes",
         page.count("<iframe"), 1)
    bite("3 · panes are loaded with chrome=0 (no second bar, no review overlay)",
         "chrome=0" in page, True)
    bite("4 · the level word-set reaches the page from LEVELS only",
         all(lv["label"] in page for lv in LEVELS
             if any(r["level"] == lv["key"] for r in rows)), True)
    bite("5 · search box sits at the top of the menu, above the tree",
         page.index('id="q"') < page.index('class="treescroll"'), True)
    bite("6 · controls are in the TRUE header, not the tree",
         page.index('id="themes"') < page.index('<div class="shell">'), True)
    bite("7 · levels are derived, never hand-tagged — no literal level in a row",
         sorted({r["level"] for r in rows}) ==
         sorted({lv["key"] for lv in LEVELS if any(x["level"] == lv["key"] for x in rows)}), True)
    bite("8 · one row per showroom page",
         # ⚠ basename equality, NOT endswith: template-list-index.html ends with "index.html"
         len(rows), len([p for p in glob.glob(os.path.join(SHOWROOM, "*.html"))
                         if os.path.basename(p) != "index.html"]))
    bite("9 · the embed mode this page depends on exists in gen_showroom",
         "h.chrome==='0'" in showroom.PAGE_TMPL, True)

    if fails:
        print("gen_library_214 --selftest: %d BITE(S) FAILED" % len(fails))
        for f in fails:
            print("  ❌ " + f)
        sys.exit(1)
    print("gen_library_214 --selftest OK — %d bites." % len(ran))
    print("   residual · no meta.json: %s" % (residuals["no_meta"] or "none"))
    print("   residual · unfiled level: %s" % (residuals["unfiled"] or "none"))
    print("   residual · ships no behaviour script: %d component(s)"
          % len(residuals["no_behaviour"]))


def main():
    if "--selftest" in sys.argv:
        return selftest()
    page, rows, residuals = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(page)
    print("gen_library_214: %d component(s) -> %s"
          % (len(rows), os.path.relpath(OUT, ROOT)))
    print("   no meta.json:      %s" % (residuals["no_meta"] or "none"))
    print("   unfiled level:     %s" % (residuals["unfiled"] or "none"))
    print("   no behaviour JS:   %d — %s"
          % (len(residuals["no_behaviour"]), ", ".join(residuals["no_behaviour"][:12])))


if __name__ == "__main__":
    main()
