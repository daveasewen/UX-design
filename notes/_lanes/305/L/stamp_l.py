# #305 lane L - stamp s305-D62 and s305-D63 enacted at commit 1. Dry run, then --write (argv[1] == 'write').
import subprocess, sys
W = '5058d963'
S = [
 ('s305-D62', W, "enacted #305 2026-09-28 - lane L: _gauge_tokens.py BUDGET_WORKING 320,000 (includes the wrap; was 256,000), BUDGET_HARD 350,000 (was 300,000), STOP_LINE_TK 300,000 (was 236,000), TOLERATED_TK 320,000, the bright-amber line (was 276,000); BUDGET_AMBER 160,000 and BOOT_CEILING_TK 130,000 unmoved. _capture_gate.py pins (160,000/320,000/350,000) and (300,000/320,000), each driven to a named refusal with the old value; pre-flight fixtures re-priced against 320,000; _WALL learns 320,000; _checkin.py and _seam.py cite D62; the context-gauge runbook's band list struck and the D62 bands added. knowledge/_standing.md:19 left as Dave's ratified text"),
 ('s305-D63', W, "enacted #305 2026-09-28 - lane L: step 5c added to knowledge/_RUNBOOK-capture-ritual.md by addition (three headings, decisions, outputs, problems; about 20 bullets at most), the #250 prose-narrative practice struck through beside it; #305's summary written in the new form at notes/_lanes/305/W/SUMMARY-BULLETS.md (19 bullets)"),
]
mode = '--write' if sys.argv[1:] == ['write'] else '--dry-run'
bad = 0
for rid, sha, st in S:
    p = subprocess.run(['python3', 'knowledge/_inscribe_ruling.py', '--set-status', rid, st, '--evidence-sha', sha, mode], capture_output=True, text=True)
    print(rid, sha, mode, 'rc', p.returncode)
    for l in (p.stdout + p.stderr).strip().splitlines()[-4:]: print('   ', l[:300])
    bad += p.returncode != 0
print('failures', bad)
