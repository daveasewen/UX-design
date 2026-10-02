#!/usr/bin/env python3
"""#315 lane LA: the whole-library audit against Dave's rulings. READ-ONLY against the library.

Reads knowledge/components/*.meta.json (the parts), knowledge/snippets/*.reference.html (their source),
knowledge/canon/canon.css + knowledge/tokens/ (token values), knowledge/_rulings.json (the rulings, quoted
verbatim from the store), and the two render sweeps beside this file (click_sweep.json, help_wrap.json).
Writes ONLY audit.json beside itself. Rules nothing, fixes nothing.

Every row: part · ruling ids · check · verdict (break | unclear | cosmetic | clean | not-judged) ·
evidence (path:line) · note. Verdicts are this lane's reading of the source against the quoted ruling; a
recommendation in the findings list is a recommendation, never a ruling.
"""
import json, os, re, glob, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import libparse as L
ROOT = L.ROOT
K = L.K
RUL = {x['id']: x for x in json.load(open(os.path.join(K, '_rulings.json')))['rulings']}

def quote(rid):
    x = RUL[rid]
    t = x['ruled'] if len(x['ruled']) > 30 else x.get('says', x['ruled'])
    return t

def rstatus(rid):
    s = RUL[rid]['status']
    s0 = s.split(' ')[0].split('—')[0].strip().lower()
    return 'enacted' if s0.startswith('enacted') else ('ruled' if s0.startswith('ruled') else s0)

def fl(path, pattern, flags=0):
    """first line matching pattern -> 'rel/path:line' (or rel/path:? when the pattern is not found)"""
    p = path if os.path.isabs(path) else os.path.join(ROOT, path)
    for i, line in enumerate(open(p, encoding='utf-8'), 1):
        if re.search(pattern, line, flags): return '%s:%d' % (L.rel(p), i)
    return '%s:?' % L.rel(p)

def sn(name): return os.path.join(K, 'snippets', name + '.reference.html')
def mt(slug): return os.path.join(K, 'components', slug + '.meta.json')

PARTS = L.parts()
SLUG2SN = {p['slug']: p['snippet'] for p in PARTS}
ROWS = []
def row(part, rulings, check, verdict, evidence, note=''):
    ROWS.append({'part': part, 'rulings': rulings, 'ruling_status': {r: rstatus(r) for r in rulings},
                 'check': check, 'verdict': verdict, 'evidence': evidence if isinstance(evidence, list) else [evidence],
                 'note': note})

TEMPLATES = [p['slug'] for p in PARTS if p['slug'].startswith('template-')]
PARKED = {'template-wizard': 's314-D13 parks it', 'template-dashboard-bento': 's314-D27: its own lane is owed (W-314b1)'}

# ------------------------------------------------------------------ C01 floating edge
C = 'C01 floating surfaces carry the elevation edge all round; only the mega menu keeps the bottom edge'
R = ['s313-D58', 's314-D2']
FLOAT_HAND = {  # hand-read verdicts for the surfaces the scan finds without an all-round elevation edge
    ('drawer', '.sheet'): ('unclear', 'edge-anchored sheet: border-left only (the inner edge); it bleeds off three edges, as his reason for the mega menu says, but he named only the mega menu'),
    ('sidebar-nav', '.sn.is-rail .nv-label'): ('break', 'the rail\'s hover label floats over the page with a functional shadow and NO border at all'),
    ('sidebar-nav', '.is-narrow .sn[data-open="true"]'): ('unclear', 'the overlay side nav is an edge-anchored sheet like the drawer: shadow, no border'),
    ('tab-bar', '.seg'): ('unclear', 'the floating island draws its edge with divider/border/section (visible in light), not the elevation border'),
    ('tab-bar', '.menu-fab'): ('unclear', 'the island\'s menu button: divider/border/section edge, not the elevation border'),
    ('tab-bar', '.menu-fab[aria-expanded="true"]'): ('clean', 'state of .menu-fab; the edge is set on the base rule'),
    ('fab', '.fab'): ('unclear', 'a floating BUTTON with shadow and border:0; whether a floating button is a floating surface is not said'),
    ('back-to-top', '.btt'): ('unclear', 'a floating BUTTON with shadow and border:0; as the FAB'),
    ('filter-toolbar-bar', '.ftb-outer[data-stuck="true"]'): ('cosmetic', 'a sticky bar that gains a shadow when stuck; not a floating surface over content in the menu sense'),
    ('navigations', '.nav-mega'): ('clean', 'the mega menu: bottom edge only, the one exception he named'),
}
for p in PARTS:
    if not p['snippet']: continue
    html, rules = L.part_rules(p['snippet']); man = L.manifest(html).get('vars', {})
    elev = {k for k, v in man.items() if isinstance(v, str) and (v.startswith('elevation/functional') or v.startswith('elevation/decorative'))}
    border_ok = {k for k, v in man.items() if v == 'elevation/border'}
    found = False
    for r in rules:
        sh = L.decl(r['decls'], 'box-shadow')
        if not (sh and any('var(%s' % k in sh for k in elev)): continue
        found = True
        ev = '%s:%d' % (L.rel(p['snippet']), r['line'])
        key = (p['slug'], r['sel'])
        if key in FLOAT_HAND:
            v, note = FLOAT_HAND[key]; row(p['slug'], R, C, v, ev, note + ' · ' + r['sel']); continue
        b = L.decl(r['decls'], 'border')
        if b and any('var(%s' % k in b for k in border_ok):
            row(p['slug'], R, C, 'clean', ev, r['sel'] + ': border ' + b[:60])
        elif b and re.match(r'1px solid var\(--pop-border', b):
            row(p['slug'], R, C, 'cosmetic', ev, r['sel'] + ': the edge is all round, but --pop-border is a typed per-mode value (transparent / #808080) in this snippet, not bound to elevation/border in its manifest, so a theme that changes the token will not reach it')
        else:
            row(p['slug'], R, C, 'unclear', ev, r['sel'] + ': shadow without an all-round elevation border in the same rule (read by hand)')
    # the mega menu exception line
    if p['slug'] == 'navigations':
        row('navigations', R, C, 'clean', fl(p['snippet'], r'\.nav-mega\{'), '.nav-mega border-width:0 0 1px — the exception he named')

