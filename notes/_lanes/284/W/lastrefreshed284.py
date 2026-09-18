#!/usr/bin/env python3
"""#284 wrap — the `Last refreshed:` line of `_LIVE-STATE.md`, in ONE transaction:

  (a) the new **#284** segment is prepended and #283's becomes the first `Previous:`;
  (b) the **#280** `Previous:` chain segment is EXTRACTED VERBATIM — its span asserted IN
      THIS PROCESS before anything is written — moved to `_LIVE-STATE-ARCHIVE.md`
      § Rolled 2026-09-18 #284 (beside the #281 ⏱ delta block this wrap rolled), and
      replaced in place by the standing `*Last refreshed (#280, trimmed at the #284 wrap)…*`
      note the #253…#283 wraps all wrote. ⛔ Nothing is deleted — moved.

The boundary moves ONE session per wrap and is one behind the 2d delta roll, exactly as
#283 (delta #280 rolled, chain segment #279 moved).
"""
import os, sys
from run_ops import run

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")

lines = open(LS, encoding="utf-8").read().split("\n")
hits = [i for i, l in enumerate(lines) if l.startswith("*Last refreshed: ")]
assert len(hits) == 1, hits
i = hits[0]
old = lines[i]

# ---- (b) extract the #280 chain segment, span asserted HERE ---------------------------------
START = "Previous: 2026-09-17 (Thu from `date` — **#280 wrap**."
END = "*Last refreshed (#279, trimmed at the #283 wrap)"
a = old.index(START)
b = old.index(END, a)
segment = old[a:b]
assert old.count(START) == 1, "the #280 segment anchor is not unique"
assert len(segment) > 4000, "the extracted #280 segment is implausibly short: %d" % len(segment)
assert segment.rstrip().endswith(")*"), segment[-40:]
print("extracted #280 chain segment: %d chars" % len(segment))

NOTE = ("*Last refreshed (#280, trimmed at the #284 wrap): #280's `Previous:` chain segment was "
        "moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-18 #284, in the same section "
        "as the #281 ⏱ delta block this wrap rolled. Nothing was deleted — moved.*  ")

