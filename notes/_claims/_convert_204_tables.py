#!/usr/bin/env python3
"""_convert_204_tables.py — DERIVE the #204 claim/challenge JSONL from the two markdown receipts.

W-44's acceptance test: drive the new schema on REAL data. This script is the derivation, kept
in-repo (`s191-D2`) so the JSONL beside it is reproducible rather than hand-typed prose.

⛔ IT READS THE #204 RECEIPTS AND NEVER WRITES THEM. Sources (originals, untouched):
   notes/_receipts/2026-08-19-204-buildpm-claim-table.md
   notes/_receipts/2026-08-19-204-verifier-challenge-table.md
Outputs (derived copies, this directory):
   notes/_claims/204-buildpm-claims.jsonl
   notes/_claims/204-verifier-challenges.jsonl

CONVERSION DECISIONS — every hand judgment is DECLARED here, in code, not applied invisibly:

 1. COMBINED ID CELLS are split. The source writes `L1-3 / L1-4`, `F-1 · F-2 · F-3`,
    `H-1 · H-2 · H-3 · H-6 · H-7` as one row answering several claims. The join keys on `id`,
    so each becomes its own row carrying the shared evidence, with a `note` recording the
    combination. Rejected alternative: keep the combined string as one id — it would join to
    nothing, and every claim inside it would surface as UNCHALLENGED, which is false.
 2. QUALIFIED IDS keep their base id. `D-7 (figure)` and `D-7 (substance)` both become `D-7`;
    the qualifier moves into `note`. This is why challenge ids are allowed to repeat.
 3. TAG / VERDICT is the first ENUM KEYWORD found in the cell, in the priority order
    CONTRADICTED > UNTESTED > CONFIRMED (uppercase only — the source writes lowercase
    "untested" inside prose). The FULL original cell is preserved in `note`, so nothing the
    enum could not carry is lost (`s204-D1`: a schema too tight forces prose back into chat).
 4. OVERRIDES below are the rows where a mechanical read would be WRONG. Each is one line with
    its reason. They are visible, few, and reviewable — the alternative (silently letting the
    keyword scanner win) is the class this whole lane exists to kill.
 5. NEW FINDINGS are `###` prose sections, not table rows, so they are declared as data below,
    with the command each one actually ran as the evidence pointer.

Usage: python3 notes/_claims/_convert_204_tables.py --write
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "knowledge", "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_os.path.join(_hg_d, "knowledge"))
from _helpgate import help_gate as _help_gate, write_gate as _write_gate
_help_gate(__doc__, __name__, __file__)
_write_gate(__file__, writes="notes/_claims/204-*.jsonl", name=__name__)

import re, json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CLAIM_MD = os.path.join(ROOT, "notes/_receipts/2026-08-19-204-buildpm-claim-table.md")
CHAL_MD = os.path.join(ROOT, "notes/_receipts/2026-08-19-204-verifier-challenge-table.md")

TAGS = ("PROVEN", "MEASURED", "CLAIMED", "UNPROVEN")

# Decision 4 — declared overrides, one reason each.
VERDICT_OVERRIDE = {
    # "PARTIALLY CONFIRMED — the theme legs are real, the *numbers* remain untested".
    # The mechanism was probed; every contrast/hit-area FIGURE was not. UNTESTED is the honest
    # enum for a row whose own text says the numbers are untested; CONFIRMED would launder it.
    "C-7": ("UNTESTED", "source says PARTIALLY CONFIRMED — mechanism probed, FIGURES untested; "
                        "mapped to UNTESTED so the join surfaces it rather than collapsing it"),
}
TAG_OVERRIDE = {
    # "CLAIMED (lanes N/P: UNPROVEN)" — the weaker half is the one that carries the risk.
    "C-8": ("CLAIMED", "source: 'CLAIMED (lanes N/P: UNPROVEN)' — the lanes-N/P half is UNPROVEN"),
    "E-2": ("PROVEN", "source: 'PROVEN + CLAIMED' — counts PROVEN, the row-91 adjudication CLAIMED"),
    "F-9": ("MEASURED", "source: 'MEASURED (content) / UNPROVEN (attribution)'"),
    "F-10": ("MEASURED", "source: 'MEASURED (content) / UNPROVEN (attribution)'"),
}
# Rows whose claim text names a declared stop / a seat that is not a worker's.
FENCES = {
    "G-8": "declared stop — a filtered run rewrites the tracked _STATE-CONTRAST-AUDIT.md",
    "D-7": "Dave's — not rulable by a worker or a conductor",
    "H-1": "Dave's — the lever is a constant Dave owns",
    "H-2": "out of fence — all three fixes write _rulings.json or narrow a RULED item",
    "H-3": "declared stop — rewrites a tracked audit",
    "H-7": "Dave's — colour judgment, red-law adjacent",
    "F-11": "fence sweep — the row that asserts nothing fenced was touched",
}


def split_cells(line):
    parts, buf, i = [], "", 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line):
            buf += line[i:i + 2]; i += 2; continue
        if line[i] == "|":
            parts.append(buf); buf = ""; i += 1; continue
        buf += line[i]; i += 1
    parts.append(buf)
    return [p.strip() for p in parts[1:-1]] if len(parts) > 2 else []


def clean(s):
    s = re.sub(r"<br\s*/?>", " · ", s)
    # ⚠ strip BOLD only. Stripping a lone `*` turns `REVIEW-204-*.html` into `REVIEW-204-.html`
    # — a glob mangled into a DEAD POINTER. Found by this lane's own evidence linter (fix loop,
    # amendment ②): 6 of its 18 first-run findings were this converter defect, not source defects.
    s = s.replace("**", "").replace("\\|", "|")
    return re.sub(r"\s+", " ", s).strip()


def declared_rc(ev):
    """Lift the FIRST `rc=N` out of the evidence prose, so the sampler compares rather than
    merely reports. No rc in the prose -> the field is ABSENT, never defaulted to 0."""
    m = re.search(r"\brc\s*=\s*(\d+)", ev)
    return int(m.group(1)) if m else None


def ids_from(cell):
    """Decision 1 + 2: split combined cells, drop qualifiers into the caller's note."""
    raw = clean(cell)
    quals = re.findall(r"\(([^)]*)\)", raw)
    raw = re.sub(r"\([^)]*\)", " ", raw)
    parts = [p.strip(" `") for p in re.split(r"\s*[/·,]\s*", raw) if p.strip(" `")]
    return parts, " · ".join(quals)


