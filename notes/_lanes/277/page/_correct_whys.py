#!/usr/bin/env python3
"""_correct_whys.py — lane CP (#277). Rewrite the two weak `$why` sentences lane
CV named at A-6, BY ADDITION.

Lane CO's files in notes/_lanes/277/charts/proposed-metas/ are NOT opened for
writing. Each corrected meta is a byte-for-byte copy of CO's proposal with ONE
textual span replaced — the same discipline CO's own splice uses, and the same
reason (#179: never re-serialise a JSON file to change a string inside it).

  dv-pie-001  cited `data-a1`/`-a2`, which live in
              knowledge/snippets/Chart-donut.reference.html, NOT in
              chart-pie.meta.json. The meta's own motion.entry states the sweep
              contract, so the pointer moves to the file that actually carries it.
  dv-bar-002  named no checkable mechanism. It now names the type composite
              (.t-cm-chart-label, which the meta says carries "labels · axis ·
              legend · values") and the axis token (data/axis, DV-D07).

A third correction is NOT written here because it is conditional on Dave: if
dv-013 keeps chart-bar at D-3, its `$why` must cite the grouped-column and
stacked-column variants and the `series` prop that mints data/series/1-5 —
where colour genuinely differentiates the data sets — rather than `orientation`,
which is about sign. dv-013 is a FAMILY rule and so is in no proposed meta yet;
the sentence is written out in REPORT.md for whoever authors it.

  python3 notes/_lanes/277/page/_correct_whys.py [--check]
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
if _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_sys.path.insert(0, _hg_d)
    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
SRC = LANE.parent / "charts" / "proposed-metas"      # lane CO — READ ONLY
OUT = LANE / "proposed-metas"
REPO = LANE.parents[3]

EDITS = {
    "chart-pie.meta.json": [(
        "Start at 12 o'clock, largest to smallest unless the categories have an inherent order — the angle contract for the segments this meta bakes as data-a1/-a2 at generation time.",
        "Start at 12 o'clock, largest to smallest unless the categories have an inherent order — the angle contract for the sweep this meta's motion.entry bakes (data-cx/-cy/-ro/-a1/-a2, no data-ri), which is where the start angle and the segment order are fixed, at generation time.",
    )],
    "chart-bar.meta.json": [(
        "Axis titles on both axes unless the labels are obvious — the get-out clause is the reason this is a judgement the author makes per instance, and the meta's axis tokens have to carry either way.",
        "Axis titles on both axes unless the labels are obvious — the meta's tokens.font-family composite routes labels, axis, legend and values through one type role, .t-cm-chart-label at 12/500, and tokens.axis mints data/axis (DV-D07) for them, so the get-out clause changes what is drawn and never which token pays for it.",
    )],
}


def main():
    check = "--check" in sys.argv
    OUT.mkdir(exist_ok=True)
    changed = []
    for name in sorted(p.name for p in SRC.glob("*.meta.json")):
        text = (SRC / name).read_text(encoding="utf-8")
        before = text
        for old, new in EDITS.get(name, []):
            if text.count(old) != 1:
                sys.exit(f"REFUSED — {name}: the span to replace occurs "
                         f"{text.count(old)} times, not once. Nothing written.")
            text = text.replace(old, new)
        # the replacement is textual; prove it is still the same document plus
        # exactly the intended string change
        a, b = json.loads(before), json.loads(text)
        if json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True) and EDITS.get(name):
            sys.exit(f"REFUSED — {name}: the edit changed nothing.")
        diff = [k for k in ("name", "purpose", "props", "tokens", "variants", "provenance")
                if a.get(k) != b.get(k)]
        if diff:
            sys.exit(f"REFUSED — {name}: the edit moved {diff}, not just a $why.")
        n_why = sum(1 for x, y in zip(a["edges"]["obeys"], b["edges"]["obeys"])
                    if x["$why"] != y["$why"])
        if n_why != len(EDITS.get(name, [])):
            sys.exit(f"REFUSED — {name}: {n_why} $why sentences moved, expected "
                     f"{len(EDITS.get(name, []))}.")
        if check:
            on_disk = (OUT / name).read_text(encoding="utf-8") if (OUT / name).exists() else None
            print(f"  {name:24s} {'OK' if on_disk == text else 'STALE'} · "
                  f"{n_why} $why rewritten · {len(b['edges']['obeys'])} obeys entries")
            continue
        (OUT / name).write_text(text, encoding="utf-8")
        changed.append((name, n_why, len(b["edges"]["obeys"])))
    if not check:
        for name, n_why, n_obeys in changed:
            print(f"  wrote {name:24s} {n_why} $why rewritten · {n_obeys} obeys entries")
        print(f"{sum(c[1] for c in changed)} sentences corrected across {len(changed)} files, "
              f"BY ADDITION — {SRC} is untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
