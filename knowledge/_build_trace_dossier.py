#!/usr/bin/env python3
"""
Knowledge-usage DOSSIER builder — entity-level breakdown, not a score.

WHY (Dave, §9 session 2026-07-07): the single-number retrieval trace answered "how much was
retrieved" but he wants to ANALYSE and TARGET specific entities — which components, which tokens,
which invented colours — and to understand what governs LAYOUT (the dimension he judges the real
difference). This builder extracts a per-entity record from every artifact and renders it as a
Swiss-styled interactive HTML dossier (charts for cognition, filter + annotate to target entities,
localStorage + export — same idiom as _REVIEW-DOSSIER-charter_2026-07-03.html).

Entity types extracted per file:
  component  — .cn-* used, matched to canon (retrieved) or unknown
  utility    — .c-* patch-layer class (retrieved-but-ungated)
  token      — var(--x): retrieved (in canon) / invented (local-only) / dangling (nowhere)
  colour     — live #rrggbb literal = INVENTED cardinal value
  icon       — inline path: library byte-match / UNKNOWN
Plus a LAYOUT block per file (the unretrieved dimension): the actual grid-template-columns each
lineage invented, max-widths, display:grid/flex counts, canon gap/layout token refs vs raw-px
spacing — so the layout divergence is visible side by side.

Writes:
  _KNOWLEDGE-USAGE-ENTITIES.json   (machine)
  _KNOWLEDGE-USAGE-TRACE.html      (the dossier — self-contained, data inlined)

Usage: python3 _build_trace_dossier.py            # default: the 07-05 §9 spread
       python3 _build_trace_dossier.py LABEL=path ...
"""
import os, re, sys, glob, json

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(HERE, "canon", "canon.css")
ICONS = os.path.join(HERE, "assets", "icons")
OUT_JSON = os.path.join(HERE, "_KNOWLEDGE-USAGE-ENTITIES.json")
OUT_HTML = os.path.join(HERE, "_KNOWLEDGE-USAGE-TRACE.html")

CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
VAR_REF = re.compile(r"var\(\s*(--[a-z0-9-]+)")
VAR_DEF = re.compile(r"(--[a-z0-9-]+)\s*:")
CN_CLASS = re.compile(r"\bcn-[a-z0-9-]+")
C_CLASS = re.compile(r"\bc-[a-z0-9-]+")
SVGRE = re.compile(r"<svg\b[^>]*?>.*?</svg>", re.S)
DRE = re.compile(r'\bd="([^"]+)"')
SHAPERE = re.compile(r"<(?:circle|rect|ellipse|polygon|polyline)\b")
CANDIDATE = re.compile(r"data-candidate|CANDIDATE|derive-and-flag|FLAG:|/\*\s*flag", re.I)
GTC = re.compile(r"grid-template-columns\s*:\s*([^;{}\n)]+)")
MAXW = re.compile(r"max-width\s*:\s*([0-9.]+(?:px|rem|em|ch|%|vw|vh))")
MEDIA = re.compile(r"@media[^{]*\{")
RAWPX = re.compile(r"(?:gap|margin|padding)\s*:\s*[^;{}]*\b\d{2,}px")


def norm(d):
    return re.sub(r"\s+", " ", d.strip())


def canon_vocab():
    try:
        s = open(CANON, encoding="utf-8").read()
    except Exception:
        return set(), set()
    return set(VAR_DEF.findall(s)), set(CN_CLASS.findall(s))


def icon_library():
    lib = set()
    for f in glob.glob(os.path.join(ICONS, "**", "*.svg"), recursive=True):
        try:
            s = open(f, encoding="utf-8").read()
        except Exception:
            continue
        for d in DRE.findall(s):
            lib.add(norm(d))
    return lib


CANON_VARS, CANON_CN = canon_vocab()
ICON_LIB = icon_library()

WCAG_NAMES = {
    "1.1.1": "Non-text content", "1.2.2": "Captions (prerecorded)", "1.2.5": "Audio description",
    "1.3.1": "Info & relationships", "1.3.2": "Meaningful sequence", "1.3.5": "Identify input purpose",
    "1.4.1": "Use of colour", "1.4.3": "Contrast (minimum)", "1.4.4": "Resize text",
    "1.4.10": "Reflow", "1.4.11": "Non-text contrast", "1.4.13": "Content on hover or focus",
    "2.1.1": "Keyboard", "2.1.2": "No keyboard trap", "2.2.1": "Timing adjustable",
    "2.2.2": "Pause, stop, hide", "2.3.3": "Animation from interactions", "2.4.1": "Bypass blocks",
    "2.4.3": "Focus order", "2.4.4": "Link purpose (in context)", "2.4.5": "Multiple ways",
    "2.4.6": "Headings & labels", "2.4.7": "Focus visible", "2.4.8": "Location",
    "2.4.11": "Focus not obscured", "2.5.7": "Dragging movements", "2.5.8": "Target size (minimum)",
    "3.3.1": "Error identification", "3.3.2": "Labels or instructions",
    "4.1.2": "Name, role, value", "4.1.3": "Status messages",
}


WCAG_DESC = {
    "1.1.1": "All non-text content (images, icons) has a text alternative that serves the equivalent purpose.",
    "1.2.2": "Captions are provided for all prerecorded audio in synchronised media.",
    "1.2.5": "Audio description is provided for all prerecorded video content.",
    "1.3.1": "Information, structure and relationships conveyed visually are also available programmatically (headings, lists, table markup, labels).",
    "1.3.2": "The reading/navigation order in the DOM is meaningful and matches the visual order.",
    "1.3.5": "Input fields collecting user info have an autocomplete purpose identified programmatically.",
    "1.4.1": "Colour is not the only visual means of conveying information or indicating an action.",
    "1.4.3": "Text has a contrast ratio of at least 4.5:1 (3:1 for large text) against its background.",
    "1.4.4": "Text can be resized up to 200% without loss of content or function.",
    "1.4.10": "Content reflows to a single column at 320px width without horizontal scrolling.",
    "1.4.11": "UI components and graphical objects have at least 3:1 contrast against adjacent colours.",
    "1.4.13": "Content revealed on hover/focus is dismissable, hoverable and persistent.",
    "2.1.1": "All functionality is operable through a keyboard.",
    "2.1.2": "Keyboard focus can be moved away from any component using only the keyboard (no trap).",
    "2.2.1": "Users can turn off, adjust or extend any time limit.",
    "2.2.2": "Moving, blinking or auto-updating content can be paused, stopped or hidden.",
    "2.3.3": "Motion animation triggered by interaction can be disabled (respects prefers-reduced-motion).",
    "2.4.1": "A mechanism is available to bypass blocks of content repeated on multiple pages.",
    "2.4.3": "Components receive focus in an order that preserves meaning and operability.",
    "2.4.4": "The purpose of each link can be determined from the link text (or its context).",
    "2.4.5": "More than one way is available to locate a page within a set.",
    "2.4.6": "Headings and labels describe the topic or purpose.",
    "2.4.7": "Any keyboard-operable interface has a visible focus indicator.",
    "2.4.8": "Information about the user's location within a set of pages is available.",
    "2.4.11": "When a component receives focus, it is not entirely hidden by author-created content.",
    "2.5.7": "Functionality using a dragging movement has a single-pointer alternative.",
    "2.5.8": "Targets are at least 24x24 CSS px (HSBC raises this to 44x44).",
    "3.3.1": "If an input error is detected, the item in error is identified and described in text.",
    "3.3.2": "Labels or instructions are provided when content requires user input.",
    "4.1.2": "For all UI components, the name, role, value and states are programmatically available to assistive tech.",
    "4.1.3": "Status messages can be programmatically determined through role/properties without receiving focus.",
}


def guideline_descriptions():
    out = {}
    for f in glob.glob(os.path.join(HERE, "guidelines", "*.md")):
        try:
            for line in open(f, encoding="utf-8"):
                s = line.strip()
                if s.startswith("title:"):
                    out[os.path.basename(f)] = s.split(":", 1)[1].strip()
                    break
                if s.startswith("# "):
                    out[os.path.basename(f)] = s[2:].split("—")[0].split("(")[0].strip()
                    break
        except Exception:
            pass
    return out


def load_xref_components():
    try:
        return json.load(open(os.path.join(HERE, "_XREF-INDEX.json"))).get("components", {})
    except Exception:
        return {}


GUIDE_DESC = guideline_descriptions()
XREF_COMPS = load_xref_components()
CN_TO_NAME = {slug_name: name for name in XREF_COMPS
              for slug_name in ["cn-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")]}


