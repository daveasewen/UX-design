# #305 C4 - stamp s305-D60 enacted at the day-two sha. Dry run, then --write (argv[1] == 'write'). s305-D58 and D59 stay ruled (D58 builds with the PoC; D59's fill question is on W-305n2).
import subprocess, sys
W = 'f6aeb264'
S = [
 ('s305-D60', W, "enacted #305 2026-09-28 - B6: the four draft-only rows built, worded exactly as R4a drafted them (gate plus prose): button's gate gains AND actions <= 1; filter-toolbar-bar, footer and template-dashboard-bento gain their when; layout.grammar joins knowledge/when-fields.json by addition (s273-D4). The other eleven accepted rows (breadcrumbs, chart-bar, headers, kpi-tile, layout-utilities, legend, navigations, stat-card, status-indicator, summary, view-options) were already in the tree byte for byte. list-items and app-shell-top-nav untouched (his Change on both; W-305e1, W-305e2). Chooser output byte-identical before and after (R5's 20: 19/20, B2's 6: 6/6)"),
]
mode = '--write' if sys.argv[1:] == ['write'] else '--dry-run'
bad = 0
for rid, sha, st in S:
    p = subprocess.run(['python3','knowledge/_inscribe_ruling.py','--set-status',rid,st,'--evidence-sha',sha,mode],capture_output=True,text=True)
    out = (p.stdout + p.stderr).strip().splitlines()
    print(rid, sha, mode, 'rc', p.returncode)
    for l in out[-6:]: print('   ', l[:300])
    bad += p.returncode != 0
print('failures', bad)
