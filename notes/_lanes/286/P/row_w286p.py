#!/usr/bin/env python3
"""#286 lane P — row `W-286p` THROUGH THE STORE'S OWN WRITER.

Same shape as `notes/_lanes/286/S/close_w285sc.py`: `knowledge/_state.py` has no `--add` CLI
(its `__main__` is a REPORTER), so the sanctioned write is the module API — `load()` /
`add()` / `check()` / `save()`. `_state.json` is never hand-edited. `add()` runs the blocking
gate itself and raises `StateError` if this row fails it, so a bad row never reaches `save()`.

DRY RUN by default; pass `--write` to save.
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

if any(i["id"] == "W-286p" for i in doc["items"]):
    sys.exit("W-286p already present — not re-adding.")

before_order = [i["id"] for i in doc["items"]]

row = _state.add(
    doc,
    id="W-286p",
    title="#286 lane P — the push REFUSED: one untracked leftover is a dirty tree",
    state="open",
    owner="dave",
    opened=286,
    project="apollo",
    home="notes/_subreports/2026-09-18-286-P-push.md",
    links=[
        "knowledge/_git_commit.sh",
        "notes/_subreports/2026-09-18-285-P-push.md",
        "notes/_subreports/2026-09-18-286-C-commit.md",
    ],
    closes_when=(
        "notes/_lanes/286/C/MSG-286-commit-2.txt.t3-rendered has been landed, removed or "
        "reconciled by a lane entitled to touch it, `bash knowledge/_git_commit.sh --push` has "
        "printed the literal `✅ pushed and VERIFIED: remote master == local db0830f7…` line, and "
        "CI has been read back for db0830f7 so its colour is known rather than inherited"
    ),
    body=(
        "ANSWERED the conductor's question: YES, the clean-tree gate counts an untracked file. "
        "_git_commit.sh:174 takes `git status --short -- . ':(exclude)notes/_REHEARSAL-LOG.jsonl'` "
        "and tests it non-empty — no status-code filter, no -uno — so a `??` path refuses the push "
        "exactly as an ` M` path does; the s137-D1 exclusion is one named file and nothing else. "
        "Verbatim refusal, exit 1: `✗ push refused: tree not clean — commit first (s133-D2; "
        "rehearsal log excluded per s137-D1). Dirty paths: ?? "
        "notes/_lanes/286/C/MSG-286-commit-2.txt.t3-rendered`. No `✅ pushed and VERIFIED` line, so "
        "per #227 no push. Refusal fires at the FIRST gate: branch check passed, credential gate / "
        "push / after-verify never reached, no token requested or entered. Local HEAD db0830f7 "
        "[ahead 2]; ls-remote still 09ddf155. CI read three times at ~90s (16:42/16:44/16:45Z), "
        "identical four rows each time, all `gates`, all completed failure, none in progress: "
        "09ddf155, d2ae9c73, 77b491b8, 9a97e006. NO run for db0830f7 and there cannot be one — it "
        "is not on the remote. INHERITED: 09ddf155 and its parent d2ae9c73 fail the same two steps "
        "in the same `gates` job — `Survey the COMMITTED tree` and `Knowledge build — all derived "
        "views + blocking gates` — while `render` and `release` pass in both, so the red predates "
        "09ddf155. db0830f7's own colour is UNKNOWN until pushed and was not extrapolated. Lane "
        "committed nothing and did not touch the leftover."
    ),
)

print("ADDED (in memory):", json.dumps(row, ensure_ascii=False, indent=2))

ok1, fails1, notes1 = _state.check(doc)
print(f"POST check ok={ok1} fails={len(fails1)}")
mine = [f for f in fails1 if f.startswith("W-286p")]
for f in mine:
    print("  MINE ⛔", f)
if mine:
    sys.exit("REFUSED by the gate — not saving.")

after_order = sorted(doc["items"], key=_state._sort_key)
print("save() would reorder items:", [i["id"] for i in after_order] != before_order + ["W-286p"])

if "--write" in sys.argv:
    _state.save(doc)
    print("SAVED")
else:
    print("DRY RUN — nothing written")