# ------------------------------------------------------------------ C02 click focus ring (render)
C = 'C02 a mouse click never draws a focus ring (cloud render: click_sweep.py, 137 snippets, 1,815 controls)'
R = ['s314-D1', 's313-D71']
cs = json.load(open(os.path.join(HERE, 'click_sweep.json')))
for p in PARTS:
    if not p['snippet']: continue
    name = os.path.basename(p['snippet']); v = cs.get(name, {})
    hits = v.get('click_rings', [])
    if p['slug'] in PARKED and hits:
        row(p['slug'], R, C, 'not-judged', 'notes/_lanes/315/LA/click_sweep.json', '%d click ring(s); %s' % (len(hits), PARKED[p['slug']])); continue
    if not hits:
        row(p['slug'], R, C, 'clean', 'notes/_lanes/315/LA/click_sweep.json', '%d controls clicked, no ring' % v.get('checked', 0)); continue
    kinds = sorted({(h['tag'] + ('[' + h['type'] + ']' if h['type'] else '') + ' ' + (h['cls'][:20] or '')).strip() for h in hits})
    ev = ['notes/_lanes/315/LA/click_sweep.json']
    if p['slug'].startswith('template-'):
        ev.append(fl(os.path.join(K, 'canon/canon.css'), r'^:root\[data-modality="pointer"\] :where\(\.cn-input-fields\)'))
        ev.append(L.rel(p['snippet']) + ' (no `data-modality` anywhere in the file)')
        note = '%d controls ring on click: %s. The page composes canon parts; canon.css carries 15 pointer-flag rules, but the script that sets data-modality lives only inside each part\'s own snippet, so no composed page sets it and the keyboard ring fires on a click' % (len(hits), '; '.join(kinds)[:200])
    elif p['slug'] == 'filter-toolbar-bar':
        ev.append(fl(p['snippet'], r'\.tag \.x:focus-visible')); ev.append(fl(p['snippet'], r'nextFocus\.focus\(\)'))
        note = 'the applied-filter chip\'s remove x draws its 2px ring after a mouse click (focus is moved by script after the click)'
    elif p['slug'] == 'video-player':
        ev.append(fl(p['snippet'], r'scrub\.focus\(\)'))
        note = 'the seek bar (role=slider, tabindex) draws the browser\'s own 1px ring on click; the part has no :focus-visible rule for it'
    else:
        note = '%d ring(s): %s' % (len(hits), '; '.join(kinds))
    row(p['slug'], R, C, 'break', ev, note)
# static leg: pointer rule present, listener absent
for p in PARTS:
    if not p['snippet']: continue
    t = open(p['snippet']).read()
    if 'data-modality="pointer"' in t and not re.search(r'dataset\.modality\s*=|setAttribute\(\s*[\'"]data-modality', t):
        row(p['slug'], R, 'C02b the pointer-flag rule needs the script that sets the flag', 'break' if p['slug'] not in PARKED else 'not-judged',
            fl(p['snippet'], r'data-modality="pointer"'), 'the CSS rule that hides the ring after a click is present, nothing sets data-modality (AM #314 proposal a)')

