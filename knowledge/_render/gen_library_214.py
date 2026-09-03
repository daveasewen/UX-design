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

WHAT #215 RESTYLED — THE CHROME, AND ONLY THE CHROME
  Dave, 2026-08-22, instructed that the library page be restyled to the Swiss /
  International Style design system (.claude/skills/swiss-design-system/SKILL.md).
  TWO PROJECT SUBSTITUTIONS override the skill's example values, both standing law:
  accent = #DA1A00 (the two-red law, s151-D1) and "black" = #1A1A1A (the ink rule).
  The project grotesque already loaded here is kept, with the skill's fallback chain.
  The restyle touches CSS + the gallery's band structure ONLY: every control, the
  theme broadcast, the #chrome=0 embed contract, both tabs, the status facet, the
  alias search, thumbnails, related strips, index.json and the redirect stub are
  unchanged in behaviour. Bites 24-27 probe the Swiss contract mechanically.
  Receipt: notes/_receipts/2026-08-22-215-library-swiss-restyle.md

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
  BM_MUTANT_DIR=/var/tmp/mut-<session> \
    python3 knowledge/_render/gen_library_214.py --break-groups
      ⬛ #218 — the MUTATION HANDLE over the new tier-nav GROUPING (the Foundations "Grids"
      group). Writes a NON-REPO copy of the index + index.json with the grouping stripped, so
      verify_grids_218.py --group-mutation can drive the group assertions RED BY NAME. It never
      writes over the real index and never writes inside the repo. ⚠ BM_MUTANT_DIR defaults to
      /var/tmp, which is SHARED ACROSS SESSIONS — a foreign mutant is unwritable AND stale, and a
      stale mutant silently proves yesterday's clause. Pass a session-suffixed directory.
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

# ⬛ #218 — THE MUTATION ARM over the new nav grouping. Set by `--break-groups`, which writes a
# NON-REPO copy of the index whose tier nav is drawn FLAT: no group label, no `.grp` wrapper, no
# `group` field in the JSON index. verify_grids_218.py --group-mutation drives that copy and
# REQUIRES the group assertions to fail, by name. A gate that has never been seen to fail is not
# a gate ([[instrument-without-a-consumer]]). It never writes over the real index and never
# writes inside the repo — the destination is BM_MUTANT_DIR (default /var/tmp), which is SHARED
# ACROSS SESSIONS, so a session-suffixed dir is the caller's job.
BREAK_GROUPS = False

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

LEVEL_NOTE = ("Tokens is a ladder tier with no entries yet — it is not drawn until it has "
              "members. Foundations gained its first two entries at #217.")

# ---------------------------------------------------------------------------
# #217 — THE FOUNDATIONS TIER, FILLED. Dave, 2026-08-22, verbatim:
#   "so we need a foundations section in the library with images and logos displayed like
#    the photography bento"
# The Foundations rung of the s215-D4 ladder existed and drew empty (a rung with nothing on it
# is not drawn). These two entries are the first members. They are NOT components: they have no
# snippet, no meta, and no showroom page — which is exactly why they cannot be discovered the
# way component rows are, and why they are declared here.
#
# ⛔ THIS IS THE ONE LIST. knowledge/_render/gen_foundations_217.py IMPORTS it to decide what to
#    build, and knowledge/_render/gen_thumbs.py imports it to decide what to shoot. A second copy
#    anywhere would fork.
#
# ⚠ THE PAGES LIVE IN showroom/_foundations/, AND THE DIRECTORY IS LOAD-BEARING. `collect()`
#    below globs `showroom/*.html` — non-recursive — and so does gen_showroom.py's orphan prune,
#    which DELETES any page in showroom/ with no snippet behind it. A foundation page in
#    showroom/ would be counted as a component by the first and deleted by the second.
#
# ⚠ THESE ROWS ARE ADDITIVE, NOT DERIVED. Every other row in this file is measured off the
#    store; these two are declared. That is a real difference and it is marked on each row as
#    `foundation: True`, so a reader of showroom/index.json can tell them apart.
# ---------------------------------------------------------------------------
FOUNDATIONS = [
    {"slug": "foundation-photography", "label": "Photography",
     "file": "photography.html", "usage": "content",
     "purpose": ("The photography foundation — the committed web derivatives of the "
                 "photography library, laid out as a bento, each opening a zero-JavaScript "
                 "lightbox carrying its EXIF description and licence source. The full set of "
                 "originals stays non-repo; derivatives are minted on demand (s217-D1).")},
    {"slug": "foundation-logos", "label": "Logos",
     "file": "logos.html", "usage": "content",
     "purpose": ("The logo foundation — the exported HSBC lockups in colour and monotone, each "
                 "on the ground its artwork requires. Every fill in every file is hardcoded, so "
                 "no logo follows a theme and each tile is pinned to its own ground.")},
    # #217 — the third entry, and the first Foundations page that is an INSTRUMENT. Ruled home:
    # s217-D5 puts the bento system in Foundations/Layout as a matrix of options over three types.
    {"slug": "foundation-bento", "label": "Bento",
     "file": "bento.html", "usage": "content",
     "purpose": ("The bento foundation — the s217-D5 option matrix, live: three types (Display, "
                 "Gallery, Dashboard) with their ruled spacing, keyline, mode, rounding and "
                 "background dials over real content, in four themes and both modes, exporting "
                 "the chosen combination as concrete values. PROPOSED beyond the ruling's own "
                 "words; nothing on it is promoted.")},
    # ⬛ s219-D3(6) — "THE LIBRARY SURFACES THE FULL EDIT-MODE OPTION SPACE, GENERATED FROM THE
    # RAILS MANIFEST — library, editor and generator read one generated file so none can drift."
    # ⚠ A SIBLING OF `bento.html`, NOT A GROUP. The explorer is the INSTRUMENT (turn the dials);
    # this is the REFERENCE (what the dials offer, and what excludes what). Grouping them would
    # pre-empt the library IA v2 word-set, which is still Dave's open ruling (W-99zg).
    {"slug": "foundation-bento-rails", "label": "Bento rails",
     "file": "bento-rails.html", "usage": "structure",
     "purpose": ("The bento edit-pass rails — every option the edit pass offers per theme and "
                 "type, the ruled CHORDS with a live specimen each, the page-level background "
                 "rail, and the exclusion rules in plain words. Generated from "
                 "knowledge/_render/_bento_edit_rails.json, the one file the library, the editor "
                 "and the generator all read (s219-D3).")},
    # ---------------------------------------------------------------------------
    # #218 — THE GRIDS GROUP. Dave, 2026-08-24, verbatim:
    #   "I think I'd like this added to the library under foundations, we should have a section
    #    called grids with subsections – the 12 col grid and these 3 types, I'd like to keep the
    #    controls so the designer can use them."
    # FOUR SEPARATE PAGES (Dave's own structure pick at the same sitting), each with its type's
    # working dials. `group` is the ONLY new field and it does ONE thing: it puts a label over
    # these four in the tier nav.
    # ⛔ IT IS NOT A NESTING SYSTEM. The library IA v2 word-set is still Dave's OPEN ruling
    #    (_state.json row W-99zg); a general hierarchy built here would pre-empt it. A group is a
    #    flat label over consecutive entries of one tier — nothing else in the file changes shape.
    # ⛔ AND THESE PAGES CARRY NO `PROPOSED` SURFACE. The s217-D5 open points P1–P5 stay on
    #    `bento.html`, which is their LIVE decision surface (row W-126). These four ship the ruled
    #    behaviour plus the working dials, and nothing else.
    # ---------------------------------------------------------------------------
    {"slug": "foundation-grids-12col", "label": "The 12-column grid", "group": "Grids",
     "file": "grids-12col.html", "usage": "structure",
     "purpose": ("The 12-column grid — the RULED layout/web and layout/app tokens rendered "
                 "live: 12 columns, the three web margin/gutter scales and the app pair, over "
                 "canon's own .l-cols / .l-span-* utilities with a column overlay. The scale "
                 "switch is a VIEW control; nothing on this page tunes a token.")},
    {"slug": "foundation-grids-display", "label": "Display grid", "group": "Grids",
     "file": "grids-display.html", "usage": "structure",
     "purpose": ("The Display bento type, live, with its ruled dials — spacing, keylines, page "
                 "and bento background — over the same content and the same maths as the matrix "
                 "explorer, exporting concrete resolved values.")},
    {"slug": "foundation-grids-gallery", "label": "Gallery grid", "group": "Grids",
     "file": "grids-gallery.html", "usage": "structure",
     "purpose": ("The Gallery bento type, live, with its ruled dials — spacing, keylines (absent "
                 "in console), justified-rows or gallery-bento mode, ragged or square bottom "
                 "edge, console image rounding, and the page/bento/caption background palette.")},
    {"slug": "foundation-grids-dashboard", "label": "Dashboard grid", "group": "Grids",
     "file": "grids-dashboard.html", "usage": "structure",
     "purpose": ("The Dashboard bento type, live — a bento of bentos, with the main-wall spacing "
                 "(never tight), the s217-D6 snapping sub-bento slider, and the s217-D8 / #218 "
                 "keyline construction: every module boxed, the corner tiles carrying the "
                 "sub-bento's radius on their outer corner, and no line in any gutter.")},
]
FOUNDATION_DIR = "_foundations"
# #218 — the group labels, in the order they are drawn under their tier. Ungrouped entries are
# drawn FIRST, in their existing order; a group is a labelled run beneath them.
FOUNDATION_GROUPS = ["Grids"]

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

