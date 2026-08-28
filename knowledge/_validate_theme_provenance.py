#!/usr/bin/env python3
"""Theme-provenance gate (ADR-0011, R-D19) — ADVISORY.

Makes "red = Legacy" mechanically visible. For every Mono-designated LIBRARY surface it flags any
colour that belongs to another theme's override set — including HARDCODED Legacy hexes in live CSS,
the blind spot the token-resolution leak gate (_validate_legacy_leak.py) cannot see because it only
walks token-manifest bindings.

Scope (see knowledge/_STYLE-PROVENANCE.md, the human record — this mirrors it):
  Mono-designated = snippets/ + _proforma/ + _review/ (the library).
  Excluded        = _fitness-test/ (test pages + pre-canon exploration + research).

ADVISORY: writes _THEME-PROVENANCE-GATE.md and always exits 0. Promote to blocking (exit 1 on
unwaived flags) once the migration in _STYLE-PROVENANCE.md §backlog is done (ADR-0011).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
THEMES = json.load(open(os.path.join(HERE, "tokens", "themes", "_themes.json")))
BASE = THEMES.get("activeBase", "apollo-mono")

# Non-base themes' owned hexes = "must not appear in a Mono surface".
FOREIGN = {}
for tid, t in THEMES["themes"].items():
    if tid == BASE:
        continue
    for hexv, why in t.get("ownsHexes", {}).items():
        FOREIGN[hexv.upper()] = f"{t['label']}: {why}"

MONO_DIRS = ["snippets", "_proforma", "_review"]
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")


def strip_noise(t):
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)          # html comments (token-manifests live here)
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)            # css comments
    t = re.sub(r'<script[^>]*application/json[^>]*>.*?</script>', "", t, flags=re.S)
    t = re.sub(r'<script[^>]*id="token-manifest"[^>]*>.*?</script>', "", t, flags=re.S)
    return t


def scan():
    """-> (flags, scanned). Extracted at #221 so the determinism clause can be BITTEN."""
    flags = []          # (dir, file, hex, reason, count)
    scanned = 0
    for d in MONO_DIRS:
        base = os.path.join(HERE, d)
        # ⛔ #221 — `os.walk` YIELDS IN FILESYSTEM ORDER, AND THIS GATE WROTE ITS REPORT IN THAT
        # ORDER. Same commit, byte-identical inputs, same interpreter — and the working tree and
        # a `git clone --no-hardlinks` of it produced DIFFERENT `_THEME-PROVENANCE-GATE.md`
        # files. Measured: both say `Scanned 164` and `48 hardcoded foreign-theme colour(s)`,
        # both are 58 lines, and 26 lines differ in EACH direction — a pure permutation. The
        # numbers were never wrong; the row order was a fingerprint of whichever filesystem
        # happened to generate the file.
        # ⚠ AND IT WAS BEING READ AS DRIFT. #220-L1 finding 7 listed this artefact as stale with
        # "26 rows changed" — the same 26. On the evidence here that row is a FALSE staleness:
        # the artefact was not out of date, it was unsorted. A non-deterministic generator is
        # worse than a stale one, because every environment disagrees with every other and no
        # comparison anywhere can mean anything. [[measure-dont-convert-units]]
        # ⚠ NO VALUE MOVES. Sorting changes the ORDER of the rows and nothing else: 164 scanned
        # and 48 findings before and after, verified.
        for root, dirs, files in os.walk(base):
            dirs.sort()
            for fn in sorted(files):
                if not fn.endswith(".html"):
                    continue
                scanned += 1
                live = strip_noise(open(os.path.join(root, fn), encoding="utf-8", errors="ignore").read())
                seen = {}
                for m in HEX_RE.finditer(live):
                    h = m.group(0).upper()
                    if h in FOREIGN:
                        seen[h] = seen.get(h, 0) + 1
                for h, n in sorted(seen.items()):
                    flags.append((d, fn, h, FOREIGN[h], n))
    # belt and braces: the walk is sorted above, and the RESULT is sorted here, so the report's
    # order is DERIVED from the data rather than observed from the disk. Either alone would do;
    # both together mean a future change to the walk cannot silently reintroduce the defect.
    flags.sort(key=lambda r: (MONO_DIRS.index(r[0]), r[1], r[2]))
    return flags, scanned


def selftest():
    """The determinism clause, driven — the class #221 found by comparing two environments."""
    fails = []
    a, scanned_a = scan()
    b, scanned_b = scan()
    if a != b:
        fails.append("TWO RUNS DISAGREE — the scan is not deterministic within one process")
    if scanned_a != scanned_b:
        fails.append("scanned count moved between two runs: %d vs %d" % (scanned_a, scanned_b))
    if a != sorted(a, key=lambda r: (MONO_DIRS.index(r[0]), r[1], r[2])):
        fails.append("REPORT ORDER IS NOT DERIVED — rows are in filesystem order, so this "
                     "artefact is a fingerprint of the machine that wrote it and no two "
                     "environments can ever agree (#221)")
    # the control: an UNSORTED copy must fail the same assertion, or the assertion proves nothing
    if len(a) > 1:
        shuffled = list(reversed(a))
        if shuffled == sorted(shuffled, key=lambda r: (MONO_DIRS.index(r[0]), r[1], r[2])):
            fails.append("CONTROL FAILED — a reversed row list still reads as sorted, so the "
                         "order assertion above cannot fail and is decoration")
    else:
        fails.append("CONTROL UNAVAILABLE — fewer than 2 rows on this tree; the order assertion "
                     "is unfalsifiable here and is DECLARED, not claimed")
    if not scanned_a:
        fails.append("POPULATION EMPTY — the gate would publish a green over nothing")
    print("theme-provenance selftest: %d row(s) over %d file(s) · 5 arm(s) · %d failure(s)"
          % (len(a), scanned_a, len(fails)))
    for f in fails:
        print("  ⛔ " + f)
    return 1 if fails else 0


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    flags, scanned = scan()

    lines = ["# Theme-provenance gate (ADR-0011, R-D19) — ADVISORY\n\n",
             f"Scanned **{scanned}** Mono-designated library files "
             f"({', '.join(MONO_DIRS)}). Foreign-theme hexes checked: "
             f"{', '.join(sorted(FOREIGN))}.\n\n",
             f"**{len(flags)}** hardcoded foreign-theme colour(s) found in live CSS "
             f"(comments + token-manifests excluded).\n"]
    if flags:
        lines.append("\n| Area | File | Hex | ×  | Belongs to |\n|---|---|---|---|---|\n")
        for d, fn, h, why, n in flags:
            lines.append(f"| {d} | {fn} | `{h}` | {n} | {why} |\n")
        lines.append("\n> These are the drift the record (`_STYLE-PROVENANCE.md` §backlog) tracks. "
                     "Re-home to Mono values, then promote this gate to blocking (ADR-0011).\n")
    else:
        lines.append("\n✅ No hardcoded foreign-theme colour in any Mono surface.\n")
    open(os.path.join(HERE, "_THEME-PROVENANCE-GATE.md"), "w", encoding="utf-8").writelines(lines)

    print(f"theme-provenance gate (ADVISORY): {len(flags)} hardcoded foreign-theme hex(es) "
          f"in {scanned} Mono files. See _THEME-PROVENANCE-GATE.md")
    sys.exit(0)   # advisory


if __name__ == "__main__":
    main()