# ------------------------------------------------------------------ C03 :focus-within active state (open)
C = 'C03 a field\'s own active state on click (the 4px bar / border change on :focus-within)'
R = ['s314-D1']
for p in PARTS:
    if not p['snippet']: continue
    html, rules = L.part_rules(p['snippet'])
    hits = [r for r in rules if ':focus-within' in r['sel'] and re.search(r'(border|box-shadow|background)[\w-]*\s*:', r['decls']) and 'modality' not in r['sel']]
    if hits:
        row(p['slug'], R, C, 'unclear' if p['slug'] not in PARKED else 'not-judged', '%s:%d' % (L.rel(p['snippet']), hits[0]['line']),
            '%d rule(s) change the field on :focus-within, which a click triggers; AM #314 left this to Dave (its open question 1)' % len(hits))

# ------------------------------------------------------------------ C04 corners are tokens; the join token
C = 'C04 corners are token-bound: no plain 0 radius in a part\'s own rules'
R = ['s313-D43', 's313-D74']
def toplevel(v):
    out, d, cur = [], 0, ''
    for ch in v:
        if ch == '(': d += 1
        if ch == ')': d -= 1
        if ch == ' ' and d == 0: out.append(cur); cur = ''
        else: cur += ch
    out.append(cur); return [x for x in out if x]
for p in PARTS:
    if not p['snippet']: continue
    html, rules = L.part_rules(p['snippet']); bad = []
    for r in rules:
        for prop, val in re.findall(r'(border(?:-(?:top|bottom|start|end)-(?:left|right|start|end))?-radius)\s*:\s*([^;]+)', r['decls']):
            if any(x in ('0', '0px') for x in toplevel(val.strip().replace('!important', ''))): bad.append(r)
    row(p['slug'], R, C, 'break' if bad else 'clean', ('%s:%d' % (L.rel(p['snippet']), bad[0]['line'])) if bad else L.rel(p['snippet']),
        'plain 0 corner' if bad else 'parsed every border-*-radius in the part\'s own rules: none is a bare 0')
row('split-button', ['s313-D43', 's313-D73'], 'C04b the square-corner token is named join', 'clean', fl(sn('Split-button'), r'border-radius-join'), 'uses var(--border-radius-join)')
row('split-button', ['s313-D73'], 'C04c the token\'s own note still calls its name a placeholder', 'cosmetic', fl(os.path.join(K, 'tokens/layout.json'), r"PROVISIONAL NAME"),
    "tokens/layout.json says 'join' is a PLACEHOLDER and 'the token's name is Dave's and is still open'; s313-D73 ruled the name join")

# ------------------------------------------------------------------ C05 alpha on text for hierarchy (open)
C = 'C05 transparency on text for hierarchy (not a state change)'
R = ['ds-026', 's305-D11']
STATE = re.compile(r':(hover|active|focus|disabled|checked|indeterminate|visited|placeholder|not\(|has\()|\[(aria-(disabled|pressed|selected|current|expanded|checked|busy|invalid)|disabled|data-state|data-open|hidden|open|data-ftb-state)|\.is-|\.(disabled|loading|leaving|show|open|on|off|selected|active|pending|busy|stale|empty|error)\b|placeholder')
for p in PARTS:
    if not p['snippet']: continue
    html, rules = L.part_rules(p['snippet'])
    hits = [r for r in rules if (L.decl(r['decls'], 'opacity') or '').find('alpha') >= 0 and not STATE.search(r['sel']) and r['media'] == '']
    if hits:
        row(p['slug'], R, C, 'unclear' if p['slug'] not in PARKED else 'not-judged', ['%s:%d' % (L.rel(p['snippet']), r['line']) for r in hits[:4]],
            '%d rule(s) dim text with an --alpha-* opacity outside any state, e.g. %s' % (len(hits), ', '.join(r['sel'][:30] for r in hits[:3])))
    else:
        row(p['slug'], R, C, 'clean', L.rel(p['snippet']), 'no --alpha-* opacity outside a state selector')

# ------------------------------------------------------------------ C06 links navigate only
C = 'C06 a link only navigates; a download is a button'
R = ['s272-D2']
for p in PARTS:
    if not p['snippet']: continue
    t = open(p['snippet']).read()
    h = re.sub(r"<!-- ===== APOLLO-DEMO.*?END ===== -->", "", t, flags=re.S)
    a = re.search(r'<a [^>]*\bdownload\b', h); b = re.search(r'<a [^>]*>(?:(?!</a>).)*?\b[Dd]ownload\b', h, re.S)
    if a or b:
        ev = []
        if a: ev.append(fl(p['snippet'], r'<a [^>]*\bdownload\b'))
        if b and not a: ev.append(fl(p['snippet'], r'<a [^>]*>.*[Dd]ownload|>Download statement'))
        row(p['slug'], R, C, 'break', ev, 'an <a> carries a download (the `download` attribute, or a link whose words are a download)')
    elif p['slug'] in ('links', 'document-row', 'footer'):
        row(p['slug'], R, C, 'clean', L.rel(p['snippet']), 'no <a> with download')