def component_detail(cn_slug):
    name = CN_TO_NAME.get(cn_slug)
    if not name:
        return "Component class not found in the cross-reference index."
    c = XREF_COMPS[name]
    parts = [f"{c.get('category','')} · {c.get('token_count',0)} tokens bound."]
    if c.get("guidelines"):
        parts.append("Governed by: " + ", ".join(g.replace(".md", "") for g in c["guidelines"]) + ".")
    if c.get("wcag_sc"):
        parts.append("Must satisfy WCAG: " + ", ".join(c["wcag_sc"]) + ".")
    ap = c.get("anti_patterns", {})
    aps = (ap.get("asserted") or []) + (ap.get("inferred_review") or [])
    if aps:
        parts.append("Anti-patterns: " + "; ".join(a[:90] for a in aps[:2]) + ".")
    return " ".join(parts)


def rule_probes(raw, live, canon_linked):
    """Detect whether governing RULES (WCAG + create.hsbc principles) were attended to in the
    artifact. Verdict: honoured (evidence present) / violated (anti-signal present) /
    not-detected (no evidence either way). This is the 'rules used' layer — the guidelines and
    WCAG rules ARE in the KG; this surfaces whether each screen honoured them."""
    ents = []
    L = live
    has_interactive = bool(re.search(r"<(button|a |input|select|textarea)", raw))
    has_img = bool(re.search(r"<img\b", raw))
    has_motion = bool(re.search(r"(transition|animation|@keyframes)", L))
    aria = len(re.findall(r"aria-|role=", raw))
    focus = len(re.findall(r":focus", L))
    reduced = "prefers-reduced-motion" in L
    radius_nonzero = re.findall(r"border-radius\s*:\s*(?!0)[0-9.]+(?:px|rem|em|%)", L)
    caps = len(re.findall(r"text-transform\s*:\s*uppercase", L))
    landmarks = len(re.findall(r"<(main|nav|header|footer|section|table|h[1-4])\b", raw))

    def add(rule, node_type, node, verdict, detail):
        ents.append({"name": rule, "type": node_type, "verdict": verdict, "count": 1,
                     "detail": detail, "rule_node": node})

    # WCAG-linked a11y probes
    add("2.4.7 Focus visible", "a11y", "W:2.4.7",
        "honoured" if focus else ("violated" if has_interactive else "not-detected"),
        f"Keyboard focus styling. Found :focus rules ×{focus}. "
        + ("Interactive elements present." if has_interactive else "No interactive elements detected."))
    add("4.1.2 Name, role, value", "a11y", "W:4.1.2",
        "honoured" if aria else ("not-detected" if not has_interactive else "violated"),
        f"ARIA/role usage ×{aria}. Interactive UI should expose name/role/value to AT.")
    add("1.1.1 Non-text content", "a11y", "W:1.1.1",
        "not-detected" if not has_img else ("honoured" if re.search(r"<img\b[^>]*alt=", raw) else "violated"),
        "Alt text on images. " + ("No <img> on this screen." if not has_img else "Images present — checked for alt."))
    add("2.3.3 Animation from interactions", "a11y", "W:2.3.3",
        "not-detected" if not has_motion else ("honoured" if reduced else "violated"),
        "prefers-reduced-motion handling. " + ("No motion on this screen." if not has_motion else
        ("Reduced-motion query present." if reduced else "Motion present but NO reduced-motion fallback.")))
    add("1.3.1 Info & relationships", "a11y", "W:1.3.1",
        "honoured" if landmarks >= 3 else "not-detected",
        f"Semantic structure (landmarks/headings/table) ×{landmarks}.")

    # create.hsbc principle probes
    add("Square corners", "principle", "G:brand-principles.md",
        "violated" if radius_nonzero else "honoured",
        "brand-principles.md: cardinal square corners. "
        + (f"Found {len(radius_nonzero)} non-zero border-radius (exceptions: Badge/Avatar only)." if radius_nonzero
           else "No rounded corners detected."))
    add("Sentence case (no ALL-CAPS)", "principle", "G:copywriting.md",
        "violated" if caps else "honoured",
        "House rule (type-rule-sentence-case): avoid ALL-CAPS labels. "
        + (f"Found text-transform:uppercase ×{caps}." if caps else "No uppercase transform."))
    add("Retrieve, don't recall (theme)", "principle", "G:dark-mode.md",
        "honoured" if canon_linked else "violated",
        "§5 retrieve-don't-recall + dark-mode theming via canon tokens. "
        + ("canon.css linked." if canon_linked else "canon.css NOT linked — brand values inferred."))
    return ents


def strip_comments(html):
    return HTML_COMMENT.sub("", CSS_COMMENT.sub("", html))


def entities_for_file(path, lineage):
    raw = open(path, encoding="utf-8").read()
    live = strip_comments(raw)
    local_defs = set(VAR_DEF.findall(live))
    canon_linked = ("canon.css" in raw) and ("class=\"canon\"" in raw or "class='canon'" in raw)

    ents = []  # {name,type,verdict,count}

    # components
    from collections import Counter
    cn_counts = Counter(CN_CLASS.findall(live))
    for name, n in sorted(cn_counts.items()):
        retr = name in CANON_CN
        ents.append({"name": "." + name, "type": "component",
                     "verdict": "retrieved" if retr else "invented", "count": n,
                     "detail": component_detail(name) if retr
                     else "Class looks like a canon component but no ." + name + " exists in canon.css — invented or mis-named."})
    # utilities (.c-* but not cn-*)
    c_counts = Counter(x for x in C_CLASS.findall(live) if not x.startswith("cn-"))
    for name, n in sorted(c_counts.items()):
        ents.append({"name": "." + name, "type": "utility", "verdict": "utility", "count": n,
                     "detail": "Hand-authored patch-layer utility (.c-*) — never gate-reviewed; used to fill a compositional gap no .cn-* covers."})

    # tokens
    var_counts = Counter(VAR_REF.findall(live))
    for name, n in sorted(var_counts.items()):
        if name in CANON_VARS:
            v, det = "retrieved", "Canon token — defined in canon.css, retrieved not invented."
        elif name in local_defs:
            v, det = "invented", "Locally-defined var — this screen invented it (not in canon.css). Colour vars here are cardinal violations."
        else:
            v, det = "dangling", "Referenced but defined nowhere (canon or local) — a broken var reference."
        ents.append({"name": name, "type": "token", "verdict": v, "count": n, "detail": det})

    # colours (live hex)
    hex_counts = Counter(HEX.findall(live))
    for name, n in sorted(hex_counts.items()):
        ents.append({"name": name.lower(), "type": "colour", "verdict": "invented", "count": n,
                     "detail": "Live hex literal. Colour is a §9 CARDINAL curb — it must be retrieved from the token store, never typed. Any live hex is a cardinal violation."})

    # icons
    lib_hits = 0
    unknown_paths = []
    for blk in SVGRE.findall(live):
        if "data-bespoke" in blk[: blk.find(">") + 1]:
            continue
        paths = DRE.findall(blk)
        for d in paths:
            if norm(d) in ICON_LIB:
                lib_hits += 1
            else:
                unknown_paths.append(norm(d)[:40])
        if not paths and SHAPERE.search(blk):
            unknown_paths.append("(shape-only)")
    if lib_hits:
        ents.append({"name": "library glyphs", "type": "icon", "verdict": "retrieved", "count": lib_hits,
                     "detail": "Inline SVG paths that byte-match the HSBC icon library in assets/icons/."})
    for d in Counter(unknown_paths).items():
        ents.append({"name": "icon: " + d[0], "type": "icon", "verdict": "invented", "count": d[1],
                     "detail": "Inline SVG that does not match any library glyph — a hand-drawn/invented icon (icon-source-rule violation)."})

    # rule-adherence layer (WCAG + create.hsbc principles) — the 'rules used' picture
    ents.extend(rule_probes(raw, live, canon_linked))

    # layout block (the unretrieved dimension). Strip @media conditions first so breakpoint
    # max-widths don't masquerade as content-container widths.
    nomedia = MEDIA.sub("{", live)
    grids = [re.sub(r"\s+", " ", g.strip()) for g in GTC.findall(nomedia) if g.strip()]
    maxw = [m.strip() for m in MAXW.findall(nomedia)]
    canon_gap = sum(1 for nm in VAR_REF.findall(live) if nm.startswith(("--gap", "--layout", "--breakpoint")))
    layout = {
        "grids": grids,
        "grid_count": len(grids),
        "max_widths": sorted(set(maxw)),
        "canon_spacing_refs": canon_gap,
        "raw_px_spacing": len(RAWPX.findall(live)),
    }

    # tallies
    def tally(t, v=None):
        return sum(1 for e in ents if e["type"] == t and (v is None or e["verdict"] == v))

    retrieved = sum(1 for e in ents if e["verdict"] == "retrieved")
    invented = sum(1 for e in ents if e["verdict"] == "invented")
    if not canon_linked and tally("component", "retrieved") == 0:
        posture = "INVENTED"
    elif tally("colour", "invented") == 0 and tally("token", "invented") == 0 and tally("component", "retrieved"):
        posture = "PURE-RETRIEVAL"
    else:
        posture = "HYBRID"

    return {
        "lineage": lineage,
        "file": os.path.basename(path),
        "canon_linked": canon_linked,
        "posture": posture,
        "candidates": len(CANDIDATE.findall(raw)),
        "entities": ents,
        "layout": layout,
        "summary": {
            "retrieved": retrieved,
            "invented": invented,
            "components_retrieved": tally("component", "retrieved"),
            "tokens_retrieved": tally("token", "retrieved"),
            "tokens_invented": tally("token", "invented"),
            "colours_invented": tally("colour", "invented"),
            "icons_invented": tally("icon", "invented"),
            "rules_honoured": sum(1 for e in ents if e["verdict"] == "honoured"),
            "rules_violated": sum(1 for e in ents if e["verdict"] == "violated"),
            "rules_nd": sum(1 for e in ents if e["verdict"] == "not-detected"),
        },
    }