# #245 (s245-D1..D5 populate): the #behaviour-manifest JSON block gen_component_partials.py derives
# beside #token-manifest is DATA, not behaviour — without the type exclusion it counted as JS lines
# and 6 passive components (account-card, action-bar, badge, confirmation, eyebrow, summary) flipped
# to ships_behaviour:true the moment their metas were typed. Exclude the CLASS (application/json).
SCRIPT_RE = re.compile(r"<script\b(?![^>]*id=\"token-manifest\")(?![^>]*type=\"application/json\")[^>]*>(.*?)</script>", re.S)
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


# ---------------------------------------------------------------------------
# ★ #221 — THE META REFERENCE IS NORMALISED, BECAUSE A LOWERCASE SLUG IS NOT A FILENAME.
#
# `collect()` built the meta path as `slug + ".meta.json"` and asked `os.path.exists`. Seven
# metas are committed with a CAPITAL prefix (`Chart-boxplot.meta.json` …) while their showroom
# pages, and therefore their slugs, are lowercase. On Dave's case-insensitive APFS that resolved;
# on Linux — which is what all three CI jobs and every shipped-pack designer run — it MISSED, and
# `level_of()` fell through to `"unfiled"` while `blurb` fell to `""`. Same commit, two different
# artefacts: a bogus seventh ladder tier, Pattern 33 -> 26, "Ladder tiers" reading 7 not 6.
# Single-variable isolation (#221): `collect()` run twice, changing only META to a genuinely
# case-sensitive copy, differed in EXACTLY those 7 rows and nothing else.
# [[gate-cannot-pass-in-one-environment]] in the shape where the ARTEFACT differs, not the verdict.
#
# ⛔ The reference is normalised HERE; the seven FILENAMES are not renamed. Whether they should be
# is Dave's — every `Chart-*.reference.html` snippet is capitalised too, so the casing may be a
# convention this generator cannot see. `--casing` (ADVISORY) names them so the question is
# visible instead of silent, and `residuals["meta_case"]` carries them into the residual report.
# ---------------------------------------------------------------------------
_META_INDEX = {}


def _meta_index(meta_dir=None):
    """`{casefolded name: real name}` for `META`, listed once. Case is PRESERVED by `listdir` on
    every filesystem, so this comparison means the same thing on APFS and on ext4."""
    d = meta_dir or META
    if d not in _META_INDEX:
        try:
            names = os.listdir(d)
        except OSError as exc:                                 # a crash is not a fail
            raise RuntimeError("REFUSED, NAMED: cannot list the component meta directory %s (%s)"
                               % (d, exc))
        _META_INDEX[d] = {n.lower(): n for n in names if n.endswith(".meta.json")}
    return _META_INDEX[d]


def resolve_meta(slug, meta_dir=None):
    """`(path_or_None, exact_case)` for `<slug>.meta.json`.

    Exact case wins. A meta that resolves only case-insensitively is STILL RESOLVED — the index
    must not depend on the filesystem it is generated on — but it is returned with
    `exact_case=False` so the caller can DECLARE it rather than skip it in silence.
    """
    d = meta_dir or META
    want = slug + ".meta.json"
    exact = os.path.join(d, want)
    idx = _meta_index(d)
    if idx.get(want.lower()) == want:
        return exact, True
    real = idx.get(want.lower())
    if real is None:
        return None, False
    return os.path.join(d, real), False


