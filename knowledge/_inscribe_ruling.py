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
  R6 ROLLING  — s177-D1: an evidence pointer into a file the capture ritual ROLLS is INVALID ON
                ARRIVAL. Point at the commit or the chat; those do not roll. The rolling-file
                list and the classifier live in `_governs.ROLLING_FILES` / `rolling_target()`
                and are NOT restated here — same one-place discipline as R5. ⛔ SCOPE: arrival
                only. Nothing already in `_rulings.json` is re-judged, because eleven such
                entries are RATIFIED RECORD and re-judging them by machine is exactly the
                re-stamp this project refuses. Built #183; QUEUED at #177 under `s172-D3`(e).
  R5 EVIDENCE — every evidence line must satisfy the `_governs.py` legal form. That ladder is
                NOT re-implemented here (two code paths for one ruling guarantees a divergence —
                that is exactly the #150 defect `evidence_form` was created to end); this module
                IMPORTS `_governs.evidence_form` and asks it.

Usage:
  python3 knowledge/_inscribe_ruling.py --entry e.json --dry-run   # prove it would insert cleanly
  python3 knowledge/_inscribe_ruling.py --entry e.json --write     # inscribe
  cat e.json | python3 knowledge/_inscribe_ruling.py --dry-run     # stdin also accepted
  python3 knowledge/_inscribe_ruling.py --selftest                 # plant-then-detect arms
  # AMEND (sanctioned #193, evidence array ONLY — `says` is unreachable from here):
  echo '["commit abc1234 - …"]' | python3 knowledge/_inscribe_ruling.py \
        --amend-evidence --id s176-D2 --dry-run
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


def _entry_span(text, rid):
    """(start, end) of the ONE ruling object whose `"id"` is `rid`, found by SCANNING.

    ⚠ The `"id": "<rid>"` literal is matched, then the enclosing `{` is walked back to and the
    object's own `}` is walked forward to with a string-aware depth scan — the same discipline
    as `_close_index`. A regex over a JSON object is how a nested brace eats a file."""
    needle = f'"id": "{rid}"'
    hits = [i for i in range(len(text)) if text.startswith(needle, i)]
    if len(hits) != 1:
        raise InscriptionRefused(
            f"⛔ REFUSED (target) — {rid!r} appears {len(hits)} times as an `id` in "
            f"{os.path.basename(RULINGS)}; amendment needs EXACTLY one target. File untouched.")
    start = text.rindex("{", 0, hits[0])
    depth = 0
    in_str = False
    esc = False
    for j in range(start, len(text)):
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
                return start, j + 1
    raise InscriptionRefused(f"⛔ REFUSED (structure) — could not find the close of ruling {rid!r}.")


def _evidence_span(text, rid):
    """(start, end) of the `[...]` that is ruling `rid`'s evidence array, in FILE coordinates."""
    lo, hi = _entry_span(text, rid)
    obj = text[lo:hi]
    key = obj.index('"evidence"')
    i = obj.index("[", key)
    depth = 0
    in_str = False
    esc = False
    for j in range(i, len(obj)):
        c = obj[j]
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
                return lo + i, lo + j + 1
    raise InscriptionRefused(f"⛔ REFUSED (structure) — could not find {rid!r}'s evidence array.")


def check_evidence_list(evidence, what="evidence"):
    """R1/R5/R6 for a bare evidence array — shared by append and amend so the two paths cannot
    diverge (the #150 defect that `evidence_form` exists to end)."""
    if not isinstance(evidence, list) or not evidence:
        raise InscriptionRefused(f"⛔ REFUSED (schema) — {what!r} must be a non-empty list. File untouched.")

    bad = [(p, evidence_error(p)) for p in evidence]                       # R5
    bad = [(p, why) for p, why in bad if why]
    if bad:
        lines = "\n".join(f"    - {p!r}: {why}" for p, why in bad)
        raise InscriptionRefused(f"⛔ REFUSED (evidence) — illegal evidence pointer(s):\n{lines}\nFile untouched.")

    rolling = [(p, _governs.rolling_target(p)) for p in evidence]          # R6 — s177-D1
    rolling = [(p, t) for p, t in rolling if t]
    if rolling:
        lines = "\n".join(
            f"    - {p!r}: aims into {t!r}, which the capture ritual ROLLS every wrap — this "
            f"pointer is guaranteed to rot, and when it does the failure is indistinguishable "
            f"from an ordinary repoint job" for p, t in rolling)
        raise InscriptionRefused(
            f"⛔ REFUSED (rolling evidence, s177-D1) — an evidence pointer into a file the "
            f"capture ritual rolls is INVALID ON ARRIVAL:\n{lines}\n"
            f"  Rolling files: {', '.join(_governs.ROLLING_FILES)}.\n"
            f"  The legal cure is to point at what does NOT roll: `commit <sha> …` or "
            f"`chat #<n> <date> (live) - …`. If the rolled text itself is the evidence, quote it "
            f"VERBATIM inside the pointer's own prose and anchor the pointer at the commit that "
            f"carried it. File untouched.")


# ---------------------------------------------------------------------------
# A — AMEND-EVIDENCE. Sanctioned #193 by Dave, for ONE job: LEGALIZING an evidence entry
# whose FORM is defective (prose with no pointer; a figure string the pathish extractor reads
# as a rotted path) without touching a single other byte of the ratified record.
#
# ⛔ SCOPE, and it is the whole safety argument: this mode may replace the `evidence` ARRAY of
# ONE existing ruling and NOTHING ELSE. `says` is never reachable from here — a ruling's words
# are Dave's and an "amend" that could reach them is a re-stamp wearing a tool's clothes
# [[header-wins-over-audit]]. The parse check below PROVES that by comparing every other ruling
# and every other field of the target for equality.
#
# It carries the SAME proof discipline as append, because the defect is the same defect: the
# obvious method (json.load → mutate → json.dump) reformats 3,000 lines to change four.
#   A1 TARGET   — the id must exist, EXACTLY once.
#   A2 TEXTUAL  — the replacement is a SPAN SWAP into the existing bytes, PROVEN BY
#                 RECONSTRUCTION: putting the OLD span back where the new one sits must give
#                 back the ORIGINAL BYTES, `==` on the raw string.
#   A3 PARSES   — the result parses, has the SAME ruling count, and differs from the original
#                 in EXACTLY ONE PLACE: the target's `evidence`.
#   A4 CHANGES  — an amend that changes nothing is refused; a no-op write is a lie in git log.
#   R5/R6       — every NEW pointer must be legal on arrival, same ladder as append.
# ---------------------------------------------------------------------------
def compose_amend(text, lo, hi, evidence):
    """Return (new_span, new_text). ⛔ Serializes ONLY the evidence array; every other byte is
    carried through by construction. Kept as its own function so the selftest can PLANT a
    tidying writer here and prove A2 is the check that catches it."""
    body = json.dumps(evidence, indent=1, ensure_ascii=False)
    new_span = "\n".join(" " + ln if ln else ln for ln in body.splitlines()).lstrip(" ")
    return new_span, text[:lo] + new_span + text[hi:]


def amend_evidence(rid, evidence, path=RULINGS, write=False):
    if not isinstance(rid, str) or not rid.strip():
        raise InscriptionRefused("⛔ REFUSED (target) — no ruling id given. File untouched.")
    for p in evidence if isinstance(evidence, list) else []:
        if not isinstance(p, str) or not p.strip():
            raise InscriptionRefused("⛔ REFUSED (schema) — every evidence line must be a non-empty string. File untouched.")
    if not isinstance(evidence, list) or not evidence:
        raise InscriptionRefused("⛔ REFUSED (schema) — 'evidence' must be a non-empty list. File untouched.")

    with open(path, encoding="utf-8") as fh:
        original = fh.read()

    data = json.loads(original)
    targets = [r for r in data.get("rulings", []) if r.get("id") == rid]
    if len(targets) != 1:                                                  # A1
        raise InscriptionRefused(
            f"⛔ REFUSED (unknown id) — {rid!r} matches {len(targets)} rulings in "
            f"{os.path.basename(path)}. Evidence is amended on an EXISTING ruling; to add a new "
            f"one use --write. File untouched.")
    old_evidence = targets[0]["evidence"]
    if old_evidence == evidence:                                           # A4
        raise InscriptionRefused(
            f"⛔ REFUSED (no change) — the submitted evidence for {rid!r} is identical to what is "
            f"already inscribed. A write that changes nothing puts a lie in git log. File untouched.")

    # R5/R6 ON THE DELTA ONLY — every pointer that is NEW in this amendment, and no other.
    # ⛔ Deliberate, and it is the R6 scope note applied one level up: a pointer already in
    # `_rulings.json` is RATIFIED RECORD and is not re-judged by machine here. The inscriber's
    # R5 is strictly narrower than `_governs`' own reader (it wants a path in the first token,
    # the reader extracts every path-shaped token anywhere in the line), so re-judging the whole
    # array would refuse to amend any ruling that carries a legacy annotated pointer — i.e. the
    # tool would be unable to fix the very entries it exists to fix, and the "fix" would have to
    # be a hand edit, which is the #179 defect wearing a workaround. New lines get the full
    # ladder; carried lines are carried [[header-wins-over-audit]].
    delta = [p for p in evidence if p not in old_evidence]
    if delta:                       # an amend that only DROPS or reorders has no new pointer
        check_evidence_list(delta)

    lo, hi = _evidence_span(original, rid)
    old_span = original[lo:hi]
    new_span, new_text = compose_amend(original, lo, hi, evidence)

    reconstructed = new_text[:lo] + old_span + new_text[lo + len(new_span):]   # A2 — the proof
    if reconstructed != original:
        raise InscriptionRefused(
            "⛔ REFUSED (not textual) — putting the OLD evidence span back does NOT give back the "
            "original bytes. Something outside the target span moved. This is the #179 defect and "
            "the whole reason this script exists. File untouched.")

    try:                                                                   # A3
        after = json.loads(new_text)
    except json.JSONDecodeError as ex:
        raise InscriptionRefused(f"⛔ REFUSED (unparseable result) — {ex}. File untouched.")
    before_rulings, after_rulings = data.get("rulings", []), after.get("rulings", [])
    if len(before_rulings) != len(after_rulings):
        raise InscriptionRefused("⛔ REFUSED (count) — the ruling count changed. File untouched.")
    if set(data) != set(after) or any(k != "rulings" and data[k] != after[k] for k in data):
        raise InscriptionRefused("⛔ REFUSED (scope) — a top-level key outside `rulings` changed. File untouched.")
    diffs = []
    for b, a in zip(before_rulings, after_rulings):
        if b == a:
            continue
        if b.get("id") != rid or {k: v for k, v in b.items() if k != "evidence"} != \
           {k: v for k, v in a.items() if k != "evidence"}:
            diffs.append(b.get("id"))
    if diffs:
        raise InscriptionRefused(
            f"⛔ REFUSED (scope) — the result differs outside {rid!r}'s evidence: {diffs}. "
            f"An amend may touch ONE array and nothing else — `says` is never reachable from "
            f"here. File untouched.")
    if after_rulings[before_rulings.index(targets[0])]["evidence"] != evidence:
        raise InscriptionRefused("⛔ REFUSED (round-trip) — the parsed evidence is not what was submitted. File untouched.")

    report = {"id": rid, "at_byte": lo, "old_span_bytes": len(old_span), "span_bytes": len(new_span),
              "file_bytes_before": len(original), "file_bytes_after": len(new_text),
              "evidence_before": len(old_evidence), "evidence_after": len(evidence),
              "textual": True, "written": False}
    if write:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_text)
        report["written"] = True
    return report


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

    check_evidence_list(entry["evidence"])                                 # R5 + R6

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

        # ARM 6 — s177-D1: a pointer into a ROLLING file is refused ON ARRIVAL, and every
        # named rolling file is driven, not just the first. An arm that proves one entry of a
        # three-entry list proves the list is READ, never that it is COMPLETE.
        p6 = _tmp_copy(td)
        for i_, roll in enumerate(_governs.ROLLING_FILES):
            r_ = copy.deepcopy(GOOD)
            r_["id"] = f"zz-selftest-R6-{i_}"
            r_["evidence"] = [f"{roll}#some anchor text"]
            try:
                inscribe(r_, p6, write=True)
                fails.append(f"arm6: a pointer into the rolling file {roll!r} was ACCEPTED")
            except InscriptionRefused as ex:
                if "rolling" not in str(ex):
                    fails.append(f"arm6: {roll} refused for the WRONG reason — {ex}")
                elif roll not in str(ex):
                    fails.append(f"arm6: the refusal does not NAME {roll!r} — {ex}")
        # ARM 6b — the bare-path form (no anchor) is caught too. The rule is about the FILE.
        r6b = copy.deepcopy(GOOD); r6b["id"] = "zz-selftest-R6b"
        r6b["evidence"] = ["_LIVE-STATE.md"]
        try:
            inscribe(r6b, p6, write=True); fails.append("arm6b: a bare rolling path was ACCEPTED")
        except InscriptionRefused as ex:
            if "rolling" not in str(ex):
                fails.append(f"arm6b: wrong reason — {ex}")
        # ARM 6c — CONTROLS, and they are the half that stops R6 becoming a word-ban.
        #   (i) a chat pointer that MENTIONS a rolling file in its prose is LEGAL — use vs
        #       mention [[gate-must-quote-what-it-forbids]];
        #   (ii) _GM-ARCHIVE.md is where the banners roll TO and does not itself roll, so a
        #        substring matcher would wrongly catch it. It must be ACCEPTED.
        for cid, ev in (("zz-selftest-R6c", ["chat #000 2026-01-01 (live) - the GOOD-MORNING.md "
                                             "banner said X, quoted verbatim here"]),
                        ("zz-selftest-R6d", ["_GM-ARCHIVE.md"]),
                        ("zz-selftest-R6e", ["commit deadbee - _LIVE-STATE.md delta as it stood"])):
            ctl = copy.deepcopy(GOOD); ctl["id"] = cid; ctl["evidence"] = ev
            try:
                inscribe(ctl, p6, write=False)
            except InscriptionRefused as ex:
                fails.append(f"arm6 CONTROL {cid}: a LEGAL pointer was refused — {ex}")
        if open(p6, encoding="utf-8").read() != open(_tmp_copy(td), encoding="utf-8").read():
            fails.append("arm6: a rolling refusal MODIFIED the file")

        # ============================ AMEND-EVIDENCE ARMS (#193) ============================
        # CONTROL FIRST, again: an amend must FIRE, be byte-exact outside its span, and be
        # readable back. Everything after it is failure-only, and a failure-only suite reads
        # green after a revert that deletes the feature.
        pa = _tmp_copy(td)
        orig_a = open(pa, encoding="utf-8").read()
        live = json.loads(orig_a)["rulings"]
        tgt = live[-1]["id"]
        old_ev = live[-1]["evidence"]
        new_ev = ["commit deadbee - synthetic amend arm", "chat #000 2026-01-01 (live) - synthetic"]
        try:
            rep = amend_evidence(tgt, list(new_ev), pa, write=True)
        except InscriptionRefused as ex:
            fails.append(f"armA0 CONTROL: a legal amend was refused — {ex}")
        else:
            after_a = open(pa, encoding="utf-8").read()
            lo, n, m = rep["at_byte"], rep["span_bytes"], rep["old_span_bytes"]
            if after_a[:lo] + orig_a[lo:lo + m] + after_a[lo + n:] != orig_a:
                fails.append("armA0 CONTROL: the written file is NOT the original bytes with one span swapped")
            back = json.loads(after_a)["rulings"]
            if [r["id"] for r in back] != [r["id"] for r in live]:
                fails.append("armA0 CONTROL: the ruling order/ids changed")
            hit = [r for r in back if r["id"] == tgt][0]
            if hit["evidence"] != new_ev:
                fails.append("armA0 CONTROL: the new evidence is not readable back")
            if any(a != b for a, b in zip(back, live) if a["id"] != tgt):
                fails.append("armA0 CONTROL: another ruling changed")
            if {k: v for k, v in hit.items() if k != "evidence"} != \
               {k: v for k, v in live[-1].items() if k != "evidence"}:
                fails.append("armA0 CONTROL: a field other than `evidence` changed on the target")

        # ARM A1 — MUTATION PROOF that the RECONSTRUCTION check itself bites, and that ONLY it
        # can. ⚠ The obvious plant (a span one byte too wide) is worthless: it is caught by the
        # PARSE check downstream, so deleting A2 entirely leaves such an arm green — that is a
        # green that cannot fail [[mutation-tests-the-clause-not-the-feature]]. The plant here is
        # a JSON-EQUIVALENT REINDENT outside the span: it parses, every ruling compares equal,
        # the scope check is happy — and it is exactly the #179 defect. Only A2 sees it.
        pa1 = _tmp_copy(td)
        orig_a1 = open(pa1, encoding="utf-8").read()
        real_ca = globals()["compose_amend"]

        def tidy_compose(text, lo_, hi_, ev):          # a "harmless" reindent of an untouched line
            span, nt = real_ca(text, lo_, hi_, ev)
            head = nt[:lo_].replace('\n "ruled":', '\n  "ruled":', 1)
            nt2 = head + nt[lo_:]
            return span, nt2
        globals()["compose_amend"] = tidy_compose
        try:
            amend_evidence(tgt, list(new_ev), pa1, write=True)
            fails.append("armA1: a tidying writer was ACCEPTED — A2 (reconstruction) is dead")
        except InscriptionRefused as ex:
            if "not textual" not in str(ex):
                fails.append(f"armA1: refused for the wrong reason (A2 must be the one that "
                             f"bites, or the arm proves a different clause) — {ex}")
        finally:
            globals()["compose_amend"] = real_ca
        if open(pa1, encoding="utf-8").read() != orig_a1:
            fails.append("armA1: FILE WAS MODIFIED despite the refusal")

        # ARM A1c — a span one byte too wide must ALSO be refused (a different clause may catch
        # this one; the point is that it never lands).
        pa1c = _tmp_copy(td)
        real_span = globals()["_evidence_span"]

        def bad_span(text, rid):
            lo_, hi_ = real_span(text, rid)
            return lo_, hi_ + 1
        globals()["_evidence_span"] = bad_span
        try:
            amend_evidence(tgt, list(new_ev), pa1c, write=True)
            fails.append("armA1c: a span-swap that ate a byte outside the array was ACCEPTED")
        except InscriptionRefused:
            pass
        finally:
            globals()["_evidence_span"] = real_span
        if open(pa1c, encoding="utf-8").read() != orig_a1:
            fails.append("armA1c: FILE WAS MODIFIED despite the refusal")

        # ARM A1b — the REFORMATTING writer, driven through amend. json.dump of the whole file
        # is the #179 defect itself; the reconstruction must reject it.
        pa1b = _tmp_copy(td)
        d_ = json.loads(orig_a1)
        for r_ in d_["rulings"]:
            if r_["id"] == tgt:
                r_["evidence"] = list(new_ev)
        reform = json.dumps(d_, indent=2)
        lo_, hi_ = real_span(orig_a1, tgt)
        if reform[:lo_] + orig_a1[lo_:hi_] + reform[lo_:] == orig_a1:
            fails.append("armA1b: a whole-file reserialization reconstructed to the original — impossible")

        # ARM A2 — an id that does not exist is REFUSED, loudly and by name.
        pa2 = _tmp_copy(td)
        try:
            amend_evidence("zz-no-such-ruling-xyzzy", list(new_ev), pa2, write=True)
            fails.append("armA2: amending a NONEXISTENT id was ACCEPTED")
        except InscriptionRefused as ex:
            if "unknown id" not in str(ex) and "target" not in str(ex):
                fails.append(f"armA2: wrong reason — {ex}")

        # ARM A3 — illegal evidence is refused on amend exactly as on append (R5) …
        try:
            amend_evidence(tgt, ["knowledge/_no_such_file_xyzzy.py"], pa2, write=True)
            fails.append("armA3: illegal evidence ACCEPTED on amend")
        except InscriptionRefused as ex:
            if "evidence" not in str(ex):
                fails.append(f"armA3: wrong reason — {ex}")
        # … and R6: a pointer into EVERY named rolling file is refused on amend too. The R6
        # scope is arrival, and an amend IS an arrival.
        for roll in _governs.ROLLING_FILES:
            try:
                amend_evidence(tgt, [f"{roll}#some anchor text"], pa2, write=True)
                fails.append(f"armA3b: a rolling pointer into {roll!r} was ACCEPTED on amend")
            except InscriptionRefused as ex:
                if "rolling" not in str(ex):
                    fails.append(f"armA3b: {roll} refused for the WRONG reason — {ex}")

        # ARM A3c — SCOPE CONTROL, and it is the half that keeps A3 from becoming a re-judge of
        # ratified record: a pointer ALREADY inscribed is CARRIED even when the inscriber's own
        # narrower R5 would reject it on arrival. Planted with a real legacy shape.
        pa3c = _tmp_copy(td)
        legacy = "git log -S FOO -- knowledge/_inscribe_ruling.py: single commit deadbee - note"
        if evidence_error(legacy) is None:
            fails.append("armA3c: the planted legacy pointer is R5-LEGAL — the plant proves nothing")
        t3 = json.loads(open(pa3c, encoding="utf-8").read())["rulings"][0]["id"]
        try:
            amend_evidence(t3, [legacy], pa3c, write=True)   # first put it in, bypassing nothing
        except InscriptionRefused:
            pass                                             # arrival correctly refuses it
        else:
            fails.append("armA3c: an ILLEGAL pointer arrived — R5 does not bite on amend")
        # now the real control: carry an already-inscribed line alongside a new legal one
        pa3d = _tmp_copy(td)
        raw3 = open(pa3d, encoding="utf-8").read()
        live3 = json.loads(raw3)["rulings"]
        carried = next((e for r in live3 for e in r["evidence"]
                        if evidence_error(e) is not None), None)
        if carried is None:
            fails.append("armA3d: no already-inscribed pointer fails the narrow R5 — arm UNMEASURED "
                         "(not a pass: the carry rule was not exercised)")
        else:
            owner = next(r["id"] for r in live3 if carried in r["evidence"])
            keep = [e for e in next(r["evidence"] for r in live3 if r["id"] == owner)]
            try:
                amend_evidence(owner, keep + ["commit deadbee - a new legal line"], pa3d, write=False)
            except InscriptionRefused as ex:
                fails.append(f"armA3d: a CARRIED ratified pointer was re-judged and refused — {ex}")

        # ARM A4 — a no-op amend is refused (a write that changes nothing lies in git log).
        try:
            amend_evidence(tgt, list(old_ev), pa2, write=True)
            fails.append("armA4: a no-op amend was ACCEPTED")
        except InscriptionRefused as ex:
            if "no change" not in str(ex):
                fails.append(f"armA4: wrong reason — {ex}")
        # empty evidence is a schema refusal, not a silent wipe
        try:
            amend_evidence(tgt, [], pa2, write=True)
            fails.append("armA4b: an EMPTY evidence array was ACCEPTED")
        except InscriptionRefused:
            pass
        if open(pa2, encoding="utf-8").read() != open(_tmp_copy(td), encoding="utf-8").read():
            fails.append("armA: an amend refusal MODIFIED the file")

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
    ap.add_argument("--amend-evidence", action="store_true",
                    help="replace ONE existing ruling's `evidence` array (and nothing else); "
                         "--entry/stdin then holds a JSON LIST of pointer strings")
    ap.add_argument("--id", help="the ruling id whose evidence is being amended")
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
              "illegal evidence · legal-evidence control · file-untouched-on-refusal · "
              "R6 rolling-file evidence refused for every named file · bare-path form · "
              "use-vs-mention + roll-TARGET controls accepted · AMEND: control fires byte-exact, "
              "reconstruction mutation-proven, unknown id · illegal + rolling evidence · no-op "
              "and empty refused, file untouched)")
        return 0

    if a.amend_evidence:
        if not a.id:
            print("⛔ --amend-evidence needs --id <ruling id>. Nothing done.", file=sys.stderr)
            return 2
        try:
            raw = open(a.entry, encoding="utf-8").read() if a.entry else sys.stdin.read()
            evidence = json.loads(raw)
        except (OSError, json.JSONDecodeError) as ex:
            print(f"⛔ REFUSED (input) — could not read the evidence array: {ex}", file=sys.stderr)
            return 2
        if not (a.dry_run or a.write):
            print("⛔ state your intention: --dry-run or --write. Nothing done.", file=sys.stderr)
            return 2
        try:
            rep = amend_evidence(a.id, evidence, a.rulings, write=a.write)
        except InscriptionRefused as ex:
            print(str(ex), file=sys.stderr)
            return 3
        verb = "AMENDED" if rep["written"] else "DRY RUN — would swap cleanly, NOTHING WRITTEN"
        print(f"{verb}: {rep['id']} evidence — textual span swap at offset {rep['at_byte']}, "
              f"{rep['old_span_bytes']} → {rep['span_bytes']} bytes; file "
              f"{rep['file_bytes_before']} → {rep['file_bytes_after']} bytes; evidence lines "
              f"{rep['evidence_before']} → {rep['evidence_after']}; reconstruction proof PASSED "
              f"(every other byte identical; `says` untouched by construction).")
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
