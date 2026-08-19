#!/usr/bin/env python3
"""_promote.py — the TWICE-CAUGHT promotion rule, as code (W-45, `s204-D1` item 2).

THE RULE, from the programme brief verbatim: *"a probe that catches a real defect TWICE (two
sessions, receipts named) becomes a CANDIDATE `_build_all.py` gate — candidature recorded in
`_DS-IMPROVEMENTS.md`, promotion itself remains governed by derivation governance (Dave
promotes)."*

WHAT THIS TOOL DOES: reads the registry manifest's `caught:` ledger, counts DISTINCT SESSIONS
per probe, and emits ready-to-paste candidature text for `knowledge/_DS-IMPROVEMENTS.md`.

⛔ WHAT IT DOES NOT DO, and this is the point:
  · it NEVER writes `_DS-IMPROVEMENTS.md` — output is stdout. Promotion is DAVE'S under
    derivation governance; a tool that wrote the register would be making the decision.
  · it NEVER wires anything into `_build_all.py`.
  · it NEVER counts one session twice. A session that caught a class three times is ONE
    session, because the rule is about INDEPENDENT OCCASIONS, not about volume.

PROVENANCE IS CARRIED INTO THE VERDICT, not laundered out of it. Ledger entries are either
`historical-mined` (the class was caught by a person/agent BEFORE this probe existed; W-45
mined the receipt) or `live-run` (this probe, running, found it). Both count toward two — the
programme brief's evidence is the LEDGER — but every candidature states its basis:
    HISTORICAL-ONLY · MIXED · LIVE
so nobody reads a retrospective pair as two live catches. [[conclusions-are-debt-s129-d5]]

KIND is counted too: `exact` (the same class the probe scans for) vs `species` (a same-species
defect on another surface — e.g. #204's `--x: var(--x)` CYCLE is the #184 silent-black species
but not the same scan). DEFAULT COUNTS EXACT ONLY. `--include-species` widens it and SAYS SO in
the output, because a species-widened count is a weaker claim and must not travel as the strict
one.

USAGE
  python3 knowledge/_probe_registry/_promote.py                 # candidates (exact only)
  python3 knowledge/_probe_registry/_promote.py --include-species
  python3 knowledge/_probe_registry/_promote.py --all           # every probe, candidate or not
  python3 knowledge/_probe_registry/_promote.py --selftest
EXIT: 0 always for a report (a candidate is NEWS, not a failure) · 1 selftest failure or an
unparseable manifest.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json, os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _registry as REG  # noqa: E402

THRESHOLD = 2  # "TWICE" — the programme brief's word, not a tunable this tool may reinterpret


def assess(row, include_species=False):
    """(is_candidate, sessions, basis, counted_entries) for one probe row."""
    entries = [c for c in row["caught"]
               if include_species or c.get("kind") == "exact"]
    sessions = sorted({c["session"] for c in entries})
    provs = {c["provenance"] for c in entries}
    basis = ("LIVE" if provs == {"live-run"} else
             "HISTORICAL-ONLY" if provs == {"historical-mined"} else
             "MIXED" if provs else "NONE")
    return len(sessions) >= THRESHOLD, sessions, basis, entries


def candidature_text(row, sessions, basis, entries, include_species):
    lines = []
    lines.append("### ds-XXX — CANDIDATE GATE: %s (probe `%s`)" % (row["klass"], row["id"]))
    lines.append("")
    lines.append("**Status:** CANDIDATE, not promoted. Emitted by "
                 "`knowledge/_probe_registry/_promote.py` from the registry ledger. "
                 "**Promotion into `_build_all.py` is Dave's** (derivation governance); this "
                 "text is evidence, not canon.")
    lines.append("")
    lines.append("**Rule satisfied:** caught in %d distinct session(s) %s — threshold is %d. "
                 "**Evidence basis: %s.**%s"
                 % (len(sessions), sessions, THRESHOLD, basis,
                    "  ⚠ SPECIES-WIDENED COUNT (`--include-species`): some entries are "
                    "same-species defects on other surfaces, not the same scan."
                    if include_species else ""))
    lines.append("")
    lines.append("**Probe:** `knowledge/_probe_registry/%s` · environment `%s`"
                 % (row["script"], row["environment"]))
    lines.append("")
    lines.append("**Receipts (named, probeable):**")
    for c in sorted(entries, key=lambda c: (c["session"], c["date"])):
        lines.append("- #%s %s · %s — `%s` *(%s, %s)*"
                     % (c["session"], c["date"], c["defect"], c["receipt"],
                        c["provenance"], c["kind"]))
    lines.append("")
    lines.append("**What the probe CANNOT see (publish it with the candidature, never after):** "
                 + row["blind"])
    if row.get("note"):
        lines.append("")
        lines.append("**Note:** " + row["note"])
    lines.append("")
    lines.append("**Blast radius if promoted:** one more gate in the chain; the environment line "
                 "above says where it can pass — a gate that cannot pass in the environment it "
                 "runs in is a defect, not rigour (#173).")
    return "\n".join(lines)


def report(rows, include_species=False, show_all=False):
    cands = []
    print("TWICE-CAUGHT ASSESSMENT (threshold=%d distinct session(s), %s)"
          % (THRESHOLD, "EXACT + SPECIES" if include_species else "EXACT kind only"))
    print("%-5s %-9s %-16s %-42s %s" % ("id", "candidate", "sessions", "class", "basis"))
    for row in rows:
        ok, sessions, basis, entries = assess(row, include_species)
        print("%-5s %-9s %-16s %-42s %s" % (row["id"], "YES" if ok else "no",
                                            ",".join(str(s) for s in sessions) or "—",
                                            row["klass"][:42], basis))
        if ok or show_all:
            cands.append((row, sessions, basis, entries, ok))
    print("\n" + "=" * 78)
    if not any(ok for *_x, ok in cands):
        print("No probe meets the twice-caught rule today. Nothing to propose — an absent "
              "candidate is a finding too (promotion by evidence, never speculation).")
    for row, sessions, basis, entries, ok in cands:
        print("\n" + "-" * 78)
        print("%s— CANDIDATURE TEXT for knowledge/_DS-IMPROVEMENTS.md (NOT WRITTEN BY THIS "
              "TOOL; paste is Dave's or the conductor's call)\n"
              % ("" if ok else "[BELOW THRESHOLD — shown by --all only] "))
        print(candidature_text(row, sessions, basis, entries, include_species))
    return 0


# ---- selftest: drive the rule on synthetic ledgers, both directions -----------------------

def _row(pid, caught):
    return {"id": pid, "klass": "k", "title": "t", "script": "_promote.py",
            "environment": "sandbox", "blind": "b", "caught": caught}


def _c(session, prov="historical-mined", kind="exact"):
    return {"session": session, "date": "2026-08-19", "defect": "d",
            "receipt": "knowledge/_probe_registry/_promote.py", "provenance": prov, "kind": kind}


def selftest():
    fails = []
    cases = [
        ("one session, twice",     _row("A", [_c(204), _c(204)]),               False, False),
        ("two sessions",           _row("B", [_c(204), _c(206)]),               True,  False),
        ("empty ledger",           _row("C", []),                               False, False),
        ("two, but one species",   _row("D", [_c(204), _c(206, kind="species")]), False, False),
        ("two, species included",  _row("E", [_c(204), _c(206, kind="species")]), True,  True),
    ]
    for label, row, want, species in cases:
        got, sessions, basis, _e = assess(row, include_species=species)
        if got != want:
            fails.append("RULE WRONG (%s): expected candidate=%s, got %s (sessions=%s)"
                         % (label, want, got, sessions))
        else:
            print("  ✅ %-24s candidate=%-5s sessions=%s basis=%s" % (label, got, sessions, basis))

    # provenance must reach the OUTPUT, or a mined receipt reads as a live catch
    row = _row("F", [_c(204), _c(206, prov="live-run")])
    ok, sessions, basis, entries = assess(row)
    txt = candidature_text(row, sessions, basis, entries, False)
    if basis != "MIXED" or "MIXED" not in txt:
        fails.append("PROVENANCE LAUNDERED: basis=%r and the emitted text does not say it" % basis)
    else:
        print("  ✅ provenance survives into the candidature text (basis=MIXED)")
    if "historical-mined" not in txt or "live-run" not in txt:
        fails.append("PROVENANCE LAUNDERED: per-entry provenance missing from the receipt list")
    else:
        print("  ✅ each receipt line carries its own provenance and kind")

    # the tool must not write anything — proven by driving it in a read-only-ish sandbox check
    before = os.path.getmtime(os.path.join(REG.ROOT, "knowledge", "_DS-IMPROVEMENTS.md"))
    report([_row("G", [_c(204), _c(206)])])
    after = os.path.getmtime(os.path.join(REG.ROOT, "knowledge", "_DS-IMPROVEMENTS.md"))
    if before != after:
        fails.append("THE TOOL WROTE _DS-IMPROVEMENTS.md — promotion is Dave's, not a script's")
    else:
        print("  ✅ _DS-IMPROVEMENTS.md untouched by a full report run (mtime unchanged)")

    # and it must survive the LIVE manifest
    rows, defects = REG.load()
    if defects:
        REG.report_defects(defects, "LIVE manifest")
        fails.append("LIVE MANIFEST UNPARSEABLE — the promotion rule cannot be trusted on it")
    else:
        n = sum(1 for r in rows if assess(r)[0])
        print("  ✅ live manifest: %d probe(s), %d meeting the twice-caught rule (exact only)"
              % (len(rows), n))

    if fails:
        print("⛔ _promote selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ _promote selftest PASS — the rule counts DISTINCT sessions, refuses one-session "
          "doubles, keeps species out unless asked, carries provenance into the output, and "
          "writes nothing.")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    rows, defects = REG.load()
    residual = REG.report_defects(defects, "manifest.jsonl")
    rc = report(rows, include_species="--include-species" in argv, show_all="--all" in argv)
    sys.exit(rc or (1 if residual else 0))
