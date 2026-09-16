#!/usr/bin/env python3
"""gen_kg_icons.py — the ICON + ICONGROUP + LOGO node/edge generator (#277 lane RI).

Enacts `s269-D1` STEP 4 by PROPOSING, never landing: put the 666 library icons,
their 10 manifest groups and the 12 logo lockups into the knowledge graph as
nodes, with the six edge types that can be read from a FIELD, a FILENAME or a
BYTE-MATCH. The design is lane IX's FINDINGS.md (`notes/_lanes/277/icons/`,
ca294b4) §2 node kinds, §3 ranked edges, §4 blockers, §5 four-decision plan.
Every figure IX measured is RE-DERIVED here from the live tree; nothing is
copied out of that document as a number.

  NODE KINDS  icon:<slug>       666   name, slug, file, group, active, fillMode
                                      (the manifest record's own fields, verbatim,
                                      plus `group` which is the manifest key the
                                      record sits under). `fills` is carried too
                                      but see `themedBy` below: it joins nothing.
              iconGroup:<slug>   10   the ten `groups` keys, slugged; `label` is
                                      the key verbatim, `count` the group length.
              logo:<stem>        12   lockup x theme x colourMode, all three
                                      PARSED FROM THE FILENAME — there is no logo
                                      manifest, the filenames are the manifest.

  EDGE TYPES  inGroup          icon  -> iconGroup   NEW   666   manifest key
              activeVariantOf  icon  -> icon        NEW   232   slug + manifest
              usesIcon         comp  -> icon        NEW   371   BYTE-MATCH
              usesLogo         comp  -> logo        NEW    18   src= attribute
              defaultFor       logo  -> (null)      NEW     2   s230-D2 verbatim
              ruledBy          icon  -> ruling      NEW     9   ruling `governs`

⛔ NO PROSE JOIN IS DRAWN, and the number says why. Testing every manifest slug
as a whole word against every component meta's text fires on 138 of 138 metas
and yields 1,736 (meta, slug) pairs, because `accessibility`, `no`, `time`,
`user`, `link`, `card` and `block` are all icon slugs. That is the exact route
`s274-D12` and `s276-D5` refused. `--prose-count` MEASURES it and prints it; no
flag draws it, and none can — there is no code path in this file that emits an
edge from a regex over a sentence.

⛔ `themedBy` (icon -> token) IS DECLINED, not forgotten. 613 of 666 records are
`fillMode: currentColor` with a single-element `fills` array, and the 8 `icon/*`
leaves in semantic-colour.json are what the CONSUMING CONTEXT sets. The relation
is identical for all 613, so the edge carries no information at the icon level.
IX §1c measured it; this file reports the split and draws nothing. The real
relation is component -> token via `tokens.icon` (a real key in 28 of 138 metas,
counted here) and it belongs to the tokens gap, not to this family.

DECLARED LIMITS OF `usesIcon` (IX §3 rank 4, carried here because the edge is
only honest with them attached):
  1. It measures the REFERENCE SNIPPET, not the component's contract. Named
     `usesIcon` (observed in the reference render), never `requiresIcon`.
  2. 81 of 666 icons are used. The edge illuminates 12% of the family; the
     library is a catalogue and the system consumes a twelfth of it.
  3. Inline paths that byte-match nothing are counted and NO edge is drawn for
     them (`_validate_icons.py` classifies them `bespoke` or UNKNOWN; this file
     does not re-classify).
  4. `<svg>` elements with no `<path>` are sprite `<use href="#...">` refs into a
     `<symbol>` in the same file. The PAIR SET is correct; per-use FREQUENCY is
     not measured, so no weight may be put on the edge.

⛔ A NEW NODE KIND AND A NEW EDGE TYPE ARE CLOSED-VOCABULARY CHANGES (#75). This
script PROPOSED; Dave ratified at #277; the door is now OPEN ON THOSE IDS AND NO
OTHERS. `--dry-run` is still the DEFAULT and writes three JSON files into THIS
LANE FOLDER and nothing else. `--land` REFUSES unless `--ratified sNNN-DN` names
an id that is BOTH recorded in knowledge/_rulings.json AND listed in RATIFIES
below. **RATIFIES IS `("s277-D4", "s277-D5", "s277-D6", "s277-D7")`** — the four
rulings of 2026-09-16 that ratify exactly this proposal. Every other id there is,
live or invented, is still refused, and bite 12 proves each refusal for its own
reason with the allowlist open.

WHERE IT LANDS. `--land` writes TWO files, knowledge/_icon_nodes.json and
knowledge/_logo_nodes.json, in the shape of knowledge/_rule_nodes.json and
knowledge/_ux_principle_nodes.json (the s274-D11 / s275-D4 precedent: an authored
node/edge file the explorer reads behind its own chip). Landed at #279 lane IL by
`--land --ratified s277-D4`.

NEVER INVENTED (fence 3, #261): a target that does not resolve to a measured node
becomes `{"t": null, "$note": "<the evidence>"}` and is counted in `unresolved`.
Five declared nulls are structural and permanent until someone rules:
  B1  `menu-search.svg` is on disk, was ruled in by `s212-D9` (2026-08-21) and is
      NOT in the manifest (`$generated` 2026-06-17). It gets NO icon: node and its
      `ruledBy` edge is declared, never invented.
  --  the 2 orphan actives whose base slug is absent from the manifest.
  B4  the 15 bases carrying `-active-2`/`-active-3`. `activeVariantOf` draws all
      232 regardless; `defaultActive` is NOT drawn and is Dave's (decision RI-3).
  B3  the 10 logos bound by no rule: `_rules-index.json` has 0 rules whose `file`
      is `logos.md`, and 0 rulings name a logo `.svg` in `governs`.
  --  `app-shell-nav-rail`, which `s230-D2` records as deliberately NOT rebound.
      It is a gap with a ruling behind it and it enters as a declared null. The
      name is taken from `s230-D2`'s OWN CLAUSE — the `says` field literally reads
      "App-shell-nav-rail deliberately NOT rebound" and `RESIDUE_RX` reads that
      clause and nothing else (#279 lane IL, RIV A3). Every component slug is NO
      LONGER tested as a substring of the ruling's English: `app-shell-top-nav`
      and `navigations` are substrings of the same sentence and must not, and now
      cannot, inherit the rail's reason. Bite 18 proves the second one stays out.

`defaultFor` is drawn with `t: null` ON PURPOSE. `s230-D2` names two of the twelve
as the theme defaults, but `theme:` is NOT a node kind in the live graph (measured
against notes/_KG-EXPLORER.html: 20 kinds, no theme) and this lane proposes THREE
kinds, not four. So the two edges carry the theme as an edge property and Dave's
verbatim line as the note, and are counted as unresolved. Inventing `theme:light`
to make an arrow land would be the thing fence 3 exists to stop.

Usage:
  python3 notes/_lanes/277/icons-propose/gen_kg_icons.py            # dry run (default)
  python3 .../gen_kg_icons.py --dry-run <dir>                       # dry run, named dir
  python3 .../gen_kg_icons.py --icons-only                          # RI-1 option (b): no iconGroup
  python3 .../gen_kg_icons.py --no-logos                            # RI-4 option (c): logos wait
  python3 .../gen_kg_icons.py --no-usesicon                         # RI-2 option (b): hold the byte-match
  python3 .../gen_kg_icons.py --prose-count                         # MEASURE the refused route
  python3 .../gen_kg_icons.py --land --ratified s277-D4                # THE LAND (#279 lane IL)
  python3 .../gen_kg_icons.py --selftest
  python3 .../gen_kg_icons.py --corpus <dir>                        # a scratch knowledge/ dir

DO-NOT-RULE: this script never edits icons.manifest.json, any .svg, any meta,
meta.schema.json, _rulings.json, _validate_kg.py, _validate_icons.py,
_build_kg_explorer.py, _rules-index.json, and never adds an icon or a logo. It
reads and proposes.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
try:
    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
except ImportError:  # a scratch corpus with no _helpgate.py is legal (the mutation harness)
    pass

import glob
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
# The lane dir is the script's home in the proposal wave. REPO is found by walking
# up to the directory that holds knowledge/ — never by counting `.parents[n]`,
# which breaks the moment the harness copies this file somewhere else.
_r = HERE
while _r != _r.parent and not (_r / "knowledge" / "_rulings.json").exists():
    _r = _r.parent
REPO = _r
K = REPO / "knowledge"
LANE = HERE
DEFAULT_OUT = LANE

FAMILY = "assets"
ICON, GROUP, LOGO = "icon:", "iconGroup:", "logo:"
LANDED_ICONS = "_icon_nodes.json"
LANDED_LOGOS = "_logo_nodes.json"

EDGE_TYPES = ("inGroup", "activeVariantOf", "usesIcon", "usesLogo", "defaultFor", "ruledBy")
# MEASURED absent from the live graph (notes/_KG-EXPLORER.html carries 20 kinds and
# none of these six edge types). Asserted by bite 13, never trusted.
EDGE_STATUS = {t: "NEW" for t in EDGE_TYPES}

# The manifest record fields carried verbatim onto the node. `slug` becomes the id.
ICON_FIELDS = ("name", "slug", "file", "active", "fillMode", "fills")
LOGO_FIELDS = ("lockup", "theme", "colourMode")

RULING_ID_RX = re.compile(r"^s\d{2,4}-D\d+$")
# The active suffix, and it is the WHOLE rule: IX measured `active == True` <=> this
# matches, on all 666 records, zero mismatches either way. Bite 2 re-proves it.
ACTIVE_RX = re.compile(r"-active(-\d+)?$")
# The three logo filename fields. No logo manifest exists; the filename IS the manifest.
LOGO_RX = re.compile(r"^(?P<lockup>.+)-(?P<theme>light|dark)-(?P<colourMode>colour|mono)$")
# `_validate_icons.py`'s OWN two rules, re-declared here because they are the join.
# Never a second geometry index: the same regex, the same normalisation, read from
# the gate at run time and asserted identical (bite 4).
DRE = re.compile(r'\bd="([^"]+)"')
SVGRE = re.compile(r'<svg\b[^>]*?>.*?</svg>', re.S)
# The only attribute route to a logo: an explicit src=/href= at an assets/logos path.
LOGO_SRC_RX = re.compile(r'(?:src|href)="[^"]*assets/logos/([^"/]+)\.svg"')
# A ruling `governs` entry that names an icon FILE (not the directory, not the manifest).
GOVERNS_ICON_RX = re.compile(r'(?:^|/)assets/icons/(?:.+/)?([^/]+)\.svg$')
GOVERNS_LOGO_RX = re.compile(r'(?:^|/)assets/logos/(?:.+/)?([^/]+)\.svg$')

# THE DOOR (#75). A ratifying id must be in _rulings.json AND in this tuple. It was
# EMPTY through the proposal wave (#277). Dave ruled on 2026-09-16 and the four ids
# below are the ratification of THIS proposal and of nothing else: s277-D4 the three
# node kinds, s277-D5 the byte-match edges, s277-D6 the 15 bases carrying no
# activeVariantOf, s277-D7 the twelve logos. Bite 12 proves that with the list open
# every other id — none, malformed, unrecorded, and a live ruling about something
# else — is still refused, each for its own reason.
RATIFIES = ("s277-D4", "s277-D5", "s277-D6", "s277-D7")

# s230-D2 is the ONE ruling that names logo defaults. The join is byte-containment of
# a LOGO FILENAME STEM in that ruling's own fields — not a pattern over English. The
# theme comes from the STEM's own parsed field, never from a word in the sentence.
DEFAULT_RULING = "s230-D2"
# THE RESIDUE ANCHOR (#279 lane IL, RIV A3). `s230-D2` records, in its own words, one
# component it deliberately did NOT rebind: "App-shell-nav-rail deliberately NOT
# rebound". This regex reads THAT CLAUSE and takes the name out of it. It is NOT the
# old test, which asked of every component slug "are you a substring of this ruling's
# English?" — three slugs answer yes (`app-shell-nav-rail`, `app-shell-top-nav`,
# `navigations`) and a fourth would have inherited the rail's reason verbatim. The
# clause names one component; only a component the clause NAMES can be a residue.
RESIDUE_RX = re.compile(r"([A-Za-z0-9][A-Za-z0-9._-]*)\s+deliberately NOT rebound", re.I)


def norm(d):
    """`_validate_icons.py`'s normalisation, verbatim. Bite 4 asserts it matches the
    gate's own source, so a drift in the gate turns this file red instead of silently
    producing a different byte-match."""
    return re.sub(r"\s+", " ", d.strip())


# ------------------------------------------------------------------ corpus

def _k(corpus=None):
    return Path(corpus) if corpus else K


def load_manifest(corpus=None):
    p = _k(corpus) / "assets" / "icons" / "icons.manifest.json"
    return json.loads(p.read_text(encoding="utf-8"))


def icon_records(man):
    """[(group_key, record)] in manifest order. The group key is a FIELD position,
    not a value inside the record — the record itself never names its group."""
    return [(g, r) for g, lst in man.get("groups", {}).items() for r in lst]


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def icons_on_disk(corpus=None):
    d = _k(corpus) / "assets" / "icons"
    return {Path(p).stem: str(Path(p).relative_to(d)) for p in
            glob.glob(str(d / "**" / "*.svg"), recursive=True)}


def logo_stems(corpus=None):
    return sorted(Path(p).stem for p in glob.glob(str(_k(corpus) / "assets" / "logos" / "*.svg")))


def rulings(corpus=None):
    p = _k(corpus) / "_rulings.json"
    if not p.exists():
        return []
    return [r for r in json.loads(p.read_text(encoding="utf-8")).get("rulings", [])
            if isinstance(r, dict) and r.get("id")]


def component_metas(corpus=None):
    """{slug: meta}. EXAMPLE- is skipped exactly as _build_kg_explorer.py skips it."""
    out = {}
    for f in sorted(glob.glob(str(_k(corpus) / "components" / "*.meta.json"))):
        slug = Path(f).name[:-len(".meta.json")]
        if slug.startswith("EXAMPLE-"):
            continue
        try:
            out[slug] = json.loads(Path(f).read_text(encoding="utf-8"))
        except Exception:
            continue
    return out


def snippet_to_component(metas):
    """The graph's OWN snippet -> component mapping, read from the metas' `edges`
    (137 `renderedBy` refs today). NO new inference: this is the same field
    _build_kg_explorer.extract() turns into component -> snippet base edges."""
    out = {}
    for slug, m in metas.items():
        for lst in (m.get("edges") or {}).values():
            if not isinstance(lst, list):
                continue
            for e in lst:
                ref = e.get("ref") if isinstance(e, dict) else e
                if isinstance(ref, str) and ref.startswith("snippet:"):
                    out.setdefault(ref[len("snippet:"):], slug)
    return out


def gate_norm_matches(corpus=None):
    """Is our `norm()` still the gate's `norm()`? Read _validate_icons.py and compare
    the two source lines that ARE the join. A gate that drifts must turn us red."""
    p = _k(corpus) / "_validate_icons.py"
    if not p.exists():
        return None
    src = p.read_text(encoding="utf-8")
    return ('re.sub(r"\\s+", " ", d.strip())' in src
            and 'DRE = re.compile(r\'\\bd="([^"]+)"\')' in src)


def build_library(corpus=None):
    """normalised `d=` -> icon slug, over every library SVG. `setdefault` keeps the
    FIRST file that owns a geometry, which is `_validate_icons.py`'s own rule."""
    d = _k(corpus) / "assets" / "icons"
    lib = {}
    for f in sorted(glob.glob(str(d / "**" / "*.svg"), recursive=True)):
        try:
            s = Path(f).read_text(encoding="utf-8")
        except Exception:
            continue
        for path_d in DRE.findall(s):
            lib.setdefault(norm(path_d), Path(f).stem)
    return lib


