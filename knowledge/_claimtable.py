#!/usr/bin/env python3
"""_claimtable.py — the claim/challenge JSONL SCHEMA and its loud loader (W-44, `s204-D1` item 1).

THE CLASS this serves: at #204 the build-PM's claim table and the verifier's challenge table
were two prose documents. The conductor had to read both and hold the correspondence in its
head; the build-PM died before writing its table and a finisher reconstructed it — one lossy
hop. Prose cannot be joined. This module gives both tables ONE schema so a script can.

THE SCHEMA (one JSONL row = one object; `kind` selects the row's dialect):

  REQUIRED, both kinds
    id        str   — the join key. Unique within a file. A challenge row's id names the
                      claim row it answers; an id with no claim counterpart is a NEW finding.
    kind      str   — "claim" | "challenge"
    claim     str   — the assertion (claim rows) or the verdict statement (challenge rows)
    evidence  str   — the PROBEABLE TOKEN per `s182-D1`: a command, a path, or a figure that
                      can be re-run or re-read. Prose alone is a lint failure, not a parse one.

  REQUIRED, kind-specific
    tag       str   — claim rows ONLY: PROVEN | MEASURED | CLAIMED | UNPROVEN
    verdict   str   — challenge rows ONLY: CONFIRMED | CONTRADICTED | UNTESTED | NEW

  OPTIONAL, both kinds
    note      str   — FREE TEXT, deliberately unconstrained. The spec prices this: "a schema
                      too tight forces prose back into chat" (the honest-refusal vocabulary
                      class). Anything the schema has no field for goes here and SURVIVES.
    fence     str   — names a fence this row touches (a declared stop, a DO-NOT-RULE item, a
                      licence boundary). ANY row with `fence` set surfaces in the join, even a
                      CONFIRMED one — a fence touch is never collapsed into a count.
    rc        int   — the exit code the evidence command is DECLARED to produce. The evidence
                      linter's sampler compares a re-run's rc against this.
    expect_stdout_contains  str — ⛔ #208, THE EXIT-CODE-BLINDNESS FIX (schema change BY
                      ADDITION — every pre-#208 row is still legal and behaves exactly as
                      before). `rc` alone proves RUNNABILITY, not REPRODUCTION: `git show`,
                      `grep -c`, `find`, `ls`, `sed -n` all exit 0 for ANY content, so the
                      #208 verifier wave watched `EVIDENCE GATE PASS` certify two rows whose
                      content it had just proved false. When THIS field is present the
                      sampler additionally requires the substring in the command's STDOUT —
                      an OBSERVATION, not an exit code.
    expect_count            int — same fix, counting dialect: the last non-empty stdout line
                      must parse as this integer (`grep -c`, `wc -l`, `git rev-list --count`).
                      An unparseable line is a LOUD failure, never a pass.
    section   str   — the human grouping the row came from (render only; never joined on).
    lane      str   — the wave lane the row belongs to (render only; never joined on).

  ⛔ UNKNOWN KEYS ARE A PARSE FAILURE, not a silent drop. A typo'd field name that vanished
  quietly would be a row nobody decided to lose — the same defect the join is built to prevent.

FAILURE IS LOUD AND NAMED (`a-crash-is-not-a-fail`): every unparseable line is reported with
its file, line number and reason; the loader NEVER skips a line silently, and every consumer
prints a RESIDUAL count. A helper that returns fewer rows than the file has lines, without
saying so, is the whole class this repo keeps re-finding.

CONSUMER at birth: `_join_claim_tables.py`, `_validate_evidence.py`, `_gen_claim_table_md.py`.
✅ #208: the `s204-D1` precondition was met by the #208 verifier wave and Dave ruled the wiring,
so this schema is now read on every build and in CI via `_validate_evidence.py`.

Selftest: `python3 knowledge/_claimtable.py --selftest` — plants one defect of each parse
class and proves the loader names it, then proves removing the defect goes green.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json, sys, os

TAGS = ("PROVEN", "MEASURED", "CLAIMED", "UNPROVEN")
VERDICTS = ("CONFIRMED", "CONTRADICTED", "UNTESTED", "NEW")
KINDS = ("claim", "challenge")

COMMON_REQUIRED = ("id", "kind", "claim", "evidence")
OPTIONAL = ("note", "fence", "rc", "section", "lane",
            # #208 expected-OBSERVATION fields (see the docstring). BY ADDITION: a row without
            # them samples exactly as it did before, so the four 208-* tables stay legal.
            "expect_stdout_contains", "expect_count")
ALLOWED = set(COMMON_REQUIRED) | set(OPTIONAL) | {"tag", "verdict"}


class Defect:
    """One named parse failure. Carries WHERE, so nothing is reported as a bare count."""

    def __init__(self, path, lineno, reason, excerpt=""):
        self.path, self.lineno, self.reason, self.excerpt = path, lineno, reason, excerpt

    def __str__(self):
        ex = (" · " + self.excerpt[:110]) if self.excerpt else ""
        return "  ⛔ %s:%d — %s%s" % (self.path, self.lineno, self.reason, ex)


def validate_row(row, path="<mem>", lineno=0):
    """Return [Defect] for one already-decoded object. Empty list == conformant."""
    out = []
    if not isinstance(row, dict):
        return [Defect(path, lineno, "row is %s, not a JSON object" % type(row).__name__)]
    unknown = sorted(set(row) - ALLOWED)
    if unknown:
        out.append(Defect(path, lineno, "unknown field(s) %s — a typo'd field is a lost row, "
                                        "not a silent drop; free text belongs in `note`" % unknown))
    for f in COMMON_REQUIRED:
        if not str(row.get(f, "")).strip():
            out.append(Defect(path, lineno, "missing required field `%s`" % f))
    kind = row.get("kind")
    if kind not in KINDS and "kind" in row:
        out.append(Defect(path, lineno, "kind=%r not one of %s" % (kind, list(KINDS))))
    if kind == "claim":
        if row.get("tag") not in TAGS:
            out.append(Defect(path, lineno, "claim row: tag=%r not one of %s"
                              % (row.get("tag"), list(TAGS))))
        if "verdict" in row:
            out.append(Defect(path, lineno, "claim row carries `verdict` — verdicts are the "
                                            "challenger's word, never the claimant's"))
    elif kind == "challenge":
        if row.get("verdict") not in VERDICTS:
            out.append(Defect(path, lineno, "challenge row: verdict=%r not one of %s"
                              % (row.get("verdict"), list(VERDICTS))))
        if "tag" in row:
            out.append(Defect(path, lineno, "challenge row carries `tag` — tags are the "
                                            "claimant's word, never the challenger's"))
    if "rc" in row and not isinstance(row["rc"], int):
        out.append(Defect(path, lineno, "rc=%r is not an integer exit code" % (row["rc"],)))
    # #208 expected-observation fields. Typed here so a mistyped expectation is a PARSE
    # failure, not a sampler surprise — the sampler must never have to guess what to compare.
    if "expect_count" in row and (isinstance(row["expect_count"], bool)
                                  or not isinstance(row["expect_count"], int)):
        out.append(Defect(path, lineno, "expect_count=%r is not an integer — it is compared "
                                        "against the command's last stdout line"
                          % (row["expect_count"],)))
    if "expect_stdout_contains" in row and not (
            isinstance(row["expect_stdout_contains"], str)
            and row["expect_stdout_contains"].strip()):
        out.append(Defect(path, lineno, "expect_stdout_contains=%r must be a NON-EMPTY string "
                                        "— an empty expectation matches everything, which is "
                                        "the exit-code blindness it exists to fix"
                          % (row.get("expect_stdout_contains"),)))
    if ("expect_stdout_contains" in row or "expect_count" in row) and not row.get("evidence", ""):
        out.append(Defect(path, lineno, "expected-observation field(s) with no `evidence` "
                                        "command to observe"))
    for f in ("note", "fence", "section", "lane"):
        if f in row and not isinstance(row[f], str):
            out.append(Defect(path, lineno, "`%s` must be a string (free text), got %s"
                              % (f, type(row[f]).__name__)))
    return out


def load(path, expect_kind=None):
    """(rows, defects). NEVER skips a line silently — every skipped line IS a defect.

    `expect_kind` (optional) additionally flags rows of the wrong dialect, so a challenge file
    handed to the claim slot fails loudly instead of joining to nothing.

    ID UNIQUENESS IS KIND-AWARE, and this is a real-data finding, not a convenience:
      · CLAIM rows must be unique on `id` — the id IS the claim, and a second row with the
        same id silently shadows the first.
      · CHALLENGE rows MAY repeat an id — a verifier can return more than one verdict on one
        claim, and #204 actually did: `D-7` was CONTRADICTED on its cited figure and CONFIRMED
        on its substance, in two rows. Forcing 1:1 would have required minting a synthetic id
        that joins to nothing, i.e. destroying the fact in order to fit the schema.
    """
    rows, defects, seen = [], [], {}
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            s = raw.strip()
            if not s or s.startswith("//"):
                continue
            try:
                obj = json.loads(s)
            except Exception as e:
                defects.append(Defect(path, lineno, "not valid JSON — %s" % e, s))
                continue
            errs = validate_row(obj, path, lineno)
            if expect_kind and isinstance(obj, dict) and obj.get("kind") not in (None, expect_kind):
                errs.append(Defect(path, lineno, "kind=%r in a file loaded as %r"
                                   % (obj.get("kind"), expect_kind)))
            if errs:
                defects.extend(errs)
                continue
            if obj["id"] in seen and obj.get("kind") != "challenge":
                defects.append(Defect(path, lineno, "duplicate id %r (first seen line %d) — "
                                      "a claim id must be unique or a row is silently shadowed"
                                      % (obj["id"], seen[obj["id"]])))
                continue
            seen[obj["id"]] = lineno
            obj["_lineno"] = lineno
            obj["_src"] = path
            rows.append(obj)
    return rows, defects


def report_defects(defects, label):
    """Print defects loudly and return the residual count. Callers exit non-zero on > 0."""
    if not defects:
        return 0
    print("⛔ %s: %d UNPARSEABLE ROW(S) — declared, never skipped:" % (label, len(defects)))
    for d in defects:
        print(str(d))
    print("   RESIDUAL: %d row(s) are NOT in the analysis below. Any count printed after this "
          "line is a count of the PARSED subset only." % len(defects))
    return len(defects)


# ---- selftest: plant-then-detect, BOTH directions ----------------------------------------------

_GOOD_CLAIM = {"id": "X-1", "kind": "claim", "claim": "the gate is green",
               "evidence": "`python3 knowledge/_validate_icons.py` -> rc=0", "tag": "PROVEN", "rc": 0}
_GOOD_CHAL = {"id": "X-1", "kind": "challenge", "claim": "reproduced",
              "evidence": "`python3 knowledge/_validate_icons.py` -> rc=0", "verdict": "CONFIRMED"}


def _write(tmp, name, objs):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="utf-8") as f:
        for o in objs:
            f.write(json.dumps(o) + "\n" if isinstance(o, dict) else o + "\n")
    return p


def selftest():
    import tempfile, copy
    fails = []
    tmp = tempfile.mkdtemp(prefix="claimtable-selftest-")

    # --- direction 1: PLANT a defect of each class, the loader MUST name it ---
    plants = [
        ("malformed JSON", '{"id": "X-2", "kind": "claim", '),
        ("unknown field", copy.deepcopy(dict(_GOOD_CLAIM, id="X-3", evidenc="typo'd"))),
        ("missing required", {k: v for k, v in _GOOD_CLAIM.items() if k != "evidence"}),
        ("bad tag", dict(_GOOD_CLAIM, id="X-5", tag="PROBABLY")),
        ("verdict on a claim row", dict(_GOOD_CLAIM, id="X-6", verdict="CONFIRMED")),
        ("bad verdict", dict(_GOOD_CHAL, id="X-7", verdict="PROBABLY")),
        ("tag on a challenge row", dict(_GOOD_CHAL, id="X-8", tag="PROVEN")),
        ("non-int rc", dict(_GOOD_CLAIM, id="X-9", rc="zero")),
    ]
    for label, plant in plants:
        p = _write(tmp, "plant.jsonl", [_GOOD_CLAIM, plant] if isinstance(plant, dict)
                   else [json.dumps(_GOOD_CLAIM), plant])
        rows, defects = load(p)
        if not defects:
            fails.append("PLANT NOT CAUGHT: %s — loader returned %d rows, 0 defects"
                         % (label, len(rows)))
        else:
            print("  ✅ plant caught (%s): %s" % (label, defects[0].reason[:80]))

    # duplicate id is its own class (shadowing)
    p = _write(tmp, "dup.jsonl", [_GOOD_CLAIM, dict(_GOOD_CLAIM)])
    rows, defects = load(p)
    if not any("duplicate id" in d.reason for d in defects):
        fails.append("PLANT NOT CAUGHT: duplicate id — a shadowed row is a lost row")
    else:
        print("  ✅ plant caught (duplicate id): shadowing named")

    # ...but a repeated CHALLENGE id is LEGAL — one claim, two verdicts (#204's D-7, real data)
    p = _write(tmp, "dup2.jsonl", [_GOOD_CHAL, dict(_GOOD_CHAL, verdict="CONTRADICTED")])
    rows, defects = load(p, expect_kind="challenge")
    if defects or len(rows) != 2:
        fails.append("REAL-DATA REGRESSION: two verdicts on one claim id were refused (%d rows, "
                     "%d defects) — #204's D-7 is exactly this shape" % (len(rows), len(defects)))
    else:
        print("  ✅ kind-aware uniqueness: one claim id may carry TWO challenge verdicts")

    # wrong dialect in the wrong slot
    p = _write(tmp, "dialect.jsonl", [_GOOD_CHAL])
    rows, defects = load(p, expect_kind="claim")
    if not defects:
        fails.append("PLANT NOT CAUGHT: challenge row loaded as a claim file")
    else:
        print("  ✅ plant caught (wrong dialect): challenge row refused in a claim slot")

    # --- direction 2: REMOVE the defects, the loader MUST go green ---
    p = _write(tmp, "clean.jsonl", [_GOOD_CLAIM, dict(_GOOD_CLAIM, id="X-10", tag="UNPROVEN",
                                                     note="free text survives · unicode ⛔ ok")])
    rows, defects = load(p, expect_kind="claim")
    if defects or len(rows) != 2:
        fails.append("REMOVAL NOT GREEN: clean file gave %d rows, %d defects (expected 2, 0)"
                     % (len(rows), len(defects)))
    else:
        print("  ✅ removal green: the clean file parses to 2 rows, 0 defects")
    if rows and rows[1].get("note", "").endswith("ok"):
        print("  ✅ free-text `note` survives the round trip unmangled (the schema-too-tight price)")
    else:
        fails.append("FREE TEXT LOST: `note` did not survive the round trip")

    if fails:
        print("⛔ _claimtable selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("✅ _claimtable selftest PASS — every planted parse defect is named, and its removal "
          "goes green (both directions).")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else
             (print(__doc__) or 0))
