#!/usr/bin/env python3
"""
gen_library_214.py — builds showroom/index.html, the component-library BROWSER
(session #214 LANE L; RULED and rebuilt at #215 under s215-D4 + s215-D5).

⛔ s215-D5 (1): LIBRARY v2 **REPLACES** showroom/index.html. This generator now OWNS
   showroom/index.html. gen_showroom.py no longer emits an index of its own (it protects
   this file from its orphan prune and bites on its absence in --check). Two indexes would
   drift, and Dave ruled they must not coexist.
   reviews/LIBRARY-2026-08-21-v2.html — the #214 address, cited in _state.json row W-99zg —
   is kept ALIVE as a generated REDIRECT STUB (WRITE-ONCE addressing, ADR-0017): the address
   still resolves, and it carries no second copy of the library to rot.

WHY IT EXISTS — Dave, 2026-08-21, verbatim:
  "On the library file I'd like to improve the interface, I'd like the controls to be in the
   true header and the component pages don't need the review overlay, its just clutter. Can I
   have a search at the top of the menu. Type filters, atom, molecule, organism, lock-up,
   shell, template etc... And any other finding mechanism that might be appropriate. All the
   components must be interactively working. i need to see how the side menu behaves."

WHAT #215 ADDED, EACH LINE ANSWERING A RULING
  s215-D4 · THE LEVEL LADDER. Foundations · Tokens (top tiers) then Primitives (RESERVED) /
    Element / Pattern / Block / Shell / Template. ONE config array — `LEVELS` — and the
    derivation `level_of()` beneath it. The word "lock-up" survives as the STORE signal
    ($layer "2 Lock-up") but is not public navigation: it derives to Block.
  s215-D4 · TWO TABS replace the facet chips. "Type" browses the ruled ladder; "Usage"
    browses by task/purpose. Both trees are generated; the tabs swap which one is shown.
  s215-D5 (2) · STATUS facet — stable / beta / deprecated, on every card and filterable
    inside either tab. Derived at ONE point (`status_of`), overridable at ONE point
    (`STATUS_OVERRIDES`) so a ruling of Dave's overwrites one place.
  s215-D5 (3) · THUMBNAILS. Cards carry `showroom/_thumbs/<slug>.png`, shot by
    knowledge/_render/gen_thumbs.py (headless chromium over the real showroom page).
    This generator only ADDRESSES them; a missing thumbnail degrades to a placeholder and
    is REPORTED as a residual, never faked.
  s215-D5 (4) · RELATED COMPONENTS. `RELATED_CLUSTERS` seeds confusable neighbours from the
    68-alias table; the one-line disambiguation is each neighbour's OWN meta `purpose`,
    first sentence — factual about THIS library by construction, never borrowed prose.
  s215-D5 (5) · MACHINE-READABLE INDEX — showroom/index.json, sorted keys and rows,
    generated from the same store in the same pass, so it cannot disagree with the page.

THE SPECIMEN RULE — [[specimen-starts-from-reference]] (#202)
  Nothing here is re-drawn. Every pane is an <iframe> at the component's OWN generated
  showroom page, which srcdoc-mounts the gated reference snippet verbatim. Not one byte of
  component markup is copied into this page. This page owns only chrome.

THEME BROADCAST (same mechanism REVIEW-213 uses; read gen_showroom.py PAGE_TMPL first)
  Each showroom page listens on `hashchange` and re-applies html[data-apollo-theme] +
  body[data-theme] + the width to its srcdoc frame. So re-theming a pane is a FRAGMENT
  assignment on iframe.src — same document, no reload, no cross-origin script access.

REGENERATE
  python3 knowledge/_render/gen_library_214.py
  python3 knowledge/_render/gen_library_214.py --check      # in-sync gate
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
OUT = os.path.join(SHOWROOM, "index.html")               # s215-D5 (1) — v2 IS the index
JSON_OUT = os.path.join(SHOWROOM, "index.json")          # s215-D5 (5)
STUB_OUT = os.path.join(ROOT, "reviews", "LIBRARY-2026-08-21-v2.html")   # kept-alive address
THUMB_DIR = os.path.join(SHOWROOM, "_thumbs")            # s215-D5 (3) — written by gen_thumbs.py
THUMB_REL = "_thumbs/%s.png"
ITINERARY = os.path.join(ROOT, "reviews", "ITINERARY-STATUS-2026-08-21-v3.json")

# The sentinel gen_showroom.py's --check bites on: proof the index it is looking at is the
# LIBRARY index and not a resurrected v1.
INDEX_SENTINEL = "<!-- APOLLO-LIBRARY-INDEX v2 (gen_library_214.py) -->"

sys.path.insert(0, KNOW)
sys.path.insert(0, os.path.join(KNOW, "canon"))
import gen_showroom as showroom          # label_of / CAT_OF / CATEGORIES — one source
import gen_theme_cascade as cascade      # the four themes, from tokens/themes/*.json

# ---------------------------------------------------------------------------
# s215-D4 — THE LEVEL LADDER, RULED. Dave, 2026-08-22:
#   "Foundations and Tokens then: Primitives(if needed)/Element/Pattern/Block/Shell/Template"
# `key` is derived mechanically and never shown; `label` is the only thing on the face of
# the page. A tier with no members is not drawn (a ladder rung with nothing on it is noise).
# ---------------------------------------------------------------------------
LEVELS = [
    {"key": "foundation", "label": "Foundations"},
    {"key": "token",      "label": "Tokens"},
    # {"key": "primitive", "label": "Primitives"},
    #   ⚠ RESERVED TIER, s215-D4: "Primitives (if needed)". Surfaced only when the store
    #   actually carries unstyled-behaviour entries. MEASURED 2026-08-22: it does not
    #   (no meta declares an unstyled/headless primitive), so the tier stays commented —
    #   uncommenting it plus adding its derivation branch to level_of() is the whole change.
    {"key": "element",  "label": "Element"},
    {"key": "pattern",  "label": "Pattern"},
    {"key": "block",    "label": "Block"},
    {"key": "shell",    "label": "Shell"},
    {"key": "template", "label": "Template"},
    {"key": "unfiled",  "label": "Unfiled"},   # never hand-tag: a gap shows as a gap
]

# s215-D4 — the definition Dave asked to be visible on the Type tab. ASSEMBLY sense.
PATTERN_DEFINITION = ("Pattern here means an assembly — a component built out of "
                      "several elements and shipped as one thing. It is not the GOV.UK "
                      "sense of a pattern (a recipe for solving a user task).")

LEVEL_NOTE = ("Foundations and Tokens are ladder tiers with no component entries in the "
              "store yet — they are not drawn until they have members.")

# ---------------------------------------------------------------------------
# s215-D5 (2) — STATUS. Release phase, derived at ONE point from TWO mechanical signals:
#   (a) the adopted itinerary measurement (s215-D2): a slug carried by a row derived GATED
#   (b) the component meta's own $status marker: "PROPOSED" / "NOT GATED" / "eye owed"
# stable  = GATED and no PROPOSED marker · beta = anything else · deprecated = a meta that
# says so. ⬛ PROPOSED-FOR-DAVE — this is a DERIVATION, not a ruling. His rulings overwrite
# ONE place: STATUS_OVERRIDES.
# ---------------------------------------------------------------------------
STATUS_OVERRIDES = {}     # slug -> "stable" | "beta" | "deprecated"   ← Dave's rulings land HERE
STATUSES = [
    {"key": "stable",     "label": "Stable"},
    {"key": "beta",       "label": "Beta"},
    {"key": "deprecated", "label": "Deprecated"},
]
STATUS_NOTE = ("Derived, not ruled: stable = gated in the adopted itinerary measurement "
               "and no PROPOSED marker on its meta; beta = everything else.")
PROPOSED_RE = re.compile(r"PROPOSED|NOT GATED|eye owed", re.I)
DEPRECATED_RE = re.compile(r"\bdeprecat", re.I)

# ---------------------------------------------------------------------------
# s215-D4 — THE USAGE GROUPING (the second tab): browse by task, not by construction.
# Derivation order, all mechanical: level (shells/templates are structure) -> per-slug
# override -> the showroom category map -> "Other".
# ---------------------------------------------------------------------------
USAGE_GROUPS = [
    {"key": "actions",    "label": "Actions"},
    {"key": "forms",      "label": "Forms and input"},
    {"key": "navigation", "label": "Navigation"},
    {"key": "feedback",   "label": "Feedback and status"},
    {"key": "data",       "label": "Data display"},
    {"key": "content",    "label": "Content and media"},
    {"key": "commerce",   "label": "Commerce and money"},
    {"key": "structure",  "label": "Structure and layout"},
    {"key": "other",      "label": "Other"},          # a gap shows as a gap
]
CAT_TO_USAGE = {
    "Actions": "actions",
    "Forms and input": "forms",
    "Navigation": "navigation",
    "Feedback and status": "feedback",
    "Data and content": "data",
    "Charts": "data",
    "Identity and display": "content",
}
LEVEL_TO_USAGE = {"shell": "structure", "template": "structure"}

# ⬛ THE JUDGMENT TABLE. Every slug whose usage group is NOT read straight off the category
# map or the level. Entries marked True are PROPOSED-FOR-DAVE in the receipt — the obvious
# assignment was made, and he rules by eye later. Entries marked False are mechanical in
# all but name (the slug says what it is).
USAGE_OVERRIDES = {
    # --- lock-ups (Block) — the category map has none of them ---
    "card-header-lockup":     ("content",   False),
    "cta-lockup":             ("content",   False),
    "feature-grid-lockup":    ("content",   False),
    "footer-doormat-lockup":  ("structure", False),
    "hero-variants":          ("content",   False),
    "page-header-lockup":     ("structure", True),
    "section-heading-lockup": ("structure", True),
    "stats-band-lockup":      ("data",      True),
    "filter-toolbar-bar":     ("forms",     False),   # alias "filter" resolves here
    # --- uncategorised elements ---
    "back-to-top":            ("navigation", False),
    "carousel":               ("content",    False),
    "cascader":               ("forms",      False),
    "document-row":           ("data",       True),
    "fab":                    ("actions",    False),
    "image-block":            ("content",    False),
    "layout-utilities":       ("structure",  False),
    "limits-meter":           ("data",       True),   # banking limits — could read commerce
    "meter":                  ("data",       False),
    "payment-card-visual":    ("commerce",   False),
    "popconfirm":             ("feedback",   False),
    "progress-bar":           ("feedback",   False),
    "qr-code":                ("content",    True),   # payment QR would read commerce
    "range-slider":           ("forms",      False),
    "rating":                 ("content",    True),   # collects input — could read forms
    "runway-bar":             ("data",       True),
    "split-button":           ("actions",    False),
    "splitter":               ("structure",  False),
    "standing-order-mandate-row": ("commerce", False),
    "transaction-row":        ("commerce",   False),
    # --- uncategorised patterns ---
    "calendar":               ("data",       True),   # display or picker — Dave's eye
    "footer":                 ("structure",  False),
    "transfer-list":          ("forms",      False),
    "tree":                   ("navigation", True),   # navigation or data display
    # --- money components sitting under other categories ---
    "account-card":           ("commerce",   True),
    "account-selector":       ("commerce",   True),
    "amount-display":         ("commerce",   True),
    "amount-input":           ("forms",      True),   # money, but it is a form field
    # --- display components that are really structure ---
    "divider":                ("structure",  True),
    "headers":                ("structure",  True),
}

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

# ---------------------------------------------------------------------------
# s215-D5 (4) — RELATED COMPONENTS. Each cluster is a set of components a searcher can
# confuse for one another; the clusters are SEEDED FROM THE ALIAS TABLE (every cluster
# below contains at least two slugs the alias table points different words at, or a pair
# one alias word could plausibly mean). Membership is the only judgment here — the
# one-line disambiguation is GENERATED from each component's own meta `purpose`, so it is
# factual about THIS library and cannot be a borrowed line from another design system.
# ---------------------------------------------------------------------------
RELATED_CLUSTERS = [
    ["dropdown", "combobox", "multi-select", "selection-controls", "cascader"],
    ["modals", "modal-lightbox", "drawer", "popover", "tooltip", "popconfirm", "confirmation"],
    ["toast", "alert", "banner", "notifications", "status-indicator", "badge"],
    ["table", "data-grid", "list-items", "document-row", "transaction-row"],
    ["stepper", "progress-bar", "progress-tracker", "runway-bar", "meter", "limits-meter"],
    ["loading-indicator", "skeleton-loader", "empty-state"],
    ["sidebar-nav", "app-shell-side-nav", "app-shell-nav-rail", "navigations", "tree"],
    ["tabs", "tab-bar", "segmented-control", "anchor-nav"],
    ["avatar", "avatar-group"],
    ["tags", "tags-input", "badge", "eyebrow"],
    ["stat-card", "kpi-tile", "cards", "account-card"],
    ["date-picker", "date-range-picker", "time-picker", "calendar"],
    ["search-field", "command-palette", "filter-toolbar-bar"],
    ["button", "icon-button", "split-button", "fab", "links", "quick-actions"],
    ["amount-display", "amount-input", "payment-card-visual"],
    ["transfer-list", "reorder", "multi-select"],
    ["splitter", "layout-utilities", "divider"],
    ["hero", "hero-variants", "carousel", "image-block"],
    ["accordion", "summary", "timeline"],
]

SCRIPT_RE = re.compile(r"<script\b(?![^>]*id=\"token-manifest\")[^>]*>(.*?)</script>", re.S)
SENTENCE_RE = re.compile(r"^(.+?[.;])(\s|$)")


def js_lines(snippet_src):
    """Mechanical behaviour signal: lines of non-manifest JS the snippet ships."""
    n = 0
    for body in SCRIPT_RE.findall(snippet_src):
        n += len([l for l in body.splitlines() if l.strip()])
    return n


def level_of(slug, meta):
    """s215-D4 ladder, derived. The STORE still says "Lock-up"; the LIBRARY says Block."""
    layer = (meta or {}).get("$layer")
    if layer == "2 Shell":
        return "shell"
    if layer == "2 Template":
        return "template"
    if layer == "2 Lock-up":            # the word survives internally, not in navigation
        return "block"
    cat = (meta or {}).get("category")
    if cat in ("atom", "molecule"):     # single controls -> Element
        return "element"
    if cat == "organism":               # composed components -> Pattern
        return "pattern"
    if cat == "template":
        return "template"
    if slug.startswith("app-shell-"):
        return "shell"
    if slug.startswith("template-"):
        return "template"
    if slug.endswith("-lockup"):
        return "block"
    return "unfiled"


def usage_of(slug, level):
    """Task/purpose grouping. Returns (group_key, is_proposed)."""
    if slug in USAGE_OVERRIDES:
        return USAGE_OVERRIDES[slug]
    if level in LEVEL_TO_USAGE:
        return LEVEL_TO_USAGE[level], False
    cat = showroom.CAT_OF.get(slug)
    if cat in CAT_TO_USAGE:
        return CAT_TO_USAGE[cat], False
    return "other", True


def gated_slugs():
    """Slugs a row of the ADOPTED itinerary measurement (s215-D2) derives as GATED."""
    if not os.path.exists(ITINERARY):
        return None
    d = json.load(open(ITINERARY))
    out = set()
    for row in d.get("rows", []):
        if row.get("derived") == "GATED":
            out.update(row.get("slugs") or [])
    return out


def status_of(slug, meta, gated):
    """s215-D5 (2). ONE derivation point; STATUS_OVERRIDES is the ONE override point."""
    if slug in STATUS_OVERRIDES:
        return STATUS_OVERRIDES[slug]
    marker = str((meta or {}).get("$status") or "")
    if DEPRECATED_RE.search(marker):
        return "deprecated"
    if gated is not None and slug in gated and not PROPOSED_RE.search(marker):
        return "stable"
    return "beta"


def first_sentence(text, cap=150):
    text = " ".join((text or "").split())
    m = SENTENCE_RE.match(text)
    line = m.group(1) if m else text
    if len(line) > cap:
        line = line[:cap - 1].rsplit(" ", 1)[0] + "…"
    return line


def collect():
    """-> (rows, residuals). One row per EXISTING showroom page — the page is the artefact."""
    snippets = {showroom.slug_of(p): p
                for p in glob.glob(os.path.join(SNIP, "*.reference.html"))}
    alias_by_slug = {}
    for a, s in ALIASES.items():
        alias_by_slug.setdefault(s, []).append(a)
    gated = gated_slugs()

    rows, residuals = [], {"no_meta": [], "unfiled": [], "no_behaviour": [], "dead_alias": [],
                           "usage_other": [], "no_thumb": [], "dead_related": [],
                           "itinerary": "read" if gated is not None else "MISSING"}
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
        use, _proposed = usage_of(slug, lvl)
        if use == "other":
            residuals["usage_other"].append(slug)
        jsl = js_lines(open(snippets[slug]).read()) if slug in snippets else 0
        if jsl == 0:
            residuals["no_behaviour"].append(slug)
        purpose = (meta or {}).get("purpose", "") or ""
        thumb = THUMB_REL % slug
        if not os.path.exists(os.path.join(ROOT, "showroom", thumb)):
            residuals["no_thumb"].append(slug)
        rows.append({
            "slug": slug,
            "label": showroom.label_of(slug),
            "cat": showroom.CAT_OF.get(slug, "More"),
            "level": lvl,
            "usage": use,
            "status": status_of(slug, meta, gated),
            "js": jsl,
            "purpose": purpose[:240],
            "blurb": first_sentence(purpose),
            "aliases": sorted(alias_by_slug.get(slug, [])),
            "thumb": thumb,
            "page": slug + ".html",
        })
    have = {r["slug"] for r in rows}
    by_slug = {r["slug"]: r for r in rows}
    residuals["dead_alias"] = sorted({s for s in ALIASES.values() if s not in have})

    # s215-D5 (4) — related, with the disambiguation taken from the NEIGHBOUR's own purpose.
    rel = {}
    dead = set()
    for cluster in RELATED_CLUSTERS:
        for s in cluster:
            if s not in have:
                dead.add(s)
                continue
            for other in cluster:
                if other == s or other not in have:
                    continue
                rel.setdefault(s, {})[other] = by_slug[other]["blurb"]
    residuals["dead_related"] = sorted(dead)
    for r in rows:
        r["related"] = [{"slug": s, "label": by_slug[s]["label"], "line": line}
                        for s, line in sorted(rel.get(r["slug"], {}).items())]
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
nav.tree a:focus-visible, summary:focus-visible, .tab:focus-visible,
.card:focus-visible{outline:2px solid var(--focus); outline-offset:2px;}
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

/* ---- search + tabs, at the TOP OF THE MENU (Dave #214/#215) ---- */
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

/* ---- s215-D4: TWO TABS replace the facet chips ---- */
.tabs{display:flex; gap:0; margin:11px 0 0; border-bottom:1px solid var(--line);}
.tab{font:inherit; font-size:12px; font-weight:500; padding:8px 14px; border:0; cursor:pointer;
  background:transparent; color:var(--mid); border-bottom:2px solid transparent; margin-bottom:-1px;}
.tab[aria-selected="true"]{color:var(--ink); border-bottom-color:var(--ink);}
.tabnote{font-size:11px; color:var(--mid); line-height:1.45; margin:8px 0 0;}

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

/* ---- the trees ---- */
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
nav.tree a[hidden], nav.tree details[hidden], .treepane[hidden]{display:none;}
.recent{padding:10px 14px; border-bottom:1px solid var(--line);}
.recent h2{font-size:11px; font-weight:500; color:var(--mid); margin:0 0 6px; letter-spacing:.04em;
  text-transform:uppercase;}
.recent a{display:block; font-size:12px; color:var(--ink); text-decoration:none; padding:3px 0;}
.recent a:hover{text-decoration:underline;}
.empty{padding:18px 14px; font-size:12px; color:var(--mid);}

/* ---- the main column: gallery OR pane ---- */
main.view{min-width:0; display:flex; flex-direction:column; background:var(--page); min-height:0;}
main.view iframe{border:0; width:100%; flex:1 1 auto; display:none; background:var(--white);}
main.view.on iframe{display:block;}
main.view.on .gallery, main.view.on .intro{display:none;}
main.view:not(.on) .panebar{display:none;}
.panebar{display:flex; gap:12px; align-items:baseline; padding:9px 16px; background:var(--white);
  border-bottom:1px solid var(--line); flex-wrap:wrap;}
.panebar .rel{font-size:11px; color:var(--mid); display:flex; gap:10px; flex-wrap:wrap;
  align-items:baseline;}
.panebar .rel a{color:var(--ink); text-decoration:none; border-bottom:1px solid var(--line);}
.panebar .rel a:hover{border-bottom-color:var(--ink);}
.panebar .rel .sep{color:var(--line);}

.intro{padding:6px 0 10px; max-width:780px; grid-column:1/-1;}
.intro h2{font-size:18px; font-weight:500; margin:0 0 10px;}
.intro p{font-size:13px; color:var(--mid); line-height:1.55; margin:0 0 10px;}
.intro code{font-family:ui-monospace,Menlo,Consolas,monospace; font-size:12px;}
.intro kbd{font:inherit; font-size:11px; border:1px solid var(--line); padding:1px 5px;
  background:var(--white);}

/* ---- s215-D5 (3): thumbnail-first browsing ---- */
.gallery{overflow-y:auto; flex:1 1 auto; padding:20px 24px 40px;
  display:grid; gap:16px; grid-template-columns:repeat(auto-fill, minmax(220px, 1fr));
  align-content:start;}
.card{display:block; background:var(--white); border:1px solid var(--line);
  text-align:left; font:inherit; color:var(--ink); cursor:pointer; padding:0;}
/* ⛔ NO `overflow:hidden` ON THE CARD, and the reason is measured, not stylistic.
   With `overflow:hidden` chromium sized every grid row to 2px — the card's borders — while
   its children still laid out at 200px + 102px (card.scrollHeight 302, offsetHeight 2,
   gridTemplateRows "230px 2px 2px 2px…", measured 2026-08-22). Removing it: 304px, correct.
   Nothing needs clipping anyway: the thumbnail is `object-fit:cover` inside its own box. */
.card:hover{border-color:var(--ink);}
.card[hidden]{display:none;}
.card .shot{display:block; width:100%; aspect-ratio:16/10; object-fit:cover; object-position:top left;
  background:var(--wash); border-bottom:1px solid var(--line);}
.card .noshot{display:flex; align-items:center; justify-content:center; width:100%;
  aspect-ratio:16/10; background:var(--wash); border-bottom:1px solid var(--line);
  font-size:11px; color:var(--mid);}
.card .body{padding:10px 12px 12px;}
.card .nm{font-size:13px; font-weight:500; display:block;}
.card .bl{font-size:11px; color:var(--mid); line-height:1.4; margin:5px 0 0;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;}
.card .tags{display:flex; gap:6px; margin:8px 0 0; align-items:center; flex-wrap:wrap;}
.pillv{font-size:10px; text-transform:uppercase; letter-spacing:.04em; color:var(--mid);}
.pill{font-size:10px; text-transform:uppercase; letter-spacing:.04em; padding:2px 7px;
  border:1px solid var(--line); border-radius:999px; color:var(--mid);}
.pill[data-status="stable"]{border-color:var(--ink); color:var(--ink);}
.pill[data-status="deprecated"]{border-color:var(--mid); color:var(--mid); text-decoration:line-through;}
.galleryempty{grid-column:1/-1; font-size:12px; color:var(--mid);}

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
<title>Apollo component library</title>
__SENTINEL__
<style>__CSS__</style>
</head>
<body>
<header class="app">
  <h1>Apollo component library</h1>
  <span class="count"><strong>__COUNT__</strong> components</span>
  <span class="now" id="now" aria-live="polite"></span>
  <span class="spacer"></span>
  <button class="btn" id="all" type="button" hidden>&#8592; All components</button>
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
    <div class="tabs" role="tablist" aria-label="Browse by">
      <button class="tab" id="tab-type" role="tab" data-tab="type" aria-selected="true"
              aria-controls="tree-type">Type</button>
      <button class="tab" id="tab-usage" role="tab" data-tab="usage" aria-selected="false"
              aria-controls="tree-usage">Usage</button>
    </div>
    <p class="tabnote" id="tabnote-type">__PATTERN_DEF__</p>
    <p class="tabnote" id="tabnote-usage" hidden>Grouped by the job the component does, not by
      how it is built. The same component appears in one usage group only.</p>
    <div class="chips" id="statuses" role="group" aria-label="Filter by release phase">__STATUS_CHIPS__</div>
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
    <div class="treepane" id="tree-type" role="tabpanel" aria-labelledby="tab-type">
__SECTIONS_TYPE__
    </div>
    <div class="treepane" id="tree-usage" role="tabpanel" aria-labelledby="tab-usage" hidden>
__SECTIONS_USAGE__
    </div>
    <p class="empty" id="noresults" hidden>Nothing matches. Try an alias &mdash;
      dropdown, spinner, snackbar, typeahead, facepile, shuttle&hellip;</p>
  </div>
</nav>

<main class="view" id="view">
  <div class="panebar" id="panebar">
    <span class="rel" id="rel"></span>
  </div>
  <div class="gallery" id="gallery">
  <div class="intro">
    <h2>Browse the library</h2>
    <p>Every pane below is the component&rsquo;s own generated showroom page, loaded live &mdash;
      its scripts run, its side-navs open, its tabs switch. Nothing on this page is a re-drawing.</p>
    <p>The controls in the header drive the pane: theme, light/dark and width are broadcast to it
      as a URL fragment, so switching theme never reloads the component.</p>
    <p>Two tabs at the top of the menu: <strong>Type</strong> is the component ladder,
      <strong>Usage</strong> is the job the component does. Release phase filters inside both.</p>
    <p>Search with <kbd>/</kbd> or <kbd>&#8984;K</kbd>. A machine-readable copy of this index is
      <code>showroom/index.json</code>.</p>
  </div>
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
  var LEVEL_LABEL=DATA.levelLabels, USAGE_LABEL=DATA.usageLabels, STATUS_LABEL=DATA.statusLabels;

  var view=document.getElementById('view'), frame=document.getElementById('vframe');
  var q=document.getElementById('q'), qclear=document.getElementById('qclear');
  var rc=document.getElementById('rc'), reset=document.getElementById('reset');
  var noresults=document.getElementById('noresults'), now=document.getElementById('now');
  var wIn=document.getElementById('w'), wv=document.getElementById('wv');
  var openBtn=document.getElementById('open'), replayBtn=document.getElementById('replay');
  var allBtn=document.getElementById('all'), gallery=document.getElementById('gallery');
  var relBox=document.getElementById('rel');
  var state={slug:null, theme:'mono', mode:'light', w:null, tab:'type', statuses:{}, flags:{}, q:''};
  var recent=[];

  /* ---------- the pane: fragment broadcast, exactly the REVIEW-213 mechanism ---------- */
  function frag(){
    var p=['theme='+state.theme,'m='+state.mode];
    if(state.w) p.push('w='+state.w);
    p.push('chrome=0');                       // library view: no second bar, no review overlay
    return '#'+p.join('&');
  }
  function pageURL(slug){ return slug+'.html'+frag(); }
  function retheme(){
    if(!state.slug) return;
    // same document + new fragment => the showroom page's hashchange handler re-themes
    // its srcdoc pane in place. Assigning the whole URL is safe: the path is unchanged.
    frame.src=pageURL(state.slug);
  }
  function drawRelated(slug){
    var r=BY[slug]; relBox.innerHTML='';
    if(!r || !r.related.length){ relBox.textContent='No related components recorded.'; return; }
    var head=document.createElement('span'); head.textContent='Related:'; relBox.appendChild(head);
    r.related.forEach(function(x,i){
      var a=document.createElement('a'); a.href='#c='+x.slug; a.dataset.slug=x.slug;
      a.textContent=x.label; a.title=x.line; relBox.appendChild(a);
      var s=document.createElement('span'); s.className='sep'; s.textContent=x.line;
      relBox.appendChild(s);
      if(i<r.related.length-1){ var d=document.createElement('span'); d.className='sep';
        d.textContent='\\u00b7'; relBox.appendChild(d); }
    });
  }
  function show(slug){
    if(!BY[slug]) return;
    state.slug=slug;
    view.classList.add('on');
    frame.src=pageURL(slug);
    now.textContent=BY[slug].label;
    openBtn.disabled=false; replayBtn.disabled=(BY[slug].js===0);
    replayBtn.title=BY[slug].js===0?'This component ships no behaviour script':'';
    allBtn.hidden=false;
    drawRelated(slug);
    document.querySelectorAll('nav.tree a[data-slug]').forEach(function(a){
      var on=(a.dataset.slug===slug);
      a.setAttribute('aria-current', String(on));
      if(on){ var d=a.closest('details'); if(d) d.open=true; }
    });
    recent=[slug].concat(recent.filter(function(s){return s!==slug;})).slice(0,6);
    drawRecent();
    setHash();
  }
  function showAll(){
    state.slug=null; view.classList.remove('on'); frame.src='about:blank';
    now.textContent=''; openBtn.disabled=true; replayBtn.disabled=true; allBtn.hidden=true;
    document.querySelectorAll('nav.tree a[data-slug]').forEach(function(a){
      a.setAttribute('aria-current','false'); });
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

  /* ---------- s215-D5 (3): the thumbnail gallery ---------- */
  function buildGallery(){
    var frag=document.createDocumentFragment();
    ROWS.forEach(function(r){
      // A DIV with button semantics, not a <button>: the card's content is flow content
      // (a <p>, a <div>), which <button>'s phrasing-only content model does not allow.
      // The keyboard contract is wired below beside the click handler.
      // (⚠ the 2px-tall card this replaced was NOT caused by the element choice — see the
      //  overflow:hidden note in the CSS. Both readings were driven; that one is the cause.)
      var c=document.createElement('div'); c.className='card';
      c.setAttribute('role','button'); c.tabIndex=0;
      c.dataset.slug=r.slug;
      var img=document.createElement('img'); img.className='shot'; img.src=r.thumb;
      img.alt=''; img.loading='lazy'; img.width=320; img.height=200;
      img.addEventListener('error',function(){
        var ph=document.createElement('span'); ph.className='noshot';
        ph.textContent='no thumbnail'; c.replaceChild(ph,img);
      });
      c.appendChild(img);
      var b=document.createElement('div'); b.className='body';
      var n=document.createElement('span'); n.className='nm'; n.textContent=r.label; b.appendChild(n);
      var bl=document.createElement('p'); bl.className='bl'; bl.textContent=r.blurb; b.appendChild(bl);
      var t=document.createElement('div'); t.className='tags';
      var p=document.createElement('span'); p.className='pill'; p.dataset.status=r.status;
      p.textContent=STATUS_LABEL[r.status]||r.status; t.appendChild(p);
      var lv=document.createElement('span'); lv.className='pillv';
      lv.textContent=(LEVEL_LABEL[r.level]||r.level)+' \\u00b7 '+(USAGE_LABEL[r.usage]||r.usage);
      t.appendChild(lv);
      b.appendChild(t); c.appendChild(b); frag.appendChild(c);
    });
    var e=document.createElement('p'); e.className='galleryempty'; e.id='galleryempty';
    e.hidden=true; e.textContent='Nothing matches.'; frag.appendChild(e);
    gallery.appendChild(frag);
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
    var st=activeKeys(state.statuses), fl=activeKeys(state.flags);
    var ok={}, why={}, n=0;
    ROWS.forEach(function(r){
      var m=matches(r, term, hits);
      var pass=m.ok
        && (st.length===0 || st.indexOf(r.status)!==-1)
        && (fl.indexOf('js')===-1 || r.js>0);
      ok[r.slug]=pass; why[r.slug]=pass?m.why:'';
      if(pass) n++;
    });
    document.querySelectorAll('nav.tree a[data-slug]').forEach(function(a){
      var pass=ok[a.dataset.slug];
      a.hidden=!pass;
      a.querySelector('.why').textContent=why[a.dataset.slug]||'';
    });
    document.querySelectorAll('nav.tree details').forEach(function(d){
      var vis=d.querySelectorAll('a[data-slug]:not([hidden])').length;
      d.hidden=(vis===0);
      d.querySelector('.c').textContent=vis;
      if(term||st.length||fl.length) d.open=true;
    });
    gallery.querySelectorAll('.card').forEach(function(c){ c.hidden=!ok[c.dataset.slug]; });
    var ge=document.getElementById('galleryempty'); if(ge) ge.hidden=(n>0);
    noresults.hidden=(n>0);
    rc.textContent=n+' of '+ROWS.length+' shown';
    var dirty=!!(term||st.length||fl.length);
    reset.hidden=!dirty; qclear.style.display=term?'block':'none';
  }

  /* ---------- s215-D4: the two tabs ---------- */
  function setTab(name){
    state.tab=name;
    document.querySelectorAll('.tab').forEach(function(b){
      b.setAttribute('aria-selected', String(b.dataset.tab===name)); });
    document.getElementById('tree-type').hidden=(name!=='type');
    document.getElementById('tree-usage').hidden=(name!=='usage');
    document.getElementById('tabnote-type').hidden=(name!=='type');
    document.getElementById('tabnote-usage').hidden=(name!=='usage');
    setHash();
  }

  /* ---------- wiring ---------- */
  q.addEventListener('input',function(){ state.q=q.value; filter(); });
  q.addEventListener('keydown',function(e){
    if(e.key==='Escape'){ q.value=''; state.q=''; filter(); q.blur(); }
    if(e.key==='Enter'){
      var first=document.querySelector('.treepane:not([hidden]) a[data-slug]:not([hidden])');
      if(first){ show(first.dataset.slug); }
    }
  });
  qclear.addEventListener('click',function(){ q.value=''; state.q=''; filter(); q.focus(); });
  reset.addEventListener('click',function(){
    q.value=''; state.q=''; state.statuses={}; state.flags={};
    document.querySelectorAll('.chip').forEach(function(c){c.setAttribute('aria-pressed','false');});
    filter();
  });
  document.addEventListener('keydown',function(e){
    var typing=/^(INPUT|TEXTAREA|SELECT)$/.test((e.target.tagName||''));
    if((e.key==='/'&&!typing) || (e.key.toLowerCase()==='k'&&(e.metaKey||e.ctrlKey))){
      e.preventDefault(); q.focus(); q.select();
    }
  });
  document.querySelector('.tabs').addEventListener('click',function(e){
    var b=e.target.closest('.tab'); if(!b) return; setTab(b.dataset.tab);
  });
  document.getElementById('statuses').addEventListener('click',function(e){
    var c=e.target.closest('.chip'); if(!c) return;
    var k=c.dataset.status, on=c.getAttribute('aria-pressed')!=='true';
    c.setAttribute('aria-pressed',String(on)); state.statuses[k]=on; filter();
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
  gallery.addEventListener('click',function(e){
    var c=e.target.closest('.card'); if(!c) return; show(c.dataset.slug);
  });
  gallery.addEventListener('keydown',function(e){        // the div-as-button keyboard contract
    var c=e.target.closest('.card'); if(!c) return;
    if(e.key==='Enter'||e.key===' '){ e.preventDefault(); show(c.dataset.slug); }
  });
  relBox.addEventListener('click',function(e){
    var a=e.target.closest('a[data-slug]'); if(!a) return;
    e.preventDefault(); show(a.dataset.slug);
  });
  allBtn.addEventListener('click',showAll);
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
    if(state.slug) window.open(state.slug+'.html'+frag().replace('&chrome=0',''));
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
    p.push('tab='+state.tab);
    p.push('theme='+state.theme); p.push('m='+state.mode);
    history.replaceState(null,'','#'+p.join('&'));
  }
  function initFromHash(){
    var h={}; location.hash.replace(/^#/,'').split('&').forEach(function(kv){
      var p=kv.split('='); if(p[0]) h[p[0]]=decodeURIComponent(p[1]||''); });
    if(h.theme) state.theme=h.theme;
    if(h.m==='light'||h.m==='dark') state.mode=h.m;
    syncSegs();
    setTab(h.tab==='usage'?'usage':'type');
    if(h.c&&BY[h.c]) show(h.c);
  }
  document.getElementById('n-js').textContent=ROWS.filter(function(r){return r.js>0;}).length;
  buildGallery();
  filter(); initFromHash();
})();
</script>
</body>
</html>
"""

