#!/usr/bin/env python3
"""_build_memento_index.py — generator for the Memento door's index (O2′, ruled #25).

Writes knowledge/_memento-index.json for `_memento_search.py` (door) over the corpus
Dave named in the ruled direction (ledger § Memento-before-Apollo: "GM sections · LS
entries · archives · briefs · ledgers") plus the memento runbooks and lane records
(option-select #25, pick 2 — the band table's only copy lives in a runbook; a memento
search that cannot reach 'grep it, never recall it' canon leaves the most-recalled text
outside the spine).

CONTRACT TIERS — closed forms REFUSE on the unknown (ds-016 class, never
enumerate-and-skip); open forms split but never refuse on heading content:

  CLOSED (structure is a vocabulary):
    GOOD-MORNING.md          — sections via _gm_usage.GM_VOCAB (IMPORTED — the only copy)
    _LIVE-STATE.md           — sections via _gm_usage.LS_VOCAB (IMPORTED)
    notes/_GAUGE-LOG.md      — blocks `#### YYYY-MM-DD #N`; any other `#### ` REFUSES
    knowledge/_lanes.json    — via _gen_lanes.load_lanes() (IMPORTED — its own validation)

  OPEN (prose files; the split is a convenience, not a schema):
    _GM-ARCHIVE.md · _LIVE-STATE-ARCHIVE.md — `## ` sections. ⚠ DELIBERATE, measured at
        first build (#25): archives hold MOVED CONTENT VERBATIM, and moved banners carry
        their own `## `-level headings (old DO-FIRST/queue/PRIOR sections), so a closed
        batch contract is falsified by the corpus itself — the author's first draft
        assumed one and the fail-loud refusal caught it, correctly. Open split is also
        the better fetch unit: a rolled `## ⏱ PRIOR DELTA` is its own record.
    notes/_MEMENTO-DECISIONS.md — `## ` sections, slug ids
    notes/_briefs/*.md          — one record per file
    notes/_dream/*.md           — one record per file
    memento runbooks            — `## `/`### ` sections, slug ids (list in RUNBOOKS below;
                                  extending the set is an edit here, deliberate)

Missing declared files REFUSE. A source class contributing ZERO records REFUSES.
Determinism: records sorted by (file, line); id collisions suffixed `-2`, `-3` in
document order; `--check` regenerates and byte-compares (the ADR-0013 ruling-4 shape).

Usage:
  python3 knowledge/_build_memento_index.py             # write the index
  python3 knowledge/_build_memento_index.py --check     # determinism / staleness gate
  python3 knowledge/_build_memento_index.py --selftest  # refusal + determinism bites
"""
import json, os, re, sys, glob as globlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_PATH = os.path.join(HERE, "_memento-index.json")
sys.path.insert(0, HERE)

GAUGE_BLOCK_RE = re.compile(r"^####\s+(\d{4}-\d{2}-\d{2})\s+#(\w+)\b")
H2_RE = re.compile(r"^##\s")
H4_RE = re.compile(r"^####\s")

RUNBOOKS = [  # the memento set — extending it is a deliberate edit, not a glob
    "knowledge/_RUNBOOK-capture-ritual.md",
    "knowledge/_RUNBOOK-context-gauge.md",
    "knowledge/_RUNBOOK-consult.md",
    "knowledge/_RUNBOOK-dream-pass.md",
    "knowledge/_RUNBOOK-git-commit.md",
]


def slug(text, maxlen=60):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen].rstrip("-") or "untitled"


def head_of(lines_or_text, limit=140):
    if isinstance(lines_or_text, str):
        lines = lines_or_text.splitlines()
    else:
        lines = lines_or_text
    for ln in lines:
        if ln.strip():
            return ln.strip()[:limit]
    return "(empty)"


def read_lines(relpath, errors):
    p = os.path.join(ROOT, relpath)
    if not os.path.exists(p):
        errors.append(f"{relpath}: declared source MISSING — refuse, never index around a hole")
        return None
    with open(p, encoding="utf-8") as f:
        return f.read().splitlines()


def rec(rid, kind, relfile, line, head, text):
    return {"id": rid, "kind": kind, "file": relfile, "line": line,
            "head": head, "text": text}


def _dedupe(records):
    seen = {}
    for r in records:
        n = seen.get(r["id"], 0) + 1
        seen[r["id"]] = n
        if n > 1:
            r["id"] = f"{r['id']}-{n}"
    return records