def casing_mismatches(meta_dir=None):
    """`[(slug, filename_on_disk)]` — every showroom slug whose meta filename differs in CASE.

    Pure string comparison over a directory listing, so it returns the same answer on a
    case-insensitive and a case-sensitive filesystem. That is the point: the defect it names is
    invisible to `os.path.exists` on exactly one of the two.
    """
    out = []
    for page in sorted(glob.glob(os.path.join(SHOWROOM, "*.html"))):
        slug = os.path.basename(page)[:-5]
        if slug == "index":
            continue
        path, exact = resolve_meta(slug, meta_dir)
        if path is not None and not exact:
            out.append((slug, os.path.basename(path)))
    return out


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
                           "no_foundation_page": [], "meta_case": [],
                           "itinerary": "read" if gated is not None else "MISSING"}
    for page in sorted(glob.glob(os.path.join(SHOWROOM, "*.html"))):
        slug = os.path.basename(page)[:-5]
        if slug == "index":
            continue
        mpath, exact_case = resolve_meta(slug)       # #221 — normalised, never filesystem-dependent
        meta = None
        if mpath is not None:
            meta = json.load(open(mpath))
            if not exact_case:
                residuals["meta_case"].append((slug, os.path.basename(mpath)))
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
            "foundation": False,          # #217 — component rows are DERIVED, foundations declared
            "group": None,                # #218 — a component row carries no group label
        })
    # #217 — the Foundations tier's declared members, appended AFTER the derived component rows
    # so `residuals` above counts components only and the two populations never blur.
    for f in FOUNDATIONS:
        page_rel = "%s/%s" % (FOUNDATION_DIR, f["file"])
        if not os.path.exists(os.path.join(SHOWROOM, FOUNDATION_DIR, f["file"])):
            residuals["no_foundation_page"].append(f["slug"])
        thumb = THUMB_REL % f["slug"]
        if not os.path.exists(os.path.join(SHOWROOM, thumb)):
            residuals["no_thumb"].append(f["slug"])
        rows.append({
            "slug": f["slug"], "label": f["label"], "cat": "Foundations",
            "level": "foundation", "usage": f["usage"],
            # Not in the itinerary measurement and carrying no meta, so status_of derives
            # "beta" — stated by the same derivation as every other row, not asserted here.
            "status": status_of(f["slug"], None, gated),
            "js": 0, "purpose": f["purpose"][:240], "blurb": first_sentence(f["purpose"]),
            "aliases": sorted(alias_by_slug.get(f["slug"], [])),
            "thumb": thumb, "page": page_rel, "foundation": True,
            # #218 — declared on the entry, carried here, drawn by sections_html(). None = no
            # label, which is what every entry before #218 has and keeps.
            "group": f.get("group"),
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
/* ===========================================================================
   SWISS / INTERNATIONAL STYLE CHROME — restyled #215 at Dave's instruction.
   Contract: .claude/skills/swiss-design-system/SKILL.md, with TWO project
   substitutions that OVERRIDE the skill's example values:
     · accent  #DA1A00  — the two-red law s151-D1 (THE red on white). The skill's
       own example red is NOT used anywhere on this page.
     · "black" #1A1A1A  — the ink rule: blackest, never pure black.
   Font: the project grotesque this chrome already loaded is KEPT, with the
   skill's fallback chain appended.
   ⛔ CHROME ONLY. Not one byte of component CSS lives here — every specimen is a
   framed load of its own generated showroom page (the specimen rule, #202).
   DARK MODE: the header's Light/Dark switch is a PANE broadcast (it re-themes the
   iframe by URL fragment); the chrome itself has never followed it and does not
   now. Swiss chrome is white-ground by design, so the light chrome is kept in
   both modes — no dark-ground accent swap is needed, so the two-red law's
   else-arm (the error-family red for dark grounds) is not reached.
   =========================================================================== */
:root{
  /* --- core, project-substituted --- */
  --accent:#DA1A00;              /* s151-D1 two-red law: 5.09:1 on white, AA normal text */
  --ink:#1A1A1A;                 /* the ink rule: 17.40:1 on white */
  --white:#FFFFFF;
  /* --- neutrals, straight from the skill --- */
  --grey-1:#F3F3F3;  /* contained section grounds */
  --grey-2:#EDEDED;  /* hairline rules, grid gaps */
  --grey-3:#D7D8D6;  /* secondary borders */
  --grey-4:#B7B7B7;  /* DECORATIVE ONLY — 2.01:1, never text */
  --grey-5:#9B9B9B;  /* DECORATIVE ONLY — 2.78:1, never text */
  --grey-6:#767676;  /* 4.54:1 on WHITE only — fails at 4.09:1 on grey-1 */
  --grey-7:#545454;  /* 7.57:1 white · 6.82:1 grey-1 — the safe secondary ink */
  --grey-8:#333333;
  /* --- aliases the chrome reads --- */
  --page:var(--white); --line:var(--grey-2); --mid:var(--grey-7); --wash:var(--grey-1);
  /* --- 8px spacing system --- */
  --s1:0.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem; --s7:6rem;
  --face:"Univers Next for HSBC","Helvetica Neue",Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box;}
html,body{height:100%;}
body{margin:0; font-family:var(--face); background:var(--page); color:var(--ink);
  -webkit-font-smoothing:antialiased; display:flex; flex-direction:column;
  font-size:16px; line-height:1.7;}

/* ---- THE LABEL PATTERN (skill): accent dash + uppercase eyebrow. The page's
   accent budget: section labels in the main column + the active tab underline.
   Sidebar and pane sub-sections use the GREY variant, so one scan never shows
   the accent in more than 2-3 places. ---- */
.label{font-size:12px; font-weight:500; letter-spacing:0.14em; text-transform:uppercase;
  color:var(--accent); display:flex; align-items:center; gap:var(--s1); margin:0 0 var(--s3);}
.label::before{content:''; display:inline-block; width:20px; height:1px; background:var(--accent);}
.sublabel{font-size:12px; font-weight:500; letter-spacing:0.14em; text-transform:uppercase;
  color:var(--grey-7); display:flex; align-items:center; gap:var(--s1); margin:0 0 var(--s1);}
.sublabel::before{content:''; display:inline-block; width:16px; height:1px; background:var(--grey-3);}

/* ---- THE TRUE HEADER (Dave #214) — the skill's nav bar: white, 1px hairline
   bottom border, wordmark left, controls right. No radius, no shadow. ---- */
/* ⚠ `flex:0 0 auto` is LOAD-BEARING, measured 2026-08-22: body is a flex COLUMN, so the
   header is a flex item. With the default `flex-shrink:1` and `min-height:56px` the header
   box stayed 56px tall while its wrapped second row laid out at y=70 — the Open button
   painted OVER the sidebar's search field. Not shrinking, it grows to hold its rows. */
header.app{display:flex; gap:var(--s2); align-items:center; flex-wrap:wrap; flex:0 0 auto;
  padding:var(--s1) var(--s3); min-height:56px; background:var(--white);
  border-bottom:1px solid var(--line); position:sticky; top:0; z-index:20;}
header.app h1{font-size:19px; font-weight:500; line-height:1.2; margin:0; white-space:nowrap;
  letter-spacing:0;}
header.app .count{font-size:12px; font-weight:400; letter-spacing:0.12em; text-transform:uppercase;
  color:var(--grey-7); font-variant-numeric:tabular-nums;}
header.app .count strong{font-weight:500; color:var(--ink);}
header.app .spacer{flex:1 1 auto;}
header.app .now{font-size:14px; font-weight:500; letter-spacing:0.04em; max-width:26ch;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
.ctl{display:flex; gap:var(--s1); align-items:center; font-size:12px; letter-spacing:0.12em;
  text-transform:uppercase; color:var(--grey-7);}

/* segmented control — 1px ink box, active cell = ink fill (the skill's primary button) */
.seg{display:inline-flex; border:1px solid var(--ink);}
.seg button{font:inherit; font-family:var(--face); font-size:12px; font-weight:500;
  letter-spacing:0.06em; text-transform:uppercase; padding:var(--s1) 12px; border:0;
  background:transparent; color:var(--ink); cursor:pointer; border-right:1px solid var(--grey-3);}
.seg button:last-child{border-right:0;}
.seg button:hover{background:var(--grey-1);}
.seg button[aria-pressed="true"]{background:var(--ink); color:var(--white);}
.seg button[aria-pressed="true"]:hover{background:var(--grey-8);}

/* ghost button (skill): no fill, no radius, 1px bottom rule. The rule is INK, not
   accent — the accent budget is spent on the label pattern and the active tab. */
.btn{font:inherit; font-family:var(--face); font-size:12px; font-weight:500;
  letter-spacing:0.06em; text-transform:uppercase; padding:var(--s1) 0; border:0;
  border-bottom:1px solid var(--ink); background:transparent; color:var(--ink); cursor:pointer;}
.btn:hover:not(:disabled){color:var(--grey-8); border-bottom-color:var(--grey-8);}
.btn:disabled{color:var(--grey-6); border-bottom-color:var(--grey-3); cursor:default;}
/* one focus treatment, ink, everywhere — 17.40:1 on white */
.seg button:focus-visible, .btn:focus-visible, input:focus-visible, .chip:focus-visible,
nav.tree a:focus-visible, summary:focus-visible, .tab:focus-visible,
.card:focus-visible{outline:2px solid var(--ink); outline-offset:2px;}
#w{width:132px; accent-color:var(--ink);}
#wv{font-size:12px; letter-spacing:0.06em; font-variant-numeric:tabular-nums; min-width:6ch;
  color:var(--ink);}

/* ---- shell ---- */
.shell{display:grid; grid-template-columns:320px 1fr; flex:1 1 auto; min-height:0;}
nav.tree{border-right:1px solid var(--line); background:var(--white); overflow-y:auto;
  display:flex; flex-direction:column; min-height:0;}

/* ---- search + tabs, at the TOP OF THE MENU (Dave #214/#215) ---- */
.find{position:sticky; top:0; background:var(--white); z-index:5;
  padding:var(--s3) var(--s2) var(--s2); border-bottom:1px solid var(--line);}
.searchwrap{position:relative;}
#q{width:100%; font:inherit; font-family:var(--face); font-size:14px; line-height:1.5;
  padding:10px 32px 10px 12px; border:1px solid var(--ink); border-radius:0;
  background:var(--white); color:var(--ink); letter-spacing:0;}
#q::placeholder{color:var(--grey-6);}   /* 4.54:1 on white */
/* the UA's own search-clear would sit beside ours — two × in one field (seen in the
   820px render, 2026-08-21). One clear affordance, and it is the one we wired. */
#q::-webkit-search-cancel-button, #q::-webkit-search-decoration{-webkit-appearance:none; display:none;}
#qclear{position:absolute; right:1px; top:1px; bottom:1px; width:30px; border:0; cursor:pointer;
  background:transparent; color:var(--grey-7); font:inherit; font-family:var(--face);
  font-size:16px; display:none;}
