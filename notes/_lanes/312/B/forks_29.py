#!/usr/bin/env python3
"""#311 overnight wave 1, lane B5 (W-308ib): the 29 colour forks of the #221 triage (bucket A 23 + A2 6,
notes/_subreports/2026-08-27-221-laneB.md section 9), re-measured at HEAD by knowledge/_validate_token_forks.py
--strict --json, each scored with the repo's bloom/dance model (reviews/_rag_bloom_model.py, loaded the way
notes/_lanes/310/C/bloom_options.py loads it), each given a PICK within a ruling on record or a QUESTION for Dave.
Scores are relative: bloom 100 = a 40px white fill on #1A1A1A; dance 100 = saturated blue 1px text on #1A1A1A.
Run from the repo root: python3 notes/_lanes/312/B/forks_29.py [--json out] [--html out]"""
import json, sys, re, subprocess, os
src=open('reviews/_rag_bloom_model.py').read(); src=src[:src.index("DPG='#1A1A1A'")]
ns={}; exec(src,ns); B,D,wcag=ns['B'],ns['D'],ns['wcag']

WHITE='#FFFFFF'; DARKPAGE='#1A1A1A'; INK='#1A1A1A'
def comp(ink,fill,w):
    """ink on fill at stroke w px -> (wcag, bloom, dance)"""
    return round(wcag(ink,fill),2), B(ink,fill,w), D(ink,fill,w)

# --- the live measurement at HEAD ---
meas_path='/tmp/b5/forks.json'
if not os.path.exists(meas_path):
    os.makedirs('/tmp/b5',exist_ok=True)
    subprocess.run([sys.executable,'knowledge/_validate_token_forks.py','--strict','--json',meas_path],capture_output=True)
meas=json.load(open(meas_path))
live={(f['prop'],f['theme'],f['mode']):f for f in meas['forks']}
def live_pair(prop,theme,mode):
    f=live.get((prop,theme,mode))
    if not f: return None
    return {'a':f['a']['file_line']+' '+f['a']['selector']+' '+f['a']['declared']+' -> '+f['a']['resolved'],
            'b':f['b']['file_line']+' '+f['b']['selector']+' '+f['b']['declared']+' -> '+f['b']['resolved']}

rows=[]
def row(n, prop, theme, mode, s221, cls, pick, rule, scores, note, to_dave=False):
    rows.append(dict(n=n, prop=prop, theme=theme, mode=mode, at_221=s221, live=live_pair(prop,theme,mode),
                     cls=cls, pick=pick, rule=rule, scores=scores, note=note, to_dave=to_dave))

# 1-2 --err mono: the third red. Composition = the global notification bar, text on fill.
for mode in ('any','dark'):
    page = WHITE if mode=='any' else DARKPAGE
    sc={'as built: white on #A8000B (2px text)':comp(WHITE,'#A8000B',2),
        'mono spine as ruled: #1A1A1A on #F6604C (2px text, s149-D1)':comp(INK,'#F6604C',2),
        'white on #F6604C (what a bare re-point would paint)':comp(WHITE,'#F6604C',2),
        'fill on page #A8000B / '+page+' (40px)':comp('#A8000B',page,40),
        'fill on page #F6604C / '+page+' (40px)':comp('#F6604C',page,40)}
    row(1 if mode=='any' else 2,'--err','mono',mode,'#f6604c vs #a8000b (canon 907 v 1842/1855)','WAIT (third red)',
        'WAIT on W-308ia (lane B6): no move tonight. When it lands, the mono answer on record is the ink camp: fill var(--rag-error) #F6604C with #1A1A1A text (5.55:1), not white.',
        'W-308ib body (the #221 --err forks in mono are the third red and wait on W-308ia); s149-D1 (mono error on surface: dark text on #F6604C); s151-D1(2) (light red on every non-white ground)',
        sc,'Contrast is the reason the legacy red survived here: the global bar paints WHITE text (--gtext #FFFFFF) and white on #F6604C is 3.1:1. The ruled mono answer flips the ink, not the fill.')

