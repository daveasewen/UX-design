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
"""
import sys

FLAGS = ("-h", "--help", "--usage")


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
