#!/usr/bin/env python3
"""_build_consult_index.py — generates knowledge/_consult-index.json.

Part 1 of the "consult" read-side tool (reviews/CONSOLIDATION-AUDIT-2026-07-18.html §3).
The corpus is superbly ID'd (465 rules, T-D/R-D/DV-D rulings, ASSERT-00x, DEF-00x, ADRs,
gates) but lives in nine-plus stores with grep as the only join. This generator builds ONE
answerable index over all of them so `_consult.py` can answer "what governs X?" in one step.

record := { id, kind, text, file, status, bite }
kind in rule | ruling | assertion | gate | adr | defect | open-item

Sources (all read-only; this script writes nothing but knowledge/_consult-index.json):
  guidelines/_rules-index.json            -> rule records
  _proforma/_TYPE-DECISIONS.md            -> ruling records (T-D\\d+ headings)
  _proforma/_RAG-DECISIONS.md             -> ruling records (R-D\\d+ headings)
  _proforma/_DATAVIZ-DECISIONS.md         -> ruling records (DV-D\\d+ standing-decision bullets)
  _assertions.json                        -> assertion records
  _validate_*.py                          -> gate records (docstring line 1 + resolved bite)
  docs/decisions/ADR-*.md                 -> adr records
  _DS-IMPROVEMENTS.md + _ICON-GAPS.md     -> defect records
  ../_LIVE-STATE.md "## OPEN" section     -> open-item records

Run:  python3 knowledge/_build_consult_index.py
Exits non-zero only on a hard read failure (missing required source file) — this is a
generator, not a gate; grow-on-miss curation lives in the lexicon, not here.
"""
import json, os, re, sys, glob as globlib

HERE = os.path.dirname(os.path.abspath(__file__))          # knowledge/
ROOT = os.path.dirname(HERE)                                # repo root
OUT = os.path.join(HERE, "_consult-index.json")


def clean_md(s):
    """Strip the light markdown decoration we don't want in searchable text."""
    s = s.replace("`", "")
    s = re.sub(r"\*\*", "", s)
    s = re.sub(r"^\s*#+\s*", "", s, flags=re.M)
    s = re.sub(r"^\s*[-*]\s+", "", s, flags=re.M)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n+", " ", s)
    return s.strip()


# ------------------------------------------------------------------ rules
def parse_rules():
    path = os.path.join(HERE, "guidelines", "_rules-index.json")
    d = json.load(open(path, encoding="utf-8"))
    out = []
    for r in d["rules"]:
        out.append({
            "id": r["id"],
            "kind": "rule",
            "text": r["rule"],
            "file": f"knowledge/guidelines/{r['file']}",
            "status": r.get("destiny", "unknown"),
            "bite": None,
        })
    return out


# ---------------------------------------------------------------- rulings
# ds-009 (2026-07-22): the ID pattern is GENERIC — any <prefix>-D<n> ledger ID — so a
# new ledger's rulings index without a code change (B-D1…B-D7 were unfindable for two
# days because this regex enumerated three prefixes and the corpus list was hardcoded).
RULING_ID_RE = re.compile(r"\b([A-Z]{1,3}-D\d+)\b")


def infer_ruling_status(heading_title):
    u = heading_title.upper()
    if "SUPERSEDED" in u:
        return "SUPERSEDED"
    if u.strip().startswith("OPEN") or " OPEN" in u:
        return "OPEN"
    if "PROVISIONAL" in u:
        return "PROVISIONAL"
    if "RULED" in u or "SOLVED" in u or "RESOLVED" in u or "APPROVED" in u:
        return "RULED"
    return "RULED"


def parse_heading_rulings(path, rel_file):
    """T-D\\d+ / R-D\\d+ headings in _TYPE-DECISIONS.md and _RAG-DECISIONS.md.

    A record's body runs from the heading to the next heading of the SAME OR
    SHALLOWER level (## vs ###), so sub-headings inside a ruling's own section
    stay part of its text.
    """
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    n = len(lines)
    out = []
    seen = set()
    i = 0
    while i < n:
        m = re.match(r"^(#{1,6})\s+(.*)$", lines[i])
        if m and RULING_ID_RE.search(lines[i]):
            level = len(m.group(1))
            rid = RULING_ID_RE.search(lines[i]).group(1)
            heading_title = clean_md(m.group(2))
            j = i + 1
            body_lines = []
            while j < n:
                lm = re.match(r"^(#{1,6})\s+", lines[j])
                if lm and len(lm.group(1)) <= level:
                    break
                body_lines.append(lines[j])
                j += 1
            body = clean_md("\n".join(body_lines))
            full_text = re.sub(r"\s+", " ", f"{heading_title}. {body}").strip()[:4000]
            if rid not in seen:
                seen.add(rid)
                out.append({
                    "id": rid, "kind": "ruling", "text": full_text,
                    "file": rel_file, "status": infer_ruling_status(heading_title),
                    "bite": None,
                })
            i = j
            continue
        i += 1
    return out


