# #305 C2 - stamp the s305 rulings whose calls are fully discharged. Dry-run all, then --write (argv[1] == 'write').
import subprocess, sys
W = '1e107eea'
S = [
 ('s305-D2', '02d679b3', "enacted #305 2026-09-27 - the cut is built and committed: X 0ef30746 (sweep, key, stamp fix), Y1 02d679b3 (manifest RATIFIED, the v1.0.14 zip), Y2 d3b809a7 (frozen ledger re-seeded); the push and CI read-back are still owed, and cold verifier V2 reads DO NOT SHIP to the audience (the shipped store carries the PoC rulings, s279-D1 against W-305n6, Dave's)"),
 ('s305-D30', '27efb7b6', "enacted #305 2026-09-27 - done at the seat by wave one's commit seat C1: the token left remote.origin.url for a repo-local get-only credential helper inside .git/ (never committed, so no commit carries it; 27efb7b6 is that seat's wave); the push of 568e2534 went through the helper, and _git_commit.sh --push learned the helper in 1e107eea"),
 ('s305-D28', W, "enacted #305 2026-09-27 - H2: STOP_LINE_TK 236,000 and TOLERATED_TK 276,000 in _gauge_tokens.py, pinned in _capture_gate.py; 256,000 and 300,000 tagged at their constants"),
 ('s305-D29', W, "enacted #305 2026-09-27 - H2: BOOT_CEILING_TK 130,000 with the Mac-seat condition written above it; the re-measure and shrink at the Mac seat is the ruling's own later step"),
 ('s305-D40', W, "enacted #305 2026-09-27 - H2: the regrowth arm arms itself when the 75 pinned rows are closed or parked (REGROWTH_ARMING_IDS); document rows born closed from #306 (DOC_BIRTH_FROM_SESSION), because #305's own report rows were minted live before the line existed"),
 ('s305-D41', W, "enacted #305 2026-09-27 - H2: four forks declared in _TOKEN-FORK-LEDGER.json, _gen_chain.py ported into both package copies, the seven deck-v7 checkers moved to _retired/deck-v7-slide-checkers-268/"),
 ('s305-D31', W, "enacted #305 2026-09-27 - H1: 95 of 95 closed, every file kept"),
 ('s305-D34', W, "enacted #305 2026-09-27 - H1: 17 of 17 closed, each with its receipt quoted"),
 ('s305-D35', W, "enacted #305 2026-09-27 - H1: 14 of 14 dispositioned per the page's table; W-305h1..h4 split out"),
 ('s305-D37', W, "enacted #305 2026-09-27 - H1: 12 component-wave rows parked (7 here, 5 under s305-D32 with both tripwires); of the 20 pages 19 parked and W-298 closed under s305-D31"),
 ('s305-D39', W, "enacted #305 2026-09-27 - H1: s135-D3 superseded; s114-D2 parked as P-305-2 and s246-D3 as P-305-1; P-272-1 and P-277-4 read enacted"),
]
mode = '--write' if sys.argv[1:] == ['write'] else '--dry-run'
bad = 0
for rid, sha, st in S:
    p = subprocess.run(['python3','knowledge/_inscribe_ruling.py','--set-status',rid,st,'--evidence-sha',sha,mode],capture_output=True,text=True)
    tail = (p.stdout + p.stderr).strip().splitlines()[-1:] or ['']
    print(rid, sha, mode, 'rc', p.returncode, '::', tail[0][:200])
    bad += p.returncode != 0
print('failures', bad)