NEW284 = (
 "2026-09-18 (Fri from `date` — **#284 wrap**. ✅ **NO DATE SPLIT: the session, its one commit, this "
 "ritual and its own commit are ALL 2026-09-18.** ⛔★★★ **READ "
 "`_HANDOFF-135-the-logo-masters-land-and-the-disk-lever-is-found.md` FIRST — IT IS NEWER THAN "
 "`_CHAIN.md` AND OUTRANKS IT**, and it does NOT replace `_HANDOFF-130`…`-134`, whose open items "
 "still stand. ⛔★★ **NO RULING WAS INSCRIBED AND `knowledge/_rulings.json` STAYS AT 620, verified "
 "at this seat by `json.load` rather than restated.** Two ruling-shaped things are on the table and "
 "**neither is inscribed, because inscribing is Dave's**: the delegation rule he restated, and the "
 "`_gauge_tokens.py` 256,000 wording fix the window finding implies. ★★ **THE 40 PER-SIZE LOGO "
 "MASTERS ARE DRAWN AND ACCEPTED BY EYE — `s282-D3` ENACTED.** One Opus lane (LM) built "
 "`knowledge/assets/logos/_gen_masters.py` (`--check` rc 0) and 40 SVGs under "
 "`knowledge/assets/logos/masters/` — 8 lockups × 5 raw heights 24/28/32/36/40, raw px width and "
 "height, no viewBox, hexagon exact on the h/4 grid, wordmark stems snapped, masterbrand widths "
 "89/104/119/133/148 — and his word off the contact sheet was ***\"the sheet is good BTW\"***. ⚠ "
 "**One flaw the lane named and he accepted over: the B's horizontals sit a pixel off the H's "
 "crossbar at 24 and 40.** ⛔ **NOT registered in `_logo_nodes.json`** (generator fence) — the open "
 "half of row `W-284lm`. ⛔★★★ **THE DISK LEVER #283 SAID DID NOT EXIST WAS FOUND AND PULLED, AND "
 "THE FIRST ACT OF #284 IS A RETRACTION OF #283'S OWN CLAIM.** `_HANDOFF-134` § THE DISK item 4 "
 "reads *\"NOT fixable from inside. NOT fixable from his Mac.\"* — **the second half is FALSE**: the "
 "VM disk is a bundle on Dave's Mac under `~/Library/Application Support/Claude/`, he pasted a web "
 "how-to (*\"we've done all this i guess\"*), was instructed, and **quit the app and trashed "
 "`claudevm.bundle` leaving the `warm` folder**. `/sessions` went **98.7% (127,716 KB free) → 0.1% "
 "(9,665,792 KB free)**, `uptime` 1 min, **the 127 dead homes gone** — and ★★ **THE SESSION SURVIVED "
 "THE REBUILD, the same chat continuing**, which `notes/_lanes/284/DISK-LEVER-2026-09-18.md` "
 "predicted it would not; that prediction is published as wrong rather than quietly corrected. ⛔ "
 "**A FINDING PLUS AN ACT, NOT A RULING** (filed, committed `ade8a403`); the carry is STRUCK with "
 "its receipt (`s183-D1`/`s188-D2`) and its body left unedited. ⛔★★ **THE CONTEXT-WINDOW FINDING "
 "AND DAVE'S CORRECTION.** Anthropic's help centre states a **1M** window for Fable 5.1 / Opus 5 in "
 "Cowork on a paid plan, with auto-compaction near the limit and *\"tools and connectors are "
 "token-intensive\"*; the conductor proposed re-basing the stop line and **Dave corrected him in the "
 "same turn — *\"but we gauged this against the messy middle problem not the 1M context window, "
 "that was actually relevant then as it is now\"*** ⇒ ★ **the 180,000 line is the QUALITY line and "
 "it STANDS; this is a finding, not a re-base, and no constant moved.** ⚠ What it does change: the "
 "256,000 *hard* figure is **not a wall for this model**, so #277/#281/#282's *\"hard-line "
 "breaches\"* were quality breaches — **a WORDING fix in `_gauge_tokens.py`, his to order, NOT "
 "DONE**. ⬛★★ **THE DELEGATION LAPSE, RULING-SHAPED AND HIS: *\"I thought we had a subs strategy, "
 "basically everything is Delegated even if its a fable sub and the lane is always an orchestrator "
 "and judgment layer so we can get more work done in a session, this seems to have been lost\"*** — "
 "restating #57 / `s204-D1`. The conductor did lane work IN SEAT four times (disk + spec ~15K · "
 "**six commit-script runs ~30K** · two screenshots read in-seat · the research in-seat) and **only "
 "the drawing was a lane**; his proposed mechanical fix — a conductor in-seat tool-output arm on "
 "`_seam.py`, a routing line at the opener, the commit as a lane by default — is **PROPOSED AND NOT "
 "BUILT**, and a conductor's proposal is not Dave's ruling. ⚙ **GAUGE, MEASURED AT THIS SEAT against "
 "the conductor's own transcript** `8fa773d6-db0f-4579-b387-cdd6bfc942fb.jsonl`, identified by its "
 "boot reading back to the token: **FILL 217,359 real over 48 turns** against **195,366 real / 36 "
 "turns DECLARED** at the brief cut ⇒ **delta 21,993**. ⛔ **37,359 past the ruled 180,000 stop "
 "line**, ✅ **2,641 INSIDE the ≤220,000 tolerance**, ✅ **256,000 NOT BREACHED — the second session "
 "running**. **BOOT 80,882 real, n=1** — +10,088 on the `s129-D1` floor 70,794, **NOT a re-base**, "
 "`BOOT_FIRSTTURN_TK` untouched, and the **NINTH** post-diet reading over `BOOT_CEILING_TK` 70,000: "
 "**cut the boot, never raise the literal** [[gate-must-quote-what-it-forbids]]. ★ **subs 159,965 "
 "across n=1** (lane LM, 57 tool uses, 797 s) — QUOTA, never FILL. ⛔ **NO PACE PANEL WAS ASKED FOR "
 "AND NONE IS INVENTED.** ⚠ **Fill drivers NAMED: ~107K of tool output at the opener, the six commit "
 "runs, two images — and the lane cost the window ~300 tokens**, which is the delegation argument in "
 "one number. ⛔ **`/sessions` 1.6% used, 9,527,112 KB free measured here** (`df` reads 2% / "
 "9,528,760 KB available) against the brief's **0.1% / 9,665,792 KB free** taken at the rebuild — "
 "**both published, neither rewritten**. ⛔ **SEVEN BLOCKING GATE FAILS STOOD AT THE OPEN; SIX ARE "
 "INHERITED AND CARRIED IN THE `#243` FORM — the TENTH consecutive wrap on that path** (the "
 "boot-drift ceiling breach and five boot double-counts: #243, #264, #272, #273, #274), **and a wrap "
 "may not repair an inherited gate fail.** ⚠ **The seventh was this seat's own — an instrument "
 "stray, `knowledge/assets/logos/_gen_masters.py.t3-rendered` — moved by a same-mount `mv` to "
 "`_to_delete/strays-284/`, never gitignored.** ⚠ **AND THE CEILING BREACH GREW BY THIS WRAP'S OWN "
 "2f ROLL, declared rather than discovered: seven readings at the open, EIGHT at the close, because "
 "#283's stratum carried 80,871 into the gate's window.** ⛔ `_validate_roles_resolve.py` **FAIL(6)** "
 "· `_validate_lane_ownership.py --selftest` **2/3** · `showroom/` **138** against an inscribed "
 "*\"108 stale\"* — all inherited, both showroom readings stand, his call. Gauge, declared skips with "
 "their sizes, the cloud-store result and not-done: the ⏱ LATEST DELTA below. **`_CARRIES.md` § `## "
 "residual → #285` is the carry set (`s225-D2`) — 539 probeable items, FOUR new, ONE STRIKE.** "
 "**This wrap's own filed report (`s218-D7`): `notes/_subreports/2026-09-18-284-W-wrap.md`.** "
 "**Narrative dossier (1b): "
 "`_DECISION-HISTORY/2026-09-18-284-the-logo-masters-and-the-disk-lever.md`.** **His words verbatim: "
 "`notes/_lanes/284/DAVE-RULINGS-2026-09-18.md`.**")

rest = old[len("*Last refreshed: "):]
new = "*Last refreshed: " + NEW284 + ")*  Previous: " + rest
assert new.count(START) == 1
new = new.replace(START + segment[len(START):], NOTE, 1) if False else new
# the extraction indices shift by the prepend; re-locate on the NEW string and splice there
a2 = new.index(START)
b2 = new.index(END, a2)
assert new[a2:b2] == segment, "the #280 span did not survive the prepend byte-identically"
new = new[:a2] + NOTE + new[b2:]
assert START not in new, "the #280 segment is still present after the trim"
assert len(new) == len(old) + len(NEW284) + len(")*  Previous: ") - len(segment) + len(NOTE)

ARCHIVE_LINES = [
    "",
    "### #280's `Previous:` chain segment — moved VERBATIM at the #284 wrap (`Last refreshed` trim)",
    "",
    segment.rstrip(),
    "",
]

OPS = [
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [old], "replace": [new]},
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
     "at": "## Rolled 2026-09-18 #284 (2d, at the #284 wrap) — via the mover", "where": "after",
     "lines": ARCHIVE_LINES},
]

if __name__ == "__main__":
    sys.exit(run("lastrefreshed", OPS, write="--write" in sys.argv, min_bytes=2000))
