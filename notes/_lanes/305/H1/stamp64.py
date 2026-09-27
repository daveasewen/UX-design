#!/usr/bin/env python3
"""#305 H1 — call 38 kind 6: stamp ONLY the rulings whose receipt was found at HEAD (file + the content that builds it,
re-checked here by content, and the commit that brought it in, by `git log -S` / blame, resolved by `git cat-file`).
The rest of the 64 stay as they are and are listed in the H1 report.  python3 stamp64.py --dry-run | --write"""
import json, subprocess, sys
WRITE = '--write' in sys.argv
R = {r['id']: r for r in json.load(open('knowledge/_rulings.json'))['rulings']}
K = {c['key']: c['ids'] for c in json.load(open('notes/_lanes/304/R6b/counts.json'))['stamps']['classes']}
T = 'knowledge/snippets/Template-dashboard-bento.reference.html'
S = [  # id, sha, file, content that must be in the file at HEAD, what the line does
 ('s184-D3', '02bfbac3', 'knowledge/canon/canon.css', '--status-positive: var(--rag-success-graphic);', 'the chart-facing alias layer --status-positive/negative/monitor/neutral over the rag-* spine'),
 ('s212-D3', 'f104cba0', 'knowledge/_FIXED-FLEX-CHARTER.md', '## 4b. Register temperature — wit licence per band (RATIFIED 2026-08-21, `s212-D3`', 'charter §4b moved PROVISIONAL -> RATIFIED'),
 ('s212-D6', 'd67d55ed', 'notes/_receipts/2026-08-21-213-sectionC-offload.md', 'offload', 'GM §C bodies offloaded into store rows (the #213 offload receipt)'),
 ('s212-D9', 'f104cba0', 'knowledge/_proforma/Masthead-interactive.html', '<symbol id="i-menu-search"', 'the Figma menu-search glyph as library asset knowledge/assets/icons/menu-search.svg and its Masthead-interactive symbol'),
 ('s217-D1', '540f2cd8', '.gitignore', 'knowledge/assets/photography/', 'originals fenced NON-REPO; knowledge/_PHOTOGRAPHY-MANIFEST.json committed'),
 ('s217-D5', '540f2cd8', 'knowledge/_render/gen_bento_matrix_217.py', 'Display renders as `data-bento-role=', 'the bento option matrix over DISPLAY / GALLERY / DASHBOARD'),
 ('s229-D2', 'baf5458e', 'knowledge/snippets/View-options.reference.html', 'AUTO-PARTIAL seg-concentric START', 'the four radius-less .seg snippets (View-options, Template-dashboard, Template-list-index, Template-report) carry the segmented radius, fixed at source through the injected seg-concentric partial'),
 ('s230-D2', '9c329a17', 'knowledge/snippets/Navigations.reference.html', 'masterbrand-light-colour.svg', 'the masthead logo defaults bound (masterbrand-light-colour / -dark-colour), text wordmarks removed (0 left in Navigations)'),
 ('s231-D2', 'e7cf3db7', T, 'c-bento', 'the bento snippet exists; e7cf3db7 is the commit that added the file'),
 ('s237-D1', '7104fc96', 'knowledge/_validate_polarities.py', 'GRADE_NAMES = {"A": "REPLICATED", "B": "STUDIED", "C": "PRACTISED", "D": "DEBUNKED", "L": "OBLIGATION"}', 'the five grade names, derived; every row of knowledge/brain/principles.json carries `grade`'),
 ('s238-D1', '7104fc96', 'knowledge/_validate_polarities.py', 'knowledge/brain/polarities.json   the 30 polarity nodes — N typed parties', 'polarities as hyper-relational nodes in the knowledge/brain/ home'),
 ('s238-D3', '7104fc96', 'knowledge/_validate_polarities.py', 'STATUS_RULES = {', 'the derived status rules (defaults derived, not asked)'),
 ('s238-D4', '7104fc96', 'knowledge/_validate_polarities.py', 'a pull between two true things (s238-D4)', 'the vocabulary is POLARITY throughout the gate'),
 ('s238-D5', '7104fc96', 'knowledge/brain/_generated/defaults-declaration.txt', 'DEFAULT+DECLARE', 'the generated defaults declaration'),
 ('s238-D6', '7104fc96', 'knowledge/_validate_polarities.py', 'return "R2-UNTYPED"', 'the generator refuses an untyped ruling link (R2-UNTYPED)'),
 ('s245-D1', '7104fc96', 'knowledge/_validate_receipt.py', 'FAIL:BEHAVIOUR-ADDRESS-FOREIGN', 'the path+fragment address with the foreign refusal (the line came in before the ruling, which took the recommendation as built)'),
 ('s245-D2', '5ae4d32c', 'knowledge/_validate_receipt.py', 'component-types.json $behaviour (s245-D2: one', '`partial` accepts one name, a list, or null'),
 ('s245-D3', '5ae4d32c', 'knowledge/_validate_receipt.py', 'FAIL:BEHAVIOUR-PROSE (s245-D3', 'a prose `behaviour` value is a named BLOCK'),
 ('s245-D6', '5ae4d32c', 'knowledge/canon/canon.css', '.c-bento.tpl-group-evidence{--bento-row-unit:240px;}', 'the role classes tpl-group-lead / -evidence / -context'),
 ('s246-D5', 'fc1209bf', T, 'the edit-pass option, not the default (s246-D5)', 'the KPI row is the template default; the 2x2 board is the edit-pass option'),
 ('s247-D3', 'fc1209bf', T, 'for the header strip, because Dave ruled', 'the two status tiles left the KPI row for the header strip'),
 ('s247-D4', 'fc1209bf', T, 'the row STAYS A ROW (s247-D4, "row for sure")', 'headline metrics are a row, pinned by page rule 10a'),
 ('s248-D3', '0979a9b7', T, 'FIT — responsive reflow on BOTH axes', 'the template components reflow on both axes'),
 ('s249-D2', 'fc1209bf', T, 'inside s249-D2 ("whatever the', 'the headline row holds the count the data dictates'),
 ('s249-D4', '0979a9b7', 'knowledge/canon/dv-behaviour.js', 's249-D4 carried the tile-height axis in', 'DP-18 (a): the library engine in dv-behaviour, one engine'),
 ('s249-D5', 'fc1209bf', T, 'what keeps s249-D5 (no ragged layouts) true here', 'no ragged layouts'),
 ('s250-D1', '0b0e6c62', 'knowledge/_validate_behaviour.py', 'CODE-ONLY bytes', 'the byte gate measures code-only bytes'),
 ('s251-D3', '33619267', 'knowledge/components/meta.schema.json', 's251-D3…D8 (the DESK eight) — the DATA-SHAPE axis', 'the DESK structures as the schema\'s data-shape axis'),
 ('s251-D5', '33619267', 'knowledge/components/meta.schema.json', 's251-D5 (Dave, #251, DESK RSQ 3', 'the `when` predicate over shape, prominence and span'),
 ('s251-D9', '866312bd', 'knowledge/components/kpi-tile.meta.json', '"provides"', 'the option space as tags in the component metas (24 metas carry provides/answers/shape/span/priority/when)'),
 ('s251-D10', '33619267', 'knowledge/components/meta.schema.json', 's251-D10 (Dave, #251, META RSQ 2 option (a))', 'one span vocabulary, 12 columns canonical'),
 ('s251-D11', '33619267', 'knowledge/components/meta.schema.json', '"priority": {', '`priority` (integer) orders providers; no new weight model'),
 ('s251-D12', '866312bd', 'knowledge/_roles_drift.py', 'The first authoring pass covered 25 metas (s251-D12)', 'the first authoring pass (the template\'s 11 $composes + 13 charts)'),
 ('s253-D2', 'dbf2780f', 'knowledge/_gm_usage.py', 'THE FIX IS THE READER, NEVER THE GATE (s253-D2', 'the scratch-script red fixed in the reader, not the gate'),
 ('s263-D4', '8a07c0ef', 'knowledge/snippets/Filter-toolbar-bar.reference.html', 'data-apollo-filter-bar data-apollo-filter-target=', 'the data-apollo-filter-* marker contract on the driver'),
 ('s269-D10', '445af025', 'knowledge/_parked.py', 'PARKED WITH A TRIPWIRE', 'knowledge/_parked.json + knowledge/_parked.py, the park-with-a-tripwire register'),
]
assert len({s[0] for s in S}) == len(S) and all(s[0] in K['intree'] for s in S)
D38 = "#305 `s305-D38` (Dave, sitting call 38, 14:29 BST, verbatim \"yes to all six\")"
log = []
for i, sha, f, frag, what in S:
    body = subprocess.run(['git', '--no-optional-locks', 'show', 'HEAD:' + f], capture_output=True, text=True).stdout   # AT HEAD, not the working tree (B1/B2 edit some of these files)
    assert frag in body, (i, f, frag)
    ln = body[:body.index(frag)].count('\n') + 1
    assert subprocess.run(['git', '--no-optional-locks', 'cat-file', '-e', sha + '^{commit}']).returncode == 0, sha
    subj = subprocess.run(['git', '--no-optional-locks', 'log', '-1', '--format=%s', sha], capture_output=True, text=True).stdout.strip()[:90]
    st = (f"enacted — PROBED AT HEAD by #305 lane H1 under {D38}, kind 6 'stamped by a probe on a file-and-line receipt': "
          f"`{f}:{ln}` — {what}; the line came in at {sha} (\"{subj}\") · was: {R[i]['status']}")
    if R[i]['status'].startswith('enacted — PROBED AT HEAD'): log.append((i, 'already')); continue
    p = subprocess.run(['python3', 'knowledge/_inscribe_ruling.py', '--set-status', i, st, '--evidence-sha', sha,
                        '--write' if WRITE else '--dry-run'], capture_output=True, text=True)
    log.append((i, p.returncode, f"{f}:{ln}", sha)); print(i, p.returncode, f"{f}:{ln}", sha, (p.stderr or '')[:120])
left = [i for i in K['intree'] if i not in {s[0] for s in S}]
json.dump({'stamped': log, 'left': left}, open(f"notes/_lanes/305/H1/stamp64.{'write' if WRITE else 'dry'}.json", 'w'), indent=1)
print('stamped', len(S), 'left', len(left), left); print('rc!=0', [x for x in log if x[1] not in (0, 'already')])
