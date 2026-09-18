#!/usr/bin/env python3
"""#286 lane R2 — row this lane's report as `W-286r`, through the store's own writer.

Same module API as close_w285lm.py: `_state.add()` is the one convenience wrapper and it
REFUSES a row with no close condition, which is the feature. `_state.json` is never hand-edited.

DRY RUN by default; pass `--write` to save.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state  # noqa: E402

REPORT = "notes/_subreports/2026-09-18-286-R2-masters-registered-as-sizes.md"

BODY = (
    '⬛ LANDED. The 40 accepted per-size logo masters are registered in knowledge/_logo_nodes.json '
    'as a `sizes` map on the 8 EXISTING logo nodes — Dave 2026-09-18, verbatim: '
    '"okay size-on-the-existing-node" (receipt: notes/_lanes/286/DAVE-RULINGS-2026-09-18.md). '
    'MEASURED: nodes 8 -> 8 (0 added, 0 removed), edges 33 -> 33 with the multiset identical, and '
    'the only other changes are `$description` and `$s282-D5.generatorVerdict`. Each of the 40 '
    'entries carries the relative path, the SVG\'s own width/height and its sha256, all re-verified '
    'against the bytes on disk. gen_kg_icons.py gained logo_masters()/svg_box() and 2 selftest '
    'bites (24, all green); `logo_stems()` is deliberately still NON-recursive, because making it '
    'recursive is how 40 `logo:<stem>-<h>` ids would be minted — the shape Dave refused. #75 is '
    'untouched: a FIELD on an existing kind is neither a new node kind nor a new edge type, and '
    'RATIFIES is unchanged.  ⬛ --land NOW MERGES INSTEAD OF CLOBBERING. It reads the landed file '
    'first and keeps, by provenance marker and not by today\'s values: every edge marked '
    '`authored: "hand"` (the 12 governedBy edges of s282-D5 are byte-identical after the run, and '
    '0 t:null stubs came back), the edge_types line for a type such an edge draws, every top-level '
    'key the generator does not produce (`$s282-D5`, `ratified`), and — after the finding below — '
    'every row-level FIELD of a rebuilt ledger row that the build does not produce. The '
    'generatorVerdict now records what was preserved, idempotently.  ⛔ SECOND FINDING, not in the '
    'brief: `_icon_nodes.json` has its OWN hand-repair script '
    '(notes/_lanes/280/inscribe-active/_inscribe2.py, bind.py\'s opposite number) and the first '
    '--land of this lane ate its 14 `flagged_as` sentences (`flagged_as` appears 0 times in the '
    'generator). The STOP condition fired: both outputs were restored byte-for-byte to HEAD '
    '(sha-proved; git checkout was unavailable — another lane held .git/index.lock, which was left '
    'alone), the merge was widened, rehearsed against a throwaway symlink corpus with the live tree '
    're-hashed untouched, and only then landed for keeps — the live output is byte-identical to the '
    'rehearsal. Nothing is lost in either file now (parsed loss test empty); the icon file\'s '
    'residual diff is ADDITIONS of Dave\'s own words (13 $his_note, 10 $his_flags) plus prose the '
    'current generator composes differently, including `his_answer` on icon:jade-lifestyle — '
    'declared, his to rule if he wants a rule about who owns a field both a human and a generator '
    'write.  ⬛ CHECKS: showroom --check, polarity, mention-map, doc-rows and _validate_kg all '
    'GREEN before and after. `_gen_chain.py --check` was ALREADY RED at lane open (not this lane; '
    'the commit lane must run the generator and stage it). `_compose_slice.py --selftest` fails the '
    'IDENTICAL 6 of 79 bites before and after — proved by swapping the pre-land files back in and '
    'restoring by sha; they are #281/#282 residue.  ⚠ OWED, NOT BUILT: notes/_KG-EXPLORER.html '
    'carries 0 occurrences of `sizes` — the builder copies every unowned node field and INSPECT '
    'renders the full record, so the field appears when the explorer is next rebuilt (no --check '
    'exists on that builder, so nothing is red meanwhile). W-285lm is CLOSED by this work, its '
    '`closes_when` unchanged.')

doc = _state.load()
ok0, fails0, notes0 = _state.check(doc)
print(f"PRE  check ok={ok0} fails={len(fails0)}")
for f in fails0:
    print("  pre-existing ⛔", f)

# ⚠ `W-286r` WAS ALREADY TAKEN — it is lane R's row (home: lane R's report, closes_when: "Dave has
# ruled the SHAPE of the master registration"). Re-pointing its `home` would orphan lane R's own
# document under the doc-row gate, which counts a doc rowed ONLY by a `home` field. So this lane's
# report takes `W-286rb` (the store's id regex is ^W-[0-9]{1,3}[a-z]{0,2}$, so "W-286r2"
# is REFUSED by the gate — measured, not guessed), and lane R's row is AMENDED (body + links) to say its
# condition is now met. Its STATE is left alone: it is not this lane's row and a commit lane may be
# quoting it as it stands.
lane_r = next((i for i in doc["items"] if i["id"] == "W-286r"), None)
if lane_r is not None:
    note = (" ⬛ #286 lane R2 UPDATE: the shape IS now ruled and the registration IS done. Dave, "
            "2026-09-18, verbatim: \"okay size-on-the-existing-node\" — a master is a SIZE FIELD "
            "on its lockup's existing node, which is lane R's shape 1 and refuses its shapes 2 and "
            "3. gen_kg_icons.py was taught assets/logos/masters/ and landed once: 40 masters "
            "attached as `sizes` on the 8 existing nodes, nodes 8 -> 8, edges 33 -> 33 multiset "
            "identical, the 12 hand-authored governedBy edges byte-identical after the run. "
            "Receipt: " + REPORT + " (row W-286rb). ⇒ THIS ROW'S `closes_when` READS AS MET; its "
            "state is left to the conductor, not moved by lane R2.")
    if "lane R2 UPDATE" not in lane_r.get("body", ""):
        lane_r["body"] = lane_r.get("body", "") + note
    for q in (REPORT, "notes/_lanes/286/R2/"):
        if q not in lane_r.setdefault("links", []):
            lane_r["links"].append(q)
    print("AMENDED W-286r body +%d chars, links now %d" % (len(note), len(lane_r["links"])))

if any(i["id"] == "W-286rb" for i in doc["items"]):
    sys.exit("W-286rb already exists — not adding a second one.")

it = _state.add(
    doc,
    id="W-286rb",
    title="#286 lane R2 — the 40 logo masters registered as `sizes` on the 8 existing nodes, and --land taught to merge instead of clobber",
    state="open",
    owner="dave",
    opened=286,
    project="apollo",
    closes_when=("Dave has read the report and either accepted `sizes` as the field name and the "
                 "generator-wins-on-fields-it-writes default, or named a different field name or "
                 "a different rule for a field both a human and the generator write"),
    home=REPORT,
    links=[REPORT,
           "notes/_lanes/286/DAVE-RULINGS-2026-09-18.md",
           "notes/_subreports/2026-09-18-286-R-masters-registered.md",
           "notes/_lanes/277/icons-propose/gen_kg_icons.py",
           "knowledge/_logo_nodes.json",
           "knowledge/assets/logos/masters/"],
    body=BODY,
)
print("ADDED (in memory):", json.dumps({k: v for k, v in it.items() if k != "body"},
                                       ensure_ascii=False, indent=1))
ok1, fails1, notes1 = _state.check(doc)
print(f"POST check ok={ok1} fails={len(fails1)}")
mine = [f for f in fails1 if f.startswith("W-286r")]  # covers W-286r and W-286rb
for f in mine:
    print("  MINE ⛔", f)
if mine:
    sys.exit("REFUSED by the gate — not saving.")

if "--write" in sys.argv:
    _state.save(doc)
    print("SAVED")
    fresh = next(i for i in _state.load()["items"] if i["id"] == "W-286rb")
    print("AFTER state:", fresh["state"], "| home:", fresh["home"])
    print("counts:", json.dumps(_state.counts(_state.load())))
else:
    print("DRY RUN — nothing written")