# ------------------------------------------------------------- closed contracts
def parse_gm_ls(records, errors):
    import _gm_usage
    for relpath, vocab, unknown, prefix in (
            ("GOOD-MORNING.md", _gm_usage.GM_VOCAB, _gm_usage._gm_unknown, "gm"),
            ("_LIVE-STATE.md", _gm_usage.LS_VOCAB, _gm_usage._ls_unknown, "ls")):
        lines = read_lines(relpath, errors)
        if lines is None:
            continue
        spans, errs = _gm_usage.split_sections(lines, vocab, unknown_check=unknown)
        if errs:
            errors.extend(f"{relpath}: {e}" for e in errs)
            continue
        for vid, (a, b) in sorted(spans.items(), key=lambda kv: kv[1][0]):
            body = "\n".join(lines[a:b])
            records.append(rec(f"{prefix}:{vid}", f"{prefix}-section", relpath, a + 1,
                               head_of(lines[a:b]), body))


def parse_gauge(records, errors):
    relpath = "notes/_GAUGE-LOG.md"
    lines = read_lines(relpath, errors)
    if lines is None:
        return
    marks = []
    for i, ln in enumerate(lines):
        m = GAUGE_BLOCK_RE.match(ln)
        if m:
            marks.append((i, m))
        elif H4_RE.match(ln):
            errors.append(f"{relpath}:{i + 1}: `#### ` block outside `#### YYYY-MM-DD #N` — "
                          f"refuse: {ln.strip()[:70]}")
    if not marks:
        errors.append(f"{relpath}: zero gauge blocks — contract broken, refuse")
        return
    if marks[0][0] > 0:
        body = "\n".join(lines[: marks[0][0]])
        records.append(rec("gauge:HDR", "gauge-block", relpath, 1, head_of(body), body))
    for n, (i, m) in enumerate(marks):
        end = marks[n + 1][0] if n + 1 < len(marks) else len(lines)
        records.append(rec(f"gauge:{m.group(1)}-{m.group(2)}", "gauge-block", relpath, i + 1,
                           lines[i].lstrip("# ").strip()[:140], "\n".join(lines[i:end])))


def parse_lanes(records, errors):
    import _gen_lanes
    lanes, errs = _gen_lanes.load_lanes()
    if errs:
        errors.extend(f"knowledge/_lanes.json: {e}" for e in errs)
        return
    for lane in lanes:
        body = json.dumps(lane, indent=1, ensure_ascii=False, sort_keys=True)
        records.append(rec(f"lane:{lane['id']}", "lane", "knowledge/_lanes.json", 1,
                           f"{lane['id']} · {lane.get('name', '')} · state={lane.get('state', '?')}",
                           body))


# --------------------------------------------------------------- open contracts
def parse_sections(records, errors, relpath, prefix, kind, heading_re=H2_RE):
    lines = read_lines(relpath, errors)
    if lines is None:
        return
    marks = [i for i, ln in enumerate(lines) if heading_re.match(ln)]
    if not marks:
        records.append(rec(f"{prefix}:ALL", kind, relpath, 1, head_of(lines),
                           "\n".join(lines)))
        return
    if marks[0] > 0:
        body = "\n".join(lines[: marks[0]])
        records.append(rec(f"{prefix}:HDR", kind, relpath, 1, head_of(body), body))
    for n, i in enumerate(marks):
        end = marks[n + 1] if n + 1 < len(marks) else len(lines)
        title = lines[i].lstrip("# ").strip()
        records.append(rec(f"{prefix}:{slug(title)}", kind, relpath, i + 1, title[:140],
                           "\n".join(lines[i:end])))


def parse_file_per_record(records, errors, pattern, prefix, kind):
    paths = sorted(globlib.glob(os.path.join(ROOT, pattern)))
    if not paths:
        errors.append(f"{pattern}: glob matched ZERO files — corpus contract broken, refuse")
        return
    for p in paths:
        rel = os.path.relpath(p, ROOT)
        with open(p, encoding="utf-8") as f:
            body = f.read()
        stem = os.path.splitext(os.path.basename(p))[0]
        records.append(rec(f"{prefix}:{stem}", kind, rel, 1, head_of(body), body))


RUNBOOK_HEADING_RE = re.compile(r"^###?\s")