def scan_snippets(corpus=None):
    """(pairs, stats) — (snippet filename, icon slug) byte-match pairs over the
    *.reference.html files, which are exactly the 137 the graph holds as snippet
    nodes. Review scratch files (_REVIEW-*.html) are not reference snippets and are
    not scanned."""
    lib = build_library(corpus)
    files = sorted(glob.glob(str(_k(corpus) / "snippets" / "*.reference.html")))
    pairs, occ, unmatched, nopath = set(), 0, 0, 0
    for f in files:
        name = Path(f).name
        try:
            html = Path(f).read_text(encoding="utf-8")
        except Exception:
            continue
        for blk in SVGRE.findall(html):
            ds = DRE.findall(blk)
            if not ds:
                nopath += 1
                continue
            occ += len(ds)
            for path_d in ds:
                hit = lib.get(norm(path_d))
                if hit:
                    pairs.add((name, hit))
                else:
                    unmatched += 1
    return pairs, {"library_keys": len(lib), "snippet_files": len(files),
                   "inline_path_occurrences": occ, "unmatched_paths": unmatched,
                   "svg_without_path": nopath}


def scan_logo_refs(corpus=None):
    out = set()
    for f in sorted(glob.glob(str(_k(corpus) / "snippets" / "*.reference.html"))):
        try:
            html = Path(f).read_text(encoding="utf-8")
        except Exception:
            continue
        for stem in LOGO_SRC_RX.findall(html):
            out.add((Path(f).name, stem))
    return out


