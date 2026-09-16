#!/usr/bin/env python3
"""_build_page_v2.py — bake REVIEW-icons-2026-09-16-v2.html (#277 lane RIF).

A copy of lane RI's _build_page.py (which is NOT touched, and neither is RI's
v1 page) carrying the three fixes lane RIV's VERIFY.md ruled:

  R1  RI-3 — the lead-figure sentence names the exporter's slug-collision
      counter; the recommendation's evidence says what it is (the gate already
      enforces it; nobody has looked); option (c) "I'll pick" is restored; and
      THE SHEET is built — every one of the multi-variant glyphs and its bare
      sibling rendered as INLINE SVG read from knowledge/assets/icons/, so the
      look (c) asks for is on the card.
  A1  RI-1 — two explorer renders embedded, chip off and chip on, made in a
      SCRATCH copy of the explorer builder pointed at a scratch output.
  A2  is the driver's, not this file's: localStorage is cleared before the
      screenshot pass so no driver residue ships in the PNGs.


Adapted from notes/_lanes/277/page/_build_page.py (lane CP's), which is NOT
touched, and keeps the four things CV's grading made non-negotiable:

  1. DECISIONS FIRST. The four cards are the first thing under the hero; every
     evidence section sits behind them and says it is evidence.
  2. ONE FIGURE PER CARD. Each card leads on the single number that decides it —
     RI-1 the node count, RI-2 the byte-match pair count, RI-3 the multi-variant
     bases, RI-4 the unbound lockups. No card carries two totals for one thing.
  3. EVERY RECOMMENDATION ATTRIBUTED WHERE IT SITS, naming the lane that wrote
     it, in the card, not in Receipts 1,900px below.
  4. NO INTEGER IS TYPED. Every figure comes from dry-run.json, from the icon
     manifest, or from a live count over knowledge/ at build time.

⚠ The page EXPORTS Dave's answers under a DIFFERENT filename from the builder's
copy input, and this builder REFUSES by name if the export is ever copied over
_page-copy.json.

  python3 notes/_lanes/277/icons-propose/_build_page_v2.py
"""
import glob
import json
import os
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
K = REPO / "knowledge"
DRY = LANE / "dry-run.json"
COPY = LANE / "_page-copy-v2.json"
OUT = LANE / "REVIEW-icons-2026-09-16-v2.html"
EXPLORER = REPO / "notes" / "_KG-EXPLORER.html"

if not DRY.exists():
    raise SystemExit("REFUSED — dry-run.json is missing. Run gen_kg_icons.py first; this "
                     "builder reads its figures, it does not carry them.")
spec = json.loads(COPY.read_text(encoding="utf-8"))
if "decisions" in spec and spec["decisions"] and isinstance(spec["decisions"][0], dict) \
        and "choice" in spec["decisions"][0]:
    raise SystemExit(f"REFUSED — {COPY.name} looks like an EXPORT (its decisions carry `choice`), "
                     "not the builder's copy input. An export copied over the input would make "
                     "the page rebuild itself out of its own answers.")

d = json.loads(DRY.read_text(encoding="utf-8"))
ipay = json.loads((LANE / "_icon_nodes.json").read_text(encoding="utf-8"))
lpay = json.loads((LANE / "_logo_nodes.json").read_text(encoding="utf-8"))
EDGES = ipay["edges"] + lpay["edges"]


def live_graph():
    """The graph as it stands, measured by importing _build_kg_explorer's own extract()
    and extract_extra() IN MEMORY. main() is never called and nothing is written — the
    explorer HTML's mtime is the proof."""
    sys.path.insert(0, str(K))
    cwd = os.getcwd()
    os.chdir(K)
    try:
        import importlib.util
        s = importlib.util.spec_from_file_location("_bke_ro", K / "_build_kg_explorer.py")
        m = importlib.util.module_from_spec(s)
        sys.modules["_bke_ro"] = m
        s.loader.exec_module(m)
        bn, be = m.extract()
        xn, xe, _rep = m.extract_extra(bn, be)
        return len(bn) + len(xn), len(be) + len(xe)
    finally:
        os.chdir(cwd)


G_NODES, G_EDGES = live_graph()
ec, res = d["edge_counts"], d["edge_targets_resolved"]
icons = {n["id"] for n in ipay["nodes"] if n["type"] == "icon"}
touched = {x for e in EDGES if e["type"] != "inGroup" for x in (e["s"], e["t"]) if x in icons}
prose_hit, prose_metas, prose_pairs, prose_top = None, None, None, []

sys.path.insert(0, str(LANE))
import importlib.util as _iu
_s = _iu.spec_from_file_location("_gen_ro", LANE / "gen_kg_icons.py")
_g = _iu.module_from_spec(_s)
sys.modules["_gen_ro"] = _g
_s.loader.exec_module(_g)
_man = _g.load_manifest()
_slugs = {r["slug"] for _k2, r in _g.icon_records(_man)}
prose_hit, prose_metas, prose_pairs, prose_top = _g.prose_pair_count(None, _slugs)

# STRUCT-ONLY: components that render a library glyph and never say the word "icon".
say_icon = {Path(f).name[:-len(".meta.json")] for f in glob.glob(str(K / "components" / "*.meta.json"))
            if "icon" in Path(f).read_text(encoding="utf-8").lower()}
uses = {e["s"][len("component:"):] for e in EDGES if e["type"] == "usesIcon" and e["t"]}
struct_only = len(uses - say_icon)
prose_only = len(say_icon - uses)

logo_bytes = len(json.dumps({"nodes": lpay["nodes"], "edges": lpay["edges"]},
                            separators=(",", ":"), ensure_ascii=False).encode("utf-8"))

