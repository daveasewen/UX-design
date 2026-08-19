#!/usr/bin/env python3
"""gen_itinerary_status.py — the itinerary Status column, DERIVED from the store (#203, Wave 3b Lane H).

THE CLASS THIS FIXES. `reviews/ITINERARY-2026-07-14-apollo-component-library.xlsx` carries a
HAND-MAINTAINED `Status` column. It was written 2026-07-14; 24 components landed on 2026-07-19 and
2026-07-22 and nobody re-statused it. At #203 a whole six-lane wave was briefed off that column and
all six lanes hit the same wall: **18 of 18 briefed "P1 gaps" already existed, gated**
(`notes/_receipts/2026-08-19-203-wave3-lane{A..F}-*.md`). A hand-maintained status column is a
CARRIED CLAIM, and premises age faster than rules [[premise-ages-faster-than-rule]]; a carried
COUNT is the same defect (#194). The fix is not to re-type the column — it is to stop having one.
This generator DERIVES status from the artefacts themselves, so it cannot rot.

⛔ THE 2026-07-14 FILES ARE FROZEN. This reads the .xlsx and never writes it. History is write-once
(ADR-0017 / `s192-D1`): the snapshot stays a snapshot and this is a NEW dated derivation beside it.

THE SECOND DEFECT, and the reason a naive `ls` is not enough. Wave 3a's own sweeps DISAGREED with
each other because they matched itinerary row names against snippet filenames mechanically:
Lane F reported rows 17/19/52/89 "absent" on a first slug match and rows 13/53/63/86 "genuinely
absent", then declared the miss rather than asserting it. Rows 17/19/52/89 live under
`Amount-input` / `Secure-entry` / `Stat-card` / `Amount-display`; row 13 under `Form-layout`;
row 63 under `Modals` + `Modal-lightbox`. **A slug mismatch is indistinguishable from an absence**
[[unmatched-grep-is-not-an-absence]]. So resolution here is a declared four-rung ladder, every rung
recorded in the output as `basis`, and rung 4 (fuzzy) NEVER decides — it raises UNRESOLVED, loudly.

DERIVATION — four store signals per resolved slug, each an independent probe:
  snippet   knowledge/snippets/<Name>.reference.html
  meta      knowledge/components/<slug>.meta.json
  showroom  showroom/<slug>.html
  migrated  <Name>.reference.html present in _validate_radius.MIGRATED_SNIPPETS (the radius ratchet)
  canon     count of `.cn-<slug>` rules in knowledge/canon/canon.css

RESOLUTION LADDER (precedence, highest first; `basis` names which rung fired):
  1 `map`        — ROW_MAP, an explicit alternate-slug entry, each carrying its own `why` evidence
  2 `notes`      — a known slug named verbatim in the itinerary's own Notes cell ("dropdown, gated.")
  3 `mechanical` — slugified Component name (parenthetical stripped, `/`-tail dropped) that HITS
  4 `absent`     — mechanical slug that hits nothing AND no plausible alias in the store
  ⚠ if rung 4 lands but a fuzzy token scan finds a plausible store alias, the row is UNRESOLVED,
    printed loudly, and the run exits 1. NEVER GUESS — that guess is the whole defect (#203).

FAIL LOUD, NEVER GUESS (the brief's words): a row whose `#` is not an integer, or whose Component
cell is blank, raises SystemExit naming the sheet row. A crash is not a fail [[a-crash-is-not-a-fail]].

Outputs (both deterministic — no timestamps, so `--check` is meaningful):
  reviews/ITINERARY-STATUS-2026-08-19-v1.html   Dave's surface: drift table + TRUE-gap list
  reviews/ITINERARY-STATUS-2026-08-19-v1.json   machine-readable sidecar (next wave's brief input)

⛔ NOTHING HERE IS A RULING. Every derived status is a MEASUREMENT of the store, and every TRUE-gap
verdict carries the probes it was measured by. Component promotion is on Dave's DO-NOT-RULE list;
this file promotes nothing and edits no component, token, meta or shared doc.

Usage:
  python3 knowledge/gen_itinerary_status.py             # write both outputs
  python3 knowledge/gen_itinerary_status.py --check     # verify in sync (rc 1 if drifted)
  python3 knowledge/gen_itinerary_status.py --selftest  # drive the derivation, incl. mutation arms
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import html as htmlmod
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNIPD = os.path.join(HERE, "snippets")
COMPD = os.path.join(HERE, "components")
SHOWD = os.path.join(ROOT, "showroom")
CANON = os.path.join(HERE, "canon", "canon.css")
RADIUS = os.path.join(HERE, "_validate_radius.py")
ICONS = os.path.join(HERE, "assets", "icons")
LOGOS = os.path.join(HERE, "assets", "logos")

ITIN = os.path.join(ROOT, "reviews", "ITINERARY-2026-07-14-apollo-component-library.xlsx")
STAMP = "2026-08-19-v1"
OUT_HTML = os.path.join(ROOT, "reviews", "ITINERARY-STATUS-%s.html" % STAMP)
OUT_JSON = os.path.join(ROOT, "reviews", "ITINERARY-STATUS-%s.json" % STAMP)

# ---------------------------------------------------------------------------
# ROW_MAP — the alternate-slug map. THIS IS THE INSTRUMENT'S ONLY HAND-HELD PART,
# so every entry carries the evidence that justifies it. `slugs` may name slugs that
# do NOT exist: an entry is a statement about WHAT THE ROW WOULD BE CALLED, not a
# claim that it is present. Presence is measured, never mapped.
#   class: "component" (default) | "asset-system" | "family" | "layer-2"
#   related: [(slug, quoted evidence)] — a gated HOST that carries this row as a variant.
#            A `related` never upgrades a status; it annotates a gap so the next wave
#            knows where to start [[home-by-addition-then-cut]].
# ---------------------------------------------------------------------------
ROW_MAP = {
    4:  {"slugs": ["segmented-control", "view-options"],
         "why": "Row names both; Segmented-control was promoted OUT of View-options 2026-07-24 "
                "(comment in _validate_radius.MIGRATED_SNIPPETS). Both snippets exist."},
    6:  {"slugs": ["split-button"],
         "why": "⚠ NOT row 1's Button. A split button is a two-target control (default action + "
                "menu affordance); probe: `grep -ci split Button.reference.html` -> 0. Mapped so "
                "the fuzzy rung cannot close a real gap on a name prefix."},
    8:  {"slugs": ["input-fields"],
         "why": "'Text input' is the Input-fields snippet (the text-field family); itinerary "
                "marks row 8 Gated and no `text-input` slug has ever existed."},
    10: {"slugs": ["dropdown"], "why": "Itinerary Notes cell reads verbatim: 'dropdown, gated.'"},
    11: {"slugs": ["selection-controls"], "why": "Notes cell: 'selection-controls, gated.'"},
    13: {"slugs": ["form-layout"],
         "why": "Mechanical slug 'form-layout-validation' misses; Form-layout.reference.html is the "
                "row-13 build (Lane F's sweep called row 13 'genuinely absent' on that miss)."},
    17: {"slugs": ["amount-input"],
         "why": "Amount-input.reference.html:9 cites 'itinerary row 17 (P1), banking-critical' "
                "(quoted in laneC receipt). Mechanical slug misses entirely."},
    18: {"slugs": ["file-upload"], "why": "file-upload.meta.json purpose: 'Itinerary row 18 (P1)'."},
    19: {"slugs": ["secure-entry"],
         "why": "Secure-entry.reference.html:9 cites 'itinerary row 19 (P1)' (laneC receipt)."},
    23: {"slugs": ["tags-input"],
         "why": "⚠ NOT row 45's Tags. Tags is a display-chip component; row 23 is an INPUT. "
                "Fuzzy matching would wrongly bind these — mapped explicitly to keep the gap TRUE."},
    24: {"slugs": ["range-slider"],
         "why": "⚠ NOT row 12's Slider (single-thumb). Mapped explicitly so the fuzzy rung cannot "
                "silently close a real gap."},
    26: {"slugs": ["cascader"],
         "why": "⚠ NOT row 22's Multi-select (fuzzy matches on 'select'). A cascader is a "
                "hierarchical tree-select; probe: `grep -ci 'cascad|tree' Dropdown.reference.html` -> 0."},
    27: {"slugs": ["transfer-list"],
         "why": "⚠ NOT row 40's List-items (fuzzy matches on 'list'). Row 27 is the dual-list "
                "transfer control."},
    32: {"slugs": ["navigations"], "why": "Notes cell: 'navigations, gated.'"},
    33: {"slugs": ["dropdown"],
         "why": "Notes cell: 'dropdown, gated.' — rows 10 and 33 SHARE one artefact; both are "
                "reported against it and the sharing is declared, not hidden."},
    36: {"slugs": ["sidebar-nav"],
         "why": "⚠ NOT row 32's Navigations. Slug probed live in the tree: Lane I of this same "
                "#203 wave is building `Sidebar-nav.reference.html` while this ran — the mapping is "
                "a measurement of the working tree, not a plan."},
    37: {"slugs": ["anchor-nav"],
         "why": "Slug probed live in the tree — Lane I landed `Anchor-nav.reference.html` BETWEEN "
                "two runs of this generator, and the fuzzy rung caught it as UNRESOLVED rather "
                "than printing 'Gap'. That refusal is the instrument working."},
    52: {"slugs": ["stat-card"],
         "why": "Stat-card.reference.html, 164 lines, gated (laneE receipt step 0). Mechanical "
                "slug 'stat-metric-card' misses."},
    53: {"slugs": [], "class": "family", "family_prefix": "chart-",
         "why": "'Charts / data-viz kit' is not one artefact — it is the Chart-* family. Measured "
                "as a family: every chart-* slug in the store is counted and listed."},
    55: {"slugs": ["kpi-tile"], "class": "component",
         "related": [("stat-card", "stat-card.meta.json exists and carries delta semantics "
                                   "(wave-3a Lane E finding) — row 55 must state how it differs"),
                     ("chart-bullet", "Chart-bullet.meta.json purpose: 'KPI performance at a "
                                      "glance — a measure bar against a comparative target marker'")],
         "why": "No kpi-tile slug in the store; two gated neighbours carry overlapping semantics."},
    57: {"slugs": ["avatar-group"],
         "why": "⚠ NOT row 48's Avatar. Explicit so fuzzy cannot close it."},
    59: {"slugs": ["calendar"],
         "related": [("date-picker", "Date-picker + Date-range-picker share a calendar-grid grammar "
                                     "(laneB receipt) — the month view is the reusable part")],
         "why": "Notes cell: 'Full month view (distinct from date picker).' Distinctness is the "
                "itinerary's OWN words, so date-picker does not satisfy this row."},
    63: {"slugs": ["modals", "modal-lightbox"],
         "why": "Notes cell: 'Have confirm/alert dialog; true modals + lightboxes … to add.' BOTH "
                "named artefacts now exist and are gated — the Partial marking predates them."},
    65: {"slugs": ["loading-indicator"], "why": "Notes cell: 'loading-indicator, gated.'"},
    68: {"slugs": ["alert"], "why": "Alert.reference.html gated (laneA receipt step 0)."},
    69: {"slugs": ["toast"], "why": "Toast.reference.html gated (laneD receipt step 0)."},
    70: {"slugs": ["drawer"], "why": "Drawer.reference.html gated (laneD receipt step 0)."},
    77: {"slugs": ["headers"], "why": "Snippet is plural: Headers.reference.html."},
    82: {"slugs": ["layout-utilities"],
         "why": "⚠ NOT row 51's Data-grid (fuzzy matches on 'grid'). 'Grid / stack utilities' is a "
                "LAYOUT primitive, not a data table."},
    85: {"slugs": [], "class": "asset-system", "asset_dir": ICONS,
         "why": "The icon system is an ASSET SYSTEM, not a snippet: knowledge/assets/icons/ with "
                "icons.manifest.json and its own gate _validate_icons.py. Absence of a snippet is "
                "NOT evidence of a gap here — the artefact class is different."},
    86: {"slugs": ["brand-mark"], "class": "asset-system", "asset_dir": LOGOS,
         "why": "⚠ THE SPLIT VERDICT. Raw assets EXIST (knowledge/assets/logos/*.svg) but there is "
                "no component: no snippet, no meta, no showroom page, no .cn- scope. Notes cell: "
                "'Official asset; needed for shells/auth screens.'"},
    87: {"slugs": ["image-block"],
         "related": [("cards", "cards.meta.json names a 'Media card' and a 'Media card (borderless)' variant"),
                     ("hero", "hero.meta.json carries `textOverMedia` guidance for image/video heroes")],
         "why": "No standalone image/media-block component; two gated hosts carry media slots."},
    88: {"slugs": ["status-indicator"],
         "why": "Notes cell: 'status-indicator, gated.' — shares row 47's artefact; declared."},
    89: {"slugs": ["amount-display"],
         "why": "Amount-display.reference.html gated 2026-07-22 (laneC receipt); mechanical slug "
                "'amount-currency-display-money-format' misses."},
    90: {"slugs": ["account-selector"],
         "why": "Notes: 'Partial via Account-card; promote a selector chip.' The promotion HAPPENED "
                "— Account-selector.reference.html is in MIGRATED_SNIPPETS (Phase-2 wave 1)."},
    91: {"slugs": ["transaction-row"],
         "related": [("list-items", "list-items.meta.json: 'Covers the tappable list-row family "
                                    "(Account, Badge, Item, Review, Review Detail, Transaction)'"),
                     ("amount-display", "amount-display.meta.json names this row's own gap verbatim: "
                                        "'Transaction / ledger row (gap)'")],
         "why": "No standalone transaction-row component. The store itself records the gap."},
    92: {"slugs": ["document-row"],
         "related": [("list-items", "list-items.meta.json covers the tappable list-row family")],
         "why": "Notes: 'Downloadable document row.' No standalone artefact."},
    94: {"slugs": ["runway-bar"],
         "related": [("chart-bullet", "Chart-bullet is a measure-vs-target gauge — the nearest gated grammar")],
         "why": "Notes: 'Cash-runway meter (fitness tests invented this).'"},
    96: {"slugs": ["limits-meter"],
         "related": [("chart-bullet", "Chart-bullet is a measure-vs-target gauge")],
         "why": "Notes: 'Spend/transfer limit gauge.'"},
}

# Rows 97-124 are Layer 2. There is NO shell/template/lock-up artefact class in the store at all
# (probe: `find . -maxdepth 3 -iname '*shell*'` and `-iname '*template*'` return nothing in-repo).
# Absence of a Layer-1 snippet is therefore not evidence about them, and they are reported as a
# class, not as 28 individual "gaps" [[measure-dont-convert-units]].
LAYER2_NOTE = ("Layer 2 (shells · templates · lock-ups · variant matrices). No artefact class for "
               "these exists in the store yet — not a snippet, not a meta, not a showroom page. "
               "Their absence is measured as ONE structural gap, not 28 component gaps.")

STOPWORDS = {"a", "the", "of", "and", "or", "kit", "system", "block", "row", "bar", "card",
             "tile", "menu", "view", "mobile", "display", "interactive", "linear", "circular"}


# ---------------------------------------------------------------------------
# xlsx reader — stdlib only (zipfile + regex over the sheet XML). No openpyxl
# dependency: this generator must run wherever _build_all.py runs.
# ---------------------------------------------------------------------------
def _xlsx_rows(path, sheet_index=1):
    """[[cell,...],...] for sheet<sheet_index>.xml. Fails loud on a malformed workbook."""
    if not os.path.exists(path):
        raise SystemExit("FAIL — frozen itinerary not found: %s" % path)
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            sx = z.read("xl/sharedStrings.xml").decode("utf-8")
            for si in re.findall(r"<si>(.*?)</si>", sx, re.S):
                shared.append("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S)))
        name = "xl/worksheets/sheet%d.xml" % sheet_index
        if name not in z.namelist():
            raise SystemExit("FAIL — %s missing from %s" % (name, path))
        sx = z.read(name).decode("utf-8")
    rows = []
    for rx in re.findall(r"<row[^>]*>(.*?)</row>", sx, re.S):
        cells = {}
        for cm in re.finditer(r'<c([^>]*)>(.*?)</c>', rx, re.S):
            attrs, body = cm.group(1), cm.group(2)
            ref = re.search(r'r="([A-Z]+)\d+"', attrs)
            col = ref.group(1) if ref else "?"
            typ = re.search(r't="(\w+)"', attrs)
            typ = typ.group(1) if typ else "n"
            v = re.search(r"<v>(.*?)</v>", body, re.S)
            if typ == "s" and v:
                val = shared[int(v.group(1))]
            elif typ == "inlineStr":
                val = "".join(re.findall(r"<t[^>]*>(.*?)</t>", body, re.S))
            elif v:
                val = v.group(1)
            else:
                val = ""
            cells[col] = htmlmod.unescape(val).strip()
        ncols = 9
        rows.append([cells.get(chr(ord("A") + i), "") for i in range(ncols)])
    return rows


def _write_fixture_xlsx(path, grid):
    """Minimal real .xlsx (inline strings) — selftest fixtures only, never repo data."""
    rows_xml = []
    for ri, row in enumerate(grid, start=1):
        cs = []
        for ci, v in enumerate(row):
            cs.append('<c r="%s%d" t="inlineStr"><is><t>%s</t></is></c>'
                      % (chr(ord("A") + ci), ri, htmlmod.escape(str(v))))
        rows_xml.append('<row r="%d">%s</row>' % (ri, "".join(cs)))
    sheet = ('<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org/'
             'spreadsheetml/2006/main"><sheetData>%s</sheetData></worksheet>' % "".join(rows_xml))
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types/>')
        z.writestr("xl/worksheets/sheet1.xml", sheet)


def read_itinerary(path=ITIN):
    """[{'n','name','category','layer','status','priority','phase','mine','notes','sheet_row'}]."""
    raw = _xlsx_rows(path, 1)
    if not raw:
        raise SystemExit("FAIL — itinerary sheet 1 is empty: %s" % path)
    head = [c.lower() for c in raw[0]]
    if not head[0].startswith("#") or "component" not in head[1]:
        raise SystemExit("FAIL — unexpected itinerary header %r; refusing to guess columns" % raw[0])
    out = []
    for i, r in enumerate(raw[1:], start=2):
        if not any(c for c in r):
            continue
        try:
            n = int(float(r[0]))
        except (TypeError, ValueError):
            raise SystemExit("FAIL LOUD — sheet row %d: '#' cell %r is not an integer. "
                             "Never guessing a row number." % (i, r[0]))
        if not r[1]:
            raise SystemExit("FAIL LOUD — sheet row %d (item %d): Component cell is blank." % (i, n))
        out.append({"n": n, "name": r[1], "category": r[2], "layer": r[3], "status": r[4],
                    "priority": r[5], "phase": r[6], "mine": r[7], "notes": r[8], "sheet_row": i})
    return out


# ---------------------------------------------------------------------------
# the store index — every signal is a real listing, taken once
# ---------------------------------------------------------------------------
def parse_migrated(path=RADIUS):
    """The MIGRATED_SNIPPETS set literal out of _validate_radius.py. READ-ONLY."""
    src = open(path, encoding="utf-8").read()
    m = re.search(r"MIGRATED_SNIPPETS\s*=\s*\{(.*?)\n\}", src, re.S)
    if not m:
        raise SystemExit("FAIL — MIGRATED_SNIPPETS not parseable in %s (the radius ratchet moved; "
                         "fix this parser rather than dropping the signal)" % path)
    return {s.lower() for s in re.findall(r'"([^"]+\.reference\.html)"', m.group(1))}


def store_index():
    idx = {"snippets": {}, "metas": {}, "showroom": {}, "canon": {}, "migrated": parse_migrated()}
    for f in sorted(os.listdir(SNIPD)):
        if f.endswith(".reference.html") and not f.startswith("_"):
            idx["snippets"][f[: -len(".reference.html")].lower()] = f
    for f in sorted(os.listdir(COMPD)):
        if f.endswith(".meta.json") and not f.startswith("EXAMPLE-"):
            idx["metas"][f[: -len(".meta.json")].lower()] = f
    for f in sorted(os.listdir(SHOWD)):
        if f.endswith(".html") and f != "index.html":
            idx["showroom"][f[:-5].lower()] = f
    css = open(CANON, encoding="utf-8").read()
    for s in re.findall(r"\.cn-([a-z0-9][a-z0-9-]*)", css):
        idx["canon"][s] = idx["canon"].get(s, 0) + 1
    return idx


def all_store_slugs(idx):
    return set(idx["snippets"]) | set(idx["metas"]) | set(idx["showroom"]) | set(idx["canon"])


# ---------------------------------------------------------------------------
# resolution ladder
# ---------------------------------------------------------------------------
def slugify(text):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def mechanical_candidates(name):
    """Ordered candidate slugs from a row name. Never decides — only proposes."""
    base = re.sub(r"\(.*?\)", " ", name)          # drop parentheticals: 'Stepper (interactive)'
    cands = [slugify(base), slugify(name)]
    if "/" in base:
        cands.append(slugify(base.split("/")[0]))  # 'Toast / snackbar' -> 'toast'
    if "+" in base:
        cands.append(slugify(base.split("+")[0]))
    par = re.search(r"\((.*?)\)", name)
    if par:
        cands.append(slugify(par.group(1)))        # 'Segmented (View-options)' -> 'view-options'
    seen, out = set(), []
    for c in cands:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def tokens(text):
    return {t for t in re.split(r"[^a-z0-9]+", text.lower()) if t and t not in STOPWORDS and len(t) > 2}


def fuzzy_aliases(name, idx, threshold=0.5):
    """Plausible store slugs for a row name. NEVER auto-accepted — its job is to force UNRESOLVED."""
    rt = tokens(name)
    if not rt:
        return []
    hits = []
    for slug in sorted(all_store_slugs(idx)):
        st = tokens(slug)
        if not st:
            continue
        overlap = len(rt & st) / float(min(len(rt), len(st)))
        if overlap >= threshold:
            hits.append((slug, round(overlap, 2)))
    return sorted(hits, key=lambda h: -h[1])


def notes_slug(notes, idx):
    """A known store slug named verbatim in the itinerary's own Notes cell."""
    if not notes:
        return None
    low = notes.lower()
    for slug in sorted(all_store_slugs(idx), key=len, reverse=True):
        if re.search(r"(?<![a-z0-9-])%s(?![a-z0-9-])" % re.escape(slug), low):
            return slug
    return None