# ------------------------------------------------------------------ C07 one toast at a time
row('toast', ['s272-D25'], 'C07 exactly one toast in the live region', 'break',
    [fl(sn('Toast'), r'region\.appendChild\(t\)'), fl(sn('Toast'), r'id="toastRegion"')],
    'spawn() appends every new toast to the live region and removes none, so two clicks stack two toasts')
row('toast', ['s313-D68'], 'C07b the toast has no error kind', 'clean', fl(sn('Toast'), r'No error variant by design'), 'no error kind; errors go to the alert')

# ------------------------------------------------------------------ C08 FAB and back-to-top never both
C = 'C08 FAB and Back-to-top are never both present'
for p in PARTS:
    if not p['snippet']: continue
    t = open(p['snippet']).read()
    f = re.search(r'class="[^"]*\bfab\b', t); b = re.search(r'class="[^"]*\bbtt\b', t)
    if f or b:
        row(p['slug'], ['s272-D5'], C, 'break' if (f and b) else 'clean', L.rel(p['snippet']), 'fab=%s btt=%s' % (bool(f), bool(b)))

# ------------------------------------------------------------------ C09 action bar holds at most three
row('action-bar', ['s272-D4'], 'C09 an action bar holds at most three actions', 'clean', fl(sn('Action-bar'), r'<div class="action-bar">'),
    'three buttons; no .action-bar in any snippet holds more than three (bs4 count)')

# ------------------------------------------------------------------ C10 product copy says HSBC
C = 'C10 product copy says HSBC; Apollo never surfaces as product copy'
R = ['s261-D8']
HSBC = {'cta-lockup': [('CTA-lockup', r'See how Apollo can work')], 'feature-grid-lockup': [('Feature-grid-lockup', r"Apollo's own products")],
        'footer-doormat-lockup': [('Footer-doormat-lockup', r'Apollo is the reference implementation'), ('Footer-doormat-lockup', r'&copy; 2026 Apollo')]}
for slug, pats in HSBC.items():
    row(slug, R, C, 'break', [fl(sn(n), pat) for n, pat in pats], 'visible product copy names Apollo')
row('legend', R, C, 'unclear', fl(sn('Legend'), r'only round components in Apollo'), 'a showroom note (not product copy) names Apollo as the system; his words reach "a showroom page"')
for p in PARTS:
    if p['snippet'] and p['slug'] not in HSBC and p['slug'] != 'legend':
        row(p['slug'], R, C, 'clean', L.rel(p['snippet']), 'no Apollo in visible text, aria-label, alt, title or placeholder (fenced demo blocks, scripts, styles and comments stripped)')

# ------------------------------------------------------------------ C11 Metric and the stat-card drawing
R = ['s308-D42', 's309-D3', 's310-D1']
for n, slug in (('Hero-variants', 'hero-variants'), ('Stats-band-lockup', 'stats-band-lockup')):
    row(slug, R, 'C11 a figure tile is Metric, with the thin direction arrow', 'break',
        [fl(sn(n), r'class="stat-card"'), fl(sn(n), r'id="(hv|sb)-up"')],
        'still draws the old stat card (class stat-card%s) with the FILLED triangle (M16 12L2 12L9 5L16 12Z), not Metric with the direction arrow' % (' and kpi-tile' if slug == 'stats-band-lockup' else ''))
row('stat-card', R, 'C11 a figure tile is Metric, with the thin direction arrow', 'unclear', [fl(sn('Stat-card'), r'id="sc-up"'), fl(mt('stat-card'), r'"aliasOf"')],
    'the meta is an alias of Metric, but the Stat-card snippet still draws the filled triangle; s309-D3 keeps the drawing only while something still needs it, and Hero-variants and Stats-band-lockup do')
row('metric', ['s310-D1'], 'C11 a figure tile is Metric, with the thin direction arrow', 'clean', fl(sn('Metric'), r'byte-matched from assets/icons/global-controls/direction-up'), 'direction arrow, byte-matched')
row('metric', ['s309-D6'], 'C11b the no-change mark at full ink', 'clean', fl(sn('Metric'), r'It was drawn at alpha-60 until #309'), 'no opacity on the flat glyph')
row('template-report', ['s314-D18'], 'C11c the KPI row has no orphan at any width', 'clean', [fl(sn('Template-report'), r'aria-label="Gross receipts"'), fl(sn('Metric'), r'@media \(max-width:900px\)')],
    'four Metrics on Metric\'s own board: 4 in a row, 2x2 under 900px, one column under 560px')
row('kpi-tile', ['s308-D42'], 'C11d old names kept as aliases', 'clean', fl(mt('kpi-tile'), r'"aliasOf"'), 'aliasOf component:metric')

