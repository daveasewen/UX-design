# #305 C3 - stamp s305-D24, D54, D55 enacted at the wave-three sha. Dry-run all, then --write (argv[1] == 'write'). s305-D10 stays ruled (W2 held the rails half).
import subprocess, sys
W = 'e4ff4284'
S = [
 ('s305-D24', W, "enacted #305 2026-09-27 - W2: rule webf-036 (\"A part keeps its own size on any page. The page arranges parts; it never shrinks them.\") in web-foundations.md, rule:webf-036 enforcedBy knowledge/_validate_own_size.py and definedIn web-foundations.md added by addition to _rule_nodes.json (the 75 restsOn edges intact), the rules index, instrument fit, the title and the explorer regenerated; appliesTo to every component not built (not asked)"),
 ('s305-D54', W, "enacted #305 2026-09-27 - W2: _validate_a11y.py's 2.3.3 clause reads per part by the receipt's splice markers (a page without markers keeps the historical whole-page line); driven red on a composed page missing one part's block, green on the control; 0 verdict changes over 282 files. Built ahead of the Apollo-MCP group on the conductor's brief; the R5 port under notes/_lanes/304/R5/ keeps the old clause"),
 ('s305-D55', W, "enacted #305 2026-09-27 - W2: notes/_jev-link-check/jev_link_check.py, hand-run, never a gate, four edge types; stops by name without a key (exit 3); first run 330 of 330 asked, 13 look wrong for Dave in notes/_jev-link-check/2026-09-27-link-check.md, nothing in the graph changed"),
]
mode = '--write' if sys.argv[1:] == ['write'] else '--dry-run'
bad = 0
for rid, sha, st in S:
    p = subprocess.run(['python3','knowledge/_inscribe_ruling.py','--set-status',rid,st,'--evidence-sha',sha,mode],capture_output=True,text=True)
    tail = (p.stdout + p.stderr).strip().splitlines()[-1:] or ['']
    print(rid, sha, mode, 'rc', p.returncode, '::', tail[0][:220])
    bad += p.returncode != 0
print('failures', bad)
