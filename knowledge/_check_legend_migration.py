#!/usr/bin/env python3
"""_check_legend_migration — the EXECUTABLE end condition for the DV-D11 legend wave.

Replaces the end condition written into `canon/dv-behaviour.js` on 2026-07-26, which read:

    grep -l data-series-toggle knowledge/snippets/Chart-*.reference.html   # returns nothing

AS WRITTEN that check can never pass. The transitional block's own source contains the bare
string `data-series-toggle` (`button[data-series-toggle]`, `getAttribute('data-series-toggle')`),
and `gen_component_partials.py` injects that source into every registered member between the
AUTO-BEHAVIOUR markers. Run on 2026-07-26 it matched all five snippets — including the
already-migrated Chart-donut. It could only go quiet AFTER the deletion it was meant to authorise.

BE PRECISE ABOUT THE FIX, because the obvious one nearly works: grepping the MARKUP form
`data-series-toggle="` (with the equals-quote) does discriminate correctly today, since no
injected JS spells it that way. Run `--verbose` to see both columns side by side.

That is string luck, not structure, and it fails in the dangerous direction. The day someone
writes `data-series-toggle="` inside a comment or a template literal in the injected source, the
check silently reports "wave incomplete" forever; worse, if the markup form ever changes shape,
it reports COMPLETE and authorises deleting a block four members still depend on. A deletion
gate should not hinge on a punctuation coincidence.

So this script does it structurally: strip the injected AUTO-BEHAVIOUR regions — the actual
distinction being drawn — then count hooks in what remains. Exit 0 when the wave is complete.

Run: python3 knowledge/_check_legend_migration.py [--verbose]
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNIPPETS = sorted((ROOT / "knowledge/snippets").glob("Chart-*.reference.html"))

# the generated regions — everything between an AUTO-BEHAVIOUR START and its matching END
INJECTED = re.compile(
    r"<!-- =+ AUTO-BEHAVIOUR .*? START.*?-->.*?<!-- =+ AUTO-BEHAVIOUR .*? END =+ -->",
    re.S,
)
OLD_HOOK = 'data-series-toggle="'
NEW_HOOK = 'class="dv-legrow'

# #66 FIX — a static `<ul class="dv-legend">` (Chart-scatter) matched NEITHER hook and read as
# "no legend — nothing to migrate". That is a matched-grep-is-not-a-presence defect: OLD_HOOK and
# NEW_HOOK are only two points in the space of legend-shaped markup, not a partition of it.
#
# The vocabulary below is GREPPED from the corpus, not invented: every `class="…"` attribute in
# the five snippets' own markup that carries a `dv-leg*` token is one of — the migrated model
# (`dv-legrow`, plus its always-co-occurring `dv-leg`, `dv-leg-item`, `dv-leg-name`, `dv-leg-sw`,
# `dv-leg-reset*`), or the dead static model (`dv-legend`, seen bare only in Chart-scatter's own
# `<ul class="dv-legend …">`). LEGEND_CLASS catches the whole token family so a THIRD shape neither
# hook recognises still lands as a loud finding instead of silently falling into "no legend".
LEGEND_CLASS = re.compile(r'class="[^"]*\bdv-leg[a-z-]*\b[^"]*"')


def own_markup(path: Path) -> str:
    """The snippet minus everything the generator injected into it."""
    return INJECTED.sub("", path.read_text(encoding="utf-8"))


def main() -> int:
    verbose = "--verbose" in sys.argv
    unmigrated, migrated, static_unmigrated, legendless = [], [], [], []

    for path in SNIPPETS:
        markup = own_markup(path)
        old, new = markup.count(OLD_HOOK), markup.count(NEW_HOOK)
        legend_class_hits = LEGEND_CLASS.findall(markup)
        if old:
            unmigrated.append((path.name, old, new))
        elif new:
            migrated.append((path.name, new))
        elif legend_class_hits:
            # (c) — legend-shaped markup present, but neither hook fired. This is the #66 case:
            # a static host (`dv-legend`, or any other dv-leg* token the corpus doesn't already
            # explain) that was never wired to the toggle/isolate machinery either model expects.
            static_unmigrated.append((path.name, sorted(set(legend_class_hits))))
        else:
            legendless.append(path.name)

    print("Legend migration — DV-D11 wave (member MARKUP only; injected blocks stripped)\n")
    for name, n in migrated:
        print(f"  ✅ {name:34} migrated — {n} dv-legrow row(s)")
    for name in legendless:
        print(f"  ·  {name:34} no legend — nothing to migrate")
    for name, hits in static_unmigrated:
        sample = hits[0]
        print(f"  ⚠  {name:34} static legend present but not migrated and not subscribed — {sample}")
    for name, old, new in unmigrated:
        mixed = f", {new} NEW" if new else ""
        print(f"  ⬛ {name:34} NOT migrated — {old} data-series-toggle hook(s){mixed}")

    if verbose:
        print("\n(raw grep, for contrast — this is the check that cannot work)")
        for path in SNIPPETS:
            raw = path.read_text(encoding="utf-8").count(OLD_HOOK)
            print(f"  {path.name:34} {raw} raw hit(s) incl. the injected block")

    print()
    if static_unmigrated:
        names = " · ".join(n for n, _ in static_unmigrated)
        print(f"⚠ STATIC LEGEND UNRESOLVED — {len(static_unmigrated)} member(s) carry unclassified")
        print(f"   legend markup, subscribed to neither model: {names}")
        print("   Migrate to `class=\"dv-legrow\"` (or confirm genuinely legendless and delete the")
        print("   static host) before this gate can authorise anything for that member.")
    if unmigrated:
        names = " · ".join(n for n, _, _ in unmigrated)
        print(f"⬛ WAVE INCOMPLETE — {len(unmigrated)} member(s) remain: {names}")
        print("   Keep the TRANSITIONAL block in canon/dv-behaviour.js.")
        return 1
    if static_unmigrated:
        return 1

    print("✅ WAVE COMPLETE — no member's own markup carries the old hook.")
    print("   Now: delete the TRANSITIONAL block in canon/dv-behaviour.js · promote")
    print('   `class="dv-legrow` to dv-legend\'s universal contract and drop it from the')
    print("   members' extraContracts · delete each member's dead .dv-legend*/.dv-legbtn*")
    print("   /.dv-quiet CSS · re-run _build_all.py (page budget should fall to ~85%).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