# 3-4 --warn mono
for mode in ('any','dark'):
    sc={'as built: #333333 on #FFBB33 (2px text)':comp('#333333','#FFBB33',2),
        'pick: #1A1A1A on #E0A61F (2px text, s122-D2)':comp(INK,'#E0A61F',2),
        'fill on white #FFBB33 (40px)':comp('#FFBB33',WHITE,40),
        'fill on white #E0A61F (40px)':comp('#E0A61F',WHITE,40)}
    row(3 if mode=='any' else 4,'--warn','mono',mode,'#e0a61f vs #ffbb33 (canon 906 v 1843/1856)','LEGACY PALETTE IN MONO',
        'Re-point .cn-notifications --warn to var(--rag-warning) (#E0A61F) and its warn text --gtext #333333 to var(--mark-warning) #1A1A1A. Snippet edit, canon regen: NOT tonight (A1 regenerates).',
        's122-D2 (mono warning fill #E0A61F, mark #1A1A1A, 7.99:1); s131-D1 (#FFBB33 is LEGACY\'s own amber); s176-D1 (#333333 is legacy\'s ink, never one literal shared across themes); s136-D1(A) free hex forbidden',
        sc,'Neither value was chosen for contrast: dark ink passes on both ambers (7.5 v 8.0). #FFBB33 is legacy\'s amber pasted into the mono scope. Not a colour choice for Dave: the mono amber is ruled.')

# 5-6 --info mono
for mode in ('any','dark'):
    sc={'as built: white on #305A85 (2px text)':comp(WHITE,'#305A85',2),
        'bare re-point: white on #78A7E8 (2px text) FAILS':comp(WHITE,'#78A7E8',2),
        'pick: #1A1A1A on #78A7E8 (2px text, s122-D2)':comp(INK,'#78A7E8',2),
        'fill on white #305A85 (40px)':comp('#305A85',WHITE,40),
        'fill on white #78A7E8 (40px)':comp('#78A7E8',WHITE,40)}
    row(5 if mode=='any' else 6,'--info','mono',mode,'#78a7e8 vs #305a85 (canon 908 v 1845/1857)','LEGACY PALETTE IN MONO',
        'Re-point .cn-notifications --info to var(--rag-information) (#78A7E8) AND flip the global bar\'s info text from white to var(--mark-info) #1A1A1A (7.04:1). Snippet edit, canon regen: NOT tonight.',
        's122-D2 (mono information fill #78A7E8, mark #1A1A1A, 7.04:1); s151-D1(4) (symbols seated on a status colour take the default ink); s149-D1 (mono joins the ink camp); s131-D1 (#305A85 is LEGACY\'s blue, reversed white)',
        sc,'Dave\'s caveat holds here: the legacy blue was kept BECAUSE the bar paints white text (7.2:1) and white on the mono blue is 2.5:1. The ruled mono answer is the ink flip (7.0:1), which is what every other mono status surface already does.')

# 7-8 --ink legacy / supercharge: name collision
for theme,chart_ink,rule_ink in (('legacy','#333333','s176-D1 legacy ink Grey 8 #333333'),('supercharge','#13110E','s176-D1 Supercharge ink warm/2 #13110E')):
    page = WHITE if theme=='legacy' else '#F7F6F4'
    sc={'banner.err: white on legacy error #A8000B (2px)':comp(WHITE,'#A8000B',2) if theme=='legacy' else comp(WHITE,'#B92F1E',2),
        'chart-bar ink '+chart_ink+' on page (2px)':comp(chart_ink,page,2)}
    row(7 if theme=='legacy' else 8,'--ink',theme,'any','#ffffff vs #333333 / #13110e (banner v chart-bar)','NAME COLLISION',
        'No colour moves. Two components use --ink as a LOCAL nickname for two different things (the error banner\'s reversed text; the chart\'s axis ink). Fix is the W-59 rename-to-local-names class, not a value.',
        's131-D1 (legacy banner text reversed WHITE on error); '+rule_ink+'; s178-D1(a) (a shared local name is unified by renaming, never by moving a value); W-59',
        sc,'Both values are ruled and both are right where they sit. Not a colour choice.')