def tables(path):
    """Yield (section, header_cells, row_cells) for every markdown table row in the file."""
    section = ""
    header = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("#"):
                section = clean(line.lstrip("# ")); header = None; continue
            if not line.lstrip().startswith("|"):
                header = None; continue
            cells = split_cells(line.strip())
            if not cells:
                continue
            if set("".join(cells).replace(" ", "")) <= set("-:"):
                continue
            if header is None:
                header = [c.lower() for c in cells]
                continue
            yield section, header, cells


def build_claims():
    rows, skipped = [], []
    for section, header, cells in tables(CLAIM_MD):
        if header[0] not in ("id",) or len(cells) < 3:
            skipped.append((section, cells[:1])); continue
        idcell = cells[0]
        # section F is | id | path | attribution | tag |; section H is | id | item | tag |
        if "path" in header:
            claim_txt = "TRACKED FILE %s — %s" % (clean(cells[1]), clean(cells[2]))
            # the PATH column is the probeable token (s182-D1); the attribution is the claim
            ev, tagcell = clean(cells[1]) + " · " + clean(cells[2]), cells[3]
        elif len(cells) == 3:
            claim_txt, ev, tagcell = clean(cells[1]), clean(cells[1]), cells[2]
        else:
            claim_txt, ev, tagcell = clean(cells[1]), clean(cells[2]), cells[3]
        # ⚠ word boundaries are LOAD-BEARING: "UNPROVEN" contains "PROVEN" as a substring, and a
        # naive `in` test tagged every declared stop in section H as PROVEN (caught in this
        # lane's own build — the exact `unmatched-grep-is-not-an-absence` shape, inverted).
        found = [t for t in ("UNPROVEN", "PROVEN", "MEASURED", "CLAIMED")
                 if re.search(r"\b%s\b" % t, tagcell)]
        ids, qual = ids_from(idcell)
        for i in ids:
            tag, why = TAG_OVERRIDE.get(i, (found[0] if found else None, ""))
            if tag is None:
                skipped.append((section, [i, tagcell])); continue
            note = " · ".join(x for x in [qual, why,
                                          ("source tag cell: " + clean(tagcell))
                                          if clean(tagcell) != tag else "",
                                          "combined source row: " + " / ".join(ids)
                                          if len(ids) > 1 else ""] if x)
            r = {"id": i, "kind": "claim", "section": section, "claim": claim_txt,
                 "evidence": ev, "tag": tag}
            rc = declared_rc(ev)
            if rc is not None:
                r["rc"] = rc
            if note:
                r["note"] = note
            if i in FENCES:
                r["fence"] = FENCES[i]
            rows.append(r)
    return rows, skipped