def parse_dataviz_rulings(path, rel_file):
    """DV-D\\d+ bold-marker bullets in the 'Standing decisions' block of
    _DATAVIZ-DECISIONS.md — this file rules by bullet, not by heading."""
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    n = len(lines)
    out = []
    seen = set()
    i = 0
    bullet_start = re.compile(r"^-\s+\*\*(DV-D\d+)\s*\xb7")
    while i < n:
        m = bullet_start.match(lines[i])
        if m:
            rid = m.group(1)
            block = [lines[i]]
            j = i + 1
            while j < n and lines[j].strip() and not lines[j].startswith("-") and not lines[j].startswith("#"):
                block.append(lines[j])
                j += 1
            body = clean_md(" ".join(block))
            body = re.sub(r"\s+", " ", body)[:2000]
            if rid not in seen:
                seen.add(rid)
                out.append({
                    "id": rid, "kind": "ruling", "text": body,
                    "file": rel_file, "status": "RULED (standing)", "bite": None,
                })
            i = j
            continue
        i += 1
    return out


def parse_rulings():
    """ds-009 fix (2026-07-22): the corpus is DISCOVERED — every _proforma/_*-DECISIONS.md
    on disk is parsed (heading-style by default; _DATAVIZ-DECISIONS.md rules by bullet).
    A ledger that yields ZERO records fails the build loudly: an unindexed ledger is
    exactly the silent hole B-D1…B-D5 fell into (unfindable by any consult query)."""
    out = []
    ledgers = sorted(globlib.glob(os.path.join(HERE, "_proforma", "_*-DECISIONS.md")))
    if not ledgers:
        raise SystemExit("consult index: no _proforma/_*-DECISIONS.md ledgers found (corpus glob broken?)")
    for path in ledgers:
        rel = "knowledge/_proforma/" + os.path.basename(path)
        if os.path.basename(path) == "_DATAVIZ-DECISIONS.md":
            got = parse_dataviz_rulings(path, rel)
        else:
            got = parse_heading_rulings(path, rel)
        if not got:
            raise SystemExit(f"consult index: ledger {rel} yielded ZERO rulings — parser/ID mismatch "
                             f"(ds-009 class). Fix the parser or the ledger; do not ship an unindexed ledger.")
        out += got
    return out


# -------------------------------------------------------------- assertions
def parse_assertions():
    path = os.path.join(HERE, "_assertions.json")
    d = json.load(open(path, encoding="utf-8"))
    out = []
    for a in d.get("assertions", []):
        text = " ".join(filter(None, [a.get("claim", ""), a.get("consequence", "")]))
        out.append({
            "id": a["id"], "kind": "assertion", "text": text.strip(),
            "file": "knowledge/_assertions.json",
            "status": a.get("kind", "unknown"), "bite": None,
        })
    return out


# ------------------------------------------------------------------ gates
def first_docstring_line(text):
    m = re.search(r'("""|\'\'\')(.*)', text)
    if not m:
        return ""
    rest = m.group(2)
    if rest.strip():
        return rest.strip()
    after = text[m.end():]
    for line in after.split("\n"):
        if line.strip():
            return line.strip()
    return ""


