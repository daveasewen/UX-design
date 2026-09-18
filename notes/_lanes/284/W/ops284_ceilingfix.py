#!/usr/bin/env python3
"""#284 wrap — CORRECTION, made before the commit and declared rather than shipped wrong.

Three surfaces (the ⏱ LATEST DELTA, the `Last refreshed` segment and the #284 stratum's
COMMIT STATE) asserted that this wrap's own 2f roll took the boot-drift CEILING BREACH from
SEVEN readings to EIGHT. The gate, run after the roll, names SEVEN: the WINDOW SLID rather
than the count growing — #276 dropped out and #283 came in. The claim is corrected at every
surface that carried it; the measurement, not the prediction, is what ships.
"""
import os, sys
from run_ops import run

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))

GM_OLD_FRAG = ("⚠ **AND THE CEILING BREACH GREW BY THIS WRAP'S OWN 2f ROLL, DECLARED RATHER THAN "
               "DISCOVERED: it named SEVEN readings at the open (#276…#282) and names EIGHT at the "
               "close, because rolling #283's stratum into this file put ITS OWN first-turn reading "
               "inside the gate's window — the figure is #283's and is not restated here, exactly as "
               "`s241-D2` requires.**")
GM_NEW_FRAG = ("⚠ **AND THIS WRAP'S OWN 2f ROLL MOVED THE CEILING BREACH'S WINDOW WITHOUT CHANGING "
               "ITS COUNT — MEASURED AFTER THE ROLL, NOT PREDICTED BEFORE IT: SEVEN readings at the "
               "open (#276…#282) and SEVEN at the close (#277…#283). Rolling #283's stratum into this "
               "file brought #283 in and pushed #276 out; #283's own first-turn figure is not "
               "restated here, exactly as `s241-D2` requires.** ⚠ **This wrap first wrote *eight* and "
               "corrected it against the gate before committing — the prediction is named, not "
               "erased.**")

LS_OLD_FRAG = ("⚠ **AND THE CEILING BREACH GREW BY THIS WRAP'S OWN 2f ROLL, DECLARED RATHER THAN "
               "DISCOVERED: it named seven readings at the open (#276…#282) and names EIGHT at the "
               "close, because rolling #283's stratum into `notes/_GAUGE-LOG.md` put 80,871 into the "
               "gate's window.**")
LS_NEW_FRAG = ("⚠ **AND THIS WRAP'S OWN 2f ROLL MOVED THE CEILING BREACH'S WINDOW WITHOUT CHANGING "
               "ITS COUNT — MEASURED AFTER THE ROLL, NOT PREDICTED BEFORE IT: SEVEN readings at the "
               "open (#276…#282) and SEVEN at the close (#277…#283). Rolling #283's stratum into "
               "`notes/_GAUGE-LOG.md` brought #283 in and pushed #276 out. This wrap first wrote "
               "*eight* and corrected it against the gate before committing.**")

HDR_OLD_FRAG = ("⚠ **AND THE CEILING BREACH GREW BY THIS WRAP'S OWN "
                "2f ROLL, declared rather than discovered: seven readings at the open, EIGHT at the "
                "close, because #283's stratum carried 80,871 into the gate's window.**")
HDR_NEW_FRAG = ("⚠ **AND THIS WRAP'S OWN 2f ROLL MOVED THE CEILING "
                "BREACH'S WINDOW WITHOUT CHANGING ITS COUNT — SEVEN at the open (#276…#282), SEVEN at "
                "the close (#277…#283); #283 came in and #276 went out. This wrap first wrote *eight* "
                "and corrected it against the gate before committing.**")


def one(path, old_frag, new_frag):
    lines = open(os.path.join(ROOT, path), encoding="utf-8").read().split("\n")
    hits = [l for l in lines if old_frag in l]
    assert len(hits) == 1, "%s: %d hit(s)" % (path, len(hits))
    return {"op": "replace", "file": path, "find": [hits[0]],
            "replace": [hits[0].replace(old_frag, new_frag)]}


OPS = [one("GOOD-MORNING.md", GM_OLD_FRAG, GM_NEW_FRAG),
       one("_LIVE-STATE.md", LS_OLD_FRAG, LS_NEW_FRAG),
       one("_LIVE-STATE.md", HDR_OLD_FRAG, HDR_NEW_FRAG)]

if __name__ == "__main__":
    sys.exit(run("ceilingfix", OPS, write="--write" in sys.argv, min_bytes=800))