def prose_pair_count(corpus=None, slugs=()):
    """MEASURE the refused route so the refusal carries a number. Returns
    (metas_hit, pairs, top). Emits NOTHING — there is no caller that turns this
    into an edge, by construction."""
    metas = component_metas(corpus)
    rx = {s: re.compile(r"(?<![A-Za-z0-9])" + re.escape(s) + r"(?![A-Za-z0-9])", re.I)
          for s in slugs}
    pairs, hit, per = 0, 0, {}
    for slug, m in metas.items():
        text = json.dumps(m, ensure_ascii=False)
        found = [s for s, r in rx.items() if r.search(text)]
        if found:
            hit += 1
        pairs += len(found)
        for s in found:
            per[s] = per.get(s, 0) + 1
    top = sorted(per.items(), key=lambda kv: (-kv[1], kv[0]))[:12]
    return hit, len(metas), pairs, top


def tokens_icon_metas(corpus=None):
    """The observation this lane HANDS OVER rather than draws: `tokens.icon` is a real
    key in N of the metas, and that is a component -> token edge for the tokens gap."""
    n = 0
    for m in component_metas(corpus).values():
        t = m.get("tokens")
        if isinstance(t, dict) and t.get("icon"):
            n += 1
    return n


# ------------------------------------------------------------------ build