# 9-10 --muted mono: hero grey vs ink-only spine  -> QUESTION
for mode in ('any','dark'):
    page = WHITE if mode=='any' else DARKPAGE
    hero = '#767676' if mode=='any' else '#9A9A9A'
    spine = '#1A1A1A' if mode=='any' else '#E1E1E1'
    sc={'hero as built: '+hero+' on page (2px text)':comp(hero,page,2),
        'spine --text-secondary '+spine+' on page (2px text)':comp(spine,page,2),
        'hero as built, 5px display size':comp(hero,page,5),
        'spine, 5px display size':comp(spine,page,5)}
    row(9 if mode=='any' else 10,'--muted','mono',mode,'#1a1a1a vs #767676 / #ffffff vs #9a9a9a (root v hero)','QUESTION',
        'QUESTION for Dave. The hero paints its sub-line in a grey the mono spine does not have: mono text/secondary IS the ink (#1A1A1A light, #E1E1E1 dark). Either the hero follows the spine (sub-line becomes ink) or mono mints a quieter text grey.',
        's136-D1(A) (free hex forbidden; the token is #1A1A1A); s176-D1 (ink principle); no ruling on record mints a mono secondary text grey',
        sc,'A real colour choice. Light: #767676 is the lowest AA pass (4.54:1). Dark: #9A9A9A cuts the bloom of the spine\'s #E1E1E1 on the dark page from 16 to 3 (a halation reason, exactly the caveat). Not settleable within a ruling on record.',True)

# 11 --data-grid mono: ds-020 fence
sc={'chart-bar grid: #E1E1E1 on white (1px)':comp('#E1E1E1',WHITE,1),
    'boxplot grid: #626262 at 10% on white ~ #F0F0F0 (1px)':comp('#F0F0F0',WHITE,1),
    'dark: --data-grid-color #484848 on #000000 tile (1px)':comp('#484848','#000000',1),
    'dark: boxplot #9D9D9D at 16% on #000000 ~ #191919 (1px)':comp('#191919','#000000',1)}
row(11,'--data-grid','mono','any','#e1e1e1 vs #626262 (chart-bar v boxplot)','FENCED GAP (ds-020)',
    'Bind the boxplot\'s --data-grid to var(--data-grid-color) with --grid-alpha 1 (the DV-D07 two-channel migration its own $note fences off). Snippet edit, canon regen: NOT tonight.',
    'Chart-boxplot.reference.html $note (ds-020 UNBOUND, "pre-DV-D07 ink-at-alpha idiom kept deliberately, receipted not filled"); ds-026 (charts stick to the SOLID palette); s123-D3 (opacity for tints, not chart grids)',
    sc,'Not a colour choice: an ink-at-alpha idiom the chart programme fenced and never migrated. On white the two grids are near-identical hairlines; on the black tile the alpha grid (~#191919) all but vanishes, so the token is the better line in dark.')

# 12-16 --data-series-1..5: the high-contrast VARIANT
hc={'1':('#766682','#484D6F'),'2':('#A45C3A','#97482C'),'3':('#577C78','#385F4F'),'4':('#7F7B45','#6E465D'),'5':('#A37E94','#7C6F34')}
for k,(std,h) in hc.items():
    sc={'standard '+std+' fill on white (40px)':comp(std,WHITE,40),
        'high-contrast '+h+' fill on white (40px)':comp(h,WHITE,40),
        'standard '+std+' on #000000 tile (40px)':comp(std,'#000000',40),
        'high-contrast '+h+' on #000000 tile (40px)':comp(h,'#000000',40)}
    row(11+int(k),'--data-series-'+k,'mono','any',std.lower()+' vs '+h.lower()+' (root v [data-contrast="high"])','SANCTIONED VARIANT',
        'No colour moves. [data-contrast="high"] is a VARIANT switch on the chart node, chosen for contrast by construction; declare it in _TOKEN-FORK-LEDGER.json as meant (the s305-D41 form) so the gate stops reading a variant as a fork.',
        's136-D1(B) (variants are sanctioned variation, carried as a switch on the owning node); Chart-bar.meta.json:35 ("high-contrast remap data/series-high-contrast/1-5 (data-contrast=\\"high\\")"); s305-D41 form (declare as meant); ds-052 (the gate reads an instance dial as a spine token)',
        sc,'The two values exist so that a user can ask for MORE contrast: that is the caveat answered. Ledger edit only; no canon change.')