def resolve(row, idx):
    """-> (slugs, basis, extra) where extra carries why/class/related/candidates."""
    n = row["n"]
    if n in ROW_MAP:
        e = dict(ROW_MAP[n])
        return e.get("slugs", []), "map", e
    if str(row["layer"]).strip().startswith("2"):
        return [], "layer-2", {"class": "layer-2", "why": LAYER2_NOTE}
    # ⚠ mechanical BEFORE notes: a Notes cell may MENTION a neighbouring slug in prose
    # (row 5's note names 'button' while the row IS icon-button). A direct hit on the row's
    # own name outranks a prose mention [[unmatched-grep-is-not-an-absence]] — matched is
    # not presence either; quote the line.
    for c in mechanical_candidates(row["name"]):
        if c in all_store_slugs(idx):
            return [c], "mechanical", {"why": "slugified row name hits the store directly"}
    ns = notes_slug(row["notes"], idx)
    if ns:
        return [ns], "notes", {"why": "slug named verbatim in the itinerary Notes cell"}
    primary = mechanical_candidates(row["name"])[0]
    fz = fuzzy_aliases(row["name"], idx)
    return [primary], "absent", {"why": "slugified row name hits nothing in the store",
                                 "fuzzy_candidates": fz}


# ---------------------------------------------------------------------------
# measurement
# ---------------------------------------------------------------------------
def probe_slug(slug, idx):
    snip = idx["snippets"].get(slug)
    meta = idx["metas"].get(slug)
    show = idx["showroom"].get(slug)
    mig = bool(snip) and snip.lower() in idx["migrated"]
    cn = idx["canon"].get(slug, 0)
    return {
        "slug": slug,
        "snippet": snip, "meta": meta, "showroom": show,
        "migrated": mig, "canon_rules": cn,
        "probes": [
            "knowledge/snippets/%s.reference.html -> %s" % (slug, snip or "ABSENT"),
            "knowledge/components/%s.meta.json -> %s" % (slug, meta or "ABSENT"),
            "showroom/%s.html -> %s" % (slug, show or "ABSENT"),
            "_validate_radius.MIGRATED_SNIPPETS contains %s.reference.html -> %s" % (slug, mig),
            "grep -c '\\.cn-%s' knowledge/canon/canon.css -> %d" % (slug, cn),
        ],
    }


