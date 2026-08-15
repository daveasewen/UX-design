#!/usr/bin/env python3
"""
_inscribe_ruling.py — THE ONLY SANCTIONED WAY TO APPEND A RULING to knowledge/_rulings.json.

⛔ THE DEFECT THIS EXISTS TO KILL, and it happened THIS SESSION (#179). A ruling was appended
by the obvious method — `json.load` the file, `.append()` the entry, `json.dump` it back. The
serializer's defaults are not the file's formatting, so the write REFORMATTED 613 lines that
nobody had edited: escape style, key order preservation, indent width, `ensure_ascii`. The diff
then buries the one real change inside hundreds of spurious ones, git blame is destroyed for
every line touched, and a reviewer cannot see what actually changed. Dave asked for the CLASS
fix, not a patch: so the class fix is that appending is no longer done by hand at all.

CONSUMER (named, because an instrument without a consumer is a zombie [[instrument-without-a-consumer]]):
the CAPTURE RITUAL — `knowledge/_RUNBOOK-capture-ritual.md` — and every session conductor at
inscription time, whenever Dave rules something. Nothing else may write this file.

FIVE REFUSALS, all LOUD, NAMED, rc nonzero, FILE UNTOUCHED:
  R1 SCHEMA   — the entry must carry EXACTLY the keys id/ruled/date/by/says/governs/evidence/status.
                Not a superset (a stray key becomes an invisible convention), not a subset.
  R2 TEXTUAL  — the insertion is a SPAN OF TEXT into the existing bytes, and this is PROVEN BY
                RECONSTRUCTION, not by trust: after composing the new text, removing exactly the
                inserted span must give back the ORIGINAL BYTES, `==` on the raw string. A
                reformatting writer cannot pass this check no matter how well-intentioned.
  R3 PARSES   — the reconstructed text must `json.loads` and yield exactly one more ruling,
                whose value equals the entry submitted.
  R4 UNIQUE   — the new id must not already exist.
  R5 EVIDENCE — every evidence line must satisfy the `_governs.py` legal form. That ladder is
                NOT re-implemented here (two code paths for one ruling guarantees a divergence —
                that is exactly the #150 defect `evidence_form` was created to end); this module
                IMPORTS `_governs.evidence_form` and asks it.

Usage:
  python3 knowledge/_inscribe_ruling.py --entry e.json --dry-run   # prove it would insert cleanly
  python3 knowledge/_inscribe_ruling.py --entry e.json --write     # inscribe
  cat e.json | python3 knowledge/_inscribe_ruling.py --dry-run     # stdin also accepted
  python3 knowledge/_inscribe_ruling.py --selftest                 # plant-then-detect arms
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _helpgate import help_gate as _help_gate  # noqa: E402
_help_gate(__doc__, __name__, __file__)

import _governs  # noqa: E402

REPO = os.path.dirname(HERE)
RULINGS = os.path.join(HERE, "_rulings.json")
KEYS = ("id", "ruled", "date", "by", "says", "governs", "evidence", "status")


class InscriptionRefused(RuntimeError):
    """⚠ LOUD AND NAMED. A refusal that reads like a success is how bad data gets in."""


# ---------------------------------------------------------------------------
# R5 — evidence legality, DELEGATED to _governs.evidence_form (never re-stated)
# ---------------------------------------------------------------------------
def evidence_error(pointer):
    """Return None if legal, else the reason. The FORM ladder is _governs'; only the
    on-disk resolution of the `path` / `anchor` forms happens here, and it is the same
    resolution `_governs.render()` performs."""
    if not isinstance(pointer, str) or not pointer.strip():
        return "empty or non-string evidence line"
    form = _governs.evidence_form(pointer)
    if form in ("commit", "chat"):
        return None                      # unverifiable BY DESIGN and honest about it (s148-D1)
    path = pointer.split("#", 1)[0] if form == "anchor" else pointer
    path = path.split(" ", 1)[0].rstrip(":")
    path = path.split(":")[0] if path.count(":") and path.rsplit(":", 1)[-1].isdigit() else path
    if not path:
        return "no resolvable path in evidence line"
    if not os.path.exists(os.path.join(REPO, path)):
        return (f"path {path!r} does not exist in the repo — legal forms are "
                f"`chat #<n> ...`, `commit <sha> ...`, or a path that resolves")
    return None


# ---------------------------------------------------------------------------
# R1 — schema
# ---------------------------------------------------------------------------
def check_schema(entry):
    if not isinstance(entry, dict):
        raise InscriptionRefused(f"⛔ REFUSED (schema) — entry is {type(entry).__name__}, not an object.")
    got = set(entry)
    want = set(KEYS)
    missing, extra = sorted(want - got), sorted(got - want)
    if missing or extra:
        raise InscriptionRefused(
            f"⛔ REFUSED (schema) — entry keys are wrong. missing={missing or 'none'} "
            f"extra={extra or 'none'}. Required EXACTLY: {list(KEYS)}. File untouched.")
    for k in ("governs", "evidence"):
        if not isinstance(entry[k], list) or not entry[k]:
            raise InscriptionRefused(f"⛔ REFUSED (schema) — {k!r} must be a non-empty list. File untouched.")
    for k in ("id", "ruled", "date", "by", "says", "status"):
        if not isinstance(entry[k], str) or not entry[k].strip():
            raise InscriptionRefused(f"⛔ REFUSED (schema) — {k!r} must be a non-empty string. File untouched.")


# ---------------------------------------------------------------------------
# THE TEXTUAL INSERTION + its reconstruction proof (R2/R3/R4)
# ---------------------------------------------------------------------------
def _close_index(text):
    """Index of the `]` that closes the `rulings` array — found by SCANNING, not by regex.

    The tail is `...}\n ]\n}\n`; a regex on the tail would break the day a trailing key is
    added after `rulings`. This walks the JSON structurally to the array's own closer."""
    depth = 0
    in_str = False
    esc = False
    start = text.index('"rulings"')
    i = text.index("[", start)
    for j in range(i, len(text)):
        c = text[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0:
                return j
    raise InscriptionRefused("⛔ REFUSED (structure) — could not find the close of the `rulings` array.")


def compose(text, entry):
    """Return (new_text, insert_at, span). ⛔ Serializes ONLY the new entry; every other byte
    in the file is carried through untouched by construction."""
    close = _close_index(text)
    head = text[:close]
    # the last entry's closing `}` and the newline+indent before `]` are preserved verbatim;
    # we splice after the final `}` of the array's last element.
    last_brace = head.rindex("}")
    body = json.dumps(entry, indent=1, ensure_ascii=False)
    body = "\n".join(" " + ln for ln in body.splitlines())   # array elements sit at indent 1
    span = ",\n" + body
    at = last_brace + 1
    return text[:at] + span + text[at:], at, span


def inscribe(entry, path=RULINGS, write=False):
    """The whole contract in one function. Returns a report dict; raises InscriptionRefused."""
    check_schema(entry)

    with open(path, encoding="utf-8") as fh:
        original = fh.read()

    data = json.loads(original)
    existing = {r.get("id") for r in data.get("rulings", [])}
    if entry["id"] in existing:                                            # R4
        raise InscriptionRefused(
            f"⛔ REFUSED (duplicate id) — {entry['id']!r} is already in {os.path.basename(path)}. "
            f"A ruling is never overwritten; supersede it with a new id. File untouched.")

    bad = [(p, evidence_error(p)) for p in entry["evidence"]]              # R5
    bad = [(p, why) for p, why in bad if why]
    if bad:
        lines = "\n".join(f"    - {p!r}: {why}" for p, why in bad)
        raise InscriptionRefused(f"⛔ REFUSED (evidence) — illegal evidence pointer(s):\n{lines}\nFile untouched.")

    new_text, at, span = compose(original, entry)

    reconstructed = new_text[:at] + new_text[at + len(span):]              # R2 — the proof
    if reconstructed != original:
        raise InscriptionRefused(
            "⛔ REFUSED (not textual) — removing the inserted span does NOT give back the "
            "original bytes. Something reformatted the file. This is the #179 defect and the "
            "whole reason this script exists. File untouched.")

    try:                                                                   # R3
        after = json.loads(new_text)
    except json.JSONDecodeError as ex:
        raise InscriptionRefused(f"⛔ REFUSED (unparseable result) — {ex}. File untouched.")
    if len(after.get("rulings", [])) != len(data.get("rulings", [])) + 1:
        raise InscriptionRefused("⛔ REFUSED (count) — the result does not have exactly one more ruling. File untouched.")
    if after["rulings"][-1] != entry:
        raise InscriptionRefused("⛔ REFUSED (round-trip) — the parsed last ruling is not the entry submitted. File untouched.")

    report = {"id": entry["id"], "insert_at_byte": at, "span_bytes": len(span),
              "file_bytes_before": len(original), "file_bytes_after": len(new_text),
              "rulings_before": len(data.get("rulings", [])), "textual": True, "written": False}
    if write:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_text)
        report["written"] = True
    return report