def build(corpus=None, icons_only=False, no_logos=False, no_usesicon=False):
    """Returns (icon_payload, logo_payload, report). Reads only; writes nothing."""
    man = load_manifest(corpus)
    recs = icon_records(man)
    slugs = {r["slug"] for _g, r in recs}
    disk = icons_on_disk(corpus)
    metas = component_metas(corpus)
    s2c = snippet_to_component(metas)
    R = rulings(corpus)
    rids = {r["id"] for r in R}

    nodes, edges, unresolved = {}, [], []

    def add(nid, label, **kw):
        n = nodes.setdefault(nid, {"id": nid, "type": nid.split(":")[0],
                                   "label": label, "fam": FAMILY})
        n.update({k: v for k, v in kw.items() if v not in (None, "", [], {})})
        return nid

    def link(s, t, ty, **kw):
        e = {"s": s, "t": t, "type": ty, "fam": FAMILY}
        e.update({k: v for k, v in kw.items() if v not in (None, "", [], {})})
        edges.append(e)
        return e

    def declare(s, ty, why, note=""):
        """A target (or a source) we cannot resolve: t:null + the evidence, counted.
        NEVER a guess and NEVER a silent drop."""
        if s is not None:
            edges.append({"s": s, "t": None, "type": ty, "fam": FAMILY, "$note": note or why})
        unresolved.append({"source": s, "type": ty, "why": why, "note": note or why})

    # ---- iconGroup: nodes ------------------------------------------------
    group_id = {}
    if not icons_only:
        for g, lst in man.get("groups", {}).items():
            gid = add(GROUP + slugify(g), g, groupKey=g, count=len(lst))
            group_id[g] = gid
    else:
        group_id = {g: None for g in man.get("groups", {})}

    # ---- icon: nodes + inGroup ------------------------------------------
    for g, r in recs:
        attrs = {f: r.get(f) for f in ICON_FIELDS}
        attrs["group"] = g
        if "$derived" in r:                      # the #264 repair's own sentence, carried
            attrs["$derived"] = r["$derived"]
        add(ICON + r["slug"], r["slug"], **attrs)
        if not icons_only:
            link(ICON + r["slug"], group_id[g], "inGroup")

    # ---- B1: on disk, ruled in, NOT in the manifest -----------------------
    stale = sorted(set(disk) - slugs)
    for s in stale:
        why = ("the .svg is on disk but NOT in icons.manifest.json ($generated "
               f"{man.get('$generated')}), so the manifest cannot resolve icon:{s} — "
               "blocker B1, a build step, not a decision")
        gov = sorted({r["id"] for r in R for e in (r.get("governs") or [])
                      for m in [GOVERNS_ICON_RX.search(str(e).strip())] if m and m.group(1) == s})
        unresolved.append({"source": None, "type": "icon:", "why": why,
                           "note": f"{s}.svg ({disk[s]})" +
                                   (f" — ruled in by {', '.join(gov)}" if gov else "")})

    # ---- activeVariantOf --------------------------------------------------
    by_base = {}
    mismatch = 0
    for _g, r in recs:
        if bool(r.get("active")) != bool(ACTIVE_RX.search(r["slug"])):
            mismatch += 1
    for _g, r in recs:
        if not r.get("active"):
            continue
        base = ACTIVE_RX.sub("", r["slug"])
        if base in slugs:
            link(ICON + r["slug"], ICON + base, "activeVariantOf")
            by_base.setdefault(base, []).append(r["slug"])
        else:
            declare(ICON + r["slug"], "activeVariantOf",
                    "the base slug the -active suffix implies is not in the manifest — "
                    "an ORPHAN ACTIVE, declared, never dropped and never invented",
                    note=f"{r['slug']} -> {base} (absent)")
    multi = {b: sorted(v) for b, v in by_base.items() if len(v) > 1}
    for b, v in sorted(multi.items()):
        unresolved.append({
            "source": ICON + b, "type": "defaultActive",
            "why": "this base carries two or three -active glyphs and NOTHING in the corpus "
                   "says which is THE active twin. activeVariantOf is drawn for all of them; "
                   "defaultActive is NOT drawn — blocker B4, and it is Dave's (RI-3)",
            "note": f"{b}: " + ", ".join(v)})

    # ---- usesIcon — the BYTE-MATCH ---------------------------------------
    scan_stats, comp_icon = {}, set()
    if not no_usesicon:
        pairs, scan_stats = scan_snippets(corpus)
        for sn, ic in sorted(pairs):
            comp = s2c.get(sn)
            if comp is None:
                declare(None, "usesIcon",
                        "the snippet carries a library glyph but no component meta renders it",
                        note=f"{sn} -> {ic}")
                continue
            if ic not in slugs:
                declare("component:" + comp, "usesIcon",
                        "the byte-matched glyph resolves to a file the manifest does not hold",
                        note=f"{comp} -> {ic}")
                continue
            comp_icon.add((comp, ic))
        for comp, ic in sorted(comp_icon):
            link("component:" + comp, ICON + ic, "usesIcon",
                 via="byte-match of normalised <path d> against the icon library "
                     "(_validate_icons.py's own norm()/DRE), through the meta's renderedBy snippet")

    # ---- logo: nodes, usesLogo, defaultFor --------------------------------
    stems = [] if no_logos else logo_stems(corpus)
    logo_fields = {}
    for stem in stems:
        m = LOGO_RX.match(stem)
        if not m:
            unresolved.append({"source": None, "type": "logo:", "why":
                               "the filename does not carry the three fields "
                               "<lockup>-<light|dark>-<colour|mono>; no node is invented",
                               "note": stem})
            continue
        f = m.groupdict()
        logo_fields[stem] = f
        add(LOGO + stem, stem, file=f"assets/logos/{stem}.svg", **f)

    logo_comp = {}
    if not no_logos:
        for sn, stem in sorted(scan_logo_refs(corpus)):
            comp = s2c.get(sn)
            if comp is None or stem not in logo_fields:
                declare(None, "usesLogo",
                        "a src= names a logo file but the snippet maps to no component, "
                        "or the stem is not a parsed logo node",
                        note=f"{sn} -> {stem}")
                continue
            logo_comp.setdefault((comp, stem), True)
        for comp, stem in sorted(logo_comp):
            link("component:" + comp, LOGO + stem, "usesLogo",
                 via='src="…/assets/logos/<file>.svg" in the component\'s renderedBy snippet')

    # ---- defaultFor — s230-D2's own words, by filename containment --------
    dr = next((r for r in R if r["id"] == DEFAULT_RULING), None)
    text = ((dr.get("ruled") or "") + "\n" + (dr.get("says") or "")) if dr else ""
    named = text_default(dr, logo_fields) if not no_logos else set()
    if dr and not no_logos:
        for stem in sorted(named):
            declare(LOGO + stem, "defaultFor",
                    f"{DEFAULT_RULING} names this stem as the default lockup, but `theme:` is "
                    "NOT a node kind in the live graph and this lane proposes three kinds, not "
                    "four. The theme is carried as an edge property; no theme: node is invented",
                    note=f'{DEFAULT_RULING} ({dr.get("date")}, by {dr.get("by")}) names '
                         f'"{stem}" — theme={logo_fields[stem]["theme"]}')
            edges[-1]["theme"] = logo_fields[stem]["theme"]
            edges[-1]["ruling"] = DEFAULT_RULING

        # the residue s230-D2 records BY NAME IN ITS OWN CLAUSE: a component it deliberately
        # did NOT rebind. Anchored on the clause (RESIDUE_RX), never on "is this slug a
        # substring of the ruling's English?" — that old test made a prose join produce a
        # declared null and would have handed a fourth substring slug the rail's reason
        # verbatim (RIV A3, fixed #279 lane IL). Case-folded because the ruling names the
        # SNIPPET file (`App-shell-nav-rail`) and the component slug is the lower-cased stem
        # of the same name.
        bound = {c for c, _s in logo_comp}
        by_low = {s.lower(): s for s in sorted(metas)}
        for name, clause in residue_clauses(dr):
            slug = by_low.get(name.lower())
            if slug is None:
                unresolved.append({
                    "source": None, "type": "usesLogo",
                    "why": f"{DEFAULT_RULING}'s own clause names a component as deliberately NOT "
                           "rebound but no component meta carries that slug — the residue is "
                           "DECLARED against the ruling's words, never attached to a guess",
                    "note": f"{name}: named by {DEFAULT_RULING} — \"{clause}\""})
                continue
            if slug in bound:
                continue
            unresolved.append({
                "source": "component:" + slug, "type": "usesLogo",
                "why": f"{DEFAULT_RULING} names this component in its own clause as deliberately "
                       "NOT rebound — a ruling-shaped residue that stays Dave's. The gap is "
                       "DECLARED, never quietly completed",
                "note": f"{slug}: no assets/logos/ src= in its snippet, and that is the ruling — "
                        f"{DEFAULT_RULING} says \"{clause}\""})

    # ---- ruledBy — a `governs` entry that NAMES an icon .svg --------------
    ruled_pairs, ruled_declared = [], []
    for r in R:
        for entry in (r.get("governs") or []):
            m = GOVERNS_ICON_RX.search(str(entry).strip())
            if not m:
                continue
            stem = m.group(1)
            if stem in slugs:
                ruled_pairs.append((stem, r["id"]))
            else:
                ruled_declared.append((stem, r["id"], str(entry).strip()))
    for stem, rid in sorted(set(ruled_pairs)):
        link(ICON + stem, "ruling:" + rid, "ruledBy")
    for stem, rid, entry in sorted(set(ruled_declared)):
        unresolved.append({"source": None, "type": "ruledBy", "why":
                           f"{rid} governs this .svg but the manifest does not hold the slug, so "
                           f"there is no icon: node to source the edge from — blocker B1 again",
                           "note": f"{rid} governs {entry}"})

    # ---- B3: the logos bound by NO rule -----------------------------------
    rule_files, logo_rules = {}, 0
    ri = _k(corpus) / "guidelines" / "_rules-index.json"
    if ri.exists():
        try:
            data = json.loads(ri.read_text(encoding="utf-8"))
            rows = data.get("rules", data) if isinstance(data, dict) else data
            for row in (rows if isinstance(rows, list) else []):
                if isinstance(row, dict) and row.get("file"):
                    rule_files[row["file"]] = rule_files.get(row["file"], 0) + 1
            logo_rules = rule_files.get("logos.md", 0)
        except Exception:
            pass
    logo_ruling_paths = sorted({m.group(1) for r in R for e in (r.get("governs") or [])
                                for m in [GOVERNS_LOGO_RX.search(str(e).strip())] if m})
    unbound = sorted(s for s in logo_fields if s not in named) if not no_logos else []
    for s in unbound:
        unresolved.append({
            "source": LOGO + s, "type": "governedBy",
            "why": f"NOTHING binds this lockup: {DEFAULT_RULING} does not name it, "
                   f"_rules-index.json holds {logo_rules} rules whose file is logos.md, and "
                   f"{len(logo_ruling_paths)} rulings name a logo .svg in governs. logos.md says "
                   "the standard lives on create.hsbc — blocker B3, and it is not ours",
            "note": f"{s}: referenced by "
                    f"{len([1 for c, st in logo_comp if st == s])} component(s)"})

    # ---- the declined and the handed-over ---------------------------------
    fillmodes = {}
    for _g, r in recs:
        fillmodes[r.get("fillMode")] = fillmodes.get(r.get("fillMode"), 0) + 1

    node_counts, edge_counts = {}, {}
    for n in nodes.values():
        node_counts[n["type"]] = node_counts.get(n["type"], 0) + 1
    for e in edges:
        edge_counts[e["type"]] = edge_counts.get(e["type"], 0) + 1
    drawn = {}
    for e in edges:
        if e["t"] is not None:
            drawn[e["type"]] = drawn.get(e["type"], 0) + 1

    def split(kinds):
        ns = [n for n in nodes.values() if n["type"] in kinds]
        ids = {n["id"] for n in ns}
        es = [e for e in edges if e["s"] in ids or e["t"] in ids
              or (str(e["s"]).startswith("component:") and e["t"] in ids)]
        return sorted(ns, key=lambda n: n["id"]), es

    inodes, iedges = split({"icon", "iconGroup"})
    lnodes, ledges = split({"logo"})

    def payload(kind, ns, es):
        return {"$description":
                f"PROPOSED {kind} nodes and their edges (#277 lane RI, s269-D1 STEP 4). "
                "NOT RATIFIED until a ruling id is recorded in knowledge/_rulings.json "
                "and listed in gen_kg_icons.RATIFIES.",
                "generated_by": "notes/_lanes/277/icons-propose/gen_kg_icons.py",
                "family": FAMILY,
                "edge_types": {t: EDGE_STATUS[t] for t in EDGE_TYPES},
                "nodes": ns, "edges": es}

    ipay = payload("icon:/iconGroup:", inodes, iedges)
    lpay = payload("logo:", lnodes, ledges)

    blob = json.dumps({"nodes": sorted(nodes.values(), key=lambda n: n["id"]), "edges": edges},
                      separators=(",", ":"), ensure_ascii=False)
    explorer = REPO / "notes" / "_KG-EXPLORER.html"
    exp_bytes = explorer.stat().st_size if explorer.exists() else 0

    report = {
        "corpus": str(_k(corpus)),
        "manifest_generated": man.get("$generated"),
        "manifest_total": man.get("$total"),
        "manifest_counts": man.get("$counts"),
        "records_read": len(recs),
        "groups_read": len(man.get("groups", {})),
        "unique_slugs": len(slugs),
        "duplicate_slugs": len(recs) - len(slugs),
        "svg_on_disk": len(disk),
        "on_disk_not_in_manifest": stale,
        "in_manifest_not_on_disk": sorted(slugs - set(disk)),
        "active_true": sum(1 for _g, r in recs if r.get("active")),
        "active_by_slug_rx": sum(1 for _g, r in recs if ACTIVE_RX.search(r["slug"])),
        "active_flag_vs_slug_mismatch": mismatch,
        "bases_with_multiple_actives": {b: v for b, v in sorted(multi.items())},
        "fill_modes": fillmodes,
        "themedBy": "DECLINED — contentless at the icon level (IX §1c): "
                    f"{fillmodes.get('currentColor', 0)} identical currentColor records against "
                    "8 icon/* token leaves the CONSUMING CONTEXT sets. Handed to the tokens gap.",
        "tokens_icon_metas": tokens_icon_metas(corpus),
        "byte_match": scan_stats,
        "usesIcon_components": len({c for c, _i in comp_icon}),
        "usesIcon_icons": len({i for _c, i in comp_icon}),
        "usesIcon_pairs": len(comp_icon),
        "icons_unused": len(slugs) - len({i for _c, i in comp_icon}),
        "logos_read": len(logo_fields),
        "logos_named_by_ruling": sorted(named),
        "logos_unbound": unbound,
        "usesLogo_components": len({c for c, _s in logo_comp}),
        "usesLogo_logos": len({s for _c, s in logo_comp}),
        "logo_rules_in_rules_index": logo_rules,
        "rulings_naming_a_logo_svg": logo_ruling_paths,
        "ruledBy_drawn": len(set(ruled_pairs)),
        "ruledBy_declared": len(set(ruled_declared)),
        "rulings_available": len(rids),
        "gate_norm_matches_validate_icons": gate_norm_matches(corpus),
        "edge_counts": edge_counts,
        "edge_targets_resolved": drawn,
        "edge_status": {t: EDGE_STATUS[t] for t in EDGE_TYPES},
        "edge_total": len(edges),
        "node_counts": node_counts,
        "node_total": len(nodes),
        "unresolved": unresolved,
        "unresolved_total": len(unresolved),
        "payload_bytes": len(blob.encode("utf-8")),
        "explorer_bytes": exp_bytes,
        "payload_pct_of_explorer": (round(100.0 * len(blob.encode("utf-8")) / exp_bytes, 2)
                                    if exp_bytes else None),
        "chip": {"family": FAMILY, "default": "OFF",
                 "precedent": "s274-D11 / #275 — an additive family's chip ships OFF, like `ux`"},
        "ratifies": list(RATIFIES),
        "options": {"icons_only": bool(icons_only), "no_logos": bool(no_logos),
                    "no_usesicon": bool(no_usesicon)},
    }
    return ipay, lpay, report