def extract_bite(text):
    """Best-effort static extraction of the glob(s)/path(s) a gate scans, resolved to a
    file count. Deliberately simple regex analysis, not a real Python AST walk — matches
    the "look for GLOBS, glob.glob, hardcoded dirs" brief. Falls back honestly."""
    var_paths = {}
    for m in re.finditer(r"^(\w+)\s*=\s*os\.path\.dirname\(os\.path\.abspath\(__file__\)\)", text, re.M):
        var_paths[m.group(1)] = "knowledge"
    for m in re.finditer(r"^(\w+)\s*=\s*os\.path\.dirname\((\w+)\)", text, re.M):
        base = var_paths.get(m.group(2))
        if base is not None:
            var_paths[m.group(1)] = os.path.dirname(base) if base else ""
    changed = True
    while changed:
        changed = False
        for m in re.finditer(r'^(\w+)\s*=\s*os\.path\.join\(\s*(\w+)\s*((?:,\s*"[^"]*")+)\s*\)', text, re.M):
            var, base, litstr = m.group(1), m.group(2), m.group(3)
            if var in var_paths or base not in var_paths:
                continue
            lits = re.findall(r'"([^"]*)"', litstr)
            parts = [p for p in [var_paths[base]] + lits if p]
            var_paths[var] = "/".join(parts)
            changed = True

    candidates = []
    # (a) glob.glob(os.path.join(VAR, "lit"...))
    for m in re.finditer(r'glob\.glob\(\s*os\.path\.join\(\s*(\w+)\s*((?:,\s*"[^"]*")*)\s*\)', text):
        base, litstr = m.group(1), m.group(2)
        basepath = var_paths.get(base)
        if basepath is None:
            continue
        lits = re.findall(r'"([^"]*)"', litstr)
        parts = [p for p in [basepath] + lits if p]
        candidates.append("/".join(parts))
    # (b) open(os.path.join(VAR, "lit"...)) single-file reads, no wildcard — skip write-mode opens
    for m in re.finditer(
        r'open\(\s*os\.path\.join\(\s*(\w+)\s*((?:,\s*"[^"]*")+)\s*\)\s*(?:,\s*"([rwax][^"]*)")?\s*\)',
        text,
    ):
        base, litstr, mode = m.group(1), m.group(2), m.group(3)
        if mode and mode[0] in "wa":
            continue
        basepath = var_paths.get(base)
        if basepath is None:
            continue
        lits = re.findall(r'"([^"]*)"', litstr)
        parts = [p for p in [basepath] + lits if p]
        pattern = "/".join(parts)
        if "*" not in pattern:
            candidates.append(pattern)
    # (c) open(VARNAME) where VARNAME already resolved to a single file path
    for m in re.finditer(r"open\(\s*(\w+)\s*\)", text):
        v = var_paths.get(m.group(1))
        if v and "." in os.path.basename(v):
            candidates.append(v)
    # (d) fallback — any "knowledge/...*....ext" literal (covers dynamic pat-variable loops,
    #     e.g. `for pat in ("knowledge/snippets/*.html", ...): glob.glob(os.path.join(ROOT, pat))`)
    if not candidates:
        for lit in re.findall(r'"(knowledge/[^"]*(?:\*[^"]*)?\.\w+)"', text):
            candidates.append(lit)

    seen, pieces = set(), []
    for pat in candidates:
        if not pat or pat in seen:
            continue
        seen.add(pat)
        full = os.path.join(ROOT, pat)
        matches = globlib.glob(full, recursive=True)
        n = len(matches)
        pieces.append(f"{pat} → {n} file{'' if n == 1 else 's'}")
    if not pieces:
        return "unknown — read the script"
    return "; ".join(pieces)


def gate_labels_from_build_all():
    """Ground truth for advisory-vs-blocking: _build_all.py's own STEPS list already says so
    in its label ("... (advisory)"). Cheaper and more honest than re-guessing from prose."""
    path = os.path.join(HERE, "_build_all.py")
    if not os.path.exists(path):
        return {}
    text = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'\("([^"]+)",\s*"([^"]+\.py)"', text):
        label, rel = m.group(1), m.group(2)
        out[os.path.basename(rel)] = label
    return out


def parse_gates():
    out = []
    step_labels = gate_labels_from_build_all()
    for fname in sorted(os.listdir(HERE)):
        if not (fname.startswith("_validate_") and fname.endswith(".py")):
            continue
        path = os.path.join(HERE, fname)
        text = open(path, encoding="utf-8").read()
        rid = fname[:-3].lstrip("_").replace("_", "-")
        docline = first_docstring_line(text)
        label = step_labels.get(fname)
        if label is None:
            status = "BLOCKING (not wired into _build_all.py)"
        elif "advisory" in label.lower():
            status = "ADVISORY"
        else:
            status = "BLOCKING"
        bite = extract_bite(text)
        out.append({
            "id": rid, "kind": "gate", "text": docline,
            "file": f"knowledge/{fname}", "status": status, "bite": bite,
        })
    return out