# 17 --mark mono: notifications inline warn #333333
sc={'as built: #333333 on #FFBB33 (mark, 2px)':comp('#333333','#FFBB33',2),
    'pick: #1A1A1A on #E0A61F (mark, 2px, s122-D2)':comp(INK,'#E0A61F',2)}
row(17,'--mark','mono','any','#1a1a1a vs #333333 (root v .inline.warn)','LEGACY INK IN MONO',
    'Re-point :where(.cn-notifications) .inline.warn --mark from #333333 to var(--mark-warning) (#1A1A1A). Lands with rows 3-4 in the same snippet edit. NOT tonight.',
    's122-D2 (mono mark #1A1A1A on all four statuses; 7.99:1 on amber); s176-D1 (#333333 is legacy\'s ink)',
    sc,'Both inks pass; the value is legacy\'s ink in a mono scope. Not a colour choice.')

# 18 --pressed mono: quick-actions #767676 v token #626262
sc={'as built: white on #767676 pressed tile (2px label)':comp(WHITE,'#767676',2),
    'pick: white on var(--tertiary-background-pressed) #626262 (2px label)':comp(WHITE,'#626262',2),
    'dark as built: white on #474747':comp(WHITE,'#474747',2),
    'dark token: white on #1A1A1A pressed':comp(WHITE,'#1A1A1A',2)}
row(18,'--pressed','mono','any','#626262 vs #767676 (list-items v quick-actions)','LEGACY GREY IN MONO',
    'Re-point .cn-quick-actions --pressed (light and dark) to var(--tertiary-background-pressed). White label contrast RISES (4.5 -> 6.1). NOT tonight.',
    's136-D1(A); s130-D6 (pressed charcoals come from each theme\'s OWN ramp; #767676 was legacy\'s escape clause, not mono\'s); the spine token --tertiary-background-pressed',
    sc,'Contrast was not why #767676 was chosen (it is the WEAKER of the two under a white label). Not a colour choice.')

# 19-20, 27-28 the disabled greys -> W-99 (s212-D1)
for n,prop,mode,a,b,who in ((19,'--disabled','any','#D7D8D6','#E1E1E1','.cn-badge hard-codes #D7D8D6; .cn-status-indicator reads var(--text-disabled)'),
                            (20,'--border-disabled','any','#E1E1E1','#D7D8D6','.cn-input-fields reads var(--form-border-disabled); .cn-dropdown hard-codes #D7D8D6'),
                            (27,'--text-disabled','any','#E1E1E1','#D7D8D6',':root #E1E1E1; .cn-dropdown hard-codes #D7D8D6'),
                            (28,'--text-disabled','dark','#808080','#767676',':root dark #808080; .cn-dropdown dark hard-codes #767676')):
    page = WHITE if mode=='any' else DARKPAGE
    sc={a+' on page (2px)':comp(a,page,2), b+' on page (2px)':comp(b,page,2), 's212-D1 pick #9D9D9D on page (2px)':comp('#9D9D9D',page,2)}
    row(n,prop,'mono',mode,a.lower()+' vs '+b.lower(),'DISABLED GREY (W-99)',
        'Re-point the hard-coded side to the spine token ('+('var(--text-disabled)' if prop!='--border-disabled' else 'var(--form-border-disabled)')+'). The token\'s VALUE is not this lane\'s: s212-D1 picked #9D9D9D and its enactment is W-99 (text-disabled and border-disabled in the same pass). NOT tonight.',
        's212-D1 (recessive disabled grey #9D9D9D; --text-disabled fixed in the SAME pass as --border-disabled; light+dark pairing UNRULED); W-99; s136-D1(A)',
        sc,who+'. Neither hex was chosen for contrast (both are decorative-disabled and under 1.5:1). The one open colour question here is s212-D1\'s dark twin, already Dave\'s under W-99, not a new one.')

