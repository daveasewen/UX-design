#!/usr/bin/env python3
"""Generate the compliance knowledge graph from component metas.

- Parses every knowledge/components/*.meta.json relatedSC array.
- Derives applies_to edges (which components cite each WCAG SC) from source-of-truth.
- Emits one schema-conformant rule file per SC + a both-way graph index.
- Validates every rule against rule.schema.json (manual check, no deps).

Edge-typing note (2026-07-14): this generator only ever writes the CLAIMED edge
(applies_to). The VERIFIED edge (verified_by — is there an executable check and
does it currently pass) is layered on separately, later in the build, by
knowledge/compliance/_build_verification_edges.py — it needs the contrast
audits and the a11y gate to have already run, which happen after this step in
_build_all.py. Don't add verified_by logic here; add it there.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, re, glob, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = os.path.join(ROOT, "components")
COMPL = os.path.join(ROOT, "compliance")
RULES = os.path.join(COMPL, "rules")
os.makedirs(RULES, exist_ok=True)

# --- WCAG SC metadata lookup (level, versions, title, severity, check, slug) ---
# severity: minor|serious|critical ; check.type: automated|semi-automated|manual
M = {
 "1.1.1": ("Non-text Content","A",["2.0","2.1","2.2"],"serious","semi-automated","Non-text content has a text alternative serving an equivalent purpose (alt text / accessible name); decorative imagery is hidden from AT.",None,"non-text-content"),
 "1.2.2": ("Captions (Prerecorded)","A",["2.0","2.1","2.2"],"serious","manual","Prerecorded synchronised media has captions.",None,"captions-prerecorded"),
 "1.2.5": ("Audio Description (Prerecorded)","AA",["2.0","2.1","2.2"],"serious","manual","Prerecorded video content has an audio description.",None,"audio-description-prerecorded"),
 "1.3.1": ("Info and Relationships","A",["2.0","2.1","2.2"],"serious","semi-automated","Structure and relationships conveyed visually are programmatically determinable (semantic markup, roles, headings, table scope, list semantics).",None,"info-and-relationships"),
 "1.3.2": ("Meaningful Sequence","A",["2.0","2.1","2.2"],"serious","semi-automated","Reading/navigation order is programmatically determinable and meaningful (e.g. DOM order matches visual order).",None,"meaningful-sequence"),
 "1.3.5": ("Identify Input Purpose","AA",["2.1","2.2"],"minor","semi-automated","Input fields collecting user info expose autocomplete/purpose tokens.",None,"identify-input-purpose"),
 "1.4.1": ("Use of Color","A",["2.0","2.1","2.2"],"serious","manual","Colour is not the only means of conveying information, indicating an action, or distinguishing a visual element (pair with text/icon/shape).",None,"use-of-color"),
 "1.4.3": ("Contrast (Minimum)","AA",["2.0","2.1","2.2"],"serious","automated","Text and images of text meet a contrast ratio of at least 4.5:1 (3:1 for large text >=18pt or >=14pt bold).","4.5:1 normal / 3:1 large","contrast-minimum"),
 "1.4.4": ("Resize Text","AA",["2.0","2.1","2.2"],"serious","semi-automated","Text can be resized up to 200% without loss of content or function.","200%","resize-text"),
 "1.4.10": ("Reflow","AA",["2.1","2.2"],"serious","semi-automated","Content reflows to a 320 CSS px viewport width without two-dimensional scrolling.","320 CSS px","reflow"),
 "1.4.11": ("Non-text Contrast","AA",["2.1","2.2"],"serious","automated","UI components and graphical objects (borders, states, focus indicators, icons that carry meaning) meet 3:1 against adjacent colours.","3:1","non-text-contrast"),
 "1.4.12": ("Text Spacing","AA",["2.1","2.2"],"serious","semi-automated","No loss of content or functionality when the user overrides text spacing: line height 1.5x font size, paragraph spacing 2x, letter spacing 0.12x, word spacing 0.16x.",None,"text-spacing"),
 "1.4.13": ("Content on Hover or Focus","AA",["2.1","2.2"],"serious","manual","Hover/focus-triggered content is dismissable (Esc), hoverable, and persistent until dismissed/blur.",None,"content-on-hover-or-focus"),
 "2.1.1": ("Keyboard","A",["2.0","2.1","2.2"],"critical","manual","All functionality is operable through a keyboard interface.",None,"keyboard"),
 "2.1.2": ("No Keyboard Trap","A",["2.0","2.1","2.2"],"critical","manual","Keyboard focus can be moved away from any component using only the keyboard (Esc / standard exits).",None,"no-keyboard-trap"),
 "2.2.1": ("Timing Adjustable","A",["2.0","2.1","2.2"],"serious","manual","Time limits can be turned off, adjusted, or extended (or are essential/exempt).",None,"timing-adjustable"),
 "2.2.2": ("Pause, Stop, Hide","A",["2.0","2.1","2.2"],"serious","manual","Moving/auto-updating content (>5s) can be paused, stopped or hidden.",None,"pause-stop-hide"),
 "2.3.3": ("Animation from Interactions","AAA",["2.1","2.2"],"minor","semi-automated","Motion animation triggered by interaction can be disabled (respect prefers-reduced-motion) unless essential.",None,"animation-from-interactions"),
 "2.4.1": ("Bypass Blocks","A",["2.0","2.1","2.2"],"serious","semi-automated","A mechanism is available to bypass repeated blocks (skip link / landmarks).",None,"bypass-blocks"),
 "2.4.2": ("Page Titled","A",["2.0","2.1","2.2"],"serious","semi-automated","Web pages have titles that describe topic or purpose.",None,"page-titled"),
 "2.4.3": ("Focus Order","A",["2.0","2.1","2.2"],"serious","manual","Focusable components receive focus in an order that preserves meaning and operability (incl. trapped/returned focus for dialogs).",None,"focus-order"),
 "2.4.4": ("Link Purpose (In Context)","A",["2.0","2.1","2.2"],"serious","semi-automated","The purpose of each link is determinable from the link text (alone or with its context); avoid 'click here'.",None,"link-purpose-in-context"),
 "2.4.5": ("Multiple Ways","AA",["2.0","2.1","2.2"],"minor","manual","More than one way is available to locate a page within a set (nav, search, sitemap).",None,"multiple-ways"),
 "2.4.6": ("Headings and Labels","AA",["2.0","2.1","2.2"],"serious","semi-automated","Headings and labels describe topic or purpose.",None,"headings-and-labels"),
 "2.4.7": ("Focus Visible","AA",["2.0","2.1","2.2"],"serious","semi-automated","Any keyboard-operable UI has a visible focus indicator.",None,"focus-visible"),
 "2.4.8": ("Location","AAA",["2.0","2.1","2.2"],"minor","manual","Information about the user's location within a set of pages is available (e.g. breadcrumbs).",None,"location"),
 "2.4.11": ("Focus Not Obscured (Minimum)","AA",["2.2"],"serious","manual","When a component receives focus it is not entirely hidden by author-created content (sticky headers, overlays).",None,"focus-not-obscured-minimum"),
 "2.5.5": ("Target Size (Enhanced)","AAA",["2.1","2.2"],"minor","semi-automated","Pointer targets are at least 44x44 CSS px (or equivalent/inline/essential exceptions). The Apollo hit-area standard target/min=44px (RULED 2026-07-24) is this AAA bar; _validate_hit_area.py is its consumer.","44x44 CSS px","target-size-enhanced"),
 "2.5.7": ("Dragging Movements","AA",["2.2"],"serious","manual","Functionality that uses a dragging movement has a single-pointer alternative that does not require dragging (e.g. move up/down controls).",None,"dragging-movements"),
 "2.5.8": ("Target Size (Minimum)","AA",["2.2"],"serious","semi-automated","Pointer targets are at least 24x24 CSS px (or have sufficient spacing/exception). HSBC's 44px targets exceed this.","24x24 CSS px (HSBC: 44px)","target-size-minimum"),
 "3.2.1": ("On Focus","A",["2.0","2.1","2.2"],"serious","manual","Receiving focus does not initiate a change of context (no auto-submit, no focus-triggered navigation or popup).",None,"on-focus"),
 "3.2.3": ("Consistent Navigation","AA",["2.0","2.1","2.2"],"serious","manual","Navigational mechanisms that are repeated on multiple pages within a set occur in the same relative order each time they are repeated, unless a change is initiated by the user.",None,"consistent-navigation"),
 "3.3.1": ("Error Identification","A",["2.0","2.1","2.2"],"serious","semi-automated","Input errors are identified in text and described to the user (not colour alone).",None,"error-identification"),
 "3.3.2": ("Labels or Instructions","A",["2.0","2.1","2.2"],"serious","semi-automated","Labels or instructions are provided when content requires user input; placeholder is not a label.",None,"labels-or-instructions"),
 "3.3.3": ("Error Suggestion","AA",["2.0","2.1","2.2"],"serious","semi-automated","If an input error is detected and suggestions for correction are known, the suggestions are provided to the user, unless it would jeopardize security or purpose.",None,"error-suggestion"),
 "4.1.1": ("Parsing (Obsolete)","A",["2.0","2.1"],"minor","automated","Markup parses cleanly: no duplicate IDs, complete start/end tags, correct nesting. REMOVED in WCAG 2.2 (deemed always-satisfied by modern parsers); retained here for 2.0/2.1 mapping — the P-2 duplicate-ID probe is the practical consumer.",None,"parsing"),
 "4.1.2": ("Name, Role, Value","A",["2.0","2.1","2.2"],"critical","semi-automated","For all UI components, name and role are programmatically determinable; states/values/properties are set and changes notified to AT.",None,"name-role-value"),
 "4.1.3": ("Status Messages","AA",["2.1","2.2"],"serious","semi-automated","Status messages are programmatically exposed (role=status/alert / aria-live) without receiving focus.",None,"status-messages"),
}

POLICY = "HSBC digital accessibility framework — WCAG 2.2 AA minimum, governed by Group Digital Experience and Accessibility (mandatory on all HSBC digital projects)."
POLICY_EXTRA = {
 "1.4.3": " GTB brand: grey-6 (#767676) is the minimum text colour on white (~4.48:1).",
 "2.5.8": " HSBC components use 44px targets, exceeding both the 24px AA minimum and the 44px AAA (2.5.5) target.",
 "1.4.1": " Recurs as a component anti-pattern: status/selection/error must not rely on colour alone.",
}
SCRE = re.compile(r"^(\d+\.\d+\.\d+)")

# --- parse component metas ---
by_sc = {}      # sc -> set(component names)
by_comp = {}    # component name -> set(sc)
skip = {"meta.schema.json"}
for f in sorted(glob.glob(os.path.join(COMP, "*.meta.json"))):
    base = os.path.basename(f)
    if base.startswith("EXAMPLE") or base in skip:
        continue
    d = json.load(open(f))
    name = d.get("name", base)
    scs = (d.get("accessibility") or {}).get("relatedSC") or []
    for entry in scs:
        m = SCRE.match(entry.strip())
        if not m:
            continue
        sc = m.group(1)
        by_sc.setdefault(sc, set()).add(name)
        by_comp.setdefault(name, set()).add(sc)

# --- report SCs found but not in lookup ---
missing = sorted(set(by_sc) - set(M))
if missing:
    print("WARN: SCs in metas but not in metadata lookup:", missing)

# --- write rule files ---
REQUIRED = {"id","sc","title","level","applies_to","check","severity","sources"}
written, errors = [], []
for sc in sorted(by_sc):
    if sc not in M:
        continue
    title, level, versions, severity, ctype, cdesc, thresh, slug = M[sc]
    rid = f"wcag-{sc}-{slug}"
    check = {"type": ctype, "description": cdesc}
    if thresh:
        check["threshold"] = thresh
    sources = {"wcag_url": f"https://www.w3.org/WAI/WCAG22/Understanding/{slug}.html"}
    # EN 301 549 mirrors WCAG SC numbering as 9.x.x.x (2.2 alignment pending for 2.2-only SCs)
    sources["en301549_clause"] = f"9.{sc}" + ("" if "2.2" not in versions or len(versions) > 1 else " (pending EN 301 549 alignment to WCAG 2.2)")
    sources["internal_policy_ref"] = POLICY + POLICY_EXTRA.get(sc, "")
    rule = {
        "id": rid, "sc": sc, "title": title, "level": level,
        "wcag_versions": versions,
        "applies_to": sorted(by_sc[sc]),
        "check": check, "severity": severity, "sources": sources,
    }
    # validate (manual)
    errs = []
    if set(rule) - (REQUIRED | {"wcag_versions"}): errs.append("extra keys")
    if not REQUIRED <= set(rule): errs.append("missing required")
    if rule["level"] not in ("A","AA","AAA"): errs.append("bad level")
    if rule["check"]["type"] not in ("automated","semi-automated","manual"): errs.append("bad check.type")
    if rule["severity"] not in ("minor","serious","critical"): errs.append("bad severity")
    if "wcag_url" not in rule["sources"]: errs.append("no wcag_url")
    if errs:
        errors.append((rid, errs))
    json.dump(rule, open(os.path.join(RULES, rid + ".json"), "w"), indent=2, ensure_ascii=False)
    written.append(rid)

# --- graph index ---
index = {
    "$description": "Compliance knowledge graph index — both-way adjacency between WCAG success criteria and components. Generated from knowledge/components/*.meta.json relatedSC by build_compliance_kg.py. Conformance basis: WCAG 2.2 AA (HSBC digital accessibility framework). The 'verification' block (SC -> verified_by-or-null) is added LATER in the build by _build_verification_edges.py — absent here, present after a full knowledge/_build_all.py run.",
    "generated": datetime.date.today().isoformat(),
    "totals": {"rules": len(written), "components": len(by_comp), "sc": len(by_sc)},
    "by_sc": {sc: sorted(list(c)) for sc, c in sorted(by_sc.items())},
    "by_component": {c: sorted(list(s)) for c, s in sorted(by_comp.items())},
    "rules": sorted(written),
}
json.dump(index, open(os.path.join(COMPL, "graph-index.json"), "w"), indent=2, ensure_ascii=False)

print(f"Wrote {len(written)} rule files to compliance/rules/")
print(f"Index: {len(by_sc)} SCs x {len(by_comp)} components")
print("Validation errors:", errors if errors else "none")
# severity / level rollups
from collections import Counter
lev = Counter(M[sc][1] for sc in by_sc if sc in M)
sev = Counter(M[sc][3] for sc in by_sc if sc in M)
print("Levels:", dict(lev), "| Severities:", dict(sev))
print("AAA (beyond AA bar):", [sc for sc in sorted(by_sc) if sc in M and M[sc][1]=="AAA"])