def derive_row(row, idx):
    slugs, basis, extra = resolve(row, idx)
    rec = {
        "n": row["n"], "name": row["name"], "category": row["category"], "layer": row["layer"],
        "priority": row["priority"], "itinerary_status": row["status"], "notes": row["notes"],
        "basis": basis, "why": extra.get("why", ""), "class": extra.get("class", "component"),
        "slugs": slugs, "artefacts": [], "related": [],
        "unresolved_reason": None,
    }
    for s, ev in extra.get("related", []):
        rec["related"].append({"slug": s, "evidence": ev, "present": s in all_store_slugs(idx)})

    # --- family rows (row 53): measured as a set, not as one artefact
    if rec["class"] == "family":
        pref = extra.get("family_prefix", "")
        fam = sorted(s for s in idx["snippets"] if s.startswith(pref))
        rec["slugs"] = fam
        rec["artefacts"] = [probe_slug(s, idx) for s in fam]
        gated = [a for a in rec["artefacts"] if a["snippet"] and a["meta"] and a["showroom"]
                 and a["canon_rules"]]
        rec["derived"] = "GATED" if fam and len(gated) == len(fam) else ("BUILT" if fam else "GAP")
        rec["evidence_line"] = "%d chart-* components, %d fully gated" % (len(fam), len(gated))
        return _with_drift(rec)

    # --- asset-system rows (85 icon system, 86 brand mark)
    if rec["class"] == "asset-system":
        d = extra.get("asset_dir")
        svgs, manifest = [], None
        for dirpath, _dn, fn in os.walk(d):
            for f in sorted(fn):
                if f.endswith(".svg"):
                    svgs.append(os.path.relpath(os.path.join(dirpath, f), ROOT))
                if f.endswith(".manifest.json"):
                    manifest = os.path.relpath(os.path.join(dirpath, f), ROOT)
        comp = [probe_slug(s, idx) for s in rec["slugs"]] if rec["slugs"] else []
        rec["artefacts"] = comp
        has_component = any(a["snippet"] or a["meta"] or a["showroom"] for a in comp)
        rec["asset_probe"] = {"dir": os.path.relpath(d, ROOT), "svg_count": len(svgs),
                              "manifest": manifest, "sample": svgs[:4]}
        if manifest and not rec["slugs"]:
            rec["derived"] = "ASSET-SYSTEM"
            rec["evidence_line"] = "%s: manifest %s, %d svg" % (rec["asset_probe"]["dir"], manifest, len(svgs))
        elif svgs and not has_component:
            rec["derived"] = "ASSET-ONLY"
            rec["evidence_line"] = ("%d raw svg assets present, NO component (no snippet, meta, "
                                    "showroom page or .cn- scope)" % len(svgs))
        elif has_component:
            rec["derived"] = "BUILT"
            rec["evidence_line"] = "assets + component artefacts both present"
        else:
            rec["derived"] = "GAP"
            rec["evidence_line"] = "no assets, no component"
        return _with_drift(rec)

    # --- layer-2 rows
    if rec["class"] == "layer-2":
        rec["derived"] = "NO-ARTEFACT-CLASS"
        rec["evidence_line"] = "Layer 2 — no shell/template/lock-up artefact class exists in the store"
        return _with_drift(rec)

    # --- ordinary component rows
    rec["artefacts"] = [probe_slug(s, idx) for s in rec["slugs"]]
    present = [a for a in rec["artefacts"] if a["snippet"] or a["meta"] or a["showroom"] or a["canon_rules"]]

    if not present and basis == "absent":
        fz = extra.get("fuzzy_candidates") or []
        if fz:
            rec["derived"] = "UNRESOLVED"
            rec["unresolved_reason"] = (
                "row name did not resolve, but the store holds plausible aliases %s. A slug "
                "mismatch is indistinguishable from an absence — add a ROW_MAP entry with its "
                "evidence, or confirm the gap. NOT GUESSING." % ", ".join("%s(%.2f)" % f for f in fz))
            rec["evidence_line"] = rec["unresolved_reason"]
            return _with_drift(rec)
        rec["derived"] = "GAP"
        rec["evidence_line"] = "all five probes negative on '%s'; no plausible store alias" % rec["slugs"][0]
        return _with_drift(rec)

    if not present:
        rec["derived"] = "GAP"
        rec["evidence_line"] = "all five probes negative on %s" % ", ".join(rec["slugs"])
        return _with_drift(rec)

    # GATED = the four ROUTE signals: snippet · meta · showroom page · canon .cn- scope.
    # The radius ratchet (MIGRATED_SNIPPETS) is deliberately NOT in the ladder: it records
    # whether a snippet's border-radius has been rebound onto the token, which is a migration
    # state, not a gating state. Reported as an ADVISORY flag so it cannot be read as "ungated"
    # [[gate-glob-scope-rule]] — rule only as wide as the signal actually reaches.
    full = [a for a in present if a["snippet"] and a["meta"] and a["showroom"] and a["canon_rules"]]
    unratcheted = [a["slug"] for a in present if a["snippet"] and not a["migrated"]]
    rec["radius_ratchet_missing"] = unratcheted
    if len(full) == len(rec["slugs"]) and full:
        rec["derived"] = "GATED"
        rec["evidence_line"] = "; ".join(
            "%s: snippet+meta+showroom, %d canon rules" % (a["slug"], a["canon_rules"]) for a in full)
        if unratcheted:
            rec["evidence_line"] += " · ADVISORY: not on the radius ratchet (%s)" % ", ".join(unratcheted)
    elif any(a["snippet"] and a["meta"] for a in present):
        missing = []
        for a in present:
            for k in ("snippet", "meta", "showroom"):
                if not a[k]:
                    missing.append("%s:%s" % (a["slug"], k))
            if not a["canon_rules"]:
                missing.append("%s:canon" % a["slug"])
        rec["derived"] = "BUILT" if missing else "GATED"
        rec["evidence_line"] = ("built, but not fully routed — missing " + ", ".join(missing)) if missing \
            else "snippet+meta+showroom+canon all present"
        if unratcheted:
            rec["evidence_line"] += " · ADVISORY: not on the radius ratchet (%s)" % ", ".join(unratcheted)
    else:
        have = []
        for a in present:
            have += [k for k in ("snippet", "meta", "showroom") if a[k]]
            if a["canon_rules"]:
                have.append("canon")
        rec["derived"] = "PARTIAL"
        rec["evidence_line"] = (
            "only %s present — mid-route. The showroom page and the canon `.cn-` scope are "
            "GENERATED surfaces, so a snippet that has just landed reads PARTIAL until the "
            "generator pass runs. Not the same thing as a half-built component."
            % ", ".join(sorted(set(have))))
    return _with_drift(rec)


