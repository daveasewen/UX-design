#!/usr/bin/env python3
"""_validate_intent_resolve.py — the INTENT ADDRESS-RESOLVE check (#195, ds-0NN scope 1).

WHAT THIS IS. `intent` on a chart meta is an ADDRESS into the one home for the
analytical-intent vocabulary, knowledge/chart-intents.json (ADR-0017 write-once:
live facts get ONE home and addresses). This script is that address's FIRST AND
ONLY resolver — the reader that makes the field a lookup rather than prose with
extra syntax.

WHY IT LANDS IN THE SAME CHANGE AS THE FIELD. An address nothing resolves is the
#145 binds gap: it LOOKS checked and is not, which is worse than a copy. The
ds-0NN candidate record states the binding rule verbatim — "entity and first
resolver land TOGETHER". This is the resolver half.

THE CHECK, ONE SEAM (address -> store), by addition only — this script never edits:
  every `intent` value on knowledge/components/*.meta.json (excluding EXAMPLE-*)
  is a key of `chart-intent` in knowledge/chart-intents.json. A value may be a
  string or a non-empty list of strings (the hybrid shape the schema permits, so
  a chart whose purpose genuinely spans two questions can say so). An unknown
  word REFUSES, loud and named: the file, the offending word, and the legal set.

WHAT THIS CANNOT SEE, DECLARED. It proves the word EXISTS in the vocabulary, not
that it is the RIGHT word for that chart. Correctness of an assignment is Dave's
eye, grounded in each meta's own `purpose` prose. A green here reads "no intent
address dangles", never "the intents are correct". It also does not require the
field: a meta without `intent` is silently skipped — presence is not this check's
business (no gate, no ratchet, no glob width is decided here).

NOT WIRED. This script is deliberately NOT in _build_all.py's tables (#195 scope
fence). Run it by hand; wiring is Dave's to rule.

Usage:  python3 knowledge/_validate_intent_resolve.py             # check mode
        python3 knowledge/_validate_intent_resolve.py --selftest  # 4 bites
Exit non-zero on any failure. An ABSENT store or an EMPTY corpus glob fails LOUD —
an absent instrument must not read as a pass (_validate_binds_ratchet.py's rule).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "chart-intents.json")
COMP = os.path.join(HERE, "components")


def load_vocabulary(store_path=STORE):
    """The ONE home. Absent or malformed = LOUD failure, never a silent empty set."""
    if not os.path.exists(store_path):
        raise SystemExit("FAIL — intent store MISSING: %s (an absent instrument is "
                         "not a pass)" % store_path)
    data = json.loads(open(store_path, encoding="utf-8").read())
    vocab = data.get("chart-intent")
    if not isinstance(vocab, dict) or not vocab:
        raise SystemExit("FAIL — %s carries no non-empty `chart-intent` object; the "
                         "vocabulary has no home" % store_path)
    return vocab


def metas(comp_dir=COMP):
    return sorted(f for f in glob.glob(os.path.join(comp_dir, "*.meta.json"))
                  if not os.path.basename(f).startswith("EXAMPLE-"))


def check(comp_dir=COMP, store_path=STORE):
    """Returns (fails, n_files, n_addresses). Every unknown word is named."""
    vocab = load_vocabulary(store_path)
    legal = sorted(vocab)
    files = metas(comp_dir)
    if not files:
        raise SystemExit("FAIL — corpus glob matched ZERO metas under %s" % comp_dir)
    fails, n_files, n_addr = [], 0, 0
    for f in files:
        try:
            d = json.loads(open(f, encoding="utf-8").read())
        except Exception as e:  # a crash is not a fail — name it and carry on
            fails.append("%s: FAIL — unparseable JSON (%s)" % (os.path.basename(f), e))
            continue
        if "intent" not in d:
            continue
        n_files += 1
        val = d["intent"]
        words = [val] if isinstance(val, str) else val
        if not isinstance(words, list) or not words or not all(isinstance(w, str) for w in words):
            fails.append("%s: FAIL — `intent` must be a string or a non-empty list of "
                         "strings, got %r" % (os.path.basename(f), val))
            continue
        for w in words:
            n_addr += 1
            if w not in vocab:
                fails.append("%s: FAIL — UNKNOWN INTENT %r — not a key of `chart-intent` "
                             "in %s. Legal set: %s. The vocabulary is ADOPTED, not "
                             "invented: add a word only by Dave's ruling."
                             % (os.path.basename(f), w,
                                os.path.relpath(store_path, os.path.dirname(HERE)),
                                ", ".join(legal)))
    return fails, n_files, n_addr


def main():
    fails, n_files, n_addr = check()
    print("intent resolve — metas carrying `intent`: %d, addresses resolved: %d"
          % (n_files, n_addr))
    if fails:
        print("\n".join(fails))
        print("RESULT: FAIL (%d)" % len(fails))
        return 1
    print("RESULT: PASS — every intent address resolves into chart-intents.json. "
          "This proves no address DANGLES; it does not prove any assignment is RIGHT.")
    return 0


def selftest():
    """4 bites. Each must FAIL for the named reason, or the check is decorative."""
    import shutil
    import tempfile
    ok = True

    def bite(name, expect_fail, build):
        nonlocal ok
        tmp = tempfile.mkdtemp()
        try:
            cdir = os.path.join(tmp, "components")
            os.makedirs(cdir)
            spath = os.path.join(tmp, "chart-intents.json")
            build(cdir, spath)
            try:
                fails, _, _ = check(cdir, spath)
                got = bool(fails)
                detail = fails[0] if fails else "(green)"
            except SystemExit as e:
                got, detail = True, str(e)
            good = (got == expect_fail)
            ok = ok and good
            print("  %s %-34s -> %s | %s" % ("PASS" if good else "BITE-MISSED",
                                             name, "FAIL" if got else "green",
                                             detail[:110]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def store(spath, words=("comparison", "distribution")):
        json.dump({"chart-intent": {w: {"definition": "x", "notFor": "y"} for w in words}},
                  open(spath, "w", encoding="utf-8"))

    def meta(cdir, name, val):
        d = {"name": name, "purpose": "p"}
        if val is not None:
            d["intent"] = val
        json.dump(d, open(os.path.join(cdir, "%s.meta.json" % name), "w", encoding="utf-8"))

    print("selftest — _validate_intent_resolve.py")
    bite("known word resolves", False,
         lambda c, s: (store(s), meta(c, "Good", "comparison")))
    bite("unknown word refuses", True,
         lambda c, s: (store(s), meta(c, "Bad", "corelation")))
    bite("unknown word inside a list refuses", True,
         lambda c, s: (store(s), meta(c, "Bad2", ["comparison", "flow"])))
    bite("absent store fails LOUD", True,
         lambda c, s: (meta(c, "Orphan", "comparison")))
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
