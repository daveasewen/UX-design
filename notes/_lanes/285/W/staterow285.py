#!/usr/bin/env python3
"""#285 wrap — the `s218-D7` store row for this wrap's own filed report.

The doc-row gate's glob covers `notes/_subreports/*.md`: a filed report with no `_state.json` row
FAILS exactly as an unrowed brief does. ⚠ The gate is blind to a document staged in the SAME
commit (#207's postscript), so the row is added HERE rather than discovered by the push.

⛔ `_state.add()` REFUSES without a real close condition — the refusal is the feature, and it is
what refused `W-285lm2` at lane C for the id pattern.
"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state

doc = _state.load()
before = len(doc["items"])
assert not any(i.get("home") == "notes/_subreports/2026-09-18-285-W-wrap.md" for i in doc["items"])

_state.add(
    doc,
    id="W-285wr",
    home="notes/_subreports/2026-09-18-285-W-wrap.md",
    title="#285 W filed report - the delegated capture ritual for #285 -> #286",
    state="open",
    owner="dave",
    opened=285,
    project="apollo",
    links=[
        "notes/_lanes/285/W/WRAP-REPORT.md",
        "notes/_lanes/285/WRAP-MEMORY-HOOK.md",
        "notes/_lanes/285/DAVE-RULINGS-2026-09-18.md",
        "_DECISION-HISTORY/2026-09-18-285-the-b-is-straightened-and-the-seam-re-quotes.md",
        "_HANDOFF-136-the-b-is-straightened-and-the-connector-answer-comes-by-act.md",
        "notes/_subreports/2026-09-18-285-LM2-logo-masters-regen.md",
        "notes/_subreports/2026-09-18-285-SC-seam-standing.md",
        "notes/_subreports/2026-09-18-285-V-verifier.md",
        "notes/_subreports/2026-09-18-285-C-commit.md",
        "notes/_subreports/2026-09-18-285-C2-showroom.md",
        "notes/_subreports/2026-09-18-285-P-push.md",
    ],
    closes_when=(
        "Dave has ruled or explicitly parked the report's ruling-shaped questions - chiefly the "
        "wording of the eight DRAFT lines in knowledge/_standing.md, HOW the accepted masters get "
        "registered in _logo_nodes.json behind the gen_kg_icons.py fence, the _gauge_tokens.py "
        "256,000 wording fix carried from #284, the delegation rule his own sentence states, the "
        "boot ceiling at its tenth reading, whether the skills get a second run after #286's cold "
        "boot measurement, whether the ritual owes a RESUME contract after a mid-ritual sub death, "
        "what to do about _seam.py's SCRATCH arm deleting a lane's own /tmp files, and what a "
        "session should do at the hard wall"
    ),
    why=(
        "The #285 wrap inscribed nothing and verified that by json.load over the rulings list "
        "(620 unchanged at the open and at the close); it STRUCK two carries with receipts - the "
        "#284 masters acceptance, which Dave reopened himself with a 4x crop of the wordmark, and "
        "the showroom's 108 stale pages, re-synced at ff354475 and verified by decoding all 108 "
        "payloads rather than sampling; it recorded Dave's re-acceptance of the regenerated "
        "masters in his own words as an ENACTMENT of s282-D3 rather than a closure of row W-285lm, "
        "whose registration half is untouched behind the generator fence; it named the connector "
        "question as ANSWERED BY AN ACT rather than a sentence, which makes #286's first move a "
        "measurement; it measured the delegation rule OBEYED for a whole session - seven Agent "
        "lanes at spawnDepth 1, none in seat, 3,382 cl100k of replies against about 738,851 real "
        "of sub FILL - without treating that as a closure of a ruling-shaped carry; it closed the "
        "one gate fail that was its own (ds-021 on knowledge/_seam.py, registered estimate-only as "
        "a declaration, not a ruling) while carrying the six inherited ones in the #243 declared "
        "not-a-wrap form for the eleventh wrap; and it named a wrap sub's mid-ritual death on a "
        "network error as luck rather than design, because nothing guarantees all-or-nothing "
        "across the ritual"
    ),
)
_state.save(doc)
print(f"_state.json: {before} -> {len(doc['items'])} items; row W-285wr added")