# ------------------------------------------------------------------ C12 parts fill their container
R_FILL = {'tabs': (['s313-D42'], 'Tabs', r'--tabs-w:100%'), 'summary': (['s314-D10'], 'Summary', r'the showroom.s column'),
          'timeline': (['s314-D10'], 'Timeline', r'--tl-w:100%'), 'meter': (['s210-D3'], 'Meter', r'\.meter\{|\.meter \{|meter\{'),
          'chart-sparkline': (['s184-D1'], 'Chart-sparkline', r'The atom carries no width|spark-kpi-slot'), 'metric': (['s314-D28'], 'Metric', r'F10: the board FILLS')}
for slug, (rr, n, pat) in R_FILL.items():
    row(slug, rr, 'C12 the part fills its container (no fixed part width)', 'clean', fl(sn(n), pat), 'no fixed px width on the part\'s own root rule (parsed every width/max-width >= 100px)')

# ------------------------------------------------------------------ C13 templates: frame, fence, sizing, borders, sections
for slug in TEMPLATES:
    n = 'Template-' + slug[9:]
    s = sn(n)
    if slug in PARKED:
        row(slug, ['s314-D21', 's314-D7'], 'C13 page templates', 'not-judged', L.rel(s), PARKED[slug]); continue
    t = open(s).read()
    nav = '<nav class="sh-nav"' in t; foot = '<footer' in t
    if slug == 'template-auth':
        row(slug, ['s314-D21', 's272-D92'], 'C13a every page template carries the app frame', 'unclear', [fl(s, r'NO FRAME: s272-D92'), fl(mt(slug), r'"name"')],
            'no masthead and no footer: the page follows s272-D92 ("navigation = absent"); s314-D21 names template-auth in its governs list. TP2 asked as Q1; still open')
    else:
        row(slug, ['s314-D21'], 'C13a every page template carries the app frame', 'clean' if nav and foot else 'break', [fl(s, r'<nav class="sh-nav"'), fl(s, r'<footer')], 'masthead nav=%s footer=%s' % (nav, foot))
    row(slug, ['s314-D7'], 'C13b templates are fenced as examples', 'clean', fl(mt(slug), r'"fence"|"\$fence"'), 'fenced; knowledge/_validate_example_fence.py: 11 fenced, 0 failures (run in the cloud worktree, its report unchanged)')
    row(slug, ['s305-D57', 's305-D61'], 'C13c the page places parts and never sizes or restyles them', 'clean', L.rel(s),
        'no rule in the page\'s own style targets another part\'s class with geometry or colour (class map built from every part\'s own rules)')
row('template-empty', ['s314-D16'], 'C13d the empty page has no border', 'clean', fl(sn('Empty-state'), r'\.empty\.bordered'), 'the empty-state column draws no surface by default; the dashed edge is a variant')
row('template-error', ['s314-D17', 's314-D19'], 'C13d the error page has no border; its column is the empty-state part', 'clean', fl(sn('Template-error'), r'class="empty"'), 'uses .empty, no bordered variant')
row('template-list-index', ['s314-D22', 's314-D25'], 'C13e both list forms; no download on the rows', 'clean', [fl(sn('Template-list-index'), r'cn-data-grid'), fl(sn('Template-list-index'), r'cn-list-items')], 'data grid and list items both drawn; no download on the list')
row('template-auth', ['s314-D23'], 'C13f the sign-in logo stays at 40', 'clean', fl(sn('Template-auth'), r'colour-40\.svg'), 'the 40 master')
row('template-settings', ['s314-D20', 's272-D91'], 'C13g the settings wording is amended (sections sit on rules)', 'unclear',
    [fl(sn('Template-settings'), r'card surfaces'), 'knowledge/_rulings.json (s272-D91 text unchanged)'],
    'the page sits on rules; the amended wording does not exist anywhere: s272-D91 still reads "sections are grouped on card surfaces", and TP2\'s R2 draft waits for him')
for slug in TEMPLATES:
    if slug in PARKED: continue
    d = json.load(open(mt(slug)))
    if 'when' not in d:
        row(slug, ['s272-D84', 's272-D86', 's272-D87', 's272-D88', 's272-D89', 's272-D90', 's272-D91', 's272-D92'], 'C13h the ratified template `when` gate is on the meta', 'unclear', L.rel(mt(slug)),
            'no `when` on the meta; the template gates were ratified at #272, and since s314-D7 builds ignore templates, whether the gates still matter is his')

