#!/usr/bin/env python3
"""_cut_harvest_rulings.py — THE CUT: Dave's exported harvest decisions -> PROPOSED rulings (#272).

⛔ THIS SCRIPT NEVER WRITES `knowledge/_rulings.json` AND NEVER WRITES A `components/*.meta.json`.
It emits PROPOSALS into an out directory and a review page. Inscription is a SEPARATE step that
Dave approves: `--inscribe` exists and REFUSES unless `--ratified` is also passed, and even then it
only prints the entries an operator must feed to `knowledge/_inscribe_ruling.py --write` by hand.
The lane that built this file never passed `--ratified`.

-----------------------------------------------------------------------------------------------
THE EXPORT SCHEMA — DERIVED FROM THE PAGE'S OWN CODE, NOT GUESSED
-----------------------------------------------------------------------------------------------
Source: `notes/_REVIEW-when-harvest-whole-library-2026-09-14-v2.html`, `exportObj()` (~line 1394)
and `doExport()` (~line 1403, `a.download = "harvest-decisions-2026-09-14.json"`).

    function exportObj(){
      var out={};
      Object.keys(state).sort().forEach(function(k){
        var r=state[k];
        out[k]={decision:r.decision||null,
                option_index:(r.option_index!=null?Number(r.option_index):null),
                notes:r.notes||"",
                at:r.at||null};
      });
      return out;
    }

So the exported FILE is a FLAT OBJECT keyed by row id (no wrapper):

    {
      "R-A-14": {"decision": "option", "option_index": 2, "notes": "…", "at": "2026-09-…Z"},
      "U-alert": {"decision": "ratify", "option_index": null, "notes": "", "at": "…"}
    }

  * key            — the row id, `tbody.row[data-rid]` on the sheet. Three families, and the
                     FAMILY IS THE SECTION (`data-sec`), NOT the id prefix — the 69 contested ids
                     come in three shapes because the three harvest lanes numbered independently:
                       sec-2  69 CONTESTED  ids `R-A-01`..`R-A-30` (lane A) · `B-01`..`B-24`
                              (lane B) · `R1`..`R16` (lane C). A prefix test misfiles all 24 of B.
                       sec-3  15 UNANIMOUS  ids `U-<component>`
                       sec-4  31 NO-SOURCE  ids `N-<component>` — declared guesses (#271)
                     These ids are EXACTLY the `id` / `component` keys of the harvest JSON.
  * decision       — "ratify" | "option" | "later" | "decline" | null   (`setDecision`, `statusOf`)
  * option_index   — Number 1..9 when decision=="option", else null     (`setDecision`, keys 1-9)
  * notes          — string, "" when empty. Dave's own words.           (`setNotes`)
  * at             — ISO-8601 string or null.

`statusOf()` on the page is the authority on what "decided" means:
    ratify | option  -> DECIDED          later -> later (undecided)
    decline          -> declined         absent/null -> open (undecided)
Only DECIDED rows are cut into proposed rulings. `later` / `decline` / `open` are LISTED.

The page's own `doImport()` accepts BOTH `{...}` and `{"decisions":{...},"at":…}` (the localStorage
shape under key `apollo-harvest-271-v2`). This loader accepts both for the same reason, and also
accepts a bare list of `{"rid":…, …}` objects, because a hand-assembled paste is a real input.

-----------------------------------------------------------------------------------------------
THE JOIN — where each row's substance comes from
-----------------------------------------------------------------------------------------------
  role / label / slice / section / flag : the SHEET's `tbody.row` data-attributes (115 rows).
  rule / components / positions(quotes) / why_contested / options / recommendation :
        `notes/_lanes/271/harvest/{A,B,C}/DECISION-TABLE.json` -> rows[] keyed by `id`  (R- rows).
  when_gate / when_prose / confidence / sources / disagreements / daves_call :
        `notes/_lanes/271/harvest/{A,B,C}/PROPOSED-WHEN.json` -> proposals[] keyed by `component`
        (U- and N- rows; the component is the row id with its 2-char prefix removed).

-----------------------------------------------------------------------------------------------
WHAT IT EMITS  (all under --out, default notes/_lanes/272/cut/)
-----------------------------------------------------------------------------------------------
  PROPOSED-RULINGS.json      one record per DECIDED non-unanimous (R-/N-) row.
                             `status` is "proposed" — NOT "ruled". Ids `s272-D<n>`, numbered by
                             ROLE (alphabetical, "—" last) then sheet row order.
                             `says`  = Dave's note VERBATIM. When the note is empty:
                                       "<decision label> — NOTE-ABSENT" and `note_absent: true`
                                       in the sidecar. A NOTE-ABSENT record can never be
                                       inscribed as his words; the sidecar says so.
                             `evidence` uses the legal `chat #272 — …` form
                                       (`knowledge/_governs.py`, CHAT_POINTER_RE, s148-D1).
                             `date` = the --date value, default 2026-09-15.
                             N- rows carry `guess_source: true` in the sidecar (no external source
                             was found for these 31 rows; #271 declared them guesses).
  PROPOSED-RULINGS-SIDECAR.json   per-id provenance the ruling record has no slot for:
                             source row id, role, slice, components, quotes, options, chosen
                             option text, note_absent / guess_source flags, quote-gate verdict.
  PROPOSED-WHEN-PATCH.json   {meta path -> {"when": "<gate> — <prose>", …}} for the UNANIMOUS
                             rows Dave RATIFIED in the export, in the s253-D1 single-string shape
                             (GATE — PROSE, split on the first em-dash; `knowledge/when-fields.json`
                             $grammar). NEVER APPLIED. The file is a proposal an operator diffs.
  QUOTE-GATE.json            every `says` run through `knowledge/_quote_gate.py` (ADVISORY).
  UNDECIDED.json             every row that is later / declined / open, with role and label.
  _REVIEW-cut-rulings-<date>.html   the review page.

Usage:
  python3 knowledge/_cut_harvest_rulings.py harvest-decisions-2026-09-14.json
  python3 knowledge/_cut_harvest_rulings.py export.json --out notes/_lanes/272/cut/
  python3 knowledge/_cut_harvest_rulings.py export.json --write        # write the out dir
  python3 knowledge/_cut_harvest_rulings.py --selftest
  python3 knowledge/_cut_harvest_rulings.py --make-synthetic /tmp/e.json
  python3 knowledge/_cut_harvest_rulings.py export.json --inscribe     # REFUSES (no --ratified)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse
import html as _html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SHEET = os.path.join(ROOT, "notes", "_REVIEW-when-harvest-whole-library-2026-09-14-v2.html")
HARVEST = os.path.join(ROOT, "notes", "_lanes", "271", "harvest")
TYPE_CSS = os.path.join(HERE, "canon", "type.css")
COMPONENTS = os.path.join(HERE, "components")
DEFAULT_OUT = os.path.join(ROOT, "notes", "_lanes", "272", "cut")
RULINGS = os.path.join(HERE, "_rulings.json")

SESSION = 272
DEFAULT_DATE = "2026-09-15"
NOTE_ABSENT = "NOTE-ABSENT"

# `statusOf()` on the sheet, transcribed. ratify|option => decided.
DECIDED = ("ratify", "option")
UNDECIDED_LABEL = {"later": "later", "decline": "declined", None: "open", "": "open"}

# Role ordering for the s272-D<n> numbering: alphabetical, with the sheet's "—" (no role) last.
NO_ROLE = "—"

# The row FAMILY is the sheet SECTION. The contested ids are three shapes (`R-A-01` lane A,
# `B-01` lane B, `R1` lane C) so the id prefix is NOT a family test.
SEC_FAMILY = {"sec-2": "R", "sec-3": "U", "sec-4": "N"}


class CutRefused(Exception):
    """The generator refuses to proceed. Nothing was written."""


# ---------------------------------------------------------------------------
# 1. THE SHEET — 115 rows, their attributes and their visible cells
# ---------------------------------------------------------------------------
_ROW_RE = re.compile(r'<tbody class="row[^"]*"([^>]*)>(.*?)</tbody>', re.S)
_ATTR_RE = re.compile(r'data-([a-z]+)="([^"]*)"')
_TAG_RE = re.compile(r"<[^>]+>")


def _detag(s):
    s = re.sub(r"<br\s*/?>", " · ", s)
    s = _TAG_RE.sub(" ", s)
    s = _html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def load_sheet(path=SHEET):
    """Row index from the decision sheet. Returns {rid: {...}} in DOCUMENT ORDER (dict keeps it)."""
    if not os.path.exists(path):
        raise CutRefused(f"⛔ REFUSED — the decision sheet is missing: {path}")
    raw = open(path, encoding="utf-8").read()
    rows, order = {}, 0
    for attrs, body in _ROW_RE.findall(raw):
        a = dict(_ATTR_RE.findall(attrs))
        rid = a.get("rid")
        if not rid:
            continue
        rows[rid] = {
            "rid": rid,
            "order": order,
            "role": a.get("role") or NO_ROLE,
            "label": _html.unescape(a.get("label", "")),
            "slice": a.get("slice", ""),
            "sec": a.get("sec", ""),
            "flag": a.get("flag") == "1",
            # The FAMILY is the SECTION, not the id prefix: the sheet's contested ids are three
            # different shapes (lane A `R-A-01`, lane B `B-01`, lane C `R1`), so a prefix test
            # would silently misfile the 24 lane-B rows. sec-2 contested · sec-3 unanimous ·
            # sec-4 no-source. Probe: `--selftest` arm0b asserts R=69 U=15 N=31.
            "family": SEC_FAMILY.get(a.get("sec", ""), "R"),
            "component": rid[2:] if rid[:2] in ("U-", "N-") else None,
            "cells": [_detag(c) for c in re.findall(r"<td\b[^>]*>(.*?)</td>", body, re.S)],
        }
        order += 1
    if not rows:
        raise CutRefused(f"⛔ REFUSED — no `tbody.row` found in {path}. The sheet's shape changed.")
    return rows


# ---------------------------------------------------------------------------
# 2. THE HARVEST — lane A/B/C source rows
# ---------------------------------------------------------------------------
def load_harvest(base=HARVEST):
    """-> (decisions {id: row}, proposals {component: proposal}). Both keyed as the sheet keys."""
    decisions, proposals = {}, {}
    for lane in ("A", "B", "C"):
        dt = os.path.join(base, lane, "DECISION-TABLE.json")
        pw = os.path.join(base, lane, "PROPOSED-WHEN.json")
        if os.path.exists(dt):
            for r in json.load(open(dt, encoding="utf-8")).get("rows", []):
                r = dict(r)
                r["_lane"] = lane
                decisions[r["id"]] = r
        if os.path.exists(pw):
            for p in json.load(open(pw, encoding="utf-8")).get("proposals", []):
                p = dict(p)
                p["_lane"] = lane
                proposals.setdefault(p["component"], p)
    if not decisions and not proposals:
        raise CutRefused(f"⛔ REFUSED — no harvest source under {base}.")
    return decisions, proposals


# ---------------------------------------------------------------------------
# 3. THE EXPORT
# ---------------------------------------------------------------------------
def load_export(path):
    """Accepts the three real shapes: the flat exportObj(), the {decisions:…} localStorage wrapper,
    and a list of {'rid':…} objects. Normalises to {rid: {decision, option_index, notes, at}}."""
    with open(path, encoding="utf-8") as fh:
        o = json.load(fh)
    if isinstance(o, list):
        o = {r["rid"]: r for r in o if isinstance(r, dict) and r.get("rid")}
    elif isinstance(o, dict) and isinstance(o.get("decisions"), dict):
        o = o["decisions"]
    if not isinstance(o, dict):
        raise CutRefused(f"⛔ REFUSED — {path} is not the export shape (flat object keyed by row id).")
    out = {}
    for rid, r in o.items():
        if not isinstance(r, dict):
            raise CutRefused(f"⛔ REFUSED — export entry {rid!r} is {type(r).__name__}, not an object.")
        oi = r.get("option_index")
        out[rid] = {
            "decision": r.get("decision") or None,
            "option_index": (int(oi) if oi not in (None, "") else None),
            "notes": (r.get("notes") or "").strip(),
            "at": r.get("at") or None,
        }
    return out


def status_of(rec):
    """`statusOf()` on the sheet, transcribed."""
    d = (rec or {}).get("decision")
    if d in DECIDED:
        return "decided"
    if d == "later":
        return "later"
    if d == "decline":
        return "declined"
    return "open"


# ---------------------------------------------------------------------------
# 4. THE CUT
# ---------------------------------------------------------------------------
def _role_key(role):
    return (1, "") if role == NO_ROLE else (0, role)


def _governs_for(row, drow, prop):
    """Non-empty list of repo paths the proposed ruling would govern. Only metas that EXIST."""
    comps = []
    if drow:
        comps = list(drow.get("components") or [])
    elif row.get("component"):
        comps = [row["component"]]
    paths = []
    for c in comps:
        p = os.path.join("knowledge", "components", f"{c}.meta.json")
        if os.path.exists(os.path.join(ROOT, p)):
            paths.append(p)
    if not paths:
        # Never invent. Fall back to the sheet itself, which is always a real artefact.
        paths = [os.path.relpath(SHEET, ROOT)]
    return paths


def _decision_label(rec, drow):
    d = rec["decision"]
    if d != "option":
        return d
    i = rec["option_index"]
    opts = (drow or {}).get("options") or []
    if i and 1 <= i <= len(opts):
        return f"option {i}"
    return f"option {i}" if i else "option"


def _chosen_option_text(rec, drow):
    if rec["decision"] != "option":
        return None
    i = rec["option_index"]
    opts = (drow or {}).get("options") or []
    if i and 1 <= i <= len(opts):
        return opts[i - 1]
    return None


def cut(export, rows, decisions, proposals, date=DEFAULT_DATE, session=SESSION):
    """-> dict with proposed_rulings, sidecar, when_patch, undecided, unknown_ids, counts."""
    unknown = sorted(k for k in export if k not in rows)

    decided, undecided = [], []
    for rid, row in rows.items():
        rec = export.get(rid)
        st = status_of(rec)
        if st == "decided":
            decided.append((rid, row, rec))
        elif rec is not None or True:
            undecided.append({
                "rid": rid, "role": row["role"], "label": row["label"],
                "family": row["family"], "status": st,
                "notes": (rec or {}).get("notes", ""),
            })

    # (b) one proposed ruling per DECIDED NON-UNANIMOUS row. U- rows are the `when` patch, not rulings.
    rulable = [t for t in decided if t[1]["family"] != "U"]
    rulable.sort(key=lambda t: (_role_key(t[1]["role"]), t[1]["order"]))

    rulings, sidecar = [], {}
    for n, (rid, row, rec) in enumerate(rulable, start=1):
        rid_out = f"s{session}-D{n}"
        drow = decisions.get(rid)
        prop = proposals.get(row.get("component") or "")
        label = _decision_label(rec, drow)
        note_absent = not rec["notes"]
        says = rec["notes"] if not note_absent else f"{label} — {NOTE_ABSENT}"
        chosen = _chosen_option_text(rec, drow)

        rule_text = (drow or {}).get("rule") or row["label"]
        if chosen:
            ruled = (f"{rule_text} — Dave chose {label}: {chosen}")
        else:
            ruled = (f"{rule_text} — Dave's decision on harvest row {rid}: {label}.")
        if row["family"] == "N":
            if prop and prop.get("when_gate"):
                ruled = (f"{rule_text} — the proposed `when` gate is: {prop['when_gate'].rstrip('.')}. "
                         f"Dave's decision on harvest row {rid}: {label}.")
            ruled += (" SOURCE: none found by the #271 harvest — this row is a DECLARED GUESS "
                      "(31 no-source rows), so the predicate is ours, not an imported one.")

        evidence = [
            f"chat #{session} — Dave's decision sheet export, row {rid}, decision \"{label}\"",
            os.path.relpath(SHEET, ROOT),
        ]
        src = os.path.join("notes", "_lanes", "271", "harvest", (drow or {}).get("_lane", ""),
                           "DECISION-TABLE.json") if drow else None
        if src and os.path.exists(os.path.join(ROOT, src)):
            evidence.append(src)

        rulings.append({
            "id": rid_out,
            "ruled": ruled,
            "date": date,
            "by": "Dave",
            "says": says,
            "governs": _governs_for(row, drow, prop),
            "evidence": evidence,
            "status": "proposed",
        })
        sidecar[rid_out] = {
            "source_row": rid,
            "role": row["role"],
            "slice": row["slice"],
            "family": row["family"],
            "label": row["label"],
            "decision": rec["decision"],
            "option_index": rec["option_index"],
            "chosen_option": chosen,
            "decided_at": rec["at"],
            "note_absent": note_absent,
            "guess_source": row["family"] == "N",
            "components": list((drow or {}).get("components") or ([row["component"]] if row.get("component") else [])),
            "quotes": (drow or {}).get("positions") or ((prop or {}).get("sources") and
                                                        {"sources": prop["sources"]}) or {},
            "why_contested": (drow or {}).get("why_contested"),
            "options": (drow or {}).get("options") or [],
            "lane_recommendation": (drow or {}).get("recommendation"),
            "when_gate": (prop or {}).get("when_gate"),
            "when_prose": (prop or {}).get("when_prose"),
            "confidence": (prop or {}).get("confidence"),
            "quote_gate": None,   # filled by run_quote_gate()
        }

    # (c) the UNANIMOUS rows Dave RATIFIED -> proposed `when` predicates, s253-D1 shape.
    when_patch, when_skipped = {}, []
    for rid, row, rec in decided:
        if row["family"] != "U":
            continue
        comp = row["component"]
        prop = proposals.get(comp)
        if not prop or not prop.get("when_gate"):
            when_skipped.append({"rid": rid, "why": "no when_gate in the #271 PROPOSED-WHEN"})
            continue
        rel = os.path.join("knowledge", "components", f"{comp}.meta.json")
        if not os.path.exists(os.path.join(ROOT, rel)):
            when_skipped.append({"rid": rid, "why": f"no meta at {rel}"})
            continue
        gate = prop["when_gate"].strip().rstrip(".")
        prose = (prop.get("when_prose") or "").strip()
        # s253-D1 / when-fields.json $grammar: ONE string, GATE — PROSE, split on the FIRST em-dash.
        value = f"{gate} — {prose}" if prose else gate
        existing = None
        try:
            existing = json.load(open(os.path.join(ROOT, rel), encoding="utf-8")).get("when")
        except Exception:
            pass
        when_patch[rel] = {
            "when": value,
            "_source_row": rid,
            "_component": comp,
            "_confidence": prop.get("confidence"),
            "_daves_note": rec["notes"],
            "_existing_when": existing,
            "_replaces_existing": existing is not None and existing != value,
            "_NOT_APPLIED": True,
        }

    counts = {
        "sheet_rows": len(rows),
        "export_entries": len(export),
        "unknown_export_ids": len(unknown),
        "decided": len(decided),
        "decided_rulable": len(rulable),
        "proposed_rulings": len(rulings),
        "note_absent": sum(1 for v in sidecar.values() if v["note_absent"]),
        "guess_source": sum(1 for v in sidecar.values() if v["guess_source"]),
        "unanimous_ratified": sum(1 for _, r, _ in decided if r["family"] == "U"),
        "when_patch": len(when_patch),
        "when_skipped": len(when_skipped),
        "undecided": len(undecided),
    }
    for st in ("later", "declined", "open"):
        counts[f"undecided_{st}"] = sum(1 for u in undecided if u["status"] == st)
    return {
        "$description": (f"#{session} PROPOSED rulings cut from Dave's harvest decision export. "
                         "NOTHING INSCRIBED. status is 'proposed', not 'ruled'."),
        "$date": date, "$session": session,
        "counts": counts,
        "unknown_export_ids": unknown,
        "proposed_rulings": rulings,
        "sidecar": sidecar,
        "when_patch": when_patch,
        "when_skipped": when_skipped,
        "undecided": sorted(undecided, key=lambda u: (_role_key(u["role"]), u["rid"])),
    }


# ---------------------------------------------------------------------------
# 5. THE QUOTE DOOR — every `says` through _quote_gate.py (ADVISORY, #269)
# ---------------------------------------------------------------------------
def run_quote_gate(result, enabled=True):
    """Fills sidecar[*]['quote_gate'] and returns the report dict. Never raises: the door is
    ADVISORY by ruling shape, so a gate that cannot run is DECLARED, not swallowed."""
    rep = {"$marker": "QUOTE-GATE ADVISORY", "ran": False, "why": None,
           "checked": 0, "found": 0, "misses": [], "skipped_short": [], "note_absent": []}
    if not enabled:
        rep["why"] = "--no-quote-gate was passed"
        return rep
    phrases, ids = [], []
    for r in result["proposed_rulings"]:
        sc = result["sidecar"][r["id"]]
        if sc["note_absent"]:
            sc["quote_gate"] = {"verdict": "note-absent", "found": False}
            rep["note_absent"].append(r["id"])
            continue
        if len(r["says"].split()) < 4:          # _quote_gate.MIN_WORDS
            sc["quote_gate"] = {"verdict": "too-short-to-check", "found": False}
            rep["skipped_short"].append({"id": r["id"], "says": r["says"]})
            continue
        phrases.append(r["says"])
        ids.append(r["id"])
    if not phrases:
        rep["why"] = "no `says` long enough to check"
        return rep
    gate = os.path.join(HERE, "_quote_gate.py")
    try:
        p = subprocess.run([sys.executable, gate] + phrases + ["--json"],
                           capture_output=True, text=True, cwd=ROOT, timeout=900)
        data = json.loads(p.stdout)
    except Exception as ex:                      # noqa: BLE001 - advisory door, declare and go on
        rep["why"] = f"could not run {gate}: {ex}"
        for i in ids:
            result["sidecar"][i]["quote_gate"] = {"verdict": "gate-did-not-run", "found": False}
        return rep
    results = data.get("results", data if isinstance(data, list) else [])
    rep["ran"] = True
    rep["checked"] = len(results)
    for rid_out, res in zip(ids, results):
        found = bool(res.get("found"))
        v = {"verdict": "found" if found else "NOT-FOUND", "found": found}
        if res.get("spelling_corrected"):
            v["spelling_corrected"] = res["spelling_corrected"]
            v["verdict"] = "found (spelling-corrected)"
        if res.get("records"):
            v["records"] = res["records"][:2]
        if res.get("nearest"):
            v["nearest"] = res["nearest"]
        result["sidecar"][rid_out]["quote_gate"] = v
        if found:
            rep["found"] += 1
        else:
            rep["misses"].append({"id": rid_out, "says": res.get("phrase"),
                                  "nearest": res.get("nearest")})
    return rep


# ---------------------------------------------------------------------------
# 6. THE REVIEW PAGE
# ---------------------------------------------------------------------------
def _e(s):
    return _html.escape("" if s is None else str(s), quote=True)


def _type_css():
    try:
        return open(TYPE_CSS, encoding="utf-8").read()
    except Exception:
        return "/* knowledge/canon/type.css NOT FOUND — declared, not faked */"


PAGE_CSS = """
:root{--accent:#DA1A00;--black:#000;--white:#fff;--grey-1:#F3F3F3;--grey-2:#EDEDED;
      --grey-3:#D7D8D6;--grey-5:#9B9B9B;--grey-6:#767676;--grey-7:#545454;--grey-8:#333;
      --s1:4px;--s2:8px;--s3:16px;--s4:24px;--s5:32px;--s6:48px;--s7:64px}