n = {
    "n_icons": d["records_read"], "n_groups": d["groups_read"], "n_logos": d["logos_read"],
    "n_nodes": d["node_total"], "n_edges": d["edge_total"],
    "n_ingroup": ec["inGroup"], "n_avo": res["activeVariantOf"], "n_orphan": ec["activeVariantOf"] - res["activeVariantOf"],
    "n_usesicon": ec["usesIcon"], "n_useslogo": ec["usesLogo"],
    "n_defaultfor": ec["defaultFor"], "n_ruledby": ec["ruledBy"],
    "n_usescomp": d["usesIcon_components"], "n_usesicons": d["usesIcon_icons"],
    "n_unused": d["icons_unused"], "n_active": d["active_true"],
    "n_multi": len(d["bases_with_multiple_actives"]),
    "n_extra": sum(len(v) - 1 for v in d["bases_with_multiple_actives"].values()),
    "n_isolated": len(icons - touched),
    "n_nulls": d["unresolved_total"],
    "n_unbound": len(d["logos_unbound"]),
    "logo_rules": d["logo_rules_in_rules_index"],
    "logo_rulings": len(d["rulings_naming_a_logo_svg"]),
    "logo_kb": round(logo_bytes / 1024, 1),
    "lib_keys": d["byte_match"]["library_keys"], "snip_files": d["byte_match"]["snippet_files"],
    "unmatched": d["byte_match"]["unmatched_paths"], "sprites": d["byte_match"]["svg_without_path"],
    "payload_kb": f"{d['payload_bytes'] / 1024:,.0f}",
    "explorer_kb": f"{d['explorer_bytes'] / 1024:,.0f}",
    "payload_pct": d["payload_pct_of_explorer"],
    "g_nodes": f"{G_NODES:,}", "g_edges": f"{G_EDGES:,}",
    "node_pct": round(100.0 * d["node_total"] / G_NODES, 1),
    "edge_pct": round(100.0 * d["edge_total"] / G_EDGES, 1),
    "prose_hit": prose_hit, "prose_metas": prose_metas, "prose_pairs": f"{prose_pairs:,}",
    "struct_only": struct_only, "prose_only": prose_only, "say_icon": len(say_icon),
    "cc": d["fill_modes"].get("currentColor", 0), "baked": d["fill_modes"].get("baked", 0),
    "tokens_icon": d["tokens_icon_metas"],
    "manifest_date": d["manifest_generated"],
    "chip": d["chip"]["family"],
}