# -------------------------------------------------------------------- adrs
def parse_adrs():
    dirpath = os.path.join(ROOT, "docs", "decisions")
    out = []
    if not os.path.isdir(dirpath):
        return out
    for fname in sorted(os.listdir(dirpath)):
        if not (fname.startswith("ADR-") and fname.endswith(".md")):
            continue
        text = open(os.path.join(dirpath, fname), encoding="utf-8").read()
        lines = text.split("\n")
        title, status = "", "unknown"
        for line in lines[:12]:
            if line.startswith("# ") and not title:
                title = line[2:].strip()
            sm = re.search(r"\*\*Status:\*\*\s*([^·\n]+)", line)
            if sm:
                status = sm.group(1).strip()
        idm = re.match(r"ADR-(\d+)", fname)
        rid = f"ADR-{idm.group(1)}" if idm else fname
        out.append({
            "id": rid, "kind": "adr", "text": title,
            "file": f"docs/decisions/{fname}", "status": status, "bite": None,
        })
    return out


# ---------------------------------------------------------------- defects
def parse_ds_improvements():
    path = os.path.join(HERE, "_DS-IMPROVEMENTS.md")
    text = open(path, encoding="utf-8").read()
    out = []
    for m in re.finditer(r"^## (ds-\d+) — (.+)$", text, re.M):
        rid, title = m.group(1), m.group(2).strip()
        chunk = text[m.end():m.end() + 400]
        sm = re.search(r"\*\*Status:\*\*\s*([^\n]+)", chunk)
        if sm:
            status = sm.group(1).strip()
        else:
            im = re.search(r"\*([^*\n]{3,80})\*", chunk)
            status = im.group(1).strip() if im else "unknown"
        out.append({
            "id": rid, "kind": "defect", "text": clean_md(title),
            "file": "knowledge/_DS-IMPROVEMENTS.md", "status": status, "bite": None,
        })
    return out


def parse_icon_gaps():
    path = os.path.join(HERE, "_ICON-GAPS.md")
    text = open(path, encoding="utf-8").read()
    out = []
    in_table = False
    for line in text.split("\n"):
        if line.startswith("| Glyph "):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("|---"):
            continue
        if not line.startswith("|"):
            break
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 3:
            continue
        glyph = clean_md(cols[0])
        needed_for = clean_md(cols[1])
        status = clean_md(cols[2])
        slug = re.sub(r"[^a-z0-9]+", "-", glyph.lower()).strip("-")
        out.append({
            "id": f"icon-gap-{slug}", "kind": "defect",
            "text": f"{glyph} — {needed_for}",
            "file": "knowledge/_ICON-GAPS.md", "status": status, "bite": None,
        })
    return out


# -------------------------------------------------------------- open items
def parse_live_state_open():
    path = os.path.join(ROOT, "_LIVE-STATE.md")
    if not os.path.exists(path):
        return []
    text = open(path, encoding="utf-8").read()
    out = []
    in_section = False
    counter = 0
    for line in text.split("\n"):
        if re.match(r"^## OPEN\b", line):
            in_section = True
            continue
        if in_section and re.match(r"^## ", line):
            break
        if not in_section:
            continue
        if line.startswith("### ") or re.match(r"^\s*-\s+\*\*", line):
            counter += 1
            cleaned = clean_md(line)
            if not cleaned:
                continue
            out.append({
                "id": f"open-{counter:03d}", "kind": "open-item",
                "text": cleaned[:500], "file": "_LIVE-STATE.md",
                "status": "OPEN", "bite": None,
            })
    return out


# --------------------------------------------------------------------- main
def main():
    records = []
    records += parse_rules()
    records += parse_rulings()
    records += parse_assertions()
    records += parse_gates()
    records += parse_adrs()
    records += parse_ds_improvements()
    records += parse_icon_gaps()
    records += parse_live_state_open()

    by_kind = {}
    for r in records:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1

    out = {
        "$description": "GENERATED by _build_consult_index.py — do not hand-edit. "
                         "Problem-domain query index for knowledge/_consult.py "
                         "(reviews/CONSOLIDATION-AUDIT-2026-07-18.html §3).",
        "count": len(records),
        "byKind": by_kind,
        "records": records,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"consult index built: {len(records)} records -> {os.path.relpath(OUT, ROOT)}")
    for k in sorted(by_kind):
        print(f"  {k:12s} {by_kind[k]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