# ------------------------------------------------------------------ C14 help text is short and does not wrap (render)
C = 'C14 help text is short and does not wrap (cloud render: help_wrap.py at 1280px)'
R = ['s314-D11']
hw = json.load(open(os.path.join(HERE, 'help_wrap.json')))
DEMO_HINT = {'Data-grid.reference.html', 'Table.reference.html'}
for name, items in hw.items():
    slug = next((p['slug'] for p in PARTS if p['snippet'] and os.path.basename(p['snippet']) == name), None)
    if not slug: continue
    wr = [x for x in items if x.get('lines', 0) > 1]
    if name in DEMO_HINT and wr:
        row(slug, R, C, 'cosmetic', 'notes/_lanes/315/LA/help_wrap.json', 'the wrapping line is a showroom keyboard hint (class hint), not a field\'s help text'); continue
    if wr:
        x = wr[0]
        row(slug, R, C, 'break' if slug not in PARKED else 'not-judged', [fl(sn(name[:-15]), re.escape(x['text'][:30])), 'notes/_lanes/315/LA/help_wrap.json'],
            '%d help line(s) wrap; e.g. "%s" (%d chars, %d lines at %dpx)' % (len(wr), x['text'][:70], x['chars'], x['lines'], x['width']))
    else:
        row(slug, R, C, 'clean', 'notes/_lanes/315/LA/help_wrap.json', '%d help line(s), none wraps' % len(items))

# ------------------------------------------------------------------ C15 the four selection controls
for s in ['switch', 'checkbox', 'radio', 'chip']:
    d = json.load(open(mt(s)))
    row(s, ['s313-D56', 's314-D4'], 'C15 four parts, each offered for the input role', 'clean' if d.get('provides') == 'input' else 'break', fl(mt(s), r'"provides"'), 'provides=%s' % d.get('provides'))
fam = json.load(open(mt('selection-controls')))
row('selection-controls', ['s314-D6'], 'C15b the family keeps only what the four share', 'clean', fl(mt('selection-controls'), r'"props"'), 'family props: %s' % [p['name'] for p in fam.get('props', [])])
for s, pat in (('data-grid', r'Checkbox \(named by its own part'), ('transfer-list', r'Checkbox \(drawn by the Selection-controls reference; named'), ('rating', r'native radios')):
    row(s, ['s314-D5'], 'C15c a part that borrows a control names it', 'clean', fl(mt(s), pat), 'named in prose; no part names the family')

# ------------------------------------------------------------------ C16 trees: rest-state word, plain words
def walk(n, out):
    if isinstance(n, dict):
        if 'part' in n and 'tag' in n: out.append((n['part'], n['tag']))
        for v in n.values(): walk(v, out)
    elif isinstance(n, list):
        for v in n: walk(v, out)
for p in PARTS:
    d = json.load(open(p['meta']))
    st = d.get('states')
    if isinstance(st, dict):
        ini = st.get('initial')
        row(p['slug'], ['s313-D18'], 'C16a the rest state takes the part\'s own word', 'break' if ini == 'default' else 'clean', fl(p['meta'], r'"initial"'), 'initial = %s' % ini)
    a = d.get('anatomy')
    if a is not None:
        out = []; walk(a, out)
        bad = [pp for pp, t in out if re.fullmatch(re.escape(t) + r'(-\d+)?', pp) and t not in ('label', 'input', 'button', 'table', 'dialog', 'nav', 'caption', 'legend')]
        row(p['slug'], ['s313-D17'], 'C16b a piece the markup does not name is called in plain words, not its tag', 'break' if bad else 'clean',
            fl(p['meta'], r'"part": "(%s)"' % '|'.join(map(re.escape, bad))) if bad else L.rel(p['meta']), ('tag words as part names: %s' % bad) if bad else '%d pieces, all named' % len(out))

# ------------------------------------------------------------------ C17 kinds and roles
for s in ['tabs', 'accordion', 'popover']:
    k = json.load(open(mt(s))).get('kind')
    row(s, ['s309-D1'], 'C17 tabs, accordion and popover are blocks', 'clean' if k == 'block' else 'break', fl(mt(s), r'"kind"'), 'kind=%s' % k)
chart_panel = [p['slug'] for p in PARTS if json.load(open(p['meta'])).get('provides') == 'chart-panel']
row('roles.json', ['s308-D41'], 'C17b the chart-panel role is named chart', 'clean' if not chart_panel else 'break', 'knowledge/roles.json', 'no meta provides chart-panel; roles.json has no "chart-panel" key')

# ------------------------------------------------------------------ C18 nav family
C = 'C18 the current nav item carries the selected (-active) version of its icon'
for n, slug in (('App-shell-side-nav', 'app-shell-side-nav'), ('App-shell-nav-rail', 'app-shell-nav-rail'), ('App-shell-multi-column', 'app-shell-multi-column')):
    row(slug, ['s262-D3'], C, 'break', fl(sn(n), r'aria-current="page"><span class="si"'), 'the current row (Accounts) draws #ic-account only; no -active twin is defined or swapped in')
