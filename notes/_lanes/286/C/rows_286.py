#!/usr/bin/env python3
"""#286 lane C — row the six filed #286 reports THROUGH THE STORE'S OWN WRITER.

WHY SIX AND NOT ONE. The brief asked lane C for its own row (`W-286c`). Measured first, before
adding anything: driving `_gate_doc_rows.py`'s own `population()`/`unrowed()` with the six report
paths planted as staged adds returns **6 unrowed** — none of the four earlier lanes rowed its
report, and the store carries no `notes/_subreports/` directory home. So the doc-row gate would
refuse this commit on all six, and `DOC_ROW_ACK` is explicitly not the remedy. Rowing them is the
fix the gate's own docstring names: "one `_state.add()` call through the store's own writer".

SHAPE: the #285 precedent exactly (`W-285c`, `W-285v`, `W-285p`, `W-285cs` …) — owner dave,
state open, condition stated, opened 286, project apollo, home = the report path, and a
`closes_when` taken from THAT LANE'S OWN ruling-shaped section, never invented here. No lane's
finding is restated as settled and no close condition is put in Dave's mouth.

DRY RUN by default; pass --write to save.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state  # noqa: E402

SUB = "notes/_subreports/2026-09-18-286-"

ROWS = [
    dict(id="W-286s", home=SUB + "S-standing-ratified.md",
         title="#286 lane S — knowledge/_standing.md out of DRAFT, W-285sc closed",
         closes_when=(
             "Dave has read or explicitly parked the lane's ruling-shaped items - chiefly whether "
             "an s286- ruling should be INSCRIBED for the standing ratification (the lane "
             "deliberately inscribed none, under s271-D4), and the stale prose at "
             "knowledge/_seam.py:26 which still calls _standing.md a DRAFT"),
         body=("The eight standing lines are byte-identical; only the header changed (git diff "
               "touches header only) and the seam still prints STANDING 8 lines - 246 cl100k. "
               "W-285sc was closed through the store's module API with Dave's verbatim "
               "\"okay go on everything\" as the receipt. Lane V verified all of this "
               "mechanically (24/24). Committed by lane C.")),

    dict(id="W-286r", home=SUB + "R-masters-registered.md",
         title="#286 lane R — the masters were NOT registered, and the generator is why",
         closes_when=(
             "Dave has ruled the SHAPE of the master registration - the gen_kg_icons.py fence is "
             "released by his \"okay go on everything\" but the generator cannot see "
             "knowledge/assets/logos/masters/, so a --land would register ZERO of the 40 masters; "
             "the three shapes lane R lays out at its section 7 are a closed-vocabulary question "
             "and none of them is a lane's call"),
         body=("THE FINDING, carried into the #286 commit message: the 40 accepted masters live "
               "in knowledge/assets/logos/masters/ and are invisible to the generator's corpus "
               "scan - `8 logos` -> `logo: 8`. The task's acceptable outcome (40 masters, or the "
               "20 masterbrand ones) is NOT reachable by running the generator. Lane R ran no "
               "generator and registered nothing; lane V confirmed both halves independently "
               "(claims 23, 24). The fence is released and the door behind it is bricked up.")),

    dict(id="W-286g", home=SUB + "G-gauge-wording-and-boot-cold.md",
         title="#286 lane G — the 256,000 wording fix in the gauge, and the boot-cold finding",
         closes_when=(
             "Dave has ruled or explicitly parked the 58 OWED locations across 10 live prose/"
             "ratified files that still carry the old 256,000 wording (amending a ratified "
             "surface is his word, not a lane's), plus the 4 FENCED locations in "
             "knowledge/_seam.py"),
         body=("knowledge/_gauge_tokens.py and knowledge/_capture_gate.py carry the wording fix. "
               "Lane V's D1 corrects the scope claim: _capture_gate.py is EXACTLY wording (AST "
               "identical under string normalisation) but _gauge_tokens.py also adds three "
               "print() statements to main() - no constant, no branch, no condition. The lane "
               "also filed the boot-cold reading and the s241-D2 instruction that the wrap log "
               "73,832 ONCE, in the post-mortem line. Committed by lane C.")),

    dict(id="W-286t", home=SUB + "T-seam-inseat-and-quiet-commit.md",
         title="#286 lane T — the seam's INSEAT arm and --quiet on _git_commit.sh",
         closes_when=(
             "Dave has ruled or explicitly parked the lane's three ruling-shaped questions - "
             "chiefly that INSEAT_WARN_TK = 10,000 is PICKED BY THE LANE, NOT RULED (the source, "
             "the registry entry and the printed line all say so on themselves), and whether the "
             "INSEAT verdict should ever become blocking"),
         body=("knowledge/_seam.py gains the INSEAT block (+213/-7) and knowledge/_git_commit.sh "
               "gains --quiet; knowledge/_capture_gate.py gains the ds-021 registration for the "
               "_seam.py MEASURERS entry (\"estimate-only\"). Lane V carries two unfixed defects "
               "on --quiet: D2, --quiet=<path> accepts any path with no git check-ignore guard; "
               "D3, the keep-filter is column-anchored so INDENTED verdict lines are dropped from "
               "the live stream on a green run. Neither can hide a refusal - any non-zero exit "
               "replays the whole transcript unfiltered, which lane V drove twice and lane C did "
               "not need to. UNPROVEN and declared by lane T: the INSEAT arm under COMPACTION.")),

    dict(id="W-286v", home=SUB + "V-verifier.md",
         title="#286 lane V — 24 of 24 testable claims PASS; six defects, two handed to the commit lane",
         closes_when=(
             "Dave has read the verdict table and either accepted the findings as answered or "
             "named which ones still need work - the live carries being D1 (the gauge change is "
             "wording plus three prints), D2 and D3 (the --quiet guards), D4 (W-285lm's "
             "closes_when and body disagree and the store's gate cannot catch it) and D6 (a "
             "stranded .git/index.lock that predates every lane)"),
         body=("HEADLINE: 24 of 24 testable claims PASS, no blocks-commit defect in the four "
               "lanes' own work. Two defects were handed to lane C and both are CLEARED there: "
               "D0, the accidental revert-and-restore of knowledge/_capture_gate.py, re-verified "
               "by lane C at git hash-object b28301ec9c8f159b464c9b554124cc793fe4a925 with BOTH "
               "lane G's wording hunks and lane T's ds-021 hunk present in git diff HEAD; and D5, "
               "the two undeletable symlink farms under notes/_lanes/286/V/, mv'd to "
               "_to_delete/286-V-symlinks/ (gitignored at .gitignore:34) per the #284 precedent. "
               "Lane C measured the farms at 449 entries EACH, not the 106 lane V counted - the "
               "mirrors hold real subdirectories that themselves hold symlinks, so the exposure "
               "was 898 symlink entries, not 212.")),

    dict(id="W-286c", home=SUB + "C-commit.md",
         title="#286 lane C — the commit: two verifier defects cleared, five lanes landed",
         closes_when=(
             "Dave has read or explicitly parked the lane's findings - chiefly that lane V's D5 "
             "symlink count was under by a factor of four (898, not 212), that `ds-021` is a "
             "DERIVED id and not a source literal so the brief's own verification recipe greps "
             "for a string that is not there, and that _CHAIN.md was regenerated on a staleness "
             "that PREDATES this session (GOOD-MORNING.md and _LIVE-STATE.md are both clean)"),
         body=("The commit lane for #286. Verified knowledge/_capture_gate.py before staging as "
               "lane V's D0 required (hash b28301ec..., 4 pre-existing _governs.py selftest fails "
               "only, both lanes' hunks present in the diff); moved the two symlink farms out to "
               "the gitignored _to_delete/286-V-symlinks/ with mv, never rm, per the sandbox "
               "delete-guard; regenerated _CHAIN.md after _gen_chain.py --check refused. Rowed "
               "all six #286 reports here because the doc-row gate measured six unrowed and "
               "DOC_ROW_ACK is not the remedy. Commit only via knowledge/_git_commit.sh with "
               "every path named (the P5 rule). NOT pushed.")),
]

COMMON = dict(state="open", owner="dave", opened=286, project="apollo", condition="stated")

doc = _state.load()

ok0, fails0, notes0 = _state.check(doc)
print(f"PRE  check ok={ok0} fails={len(fails0)} notes={len(notes0)}")
for f in fails0:
    print("  pre-existing ⛔", f)

have = {i["id"] for i in doc["items"]}
for r in ROWS:
    if r["id"] in have:
        sys.exit(f"REFUSED — {r['id']} already exists; this lane does not overwrite another row.")

for r in ROWS:
    fields = dict(COMMON)
    fields.update(r)
    fields["links"] = ["notes/_subreports/2026-09-18-286-V-verifier.md",
                       "notes/_lanes/286/DAVE-RULINGS-2026-09-18.md"]
    _state.add(doc, **fields)
    print("ADDED", r["id"], "->", r["home"])

ok1, fails1, notes1 = _state.check(doc)
print(f"POST check ok={ok1} fails={len(fails1)}")
mine = [f for f in fails1 if any(f.startswith(r["id"]) for r in ROWS)]
for f in mine:
    print("  MINE ⛔", f)
if mine:
    sys.exit("REFUSED by the gate — not saving.")
new = [f for f in fails1 if f not in fails0]
for f in new:
    print("  NEW (not id-prefixed) ⛔", f)
if new:
    sys.exit("REFUSED — this script introduced a new gate failure. Not saving.")

if "--write" in sys.argv:
    _state.save(doc)
    print("SAVED")
else:
    print("DRY RUN — nothing written")
