#!/usr/bin/env python3
"""_could_not_ask.py — THE COULD-NOT-ASK CONVENTION, in one place, for the whole class.

★ WHY THIS EXISTS (#193, extending #183). #173 found the class and #183 built the remedy for
exactly ONE member of it: `_gen_chain.py --check` refuses — rather than saying STALE — when the
tier it can reach differs from the tier the committed file is stamped with. The remedy was
correct and it was LOCAL: the refusal was spelled in prose inside one module, it exited `1`, and
nothing downstream could tell that `1` apart from a real failure. So the survey printed
`0 could-not-ask` in the same breath as `❌ [109] … exit 1`, and CI's "Knowledge build" step
never ran because the survey ahead of it was red for a refusal that had already named itself.

⇒ A refusal that no consumer can RECOGNISE is a failure wearing an apology. This module makes
the refusal MACHINE-READABLE, so a survey can count it as a third verdict instead of guessing
from prose.

THE CONVENTION — two halves, and BOTH are required:

  1. EXIT CODE `77` (`EXIT`). Distinct from `0` (pass), `1` (a real, measured failure) and `2`
     (bad arguments / a refusal to run at all, which several gates already use). 77 is not a
     magic number with meaning elsewhere in this repo; it is simply unused, which is the whole
     requirement. ⚠ A refusal is still NON-ZERO: a caller that has no idea what 77 means (`||`
     in `_git_commit.sh`, `set -e`, a CI `run:` line) keeps its old, safe behaviour of stopping.
     Only a caller that has been TAUGHT the code treats it as a third verdict.

  2. A FIRST LINE beginning `COULD-NOT-ASK:` (`MARKER`), carrying the reason IN THE GATE'S OWN
     WORDS. The exit code lets a consumer bucket it; the line lets a HUMAN read why without
     re-running anything. [[measuring-tool-must-not-guess]] — the reason is written by the gate
     that knows which input it could not reach, never inferred by the consumer.

⛔ WHAT A REFUSAL MAY BE KEYED ON. The UNREACHABLE INPUT, named: a gitignored key or cache that
a checkout cannot have, an import that is not installed, a path outside the committed tree.
NEVER on "am I in CI" — an env-var skip reproduces the #173 lie in a new shape
[[gate-cannot-pass-in-one-environment]]: it makes the gate's verdict a function of the runner's
identity rather than of what the runner can reach, and the first honest environment to set that
variable gets a silent pass. Every refusal in this repo must be reproducible on ANY machine by
taking the input away, and that is exactly how each one is mutation-proven.

⚠ AND IT MUST STILL BITE. A refusal path is only honest if the REACHABLE side still fails: each
gate that gained one carries two arms — the refusal fires when the input is gone, AND a real
staleness on the reachable tier still exits 1. A refusal that swallows its gate's purpose is
worse than the disease it cures.

Usage (inside a gate):
    import _could_not_ask as cna
    return cna.refuse("_CHAIN.md", "the committed file is stamped `real`; this environment "
                                   "can only reach `tape (cl100k ESTIMATE)` …")

Usage (inside a consumer):
    if cna.is_refusal(rc):
        reason = cna.reason_in(stdout + stderr)   # None when the gate did not say
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import sys

EXIT = 77
MARKER = "COULD-NOT-ASK:"


def refuse(subject, reason, stream=None):
    """Print the refusal in the convention's shape and return `EXIT` so a caller can `return` it.

    `subject` is the ARTEFACT or gate the verdict was wanted about; `reason` must name the input
    that could not be reached, and should say WHERE the proof is reachable when that is known —
    a reader who is told only "cannot ask" has been handed a shrug.
    """
    out = stream or sys.stdout
    print(f"{MARKER} {subject} — {reason}", file=out)
    return EXIT


def is_refusal(rc):
    """True iff this exit code is a self-declared refusal rather than a verdict."""
    return rc == EXIT


def reason_in(text):
    """The first `COULD-NOT-ASK:` line in some captured output, or None.

    ⚠ Returns None rather than a placeholder when the marker is absent: a consumer that
    manufactured a reason would be inventing the one thing the convention exists to carry.
    """
    for line in (text or "").splitlines():
        s = line.strip()
        i = s.find(MARKER)
        if i != -1:
            return s[i:].strip()
    return None


def selftest():
    """Bites. Small surface, but every consumer depends on these exact answers."""
    fails = []

    def bite(what, ok):
        print(f"    {'✓' if ok else '✗'} {what}")
        if not ok:
            fails.append(what)

    import io
    buf = io.StringIO()
    rc = refuse("thing", "the input is gone", stream=buf)
    bite("refuse() returns the convention's exit code", rc == EXIT)
    bite("EXIT is not 0/1/2 — it cannot be confused with pass, fail, or bad-arguments",
         EXIT not in (0, 1, 2))
    bite("refuse() prints a line that STARTS with the marker", buf.getvalue().startswith(MARKER))
    bite("the printed line carries the gate's own reason, not a summary",
         "the input is gone" in buf.getvalue())
    bite("is_refusal() is true for EXIT and false for a real failure",
         is_refusal(EXIT) and not is_refusal(1) and not is_refusal(0) and not is_refusal(2))
    bite("reason_in() finds the marker line in captured output",
         reason_in("noise\n" + buf.getvalue() + "more") == buf.getvalue().strip())
    bite("reason_in() finds it when the gate prefixed the line (✗ / indentation)",
         reason_in(f"  ✗ {MARKER} tier divergence").endswith("tier divergence"))
    bite("reason_in() returns None — never a manufactured reason — when the marker is absent",
         reason_in("✗ something is STALE") is None and reason_in("") is None
         and reason_in(None) is None)
    print(f"  {'✅' if not fails else '❌'} _could_not_ask selftest: "
          f"{'all bites pass' if not fails else f'{len(fails)} bite(s) failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print(__doc__)