#qclear:hover{color:var(--ink);}
.find .hint{font-size:12px; line-height:1.5; color:var(--grey-7); margin:var(--s1) 0 0;}

/* ---- s215-D4: TWO TABS — the skill's nav pattern. Active = ACCENT underline
   (the one structural accent moment besides the label pattern). ---- */
.tabs{display:flex; gap:var(--s4); margin:var(--s3) 0 0; border-bottom:1px solid var(--line);}
.tab{font:inherit; font-family:var(--face); font-size:14px; font-weight:500; letter-spacing:0.06em;
  text-transform:uppercase; padding:0 0 10px; border:0; cursor:pointer; background:transparent;
  color:var(--grey-7); border-bottom:2px solid transparent; margin-bottom:-1px;}
.tab:hover{color:var(--ink);}
.tab[aria-selected="true"]{color:var(--ink); border-bottom-color:var(--accent);}
.tabnote{font-size:12px; color:var(--grey-7); line-height:1.55; margin:var(--s2) 0 0;}

.chips{display:flex; flex-wrap:wrap; gap:var(--s1); margin:var(--s2) 0 0;}
.chip{font:inherit; font-family:var(--face); font-size:12px; letter-spacing:0.06em;
  text-transform:uppercase; padding:4px 10px; border:1px solid var(--grey-3); border-radius:0;
  background:var(--white); color:var(--grey-7); cursor:pointer;
  display:inline-flex; gap:var(--s1); align-items:baseline;}
.chip .n{color:var(--grey-7); font-variant-numeric:tabular-nums;}
.chip:hover{border-color:var(--ink); color:var(--ink);}
.chip[aria-pressed="true"]{background:var(--ink); color:var(--white); border-color:var(--ink);}
.chip[aria-pressed="true"] .n{color:var(--white); opacity:.75;}
.resultline{font-size:12px; letter-spacing:0.06em; text-transform:uppercase; color:var(--grey-7);
  margin:var(--s2) 0 0; display:flex; gap:var(--s2); align-items:baseline;}
.resultline button{font:inherit; font-family:var(--face); font-size:12px; letter-spacing:0.06em;
  text-transform:uppercase; border:0; background:transparent; padding:0 0 1px; color:var(--ink);
  border-bottom:1px solid var(--ink); cursor:pointer;}

/* ---- the trees ---- */
.treescroll{overflow-y:auto; flex:1 1 auto; padding-bottom:var(--s4);}
nav.tree details{border-bottom:1px solid var(--line);}
nav.tree summary{font-size:12px; font-weight:500; letter-spacing:0.12em; text-transform:uppercase;
  padding:12px var(--s2); cursor:pointer; list-style:none; display:flex; align-items:baseline;
  gap:var(--s1); color:var(--ink);}
nav.tree summary:hover{background:var(--grey-1);}
nav.tree summary::-webkit-details-marker{display:none;}
nav.tree summary::before{content:"\\25B8"; font-size:9px; color:var(--grey-5); transition:transform 140ms;}
nav.tree details[open] summary::before{transform:rotate(90deg);}
nav.tree summary .c{margin-left:auto; font-size:12px; letter-spacing:0.06em; color:var(--grey-7);
  font-variant-numeric:tabular-nums;}
nav.tree a{display:flex; gap:var(--s1); align-items:baseline; font-size:14px; line-height:1.5;
  color:var(--ink); text-decoration:none; padding:var(--s1) var(--s2) var(--s1) var(--s4);
  border-left:2px solid transparent;}
nav.tree a:hover{background:var(--grey-1);}
nav.tree a[aria-current="true"]{border-left-color:var(--ink); font-weight:500; background:var(--grey-1);}
nav.tree a .lvl{margin-left:auto; font-size:12px; letter-spacing:0.06em; color:var(--grey-7);
  white-space:nowrap;}
nav.tree a .why{font-size:12px; color:var(--grey-7);}
/* #218 — a GROUP inside a tier: one label over a run of entries. Indented one step past the
   tier's own links so the relationship reads without a second disclosure widget. */
nav.tree .grp{border-top:1px solid var(--line);}
nav.tree .grpl{display:flex; align-items:baseline; gap:var(--s1); font-size:12px; font-weight:500;
  letter-spacing:0.12em; text-transform:uppercase; color:var(--grey-7);
  padding:10px var(--s2) 6px var(--s3);}
nav.tree .grpl .c{margin-left:auto; letter-spacing:0.06em; font-variant-numeric:tabular-nums;}
nav.tree .grp a{padding-left:var(--s5);}
nav.tree a[hidden], nav.tree details[hidden], nav.tree .grp[hidden], .treepane[hidden]{display:none;}
.recent{padding:var(--s2); border-bottom:1px solid var(--line);}
.recent h2{margin:0 0 var(--s1);}
.recent a{display:block; font-size:14px; color:var(--ink); text-decoration:none; padding:2px 0;}
.recent a:hover{text-decoration:underline;}
.empty{padding:var(--s3) var(--s2); font-size:14px; line-height:1.6; color:var(--grey-7);}

/* ---- the main column: gallery OR pane ---- */
main.view{min-width:0; display:flex; flex-direction:column; background:var(--white); min-height:0;}
main.view iframe{border:0; width:100%; flex:1 1 auto; display:none; background:var(--white);}
main.view.on iframe{display:block;}
main.view.on .gallery{display:none;}
main.view:not(.on) .panebar{display:none;}
.panebar{display:flex; gap:var(--s3); align-items:baseline; padding:var(--s2) var(--s3);
  background:var(--white); border-bottom:1px solid var(--line); flex-wrap:wrap;}
.panebar .rel{font-size:12px; color:var(--grey-7); display:flex; gap:var(--s2); flex-wrap:wrap;
  align-items:baseline;}
.panebar .rel .relhead{font-weight:500; letter-spacing:0.14em; text-transform:uppercase;
  color:var(--grey-7);}
.panebar .rel a{color:var(--ink); text-decoration:none; border-bottom:1px solid var(--grey-3);}
.panebar .rel a:hover{border-bottom-color:var(--ink);}
.panebar .rel .sep{color:var(--grey-7);}

/* ---- the gallery: SWISS BANDS. A full-width opener, then a 3-column split, then
   the card grid on a grey-1 ground — never the same grid three sections running,
   and every band closed by a full-width 1px hairline RULE, not a gap. ---- */