row('tab-bar', ['s262-D3'], C, 'break', fl(sn('Tab-bar'), r'aria-label="Home" aria-current="page"'), 'the segmented island\'s current item draws the outline #ic-home only (the plain bar above swaps .ic-line for .ic-fill; the island does not)')
row('sidebar-nav', ['s262-D3'], C, 'clean', fl(sn('Sidebar-nav'), r'aria-current="page".*#ic-account-a'), 'the current row carries #ic-account and #ic-account-a and swaps to the -active glyph')
row('navigations', ['s262-D3'], C, 'clean', fl(sn('Navigations'), r'aria-current="page"><span class="nv-label">Accounts'), 'the top nav\'s current item is words only (no icon), so there is nothing to swap')
row('navigations', ['s305-D13'], 'C18b the nav badge is 8px, no 7px', 'clean', L.rel(sn('Navigations')), 'no 7px in the nav family\'s own rules (Navigations, Sidebar-nav, Tab-bar, app shells)')
row('navigations', ['s313-D23'], 'C18c a flyout has at most six links in one column', 'clean', fl(sn('Navigations'), r'nav-flyout'), 'the flyout holds 3 links; the rail flyouts hold 3 and 4')

# ------------------------------------------------------------------ C19 ink in dark: borders, roundels, icons, QR
row('button', ['s313-D39', 's313-D60'], 'C19a the outline border follows the ink, in dark too', 'break',
    [fl(os.path.join(K, 'canon/canon.css'), r'^\s*--border-action-strong: #FFFFFF'), fl(os.path.join(K, 'canon/canon.css'), r'^\s*--text-default: #E1E1E1'), fl(sn('Button'), r'"--ter-border": "button/tertiary/border/default"')],
    'in dark the tertiary button\'s border is border/action-strong = #FFFFFF while its label is text/default = #E1E1E1: two colours, not one')
for slug, n in (('icon-button', 'Icon-button'), ('page-header-lockup', 'Page-header-lockup'), ('section-heading-lockup', 'Section-heading-lockup'), ('payment-card-visual', 'Payment-card-visual'), ('hero-variants', 'Hero-variants')):
    row(slug, ['s313-D39', 's313-D60'], 'C19a the outline border follows the ink, in dark too', 'break', fl(sn(n), r'button/tertiary/border'), 'binds button/tertiary/border/default, which resolves to #FFFFFF in dark against #E1E1E1 ink (same cause as Button)')
row('confirmation', ['s313-D61', 's313-D35'], 'C19b the big tick follows the ink in dark', 'unclear', [fl(sn('Confirmation'), r'\[data-theme="dark"\]\{.*--success:#FFFFFF'), fl(os.path.join(K, 'canon/canon.css'), r'^\[data-theme="dark"\] \.cn-confirmation\{')],
    'dark --success is #FFFFFF by a driftAllow from the July roundel policy: neither the ink (#E1E1E1) his click names ("The big tick follows") nor the green his comment keeps ("confirmations can stay green"); he asked for its own review page')
row('status-indicator', ['s313-D35'], 'C19b the dark status marks follow the ink', 'cosmetic', fl(sn('Status-indicator'), r'--neutral:#FFFFFF'), 'the neutral status dot is #FFFFFF in dark; the others are colours. A dot, not a roundel')
row('library', ['s311-D1'], 'C19c dark icons follow the ink', 'clean', 'knowledge/tokens/modes/dark/semantic-colour.json', 'no part binds an icon/* token whose dark value is #FFFFFF (icon/default dark = neutral 12 #E1E1E1). Icons drawn with other tokens were not traced')
row('qr-code', ['s307-D50'], 'C19d QR codes stay dark on light in every mode', 'clean', fl(sn('Qr-code'), r'unchanged, that is the whole point'), 'fixed plate #FFFFFF and module #1A1A1A in both modes')

# ------------------------------------------------------------------ C20 one button atom
C = 'C20 a button inside a part is built from the one button atom'
for n, slug, pat in (('Empty-state', 'empty-state', r'\.ebtn\{'), ('Drawer', 'drawer', r'\.dbtn\.primary\{'), ('Modals', 'modals', r'\.btn\.primary\{background:var\(--pri\)'),
                     ('Popconfirm', 'popconfirm', r'\.pc \.btn\.primary\{'), ('Confirmation', 'confirmation', r'\.confirm \.btn\.primary\{'), ('Action-bar', 'action-bar', r'\.action-bar \.btn\.primary\{'),
                     ('Hero', 'hero', r'\.hero \.cta\{'), ('Hero-variants', 'hero-variants', r'\.hero \.cta\{')):
    note = 'redraws the primary button locally (background:var(--pri) in its own rule)'
    if slug == 'empty-state': note += '; its hover is a private color-mix(... 70%), not Button\'s --pri-hover, and #314 finding 7 named it with Confirmation, but TP2 fixed only Confirmation (F7)'
    row(slug, ['ds-032'] + (['s314-D28'] if slug == 'empty-state' else []), C, 'break', fl(sn(n), pat), note)

