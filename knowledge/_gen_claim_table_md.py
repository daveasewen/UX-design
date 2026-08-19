#!/usr/bin/env python3
"""_gen_claim_table_md.py — the human render, GENERATED FROM the JSONL (W-44, `s204-D1` leg 4).

WHY IT EXISTS: `s204-D1` prices this explicitly — "markdown human-readable renders are
generated FROM the JSONL, never hand-kept beside it (write-once, ADR-0017)". A hand-kept
markdown twin of a JSONL is two homes for one live fact; the second one rots and then briefs
somebody. This script is the only legal way a claim/challenge table becomes prose.

It emits a HEADER STAMP naming the source JSONL and this script, so a reader who finds the
markdown alone knows it is derived and where to edit. It also emits the generated tag/verdict
tallies — a typed count lies; these are computed from the rows (`_state.counts` precedent, #88).

USAGE
  python3 knowledge/_gen_claim_table_md.py <rows.jsonl> --out <table.md> [--title "..."]
  python3 knowledge/_gen_claim_table_md.py <rows.jsonl> --stdout
  python3 knowledge/_gen_claim_table_md.py --selftest

Rows are grouped by their optional `section` field, in first-appearance order; rows with no
`section` land in a trailing "Ungrouped" block rather than being dropped — a row with a missing
optional field must never vanish from the render.

Parse failures are LOUD, NAMED, and make the render REFUSE (rc=1) rather than emit a table that
silently describes a subset. A partial render that looks complete is the worse artefact.

CONSUMER at birth: the PM-wave receipts. Declared: NOT wired into `_build_all.py` or CI.

Selftest: plants a defect (a row whose `section` is missing, a row that will not parse) and
proves the render names it / keeps it; removal goes green.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate, write_gate as _write_gate
_help_gate(__doc__, __name__, __file__)
_write_gate(__file__, writes="the --out markdown table", name=__name__)

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _claimtable as CT

UNGROUPED = "Ungrouped (no `section` field — kept, never dropped)"


def _cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def render(rows, source, title=None):
    kinds = {r["kind"] for r in rows}
    is_claim = "claim" in kinds
    L = []
    L.append("# " + (title or "Claim/challenge table"))
    L.append("")
    L.append("*⛔ **GENERATED — DO NOT HAND-EDIT.** Source of truth: `%s`. Regenerate with*"
             % source)
    L.append("*`python3 knowledge/_gen_claim_table_md.py %s --out <this file>`.*" % source)
    L.append("*Write-once, ADR-0017: one home for the live facts, this file is an address.*")
    L.append("")
    if is_claim:
        tally = {t: sum(1 for r in rows if r.get("tag") == t) for t in CT.TAGS}
    else:
        tally = {v: sum(1 for r in rows if r.get("verdict") == v) for v in CT.VERDICTS}
    L.append("**Generated tally (%d row(s)):** " % len(rows)
             + " · ".join("%s %d" % (k, v) for k, v in tally.items()))
    fenced = [r for r in rows if r.get("fence")]
    if fenced:
        L.append("")
        L.append("**Fence touches: %d** — `%s`" % (len(fenced), "`, `".join(r["id"] for r in fenced)))
    order, groups = [], {}
    for r in rows:
        s = r.get("section") or UNGROUPED
        if s not in groups:
            groups[s] = []
            order.append(s)
        groups[s].append(r)
    if UNGROUPED in order:            # trailing, but present
        order = [s for s in order if s != UNGROUPED] + [UNGROUPED]
    head = ("| id | claim | evidence pointer | tag | note |" if is_claim
            else "| id | verdict statement | evidence | verdict | note |")
    for s in order:
        L.append("")
        L.append("## " + s)
        L.append("")
        L.append(head)
        L.append("|---|---|---|---|---|")
        for r in groups[s]:
            note = " ".join(x for x in [("⛔ FENCE: " + r["fence"]) if r.get("fence") else "",
                                        r.get("note", "")] if x)
            L.append("| `%s` | %s | %s | **%s** | %s |" % (
                r["id"], _cell(r["claim"]), _cell(r["evidence"]),
                r.get("tag") or r.get("verdict"), _cell(note) or "—"))
    L.append("")
    return "\n".join(L)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    prev = None
    for a in argv:
        if prev in ("--out", "--title"):
            args = [x for x in args if x != a]
        prev = a
    if len(args) != 1:
        sys.stderr.write("✖ REFUSED: need exactly one <rows.jsonl>; got %r\n" % (args,))
        return 2
    src = args[0]
    rows, defects = CT.load(src)
    if CT.report_defects(defects, src):
        print("⛔ REFUSING TO RENDER — a partial table that looks complete is the worse artefact.")
        return 1
    title = argv[argv.index("--title") + 1] if "--title" in argv else None
    text = render(rows, src, title)
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print("✅ generated %s from %s (%d row(s))" % (out, src, len(rows)))
    else:
        print(text)
    return 0


def selftest():
    import tempfile
    fails = []
    tmp = tempfile.mkdtemp(prefix="genclaim-selftest-")
    good = [{"id": "A-1", "kind": "claim", "claim": "a", "evidence": "`ls`", "tag": "PROVEN",
             "section": "S1"},
            {"id": "A-2", "kind": "claim", "claim": "b|pipe", "evidence": "`ls`",
             "tag": "UNPROVEN", "fence": "declared stop"}]
    p = os.path.join(tmp, "ok.jsonl")
    with open(p, "w") as f:
        for o in good:
            f.write(json.dumps(o) + "\n")
    rows, _ = CT.load(p)
    text = render(rows, p, "T")

    # direction 1 — PLANT: a row with no `section` must NOT disappear
    if "A-2" not in text or UNGROUPED not in text:
        fails.append("DROPPED ROW: the section-less row A-2 is absent from the render")
    else:
        print("  ✅ plant caught: a row with no `section` is kept in a trailing group, not dropped")
    if "b\\|pipe" not in text:
        fails.append("TABLE BROKEN: a pipe in a cell was not escaped — the markdown table splits")
    else:
        print("  ✅ pipe in a cell is escaped (the render cannot be corrupted by content)")
    if "GENERATED — DO NOT HAND-EDIT" not in text or p not in text:
        fails.append("NO PROVENANCE STAMP: the render does not name its source JSONL")
    else:
        print("  ✅ provenance stamp names the source JSONL and the regenerate command")
    if "PROVEN 1" not in text or "UNPROVEN 1" not in text:
        fails.append("TALLY WRONG: generated tally does not match the rows")
    else:
        print("  ✅ tally is generated from the rows, not typed")
    if "Fence touches: 1" not in text:
        fails.append("FENCE INVISIBLE: a fenced row is not called out in the header")
    else:
        print("  ✅ fence touch surfaced in the header")

    # direction 1b — PLANT an unparseable row: the render must REFUSE
    bad = os.path.join(tmp, "bad.jsonl")
    with open(bad, "w") as f:
        f.write(json.dumps(good[0]) + "\n{BROKEN\n")
    if main([bad, "--stdout"]) != 1:
        fails.append("PARTIAL RENDER: an unparseable row did not make the render refuse")
    else:
        print("  ✅ plant caught: an unparseable row makes the render REFUSE (rc=1)")

    # direction 2 — REMOVE: the clean file renders green
    out = os.path.join(tmp, "out.md")
    if main([p, "--out", out]) != 0 or not os.path.exists(out):
        fails.append("REMOVAL NOT GREEN: the clean file did not render")
    else:
        print("  ✅ removal green: the clean file renders to %d bytes" % os.path.getsize(out))

    if fails:
        print("⛔ _gen_claim_table_md selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ _gen_claim_table_md selftest PASS — both directions.")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