.gallery{overflow-y:auto; flex:1 1 auto; display:block; padding:0;}
.band{padding:var(--s6) var(--s5); border-bottom:1px solid var(--line); max-width:1200px;}
.band:last-child{border-bottom:0;}
.band h2{font-size:34px; font-weight:400; line-height:1.15; letter-spacing:-0.01em;
  margin:0 0 var(--s4); max-width:20ch;}
.band p.lead{font-size:19px; font-weight:400; line-height:1.5; color:var(--ink); margin:0;
  max-width:34ch;}

/* stat display (skill): head1 numerals at ultra-light, caption labels beneath */
.stats{display:grid; grid-template-columns:repeat(4, minmax(0,1fr)); gap:var(--s4);
  border-top:1px solid var(--line); padding-top:var(--s4);}
.stat .n{display:block; font-size:43px; font-weight:200; line-height:1.05; letter-spacing:0;
  color:var(--ink); font-variant-numeric:tabular-nums;}
.stat .k{display:block; font-size:12px; font-weight:400; letter-spacing:0.12em;
  text-transform:uppercase; color:var(--grey-7); margin-top:var(--s1); line-height:1.5;}

/* proposition split (skill): 3fr | 1fr divider | 4fr */
.split{display:grid; grid-template-columns:3fr 1fr 4fr; gap:var(--s5); align-items:start;}
.split .vrule{border-left:1px solid var(--line); min-height:120px; height:100%;}
.note{border-top:1px solid var(--line); padding-top:var(--s2); margin-top:var(--s4);}
.note:first-child{border-top:0; padding-top:0; margin-top:0;}
.note .ix{display:block; font-size:34px; font-weight:200; line-height:1;
  color:var(--grey-4); margin-bottom:var(--s1);}   /* DECORATIVE index numeral — skill exemption */
.note h3{font-size:19px; font-weight:500; line-height:1.2; margin:0 0 var(--s1);}
.note p{font-size:16px; line-height:1.75; color:var(--ink); margin:0;}
.note code{font-family:ui-monospace,Menlo,Consolas,monospace; font-size:14px;}
.note kbd{font:inherit; font-family:var(--face); font-size:12px; border:1px solid var(--grey-3);
  padding:1px 6px; background:var(--white);}

/* ---- s215-D5 (3): thumbnail-first browsing — the skill's feature grid.
   grey-1 ground, 1px grey-2 gaps between white cells, no radius, no shadow. ---- */
.gridband{background:var(--grey-1); max-width:none;}
.cardgrid{display:grid; gap:1px; background:var(--grey-2); border:1px solid var(--grey-2);
  grid-template-columns:repeat(auto-fill, minmax(220px, 1fr)); align-content:start;}
.card{display:block; background:var(--white); border:0; border-radius:0;
  text-align:left; font:inherit; font-family:var(--face); color:var(--ink); cursor:pointer;
  padding:0; position:relative;}
/* ⛔ NO `overflow:hidden` ON THE CARD, and the reason is measured, not stylistic.
   With `overflow:hidden` chromium sized every grid row to 2px — the card's borders — while
   its children still laid out at 200px + 102px (card.scrollHeight 302, offsetHeight 2,
   gridTemplateRows "230px 2px 2px 2px…", measured 2026-08-22). Removing it: 304px, correct.
   Nothing needs clipping anyway: the thumbnail is `object-fit:cover` inside its own box. */
.card:hover{outline:1px solid var(--ink); z-index:1;}
.card[hidden]{display:none;}
.card .shot{display:block; width:100%; aspect-ratio:16/10; object-fit:cover; object-position:top left;
  background:var(--grey-1); border-bottom:1px solid var(--grey-2);}
.card .noshot{display:flex; align-items:center; justify-content:center; width:100%;
  aspect-ratio:16/10; background:var(--grey-1); border-bottom:1px solid var(--grey-2);
  font-size:12px; letter-spacing:0.06em; text-transform:uppercase; color:var(--grey-7);}
.card .body{padding:var(--s2);}
.card .nm{font-size:14px; font-weight:500; line-height:1.4; display:block;}
.card .bl{font-size:12px; color:var(--grey-7); line-height:1.5; margin:var(--s1) 0 0;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;}
.card .tags{display:flex; gap:var(--s1); margin:var(--s2) 0 0; align-items:center; flex-wrap:wrap;}
.pillv{font-size:12px; letter-spacing:0.06em; text-transform:uppercase; color:var(--grey-7);}
.pill{font-size:12px; text-transform:uppercase; letter-spacing:0.06em; padding:1px 8px;
  border:1px solid var(--grey-3); border-radius:0; color:var(--grey-7);}
.pill[data-status="stable"]{border-color:var(--ink); color:var(--ink);}
.pill[data-status="deprecated"]{border-color:var(--grey-6); color:var(--grey-7); text-decoration:line-through;}
.galleryempty{font-size:14px; color:var(--grey-7); margin:var(--s3) 0 0;}