# 21-23 the tints
for n,prop,a,b,tok in ((21,'--err-t','#F9F2F3','#FDD9D4','var(--rag-error-tint)'),(22,'--info-t','#EBEFF4','#DFEAF9','var(--rag-information-tint)'),(23,'--warn-t','#FFF8EA','#F6E6C0','var(--rag-warning-tint)')):
    sc={'ink #1A1A1A on notifications tint '+a+' (2px)':comp(INK,a,2),'ink #1A1A1A on spine tint '+b+' (2px)':comp(INK,b,2),
        'tint '+a+' on white page (40px)':comp(a,WHITE,40),'tint '+b+' on white page (40px)':comp(b,WHITE,40)}
    row(n,prop,'mono','any',a.lower()+' vs '+b.lower()+' (notifications v alert)','LEGACY TINT IN MONO',
        'Re-point .cn-notifications '+prop+' (light and its hard-coded dark twin) to '+tok+'. '+('Lands with the --err answer (W-308ia), same snippet.' if prop=='--err-t' else 'Lands with rows 3-6, same snippet edit.')+' NOT tonight.',
        's134-D4 (mono tint shells carry #1A1A1A glyph ink, the s122-D2 pastels); s123-D3 (mono tints are the spine\'s tuned values); s136-D1(A)',
        sc,'Ink passes on both by a mile (>13:1). The legacy tints are paler, so the mono tint is the more visible shell on white: a legibility gain, not a loss. Not a colour choice.')

# 24-25 --surface supercharge dark ; 26 --panel
sc={'account-card tile #13110E on page #25211C (40px)':comp('#13110E','#25211C',40),'headers section #25211C on page #25211C (40px)':comp('#25211C','#25211C',40),
    'SC dark text #F7F6F4 on #13110E (2px)':comp('#F7F6F4','#13110E',2),'SC dark text #F7F6F4 on #25211C (2px)':comp('#F7F6F4','#25211C',2)}
row(24,'--surface','supercharge','dark','#2a2621 vs #2e2a25 (the #221 pair no longer exists)','NAME COLLISION (values moved)',
    'No colour moves. Today the pair is .cn-account-card #13110E (the tile, s310-D4) v .cn-headers #25211C (the section, s311-D2): two components whose local --surface aliases two different ruled paths (surface/raised v surface/subtle). W-59 rename class.',
    's310-D4 (SC tiles #13110E); s311-D2 (SC dark page and section warm/4 #25211C); s178-D1(a); W-59',
    sc,'Both values are this week\'s rulings. Not a colour choice.')
row(25,'--surface','supercharge','dark','#2a2621 vs #1a1a1a (the #221 second pair)','GONE',
    'Nothing to settle: the #1A1A1A side was the generator locking background/default after its light half, fixed by s311-D2 (2026-09-30). The gate no longer measures it.',
    's311-D2', {}, 'Resolved by a ruling already enacted.')
rows[-1]['live']=None  # the gate measures row 24's pair under this key, not this one
sc={'multi-column panel #13110E on page #25211C (40px)':comp('#13110E','#25211C',40),'nav-rail panel #25211C on page #25211C (40px)':comp('#25211C','#25211C',40)}
row(26,'--panel','supercharge','dark','#2a2621 vs #1a1a1a (multi-column v nav-rail)','DECLARED (stands)',
    'Stands DECLARED-s215 in the ledger; only the values moved with s310-D4/s311-D2 (tile #13110E, page #25211C). Refresh the ledger row\'s first_evidence text when the ledger is next touched.',
    '_TOKEN-FORK-LEDGER.json --panel DECLARED-s215 ("two app shells legitimately paint different panel grounds in supercharge dark"); s310-D4; s311-D2',
    sc,'Not a colour choice.')

# 29 --ter-border supercharge: pure black token -> QUESTION
sc={'action-bar border #000000 on SC page #F7F6F4 (1px)':comp('#000000','#F7F6F4',1),'button border #13110E on SC page #F7F6F4 (1px)':comp('#13110E','#F7F6F4',1),
    'mono spine --tertiary-border-default #000000 on white (1px)':comp('#000000',WHITE,1),'mono ink #1A1A1A on white (1px)':comp(INK,WHITE,1)}