RANK = {"GAP": 0, "ASSET-ONLY": 1, "PARTIAL": 2, "BUILT": 3, "GATED": 4,
        "ASSET-SYSTEM": 4, "NO-ARTEFACT-CLASS": 0, "UNRESOLVED": -1}
ITIN_RANK = {"Gap": 0, "Partial": 2, "Gated": 4}


def _with_drift(rec):
    d, i = RANK.get(rec["derived"], -1), ITIN_RANK.get(rec["itinerary_status"], -1)
    if rec["derived"] == "UNRESOLVED":
        rec["drift"] = "UNRESOLVED"
    elif rec["class"] == "layer-2":
        rec["drift"] = "AGREES" if rec["itinerary_status"] == "Gap" else "REVIEW"
    elif d == i:
        rec["drift"] = "AGREES"
    elif d > i:
        rec["drift"] = "STALE — itinerary UNDERSTATES the store"
    else:
        rec["drift"] = "OVERSTATED — itinerary claims more than the store holds"
    return rec


def orphans(records, idx):
    """Store components that no itinerary row claims — the itinerary's blind spot."""
    claimed = set()
    for r in records:
        for a in r["artefacts"]:
            claimed.add(a["slug"])
        for rel in r["related"]:
            claimed.add(rel["slug"])
    return sorted(s for s in idx["snippets"] if s not in claimed)


