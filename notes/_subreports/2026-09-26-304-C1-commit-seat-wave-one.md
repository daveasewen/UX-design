# #304 C1 — the commit seat, wave one: Runs 1, 2 and 5 and the day's pages in one commit

provenance: 304 · 2026-09-26 (Saturday evening) · Opus 5.5 commit seat, delegated by the #304 conductor · mount HEAD `571d458c` at start
status: INTERIM — this copy is the one that rides the wave-one commit itself; the commit sha, push range and CI read-back are appended in the final version, which rides the NEXT commit.

## DONE BEFORE THE COMMIT

1. The verifier's fix: the twelve `RATIFY_IDS` rulings restored to `ruled` through `_inscribe_ruling.py --set-status … ruled --write` (each reconstruction proof PASSED). `ratification_status()` reads all twelve cuts RATIFIED; store count 638; `_gate_release_audit.py --check` PASS, `--selftest` 10 bites 0 fail; `s282_pointers.py .` ALREADY POINTED ×4. Log: `notes/_lanes/304/C1/step1-restore12.log`, `step1-verify.log`.
2. `notes/_lanes/304/R2/cite_lines.json` (90.8 MB) kept out by a commented `.gitignore` line; nothing else in the wave is over 5 MB.
3. Doc rows minted for the thirteen #304 reports (script `notes/_lanes/304/C1/mint_304.py`).