def text_default(dr, logo_fields):
    """The stems s230-D2 names, by byte-containment of the FILENAME STEM in the
    ruling's own fields. Returns a set; empty if the ruling is absent."""
    if not dr:
        return set()
    text = (dr.get("ruled") or "") + "\n" + (dr.get("says") or "")
    return {s for s in logo_fields if s in text}


def residue_clauses(dr):
    """[(name, clause)] — the components the ruling's OWN CLAUSE names as deliberately
    NOT rebound, with the ruling's sentence quoted back so the declared null carries the
    ruling's reason and never a reason hardcoded here (RIV A3). Returns [] if the ruling
    is absent or carries no such clause: a residue nobody wrote down is not a residue."""
    if not dr:
        return []
    text = (dr.get("ruled") or "") + "\n" + (dr.get("says") or "")
    out = []
    for m in RESIDUE_RX.finditer(text):
        tail = text[m.start():]
        stop = tail.find(". ")
        clause = tail[:stop + 1] if 0 < stop <= 200 else tail[:200]
        out.append((m.group(1), re.sub(r"\s+", " ", clause).strip()))
    return out


# ------------------------------------------------------------------ the door

def ruling_exists(rid, corpus=None):
    return any(r["id"] == rid for r in rulings(corpus))


def land(corpus=None, ratified=None, **kw):
    """Refuses unless the id is well-formed, RECORDED in _rulings.json, and LISTED in
    RATIFIES. RATIFIES now holds the four s277-D4..D7 ids and NOTHING else, so every
    other id — live, malformed, absent — is still refused, each at its own gate (#75)."""
    if not ratified:
        raise SystemExit("REFUSED — --land needs --ratified sNNN-DN (three new node kinds and six "
                         "new edge types are closed-vocabulary changes, #75)")
    if not RULING_ID_RX.match(ratified):
        raise SystemExit(f"REFUSED — --ratified '{ratified}' is not a ruling id (sNNN-DN)")
    if not ruling_exists(ratified, corpus):
        raise SystemExit(f"REFUSED — ruling '{ratified}' is not in _rulings.json. "
                         "An unrecorded ratification is not a ratification.")
    if ratified not in RATIFIES:
        raise SystemExit(f"REFUSED — '{ratified}' is a real ruling but it does not ratify THIS "
                         f"proposal. gen_kg_icons.RATIFIES is {RATIFIES!r}. A ruling about "
                         "something else is not a door.")
    ipay, lpay, report = build(corpus, **kw)
    for pay, name in ((ipay, LANDED_ICONS), (lpay, LANDED_LOGOS)):
        pay["ratified"] = ratified
        pay["$description"] = (f"RATIFIED {name} under {ratified} (#277 lane RI; s269-D1 STEP 4). "
                               f"Regenerate with `gen_kg_icons.py --land --ratified {ratified}`; "
                               "never hand-edit.")
        (_k(corpus) / name).write_text(json.dumps(pay, indent=2, ensure_ascii=False) + "\n",
                                       encoding="utf-8")
    report["landed"] = {"ratified": ratified, "files": [LANDED_ICONS, LANDED_LOGOS]}
    return report


