#!/usr/bin/env python3
"""#269 wrap — ritual step 4. Inscribe s269-D1 … s269-D10 through the ONLY sanctioned writer.

⛔ THE DO-NOT-RULE DISCIPLINE THIS FILE ENACTS. Every `says` below is DAVE'S SENTENCE, VERBATIM
(spelling as he typed it — `s269-D7` is the ruling that makes a corrected spelling still his
words, and it is applied to the OTHER quotes, never to itself). Every `ruled` field states the
CONDUCTOR'S READING of that sentence and SAYS SO IN ITS OWN TEXT — the numbered readings of the
six KG-gap recommendations are a reading, not his words, and the whole point of the quote gate
this session built is that the two are never blurred.

D1…D6 all quote ONE sentence because he accepted the six in one breath.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

SIX = (
    "Dave, chat, 2026-09-14, verbatim (his spelling, uncorrected): \"I think your "
    "recommendations for the 6 look good, personas and JTBD is interesting but we don't have "
    "any we can rely on, could we create placeholders, or create our own on the back of some "
    "research? I don't want to loose the idea. We will be adding more, for example I'm trying "
    "to get hold of our CX principles.\" Full text: "
    "notes/_lanes/269/kg-gaps/DAVE-RULINGS-2026-09-14.md (commit 33b709d)."
)

EV_SIX = [
    "notes/_lanes/269/kg-gaps/DAVE-RULINGS-2026-09-14.md",
    "_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html",
    "commit 33b709d",
]

READING = ("CONDUCTOR'S READING of the sentence in `says`, labelled as a reading and NOT as "
           "Dave's words: ")

ENTRIES = [
    {
        "id": "s269-D1",
        "ruled": READING + "GO on the KG-gap proposal's recommended order 1-5 - "
                 "(1) roles + DESK fields, (2) the 470 tagged rules, (3) the 145 principles "
                 "plus 22 polarity edges, (4) icons then logos, (5) the edge types setIn / "
                 "behaviourFrom / capturedFrom / acceptsCapability. Nothing in the proposal is "
                 "enacted by this ruling: each step still PROPOSES its schema diff and Dave "
                 "ratifies it, because a new edge type is a vocabulary change (#75).",
        "date": "2026-09-14",
        "by": "Dave",
        "says": SIX,
        "governs": ["_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html",
                    "knowledge/_build_kg_explorer.py", "knowledge/gen_kg_edges.py"],
        "evidence": EV_SIX,
        "status": "ruled",
    },
    {
        "id": "s269-D2",
        "ruled": READING + "THE UX-PRINCIPLE NODE PREFIX IS `ux:`. The prefixes `principle:` "
                 "and `guideline:` are ALREADY TAKEN by the WCAG family in the graph - measured "
                 "in notes/_lanes/269/kg-gaps/A-inventory.json, not assumed - so the 145 "
                 "in-house principles enter under `ux:` and never collide with WCAG.",
        "date": "2026-09-14",
        "by": "Dave",
        "says": SIX,
        "governs": ["_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html",
                    "knowledge/_build_kg_explorer.py"],
        "evidence": EV_SIX,
        "status": "ruled",
    },
    {
        "id": "s269-D3",
        "ruled": READING + "TOKENS ENTER THE GRAPH AT TIER GRAIN - semantic versus primitive - "
                 "and NEVER as 932 leaf nodes. The leaf-per-token shape was priced and rejected "
                 "as a graph that cannot be read.",
        "date": "2026-09-14",
        "by": "Dave",
        "says": SIX,
        "governs": ["_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html",
                    "knowledge/_build_kg_explorer.py"],
        "evidence": EV_SIX,
        "status": "ruled",
    },
    {
        "id": "s269-D4",
        "ruled": READING + "A PHOTOGRAPHY NODE IS THE MANIFEST ROW, with the original and its "
                 "derivatives carried as ATTRIBUTES of that row rather than as separate nodes. "
                 "Declared beside it: the photography KG-NOTE is STALE - it says 12 derivatives "
                 "and the folder holds 251.",
        "date": "2026-09-14",
        "by": "Dave",
        "says": SIX,
        "governs": ["_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html"],
        "evidence": EV_SIX,
        "status": "ruled",
    },
    {
        "id": "s269-D5",
        "ruled": READING + "COMPONENT METAS CITE PRINCIPLES, AND THE FIRST SET IS THE SIX "
                 "A-GRADE LAWS - not all 145 at once. The citation edge starts where the "
                 "evidence is strongest and widens later on his word.",
        "date": "2026-09-14",
        "by": "Dave",
        "says": SIX,
        "governs": ["_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html",
                    "knowledge/components/meta.schema.json"],
        "evidence": EV_SIX,
        "status": "ruled",
    },
    {
        "id": "s269-D6",
        "ruled": READING + "TWO NEW ENTITY KINDS ARE IN SCOPE NOW - content standard and "
                 "lifecycle status. PERSONA AND JTBD ARE NOT DROPPED: he asked for placeholders "
                 "or research-backed provisional personas in his own sentence (\"I don't want to "
                 "loose the idea\"), and the idea is PARKED WITH A TRIPWIRE as P-269-9 in "
                 "knowledge/_parked.json, firing when knowledge/guidelines moves - which is when "
                 "the CX principles he is chasing arrive.",
        "date": "2026-09-14",
        "by": "Dave",
        "says": SIX,
        "governs": ["_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html",
                    "knowledge/_parked.json", "knowledge/components/meta.schema.json"],
        "evidence": EV_SIX,
        "status": "ruled",
    },
    {
        "id": "s269-D7",
        "ruled": "A SPELLING CORRECTION INSIDE A QUOTE OF DAVE'S IS STILL HIS WORDS; A CHANGED "
                 "WORD OR DIGIT IS NOT. knowledge/_quote_gate.py implements exactly that line: "
                 "\"resaech\" -> \"research\" passes as his, \"six\" -> \"6\" does not, and "
                 "punctuation and markdown marks are transcription rather than a miss. The gate "
                 "is ADVISORY and read-only.",
        "date": "2026-09-13",
        "by": "Dave",
        "says": "Dave, chat, 2026-09-13, verbatim: \"obviously this should be corrected, I have "
                "very dyslexic fingers as well as my very bad spelling brain\".",
        "governs": ["knowledge/_quote_gate.py", "knowledge/_ngram.py"],
        "evidence": ["knowledge/_quote_gate.py", "commit 6fd65b4", "commit 4f116c2"],
        "status": "ruled",
    },
    {
        "id": "s269-D8",
        "ruled": "THE DEMO AUDIENCE PHRASE IS \"an operator not a platform owner\" - HIS "
                 "ORIGINAL WORDING, restored to the run-of-show and the demo-prep page where a "
                 "paraphrase had put \"designer\". Found by the quote gate on its first day, "
                 "which is the receipt for the gate as much as for the phrase.",
        "date": "2026-09-13",
        "by": "Dave",
        "says": "Dave, chat, 2026-09-13, verbatim: \"'an operator not a platform owner' is the "
                "original phrase I think\".",
        "governs": ["notes/_RUN-OF-SHOW-david-rice-2026-09-10-v1.html",
                    "notes/_DEMO-PREP-david-rice-hsbc.html"],
        "evidence": ["notes/_RUN-OF-SHOW-david-rice-2026-09-10-v1.html",
                     "notes/_DEMO-PREP-david-rice-hsbc.html", "commit 6fd65b4"],
        "status": "ruled",
    },
    {
        "id": "s269-D9",
        "ruled": "THE N-GRAM DOORS WERE BUILT UNDER THIS WORD, AND THE CONDITION IN IT IS PART "
                 "OF THE RULING: safe, with the usual dependencies and externalities tested. "
                 "knowledge/_ngram.py (11 bites), knowledge/_quote_gate.py (14 bites) and "
                 "knowledge/_near_dupes.py are all READ-ONLY and ADVISORY, and the memento pack "
                 "was left byte-identical - _search_core.py and _memento_search.py are pinned by "
                 "_validate_package_delta.py, so any ranking change is a RELEASE, not an edit "
                 "(parked as P-269-1 / P-269-2).",
        "date": "2026-09-13",
        "by": "Dave",
        "says": "Dave, chat, 2026-09-13, verbatim (his spelling, uncorrected): \"as long as it's "
                "safe and you test the usual dependancies and externalities lets go for it\" and "
                "\"we are well behind pace so you can be really thorough and use fable level "
                "judgment liberally\".",
        "governs": ["knowledge/_ngram.py", "knowledge/_quote_gate.py",
                    "knowledge/_near_dupes.py", "knowledge/_validate_package_delta.py"],
        "evidence": ["knowledge/_ngram.py", "knowledge/_near_dupes.py", "commit d8ebc51",
                     "commit f02fe4c"],
        "status": "ruled",
    },
    {
        "id": "s269-D10",
        "ruled": "A PARKED ITEM IS RECORDED WITH A TRIPWIRE, NOT WITH A PROMISE. "
                 "knowledge/_parked.json is the register (P-269-1 ... P-269-9) and "
                 "knowledge/_parked.py is the door (--check / --due <event> / --list / "
                 "--selftest, 10 bites); six events can fire a row - release-cut, kg-edge-gen, "
                 "dream-pass, memento-cut, token-report, guidelines-ingest - through five hooks "
                 "that PRINT ONLY, are wrapped in try/except and never return a verdict. Driven, "
                 "not asserted: a v1.0.14 manifest fires three. Park items HERE, never in "
                 "_CARRIES.md, whose contract is carrying and not scheduling.",
        "date": "2026-09-14",
        "by": "Dave",
        "says": "Dave, chat, 2026-09-13, verbatim: \"store them for future sake, can they be "
                "triggered, or can we have a hook so they don't get missed at the appropriate "
                "time\"; and 2026-09-14: \"okay we need this recorded with tripwires\".",
        "governs": ["knowledge/_parked.json", "knowledge/_parked.py",
                    "knowledge/gen_kg_edges.py", "knowledge/_RUNBOOK-dream-pass.md"],
        "evidence": ["knowledge/_parked.json", "knowledge/_parked.py", "commit 445af02",
                     "commit 814344e"],
        "status": "ruled",
    },
]

mode = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
for e in ENTRIES:
    p = os.path.join(HERE, "entry-%s.json" % e["id"])
    with open(p, "w", encoding="utf-8") as f:
        json.dump(e, f, ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "knowledge", "_inscribe_ruling.py"),
                        "--entry", p, mode], capture_output=True, text=True, cwd=ROOT)
    print(e["id"], "rc", r.returncode, (r.stdout or "").strip()[-300:], (r.stderr or "").strip()[-400:])
    if r.returncode != 0:
        sys.exit(1)
