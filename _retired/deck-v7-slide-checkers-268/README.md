provenance: 305 · 2026-09-27 · lane H2 (code housekeeping)

# The seven deck-v7 slide checkers — retired, not deleted

These seven drivers checked the #268 demo deck's slides (deck v3 to v7.5) between 11 and 13 September 2026.
They lived in `knowledge/_render/`. Nothing in the repo calls them (`git grep` finds no caller outside the seven
files), they were never `_build_all.py` steps, and #304 Run 1 had only guarded them for the help gate.

Retired by Dave at the sitting of Sunday 27 September 2026, call 41, verbatim: "declare, port now, retire" —
ruling `s305-D41` ("they move to an archive folder, nothing deleted"). Moved here by `mv`, byte-unchanged.

- `verify_demo_slides_268.py` · `_v3` · `_v5` · `_v6` · `_v7` · `_v74_gearbox` · `_v75_gearbox`

They find their helpers by walking up to `knowledge/_helpgate.py`, which they cannot reach from here — to run one
again, move it back to `knowledge/_render/`. The help gate skips `_retired/` by name, so they no longer count in its scan.