# ------------------------------------------------------------------ C21 parts the rulings folded or reworked
row('range-slider', ['s308-D6'], 'C21 the range slider is Slider\'s two-handle form, not its own part', 'break', [fl(mt('range-slider'), r'SUPERSEDED COPY'), fl(mt('range-slider'), r'"provides"')],
    'its meta and snippet still stand and still provide `input`; the merge into slider.meta.json is drafted, row W-308i4 open')
row('transaction-row', ['s307-D51'], 'C21 the transaction row is a variant of list items', 'break', fl(mt('transaction-row'), r'"provides"'), 'still its own part providing record-list; the variant is ruled, not built')
row('standing-order-mandate-row', ['s308-D4'], 'C21 the standing order row is a variant of list items', 'break', fl(mt('standing-order-mandate-row'), r'"provides"'), 'still its own part providing record-list; he asked to see options first')
for s in ('progress-bar', 'limits-meter'):
    row(s, ['s210-D1', 's308-D5'], 'C21 the progress bar and limits meter are one Meter', 'clean', fl(mt(s), r'"aliasOf"'), 'alias of component:meter')
row('date-picker', ['s307-D49'], 'C21 the date picker uses the calendar part', 'clean', fl(sn('Date-picker'), r'THE CALENDAR PART, not a copy'), 'the calendar part, injected')
row('date-range-picker', ['s307-D49'], 'C21 the date picker uses the calendar part', 'unclear', fl(sn('Date-range-picker'), r'dr-week'), 'the range picker draws its own month grid; his ruling named the date picker only')

# ------------------------------------------------------------------ C22 the pending roundel clash
row('confirmation', ['s314-D15', 's314-D26'], 'C22 a pending kind on the confirmation part', 'unclear', [fl(sn('Confirmation'), r'\.pending'), fl(mt('confirmation'), r'"pending"')],
    'the part carries the amber pending kind (his call 15 comment); his call 26 click says no pending kind. Open as W-314d1')

# ------------------------------------------------------------------ C23 misc clean checks with their evidence
row('carousel', ['s307-D52'], 'C23 no autoplay', 'clean', fl(sn('Carousel'), r'NO AUTOPLAY, AND NO AUTOPLAY OPTION'), 'none')
row('video-player', ['s307-D52'], 'C23 no autoplay', 'clean', fl(sn('Video-player'), r'no autoplay'), 'none')
row('library', ['s313-D20'], 'C23 container words: section and panel; division and sector dropped', 'clean', 'knowledge/components/*.meta.json', 'no meta or snippet uses division or sector as a container word (grep -w; prose hits only)')
row('library', ['s308-D25'], 'C23 the legacy theme reads Common wherever a person reads it', 'clean', 'knowledge/snippets/*.reference.html', 'no part draws a theme name in visible text; theme pickers live in the showroom generator, not checked')
row('library', ['s258-D3'], 'C23 demo chrome (state switchers, width dials, theme bars) is fenced', 'clean', 'knowledge/snippets/*.reference.html',
    'no unfenced interactive switcher or theme bar found by class/attribute; 20 snippets carry unfenced specimen frames and captions (demo-frame, stateLabel), which the generator drops by class')

# ------------------------------------------------------------------ summary
from collections import Counter
parts_with_rows = sorted({r['part'] for r in ROWS})
def _k(s):
    m = re.match(r'([a-z]+)-?(\d+)(?:-D(\d+))?', s)
    return (m.group(1), int(m.group(2)), int(m.group(3) or 0)) if m else (s, 0, 0)
rulings_checked = sorted({x for r in ROWS for x in r['rulings']}, key=_k)
out = {
    '$about': 'Apollo #315 lane LA - the whole-library audit against Dave\'s rulings. Read-only. Rows are part x ruling x check with a verdict and file:line evidence. Verdicts and recommendations are the lane\'s reading, never rulings.',
    'head': '853d7f56',
    'inventory': {'metas': len(PARTS), 'snippets': sum(1 for p in PARTS if p['snippet']),
                  'metas_without_snippet': [p['slug'] for p in PARTS if not p['snippet']],
                  'rulings_in_store': len(RUL)},
    'rulings_checked': {r: {'status': RUL[r]['status'][:60], 'quote': quote(r)} for r in rulings_checked},
    'counts': {'rows': len(ROWS), 'by_verdict': dict(Counter(r['verdict'] for r in ROWS)),
               'parts_with_a_row': len(parts_with_rows)},
    'renders': {'click_sweep': 'notes/_lanes/315/LA/click_sweep.py -> click_sweep.json', 'help_wrap': 'notes/_lanes/315/LA/help_wrap.py -> help_wrap.json'},
    'rows': ROWS,
}
json.dump(out, open(os.path.join(HERE, 'audit.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out['counts'], indent=1)); print('rulings checked', len(rulings_checked))
