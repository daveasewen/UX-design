"""Seat 304-R6b build: three decision pages for Tuesday 29 September. Copies the house CSS (both style blocks)
and the decisions overlay from the Apollo-MCP v2 proposal page (never redrawn), adds common.css, fills every
%%TOKEN%% from counts.json (computed by counts.py), and writes the pages into notes/. Run from the repo root."""
import os, re, json, html
ROOT = os.getcwd(); HERE = os.path.join(ROOT, 'notes/_lanes/304/R6b')
HOUSE = os.path.join(ROOT, 'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html')
C = json.load(open(os.path.join(HERE, 'counts.json')))
def rep(s, a, b):
    assert s.count(a) == 1, a[:70]
    return s.replace(a, b)
house = open(HOUSE, encoding='utf-8').read()
i = house.index('<style>'); j = house.index('</style>', i) + 8
k = house.index('<style>', j); l = house.index('</style>', k) + 8
CSS = house[i:j] + '\n' + house[k:l] + '\n' + open(os.path.join(HERE, 'common.css'), encoding='utf-8').read()
m = house.index("<!-- ===== DAVE'S DECISIONS"); n = house.index('</script>', m) + 9
OVER = house[m:n]
OLDCFG = "page:'proposal-apollo-mcp-v2', title:'Apollo-MCP, proposal v2', path:'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'"
def overlay(pid, title, path):
    o = rep(OVER, OLDCFG, "page:'%s', title:'%s', path:'%s'" % (pid, title, path))
    o = rep(o, "copied from the story proposal v2 (#289) at #304", "copied from the Apollo-MCP proposal v2 (#304 lane M) by seat R6b")
    o = rep(o, "skip:function(el){ return el.id==='tech' || el.id==='sources'; }", "skip:function(el){ return el.id==='tech'; }")
    return o
def code(ids): return ', '.join('<code>%s</code>' % html.escape(x) for x in ids)
def fill(s, T):
    for key, v in T.items(): s = s.replace('%%' + key + '%%', str(v))
    left = re.findall(r'%%[A-Za-z0-9_]+%%', s); assert not left, left
    return s
def fmt(n): return '{:,}'.format(n)
PAGES = []
# ---------- CI ----------
ci = C['ci']; fc = ci['final_counts']; bc = ci['before_counts']; bm = C['badge']['snippets']
nav7 = bm['Navigations']['7px']; nav8 = bm['Navigations']['8px']
def w(x): return ('%.1f' % x).rstrip('0').rstrip('.') + 'px'
sw = []
for f in C['forks']:
    name = {'--status-positive': 'Positive', '--status-negative': 'Negative', '--status-neutral': 'Neutral'}[f['token']]
    sw.append('<div><p class="hd">%s</p>'
              '<div class="row"><div class="blk" style="background:%s"></div><div class="v"><b>Bar fill</b> %s · %s to 1</div></div>'
              '<div class="row"><div class="ln"><i style="background:%s"></i></div><div class="v"><b>Sparkline line</b> %s · %s to 1</div></div></div>'
              % (name, f['bar'], f['bar'].upper(), f['bar_cr'], f['spark'], f['spark'].upper(), f['spark_cr']))
T = {'PASS_AFTER': fc['PASS'], 'FAIL_AFTER': fc['FAIL'], 'CNA_AFTER': fc['CNA'], 'PASS_BEFORE': bc['PASS'], 'FAIL_BEFORE': bc['FAIL'], 'CNA_BEFORE': bc['CNA'],
     'W12_7': w(nav7['width_by_count']['12']), 'W12_8': w(nav8['width_by_count']['12']), 'W128_7': w(nav7['width_by_count']['128']), 'W128_8': w(nav8['width_by_count']['128']),
     'SWATCHES': ''.join(sw), 'FAIL_LIST': ' '.join('<code>[%d]</code>' % x for x in ci['final_fail']),
     'N7_NAV': nav7['chips_at_7px_in_snippet'], 'N7_SIDE': bm['Sidebar-nav']['7px']['chips_at_7px_in_snippet'],
     'W_ROW7': ' / '.join(w(nav7['width_by_count'][t]) for t in ('3', '12', '128')), 'W_ROW8': ' / '.join(w(nav8['width_by_count'][t]) for t in ('3', '12', '128'))}
PAGES.append(('ci.src.html', 'notes/_DECIDE-304-ci-calls-2026-09-26-v1.html', 'decide-304-ci-calls-v1', 'The CI calls, decision page v1', T))
# ---------- stamps ----------
st = C['stamps']; cl = {c['key']: c for c in st['classes']}; r2 = st['r2_counts']['rulings']
T = {'N_UNC': st['total_uncertain'], 'R2_STAMPED': r2['after_R2']['stamped_by_304'], 'R2_SHA_BEFORE': r2['HEAD_571d458c']['of_which_with_sha_evidence'],
     'R2_SHA_AFTER': r2['after_R2']['of_which_with_sha_evidence'], 'N_NOID': st['not_found']['no_id_receipt'], 'N_WHEN': st['not_found']['when_harvest'],
     'N_PROBE': st['not_found']['probe_verified'], 'N_LEFTOPEN': st['closes_left_open'],
     'RG_HEAD': st['r2_counts']['regrowth_named_rows_on_HEAD_store'], 'RG_NOW': st['r2_counts']['regrowth_named_rows_after']}
