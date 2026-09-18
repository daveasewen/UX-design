#!/usr/bin/env python3
"""#286 lane C2 — row `W-286cs` THROUGH THE STORE'S OWN WRITER.

Same shape as notes/_lanes/286/P/row_w286p.py: `_state.py` has no `--add` CLI, so the
sanctioned write is the module API — load() / add() / check() / save(). `_state.json` is
never hand-edited. DRY RUN by default; pass --write to save.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state  # noqa: E402

doc = _state.load()
ok0, fails0, notes0 = _state.check(doc)
print(f"PRE  check ok={ok0} fails={len(fails0)} notes={len(notes0)}")
for f in fails0:
    print("  pre-existing ⛔", f)

if any(i["id"] == "W-286cs" for i in doc["items"]):
    sys.exit("W-286cs already present — not re-adding.")

before_order = [i["id"] for i in doc["items"]]

row = _state.add(
    doc,
    id="W-286cs",
    title="#286 lane C2 — lane R2 re-verified independently, committed, and pushed",
    state="open",
    owner="claude",
    opened=286,
    project="apollo",
    home="notes/_subreports/2026-09-18-286-C2-commit-and-push.md",
    links=[
        "notes/_subreports/2026-09-18-286-R2-masters-registered-as-sizes.md",
        "notes/_subreports/2026-09-18-286-P-push.md",
        "notes/_subreports/2026-09-18-286-C-commit.md",
        "knowledge/_git_commit.sh",
        "notes/_lanes/286/C2/verify.py",
    ],
    closes_when=(
        "Dave has read this lane's independent re-derivation of lane R2 and the CI read-back "
        "appended to it, and has said either that the `sizes` registration stands as committed "
        "or what about it is wrong"
    ),
    body=(
        "INDEPENDENT CHECK OF LANE R2, re-derived by notes/_lanes/286/C2/verify.py from "
        "`git show HEAD:knowledge/_logo_nodes.json` and the working copy, not read off R2's "
        "report: node count 8 == 8, node id sets identical, edge multiset identical at 33 == 33, "
        "12 `governedBy` edges present and BYTE-IDENTICAL to HEAD, every one of the 8 nodes "
        "carrying a `sizes` map of exactly 5 entries, and all 40 sha256 digests recomputed from "
        "the bytes on disk and matched — 40/40, steps [24, 28, 32, 36, 40]. GREEN; no STOP "
        "condition met. OBSERVED, not a defect in R2: `hexagon-dark-colour` and "
        "`hexagon-light-colour` carry identical sha256 at all five steps — the two masters are "
        "byte-identical files under different names, a property of the master corpus that the "
        "registration faithfully records. `hexagon-*-mono` and both `masterbrand` pairs do "
        "differ. Flagged for Dave's eye, nothing changed on account of it. COMMIT: through "
        "`knowledge/_git_commit.sh` with SESSION_N=286, --quiet, msgfile under "
        "notes/_lanes/286/C2/, every path named — R2's four tracked outputs, the amended rulings "
        "file, notes/_lanes/286/{R2,P,C2}/, the .t3-rendered leftover that refused lane P's push "
        "(committed as a session record per the brief), the P/R2/C2 reports, and _CHAIN.md, which "
        "_gen_chain.py --check was RED on at lane open with the same pre-existing staleness lane "
        "C and lane R2 both measured. notes/_lanes/286/C2/ had to be named too: the push gate "
        "refuses on ANY untracked path (_git_commit.sh:174, lane P's finding), so leaving this "
        "lane's own working files untracked would have reproduced the failure it was sent to "
        "clear. The four fenced generators were not run; the T3 prefix was never hand-written; "
        "`rm .git/index.lock` was never run. CARRIED, not settled: W-286r reads as MET but its "
        "state is still `open` and that close is the conductor's, not a commit lane's; the field "
        "key `sizes` is R2's reading of the file's vocabulary and not Dave's word; the explorer "
        "does not yet show the field; the boot-drift CEILING BREACH and the boot double-count "
        "lane C left standing are untouched and will BLOCK at the wrap's --wrap run."
    ),
)

print("ADDED (in memory):", json.dumps(row, ensure_ascii=False, indent=2)[:900])

ok1, fails1, notes1 = _state.check(doc)
print(f"POST check ok={ok1} fails={len(fails1)}")
mine = [f for f in fails1 if f.startswith("W-286cs")]
for f in mine:
    print("  MINE ⛔", f)
if mine:
    sys.exit("REFUSED by the gate — not saving.")
for n in notes1:
    print("  NOTE:", n)

after_order = sorted(doc["items"], key=_state._sort_key)
print("save() would reorder items:", [i["id"] for i in after_order] != before_order + ["W-286cs"])

if "--write" in sys.argv:
    _state.save(doc)
    print("SAVED")
else:
    print("DRY RUN — nothing written")