@media (prefers-color-scheme: dark){
  :root{--accent:#F6604C;--black:#fff;--white:#1A1A1A;--grey-1:#242424;--grey-2:#333;
        --grey-3:#454545;--grey-5:#8C8C8C;--grey-6:#A8A8A8;--grey-7:#C6C6C6;--grey-8:#E4E4E4}}
*{box-sizing:border-box}
html,body{margin:0;padding:0;max-width:100%;overflow-x:hidden}
body{background:var(--white);color:var(--black);font-family:var(--uf);font-size:16px;
     line-height:24px;font-weight:400;-webkit-font-smoothing:antialiased}
main{max-width:1160px;margin:0 auto;padding:var(--s5) var(--s4) var(--s7)}
header.top{border-bottom:2px solid var(--black);padding-bottom:var(--s4);margin-bottom:var(--s5)}
.kicker{font-size:12px;line-height:16px;letter-spacing:.08em;text-transform:uppercase;
        color:var(--accent);font-weight:500;margin:0 0 var(--s2)}
h1{font-size:40px;line-height:48px;font-weight:300;margin:0 0 var(--s3);letter-spacing:-.01em}
h2{font-size:24px;line-height:32px;font-weight:400;margin:var(--s6) 0 var(--s3);
   padding-bottom:var(--s2);border-bottom:1px solid var(--grey-3)}
h3{font-size:18px;line-height:26px;font-weight:500;margin:var(--s5) 0 var(--s3);
   text-transform:uppercase;letter-spacing:.06em}
p{margin:0 0 var(--s3);max-width:74ch}
.warn{border-left:2px solid var(--accent);background:var(--grey-1);padding:var(--s3);
      margin:0 0 var(--s4);font-weight:500}
.counts{display:grid;grid-template-columns:repeat(auto-fit,minmax(132px,1fr));gap:1px;
        background:var(--grey-3);border:1px solid var(--grey-3);margin:0 0 var(--s4)}
.counts div{background:var(--white);padding:var(--s3)}
.counts b{display:block;font-size:32px;line-height:38px;font-weight:300}
.counts span{display:block;font-size:11px;line-height:15px;letter-spacing:.06em;
             text-transform:uppercase;color:var(--grey-6);margin-top:var(--s1)}
.card{border-top:1px solid var(--grey-3);padding:var(--s4) 0}
.card:first-of-type{border-top:2px solid var(--black)}
.cid{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;font-weight:600;
     color:var(--accent)}
.crule{font-size:19px;line-height:27px;font-weight:400;margin:var(--s2) 0 var(--s3)}
.tags{margin:0 0 var(--s3)}
.tag{display:inline-block;font-size:11px;line-height:16px;letter-spacing:.05em;
     text-transform:uppercase;border:1px solid var(--grey-3);color:var(--grey-7);
     padding:1px 6px;margin:0 var(--s1) var(--s1) 0}
.tag.red{border-color:var(--accent);color:var(--accent);font-weight:500}
.two{display:grid;grid-template-columns:1fr 1fr;gap:var(--s4)}
.pane{min-width:0}
.plab{font-size:11px;line-height:15px;letter-spacing:.08em;text-transform:uppercase;
      color:var(--grey-6);border-bottom:1px solid var(--grey-3);padding-bottom:var(--s1);
      margin:0 0 var(--s2)}
.q{margin:0 0 var(--s2);font-size:14px;line-height:20px;overflow-wrap:anywhere}
.q b{font-weight:500;color:var(--grey-7)}
.says{background:var(--grey-1);border-left:2px solid var(--black);padding:var(--s3);
      font-size:16px;line-height:24px;overflow-wrap:anywhere}
.says.absent{border-left-color:var(--accent);color:var(--accent)}
.sub{font-size:12px;line-height:17px;color:var(--grey-6);margin-top:var(--s2)}
/* inline, NOT inline-block: inline-block leaves a visible gap before a following full stop
   and breaks the baseline inside a sentence (seen at 1280 on the first render). */
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;background:var(--grey-1);
     padding:1px 4px;overflow-wrap:anywhere;word-break:break-word;max-width:100%}
.tblwrap{overflow-x:auto;max-width:100%;margin:0 0 var(--s4)}
table{border-collapse:collapse;width:100%;font-size:14px;line-height:20px}
th,td{text-align:left;vertical-align:top;padding:var(--s2) var(--s3) var(--s2) 0;
      border-bottom:1px solid var(--grey-3)}
th{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--grey-6);
   border-bottom:1px solid var(--black);font-weight:500}