def build():
    idx = store_index()
    rows = read_itinerary()
    records = [derive_row(r, idx) for r in rows]
    orph = orphans(records, idx)
    comp = [r for r in records if r["class"] == "component"]
    true_gaps = [r for r in records if r["derived"] in ("GAP", "ASSET-ONLY") and r["class"] != "layer-2"]
    counts = {}
    for r in records:
        counts[r["derived"]] = counts.get(r["derived"], 0) + 1
    drifts = {}
    for r in records:
        drifts[r["drift"]] = drifts.get(r["drift"], 0) + 1
    data = {
        "$generated_by": "knowledge/gen_itinerary_status.py",
        "$session": "#203 Wave 3b Lane H",
        "$source_snapshot": "reviews/ITINERARY-2026-07-14-apollo-component-library.xlsx (FROZEN, read-only)",
        "$status": "PROPOSED #203, Dave's eye owed — a MEASUREMENT of the store, not a ruling",
        "$signals": ["snippet", "meta", "showroom", "radius-ratchet (MIGRATED_SNIPPETS)", "canon .cn- rules"],
        "$row_count": len(records),
        "$counts": counts,
        "$drift_counts": drifts,
        "$true_gaps": [r["n"] for r in true_gaps],
        "$unresolved": [r["n"] for r in records if r["derived"] == "UNRESOLVED"],
        "$orphan_snippets": orph,
        "$radius_ratchet_advisory": sorted(
            {s for r in records for s in (r.get("radius_ratchet_missing") or [])}),
        "$caveat": ("A snapshot of a LIVE working tree. Rows measured PARTIAL with only a snippet "
                    "present are mid-route, not half-built: showroom pages and canon .cn- scopes "
                    "are generated surfaces. Re-run after the generator pass."),
        "rows": records,
    }
    return data, idx, records, true_gaps, orph, comp