def collect(spec):
    if os.path.isdir(spec):
        return sorted(glob.glob(os.path.join(spec, "*.html")))
    return [spec] if os.path.exists(spec) else []


def slugify(name):
    return "cn-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build_reading_layer():
    """Embed the actual guideline doc bodies + WCAG descriptions + per-component meta so the
    accordion can display full rule text in-tool (Dave's 'read through them here' ask)."""
    refd = set(["brand-principles.md", "copywriting.md", "dark-mode.md"])
    for c in XREF_COMPS.values():
        refd.update(c.get("guidelines", []))
    docs = {}
    for g in sorted(x for x in refd if x):
        p = os.path.join(HERE, "guidelines", g)
        if os.path.exists(p):
            try:
                docs[g] = open(p, encoding="utf-8").read()
            except Exception:
                pass
    wcag = {sc: {"name": WCAG_NAMES.get(sc, sc), "desc": WCAG_DESC.get(sc, "")}
            for sc in sorted(set(WCAG_NAMES) | set(WCAG_DESC))}  # sorted: deterministic (dream-pass v2 P2, 2026-07-26)
    comp_meta = {}
    for name, c in XREF_COMPS.items():
        slug = "cn-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        ap = c.get("anti_patterns", {})
        comp_meta[slug] = {
            "name": name, "category": c.get("category", ""), "token_count": c.get("token_count", 0),
            "guidelines": c.get("guidelines", []), "wcag": c.get("wcag_sc", []),
            "anti": ((ap.get("asserted") or []) + (ap.get("inferred_review") or []))[:4],
        }
    return {"docs": docs, "wcag": wcag, "comp_meta": comp_meta}


def build_graph(files_data):
    """Build the actual DS knowledge graph from _XREF-INDEX.json: components <-> god-node tokens
    <-> guidelines <-> WCAG SCs. Overlay = which components the §9 spread actually retrieved."""
    xref_path = os.path.join(HERE, "_XREF-INDEX.json")
    try:
        xref = json.load(open(xref_path))
    except Exception:
        return {"nodes": [], "links": [], "note": "no _XREF-INDEX.json"}
    comps = xref.get("components", {})

    # which .cn-* did the spread retrieve?
    used_cn = set()
    for f in files_data:
        for e in f["entities"]:
            if e["type"] == "component" and e["verdict"] == "retrieved":
                used_cn.add(e["name"].lstrip("."))

    # blast counts
    from collections import Counter
    tok_blast, guide_blast, wcag_blast = Counter(), Counter(), Counter()
    for c in comps.values():
        for t in c.get("god_nodes_touched", []):
            tok_blast[t] += 1
        for g in c.get("guidelines", []):
            guide_blast[g] += 1
        for w in c.get("wcag_sc", []):
            wcag_blast[w] += 1

    nodes, links = [], []
    seen = set()

    def add(nid, ntype, label, **kw):
        if nid in seen:
            return
        seen.add(nid)
        nodes.append({"id": nid, "type": ntype, "label": label, **kw})

    for name, c in comps.items():
        add("C:" + name, "component", name, cat=c.get("category", ""),
            retrieved=(slugify(name) in used_cn), degree=c.get("token_count", 0))
    for t, b in tok_blast.items():
        add("T:" + t, "token", t.split("/")[-1], full=t, blast=b)
    for g, b in guide_blast.items():
        add("G:" + g, "guideline", g.replace(".md", ""), blast=b)
    for w, b in wcag_blast.items():
        add("W:" + w, "wcag", w, blast=b)

    for name, c in comps.items():
        cid = "C:" + name
        for t in c.get("god_nodes_touched", []):
            links.append({"s": cid, "t": "T:" + t, "k": "token"})
        for g in c.get("guidelines", []):
            links.append({"s": cid, "t": "G:" + g, "k": "guideline"})
        for w in c.get("wcag_sc", []):
            links.append({"s": cid, "t": "W:" + w, "k": "wcag"})

    return {
        "nodes": nodes, "links": links,
        "counts": {
            "component": sum(1 for n in nodes if n["type"] == "component"),
            "token": sum(1 for n in nodes if n["type"] == "token"),
            "guideline": sum(1 for n in nodes if n["type"] == "guideline"),
            "wcag": sum(1 for n in nodes if n["type"] == "wcag"),
            "retrieved_components": len(used_cn),
        },
    }


def default_lineages():
    ft = os.path.join(HERE, "_fitness-test")
    return {
        "governed-Sonnet": os.path.join(ft, "register-spread-2026-07-05"),
        "governed-Opus": os.path.join(ft, "register-spread-2026-07-05-opus"),
        "diagnostic": os.path.join(ft, "register-spread-2026-07-05-diagnostic"),
    }


# ---------- HTML (Swiss dossier) ----------
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Knowledge-usage trace — §9 spread</title>
<style>
:root{
  --accent:#DB0011; --accent-3:#730014; --black:#000; --white:#fff;
  --g1:#F3F3F3; --g2:#EDEDED; --g3:#D7D8D6; --g5:#9B9B9B; --g6:#767676; --g7:#545454; --g8:#333;
  --ret:#111; --inv:#DB0011; --util:#767676; --dang:#B7791F;
  --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem; --s7:6rem;
  --max:1200px; --font:"Univers Next","Helvetica Neue",Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box;}
body{margin:0;font-family:var(--font);color:var(--black);background:var(--white);
  font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased;}
.prog{position:fixed;top:0;left:0;height:2px;background:var(--accent);width:0;z-index:60;transform-origin:left;}
.nav{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:var(--s3);
  background:var(--white);border-bottom:1px solid var(--g2);height:56px;padding:0 var(--s4);}
.nav .brand{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;display:flex;align-items:center;gap:8px;}
.nav .brand::before{content:"";width:20px;height:1px;background:var(--accent);}
.nav .ctx{font-size:13px;color:var(--g6);}
.nav .spacer{flex:1;}
.nav .meta{font-size:12px;color:var(--g6);letter-spacing:.02em;}
.btn{font-family:var(--font);font-size:12px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;
  background:var(--black);color:var(--white);border:0;padding:10px 16px;cursor:pointer;}
.btn:hover{background:var(--g8);}
.btn.ghost{background:transparent;color:var(--black);border-bottom:1px solid var(--accent);padding:6px 2px;}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--s4);}
.rail{position:fixed;top:96px;left:24px;z-index:30;display:flex;flex-direction:column;gap:10px;}
.rail a{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);text-decoration:none;
  border-left:2px solid var(--g2);padding:2px 0 2px 12px;transition:color .15s,border-color .15s;}
.rail a:hover,.rail a.on{color:var(--black);border-color:var(--accent);}
@media(max-width:1360px){.rail{display:none;}}
.label{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);
  display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s2);}
.label::before{content:"";width:20px;height:1px;background:var(--accent);}
.rule{border:0;border-top:1px solid var(--g2);margin:0;}
.hero{padding:var(--s7) 0 var(--s5);}
.hero h1{font-size:43px;line-height:1.1;font-weight:300;margin:0 0 var(--s4);max-width:16em;}
.hero h1 b{font-weight:600;}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--g2);border:1px solid var(--g2);margin-top:var(--s4);}
.stat{background:var(--white);padding:var(--s3);}
.stat .n{font-size:34px;font-weight:200;line-height:1;}
.stat .n b{font-weight:600;color:var(--accent);}
.stat .c{font-size:12px;color:var(--g6);letter-spacing:.04em;text-transform:uppercase;margin-top:8px;}
section.band{padding:var(--s6) 0;}
.hdr{font-size:19px;font-weight:500;margin:0 0 var(--s2);}
.sub{color:var(--g7);max-width:44em;margin:0 0 var(--s4);}