for key, c in cl.items(): T['N_' + key] = c['n']; T['IDS_' + key] = code(c['ids'])
assert len(st['ruled_not_built']) == 11
PAGES.append(('stamps.src.html', 'notes/_DECIDE-304-uncertain-stamps-2026-09-26-v1.html', 'decide-304-uncertain-stamps-v1', 'The uncertain stamps, decision page v1', T))
# ---------- housekeeping ----------
a2 = C['a2']['decisions']; D = {k.split()[0]: v for k, v in a2.items()}
kc = C['carries']['by_class']
series = sum(v for k2, v in kc.items() if k2.startswith('series:') and 'boilerplate' not in k2)
boil = kc['series: boilerplate: what this wrap did not do / pitfalls']
diet = kc['struck but still carried'] + kc['deck / Friday / demo (event now past)'] + kc['fragment (splitter artefact)'] + boil + series
assert diet + kc['substantive'] == C['carries']['total']
LEGACY = [
 ('Encode before the wave: the chart-encoding gaps from late July.', 'Close when its first finding is ruled, or rule it overtaken by the chart engine of 8 and 9 September (estimate).'),
 ('A disabled-state follow-through from July.', 'Fold into the disabled-grey build row and close with it.'),
 ('The legend and behaviour size ceiling.', 'Close when the page-budget rulings are confirmed to replace it (estimate).'),
 ('The chart plot area measured from the gutter.', 'Close when the bar chart renders real HSBC labels unclipped at the narrow floor and your eye passes it.'),
 ('Floating growth on charts.', 'Fold into the stacked-surfaces row; close when the third surface carries it.'),
 ('The instrument-fit remainder.', 'Park part 2 with a tripwire, turn part 4 into one question, close the row.'),
 ('The citation question behind the citation gate.', 'Fold into the citation gate, which the stamps page recommends parking.'),
 ('A floated item that would overrule a standing instruction.', 'Rule it overtaken by the work store and strike-by-addition (estimate).'),
 ('Six sub-items still owed from late July.', 'Split any live one into its own row, close the bundle.'),
 ('How work is delegated between seats.', 'Close as answered by the team shape you adopted on 19 August.'),
 ('The per-gate test plan.', 'Close: its own text says closed, all five ratified.'),
 ('A deadlock between an index and a cap.', 'Close when the rolls are retired, or rule it overtaken now.'),
 ('A July dossier still marked owed.', 'Drop.'),
 ('Runbooks that tell a seat to write to /tmp.', 'Close when no runbook does, with a gate that proves it.'),
]
assert len(LEGACY) == D['D5']['live_now'] == 14
legacy = ''.join('<tr><td data-l="Row">%s</td><td data-l="Proposed">%s</td></tr>' % (html.escape(a), html.escape(b)) for a, b in LEGACY)
a2t = ' · '.join('%s %d → %d' % (html.escape(k), v['a2'], v['live_now']) for k, v in a2.items()) + '.'
ct = ' · '.join('%s %d' % (html.escape(k2), v) for k2, v in sorted(kc.items(), key=lambda kv: -kv[1]))
sto = C['store']
T = {'UNION_NOW': C['a2']['union_live_now'], 'UNION_A2': C['a2']['union_a2'], 'UNION_GONE': C['a2']['union_a2'] - C['a2']['union_live_now'],
     'DAVE_LIVE': sto['live_by_owner']['dave'], 'CLAUDE_LIVE': sto['live_by_owner']['claude'], 'LIVE': sto['states']['open'], 'ITEMS': sto['items'],
     'DIET': diet, 'CARRIES': C['carries']['total'], 'C_STRUCK': kc['struck but still carried'], 'C_DECK': kc['deck / Friday / demo (event now past)'],
     'C_FRAG': kc['fragment (splitter artefact)'], 'C_BOIL': boil, 'C_SERIES': series, 'C_SUB': kc['substantive'],
     'LEGACY': legacy, 'A2_TABLE': a2t, 'CARRY_TABLE': ct, 'BOOT_LINE': html.escape(C['boot_ceiling_line'].split('#')[0].strip())}
for key in ('D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'): T[key] = D[key]['live_now']
PAGES.append(('house.src.html', 'notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html', 'decide-304-housekeeping-and-lines-v1', 'Housekeeping and lines, decision page v1', T))
for src, out, pid, title, T in PAGES:
    s = open(os.path.join(HERE, src), encoding='utf-8').read()
    s = rep(s, '<!--CSS-->', CSS); s = rep(s, '<!--OVERLAY-->', overlay(pid, title, out))
    s = fill(s, T)
    open(os.path.join(ROOT, out), 'w', encoding='utf-8').write(s)
    print('wrote', out, len(s), 'bytes')