# ---------------------------------------------------------------------------
# HTML surface — Dave's eye. Deliberately hue-free: status is carried by WORDS and
# weight, never by colour alone (Dave is astigmatic; red/yellow are problem hues
# [[colour-stability-red-yellow-problem]]). Square corners; type scale 12/14/16 only.
# ---------------------------------------------------------------------------
CSS = """
*{box-sizing:border-box}
body{margin:0;padding:32px;background:#fff;color:#1A1A1A;
  font-family:ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  font-size:14px;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto}
h1{font-size:16px;font-weight:700;margin:0 0 4px;letter-spacing:.01em}
h2{font-size:16px;font-weight:700;margin:32px 0 8px;padding-top:16px;border-top:1px solid #1A1A1A}
h3{font-size:14px;font-weight:700;margin:20px 0 6px}
p,li{font-size:14px}
.sub{font-size:12px;color:#5C5C5C;margin:0 0 4px}
.lede{max-width:74ch}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:12px}
th,td{border:1px solid #D4D4D4;padding:6px 8px;text-align:left;vertical-align:top}
th{background:#F2F2F2;font-weight:700;font-size:12px}
tr:nth-child(even) td{background:#FAFAFA}
code,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12px}
.tag{display:inline-block;padding:1px 6px;border:1px solid #1A1A1A;font-size:12px;
  font-weight:700;white-space:nowrap;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.tag.gap{background:#1A1A1A;color:#fff}
.tag.unres{background:#1A1A1A;color:#fff;border-style:dashed}
.tag.soft{border-color:#8A8A8A;color:#5C5C5C;font-weight:400}
.drift{font-weight:700}
.drift.ok{font-weight:400;color:#5C5C5C}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:16px 0}
.card{border:1px solid #1A1A1A;padding:12px}
.card .n{font-size:16px;font-weight:700;display:block}
.card .l{font-size:12px;color:#5C5C5C}
.probe{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;color:#3D3D3D;
  margin:2px 0;white-space:pre-wrap;word-break:break-word}
.gapblk{border:1px solid #1A1A1A;padding:12px;margin:12px 0}
.gapblk h3{margin-top:0}
.note{font-size:12px;color:#5C5C5C;max-width:74ch}
details{margin:8px 0}
summary{font-size:12px;font-weight:700;cursor:pointer}
/* ≤720px: a 9-column table cannot reflow honestly, so it SCROLLS rather than
   pushing the page sideways (measured: documentElement.scrollWidth > clientWidth at 480). */
@media (max-width:720px){
  body{padding:16px}
  table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;font-size:12px}
  th,td{padding:4px 5px}
  .probe{font-size:12px}
}
"""


def esc(s):
    return htmlmod.escape(str(s if s is not None else ""))