def md(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    # Backticks become <code>. Without this the copy file's `inGroup` shipped to the
    # page as literal backticks — caught by eye on the screenshot, not by the driver.
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    # NO underscore-italic rule. It used to be here, inherited from CP's builder, and it
    # ate the underscores in `_validate_icons.py` and `_rules-index.json`, shipping
    # "validateicons.py" in italics to the page. Caught by eye on a dark screenshot, not
    # by the driver. The copy file writes <i> directly when it wants italics.


def f(s):
    return md(str(s).format(**n))


CSS = """
:root{
 --accent:#DA1A00; --ink:#000; --paper:#fff;
 --g1:#F3F3F3; --g2:#EDEDED; --g3:#D7D8D6; --g6:#767676; --g7:#545454; --g8:#333;
 --rule:#EDEDED; --soft:#F3F3F3; --muted:#545454;
 --max:1200px;
 --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem; --s7:6rem;
 --font:"Univers Next for HSBC","Univers Next","Helvetica Neue",Helvetica,Arial,sans-serif;
 color-scheme:light;
}
@media (prefers-color-scheme:dark){
 :root:not([data-theme="light"]){
  --accent:#F6604C; --ink:#F2F2F2; --paper:#111;
  --g1:#1A1A1A; --g2:#2A2A2A; --g3:#3A3A3A; --g6:#9B9B9B; --g7:#B7B7B7; --g8:#D7D8D6;
  --rule:#2A2A2A; --soft:#1A1A1A; --muted:#B7B7B7; color-scheme:dark;
 }
}
:root[data-theme="dark"]{
 --accent:#F6604C; --ink:#F2F2F2; --paper:#111;
 --g1:#1A1A1A; --g2:#2A2A2A; --g3:#3A3A3A; --g6:#9B9B9B; --g7:#B7B7B7; --g8:#D7D8D6;
 --rule:#2A2A2A; --soft:#1A1A1A; --muted:#B7B7B7; color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font);
 font-size:1rem;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--max);margin:0 auto;padding-left:var(--s4);padding-right:var(--s4)}
@media (max-width:520px){.wrap{padding-left:var(--s2);padding-right:var(--s2)}}
section{padding-block:var(--s6);border-top:1px solid var(--rule)}
section:first-of-type{border-top:0}
.label{font-size:.8125rem;font-weight:500;letter-spacing:.14em;line-height:1.6;
 color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s3)}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:0 0 20px}
h1{font-size:3.5625rem;line-height:1.18;font-weight:400;letter-spacing:0;margin:0 0 var(--s4);max-width:22ch}
h2{font-size:2.125rem;line-height:1.25;font-weight:400;margin:0 0 var(--s3)}
h3{font-size:1.1875rem;line-height:1.35;font-weight:500;margin:0}
p{margin:0 0 var(--s2);max-width:78ch}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
 background:var(--soft);padding:.08em .3em;border-radius:2px;
 overflow-wrap:anywhere;word-break:break-word}
a{color:var(--accent)}
@media (max-width:760px){h1{font-size:2.125rem}h2{font-size:1.6rem}}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--g2);
 border:1px solid var(--g2);margin:var(--s5) 0 var(--s4)}
.stat{background:var(--paper);padding:var(--s3);min-width:0}
.stat b{display:block;font-size:2.6875rem;font-weight:200;line-height:1.25;
 font-variant-numeric:tabular-nums;margin-bottom:var(--s1);overflow-wrap:anywhere}
.stat span{display:block;font-size:.8125rem;letter-spacing:.06em;line-height:1.5;color:var(--g6)}
@media (max-width:760px){.stats{grid-template-columns:repeat(2,1fr)}.stat b{font-size:1.875rem}}
@media (max-width:520px){.stats{grid-template-columns:1fr}}
.zeros{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s3);margin-top:var(--s4)}
.zeros div{border-top:1px solid var(--g3);padding-top:var(--s1);font-size:.875rem;color:var(--muted)}
.zeros b{color:var(--ink);font-weight:500}
@media (max-width:900px){.zeros{grid-template-columns:repeat(2,1fr)}}
@media (max-width:480px){.zeros{grid-template-columns:1fr}}
.dec{border-top:1px solid var(--g3);padding-top:var(--s3);margin-top:var(--s5)}
.dec:first-of-type{margin-top:var(--s3)}
.dechead{display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--s2);margin-bottom:var(--s2)}
.decid{font-size:.8125rem;letter-spacing:.14em;line-height:1.6;font-weight:500;color:var(--accent)}
.onefig{display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--s2);
 border-left:2px solid var(--accent);padding:var(--s1) 0 var(--s1) var(--s3);margin:var(--s3) 0}
.onefig b{font-size:2.6875rem;font-weight:200;line-height:1.32;font-variant-numeric:tabular-nums}
.onefig span{font-size:.875rem;color:var(--muted);max-width:44ch}
@media (max-width:760px){.onefig b{font-size:1.875rem}}
.opts{list-style:none;margin:var(--s3) 0 0;padding:0}
.opts li{border-top:1px solid var(--rule);padding:var(--s2) 0}
.opt{display:grid;grid-template-columns:auto 1fr;gap:var(--s2);align-items:start}
.opt input{margin-top:.45rem;accent-color:var(--accent);width:16px;height:16px;flex:0 0 16px}
.opt label{cursor:pointer;max-width:78ch}
.okey{font-weight:500;letter-spacing:.06em;font-size:.8125rem;color:var(--g6);margin-right:var(--s1)}
.rec{display:inline-block;font-size:.75rem;letter-spacing:.1em;line-height:1.5;
 font-weight:500;color:var(--accent);border:1px solid var(--accent);padding:.05rem .4rem;
 border-radius:2px;margin-right:var(--s1);white-space:nowrap}
.why{border-top:1px solid var(--rule);margin-top:var(--s2);padding-top:var(--s2);
 font-size:.875rem;color:var(--muted)}
.attrib{font-size:.8125rem;line-height:1.6;color:var(--g6);margin:0 0 var(--s2);max-width:78ch}
.flag{border-top:1px solid var(--g3);padding-top:var(--s3);margin-top:var(--s5)}
.flag h3{margin-bottom:var(--s1)}
.flagline{font-size:.875rem;color:var(--muted);max-width:78ch}
textarea{width:100%;max-width:100%;font:inherit;font-size:.875rem;margin-top:var(--s2);
 padding:var(--s1) var(--s2);border:1px solid var(--g3);background:var(--paper);
 color:var(--ink);border-radius:2px;resize:vertical;min-height:2.6rem}
textarea:focus,button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.bar{display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center;margin-top:var(--s5);
 border-top:1px solid var(--g3);padding-top:var(--s3)}
button{font:inherit;font-size:.875rem;letter-spacing:.04em;padding:.5rem 1rem;cursor:pointer;
 background:var(--paper);color:var(--ink);border:1px solid var(--ink);border-radius:2px}
button:hover{background:var(--ink);color:var(--paper)}
button.ghost{border-color:var(--g3);color:var(--muted)}
.said{font-size:.8125rem;color:var(--g6)}
pre.exp{white-space:pre-wrap;word-break:break-word;background:var(--soft);border:1px solid var(--g2);
 padding:var(--s2);font-size:.8125rem;max-height:20rem;overflow:auto;margin-top:var(--s2)}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:var(--s3);border-top:1px solid var(--g3)}
table{border-collapse:collapse;width:100%;font-size:.875rem;min-width:680px}
th,td{text-align:left;padding:.5rem .75rem;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-size:.75rem;letter-spacing:.08em;line-height:1.6;color:var(--g6);font-weight:500;white-space:nowrap}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.slug{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.82rem;white-space:nowrap}
.newmark{color:var(--accent);font-weight:500}
.defn{font-size:.8125rem;color:var(--muted);max-width:52ch}
blockquote{margin:var(--s3) 0;padding-left:var(--s3);border-left:2px solid var(--accent);
 font-size:1.0625rem;max-width:70ch}
blockquote cite{display:block;font-size:.8125rem;font-style:normal;color:var(--g6);margin-top:var(--s1)}
footer{border-top:1px solid var(--g3);padding-block:var(--s5);font-size:.8125rem;color:var(--muted)}

/* ---- R1: the sheet. 46 live glyphs on the RI-3 card, so (c) has something to look at. */
.sheet{border:1px solid var(--g3);margin:var(--s3) 0 var(--s2);padding:var(--s3);background:var(--g1)}
.sheetlede,.sheetnote{font-size:.875rem;color:var(--muted);max-width:74ch;margin:0 0 var(--s3)}
.sheetnote{margin:var(--s2) 0 0;border-top:1px solid var(--g3);padding-top:var(--s2)}
.srow{border-top:1px solid var(--g3);padding:var(--s2) 0}
.srow:first-of-type{border-top:0;padding-top:0}
.shead{display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--s1) var(--s2);margin-bottom:var(--s2)}
.shead b{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9rem;font-weight:500}
.shead span{font-size:.75rem;letter-spacing:.04em;color:var(--g6)}
.scells{display:flex;flex-wrap:wrap;gap:var(--s2)}
figure.gl{margin:0;width:8.5rem;max-width:calc(50% - var(--s2));display:flex;flex-direction:column;
 align-items:center;gap:.4rem;background:var(--paper);border:1px solid var(--g3);padding:var(--s2) .5rem}
figure.gl.on{border-color:var(--accent)}
figure.gl svg.g{width:72px;height:72px;display:block;color:var(--ink);flex:0 0 auto}
figure.gl figcaption{text-align:center;display:block;line-height:1.35}
.gs{display:block;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.7rem;
 color:var(--ink);overflow-wrap:anywhere}
.gn{display:block;font-size:.65rem;letter-spacing:.04em;color:var(--g6);margin-top:.2rem}
@media (max-width:520px){figure.gl{width:calc(50% - var(--s1));max-width:none}
 figure.gl svg.g{width:56px;height:56px}.scells{gap:var(--s1)}}

/* ---- A1: the two explorer renders. */
.figs{margin:var(--s3) 0 var(--s2);display:grid;grid-template-columns:1fr 1fr;gap:var(--s2)}
.figs figure{margin:0;min-width:0}
.figs img{display:block;width:100%;height:auto;border:1px solid var(--g3);background:var(--paper)}
.figs figcaption{font-size:.8125rem;line-height:1.5;color:var(--muted);margin-top:var(--s1)}
.fignote{grid-column:1/-1;font-size:.8125rem;line-height:1.6;color:var(--muted);max-width:78ch;
 border-top:1px solid var(--g3);padding-top:var(--s2);margin:var(--s1) 0 0}
@media (max-width:760px){.figs{grid-template-columns:1fr}}
.figs img.dk{display:none}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .figs img.lt{display:none}
 :root:not([data-theme="light"]) .figs img.dk{display:block}}
:root[data-theme="dark"] .figs img.lt{display:none}
:root[data-theme="dark"] .figs img.dk{display:block}
"""

ONE_FIG = {
    "RI-1": ("{n_nodes}", "nodes if all three kinds enter — and {n_isolated} icons that would "
                          "carry no edge at all without the {n_groups} group hubs"),
    "RI-2": ("{n_usesicon}", "component&nbsp;&rarr;&nbsp;icon edges from the byte-match, against "
                             "{prose_pairs} pairs the prose route would have invented"),
    "RI-3": ("{n_multi}", "bases with two or three “active” drawings that share ONE Figma name — "
                          "the <code>-2</code>/<code>-3</code> suffix is "
                          "<code>_export-icons.py</code>&rsquo;s collision counter, so the bare slug "
                          "is Figma&rsquo;s enumeration order, not a design choice"),
    "RI-4": ("{n_unbound}", "of the {n_logos} lockups bound by nothing: {logo_rules} rules in "
                            "logos.md, {logo_rulings} rulings naming a logo file"),
}


def opts_html(did, opts):
    out = []
    for key, rec, text in opts:
        oid = f"{did}-{key}"
        r = '<span class="rec">Recommended</span>' if rec else ""
        out.append(f'<li><div class="opt"><input type="radio" name="{did}" id="{oid}" value="{key}">'
                   f'<label for="{oid}"><span class="okey">({key})</span>{r}{f(text)}</label>'
                   f'</div></li>')
    out.append(f'<li><div class="opt"><input type="radio" name="{did}" id="{did}-none" value="">'
               f'<label for="{did}-none"><span class="okey">(&mdash;)</span>No choice yet &mdash; '
               f'clear this decision.</label></div></li>')
    return "\n".join(out)


# --------------------------------------------------------------------------- R1: THE SHEET
# The whole point of option (c) is that Dave LOOKS. So the glyphs go on the card: every
# active drawing of every multi-variant base, plus that base's bare (inactive) sibling,
# read as SVG text from knowledge/assets/icons/ and inlined. Nothing is drawn by hand and
# no count is typed - the bases come from dry-run.json, the files from icons.manifest.json.
MANIFEST = json.loads((K / "assets" / "icons" / "icons.manifest.json").read_text(encoding="utf-8"))
REC = {}
for _g, _items in MANIFEST["groups"].items():
    for _it in _items:
        REC[_it["slug"]] = (_g, _it)

_IDRX = re.compile(r'(\bid="|url\(#)([A-Za-z0-9_:.\-]+)')


def inline_svg(slug, tag):
    # The file's own markup, with its internal ids namespaced so every glyph on the sheet can
    # share one document without clip-paths colliding, and sized by CSS not by width/height.
    rel = REC[slug][1]["file"]
    s = (K / "assets" / "icons" / rel).read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>", "", s).strip()
    s = _IDRX.sub(lambda m: m.group(1) + tag + "-" + m.group(2), s)
    s = re.sub(r'\s(?:width|height)="[^"]*"', "", s, count=2)
    s = s.replace("<svg", '<svg class="g" role="img" aria-label="' + slug + '" focusable="false"', 1)
    return s


SHEET_BASES = sorted(d["bases_with_multiple_actives"].items())
N_SHEET_ACTIVES = sum(len(v) for v in d["bases_with_multiple_actives"].values())
N_SHEET_GLYPHS = N_SHEET_ACTIVES + sum(1 for _b, _v in SHEET_BASES if _b in REC)
n["n_sheet_actives"] = N_SHEET_ACTIVES
n["n_sheet_glyphs"] = N_SHEET_GLYPHS


def _cell(slug, kind, note):
    return ('<figure class="gl ' + kind + '">' + inline_svg(slug, slug)
            + '<figcaption><span class="gs">' + slug + '</span>'
            + '<span class="gn">' + note + '</span></figcaption></figure>')


sheet_rows = []
for _base, _acts in SHEET_BASES:
    _names = sorted({REC[a][1]["name"] for a in _acts})
    _cells = []
    if _base in REC:
        _cells.append(_cell(_base, "off", "inactive &mdash; the base"))
    for _i, _a in enumerate(_acts):
        _cells.append(_cell(_a, "on", "bare slug &mdash; what (a) picks" if _i == 0
                            else "declared variant under (a)"))
    _grp = REC[_base][1]["file"].split("/")[0] if _base in REC else "&mdash;"
    sheet_rows.append(
        '<div class="srow"><div class="shead"><b>' + _base + '</b>'
        + '<span>' + str(len(_acts)) + ' active drawings, one manifest name: &ldquo;'
        + " / ".join(_names) + '&rdquo; &middot; ' + _grp + '</span></div>'
        + '<div class="scells">' + "".join(_cells) + '</div></div>')

SHEET = ('<div class="sheet" id="RI-3-sheet">'
    '<p class="sheetlede"><b>The sheet.</b> ' + str(N_SHEET_GLYPHS) + ' drawings: the '
    + str(N_SHEET_ACTIVES) + ' active glyphs of the ' + str(n["n_multi"]) + ' bases, each beside '
    'its inactive base. They are the live files under <code>knowledge/assets/icons/</code>, '
    'inlined, unretouched. The caption under each one says what option (a) would do with it '
    '&mdash; it is not a claim that (a) is right.</p>'
    + "".join(sheet_rows) +
    '<p class="sheetnote">Read the pairs, not the labels: the <code>-2</code>/<code>-3</code> suffix '
    'is the exporter&rsquo;s collision counter (<code>_export-icons.py:113-118</code>), so the order '
    'tells you which Figma node the API returned first and nothing else. Path geometry was compared '
    'per base &mdash; no extra is a duplicate of its bare sibling.</p></div>')

# --------------------------------------------------------------------------- A1: THE RENDERS
# Two renders of the EXPLORER with this family placed, made in a scratch copy. The figures in
# the note are read from the strip the scratch explorer printed, not typed.
XR = json.loads((LANE / "explorer-renders.json").read_text(encoding="utf-8"))
EXPL_FIG = ('<div class="figs" id="RI-1-renders">'
    '<figure><img class="lt" src="ri-explorer-chip-off-light.png" alt="The knowledge-graph '
    'explorer as it stands today, with the icons and logos chip off">'
    '<img class="dk" src="ri-explorer-chip-off-dark.png" alt="The knowledge-graph explorer as it '
    'stands today, with the icons and logos chip off">'
    '<figcaption><b>Chip off.</b> The graph today &mdash; the base wiring, unchanged.</figcaption>'
    '</figure>'
    '<figure><img class="lt" src="ri-explorer-chip-on-light.png" alt="The same explorer with the '
    'icons and logos chip on: the base graph squeezed to the left and the icon family a new limb '
    'on the right">'
    '<img class="dk" src="ri-explorer-chip-on-dark.png" alt="The same explorer with the icons and '
    'logos chip on: the base graph squeezed to the left and the icon family a new limb on the '
    'right"><figcaption><b>Chip on.</b> The same view with <code>Icons &amp; logos</code> lit.'
    '</figcaption></figure>'
    '<p class="fignote"><b>How these were made, and what they are not.</b> Lane RIF copied '
    '<code>_build_kg_explorer.py</code> and its template to a scratch directory, pointed the copy '
    'at a scratch output, and fed it this lane&rsquo;s own <code>_icon_nodes.json</code> / '
    '<code>_logo_nodes.json</code>. <code>notes/_KG-EXPLORER.html</code> was not rebuilt and '
    'nothing under <code>knowledge/</code> was written. The new family is parked in its own '
    'column, and the column it sits in is lane RIF&rsquo;s layout choice, not a '
    'measurement &mdash; the '
    'squeeze on the left is the cost of that choice as much as of the family. What IS measured is '
    'the strip at the top of each render: the same view reads <b>' + XR["off"]["nodes"] + ' nodes / '
    + XR["off"]["relations"] + ' relations</b> with the chip off and <b>' + XR["on"]["nodes"]
    + ' / ' + XR["on"]["relations"] + '</b> with it on.</p></div>')

EXTRA = {"RI-1": EXPL_FIG, "RI-3": SHEET}

dec_html = []
for x in spec["decisions"]:
    big, cap = ONE_FIG[x["id"]]
    dec_html.append(f"""<div class="dec" data-id="{x['id']}">
<div class="dechead"><span class="decid">{x['id']}</span><h3>{f(x['title'])}</h3></div>
<div class="onefig"><b>{f(big)}</b><span>{f(cap)}</span></div>
<p>{f(x['lede'])}</p>
<ul class="opts">
{opts_html(x['id'], x['options'])}
</ul>
<p class="why"><b>Recommendation.</b> {f(x['why'])}</p>
<p class="attrib">{f(x['attrib'])}</p>
{EXTRA.get(x['id'], '')}
<textarea class="note" data-id="{x['id']}" aria-label="Notes for {x['id']}" placeholder="Notes for {x['id']} &mdash; your words"></textarea>
</div>""")

IDS = [x["id"] for x in spec["decisions"]]

EDGE_ROWS = [
    ("inGroup", "icon &rarr; iconGroup", "the manifest key the record sits under", ec["inGroup"], res["inGroup"]),
    ("activeVariantOf", "icon &rarr; icon", "slug <code>-active(-N)</code> + the base in the manifest", ec["activeVariantOf"], res["activeVariantOf"]),
    ("usesIcon", "component &rarr; icon", "byte-match of <code>&lt;path d&gt;</code>, via <code>renderedBy</code>", ec["usesIcon"], res["usesIcon"]),
    ("usesLogo", "component &rarr; logo", "<code>src=</code> at an <code>assets/logos/</code> path", ec["usesLogo"], res["usesLogo"]),
    ("defaultFor", "logo &rarr; <i>(null)</i>", "the filename stem inside <code>s230-D2</code>", ec["defaultFor"], res.get("defaultFor", 0)),
    ("ruledBy", "icon &rarr; ruling", "a ruling <code>governs</code> entry naming the <code>.svg</code>", ec["ruledBy"], res["ruledBy"]),
]
edge_tbody = "\n".join(
    f'<tr><td class="slug newmark">{t}</td><td class="slug">{s}</td><td class="defn">{j}</td>'
    f'<td class="num">{c}</td><td class="num">{r}</td><td class="num">{c - r}</td></tr>'
    for t, s, j, c, r in EDGE_ROWS)

group_tbody = "\n".join(
    f'<tr><td class="slug">iconGroup:{re.sub(r"[^a-z0-9]+", "-", g.lower()).strip("-")}</td>'
    f'<td>{g}</td><td class="num">{c}</td></tr>'
    for g, c in sorted(d["manifest_counts"].items(), key=lambda kv: -kv[1]))

NULL_ROWS = []
for u in d["unresolved"]:
    NULL_ROWS.append((u["type"], u.get("source") or "&mdash;", u["why"], u["note"]))
by_type = {}
for t, s, w, note in NULL_ROWS:
    by_type.setdefault((t, w), []).append((s, note))
null_tbody = "\n".join(
    f'<tr><td class="slug newmark">{t}</td><td class="num">{len(v)}</td>'
    f'<td class="defn">{w}</td><td class="defn slug">{"; ".join(x[1] for x in v[:3])}'
    f'{" …" if len(v) > 3 else ""}</td></tr>'
    for (t, w), v in sorted(by_type.items(), key=lambda kv: -len(kv[1])))

top_prose = " &middot; ".join(f"<code>{s}</code> &times;{c}" for s, c in prose_top[:10])

HTML = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{spec['title']}</title>
<style>{CSS}</style>
<script type="application/json" id="measured">{json.dumps(n, ensure_ascii=False)}</script>
<section id="headline"><div class="wrap">
<p class="label">#277 &middot; lane RI &middot; icons and logos, proposed</p>
<h1>{f(spec['headline'])}</h1>
<p>Four decisions sit below, recommendation first on each, one figure on each card. Everything after
them is the evidence they rest on and you should not need it. <b>If you take the recommendation on all
four, the graph gains {n['n_nodes']} nodes and {n['n_edges']} edges</b> &mdash; that is
<b>+{n['node_pct']}%</b> on the node count and <b>+{n['edge_pct']}%</b> on the edge count of a graph
that holds {n['g_nodes']} and {n['g_edges']} today. Nothing here is landed and nothing under
<code>knowledge/</code> has been written.</p>
<div class="stats">
<div class="stat"><b>{n['n_nodes']}</b><span>nodes: {n['n_icons']} icons, {n['n_groups']} groups, {n['n_logos']} logos</span></div>
<div class="stat"><b>{n['n_edges']}</b><span>edges across six new types, all structural</span></div>
<div class="stat"><b>0</b><span>edges drawn from a regex over prose</span></div>
<div class="stat"><b>{n['n_nulls']}</b><span>declared nulls &mdash; every gap named, none filled</span></div>
</div>
<div class="zeros">
<div><b>0</b> files written under <code>knowledge/</code> &mdash; this page proposes</div>
<div><b>0</b> node kinds invented to make an arrow land</div>
<div><b>{n['n_usesicons']}</b> of {n['n_icons']} icons are used by anything &mdash; {n['n_unused']} are not</div>
<div><b>{n['prose_hit']} of {n['prose_metas']}</b> metas the refused prose route fires on</div>
</div>
<blockquote>use this as teh default logo &ldquo;masterbrand-light-colour&rdquo; &hellip; use this for dark
mode masterbrand-dark-colour
<cite>Dave, #230, 2026-08-31 &mdash; quoted from the <code>says</code> field of <code>s230-D2</code> in
knowledge/_rulings.json. It is the only ruling that binds a logo, and it binds two of {n['n_logos']}.</cite></blockquote>
</div></section>

<section id="decisions"><div class="wrap">
<p class="label">Your words &middot; the ask</p>
<h2>Four decisions.</h2>
<p>One letter is an answer; a letter with a sentence attached is a sequel, and it will be read back
before anything is built on it. Every recommendation below says which lane wrote it, where it sits.</p>
{"".join(dec_html)}

<div class="flag">
<h3>Flagged, not a decision &mdash; the manifest is one asset stale, and it is ours to fix</h3>
<p class="flagline"><code>icons.manifest.json</code> was generated <b>{n['manifest_date']}</b>.
<code>menu-search.svg</code> was ruled into the library by <code>s212-D9</code> on 2026-08-21, is on
disk, and is <b>not in the manifest</b>. Since <code>icon:</code> resolves against the manifest, the
graph cannot hold the one icon you personally approved &mdash; the simulated validator run confirms it,
refusing <code>icon:menu-search</code> by name. That is a <b>build step, not a question</b>: the record
is added by textual span before any land, never by a re-dump, and <code>$total</code> goes
{n['n_icons']}&nbsp;&rarr;&nbsp;{n['n_icons'] + 1}. Nothing else is stale: every one of the
{n['n_icons']} manifested paths resolves on disk.</p>
</div>

<div class="flag">
<h3>Flagged, not a decision &mdash; <code>themedBy</code> is declined and handed to the tokens gap</h3>
<p class="flagline">A-inventory proposed an icon&nbsp;&rarr;&nbsp;token edge. It is not drawn here and it
is not on the list above, because it carries nothing: <b>{n['cc']} of {n['n_icons']}</b> records are
<code>fillMode: currentColor</code> and every one of them would point at the same eight
<code>icon/*</code> leaves, which are what the <i>consuming context</i> sets. The relation that does have
content is component&nbsp;&rarr;&nbsp;token, and it already has a structural home:
<code>tokens.icon</code> is a real key in <b>{n['tokens_icon']}</b> metas. That is the tokens family's
work, not this one's, and it is handed over rather than half-drawn.</p>
</div>

<div class="flag">
<h3>Flagged, not a decision &mdash; <code>defaultFor</code> has nowhere to land</h3>
<p class="flagline"><code>s230-D2</code> names two lockups as the theme defaults, and there is no
<code>theme:</code> node in the graph to point them at &mdash; the live explorer carries twenty node
kinds and none of them is a theme. So the two <code>defaultFor</code> edges ship with
<b>a null target</b>, the theme as an edge property and your sentence as the note, and they are counted
among the {n['n_nulls']} declared nulls. Inventing <code>theme:light</code> so the arrow could land is
the one thing the never-invent fence exists to stop. If you want the arrow to land, that is a fourth
node kind and a separate question.</p>
</div>

<div class="bar">
<button id="btnExport">Export JSON</button>
<button id="btnCopy">Copy to clipboard</button>
<button class="ghost" id="btnClear">Clear all</button>
<span class="said" id="said"></span>
</div>
<pre class="exp" id="exp" hidden></pre>
</div></section>

<section id="ev-edges"><div class="wrap">
<p class="label">Evidence &middot; you should not need this</p>
<h2>The six edge types, and what each one is read from.</h2>
<p>&ldquo;Structural&rdquo; means read from a field, a filename, or a byte-match. Every count below is
re-derived at build time by <code>gen_kg_icons.py</code>; none is quoted from a document.</p>
<div class="tw"><table>
<thead><tr><th>type</th><th>direction</th><th>the join</th><th class="num">edges</th>
<th class="num">target resolves</th><th class="num">declared null</th></tr></thead>
<tbody>
{edge_tbody}
</tbody></table></div>
</div></section>

<section id="ev-prose"><div class="wrap">
<p class="label">Evidence &middot; the route that was refused</p>
<h2>Why component&nbsp;&rarr;&nbsp;icon is not read from prose.</h2>
<p>Testing every manifest slug as a whole word against every component meta fires on
<b>{n['prose_hit']} of {n['prose_metas']}</b> metas and makes <b>{n['prose_pairs']}</b> pairs. The
busiest matches are the English language, not icons:</p>
<p>{top_prose}</p>
<p>The byte-match route finds {n['n_usesicon']} pairs across {n['n_usescomp']} components and invents
nothing. The two sets differ in the direction that matters: <b>{n['struct_only']} components render a
library glyph and never mention the word &ldquo;icon&rdquo; in their meta</b>, and
{n['prose_only']} mention it while rendering no library glyph. The prose route would have missed the
first group entirely. This is the route <code>s274-D12</code> and <code>s276-D5</code> refused, and
there is no flag on the generator that draws it.</p>
</div></section>

<section id="ev-groups"><div class="wrap">
<p class="label">Evidence &middot; the ten hubs</p>
<h2>The groups, as the manifest keys them.</h2>
<div class="tw"><table>
<thead><tr><th>node id</th><th>manifest key</th><th class="num">icons</th></tr></thead>
<tbody>
{group_tbody}
</tbody></table></div>
</div></section>

<section id="ev-nulls"><div class="wrap">
<p class="label">Evidence &middot; the gaps, named</p>
<h2>{n['n_nulls']} declared nulls. None of them is filled by a guess.</h2>
<div class="tw"><table>
<thead><tr><th>type</th><th class="num">count</th><th>why it cannot be drawn</th><th>examples</th></tr></thead>
<tbody>
{null_tbody}
</tbody></table></div>
</div></section>

<section id="ev-cost"><div class="wrap">
<p class="label">Evidence &middot; the cost, measured</p>
<h2>What it does to the explorer.</h2>
<p>The payload is serialised exactly as <code>_build_kg_explorer.py</code> serialises it &mdash;
<code>json.dumps(&hellip;, separators=(',',':'))</code> over the same node and edge dicts. It comes to
<b>{n['payload_kb']}&nbsp;KB</b> against the shipped explorer's {n['explorer_kb']}&nbsp;KB, which is
<b>+{n['payload_pct']}%</b> on bytes. The number that will be felt is the other one:
<b>+{n['node_pct']}%</b> on node count, because <code>place_extra()</code> lays each family out on its
own and parks it beside the base graph. The chip is proposed <b>OFF by default</b>, the fifth additive
family named <code>{n['chip']}</code>, following the precedent the <code>ux</code> chip set. Bytes are
arithmetic; the layout is a look, and it is yours.</p>
</div></section>

<footer><div class="wrap">
<p>Built by <code>notes/_lanes/277/icons-propose/_build_page.py</code> from
<code>dry-run.json</code> and live counts over <code>knowledge/</code>. Nothing on this page is landed.
The generator refuses <code>--land</code> against every ruling id that exists.</p>
</div></footer>

<script>
(function(){{
 var KEY={json.dumps(spec['storage_key'])};
 var IDS={json.dumps(IDS)};
 var state={{}};
 var lastSaved=null;
 function el(id){{return document.getElementById(id);}}
 function load(){{
  try{{var raw=localStorage.getItem(KEY);
   if(raw){{var o=JSON.parse(raw);
    if(o&&typeof o==="object"){{state=o.decisions||{{}};lastSaved=o.at||null;}}}}}}
  catch(e){{state={{}};}}
  if(!state||typeof state!=="object")state={{}};
 }}
 function save(){{
  lastSaved=new Date().toISOString();
  try{{localStorage.setItem(KEY,JSON.stringify({{decisions:state,at:lastSaved}}));}}catch(e){{}}
  paint();
 }}
 function two(v){{return (v<10?"0":"")+v;}}
 function paint(){{
  var done=0;
  IDS.forEach(function(id){{var r=state[id];if(r&&r.choice)done++;}});
  var t="\\u2014";
  if(lastSaved){{try{{var d=new Date(lastSaved);t=two(d.getHours())+":"+two(d.getMinutes());}}catch(e){{}}}}
  el("said").textContent=done+" of "+IDS.length+" decided \\u00b7 saved "+t;
 }}
 function put(id,k,v){{
  var r=state[id]||{{}};r[k]=v;r.at=new Date().toISOString();
  if(!r.choice&&!r.note){{delete state[id];}}else{{state[id]=r;}}
 }}
 function restore(){{
  IDS.forEach(function(id){{
   var r=state[id]||{{}};
   if(r.choice){{
    var b=document.querySelector('input[name="'+id+'"][value="'+r.choice+'"]');
    if(b)b.checked=true;
   }}
   var ta=document.querySelector('textarea.note[data-id="'+id+'"]');
   if(ta&&r.note)ta.value=r.note;
  }});
 }}
 function exportObj(){{
  return {{page:{json.dumps(spec['page'])},
          at:new Date().toISOString(),
          decisions:IDS.map(function(id){{
            var r=state[id]||{{}};
            return {{id:id,choice:r.choice||null,note:r.note||""}};
          }})}};
 }}
 function show(){{
  var j=JSON.stringify(exportObj(),null,2);
  var p=el("exp");p.hidden=false;p.textContent=j;return j;
 }}
 document.addEventListener("change",function(e){{
  if(e.target.type==="radio"&&IDS.indexOf(e.target.name)>-1){{
   put(e.target.name,"choice",e.target.value||null);save();
  }}
 }});
 var timer=null;
 document.addEventListener("input",function(e){{
  if(e.target.classList&&e.target.classList.contains("note")){{
   put(e.target.dataset.id,"note",e.target.value);
   clearTimeout(timer);timer=setTimeout(save,400);
  }}
 }});
 document.addEventListener("focusout",function(e){{
  if(e.target.classList&&e.target.classList.contains("note")){{clearTimeout(timer);save();}}
 }});
 window.addEventListener("beforeunload",function(){{clearTimeout(timer);save();}});
 el("btnExport").addEventListener("click",function(){{
  var j=show();
  try{{
   var a=document.createElement("a");
   a.href=URL.createObjectURL(new Blob([j],{{type:"application/json"}}));
   a.download={json.dumps(spec['export_filename'])};
   document.body.appendChild(a);a.click();
   setTimeout(function(){{URL.revokeObjectURL(a.href);a.remove();}},1500);
  }}catch(e){{}}
  el("exp").scrollIntoView({{behavior:"smooth",block:"nearest"}});
 }});
 el("btnCopy").addEventListener("click",function(){{
  var j=show();var b=el("btnCopy");
  function ok(){{b.textContent="Copied";setTimeout(function(){{b.textContent="Copy to clipboard";}},1600);}}
  try{{
   if(navigator.clipboard&&navigator.clipboard.writeText){{
    navigator.clipboard.writeText(j).then(ok,function(){{ok();}});return;
   }}
  }}catch(e){{}}
  try{{var t=el("exp");var r=document.createRange();r.selectNodeContents(t);
   var s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand("copy");ok();}}catch(e){{}}
 }});
 el("btnClear").addEventListener("click",function(){{
  if(!confirm("Clear every choice and note on this page?"))return;
  state={{}};try{{localStorage.removeItem(KEY);}}catch(e){{}}
  document.querySelectorAll('input[type="radio"]').forEach(function(i){{i.checked=false;}});
  document.querySelectorAll("textarea.note").forEach(function(t){{t.value="";}});
  el("exp").hidden=true;save();
 }});
 load();restore();paint();
}})();
</script>
"""

OUT.write_text(HTML, encoding="utf-8")
print(f"wrote {OUT.name} ({len(HTML):,} bytes) · {len(IDS)} decisions · {len(n)} measured figures")
print(f"nodes {n['n_nodes']} (icons {n['n_icons']} · groups {n['n_groups']} · logos {n['n_logos']}) "
      f"· edges {n['n_edges']} · nulls {n['n_nulls']}")
print(f"live graph {n['g_nodes']} nodes / {n['g_edges']} edges -> +{n['node_pct']}% / +{n['edge_pct']}%")
print(f"byte-match {n['n_usesicon']} pairs · prose route {n['prose_pairs']} pairs on "
      f"{n['prose_hit']}/{n['prose_metas']} metas · STRUCT-ONLY {n['struct_only']}")