def build_records():
    records, errors = [], []
    parse_gm_ls(records, errors)
    parse_sections(records, errors, "_GM-ARCHIVE.md", "gm-archive", "gm-archive-section")
    parse_sections(records, errors, "_LIVE-STATE-ARCHIVE.md", "ls-archive", "ls-archive-section")
    parse_sections(records, errors, "notes/_MEMENTO-DECISIONS.md", "ledger", "ledger-section")
    parse_gauge(records, errors)
    parse_file_per_record(records, errors, "notes/_briefs/*.md", "brief", "brief")
    parse_file_per_record(records, errors, "notes/_dream/*.md", "dream", "dream")
    for rb in RUNBOOKS:
        stem = os.path.splitext(os.path.basename(rb))[0].replace("_RUNBOOK-", "")
        parse_sections(records, errors, rb, f"runbook:{stem}", "runbook-section",
                       heading_re=RUNBOOK_HEADING_RE)
    parse_lanes(records, errors)
    if errors:
        return None, errors
    kinds = {r["kind"] for r in records}
    expected = {"gm-section", "ls-section", "gm-archive-section", "ls-archive-section",
                "ledger-section", "gauge-block", "brief", "dream", "runbook-section", "lane"}
    missing = expected - kinds
    if missing:
        return None, [f"source class contributed ZERO records: {sorted(missing)} — refuse "
                      f"(an empty class is a broken parser, not a quiet corpus)"]
    records.sort(key=lambda r: (r["file"], r["line"], r["id"]))
    _dedupe(records)
    return records, []


def render(records):
    payload = {
        "$generated_by": "knowledge/_build_memento_index.py — never hand-edit; "
                         "regenerated every build (O2′ #25)",
        "records": records,
    }
    return json.dumps(payload, indent=1, ensure_ascii=False, sort_keys=True) + "\n"


# ------------------------------------------------------------------ selftest
def selftest():
    fails = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)

    # closed-contract refusals, on string fixtures (no temp files — the sandbox
    # call-boundary lesson: everything in one process)
    global read_lines
    real_read = read_lines
    try:
        recs, errs = [], []
        read_lines = lambda rp, e: ["#### 2026-07-27 #6", "b", "#### not-a-date"]  # noqa: E731
        parse_gauge(recs, errs)
        bite("gauge: malformed `#### ` REFUSES", any("outside" in e for e in errs))
        recs, errs = [], []
        read_lines = lambda rp, e: ["preamble only, no blocks"]  # noqa: E731
        parse_gauge(recs, errs)
        bite("gauge: zero blocks REFUSES", any("zero gauge blocks" in e for e in errs))
        # archives are OPEN by measured necessity (#25): a stray `## ` heading must NOT
        # refuse — it becomes its own record (moved content is arbitrary by nature)
        recs, errs = [], []
        read_lines = lambda rp, e: ["# t", "## Batch 2026-07-28 #24 — moved", "c",  # noqa: E731
                                    "## ⬛ DO THIS FIRST", "moved queue content"]
        parse_sections(recs, errs, "FIXTURE.md", "gm-archive", "gm-archive-section")
        bite("archive: open split — moved `## ` headings become records, no refusal",
             not errs and len(recs) == 3)  # HDR + 2 sections
    finally:
        read_lines = real_read
    # missing-file refusal through the real reader
    recs3, errs3 = [], []
    read_lines("notes/__no_such_file__.md", errs3)
    bite("missing declared source REFUSES", any("MISSING" in e for e in errs3))
    # id collision suffixing is deterministic
    d = _dedupe([{"id": "a"}, {"id": "a"}, {"id": "a"}])
    bite("collision suffixing deterministic", [r["id"] for r in d] == ["a", "a-2", "a-3"])
    # slug stability
    bite("slug stable", slug("★ #24 — O1′ ENACTED: lanes-as-records!") == "24-o1-enacted-lanes-as-records")
    # the real corpus builds, every class present, and the render is deterministic
    records, errors = build_records()
    bite("real corpus builds clean", records is not None and not errors)
    if records is not None:
        r2, _ = build_records()
        bite("determinism: two builds render identically", render(records) == render(r2))
        bite("real corpus: every source class present",
             {r["kind"] for r in records} >= {"gm-section", "ls-section", "gm-archive-section",
                                             "ls-archive-section", "ledger-section", "gauge-block",
                                             "brief", "dream", "runbook-section", "lane"})
    else:
        print("   (real-corpus errors: %s)" % errors[:3])

    if fails:
        print(f"selftest FAILED — {len(fails)} bite(s): {fails}")
        return 1
    print("selftest OK — closed contracts refuse, open contracts split, build deterministic.")
    return 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    records, errors = build_records()
    if errors:
        print("memento index: REFUSING to write —")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    text = render(records)
    if "--check" in sys.argv:
        if not os.path.exists(OUT_PATH):
            print("memento index --check: index file missing — run the build")
            return 1
        with open(OUT_PATH, encoding="utf-8") as f:
            on_disk = f.read()
        if on_disk != text:
            print("memento index --check: STALE — regenerate (the index on disk does not "
                  "match the corpus; never hand-edit it)")
            return 1
        print(f"memento index --check: current ({len(records)} records)")
        return 0
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    kinds = {}
    for r in records:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(f"memento index: {len(records)} records → {os.path.relpath(OUT_PATH, ROOT)} "
          f"({', '.join(f'{k}:{v}' for k, v in sorted(kinds.items()))})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
