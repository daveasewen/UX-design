"""A2 #304 read-only analysis of knowledge/_state.json live items. Writes JSON beside itself."""
import json, re, collections as C, datetime as DT, os
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../..'))
OUT=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(os.path.join(ROOT,'knowledge/_state.json')))
items=d['items']; live=[i for i in items if i['state'] in ('open','blocked','ruled')]
# session -> first commit date
sd={}
for l in open(os.path.join(OUT,'gitlog.txt')):
    h,dt,s=l.rstrip('\n').split('|',2)
    for x in re.findall(r'#(\d{2,3})\b',s[:40]):
        n=int(x); sd[n]=min(sd.get(n,dt),dt)
TODAY=DT.date(2026,9,26); CUR=304
def age_days(n):
    if n in sd: return (TODAY-DT.date.fromisoformat(sd[n])).days
    return None
def txt(i): return ' '.join([i['title'],i.get('body') or '',i['closes_when'] or ''])
# ---- KIND (what the row IS) from title
KINDS=[
 ('wrap-artefact', r"wrap memory hook|delegated[- ]wrap brief|WRAP BRIEF|wrap brief|WRAP FILED|capture ritual|\bW filed report|^#\d+ W\b|^#\d+ W -|#\d+ wrap\b|handoff -|dossier|DOSSIER|words verbatim|CLOSING-wrap|POST-WRAP CAPTURE|wrap sub filed|wrap report|#\d+ W - the wrap|^#\d+ wrap —"),
 ('brief', r"\bBRIEF\b|\bbrief\b|divvy|COMMON LANE RULES|TEMPLATE -"),
 ('filed-report', r"filed report|FILED REPORT|\bFILED\b|filed sub-?report|sub-report|RECEIPT|receipt|verify|VERIFIER|COLD RUN|\blane [A-Z0-9]+ —|\blane [A-Z0-9]+ -|filed\b|REPORT|report"),
 ('review-surface', r"review page|REVIEW|decision page|DECISION PAGE|sitting index|SITTING PAGE|PLAN v|plan page|explorer|option page|decision surface|THREE READINGS|CONFIRM PASS|LIBRARY v2|TUNER|DEMO|MATRIX|GALLERY|LOGOS INTO|FOUNDATIONS TIER"),
 ('instrument', r"NEW INSTRUMENT|instrument|registry|_boot_decompose|gate\b|probe BUILT"),
 ('proposed-build', r"PROPOSED-NOT-RULED|BUILT PROPOSED|PROPOSED"),
 ('drawing/deck', r"deck v|slide|workers v|brain|callipers|catalogue|robot|books|drawing"),
]
def kind(i):
    t=i['title']
    for k,rx in KINDS:
        if re.search(rx,t): return k
    return 'work-item'
# ---- CLOSE TYPE
DAVE_RX=r"\bDave(?:'s)?\b[^.;]{0,40}\b(rule|ruled|rules|answer|answered|answers|read|looked|said|says|seen|sees|worked|sat|sits|confirm|confirmed|given|gives|driven|promotes|picks|picked|ratif|eye|word|turned|acted|declin|accept|test|cold test|pass|report|strik|struck|adopt|views|parks|signs|has had|opened|open|export|pushed|run|runs|named|names|watched|watches|pastes|works|decided|decides|blessed|reviewed|inscribed|asks|keeps|signed|observed|recognises)|\bhis (word|eye|call|pick|read|own screen|own machine|slide-by-slide)\b|\bby Dave\b|Dave's (export|fifteen|live|cold|word|eye)|ratified by Dave|Dave rules|on Dave word|Daves eye|Dave'?s eye"
MECH_RX=r"wrap commit|subject read back|read back from git log|opener (has|reads|or)|#\d+ opener|#\d+ has (answered|read|measured|driven|built|re-run)|#\d+'s opener|closes with|rides its lane|W-\d+[a-z0-9]* closes|superseded by|retired (with|when)|absorbed into|becomes historical|is history|document row|dated history|cited (this|BY PATH|by path)|cites (this|it)|REPLAY-THESE|sub-report is filed|report is filed|placement receipt|Project memory|wrap lands|has FILED|landed in git|the carried items|crank closes|windows close"
def closetype(i):
    cw=i['closes_when']
    if not cw: return 'UNCONDITIONED'
    dv=bool(re.search(DAVE_RX,cw)); mc=bool(re.search(MECH_RX,cw,re.I))
    if dv and not re.search(r"or (explicitly )?carried|explicitly carried|or carried|or the conductor",cw): return 'DAVE'
    if dv: return 'DAVE-or-CARRY'
    if mc: return 'EVENT'
    return 'BUILD'
# past-horizon: close event names a session that has already happened
def horizon(i):
    cw=i['closes_when'] or ''
    ns=[int(x) for x in re.findall(r'#(\d{3})',cw)]
    ns+= [int(x) for x in re.findall(r"\b(\d{3})'s opener",cw)]
    return max(ns) if ns else None
