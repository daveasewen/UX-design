#!/usr/bin/env python3
"""
_helpgate.py — the ONE remedy for the GENERATORS-WRITE-BY-DEFAULT class (#158).

The class (homed in `_FUTURE-STATE.md` § "COPIED UP AT #153's 2d EXIT CHECK",
born #150, unfixed through #157): a generator does its work — and its WRITES —
before it has looked at argv. `python3 knowledge/gen_showroom.py --help` at #157
therefore rewrote `showroom/`; an unrecognised argv entry was silently taken as a
snippet-name FILTER because there was no argv contract at all. Every `_build_*`,
`_validate_*` and `gen_*` script that emits an audit file shared the defect: at
#158 a runtime write-probe measured **52 scripts that attempted a repo write on a
bare `--help`**, 14 of them at MODULE level (before any `main()` even exists).

The remedy is one line at the TOP of each entry point, before the module's own
work can run:

    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

`help_gate` answers `-h` / `--help` with the module docstring and exits 0 — so the
help path can never reach a write. It is a NO-OP when the module is imported as a
library (`__name__ != "__main__"`), so importers like gen_showroom -> gen_theme_cascade
are unaffected.

The gate that keeps it there: `knowledge/_validate_help_gate.py` (AST — it parses
the consumer's grammar: every entry-point script must call the guard among its
opening statements, before any other executable statement).

This module deliberately has NO side effects of its own.

--------------------------------------------------------------------------------
SIBLING LEG — `write_gate`: the NO-ARGS write freedom (#158 residual ⑤).

`help_gate` closes the `--help` path. Its sibling leg is the BARE invocation:
`python3 knowledge/_audit_props_axes.py` with no argv at all silently overwrote
a dated, session-stamped review artefact, because its output path was an argparse
DEFAULT rather than a stated intention. Same class, other door: the script did
work — and WRITES — that argv never asked for.

The remedy is the same shape, one line at the TOP of the entry point, directly
after the help gate:

    from _helpgate import write_gate as _write_gate; _write_gate(__file__)

`write_gate` REFUSES a bare no-args invocation, LOUD and NAMED (a marker string
`REFUSED (write-gate)`, exit 2, on stderr) and tells the caller which flag makes
the write intentional. It is a no-op the moment argv carries ANY argument — so
`--help`, the script's real flags, and the explicit `--write` all proceed, and no
existing invocation that stated its intention is affected.

Scripts whose no-args write is their DESIGNED contract are NOT gated (that would
break a documented workflow); they stay off the wiring list deliberately.
"""
import os
import sys

FLAGS = ("-h", "--help", "--usage")

WRITE_FLAG = "--write"
REFUSAL_MARKER = "REFUSED (write-gate)"


def help_gate(doc, name="__main__", file=None):
    """Exit 0 with usage text when argv asks for help. No-op on import."""
    if name != "__main__":
        return
    if not any(a in FLAGS for a in sys.argv[1:]):
        return
    text = (doc or "").strip()
    if not text:
        text = "%s — no module docstring." % (file or sys.argv[0])
    sys.stdout.write(text + "\n")
    sys.exit(0)


def write_gate(file=None, flag=WRITE_FLAG, writes=None, name="__main__"):
    """Refuse a BARE (no-argv) invocation of a script that writes. No-op on import.

    Fails LOUD and NAMED: marker `REFUSED (write-gate)`, exit 2, stderr. Never
    silently skips — the only silent path is "argv carried an argument", i.e. the
    caller stated an intention.
    """
    if name != "__main__":
        return
    if sys.argv[1:]:
        return
    who = os.path.basename(file or sys.argv[0] or "<script>")
    target = (" It would overwrite: %s." % writes) if writes else ""
    sys.stderr.write(
        "✖ %s: %s WRITES FILES and was invoked with NO ARGUMENTS.%s\n"
        "  A bare run is not a stated intention (#158 write-by-default class, no-args leg).\n"
        "  Pass %s to confirm the write, or pass the script's real arguments"
        " (%s --help for the contract).\n" % (REFUSAL_MARKER, who, target, flag, who))
    sys.exit(2)