@media (max-width:1100px){
  .split{grid-template-columns:1fr; gap:var(--s4);}
  .split .vrule{display:none;}
  .stats{grid-template-columns:repeat(2, minmax(0,1fr));}
}
@media (max-width:820px){
  .shell{grid-template-columns:1fr;}
  nav.tree{border-right:0; border-bottom:1px solid var(--line); max-height:46vh;}
  .band{padding:var(--s5) var(--s3);}
  .band h2{font-size:27px;}
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
  <span class="count"><strong>__COUNT__</strong> components &middot;
    <strong>__FCOUNT__</strong> foundations</span>
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
    <h2 class="sublabel">Recently opened</h2>
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
    <section class="band" id="intro">
      <p class="label">The library</p>
      <h2>Every component, live on its own page</h2>
      <div class="stats">
        <div class="stat"><span class="n">__COUNT__</span><span class="k">Components</span></div>
        <div class="stat"><span class="n">__STAT_TIERS__</span><span class="k">Ladder tiers</span></div>
        <div class="stat"><span class="n">__STAT_USAGE__</span><span class="k">Usage groups</span></div>
        <div class="stat"><span class="n">__STAT_JS__</span><span class="k">Ship behaviour</span></div>
      </div>
    </section>
    <section class="band split">
      <div>
        <p class="label">How it works</p>
        <p class="lead">Nothing on this page is a re-drawing. Every pane is the component&rsquo;s
          own generated showroom page, loaded live.</p>
      </div>
      <div class="vrule" aria-hidden="true"></div>
      <div>
        <div class="note"><span class="ix">01</span>
          <h3>Live pages, not pictures</h3>
          <p>Each pane loads the component&rsquo;s generated showroom page, so its scripts run,
            its side-navs open and its tabs switch.</p></div>
        <div class="note"><span class="ix">02</span>
          <h3>The header drives the pane</h3>
          <p>Theme, light/dark and width are broadcast to the pane as a URL fragment, so switching
            theme never reloads the component.</p></div>
        <div class="note"><span class="ix">03</span>
          <h3>Two ways in</h3>
          <p><strong>Type</strong> is the component ladder; <strong>Usage</strong> is the job the
            component does. Release phase filters inside both. Search with <kbd>/</kbd> or
            <kbd>&#8984;K</kbd>; a machine-readable copy of this index is
            <code>showroom/index.json</code>.</p></div>
      </div>
    </section>
    <section class="band gridband">
      <p class="label">All components</p>
      <div class="cardgrid" id="cardgrid"></div>
      <p class="galleryempty" id="galleryempty" hidden>Nothing matches.</p>
    </section>
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
  // #217 — the row OWNS its page address. Component rows say "<slug>.html"; Foundations rows
  // say "_foundations/<name>.html", a directory deeper. Reconstructing the URL from the slug
  // (which this did until #217) would send every Foundations pane to a 404.
  function pageURL(slug){ return BY[slug].page+frag(); }
  function retheme(){
    if(!state.slug) return;
    // same document + new fragment => the showroom page's hashchange handler re-themes
    // its srcdoc pane in place. Assigning the whole URL is safe: the path is unchanged.
    frame.src=pageURL(state.slug);
  }
  function drawRelated(slug){
    var r=BY[slug]; relBox.innerHTML='';
    if(!r || !r.related.length){ relBox.textContent='No related components recorded.'; return; }
    var head=document.createElement('span'); head.className='relhead';
    head.textContent='Related'; relBox.appendChild(head);
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
    document.getElementById('cardgrid').appendChild(frag);
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
    // #218 — a group label with nothing under it is a lie about the filter. The group hides
    // with its last visible member, and its own count follows the filter like the tier's does.
    document.querySelectorAll('nav.tree .grp').forEach(function(g){
      var vis=g.querySelectorAll('a[data-slug]:not([hidden])').length;
      g.hidden=(vis===0);
      var c=g.querySelector('.grpl .c'); if(c) c.textContent=vis;
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
    if(state.slug) window.open(BY[state.slug].page+frag().replace('&chrome=0',''));
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
<title>Apollo component library &middot; moved</title>
<style>
:root{--ink:#1A1A1A; --accent:#DA1A00; --grey-2:#EDEDED; --grey-7:#545454;
 --face:"Univers Next for HSBC","Helvetica Neue",Helvetica,Arial,sans-serif;}
body{font-family:var(--face); margin:0; padding:64px 48px; color:var(--ink);
 background:#FFFFFF; font-size:16px; line-height:1.7;}
.wrap{max-width:1200px;}
.label{font-size:12px; font-weight:500; letter-spacing:0.14em; text-transform:uppercase;
 color:var(--accent); display:flex; align-items:center; gap:8px; margin:0 0 24px;}
.label::before{content:''; display:inline-block; width:20px; height:1px; background:var(--accent);}
h1{font-size:34px; font-weight:400; line-height:1.15; letter-spacing:-0.01em; margin:0 0 32px;
 max-width:20ch;}
p{max-width:60ch; margin:0 0 16px;}
.rule{border-top:1px solid var(--grey-2); margin:32px 0; max-width:1200px;}
.meta{font-size:12px; color:var(--grey-7); line-height:1.6;}
a{color:var(--ink); text-decoration:none; border-bottom:1px solid var(--ink);}
code{font-family:ui-monospace,Menlo,Consolas,monospace; font-size:14px;}
</style>
</head>
<body>
<div class="wrap">
<p class="label">Moved</p>
<h1>This address now points at the library</h1>
<p>Library v2 <strong>replaced</strong> <code>showroom/index.html</code> at session #215
(ruling <code>s215-D5</code>, decision 1: two indexes would drift). The library now lives at
<a href="../showroom/index.html">showroom/index.html</a>.</p>
<div class="rule"></div>
<p class="meta">This file is a generated redirect, kept so the #214 address cited in
<code>knowledge/_state.json</code> row <code>W-99zg</code> still resolves (WRITE-ONCE
addressing, ADR-0017). It is written by
<code>knowledge/_render/gen_library_214.py</code>; never hand-edit it.</p>
</div>
</body>
</html>
"""


def _tree_link(r, lvl_label):
    return ('<a data-slug="%s" href="#c=%s" aria-current="false" title="%s">'
            '<span class="nm">%s</span><span class="why"></span>'
            '<span class="lvl">%s</span></a>'
            % (r["slug"], r["slug"],
               htmlmod.escape((r["purpose"][:110] or r["label"]), quote=True),
               htmlmod.escape(r["label"]), htmlmod.escape(lvl_label[r["level"]])))


def sections_html(rows, groups, key, lvl_label):
    """One <details> per group, in the config's order. Empty groups are not drawn.

    #218 — GROUPS INSIDE A TIER. An entry may carry a `group` label (today only the Foundations
    Grids four). Ungrouped entries are drawn first, exactly as before; each group is then drawn
    as a labelled run beneath them. ⛔ The mechanism is one level deep on purpose — the library
    IA v2 word-set is Dave's open ruling (W-99zg) and a general nesting system built here would
    pre-empt it. ⚠ BREAK_GROUPS is the #218 mutation arm: the labels and their wrappers are
    stripped and every entry is drawn flat, so the group assertion in verify_grids_218.py can be
    seen to go RED by name. It writes NON-REPO only (--break-groups)."""
    out = []
    by = {}
    for r in rows:
        by.setdefault(r[key], []).append(r)
    for g in groups:
        items = sorted(by.get(g["key"], []), key=lambda r: r["label"])
        if not items:
            continue
        flat = [r for r in items if not r.get("group")] if not BREAK_GROUPS else items
        links = "".join(_tree_link(r, lvl_label) for r in flat)
        if not BREAK_GROUPS:
            seen = []
            for r in items:
                if r.get("group") and r["group"] not in seen:
                    seen.append(r["group"])
            for gname in seen:
                members = [r for r in items if r.get("group") == gname]
                links += ('<div class="grp" data-group="%s">'
                          '<span class="grpl">%s<span class="c">%d</span></span>%s</div>'
                          % (htmlmod.escape(gname, quote=True), htmlmod.escape(gname),
                             len(members),
                             "".join(_tree_link(r, lvl_label) for r in members)))
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

    # Swiss stat display (#215 restyle): counted from THIS pass, never hand-typed.
    tiers_drawn = len({r["level"] for r in rows})
    usage_drawn = len({r["usage"] for r in rows})
    js_count = len([r for r in rows if r["js"] > 0])
    # #217 — the two populations are counted APART on the face of the page. A Foundations entry
    # is not a component and the header must not imply it is.
    comp_count = len([r for r in rows if not r["foundation"]])
    found_count = len(rows) - comp_count

    data = json.dumps({"rows": rows, "aliases": ALIASES,
                       "levelLabels": lvl_label, "usageLabels": use_label,
                       "statusLabels": st_label}, sort_keys=True)
    page = (TMPL
            .replace("__CSS__", CSS)
            .replace("__SENTINEL__", INDEX_SENTINEL)
            .replace("__COUNT__", str(comp_count))
            .replace("__FCOUNT__", str(found_count))
            .replace("__STAT_TIERS__", str(tiers_drawn))
            .replace("__STAT_USAGE__", str(usage_drawn))
            .replace("__STAT_JS__", str(js_count))
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
        "$ruling": "s215-D4 + s215-D5 + #217 Foundations",
        "$count": len(rows),
        "$component_count": comp_count,
        "$foundation_count": found_count,
        "$levels": [{"key": lv["key"], "label": lv["label"]} for lv in LEVELS],
        # #218 — the group word-set, ONE list, so a reader of the index can tell a group label
        # from a free-text field. Absent under the mutation arm.
        **({} if BREAK_GROUPS else {"$foundation_groups": list(FOUNDATION_GROUPS)}),
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
             "foundation": r["foundation"],     # #217 — declared entry, not a derived component
             # #218 — the group label, or null. ⚠ Absent under the --break-groups arm, which is
             # how the JSON half of the group assertion is seen to go red.
             **({} if BREAK_GROUPS else {"group": r.get("group")}),
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
    bite("8 · one COMPONENT row per showroom page (#217: foundations are counted apart)",
         # ⚠ basename equality, NOT endswith: template-list-index.html ends with "index.html"
         # ⚠ the glob is NON-RECURSIVE, which is what keeps showroom/_foundations/*.html out.
         len([r for r in rows if not r["foundation"]]),
         len([p for p in glob.glob(os.path.join(SHOWROOM, "*.html"))
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
         ["Foundations", "Element", "Pattern", "Block", "Shell", "Template"])
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

    # ---- #215 SWISS RESTYLE. Each bite probes the chrome CSS the page actually
    # ships, not the generator's intent.
    css = page.split("<style>", 1)[1].split("</style>", 1)[0]
    bite("24 · Swiss · no radius and no shadow anywhere in the chrome",
         (re.findall(r"border-radius:\s*(?!0)[^;}]+", css), "box-shadow" in css),
         ([], False))
    bite("25 · s151-D1 two-red law + the ink rule — the only red is #DA1A00, no pure black",
         (sorted({c.upper() for c in re.findall(r"#[0-9A-Fa-f]{6}", css)
                  if int(c[1:3], 16) > 150 and int(c[3:5], 16) < 120}),
          "#000000" in css.upper(), "#DB0011" in css.upper()),
         (["#DA1A00"], False, False))
    bite("26 · Swiss · the label pattern is drawn with an accent dash + uppercase eyebrow",
         (".label::before" in css and "text-transform:uppercase" in css
          and 'class="label"' in page,
          page.count('class="label"') >= 3), (True, True))
    bite("27 · Swiss · the accent fills nothing but the 1px label dash (never a surface)",
         sorted(" ".join(sel.split()).split("}")[-1].strip()
                for sel in re.findall(
                    r"([^{}]*)\{[^{}]*background:\s*(?:var\(--accent\)|#DA1A00)",
                    css, re.I)),
         [".label::before"])

    # ---- #217 FOUNDATIONS. Each bite probes the page/index the generator actually ships.
    fnd = [r for r in rows if r["foundation"]]
    bite("28 · #217 · the Foundations tier is DRAWN, with the declared entries as its members",
         (sorted(r["slug"] for r in fnd), sorted(f["slug"] for f in FOUNDATIONS),
          "Foundations" in type_tree),
         (sorted(f["slug"] for f in FOUNDATIONS), sorted(f["slug"] for f in FOUNDATIONS), True))
    bite("29 · #217 · a Foundations pane is addressed by its OWN page, not by <slug>.html",
         sorted(r["page"] for r in fnd),
         sorted("%s/%s" % (FOUNDATION_DIR, f["file"]) for f in FOUNDATIONS))
    # ⛔ THE DIRECTORY IS THE FENCE, and this is the bite that keeps it. If a foundation page
    # were ever emitted into showroom/ it would be counted as a component here AND deleted by
    # gen_showroom.py's orphan prune — both non-recursive globs over showroom/*.html.
    bite("30 · #217 · no foundation page sits in showroom/ where the orphan prune would eat it",
         [f["file"] for f in FOUNDATIONS
          if os.path.exists(os.path.join(SHOWROOM, f["file"]))], [])
    bite("31 · #217 · components and foundations are counted APART on the face of the page",
         ('<strong>%d</strong> components' % len([r for r in rows if not r["foundation"]]) in page,
          '<strong>%d</strong> foundations' % len(fnd) in page), (True, True))
    bite("32 · #217 · the JSON index marks which rows are declared, not derived",
         sorted(c["slug"] for c in idx["components"] if c["foundation"]),
         sorted(f["slug"] for f in FOUNDATIONS))

    # ---- #218 THE GRIDS GROUP. Probed on the SHIPPED nav markup and the SHIPPED index, never
    # on the config list alone — a group that is declared and not drawn is the whole failure.
    grp_members = [f for f in FOUNDATIONS if f.get("group") == "Grids"]
    bite("33 · #218 · the Grids group is declared with FOUR members, all in Foundations",
         (len(grp_members),
          sorted(f["slug"] for f in grp_members),
          sorted({r["level"] for r in rows if r.get("group") == "Grids"})),
         (4,
          ["foundation-grids-12col", "foundation-grids-dashboard",
           "foundation-grids-display", "foundation-grids-gallery"],
          ["foundation"]))
    bite("34 · #218 · the group LABEL and its wrapper reach the tier nav, with its own count",
         ('<div class="grp" data-group="Grids">' in type_tree,
          '<span class="grpl">Grids<span class="c">4</span></span>' in type_tree),
         (True, True))
    bite("35 · #218 · every grouped entry's link sits INSIDE its group wrapper, not beside it",
         sorted(re.findall(r'data-slug="(foundation-grids-[a-z0-9]+)"',
                           type_tree.split('<div class="grp" data-group="Grids">', 1)[-1]
                           .split("</div>", 1)[0])),
         ["foundation-grids-12col", "foundation-grids-dashboard",
          "foundation-grids-display", "foundation-grids-gallery"])
    bite("36 · #218 · the group is ONE level deep — no group carries a nested group (W-99zg)",
         '<div class="grp"' in type_tree.split('<div class="grp"', 1)[-1], False)
    bite("37 · #218 · the JSON index round-trips the group on the same four slugs, and null else",
         (sorted(c["slug"] for c in idx["components"] if c.get("group") == "Grids"),
          sorted({str(c.get("group")) for c in idx["components"] if not c.get("group")}),
          idx.get("$foundation_groups")),
         (["foundation-grids-12col", "foundation-grids-dashboard",
           "foundation-grids-display", "foundation-grids-gallery"],
          ["None"], ["Grids"]))
    # ⛔ THE ARM IS BITTEN TOO. A mutation handle that never gets built is an instrument without a
    # consumer; this proves the flag really strips what the assertions above look for.
    global BREAK_GROUPS
    BREAK_GROUPS = True
    try:
        mpage, mjson, _mrows, _mres = build()
    finally:
        BREAK_GROUPS = False
    bite("38 · #218 · --break-groups really strips the grouping (the arm can go red)",
         ('<div class="grp"' in mpage,
          any("group" in c for c in json.loads(mjson)["components"]),
          sorted(re.findall(r'data-slug="(foundation-grids-[a-z0-9]+)"', mpage)) ==
          sorted(re.findall(r'data-slug="(foundation-grids-[a-z0-9]+)"', page))),
         (False, False, True))

    # ★ 39/40/41 (#221) — THE CASE-SENSITIVITY BITE, DRIVEN ON A REAL CASE-SENSITIVE FILESYSTEM.
    # A bite that only asserts about `resolve_meta` would prove nothing on APFS, where the old
    # broken code also passed. So: mirror the metas into a scratch directory (POSIX /var/tmp is
    # case-sensitive; APFS-mounted repo paths are not), and drive `collect()` against it. Bite 39
    # is the FIX — the rows must be identical. Bite 40 is the MUTATION — with `resolve_meta`
    # replaced by the old exact-path lookup, the same run must go WRONG, by name, so the bite is
    # proved falsifiable rather than merely green. Bite 41 fixes the advisory arm's two verdicts.
    import shutil as _sh, tempfile as _tf
    _scratch = _tf.mkdtemp(prefix="lib214-case-", dir=os.environ.get("TMPDIR", "/var/tmp"))
    try:
        for _n in os.listdir(META):
            if _n.endswith(".meta.json"):
                _sh.copyfile(os.path.join(META, _n), os.path.join(_scratch, _n))
        _cs_is_sensitive = not os.path.exists(
            os.path.join(_scratch, "Chart-boxplot.meta.json".lower()))
        _real_meta = META
        try:
            globals()["META"] = _scratch
            _META_INDEX.pop(_scratch, None)
            _cs_rows, _cs_res = collect()
        finally:
            globals()["META"] = _real_meta
        bite("39 · #221 · a case-sensitive filesystem yields the IDENTICAL index (the CI defect)",
             (_cs_is_sensitive, _cs_rows == rows, _cs_res["no_meta"]),
             (True, True, []))
        # MUTATION: put the pre-#221 lookup back and watch the same run break, by name.
        _saved = globals()["resolve_meta"]
        try:
            globals()["resolve_meta"] = lambda s, d=None: (
                (os.path.join(d or META, s + ".meta.json"), True)
                if os.path.exists(os.path.join(d or META, s + ".meta.json")) else (None, False))
            globals()["META"] = _scratch
            _mut_rows, _mut_res = collect()
        finally:
            globals()["resolve_meta"] = _saved
            globals()["META"] = _real_meta
        bite("40 · #221 · …and the OLD exact-path lookup demonstrably loses those rows to 'unfiled'",
             (sorted(_mut_res["no_meta"]) == sorted(_mut_res["unfiled"]),
              len(_mut_res["no_meta"]) > 0 if _cs_is_sensitive else True,
              _mut_rows != rows if _cs_is_sensitive else True),
             (True, True, True))
        # BOTH VERDICTS of the advisory arm, on this platform, whatever it is: a lowercased
        # mirror is the CLEAN tree (arm clears), the repo's own metas are the DIRTY one (arm
        # fires). A gate that cannot reach both verdicts here is the #173 class.
        _clean = _tf.mkdtemp(prefix="lib214-clean-", dir=os.environ.get("TMPDIR", "/var/tmp"))
        try:
            for _n in os.listdir(META):
                if _n.endswith(".meta.json"):
                    _sh.copyfile(os.path.join(META, _n), os.path.join(_clean, _n.lower()))
            _META_INDEX.pop(_clean, None)
            bite("41 · #221 · the ADVISORY casing arm reaches BOTH verdicts on this platform",
                 (casing_mismatches(_clean), bool(casing_mismatches(_scratch))),
                 ([], bool(casing_mismatches())))
        finally:
            _sh.rmtree(_clean, ignore_errors=True)
    finally:
        _sh.rmtree(_scratch, ignore_errors=True)

    if fails:
        print("gen_library_214 --selftest: %d BITE(S) FAILED" % len(fails))
        for f in fails:
            print("  ❌ " + f)
        sys.exit(1)
    print("gen_library_214 --selftest OK — %d bites." % len(ran))
    print("   residual · no meta.json: %s" % (residuals["no_meta"] or "none"))
    print("   residual · meta filename CASE differs from slug (#221, resolved not skipped): %s"
          % (", ".join("%s -> %s" % t for t in residuals["meta_case"]) or "none"))
    print("   residual · unfiled level: %s" % (residuals["unfiled"] or "none"))
    print("   residual · usage group 'Other': %s" % (residuals["usage_other"] or "none"))
    print("   residual · missing thumbnail: %d entry(s)" % len(residuals["no_thumb"]))
    print("   residual · foundation page not on disk: %s"
          % (residuals["no_foundation_page"] or "none"))
    print("   residual · ships no behaviour script: %d component(s)"
          % len(residuals["no_behaviour"]))


def report(rows, residuals):
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("   status:            %s" % ", ".join("%s %d" % (k, counts[k]) for k in sorted(counts)))
    print("   itinerary source:  %s" % residuals["itinerary"])
    print("   no meta.json:      %s" % (residuals["no_meta"] or "none"))
    print("   meta case mismatch: %s"        # #221 — declared, never a silent case-insensitive win
          % (", ".join("%s -> %s" % t for t in residuals["meta_case"]) or "none"))
    print("   unfiled level:     %s" % (residuals["unfiled"] or "none"))
    print("   usage 'Other':     %s" % (residuals["usage_other"] or "none"))
    print("   foundation page missing: %s" % (residuals["no_foundation_page"] or "none"))
    print("   missing thumbnail: %d — %s"
          % (len(residuals["no_thumb"]), ", ".join(residuals["no_thumb"][:8]) or "none"))
    print("   no behaviour JS:   %d — %s"
          % (len(residuals["no_behaviour"]), ", ".join(residuals["no_behaviour"][:8])))


def casing_arm():
    """`--casing` · ⬛ ADVISORY AT BIRTH (#221) — not wired into `_build_all.py`, not in `gates.yml`,
    and promotion to blocking is Dave's word.

    Exit **1** when any showroom slug's meta filename differs from the slug in CASE, **0** when
    none do. The comparison is string-against-`os.listdir`, so THE SAME VERDICT IS REACHABLE ON
    BOTH PLATFORMS — which is the whole point: `os.path.exists` gives opposite answers on APFS and
    ext4, and that difference is what silently degraded 7 rows of the index in CI
    [[gate-cannot-pass-in-one-environment]]. `resolve_meta()` now makes the ARTEFACT identical
    either way; this arm keeps the underlying mismatch VISIBLE instead of absorbed.
    """
    bad = casing_mismatches()
    if not bad:
        print("✅ meta-filename casing (ADVISORY, #221): every showroom slug has an EXACT-CASE "
              "meta. The index cannot differ by filesystem.")
        return 0
    print("⚠ META FILENAME CASING (ADVISORY, #221) — %d slug(s) resolve only case-insensitively:"
          % len(bad))
    for slug, fname in bad:
        print("   %-24s slug expects %-28s on disk it is %s" % (slug, slug + ".meta.json", fname))
    print("   These RESOLVE (gen_library_214 normalises the reference), so the index is identical "
          "on APFS and ext4. Renaming the files is a naming-convention question and is DAVE'S: "
          "the sibling `Chart-*.reference.html` snippets are capitalised too.")
    return 1


def main():
    if "--casing" in sys.argv:
        # ⛔ sys.exit, NOT return: `main()`'s return value is discarded at the bottom of this file,
        # so an arm that merely `return`s its verdict is an [[instrument-without-a-consumer]] —
        # it would have printed RED and exited 0. Caught by driving it, not by reading it.
        sys.exit(casing_arm())
    if "--selftest" in sys.argv:
        return selftest()
    if "--break-groups" in sys.argv:
        # ⬛ #218 MUTATION ARM. NON-REPO by construction: the destination is BM_MUTANT_DIR, never
        # showroom/. ⚠ /var/tmp IS SHARED ACROSS SESSIONS and a foreign mutant is both unwritable
        # and STALE — a stale mutant silently proves yesterday's clause. Pass a session-suffixed
        # BM_MUTANT_DIR; the write below is checked and refused loudly if it cannot land.
        global BREAK_GROUPS
        BREAK_GROUPS = True
        mdir = os.environ.get("BM_MUTANT_DIR", "/var/tmp")
        os.makedirs(mdir, exist_ok=True)
        page, index_json, _rows, _resid = build()
        for name, content in (("library-index-GROUPS-BROKEN.html", page),
                              ("library-index-GROUPS-BROKEN.json", index_json)):
            dest = os.path.join(mdir, name)
            open(dest, "w").write(content)
            print("gen_library_214 --break-groups: wrote %s (%d bytes)"
                  % (dest, os.path.getsize(dest)))
        return
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
    print("gen_library_214: %d component(s) + %d foundation(s) -> %s + %s (%d file(s) written)"
          % (len([r for r in rows if not r["foundation"]]),
             len([r for r in rows if r["foundation"]]),
             os.path.relpath(OUT, ROOT), os.path.relpath(JSON_OUT, ROOT), len(stale)))
    report(rows, residuals)


if __name__ == "__main__":
    main()