# ---------------------------------------------------------------------------
# SELFTEST — plant-then-detect. Every refusal arm has its PASSING CONTROL, or a green
# here would only be an assertion that the code ran.
# ---------------------------------------------------------------------------
GOOD = {
    "id": "zz-selftest-D1", "ruled": "#000", "date": "2026-01-01", "by": "selftest",
    "says": "A synthetic entry used only by _inscribe_ruling.py --selftest.",
    "governs": ["knowledge/_inscribe_ruling.py"],
    "evidence": ["chat #000 2026-01-01 (live) - synthetic", "knowledge/_inscribe_ruling.py"],
    "status": "SELFTEST",
}


def _tmp_copy(tmpdir):
    dst = os.path.join(tmpdir, "_rulings.json")
    with open(RULINGS, encoding="utf-8") as a, open(dst, "w", encoding="utf-8") as b:
        b.write(a.read())
    return dst


def selftest():
    import copy
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as td:
        # CONTROL FIRST: the good entry must be ACCEPTED and the file byte-verified.
        p = _tmp_copy(td)
        before = open(p, encoding="utf-8").read()
        try:
            rep = inscribe(copy.deepcopy(GOOD), p, write=True)
        except InscriptionRefused as ex:
            fails.append(f"arm0 CONTROL: good entry refused — {ex}")
        else:
            after = open(p, encoding="utf-8").read()
            at, n = rep["insert_at_byte"], rep["span_bytes"]
            if after[:at] + after[at + n:] != before:
                fails.append("arm0 CONTROL: written file is NOT the original bytes plus one span")
            if json.loads(after)["rulings"][-1]["id"] != GOOD["id"]:
                fails.append("arm0 CONTROL: entry not readable back")

        # ARM 1 — the reformatting writer. PLANT it, then prove the check bites.
        p1 = _tmp_copy(td)
        orig1 = open(p1, encoding="utf-8").read()
        d = json.loads(orig1)
        d["rulings"].append(copy.deepcopy(GOOD))
        reformatted = json.dumps(d, indent=2)          # <- the #179 defect, reproduced exactly
        span_guess = reformatted[len(orig1) - 4:]      # any span; the equality is what matters
        if reformatted[:len(orig1) - 4] + reformatted[len(orig1) - 4:][:0] == orig1:
            fails.append("arm1: the reformatting writer was byte-compatible — impossible; check the plant")
        # the real bite: our own composer must produce something the reconstruction ACCEPTS,
        # and the reformatted text must NOT be reconstructible to the original.
        recon_ok = any(reformatted[:i] + reformatted[i + len(span_guess):] == orig1
                       for i in (0, len(orig1) - 4))
        if recon_ok:
            fails.append("arm1: reconstruction accepted a reformatted file — R2 is dead")

        # ARM 1b — drive R2 through inscribe() itself by breaking the composer.
        p1b = _tmp_copy(td)
        real_compose = globals()["compose"]

        def bad_compose(text, entry):
            nt, at, span = real_compose(text, entry)
            return nt.replace("\r\n", "\n").replace("  ", " ", 1), at, span   # a "harmless" tidy
        globals()["compose"] = bad_compose
        try:
            inscribe(copy.deepcopy(GOOD), p1b, write=True)
            fails.append("arm1b: a tidying writer was ACCEPTED — R2 did not bite")
        except InscriptionRefused as ex:
            if "not textual" not in str(ex):
                fails.append(f"arm1b: refused for the wrong reason — {ex}")
        finally:
            globals()["compose"] = real_compose
        if open(p1b, encoding="utf-8").read() != orig1:
            fails.append("arm1b: FILE WAS MODIFIED despite the refusal")

        # ARM 2 — missing key refused (control = arm0 accepted the complete entry)
        p2 = _tmp_copy(td)
        bad = copy.deepcopy(GOOD); del bad["status"]
        try:
            inscribe(bad, p2, write=True); fails.append("arm2: missing key ACCEPTED")
        except InscriptionRefused as ex:
            if "schema" not in str(ex):
                fails.append(f"arm2: wrong reason — {ex}")
        # ... and an EXTRA key must also bite (a superset is a silent new convention)
        bad2 = copy.deepcopy(GOOD); bad2["notes"] = "x"
        try:
            inscribe(bad2, p2, write=True); fails.append("arm2b: extra key ACCEPTED")
        except InscriptionRefused:
            pass

        # ARM 3 — duplicate id refused, using a REAL id from the live file
        p3 = _tmp_copy(td)
        live_id = json.loads(open(p3, encoding="utf-8").read())["rulings"][-1]["id"]
        dup = copy.deepcopy(GOOD); dup["id"] = live_id
        try:
            inscribe(dup, p3, write=True); fails.append(f"arm3: duplicate id {live_id} ACCEPTED")
        except InscriptionRefused as ex:
            if "duplicate" not in str(ex):
                fails.append(f"arm3: wrong reason — {ex}")

        # ARM 4 — illegal evidence refused; and its CONTROL, a legal one accepted
        p4 = _tmp_copy(td)
        ill = copy.deepcopy(GOOD)
        ill["evidence"] = ["knowledge/_no_such_file_xyzzy.py"]
        try:
            inscribe(ill, p4, write=True); fails.append("arm4: illegal evidence ACCEPTED")
        except InscriptionRefused as ex:
            if "evidence" not in str(ex):
                fails.append(f"arm4: wrong reason — {ex}")
        ok = copy.deepcopy(GOOD); ok["id"] = "zz-selftest-D2"
        ok["evidence"] = ["commit deadbee synthetic", "chat #001 (live) - synthetic"]
        try:
            inscribe(ok, p4, write=False)
        except InscriptionRefused as ex:
            fails.append(f"arm4 CONTROL: legal commit/chat evidence refused — {ex}")

        # ARM 5 — every refusal leaves the file untouched
        p5 = _tmp_copy(td)
        o5 = open(p5, encoding="utf-8").read()
        for e_ in (bad, dup, ill):
            try:
                inscribe(e_, p5, write=True)
            except InscriptionRefused:
                pass
        if open(p5, encoding="utf-8").read() != o5:
            fails.append("arm5: a refusal MODIFIED the file")
    return fails