footer{margin-top:var(--s7);border-top:2px solid var(--black);padding-top:var(--s4);
       font-size:13px;line-height:19px;color:var(--grey-7)}
@media (max-width:780px){
  main{padding:var(--s4) var(--s3) var(--s6)}
  h1{font-size:28px;line-height:36px}
  .two{grid-template-columns:1fr;gap:var(--s3)}
  .counts{grid-template-columns:repeat(2,1fr)}
  .counts b{font-size:26px;line-height:32px}
}
"""


def render_page(result, qrep, export_path, date=DEFAULT_DATE, session=SESSION):
    c = result["counts"]
    sidecar = result["sidecar"]
    by_role = {}
    for r in result["proposed_rulings"]:
        by_role.setdefault(sidecar[r["id"]]["role"], []).append(r)

    P = []
    P.append("<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">")
    P.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    P.append(f"<title>#{session} the cut — proposed rulings from Dave's harvest decisions</title>")
    P.append("<style>\n/* ===== knowledge/canon/type.css — baked in verbatim ===== */\n")
    P.append(_type_css())
    P.append("\n/* ===== page ===== */\n")
    P.append(PAGE_CSS)
    P.append("</style></head><body><main>")

    P.append('<header class="top">')
    P.append(f'<p class="kicker">#{session} · {_e(date)} · the cut</p>')
    P.append("<h1>Proposed rulings from your harvest decisions</h1>")
    P.append('<div class="warn">NOTHING IS INSCRIBED. Every record below is <code>status: '
             '&quot;proposed&quot;</code>. No <code>knowledge/_rulings.json</code> entry, no '
             '<code>components/*.meta.json</code> field and no gate was touched by the generator '
             "that made this page. The <code>when</code> predicates for the unanimous rows are a "
             "proposed-patch FILE, not an edit.</div>")
    P.append('<div class="counts">')
    for k, lab in (("proposed_rulings", "proposed rulings"),
                   ("decided", "rows you decided"),
                   ("unanimous_ratified", "unanimous ratified"),
                   ("when_patch", "when predicates proposed"),
                   ("note_absent", "no note (NOTE-ABSENT)"),
                   ("guess_source", "guess-source rows"),
                   ("undecided", "undecided"),
                   ("sheet_rows", "rows on the sheet")):
        P.append(f'<div><b>{c.get(k, 0)}</b><span>{lab}</span></div>')
    P.append("</div>")
    qline = ("did not run — " + str(qrep.get("why"))) if not qrep.get("ran") else (
        f"{qrep['found']} of {qrep['checked']} of your notes found verbatim in the record; "
        f"{len(qrep['misses'])} not found")
    P.append(f'<p class="sub">Export: <code>{_e(os.path.basename(export_path))}</code> · '
             f'source sheet: <code>{_e(os.path.relpath(SHEET, ROOT))}</code> · '
             f'quote gate (ADVISORY): {_e(qline)}.</p>')
    P.append("</header>")

    if result["unknown_export_ids"]:
        P.append('<div class="warn">'
                 f'{len(result["unknown_export_ids"])} exported id(s) match no row on the sheet and '
                 f'were IGNORED: <code>{_e(", ".join(result["unknown_export_ids"][:20]))}</code></div>')

    # --- the proposed rulings, by role -------------------------------------
    P.append("<h2>Proposed rulings, by role</h2>")
    if not result["proposed_rulings"]:
        P.append("<p>No decided non-unanimous row in this export, so nothing was cut.</p>")
    for role in sorted(by_role, key=_role_key):
        P.append(f'<h3>{_e("no role" if role == NO_ROLE else role)} '
                 f'· {len(by_role[role])}</h3>')
        for r in by_role[role]:
            sc = sidecar[r["id"]]
            P.append('<div class="card">')
            P.append(f'<span class="cid">{_e(r["id"])}</span> '
                     f'<code>{_e(sc["source_row"])}</code>')
            P.append(f'<p class="crule">{_e(r["ruled"])}</p>')
            P.append('<p class="tags">')
            dec = sc["decision"] + (f" {sc['option_index']}" if sc["option_index"] else "")
            P.append(f'<span class="tag">{_e(dec)}</span>')
            if sc["slice"]:
                P.append(f'<span class="tag">slice {_e(sc["slice"])}</span>')
            for comp in sc["components"][:6]:
                P.append(f'<span class="tag">{_e(comp)}</span>')
            if sc["guess_source"]:
                P.append('<span class="tag red">guess-source</span>')
            if sc["note_absent"]:
                P.append(f'<span class="tag red">{NOTE_ABSENT}</span>')
            qg = sc.get("quote_gate") or {}
            if qg.get("verdict") == "NOT-FOUND":
                P.append('<span class="tag red">quote gate: not found</span>')
            elif qg.get("verdict", "").startswith("found"):
                P.append(f'<span class="tag">quote gate: {_e(qg["verdict"])}</span>')
            P.append("</p>")

            P.append('<div class="two">')
            P.append('<div class="pane"><p class="plab">what the systems said — verbatim</p>')
            quotes = sc.get("quotes") or {}
            if isinstance(quotes, dict) and "sources" in quotes:
                P.append('<p class="q">' + " · ".join(_e(s) for s in quotes["sources"]) + "</p>")
            elif isinstance(quotes, dict) and quotes:
                for sys_name, q in list(quotes.items())[:12]:
                    P.append(f'<p class="q"><b>{_e(sys_name)}</b> — {_e(q)}</p>')
            else:
                P.append('<p class="q">no source found — declared guess (#271).</p>')
            if sc.get("why_contested"):
                P.append(f'<p class="sub">{_e(sc["why_contested"])}</p>')
            P.append("</div>")

            P.append('<div class="pane"><p class="plab">your note — verbatim, the <code>says</code></p>')
            cls = "says absent" if sc["note_absent"] else "says"
            P.append(f'<div class="{cls}">{_e(r["says"])}</div>')
            if sc.get("chosen_option"):
                P.append(f'<p class="sub"><b>Option {sc["option_index"]}:</b> {_e(sc["chosen_option"])}</p>')
            if sc["note_absent"]:
                P.append('<p class="sub">You decided this row but left no note, so the '
                         '<code>says</code> is a MARKER, not your words. It cannot be inscribed as '
                         "a quote until you give one.</p>")
            if qg.get("nearest"):
                P.append(f'<p class="sub">quote gate nearest: <code>{_e(qg["nearest"].get("id"))}</code> '
                         f'· shared bigrams {_e(qg["nearest"].get("shared_bigrams"))}</p>')
            P.append(f'<p class="sub">governs: <code>{_e(" · ".join(r["governs"]))}</code></p>')
            P.append(f'<p class="sub">evidence: {_e(r["evidence"][0])}</p>')
            P.append("</div></div></div>")

    # --- the when patch -----------------------------------------------------
    P.append("<h2>Proposed <code>when</code> predicates — the unanimous rows you ratified</h2>")
    P.append("<p>s253-D1 shape: one string, <b>GATE — PROSE</b>, split on the first em-dash. "
             "Written to <code>PROPOSED-WHEN-PATCH.json</code> only. "
             "<b>No meta was touched.</b></p>")
    if not result["when_patch"]:
        P.append("<p>No unanimous row was ratified in this export, so no predicate was proposed.</p>")
    else:
        P.append('<div class="tblwrap"><table><thead><tr><th>meta</th><th>row</th>'
                 '<th>proposed <code>when</code></th><th>replaces?</th></tr></thead><tbody>')
        for path, v in sorted(result["when_patch"].items()):
            P.append(f'<tr><td><code>{_e(path)}</code></td><td><code>{_e(v["_source_row"])}</code>'
                     f'<br><span class="sub">{_e(v.get("_confidence"))}</span></td>'
                     f'<td>{_e(v["when"])}</td>'
                     f'<td>{"YES — an existing when would be overwritten" if v["_replaces_existing"] else "no"}</td></tr>')
        P.append("</tbody></table></div>")
    if result["when_skipped"]:
        P.append('<p class="sub">Skipped: ' +
                 _e("; ".join(f'{s["rid"]} ({s["why"]})' for s in result["when_skipped"])) + "</p>")

    # --- undecided ----------------------------------------------------------
    P.append("<h2>Not ruled — still yours</h2>")
    P.append(f'<p>{c["undecided"]} rows carry no decision that cuts a ruling: '
             f'{c.get("undecided_open", 0)} open, {c.get("undecided_later", 0)} later, '
             f'{c.get("undecided_declined", 0)} declined. Nothing below was ruled, guessed or '
             "assumed.</p>")
    P.append('<div class="tblwrap"><table><thead><tr><th>row</th><th>role</th><th>status</th>'
             "<th>rule</th></tr></thead><tbody>")
    for u in result["undecided"]:
        P.append(f'<tr><td><code>{_e(u["rid"])}</code></td>'
                 f'<td>{_e("—" if u["role"] == NO_ROLE else u["role"])}</td>'
                 f'<td>{_e(u["status"])}</td><td>{_e(u["label"])}</td></tr>')
    P.append("</tbody></table></div>")

    P.append("<footer><p><b>How this page was made.</b> "
             f"<code>knowledge/_cut_harvest_rulings.py {_e(os.path.basename(export_path))}</code>. "
             "It joins your export to the #271 harvest rows and emits proposals. It never writes "
             "<code>knowledge/_rulings.json</code>; its <code>--inscribe</code> arm refuses unless "
             "<code>--ratified</code> is passed, and the lane that built it never passed it. "
             "Quotes are the #271 harvest's verbatim spans, capped under 15 words by "
             "<code>knowledge/_RUNBOOK-external-claims.md</code>.</p></footer>")
    P.append("</main></body></html>")
    return "\n".join(P)


# ---------------------------------------------------------------------------
# 7. THE SYNTHETIC EXPORT — the sheet's own model, for the selftest and the drive
# ---------------------------------------------------------------------------
# A phrase that IS in the Memento corpus, so the quote gate has a positive control and the
# mutation arm has something to break. Probed 2026-09-15: found in 3 records.
REAL_QUOTE = "180 was decided because we use a sub for the wrap"


def make_synthetic(rows, decisions, proposals, at="2026-09-15T09:00:00.000Z"):
    """3 decided non-unanimous + 1 unanimous ratified + 1 undecided, all REAL row ids."""
    R = [r for r in rows.values() if r["family"] == "R"]
    N = [r for r in rows.values() if r["family"] == "N"]
    U = [r for r in rows.values() if r["family"] == "U" and proposals.get(r["component"], {}).get("when_gate")]
    L = [r for r in rows.values() if r["family"] == "R"]
    if len(R) < 3 or not N or not U:
        raise CutRefused("⛔ REFUSED — the sheet does not carry the three row families.")
    # pick an R row whose DECISION-TABLE entry has >= 2 options, so `option 2` resolves to real text
    opt_row = next((r for r in R if len(decisions.get(r["rid"], {}).get("options") or []) >= 2), R[0])
    others = [r for r in R if r["rid"] != opt_row["rid"]]
    e = {
        opt_row["rid"]: {"decision": "option", "option_index": 2, "notes": REAL_QUOTE, "at": at},
        others[0]["rid"]: {"decision": "ratify", "option_index": None,
                           "notes": "yes do that one, it is the only one a gate can check", "at": at},
        N[0]["rid"]: {"decision": "ratify", "option_index": None, "notes": "", "at": at},  # NOTE-ABSENT + guess-source
        U[0]["rid"]: {"decision": "ratify", "option_index": None, "notes": "fine", "at": at},
        others[1]["rid"]: {"decision": "later", "option_index": None, "notes": "come back to this", "at": at},
    }
    return e


# ---------------------------------------------------------------------------
# 8. WRITE
# ---------------------------------------------------------------------------
def _dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return path


def write_out(result, qrep, out_dir, export_path, date=DEFAULT_DATE, session=SESSION):
    written = []
    written.append(_dump(os.path.join(out_dir, "PROPOSED-RULINGS.json"), {
        "$description": result["$description"],
        "$WARNING": "status is 'proposed'. Inscription is a separate step Dave approves.",
        "$date": date, "$session": session, "$export": os.path.basename(export_path),
        "counts": result["counts"],
        "rulings": result["proposed_rulings"],
    }))
    written.append(_dump(os.path.join(out_dir, "PROPOSED-RULINGS-SIDECAR.json"), {
        "$description": "per-proposed-id provenance the ruling record has no slot for.",
        "sidecar": result["sidecar"], "unknown_export_ids": result["unknown_export_ids"],
    }))
    written.append(_dump(os.path.join(out_dir, "PROPOSED-WHEN-PATCH.json"), {
        "$description": ("PROPOSED `when` additions for the UNANIMOUS rows Dave ratified. "
                         "s253-D1 shape (GATE — PROSE, one string). NEVER APPLIED by this script."),
        "$shape": "meta path -> {when, _source_row, _component, _confidence, _existing_when, ...}",
        "$date": date, "$session": session,
        "patch": result["when_patch"], "skipped": result["when_skipped"],
    }))
    written.append(_dump(os.path.join(out_dir, "QUOTE-GATE.json"), qrep))
    written.append(_dump(os.path.join(out_dir, "UNDECIDED.json"), {
        "$description": "rows with no decision that cuts a ruling. LISTED, NOT RULED.",
        "counts": {k: v for k, v in result["counts"].items() if k.startswith("undecided")},
        "rows": result["undecided"],
    }))
    page = os.path.join(out_dir, f"_REVIEW-cut-rulings-{date}.html")
    os.makedirs(out_dir, exist_ok=True)
    with open(page, "w", encoding="utf-8") as fh:
        fh.write(render_page(result, qrep, export_path, date=date, session=session))
    written.append(page)
    return written


# ---------------------------------------------------------------------------
# 9. THE INSCRIPTION DOOR — refuses
# ---------------------------------------------------------------------------
def inscribe(result, ratified=False):
    """⛔ There is no path through this function that writes _rulings.json. --ratified only
    unlocks PRINTING the entries for an operator to feed to _inscribe_ruling.py by hand."""
    if not ratified:
        raise CutRefused(
            "⛔ REFUSED (--inscribe without --ratified) — a proposed ruling is not a ruling. "
            "Dave ratifies the cut on the review page first; then an operator feeds each entry to "
            "`python3 knowledge/_inscribe_ruling.py --entry <file> --write`. This script NEVER "
            f"writes {os.path.relpath(RULINGS, ROOT)}.")
    bad = [r["id"] for r in result["proposed_rulings"] if result["sidecar"][r["id"]]["note_absent"]]
    print("⚠ --ratified: PRINTING entries only. This script still writes no ruling file.")
    if bad:
        print(f"⛔ {len(bad)} entr(ies) are {NOTE_ABSENT} and must not be inscribed as his "
              f"words: {', '.join(bad)}")
    for r in result["proposed_rulings"]:
        e = dict(r)
        e["status"] = "ruled"
        print(json.dumps(e, ensure_ascii=False, indent=2))
    return 0


# ---------------------------------------------------------------------------
# 10. SELFTEST
# ---------------------------------------------------------------------------
def selftest():
    fails = []
    rows = load_sheet()
    decisions, proposals = load_harvest()

    # arm 0 — the sheet's shape is what the schema in the docstring says
    if len(rows) != 115:
        fails.append(f"arm0: sheet has {len(rows)} rows, expected 115")
    fam = {f: sum(1 for r in rows.values() if r["family"] == f) for f in "RUN"}
    if fam != {"R": 69, "U": 15, "N": 31}:
        fails.append(f"arm0b: row families are {fam}, expected R=69 U=15 N=31")

    # arm 1 — the synthetic: 3 decided non-unanimous, 1 unanimous ratified, 1 undecided
    e = make_synthetic(rows, decisions, proposals)
    res = cut(e, rows, decisions, proposals)
    c = res["counts"]
    for k, want in (("proposed_rulings", 3), ("unanimous_ratified", 1), ("when_patch", 1),
                    ("decided", 4), ("note_absent", 1), ("guess_source", 1),
                    ("undecided_later", 1), ("undecided", 111)):
        if c.get(k) != want:
            fails.append(f"arm1: counts[{k}] = {c.get(k)}, expected {want}")
    ids = [r["id"] for r in res["proposed_rulings"]]
    if ids != [f"s272-D{i}" for i in (1, 2, 3)]:
        fails.append(f"arm1b: ids are {ids}, expected s272-D1..D3")

    # arm 2 — NOTE-ABSENT: a decided row with no note never claims his words
    absent = [r for r in res["proposed_rulings"] if res["sidecar"][r["id"]]["note_absent"]]
    if len(absent) != 1:
        fails.append(f"arm2: expected exactly 1 NOTE-ABSENT record, got {len(absent)}")
    elif NOTE_ABSENT not in absent[0]["says"]:
        fails.append(f"arm2b: NOTE-ABSENT record's says does not carry the marker: {absent[0]['says']!r}")

    # arm 3 — the `when` patch is the s253-D1 shape and points at a REAL meta, unapplied
    for path, v in res["when_patch"].items():
        if not os.path.exists(os.path.join(ROOT, path)):
            fails.append(f"arm3: when patch aims at a meta that does not exist: {path}")
        if "—" not in v["when"]:
            fails.append(f"arm3b: when value has no em-dash, so it is not GATE — PROSE: {path}")
        if not v.get("_NOT_APPLIED"):
            fails.append(f"arm3c: when patch entry is not marked _NOT_APPLIED: {path}")
        before = json.load(open(os.path.join(ROOT, path), encoding="utf-8"))
        if before.get("when") == v["when"] and v["_replaces_existing"]:
            fails.append(f"arm3d: the meta on disk already carries the proposed when: {path}")

    # arm 4 — evidence pointers are the LEGAL `chat #<n> …` form (_governs.py, s148-D1)
    try:
        sys.path.insert(0, HERE)
        import _governs
        for r in res["proposed_rulings"]:
            if not _governs.is_chat_pointer(r["evidence"][0]):
                fails.append(f"arm4: {r['id']} evidence[0] is not a legal chat pointer: "
                             f"{r['evidence'][0]!r}")
    except Exception as ex:                       # noqa: BLE001
        fails.append(f"arm4: could not check evidence form against _governs.py: {ex}")

    # arm 5 — the ruling record passes _inscribe_ruling.check_schema once status is flipped
    try:
        import _inscribe_ruling as ins
        for r in res["proposed_rulings"]:
            e2 = dict(r); e2["status"] = "ruled"
            ins.check_schema(e2)
    except Exception as ex:                       # noqa: BLE001
        fails.append(f"arm5: a proposed record fails _inscribe_ruling.check_schema: {ex}")

    # arm 6 — the inscription door REFUSES without --ratified
    try:
        inscribe(res, ratified=False)
        fails.append("arm6: --inscribe without --ratified DID NOT REFUSE")
    except CutRefused:
        pass

    # arm 7 — nothing this run wrote _rulings.json (mtime is the probe)
    before = os.path.getmtime(RULINGS) if os.path.exists(RULINGS) else None
    cut(e, rows, decisions, proposals)
    after = os.path.getmtime(RULINGS) if os.path.exists(RULINGS) else None
    if before != after:
        fails.append("arm7: _rulings.json mtime CHANGED during a cut — the script wrote canon")

    # arm 8 — THE QUOTE GATE POSITIVE CONTROL + arm 9, THE MUTATION
    qrep = run_quote_gate(res)
    if not qrep.get("ran"):
        fails.append(f"arm8: the quote gate did not run: {qrep.get('why')}")
    else:
        ctl = [r for r in res["proposed_rulings"] if r["says"] == REAL_QUOTE]
        if not ctl:
            fails.append("arm8b: the synthetic carries no real-quote positive control")
        else:
            v = res["sidecar"][ctl[0]["id"]]["quote_gate"]
            if not v.get("found"):
                fails.append(f"arm8c: the positive control {REAL_QUOTE!r} was NOT found — the "
                             f"gate cannot report a corruption it cannot see. verdict={v}")
        # arm 9 — MUTATION: corrupt the control `says`, the gate must REPORT it as a miss.
        e_mut = dict(e)
        for rid, rec in e_mut.items():
            if rec["notes"] == REAL_QUOTE:
                e_mut[rid] = dict(rec, notes="180 was agreed because we use a sub for the wrap")
        res_m = cut(e_mut, rows, decisions, proposals)
        q_m = run_quote_gate(res_m)
        if not q_m.get("ran"):
            fails.append("arm9: the mutation arm's quote gate did not run")
        elif not q_m["misses"]:
            fails.append("arm9: MUTATION SURVIVED — a corrupted `says` was NOT reported by the "
                         "quote gate. The gate is decorative.")
        else:
            got = q_m["misses"][0]["says"]
            if "agreed" not in (got or ""):
                fails.append(f"arm9b: the reported miss is not the corrupted phrase: {got!r}")

    # arm 10 — the page renders, carries the no-inscription warning, and bakes type.css
    page = render_page(res, qrep, "synthetic.json")
    for needle in ("NOTHING IS INSCRIBED", "t-ed-body", "prefers-color-scheme",
                   "Not ruled — still yours", "s272-D1"):
        if needle not in page:
            fails.append(f"arm10: the review page is missing {needle!r}")
    if "overflow-x:auto" not in page:
        fails.append("arm10b: no horizontal-scroll container for the tables (400px overflow risk)")

    # arm 11 — an unknown exported id is IGNORED and DECLARED, never cut
    res_u = cut(dict(e, **{"R-Z-99": {"decision": "ratify", "option_index": None,
                                      "notes": "x", "at": None}}),
                rows, decisions, proposals)
    if res_u["unknown_export_ids"] != ["R-Z-99"]:
        fails.append(f"arm11: unknown id not declared: {res_u['unknown_export_ids']}")
    if len(res_u["proposed_rulings"]) != 3:
        fails.append("arm11b: an unknown exported id was cut into a ruling")

    print("\n".join("⛔ " + f for f in fails) if fails else
          "✓ _cut_harvest_rulings selftest: 12 arms GREEN (incl. quote-gate mutation).")
    print(f"  sheet {len(rows)} rows (R=69 U=15 N=31) · harvest {len(decisions)} decision rows "
          f"· {len(proposals)} when proposals")
    print(f"  synthetic: 3 decided non-unanimous → {len(res['proposed_rulings'])} proposed "
          f"rulings · 1 unanimous ratified → {len(res['when_patch'])} when patch "
          f"· {res['counts']['undecided_later']} later")
    return 1 if fails else 0


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", nargs="?", help="Dave's harvest-decisions-*.json")
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--date", default=DEFAULT_DATE)
    ap.add_argument("--session", type=int, default=SESSION)
    ap.add_argument("--dry-run", action="store_true", default=True,
                    help="(default) compute and report; write nothing")
    ap.add_argument("--write", action="store_true", help="write the out dir")
    ap.add_argument("--no-quote-gate", action="store_true")
    ap.add_argument("--inscribe", action="store_true",
                    help="REFUSES unless --ratified; even then it only PRINTS entries")
    ap.add_argument("--ratified", action="store_true", help="Dave ratified the cut (never a write)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--make-synthetic", metavar="PATH",
                    help="write a synthetic export built from the real sheet's model")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    rows = load_sheet()
    decisions, proposals = load_harvest()

    if a.make_synthetic:
        _dump(a.make_synthetic, make_synthetic(rows, decisions, proposals))
        print(f"synthetic export → {a.make_synthetic}")
        return 0

    if not a.export:
        ap.error("an export path is required (or --selftest / --make-synthetic)")

    export = load_export(a.export)
    res = cut(export, rows, decisions, proposals, date=a.date, session=a.session)
    qrep = run_quote_gate(res, enabled=not a.no_quote_gate)

    if a.inscribe:
        return inscribe(res, ratified=a.ratified)

    c = res["counts"]
    print(f"#{a.session} CUT — {a.export}")
    for k in sorted(c):
        print(f"  {k:24s} {c[k]}")
    if res["unknown_export_ids"]:
        print(f"  ⚠ unknown exported ids IGNORED: {', '.join(res['unknown_export_ids'])}")
    if qrep.get("ran"):
        print(f"  QUOTE-GATE ADVISORY: {qrep['found']}/{qrep['checked']} found, "
              f"{len(qrep['misses'])} NOT FOUND, {len(qrep['note_absent'])} NOTE-ABSENT")
        for m in qrep["misses"]:
            print(f"    ⛔ {m['id']}: {m['says']!r}")
    else:
        print(f"  QUOTE-GATE did not run: {qrep.get('why')}")

    if a.write:
        for p in write_out(res, qrep, a.out, a.export, date=a.date, session=a.session):
            print(f"  → {os.path.relpath(p, ROOT)}")
    else:
        print("  (dry run — nothing written. Pass --write.)")
    print("  ⛔ knowledge/_rulings.json and every components/*.meta.json UNTOUCHED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