def _dry(corpus, out_dir, **kw):
    ipay, lpay, report = build(corpus, **kw)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "_icon_nodes.json").write_text(
        json.dumps(ipay, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out_dir / "_logo_nodes.json").write_text(
        json.dumps(lpay, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report["mode"] = "dry-run"
    report["wrote"] = [str(out_dir / "_icon_nodes.json"), str(out_dir / "_logo_nodes.json"),
                       str(out_dir / "dry-run.json")]
    (out_dir / "dry-run.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


# ------------------------------------------------------------------ selftest

def _mini(tmp):
    """Synthetic knowledge/ dir — touches nothing in the live tree.

    Shapes deliberately planted, each of which a careless generator gets wrong:
      · `alpha` / `alpha-active` / `alpha-active-2` — the B4 multi-active base.
      · `ghost-active` — an ORPHAN: no `ghost` in the manifest.
      · `stray` — on DISK but NOT in the manifest, and RULED IN by s001-D1 (B1).
      · `beta` shares its geometry with NOTHING; `alpha` geometry appears inline in
        a snippet, so the byte-match must find exactly one pair.
      · one inline path matching nothing, and one <svg> with no <path> (sprite).
      · `accessibility` is a slug AND a word in a meta's prose — the prose route
        would fire and no edge may appear for it.
      · logos: 2 well-formed stems + 1 malformed (`badname.svg`), one named by the
        ruling, one referenced by a snippet, one bound by nothing.
    """
    k = tmp / "knowledge"
    (k / "assets" / "icons" / "grp-one").mkdir(parents=True)
    (k / "assets" / "logos").mkdir(parents=True)
    (k / "snippets").mkdir(parents=True)
    (k / "components").mkdir(parents=True)
    (k / "guidelines").mkdir(parents=True)

    D_ALPHA = "M0 0 L10 10"
    D_BETA = "M1 1 L2 2"
    rec = lambda n, s, f, a, fm: {"name": n, "slug": s, "file": f, "active": a,
                                  "fillMode": fm, "fills": ["#333333"]}
    man = {"$source": "mini", "$generated": "2026-01-01",
           "groups": {"Grp One": [rec("Alpha", "alpha", "grp-one/alpha.svg", False, "currentColor"),
                                  rec("Alpha Active", "alpha-active", "grp-one/alpha-active.svg",
                                      True, "currentColor"),
                                  rec("Alpha Active 2", "alpha-active-2",
                                      "grp-one/alpha-active-2.svg", True, "baked"),
                                  rec("Ghost Active", "ghost-active", "grp-one/ghost-active.svg",
                                      True, "currentColor"),
                                  rec("Beta", "beta", "grp-one/beta.svg", False, "currentColor"),
                                  rec("Accessibility", "accessibility",
                                      "grp-one/accessibility.svg", False, "currentColor")]},
           "$counts": {"Grp One": 6}, "$total": 6}
    (k / "assets" / "icons" / "icons.manifest.json").write_text(json.dumps(man, indent=1),
                                                                encoding="utf-8")
    for slug, d in (("alpha", D_ALPHA), ("alpha-active", "M3 3 L4 4"),
                    ("alpha-active-2", "M5 5 L6 6"), ("ghost-active", "M7 7 L8 8"),
                    ("beta", D_BETA), ("accessibility", "M9 9 L9 0"), ("stray", "M8 0 L8 1")):
        (k / "assets" / "icons" / "grp-one" / f"{slug}.svg").write_text(
            f'<svg><path d="{d}"/></svg>', encoding="utf-8")
    # `mark-light-mono` shares the LOCKUP WORD with the two the ruling names but its own
    # stem appears nowhere in it: a defaultFor that matched the lockup instead of the whole
    # filename would name three, and bite 9 would go red.
    for stem, body in (("mark-light-colour", "a"), ("mark-dark-colour", "b"),
                       ("mark-light-mono", "c"), ("badname", "d")):
        (k / "assets" / "logos" / f"{stem}.svg").write_text(f"<svg><!--{body}--></svg>",
                                                            encoding="utf-8")

    # one.reference.html: the alpha geometry (NORMALISED differently — extra whitespace,
    # so a generator that skipped norm() finds nothing), one unmatched path, one sprite.
    (k / "snippets" / "one.reference.html").write_text(
        f'<svg><path d="  {D_ALPHA}  "/></svg>'
        '<svg><path d="M99 99 L98 98"/></svg>'
        '<svg><use href="#sprite"/></svg>'
        '<img src="../assets/logos/mark-light-colour.svg">', encoding="utf-8")
    # two.reference.html maps to NO component: its pair must be declared, not dropped.
    (k / "snippets" / "two.reference.html").write_text(
        f'<svg><path d="{D_BETA}"/></svg>', encoding="utf-8")

    (k / "components" / "widget.meta.json").write_text(json.dumps({
        "name": "Widget", "provenance": {"by": "mini"},
        "notes": "This component has excellent accessibility and no icons at all.",
        "tokens": {"icon": "icon/default"},
        "edges": {"renderedBy": [{"ref": "snippet:one.reference.html"}]}}, indent=1),
        encoding="utf-8")
    (k / "components" / "EXAMPLE-skip.meta.json").write_text(json.dumps(
        {"name": "Skip", "edges": {}}, indent=1), encoding="utf-8")
    (k / "components" / "rail.meta.json").write_text(json.dumps(
        {"name": "Rail", "provenance": {"by": "mini"}, "edges": {}}, indent=1), encoding="utf-8")
    # `chrome` is the A3 control: its slug IS a substring of the ruling's English ("on light
    # chrome"), it binds no logo, and the ruling's clause does NOT name it. The old
    # substring-over-English test gave it a declared null with the rail's reason attached;
    # the clause anchor must leave it alone. Bite 18 is the whole point of this file.
    (k / "components" / "chrome.meta.json").write_text(json.dumps(
        {"name": "Chrome", "provenance": {"by": "mini"}, "edges": {}}, indent=1), encoding="utf-8")

    (k / "_rulings.json").write_text(json.dumps({"rulings": [
        {"id": "s001-D1", "ruled": "the stray glyph is library", "date": "2026-01-02", "by": "Dave",
         "says": "x", "governs": ["knowledge/assets/icons/grp-one/stray.svg",
                                  "knowledge/assets/icons/grp-one/alpha.svg",
                                  "knowledge/assets/icons/"]},
        {"id": "s230-D2", "ruled": 'default logo "mark-light-colour" on light chrome, '
                                   "mark-dark-colour on dark chrome",
         "date": "2026-01-03", "by": "Dave",
         "says": "rail deliberately NOT rebound — a ruling-shaped residue that stays Dave's",
         "governs": ["knowledge/snippets/one.reference.html"]},
        # the mini's ratifying id: the ONE recorded ruling that is also in RATIFIES, so the
        # door can be shown to open for it and for nothing else (bites 12 and 17).
        {"id": "s277-D4", "ruled": "the mini asset kinds enter", "date": "2026-01-04",
         "by": "Dave", "says": "go"}]}, indent=1), encoding="utf-8")
    (k / "guidelines" / "_rules-index.json").write_text(json.dumps(
        {"rules": [{"id": "icon-001", "file": "icons.md"}]}, indent=1), encoding="utf-8")
    (k / "_validate_icons.py").write_text(
        'DRE = re.compile(r\'\\bd="([^"]+)"\')\n'
        'def norm(d):\n    return re.sub(r"\\s+", " ", d.strip())\n', encoding="utf-8")
    return k


def selftest():
    fails = []

    def bite(n, desc, cond):
        """`cond` may be a bool or a zero-arg callable. A callable that RAISES is a
        FAIL, not a crash: a mutant that deletes a field must turn the bite red, not
        blow the harness up and be scored 'did not even run'."""
        if callable(cond):
            try:
                cond = bool(cond())
            except Exception as e:
                cond = False
                desc += f"  [raised {type(e).__name__}: {e}]"
        print(("  ok  " if cond else "  FAIL") + f"  bite {n}: {desc}")
        if not cond:
            fails.append(n)

    with tempfile.TemporaryDirectory() as td:
        k = _mini(Path(td))
        ipay, lpay, rep = build(k)
        E = ipay["edges"] + lpay["edges"]
        ids = {n["id"] for n in ipay["nodes"]} | {n["id"] for n in lpay["nodes"]}

        def of(ty):
            return [e for e in E if e["type"] == ty]

        src = json.loads((k / "assets" / "icons" / "icons.manifest.json").read_text())
        rows = {r["slug"]: r for lst in src["groups"].values() for r in lst}

        # 1 — every manifest record becomes ONE icon: node whose fields equal the record
        #     byte for byte, plus the group key it SITS UNDER (which the record never names).
        a = [n for n in ipay["nodes"] if n["id"] == "icon:alpha"][0]
        bite(1, "every manifest record becomes an icon: node carrying its own fields verbatim + its group key", lambda:
             rep["node_counts"]["icon"] == 6 and rep["records_read"] == 6
             and all(n.get(f) == rows[n["slug"]].get(f)
                     for n in ipay["nodes"] if n["type"] == "icon"
                     for f in ICON_FIELDS if rows[n["slug"]].get(f) not in (None, "", [], {}))
             and a["group"] == "Grp One" and a["file"] == "grp-one/alpha.svg"
             and a["fillMode"] == "currentColor" and a["fills"] == ["#333333"]
             and "group" not in rows["alpha"])

        # 2 — MUTATION: `active` is the SLUG's rule, re-proved both ways, and inGroup is total.
        bite(2, "active<->slug agreement is re-derived (0 mismatches) and inGroup covers every icon once", lambda:
             rep["active_flag_vs_slug_mismatch"] == 0 and rep["active_true"] == 3
             and rep["active_by_slug_rx"] == 3
             and len(of("inGroup")) == 6 and rep["node_counts"]["iconGroup"] == 1
             and {e["t"] for e in of("inGroup")} == {"iconGroup:grp-one"})

        # 3 — MUTATION: an ORPHAN active is t:null + note; a multi-active base is declared;
        #     activeVariantOf is still drawn for every resolvable one.
        av = of("activeVariantOf")
        orph = [e for e in av if e["t"] is None]
        bite(3, "activeVariantOf draws the resolvable twins, declares the orphan as t:null, and declares B4 without drawing defaultActive", lambda:
             len([e for e in av if e["t"]]) == 2
             and {e["t"] for e in av if e["t"]} == {"icon:alpha"}
             and len(orph) == 1 and "ghost-active" in orph[0]["$note"]
             and "icon:ghost" not in ids
             and rep["bases_with_multiple_actives"] == {"alpha": ["alpha-active", "alpha-active-2"]}
             and not of("defaultActive")
             and any(u["type"] == "defaultActive" and "B4" in u["why"] for u in rep["unresolved"]))

        # 4 — MUTATION: the byte-match is `_validate_icons.py`'s OWN norm(). The snippet's
        #     path carries extra whitespace, so a generator that dropped norm() finds ZERO.
        # The gate-drift arm: rewrite the mini's _validate_icons.py so it no longer carries
        # the two lines that ARE the join, and the assertion must flip to False. An
        # assertion that cannot say no is not an assertion.
        _gate = (k / "_validate_icons.py").read_text(encoding="utf-8")
        (k / "_validate_icons.py").write_text("def norm(d):\n    return d.upper()\n",
                                              encoding="utf-8")
        _drift = gate_norm_matches(k)
        (k / "_validate_icons.py").write_text(_gate, encoding="utf-8")
        bite(4, "usesIcon comes from the gate's own normalised byte-match (whitespace-insensitive) and a DRIFTED gate flips the assertion to False", lambda:
             rep["gate_norm_matches_validate_icons"] is True and _drift is False
             and rep["usesIcon_pairs"] == 1 and rep["usesIcon_components"] == 1
             and rep["usesIcon_icons"] == 1
             and of("usesIcon")[0]["s"] == "component:widget"
             and of("usesIcon")[0]["t"] == "icon:alpha"
             and rep["byte_match"]["unmatched_paths"] == 1
             and rep["byte_match"]["svg_without_path"] == 1)

        # 5 — MUTATION: the PROSE route is never drawn. `accessibility` is a slug AND a
        #     word in widget's meta; the byte-match found no alpha-free pair for it.
        hits, metas_n, pairs, _top = prose_pair_count(k, {r["slug"] for r in rows.values()})
        bite(5, "the prose route fires in the corpus and NO edge is drawn from it — measured, refused, counted", lambda:
             hits >= 1 and pairs >= 1 and metas_n == 3
             and not [e for e in of("usesIcon") if e["t"] == "icon:accessibility"]
             and not [e for e in E if e.get("via", "").startswith("prose")])

        # 6 — a snippet that maps to NO component is declared, never dropped and never
        #     attached to a guessed component.
        bite(6, "an icon-bearing snippet with no component is declared in unresolved and drops no pair silently", lambda:
             any(u["type"] == "usesIcon" and "two.reference.html" in u["note"]
                 for u in rep["unresolved"])
             and not [e for e in of("usesIcon") if e["t"] == "icon:beta"])

        # 7 — B1: on disk, RULED IN, not in the manifest -> no node, and its ruledBy is declared.
        bite(7, "a ruled-in .svg missing from the manifest gets NO node, is named as B1, and its ruledBy edge is declared not invented", lambda:
             rep["on_disk_not_in_manifest"] == ["stray"] and rep["in_manifest_not_on_disk"] == []
             and "icon:stray" not in ids
             and any(u["type"] == "icon:" and "B1" in u["why"] and "s001-D1" in u["note"]
                     for u in rep["unresolved"])
             and rep["ruledBy_declared"] == 1 and rep["ruledBy_drawn"] == 1
             and of("ruledBy")[0]["s"] == "icon:alpha"
             and of("ruledBy")[0]["t"] == "ruling:s001-D1")

        # 8 — logos: three filename fields parsed, a malformed stem REFUSED (no node),
        #     usesLogo from src= only.
        bite(8, "logo nodes parse lockup/theme/colourMode from the filename, refuse a malformed stem, and usesLogo comes from src=", lambda:
             rep["logos_read"] == 3 and "logo:badname" not in ids
             and [n for n in lpay["nodes"] if n["id"] == "logo:mark-light-colour"][0]["theme"] == "light"
             and [n for n in lpay["nodes"] if n["id"] == "logo:mark-dark-colour"][0]["colourMode"] == "colour"
             and len([e for e in of("usesLogo") if e["t"]]) == 1
             and of("usesLogo")[0]["s"] == "component:widget"
             and any(u["type"] == "logo:" and u["note"] == "badname" for u in rep["unresolved"]))

        # 9 — MUTATION: defaultFor is s230-D2's FILENAME containment, the theme comes from
        #     the STEM's parsed field, and NO theme: node is invented.
        df = of("defaultFor")
        bite(9, "defaultFor fires on exactly the stems s230-D2 names, carries the stem's own theme, and invents no theme: node", lambda:
             len(df) == 2 and all(e["t"] is None for e in df)
             and {e["theme"] for e in df} == {"light", "dark"}
             and all(e["ruling"] == "s230-D2" for e in df)
             and not any(i.startswith("theme:") for i in ids)
             and all("s230-D2" in e["$note"] for e in df))

        # 10 — the s230-D2 RESIDUE: a component the ruling's CLAUSE names and that binds no
        #      logo is declared as a gap, never quietly completed, and the ruling's own
        #      sentence is quoted into the note instead of a reason hardcoded in this file.
        _res = [u for u in rep["unresolved"]
                if u["source"] == "component:rail" and u["type"] == "usesLogo"]
        bite(10, "a component s230-D2's own clause names but that binds no logo enters as a declared null quoting the ruling", lambda:
             len(_res) == 1 and "s230-D2" in _res[0]["why"]
             and "deliberately NOT rebound" in _res[0]["note"]
             and "56px" not in _res[0]["why"] + _res[0]["note"]   # the reason is the ruling's, not ours
             and not any(u["source"] == "component:widget" and u["type"] == "usesLogo"
                         for u in rep["unresolved"]))

        # 18 — A3 (RIV, #279 lane IL): THE SECOND SUBSTRING SLUG. `chrome` is a substring of
        #      s230-D2's English ("on light chrome") and binds no logo, so the old
        #      substring-over-English test produced a null for it with the rail's reason
        #      attached. The clause anchor must leave it — and every other non-named slug —
        #      alone, while still finding the one the ruling names.
        dr10 = next(r for r in rulings(k) if r["id"] == "s230-D2")
        _rtext = ((dr10.get("ruled") or "") + "\n" + (dr10.get("says") or "")).lower()
        bite(18, "the residue is anchored on s230-D2's own clause: a SECOND slug that is merely a substring of the ruling's English produces NO null", lambda:
             "chrome" in _rtext and "chrome" in component_metas(k)
             and [n for n, _c in residue_clauses(dr10)] == ["rail"]
             and {u["source"] for u in rep["unresolved"] if u["type"] == "usesLogo"}
                 == {"component:rail"})

        # 11 — MUTATION: the three option flags each remove exactly their own thing.
        p_i, l_i, r_i = build(k, icons_only=True)
        p_l, l_l, r_l = build(k, no_logos=True)
        p_u, l_u, r_u = build(k, no_usesicon=True)
        bite(11, "--icons-only drops iconGroup+inGroup, --no-logos drops every logo node and edge, --no-usesicon drops only the byte-match", lambda:
             "iconGroup" not in r_i["node_counts"] and "inGroup" not in r_i["edge_counts"]
             and r_i["node_counts"]["icon"] == 6
             and r_l["logos_read"] == 0 and not l_l["nodes"]
             and not [e for e in p_l["edges"] + l_l["edges"]
                      if e["type"] in ("usesLogo", "defaultFor")]
             and "usesIcon" not in r_u["edge_counts"] and r_u["edge_counts"]["inGroup"] == 6)

        # 12 — THE DOOR, WITH THE ALLOWLIST OPEN (#279 lane IL). RATIFIES now holds the four
        #      s277-D4..D7 ids, and the door must still refuse everything else: no id, a
        #      malformed id, an unrecorded id, and a LIVE ruling that is not in the list —
        #      each for ITS OWN reason, writing nothing. A door that gives one answer to four
        #      different keys cannot be shown to be checking four things.
        live = [r["id"] for r in rulings(k)]
        not_listed = [r for r in live if r not in RATIFIES]
        msgs = {}
        for bad in [None, "not-a-ruling", "s999-D9"] + not_listed:
            try:
                land(k, bad)
                msgs[bad] = "LANDED"
            except SystemExit as e:
                msgs[bad] = str(e)
        bite(12, "with the allowlist OPEN, --land still REFUSES for the RIGHT reason at each gate — no id, malformed, not in _rulings.json, a live ruling not in RATIFIES — and writes no file", lambda:
             RATIFIES == ("s277-D4", "s277-D5", "s277-D6", "s277-D7")
             and len(live) == 3 and sorted(not_listed) == ["s001-D1", "s230-D2"]
             and all(v != "LANDED" for v in msgs.values())
             and "--ratified sNNN-DN" in msgs[None]
             and "is not a ruling id" in msgs["not-a-ruling"]
             and "is not in _rulings.json" in msgs["s999-D9"]
             and all("does not ratify THIS proposal" in msgs[r] for r in not_listed)
             and not (k / LANDED_ICONS).exists() and not (k / LANDED_LOGOS).exists())

        # 13 — the edge-status table is honest: all six are NEW, and no edge type outside
        #      the declared six is ever emitted.
        bite(13, "all six edge types are declared NEW and no seventh type is emitted", lambda:
             sorted(rep["edge_status"]) == sorted(EDGE_TYPES)
             and set(rep["edge_status"].values()) == {"NEW"}
             and set(rep["edge_counts"]) <= set(EDGE_TYPES))

        # 14 — themedBy is DECLINED in words and in fact: 0 edges, and the fill split is
        #      reported so the decline can be checked rather than believed.
        bite(14, "themedBy is declined: zero token edges, the fillMode split reported, tokens.icon handed over", lambda:
             not [e for e in E if e["type"] == "themedBy"]
             and not any(str(e.get("t") or "").startswith("token:") for e in E)
             and rep["fill_modes"] == {"currentColor": 5, "baked": 1}
             and "DECLINED" in rep["themedBy"] and rep["tokens_icon_metas"] == 1)

        # 15 — a dry run writes into the OUT DIR and leaves the corpus byte-identical.
        with tempfile.TemporaryDirectory() as td2:
            k2 = _mini(Path(td2))
            before = {str(p): p.read_bytes() for p in k2.rglob("*") if p.is_file()}
            out = Path(td2) / "outdir"
            r15 = _dry(k2, out)
            now = {str(p): p.read_bytes() for p in k2.rglob("*") if p.is_file()}
            bite(15, "--dry-run writes its three JSONs outside the corpus and leaves the corpus byte-identical",
                 before == now and (out / "_icon_nodes.json").exists()
                 and (out / "_logo_nodes.json").exists() and (out / "dry-run.json").exists()
                 and not (k2 / LANDED_ICONS).exists() and not (k2 / LANDED_LOGOS).exists()
                 and r15["mode"] == "dry-run")

        # 16 — the payload is measured, not estimated, and the chip default is OFF.
        bite(16, "the explorer payload is measured in bytes from the serialised nodes+edges and the chip ships OFF", lambda:
             isinstance(rep["payload_bytes"], int) and rep["payload_bytes"] > 0
             and rep["chip"]["family"] == FAMILY and rep["chip"]["default"] == "OFF")

        # 17 — THE LANDING PATH, reached the way the real land is reached (#279 lane IL): the
        #      REAL allowlist, an id that is BOTH recorded in the corpus's _rulings.json and
        #      listed in RATIFIES. No global is mutated by this bite any more — the door is
        #      open on s277-D4 and the test walks through the same door the lane does.
        snap = {str(p): p.read_bytes() for p in k.rglob("*") if p.is_file()}
        try:
            r17 = land(k, "s277-D4")
            li = json.loads((k / LANDED_ICONS).read_text(encoding="utf-8"))
            ll = json.loads((k / LANDED_LOGOS).read_text(encoding="utf-8"))
            after = {str(p): p.read_bytes() for p in k.rglob("*") if p.is_file()
                     and p.name not in (LANDED_ICONS, LANDED_LOGOS)}
        finally:
            for nm in (LANDED_ICONS, LANDED_LOGOS):
                (k / nm).unlink(missing_ok=True)
        bite(17, "--land through the REAL allowlist writes exactly the two node files, NAMES the ruling, drops the PROPOSED text, and leaves every input byte-identical", lambda:
             "s277-D4" in RATIFIES and ruling_exists("s277-D4", k)
             and r17["landed"]["ratified"] == "s277-D4"
             and li["ratified"] == "s277-D4" and ll["ratified"] == "s277-D4"
             and "s277-D4" in li["$description"] and "s277-D4" in ll["$description"]
             and not any(w in li["$description"] + ll["$description"]
                         for w in ("PROPOSED", "NOT RATIFIED"))
             and after == snap)

    print("SELFTEST PASS" if not fails else f"SELFTEST FAIL — bites {fails}")
    return 1 if fails else 0


# ------------------------------------------------------------------ entry

def main():
    try:  # #269 PARKED-WITH-A-TRIPWIRE hook: advisory print, never a gate
        import _parked; _parked.notice("kg-edge-gen")
    except BaseException:
        pass
    argv = sys.argv[1:]
    if "--selftest" in argv:
        return selftest()

    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else default

    corpus = Path(opt("--corpus")) if opt("--corpus") else None
    kw = {"icons_only": "--icons-only" in argv, "no_logos": "--no-logos" in argv,
          "no_usesicon": "--no-usesicon" in argv}

    if "--prose-count" in argv:
        man = load_manifest(corpus)
        slugs = {r["slug"] for _g, r in icon_records(man)}
        hits, total, pairs, top = prose_pair_count(corpus, slugs)
        print(f"PROSE ROUTE — REFUSED (s274-D12, s276-D5). Measured, never drawn:")
        print(f"  metas containing >=1 exact manifest slug as a token : {hits} of {total}")
        print(f"  total (meta, slug) prose pairs                      : {pairs}")
        print("  top: " + " · ".join(f"{s} x{n}" for s, n in top))
        print("  NO CODE PATH in this file turns any of these into an edge.")
        return 0

    if "--land" in argv:
        rep = land(corpus, opt("--ratified"), **kw)
        print(f"LANDED — ratified {rep['landed']['ratified']} · {rep['landed']['files']}")
        return 0

    out = Path(opt("--dry-run") or opt("--out") or str(DEFAULT_OUT))
    rep = _dry(corpus, out, **kw)
    print(f"DRY RUN — {rep['records_read']} icon records · {rep['groups_read']} groups · "
          f"{rep['logos_read']} logos  ->  {rep['node_total']} nodes · {rep['edge_total']} edges")
    print(f"  nodes: {rep['node_counts']}")
    print(f"  edges: {rep['edge_counts']}")
    print(f"  edge targets resolved: {rep['edge_targets_resolved']}")
    print(f"  status: {rep['edge_status']}")
    print(f"  byte-match: {rep['byte_match']} -> {rep['usesIcon_pairs']} pairs / "
          f"{rep['usesIcon_components']} components / {rep['usesIcon_icons']} icons "
          f"({rep['icons_unused']} of {rep['unique_slugs']} icons unused)")
    print(f"  declared nulls (unresolved): {rep['unresolved_total']}")
    print(f"  payload {rep['payload_bytes']:,} B against explorer {rep['explorer_bytes']:,} B "
          f"= +{rep['payload_pct_of_explorer']}%")
    print(f"  chip: {rep['chip']['family']} default {rep['chip']['default']}")
    print(f"  wrote {out}")
    print("  NOT LANDED — this is a dry run. Three node kinds and six edge types are "
          f"closed-vocabulary changes (#75); RATIFIES is {RATIFIES!r}, so --land accepts "
          "those ids and refuses every other id there is.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