/* charts */
.chartrow{display:grid;grid-template-columns:1fr 2.4fr;gap:var(--s3);align-items:center;
  padding:10px 0;border-top:1px solid var(--g2);}
.chartrow:first-child{border-top:0;}
.crlabel .f{font-weight:500;font-size:14px;}
.crlabel .l{font-size:11px;color:var(--g6);letter-spacing:.06em;text-transform:uppercase;}
.crlabel .p{font-size:10px;letter-spacing:.08em;text-transform:uppercase;padding:1px 6px;display:inline-block;margin-top:3px;}
.p.PURE-RETRIEVAL{background:#111;color:#fff;}
.p.HYBRID{background:var(--dang);color:#fff;}
.p.INVENTED{background:var(--accent);color:#fff;}
.bar{display:flex;height:26px;background:var(--g1);font-size:11px;color:#fff;overflow:hidden;}
.bar span{display:flex;align-items:center;justify-content:center;min-width:0;white-space:nowrap;}
.bar .ret{background:var(--ret);}
.bar .inv{background:var(--inv);}
.bar .util{background:var(--util);}
.bar .dang{background:var(--dang);}
.legend{display:flex;gap:var(--s3);font-size:12px;color:var(--g7);margin-top:var(--s3);flex-wrap:wrap;}
.legend i{display:inline-block;width:12px;height:12px;margin-right:6px;vertical-align:-1px;}

/* layout dimension */
.dim{display:grid;grid-template-columns:1fr 2fr;gap:var(--s6);align-items:start;}
.dim .idx{font-size:84px;font-weight:200;line-height:.9;color:var(--g3);}
.dim .dl{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--black);font-weight:500;margin-top:var(--s2);}
.gridcmp{display:grid;grid-template-columns:1fr;gap:1px;background:var(--g2);border:1px solid var(--g2);margin-top:var(--s3);}
.gridcmp .gc{background:var(--white);padding:var(--s2) var(--s3);display:grid;grid-template-columns:9rem 1fr;gap:var(--s3);}
.gridcmp .gc .gl{font-size:12px;font-weight:500;letter-spacing:.04em;}
.gridcmp .gc .gv{font-size:12px;color:var(--g7);font-family:ui-monospace,monospace;line-height:1.5;word-break:break-word;}
.gridcmp .gc .gv em{color:var(--accent);font-style:normal;}

/* explorer */
.filters{display:flex;flex-wrap:wrap;gap:var(--s3);align-items:center;padding:var(--s3) 0;border-top:1px solid var(--g2);border-bottom:1px solid var(--g2);position:sticky;top:56px;background:var(--white);z-index:40;}
.cgroup{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
.gl{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);}
.chip{font-family:var(--font);font-size:12px;border:1px solid var(--g3);background:var(--white);padding:5px 10px;cursor:pointer;letter-spacing:.02em;}
.chip.on{background:var(--black);color:var(--white);border-color:var(--black);}
.chip .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;vertical-align:0;}
table{width:100%;border-collapse:collapse;margin-top:var(--s3);font-size:13px;}
th{text-align:left;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--g6);
  border-bottom:1px solid var(--g3);padding:8px 10px;position:sticky;top:var(--thtop,110px);background:var(--white);z-index:20;box-shadow:0 1px 0 var(--g3);}
td{border-bottom:1px solid var(--g2);padding:8px 10px;vertical-align:top;}
tr.tgt td{background:#FFF8F1;}
.ename{font-family:ui-monospace,monospace;font-size:12px;}
.vpill{font-size:10px;letter-spacing:.06em;text-transform:uppercase;padding:1px 7px;color:#fff;display:inline-block;white-space:nowrap;}
.v-retrieved{background:var(--ret);}
.v-invented{background:var(--inv);}
.v-utility{background:var(--util);}
.v-dangling{background:var(--dang);}
.v-honoured{background:#0F9D58;}
.v-violated{background:var(--accent);}
.v-not-detected{background:#B7B7B7;}
.ename.tog{cursor:pointer;border-bottom:1px dotted var(--g3);}
.ename.tog::before{content:"▸ ";color:var(--g5);}
.ename.tog.open::before{content:"▾ ";}
tr.detail td{background:var(--g1);color:var(--g7);font-size:12.5px;line-height:1.6;padding:10px 14px;}
tr.detail .dwrap{max-width:64em;}
tr.detail .dk{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--g6);display:block;margin:10px 0 4px;}
tr.detail p{margin:4px 0;}
tr.detail ul{margin:4px 0 4px 18px;padding:0;}
tr.detail li{margin:2px 0;}
details.doc{border:1px solid var(--g3);background:#fff;margin:5px 0;}
details.doc>summary{cursor:pointer;padding:7px 10px;font-size:12px;color:var(--black);list-style:none;}
details.doc>summary::-webkit-details-marker{display:none;}
details.doc>summary::before{content:"▸ ";color:var(--g5);}
details.doc[open]>summary::before{content:"▾ ";}
details.doc[open]>summary{border-bottom:1px solid var(--g2);}
.docbody{padding:8px 16px 14px;max-height:460px;overflow:auto;color:var(--g8);}
.docbody h3,.docbody h4,.docbody h5,.docbody h6{font-size:13px;margin:12px 0 4px;color:var(--black);letter-spacing:.02em;}
.docbody p{font-size:12.5px;line-height:1.65;}
.docbody code{background:var(--g1);padding:1px 4px;font-size:11.5px;}
.docbody pre{background:var(--g1);padding:8px 10px;overflow:auto;font-size:11.5px;}
.docbody hr{border:0;border-top:1px solid var(--g2);margin:10px 0;}
.docmiss{color:var(--g6);font-style:italic;}
.tp{font-size:11px;color:var(--g6);letter-spacing:.06em;text-transform:uppercase;}
.tgtbtn{font-family:var(--font);font-size:11px;border:1px solid var(--g3);background:var(--white);padding:3px 9px;cursor:pointer;letter-spacing:.04em;text-transform:uppercase;}
.tgtbtn.on{background:var(--accent);color:#fff;border-color:var(--accent);}
.note{width:100%;font-family:var(--font);font-size:12px;border:1px solid var(--g3);padding:5px 7px;resize:vertical;min-height:30px;margin-top:4px;}
.count{color:var(--g5);font-variant-numeric:tabular-nums;}
footer{padding:var(--s6) 0;color:var(--g6);font-size:12px;border-top:1px solid var(--g2);margin-top:var(--s5);}
.modal{position:fixed;inset:0;background:rgba(0,0,0,.5);display:none;align-items:center;justify-content:center;z-index:80;padding:var(--s4);}
.modal.show{display:flex;}
.mcard{background:#fff;max-width:820px;width:100%;max-height:86vh;display:flex;flex-direction:column;}
.mhead{display:flex;align-items:center;gap:var(--s2);padding:var(--s3);border-bottom:1px solid var(--g2);}
.mhead .t{font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:500;flex:1;}
.mbody{padding:var(--s3);overflow:auto;}
textarea.exp{width:100%;height:52vh;font-family:ui-monospace,monospace;font-size:12px;border:1px solid var(--g3);padding:var(--s2);}
.savenote{position:fixed;bottom:20px;right:20px;background:#111;color:#fff;font-size:12px;padding:8px 14px;opacity:0;transition:opacity .2s;z-index:90;letter-spacing:.06em;text-transform:uppercase;}
.savenote.show{opacity:1;}
.insight{border-left:2px solid var(--accent);padding:2px 0 2px var(--s3);margin:var(--s3) 0;max-width:46em;}
.insight b{font-weight:600;}
.gfilters{position:static;}
.gstage{position:relative;border:1px solid var(--g2);background:#FAFAFA;margin-top:var(--s3);}
#gcanvas{display:block;width:100%;height:560px;cursor:grab;}
#gcanvas:active{cursor:grabbing;}
.gtip{position:absolute;pointer-events:none;background:#111;color:#fff;font-size:12px;padding:7px 10px;
  max-width:240px;opacity:0;transition:opacity .1s;z-index:5;line-height:1.4;}
.gtip .tt{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--g5);}
.gtip b{font-weight:600;}
.glegend{position:absolute;top:12px;left:12px;background:rgba(255,255,255,.9);padding:10px 12px;font-size:12px;line-height:1.9;border:1px solid var(--g2);}
.glegend .lg{display:flex;align-items:center;gap:8px;}
.glegend i{width:11px;height:11px;display:inline-block;border-radius:50%;}
.glegend .lg.small{color:var(--g6);font-size:11px;}
.gcaption{position:absolute;bottom:12px;right:12px;left:12px;text-align:right;font-size:12px;color:var(--g7);pointer-events:none;}
@media(max-width:820px){.chartrow,.dim,.stats{grid-template-columns:1fr;}.stats{grid-template-columns:1fr 1fr;}#gcanvas{height:440px;}}
</style></head>
<body>
<div class="prog" id="prog"></div>
<div class="nav">
  <span class="brand">Knowledge-usage trace</span>
  <span class="ctx">§9 spread · 2026-07-05</span>
  <span class="spacer"></span>
  <span class="meta" id="navMeta"></span>
  <button class="btn" onclick="openExport()">Export targets</button>
</div>

<nav class="rail" id="rail">
  <a href="#s-graph">Knowledge graph</a>
  <a href="#s-prov">Provenance</a>
  <a href="#s-layout">Layout</a>
  <a href="#s-explore">Entity explorer</a>
</nav>

<div class="wrap">
  <section class="hero">
    <p class="label">Retrieved vs invented — entity level</p>
    <h1>What did each lineage <b>retrieve</b> from the knowledge base, and what did it <b>invent</b>?</h1>
    <p class="sub">Reconstructed from the artifacts themselves. Colour is a §9 <b>cardinal</b> curb — it must be retrieved, never typed — so any live hex is a cardinal violation. Filter and target specific entities below; your targets export as a worklist.</p>
    <div class="stats" id="stats"></div>
  </section>
</div>
<hr class="rule">

<div class="wrap">
  <section class="band" id="s-graph">
    <p class="label">The knowledge graph — what the engine draws from</p>
    <h2 class="hdr">38 components, wired to the tokens, guidelines and WCAG rules that govern them</h2>
    <p class="sub">This is the graph the trace measures against. Drag a node, hover to isolate its neighbours, switch views. Note what is <b>not</b> here: no page-layout node — because, as the layout section below shows, composition is never graphed. The <b>Retrieval overlay</b> colours each component by whether the §9 spread actually used it.</p>
    <div class="filters gfilters">
      <div class="cgroup"><span class="gl">View</span><span id="gViews"></span></div>
      <div class="cgroup" id="gLayersWrap"><span class="gl">Layers</span><span id="gLayers"></span></div>
      <div class="cgroup"><span class="gl"></span><button class="chip" onclick="graphRestart()">↻ Re-run layout</button></div>
    </div>
    <div class="gstage">
      <canvas id="gcanvas"></canvas>
      <div class="gtip" id="gtip"></div>
      <div class="glegend" id="glegend"></div>
      <div class="gcaption" id="gcaption"></div>
    </div>
  </section>
</div>
<hr class="rule">

<div class="wrap">
  <section class="band" id="s-prov">
    <p class="label">Provenance by screen</p>
    <h2 class="hdr">Every screen, black = retrieved, red = invented</h2>
    <p class="sub">Bar width = entity mentions. The governed lineages sit at near-pure retrieval; the diagnostic (deliberately unconstrained) is where invention lives. Watch that these two axes — provenance and the layout quality Dave preferred — move independently.</p>
    <div id="charts"></div>
    <div class="legend">
      <span><i style="background:var(--ret)"></i>retrieved (canon token / .cn-* / library icon)</span>
      <span><i style="background:var(--inv)"></i>invented (live hex / local var / unknown icon)</span>
      <span><i style="background:var(--util)"></i>utility (.c-* patch layer)</span>
      <span><i style="background:var(--dang)"></i>dangling (defined nowhere)</span>
    </div>
  </section>
</div>
<hr class="rule">

<div class="wrap">
  <section class="band" id="s-layout">
    <div class="dim">
      <div>
        <div class="idx">01</div>
        <div class="dl">What governs layout?</div>
      </div>
      <div>
        <h2 class="hdr">The KB governs the <em>measure</em> — not the <em>composition</em></h2>
        <p class="sub">Direct answer to the question. The knowledge base <b>does</b> govern layout primitives: a 12-column grid, ~1280px max width, 20px gutters/margins and the breakpoint ladder (<span class="ename">web-foundations.md</span> §Responsive grid, <span class="ename">tokens/layout.json</span>, <span class="ename">--layout-web-columns</span>, <span class="ename">--breakpoint-*</span>, <span class="ename">--gap-*</span>). But it governs no <b>page template</b>: the charter states it outright — <em>"the canon has no template layer — this is always inferred"</em> (§ fixed-flex line 34). Confirmed: there is <b>zero</b> <span class="ename">.cn-page / .cn-grid / .cn-layout</span> class. Component-internal composition is retrieved from <span class="ename">.cn-*</span>; the arrangement of components into a screen is <b>always the model's own inference</b>, steered only softly by <span class="ename">brand-principles.md</span> (single focal point, clarity over decoration) and, at expressive only, the Linear/Stripe/Mercury/Ramp reference nudge.</p>
        <div class="insight">
          <b>So layout is the one dimension the rules don't retrieve.</b> The provenance chart above shows governed screens at pure retrieval — but that measures colour, tokens and components, not layout. The "flatness" can't come from retrieving a bad layout, because no layout is retrieved. It comes from composing an inferred layout out of a <b>fixed vocabulary of create.hsbc human components</b> — which is exactly Dave's hypothesis that the rules may be too tight at the source.
        </div>
        <p class="sub">Below: the actual <span class="ename">grid-template-columns</span> each lineage invented for this same screen — the layout divergence made visible.</p>
        <div class="gridcmp" id="gridcmp"></div>
      </div>
    </div>
  </section>
</div>
<hr class="rule">

<div class="wrap">
  <section class="band" id="s-explore">
    <p class="label">Entity explorer</p>
    <h2 class="hdr">Target specific entities — primitives <em>and</em> rules</h2>
    <p class="sub">Now includes the <b>rule layer</b>: WCAG success criteria and create.hsbc principles, with a verdict of <b>honoured</b> / <b>violated</b> / <b>not-detected</b> per screen — the guidelines and A11y rules that <em>are</em> in the graph but that primitive-matching couldn't see. Click any entity name to read its detail. Filter by lineage, type and verdict; mark a <b>target</b> and add a note — targets export as a worklist.</p>
    <div class="filters" id="expFilters">
      <div class="cgroup"><span class="gl">Lineage</span><span id="fLin"></span></div>
      <div class="cgroup"><span class="gl">Type</span><span id="fType"></span></div>
      <div class="cgroup"><span class="gl">Verdict</span><span id="fVer"></span></div>
      <div class="cgroup"><span class="gl"></span><button class="chip" id="fTgt" onclick="toggleTgtOnly()">Targets only</button></div>
    </div>
    <table>
      <thead><tr><th>Entity</th><th>Type</th><th>Verdict</th><th>Lineage · file</th><th class="count">×</th><th>Target</th></tr></thead>
      <tbody id="rows"></tbody>
    </table>
    <p class="sub" id="emptyNote" style="margin-top:var(--s3)"></p>
  </section>
  <footer id="foot"></footer>
</div>

<div class="modal" id="expModal">
  <div class="mcard">
    <div class="mhead"><span class="t">Targeted entities — worklist</span>
      <button class="btn ghost" onclick="copyExp()">Copy</button>
      <button class="btn ghost" onclick="closeExport()">Close</button></div>
    <div class="mbody"><textarea class="exp" id="expText" readonly></textarea></div>
  </div>
</div>
<div class="savenote" id="savenote">saved</div>

<script>
const DATA = __DATA__;
const STORE = "kb-trace-targets-v1";
let state = {}; try{state = JSON.parse(localStorage.getItem(STORE))||{};}catch(e){state={};}
let fLin=null, fType=null, fVer=null, tgtOnly=false;
const expanded=new Set();
const VERDS=["retrieved","invented","utility","dangling","honoured","violated","not-detected"];
const TYPES=["component","token","colour","icon","utility","a11y","principle"];
const PROV=["retrieved","invented","utility","dangling"];

// flatten entities with a stable id
const FLAT=[];
DATA.files.forEach(f=>{
  f.entities.forEach((e,i)=>{
    FLAT.push({id:f.lineage+"|"+f.file+"|"+e.type+"|"+e.name, name:e.name,type:e.type,
      verdict:e.verdict,count:e.count,lineage:f.lineage,file:f.file,detail:e.detail||"",rule_node:e.rule_node||""});
  });
});

function save(){try{localStorage.setItem(STORE,JSON.stringify(state));}catch(e){}
  const n=document.getElementById("savenote");n.classList.add("show");
  clearTimeout(window._st);window._st=setTimeout(()=>n.classList.remove("show"),800);}
function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}

function renderStats(){
  const s=DATA.totals;
  const cells=[
    ["<b>"+s.pct_invented+"%</b>","of primitives invented"],
    [s.retrieved,"retrieved primitives"],
    [s.rules_honoured+"<b>/"+s.rules_violated+"</b>","rules honoured / <b>violated</b>"],
    [DATA.files.length,"screens · "+DATA.lineages.length+" lineages"]
  ];
  document.getElementById("stats").innerHTML=cells.map(c=>
    `<div class="stat"><div class="n">${c[0]}</div><div class="c">${c[1]}</div></div>`).join("");
  document.getElementById("navMeta").textContent=s.retrieved+" retrieved · "+s.invented+" invented";
}

function renderCharts(){
  const order={"governed-Sonnet":0,"governed-Opus":1,"diagnostic":2};
  const files=[...DATA.files].sort((a,b)=>(order[a.lineage]??9)-(order[b.lineage]??9)||a.file.localeCompare(b.file));
  const provTot=f=>f.entities.filter(e=>PROV.includes(e.verdict)).reduce((s,e)=>s+e.count,0);
  const maxTot=Math.max(...files.map(provTot));
  document.getElementById("charts").innerHTML=files.map(f=>{
    const agg={retrieved:0,invented:0,utility:0,dangling:0};
    f.entities.forEach(e=>{if(PROV.includes(e.verdict))agg[e.verdict]=(agg[e.verdict]||0)+e.count;});
    const tot=agg.retrieved+agg.invented+agg.utility+agg.dangling;
    const w=v=>tot?(v/maxTot*100).toFixed(1):0;
    const seg=(cls,v)=>v?`<span class="${cls}" style="width:${w(v)}%">${v>=6?v:""}</span>`:"";
    return `<div class="chartrow">
      <div class="crlabel"><span class="f">${esc(f.file)}</span>
        <div class="l">${esc(f.lineage)}</div>
        <span class="p ${f.posture}">${f.posture}</span></div>
      <div class="bar">${seg("ret",agg.retrieved)}${seg("util",agg.utility)}${seg("dang",agg.dangling)}${seg("inv",agg.invented)}</div>
    </div>`;
  }).join("");
}

function renderGridCmp(){
  const order={"governed-Sonnet":0,"governed-Opus":1,"diagnostic":2};
  // pick the expressive/most-elaborate screen per lineage for a fair layout comparison
  const pick={};
  DATA.files.forEach(f=>{
    const score=f.layout.grid_count;
    if(!pick[f.lineage]||score>pick[f.lineage].layout.grid_count) pick[f.lineage]=f;
  });
  const rows=Object.values(pick).sort((a,b)=>(order[a.lineage]??9)-(order[b.lineage]??9));
  document.getElementById("gridcmp").innerHTML=rows.map(f=>{
    const gs=f.layout.grids.slice(0,4).map(g=>esc(g)).join("<br>")||"<em>none — single-column flow</em>";
    const mw=f.layout.max_widths.join(", ")||"—";
    return `<div class="gc"><div class="gl">${esc(f.lineage)}<br><span class="tp">${f.layout.grid_count} grids · ${f.layout.canon_spacing_refs} canon-space · ${f.layout.raw_px_spacing} raw-px</span></div>
      <div class="gv">${gs}<br><span class="tp">max-width: ${esc(mw)}</span></div></div>`;
  }).join("");
}

function chipRow(el,items,active,fn,colors){
  document.getElementById(el).innerHTML=items.map(it=>{
    const on=active===it?" on":"";
    const dot=colors&&colors[it]?`<span class="dot" style="background:${colors[it]}"></span>`:"";
    return `<button class="chip${on}" onclick="${fn}('${it}')">${dot}${it}</button>`;
  }).join(" ");
}
const VCOL={retrieved:"#111",invented:"#DB0011",utility:"#767676",dangling:"#B7791F",
  honoured:"#0F9D58",violated:"#DB0011","not-detected":"#B7B7B7"};
function renderFilters(){
  chipRow("fLin",DATA.lineages,fLin,"setLin");
  chipRow("fType",TYPES,fType,"setType");
  chipRow("fVer",VERDS,fVer,"setVer",VCOL);
  document.getElementById("fTgt").classList.toggle("on",tgtOnly);
}
function setLin(v){fLin=fLin===v?null:v;renderFilters();renderRows();}
function setType(v){fType=fType===v?null:v;renderFilters();renderRows();}
function setVer(v){fVer=fVer===v?null:v;renderFilters();renderRows();}
function toggleTgtOnly(){tgtOnly=!tgtOnly;renderFilters();renderRows();}

// minimal markdown -> html for reading guideline docs in-tool
function mdToHtml(md){
  if(!md)return "";
  const lines=md.replace(/\r/g,"").split("\n");let out=[],inList=false,inCode=false;
  const inl=s=>esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").replace(/`([^`]+)`/g,"<code>$1</code>")
    .replace(/\[([^\]]+)\]\([^)]+\)/g,"$1");
  const closeL=()=>{if(inList){out.push("</ul>");inList=false;}};
  for(let ln of lines){
    if(ln.trim().startsWith("```")){inCode=!inCode;out.push(inCode?"<pre>":"</pre>");continue;}
    if(inCode){out.push(esc(ln));continue;}
    if(/^---+$/.test(ln.trim())){closeL();out.push("<hr>");continue;}
    let m;
    if(m=ln.match(/^(#{1,6})\s+(.*)/)){closeL();const lv=Math.min(m[1].length+2,6);out.push(`<h${lv}>${inl(m[2])}</h${lv}>`);continue;}
    if(m=ln.match(/^\s*[-*]\s+(.*)/)){if(!inList){out.push("<ul>");inList=true;}out.push(`<li>${inl(m[1])}</li>`);continue;}
    if(!ln.trim()){closeL();continue;}
    closeL();out.push(`<p>${inl(ln)}</p>`);
  }
  closeL();if(inCode)out.push("</pre>");
  return out.join("\n");
}
function docBlock(fname){
  const md=DATA.docs&&DATA.docs[fname];
  if(!md)return `<div class="docmiss">Full text for <code>${esc(fname)}</code> not embedded (not in the referenced set).</div>`;
  return `<details class="doc"><summary>Read <b>${esc(fname)}</b> (${md.length.toLocaleString()} chars)</summary><div class="docbody">${mdToHtml(md)}</div></details>`;
}
function renderDetail(e){
  if(e.type==="a11y"){
    const sc=(e.rule_node||"").replace("W:","");const w=(DATA.wcag||{})[sc]||{};
    return `<div class="dwrap"><span class="dk">WCAG ${esc(sc)} · ${esc(w.name||"")}</span>
      <p><b>Probe:</b> ${esc(e.detail)}</p><p><b>Success criterion:</b> ${esc(w.desc||"—")}</p></div>`;
  }
  if(e.type==="principle"){
    const g=(e.rule_node||"").replace("G:","");
    return `<div class="dwrap"><span class="dk">create.hsbc principle</span>
      <p><b>Probe:</b> ${esc(e.detail)}</p>${docBlock(g)}</div>`;
  }
  if(e.type==="component"){
    const slug=e.name.replace(/^\./,"");const m=(DATA.comp_meta||{})[slug];
    if(!m)return `<div class="dwrap"><span class="dk">component</span>${esc(e.detail)}</div>`;
    const gl=m.guidelines.map(docBlock).join("");
    const wl=m.wcag.map(sc=>{const w=(DATA.wcag||{})[sc]||{};return `<li><b>${esc(sc)}</b> ${esc(w.name||"")} — ${esc(w.desc||"")}</li>`;}).join("");
    const ap=m.anti.length?`<p class="dk">Anti-patterns</p><ul>${m.anti.map(a=>`<li>${esc(a)}</li>`).join("")}</ul>`:"";
    return `<div class="dwrap"><span class="dk">${esc(m.category)} · ${m.token_count} tokens</span>
      <p class="dk">Governing guidelines — click to read</p>${gl||"<p>—</p>"}
      <p class="dk">Must satisfy (WCAG)</p><ul>${wl||"<li>—</li>"}</ul>${ap}</div>`;
  }
  return `<div class="dwrap"><span class="dk">${e.type} · ${e.verdict}</span>${esc(e.detail)||"<em>No detail.</em>"}</div>`;
}
function isTgt(id){return !!(state[id]&&state[id].t);}
function renderRows(){
  let list=FLAT.filter(e=>(!fLin||e.lineage===fLin)&&(!fType||e.type===fType)&&(!fVer||e.verdict===fVer)&&(!tgtOnly||isTgt(e.id)));
  const o={violated:0,invented:1,dangling:2,"not-detected":3,utility:4,honoured:5,retrieved:6};
  list.sort((a,b)=>((o[a.verdict]??9)-(o[b.verdict]??9))||(b.count-a.count)||a.name.localeCompare(b.name));
  document.getElementById("rows").innerHTML=list.map(e=>{
    const t=isTgt(e.id);const note=(state[e.id]&&state[e.id].n)||"";const op=expanded.has(e.id);
    let html=`<tr class="${t?'tgt':''}">
      <td><span class="ename tog${op?' open':''}" onclick="toggleExp('${e.id}')">${esc(e.name)}</span>${t?`<textarea class="note" placeholder="why target this…" oninput="setNote('${e.id}',this.value)">${esc(note)}</textarea>`:""}</td>
      <td><span class="tp">${e.type}</span></td>
      <td><span class="vpill v-${e.verdict}">${e.verdict}</span></td>
      <td><span class="tp">${esc(e.lineage)}</span><br>${esc(e.file)}</td>
      <td class="count">${e.count}</td>
      <td><button class="tgtbtn${t?' on':''}" onclick="toggleTgt('${e.id}')">${t?'✓ target':'target'}</button></td>
    </tr>`;
    if(op){html+=`<tr class="detail"><td colspan="6">${renderDetail(e)}</td></tr>`;}
    return html;
  }).join("");
  document.getElementById("emptyNote").textContent=list.length?"":"No entities match these filters.";
}
function toggleExp(id){expanded.has(id)?expanded.delete(id):expanded.add(id);renderRows();}
function toggleTgt(id){state[id]=state[id]||{};state[id].t=!state[id].t;if(!state[id].t&&!state[id].n)delete state[id];save();renderRows();}
function setNote(id,v){state[id]=state[id]||{t:true};state[id].n=v;save();}

function buildExp(){
  const tgts=FLAT.filter(e=>isTgt(e.id));
  let out="# Knowledge-usage — targeted entities\n\nGenerated from _KNOWLEDGE-USAGE-TRACE.html · "+new Date().toISOString().slice(0,10)+"\n\n";
  if(!tgts.length){return out+"_(no entities targeted yet)_\n";}
  const byLin={};tgts.forEach(e=>{(byLin[e.lineage]=byLin[e.lineage]||[]).push(e);});
  Object.keys(byLin).forEach(l=>{
    out+="## "+l+"\n\n| entity | type | verdict | file | × | note |\n|---|---|---|---|--:|---|\n";
    byLin[l].forEach(e=>{const n=(state[e.id]&&state[e.id].n)||"";
      out+=`| \`${e.name}\` | ${e.type} | ${e.verdict} | ${e.file} | ${e.count} | ${n.replace(/\n/g,' ')} |\n`;});
    out+="\n";
  });
  return out;
}
function openExport(){document.getElementById("expText").value=buildExp();document.getElementById("expModal").classList.add("show");}
function closeExport(){document.getElementById("expModal").classList.remove("show");}
function copyExp(){const t=document.getElementById("expText");t.select();try{document.execCommand("copy");}catch(e){}
  const b=event.target,o=b.textContent;b.textContent="Copied";setTimeout(()=>b.textContent=o,1200);}
document.getElementById("expModal").addEventListener("click",e=>{if(e.target.id==="expModal")closeExport();});

document.getElementById("foot").innerHTML="Generated by <span class='ename'>_build_trace_dossier.py</span> · measures provenance/adherence, not layout quality or gestalt. A screen can be pure-retrieval and still feel flat, or invented and feel great — read alongside the visual verdict, not instead of it.";

const RAIL=[["s-graph"],["s-prov"],["s-layout"],["s-explore"]];
function computeStick(){const nav=document.querySelector(".nav").offsetHeight||56;
  const ef=document.getElementById("expFilters");const fh=ef?ef.offsetHeight:52;
  document.documentElement.style.setProperty("--thtop",(nav+fh)+"px");}
function onScroll(){const h=document.documentElement;const sc=h.scrollTop/(h.scrollHeight-h.clientHeight||1);
  document.getElementById("prog").style.transform="scaleX("+sc+")";
  // rail spy
  const y=h.scrollTop+120;let cur=RAIL[0][0];
  RAIL.forEach(r=>{const el=document.getElementById(r[0]);if(el&&el.offsetTop<=y)cur=r[0];});
  document.querySelectorAll(".rail a").forEach(a=>a.classList.toggle("on",a.getAttribute("href")==="#"+cur));}
addEventListener("scroll",onScroll);
addEventListener("resize",computeStick);

/* ---------------- knowledge graph (hand-rolled canvas force sim) ---------------- */
const GTYPE={component:{c:"#111",r:6,label:"Component"},token:{c:"#DB0011",r:5,label:"God-node token"},
  guideline:{c:"#2563EB",r:5,label:"Guideline"},wcag:{c:"#0F9D58",r:4,label:"WCAG SC"}};
let gView="structure", gLayers={token:true,guideline:true,wcag:true};
const G=DATA.graph||{nodes:[],links:[]};
const cv=document.getElementById("gcanvas"), cx=cv.getContext("2d");
let N=[],L=[],anim=null,drag=null,hover=null,DPR=Math.min(devicePixelRatio||1,2);
let W=0,H=0;

function sizeCanvas(){const r=cv.getBoundingClientRect();W=r.width;H=r.height;
  cv.width=W*DPR;cv.height=H*DPR;cx.setTransform(DPR,0,0,DPR,0,0);}

function activeNodes(){
  if(gView==="blast"){return G.nodes.filter(n=>n.type==="token");}
  return G.nodes.filter(n=>n.type==="component"||(gLayers[n.type]));
}
function buildSim(){
  sizeCanvas();
  const keep=new Set(activeNodes().map(n=>n.id));
  N=G.nodes.filter(n=>keep.has(n.id)).map(n=>({...n,
    x:W/2+(Math.random()-.5)*W*.6, y:H/2+(Math.random()-.5)*H*.6, vx:0,vy:0,
    r:(GTYPE[n.type].r)+(n.blast?Math.min(n.blast*0.5,7):0)+(n.type==="component"?Math.min((n.degree||0)*0.15,4):0)}));
  const idx={};N.forEach(n=>idx[n.id]=n);
  L=(gView==="blast"?[]:G.links.filter(l=>keep.has(l.s)&&keep.has(l.t)&&gLayers[l.k]))
    .map(l=>({s:idx[l.s],t:idx[l.t],k:l.k})).filter(l=>l.s&&l.t);
  // blast view: radial ring by blast desc
  N.forEach(n=>n.pinned=false);
  if(gView==="blast"){
    const s=[...N].sort((a,b)=>b.blast-a.blast);
    s.forEach((n,i)=>{const ang=i/s.length*Math.PI*2;const rad=70+(18-Math.min(n.blast,18))*12;
      n.x=W/2+Math.cos(ang)*rad;n.y=H/2+Math.sin(ang)*rad;n.pinned=true;});
  }
  cool=1;startAnim();
}
let cool=1;
function step(){
  const rep=gView==="blast"?1400:2200, klen=gView==="blast"?0:64;
  for(let i=0;i<N.length;i++){const a=N[i];
    for(let j=i+1;j<N.length;j++){const b=N[j];
      let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy||1;if(d2>90000)continue;
      let d=Math.sqrt(d2),f=rep/d2;dx/=d;dy/=d;a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f;}}
  L.forEach(l=>{let dx=l.t.x-l.s.x,dy=l.t.y-l.s.y,d=Math.sqrt(dx*dx+dy*dy)||1,f=(d-klen)*0.012;
    dx/=d;dy/=d;l.s.vx+=dx*f;l.s.vy+=dy*f;l.t.vx-=dx*f;l.t.vy-=dy*f;});
  N.forEach(n=>{if(n.pinned&&n!==drag)return;n.vx+=(W/2-n.x)*0.002;n.vy+=(H/2-n.y)*0.002;
    if(n===drag)return;n.vx*=0.86;n.vy*=0.86;n.x+=n.vx*cool;n.y+=n.vy*cool;
    n.x=Math.max(n.r,Math.min(W-n.r,n.x));n.y=Math.max(n.r,Math.min(H-n.r,n.y));});
  cool*=0.992;if(cool<0.03)cool=0.03;
}
function draw(){
  cx.clearRect(0,0,W,H);
  const hi=hover, nb=new Set();
  if(hi){nb.add(hi.id);L.forEach(l=>{if(l.s===hi)nb.add(l.t.id);if(l.t===hi)nb.add(l.s.id);});}
  L.forEach(l=>{const on=!hi||(nb.has(l.s.id)&&nb.has(l.t.id));
    cx.strokeStyle=on?(hi?"rgba(17,17,17,.28)":"rgba(0,0,0,.09)"):"rgba(0,0,0,.03)";
    cx.lineWidth=on&&hi?1.2:0.6;cx.beginPath();cx.moveTo(l.s.x,l.s.y);cx.lineTo(l.t.x,l.t.y);cx.stroke();});
  N.forEach(n=>{const on=!hi||nb.has(n.id);
    let col=GTYPE[n.type].c;
    if(gView==="overlay"&&n.type==="component")col=n.retrieved?"#111":"#D7D8D6";
    cx.globalAlpha=on?1:0.18;cx.beginPath();cx.arc(n.x,n.y,n.r,0,7);cx.fillStyle=col;cx.fill();
    if(gView==="overlay"&&n.type==="component"&&!n.retrieved){cx.lineWidth=1;cx.strokeStyle="#B7B7B7";cx.stroke();}
    if(n===hi){cx.lineWidth=2;cx.strokeStyle=col;cx.stroke();}
    cx.globalAlpha=1;});
  // labels for big/hovered nodes
  cx.font="11px "+getComputedStyle(document.body).fontFamily;cx.fillStyle="#333";
  N.forEach(n=>{const big=(n.blast&&n.blast>=7)||(n.type==="component"&&(n.degree||0)>=11);
    if((big&&(!hi))||n===hi||(hi&&nb.has(n.id)&&(n.type==="component"||n.blast>=6))){
      cx.globalAlpha=(!hi||nb.has(n.id))?1:0.2;cx.fillText(n.label,n.x+n.r+3,n.y+3);cx.globalAlpha=1;}});
}
function frame(){step();draw();anim=requestAnimationFrame(frame);}
function startAnim(){if(anim)cancelAnimationFrame(anim);frame();}
function graphRestart(){buildSim();}

function pick(mx,my){let best=null,bd=999;N.forEach(n=>{const d=Math.hypot(n.x-mx,n.y-my);
  if(d<Math.max(n.r+4,9)&&d<bd){bd=d;best=n;}});return best;}
function evtPos(e){const r=cv.getBoundingClientRect();const t=e.touches?e.touches[0]:e;
  return {x:t.clientX-r.left,y:t.clientY-r.top};}
cv.addEventListener("mousemove",e=>{const p=evtPos(e);
  if(drag){drag.x=p.x;drag.y=p.y;drag.vx=drag.vy=0;cool=Math.max(cool,.5);return;}
  hover=pick(p.x,p.y);const tip=document.getElementById("gtip");
  if(hover){const g=GTYPE[hover.type];let extra="";
    if(hover.type==="token")extra="touches <b>"+hover.blast+"</b> components · "+esc(hover.full||"");
    else if(hover.blast)extra="on <b>"+hover.blast+"</b> components";
    else if(hover.type==="component")extra=(gView==="overlay"?(hover.retrieved?"<b>retrieved</b> by the spread":"<b>not used</b> by the spread"):esc(hover.cat||""));
    tip.innerHTML="<span class='tt'>"+g.label+"</span><br><b>"+esc(hover.label)+"</b><br>"+extra;
    tip.style.left=Math.min(p.x+14,W-250)+"px";tip.style.top=(p.y+14)+"px";tip.style.opacity=1;cv.style.cursor="pointer";}
  else{tip.style.opacity=0;cv.style.cursor="grab";}});
cv.addEventListener("mousedown",e=>{const p=evtPos(e);drag=pick(p.x,p.y);if(drag){drag.fixed=true;}});
addEventListener("mouseup",()=>{drag=null;});
cv.addEventListener("mouseleave",()=>{hover=null;document.getElementById("gtip").style.opacity=0;});

function renderGraphControls(){
  const views=[["structure","Structure"],["blast","Blast radius"],["overlay","Retrieval overlay"]];
  document.getElementById("gViews").innerHTML=views.map(v=>
    `<button class="chip${gView===v[0]?' on':''}" onclick="setGView('${v[0]}')">${v[1]}</button>`).join(" ");
  const layers=[["token","tokens"],["guideline","guidelines"],["wcag","WCAG"]];
  document.getElementById("gLayers").innerHTML=layers.map(l=>
    `<button class="chip${gLayers[l[0]]?' on':''}" onclick="toggleLayer('${l[0]}')"><span class="dot" style="background:${GTYPE[l[0]].c}"></span>${l[1]}</button>`).join(" ");
  document.getElementById("gLayersWrap").style.display=gView==="structure"?"":"none";
  // legend + caption
  const lg=[["component","Component"],["token","God-node token"],["guideline","Guideline"],["wcag","WCAG SC"]];
  let leg=lg.map(x=>`<div class="lg"><i style="background:${GTYPE[x[0]].c}"></i>${x[1]}</div>`).join("");
  if(gView==="overlay")leg=`<div class="lg"><i style="background:#111"></i>retrieved by spread</div><div class="lg"><i style="background:#D7D8D6"></i>never used</div><div class="lg small">${G.counts.retrieved_components} of ${G.counts.component} components used</div>`;
  if(gView==="blast")leg=`<div class="lg small">Ring: inner = highest blast radius.<br>Bigger = more components depend on it.</div>`;
  document.getElementById("glegend").innerHTML=leg;
  const caps={structure:G.counts.component+" components · "+G.counts.token+" god-tokens · "+G.counts.guideline+" guidelines · "+G.counts.wcag+" WCAG rules",
    blast:"18 god-node tokens — the shared dependencies. Change one, and every linked component moves.",
    overlay:"Grey = a governed component the §9 spread never reached. The vocabulary is larger than any one screen uses."};
  document.getElementById("gcaption").textContent=caps[gView];
}
function setGView(v){gView=v;renderGraphControls();buildSim();}
function toggleLayer(k){gLayers[k]=!gLayers[k];renderGraphControls();buildSim();}
let rz;addEventListener("resize",()=>{clearTimeout(rz);rz=setTimeout(buildSim,200);});

renderStats();renderCharts();renderGridCmp();renderFilters();renderRows();
renderGraphControls();buildSim();computeStick();onScroll();
addEventListener("load",computeStick);
</script>
</body></html>
"""


def build(lineages):
    files_data = []
    for label, spec in lineages.items():
        for f in collect(spec):
            files_data.append(entities_for_file(f, label))

    # totals
    all_ents = [e for f in files_data for e in f["entities"]]
    tot_mentions = sum(e["count"] for e in all_ents)
    retrieved = sum(1 for e in all_ents if e["verdict"] == "retrieved")
    invented = sum(1 for e in all_ents if e["verdict"] == "invented")
    denom = retrieved + invented or 1
    totals = {
        "retrieved": retrieved,
        "invented": invented,
        "pct_invented": round(invented / denom * 100),
        "colours_invented": sum(1 for e in all_ents if e["type"] == "colour"),
        "mentions": tot_mentions,
        "rules_honoured": sum(1 for e in all_ents if e["verdict"] == "honoured"),
        "rules_violated": sum(1 for e in all_ents if e["verdict"] == "violated"),
        "rules_nd": sum(1 for e in all_ents if e["verdict"] == "not-detected"),
    }
    reading = build_reading_layer()
    payload = {
        "lineages": list(lineages.keys()),
        "files": files_data,
        "totals": totals,
        "graph": build_graph(files_data),
        "docs": reading["docs"],
        "wcag": reading["wcag"],
        "comp_meta": reading["comp_meta"],
    }
    json.dump(payload, open(OUT_JSON, "w"), indent=2)
    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(payload))
    open(OUT_HTML, "w", encoding="utf-8").write(html)
    print("Wrote", os.path.relpath(OUT_HTML, HERE), "and", os.path.relpath(OUT_JSON, HERE))
    print(f"  {len(files_data)} files · {retrieved} retrieved · {invented} invented "
          f"({totals['pct_invented']}% invented) · {totals['colours_invented']} invented colours")


def main():
    args = [a for a in sys.argv[1:]]
    if args:
        lineages = {}
        for a in args:
            label, p = a.split("=", 1)
            lineages[label] = p if os.path.isabs(p) else os.path.join(HERE, p)
    else:
        lineages = default_lineages()
    build(lineages)


if __name__ == "__main__":
    main()
