# Dave's words — #311 after the wrap, Thu 2026-10-01 (chat, verbatim)

12:32 BST, quoting the conductor's line "Warnings from the push: _CHAIN.md is over its size warning. GitHub flagged _memento-index.json at 50.6 MB, which is close to the point where GitHub starts refusing files.": "okay what do we do about this"

The conductor's recommendation (not his words): (1) stop committing `_memento-index.json` — build it fresh at the opener and in CI, and change the determinism check to compare two fresh builds; fallback, shrink it (pointers not copies, no indent); avoid Git LFS. (2) move the eleven older "wrap date split" lines out of the GOOD-MORNING header into the archive, leaving one line that counts them and points there (s294-D11 already rules the shape).

12:35 BST: "yes to both, I want our plan to run smoothly"