# ---- THEME
THEMES=[
 ('T1 Friday deck & presentation', r"deck|slide|\bthe brain\b|brain's|brain slide|brain turns|brain in the|callipers|workers|catalogue|robot|drawing|plant|press loop|strand map|arc board|\bask\b.*slide|presentation|Friday|demo prompt|chapter rail|books|kinematic|conveyor|typography and alignment|copy editor|publisher|art director|running order"),
 ('T2 Wrap ritual, boot, context window & Memento machinery', r"wrap|capture ritual|boot|memory hook|MEMORY\.md|handoff|dossier|gauge|FILL|window|_CHAIN|GOOD-MORNING|\bGM\b|Memento|Gumdrop|carries|_CARRIES|recall probe|seam|dream[- ]pass|chain-diet|2c|roll|index-vocab|DOFIRST|context-territory|conditional-band|PM[- ]topology|mechanisation|delegat|divvy|parallel windows|Project instructions|cloud|opener|words verbatim|verbatim"),
 ('T3 Designer pack, releases & cold-start', r"v1\.0\.\d+|Spider|bake|pack|release|RATIFY|cold[- ]start|cold test|grill-me|Copilot|designer first hour|designer-skills|manifest|CUT\b|\bcut\b|re-stage|proving zip|encoder|tiktoken|cl100k|Factory|dev team|npm"),
 ('T4 Gates, CI & verifiers', r"\bgate|\bCI\b|verifier|validator|_validate|probe registry|selftest|false green|\breds?\b|build-verdict|help gate|runbook|Actions runtime|/tmp|\block\b|instrument|mechanisation|verify"),
 ('T5 Knowledge graph, rules & principles', r"\bKG\b|graph|explorer|principle|polarit|tension|rules?\b|restsOn|ruling edges|edge|icons?\b|logos?|lockup|roles|provides|meta|when[- ]predicate|verbs|orphan|chip|twins|WCAG|scope per guideline|taxonomy|constitution|designer's brain|ASK page|interchangeab|behaviour address|composition edge"),
 ('T6 Charts & data-viz engine', r"chart|dataviz|DataViz|dv-|DV-D|donut|sparkline|legend|engine|scatter|histogram|butterfly|candlestick|boxplot|pie|stacked|bullet|combo|Meter|G15|G16|intro-motion|bar-motion"),
 ('T7 Dashboards, bento & one-shot composition', r"bento|dashboard|DP-\d|\bDP\d|template|one-shot|cold run|frozen prompt|W1|W2|W3|density|rhythm|FIT\b|VFIT|composition|compose|gutter|grid|FAB|KPI|filter-toolbar|Overview|kpi"),
 ('T8 Components, tokens & themes', r"component|snippet|wave-\d|wave [3-6]|segmented|spacing|radius|caption|mono|token|descender|photograph|Foundations|theme|disabled|ds-0\d\d|RAG|palette|mint|type\.css|hit-area|a11y|contrast|nav family|footer|calendar|carousel|cascader|progress|CSS delivery|phantom|quality-forms|Time-picker|Date|seg\b|console"),
 ('T9 New strands: research (Jev, MCP/GenUI, APCA)', r"Jev|TypeSafe|MCP|GenUI|agent-UI|A2UI|APCA|research|R-KREPE|R-HYPER|playbook"),
]
ORDER=['T9','T1','T6','T7','T5','T3','T8','T4','T2']
TH={n[:2]:(n,rx) for n,rx in THEMES}
def theme(i):
    if kind(i)=='wrap-artefact': return TH['T2'][0]
    t=i['title']; full=txt(i)
    for k in ORDER:
        n,rx=TH[k]
        if re.search(rx,t): return n
    for k in ORDER:
        n,rx=TH[k]
        if re.search(rx,full): return n
    return 'T0 Other'
rows=[]
for i in live:
    n=i['opened']; hz=horizon(i)
    r=dict(id=i['id'],owner=i['owner'],opened=n,age_sessions=(CUR-n) if n else None,age_days=age_days(n) if n else None,
           project=i['project'],kind=kind(i),close=closetype(i),theme=theme(i),horizon=hz,
           horizon_passed=(hz is not None and hz<CUR),title=i['title'][:160],closes_when=(i['closes_when'] or '')[:400],home=i['home'])
    rows.append(r)
json.dump(rows,open(os.path.join(OUT,'live_clustered.json'),'w'),indent=1)
def tab(key):
    c=C.Counter((r[key],r['owner']) for r in rows); ks=sorted(set(r[key] for r in rows))
    for k in ks:
        dv=c[(k,'dave')]; cl=c[(k,'claude')]
        ages=[r['age_days'] for r in rows if r[key]==k and r['age_days'] is not None]
        ages.sort()
        med=ages[len(ages)//2] if ages else None
        print(f"{k:58s} total {dv+cl:4d}  dave {dv:4d}  claude {cl:4d}  median age {med}d  oldest {max(ages) if ages else None}d")
print('LIVE',len(rows),C.Counter(r['owner'] for r in rows))
print('\n== THEME'); tab('theme')
print('\n== KIND'); tab('kind')
print('\n== CLOSE'); tab('close')
print('\n== KIND x CLOSE'); 
for (k,c),v in sorted(C.Counter((r['kind'],r['close']) for r in rows).items()): print(f"{k:16s} {c:14s} {v}")
print('\n== horizon passed (event names a past session):',sum(r['horizon_passed'] for r in rows), C.Counter((r['close'],r['owner']) for r in rows if r['horizon_passed']))
print('age buckets days',C.Counter(('<=7' if a<=7 else '8-14' if a<=14 else '15-30' if a<=30 else '>30') for a in [r['age_days'] for r in rows if r['age_days'] is not None]))
print('opened 0:',sum(1 for r in rows if not r['opened']))
