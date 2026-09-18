#!/usr/bin/env python3
"""#285 wrap — the three MISSING `s218-D7` store rows the doc-row gate refused on, post-staging.

⚠ SECOND INSTANCE OF THE SAME FINDING IN ONE SESSION: `_state.add()` REFUSED `W-285c2` with
`id does not match '^(?:W-[0-9]{1,3}[a-z]{0,2}|G[0-9]{1,2}[a-z]?)$'` — the pattern allows at most
two trailing lowercase letters and NO DIGIT AFTER THEM. Lane C met it on `W-285lm2`; this seat met
it on `W-285c2`. The showroom row is therefore `W-285cs`. ⛔ A FINDING, NOT A FIX: the pattern is
not widened here, because an id scheme is a convention and changing one at a wrap is not this
seat's call.

⛔ NAMED, NOT SMOOTHED, AND NOT `DOC_ROW_ACK`'d. The C, C2 and P lanes each filed a report and
none of them rowed it; the gate found all three at the wrap, which is exactly the
forgotten-document class it exists to catch. The remedy it names is one `_state.add()` per
report, and that is what this does — an ack would have declared the gap instead of closing it,
for no reason other than haste.
"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state

doc = _state.load()
before = len(doc["items"])

ROWS = [
 dict(id="W-285c", home="notes/_subreports/2026-09-18-285-C-commit.md",
      title="#285 C filed report - the commit lane that landed LM2 + SC (b99d092c)",
      links=["notes/_subreports/2026-09-18-285-LM2-logo-masters-regen.md",
             "notes/_subreports/2026-09-18-285-SC-seam-standing.md",
             "knowledge/_RUNBOOK-git-commit.md"],
      closes_when=("Dave has read or explicitly parked the lane's ruling-shaped questions - chiefly "
                   "the store id pattern that REFUSED W-285lm2 (no digit after the trailing letters, "
                   "so the LM2 row is W-285lm) and the declared showroom gap this lane measured, "
                   "verified and then reverted rather than landing"),
      why=("Lane C landed b99d092c in three runs, each refusal the script working: the showroom sync "
           "gate, the doc-row gate and a chain-stale check. It met a stranded .git/index.lock at lane "
           "start with the documented stale 0-byte signature and did NOT rm it - the script's own "
           "clear_locks() mv-aside cleared it, which is the sanctioned path. It also measured the "
           "108-page showroom re-sync, verified it, and then REVERTED it as a DECLARED gap rather "
           "than widening its own scope; Dave's '1. go' turned that measurement into lane C2")),
 dict(id="W-285cs", home="notes/_subreports/2026-09-18-285-C2-showroom.md",
      title="#285 C2 filed report - the showroom re-sync commit lane (ff354475)",
      links=["notes/_subreports/2026-09-18-285-C-commit.md",
             "notes/_lanes/285/DAVE-RULINGS-2026-09-18.md"],
      closes_when=("Dave has read or explicitly parked the lane's findings - chiefly that showroom/ "
                   "holds 138 top-level .html because 137 are generator-owned and index.html is "
                   "owned by gen_library_214.py, so the long-carried '138 v 108' is an explanation "
                   "rather than a gap, and that the W-285lm row was amended with his acceptance "
                   "through the store's own writer without inventing a close condition"),
      why=("Cut on Dave's '1. go'. Two runs, cap four. It ran exactly one generator - the one the "
           "gate itself names - and verified the 108-page diff BY DECODING every base64 payload "
           "rather than sampling: non-payload lines byte-identical in all 108, and in all 108 the "
           "single changed line is the old line with :is( replaced by :where( and nothing else. It "
           "recorded Dave's '2. accept' into the W-285lm row's body, leaving closes_when untouched, "
           "so an acceptance did not become an invented closure")),
 dict(id="W-285p", home="notes/_subreports/2026-09-18-285-P-push.md",
      title="#285 P filed report - the push lane that refused on a dirty tree, and its CI read-back",
      links=["notes/_subreports/2026-09-18-285-C-commit.md",
             "notes/_subreports/2026-09-18-285-C2-showroom.md"],
      closes_when=("Dave has read or explicitly parked the lane's finding - that the ratified push "
                   "path refused on a tree made dirty by OTHER lanes' outputs, so a push lane cut "
                   "before the session's own reports are committed cannot succeed, and whether the "
                   "push should therefore be cut only after the wrap's commit"),
      why=("The lane ran the only sanctioned push path and got '✗ push refused: tree not clean - "
           "commit first (s133-D2; rehearsal log excluded per s137-D1)', naming three dirty paths "
           "that belonged to other lanes. It was forbidden to commit, so it STOPPED and said so "
           "rather than widening its scope to clear its own blocker - the lane contract working. It "
           "also read CI back unauthed and quoted three runs literally, claiming no colour for a "
           "commit that was not on the remote")),
]
for r in ROWS:
    _state.add(doc, state="open", owner="dave", opened=285, project="apollo", **r)
_state.save(doc)
print(f"_state.json: {before} -> {len(doc['items'])} items; rows " + ", ".join(r["id"] for r in ROWS))