row(29,'--ter-border','supercharge','any','#000000 vs #13110e (action-bar v button)','QUESTION',
    'QUESTION for Dave. The SPINE token tertiary/border/default is pure black #000000 in Supercharge AND in Mono (canon.css:387, :26864); the SC button override alone paints the theme darkest #13110E. Does the ink rule (never pure black, halation) reach the outline border? If yes the token moves to each theme\'s darkest; if no the button override is the fork and returns to the token.',
    's176-D1 (blackest ink that is not pure black, per theme: SC #13110E, mono #1A1A1A) rules INK, not borders; s136-D1(A); notes/_subreports/2026-08-27-221-laneB.md section 9 item 2 flagged it for his eye',
    sc,'A real colour choice with a rule that stops one short of it. Measurement cannot settle it: a 1px dark line on a light ground blooms the same either way (the model is one-sided, bright feature on dark).',True)

rows.sort(key=lambda r:r['n'])

# --- forks measured today that were NOT among the 29 ---
new_since_221=[
 dict(prop='--ink',theme='common',mode='any',live=live_pair('--ink','common','any'),cls='NAME COLLISION',
      pick='Same as row 7: common is legacy\'s alias (the theme arrived after #221). W-59 class.',rule='s131-D1; s176-D1; W-59'),
 dict(prop='--surface',theme='mono',mode='dark',live=live_pair('--surface','mono','dark'),cls='HARD-CODED (B7 loose end)',
      pick='Template-error dark --surface #1F1F1F v the s310-D3 tile #000000: lane B7\'s named loose end ("Template-error\'s hard-coded --surface:#1F1F1F in dark"). Re-point to var(--tertiary-background-default).',rule='s310-D3; job B brief, loose ends lane B7'),
]

out={'$id':'FORKS-29-B5-2026-10-01','$lane':'#311 overnight wave 1, lane B5 (Fable), W-308ib',
     '$frame':'the 29 = bucket A (23) + bucket A2 (6) of notes/_subreports/2026-08-27-221-laneB.md section 9, re-measured at HEAD',
     '$measured':meas['summary'],'$scores':'reviews/_rag_bloom_model.py v0 (relative; bloom 100 = 40px white fill on #1A1A1A, dance 100 = saturated blue 1px text on #1A1A1A); wcag = flat ratio',
     'rows':rows,'new_since_221':new_since_221}
args=sys.argv[1:]
if '--json' in args: json.dump(out,open(args[args.index('--json')+1],'w'),indent=1,ensure_ascii=False)
if '--html' in args:
    def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    h=['<table class="forks-29"><thead><tr><th>#</th><th>token · theme · mode</th><th>at #221</th><th>class</th><th>pick</th><th>rule cited</th><th>contrast · bloom · dance</th><th>note</th></tr></thead><tbody>']
    for r in rows:
        sc='<br>'.join(f'{esc(k)}: <b>{v[0]}:1</b> · bloom {v[1]} · dance {v[2]}' for k,v in r['scores'].items()) or '—'
        cls=('<b>'+esc(r['cls'])+'</b>') if r['to_dave'] else esc(r['cls'])
        h.append(f'<tr class="{"to-dave" if r["to_dave"] else ""}"><td>{r["n"]}</td><td><code>{esc(r["prop"])}</code> · {esc(r["theme"])} · {esc(r["mode"])}</td><td>{esc(r["at_221"])}</td><td>{cls}</td><td>{esc(r["pick"])}</td><td>{esc(r["rule"])}</td><td>{sc}</td><td>{esc(r["note"])}</td></tr>')
    h.append('</tbody></table>')
    open(args[args.index('--html')+1],'w').write('\n'.join(h)+'\n')
from collections import Counter
c=Counter(r['cls'] for r in rows)
print('rows',len(rows),'to_dave',sum(r['to_dave'] for r in rows)); print(dict(c))
for r in rows: print(r['n'],r['prop'],r['theme'],r['mode'],'|',r['cls'],'|',('LIVE' if r['live'] else 'not measured today'))
for r in rows:
    for k,v in r['scores'].items(): print(f"  {r['n']:>2} {k[:72]:72} {v[0]:>6} {v[1]:>6} {v[2]:>6}")