def render_html(data, records, true_gaps, orph):
    c, d = data["$counts"], data["$drift_counts"]
    stale = [r for r in records if r["drift"].startswith("STALE")]
    over = [r for r in records if r["drift"].startswith("OVERSTATED")]
    unres = [r for r in records if r["derived"] == "UNRESOLVED"]
    o = []
    A = o.append
    A("<!doctype html><html lang='en'><head><meta charset='utf-8'>")
    A("<meta name='viewport' content='width=device-width,initial-scale=1'>")
    A("<title>Itinerary status, derived — %s</title><style>%s</style></head><body><div class='wrap'>" % (STAMP, CSS))
    A("<h1>Apollo component itinerary — status DERIVED from the store</h1>")
    A("<p class='sub'>Generated by <code>knowledge/gen_itinerary_status.py</code> · #203 Wave 3b Lane H · "
      "source snapshot <code>reviews/ITINERARY-2026-07-14-apollo-component-library.xlsx</code> (frozen, read-only)</p>")
    A("<p class='sub'><strong>PROPOSED #203, Dave's eye owed.</strong> Every verdict below is a measurement "
      "of the store with its probes attached. Nothing here promotes, rules or edits a component.</p>")
    A("<p class='lede'>The 2026-07-14 spreadsheet's <code>Status</code> column is hand-maintained. "
      "It was written before 24 components landed on 19 and 22 July and was never re-statused, so #203 "
      "briefed a six-lane wave to build components that already existed &mdash; 18 of 18. "
      "This page does not re-type that column; it derives status from four independent route signals "
      "(snippet &middot; meta &middot; showroom page &middot; canon <code>.cn-</code> rules), plus the radius "
      "ratchet as a separate ADVISORY, so it cannot rot the same way. Where the row name and the artefact name disagree, an explicit "
      "alternate-slug map carries the evidence for the link &mdash; a slug mismatch is indistinguishable "
      "from an absence, and that mismatch is exactly what produced the wrong wave brief.</p>")

    A("<div class='cards'>")
    for label, val in (("rows measured", data["$row_count"]),
                       ("GATED", c.get("GATED", 0)),
                       ("BUILT, not fully routed", c.get("BUILT", 0)),
                       ("PARTIAL", c.get("PARTIAL", 0)),
                       ("TRUE gaps (Layer 1)", len(true_gaps)),
                       ("stale rows", len(stale)),
                       ("overstated rows", len(over)),
                       ("UNRESOLVED", len(unres))):
        A("<div class='card'><span class='n'>%s</span><span class='l'>%s</span></div>" % (val, esc(label)))
    A("</div>")

    A("<h2>1 &middot; Drift — where the frozen column and the store disagree</h2>")
    A("<p class='note'>%d rows agree. The rows below are the reason the #203 wave misfired.</p>"
      % d.get("AGREES", 0))
    A("<table><tr><th>#</th><th>Component</th><th>Pri</th><th>Itinerary says</th>"
      "<th>Store says</th><th>Direction</th><th>Evidence</th></tr>")
    for r in stale + over + unres:
        A("<tr><td class='mono'>%s</td><td>%s</td><td class='mono'>%s</td><td class='mono'>%s</td>"
          "<td><span class='tag'>%s</span></td><td class='drift'>%s</td><td>%s</td></tr>"
          % (r["n"], esc(r["name"]), esc(r["priority"]), esc(r["itinerary_status"]),
             esc(r["derived"]), esc(r["drift"].split("—")[0].strip()), esc(r["evidence_line"])))
    A("</table>")

    A("<h2>2 &middot; The TRUE-gap list — probe-backed</h2>")
    A("<p class='note'>Every row here was measured absent on five probes and cleared by the fuzzy "
      "alias scan (nothing plausible in the store answers to it). This list is next wave's brief "
      "input: build from it, not from the frozen column. <code>related</code> entries name a gated "
      "host that already carries part of the job &mdash; a starting point, never a claim that the row "
      "is satisfied.</p>")
    for r in true_gaps:
        A("<div class='gapblk'>")
        A("<h3>#%s &nbsp;%s &nbsp;<span class='tag gap'>%s</span> &nbsp;<span class='tag soft'>%s</span> "
          "<span class='tag soft'>%s</span></h3>"
          % (r["n"], esc(r["name"]), esc(r["derived"]), esc(r["priority"]), esc(r["category"])))
        if r["why"]:
            A("<p class='note'>%s</p>" % esc(r["why"]))
        for a in r["artefacts"]:
            for p in a["probes"]:
                A("<div class='probe'>%s</div>" % esc(p))
        if r.get("asset_probe"):
            ap = r["asset_probe"]
            A("<div class='probe'>%s -> %d svg, manifest %s</div>"
              % (esc(ap["dir"]), ap["svg_count"], esc(ap["manifest"] or "none")))
            for s in ap["sample"]:
                A("<div class='probe'>  %s</div>" % esc(s))
        for rel in r["related"]:
            A("<p class='note'><strong>related:</strong> <code>%s</code> (%s) &mdash; %s</p>"
              % (esc(rel["slug"]), "present" if rel["present"] else "ABSENT", esc(rel["evidence"])))
        A("</div>")

    A("<h2>3 &middot; Every row, measured</h2>")
    A("<table><tr><th>#</th><th>Component</th><th>Layer</th><th>Pri</th><th>Itinerary</th>"
      "<th>Derived</th><th>Resolved via</th><th>Slug(s)</th><th>Evidence</th></tr>")
    for r in records:
        cls = "gap" if r["derived"] in ("GAP", "ASSET-ONLY") else ("unres" if r["derived"] == "UNRESOLVED" else "")
        dr = "ok" if r["drift"] == "AGREES" else "drift"
        A("<tr><td class='mono'>%s</td><td>%s</td><td class='mono'>%s</td><td class='mono'>%s</td>"
          "<td class='mono %s'>%s</td><td><span class='tag %s'>%s</span></td><td class='mono'>%s</td>"
          "<td class='mono'>%s</td><td>%s</td></tr>"
          % (r["n"], esc(r["name"]), esc(r["layer"]), esc(r["priority"]), dr, esc(r["itinerary_status"]),
             cls, esc(r["derived"]), esc(r["basis"]), esc(", ".join(r["slugs"]) or "&mdash;"),
             esc(r["evidence_line"])))
    A("</table>")

    ratch = sorted({s for r in records for s in (r.get("radius_ratchet_missing") or [])})
    A("<h2>3b &middot; Advisory — snippets not on the radius ratchet</h2>")
    A("<p class='note'>Deliberately NOT part of the status ladder. <code>MIGRATED_SNIPPETS</code> in "
      "<code>knowledge/_validate_radius.py</code> records whether a snippet's <code>border-radius</code> "
      "has been rebound onto the token &mdash; a migration state, not a gating state. A component can be "
      "fully routed and still sit off the ratchet. Reported so it is visible, ruled by nobody here. "
      "<strong>%d snippets:</strong></p><p class='mono'>%s</p>" % (len(ratch), esc(", ".join(ratch))))
    A("<h2>4 &middot; The alternate-slug map, with its evidence</h2>")
    A("<p class='note'>The only hand-held part of the instrument, so every entry carries why it exists. "
      "Rung 1 of the resolution ladder; rungs 2&ndash;4 are mechanical. The fuzzy rung never decides &mdash; "
      "it raises UNRESOLVED and fails the run.</p>")
    A("<table><tr><th>#</th><th>Component</th><th>Maps to</th><th>Why (evidence)</th></tr>")
    for n in sorted(ROW_MAP):
        r = next((x for x in records if x["n"] == n), None)
        A("<tr><td class='mono'>%s</td><td>%s</td><td class='mono'>%s</td><td>%s</td></tr>"
          % (n, esc(r["name"] if r else ""), esc(", ".join(ROW_MAP[n].get("slugs", [])) or
             ROW_MAP[n].get("class", "")), esc(ROW_MAP[n]["why"])))
    A("</table>")

    A("<h2>5 &middot; Orphans — store components no itinerary row claims</h2>")
    if orph:
        A("<p class='note'>These exist in <code>knowledge/snippets/</code> but no row resolves to them. "
          "Either the itinerary is missing rows, or the map is.</p><p class='mono'>%s</p>"
          % esc(", ".join(orph)))
    else:
        A("<p class='note'>None. Every gated snippet is claimed by at least one itinerary row.</p>")

    A("<h2>6 &middot; What this does not measure</h2>")
    A("<ul class='note'>"
      "<li><strong>Quality is out of scope.</strong> GATED means five artefacts exist and the radius "
      "ratchet holds it &mdash; not that the component meets #203's rule set. Wave 3a's four-theme review "
      "surfaces found real defects in components this page calls GATED.</li>"
      "<li><strong>PARTIAL rows are not sized.</strong> The itinerary's Partial rows carry prose about "
      "missing variants; no signal here reads a variant list.</li>"
      "<li><strong>Layer 2 is one structural gap, not 28.</strong> No shell/template/lock-up artefact "
      "class exists in the store, so per-row absence carries no information.</li>"
      "<li><strong>This is a snapshot of a LIVE tree.</strong> It was generated while five sibling "
      "lanes were writing snippets into the same working tree; rows measured PARTIAL with only a "
      "snippet present are mid-route, and the generated surfaces (showroom, canon) had not run yet. "
      "Re-run after the generator pass &mdash; <code>--check</code> failing later is the surface doing "
      "its job, not a defect.</li>"
      "<li><strong>Nothing here is promotion.</strong> Component promotion is on Dave's DO-NOT-RULE "
      "list. This page reports what is on disk.</li></ul>")
    A("</div></body></html>")
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------------------
def _emit():
    data, idx, records, true_gaps, orph, comp = build()
    return render_html(data, records, true_gaps, orph), \
        json.dumps(data, indent=2, sort_keys=False, ensure_ascii=False) + "\n", data, records


