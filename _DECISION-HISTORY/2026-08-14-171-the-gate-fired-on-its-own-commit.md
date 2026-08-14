# #171 — the new gate fired on its own commit (2026-08-14)

provenance: local_d64be1e5-ca7e-4a3b-a3c7-3388292f1242 · 2026-08-14
status: observed

*Session #171, FABLE conductor + one OPUS build sub, conductor wrap. Spine entry: `_LIVE-STATE.md` ⏱ LATEST delta #171. Ledger: `knowledge/_rulings.json` § `s171-D1`. Both-way link: this dossier is named from both.*

## The arc

The session opened as the #171 opener digest owed by #170's post-wrap addendum: two findings (the `_gen_titles.py` parser defect that shipped #169's degenerate rename, and the `_git_commit.sh` subject-assert that compared a value to itself) plus the boot-drift refresh already put to Dave in the gauge log. Dave ruled all three in one breath — verbatim **"lets just fix everything"** — after an itemised read-back that named the band refresh as a ruling being taken. No objection; recorded as ratification, not laundered silently.

## Finding 1 — the parser defect was corpus-wide, not an incident

The build sub reconstructed every `★ LATEST` banner ever committed (200 distinct, #48→#170) and drove the old parser over all of them: **9 degenerate emissions**, spanning the #163–#169 idiom era — not one bad banner but an idiom shift the parser never followed. The mechanism was two-stage: the divider split landed on a ` — ` *inside* a bold clause, and the bold-pairing regex then paired that clause's closing `**` with the next clause's opening `**`, so the extracted "headline" was the decoration between clauses. The fix walks to the first ` — ` **not inside a bold span** and refuses, named, if none exists. Post-fix: 0 degenerates over the corpus, and #170 derives exactly its dossier title. A dead-end worth recording: the first regression fixture was too trimmed and **passed on the mutant** — a green that couldn't fail — caught and rewritten before landing. Declared residual: 23 of 120 parseable renames exceed the 120-tape cap and refuse loudly at wrap (pre-existing rule, untouched).

## Finding 2 — the assert was structurally unable to fail, and it was proven before it was replaced

Driven on the real script in a scratch clone: a visibly doubled subject **shipped with the assert green, rc=0**, because T3 writes the generated subject into the msgfile's line 1 seconds before the assert reads that same line back. The honest fix moves the comparison to `git log -1 --format=%s` against the **generated headline held in a shell variable** — the msgfile, which T3 rewrites, is demoted to a labelled diagnostic. The new assert was driven to a named refusal on the same corruption the old one waved through; old and new run side by side on identical input (rc=0 vs rc=1) so the **delta** is what's asserted. Honest residual: the `--wrap` leg is verified by construction only — a scratch clone refuses at the wrap gate — so this session's own wrap commit is its first live wrap drive.

## Finding 3 — the #170 gate was proven in anger, by accident, on this session's own commit

The fix commit's first invocation was refused (no `SESSION_N`) — and that refused run had **already written the T3 prefix into the msgfile**: the write-back class, live, in the very session that narrowed it. The reinvocation with the same file hit the #170 reused-msgfile gate's named refusal instead of shipping a doubled subject. A fresh msgfile committed clean (`6d5db13`), with the new memory-held assert passing its first live drive. The fence was crossed by accident and it held — #170's "unproven in anger" carry is consumed.

## The ruling — s171-D1

Boot band re-based on the drifted post-#164 series: `BOOT_FIRSTTURN_TK` 54,859 → **56,158**, err 1,178 → **849** (n=7 mean incl. #171's measured 56,746; the s129-D1 half-range method re-measured, not re-argued). Stop line and budgets untouched — a costlier boot moves the room, never the line. The s129-D1 block stays as history; the stale prose pointer in `_capture_gate.py` was updated in the same pass.

## What went wrong, and what caught it

The first `s171-D1` insertion into `_rulings.json` landed **inside `s158-D4`'s `open:` array** — valid JSON (the whole-file parse passed), wrong home. The read-back caught it: entry count 148 with the entry present is a contradiction. Reverted via git (after clearing a stale `index.lock` with the delete grant), re-inserted at the true tail with a **prior-entries-compared-equal** assert. The lesson: a validity check is not a location check — splice-point assertions are part of any textual JSON insertion.

## Resolved state / open

Fixed and pushed at `6d5db13`; wrap commit follows. Open: the wrap-leg assert (by construction only — read the subject back at every wrap until one fails honestly) · the 120-tape refusals (declared) · everything on the #171 banner's carried residual, ages +1.
