#!/usr/bin/env python3
"""_dtcg_units.py — the unit-strip seam for the s141-D1 (A) number->dimension migration.

s141-D1 (Dave, #141) migrated 104 unitless $type:"number" px tokens to
$type:"dimension" with a "Npx" string $value. The WIRE FORMAT changed; the DESIGN
VALUES did not. Every consumer that did arithmetic or CSS formatting on the raw
numeric $value would otherwise silently change its output (0 -> "0px", and the
UNITLESS letter-spacing tokens -> "-1px", which is a different CSS declaration).

This module is that one place. A consumer calls px_number() at its READ SITE and
carries on with the number it always had. It is deliberately narrow:
  * only a plain "<number>px" string is stripped;
  * any other string (rem/%/em, an alias "{a.b}", prose) is returned UNCHANGED, so a
    consumer that already handles units is not damaged;
  * a number is returned unchanged.

Returning the value unchanged rather than raising is the right refusal here: this
helper's job is to undo ONE known encoding change, not to police the spine. The
spine is policed by knowledge/_validate_dtcg.py (DTCG-005 / DTCG-006).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re

_PX_RE = re.compile(r"^(-?\d+(?:\.\d+)?)px$")


def px_number(value):
    """"16px" -> 16 ; "-1px" -> -1 ; "0px" -> 0 ; anything else -> unchanged."""
    if isinstance(value, str):
        m = _PX_RE.match(value.strip())
        if m:
            f = float(m.group(1))
            return int(f) if f.is_integer() else f
    return value


def is_px_string(value):
    return isinstance(value, str) and bool(_PX_RE.match(value.strip()))