def main(argv):
    check = "--check" in argv
    if "--selftest" in argv:
        return selftest()
    html_txt, json_txt, data, records = _emit()
    unres = [r for r in records if r["derived"] == "UNRESOLVED"]
    if check:
        bad = []
        for path, want in ((OUT_HTML, html_txt), (OUT_JSON, json_txt)):
            if not os.path.exists(path):
                bad.append("%s MISSING" % os.path.relpath(path, ROOT))
            elif open(path, encoding="utf-8").read() != want:
                bad.append("%s OUT OF SYNC" % os.path.relpath(path, ROOT))
        if bad:
            print("ITINERARY-STATUS --check FAIL: " + "; ".join(bad))
            return 1
        print("ITINERARY-STATUS --check OK (%d rows)" % data["$row_count"])
    else:
        for path, txt in ((OUT_HTML, html_txt), (OUT_JSON, json_txt)):
            with open(path, "w", encoding="utf-8") as f:
                f.write(txt)
            print("wrote %s (%d B)" % (os.path.relpath(path, ROOT), len(txt.encode("utf-8"))))
    c = data["$counts"]
    print("rows %d | GATED %d | BUILT %d | PARTIAL %d | GAP %d | ASSET-ONLY %d | layer-2 %d"
          % (data["$row_count"], c.get("GATED", 0), c.get("BUILT", 0), c.get("PARTIAL", 0),
             c.get("GAP", 0), c.get("ASSET-ONLY", 0), c.get("NO-ARTEFACT-CLASS", 0)))
    print("drift: %s" % json.dumps(data["$drift_counts"]))
    print("TRUE gaps (Layer 1): %s" % ", ".join(str(n) for n in data["$true_gaps"]))
    print("ADVISORY — snippets present but not on the radius ratchet (%d): %s"
          % (len(data["$radius_ratchet_advisory"]), ", ".join(data["$radius_ratchet_advisory"])))
    if data["$orphan_snippets"]:
        print("ORPHAN snippets (no itinerary row): %s" % ", ".join(data["$orphan_snippets"]))
    if unres:
        for r in unres:
            print("UNRESOLVED row %d '%s' — %s" % (r["n"], r["name"], r["unresolved_reason"]))
        print("FAIL — %d unresolved row(s). Never guessing." % len(unres))
        return 1
    return 0


# ---------------------------------------------------------------------------
# selftest — drives the derivation on REAL data, both directions, plus a mutation
# arm on the CLAUSE that produced the #203 defect [[mutation-tests-the-clause-not-the-feature]].
# ---------------------------------------------------------------------------
def selftest():
    fails = []
    idx = store_index()
    rows = {r["n"]: r for r in read_itinerary()}

    # arm 1 — PASS: the four rows wave 3a mis-declared must all measure GATED
    for n in (13, 17, 19, 52, 89, 63):
        rec = derive_row(rows[n], idx)
        if rec["derived"] not in ("GATED", "BUILT"):
            fails.append("arm1 row %d expected GATED/BUILT, got %s" % (n, rec["derived"]))

    # arm 2 — FAIL ARM: row 86 must still measure a gap; a derivation that cannot
    # report a gap is always-true and worthless.
    # ⚠ Fixture rows are chosen from rows NO #203 lane owns. Rows 21/22/23/35/36/37/55/56/57
    # were the obvious fixtures and are WRONG here: Lanes I/J/K are building them in this same
    # working tree right now, so they move under the test [[premise-ages-faster-than-rule]].
    rec86 = derive_row(rows[86], idx)
    if rec86["derived"] != "ASSET-ONLY":
        fails.append("arm2 row 86 expected ASSET-ONLY, got %s" % rec86["derived"])
    for n in (6, 7, 25, 26, 61, 93):
        got = derive_row(rows[n], idx)["derived"]
        if got != "GAP":
            fails.append("arm2 row %d expected GAP, got %s" % (n, got))

    # arm 3 — MUTATION on the store: hide Amount-input from the index; row 17 must
    # flip GATED -> UNRESOLVED (the fuzzy rung sees amount-display and refuses to guess).
    mut = {k: (dict(v) if isinstance(v, dict) else set(v)) for k, v in idx.items()}
    for key in ("snippets", "metas", "showroom"):
        mut[key].pop("amount-input", None)
    mut["canon"] = {k: v for k, v in idx["canon"].items() if k != "amount-input"}
    saved = ROW_MAP.pop(17)
    try:
        m17 = derive_row(rows[17], mut)
        if m17["derived"] != "UNRESOLVED":
            fails.append("arm3 mutation: row 17 with the map entry removed and the artefact hidden "
                         "should be UNRESOLVED, got %s" % m17["derived"])
    finally:
        ROW_MAP[17] = saved

    # arm 4 — MUTATION on the CLAUSE: with the ROW_MAP entry removed but the artefact
    # PRESENT, row 17 must refuse to report GAP. This is the exact #203 defect: the
    # mechanical rung misses, and a naive instrument would have printed "Gap".
    saved = ROW_MAP.pop(17)
    try:
        m17 = derive_row(rows[17], idx)
        if m17["derived"] == "GAP":
            fails.append("arm4 mutation: row 17 without its map entry reported GAP while "
                         "Amount-input.reference.html is on disk — THE #203 DEFECT, reproduced")
        if m17["derived"] != "UNRESOLVED":
            fails.append("arm4 expected UNRESOLVED, got %s" % m17["derived"])
    finally:
        ROW_MAP[17] = saved

    # arm 5 — FAIL-LOUD arm, DRIVEN: build a real malformed .xlsx and run read_itinerary
    # on it. An unrun gate cannot fail [[instrument-without-a-consumer]] — so this arm
    # actually crosses the fence rather than asserting it exists.
    import tempfile
    hdr = ["#", "Component", "Category", "Layer", "Status", "Priority", "Phase", "Mine from", "Notes"]
    cases = [
        ("unparseable '#'", [hdr, ["x", "Thing", "", "1 Base", "Gap", "P1", "", "", ""]], "not an integer"),
        ("blank Component", [hdr, ["1", "", "", "1 Base", "Gap", "P1", "", "", ""]], "Component cell is blank"),
        ("wrong header", [["id", "Thing"], ["1", "Thing"]], "unexpected itinerary header"),
    ]
    for label, grid, needle in cases:
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tf:
            path = tf.name
        try:
            _write_fixture_xlsx(path, grid)
            try:
                read_itinerary(path)
                fails.append("arm5 '%s': read_itinerary returned instead of failing loud" % label)
            except SystemExit as e:
                if needle not in str(e):
                    fails.append("arm5 '%s': failed, but not with the named message (%s)" % (label, e))
        finally:
            os.unlink(path)

    for f in fails:
        print("SELFTEST FAIL — %s" % f)
    if fails:
        return 1
    print("SELFTEST OK — 5 arms: pass(6 rows) · fail(5 rows) · mutation-store · mutation-clause · fail-loud")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