STUB_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=../showroom/index.html">
<title>Apollo component library · moved</title>
<style>body{font-family:"Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;
 margin:0; padding:48px 32px; color:#1A1A1A; background:#FAFAFA;}
 p{font-size:14px; line-height:1.6; max-width:60ch;} a{color:#1A1A1A;}</style>
</head>
<body>
<h1 style="font-size:20px;font-weight:500;margin:0 0 12px;">This address moved</h1>
<p>Library v2 <strong>replaced</strong> <code>showroom/index.html</code> at session #215
(ruling <code>s215-D5</code>, decision 1: two indexes would drift). The library now lives at
<a href="../showroom/index.html">showroom/index.html</a>.</p>
<p>This file is a generated redirect, kept so the #214 address cited in
<code>knowledge/_state.json</code> row <code>W-99zg</code> still resolves (WRITE-ONCE
addressing, ADR-0017). It is written by
<code>knowledge/_render/gen_library_214.py</code>; never hand-edit it.</p>
</body>
</html>
"""


def sections_html(rows, groups, key, lvl_label):
    """One <details> per group, in the config's order. Empty groups are not drawn."""
    out = []
    by = {}
    for r in rows:
        by.setdefault(r[key], []).append(r)
    for g in groups:
        items = sorted(by.get(g["key"], []), key=lambda r: r["label"])
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
        out.append('<details open><summary>%s<span class="c">%d</span></summary>%s</details>'
                   % (htmlmod.escape(g["label"]), len(items), links))
    return "\n".join(out)


def build():
    rows, residuals = collect()
    themes = cascade.load_themes()
    btns = "".join(
        '<button data-theme="%s" aria-pressed="%s">%s</button>'
        % (t["attr"], "true" if t["attr"] == "mono" else "false",
           htmlmod.escape(t["label"].replace("Apollo ", "")))
        for t in themes)

    scounts = {}
    for r in rows:
        scounts[r["status"]] = scounts.get(r["status"], 0) + 1
    status_chips = "".join(
        '<button class="chip" data-status="%s" aria-pressed="false" title="%s">%s '
        '<span class="n">%d</span></button>'
        % (s["key"], htmlmod.escape(STATUS_NOTE, quote=True),
           htmlmod.escape(s["label"]), scounts.get(s["key"], 0))
        for s in STATUSES if scounts.get(s["key"], 0))

    lvl_label = {lv["key"]: lv["label"] for lv in LEVELS}
    use_label = {u["key"]: u["label"] for u in USAGE_GROUPS}
    st_label = {s["key"]: s["label"] for s in STATUSES}

    data = json.dumps({"rows": rows, "aliases": ALIASES,
                       "levelLabels": lvl_label, "usageLabels": use_label,
                       "statusLabels": st_label}, sort_keys=True)
    page = (TMPL
            .replace("__CSS__", CSS)
            .replace("__SENTINEL__", INDEX_SENTINEL)
            .replace("__COUNT__", str(len(rows)))
            .replace("__THEME_BTNS__", btns)
            .replace("__PATTERN_DEF__", htmlmod.escape(PATTERN_DEFINITION))
            .replace("__STATUS_CHIPS__", status_chips)
            .replace("__SECTIONS_TYPE__", sections_html(rows, LEVELS, "level", lvl_label))
            .replace("__SECTIONS_USAGE__", sections_html(rows, USAGE_GROUPS, "usage", lvl_label))
            .replace("__DATA__", data))

    # s215-D5 (5) — the machine-readable index, from the SAME pass. Deterministic:
    # rows sorted by slug, keys sorted, no timestamp.
    index = {
        "$generated_by": "knowledge/_render/gen_library_214.py",
        "$ruling": "s215-D4 + s215-D5",
        "$count": len(rows),
        "$levels": [{"key": lv["key"], "label": lv["label"]} for lv in LEVELS],
        "$usage_groups": [{"key": u["key"], "label": u["label"]} for u in USAGE_GROUPS],
        "$statuses": [{"key": s["key"], "label": s["label"]} for s in STATUSES],
        "$status_derivation": STATUS_NOTE,
        "components": [
            {"slug": r["slug"], "name": r["label"], "level": r["level"],
             "level_label": lvl_label[r["level"]], "usage": r["usage"],
             "usage_label": use_label[r["usage"]], "status": r["status"],
             "aliases": r["aliases"],
             "related": [x["slug"] for x in r["related"]],
             "thumbnail": r["thumb"], "page": r["page"],
             "ships_behaviour": r["js"] > 0,
             "blurb": r["blurb"]}
            for r in sorted(rows, key=lambda r: r["slug"])
        ],
    }
    index_json = json.dumps(index, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    return page, index_json, rows, residuals


def selftest():
    fails, ran = [], []

    def bite(name, got, want):
        ran.append(name)
        if got != want:
            fails.append("%s\n     got:  %r\n     want: %r" % (name, got, want))

    page, index_json, rows, residuals = build()
    idx = json.loads(index_json)

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
    # ---- s215-D4 / s215-D5 ----
    bite("10 · s215-D4 · TWO TABS, and the facet chips they replaced are gone",
         ('data-tab="type"' in page and 'data-tab="usage"' in page
          and 'data-level=' not in page), True)
    # ⚠ These two read the NAVIGATION, not the whole file: the embedded JSON island carries
    # every label key, and component `purpose` prose legitimately says "lock-up" inside a
    # title attribute. Testing `in page` measured the payload, not the navigation.
    type_tree = page.split('id="tree-type"', 1)[1].split('id="tree-usage"', 1)[0]
    usage_tree = page.split('id="tree-usage"', 1)[1].split('<p class="empty"', 1)[0]
    nav_groups = re.findall(r"<summary>(.*?)<span", type_tree + usage_tree)
    bite("11 · s215-D4 · the ruled ladder words are the tiers the Type tab draws",
         re.findall(r"<summary>(.*?)<span", type_tree),
         ["Element", "Pattern", "Block", "Shell", "Template"])
    bite("12 · s215-D4 · 'lock-up' is not public navigation (it stays a store signal)",
         [g for g in nav_groups if "ock-up" in g], [])
    bite("13 · s215-D4 · the assembly-sense Pattern definition is on the Type tab",
         PATTERN_DEFINITION.split(" — ")[0] in page, True)
    bite("14 · s215-D5 (2) · every row carries a status from the ruled set",
         sorted({r["status"] for r in rows}) ==
         sorted({s for s in {r["status"] for r in rows}
                 if s in {x["key"] for x in STATUSES}}), True)
    bite("15 · s215-D5 (2) · status has ONE override point and it is empty until Dave rules",
         isinstance(STATUS_OVERRIDES, dict), True)
    bite("16 · s215-D5 (3) · every card addresses a thumbnail under _thumbs/",
         all(r["thumb"] == "_thumbs/" + r["slug"] + ".png" for r in rows), True)
    bite("17 · s215-D5 (4) · related lines are the neighbour's OWN purpose, never invented",
         all(x["line"] == "" or x["line"] == next(o["blurb"] for o in rows if o["slug"] == x["slug"])
             for r in rows for x in r["related"]), True)
    bite("18 · s215-D5 (4) · every related target exists in the library",
         residuals["dead_related"], [])
    bite("19 · s215-D5 (5) · the JSON index has one component per page, sorted by slug",
         (len(idx["components"]),
          [c["slug"] for c in idx["components"]] == sorted(c["slug"] for c in idx["components"])),
         (len(rows), True))
    bite("20 · s215-D5 (5) · the JSON index agrees with the page on every level/status",
         all(c["level"] == next(r["level"] for r in rows if r["slug"] == c["slug"])
             and c["status"] == next(r["status"] for r in rows if r["slug"] == c["slug"])
             for c in idx["components"]), True)
    bite("21 · s215-D5 (1) · this generator owns showroom/index.html and stamps the sentinel",
         (os.path.abspath(OUT) == os.path.abspath(os.path.join(SHOWROOM, "index.html")),
          INDEX_SENTINEL in page), (True, True))
    bite("22 · s215-D5 (1) · gen_showroom no longer emits an index of its own",
         hasattr(showroom, "INDEX_TMPL"), False)
    bite("23 · usage groups are drawn from the ruled group set only",
         sorted({r["usage"] for r in rows}) ==
         sorted({u for u in {r["usage"] for r in rows}
                 if u in {g["key"] for g in USAGE_GROUPS}}), True)

    if fails:
        print("gen_library_214 --selftest: %d BITE(S) FAILED" % len(fails))
        for f in fails:
            print("  ❌ " + f)
        sys.exit(1)
    print("gen_library_214 --selftest OK — %d bites." % len(ran))
    print("   residual · no meta.json: %s" % (residuals["no_meta"] or "none"))
    print("   residual · unfiled level: %s" % (residuals["unfiled"] or "none"))
    print("   residual · usage group 'Other': %s" % (residuals["usage_other"] or "none"))
    print("   residual · missing thumbnail: %d component(s)" % len(residuals["no_thumb"]))
    print("   residual · ships no behaviour script: %d component(s)"
          % len(residuals["no_behaviour"]))


def report(rows, residuals):
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("   status:            %s" % ", ".join("%s %d" % (k, counts[k]) for k in sorted(counts)))
    print("   itinerary source:  %s" % residuals["itinerary"])
    print("   no meta.json:      %s" % (residuals["no_meta"] or "none"))
    print("   unfiled level:     %s" % (residuals["unfiled"] or "none"))
    print("   usage 'Other':     %s" % (residuals["usage_other"] or "none"))
    print("   missing thumbnail: %d — %s"
          % (len(residuals["no_thumb"]), ", ".join(residuals["no_thumb"][:8]) or "none"))
    print("   no behaviour JS:   %d — %s"
          % (len(residuals["no_behaviour"]), ", ".join(residuals["no_behaviour"][:8])))


def main():
    if "--selftest" in sys.argv:
        return selftest()
    page, index_json, rows, residuals = build()
    check = "--check" in sys.argv
    targets = [(OUT, page), (JSON_OUT, index_json), (STUB_OUT, STUB_TMPL)]
    stale = []
    for path, content in targets:
        cur = open(path).read() if os.path.exists(path) else None
        if cur != content:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                open(path, "w").write(content)
    if check:
        if stale:
            print("gen_library_214 --check: OUT OF SYNC — %s\n"
                  "Run: python3 knowledge/_render/gen_library_214.py" % stale)
            sys.exit(1)
        print("gen_library_214 --check OK — %d component(s), index + index.json + stub in sync."
              % len(rows))
        return
    print("gen_library_214: %d component(s) -> %s + %s (%d file(s) written)"
          % (len(rows), os.path.relpath(OUT, ROOT), os.path.relpath(JSON_OUT, ROOT), len(stale)))
    report(rows, residuals)


if __name__ == "__main__":
    main()