NEW_ROWS = [
    {"id": "NEW-1", "verdict": "NEW",
     "claim": "Three of six review pages ship duplicated `id` attributes, 8x each, and the "
              "duplicates are aria-labelledby targets — document-row 4, payment-card-visual 7, "
              "runway-bar 5; lane M's pages are clean (96 unique of 96)",
     "evidence": "`grep -c 'id=\"rwy1-label\"' reviews/REVIEW-204-runway-bar-four-themes-v1.html` "
                 "· source ran a Counter over re.findall(r'\\sid=\"([^\"]+)\"') per review page "
                 "-> document-row 32 ids/4 unique · payment-card-visual 56/7 · runway-bar 40/5",
     "note": "no gate parses the review pages — they sit outside knowledge/snippets/ (#122)"},
    {"id": "NEW-2", "verdict": "NEW",
     "claim": "Document-row collapses canon's three error tokens into one local --error in both "
              "light and dark; conformant as shipped, but the naming is a loaded gun for the next "
              "edit that paints error TEXT with it (#DA1A00-on-white is the two-red law)",
     "evidence": "knowledge/snippets/Document-row.reference.html:149 and :158 declare "
                 "`--error:#F6604C`; knowledge/canon/canon.css:308-311 distinguishes "
                 "--rag-error-background / --rag-error-glyph / --rag-error-ink",
     "note": "fix is one rename to --error-fill; s151-D1 two-red law is NOT breached today"},
    {"id": "NEW-3", "verdict": "NEW",
     "claim": "A red --check that CI does not run: _build_memento_index.py --check exits 1 STALE "
              "and no job invokes it — instrument-without-a-consumer, and three workers were "
              "served a previous session's corpus by _memento_search.py",
     "evidence": "`python3 knowledge/_build_memento_index.py --check` -> rc=1 · "
                 "`memento index --check: STALE`", "rc": 1,
     "note": "rc measured off a file redirect, not a pipe — the pipe read rc=0 from tail"},
    {"id": "NEW-4", "verdict": "NEW",
     "claim": "A probe that was expected to contradict and did not: the four-theme spreads are "
              "genuinely four themes, and the #184 dangling-var probe found UNRESOLVED=[] across "
              "all six review pages, 174 references checked",
     "evidence": "`grep -oE '\\[data-apollo-theme=\"[a-z]+\"\\]' knowledge/canon/canon.css` -> "
                 "legacy 262 · supercharge 262 · console 205 scoped rules; review pages link "
                 "../knowledge/canon/canon.css at :7-8",
     "note": "recorded because a negative result is worth something"},
]


def build_challenges():
    rows, skipped = [], []
    for section, header, cells in tables(CHAL_MD):
        if header[0] != "id" or "verdict" not in header or len(cells) < 3:
            skipped.append((section, cells[:1])); continue
        idcell, vcell, ev = cells[0], cells[1], clean(cells[2])
        ids, qual = ids_from(idcell)
        for i in ids:
            if i in VERDICT_OVERRIDE:
                verdict, why = VERDICT_OVERRIDE[i]
            else:
                why = ""
                verdict = ("CONTRADICTED" if "CONTRADICTED" in vcell else
                           "UNTESTED" if "UNTESTED" in vcell else
                           "CONFIRMED" if "CONFIRMED" in vcell else None)
            if verdict is None:
                skipped.append((section, [i, vcell])); continue
            note = " · ".join(x for x in [
                qual, why,
                ("source verdict cell: " + clean(vcell)) if clean(vcell) != verdict else "",
                ("combined source row: " + " / ".join(ids)) if len(ids) > 1 else ""] if x)
            r = {"id": i, "kind": "challenge", "section": section,
                 "claim": clean(vcell) or verdict, "evidence": ev, "verdict": verdict}
            rc = declared_rc(ev)
            if rc is not None:
                r["rc"] = rc
            if note:
                r["note"] = note
            if i in FENCES:
                r["fence"] = FENCES[i]
            rows.append(r)
    for n in NEW_ROWS:
        rows.append(dict(n, kind="challenge", section="3 · NEW FINDINGS"))
    return rows, skipped


def main():
    claims, cskip = build_claims()
    chals, hskip = build_challenges()
    for name, rows, skip in (("204-buildpm-claims.jsonl", claims, cskip),
                             ("204-verifier-challenges.jsonl", chals, hskip)):
        p = os.path.join(HERE, name)
        with open(p, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("wrote %s — %d row(s); %d source row(s) carried no enum and were SKIPPED (declared, "
              "not silent): %s" % (p, len(rows), len(skip),
                                   [s[1] for s in skip][:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
