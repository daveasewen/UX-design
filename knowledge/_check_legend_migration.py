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


def own_markup(path: Path) -> str:
    """The snippet minus everything the generator injected into it."""
    return INJECTED.sub("", path.read_text(encoding="utf-8"))


def main() -> int:
    verbose = "--verbose" in sys.argv
    unmigrated, migrated, legendless = [], [], []

    for path in SNIPPETS:
        markup = own_markup(path)
        old, new = markup.count(OLD_HOOK), markup.count(NEW_HOOK)
        if old:
            unmigrated.append((path.name, old, new))
        elif new:
            migrated.append((path.name, new))
        else:
            legendless.append(path.name)

    print("Legend migration — DV-D11 wave (member MARKUP only; injected blocks stripped)\n")
    for name, n in migrated:
        print(f"  ✅ {name:34} migrated — {n} dv-legrow row(s)")
    for name in legendless:
        print(f"  ·  {name:34} no legend — nothing to migrate")
    for name, old, new in unmigrated:
        mixed = f", {new} NEW" if new else ""
        print(f"  ⬛ {name:34} NOT migrated — {old} data-series-toggle hook(s){mixed}")

    if verbose:
        print("\n(raw grep, for contrast — this is the check that cannot work)")
        for path in SNIPPETS:
            raw = path.read_text(encoding="utf-8").count(OLD_HOOK)
            print(f"  {path.name:34} {raw} raw hit(s) incl. the injected block")

    print()
    if unmigrated:
        names = " · ".join(n for n, _, _ in unmigrated)
        print(f"⬛ WAVE INCOMPLETE — {len(unmigrated)} member(s) remain: {names}")
        print("   Keep the TRANSITIONAL block in canon/dv-behaviour.js.")
        return 1

    print("✅ WAVE COMPLETE — no member's own markup carries the old hook.")
    print("   Now: delete the TRANSITIONAL block in canon/dv-behaviour.js · promote")
    print('   `class="dv-legrow` to dv-legend\'s universal contract and drop it from the')
    print("   members' extraContracts · delete each member's dead .dv-legend*/.dv-legbtn*")
    print("   /.dv-quiet CSS · re-run _build_all.py (page budget should fall to ~85%).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