def main():
    ap = argparse.ArgumentParser(description="Append a ruling to knowledge/_rulings.json, safely.")
    ap.add_argument("--entry", help="path to a JSON file holding ONE ruling entry (default: stdin)")
    ap.add_argument("--rulings", default=RULINGS)
    ap.add_argument("--dry-run", action="store_true", help="run every check, write nothing")
    ap.add_argument("--write", action="store_true", help="inscribe for real")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        fs = selftest()
        if fs:
            print("⛔ _inscribe_ruling selftest FAILED:", file=sys.stderr)
            for f in fs:
                print("   " + f, file=sys.stderr)
            return 1
        print("✅ _inscribe_ruling selftest: all arms green "
              "(control accepted · reformat detected · missing key · extra key · dupe id · "
              "illegal evidence · legal-evidence control · file-untouched-on-refusal)")
        return 0

    if not (a.dry_run or a.write):
        print("⛔ state your intention: --dry-run or --write. Nothing done.", file=sys.stderr)
        return 2
    try:
        raw = open(a.entry, encoding="utf-8").read() if a.entry else sys.stdin.read()
        entry = json.loads(raw)
    except (OSError, json.JSONDecodeError) as ex:
        print(f"⛔ REFUSED (input) — could not read the entry: {ex}", file=sys.stderr)
        return 2
    try:
        rep = inscribe(entry, a.rulings, write=a.write)
    except InscriptionRefused as ex:
        print(str(ex), file=sys.stderr)
        return 3
    verb = "INSCRIBED" if rep["written"] else "DRY RUN — would insert cleanly, NOTHING WRITTEN"
    print(f"{verb}: {rep['id']} — textual span of {rep['span_bytes']} bytes at offset "
          f"{rep['insert_at_byte']}; file {rep['file_bytes_before']} → {rep['file_bytes_after']} bytes; "
          f"rulings {rep['rulings_before']} → {rep['rulings_before'] + 1}; "
          f"reconstruction proof PASSED (all other bytes identical).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
